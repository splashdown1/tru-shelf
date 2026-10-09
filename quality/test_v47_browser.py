from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from playwright.sync_api import sync_playwright
from test_v45_browser import run as run_reader_regressions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = PROJECT_ROOT / "test-candidates" / "v47" / "TRU-v47.html"
PORTAL_URL = "https://splashdown1.github.io/tru-shelf/portal/"


def verify_new_tab(page, link, label: str) -> None:
    if link.get_attribute("href") != PORTAL_URL:
        raise AssertionError(f"{label} does not point to the public family index")
    if link.get_attribute("target") != "_blank":
        raise AssertionError(f"{label} must open a new tab")
    rel = set((link.get_attribute("rel") or "").split())
    if not {"noopener", "noreferrer"}.issubset(rel):
        raise AssertionError(f"{label} must prevent access to its opener")


def run_portal_links(target: Path) -> None:
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
            if not page.evaluate("window.__TRU_V47_NEW_TAB_PORTAL__ === true"):
                raise AssertionError("v47 build marker is missing")
            start_url = target.resolve().as_uri()
            gold_link = page.locator("[data-tru-portal]")
            verify_new_tab(page, gold_link, "gold portal control")
            if gold_link.get_attribute("aria-label") != "Open the TRU Portal index in a new tab; the reader stays open":
                raise AssertionError("gold portal accessible name does not describe its new-tab behaviour")
            help_result = page.evaluate("window.route('help')")
            expected_help = "the gold ◈ TRU Portal opens the full searchable family index in a new tab; the reader stays open."
            if help_result.get("portal_action") != "open" or expected_help not in help_result.get("reply", ""):
                raise AssertionError("in-reader help copy does not describe new-tab navigation")
            panel_link = page.locator("#tru-portal-panel a")
            page.evaluate("document.getElementById('tru-portal-panel').style.display='block'")
            if panel_link.count() != 1 or "TRU INDEX" not in panel_link.inner_text():
                raise AssertionError("status panel directory link is missing")
            verify_new_tab(page, panel_link, "status panel link")
            for link, label in ((gold_link, "gold portal control"), (panel_link, "status panel link")):
                with page.expect_popup(timeout=15000) as popup_info:
                    link.click()
                popup = popup_info.value
                popup.wait_for_load_state("domcontentloaded", timeout=15000)
                if popup.url != PORTAL_URL or popup.title() != "TRU Portal test":
                    raise AssertionError(f"{label} opened the wrong destination: {popup.url!r}")
                if page.url != start_url or page.locator("[data-tru-portal]").count() != 1:
                    raise AssertionError(f"{label} replaced or closed the reader tab")
                popup.close()
            if console_errors or page_errors:
                raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v47 reader and new-tab portal regressions")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    target = parser.parse_args().html
    if not target.is_file():
        raise SystemExit(f"candidate is missing: {target}")
    run_reader_regressions(target)
    run_portal_links(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"V47_BROWSER_SMOKE_OK inherited_reader_checks=15 gold_portal=new-tab reader-stays-open status_link=new-tab console=clean sha256={digest}")


if __name__ == "__main__":
    main()
