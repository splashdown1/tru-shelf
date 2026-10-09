from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v46" / "TRU-v46.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v47" / "TRU-v47.html"
EXPECTED_BASE_SHA256 = "3a06dee754ca16e03ac88df1a1256c61c6b9fd40aa0d819b246cee99a796197b"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T13:26:00.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T13:51:24.000Z";'
OLD_TITLE = "<title>TRU v46 — Text-Rooted Understanding</title>".encode()
NEW_TITLE = "<title>TRU v47 — Text-Rooted Understanding</title>".encode()
PORTAL_URL = "https://splashdown1.github.io/tru-shelf/portal/"
OLD_GOLD_LINK = f'<a data-tru-portal href="{PORTAL_URL}" style='.encode()
NEW_GOLD_LINK = f'<a data-tru-portal href="{PORTAL_URL}" target="_blank" rel="noopener noreferrer" style='.encode()
OLD_PANEL_LINK = f'<a href="{PORTAL_URL}" style='.encode()
NEW_PANEL_LINK = f'<a href="{PORTAL_URL}" target="_blank" rel="noopener noreferrer" style='.encode()
OLD_BUILD_LABEL = '"v46 • "+__TRU_BUILD__'.encode()
NEW_BUILD_LABEL = '"v47 • "+__TRU_BUILD__'.encode()
OLD_PORTAL_LABEL = b'portal.title="Open the searchable TRU family index in this tab.";portal.setAttribute("aria-label","Open the TRU Portal index in this tab")'
NEW_PORTAL_LABEL = b'portal.title="Open the searchable TRU family index in a new tab; this reader stays open.";portal.setAttribute("aria-label","Open the TRU Portal index in a new tab; the reader stays open")'
OLD_PORTAL_COPY = "the gold ◈ TRU Portal opens the full searchable family index; use browser Back to return.".encode()
NEW_PORTAL_COPY = "the gold ◈ TRU Portal opens the full searchable family index in a new tab; the reader stays open.".encode()
PATCH_MARKER = b'<script id="tru-v47-new-tab-portal">window.__TRU_V47_NEW_TAB_PORTAL__=true;</script>'


def replace_once(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{label} must appear exactly once; found {count}")
    return source.replace(old, new, 1)


def build(base: Path, output: Path, force: bool) -> str:
    source = base.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != EXPECTED_BASE_SHA256:
        raise SystemExit(f"pinned v46 base hash mismatch: expected {EXPECTED_BASE_SHA256}, found {digest}")
    if source.count(OLD_BUILD_STAMP) != 1 or source.count(OLD_TITLE) != 1:
        raise SystemExit("the pinned v46 build stamp or title is missing or not unique")
    if source.count(OLD_GOLD_LINK) != 1 or source.count(OLD_PANEL_LINK) != 1:
        raise SystemExit("the gold portal link or status-panel link is missing or not unique")
    if source.count(OLD_BUILD_LABEL) != 1 or source.count(OLD_PORTAL_LABEL) != 1 or source.count(OLD_PORTAL_COPY) != 1:
        raise SystemExit("the v46 label or same-tab portal text is missing or not unique")
    if PATCH_MARKER in source:
        raise SystemExit("the v47 patch is already present in the v46 base")
    if source.count(b"</body>") != 1:
        raise SystemExit("the body insertion point is missing or not unique")
    if output.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing candidate: {output}; pass --force to rebuild")
    candidate = source.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    candidate = replace_once(candidate, OLD_TITLE, NEW_TITLE, "document title")
    candidate = replace_once(candidate, OLD_GOLD_LINK, NEW_GOLD_LINK, "gold portal link")
    candidate = replace_once(candidate, OLD_PANEL_LINK, NEW_PANEL_LINK, "status panel link")
    candidate = replace_once(candidate, OLD_BUILD_LABEL, NEW_BUILD_LABEL, "portal build label")
    candidate = replace_once(candidate, OLD_PORTAL_LABEL, NEW_PORTAL_LABEL, "portal accessible label")
    candidate = replace_once(candidate, OLD_PORTAL_COPY, NEW_PORTAL_COPY, "portal help copy")
    candidate = candidate.replace(b"</body>", PATCH_MARKER + b"\n</body>", 1)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(candidate)
    return hashlib.sha256(candidate).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned v47 TRU new-tab portal candidate from v46")
    parser.add_argument("--base", type=Path, default=BASE_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    digest = build(args.base, args.output, args.force)
    print(f"built {args.output} sha256={digest} bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
