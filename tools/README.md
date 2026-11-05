# TRU Shelf Tools

Small, source-bound helpers for managing the public shelf.

## tru_shelf.py

Three verbs only:

| Command   | What it does                                                                 | Side effects                                      |
|-----------|------------------------------------------------------------------------------|---------------------------------------------------|
| `propose` | Creates a dated proposal under `proposals/` with description + current hashes | Writes new directory + files                      |
| `approve` | Records an explicit human approval stamp on an existing proposal             | Writes `APPROVED.md` only                         |
| `check`   | Verifies a proposal still matches the live tree (paths + SHA-256)            | Read-only; prints PASS / FAIL                     |

Nothing is applied automatically. The tool records intent and protects the audit trail. Application remains a deliberate later step (local git, Claude Code, or another session).

### Usage

```bash
# From the root of tru-shelf
python tools/tru_shelf.py propose "Short human description of the intended change"
python tools/tru_shelf.py approve proposals/2026-11-04-... "Looks good"
python tools/tru_shelf.py check proposals/2026-11-04-...
```

### Design rules (non-negotiable)

- Deterministic. Same inputs → same hashes.
- No network.
- No invention. If a path or hash is missing, it reports a gap.
- Single-file Python 3. No dependencies beyond the standard library.
- A gap stays a gap.

### Layout created by propose

```
proposals/
  2026-11-04-191500-short-slug/
    DESCRIPTION.md     # human text + timestamp
    MANIFEST.json      # paths + sha256 of the live files at propose time
    APPROVED.md        # written only by `approve`
```

### Status

First cut. 4 November 2026.
