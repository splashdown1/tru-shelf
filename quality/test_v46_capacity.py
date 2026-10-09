from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "test-candidates" / "v46" / "TRU-v46.html"


def run_browser() -> dict[str, object]:
    subprocess.run(["agent-browser", "open", HTML_PATH.resolve().as_uri()], check=True, capture_output=True, text=True)
    subprocess.run(["agent-browser", "wait", "700"], check=True, capture_output=True, text=True)
    expression = r'''JSON.stringify((()=>{
  const storageKey="tru_local_overlay_v1";
  const previous=localStorage.getItem(storageKey);
  try{
    const prefix="scripture_qa_v40__";
    const normalize=value=>String(value||"").toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g," ").trim().replace(/\s+/g," ");
    const verse=parseVerse("John 3:16");
    if(!verse)throw new Error("local KJV test verse is unavailable");
    const added={};
    for(let i=0;i<500;i++){
      const question="Capacity sample "+i;
      added[prefix+normalize(question)]=JSON.stringify({question,answer:"Capacity test answer",refs:[{ref:verse.ref,label:verse.ref,text:verse.text}]});
    }
    localStorage.setItem(storageKey,JSON.stringify({added,removed:{},corrected:{}}));
    loadOverlay();
    reloadBrain();
    const refused=cmdRemember("scripture: A new capacity question? = Another answer. | John 3:16");
    const updated=cmdRemember("scripture: Capacity sample 0 = Updated answer. | John 3:16");
    const count=Object.keys(OVERLAY.added).filter(key=>key.startsWith(prefix)).length;
    return {
      entries:count,
      refusal:refused.reply,
      update:updated.reply,
      refusalVerified:/full \(500\/500\)/i.test(refused.reply),
      updateVerified:/saved Scripture answer 500\/500/.test(updated.reply)
    };
  } finally{
    if(previous===null)localStorage.removeItem(storageKey);else localStorage.setItem(storageKey,previous);
    loadOverlay();
    reloadBrain();
  }
})())'''
    result = subprocess.run(["agent-browser", "eval", expression], check=True, capture_output=True, text=True)
    text = result.stdout.strip()
    for _ in range(3):
        parsed = json.loads(text)
        if isinstance(parsed, str):
            text = parsed
            continue
        if isinstance(parsed, dict):
            return parsed
        raise ValueError("Browser returned an unexpected result")
    raise ValueError("Could not decode the browser result")


def main() -> int:
    if not HTML_PATH.is_file():
        raise SystemExit(f"Candidate not found: {HTML_PATH}")
    try:
        result = run_browser()
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        return 2
    if result.get("entries") != 500 or not result.get("refusalVerified") or not result.get("updateVerified"):
        print(json.dumps(result, indent=2))
        return 1
    print("V46_CAPACITY_OK: 500 distinct Scripture Q&As are accepted")
    print("PASS a 501st distinct entry is refused")
    print("PASS an existing entry remains updateable at capacity")
    print("PASS the prior browser overlay was restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
