from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = PROJECT_ROOT / "test-candidates" / "v45" / "TRU-v45.html"
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
    ("where is heaven?", "God’s dwelling place", "TOPICAL"),
    ("What is a chair?", "No exact local Bible lexicon entry", "GAP"),
    ("Can you tell me what a chair is in Scripture?", "No exact local Bible lexicon entry", "GAP"),
    ("What is a door?", "H8179", "DEFINE"),
    ("Can you tell me what a door is in Scripture?", "H8179", "DEFINE"),
    ("What is a harp?", "EASTON", "DEFINE"),
]


def run(target: Path) -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
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
            deep_card = None
            heaven_card = None
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
                if query == "h1323":
                    deep_card = answers.nth(before)
                if query == "where is heaven?":
                    heaven_card = answers.nth(before)
            if deep_card is None or heaven_card is None:
                raise AssertionError("polish regression queries did not render")
            disclosure = deep_card.locator("details.tru-deep-details")
            if disclosure.count() != 1 or disclosure.get_attribute("open") is not None:
                raise AssertionError("the full original-language entry must be collapsed by default")
            if re.search(r"\bV:\d{1,3}\b", deep_card.inner_text()) or re.search(r"\\\s*\\", deep_card.inner_text()):
                raise AssertionError("the displayed lexicon entry still contains extraction noise")
            disclosure.locator("summary").click()
            if disclosure.get_attribute("open") is None or len(disclosure.locator(".tru-deep-text").inner_text()) < 100:
                raise AssertionError("the full lexicon entry did not open with readable content")
            refs = heaven_card.locator("button.tru-ref")
            if refs.count() != 3:
                raise AssertionError(f"expected three linked KJV passages, found {refs.count()}")
            before = answers.count()
            refs.first.click()
            page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
            if not answers.last.inner_text().startswith("SCRIPTURE") or "Deuteronomy 26:15" not in answers.last.inner_text():
                raise AssertionError("clicking topical evidence did not open the cited verse")
            checks = page.evaluate("""() => {
              const firstGap = window.route("nonsense query");
              const secondGap = window.route("zzzx qqqq");
              const personal = window.route("are you saved?");
              const index = personal.sugContinuation ? window.route(personal.sugContinuation.query) : null;
              const deep = window.route("h1323");
              const heaven = window.route("where is heaven?");
              const unmatchedIndex = window.route("word index: zzzzx");
              const originalVoiceList = window.readerVoiceList;
              window.setReaderGender("female");
              window.readerVoiceList = () => [{name:"Local English Voice",lang:"en-US",localService:true,voiceURI:"local"}];
              const voiceFirst = window.readerVoiceStatus();
              const voiceSecond = window.readerVoiceStatus();
              window.readerVoiceList = originalVoiceList;
              return {firstGap,secondGap,personal,index,deep,heaven,unmatchedIndex,voiceFirst,voiceSecond,modeLabel:document.querySelector(".mode-switch .tru-mode-label")?.textContent||""};
            }""")
            if checks["firstGap"]["verdict"] != "GAP" or "Try a verse" not in checks["firstGap"]["reply"]:
                raise AssertionError(f"first GAP guidance changed unexpectedly: {checks['firstGap']!r}")
            if checks["secondGap"]["verdict"] != "GAP" or "No supported match" not in checks["secondGap"]["reply"] or "Try a verse" in checks["secondGap"]["reply"]:
                raise AssertionError(f"repeated GAP guidance was not shortened: {checks['secondGap']!r}")
            suggestion = checks["personal"].get("sugContinuation") or {}
            if checks["personal"].get("verdict") != "GAP" or suggestion.get("query") != "word index: saved":
                raise AssertionError(f"personal-status question must remain a GAP with a safe follow-up: {checks['personal']!r}")
            if not checks["index"] or checks["index"].get("verdict") != "DEFINE" or "107 times" not in checks["index"].get("reply", ""):
                raise AssertionError(f"saved word-index follow-up failed: {checks['index']!r}")
            if checks["heaven"].get("verdict") != "TOPICAL" or "God’s dwelling place" not in checks["heaven"].get("reply", ""):
                raise AssertionError("place question did not return bounded topical evidence")
            if "a daughter" not in checks["deep"].get("reply", "") or 'class="tru-deep-details"' not in checks["deep"].get("reply", ""):
                raise AssertionError("original-language data was not retained in a collapsible detail block")
            if re.search(r"\bV:\d{1,3}\b", checks["deep"].get("reply", "")) or re.search(r"\\\s*\\", checks["deep"].get("reply", "")):
                raise AssertionError("lexicon display cleanup left extraction artifacts")
            if checks["unmatchedIndex"].get("verdict") != "GAP" or checks["modeLabel"] != "MODE":
                raise AssertionError("unknown word-index or explicit mode-label regression")
            if not checks["voiceFirst"].startswith("No recognizable female voice listed"):
                raise AssertionError(f"first voice mismatch notice changed: {checks['voiceFirst']!r}")
            if not checks["voiceSecond"].startswith("Using local voice") or "Choose a named voice" in checks["voiceSecond"]:
                raise AssertionError(f"repeated voice mismatch notice was not condensed: {checks['voiceSecond']!r}")
            before = answers.count()
            page.fill(input_selector, "are you saved?")
            page.locator(send_selector).click()
            page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
            gap_card = answers.last
            follow_up = gap_card.locator("button.next-action")
            if not gap_card.inner_text().startswith("GAP") or follow_up.count() != 1 or "saved" not in follow_up.inner_text().lower():
                raise AssertionError("personal-status GAP did not render its KJV word-index follow-up")
            before = answers.count()
            follow_up.click()
            page.wait_for_function("count => document.querySelectorAll('#chat .msg .vd').length > count", arg=before, timeout=120000)
            if not answers.last.inner_text().startswith("DEFINE") or "107 times" not in answers.last.inner_text():
                raise AssertionError("rendered word-index follow-up did not report the saved count")
            page.set_viewport_size({"width":390,"height":844})
            page.reload(wait_until="load",timeout=120000)
            page.wait_for_function("document.querySelector('#status')?.textContent.includes('READY')",timeout=120000)
            mobile=page.evaluate("""() => {
              const header=document.querySelector('.header').getBoundingClientRect();
              const sub=document.querySelector('#sub');
              const pseudo=getComputedStyle(sub,'::after').content;
              const badge=document.querySelector('#badge').getBoundingClientRect();
              const mode=document.querySelector('.mode-switch').getBoundingClientRect();
              return {headerHeight:header.height,viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,pseudo,fullSummary:sub.title,modeLabel:!!document.querySelector('.mode-switch .tru-mode-label'),controlsOverlap:badge.right>mode.left+1,modeRight:mode.right};
            }""")
            if mobile["headerHeight"]>90 or mobile["scrollWidth"]>mobile["viewport"]+1 or "31k KJV" not in mobile["pseudo"] or "14,088" not in mobile["fullSummary"] or mobile["controlsOverlap"] or mobile["modeRight"]>mobile["viewport"]+1 or not mobile["modeLabel"]:
                raise AssertionError(f"mobile header is not compact and readable: {mobile!r}")
            if console_errors or page_errors:
                raise AssertionError(f"console errors={console_errors!r} page errors={page_errors!r}")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v45 offline and reading-polish regression checks")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    target = parser.parse_args().html
    if not target.is_file():
        raise SystemExit(f"candidate is missing: {target}")
    run(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"V45_BROWSER_SMOKE_OK cases={len(CASES)} routes=heaven-evidence lexicon=clean-collapsible voice_mismatch=1 mode-label=present console=clean sha256={digest}")


if __name__ == "__main__":
    main()
