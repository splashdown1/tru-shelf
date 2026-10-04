# TRU v27 test candidate

**Status:** Public, versioned test candidate; not a canonical release. It supersedes v26 for testing the lexicon source corrections. The Shelf homepage, Portal, Chair source and earlier candidates are unchanged.

**TRU Clock build timestamp:** `2026-10-04T01:13:41.139Z` (UTC ISO string from `new Date().toISOString()`). Conversation-state timestamps remain Unix milliseconds from `Date.now()`.
**TRU Clock audit timestamp:** `2026-10-04T01:15:40.000Z` (the audit pass that found and corrected the seven records).

## What changed

The v26 audit found seven LOGOS lexicon records whose `def` and `usage` fields carried editorial summaries and doctrinal claims presented as lexicon text — the same defect class v22 fixed for G26. The v26 merge carried the v22 query fixes but not these data fields. v27 replaces them with source-checked text and leaves every other byte of the v26 pack alone:

- **G5485 (grace)** — was "Grace, favor, kindness, gratitude. Unmerited favor of God toward sinners; free gift of salvation" / "Key Pauline term for God's free, unearned favor". Now quotes Strong's definition and the Thayer outline of biblical usage; KJV count line checked (grace 130x, favour 6x, thanks 4x, thank 4x, thank with G2192 3x, pleasure 2x, misc 7x — total 156x).
- **G4102 (faith)** — was "Faith, trust, belief, fidelity, assurance. Moral conviction… reliance upon Christ for salvation" / "Central NT term for saving faith". Now quotes Strong's definition and the Thayer outline; KJV counts added (faith 239x, assurance 1x, belief 1x, fidelity 1x — total 244x).
- **G1680 (hope)** — was "Confident expectation of good, especially future salvation and resurrection" / "Christian hope is certain, grounded in God's promises". Now quotes Strong's definition and the Thayer outline; KJV counts checked (hope 53x, faith 1x — total 54x).
- **H3176 (yâchal), H8615 (tiqwâ), H7663 (sâbar), H8431 (tôwcheleth)** — the hope/wait set carried editorial "To wait, to hope…" summaries and usage commentary ("A major OT word for hope"). Now quote Strong's definitions and the BDB outline of biblical usage; KJV counts added (H3176: hope 22x, wait 12x, tarry 3x, trust 2x, variant 2x, stayed 1x; H8615: hope 23x, expectation 7x, line 2x, the thing that I long for 1x, expected 1x; H7663: hope 3x, wait 2x, view 2x, tarry 1x; H8431: hope 6x).

The `grace of god` note in the doctrinal phrase map was reviewed and left alone: it is labelled `tier: curated`, which is the honest place for an interpretive line.

## Verification

- All 10 embedded JSON slots and 14,088 LOGOS records parse. The seven records are the only lexicon bytes changed; the byte diff touches no other record.
- Browser-tested offline, no page errors, no console messages, zero external requests: `define grace`, `word study grace`, `define faith`, `word study faith`, `define hope`, `word study hope`, `strongs g5485`, `strongs g4102`, `strongs g1680`, `strongs h3176`, `strongs h8615`, `strongs h7663`, `strongs h8431`.
- Regression sweep unchanged from v26: `define love`, `word study love`, `define English`, `word study English`, `tell me about math`, `strongs h4962`, `inflame`, `woe unto them` (top 3 of 17), `genesis 1:1`, `luke 1:81` (honest not-found), `read at zorak 2:4` (honest not-found), `read at john 3` + `next verse` + `where am i`, `45% of 100`, `remember:`/`recall:` round trip, `lords prayer`, `10 commandments`, `jesus life`, `capital of france` (core boundary), Chair `storm` card and Chair `grace` miss (`Not packed.`), complete 1,034-character BDB H1814 text ending `Ezek 24:10`.

## Sources

- G5485: [Blue Letter Bible — Strong's G5485](https://www.blueletterbible.org/lexicon/g5485/kjv/tr/0-1)
- G4102: [Blue Letter Bible — Strong's G4102](https://www.blueletterbible.org/lexicon/g4102/kjv/tr/0-1)
- G1680: [Blue Letter Bible — Strong's G1680](https://www.blueletterbible.org/lexicon/g1680/kjv/tr/0-1)
- H3176: [Blue Letter Bible — Strong's H3176](https://www.blueletterbible.org/lexicon/h3176/kjv/wlc/0-1)
- H8615: [Blue Letter Bible — Strong's H8615](https://www.blueletterbible.org/lexicon/h8615/kjv/wlc/0-1)
- H7663: [Blue Letter Bible — Strong's H7663](https://www.blueletterbible.org/lexicon/h7663/kjv/wlc/0-1)
- H8431: [Blue Letter Bible — Strong's H8431](https://www.blueletterbible.org/lexicon/h8431/kjv/wlc/0-1)
- BDB outlines for the four Hebrew records cross-checked against the embedded BDB payload in the file itself.

## Artifact

- `TRU-v27.html` and `index.html` are byte-identical.
- Size: 35,409,887 bytes
- SHA-256: `8b8435cfdedd2852dc56cc5e13b664dc54ade5c64ec9f56229493bd965d179ce`
- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v27/
- Direct app: https://splashdown1.github.io/tru-shelf/test-candidates/v27/TRU-v27.html
