# TRU v43 — Text-Rooted Understanding

**Status:** public static human-test candidate; not canonical.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v43/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v43/TRU-v43.html

## What changed

- Repaired the Strong’s glosses flagged in the original baseline using pinned Open Scriptures Hebrew and MorphGNT Greek sources. The audit tracks 2,413 modular IDs and 3,332 standalone IDs, including 177 additional source-mangled modular glosses and seven standalone ones; both repair checks now report zero pending corrections and zero missing source definitions.
- Restored plural lookup so `define Graces` returns the likely singular entry, G5485; `define churches` is covered too. The response labels this as a likely singular fallback rather than an exact plural entry.
- TRU now explains its chosen name: **Text-Rooted Understanding**. It states that it is an offline Scripture and word-study tool, not infallible.
- Retained the 500-entry browser-local Scripture teaching shelf. It starts empty and each taught answer must cite one to five individual verses in the local KJV.

## Try it

Open the app and try `what does TRU mean?`, `define Graces`, `define churches`, `H1323`, `H8598`, `G932`, `faith without works`, and `John 3:16`.

Teach an answer with:

```text
remember: scripture: <question> = <brief answer> | <KJV verse>; <another KJV verse>
```

For example:

```text
remember: scripture: How can I find hope? = Hope is anchored in God's promise. | Romans 15:13; Hebrews 6:19
```

Saved answers stay in that browser’s local storage. Verse existence is checked against the local KJV; the user-supplied interpretation is not independently checked. Matching is exact apart from case and punctuation; it does not infer paraphrases. The full command guide is in [`../v40/README.md`](../v40/README.md).

## Verification

- Pinned repair checks: zero pending changes, zero unavailable source definitions; baseline defect targets and source hashes are recorded in the private modular source repository.
- Modular-source build: both offline HTML artifacts rebuild byte-identically; the 27-case source smoke suite passes with a clean console.
- v43 browser smoke: 9/9 checks pass offline with a clean console, including corrected Strong’s entries, plural lookups, the name answer, Scripture routes, and preserved truth routing.
- Existing benchmarks on this exact artifact: question-quality 28/28 scored targets (3 intentionally unscored review cases), object routing 5/5, Scripture teaching 8/8.
- Teaching-shelf boundary: 500 entries accepted, the 501st refused, and an existing entry remains updateable at capacity.
- The v43 builder reproduces the artifact byte-for-byte from the pinned v40 page and verified modular lexicon source.

## Artifact and lineage

- v40 parent SHA-256: `8c7df8f1b79efc5dee5ff8ac6863043d726444ccfd965343b4ab6d4d26fdefad`.
- Repaired modular source HTML SHA-256: `0c76884bf3d0d3b735fc3105efb916021b151b6dd63efb96789b5ad905b2ec7e`.
- Embedded repaired lexicon block SHA-256: `e21c8147da25e72f61bf04f4173e162af073943a73976034befe34136b8e2597`.
- v43 app size: 35,360,360 bytes.
- v43 app SHA-256: `8ab37266a47076e0213e1ed7464927b7a13dc0144d99eefa774da57ad2ad9f9c`.
- Repair-target manifest SHA-256: `7c4aab518083861e94070438e24ad923e6d68c7c9552e182073949071eacde4e`.

The public page serves a static HTML file; the builder needs the verified modular source artifact, which is in the private source repository. This candidate does not replace v40, any earlier candidate, or the TRU Shelf homepage.

Builder: [`build_v43.py`](../../quality/build_v43.py). Tests: [`test_v43_browser.py`](../../quality/test_v43_browser.py) and [`test_v43_capacity.py`](../../quality/test_v43_capacity.py). Benchmark results: [`question-quality-v43-v1.0.json`](../../quality/reports/question-quality-v43-v1.0.json), [`object-routing-v43-v1.0.json`](../../quality/reports/object-routing-v43-v1.0.json), and [`scripture-teaching-v43-v1.0.json`](../../quality/reports/scripture-teaching-v43-v1.0.json).
