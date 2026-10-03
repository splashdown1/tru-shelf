# TRU v25 test candidate

**Status:** Public versioned test candidate, not a canonical release. This adds only `test-candidates/v25/`; the Shelf homepage, Portal, Chair source and earlier releases are unchanged.

**TRU Clock build timestamp:** `2026-10-03T13:56:32.912Z` (UTC ISO string from `new Date().toISOString()`). Conversation state continues to use Unix-millisecond `Date.now()` marks.
**Local audit timestamp (TRU Clock):** `2026-10-03T14:07:39.036Z` (UTC ISO string).
**Public audit timestamp (TRU Clock):** `2026-10-03T14:07:39.036Z` (UTC ISO string).

## What changed

- v25 starts from the user-authored Chair app at `v24/TRU-v24.html`, including the latest in-page Chair fix from source commit `5cf8eb6` (source SHA-256 `97cab1436dc03bcca1ad1ac95d30a00c018941958b96e4b56e6a2a8639dfd5da`), not the separate `test-candidates/v24/` lineage.
- Preserves the user's newer non-popup Chair panel; it is verified with the packed `storm` card.
- Removed all three display caps from the DEEP BDB/Thayer paths (900, 900 and 700 characters). The full 1,034-character BDB H1814 entry now reaches “Ezek 24:10.”
- Removed the duplicated H1814 Strong’s gloss, leaving one source-checked definition: [Blue Letter Bible H1814](https://www.blueletterbible.org/lexicon/h1814/kjv/wlc/0-1).
- Phrase search still returns its three best matches, but now says how many matches exist. “woe unto them” reports “Showing the top 3 of 17 matches.”
- Both visible build badges identify v25 and use the ISO-UTC TRU Clock timestamp.
- Removed one inherited whitespace-only line from the test artifact to keep the new candidate diff clean; v24 source files remain unchanged.

## Verification

The workspace v25 builder and verifier pass. The verifier parses all 10 embedded JSON slots and all 14,088 LOGOS entries, checks the exact base hash and patch set, confirms the full H1814 BDB text and timestamp, and asserts all three DEEP truncation caps are gone.

Local Chromium smoke tests passed for `inflame`, direct `H1814`, `woe unto them`, and the Chair’s packed `storm` card. At 320 px there is no horizontal overflow; there are no browser errors or console messages. The app makes no external requests and remains offline. This test browser has no installed offline English voice, so audible speech was not verified.

- Artifact: `TRU-v25.html` and `index.html`, identical bytes
- Size: 35,405,059 bytes
- SHA-256: `72917d627e15b520a563df1841fc4805e4cc7f8b1d469a31d87c81305eca2c6e`
- Preview: https://splashdown1.github.io/tru-shelf/test-candidates/v25/
- Direct app: https://splashdown1.github.io/tru-shelf/test-candidates/v25/TRU-v25.html
