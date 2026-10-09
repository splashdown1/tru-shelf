from __future__ import annotations

from pathlib import Path

import test_v46_capacity

PROJECT_ROOT = Path(__file__).resolve().parents[1]
test_v46_capacity.HTML_PATH = PROJECT_ROOT / "test-candidates" / "v47" / "TRU-v47.html"


def main() -> int:
    target = test_v46_capacity.HTML_PATH
    if not target.is_file():
        raise SystemExit(f"Candidate not found: {target}")
    result = test_v46_capacity.run_browser()
    if result.get("entries") != 500 or not result.get("refusalVerified") or not result.get("updateVerified"):
        raise SystemExit(f"V47 teaching-capacity test failed: {result}")
    print("V47_CAPACITY_OK: 500 distinct Scripture Q&As are accepted")
    print("PASS a 501st distinct entry is refused")
    print("PASS an existing entry remains updateable at capacity")
    print("PASS the prior browser overlay was restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
