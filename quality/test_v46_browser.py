from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from playwright.sync_api import sync_playwright
from test_v45_browser import run as run_reader_regressions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = PROJECT_ROOT / "test-candidates" / "v46" / "TRU-v46.html"
PORTAL_URL = "https://splashdown1.github.io/tru-shelf/portal/"


def run_portal_link(target: Path) -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        page = browser.new_page()
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.context.route(PORTAL_URL, lambda route: route.fulfill(status=200, body="<!doctype html><title>TRU Portal test</title>", content_type="text/html"))
        try:
            page.goto(target.resolve().as_uri(), wait_until="load", timeout=120000)
            if not page.evaluate("window.__TRU_V46_PORTAL_INDEX__ === true"):
                raise AssertionError("v46 build marker is missing")
            link = page.locator("[data-tru-portal]")
            if link.get_attribute("href") != PORTAL_URL or link.get_attribute("target") is not None:
                raise AssertionError("gold portal must open the public index in the same tab")
            if link.get_attribute("aria-label") != "Open the TRU Portal index in this tab":
                raise AssertionError("gold portal accessible name does not describe its destination")
            help_result = page.evaluate("window.route('help')")
            expected_help = "the gold ◈ TRU Portal opens the full searchable family index; use browser Back to return."
            if help_result.get("portal_action") != "open" or expected_help not in help_result.get("reply", ""):
                raise AssertionError("in-reader help copy does not describe same-tab navigation")
            panel_link = page.locator("#tru-portal-panel a")
            if panel_link.get_attribute("href") != PORTAL_URL or panel_link.get_attribute("target") is not None or "TRU INDEX" not in panel_link.inner_text():
                raise AssertionError("the in-reader status panel must retain a same-tab index link")
            link.click()
            if page.url != PORTAL_URL or page.title() != "TRU Portal test":
                raise AssertionError(f"gold portal did not navigate this tab to the index: {page.url}")
            page.go_back(wait_until="load", timeout=120000)
            if page.url != target.resolve().as_uri() or page.locator("[data-tru-portal]").count() != 1:
                raise AssertionError("browser Back did not return from the index to the reader")
            if console_errors or page_errors:
                raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v46 reader and gold-portal navigation regressions")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    target = parser.parse_args().html
    if not target.is_file():
        raise SystemExit(f"candidate is missing: {target}")
    run_reader_regressions(target)
    run_portal_link(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"V46_BROWSER_SMOKE_OK inherited_reader_checks=15 gold_portal=same-tab/back-works help_copy=correct status_link=present console=clean sha256={digest}")


if __name__ == "__main__":
    main()
