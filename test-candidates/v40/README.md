# TRU v40 — Scripture teaching shelf

**Status:** new versioned public human-test candidate; not canonical.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v40/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v40/TRU-v40.html

## What changed from v39

v40 adds a browser-local teaching shelf for up to 500 exact question-and-answer entries. It is empty on first use; this release does **not** preload or invent 500 answers.

Teach an entry in the app's input line using:

```text
remember: scripture: <question> = <brief answer> | <KJV verse>; <another KJV verse>
```

Example:

```text
remember: scripture: How can I find hope? = Hope is anchored in God's promise. | Romans 15:13; Hebrews 6:19
```

TRU checks each reference against its local KJV, then shows your wording beside the exact quoted verses. Use one to five individual verse references separated by semicolons; verse ranges are not accepted. To list entries, ask `scripture answers`. To remove one, use `forget: scripture: <question>`. The ordinary `export` command downloads the brain and local overlay, including these entries; `reset` clears the overlay.

A taught answer is returned only when the saved question matches after case and punctuation are normalised. TRU does not guess paraphrases; add the alternate wording as another entry if you want it matched. References and quoted text are checked locally, but the answer and its interpretation are user-supplied and are **not** independently evaluated for theological accuracy.

These entries are saved in that browser's local memory, not embedded in the public HTML or shared with other users. Export your overlay if you want a backup.

## Human checks

1. Teach the hope example above; expect `MEMORY`, a saved count such as `1/500`, and the two locally checked citations.
2. Ask `How can I find hope` with changed punctuation or capitalisation; expect the taught answer, followed by the complete KJV text for Romans 15:13 and Hebrews 6:19.
3. Ask the same question with a substantially different paraphrase; it should not silently reuse the teaching. Add the paraphrase as a separate question if wanted.
4. Try to teach an invalid reference such as `John 999:999`; expect `No answer stored`.
5. Ask `scripture answers`; confirm the question is listed, then remove it with `forget: scripture: How can I find hope?`.
6. Use `remember: favourite_hymn = ...` to confirm ordinary personal memory remains available.
7. Confirm all ordinary Bible lookup, Hebrew/Greek lexical priority, chair/door routing, and Easton harp answers still work.

## Automated checks

- Scripture-teaching v1.0: 8/8 sequential checks pass, covering citation rejection, save/lookup/list/remove, and ordinary memory compatibility.
- Capacity check: the 500th distinct entry is accepted; a 501st is refused; an existing entry can still be updated.
- Five-plus-word question pilot: v40 passes all 28 scored targets; 3 review cases remain unscored pending human judgement.
- Object-routing v1.0: v40 passes 5/5.
- The deterministic verifier confirms the v39 parent hash and all 11 embedded data blocks unchanged.
- A real local-browser input test saved and retrieved a two-verse answer.

## Artifact and lineage

- Parent v39 SHA-256: `be82106355cf5848f1533df0c8cc216f505d1ad03bf622e2a98b4a8812e66ebb`.
- App size: 35,467,822 bytes.
- v40 SHA-256: `8c7df8f1b79efc5dee5ff8ac6863043d726444ccfd965343b4ab6d4d26fdefad`.
- Build stamp: `2026-10-06T13:36:27.000Z`.

This artifact-based candidate does not reproduce v17 from the still-missing matching modular source tree. It is added only at the new `test-candidates/v40/` path; the Shelf homepage, earlier candidates, and canonical files are unchanged.
