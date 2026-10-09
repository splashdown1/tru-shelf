# TRU v45 — Text-Rooted Understanding

**Status:** public static human-test candidate; not canonical.

- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v45/
- App: https://splashdown1.github.io/tru-shelf/test-candidates/v45/TRU-v45.html
- Prior candidate, preserved: https://splashdown1.github.io/tru-shelf/test-candidates/v44/

## What changed

- BDB and Thayer original-language entries now sit in a closed-by-default, scrollable detail panel. The displayed text removes obvious extraction noise; the embedded source data is unchanged.
- “Where is heaven?” now receives a bounded answer from the local Nave–Torrey topic index, with three linked KJV passages: Deuteronomy 26:15, Isaiah 66:1, and Matthew 6:9. The wording distinguishes a topic classification from a physical location.
- The header has a visible MODE label and compact phone layout; the full corpus summary remains available in the app.
- v44 routing, GAP handling, voice notice, personal-question boundary, and teaching shelf are retained.

## Verification

The v45 artifact is pinned at SHA-256 `1cffce39f2ce605d52f0d2bc9b58c83acaa9bd1aeed7d04ae9eb10aec5d0b23c`.

- Browser regression: 15 query/interaction checks pass; no console or page errors.
- Question quality: 28/28 scored targets pass; 3 cases remain explicitly review-only.
- Object routing: 5/5 pass.
- Scripture teaching: 8/8 pass.
- Capacity: 500 entries accepted, the 501st refused, and an existing entry remains updateable.
- Mobile: 390×844 CSS-pixel viewport, no horizontal overflow.

Reports are under [`quality/reports/`](../../quality/reports/), including the combined [v45 polish smoke record](../../quality/reports/v45-polish-smoke-v1.0.json).

## Rebuild and retest

From the repository root:

```sh
python3 quality/build_v45.py --force
python3 quality/test_v45_browser.py
python3 quality/test_v45_capacity.py
python3 quality/benchmarks/run_question_benchmark.py --html test-candidates/v45/TRU-v45.html --record /tmp/question-quality-v45-recheck.json
python3 quality/benchmarks/run_question_benchmark.py --html test-candidates/v45/TRU-v45.html --cases quality/benchmarks/object-routing-v1.0.jsonl --minimum-words 1 --record /tmp/object-routing-v45-recheck.json
python3 quality/benchmarks/run_question_benchmark.py --html test-candidates/v45/TRU-v45.html --cases quality/benchmarks/scripture-teaching-v1.0.jsonl --minimum-words 1 --record /tmp/scripture-teaching-v45-recheck.json
```

The builder pins v44’s exact hash and refuses to overwrite v45 unless `--force` is supplied. These curated checks do not establish full source completeness or theological correctness.
