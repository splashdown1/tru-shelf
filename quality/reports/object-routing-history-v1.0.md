# Object-routing history audit v1.0

**Audit date:** 2026-10-06 UTC<br>
**Parent snapshot:** public `splashdown1/tru-shelf` main at v38, commit `b91e3857b59e402022b3fe04d43281f08d25cc37`<br>
**Scope:** five object-definition queries tested against each public candidate v19–v38: 20 versions, 100 router observations. No app state was retained between candidate loads.

| Query | Identical result across v19–v38 | Assessment |
|---|---|---|
| `What is a chair?` | `DEFINE` from Thayer deep lexicon G2828, whose gloss incidentally contains “chair” | Misleading collision; not an exact English Bible-term entry |
| `What is a door?` | KJV phrase search for “a door” | Wrong route for a definition; exact local door entries exist |
| `Can you tell me what a chair is in Scripture?` | Generic `GAP` | Safe but needlessly broad; does not explain exact-term lookup found no match |
| `Can you tell me what a door is in Scripture?` | Generic `GAP` | Missed exact local door entries |
| `What is a harp?` | Easton’s Dictionary entry | Correct control; later routing must preserve it |

All 20 candidates behaved identically on this set. The five observations for each version are preserved in `object-routing-history-v1.0.json`; the v38/v39 five-case score reports are `object-routing-v38-v1.0.json` and `object-routing-v39-v1.0.json`.

v39 corrects the four chair/door behaviours without altering embedded source data: a direct single-term question uses the exact local term result when the initial route is a generic GAP, phrase-search noise, or an incidental deep-gloss collision. It leaves an already-relevant dictionary result intact. The focused fixture scores v38 1/5 and v39 5/5. The sanitised five-plus-word `question-quality-public-v1.0` pilot scores 28/28 target checks on both v38 and v39; its 3 review-only cases remain unscored.

The audit evaluated candidate query routing in an isolated browser context, not human interpretation of every source entry. These prompts are generic object-definition tests and include no personal identifiers. Public v39 UI smoke checks separately confirmed the door response cites H8179, the chair response is an explicit exact-match GAP, the longer door question resolves, and browser page errors are clear. See the versioned v39 human checks at `https://splashdown1.github.io/tru-shelf/test-candidates/v39/`.
