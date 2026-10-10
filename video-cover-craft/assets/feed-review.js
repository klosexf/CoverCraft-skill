"use strict";
(() => {
  const data = JSON.parse(document.getElementById("cover-data").textContent);
  const $ = id => document.getElementById(id);
  const images = data.images;
  const actions = {adjust:"调整", enlarge:"放大", reduce:"弱化", remove:"删除", preserve:"保留"};
  const priorities = {high:"优先改", normal:"随后改", low:"可选"};
  const verdicts = {pending:"待复核", resolved:"已解决 / 已保留", uncertain:"仍需修改"};
  const states = new Map();
  const currentIndex = images.findIndex(image => image.sha256 === data.currentImageSha256);
  const previousIndex = images.findIndex(image => image.sha256 === data.previousImageSha256);
  let selected = currentIndex >= 0 ? currentIndex : 0, draft = null, editing = null, pointer = null, toastTimer;
  let storageOK = true;
  const emptyState = () => ({notes:[], focus:null, masks:[]});
  const row = () => images[selected];
  const state = () => states.get(row().sha256);
  const key = hash => "covercraft-review-v1:" + hash;
  function el(tag, cls, text) { const n = document.createElement(tag); if(cls) n.className=cls; if(text!==undefined) n.textContent=text; return n; }
  function button(text, fn) { const n=el("button",null,text); n.type="button"; n.addEventListener("click",fn); return n; }
  function toast(text) { $("notice").textContent=text; $("notice").classList.add("visible"); clearTimeout(toastTimer); toastTimer=setTimeout(()=>$("notice").classList.remove("visible"),5000); }
  const clamp = n => Math.max(0,Math.min(1,n));
  const round = n => Math.round(n*100000)/100000;
  function rectValid(r) { return r && [r.x,r.y,r.w,r.h].every(n=>typeof n==="number" && Number.isFinite(n)) && r.x>=0 && r.y>=0 && r.w>0 && r.h>0 && r.x+r.w<=1.00001 && r.y+r.h<=1.00001; }
  function normalizeState(raw) {
    if(!raw || !Array.isArray(raw.notes) || raw.notes.length>500) throw Error("批注格式不正确或数量过多");
    const ids=new Set();
    const notes=raw.notes.map(n=>{
      if(!n || typeof n.id!=="string" || n.id.length>120 || ids.has(n.id) || !Object.hasOwn(actions,n.action) || !Object.hasOwn(priorities,n.priority) || typeof n.instruction!=="string" || !n.instruction.trim() || n.instruction.length>1500 || typeof n.observation!=="string" || n.observation.length>1500 || (n.rect!==null && !rectValid(n.rect))) throw Error("批注内容或区域不合法");
      ids.add(n.id);
      const checks={};
      if(n.verifications && typeof n.verifications==="object" && !Array.isArray(n.verifications)) {
        for(const [hash,v] of Object.entries(n.verifications)) {
          if(!/^[a-f0-9]{64}$/.test(hash) || !v || !Object.hasOwn(verdicts,v.status) || typeof v.at!=="string") throw Error("复核记录不合法");
          checks[hash]={status:v.status,at:v.at.slice(0,60)};
        }
      }
      return {id:n.id,rect:n.rect ? {...n.rect}:null,action:n.action,priority:n.priority,observation:n.observation,instruction:n.instruction,verifications:checks};
    });
    if(raw.focus!=null && !rectValid(raw.focus)) throw Error("焦点区域不合法");
    if(raw.masks!=null && (!Array.isArray(raw.masks) || raw.masks.length>100 || !raw.masks.every(rectValid))) throw Error("遮盖区域不合法");
    return {notes,focus:raw.focus || null,masks:raw.masks || []};
  }
  function save() {
    try { localStorage.setItem(key(row().sha256),JSON.stringify(state())); }
    catch(_) { storageOK=false; }
    storageStatus();
  }
  function storageStatus() {
    $("storage-status").textContent=storageOK ? "已自动保存到当前浏览器。导出批注可备份，也可在新预览中导入。" : "浏览器无法持久保存；关闭前请导出批注 .json，避免丢失。";
  }
  for(const image of images) {
    if(states.has(image.sha256)) continue;
    let saved=emptyState();
    try { const raw=localStorage.getItem(key(image.sha256)); if(raw) saved=normalizeState(JSON.parse(raw)); }
    catch(_) { storageOK=false; }
    states.set(image.sha256,saved);
  }
  function importFeedback(raw, persist=true) {
    if(!raw || raw.schema_version!==1 || raw.kind!=="covercraft-feedback" || !Array.isArray(raw.images) || raw.images.length>100) throw Error("不是有效的封面批注文件");
    const prepared=[], seen=new Set(); let skipped=0;
    for(const entry of raw.images) {
      if(!entry || typeof entry.image_sha256!=="string" || !/^[a-f0-9]{64}$/.test(entry.image_sha256) || seen.has(entry.image_sha256)) throw Error("图片标识不合法或重复");
      seen.add(entry.image_sha256);
      const clean=normalizeState(entry);
      if(!states.has(entry.image_sha256)) { skipped++; continue; }
      prepared.push([entry.image_sha256,clean]);
    }
    for(const [hash,clean] of prepared) {
      const old=states.get(hash), merged=new Map(old.notes.map(n=>[n.id,n]));
      for(const note of clean.notes) if(!merged.has(note.id)) merged.set(note.id,note);
      if(merged.size>500) throw Error("合并后批注超过 500 条，请拆分文件");
    }
    for(const [hash,clean] of prepared) {
      const old=states.get(hash), merged=new Map(old.notes.map(n=>[n.id,n]));
      for(const note of clean.notes) if(!merged.has(note.id)) merged.set(note.id,note);
      // Existing browser edits take precedence when a saved file is imported again.
      const next={notes:[...merged.values()], focus:old.focus || clean.focus, masks:old.masks.length ? old.masks : clean.masks};
      states.set(hash,next);
      if(persist) { try { localStorage.setItem(key(hash),JSON.stringify(next)); } catch(_) { storageOK=false; } }
    }
    storageStatus();
    return `已匹配 ${prepared.length} 张图片${skipped ? `；另有 ${skipped} 张不在本页，未导入` : ""}。重复批注保留浏览器现有内容。`;
  }
  if(data.feedback) { try { importFeedback(data.feedback); } catch(e) { toast("内置批注未载入："+e.message); } }
  function switchTab(name) {
    for(const n of document.querySelectorAll("[data-tab]")) n.setAttribute("aria-pressed",String(n.dataset.tab===name));
    for(const t of ["feed","review","compare"]) $("panel-"+t).hidden=t!==name;
    if(name==="review") renderReview();
    if(name==="compare") renderCompare();
  }
  document.querySelectorAll("[data-tab]").forEach(n=>n.addEventListener("click",()=>switchTab(n.dataset.tab)));
  function makeCard(image,index) {
    const card=el("article","card candidate"); card.append(el("div","card-label",versionLabel(index)));
    const frame=el("div","frame"); frame.style.aspectRatio=image.size[0]+" / "+image.size[1];
    const link=el("a"); link.href=image.file; link.target="_blank"; link.rel="noopener";
    const img=el("img"); img.src=image.file; img.alt=image.label; img.width=image.size[0]; img.height=image.size[1]; link.append(img); frame.append(link);
    for(const side of ["left","right"]) frame.append(el("div","zone "+side));
    frame.append(el("span","badge duration","12:34"),el("span","badge likes","♡"));
    const meta=el("div","meta"); meta.append(el("p","video-title",data.videoTitle || "未提供视频标题"),button("诊断这张",()=>selectForReview(index)));
    card.append(frame,meta); return card;
  }
  function sample(text) {
    const card=el("article","card sample"),frame=el("div","frame"),art=el("div","sample-art",text);
    frame.style.aspectRatio=images[0].size[0]+" / "+images[0].size[1]; art.append(el("small",null,"模拟示例卡片")); frame.append(art); card.append(el("div","card-label","周边示例"),frame); return card;
  }
  $("feed").append(sample("工具对比"),...images.map(makeCard),sample("实用教程"));
  $("count").textContent=images.length+" 张封面";
  $("theme").onclick=()=>{ const dark=document.body.classList.toggle("dark"); $("theme").textContent=dark ? "切换浅色":"切换深色"; };
  $("width").onchange=e=>document.documentElement.style.setProperty("--card-width",e.target.value+"px");
  for(const [id,cls] of [["overlays","show-overlays"],["zones","show-zones"],["crop","crop"],["context","with-context"]]) $(id).onchange=e=>document.body.classList.toggle(cls,e.target.checked);
  function versionLabel(index) {
    const image=images[index];
    if(currentIndex<0) return image.label;
    return (image.sha256===data.currentImageSha256 ? "当前版本 · " : "历史版本 · ")+image.label;
  }
  for(const id of ["review-image","compare-before","compare-after"]) images.forEach((image,i)=>{const option=el("option",null,versionLabel(i));option.value=i;$(id).append(option);});
  $("review-image").value=selected;
  $("compare-before").value=previousIndex>=0 ? previousIndex : 0;
  $("compare-after").value=currentIndex>=0 ? currentIndex : Math.min(1,images.length-1);
  function selectForReview(index) {
    selected=index; $("review-image").value=index; resetForm(); switchTab("review");
  }
  $("review-image").onchange=e=>selectForReview(Number(e.target.value));
  $("back-current").onclick=()=>selectForReview(currentIndex);
  $("annotate-after").onclick=()=>selectForReview(Number($("compare-after").value));
  function updateTarget() {
    const historical=currentIndex>=0 && row().sha256!==data.currentImageSha256;
    $("review-target-message").textContent=historical
      ? "正在查看历史版本。这里的批注仍绑定旧图；继续这一轮修改请返回当前版本。"
      : currentIndex>=0 ? "正在批注当前版本。新批注只针对这张图；上一轮批注保留在版本对比中。" : "新批注只针对当前选中的图片；切换图片可分别记录。";
    $("review-context").classList.toggle("historical",historical);
    $("back-current").hidden=!historical;
    $("export-target").textContent="修改目标："+versionLabel(selected);
    $("export-scope").textContent=state().notes.length ? `仅复制这张图的 ${state().notes.length} 条批注。全部版本记录可单独备份。` : "这张图还没有批注，请先圈选并保存。上一轮要求不会自动加入新修改单。";
    $("copy-brief").disabled=$("export-md").disabled=!state().notes.length;
  }
  function locationText(r) { return r ? `左 ${Math.round(r.x*100)}%，上 ${Math.round(r.y*100)}%，宽 ${Math.round(r.w*100)}%，高 ${Math.round(r.h*100)}%` : "整张图"; }
  function resetForm() { editing=null;draft=null;$("note-form").reset();$("form-title").textContent="添加批注";$("region-label").textContent="范围：整张图";renderRegions(); }
  function editNote(note) {editing=note.id;draft=note.rect;$("form-title").textContent="编辑批注";$("region-label").textContent="范围："+locationText(draft);$("note-action").value=note.action;$("note-priority").value=note.priority;$("note-observation").value=note.observation;$("note-instruction").value=note.instruction;renderRegions();}
  $("new-note").onclick=resetForm;
  $("note-form").onsubmit=e=>{
    e.preventDefault(); const instruction=$("note-instruction").value.trim(); if(!instruction) return;
    if(!editing && state().notes.length>=500) return toast("批注已达上限，请整理后再添加。");
    const previous=state().notes.find(n=>n.id===editing);
    const next={id:editing || `n-${Date.now()}-${Math.random().toString(36).slice(2,10)}`,rect:draft ? {...draft}:null,action:$("note-action").value,priority:$("note-priority").value,observation:$("note-observation").value.trim(),instruction,verifications:{}};
    // A changed instruction requires a fresh review; don't reuse old verdicts.
    if(previous) state().notes[state().notes.indexOf(previous)]=next; else state().notes.push(next);
    save();resetForm();renderNotes();toast("批注已保存；可导出交回聊天。");
  };
  function noteBlock(note,index,compareTarget) {
    const box=el("div","note"),top=el("div","note-top");top.append(el("strong",null,`${index+1}. ${actions[note.action]}`),el("small",null,priorities[note.priority]));box.append(top,el("small",null,locationText(note.rect)));
    if(note.observation) box.append(el("p","muted","观察："+note.observation));
    box.append(el("p",null,note.instruction));const controls=el("div","note-actions");
    if(compareTarget!==undefined) {
      const before=images[Number($("compare-before").value)],active=note.verifications[compareTarget]?.status || "pending";
      for(const [status,label] of Object.entries(verdicts)) {
        const b=button(label,()=>{note.verifications[compareTarget]={status,at:new Date().toISOString()};try {localStorage.setItem(key(before.sha256),JSON.stringify(states.get(before.sha256)));}catch(_){storageOK=false;}storageStatus();renderCompareNotes();});
        b.disabled=before.sha256===compareTarget;b.setAttribute("aria-pressed",String(status===active));controls.append(b);
      }
    } else {
      controls.append(button("定位 / 编辑",()=>editNote(note)),button("删除批注",()=>{state().notes=state().notes.filter(n=>n.id!==note.id);save();if(editing===note.id)resetForm();renderRegions();renderNotes();}));
    }
    box.append(controls);return box;
  }
  function renderNotes() { updateTarget(); $("note-count").textContent=state().notes.length+" 条";$("note-list").replaceChildren(...state().notes.map((n,i)=>noteBlock(n,i)));if(!state().notes.length)$("note-list").append(el("p","empty","先圈出一个问题，或记录一个需要保留的地方。")); }
  function region(r,cls,label) {const n=el("div","region "+cls);for(const [prop,val] of Object.entries({left:r.x,top:r.y,width:r.w,height:r.h}))n.style[prop]=(val*100)+"%";if(label)n.append(el("span","region-tag",label));return n;}
  function renderRegions() {
    const layer=$("review-layer");layer.replaceChildren();
    if($("show-masks").checked) state().masks.forEach(r=>layer.append(region(r,"mask")));
    if(state().focus) layer.append(region(state().focus,"focus","期望焦点"));
    state().notes.forEach((n,i)=>{if(n.rect)layer.append(region(n.rect,n.id===editing ? "selected":"",String(i+1)));});
    if(draft && !editing) layer.append(region(draft,"draft","待保存"));
    if(pointer?.rect) layer.append(region(pointer.rect,"draft"));
  }
  function renderReview() {$("review-img").src=row().file;$("review-img").alt=row().label;$("review-stage").style.aspectRatio=row().size[0]+" / "+row().size[1];renderRegions();renderNotes();applyFilters();}
  function applyFilters() {$("review-img").style.filter=`grayscale(${$("grayscale").checked ? 1:0}) blur(${$("blur").value}px)`;$("blur-value").value=$("blur").value;}
  $("grayscale").onchange=applyFilters;$("blur").oninput=applyFilters;$("show-masks").onchange=renderRegions;
  $("clear-masks").onclick=()=>{state().masks=[];save();renderRegions();};$("clear-focus").onclick=()=>{state().focus=null;save();renderRegions();};
  $("reset-diagnostics").onclick=()=>{$("grayscale").checked=false;$("blur").value=0;state().masks=[];state().focus=null;save();applyFilters();renderRegions();};
  function peek(active) {$("review-img").style.filter=active ? "none":`grayscale(${$("grayscale").checked ? 1:0}) blur(${$("blur").value}px)`;$("review-layer").style.visibility=active ? "hidden":"visible";}
  $("peek").onpointerdown=e=>{$("peek").setPointerCapture(e.pointerId);peek(true);};$("peek").onpointerup=()=>peek(false);$("peek").onpointercancel=()=>peek(false);$("peek").onblur=()=>peek(false);
  $("peek").onkeydown=e=>{if(e.key===" " || e.key==="Enter"){e.preventDefault();peek(true);}};$("peek").onkeyup=()=>peek(false);
  $("draw-mode").onchange=()=>{$("draw-hint").textContent={note:"在图上拖出矩形，再填写观察和改法。也可直接添加整图批注。",mask:"框住一个干扰元素，观察遮住后主次是否更清楚。遮盖不会自动成为删除指令。",focus:"框住你希望最先被注意的区域，再用灰度或模糊检查它是否突出。"}[$("draw-mode").value];};
  function point(e) {const b=$("review-stage").getBoundingClientRect();return {x:clamp((e.clientX-b.left)/b.width),y:clamp((e.clientY-b.top)/b.height)};}
  $("review-stage").onpointerdown=e=>{if(e.button!==0)return;const p=point(e);pointer={id:e.pointerId,start:p,rect:null};$("review-stage").setPointerCapture(e.pointerId);};
  $("review-stage").onpointermove=e=>{if(!pointer || pointer.id!==e.pointerId)return;const p=point(e),a=pointer.start;pointer.rect={x:round(Math.min(a.x,p.x)),y:round(Math.min(a.y,p.y)),w:round(Math.abs(a.x-p.x)),h:round(Math.abs(a.y-p.y))};renderRegions();};
  $("review-stage").onpointerup=e=>{
    if(!pointer || pointer.id!==e.pointerId)return;const r=pointer.rect;pointer=null;
    if(r && r.w>.008 && r.h>.008) {
      const mode=$("draw-mode").value;
      if(mode==="mask") {if(state().masks.length<100)state().masks.push(r);save();}
      else if(mode==="focus") {state().focus=r;save();}
      else {resetForm();draft=r;$("region-label").textContent="范围："+locationText(r);$("note-instruction").focus({preventScroll:true});}
    }
    renderRegions();
  };
  $("review-stage").onpointercancel=()=>{pointer=null;renderRegions();};
  function renderCompareNotes() {const before=images[Number($("compare-before").value)],after=images[Number($("compare-after").value)],notes=states.get(before.sha256).notes;$("compare-notes").replaceChildren(...notes.map((n,i)=>noteBlock(n,i,after.sha256)));if(!notes.length)$("compare-notes").append(el("p","empty","修改前的图片还没有批注。可先诊断，或导入之前导出的批注文件。"));}
  function renderCompare() {
    const before=images[Number($("compare-before").value)],after=images[Number($("compare-after").value)];
    const sameRatio=Math.abs(before.size[0]/before.size[1]-after.size[0]/after.size[1])<.0001;
    $("compare-mode").options[1].disabled=!sameRatio;
    if(!sameRatio)$("compare-mode").value="side";
    const wipe=$("compare-mode").value==="wipe";
    $("compare-hint").textContent=before.sha256===after.sha256 ? "当前选择的是同一张图片；请加入或选择修改后的图片再复核。" : !sameRatio ? "两张图片比例不同，保留各自比例并排显示；滑杆叠图暂不可用。" : "原图并排或对齐比较；此处不叠加诊断滤镜。";
    const host=$("compare-images");host.replaceChildren();
    if(wipe) {
      const frame=el("div","compare-wipe");for(const [image,cls] of [[before,"before"],[after,"after"]]){const img=el("img",cls);img.src=image.file;img.alt=image.label;frame.append(img);}frame.append(el("div","wipe-line"),el("span","wipe-label left","修改后"),el("span","wipe-label right","修改前"));host.append(frame);
    } else {
      const pair=el("div","compare-side");for(const [image,label] of [[before,"修改前"],[after,"修改后"]]){const fig=el("figure"),img=el("img");img.src=image.file;img.alt=image.label;fig.append(el("figcaption",null,label+" · "+image.label),img);pair.append(fig);}host.append(pair);
    }
    $("wipe-control").hidden=!wipe;applyWipe();renderCompareNotes();
  }
  function applyWipe() {const amount=Number($("wipe").value),img=document.querySelector(".compare-wipe .after"),line=document.querySelector(".wipe-line");if(img)img.style.clipPath=`inset(0 ${100-amount}% 0 0)`;if(line)line.style.left=amount+"%";$("wipe-value").value=amount+"%";}
  $("wipe").oninput=applyWipe;for(const id of ["compare-before","compare-after","compare-mode"])$(id).onchange=renderCompare;
  function exportObject() {
    const unique=[...new Map(images.map(i=>[i.sha256,i])).values()];
    return {schema_version:1,kind:"covercraft-feedback",created_at:new Date().toISOString(),video_title:data.videoTitle || null,active_image_sha256:row().sha256,images:unique.map(i=>({image_sha256:i.sha256,image_file:i.file,label:i.label,size:i.size,...states.get(i.sha256)}))};
  }
  function brief() {
    const active=exportObject().images.filter(image=>image.image_sha256===row().sha256);
    const lines=["# 封面修改单","","本轮修改目标："+versionLabel(selected),"请仅针对下方指定图片执行本轮批注，用户锁定的文案、身份与画幅继续有效。其他版本的历史批注不作为本轮修改要求。","批注区域用于表达位置，不承诺精确局部编辑。灰度、模糊和临时遮盖不写入成图。",""];
    for(const image of active) {
      if(!image.notes.length)continue;
      lines.push(`## ${image.label}`,`图片：${image.image_file}`,`图片 SHA-256：${image.image_sha256}`,"");
      const ordered=[...image.notes].sort((a,b)=>(a.action==="preserve"?-1:0)-(b.action==="preserve"?-1:0) || ["high","normal","low"].indexOf(a.priority)-["high","normal","low"].indexOf(b.priority));
      ordered.forEach((n,i)=>{
        lines.push(`${i+1}. 【${actions[n.action]} / ${priorities[n.priority]}】${n.instruction}`,`   范围：${locationText(n.rect)}`);
        if(n.observation)lines.push(`   可见依据：${n.observation}`);
        for(const [hash,v] of Object.entries(n.verifications)){const target=images.find(im=>im.sha256===hash);lines.push(`   对「${target?.label || hash.slice(0,12)}」的人工复核：${verdicts[v.status]}（${v.at}；SHA-256 ${hash}）`);}
        lines.push("");
      });
    }
    if(!active.some(i=>i.notes.length))lines.push("尚无批注，请先在诊断页记录观察与改法。");
    lines.push("复核方式：生成新版本后，将修改前后图片一同放进预览，导入批注备份并逐项核对。保留项也需要检查，不能只确认问题是否消失。");return lines.join("\n");
  }
  function download(name,text,type) {const blob=new Blob([text],{type}),url=URL.createObjectURL(blob),a=el("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
  $("export-md").onclick=()=>download("cover-revision-brief.md",brief(),"text/markdown;charset=utf-8");
  $("export-json").onclick=()=>download("cover-feedback.json",JSON.stringify(exportObject(),null,2),"application/json");
  $("copy-brief").onclick=async()=>{const text=brief();try{if(!navigator.clipboard)throw Error();await navigator.clipboard.writeText(text);toast("修改指令已复制，请连同对应原图交回聊天。");}catch(_){$("copy-text").value=text;$("copy-dialog").showModal();$("copy-text").select();}};
  $("close-copy").onclick=()=>$("copy-dialog").close();
  $("import-json").onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>5*1024*1024)throw Error("文件超过 5 MB");const message=importFeedback(JSON.parse(await file.text()));resetForm();renderReview();renderCompare();toast(message);}catch(err){toast("未导入："+err.message);}finally{e.target.value="";}};
  storageStatus();renderReview();renderCompare();
  if(currentIndex>=0) switchTab("review");
})();
