# TRU v35 — exact lexical lookup test

**Status:** New versioned public test candidate; not a canonical release.

**Preview:** `https://splashdown1.github.io/tru-shelf/test-candidates/v35/`

**Direct app:** `https://splashdown1.github.io/tru-shelf/test-candidates/v35/TRU-v35.html`

## Change from v34

A bare one-word lexical search now requires an exact key in the local Strong's indexes. It no longer matches a word merely because it appears somewhere in another entry's gloss or usage. This closes the false positive where `English` returned Hebrew H853 because that entry's gloss says “unrepresented in English”. The explicit `Strong's H853` lookup is unchanged.

No lexicon, KJV, topical, dictionary or Math data changed. Other routes, including `math` and the exact `love` match, are preserved.

## Human checks

1. Search `English` — expect a clear GAP, not H853.
2. Search `define English` — expect the same exact-match GAP.
3. Search `Strong's H853` — expect the explicit Hebrew entry.
4. Search `love` — expect the existing exact Strong's matches.
5. Search `math` and `circle` — expect Math Mathematics and Hebrew H2329 respectively.

## Artifact

- Parent: v34 at commit `19a02a87509c40cdd10b8511c6fa37ad1b101240`, SHA-256 `1de821af9d834ed53a7a5be7ff3cbc6f72f7e44fb471e7ab0b6d877c0d4dab93`.
- App size: 35,447,067 bytes.
- v35 SHA-256: `c738c0d3fc305f523a3f34da1ae1381c0fc618e47319dd88ed96041ac42b09f3`.
- Build stamp: `2026-10-05T10:16:11.000Z`.

This is an artifact-based patch, not a build from the missing matching v17 modular source tree. It does not alter the Shelf homepage or canonical releases.
