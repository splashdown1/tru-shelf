# TRU v29 test candidate

**Status:** Local audit build from public v28. Not pushed. Not a canonical release. Not a shelf lane.

**Parent:** splashdown1/tru-shelf `test-candidates/v28` commit `22bbea2f` (zocomputer, 2026-10-04T02:03:10Z).

**TRU Clock build timestamp:** `2026-10-04T02:20:00.000Z`

**SHA-256:** `d5db2b284e373fe6d6c364c337b1e6c7125d67dbec2bd9487e8cf6988e119f83`

**Size:** 35,435,236 bytes

`TRU-v29.html` and `index.html` are the same file.

## What v29 changes

Carries the v28 math canon (44 entries, 172 titles) and applies the audit fixes:

- G4102 KJV line now matches Blue Letter Bible total 244: faith 239, assurance 1, believe (with G1537) 1, belief 1, them that believe 1, fidelity 1.
- The seven v27 usage fields are marked `Abridged outline.` They are not full Thayer.
- G1680 `root` filled from the Strong's line already in `def`.
- `math:` prefix now forces the MATH card even when Strong's has the word.
- Bare `math` and `maths` stay off the math lane (scripture / gap path). `define mathematics` and `math: mathematics` still open Ray Art. 6–8.
- MATH now runs after the calculator, not before commands.
- Prime card keeps Ray's quote, including 1 as prime, and adds a source note that the modern definition excludes 1.

## Still open

- Usage fields are labeled, not expanded to full Thayer.
- Euclid figure-letter handling disagrees between the v28 README (kept) and the pack provenance (omitted). Quotes were not rewritten.
- Words with an exact Strong's hit still lose the bare and `define` forms: circle, square, point, line, division, addition, angle, plane, faith. Force with `math:`.
- 44 entries, not the 30 the v28 README counted.
- No network check was re-run in a browser for this local build.

## Live parent

https://splashdown1.github.io/tru-shelf/test-candidates/v28/
