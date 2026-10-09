# TRU Shelf quality and audit materials

The live page is [TRU Shelf Quality & Audit](https://splashdown1.github.io/tru-shelf/quality/). This folder publishes repeatable local regression checks and recorded results. It is separate from TRU's offline app data.

## Current human-test candidate: v46

- [v46 preview](https://splashdown1.github.io/tru-shelf/test-candidates/v46/)
- [v46 app](https://splashdown1.github.io/tru-shelf/test-candidates/v46/TRU-v46.html)
- [v46 test notes](../test-candidates/v46/README.md)
- [v46 portal-link smoke report](reports/portal-v46-smoke-v1.0.json)
- App SHA-256: `3a06dee754ca16e03ac88df1a1256c61c6b9fd40aa0d819b246cee99a796197b`

v46 is a pinned portal patch to v45: the gold control opens the searchable TRU family index in the same tab, browser Back returns to the reader, and the reader's short architecture reply describes that destination. Scripture, lexicon, topical data, and answer routing are unchanged. The v45 15-check reader suite passes on v46, and the v46 browser check verifies same-tab navigation and return history. The portal itself renders 92 searchable cards, including the published v19–v40 and v43–v46 reader candidates, public engines/lanes, and seven Internet Archive film links. The videos are not copied into this repository.

```sh
python3 quality/build_v46.py --output /tmp/TRU-v46-rebuilt.html
cmp /tmp/TRU-v46-rebuilt.html test-candidates/v46/TRU-v46.html
python3 quality/test_v46_browser.py
python3 quality/test_v46_capacity.py
python3 quality/test_portal_index.py
```

The reader remains a test candidate, not a canonical release. v46 passed the 500-entry teaching-capacity boundary directly. The movie shelf is a static catalogue with external playback; its linked source records and file sizes can change independently.

## Previous human-test candidate: v45

- [v45 preview](https://splashdown1.github.io/tru-shelf/test-candidates/v45/)
- [v45 app](https://splashdown1.github.io/tru-shelf/test-candidates/v45/TRU-v45.html)
- [v45 test notes](../test-candidates/v45/README.md)
- [v45 combined polish report](reports/v45-polish-smoke-v1.0.json)
- [v45 question-quality report](reports/question-quality-v45-v1.0.json)
- [v45 object-routing report](reports/object-routing-v45-v1.0.json)
- [v45 Scripture-teaching report](reports/scripture-teaching-v45-v1.0.json)
- App SHA-256: `1cffce39f2ce605d52f0d2bc9b58c83acaa9bd1aeed7d04ae9eb10aec5d0b23c`

v45 is a reproducible, pinned static update to v44. It presents the long BDB/Thayer material in a collapsible, cleaned display, gives “where is heaven?” three linked passages from the local KJV and topical index without claiming a physical coordinate, and makes the header more legible on phones. The embedded data and source lineage are unchanged. It retains v44’s GAP boundaries, word-index follow-up, voice notice, and teaching shelf.

```sh
python3 quality/build_v45.py --output /tmp/TRU-v45-rebuilt.html
cmp /tmp/TRU-v45-rebuilt.html test-candidates/v45/TRU-v45.html
python3 quality/test_v45_browser.py
python3 quality/test_v45_capacity.py
```

The 15 browser query/interaction checks pass with a clean console; question quality is 28/28 scored targets with 3 review-only; object routing is 5/5; Scripture teaching is 8/8; and the 500-entry capacity boundary passes. This remains a public test candidate, not a canonical release.

## Previous candidate: v44

- [v44 preview](https://splashdown1.github.io/tru-shelf/test-candidates/v44/)
- [v44 app](https://splashdown1.github.io/tru-shelf/test-candidates/v44/TRU-v44.html)
- [v44 test notes](../test-candidates/v44/README.md)
- [v44 route and voice regression report](reports/v44-fix-smoke-v1.0.json)
- App SHA-256: `0388514562e13159c8511ed9c0bd235ef1aae2b30ebb5d1f38310e8f85803b93`

v44 keeps personal-status questions as GAPs, adds a verified KJV word-index follow-up where one exists, avoids repeating generic GAP instructions, and shortens repeated voice-mismatch notices without changing voice selection. `are you saved?` remains a GAP; its follow-up reports only the word’s 107 KJV occurrences and references.

## Historical candidate: v40

- [v40 preview](https://splashdown1.github.io/tru-shelf/test-candidates/v40/)
- [v40 app](https://splashdown1.github.io/tru-shelf/test-candidates/v40/TRU-v40.html)
- [v40 test notes](../test-candidates/v40/README.md)
- App SHA-256: `8c7df8f1b79efc5dee5ff8ac6863043d726444ccfd965343b4ab6d4d26fdefad`

v40 is a non-canonical, artifact-based patch to public v39. It adds a browser-local teaching shelf for up to 500 question-and-answer entries. Each entry needs one to five individual references that resolve in the local KJV. The user-supplied answer is shown with the exact local KJV text; citation existence is checked, but interpretation is not independently reviewed. Exact question matching normalises case and punctuation and does not infer paraphrases. The shelf starts empty and is personal to each browser; it is not a preloaded 500-question corpus.

## Verify v40 lineage

The pinned verifier reconstructs v40 from the public v39 artifact and confirms that all 11 embedded source/data blocks are byte-identical:

```sh
python3 quality/verify_v40.py
```

For a separate rebuild, use a new output path; the builder refuses to overwrite an existing file:

```sh
python3 quality/build_v40.py --output /tmp/TRU-v40-rebuilt.html
cmp /tmp/TRU-v40-rebuilt.html test-candidates/v40/TRU-v40.html
```

The v40 builder and verifier use only Python's standard library: [`build_v40.py`](build_v40.py) and [`verify_v40.py`](verify_v40.py). The matching modular source tree for v17 SUPER remains unrecovered; v40 does not claim to reproduce that source build.

## Published checks

### Five-plus-word question pilot (`question-quality-public-v1.0`)

Thirty-one generic prompts cover Bible questions, Scripture lookup, word study, explicit Hebrew/Greek intent, bounded out-of-scope queries, and three intentionally unscored review cases. v38, v39, v40, v43, v44 and v45 pass 28 of 28 scored target checks; three cases remain `REVIEW`. This is a curated pilot, not a statistically representative benchmark.

- Fixture: [`benchmarks/question-quality-public-v1.0.jsonl`](benchmarks/question-quality-public-v1.0.jsonl)
- v38 report: [`reports/question-quality-v38-v1.0.json`](reports/question-quality-v38-v1.0.json)
- v39 report: [`reports/question-quality-v39-v1.0.json`](reports/question-quality-v39-v1.0.json)
- v40 report: [`reports/question-quality-v40-v1.0.json`](reports/question-quality-v40-v1.0.json)
- v43 report: [`reports/question-quality-v43-v1.0.json`](reports/question-quality-v43-v1.0.json)
- v44 report: [`reports/question-quality-v44-v1.0.json`](reports/question-quality-v44-v1.0.json)
- v45 report: [`reports/question-quality-v45-v1.0.json`](reports/question-quality-v45-v1.0.json)

### Exact-term object routing (`object-routing-v1.0`)

Five checks cover exact definitions for `chair` and `door`, both as short and longer questions, plus a dictionary answer that must be preserved. v38 passes 1/5; v39, v40, v43, v44 and v45 pass 5/5.

- Fixture: [`benchmarks/object-routing-v1.0.jsonl`](benchmarks/object-routing-v1.0.jsonl)
- v38 report: [`reports/object-routing-v38-v1.0.json`](reports/object-routing-v38-v1.0.json)
- v39 report: [`reports/object-routing-v39-v1.0.json`](reports/object-routing-v39-v1.0.json)
- v40 report: [`reports/object-routing-v40-v1.0.json`](reports/object-routing-v40-v1.0.json)
- v43 report: [`reports/object-routing-v43-v1.0.json`](reports/object-routing-v43-v1.0.json)
- v44 report: [`reports/object-routing-v44-v1.0.json`](reports/object-routing-v44-v1.0.json)
- v45 report: [`reports/object-routing-v45-v1.0.json`](reports/object-routing-v45-v1.0.json)
- Historical comparison: [`reports/object-routing-history-v1.0.md`](reports/object-routing-history-v1.0.md), with all 100 machine-readable observations in [`reports/object-routing-history-v1.0.json`](reports/object-routing-history-v1.0.json)

### Scripture teaching mechanics (`scripture-teaching-v1.0`)

Eight sequential local checks cover missing or invalid citations, a valid answer and exact retrieval, listing and removal, and backward compatibility with ordinary `remember:`. All 8 pass on v40, v43, v44 and v45. Separate isolated browser tests fill the 500-entry capacity and confirm a new question is refused while an existing one remains updateable.

- Fixture: [`benchmarks/scripture-teaching-v1.0.jsonl`](benchmarks/scripture-teaching-v1.0.jsonl)
- v40 report: [`reports/scripture-teaching-v40-v1.0.json`](reports/scripture-teaching-v40-v1.0.json)
- v40 capacity check: [`test_v40_capacity.py`](test_v40_capacity.py)
- v43 report: [`reports/scripture-teaching-v43-v1.0.json`](reports/scripture-teaching-v43-v1.0.json)
- v43 capacity check: [`test_v43_capacity.py`](test_v43_capacity.py)
- v44 report: [`reports/scripture-teaching-v44-v1.0.json`](reports/scripture-teaching-v44-v1.0.json)
- v44 capacity check: [`test_v44_capacity.py`](test_v44_capacity.py)
- v45 report: [`reports/scripture-teaching-v45-v1.0.json`](reports/scripture-teaching-v45-v1.0.json)
- v45 capacity check: [`test_v45_capacity.py`](test_v45_capacity.py)

The teaching feature's 500-entry capacity is **not** a 500-question benchmark and does not mean any answers are preloaded. The five-plus-word pilot remains at 31 cases; expand its answer key only in small, source-checked batches after human review.

## Earlier v39 lineage

The v39 candidate is preserved at [its preview](https://splashdown1.github.io/tru-shelf/test-candidates/v39/). Its deterministic builder and verifier remain available as [`build_v39.py`](build_v39.py) and [`verify_v39.py`](verify_v39.py).

## Re-running locally

The runner requires Python 3 and `agent-browser`. It opens the standalone artifact and calls TRU's local router directly; it does not use an external model service. Each fixture is executed sequentially in one browser session so stateful command tests can teach, retrieve, and forget an entry.

From the repository root:

```sh
python3 quality/verify_v40.py
python3 quality/benchmarks/run_question_benchmark.py \
  --html test-candidates/v40/TRU-v40.html \
  --cases quality/benchmarks/question-quality-public-v1.0.jsonl \
  --record quality/reports/local-question-results.json

python3 quality/benchmarks/run_question_benchmark.py \
  --html test-candidates/v40/TRU-v40.html \
  --cases quality/benchmarks/object-routing-v1.0.jsonl \
  --minimum-words 1 \
  --record quality/reports/local-object-results.json

python3 quality/benchmarks/run_question_benchmark.py \
  --html test-candidates/v40/TRU-v40.html \
  --cases quality/benchmarks/scripture-teaching-v1.0.jsonl \
  --minimum-words 1 \
  --record quality/reports/local-scripture-teaching-results.json
```

The runner refuses to overwrite an existing report path. Choose new filenames. These targeted tests do not prove every KJV citation is theologically adequate, validate user-supplied interpretations, or establish general-purpose performance. The three review-only prompts remain unscored until their intended behaviour is agreed.

### Human session audit (2026-10-06)

A real-machine session transcript was audited against the v40 artifact source: [`reports/human-session-audit-v40-2026-10-06.md`](reports/human-session-audit-v40-2026-10-06.md). GAP/doctrine behaviour held; the audit also found source and presentation defects in the Strong’s block plus routing/voice issues. v43 repaired its flagged Strong’s glosses against pinned Hebrew and Greek source snapshots, restored plural fallback, and named TRU; v44 addresses repeated GAP guidance and voice-mismatch repetition; v45 improves lexicon presentation and surfaces bounded, cited topical evidence. The selected repairs do not establish the entire lexicon’s completeness or theological correctness.
