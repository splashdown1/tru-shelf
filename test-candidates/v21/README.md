# TRU v21 test candidate

This is a public testing candidate, not a canonical release. The app is a single self-contained HTML file and runs offline after it is opened or downloaded.

## What changed

- Open-ended discussion questions now offer supported starting points.
- General mathematics no longer resolves to Hebrew H4962; an explicit `strongs h4962` request still returns the lexicon entry.
- Corrected the damaged or incomplete definitions recorded in the v20 source notes: H776, G1093, H4962, H6106 and G2222.
- Refreshed the idle Bible-reader status when local voices appear, without overwriting active or paused verse progress.

## Candidate integrity

- File: `TRU-v21.html` — 35,029,246 bytes
- SHA-256: `d19abf7c089d739f7964e6b556d21abd8ffe154780c773cccb941d8b7fdfc9f9`
- Status: public test candidate; not a canonical release

## Verification

The v21 verifier passes the inherited v18–v20 integrity and data checks. Browser tests confirm the mathematics boundary, the explicit H4962 lookup, and the delayed-voice status refresh. The voice-refresh test uses a simulated locally installed voice; audible speech has not been verified on a device with a confirmed offline voice.

The candidate occupies its own versioned path. The TRU Shelf homepage, existing lanes and canonical release files are unchanged.
