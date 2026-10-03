# TRU v20 test candidate

This is a public testing candidate, not a canonical release. The app is a single self-contained HTML file and runs offline after it is opened or downloaded.

## What changed

- Open-ended discussion questions now offer supported ways to start.
- General mathematics no longer resolves to the Hebrew transliteration `maṯ`; explicit `strongs h4962` lookup remains available.
- Corrected H776’s duplicated definition and restored its missing `land (1,543x)` translation count.
- Repaired the displayed definitions for G1093, H4962, H6106, and G2222.
- Retains the v19 lexicon reconciliation and reviewed H7965 and G1515 corrections.

## Integrity

- File: `TRU-v20.html` — 35,029,095 bytes
- SHA-256: `43c4d52e969e1beeafffb4d1e49c605e3e85b2d6522af9c78bfddab2148042a5`

## Source references

- [H776 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/h776/kjv/wlc/0-1)
- [G1093 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/g1093/kjv/tr/0-1)
- [H4962 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/h4962/kjv/wlc/0-1)
- [H6106 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/h6106/kjv/wlc/0-1)
- [G2222 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/g2222/kjv/tr/0-1)
- [H7965 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/h7965/kjv/wlc/0-1)
- [G1515 — Blue Letter Bible](https://www.blueletterbible.org/lexicon/g1515/kjv/tr/0-1)

## Test notes

Local UI checks covered the discussion prompt, both general-mathematics phrasings, the explicit H4962 lookup, `word study earth`, and `tell me about life`. The embedded data verifier passed. Offline speech output remains device-dependent and was not verified on a device with a confirmed installed voice. The public candidate is isolated under a new versioned directory; the Shelf homepage and canonical releases are unchanged.
