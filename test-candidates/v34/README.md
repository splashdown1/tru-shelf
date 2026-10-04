# TRU v34 — light theme and control-layout test

**Status:** New versioned public test candidate; not a canonical release.

**Preview:** `https://splashdown1.github.io/tru-shelf/test-candidates/v34/`

**Direct app:** `https://splashdown1.github.io/tru-shelf/test-candidates/v34/TRU-v34.html`

## Changes from v33

- Adds a **LIGHT**/**DARK** toggle. Dark remains the default; the selected theme is saved on that device and restored on reload.
- Adds light-theme text and control colours with verified minimum contrast of 6.07:1 for the checked text pairs; both the opening summary and response cards use darker readable text.
- Separates Chair and TRU Portal on desktop. On narrow screens both controls move into a separate header row, instead of covering the conversation.
- Adds accessible names and descriptions: Chair searches the small offline survival-card and packed-place collection; TRU Portal shows lane, offline-runtime, source and build information.
- Updates both Portal build labels to v34.

## Human checks

1. Click **LIGHT** and confirm the background becomes pale with readable dark text; reload and confirm the choice sticks.
2. Click **DARK** and confirm the original black theme returns.
3. Check that Chair and TRU Portal do not overlap on desktop or a phone-sized screen.
4. Open Chair, search `salt` or `Mobile`, and confirm it returns only packed offline results (otherwise it says “Not packed”).
5. Open TRU Portal and confirm it shows the offline lanes and v34 build stamp.

The local browser smoke test passed in both themes. The controls were separate at desktop and phone sizes; the theme persisted; Chair and Portal opened; there were no browser errors. Human acceptance is still pending.

## Artifact

- Parent: v33 at commit `29d039cf88e9e200c2ced529284008b70cff7c24`, SHA-256 `84ad555375198d16588d9bec28ae2c3ff4140f205f620a5521f256a8698e2f08`.
- App size: 35,446,976 bytes.
- v34 SHA-256: `1de821af9d834ed53a7a5be7ff3cbc6f72f7e44fb471e7ab0b6d877c0d4dab93`.
- Build stamp: `2026-10-04T22:22:38.000Z`.

This is an artifact-based patch, not a build from the missing matching v17 modular source tree. It does not change TRU content, data or canonical releases.
