# TRU v22 test candidate

**Status:** Public versioned test candidate; not a canonical release. The TRU Shelf homepage, existing lanes and release files are unchanged.

## What changed

- `define` now returns a concise glossary result from exact Strong’s English/lemma matches. `word study` retains the expanded lexicon, Nave topic, Easton and Thayer material.
- Single-word `define` and `word study` lookups no longer fall through to broad definition-text matching. An unsupported ordinary word returns an explicit gap instead of an unrelated Strong’s record.
- Source-checked H157, G25 and G26 definitions and KJV counts against Blue Letter Bible. G26 no longer claims “unconditional love” or a lexical opposition to *philia* and *eros*.
- Restored Nave’s Love heading “OF MAN FOR JESUS” from the scanned original. Dotted “See” markers now render as See references; dotted list entries render as bullets.
- Corrected the opening quotation mark in Easton’s Love entry and repaired the malformed opening of Thayer’s G26 entry from the source text. Other original source punctuation is retained.
- Voice status reports the local English voice count and actual AUTO/selected voice. A gender button is described as a preference when the installed voice name does not identify gender.
- Retains the mathematics boundary, explicit H4962 lookup, earlier lexicon corrections, and voice-list refresh when voices arrive.

## Browser checks

Passed in the local browser, offline, with no console errors:

- `define love` returns only the three concise exact glossary matches H157, G25 and G26; it does not append Easton, Thayer or Nave material and does not claim “unconditional” love.
- `word study love` retains the expanded entry, topic, Easton text and Thayer text.
- `topic: love` shows “OF MAN FOR JESUS”, clean See references and readable list bullets; no `0F` or `.See` remains in the Love result.
- `define English` and `word study English` return a no-match gap, not an unrelated Strong’s result.
- `define Strong's H157` is concise; `word study Strong's H157` returns the expanded BDB entry.
- `define math` and `tell me about math` remain outside TRU’s Bible sources; `what should we discuss?` does not suggest maths; an explicit Strong’s H4962 lookup remains available.
- Voice status was tested with a simulated installed voice and accurately reported AUTO’s selected voice and the unmatched gender preference. This test browser exposed zero local English voices, so audible speech still needs testing on a device with a confirmed voice.

## Source checks

- Strong’s H157: [Blue Letter Bible](https://www.blueletterbible.org/lexicon/h157/kjv/wlc/0-1)
- Strong’s G25: [Blue Letter Bible](https://www.blueletterbible.org/lexicon/g25/kjv/tr/0-1)
- Strong’s G26 and Thayer: [Blue Letter Bible](https://www.blueletterbible.org/lexicon/g26/kjv/tr/0-1)
- Nave’s Love heading: [digitised original, 1903 scan OCR](https://archive.org/download/navestopicalbibl00nave/navestopicalbibl00nave_djvu.txt), around lines 136633–136637. It reads “OF MAN FOR JESUS”.
- Easton’s Love entry: [Bible Study Tools](https://www.biblestudytools.com/dictionaries/eastons-bible-dictionary/love.html). The comma after “Trench:” is present in that source and was retained; only the quotation mark was corrected to an opening mark.

## Rebuild and verify

From `v18-rebuild/`, run `python3 build_v22.py` and `python3 verify_v22.py`. The builder verifies the pinned v21 base before creating this artifact. The verifier checks the source-backed field changes, unchanged lexicon record count and absence of unrelated data edits.

- **Artifact:** `TRU-v22.html` — 35,033,186 bytes
- **SHA-256:** `6a2a2c4e9ada272b3af128d21b2152e57cce4d7fa855500f41a06d3b5d4bea01`
