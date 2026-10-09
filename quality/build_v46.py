from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v45" / "TRU-v45.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v46" / "TRU-v46.html"
EXPECTED_BASE_SHA256 = "1cffce39f2ce605d52f0d2bc9b58c83acaa9bd1aeed7d04ae9eb10aec5d0b23c"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T10:48:03.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T13:26:00.000Z";'
OLD_TITLE = "<title>TRU v45 — Text-Rooted Understanding</title>".encode()
NEW_TITLE = "<title>TRU v46 — Text-Rooted Understanding</title>".encode()
PORTAL_URL = "https://splashdown1.github.io/tru-shelf/portal/"
PATCH_MARKER = b'<script id="tru-v46-gold-portal-index">window.__TRU_V46_PORTAL_INDEX__=true;</script>'
OLD_LINK = b'<a data-tru-portal href="#"'
NEW_LINK = f'<a data-tru-portal href="{PORTAL_URL}"'.encode()
OLD_HANDLER = '''  a.removeAttribute("href");a.style.cursor="pointer";
  a.addEventListener("click",function(ev){
    ev.preventDefault();
    var open=p.style.display!=="none";
    p.style.display=open?"none":"block";
    if(!open){
      try{document.getElementById("portal-stats").textContent=nodeCountSummary();}
      catch(e){document.getElementById("portal-stats").textContent="offline engine";var b=document.getElementById("badge");if(b)document.getElementById("portal-stats").textContent=b.textContent;}
      document.getElementById("portal-build").textContent="v34 • "+__TRU_BUILD__;
    }
  });'''.encode()
NEW_HANDLER = '  a.style.cursor="pointer";'.encode()
OLD_BUILD_LABEL = '"v34 • "+__TRU_BUILD__'.encode()
NEW_BUILD_LABEL = '"v46 • "+__TRU_BUILD__'.encode()
OLD_PORTAL_COPY = "The ◈ TRU Portal button shows build details.".encode()
NEW_PORTAL_COPY = "Ask about TRU for build details; the gold ◈ TRU Portal opens the full searchable family index; use browser Back to return.".encode()
OLD_PORTAL_LABEL = b'portal.title="TRU Portal: show lane, offline-runtime, source and build information.";portal.setAttribute("aria-label","Open TRU Portal status and build information");portal.setAttribute("role","button");portal.setAttribute("tabindex","0");portal.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();portal.click()}})'
NEW_PORTAL_LABEL = b'portal.title="Open the searchable TRU family index in this tab.";portal.setAttribute("aria-label","Open the TRU Portal index in this tab")'
PANEL_ANCHOR = b'<div style="color:#6b7f8a;font-size:10.5px;line-height:1.7">\nLANES'
PANEL_INSERT = b'<div style="margin-top:8px"><a href="' + PORTAL_URL.encode() + b'" style="color:#e8c96a;text-decoration:underline">OPEN THE FULL TRU INDEX \xe2\x86\x97</a></div>\n' + PANEL_ANCHOR


def replace_once(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{label} must appear exactly once; found {count}")
    return source.replace(old, new, 1)


def build(base: Path, output: Path, force: bool) -> str:
    source = base.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != EXPECTED_BASE_SHA256:
        raise SystemExit(f"pinned v45 base hash mismatch: expected {EXPECTED_BASE_SHA256}, found {digest}")
    if source.count(OLD_BUILD_STAMP) != 1 or source.count(OLD_TITLE) != 1:
        raise SystemExit("the v45 build stamp or title is missing or not unique")
    if source.count(OLD_LINK) != 1 or source.count(OLD_HANDLER) != 1:
        raise SystemExit("the gold portal link or old click handler is missing or not unique")
    if source.count(OLD_PORTAL_LABEL) != 1 or source.count(PANEL_ANCHOR) != 1:
        raise SystemExit("the portal accessibility label or panel link point is missing or not unique")
    if source.count(OLD_BUILD_LABEL) != 2 or source.count(OLD_PORTAL_COPY) != 1:
        raise SystemExit("the stale portal build labels or reply copy are missing or not unique")
    if PATCH_MARKER in source:
        raise SystemExit("the v46 patch is already present in the v45 base")
    if source.count(b"</body>") != 1:
        raise SystemExit("the body insertion point is missing or not unique")
    if output.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing candidate: {output}; pass --force to rebuild")
    candidate = source.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    candidate = candidate.replace(OLD_TITLE, NEW_TITLE, 1)
    candidate = replace_once(candidate, OLD_LINK, NEW_LINK, "gold portal link")
    candidate = replace_once(candidate, OLD_HANDLER, NEW_HANDLER, "gold portal click handler")
    candidate = replace_once(candidate, OLD_PORTAL_LABEL, NEW_PORTAL_LABEL, "portal accessibility label")
    candidate = candidate.replace(OLD_BUILD_LABEL, NEW_BUILD_LABEL)
    candidate = replace_once(candidate, OLD_PORTAL_COPY, NEW_PORTAL_COPY, "portal help copy")
    candidate = replace_once(candidate, PANEL_ANCHOR, PANEL_INSERT, "portal panel directory link")
    candidate = candidate.replace(b"</body>", PATCH_MARKER + b"\n</body>", 1)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(candidate)
    return hashlib.sha256(candidate).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned v46 TRU same-tab index-link candidate from v45")
    parser.add_argument("--base", type=Path, default=BASE_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    digest = build(args.base, args.output, args.force)
    print(f"built {args.output} sha256={digest} bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
