"""Readable, progressively enhanced landing page for the learner publication."""
from html import escape as e
import json
from landing_content import COMPARISON_NOTICE, COMPARISONS, LESSON_PATH


def site_navigation(prefix='', current=''):
    links = [('learn.html?unit=0','교재'),('visual.html','시각화 워크북'),('erp.html','ERP'),('guide.html','사용 안내'),('resources.html','자료실')]
    items = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if url.split('?')[0] == current else '')+f'>{label}</a>' for url,label in links)
    target = 'workspace' if current == 'erp.html' else 'content'
    return f'''<a class="site-skip" href="#{target}">본문으로 바로가기</a><header class="site-header"><nav class="site-nav" aria-label="주 메뉴"><a class="site-brand" href="{prefix}index.html"><span class="site-brand-mark" aria-hidden="true">M</span><span><strong>모아페이 · PM 실습</strong><small>FROM EVIDENCE TO DECISION</small></span></a><button type="button" id="site-menu-toggle" aria-expanded="false" aria-controls="site-links">메뉴</button><div class="site-links" id="site-links">{items}</div></nav></header>'''


def site_footer(prefix=''):
    return f'''<footer class="site-footer"><div><strong>모아페이 · 금융 프로젝트 PM 실습</strong><p>가상 회사에서 연습하는 실제 PM의 일.</p></div><div>Level 1 · 교육용 가상 자료<br>완료 판단은 문서의 근거·판단·연결을 확인합니다.<br><a href="{prefix}pathway.html">완료 기준과 후속 레벨</a> · <a href="{prefix}standards.html">표준 적용 안내</a></div><div>학습 기록을 서버에 제출하지 않습니다.<br>실제 수강생 파일럿과 수업 시간 측정은 별도 진행합니다.</div></footer>'''


def workspace_svg():
    return '''<svg id="scene-fallback" viewBox="0 0 680 460" role="img" aria-labelledby="desk-title desk-desc">
<title id="desk-title">원천자료에서 헌장, 계획, 변경 기록, 운영 인계로 이어지는 PM의 책상</title>
<desc id="desk-desc">각 문서는 앞 문서의 근거를 이어받습니다. 아래 단계 버튼으로 필요한 업무를 살펴볼 수 있습니다.</desc>
<defs><pattern id="desk-grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#78928e" stroke-opacity=".13"/></pattern><filter id="paper-shadow" x="-30%" y="-30%" width="180%" height="190%"><feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#0b2930" flood-opacity=".18"/></filter></defs>
<rect x="10" y="10" width="660" height="435" rx="4" fill="url(#desk-grid)"/>
<g fill="none" stroke="#779f95" stroke-width="2" stroke-dasharray="4 7"><path d="M173 195C173 115 326 160 326 115"/><path d="M407 150C545 150 485 255 543 255"/><path d="M534 310C534 403 303 325 303 365"/><path d="M238 351C136 365 150 255 112 255"/></g>
<g data-desk-stage="0" transform="translate(50 154) rotate(-9 80 70)" filter="url(#paper-shadow)"><rect width="165" height="202" rx="3" fill="#e4eae6"/><rect x="8" y="-8" width="165" height="202" rx="3" fill="#fffdf6"/><rect x="23" y="12" width="30" height="4" fill="#d4a653"/><text x="23" y="45" fill="#173443" font-size="17" font-weight="700">회사 원천자료</text><text x="23" y="68" fill="#607480" font-size="11">S01 · S02 · S05</text><path d="M23 89H150M23 105H138M23 121H149M23 137H117" stroke="#b9cac4" stroke-width="3"/><rect x="23" y="155" width="83" height="19" rx="2" fill="#e7eeec"/><text x="29" y="169" font-size="10" fill="#176a62">사실에서 시작</text></g>
<g data-desk-stage="1" transform="translate(245 56) rotate(5 95 100)" filter="url(#paper-shadow)"><rect x="5" y="8" width="202" height="264" rx="3" fill="#cad8d1"/><rect width="202" height="264" rx="3" fill="#fffefa"/><path d="M0 0H202V8H0Z" fill="#176a62"/><text x="22" y="40" fill="#607480" font-size="10" letter-spacing="2">PROJECT CHARTER</text><text x="22" y="70" fill="#173443" font-size="23" font-weight="700">프로젝트 헌장</text><text x="22" y="96" fill="#607480" font-size="11">MP-01 / 모아페이</text><path d="M22 113H180" stroke="#d1dbd6"/><g fill="#173443" font-size="12"><text x="22" y="140">시작할 이유</text><text x="22" y="177">목표와 범위</text><text x="22" y="214">책임과 권한</text></g><path d="M22 153H169M22 190H154M22 227H175" stroke="#c3d1cb" stroke-width="3"/><rect x="132" y="28" width="47" height="18" rx="9" fill="#e7eeec"/><text x="141" y="40" fill="#176a62" font-size="9">검토용</text></g>
<g data-desk-stage="2" transform="translate(456 212) rotate(9 85 60)" filter="url(#paper-shadow)"><rect width="178" height="169" rx="3" fill="#fffefa"/><text x="18" y="30" fill="#173443" font-size="16" font-weight="700">실행할 계획</text><text x="18" y="51" fill="#607480" font-size="10">범위 → 일정 → 예산</text><path d="M48 66V145M80 66V145M112 66V145M144 66V145" stroke="#e0e8e3"/><g fill="#b6cdc5"><rect x="18" y="73" width="53" height="12" rx="2"/><rect x="56" y="97" width="68" height="12" rx="2"/></g><rect x="104" y="121" width="55" height="12" rx="2" fill="#176a62"/></g>
<g data-desk-stage="3" transform="translate(248 346) rotate(-4)"><rect width="164" height="66" rx="3" fill="#e2b763"/><text x="16" y="28" fill="#173443" font-size="13" font-weight="700">이 결정의 근거는?</text><text x="16" y="48" fill="#3f5151" font-size="11">작성 → 검토 → 수정 → 승인</text></g>
<g data-desk-stage="4"><circle cx="497" cy="117" r="26" fill="none" stroke="#acc2b9"/><path d="M485 117L494 125L510 109" fill="none" stroke="#176a62" stroke-width="3"/><text x="497" y="158" text-anchor="middle" fill="#526d68" font-size="11">운영 인계</text></g>
</svg>'''


