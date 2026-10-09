# TRU v46 — Text-Rooted Understanding

**Status:** public static human-test candidate; not canonical.

- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v46/
- App: https://splashdown1.github.io/tru-shelf/test-candidates/v46/TRU-v46.html
- Family index: https://splashdown1.github.io/tru-shelf/portal/
- Previous candidate, preserved: https://splashdown1.github.io/tru-shelf/test-candidates/v45/

## What changed

- The gold TRU Portal control opens the searchable family index in the same tab; browser Back returns to the reader.
- The portal control and its short architecture reply now point to the searchable index. Scripture, lexicon, topical data, answer routing, and offline-reader behaviour remain v45.
- The family index lists published reader candidates, current engines, field doors, preserved lineage, and seven Internet Archive film records. Video files are not copied into GitHub Pages; each player loads only when opened.
- The film records are marked Public Domain or Public Domain Mark by Internet Archive. Rights in newer music, restoration, or subtitles can differ, as can rights outside the United States. The portal links to the source records rather than redistributing their files.

## Verification

The v46 artifact is reproducibly built from the pinned v45 file (SHA-256 `1cffce39f2ce605d52f0d2bc9b58c83acaa9bd1aeed7d04ae9eb10aec5d0b23c`) and has SHA-256 `3a06dee754ca16e03ac88df1a1256c61c6b9fd40aa0d819b246cee99a796197b`.

- Inherited reader regression: all 15 query and interaction checks pass; no browser console or page errors.
- Gold portal navigation: opens the searchable index in the same tab; browser Back returns to the reader; accessible name describes its destination.
- Portal index: 92 searchable cards; filtering and lazy video-player activation pass.
- Teaching capacity: 500 entries accepted; a 501st distinct entry is refused; an existing entry remains updateable.
- v45's question, object-routing, and teaching benchmarks remain the latest content benchmarks. v46 changes no answer routing, so no new answer-quality claim is made.

## Rebuild and retest

From the repository root:

```sh
python3 quality/build_v46.py
python3 quality/test_v46_browser.py
python3 quality/test_v46_capacity.py
python3 quality/test_portal_index.py
```

Older published reader candidates remain available for comparison. A version number does not make a candidate canonical; source completeness and theological correctness are not established by these curated tests.
