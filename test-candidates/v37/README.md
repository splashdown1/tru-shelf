# TRU v37 — explicit language priority

**Status:** new versioned public test candidate; not a canonical release.

**Preview:** `https://splashdown1.github.io/tru-shelf/test-candidates/v37/`

**Direct app:** `https://splashdown1.github.io/tru-shelf/test-candidates/v37/TRU-v37.html`

## Change from v36

When a lexical question explicitly asks for Hebrew or Greek, v37 puts matching Strong’s entries first and retains the other-language entries afterwards. For example, a Hebrew question about peace now begins with H7965; a Greek question begins with G1515. Queries without an explicit language keep their existing order. This is a ranking change only: no embedded Bible, lexicon, topical or dictionary data changed.

## Human checks

1. `What does peace mean in Hebrew?` — expect Hebrew H7965 first; related Hebrew records remain available, followed by Greek material.
2. `What does peace mean in Greek?` — expect Greek G1515 first, with Hebrew material retained.
3. `What does peace mean in the Bible?` — no language preference; the existing default order begins with G1515.
4. `Can I find hope here?` — expect Romans 15:13, Hebrews 6:19 and 1 Peter 1:3.
5. `What does Jesus say about loving enemies?` — expect Luke 6:27 and Matthew 5:44, without Luke 19:27.
6. `What is the Bitcoin price today in dollars?` — expect the explicit offline-scope boundary.

## Automated checks

- The five-plus-word question-quality v1.2 pilot scored **27/27 targets passed, 0 failed; 3 review-only questions deferred** on v37. v36 scored 26/27 because Hebrew H7965 appeared after Greek G1515 for the explicit Hebrew question; v35 scored 1/27. See the local test-only reports in the audit workspace.
- The v37 verifier confirms a deterministic patch from v36 and all 11 embedded source/data blocks byte-identical.

## Artifact

- Parent v36: commit `14db2fa5d9f097e359a866c1aea044e89564ba8e`; SHA-256 `3f0974f1836ca0df685857ffa888962859c990b9d2fa7a83865c265aeeea6fa5`.
- App size: 35,456,973 bytes.
- v37 SHA-256: `ce72c5a5befd5111a297957475a375c61e5b1e6f19ba226ddcea7af727de5096`.
- Build stamp: `2026-10-05T13:23:28.000Z`.

This is an artifact-based patch, not a build from the still-missing matching v17 modular source tree. It adds only this new versioned test path; the Shelf homepage and canonical releases are unchanged.