def render_landing(modules, tour):
    first = LESSON_PATH[0]
    compare = COMPARISONS[0]
    scene_labels = ['근거', '헌장', '계획', '변경', '인계']
    scene_buttons = ''.join(f'<button type="button" data-scene-stage="{i}" aria-pressed="{str(i == 0).lower()}"><span>0{i+1}</span>{label}</button>' for i, label in enumerate(scene_labels))
    journey_buttons = ''.join(f'<button type="button" data-journey="{i}" aria-pressed="{str(i == 0).lower()}"><span>{"·".join(map(str,p["units"]))}단원</span><strong>{e(p["label"])}</strong><b aria-hidden="true">↗</b></button>' for i,p in enumerate(LESSON_PATH))
    outcomes = ['회사 자료를 읽는 기준','착수할 이유와 권한','요구·범위·완료 조건','작업 순서와 담당 자원','추정·예산·현금 구분','품질 확인과 위험 대응','외주·팀·소통의 약속','계획 통합과 실행 기록','성과·편차·변경 판단','인수·이관·종료의 증거']
    unit_links = ''.join(f'<a href="learn.html?unit={i}"><span class="landing-unit-no">{i:02}</span><span><strong>{e(title)}</strong><small>{outcomes[i]}</small></span><span aria-hidden="true">↗</span></a>' for i,title in enumerate(modules))
    compare_buttons = ''.join(f'<button type="button" data-compare="{c["id"]}" aria-pressed="{str(i == 0).lower()}">{e(c["label"])}</button>' for i,c in enumerate(COMPARISONS))
    change_list = ''.join(f'<li><strong>{e(c["label"])}</strong><span>{e(c["why"])}</span></li>' for c in compare['changes'])
    data = json.dumps({'path':LESSON_PATH,'comparisons':COMPARISONS}, ensure_ascii=False).replace('<', '\\u003c')
    return f'''
<section class="landing-hero" aria-labelledby="landing-title">
 <div class="landing-hero-copy"><p class="landing-kicker"><span></span>금융 프로젝트 PM 실습 · LEVEL 1</p>
 <h1 id="landing-title">흩어진 자료를,<br>설명할 수 있는<br><em>프로젝트로.</em></h1>
 <p class="landing-lead">첫 프로젝트를 맡았다면, 무엇부터 해야 할까요?<br>회사 자료를 읽고, 문서를 쓰고, 검토를 거쳐<br class="landing-desktop-break"> 다음 결정으로 이어 가는 PM의 일을 배웁니다.</p>
 <div class="landing-actions"><a class="landing-button landing-primary" href="learn.html?unit=0">0단원부터 시작하기 →</a><a class="landing-text-link" href="#comparison">내 문서는 어떻게 달라질까? ↘</a></div>
 <p class="landing-micro">설치·로그인 없이 시작 · 한국어 교재 · 가상회사 원천자료</p></div>
 <div class="landing-workspace"><div class="landing-desk-top"><span>MOAPAY / PM WORKSPACE</span><button type="button" id="scene-toggle" aria-pressed="false" hidden>입체 모형으로 보기</button></div>
 <div class="landing-scene-wrap">{workspace_svg()}<div id="scene-host" hidden aria-hidden="true"></div></div>
 <div class="landing-scene-steps" aria-label="프로젝트 문서의 연결">{scene_buttons}</div>
 <div class="landing-scene-caption"><strong id="scene-heading">모든 문장은 근거에서 시작합니다.</strong><p id="scene-description">회사 자료·인터뷰·거래 기록에서 사실을 찾고, 확인이 필요한 조건을 구분합니다.</p></div><p id="scene-status" role="status" class="landing-sr-only"></p>
 </div>
</section>
<section class="landing-context" aria-labelledby="context-title"><p class="landing-kicker">당신의 첫 업무</p><div><h2 id="context-title">모아페이의 내부 PM,<br>한지우로 합류합니다.</h2><p>결제·정산 서비스는 이미 운영 중입니다. 이번 임무는 가맹점 정산을 확인하고, 대사하고, 예외를 처리하는 일을 개선하는 것. 운영·재무·개발 담당자가 제공한 자료를 바탕으로 프로젝트를 이끌어 보세요.</p></div><dl><div><dt>10개 단원</dt><dd>입사 첫날부터 종료까지</dd></div><div><dt>49개 프로세스</dt><dd>문서·검토·결정으로 실습</dd></div><div><dt>하나의 프로젝트</dt><dd>앞에서 쓴 문서를 계속 연결</dd></div></dl></section>
<section id="journey" class="landing-section" aria-labelledby="journey-heading"><div class="landing-section-intro"><p class="landing-kicker">배우는 순서</p><h2 id="journey-heading">문서의 이름보다,<br>일이 이어지는 이유를.</h2><p>단계를 선택해 입력 자료가 어떤 판단과 결과로 이어지는지 살펴보세요. 계획은 실행 중에도 다시 검토하고 갱신합니다.</p></div>
<div class="landing-journey-grid"><div class="landing-journey-nav" aria-label="학습 여정 선택">{journey_buttons}</div><div class="landing-journey-detail"><p class="landing-kicker" id="journey-units">0·1단원</p><h3 id="journey-title">{e(first['label'])}</h3><p id="journey-question" class="landing-question">{e(first['question'])}</p><div id="journey-diagram" aria-label="자료에서 산출물로 이어지는 흐름"><ol class="landing-flow"><li>사업 제안·운영 자료</li><li>목표·범위·권한 정리</li><li>담당자 검토</li><li>헌장·이해관계자</li></ol></div><dl class="landing-journey-notes"><div><dt>내가 하는 일</dt><dd id="journey-action">{e(first['action'])}</dd></div><div><dt>설명할 수 있는 것</dt><dd id="journey-result">{e(first['result'])}</dd></div></dl><p id="journey-artifact" class="landing-artifacts">{e(first['artifact'])}</p><a id="journey-link" class="landing-text-link" href="learn.html?unit=0">이 구간의 교재 읽기 →</a></div></div></section>
<div class="landing-tour-wrap">{tour}</div>
<section class="landing-section landing-syllabus" aria-labelledby="syllabus-title"><div class="landing-section-intro"><p class="landing-kicker">읽고, 조회하고, 작성하기</p><h2 id="syllabus-title">한 단원씩.<br>하나의 프로젝트가 남도록.</h2><p>본문으로 개념을 이해하고 원천자료를 찾아 작성합니다. 검토 의견을 반영한 문서는 다음 단원의 입력이 됩니다. 관계가 헷갈릴 때 시각화 워크북을 펼쳐 보세요.</p><a class="landing-text-link" href="visual.html">흐름도·간트·원가를 직접 살펴보기 ↗</a></div><div class="landing-unit-list">{unit_links}</div></section>
<section class="landing-start-notes" aria-labelledby="start-notes-title"><div><p class="landing-kicker">시작하기 전에</p><h2 id="start-notes-title">따라갈 수 있도록,<br>필요한 자료부터.</h2><p>설명·원천·작성 양식이 같은 프로젝트를 가리킵니다.</p><a class="landing-text-link" href="guide.html">ERP 첫 사용 안내 →</a></div><div><details><summary>ERP나 SQL을 처음 써도 되나요?</summary><p>업무별 메뉴에서 조건을 고르고 조회하면 됩니다. 교재가 어떤 메뉴에서 어떤 행을 확인할지 안내합니다. SQL은 같은 자료를 읽는 선택 학습 경로입니다.</p></details><details><summary>조회했는데 자료가 비어 있어요.</summary><p>처음에는 착수 전 자료 S0를 읽습니다. 아직 승인하지 않은 계획이나 발생하지 않은 실적은 비어 있습니다. 해당 단원의 검토를 마친 뒤 교재의 자료 선택으로 다음 시점을 엽니다.</p></details><details><summary>작성하고 승인받는 과정은 어떻게 하나요?</summary><p>웹 워크북 또는 내려받은 양식에 문서를 작성하고, 제공된 검토 의견과 승인 조건을 대조합니다. 자료를 열거나 시뮬레이션을 실행한 것만으로 내 문서가 승인되지는 않습니다. 개인 학습은 제공 기록으로, 수업은 같은 내용을 역할 활동으로 진행합니다.</p></details><details><summary>Level 1을 마친 다음에는요?</summary><p>근거를 찾고 문서를 연결하는 독립 수행을 먼저 확인합니다. Level 2는 변경과 편차, Level 3는 불확실성과 이해관계 조정, Level 4는 사업 성과와 복수 프로젝트로 확장합니다. 후속 레벨은 교육 체계를 설계한 단계입니다.</p><a href="pathway.html">완료 기준과 다음 레벨 →</a></details></div></section>
<section id="comparison" class="landing-section landing-comparison" aria-labelledby="comparison-title"><div class="landing-section-intro"><p class="landing-kicker">학습이 향하는 변화</p><h2 id="comparison-title">“작성했습니다”에서<br><em>“이렇게 판단했습니다”로.</em></h2><p>멋진 양식보다 중요한 것은 근거와 책임이 읽히는 문장입니다. 같은 상황의 초안을 비교하고, 내 문서에 더할 내용을 찾아보세요.</p></div>
<div class="landing-compare-tabs" aria-label="비교할 문장 선택">{compare_buttons}</div><p id="compare-document" class="landing-document-label">{e(compare['document'])} · 근거 {', '.join(compare['sources'])}</p>
<div class="landing-papers"><article class="landing-paper landing-paper-before"><div class="landing-paper-label"><span>BEFORE</span><b>첫 초안</b></div><h3 id="compare-before-title">{e(compare['before']['title'])}</h3><p id="compare-before">{e(compare['before']['body'])}</p><span class="landing-paper-foot">다음 사람이 같은 뜻으로 이해할 수 있을까요?</span></article><article class="landing-paper landing-paper-after"><div class="landing-paper-label"><span>AFTER</span><b>근거를 반영한 작성 예시</b></div><h3 id="compare-after-title">{e(compare['after']['title'])}</h3><p id="compare-after">{e(compare['after']['body'])}</p><span class="landing-paper-foot">교육용 부분 예시 · 실제 승인 기록 아님</span></article></div>
<div class="landing-revision-control"><label for="compare-range">문장을 다듬는 과정</label><input id="compare-range" type="range" min="0" max="2" step="1" value="2" aria-valuetext="검토 가능한 문장"><output id="compare-phase" for="compare-range">검토 가능한 문장</output></div>
<ol id="compare-changes" class="landing-changes">{change_list}</ol><div class="landing-compare-question"><p id="compare-question">{e(compare['question'])}</p><a id="compare-link" class="landing-text-link" href="{e(compare['link'],quote=True)}">이 문장을 쓰는 실습으로 →</a></div><p class="landing-notice">{e(COMPARISON_NOTICE)}</p></section>
<section class="landing-finish"><p class="landing-kicker">이제, 내 프로젝트의 첫 페이지</p><h2>빈 양식을 채우는 사람에서,<br>다음 일을 연결하는 PM으로.</h2><p>헌장, 계획, 실행 기록, 변경 판단, 종료 인계.<br>각 문서가 왜 필요한지 설명할 수 있는 기록을 만들어 보세요.</p><a class="landing-button landing-primary" href="learn.html?unit=0">내 첫 프로젝트 시작하기 →</a><a class="landing-text-link" href="resources.html">교재·양식·인쇄본 둘러보기</a></section>
<script type="application/json" id="landing-data">{data}</script>
<noscript><p>입체 모형과 단계 선택은 JavaScript를 켜면 사용할 수 있습니다. 위 안내와 단원 링크로 학습을 시작할 수 있습니다.</p></noscript>'''
