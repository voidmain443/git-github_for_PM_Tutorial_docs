/* D3 guided playback is a learning aid, never a change to ERP facts. */
export function playback(host,steps,choose,options={}){
 const root=typeof host==='string'?document.querySelector(host):host;
 if(!root||!steps.length)return()=>{};
 const d3=window.d3,reduce=matchMedia('(prefers-reduced-motion: reduce)');let i=0,timer=null,disposed=false;
 const panel=document.createElement('div');panel.className='wb-playback';
 panel.innerHTML='<div class="wb-controls"><button data-play>순서대로 재생</button><button data-next>한 단계씩 보기</button><button data-reset>처음으로</button><label>읽기 속도 <select data-speed><option value="6500">천천히</option><option value="3500">보통</option><option value="12000">여유롭게</option></select></label></div><p data-narration role="status"></p><p class="wb-note">재생은 설명 순서를 보여 줍니다. 실제 업무 시간·공수·승인 상태와는 다릅니다.</p>';
 root.append(panel);const play=panel.querySelector('[data-play]'),next=panel.querySelector('[data-next]'),reset=panel.querySelector('[data-reset]'),speed=panel.querySelector('[data-speed]'),narration=panel.querySelector('[data-narration]');
 const stop=()=>{clearTimeout(timer);timer=null;play.textContent='순서대로 재생';play.setAttribute('aria-pressed','false');};
 function show(index,animate=true){if(disposed)return;i=index;choose(i);narration.textContent=`${i+1} / ${steps.length} · ${steps[i]}`;
  if(d3&&options.diagram){const svg=d3.select(options.diagram).select('svg');svg.selectAll('.wb-traveller').interrupt().remove();const paths=svg.selectAll('path.arrow').nodes(),path=paths[Math.max(0,i-1)];if(i>0&&path){const p=path.getPointAtLength(0),dot=svg.append('circle').attr('class','wb-traveller').attr('r',6).attr('fill','#bf7e3b').attr('stroke','#fff').attr('stroke-width',2).attr('cx',p.x).attr('cy',p.y);
   if(animate&&!reduce.matches)dot.transition().duration(1100).ease(d3.easeCubicInOut).attrTween('transform',()=>t=>{const pt=path.getPointAtLength(t*path.getTotalLength());return `translate(${pt.x-p.x},${pt.y-p.y})`;});else{const end=path.getPointAtLength(path.getTotalLength());dot.attr('cx',end.x).attr('cy',end.y);}}}
 }
 function tick(){if(disposed)return;if(i>=steps.length-1){stop();return;}show(i+1);timer=setTimeout(tick,Number(speed.value));}
 play.onclick=()=>{if(timer){stop();return;}if(reduce.matches){show((i+1)%steps.length,false);return;}if(i===steps.length-1)show(0);play.textContent='일시정지';play.setAttribute('aria-pressed','true');timer=setTimeout(tick,Number(speed.value));};
 next.onclick=()=>{stop();show((i+1)%steps.length);};reset.onclick=()=>{stop();show(0);};speed.onchange=()=>{if(timer){clearTimeout(timer);timer=setTimeout(tick,Number(speed.value));}};
 const visibility=()=>{if(document.hidden)stop();};const motion=()=>{stop();play.disabled=reduce.matches;if(reduce.matches)narration.textContent='동작 줄이기 설정: 한 단계씩 보기로 같은 설명을 확인하세요.';};
 document.addEventListener('visibilitychange',visibility);reduce.addEventListener('change',motion);show(0,false);motion();
 const dispose=()=>{disposed=true;stop();document.removeEventListener('visibilitychange',visibility);reduce.removeEventListener('change',motion);if(options.diagram)d3?.select(options.diagram).selectAll('*').interrupt();panel.remove();};
 dispose.select=index=>{stop();show(index);};return dispose;
}
export function schedulePlayback(model,result,lag){
 const byId=Object.fromEntries(result.activities.map(a=>[a.id,a]));
 const steps=result.activities.map(a=>{const preds=a.predecessors.map(id=>`${id}의 EF ${byId[id].ef}${id==='D'&&a.id==='E'&&lag?' + ('+lag+')':''}`);return `${a.id}: ${preds.length?'선행 조건 '+preds.join(', ')+' 중 가장 늦은 경계가 ES '+a.es:'선행 활동이 없어 ES 0'}. EF = ES ${a.es} + 기간 ${a.duration} = ${a.ef}.`;});
 steps.push(`후진 계산: 종료 경계 ${result.finish}부터 거꾸로 LS와 LF를 계산합니다. 총여유 = LS − ES이며, 0인 활동 ${result.critical.join(' → ')}을 지연시키면 다른 조건이 같을 때 전체 완료도 늦어집니다.`);
 const host=document.createElement('section');host.className='card';host.innerHTML='<h3>계산의 이유를 순서대로 보기</h3>';document.querySelector('#schedule-result').prepend(host);
 return playback(host,steps,i=>{const id=result.activities[i]?.id;window.d3.select('#schedule-network').selectAll('[data-activity]').attr('stroke-width',d=>null).classed('wb-calculating',function(){return this.dataset.activity===id;});document.querySelectorAll('#schedule-result tbody tr').forEach((row,j)=>row.classList.toggle('wb-active-row',j===i));});
}
