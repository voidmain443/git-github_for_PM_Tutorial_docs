/* Optional learning tools. Drafts stay in memory; no account or submission store. */
(function(){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const drafts=new Map(), choices=new Map();let mountId=0;
const split=line=>line.trim().replace(/^\||\|$/g,'').split(/(?<!\\)\|/).map(x=>x.trim());
function download(name,body){const u=URL.createObjectURL(new Blob([body],{type:'text/markdown;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
// Treat every authored value as text, including when a learner imports a draft.
function formHTML(raw){const lines=raw.split('\n');let out='';for(let i=0;i<lines.length;i++){
 const line=lines[i];if(line.startsWith('|')&&/^\|[\s:|\-]+$/.test(lines[i+1]||'')){
  const headers=split(line);out+='<div class="reading-table"><table><thead><tr>'+headers.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead><tbody>';i+=2;
  for(;i<lines.length&&lines[i].startsWith('|');i++){const cells=split(lines[i]);out+='<tr>'+cells.map((v,j)=>'<td><label class="study-cell-label">'+esc(headers[j]||'작성')+'</label><textarea data-cell="'+i+','+j+'" aria-label="'+esc((cells[0]||'행')+' · '+(headers[j]||'작성'))+'" rows="3">'+esc(v.replace(/<br\s*\/?\s*>/gi,'\n').replace(/\\\|/g,'|'))+'</textarea></td>').join('')+'</tr>';}
  out+='</tbody></table></div>';i--;continue;
 }
 if(/^#{1,3} /.test(line)){const n=Math.min(4,line.match(/^#+/)[0].length+1);out+='<h'+n+'>'+esc(line.replace(/^#+ /,''))+'</h'+n+'>';}else if(line.trim())out+='<p>'+esc(line)+'</p>';
}return out;}
window.addEventListener('beforeunload',e=>{if([...drafts.values()].some(d=>d.dirty)){e.preventDefault();e.returnValue='';}});
window.addEventListener('message',e=>{const f=document.querySelector('#study-frame');if(f&&e.source===f.contentWindow&&e.origin===location.origin&&e.data?.type==='pm-visual-height'&&Number.isFinite(e.data.height))f.style.height=Math.max(600,Math.min(15000,e.data.height))+'px';});
window.PMStudy={mount({lesson,step,unit}){
 const token=++mountId,$=s=>document.querySelector(s);
 if(step.locked)return;
 const body=$('#quiz-slot');
 if(step.selfCheck){const q=step.selfCheck;body.insertAdjacentHTML('beforeend',`<section id="study-quiz" class="study-panel" aria-labelledby="study-question"><span class="study-eyebrow">생각을 확인하기</span><h3 id="study-question">${esc(q.question)}</h3><p class="hint">선택 후 이유를 읽고, 자신의 문서에서 같은 판단을 설명해 보세요. 점수는 저장하지 않습니다.</p><div class="study-answers">${q.options.map((o,i)=>`<button data-answer="${i}" aria-pressed="false">${i+1}. ${esc(o)}</button>`).join('')}</div><p id="study-feedback" role="status" hidden></p></section>`);
  document.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-answer]').forEach(x=>x.setAttribute('aria-pressed',x===b));$('#study-feedback').hidden=false;$('#study-feedback').textContent=(Number(b.dataset.answer)===q.answer?'이 판단이 적절합니다. ':'다시 생각해 보세요. ')+q.explanation;});}
 if(PMApp.isStatic&&step.visualAid){const aid=step.visualAid;$('#visual-slot').innerHTML=`<details id="study-simulation" class="study-panel"><summary>그림으로 확인하기 · 선택</summary><p>${esc(aid.purpose)}</p><p class="hint">설명과 표로 이해했다면 바로 작성으로 넘어가도 됩니다. 현재 자료 ${esc(lesson.currentStage)}만 사용하며, 닫으면 재생도 종료됩니다.</p><a href="visual.html?lab=${esc(aid.lab)}" target="_blank" rel="noopener">큰 화면에서 열기 ↗</a><div id="study-frame-slot"></div></details>`;
  const panel=$('#study-simulation'),slot=$('#study-frame-slot');panel.ontoggle=()=>{if(panel.open){if(!slot.firstChild)slot.innerHTML=`<iframe id="study-frame" title="${unit}단원 시각화 실습" src="visual.html?lab=${esc(aid.lab)}&embed=1" loading="lazy"></iframe>`;}else slot.replaceChildren();};}
 const names=step.downloads||[];if(!names.length)return;
 $('#templates').insertAdjacentHTML('afterend',`<details id="study-writing" class="study-panel"><summary>웹에서 양식 작성하기 · 선택 사항</summary><p>아래 표에서 초안을 작성하고 Markdown 파일로 보관하세요. 같은 양식은 이 페이지 안에서 이어 쓰며, 새로고침·다른 페이지 이동 시에는 내보낸 파일을 다시 불러옵니다. 조회·작성 기록을 서버에 저장하지 않습니다.</p><div class="bar"><label for="study-template">작성 문서</label><select id="study-template">${names.map(n=>`<option>${esc(n)}</option>`).join('')}</select><button id="study-load">양식 열기 / 이어 쓰기</button></div><div class="bar study-tools"><button id="study-export" disabled>작성본 내려받기</button><label class="downloadlink" for="study-import">이 문서의 작성본 불러오기<input id="study-import" type="file" accept=".md,.txt,text/plain,text/markdown"></label></div><p id="study-writing-status" role="status"></p><div id="study-preview"></div><details id="study-markdown" hidden><summary>원문으로 편집 · 행 추가와 자유 서술</summary><label for="study-editor">Markdown 원문 (표 편집과 연결됩니다)</label><textarea id="study-editor" spellcheck="false" rows="18"></textarea></details></details>`);
 const select=$('#study-template');select.value=choices.get(unit)&&names.includes(choices.get(unit))?choices.get(unit):names[0];let opened=null,loadId=0;
 const status=text=>$('#study-writing-status').textContent=text;
 const renderForm=()=>{const d=drafts.get(opened);$('#study-preview').innerHTML=formHTML(d.text);document.querySelectorAll('[data-cell]').forEach(el=>el.oninput=()=>{const [line,col]=el.dataset.cell.split(',').map(Number),lines=d.text.split('\n'),cells=split(lines[line]);cells[col]=el.value.replace(/\|/g,'\\|').replace(/\n/g,'<br>');lines[line]='| '+cells.join(' | ')+' |';d.text=lines.join('\n');d.dirty=true;$('#study-editor').value=d.text;status('이 페이지의 임시 초안입니다. 이동 전에 작성본을 내려받으세요.');});};
 const display=(name)=>{opened=name;const d=drafts.get(name);$('#study-editor').value=d.text;$('#study-markdown').hidden=false;$('#study-export').disabled=false;renderForm();status(name+' · '+(d.dirty?'아직 파일로 보관하지 않은 수정이 있습니다.':'원천 ERP와 별도의 학습자 작성본입니다.'));};
 $('#study-load').onclick=async()=>{const name=select.value,request=++loadId;choices.set(unit,name);try{if(!drafts.has(name)){const r=await fetch(PMApp.href('/download?name='+encodeURIComponent(name)));if(!r.ok)throw Error('양식을 열지 못했습니다.');const text=await r.text();if(token!==mountId||request!==loadId)return;drafts.set(name,{text,dirty:false});}if(request===loadId)display(name);}catch(e){status(e.message);}};
 select.onchange=()=>{loadId++;opened=null;$('#study-preview').innerHTML='';$('#study-markdown').hidden=true;$('#study-export').disabled=true;status('양식 열기를 누르면 선택한 문서가 표시됩니다.');};
 $('#study-editor').oninput=()=>{if(!opened)return;drafts.set(opened,{text:$('#study-editor').value,dirty:true});renderForm();status('이 페이지의 임시 초안입니다. 이동 전에 내려받으세요.');};
 $('#study-export').onclick=()=>{if(!opened)return;const d=drafts.get(opened);download(opened.replace(/\.md$/,'_작성본.md'),d.text);d.dirty=false;status('작성본 다운로드를 요청했습니다. 파일이 보관되었는지 확인하세요.');};
 $('#study-import').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>1000000)throw Error('1MB 이하의 Markdown 작성본을 선택하세요.');const text=await file.text();if(token!==mountId)return;const name=select.value;if(drafts.get(name)?.dirty&&!confirm('이 문서의 아직 내려받지 않은 초안을 불러온 파일로 바꿀까요? 취소한 뒤 먼저 내보낼 수 있습니다.'))return;drafts.set(name,{text,dirty:false});choices.set(unit,name);display(name);status(file.name+' 내용을 '+name+' 초안으로 불러왔습니다.');}catch(error){status(error.message);}finally{e.target.value='';}};
 if(drafts.has(select.value))display(select.value);
}};
})();
