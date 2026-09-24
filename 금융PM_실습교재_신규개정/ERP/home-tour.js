/* Prerecorded UI guidance. No ERP API, learner records, or automatic playback. */
(function(){
'use strict';
const $=s=>document.querySelector(s),host=$('#home-tour');if(!host)return;
const {clips}=JSON.parse($('#home-tour-data').textContent),media=name=>'tour-media/'+name;
let selected=0,frame=0,playing=false,started=0,request=0,controller=null,objectURL=null,timers=[];
const blobs=new Map(),motion=matchMedia('(prefers-reduced-motion: reduce)');
const status=text=>$('#tour-status').textContent=text;
const clip=()=>clips[selected];
function caption(){const c=clip();$('#tour-frame-label').textContent=`${frame+1} / ${c.frames.length}컷 · ${c.frames[frame].label}`;$('#tour-screen').alt=c.frames[frame].label;$('#tour-prev-frame').disabled=frame===0;$('#tour-next-frame').disabled=frame===c.frames.length-1;}
function still(){const c=clip(),img=$('#tour-screen');img.src=media(c.frames[frame].still);img.width=c.width;img.height=c.height;caption();}
function clearPlayback(){
 request++;controller?.abort();controller=null;timers.forEach(clearTimeout);timers=[];
 if(playing){const elapsed=performance.now()-started;frame=Math.max(0,clip().frames.findLastIndex(f=>f.atMs<=elapsed));}
 playing=false;$('#tour-play').disabled=false;$('#tour-play').setAttribute('aria-pressed','false');$('#tour-play').textContent='▶ 처음부터 재생';still();
 if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}
}
function stop(message){clearPlayback();if(message)status(message);}
function choose(index){
 clearPlayback();selected=index;frame=0;const c=clip();still();
 document.querySelectorAll('[data-tour-step]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.tourStep===c.id));
 $('#tour-step-label').textContent=`${selected+1} / ${clips.length} · ${c.short}`;
 for(const key of ['title','action','check','handoff'])$('#tour-'+key).textContent=c[key];
 $('#tour-open').href=c.link;$('#tour-open').textContent=c.linkText;
 $('#tour-gif').href=media(c.gif);$('#tour-gif').download=c.gif;$('#tour-play').textContent='▶ 이 단계 재생';
 status(motion.matches?'동작 줄이기 설정이 켜져 있습니다. 컷을 넘겨 읽거나 원할 때만 재생하세요.':'자동으로 재생되지 않습니다. 화면 속 버튼은 안내용이며, 실제 실습은 아래 링크에서 시작합니다.');
}
async function play(){
 if(playing){stop('현재 컷에서 멈췄습니다. 컷을 넘겨 보거나 처음부터 다시 재생할 수 있습니다.');return;}
 clearPlayback();frame=0;still();const current=clip(),token=++request;
 $('#tour-play').disabled=true;status('이 단계의 GIF를 불러오고 있습니다…');controller=new AbortController();
 try{
  let blob=blobs.get(current.id);
  if(!blob){const response=await fetch(media(current.gif),{signal:controller.signal});if(!response.ok)throw Error('GIF를 불러오지 못했습니다.');blob=await response.blob();blobs.set(current.id,blob);}
  if(token!==request)return;
  objectURL=URL.createObjectURL(blob);const probe=new Image();probe.src=objectURL;await probe.decode();
  if(token!==request)return;
  $('#tour-screen').src=objectURL;playing=true;started=performance.now();controller=null;
  $('#tour-play').disabled=false;$('#tour-play').textContent='■ 현재 컷에서 멈추기';$('#tour-play').setAttribute('aria-pressed','true');
  status('녹화 화면을 한 번 재생합니다. 정지하거나 컷을 넘겨 원하는 위치를 확인하세요.');
  current.frames.forEach((f,i)=>{if(i)timers.push(setTimeout(()=>{if(token===request&&playing){frame=i;caption();}},f.atMs));});
  timers.push(setTimeout(()=>{if(token===request){stop();frame=current.frames.length-1;still();status('이 단계의 안내가 끝났습니다. 아래 링크로 직접 해보거나 다음 단계를 선택하세요.');}},current.durationMs));
 }catch(error){if(token!==request)return;stop('GIF를 불러오지 못했습니다. 이전·다음 컷과 아래 글 설명은 계속 사용할 수 있습니다.');}
}
document.querySelectorAll('[data-tour-step]').forEach(b=>b.addEventListener('click',()=>choose(clips.findIndex(c=>c.id===b.dataset.tourStep))));
$('#tour-play').addEventListener('click',play);
function move(delta){clearPlayback();frame=Math.max(0,Math.min(clip().frames.length-1,frame+delta));still();status('정지 화면입니다. 강조된 위치와 아래 설명을 함께 확인하세요.');}
$('#tour-prev-frame').addEventListener('click',()=>move(-1));$('#tour-next-frame').addEventListener('click',()=>move(1));
$('#tour-zoom').addEventListener('click',()=>{
 clearPlayback();const c=clip(),img=$('#tour-zoom-image');img.src=media(c.frames[frame].still);img.width=c.width;img.height=c.height;img.alt=c.frames[frame].label;
 $('#tour-zoom-caption').textContent=$('#tour-frame-label').textContent;$('#tour-dialog').showModal();$('#tour-dialog-close').focus();
 const focus=c.frames[frame].focus||{x:c.width/2,y:c.height/2};
 requestAnimationFrame(()=>{const pane=$('.tour-zoom-scroll');pane.scrollTo({left:Math.max(0,focus.x-pane.clientWidth/2),top:Math.max(0,focus.y-pane.clientHeight/2),behavior:'instant'});});
});
$('#tour-dialog-close').addEventListener('click',()=>$('#tour-dialog').close());
$('#tour-dialog').addEventListener('close',()=>$('#tour-zoom').focus());
document.addEventListener('visibilitychange',()=>{if(document.hidden&&(playing||controller))stop('다른 화면으로 이동해 재생을 멈췄습니다.');});
if('IntersectionObserver' in window)new IntersectionObserver(entries=>{if(!entries[0].isIntersecting&&(playing||controller))stop('안내 화면을 벗어나 재생을 멈췄습니다.');},{threshold:0}).observe($('#tour-screen'));
motion.addEventListener('change',()=>{if(motion.matches){stop('동작 줄이기 설정에 따라 재생을 멈췄습니다. 컷을 하나씩 넘겨 확인하세요.');}});
window.addEventListener('pagehide',()=>clearPlayback());
choose(0);
})();
