from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = Path(__file__).with_name("question-quality-public-v1.0.jsonl")
DEFAULT_HTML = ROOT / "test-candidates" / "v39" / "TRU-v39.html"


def load_cases(path: Path, minimum_words: int = 5) -> list[dict[str, Any]]:
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    seen: set[str] = set()
    for case in cases:
        case_id = case["id"]
        if case_id in seen:
            raise ValueError(f"Duplicate case id: {case_id}")
        seen.add(case_id)
        words = re.findall(r"[\w]+(?:['’][\w]+)?", case["query"], flags=re.UNICODE)
        case["word_count"] = len(words)
        if len(words) < minimum_words:
            raise ValueError(f"Case {case_id!r} has only {len(words)} words; minimum is {minimum_words}: {case['query']}")
    return cases


def browser_results(html_path: Path, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    subprocess.run(["agent-browser", "open", html_path.resolve().as_uri()], check=True, capture_output=True, text=True)
    subprocess.run(["agent-browser", "wait", "500"], check=True, capture_output=True, text=True)
    payload = json.dumps([{"id": c["id"], "query": c["query"]} for c in cases], ensure_ascii=True)
    expression = (
        'JSON.stringify((()=>{'
        'if(typeof route!=="function")throw new Error("TRU route function is unavailable");'
        'if(typeof addTurn==="function")addTurn=()=>{};'
        'if(Array.isArray(HISTORY))HISTORY.length=0;'
        f'const cases={payload};'
        'return cases.map(c=>{const r=route(c.query)||{};'
        'const reply=String(r.reply||"").replace(/<[^>]*>/g," ").replace(/\\s+/g," ").trim();'
        'return {id:c.id,verdict:String(r.verdict||""),source:String(r.source||""),'
        'scripture_ref:String(r.scripture_ref||""),refs:Array.isArray(r.refs)?r.refs.map(String):[],'
        'nodes:Array.isArray(r.nodes_used)?r.nodes_used.map(n=>String(n.k||n)):[],reply:reply.slice(0,12000)};});'
        '})())'
    )
    result = subprocess.run(["agent-browser", "eval", expression], check=True, capture_output=True, text=True)
    text = result.stdout.strip()
    for _ in range(3):
        parsed = json.loads(text)
        if isinstance(parsed, str):
            text = parsed
            continue
        if not isinstance(parsed, list):
            raise ValueError("Browser returned a non-list result")
        return parsed
    raise ValueError("Could not decode browser result")


def evaluate(case: dict[str, Any], result: dict[str, Any]) -> tuple[str, list[str]]:
    if case.get("status") == "review":
        return "REVIEW", []
    checks = case.get("checks", {})
    failures: list[str] = []
    verdict = result["verdict"].upper()
    reply = result["reply"].casefold()
    evidence = " ".join([
        reply,
        result["source"].casefold(),
        result["scripture_ref"].casefold(),
        " ".join(result["refs"]).casefold(),
        " ".join(result["nodes"]).casefold(),
    ])
    allowed = checks.get("verdict_any")
    if allowed and verdict not in {value.upper() for value in allowed}:
        failures.append("unexpected verdict: " + verdict)
    forbidden = checks.get("verdict_none", [])
    if verdict in {value.upper() for value in forbidden}:
        failures.append("forbidden verdict: " + verdict)
    for term in checks.get("evidence_any", []):
        if not any(value.casefold() in evidence for value in term):
            failures.append("missing any evidence: " + " / ".join(term))
    for term in checks.get("reply_any", []):
        if not any(value.casefold() in reply for value in term):
            failures.append("missing reply wording: " + " / ".join(term))
    for term in checks.get("reply_none", []):
        if any(value.casefold() in reply for value in term):
            failures.append("forbidden reply wording: " + " / ".join(term))
    for sequence in checks.get("reply_order", []):
        positions = [reply.find(value.casefold()) for value in sequence]
        if any(position < 0 for position in positions):
            failures.append("missing ordered reply term: " + " before ".join(sequence))
        elif positions != sorted(positions):
            failures.append("reply terms are out of order: " + " before ".join(sequence))
    return ("FAIL", failures) if failures else ("PASS", [])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run TRU's five-plus-word question benchmark against a local HTML candidate.")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    parser.add_argument("--record", type=Path, help="Write the observed result snapshot to a new JSON file.")
    parser.add_argument("--minimum-words", type=int, default=5, help="Minimum query length (default: 5; use 1 for short-query suites).")
    args = parser.parse_args()
    if not args.html.is_file():
        parser.error(f"Candidate HTML not found: {args.html}")
    if args.record and args.record.exists():
        parser.error(f"Refusing to overwrite existing baseline: {args.record}")
    cases = load_cases(args.cases, args.minimum_words)
    results = browser_results(args.html, cases)
    by_id = {result["id"]: result for result in results}
    if len(by_id) != len(cases) or set(by_id) != {case["id"] for case in cases}:
        raise ValueError("Browser result ids do not match benchmark case ids")
    summary = []
    counts = {"PASS": 0, "FAIL": 0, "REVIEW": 0}
    for case in cases:
        result = by_id[case["id"]]
        status, failures = evaluate(case, result)
        counts[status] += 1
        summary.append({"id": case["id"], "words": case["word_count"], "status": status, "verdict": result["verdict"], "source": result["source"], "failures": failures})
        print(f"{status:6} {case['id']:<24} {case['word_count']:>2} words  {result['verdict']}")
        for failure in failures:
            print(f"       - {failure}")
    print(f"\n{len(cases)} cases: {counts['PASS']} pass, {counts['FAIL']} fail, {counts['REVIEW']} review")
    if args.record:
        artifact_hash = hashlib.sha256(args.html.read_bytes()).hexdigest()
        try:
            artifact_path = args.html.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            artifact_path = args.html.name
        document = {
            "benchmark": args.cases.stem,
            "artifact": artifact_path,
            "artifact_sha256": artifact_hash,
            "cases": [
                {"id": case["id"], "query": case["query"], "word_count": case["word_count"], "target_status": case.get("status", "target"), "observed": by_id[case["id"]]}
                for case in cases
            ],
            "summary": counts,
        }
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Recorded {args.record.resolve()}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        raise SystemExit(2)
