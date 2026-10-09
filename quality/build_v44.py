from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v43" / "TRU-v43.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v44" / "TRU-v44.html"
EXPECTED_BASE_SHA256 = "8ab37266a47076e0213e1ed7464927b7a13dc0144d99eefa774da57ad2ad9f9c"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T01:27:39.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T02:30:43.000Z";'
OLD_TITLE = "<title>TRU v43 — Text-Rooted Understanding</title>".encode()
NEW_TITLE = "<title>TRU v44 — Text-Rooted Understanding</title>".encode()
PATCH_MARKER = b'<script id="tru-v44-route-voice-fixes">'
PATCH = r'''<script id="tru-v44-route-voice-fixes">
(function(){
  if(window.__TRU_V44_PATCH)return;
  const baseRoute=window.route;
  if(typeof baseRoute!=="function")throw new Error("TRU route not available for v44 patch");
  window.__TRU_V44_PATCH=true;
  let gapGuidanceShown=false;
  const guidance="No canon match. Try a verse, a word, a Strong's number, or a phrase from Scripture.";
  function recordTurn(question,result){
    if(typeof window.addTurn!=="function")return;
    const stored={...result,nodes_used:(result.nodes_used||[]).map(node=>typeof node==="string"?{k:node}:node)};
    window.addTurn(question,stored);
  }
  window.route=function(query){
    const question=String(query??"");
    const indexedCommand=question.trim().match(/^word\s+index\s*:\s*(.+)$/i);
    if(indexedCommand&&typeof window.bibleWordLookup==="function"){
      const word=indexedCommand[1].trim();
      const indexed=window.bibleWordLookup(word);
      if(indexed&&indexed.verdict==="DEFINE"&&indexed.bible_word_index){
        const result={...indexed,original_question:question,contextual:false,context_topic:null};
        recordTurn(question,result);
        return result;
      }
      const missing={reply:"No exact KJV word-index entry was found. Try a Bible word or a verse reference.",verdict:"GAP",source:"KJV word index • local",nodes_used:[],follow_up:false,original_question:question,contextual:false,context_topic:null};
      recordTurn(question,missing);
      return missing;
    }
    const result=baseRoute(query);
    if(!result||result.verdict!=="GAP")return result;
    const gap={...result};
    const personal=question.trim().match(/^(?:are you|am i|is he|is she|are we|are they)\s+(?:a\s+|an\s+|the\s+)?([a-z]+)[?!.,]*$/i);
    if(!gap.sugContinuation&&personal&&typeof window.bibleWordLookup==="function"){
      const word=personal[1].toLowerCase();
      const indexed=window.bibleWordLookup(word);
      if(indexed&&indexed.verdict==="DEFINE"&&indexed.bible_word_index){
        gap.sugContinuation={label:"Check “"+word+"” in the KJV word index",query:"word index: "+word};
      }
    }
    if(typeof gap.reply==="string"&&gap.reply.includes(guidance)){
      if(gapGuidanceShown)gap.reply=gap.reply.replace(guidance,"No supported match was found in the local sources.");
      else gapGuidanceShown=true;
    }
    return gap;
  };
  if(typeof window.readerVoiceStatus==="function"){
    const baseVoiceStatus=window.readerVoiceStatus;
    let mismatchNoticeShown=false;
    window.readerVoiceStatus=function(){
      const status=baseVoiceStatus.apply(this,arguments);
      if(typeof status!=="string"||!status.startsWith("No recognizable "))return status;
      if(!mismatchNoticeShown){mismatchNoticeShown=true;return status;}
      const match=status.match(/; using local voice (.+?)\. Choose a named voice if needed\.$/);
      return match?"Using local voice "+match[1]+".":"Using the available local English voice.";
    };
  }
})();
</script>'''


def build(base: Path, output: Path, force: bool) -> str:
    source = base.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != EXPECTED_BASE_SHA256:
        raise SystemExit(f"pinned v43 base hash mismatch: expected {EXPECTED_BASE_SHA256}, found {digest}")
    if source.count(OLD_BUILD_STAMP) != 1:
        raise SystemExit("the v43 build stamp is missing or not unique")
    if source.count(OLD_TITLE) != 1:
        raise SystemExit("the v43 title is missing or not unique")
    if PATCH_MARKER in source:
        raise SystemExit("the v44 patch is already present in the base")
    if source.count(b"</body>") != 1:
        raise SystemExit("the body insertion point is missing or not unique")
    if output.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing candidate: {output}; pass --force to rebuild")
    candidate = source.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    candidate = candidate.replace(OLD_TITLE, NEW_TITLE, 1)
    candidate = candidate.replace(b"</body>", PATCH.encode() + b"\n</body>", 1)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(candidate)
    return hashlib.sha256(candidate).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned v44 human-test candidate from v43")
    parser.add_argument("--base", type=Path, default=BASE_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    digest = build(args.base, args.output, args.force)
    print(f"built {args.output} sha256={digest} bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
