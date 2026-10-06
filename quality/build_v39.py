from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v38" / "TRU-v38.html"
BASE_SHA256 = "a1cee6f5b01e0c11cfd53046533b924125125180d1b11fd84be8695329c147ea"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-05T15:42:36.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-06T12:11:11.000Z";'
PATCH_MARKER = b'<script id="tru-v39-exact-term-question">'
PATCH_SCRIPT = r'''<script id="tru-v39-exact-term-question">
(function(){
  if(window.__TRU_V39_EXACT_TERM_QUESTION)return;
  window.__TRU_V39_EXACT_TERM_QUESTION=true;
  const previousRoute=route;
  function exactTermQuestion(raw){
    const text=String(raw||"").trim().replace(/[?!.]+$/g,"").trim();
    const tail="(?:\\s+in\\s+(?:the\\s+)?(?:bible|scripture))?";
    const patterns=[
      new RegExp("^(?:what\\s+is|what's)\\s+(?:(?:a|an|the)\\s+)?([a-z][a-z'-]*)"+tail+"$","i"),
      new RegExp("^(?:can|could)\\s+you\\s+(?:please\\s+)?tell\\s+me\\s+what\\s+(?:(?:a|an|the)\\s+)?([a-z][a-z'-]*)\\s+is"+tail+"$","i")
    ];
    for(const pattern of patterns){
      const match=text.match(pattern);
      if(match)return match[1].toLowerCase();
    }
    return null;
  }
  function exactTermAnswer(raw){
    const term=exactTermQuestion(raw);
    if(!term)return null;
    const original=previousRoute(raw);
    const exact=previousRoute(term);
    if(!exact)return original?{...original,original_question:raw}:null;
    const source=String(original&&original.source||"").toLowerCase();
    const reply=String(original&&original.reply||"").toLowerCase();
    const needsExact=!original||String(original.verdict||"").toUpperCase()==="GAP";
    const phraseNoise=String(original&&original.verdict||"").toUpperCase()==="SCRIPTURE"&&reply.includes("phrase •");
    const deepGlossNoise=String(original&&original.verdict||"").toUpperCase()==="DEFINE"&&source.includes("deep lexicon")&&String(exact.verdict||"").toUpperCase()==="GAP";
    const result=needsExact||phraseNoise||deepGlossNoise?exact:original;
    return {...result,original_question:raw,_exact_term_question:result===exact};
  }
  route=function(q){
    const termResult=exactTermAnswer(q);
    if(termResult){
      if(typeof addTurn==="function")addTurn(q,termResult);
      return termResult;
    }
    return previousRoute(q);
  };
})();
</script>'''
PATCH = PATCH_SCRIPT.encode("utf-8") + b"\n</body>"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: bytes) -> bytes:
    if sha256(source) != BASE_SHA256:
        raise ValueError("Pinned v38 parent hash does not match")
    if source.count(PATCH_MARKER) != 0 or source.count(b"</body>") != 1:
        raise ValueError("Expected an untouched v38 page-end anchor")
    if source.count(OLD_BUILD_STAMP) != 1:
        raise ValueError("Expected one pinned v38 build stamp")
    updated = source.replace(b"</body>", PATCH, 1)
    updated = updated.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned TRU v39 exact-term question candidate")
    parser.add_argument("--output", type=Path, required=True, help="New, unused output file; existing files are never overwritten.")
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"Refusing to overwrite existing file: {args.output}")
    source = BASE_PATH.read_bytes()
    result = transform(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result)
    print(f"BUILT {args.output.resolve()}")
    print(f"PARENT_SHA256 {sha256(source)}")
    print(f"BYTES {len(result)}")
    print(f"SHA256 {sha256(result)}")


if __name__ == "__main__":
    main()
