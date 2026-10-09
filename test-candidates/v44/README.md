# TRU v44 — Text-Rooted Understanding

**Status:** public static human-test candidate; not canonical.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v44/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v44/TRU-v44.html

## What changed

- Retains v43’s source-checked Strong’s repair set, selected plural fallback, Text-Rooted Understanding answer, and browser-local Scripture teaching shelf.
- Keeps personal questions such as `are you saved?` as a GAP. When the word is present in the KJV index, TRU offers a separate `word index: saved` lookup. That returns the local occurrence count and references; it does not answer the personal or doctrinal question.
- Shows the full generic GAP guidance once per session, then uses a shorter miss notice.
- Shows the full voice-mismatch notice once, then condenses repeated notices. Voice selection and local speech behaviour are unchanged.

## Try it

Test `what does TRU mean?`, `define Graces`, `are you saved?`, then use its follow-up or type `word index: saved`. The KJV index reports 107 occurrences and first references. Also try `nonsense query` followed by `zzzx qqqq` to check repeated GAP wording, and `where is heaven?` to confirm its existing topic suggestion is preserved.

Regression checks retained from v43: `define churches`, `H1323`, `H8598`, `G932`, `faith without works`, and `John 3:16`.

The Scripture teaching shelf starts empty and stores up to 500 exact question-and-answer pairs in that browser’s local storage. Each taught answer needs one to five references present in the local KJV. Verse existence is checked; the interpretation itself is not independently checked. See the [v40 teaching guide](../v40/README.md) for the command format and limits.

## Verification

- Browser smoke: 9/9 core checks; targeted checks cover the GAP follow-up, KJV index route, repeated-GAP wording, retained topic suggestion, and voice-mismatch notice; offline mode and browser console clean.
- Question-quality pilot: 28/28 scored targets; 3 review-only cases remain unscored.
- Object routing: 5/5. Scripture teaching mechanics: 8/8.
- Capacity check: 500 distinct entries accepted, the 501st refused, and an existing entry remains updateable at capacity.
- These are regression checks, not proof of complete theological correctness, source completeness, or general-purpose performance.

## Rebuild and test

From the repository root, reproduce the v44 artifact from the pinned v43 parent:

```sh
python3 quality/build_v44.py --output /tmp/TRU-v44-rebuilt.html
cmp /tmp/TRU-v44-rebuilt.html test-candidates/v44/TRU-v44.html
python3 quality/test_v44_browser.py
python3 quality/test_v44_capacity.py
```

The builder refuses to overwrite an existing output unless `--force` is supplied. Benchmark fixtures and the pinned v44 JSON results are in `quality/benchmarks/` and `quality/reports/`.

## Artifact and lineage

- v43 parent SHA-256: `8ab37266a47076e0213e1ed7464927b7a13dc0144d99eefa774da57ad2ad9f9c`.
- v44 build stamp: `2026-10-09T02:30:43Z`.
- v44 app size: 35,363,336 bytes.
- v44 app SHA-256: `0388514562e13159c8511ed9c0bd235ef1aae2b30ebb5d1f38310e8f85803b93`.

Builder: [`build_v44.py`](../../quality/build_v44.py). Browser tests: [`test_v44_browser.py`](../../quality/test_v44_browser.py) and [`test_v44_capacity.py`](../../quality/test_v44_capacity.py). Results: [`question-quality-v44-v1.0.json`](../../quality/reports/question-quality-v44-v1.0.json), [`object-routing-v44-v1.0.json`](../../quality/reports/object-routing-v44-v1.0.json), [`scripture-teaching-v44-v1.0.json`](../../quality/reports/scripture-teaching-v44-v1.0.json), and [`v44-fix-smoke-v1.0.json`](../../quality/reports/v44-fix-smoke-v1.0.json).

This candidate adds a local UI/routing layer over the pinned v43 HTML. It does not replace the TRU Shelf homepage, v40, or prior candidates.
