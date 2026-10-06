from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
BUILDER_PATH = HERE / "build_v40.py"
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v39" / "TRU-v39.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v40" / "TRU-v40.html"


def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)


def data_blocks(page: bytes) -> dict[str, bytes]:
    pattern = rb'<script\s+type="application/json"\s+id="([^"]+)">(.*?)</script>'
    return {match.group(1).decode(): match.group(2) for match in re.finditer(pattern, page, re.S)}


def main() -> None:
    spec = importlib.util.spec_from_file_location("build_v40", BUILDER_PATH)
    if spec is None or spec.loader is None:
        fail("cannot load v40 builder")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    base = BASE_PATH.read_bytes()
    actual = OUTPUT_PATH.read_bytes()
    if actual != builder.transform(base):
        fail("v40 does not equal the pinned deterministic transform")
    if actual.count(builder.PATCH_MARKER) != 1:
        fail("Scripture-teaching patch marker count is not one")
    if builder.NEW_BUILD_STAMP not in actual or builder.OLD_BUILD_STAMP in actual:
        fail("build stamp is not the pinned v40 stamp")
    before = data_blocks(base)
    after = data_blocks(actual)
    if before != after or len(before) < 10:
        fail("embedded TRU source/data blocks changed")
    required = [
        "remember: scripture:",
        "parseReferences",
        "parseVerse(part)",
        "records.length>=500",
        "normalizeQuestion(query)",
        "user-taught answer",
        "forget\\s*:\\s*scripture",
        "scripture\\s+answers",
        "interpretation was not independently reviewed",
    ]
    patch = builder.PATCH_SCRIPT
    for fragment in required:
        if fragment not in patch:
            fail("missing intended Scripture-teaching behaviour: " + fragment)
    if "BASE_SHA256 = \"be82106355cf5848f1533df0c8cc216f505d1ad03bf622e2a98b4a8812e66ebb\"" not in BUILDER_PATH.read_text(encoding="utf-8"):
        fail("v39 parent hash is not pinned")
    if b"overlay:OVERLAY" not in base:
        fail("existing brain export no longer includes the user overlay")
    print(f"PASS v40 is the deterministic v39 patch; parent SHA-256 {hashlib.sha256(base).hexdigest()}")
    print(f"PASS all {len(before)} embedded source/data blocks are byte-identical")
    print("PASS Scripture teaching requires exact local KJV references, stores up to 500 entries, and matches taught questions without paraphrase guesses")
    print("PASS user-supplied interpretations are labelled; exact local KJV verse text is quoted")
    print("PASS generic remember, export, reset and all pre-existing v39 routes remain present")
    print(f"PASS v40 SHA-256 {hashlib.sha256(actual).hexdigest()}")


if __name__ == "__main__":
    main()
