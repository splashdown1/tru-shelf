from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILMS = ["Shadow Ranch", "Camille", "The Lost World", "The General", "Speedy", "The Bat", "Greed"]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def expect_new_tab(page, link, url: str, title: str, label: str) -> None:
    if link.count() != 1:
        raise AssertionError(f"{label} must appear once")
    if link.get_attribute("target") != "_blank":
        raise AssertionError(f"{label} must open in a new tab")
    rel = set((link.get_attribute("rel") or "").split())
    if not {"noopener", "noreferrer"}.issubset(rel):
        raise AssertionError(f"{label} must safely detach the new tab")
    source_url = page.url
    with page.expect_popup(timeout=15000) as popup_info:
        link.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded", timeout=15000)
    if popup.url != url or title not in popup.title():
        raise AssertionError(f"{label} opened the wrong destination: {popup.url!r} {popup.title()!r}")
    if page.url != source_url:
        raise AssertionError(f"{label} replaced the original tab")
    popup.close()


def main() -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(PROJECT_ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            page = browser.new_page()
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.context.route("https://archive.org/embed/**", lambda route: route.abort())
            try:
                page.goto(f"{base_url}/portal/", wait_until="load", timeout=120000)
                if page.title() != "TRU Portal — Master Index":
                    raise AssertionError(f"wrong page title: {page.title()!r}")
                subtitle = page.locator(".sub").inner_text()
                if "Text-Rooted Understanding" not in subtitle or "new tab" not in subtitle or "stays open" not in subtitle:
                    raise AssertionError("portal subtitle does not explain TRU and the new-tab behaviour")
                if page.locator('a[href^="#"][target]').count() != 0:
                    raise AssertionError("section links must stay in the portal tab")
                if page.locator('nav a[href="../"][target]').count() != 0 or page.locator('footer a[href="../"][target]').count() != 0:
                    raise AssertionError("return-to-shelf links must stay in the current tab")
                cards = page.locator(".index-card")
                card_count = cards.count()
                if card_count != 93:
                    raise AssertionError(f"expected 93 searchable entries including v47, found {card_count}")
                if page.locator('#current-versions .index-card').filter(has_text="TRU v47").count() != 1:
                    raise AssertionError("the v47 test candidate must appear in current versions")
                for title in FILMS:
                    if page.locator("#films-out .movie-card").filter(has_text=title).count() != 1:
                        raise AssertionError(f"film card missing or duplicated: {title}")
                if page.locator(".player iframe[src]").count() != 0:
                    raise AssertionError("video embeds must stay unloaded until selected")
                search = page.locator("#index-search")
                search.fill("v25")
                if page.locator("#older-versions-out .index-card:visible").filter(has_text="TRU v25").count() != 1:
                    raise AssertionError("type-to-search did not find the v25 reader")
                if "1 result" not in page.locator("#search-status").inner_text():
                    raise AssertionError("search status did not report the filtered result")
                search.fill("shelter")
                if page.locator("#lanes-out .index-card:visible").filter(has_text="Shelter").count() != 1:
                    raise AssertionError("type-to-search did not find the Shelter field door")
                search.fill("shadow ranch")
                film = page.locator("#films-out .movie-card:visible").filter(has_text="Shadow Ranch")
                if film.count() != 1:
                    raise AssertionError("type-to-search did not find the western")
                film.locator(".player summary").click()
                frame = film.locator("iframe")
                if frame.get_attribute("src") != "https://archive.org/embed/ShadowRanch1930-BuckJones?autoplay=0":
                    raise AssertionError("selected film did not load its Archive player")
                if page.locator("#engines").is_visible():
                    raise AssertionError("unmatched portal sections should be hidden during a filtered search")
                search.fill("")
                if page.locator("#current-versions .index-card:visible").filter(has_text="TRU v47").count() != 1 or page.locator("#older-versions").get_attribute("open") is not None:
                    raise AssertionError("clearing the search did not restore the default index view")
                lane_names = page.locator("#lanes-out .index-card .big").all_inner_texts()
                if "Synthetic Intelligence" not in lane_names or "AI" in lane_names:
                    raise AssertionError("the lane must display as Synthetic Intelligence, not AI")
                synthetic_url = "https://splashdown1.github.io/tru-ai/"
                sky_url = "https://splashdown1.github.io/tru-sky/"
                page.context.route(synthetic_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Synthetic Intelligence test</title>", content_type="text/html"))
                page.context.route(sky_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Sky test</title>", content_type="text/html"))
                synthetic_link = page.locator("#lanes-out .index-card").filter(has_text="Synthetic Intelligence").locator(f'a[href="{synthetic_url}"]').first
                expect_new_tab(page, synthetic_link, synthetic_url, "Synthetic Intelligence test", "Synthetic Intelligence lane")
                sky_link = page.locator("#lanes-out .index-card").filter(has_text="Sky").locator(f'a[href="{sky_url}"]').first
                expect_new_tab(page, sky_link, sky_url, "Sky test", "Sky field door")
                v47_preview = page.locator('#current-versions .index-card').filter(has_text="TRU v47").locator('a[href="../test-candidates/v47/"]')
                expect_new_tab(page, v47_preview, f"{base_url}/test-candidates/v47/", "TRU v47", "v47 preview")
                page.locator('nav a[href="../"]').click()
                if page.url != f"{base_url}/" or page.title() != "TRU SHELF":
                    raise AssertionError("TRU Shelf return link did not use the current tab")
                page.go_back(wait_until="load", timeout=120000)
                if page.url != f"{base_url}/portal/":
                    raise AssertionError("browser Back did not return from the shelf to the portal")
                page.set_viewport_size({"width": 390, "height": 844})
                if page.evaluate("document.documentElement.scrollWidth > innerWidth"):
                    raise AssertionError("portal index overflows horizontally on a phone-sized viewport")
                root = browser.new_page()
                root.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                root.on("pageerror", lambda error: page_errors.append(str(error)))
                root.goto(f"{base_url}/", wait_until="load", timeout=120000)
                root.context.route(sky_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Sky test</title>", content_type="text/html"))

                if "new tab" not in root.locator(".sub").inner_text() or "stays open" not in root.locator(".sub").inner_text():
                    raise AssertionError("shelf subtitle does not explain that the shelf stays open")
                local_portal_url = f"{base_url}/portal/"
                expect_new_tab(root, root.locator('a[href="portal/"]'), local_portal_url, "TRU Portal — Master Index", "shelf portal link")
                home_sky = root.locator(f'a[href="{sky_url}"]').first
                expect_new_tab(root, home_sky, sky_url, "Sky test", "shelf Sky lane")
                if console_errors or page_errors:
                    raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f"PORTAL_INDEX_OK cards={card_count} films={len(FILMS)} new-tab-app-links=passed in-tab-sections-and-return=passed live-search=passed lazy-embed=passed mobile=passed console=clean")


if __name__ == "__main__":
    main()
