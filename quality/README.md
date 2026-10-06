# TRU Shelf quality and audit materials

The live page is [TRU Shelf Quality & Audit](https://splashdown1.github.io/tru-shelf/quality/). This folder publishes repeatable local regression checks and recorded results. It is separate from TRU's offline app data.

## Current human-test candidate: v40

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

Thirty-one generic prompts cover Bible questions, Scripture lookup, word study, explicit Hebrew/Greek intent, bounded out-of-scope queries, and three intentionally unscored review cases. v38, v39 and v40 pass 28 of 28 scored target checks; three cases remain `REVIEW`. This is a curated pilot, not a statistically representative benchmark.

- Fixture: [`benchmarks/question-quality-public-v1.0.jsonl`](benchmarks/question-quality-public-v1.0.jsonl)
- v38 report: [`reports/question-quality-v38-v1.0.json`](reports/question-quality-v38-v1.0.json)
- v39 report: [`reports/question-quality-v39-v1.0.json`](reports/question-quality-v39-v1.0.json)
- v40 report: [`reports/question-quality-v40-v1.0.json`](reports/question-quality-v40-v1.0.json)

### Exact-term object routing (`object-routing-v1.0`)

Five checks cover exact definitions for `chair` and `door`, both as short and longer questions, plus a dictionary answer that must be preserved. v38 passes 1/5; v39 and v40 pass 5/5.

- Fixture: [`benchmarks/object-routing-v1.0.jsonl`](benchmarks/object-routing-v1.0.jsonl)
- v38 report: [`reports/object-routing-v38-v1.0.json`](reports/object-routing-v38-v1.0.json)
- v39 report: [`reports/object-routing-v39-v1.0.json`](reports/object-routing-v39-v1.0.json)
- v40 report: [`reports/object-routing-v40-v1.0.json`](reports/object-routing-v40-v1.0.json)
- Historical comparison: [`reports/object-routing-history-v1.0.md`](reports/object-routing-history-v1.0.md), with all 100 machine-readable observations in [`reports/object-routing-history-v1.0.json`](reports/object-routing-history-v1.0.json)

### Scripture teaching mechanics (`scripture-teaching-v1.0`)

Eight sequential local checks cover missing or invalid citations, a valid answer and exact retrieval, listing and removal, and backward compatibility with ordinary `remember:`. All 8 pass on v40. A separate isolated browser test fills the 500-entry capacity and confirms a new question is refused while an existing one remains updateable.

- Fixture: [`benchmarks/scripture-teaching-v1.0.jsonl`](benchmarks/scripture-teaching-v1.0.jsonl)
- v40 report: [`reports/scripture-teaching-v40-v1.0.json`](reports/scripture-teaching-v40-v1.0.json)- Capacity check: [`test_v40_capacity.py`](test_v40_capacity.py) — verifies the 500-entry limit and safe update at capacity.

The teaching feature's 500-entry capacity is **not** a 500-question benchmark and does not mean any answers are preloaded. The five-plus-word pilot remains at 31 cases; expand its answer key only in small, source-checked batches after human review.

## Earlier v39 lineage

The v39 candidate is preserved at [its preview](https://splashdown1.github.io/tru-shelf/test-candidates/v39/). Its deterministic builder and verifier remain available as [`build_v39.py`](build_v39.py) and [`verify_v39.py`](verify_v39.py).

## Re-running locally

The runner requires Python 3 and `agent-browser`. It opens the standalone artifact and calls TRU's local router directly; it does not use an AI service. Each fixture is executed sequentially in one browser session so stateful command tests can teach, retrieve, and forget an entry.

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

A real-machine session transcript was audited against the v40 artifact source: [`reports/human-session-audit-v40-2026-10-06.md`](reports/human-session-audit-v40-2026-10-06.md). GAP/doctrine behaviour held; the audit verifies lexicon data defects in the embedded Strong's block (1,415 duplicated definitions, 523 empty definitions, plus usage-token and transliteration mangling) that predate v40, and two routing/voice findings. These are recorded, not yet fixed.
