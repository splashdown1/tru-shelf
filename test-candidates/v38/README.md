# TRU v38 — source-backed dictionary use answers

**Status:** versioned public human-test candidate; not a canonical release.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v38/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v38/TRU-v38.html

## Change from v37

v38 recognises direct questions about an item's use when the local Easton's Dictionary has an exact title entry and wording that supports the answer. For example, “What do you use a harp for?” quotes the relevant harp-use sentences and keeps Easton's source label. It does not infer an answer when no matching entry or supporting sentence exists. The language-priority behaviour from v37 is retained. No embedded Bible, lexicon, topic, dictionary or other source data changed.

## Human checks

1. `What is a harp?` — expect the full Easton entry as before.
2. `Tell me more`, then `What do you use a harp for?` — expect Easton's cited accompaniment sentence and the note about the music's soothing effect, without the unrelated instrument-construction passage.
3. `What is a harp used for?` — expect the same source-backed answer.
4. `What do you use a telescope for?` — expect GAP rather than an invented answer if no exact Easton entry supports it.
5. `What does peace mean in Hebrew?` — Hebrew H7965 first.
6. `What does peace mean in Greek?` — Greek G1515 first; related entries remain.

## Automated checks

- The five-plus-word pilot v1.3 contains 31 prompts: 28 scored targets and 3 human-review cases. v37 passes 27/28 targets and fails the new harp-use case; v38 passes 28/28 with 0 failures. The 3 review cases remain deferred. See the audit workspace's `v18-rebuild/benchmarks/` reports.
- The v38 verifier confirms a deterministic patch from v37 and all 11 embedded source/data blocks byte-identical.
- Browser checks passed for the harp follow-up, the alternate “used for” phrasing, an unsupported telescope control, and the original full harp definition.

## Artifact

- Parent v37 commit: `8321f32b3e09796255f8a5a6ae5e8386f806d8fb`; SHA-256 `ce72c5a5befd5111a297957475a375c61e5b1e6f19ba226ddcea7af727de5096`.
- App size: 35,459,100 bytes.
- v38 SHA-256: `a1cee6f5b01e0c11cfd53046533b924125125180d1b11fd84be8695329c147ea`.
- Build stamp: `2026-10-05T15:42:36.000Z`.

This artifact-based test candidate does not reproduce v17 from the still-missing matching modular source tree. It adds only the new versioned test path; the Shelf homepage and canonical releases are unchanged.
