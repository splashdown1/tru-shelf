# TRU Shelf quality and audit materials

The live page is [TRU Shelf Quality & Audit](https://splashdown1.github.io/tru-shelf/quality/). This folder publishes repeatable local regression checks and their recorded results. It is separate from TRU's offline app data.

## Current candidate

- [v39 preview](https://splashdown1.github.io/tru-shelf/test-candidates/v39/)
- [v39 app](https://splashdown1.github.io/tru-shelf/test-candidates/v39/TRU-v39.html)
- [v39 test notes](../test-candidates/v39/README.md)
- Commit: `2803c5d074a90ae54c922604ea92aba48d39ce9a`
- App SHA-256: `be82106355cf5848f1533df0c8cc216f505d1ad03bf622e2a98b4a8812e66ebb`

v39 is a human-test candidate, not a canonical release. It is a routing-only, artifact-based patch to v38; all 11 embedded source/data blocks are unchanged. The matching modular source tree for v17 SUPER has not been recovered, so this candidate does not claim to reproduce that source build.

## Verify the v39 lineage

The pinned verifier checks the public v39 SHA-256, reconstructs the deterministic patch from the public v38 artifact, and confirms all 11 embedded source/data blocks are unchanged. It does not alter the published candidate.

```sh
python3 quality/verify_v39.py
```

To create and verify a separate rebuilt copy, choose a new, unused output path. The builder refuses to overwrite an existing file:

```sh
python3 quality/build_v39.py --output /tmp/TRU-v39-rebuilt.html
python3 quality/verify_v39.py --artifact /tmp/TRU-v39-rebuilt.html
```

The builder and verifier use only Python's standard library. Their source is [`build_v39.py`](build_v39.py) and [`verify_v39.py`](verify_v39.py).

## Published checks

### Five-plus-word pilot (`question-quality-public-v1.0`)

Thirty-one generic prompts cover Bible questions, Scripture lookup, word study, explicit Hebrew/Greek intent, bounded out-of-scope queries, and three intentionally unscored review cases. v38 and v39 each pass 28 of 28 scored target checks; three cases remain `REVIEW`. The fixture is a sanitised, public test set rather than a transcript of private conversations.

- Fixture: [`benchmarks/question-quality-public-v1.0.jsonl`](benchmarks/question-quality-public-v1.0.jsonl)
- v38 report: [`reports/question-quality-v38-v1.0.json`](reports/question-quality-v38-v1.0.json)
- v39 report: [`reports/question-quality-v39-v1.0.json`](reports/question-quality-v39-v1.0.json)

### Exact-term object routing (`object-routing-v1.0`)

Five checks cover exact definitions for `chair` and `door`, both as short and longer questions, plus a dictionary answer that must be preserved. The v38 result is 1/5; v39 is 5/5.

- Fixture: [`benchmarks/object-routing-v1.0.jsonl`](benchmarks/object-routing-v1.0.jsonl)
- v38 report: [`reports/object-routing-v38-v1.0.json`](reports/object-routing-v38-v1.0.json)
- v39 report: [`reports/object-routing-v39-v1.0.json`](reports/object-routing-v39-v1.0.json)
- Historical comparison: [`reports/object-routing-history-v1.0.md`](reports/object-routing-history-v1.0.md), with all 100 machine-readable observations in [`reports/object-routing-history-v1.0.json`](reports/object-routing-history-v1.0.json)

## Re-running locally

The runner requires Python 3 and the `agent-browser` command. It loads the candidate HTML into a local browser and calls TRU's local router directly; it does not call an AI service or retain app memory between test cases.

Verify the pinned v39 parent, exact deterministic patch and unchanged embedded data blocks:

```sh
python3 quality/verify_v39.py
```

To rebuild without risking an already-published file, choose a new output path. The builder refuses to overwrite existing files:

```sh
python3 quality/build_v39.py --output /tmp/TRU-v39-rebuilt.html
cmp /tmp/TRU-v39-rebuilt.html test-candidates/v39/TRU-v39.html
```

From the repository root:

```sh
python3 quality/benchmarks/run_question_benchmark.py \
  --html test-candidates/v39/TRU-v39.html \
  --record quality/reports/local-question-results.json

python3 quality/benchmarks/run_question_benchmark.py \
  --html test-candidates/v39/TRU-v39.html \
  --cases quality/benchmarks/object-routing-v1.0.jsonl \
  --minimum-words 1 \
  --record quality/reports/local-object-results.json
```

The runner refuses to overwrite an existing report path. Choose a new filename each time. To compare v38, change the `--html` path to `test-candidates/v38/TRU-v38.html` and use a new report name.

## Limits

These are focused regression tests, not a statistically representative language benchmark and not theological validation. Target checks confirm expected routing, citations or evidence markers for the questions listed; they do not prove the completeness or correctness of every passage or interpretation. Review-only cases are deliberately not scored until their intended behaviour is agreed. The history audit tested five prompts against public candidates v19–v38; it does not establish that every historical query behaves identically.
