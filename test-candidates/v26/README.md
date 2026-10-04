# TRU v26 test candidate

**Status:** Historical public versioned test candidate; v27 is the current candidate for testing the lexicon source corrections. v26 is not a canonical release. The Shelf homepage, Portal, Chair source and canonical releases are unchanged.

**TRU Clock build timestamp:** `2026-10-03T21:26:21.659Z` (UTC ISO string from `new Date().toISOString()`). Conversation-state timestamps remain Unix milliseconds from `Date.now()`.
**TRU Clock audit timestamp:** `2026-10-03T21:28:12.946Z` (UTC ISO string from `new Date().toISOString()`).

## What changed

The v25 audit found that its separate Chair-source lineage retained the Chair, complete DEEP lexicon text and phrase-result count, but had not carried forward the approved v22/v24 query corrections. v26 merges those corrections onto the pinned v25 artifact:

- `define <word>` now returns up to three exact Strong’s matches in a concise answer; `word study <word>` retains the full lexical, topical, dictionary and DEEP study.
- Approximate English matches no longer become unrelated Strong’s entries. `define English` and `word study English` now report a local lexical gap.
- General mathematics returns a clear TRU-scope boundary without an irrelevant H4962 suggestion; an explicit `Strong’s H4962` lookup still works.
- Restores source-reviewed H157, G25 and G26 glosses, plus the documented Love topic, Easton and Thayer corrections.
- Preserves the Chair panel, all 14,088 LOGOS records, complete 1,034-character BDB H1814 text and phrase count disclosure (`woe unto them`: top 3 of 17).

## Verification

`build_v26.py` and `verify_v26.py` in the local rebuild package pass. The verifier pins v25 by SHA-256, checks all 10 embedded JSON slots and 14,088 LOGOS records, confirms the new query behavior and its source corrections, and checks that the v25 Chair, phrase counts and full DEEP entry remain intact.

Browser-tested locally, with the page offline: `define love`, `word study love`, `define English`, `word study English`, `tell me about math`, `strongs h4962`, `inflame` and `woe unto them`. `word study love` no longer prompts the user to request the same study again. The Chair and reader controls remain present; 320 px and 390 px layouts have no horizontal overflow. No page errors, console messages or third-party requests were observed. Actual speech playback is unverified because this browser exposes no offline English voice.

## Artifact

- `TRU-v26.html` and `index.html` are byte-identical.
- Size: 35,408,514 bytes
- SHA-256: `d989503fa4b137597a04cf7be802cdd7c69026a860bdde48cb410c613440102f`
- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v26/
- Direct app: https://splashdown1.github.io/tru-shelf/test-candidates/v26/TRU-v26.html
