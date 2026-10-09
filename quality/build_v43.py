from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v40" / "TRU-v40.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v43" / "TRU-v43.html"
EXPECTED_BASE_SHA256 = "8c7df8f1b79efc5dee5ff8ac6863043d726444ccfd965343b4ab6d4d26fdefad"
EXPECTED_LEXICON_SOURCE_SHA256 = "e21c8147da25e72f61bf04f4173e162af073943a73976034befe34136b8e2597"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-06T13:36:27.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T01:27:39.000Z";'
TITLE_OLD = b"<title>TRU</title>"
TITLE_NEW = "<title>TRU v43 — Text-Rooted Understanding</title>".encode("utf-8")
LEXICON_PATTERN = re.compile(rb'(<script type="application/json" id="logos-lexicon">)(.*?)</script>', re.S)
PATCH_MARKER = b'<script id="tru-v43-identity">'
IDENTITY_PATCH = r'''<script id="tru-v43-identity">
(function(){
  if(window.__TRU_V43_IDENTITY)return;
  const baseRoute=window.route;
  if(typeof baseRoute!=="function")throw new Error("TRU route not available for v43 patch");
  window.__TRU_V43_IDENTITY=true;
  function singularCandidates(word){
    if(word.length<4||["news","series","species","scissors","mathematics","politics","physics"].includes(word))return [];
    const candidates=[];
    if(/ies$/.test(word))candidates.push(word.slice(0,-3)+"y");
    if(/(?:ches|shes|xes|zes|sses|oes)$/.test(word))candidates.push(word.slice(0,-2));
    if(/s$/.test(word))candidates.push(word.slice(0,-1));
    if(/es$/.test(word))candidates.push(word.slice(0,-2));
    return [...new Set(candidates)].filter(value=>value.length>=3&&/^[a-z]+$/.test(value));
  }
  window.route=function(query){
    const compact=String(query||"").toLowerCase().replace(/[^a-z0-9]/g,"");
    if(compact==="whatistru"||compact==="whatdoestrumean"||compact==="whatdoestrustandfor")return {reply:"TRU stands for Text-Rooted Understanding. It is a local, offline Scripture and word-study tool that retrieves from the KJV, Strong's lexicon, cross-references, and bundled study material. It shows its sources when available and returns GAP when the local evidence is insufficient. The name describes the standard this build aims to meet, not a guarantee that every answer is correct; the evidence can be checked.",verdict:"TRU_CORE",source:"TRU core identity • local",nodes_used:[],follow_up:false,route_class:"TRU_CORE"};
    const existing=baseRoute(query);
    if(existing&&existing.verdict!=="GAP")return existing;
    const match=String(query||"").match(/^\s*(?:define\s+)?([a-z]+)\s*[.!?]*\s*$/i);
    if(match&&typeof window.lexiconQuery==="function"){
      const word=match[1].toLowerCase();
      for(const candidate of singularCandidates(word)){
        const result=window.lexiconQuery(candidate);
        if(result&&result.verdict==="DEFINE")return {...result,source:"LOGOS Lexicon • likely singular fallback • local",lexicon_requested_term:word,lexicon_term:candidate,lexicon_normalization:{kind:"possible_plural",from:word,to:candidate}};
      }
    }
    return existing;
  };
})();
</script>
</body>'''.encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_lexicon(source: bytes) -> bytes:
    if sha256(source) != EXPECTED_SOURCE_ARTIFACT_SHA256:
        raise ValueError("Pinned repaired modular source artifact hash does not match")
    matches = list(LEXICON_PATTERN.finditer(source))
    if len(matches) != 1:
        raise ValueError("Expected exactly one embedded LOGOS Lexicon block in the source artifact")
    payload = matches[0].group(2)
    if sha256(payload) != EXPECTED_LEXICON_SOURCE_SHA256:
        raise ValueError("Pinned repaired lexicon block hash does not match")
    pack = json.loads(payload)
    if pack.get("schema") != "logos-lexicon-pack-v1" or len(pack.get("entries", {})) != 14088:
        raise ValueError("Unexpected repaired lexicon pack schema or entry count")
    return payload


def transform(base: bytes, lexicon: bytes) -> bytes:
    if sha256(base) != EXPECTED_BASE_SHA256:
        raise ValueError("Pinned v40 parent hash does not match")
    if base.count(TITLE_OLD) != 1 or base.count(OLD_BUILD_STAMP) != 1 or base.count(b"</body>") != 1:
        raise ValueError("Expected one pinned v40 title, build stamp, and page-end anchor")
    if base.count(PATCH_MARKER) or not lexicon:
        raise ValueError("The v43 identity patch is already present or the lexicon is empty")
    matches = list(LEXICON_PATTERN.finditer(base))
    if len(matches) != 1:
        raise ValueError("Expected exactly one embedded LOGOS Lexicon block in the v40 artifact")
    old_pack = json.loads(matches[0].group(2))
    new_pack = json.loads(lexicon)
    if old_pack.get("schema") != new_pack.get("schema") or len(old_pack.get("entries", {})) != 14088:
        raise ValueError("The v40 and repaired lexicon pack schemas do not match")
    result = base[:matches[0].start(2)] + lexicon + base[matches[0].end(2):]
    result = result.replace(TITLE_OLD, TITLE_NEW, 1)
    result = result.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    return result.replace(b"</body>", IDENTITY_PATCH, 1)


EXPECTED_SOURCE_ARTIFACT_SHA256 = "0c76884bf3d0d3b735fc3105efb916021b151b6dd63efb96789b5ad905b2ec7e"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned v43 human-test candidate from v40 plus the verified repaired lexicon")
    parser.add_argument("--base", type=Path, default=BASE_PATH)
    parser.add_argument("--lexicon-source", type=Path, required=True, help="Verified modular HTML artifact containing the repaired LOGOS Lexicon pack")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    result = transform(args.base.read_bytes(), extract_lexicon(args.lexicon_source.read_bytes()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result)
    print(f"BUILT {args.output.resolve()}")
    print(f"PARENT_SHA256 {sha256(args.base.read_bytes())}")
    print(f"LEXICON_SOURCE_SHA256 {EXPECTED_LEXICON_SOURCE_SHA256}")
    print(f"BYTES {len(result)}")
    print(f"SHA256 {sha256(result)}")


if __name__ == "__main__":
    main()
