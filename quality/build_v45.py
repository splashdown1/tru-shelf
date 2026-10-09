from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "test-candidates" / "v44" / "TRU-v44.html"
OUTPUT_PATH = PROJECT_ROOT / "test-candidates" / "v45" / "TRU-v45.html"
EXPECTED_BASE_SHA256 = "0388514562e13159c8511ed9c0bd235ef1aae2b30ebb5d1f38310e8f85803b93"
OLD_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T02:30:43.000Z";'
NEW_BUILD_STAMP = b'const __TRU_BUILD__="2026-10-09T10:48:03.000Z";'
OLD_TITLE = "<title>TRU v44 — Text-Rooted Understanding</title>".encode()
NEW_TITLE = "<title>TRU v45 — Text-Rooted Understanding</title>".encode()
PATCH_MARKER = b'<script id="tru-v45-reading-polish">'
PATCH = r'''<script id="tru-v45-reading-polish">
(function(){
  if(window.__TRU_V45_PATCH)return;
  const baseRoute=window.route;
  if(typeof baseRoute!=="function")throw new Error("TRU route not available for v45 patch");
  window.__TRU_V45_PATCH=true;
  const style=document.createElement("style");
  style.textContent=`
    .mode-switch{gap:8px!important;margin-left:10px!important;padding-left:10px!important;border-left:1px solid rgba(0,229,255,.22)}
    .mode-switch .tru-mode-label{color:rgba(180,225,240,.48);font:8px ui-monospace,monospace;letter-spacing:1.1px}
    .mode-switch button{min-width:54px;min-height:28px}
    .tru-deep-details{margin:12px 0 4px;border:1px solid rgba(0,229,255,.22);border-radius:8px;background:rgba(0,20,30,.48);overflow:hidden}
    .tru-deep-details>summary{display:flex;align-items:center;justify-content:space-between;gap:12px;cursor:pointer;list-style:none;padding:10px 12px;color:#9ed7ff;font:10px ui-monospace,monospace;letter-spacing:.35px}
    .tru-deep-details>summary::-webkit-details-marker{display:none}
    .tru-deep-details>summary:after{content:"＋";color:#00e5ff;font-size:14px}
    .tru-deep-details[open]>summary:after{content:"−"}
    .tru-deep-details[open]>summary{border-bottom:1px solid rgba(0,229,255,.16)}
    .tru-deep-details .tru-deep-label{color:rgba(180,225,240,.48);font-size:9px;letter-spacing:.2px;text-align:right}
    .tru-deep-text{max-height:55vh;overflow:auto;padding:12px 14px 16px;color:rgba(206,225,232,.82);font:12px/1.75 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
    .tru-place-answer{max-width:860px}
    .tru-place-answer .tru-topic-intro{margin:8px 0 12px;color:#c2d7df;line-height:1.6}
    .tru-verse-evidence{margin:8px 0;padding:10px 12px;border:1px solid rgba(0,229,255,.18);border-radius:7px;background:rgba(0,20,30,.4)}
    .tru-verse-evidence .tru-ref{display:inline-block;border:1px solid rgba(0,229,255,.34);border-radius:5px;padding:3px 8px;background:rgba(0,229,255,.07);color:#52dfff;font:10px ui-monospace,monospace;cursor:pointer}
    .tru-verse-evidence p{margin:7px 0 0;color:rgba(225,239,243,.86);line-height:1.55}
    .tru-topic-source{margin-top:10px;color:rgba(180,225,240,.5);font-size:9px;letter-spacing:.5px}
    @media(max-width:560px){
      .header{align-items:center!important;gap:6px!important;padding:6px 8px!important}
      .holo-mini{width:30px!important;height:30px!important;flex:0 0 30px!important}
      .title-block{min-width:0!important;flex:1 1 76px!important}
      .title{font-size:15px!important;letter-spacing:1.6px!important;line-height:1!important}
      #sub{font-size:0!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1!important}
      #sub::after{content:"31k KJV · 14k lexicon";font:6.5px ui-monospace,monospace;letter-spacing:0}
      .badge{flex:0 1 auto!important;max-width:68px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
      .mode-switch{gap:4px!important;margin-left:2px!important;padding-left:6px!important}
      .mode-switch .tru-mode-label{font-size:7px;letter-spacing:.6px}
      .mode-switch button{min-width:0;min-height:26px;padding:5px 5px!important;font-size:8px!important}
      .tru-deep-details>summary{align-items:flex-start;flex-direction:column;gap:4px}
      .tru-deep-details .tru-deep-label{text-align:left}
      .tru-deep-text{font-size:11px;max-height:48vh}
    }
  `;
  document.head.appendChild(style);
  function decorateMode(){
    document.querySelectorAll(".mode-switch").forEach(function(switcher){
      if(!switcher.querySelector(".tru-mode-label")){
        const label=document.createElement("span");
        label.className="tru-mode-label";
        label.textContent="MODE";
        switcher.prepend(label);
      }
      switcher.querySelectorAll("button[data-tru-mode]").forEach(function(button){
        const mode=button.getAttribute("data-tru-mode");
        button.setAttribute("aria-label",mode==="light"?"Light theme":"Offline mode");
      });
    });
  }
  decorateMode();
  const subtitle=document.getElementById("sub");
  if(subtitle){
    const updateSubtitleTitle=function(){subtitle.setAttribute("title",subtitle.textContent||"TRU corpus summary");};
    updateSubtitleTitle();
    new MutationObserver(updateSubtitleTitle).observe(subtitle,{childList:true,characterData:true,subtree:true});
  }
  function escapeHTML(value){
    return String(value).replace(/[&<>"']/g,function(ch){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch];});
  }
  function cleanDeepText(value){
    return String(value||"")
      .replace(/\\\s*\\\s*/g," ")
      .replace(/\bV:\d{1,3}(?:\s*;\s*V:\d{1,3}){2,}\s*;?/g," ")
      .replace(/[ \t]{2,}/g," ")
      .replace(/[ \t]*\n[ \t]*/g,"\n")
      .replace(/\n{3,}/g,"\n\n")
      .replace(/\s+([,;.])/g,"$1")
      .replace(/([,;:])(?=\S)/g,"$1 ")
      .trim();
  }
  function detailsBlock(title,text,open){
    return '<details class="tru-deep-details"'+(open?' open':'')+'><summary><span>Full original-language entry</span><span class="tru-deep-label">'+escapeHTML(title)+' · reading cleanup applied</span></summary><div class="tru-deep-text">'+escapeHTML(cleanDeepText(text))+'</div></details>';
  }
  function polishDeep(reply,question){
    const text=String(reply||"");
    const open=/^\s*deep\b/i.test(String(question||""));
    const marker="\n\nDEEP • ";
    const at=text.indexOf(marker);
    if(at>=0){
      const leading=text.slice(0,at).trimEnd();
      const deep=text.slice(at+2).trim();
      const lineEnd=deep.indexOf("\n");
      const heading=lineEnd<0?deep:deep.slice(0,lineEnd);
      const body=lineEnd<0?"":deep.slice(lineEnd+1).trim();
      const title=heading.replace(/^DEEP\s*[•·]\s*/i,"").trim()||"BDB / Thayer";
      return leading+detailsBlock(title,body,open);
    }
    const match=text.match(/^DEEP LEXICON\s*[•·]\s*([^\n]+)\n+([\s\S]*)$/i);
    if(match){
      return '<div class="enc-title">DEEP LEXICON • '+escapeHTML(match[1].trim())+'</div>'+detailsBlock("Full BDB / Thayer entry",match[2],true);
    }
    return text;
  }
  function verseCard(reference,shortRef){
    const verse=window.parseVerse(reference);
    if(!verse||!verse.text)return null;
    const label=verse.ref||reference;
    return '<article class="tru-verse-evidence"><button type="button" class="tru-ref" data-q="'+escapeHTML(label)+'" aria-label="Open '+escapeHTML(label)+' in the reader">'+escapeHTML(shortRef||label)+'</button><p>'+escapeHTML(verse.text)+'</p></article>';
  }
  function heavenEvidence(question,result){
    const query=String(question||"").trim().toLowerCase().replace(/[?!.,;:]+$/g,"");
    if(!/^where\b/.test(query)||!/\bheaven\b/.test(query)||!/\b(?:is|are|was|were)\b/.test(query))return null;
    if(typeof window.topicalQuery!=="function"||typeof window.parseVerse!=="function")return null;
    const topic=window.topicalQuery("heaven");
    if(!topic||topic.verdict!=="TOPICAL")return null;
    const sourceText=String(topic.reply||"").replace(/<[^>]*>/g," ");
    const selected=[
      {short:"Deuteronomy 26:15",topicText:"De 26:15"},
      {short:"Isaiah 66:1",topicText:"Isa 57:15; 63:15; 66:1"},
      {short:"Matthew 6:9",topicText:"Mt 5:34,45; 6:9"}
    ];
    const cards=[];
    for(const item of selected){
      if(!sourceText.includes(item.topicText))return null;
      const card=verseCard(item.short,item.short);
      if(!card)return null;
      cards.push(card);
    }
    return {
      ...result,
      reply:'<div class="tru-place-answer"><div class="enc-title">TOPIC • HEAVEN</div><div class="tru-topic-intro">The local Nave–Torrey topic index groups HEAVEN under “God’s dwelling place”. It gives Scripture references, not a physical map location. Here are three KJV passages listed in that topic:</div>'+cards.join("")+'<div class="tru-topic-source">NAVE + TORREY TOPIC INDEX · KJV TEXT · LOCAL</div></div>',
      verdict:"TOPICAL",
      source:"Nave's Topical Bible + Torrey's Textbook + KJV • local",
      nodes_used:topic.nodes_used||[],
      scripture_ref:null,
      evidence:selected.map(function(x){return x.short;}),
      follow_up:true,
      sugContinuation:{label:"Open the full HEAVEN topic index",query:"heaven"}
    };
  }
  window.route=function(query){
    const result=baseRoute.apply(this,arguments);
    if(!result)return result;
    const enhanced={...result,reply:polishDeep(result.reply,query)};
    const heaven=heavenEvidence(query,enhanced);
    return heaven||enhanced;
  };
})();
</script>'''


def build(base: Path, output: Path, force: bool) -> str:
    source = base.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != EXPECTED_BASE_SHA256:
        raise SystemExit(f"pinned v44 base hash mismatch: expected {EXPECTED_BASE_SHA256}, found {digest}")
    if source.count(OLD_BUILD_STAMP) != 1:
        raise SystemExit("the v44 build stamp is missing or not unique")
    if source.count(OLD_TITLE) != 1:
        raise SystemExit("the v44 title is missing or not unique")
    if PATCH_MARKER in source:
        raise SystemExit("the v45 patch is already present in the base")
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
    parser = argparse.ArgumentParser(description="Build the pinned v45 reading-polish candidate from v44")
    parser.add_argument("--base", type=Path, default=BASE_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    digest = build(args.base, args.output, args.force)
    print(f"built {args.output} sha256={digest} bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
