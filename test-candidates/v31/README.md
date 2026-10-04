# TRU v31 human-test candidate

**Status:** New versioned public test candidate. Not canonical; not a Shelf lane.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v31/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v31/TRU-v31.html

**Parent:** v30, SHA-256 `df6fcf9f8756a77ba6b5971b49a3ac1ccf0218caea4399ee3468dcd5df4f9c42`.

**Build:** 2026-10-04T04:33:14.000Z UTC · 35,436,254 bytes · SHA-256 `bd16405f63035b06483eb259c11f43cfdf2f295104bc4d7b4362e8d883cab190`.

## Change

v30 human testing found that bare `math` resolved to Hebrew Strong’s H4962, which is unrelated to general mathematics. v31 adds a small scope guard for unqualified `math` / `maths` requests and common question forms. The reply states that general mathematics is outside TRU’s offline Bible sources and points to relevant Scripture help; it does **not** suggest H4962.

The guard runs before generic routing. Explicit `math:` queries, the Math canon title `mathematics`, and explicit Strong’s lookups remain available. All app data and the v30 Euclid source-disclosure note are unchanged.

## Five human checks

1. Enter `math`. Expect the general-mathematics scope reply, not a Strong’s card.
2. Enter `tell me about math`. Expect the same reply, with no H4962 suggestion.
3. Enter `math: circle`. Expect the Euclid MATH card with the v30 source note.
4. Enter `define mathematics`. Expect the existing Math canon entry.
5. Enter `Strong’s H4962`. Expect the explicit Hebrew lexicon entry.

Unqualified collisions such as `circle` still resolve through the Bible lexicon; use `math:` for the Math canon. This is a human-test candidate, not a canonical release. The matching modular source tree for v17 SUPER remains missing; v31 is a pinned artifact-based patch from v30.
