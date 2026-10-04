# TRU v28 test candidate

**Status:** Public, versioned test candidate; not a canonical release. It supersedes v27 for testing the new MATH canon lane. The Shelf homepage, Portal, Chair source and canonical releases are unchanged.

**TRU Clock build timestamp:** `2026-10-04T02:02:28.010Z` (UTC ISO string from `new Date().toISOString()`). Conversation-state timestamps are unchanged local behaviour.

**SHA-256:** `cd22b3b57c4782ca6a2ce9436d992809ea37cdfee70f9331e0d15f48229a4318`

## What v28 adds — MATH canon lane

A source-bound mathematics lane, same doctrine as the rest: quoted text only, provenance on every card, honest GAP outside it.

**Sources (both public domain):**

1. **Ray's New Higher Arithmetic** (Joseph Ray, Cincinnati: Van Antwerp, Bragg & Co., 1880) — definitions and numbered Principles of the four operations (Arts. 51, 53, 59–60, 72–76), number theory (Art. 91: integer, prime, composite, prime to each other, even, odd, perfect, imperfect, divisor, multiple, prime factor), common divisor (Art. 97), greatest common divisor (Art. 98), factoring (Art. 92), least common multiple (Art. 102), and the introduction (Arts. 2, 6–7: quantity, mathematics and its elementary branches). Source text: archive.org item `raysnewhigherari00rayjrich` (djvu OCR); obvious OCR slips corrected by hand against the same text (e.g. "TJie"→"The", "whicliever"→"whichever"). No other edits.
2. **Euclid, Elements, Book I** — ed. John Casey, Dublin, 1885 (Project Gutenberg #21076) — Definitions i–xxxiv (point, line, straight line, surface, plane, plane figure, angle and its kinds, triangle kinds, polygon kinds, circle and its parts), Postulates i–iii, Axioms i–xii. Figure-letter references ("as A", "such as AB") kept verbatim; they refer to the printed book's figures.

Both `README.md` provenance records and per-card citation lines are stored in the file. Every MATH card quotes only, and names its article/definition.

## Lane law (route order unchanged)

- MATH fires after the Bible reader/commands/calculator gate and **only** on exact whole-query matches against the math title index.
- A `define X` / `what is X` form yields MATH **only when X has no exact Strong's entry** — existing scripture canon is never narrowed (`define circle`, `define square`, `define point`, `define division` all still return Strong's).
- Explicit prefix `math: <term>` (mirrors `topic:`) forces the MATH card.
- Bare terms that used to GAP (`prime number`, `greatest common divisor`, `gcd`, `lcm`, `axioms`, `postulates`, `hypotenuse`, `perfect number`, …) now return MATH.
- Bare `math` stays Strong's H4962 (מַת) — scripture first, as before.
- `define mathematics` now returns Ray's Art. 6–7 instead of the old TRU_CORE refusal. Arithmetic itself stays in the CALC lane (local, deterministic).
- GAP stays a gap: anything not in the canon (calculus, algebra methods, statistics) is still not packed.

## Pack stats

- 30 canon entries (24 Ray's arithmetic, 6+6 Euclid geometry groups incl. postulates and axioms).
- Zero network requests at runtime (verified). Zero console errors (verified).

## Regression sweep (all verified live)

`define mathematics`, `axioms`, `hypotenuse`, `math: multiplication`, `prime number`, `greatest common divisor`, `perfect number` → MATH with citation; `define circle`/`square`/`point`/`faith` → DEFINE unchanged; `12 times 12`, `45% of 100`, `divide 100 by 4` → CALC unchanged; `john 3:16` → SCRIPTURE unchanged; `topic: prayer` → TOPICAL unchanged; Chair panel, reader, memory, GAP paths unchanged.

**Live:** https://splashdown1.github.io/tru-shelf/test-candidates/v28/ and https://splashdown1.github.io/tru-shelf/test-candidates/v28/TRU-v28.html
