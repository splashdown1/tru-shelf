# TRU v30 human-test candidate

**Status:** New versioned public test candidate. Not canonical; not a Shelf lane.

**Preview:** https://splashdown1.github.io/tru-shelf/test-candidates/v30/

**Direct app:** https://splashdown1.github.io/tru-shelf/test-candidates/v30/TRU-v30.html

**Change:** Correct the Euclid source disclosure and render the escaped MATH card markup as a formatted card. This is an artifact-based variant of v29; it does not claim to rebuild v17 from the missing modular source tree.

**Parent artifact:** v29, SHA-256 `d5db2b284e373fe6d6c364c337b1e6c7125d67dbec2bd9487e8cf6988e119f83`.

**Build stamp:** `2026-10-04T03:58:15.000Z`.

**Artifact:** 35,435,836 bytes; SHA-256 `df6fcf9f8756a77ba6b5971b49a3ac1ccf0218caea4399ee3468dcd5df4f9c42`.

## Source audit

The embedded provenance previously said that Euclid figure-letter references were omitted wherever they referred to diagrams. Casey's 1885 Book I does not support that blanket statement: Definition XIII retains `BAC`, `CAD`, `BA`, and `AD`; Definitions XXXIII–XXXIV include `CD` and `AB` examples that the app excerpt omits; Axiom XII has parenthetical labels `(AB, CD)`, `(AC)`, `(BAC, ACD)` that the app excerpt also omits. The app does not include the printed diagrams.

v30 describes this mixed treatment in the pack metadata and in each Euclid MATH card. It leaves the 44 entries, 172 title keys, quoted entry text, Ray prime note, and all other data unchanged. It also adds `html: true` to the already-escaped MATH response so the formatted card renders instead of exposing literal `<div>` tags.

Primary source: [Project Gutenberg eBook 21076, First Six Books of the Elements of Euclid](https://www.gutenberg.org/cache/epub/21076/pg21076-images.html), especially Book I Definitions XIII and XXXIII–XXXIV and Axiom XII.

## Human checks

1. Ask `math: supplements`. Confirm the definition still includes `BAC`, `CAD`, `BA`, and `AD`, and that the source note is readable beneath it.
2. Ask `math: radius` and `math: axioms`. Confirm the same disclosure explains which figure labels were omitted and no HTML tags appear literally.
3. Ask `john 3:16` and `2+2`. Confirm scripture and calculator routing remain intact.
4. For ambiguous word lookups, the `math:` prefix is still required when a term also has a Strong's entry.

## Inherited limitations

- Thayer usage fields remain labeled abridgements, not full Thayer entries.
- A term with an exact Strong's hit may resolve through the lexicon unless the query starts with `math:`.
- The modular source tree matching canonical v17 remains missing; v30 is reproducibly derived from the v29 artifact.
- Human testing is still required; this README records expected checks, not user-test results.
