# TRU Song — spoken delivery test candidate

**Status:** test candidate, not canonical. Base: v28 Super (sha `cd22b3b57c…`) + TRU Song layer (sha `38f0e75959160ad1ac1905602ee6f632bf6223060cff1bfe0bbdf3362d7a8593`), 35,439,831 bytes, stamp 2026-10-06.

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/song/TRU-Song.html

## What it adds

- 66-book curated genre pacing map (law / narrative / poetry / prophecy / gospel / epistle → rate ×0.93–1.00 + verse gaps 350–950 ms). Classification is for pacing only — not source text, not interpretation.
- SONG AUTO / SONG FLAT toggle in the reader bar (AUTO default, persists via `tru_song_mode`). FLAT = previous flat delivery exactly.
- Voice commands: `song on`, `song off`, `song status`, `flat reading`.
- Portal panel Song section. `_RAINBOW` pitch path untouched (D1 pending).

## Test checklist (joe)

1. Pick a voice, press TEST VOICE.
2. Start the reader at Psalms (poetry pace: slower, more silence between verses), then Genesis (law/narrative: plain, shorter gaps).
3. Toggle SONG FLAT mid-read — delivery returns to uniform.
4. `song status` / `song off` / `song on` from the input line.
