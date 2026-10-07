# TRU Song v3 — spoken-reading test candidate

**Status:** public human-test candidate, not canonical and not a TRU SUPER release. This is a new immutable path based on Song v2.

- **Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/song-v3/
- **Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/song-v3/TRU-Song.html
- **Artifact:** 35,442,375 bytes; SHA-256 `d793bf35386266e7ee0e1c22f6645d3a8e5b253481a7d6334609f1e0ad426813`.
- **Change:** the spoken stream omits recognised KJV marginal-note markers (`Heb.`, `Gr.`, `or,`, and `that is,`) and their glosses. The displayed/source KJV text and embedded Bible data are unchanged; the reader indicates when a note was omitted from speech.
- **Verification:** across all 31,100 KJV verses, 6,443 verses contain one of those note markers; the speech filter removes all recognised markers and produces no empty utterances. The embedded KJV data block is byte-identical to v2. In a browser with a test voice, `tru start singing at psalms 23:6` speaks the verse ending `...for ever.` without saying “Heb.” or “to length of days.”

Song is genre-paced spoken reading, not melodic singing. Audible playback on a user's device depends on its installed browser speech voice; the browser test captures the speech text rather than producing real audio.
