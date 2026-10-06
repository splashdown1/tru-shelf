# Human session audit — v40 (real machine, joe)

Date: 2026-10-06 · Artifact: `test-candidates/v40/TRU-v40.html` (sha `8c7df8f1…`) · Session: ~18 queries, live transcript reviewed against the artifact source.

## What worked (doctrine held)

- **Honest GAP, no reframing:** "should I eat people?", "I want to murder the moon", "are you gay?", "what the fuck" all → GAP with zero moralising and zero forced scripture. Out-of-canon boundary doctrine intact.
- Phrase search ("tell me about Jesus Christ" → 1co 1:1–3, top 3 of 206), Easton dictionary ("what is love?" → full 1897 entry), Strong's define ("define love", "define hope" clean), TRU_CORE identity/presence answers, memory (50 turns), OFFLINE badge.

## Verified data defects — Strong's lexicon block (14,088 entries parsed)

Found by inspecting the embedded lexicon in the artifact, not inferred from the session. These predate v40 (v40 is a byte-pinned patch of v39 that does not touch the lexicon).

| # | Defect | Count | Example |
|---|---|---|---|
| D1 | **Duplicated definition** — translit+definition block appears twice in `def`, second copy often space-stripped | 1,415 (10.0%: 1,000 H / 415 G) | H1: "awb a primitive word father… — chief, (fore-) father(-less), awb a primitive word father…" |
| D2 | **Empty `def`** — gloss lost, usage field still populated | 523 (3.7%: 403 H / 120 G) | G18 ἀγαθός, G165 αἰών, G109 ἀήρ, H4191 מוּת, H8598 תַּפּוּחַ |
| D3 | **KJV usage list contains bare `()` token** | 436 lists | G1537: "with(25x), ()" |
| D4 | **Adjacent duplicate usage tokens** | 41 lists | H8598: "apple tree, apple tree" |
| D5 | **Mangled short defs** — transliteration split on commas/hyphens, etymology cut to a bare "from" | 232 | H1323: "bath from bath from"; G932: "basile ' -ah from"; G71: "br ch ,brekh' -o" |

Session-visible impact: 2 of 7 define queries ("define kill", "define apple") displayed damaged cards — empty gloss (H4191, H8598), duplicated gloss (H5221, H2026), mangled gloss (H1323). This is a source-bound data-corruption issue, the worst class for this project: the engine is correctly quoting its data, and the data is wrong.

## Verified routing findings (code-inspected)

- **R1 (LOW):** "are you saved?" → GAP without a suggestion, while "are you straight?" suggested STRAIGHT and "where is heaven?" suggested HEAVEN. Cause: `typoSuggest()` requires a single bare word (`/^[a-z]{4,}$/`) so phrases never get lexicon suggestions; `topicTitleSuggest()` only covers Nave's titles ("STRAIGHT", "HEAVEN" are titles; "SAVED" is not). Design gap, not corruption — but "saved" is an indexed lexicon word, so the honest suggestion is reachable data.
- **R2 (MEDIUM, voice regression):** every GAP card repeats the full guidance line ("No canon match. Try a verse, a word, a Strong's number, or a phrase from Scripture."). No once-per-session gate exists in the artifact (no `gapShown`-like state). Doctrine: full guidance on first GAP only; subsequent GAPs get one quiet line. The session showed 11 GAP cards all carrying the full boilerplate.
- **R3 (MINOR):** voice fallback notice ("No recognizable female voice listed; using local voice Chrome OS US English 1") appeared twice in one session (reader boot + panel). Consistent with v15 F1 doctrine (Android voices intentionally not gender-guessed) but the message should appear once.

## Reproduction

```python
# parse the embedded lexicon from TRU-v40.html and count defects
import json, re
html = open('test-candidates/v40/TRU-v40.html', encoding='utf-8').read()
pat = re.compile(r'"([HG]\d+)":\{"lemma":')
# brace-match each entry body, json.loads, then:
#   dup  = definition block repeated (space-insensitive) after first " — "
#   empty= def.strip() == ""
#   paren= '"()"' or "()" inside kjv field
```

Counts above were produced 2026-10-06 against sha `8c7df8f1…`.

## Recommended priority

1. D2 empty defs on common words (define good → empty gloss is user-visible on the most common queries).
2. D1 duplication (10% of the corpus, visible on kill/love-adjacent words).
3. R2 GAP one-liner gate (voice doctrine).
4. D5, D3, D4 (cosmetic but source-bound).
5. R1 suggestion reach for indexed words inside phrases.
