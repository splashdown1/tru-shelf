# TRU v33 human-test candidate

**Status:** New versioned public test candidate. Not canonical and not a Shelf lane.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v33/
**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v33/TRU-v33.html

## Change

The earlier `thoughts about forgiveness` query returned a GAP. v33 fixes the red-letter query adapter to read the bundled index's nested book/chapter/verse map, then adds a focused, source-backed “WORDS OF JESUS • FORGIVENESS” card for direct forgiveness prompts. It includes ten KJV quotations or excerpts across six passages marked as Jesus’ words: Matthew 6:14–15; Matthew 18:22; Mark 11:25; Luke 17:3–4; Luke 23:34; and Luke 7:47–48, 50. Luke 23:34 is shown as the speech-only excerpt “Father, forgive them; for they know not what they do,” excluding the verse’s narrator text. No paraphrase is added. Verse references are clickable and open the local KJV text.

The same card appends to `word study forgiveness`; it does not replace the existing LOGOS lexicon, Nave/Torrey topic, dictionary or deep-entry material. This is a focused forgiveness route, not a general doctrinal-answer system.

## Test these five inputs

1. `msgs from Christ about forgiveness` — expect the six-passage quotation card.
2. `thoughts about forgiveness` — same card.
3. `word study forgiveness` — existing word study first, then the quotation card.
4. `what did Jesus say about mercy` — check the repaired general red-letter query path.
5. `thoughts about money` — should remain a GAP; the new route must not swallow unrelated questions.

Click a verse reference in the card to confirm it opens the matching local KJV verse.

## Build and verification

- Parent: v32 artifact, SHA-256 `3e7f30d68f5720855164a508c6ae40beb7fa292b89ad81ff19deed7ea51d7da7`.
- v33 app: 35,441,403 bytes; SHA-256 `84ad555375198d16588d9bec28ae2c3ff4140f205f620a5521f256a8698e2f08`.
- The verifier checks all ten references against the bundled KJV and compressed local red-letter index, checks the Luke 23:34 excerpt against its exact KJV text, and confirms all embedded source data is unchanged.
- The matching v17 SUPER modular source remains unavailable. v33 is an honestly labelled, pinned artifact-based test candidate, not a recovered-source build.
