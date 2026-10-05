# TRU v36 — five-plus-word question handling

**Status:** new versioned public test candidate; not a canonical release.

**Preview:** `https://splashdown1.github.io/tru-shelf/test-candidates/v36/`

**Direct app:** `https://splashdown1.github.io/tru-shelf/test-candidates/v36/TRU-v36.html`

## Change from v35

v36 adds a narrow natural-question layer for five-or-more-word questions that maps recognised Bible topics and Strong’s lookups to existing local evidence. It returns KJV passages for hope, courage, mercy, rest, and love of God; exact topical or lexicon entries where appropriate; and locally indexed words of Jesus for forgiveness, loving enemies, and loving one another. Clear live/general-information requests receive an explicit offline-scope answer instead of unrelated TRU identity text. Existing short queries and the underlying source data remain unchanged.

This is a bounded routing layer, not a claim of general conversational understanding. Unsupported or ambiguous questions should remain gaps or be reviewed, not be answered by guesswork.

## Human checks

1. `Can I find hope here?` — expect Romans 15:13, Hebrews 6:19 and 1 Peter 1:3.
2. `What does Jesus say about loving enemies?` — expect Luke 6:27 and Matthew 5:44, without Luke 19:27.
3. `What does Jesus say about forgiveness?` — expect the existing locally sourced words-of-Jesus forgiveness card.
4. `What does peace mean in Hebrew?` — expect the local Strong’s entries including H7965.
5. `What is the Bitcoin price today in dollars?` — expect an explicit offline/non-Bible-sources boundary.
6. `Can you tell me about math?` — expect the Mathematics entry. Also check that one-word `hope` and `love` still use their existing routes.

## Automated checks

- The five-plus-word benchmark v1.1 scored **26/26 targets passed, 0 failed; 3 review-only questions deferred** on v36. The same 26 targets scored 1 pass and 25 failures on v35. The pinned report is in the local audit workspace; it is not app data.
- The v36 verifier confirms a deterministic artifact-based patch and byte-identical embedded source/data blocks.

## Artifact

- Parent v35: commit `759a6118ec93be896aaaa5cba943d1b1e1b9439d`; SHA-256 `c738c0d3fc305f523a3f34da1ae1381c0fc618e47319dd88ed96041ac42b09f3`.
- App size: 35,453,818 bytes.
- v36 SHA-256: `3f0974f1836ca0df685857ffa888962859c990b9d2fa7a83865c265aeeea6fa5`.
- Build stamp: `2026-10-05T12:07:20.000Z`.

This is an artifact-based patch, not a build from the still-missing matching v17 modular source tree. It adds only this new versioned candidate; it does not change the Shelf homepage or canonical releases.
