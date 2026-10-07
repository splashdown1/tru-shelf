# TRU Song v2 — spoken-reading test candidate

**Status:** public test candidate, not canonical. This is an immutable versioned path.

- **Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/song-v2/
- **Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/song-v2/TRU-Song.html
- **Artifact:** 35,441,325 bytes; SHA-256 `f3f84d226a1fb142c174bdc50ba9b6fb3f79bc1fb1cec14bc5e6fca4221418af`.
- **Lineage:** exact app artifact from `tru-shelf` commit `b6e63a1`; this separate path keeps the already-published v1 at `/test-candidates/song/` unchanged.

## Test

Enter `Tru start singing at Psalms 23`. Expected: TRU reports **“Song AUTO on — Starting the KJV at Psalms 23:1”**, the reader moves to Psalm 23:1, and the verse appears. `tru start reading at Psalms 23` should also start the reader. The pace indicator should identify Psalms as poetry. Existing `song on`, `song off`, `song status`, and `flat reading` commands remain available.

**Song is genre-paced spoken reading, not melodic singing.** Audible playback depends on a speech voice installed and available in the browser/device; without one the app reports read-along-only mode.
