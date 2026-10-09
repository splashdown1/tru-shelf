# TRU v47 — Text-Rooted Understanding

**Status:** public static human-test candidate; not canonical.

- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v47/
- App: https://splashdown1.github.io/tru-shelf/test-candidates/v47/TRU-v47.html
- Family index: https://splashdown1.github.io/tru-shelf/portal/
- Previous candidate, preserved: https://splashdown1.github.io/tru-shelf/test-candidates/v46/

## What changed

- The gold Portal button and status-panel shortcut open the searchable family index in a new tab; the reader remains open in its original tab.
- Shelf and Portal links that launch an app, lane, candidate, or source open new tabs. In-page section and return-to-shelf navigation stay in the current tab.
- The reader's short help reply and accessible label explain the new-tab behaviour.
- Scripture, lexicon, topical data, question routing, and offline-reader behaviour are unchanged from v46.

## Verification

The v47 artifact is reproducibly built from the pinned v46 file (SHA-256 `3a06dee754ca16e03ac88df1a1256c61c6b9fd40aa0d819b246cee99a796197b`) and has SHA-256 `f20d775a7c66349df9154c5d0418d8ba07182d3e11e48931855b0bbe21d61761`.

- Inherited reader browser regression: 15 checks passed; no console or page errors.
- Gold Portal and status-panel links: open a separate tab without replacing the reader.
- Portal index: 93 searchable cards; search, lazy video loading, and mobile layout pass.
- Capacity: 500 Scripture Q&As accepted, the 501st refused, and an existing entry remains updateable.

Reports are recorded in [`quality/reports/portal-v47-smoke-v1.0.json`](../../quality/reports/portal-v47-smoke-v1.0.json). These curated checks do not establish full source completeness or theological correctness.

## Rebuild and retest

```sh
python3 quality/build_v47.py
python3 quality/test_v47_browser.py
python3 quality/test_v47_capacity.py
python3 quality/test_portal_index.py
```
