# TRU v32 human-test candidate

**Status:** Versioned public test candidate; not canonical and not a Shelf lane.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v32/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v32/TRU-v32.html

**Change:** Unqualified `math`, `maths`, and forms such as `define math` now resolve to the Math canon's **Mathematics** entry. This prevents the generic word `math` from falling through to the unrelated Strong's H4962 Hebrew entry. `math: <term>` remains the explicit Math-canon route; ordinary `circle` still favours the exact Bible lexicon match.

**Parent:** v31 artifact, SHA-256 `bd16405f63035b06483eb259c11f43cfdf2f295104bc4d7b4362e8d883cab190`.

**Build:** 2026-10-04T12:41:38.000Z · 35,435,806 bytes · SHA-256 `3e7f30d68f5720855164a508c6ae40beb7fa292b89ad81ff19deed7ea51d7da7`.

The build is an exact pinned patch from the v31 generated app. All embedded data is unchanged: 44 Math entries, 172 title keys, and all other data slots. It retains v30's corrected Euclid source disclosure and formatted MATH card.

## Five checks for human testing

1. `math` → the MATH Mathematics card, not Strong's H4962.
2. `maths` → the same Mathematics card.
3. `tell me about math` or `define math` → the Mathematics card.
4. `math: circle` → the Euclid MATH card; plain `circle` → the Bible lexicon match.
5. `Strong's H4962` → the Hebrew lexicon entry remains directly available.

The matching modular source tree for v17 SUPER remains missing. v32 is an artifact-based test candidate, not a canonical release or a claim that the old modular repository reproduces v17.
