# TRU v23 test candidate

This is a public testing candidate, not a canonical release. The app is a single self-contained HTML file and runs offline after it is opened or downloaded.

Cut from the v21 candidate. v22 was left alone.

## What changed

- Hold-to-talk is refused. Browser speech recognition leaves the phone, so v23 does not construct `SpeechRecognition` or `webkitSpeechRecognition`.
- A hold on the mic control says listen is not packed. Type the ask.
- Speech out remains. The reader still uses the device's local `speechSynthesis` voice.
- The build label reads v23. Counts, lexicon, and verse data are the v21 pack.

## Candidate integrity

- File: `TRU-v23.html` — 35,028,585 bytes
- SHA-256: `cb577581769bbfadf6cf908385ce9996b360b1d337e3da22931633e590b1ee7a`
- Parent: v21 `d19abf7c089d739f7964e6b556d21abd8ffe154780c773cccb941d8b7fdfc9f9`
- Status: public test candidate; not a canonical release

## Not claimed

Audible speech was not verified on a device. The voice line still says when no named female or male voice is listed, and falls back to a local voice. That is a device limit, not a new pack.
