# TRU v24 test candidate

**Status:** Public versioned test candidate, not a canonical release. The TRU Shelf homepage, lanes and release files are unchanged.

**TRU Clock build timestamp:** `2026-10-03T12:24:22.884Z` (UTC ISO string, the format produced by `new Date().toISOString()`). Conversation-state marks remain Unix milliseconds from `Date.now()`, as specified by [TRU Clock](https://github.com/splashdown1/tru-clock).

## What changed

- Combines v22's concise exact-match definitions, expanded word studies, source-reviewed lexicon and Love-topic corrections, and voice reporting with v23's typed-input-only reader. Browser speech recognition remains disabled.
- General maths queries now return a short scope boundary with no speculative H4962 cross-suggestion. Explicit `Strong's H4962` still works.
- `define` shows the concise glossary view; `word study` keeps the full lexicon, topic, Easton and Thayer material. Unsupported English words return an explicit gap instead of a guessed Strong's match.

## Verification

- `python3 build_v24.py` and `python3 verify_v24.py` pass. The verifier checks the pinned v22/v23 inputs, all 10 embedded JSON slots, all 14,088 LOGOS records, the documented source corrections and exact byte-level scope of the v24 patches.
- Browser-smoked offline: `define love`, `word study love`, `topic: love`, `define English`, `word study English`, `define math`, `tell me about math`, and explicit `strongs h4962`. Love shows the corrected Nave heading and clean references/bullets; maths makes no H4962 suggestion; explicit H4962 remains available.
- Simulated two local English voices: AUTO reported the selected voice and gender-preference match accurately. With zero local voices exposed, the page reports 0 and disables the test button. Audible speech was not verified on a device with a real installed voice.
- The local browser reported no JavaScript errors or external network requests. Speech-recognition input is not included.

## Rebuild

From `v18-rebuild/`:

```sh
python3 build_v24.py
python3 verify_v24.py
```

- **Artifact:** `TRU-v24.html` — 35,032,318 bytes
- **SHA-256:** `3b083d444589a6158601302f4ef839f3cc896ae27d98954f21e2484d2d92162c`
- **Build timestamp:** `2026-10-03T12:24:22.884Z`
