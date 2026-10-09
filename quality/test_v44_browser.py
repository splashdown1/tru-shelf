from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = PROJECT_ROOT / "test-candidates" / "v44" / "TRU-v44.html"
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
            result = page.evaluate("""() => {
              const firstGap = window.route("nonsense query");
              const secondGap = window.route("zzzx qqqq");
              const personal = window.route("are you saved?");
              const index = personal.sugContinuation ? window.route(personal.sugContinuation.query) : null;
              const heaven = window.route("where is heaven?");
              const unmatchedIndex = window.route("word index: zzzzx");
              const originalVoiceList = window.readerVoiceList;
              window.setReaderGender("female");
              window.readerVoiceList = () => [{name:"Local English Voice",lang:"en-US",localService:true,voiceURI:"local"}];
              const voiceFirst = window.readerVoiceStatus();
              const voiceSecond = window.readerVoiceStatus();
              window.readerVoiceList = originalVoiceList;
              return {firstGap,secondGap,personal,index,heaven,unmatchedIndex,voiceFirst,voiceSecond};
            }""")
            if result["firstGap"]["verdict"] != "GAP" or "Try a verse" not in result["firstGap"]["reply"]:
                raise AssertionError(f"first GAP guidance changed unexpectedly: {result['firstGap']!r}")
            if result["secondGap"]["verdict"] != "GAP" or "No supported match" not in result["secondGap"]["reply"] or "Try a verse" in result["secondGap"]["reply"]:
                raise AssertionError(f"repeated GAP guidance was not shortened: {result['secondGap']!r}")
            personal = result["personal"]
            suggestion = personal.get("sugContinuation") or {}
            if personal.get("verdict") != "GAP" or suggestion.get("query") != "word index: saved" or "saved" not in suggestion.get("label", "").lower():
                raise AssertionError(f"personal-status question must stay a GAP and offer a verified word-index follow-up: {personal!r}")
            indexed = result["index"]
            if not indexed or indexed.get("verdict") != "DEFINE" or indexed.get("bible_word_index") is not True or indexed.get("word") != "saved" or "107 times" not in indexed.get("reply", ""):
                raise AssertionError(f"saved word-index follow-up failed: {indexed!r}")
            if not result["heaven"].get("sugContinuation"):
                raise AssertionError(f"existing topic suggestion was lost: {result['heaven']!r}")
            if result["unmatchedIndex"].get("verdict") != "GAP":
                raise AssertionError(f"unknown word-index command must remain a GAP: {result['unmatchedIndex']!r}")
            if not result["voiceFirst"].startswith("No recognizable female voice listed"):
                raise AssertionError(f"first voice mismatch notice changed unexpectedly: {result['voiceFirst']!r}")
            if not result["voiceSecond"].startswith("Using local voice") or "Choose a named voice" in result["voiceSecond"]:
                raise AssertionError(f"repeated voice mismatch notice was not condensed: {result['voiceSecond']!r}")
            before = answers.count()
            page.fill(input_selector, "are you saved?")
            page.locator(send_selector).click()
            page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
            gap_card = answers.last
            gap_text = gap_card.inner_text()
            follow_up = gap_card.locator("button.next-action")
            if not gap_text.startswith("GAP") or follow_up.count() != 1 or "saved" not in follow_up.inner_text().lower():
                raise AssertionError(f"the personal-status GAP did not render its saved-word follow-up: {gap_text!r}")
            before = answers.count()
            follow_up.click()
            page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
            follow_up_text = answers.last.inner_text()
            if not follow_up_text.startswith("DEFINE") or "107 times" not in follow_up_text:
                raise AssertionError(f"the rendered word-index follow-up failed: {follow_up_text[:500]!r}")
            if console_errors or page_errors:
                raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v44 offline and regression smoke checks")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    target = parser.parse_args().html
    if not target.is_file():
        raise SystemExit(f"candidate is missing: {target}")
    run(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"V44_BROWSER_SMOKE_OK cases={len(CASES)} route_fixes=4 voice_mismatch=1 mode=OFFLINE console=clean sha256={digest}")


if __name__ == "__main__":
    main()
