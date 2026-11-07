#!/usr/bin/env python3
"""tru_shelf.py - TRU shelf intake: propose -> approve -> check.

The shelf stores only ESTABLISHED items. An item is established when it is
pinned to a full 40-hex commit SHA. Everything else stays in pending.json.
Everything falls under one pack-level timestamp (shelf.json["timestamp"]).
Stdlib only. Works offline.

  tru_shelf.py propose  --repo owner/name --sha <40hex> [--path P] [--note N] [--by WHO] [--file F]
  tru_shelf.py list     [--pending]
  tru_shelf.py approve  <id>            # moves pending -> shelf (needs pinned SHA)
  tru_shelf.py reject   <id> [--why W]
  tru_shelf.py check                    # audits the whole shelf; exit 1 on failure
Add, not just take: every item records who contributed it (--by).
"""
import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone

ROOT = os.environ.get("TRU_SHELF_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shelf"))
SHELF = os.path.join(ROOT, "shelf.json")
PENDING = os.path.join(ROOT, "pending.json")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
VERSION = "1.0.0"

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)

def new_shelf():
    return {"schema": "tru-shelf", "version": VERSION, "timestamp": now(), "items": []}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def item_id(repo, sha, path):
    return hashlib.sha256(f"{repo}@{sha}:{path}".encode()).hexdigest()[:12]

def problems(item):
    out = []
    if not REPO_RE.match(item.get("repo", "")):
        out.append("repo must look like owner/name")
    if not SHA_RE.match(item.get("sha", "")):
        out.append("sha must be a full 40-hex commit SHA (branches/tags/short SHAs are not established)")
    if not item.get("contributed_by"):
        out.append("contributed_by is required")
    if item.get("id") != item_id(item.get("repo", ""), item.get("sha", ""), item.get("path", "")):
        out.append("id does not match repo+sha+path")
    return out

def cmd_propose(a):
    item = {"repo": a.repo, "sha": a.sha.lower(), "path": a.path or "", "note": a.note or "",
            "contributed_by": a.by, "proposed_at": now()}
    item["id"] = item_id(item["repo"], item["sha"], item["path"])
    if a.file:
        item["file_sha256"] = sha256_file(a.file)
    shelf = load(SHELF, new_shelf())
    pend = load(PENDING, [])
    if any(i["id"] == item["id"] for i in shelf["items"] + pend):
        print(f"already known: {item['id']}"); return 0
    pend.append(item); save(PENDING, pend)
    msgs = problems(item)
    print(f"proposed {item['id']}" + (f"  (not yet approvable: {'; '.join(msgs)})" if msgs else ""))
    return 0

def cmd_list(a):
    data = load(PENDING, []) if a.pending else load(SHELF, new_shelf())["items"]
    for i in data:
        print(f"{i['id']}  {i['repo']}@{i['sha'][:10]}  {i.get('path','')}  by {i['contributed_by']}")
    print(f"{len(data)} item(s)")
    return 0

def cmd_approve(a):
    pend = load(PENDING, [])
    hit = [i for i in pend if i["id"] == a.id]
    if not hit:
        print("no such pending id", file=sys.stderr); return 1
    item = hit[0]; msgs = problems(item)
    if msgs:
        print("refused: " + "; ".join(msgs), file=sys.stderr); return 1
    shelf = load(SHELF, new_shelf())
    item["approved_at"] = now()
    shelf["items"].append(item)
    save(SHELF, shelf)
    save(PENDING, [i for i in pend if i["id"] != a.id])
    print(f"established {a.id}")
    return 0

def cmd_reject(a):
    pend = load(PENDING, [])
    if not any(i["id"] == a.id for i in pend):
        print("no such pending id", file=sys.stderr); return 1
    save(PENDING, [i for i in pend if i["id"] != a.id])
    print(f"rejected {a.id}" + (f": {a.why}" if a.why else ""))
    return 0

def cmd_check(a):
    shelf = load(SHELF, None)
    if shelf is None:
        print("no shelf yet"); return 0
    bad, seen = 0, set()
    if not shelf.get("timestamp"):
        print("FAIL pack-level timestamp missing"); bad += 1
    for i in shelf["items"]:
        msgs = problems(i)
        if not i.get("approved_at"):
            msgs.append("missing approved_at")
        if i["id"] in seen:
            msgs.append("duplicate id")
        seen.add(i["id"])
        for m in msgs:
            print(f"FAIL {i.get('id','?')}: {m}"); bad += 1
    print(f"{len(shelf['items'])} item(s), {bad} problem(s)")
    return 1 if bad else 0

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("propose"); x.add_argument("--repo", required=True); x.add_argument("--sha", required=True)
    x.add_argument("--path"); x.add_argument("--note"); x.add_argument("--by", default="unknown"); x.add_argument("--file")
    x.set_defaults(f=cmd_propose)
    x = s.add_parser("list"); x.add_argument("--pending", action="store_true"); x.set_defaults(f=cmd_list)
    x = s.add_parser("approve"); x.add_argument("id"); x.set_defaults(f=cmd_approve)
    x = s.add_parser("reject"); x.add_argument("id"); x.add_argument("--why"); x.set_defaults(f=cmd_reject)
    x = s.add_parser("check"); x.set_defaults(f=cmd_check)
    a = p.parse_args(); sys.exit(a.f(a))

if __name__ == "__main__":
    main()
