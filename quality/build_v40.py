from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v39" / "TRU-v39.html"
BASE_SHA256 = "be82106355cf5848f1533df0c8cc216f505d1ad03bf622e2a98b4a8812e66ebb"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v40" / "TRU-v40.html"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-06T12:11:11.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-06T13:36:27.000Z";'
PATCH_MARKER = b'<script id="tru-v40-scripture-teaching">'
PATCH_SCRIPT = r'''<script id="tru-v40-scripture-teaching">
(function(){
  if(window.__TRU_V40_SCRIPTURE_TEACHING)return;
  window.__TRU_V40_SCRIPTURE_TEACHING=true;
  const PREFIX="scripture_qa_v40__";
  const HELP="teach TRU a Scripture-grounded answer with: remember: scripture: <question> = <brief answer> | <KJV verse>; <another KJV verse>. References are checked against the local KJV; the answer wording is yours to review.";
  function normalizeQuestion(value){
    return String(value||"").toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g," ").trim().replace(/\s+/g," ");
  }
  function readRecords(){
    try{
      loadOverlay();
      const added=OVERLAY.added||{};
      const out=[];
      for(const key of Object.keys(added)){
        if(!key.startsWith(PREFIX))continue;
        try{const record=JSON.parse(added[key]);if(record&&record.question&&record.answer&&Array.isArray(record.refs))out.push({key,record});}catch(e){}
      }
      return out;
    }catch(e){return [];}
  }
  function parseReferences(text){
    const parts=String(text||"").split(";").map(part=>part.trim()).filter(Boolean);
    if(parts.length<1||parts.length>5)return null;
    const out=[];
    for(const part of parts){
      if(!/^(?:[1-3]\s*)?[a-z]+(?:\s+(?:of|the|and|[a-z]+)){0,2}\s+\d{1,3}:\d{1,3}$/i.test(part))return null;
      const verse=parseVerse(part);
      if(!verse)return null;
      if(!out.some(item=>item.ref.toLowerCase()===verse.ref.toLowerCase()))out.push({ref:verse.ref,label:longReferenceLabel(verse.ref),text:verse.text});
    }
    return out.length?out:null;
  }
  function rememberScripture(body){
    const match=String(body||"").trim().match(/^scripture\s*:\s*(.+?)\s*=\s*(.+?)\s*\|\s*(.+)$/i);
    if(!match)return {reply:"No answer stored. "+HELP,verdict:"MEMORY",source:"local Scripture teaching",nodes_used:[],follow_up:false};
    const question=match[1].trim();
    const answerText=match[2].trim();
    const refs=parseReferences(match[3]);
    if(question.length<3||question.length>240||!answerText||answerText.length>1800||!refs){
      return {reply:"No answer stored. Use 1–5 exact KJV verse references separated by semicolons; verse ranges are not accepted. Check the question and answer length. "+HELP,verdict:"MEMORY",source:"local KJV validation",nodes_used:[],follow_up:false};
    }
    const normalized=normalizeQuestion(question);
    if(!normalized)return {reply:"No answer stored. Add a real question. "+HELP,verdict:"MEMORY",source:"local Scripture teaching",nodes_used:[],follow_up:false};
    const key=PREFIX+normalized;
    const records=readRecords();
    if(!OVERLAY.added[key]&&records.length>=500)return {reply:"The Scripture teaching shelf is full (500/500). Forget an entry before adding another.",verdict:"MEMORY",source:"local Scripture teaching",nodes_used:[],follow_up:false};
    const record={question,answer:answerText,refs};
    OVERLAY.added[key]=JSON.stringify(record);
    delete OVERLAY.corrected[key];
    delete OVERLAY.removed[key];
    saveOverlay();
    reloadBrain();
    const count=readRecords().length;
    return {reply:"saved Scripture answer "+count+"/500 for: "+question+"\nKJV references checked locally: "+refs.map(item=>item.label).join("; "),verdict:"MEMORY",source:"user-taught answer • local KJV references",nodes_used:[{k:key,w:1}],follow_up:false};
  }
  function listScriptureAnswers(){
    const records=readRecords();
    if(!records.length)return {reply:"No Scripture answers taught yet (0/500). "+HELP,verdict:"MEMORY",source:"local Scripture teaching shelf",nodes_used:[],follow_up:false};
    return {reply:"Scripture teaching shelf: "+records.length+"/500\n"+records.slice(0,20).map(item=>"• "+item.record.question).join("\n")+(records.length>20?"\n… and "+(records.length-20)+" more":""),verdict:"MEMORY",source:"local Scripture teaching shelf",nodes_used:[],follow_up:false};
  }
  function forgetScriptureAnswer(question){
    const normalized=normalizeQuestion(question);
    const key=PREFIX+normalized;
    if(!normalized||!OVERLAY.added[key])return {reply:"No taught Scripture question matches that exact wording.",verdict:"MEMORY",source:"local Scripture teaching shelf",nodes_used:[],follow_up:false};
    delete OVERLAY.added[key];
    delete OVERLAY.corrected[key];
    delete OVERLAY.removed[key];
    saveOverlay();
    reloadBrain();
    return {reply:"forgot taught Scripture question: "+question.trim(),verdict:"MEMORY",source:"local Scripture teaching shelf",nodes_used:[],follow_up:false};
  }
  const baseIsMetaJunk=isMetaJunk;
  isMetaJunk=function(node){
    if(String(node&&node.k||"").startsWith(PREFIX))return true;
    return baseIsMetaJunk(node);
  };
  const baseRemember=cmdRemember;
  cmdRemember=function(body){
    if(/^scripture\s*:/i.test(String(body||"").trim()))return rememberScripture(body);
    const result=baseRemember(body);
    if(result&&/^teach me with: remember:/i.test(String(result.reply||"")))result.reply=HELP;
    return result;
  };
  const baseCommand=command;
  command=function(query){
    const raw=String(query||"").trim();
    if(/^scripture\s+answers(?:\s+list)?[.!?]*$/i.test(raw))return listScriptureAnswers();
    const forget=raw.match(/^forget\s*:\s*scripture\s*:\s*(.+)$/i);
    if(forget)return forgetScriptureAnswer(forget[1]);
    return baseCommand(query);
  };
  const baseAnswer=answer;
  answer=function(q,scripture,nodes,small,follow){
    const result=baseAnswer(q,scripture,nodes,small,follow);
    return String(result).replace("teach me: remember: <term> = <your definition>",HELP);
  };
  const baseRoute=route;
  route=function(query){
    const normalized=normalizeQuestion(query);
    if(normalized){
      const found=readRecords().find(item=>normalizeQuestion(item.record.question)===normalized);
      if(found){
        const record=found.record;
        const cited=record.refs.map(item=>'<span class="tru-ref" data-q="'+esc(item.ref)+'" style="color:#00e5ff;cursor:pointer">'+esc(item.label)+'</span> — '+esc(item.text)).join("<br><br>");
        const reply='<strong>ANSWER YOU TAUGHT</strong><br>'+esc(record.answer).replace(/\n/g,"<br>")+'<br><br><strong>KJV • LOCAL</strong><br>'+cited+'<br><br><span style="opacity:.75">Your wording is user-supplied. References and quoted verse text were checked against the local KJV; the interpretation was not independently reviewed.</span>';
        const result={reply,verdict:"SCRIPTURE",scripture_ref:record.refs[0].ref,source:"user-taught answer • references checked against local KJV",html:true,nodes_used:[{k:found.key,w:1,source:"KJV_BIBLE",t:"scripture teaching"}],follow_up:false,original_question:query};
        if(typeof addTurn==="function")addTurn(query,result);
        return result;
      }
    }
    return baseRoute(query);
  };
})();
</script>'''
PATCH = PATCH_SCRIPT.encode("utf-8") + b"\n</body>"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: bytes) -> bytes:
    if sha256(source) != BASE_SHA256:
        raise ValueError("Pinned v39 parent hash does not match")
    if source.count(PATCH_MARKER) != 0 or source.count(b"</body>") != 1:
        raise ValueError("Expected an untouched v39 page-end anchor")
    if source.count(OLD_BUILD_STAMP) != 1:
        raise ValueError("Expected one pinned v39 build stamp")
    updated = source.replace(b"</body>", PATCH, 1)
    updated = updated.replace(OLD_BUILD_STAMP, NEW_BUILD_STAMP, 1)
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the pinned TRU v40 Scripture-teaching candidate")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"Refusing to overwrite existing candidate: {args.output}")
    source = BASE_PATH.read_bytes()
    result = transform(source)
    args.output.write_bytes(result)
    print(f"BUILT {args.output.resolve()}")
    print(f"PARENT_SHA256 {sha256(source)}")
    print(f"BYTES {len(result)}")
    print(f"SHA256 {sha256(result)}")


if __name__ == "__main__":
    main()
