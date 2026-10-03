# TRU v25 test candidate

**Status:** Historical public versioned test candidate; v26 is the current candidate for testing the merged query corrections. v25 is not a canonical release. The Shelf homepage, Portal, Chair source and earlier releases are unchanged.

**TRU Clock build timestamp:** `2026-10-03T13:56:32.912Z` (UTC ISO string from `new Date().toISOString()`). Conversation state continues to use Unix-millisecond `Date.now()` marks.
**Audit timestamp (TRU Clock):** `2026-10-03T21:19:56.171Z` (UTC ISO string from `new Date().toISOString()`).

## What changed

- v25 starts from the user-authored Chair app at `v24/TRU-v24.html`, including the latest in-page Chair fix from source commit `5cf8eb6` (source SHA-256 `97cab1436dc03bcca1ad1ac95d30a00c018941958b96e4b56e6a2a8639dfd5da`), not the separate `test-candidates/v24/` lineage.
- Preserves the user's newer non-popup Chair panel; it is verified with the packed `storm` card.
- Removed all three display caps from the DEEP BDB/Thayer paths (900, 900 and 700 characters). The full 1,034-character BDB H1814 entry now reaches “Ezek 24:10.”
- Removed the duplicated H1814 Strong’s gloss, leaving one source-checked definition: [Blue Letter Bible H1814](https://www.blueletterbible.org/lexicon/h1814/kjv/wlc/0-1).
- Phrase search still returns its three best matches, but now says how many matches exist. “woe unto them” reports “Showing the top 3 of 17 matches.”
- Both visible build badges identify v25 and use the ISO-UTC TRU Clock timestamp.
- Removed one inherited whitespace-only line from the test artifact to keep the new candidate diff clean; v24 source files remain unchanged.

## Verification

The workspace v25 builder and verifier pass their structural checks: all 10 embedded JSON slots and 14,088 LOGOS entries parse, the pinned base and patch set match, and the H1814 BDB text is complete with all three DEEP display caps removed. A later behavior audit found v25 did not carry forward the approved v22/v24 query fixes: `tell me about math` still suggested H4962, `define English` returned unrelated H853, and `define love` expanded into a full multi-source study. The v25 verifier did not test those routing behaviors. v26 merges the corrections while preserving v25's Chair, full DEEP text and phrase counts.

Local Chromium smoke tests passed for `inflame`, direct `H1814`, `woe unto them`, and the Chair’s packed `storm` card. At 320 px there is no horizontal overflow; there are no browser errors or console messages. The app makes no external requests and remains offline. This test browser has no installed offline English voice, so audible speech was not verified.

- Artifact: `TRU-v25.html` and `index.html`, identical bytes
- Size: 35,405,057 bytes
- SHA-256: `6d159689683051a6999f090835b89570200cce1c9834f2015605ad9ca67a7620`
- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v25/
- Direct app: https://splashdown1.github.io/tru-shelf/test-candidates/v25/TRU-v25.html
