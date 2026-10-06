# TRU v39 — exact-term question routing

**Status:** new versioned public human-test candidate; not a canonical release.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v39/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v39/TRU-v39.html

## Change from v38

v39 fixes two misleading routes found in a five-query comparison across every public candidate from v19 to v38:

- `What is a chair?` previously matched an incidental Thayer G2828 gloss. The exact local English-term lookup now returns a clear no-match GAP instead of presenting that deep lexicon entry as the definition of an ordinary chair.
- `What is a door?` previously searched the phrase “a door” in the KJV. It now resolves the exact door term to Hebrew Strong's H8179.
- `Can you tell me what a chair/door is in Scripture?` follows the same exact-term rule, giving a precise GAP for chair and the H8179 lexical entry for door.
- A relevant existing result is preserved: `What is a harp?` still returns the full Easton's Dictionary entry. The v38 harp-use follow-up and v37 Hebrew/Greek language priority are retained.

The patch changes routing only. All 11 embedded source/data blocks are byte-identical to v38; no new claims or source text were added.

## Human checks

1. `What is a chair?` — expect a clear local no-match, not Thayer G2828.
2. `What is a door?` — expect DEFINE with H8179, not a KJV phrase-search card.
3. `Can you tell me what a chair is in Scripture?` — expect the precise no-match.
4. `Can you tell me what a door is in Scripture?` — expect H8179.
5. `What is a harp?` — confirm the full Easton's entry is preserved.
6. `What do you use a harp for?` — confirm the source-backed Easton usage response remains.
7. `What does peace mean in Hebrew?` and `What does peace mean in Greek?` — confirm the requested Strong's language comes first.

## Automated checks

- The all-candidate audit ran five queries against all 20 public candidates v19–v38 (100 observations); the same four routing defects and the harp control appeared in each version.
- Object-routing v1.0: v38 passes 1/5; v39 passes 5/5.
- The five-plus-word question-quality v1.3 pilot remains unchanged: v39 passes all 28 scored targets; 3 review cases remain unscored pending human judgement.
- The deterministic verifier confirms the v38 parent hash and all 11 embedded data blocks unchanged.

## Artifact

- Parent v38 SHA-256: `a1cee6f5b01e0c11cfd53046533b924125125180d1b11fd84be8695329c147ea`.
- App size: 35,461,001 bytes.
- v39 SHA-256: `be82106355cf5848f1533df0c8cc216f505d1ad03bf622e2a98b4a8812e66ebb`.
- Build stamp: `2026-10-06T12:11:11.000Z`.

This artifact-based candidate does not reproduce v17 from the still-missing matching modular source tree. It is added only at the new `test-candidates/v39/` path; the Shelf homepage, earlier candidates, and canonical files are unchanged.
