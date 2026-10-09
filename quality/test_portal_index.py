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
                if page.locator('a[target="_blank"]').count() != 0:
                    raise AssertionError("portal links must stay in the current tab so browser Back works")
                if "Text-Rooted Understanding" not in page.locator(".sub").inner_text():
                    raise AssertionError("portal subtitle does not define TRU")
                cards = page.locator(".index-card")
                card_count = cards.count()
                if card_count != 92:
                    raise AssertionError(f"expected 92 searchable entries, found {card_count}")
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
                if page.locator("#current-versions .index-card:visible").filter(has_text="TRU v46").count() != 1 or page.locator("#older-versions").get_attribute("open") is not None:
                    raise AssertionError("clearing the search did not restore the default index view")
                lane_names = page.locator("#lanes-out .index-card .big").all_inner_texts()
                if "Synthetic Intelligence" not in lane_names or "AI" in lane_names:
                    raise AssertionError("the AI lane must display as Synthetic Intelligence")
                synthetic_url = "https://splashdown1.github.io/tru-ai/"
                page.context.route(synthetic_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Synthetic Intelligence test</title>", content_type="text/html"))
                synthetic_link = page.locator("#lanes-out .index-card").filter(has_text="Synthetic Intelligence").locator(f'a[href="{synthetic_url}"]').first
                if synthetic_link.count() != 1 or synthetic_link.get_attribute("target") is not None:
                    raise AssertionError("the Synthetic Intelligence lane must stay in the portal tab")
                synthetic_link.click()
                if page.url != synthetic_url or page.title() != "Synthetic Intelligence test":
                    raise AssertionError("the Synthetic Intelligence lane did not navigate in the current tab")
                page.go_back(wait_until="load", timeout=120000)
                if page.url != f"{base_url}/portal/":
                    raise AssertionError("browser Back did not return from Synthetic Intelligence to the portal")
                page.set_viewport_size({"width": 390, "height": 844})
                if page.evaluate("document.documentElement.scrollWidth > innerWidth"):
                    raise AssertionError("portal index overflows horizontally on a phone-sized viewport")
                synthetic_url = "https://splashdown1.github.io/tru-ai/"
                page.context.route(synthetic_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Synthetic Intelligence test</title>", content_type="text/html"))
                synthetic_card = page.locator("#lanes-out .index-card").filter(has_text="Synthetic Intelligence")
                synthetic_link = synthetic_card.locator(f'a[href="{synthetic_url}"]')
                if synthetic_card.count() != 1 or synthetic_link.count() != 1 or synthetic_link.get_attribute("target") is not None:
                    raise AssertionError("Synthetic Intelligence must be visibly named and open in the current tab")
                synthetic_link.click()
                if page.url != synthetic_url or page.title() != "Synthetic Intelligence test":
                    raise AssertionError("Synthetic Intelligence lane navigation did not use the current tab")
                page.go_back(wait_until="load", timeout=120000)
                if page.url != f"{base_url}/portal/":
                    raise AssertionError("browser Back did not return from Synthetic Intelligence to the portal")
                sky_url = "https://splashdown1.github.io/tru-sky/"
                page.context.route(sky_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Sky test</title>", content_type="text/html"))
                sky_link = page.locator("#lanes-out .index-card").filter(has_text="Sky").locator(f'a[href="{sky_url}"]').first
                if sky_link.count() != 1 or sky_link.get_attribute("target") is not None:
                    raise AssertionError("the Sky field-door link must stay in the portal tab")
                sky_link.click()
                if page.url != sky_url or page.title() != "Sky test":
                    raise AssertionError("portal lane navigation did not use the current tab")
                page.go_back(wait_until="load", timeout=120000)
                if page.url != f"{base_url}/portal/":
                    raise AssertionError("browser Back did not return from a lane to the portal")
                root = browser.new_page()
                root.context.route(sky_url, lambda route: route.fulfill(status=200, body="<!doctype html><title>Sky test</title>", content_type="text/html"))
                root.goto(f"{base_url}/", wait_until="load", timeout=120000)
                portal_link = root.locator('a[href="portal/"]')
                if portal_link.count() != 1 or portal_link.get_attribute("target") is not None:
                    raise AssertionError("TRU Shelf home page must open the family index in the current tab")
                portal_link.click()
                if root.url != f"{base_url}/portal/" or root.title() != "TRU Portal — Master Index":
                    raise AssertionError("TRU Shelf portal navigation did not use the current tab")
                root.go_back(wait_until="load", timeout=120000)
                if root.url != f"{base_url}/":
                    raise AssertionError("browser Back did not return from the portal to TRU Shelf")
                home_sky = root.locator(f'a[href="{sky_url}"]').first
                if home_sky.count() != 1 or home_sky.get_attribute("target") is not None:
                    raise AssertionError("TRU Shelf field-door links must stay in the current tab")
                home_sky.click()
                if root.url != sky_url or root.title() != "Sky test":
                    raise AssertionError("TRU Shelf lane navigation did not use the current tab")
                root.go_back(wait_until="load", timeout=120000)
                if root.url != f"{base_url}/":
                    raise AssertionError("browser Back did not return from a lane to TRU Shelf")
                root.close()
                if console_errors or page_errors:
                    raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f"PORTAL_INDEX_OK cards={card_count} films={len(FILMS)} live-search=passed lazy-embed=passed mobile=passed all-routes=same-tab/back-works console=clean")


if __name__ == "__main__":
    main()
