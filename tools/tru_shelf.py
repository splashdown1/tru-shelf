#!/usr/bin/env python3
"""TRU Shelf — propose / approve / check

Deterministic, offline, zero-dependency helper for shelf changes.
Nothing is applied automatically. A gap stays a gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_DIR = PROJECT_ROOT / "proposals"

# Paths we care about for shelf integrity (extend later if needed).
# Relative to PROJECT_ROOT.
TRACKED_PATHS = [
    "README.md",
    "index.html",
    "portal/index.html",
    "quality/index.html",
    "quality/README.md",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(text: str, max_len: int = 40) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-") or "change"


def collect_manifest() -> dict[str, str | None]:
    """Return {rel_path: sha256 or None} for every tracked path."""
    manifest: dict[str, str | None] = {}
    for rel in TRACKED_PATHS:
        full = PROJECT_ROOT / rel
        manifest[rel] = sha256_file(full)
    return manifest


def cmd_propose(description: str) -> int:
    if not description.strip():
        print("GAP: description is empty", file=sys.stderr)
        return 1

    now = utc_now()
    stamp = now.strftime("%Y-%m-%d-%H%M%S")
    slug = slugify(description)
    prop_dir = PROPOSALS_DIR / f"{stamp}-{slug}"

    if prop_dir.exists():
        print(f"GAP: proposal directory already exists: {prop_dir}", file=sys.stderr)
        return 1

    prop_dir.mkdir(parents=True, exist_ok=False)

    manifest = collect_manifest()
    (prop_dir / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    desc = (
        f"# Proposal\n\n"
        f"**Created:** {now.isoformat()}\n\n"
        f"**Description:**\n\n{description.strip()}\n\n"
        f"---\n\n"
        f"This proposal records the state of tracked shelf files at creation time.\n"
        f"It does not apply any change. Use `approve` then a deliberate apply step.\n"
    )
    (prop_dir / "DESCRIPTION.md").write_text(desc, encoding="utf-8")

    print(f"PROPOSED  {prop_dir.relative_to(PROJECT_ROOT)}")
    print(f"  files tracked: {len(manifest)}")
    missing = [p for p, h in manifest.items() if h is None]
    if missing:
        print(f"  GAP: missing at propose time: {', '.join(missing)}")
    return 0


def cmd_approve(proposal_path: str, note: str) -> int:
    prop = Path(proposal_path)
    if not prop.is_absolute():
        prop = PROJECT_ROOT / prop
    if not prop.is_dir():
        print(f"GAP: proposal directory not found: {prop}", file=sys.stderr)
        return 1

    approved = prop / "APPROVED.md"
    if approved.exists():
        print(f"GAP: already approved: {approved}", file=sys.stderr)
        return 1

    now = utc_now()
    body = (
        f"# Approved\n\n"
        f"**When:** {now.isoformat()}\n\n"
        f"**Note:**\n\n{note.strip() or '(no note)'}\n\n"
        f"---\n\n"
        f"Approval records human intent. It does not apply the change.\n"
    )
    approved.write_text(body, encoding="utf-8")
    print(f"APPROVED  {prop.relative_to(PROJECT_ROOT)}")
    return 0


def cmd_check(proposal_path: str) -> int:
    prop = Path(proposal_path)
    if not prop.is_absolute():
        prop = PROJECT_ROOT / prop
    if not prop.is_dir():
        print(f"GAP: proposal directory not found: {prop}", file=sys.stderr)
        return 1

    manifest_path = prop / "MANIFEST.json"
    if not manifest_path.is_file():
        print(f"GAP: MANIFEST.json missing in {prop}", file=sys.stderr)
        return 1

    try:
        recorded = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"GAP: MANIFEST.json is not valid JSON: {e}", file=sys.stderr)
        return 1

    current = collect_manifest()
    mismatches: list[str] = []
    missing_now: list[str] = []
    extra_recorded: list[str] = []

    for path, old_hash in recorded.items():
        new_hash = current.get(path)
        if new_hash is None:
            missing_now.append(path)
        elif old_hash is None and new_hash is not None:
            mismatches.append(f"{path}: was missing, now present")
        elif old_hash is not None and new_hash is None:
            mismatches.append(f"{path}: was present, now missing")
        elif old_hash != new_hash:
            mismatches.append(f"{path}: hash changed")

    for path in current:
        if path not in recorded:
            extra_recorded.append(path)  # should not happen with fixed TRACKED_PATHS

    approved = (prop / "APPROVED.md").is_file()

    print(f"CHECK  {prop.relative_to(PROJECT_ROOT)}")
    print(f"  approved: {'yes' if approved else 'no'}")

    if not mismatches and not missing_now:
        print("  status: PASS — live tree matches the proposal snapshot")
        return 0

    print("  status: FAIL")
    for m in mismatches:
        print(f"    mismatch: {m}")
    for m in missing_now:
        print(f"    missing now: {m}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="TRU Shelf propose / approve / check (no auto-apply)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_propose = sub.add_parser("propose", help="Create a new proposal snapshot")
    p_propose.add_argument("description", help="Short human description of the change")

    p_approve = sub.add_parser("approve", help="Record human approval (does not apply)")
    p_approve.add_argument("proposal", help="Path to the proposal directory")
    p_approve.add_argument("note", nargs="?", default="", help="Optional approval note")

    p_check = sub.add_parser("check", help="Verify proposal still matches live tree")
    p_check.add_argument("proposal", help="Path to the proposal directory")

    args = parser.parse_args()

    if args.command == "propose":
        return cmd_propose(args.description)
    if args.command == "approve":
        return cmd_approve(args.proposal, args.note)
    if args.command == "check":
        return cmd_check(args.proposal)

    print("GAP: unknown command", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
