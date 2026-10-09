from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = PROJECT_ROOT / "test-candidates" / "v43" / "TRU-v43.html"
CASES = [
    ("what does TRU mean?", "Text-Rooted Understanding", "TRU_CORE"),
    ("what does T.R.U. stand for?", "Text-Rooted Understanding", "TRU_CORE"),
    ("define Graces", "G5485", "DEFINE"),
    ("define churches", "G1577", "DEFINE"),
    ("h1323", "a daughter", "DEFINE"),
    ("h8598", "an apple", "DEFINE"),
    ("g932", "properly, royalty", "DEFINE"),
    ("faith without works", "James 2:17", "TRUTH"),
    ("john 3:16", "John 3:16", "SCRIPTURE"),
]


def run(target: Path) -> None:
    console_errors = []
    page_errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        page = browser.new_page()
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        try:
            page.goto(target.resolve().as_uri(), wait_until="load", timeout=120000)
            page.wait_for_function("document.querySelector('#status')?.textContent.includes('READY')", timeout=120000)
            status = page.locator("#status").inner_text().lower()
            if "offline" not in status and "air-gapped" not in status:
                raise AssertionError(f"runtime is not offline: {status}")
            input_selector = "#askInput" if page.locator("#askInput").count() else "#input"
            send_selector = "#askBtn" if page.locator("#askBtn").count() else "#send"
            if not page.locator(input_selector).count() or not page.locator(send_selector).count():
                raise AssertionError("ask controls are missing")
            answers = page.locator("#chat .msg:has(.vd)")
            for query, fragment, verdict in CASES:
                before = answers.count()
                page.fill(input_selector, query)
                page.locator(send_selector).click()
                page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
                answer = answers.last.inner_text()
                if not answer.startswith(verdict) or fragment.lower() not in answer.lower():
                    raise AssertionError(f"{query}: expected {verdict} and {fragment!r}; got {answer[:500]!r}")
                if "internal fault" in answer.lower():
                    raise AssertionError(f"{query}: runtime fault: {answer[:500]}")
            if console_errors or page_errors:
                raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    target = parser.parse_args().html
    if not target.is_file():
        raise SystemExit(f"candidate is missing: {target}")
    run(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"V43_BROWSER_SMOKE_OK cases={len(CASES)} mode=OFFLINE console=clean sha256={digest}")


if __name__ == "__main__":
    main()
