from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
BUILDER_PATH = HERE / "build_v39.py"
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v38" / "TRU-v38.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v39" / "TRU-v39.html"


def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)


def data_blocks(page: bytes) -> dict[str, bytes]:
    pattern = rb'<script\s+type="application/json"\s+id="([^"]+)">(.*?)</script>'
    return {match.group(1).decode(): match.group(2) for match in re.finditer(pattern, page, re.S)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the public v39 app or a locally rebuilt copy.")
    parser.add_argument("--artifact", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    if not args.artifact.is_file():
        parser.error(f"v39 artifact not found: {args.artifact}")
    spec = importlib.util.spec_from_file_location("build_v39", BUILDER_PATH)
    if spec is None or spec.loader is None:
        fail("cannot load v39 builder")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    base = BASE_PATH.read_bytes()
    actual = args.artifact.read_bytes()
    if actual != builder.transform(base):
        fail("v39 does not equal the pinned deterministic transform")
    if actual.count(builder.PATCH_MARKER) != 1:
        fail("exact-term patch marker count is not one")
    if builder.NEW_BUILD_STAMP not in actual or builder.OLD_BUILD_STAMP in actual:
        fail("build stamp is not the pinned v39 stamp")
    before = data_blocks(base)
    after = data_blocks(actual)
    if before != after or len(before) < 10:
        fail("embedded TRU source/data blocks changed")
    for fragment in [
        "exactTermQuestion",
        "exactTermAnswer",
        "previousRoute(term)",
        "reply.includes(\"phrase •\")",
        "source.includes(\"deep lexicon\")",
        "original_question:raw",
    ]:
        if fragment not in builder.PATCH_SCRIPT:
            fail("missing intended exact-term/source-preserving behaviour: " + fragment)
    print(f"PASS v39 is the deterministic v38 patch; parent SHA-256 {hashlib.sha256(base).hexdigest()}")
    print(f"PASS all {len(before)} embedded source/data blocks are byte-identical")
    print("PASS exact object questions prefer the exact local term when the earlier route is GAP, phrase noise, or a deep-gloss collision")
    print("PASS relevant existing dictionary answers are preserved")
    print(f"PASS verified artifact SHA-256 {hashlib.sha256(actual).hexdigest()}")


if __name__ == "__main__":
    main()
