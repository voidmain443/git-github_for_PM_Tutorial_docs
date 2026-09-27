"""An actionable, reading-first guide to the public Level 1 learning site.

The guide uses the same S0 records, button labels, and deep links as the reader.
It does not write progress or change the learner's selected data stage.
"""

from urllib.parse import quote


def render_guide(manual_html: str) -> str:
    """Return the guide body; the caller supplies the shared site shell and CSS."""
    g00 = quote("G00_업무파악_작성용초안.md")
    return f'''<div class="guide-page">
<section class="guide-hero" aria-labelledby="guide-title">
  <p class="guide-eyebrow">처음 사용하는 학생을 위한 학습 가이드</p>
  <h1 id="guide-title">어디서 시작하고,<br>무엇을 남기나요?</h1>
  <p class="guide-lead">교재에서 오늘의 업무를 읽고, ERP에서 근거를 찾고, 내 문서로 설명합니다. 처음에는 이 세 가지면 충분합니다. 아래에서 정산 한 건을 조회해 메모를 검토하는 과정까지 함께 해 봅니다.</p>
  <div class="guide-actions"><a class="button primary" href="learn.html?unit=0">0단원부터 읽기 →</a><a class="button" href="#guide-first-lab">첫 조회 함께 따라 하기 ↓</a></div>
  <p class="guide-hero-note">브라우저에서 바로 시작 · 로그인과 설치 불필요 · SQL은 선택 사항</p>
</section>

<div class="guide-layout">
<nav class="guide-nav" aria-label="사용 안내 차례">
  <p>필요한 곳으로</p>
  <a href="#guide-start">시작 전 준비</a>
  <a href="#guide-menus">메뉴를 여는 순간</a>
  <a href="#guide-first-lab">첫 조회부터 검토까지</a>
  <a href="#guide-save">작성본 보관하기</a>
  <a href="#guide-next">다음 단원으로 가기</a>
  <a href="#guide-faq">막혔을 때</a>
  <a href="#guide-reference">전체 ERP 참고 설명</a>
</nav>
<div class="guide-body">

<section class="guide-section" id="guide-start" aria-labelledby="guide-start-title">
  <p class="guide-eyebrow">시작 전 준비</p>
  <h2 id="guide-start-title">처음에는 교재 탭 하나만 여세요.</h2>
  <p>여러분은 가상회사 <strong>모아페이의 내부 PM 한지우</strong>입니다. 이미 운영 중인 결제·정산 서비스에서 가맹점 정산 확인과 대사, 예외처리를 개선하는 일을 맡았습니다. 0단원에서 회사 업무를 파악한 다음, 1단원에서 프로젝트 헌장을 작성합니다.</p>
  <p>먼저 <a href="learn.html?unit=0&amp;view=chapter">0단원 「회사에 합류하기」</a>를 엽니다. 위쪽의 <strong>「현재 자료: S0 · 착수 전」</strong>을 확인하고 「단원 본문 읽기」부터 시작하세요. ERP가 필요한 순간에는 교재의 조회 링크가 새 탭을 열어 줍니다. 교재 탭은 그대로 두고, 확인을 마치면 돌아오면 됩니다.</p>
  <ol class="guide-route" aria-label="한 업무를 수행하는 순서">
    <li><strong>읽기</strong><span>이번 업무와 질문</span></li>
    <li><strong>찾기</strong><span>원천 문서·ERP</span></li>
    <li><strong>작성하기</strong><span>근거와 내 판단</span></li>
    <li><strong>검토·수정</strong><span>의견과 수정 이유</span></li>
    <li><strong>넘기기</strong><span>다음 문서의 입력</span></li>
  </ol>
  <aside class="guide-note"><strong>오늘 남길 것은 짧은 업무 파악 메모입니다.</strong><p>0단원에서는 G00에 회사 업무, 확인할 사람, 조회한 금액의 뜻을 정리합니다. 모든 메뉴를 둘러보거나 새로운 문서를 여러 개 만들 필요는 없습니다. 같은 메모를 보완하며 다음 헌장 작성에 가져갈 근거를 모으세요.</p></aside>
</section>

<section class="guide-section" id="guide-menus" aria-labelledby="guide-menus-title">
  <p class="guide-eyebrow">필요한 메뉴 고르기</p>
  <h2 id="guide-menus-title">이 일이 필요할 때, 이 메뉴로 갑니다.</h2>
  <p>상단 메뉴는 별개의 과목이 아닙니다. 한 프로젝트를 읽고, 확인하고, 작성하는 데 쓰는 작업 공간입니다. 교재를 중심으로 필요한 곳을 다녀오세요.</p>
  <div class="guide-menu-list">
    <article class="guide-menu">
      <div class="guide-menu-head"><h3><a href="learn.html?unit=0">교재</a></h3><p>“지금 무엇을 해야 하지?”</p></div>
      <dl class="guide-menu-meta"><div><dt>누를 순서</dt><dd>단원 선택 → 「단원 본문 읽기」 → 「이 단원의 단계별 실습 시작하기」 → 개념·근거·작성</dd></div><div><dt>확인할 것</dt><dd>왜 하는 업무인지, 어떤 자료가 필요한지, 검토자는 무엇을 묻는지 읽습니다.</dd></div><div><dt>남길 것</dt><dd>해당 단원의 문서 초안과 검토·수정 기록. 웹 작성 영역도 교재의 「3. 작성·검토」 안에 있습니다.</dd></div></dl>
    </article>
    <article class="guide-menu">
      <div class="guide-menu-head"><h3><a href="erp.html" target="_blank" rel="noopener">ERP ↗</a></h3><p>“이 문장을 뒷받침할 회사 기록은?”</p></div>
      <dl class="guide-menu-meta"><div><dt>누를 순서</dt><dd>교재의 조회 링크 또는 ERP → 업무 메뉴 → 「초기화」 → 정확히 일치 조건 → 「조회」 → 식별자 상세</dd></div><div><dt>확인할 것</dt><dd>자료 시점, 기록 번호, 담당자, 금액과 단위. 표의 요약을 본 뒤 상세에서 이유와 연결 자료를 읽습니다.</dd></div><div><dt>남길 것</dt><dd>내 문서의 근거 위치와 확인한 사실. 조회 결과가 필요할 때만 「CSV 내보내기」를 사용합니다.</dd></div></dl>
    </article>
    <article class="guide-menu">
      <div class="guide-menu-head"><h3><a href="visual.html">시각화 워크북</a></h3><p>“관계나 변화가 그림으로는 어떻게 보일까?”</p></div>
      <dl class="guide-menu-meta"><div><dt>누를 순서</dt><dd>교재의 시각화 실습 열기, 또는 시각화 워크북 → 해당 단원 선택 → 조건 조작 → 결과 확인</dd></div><div><dt>확인할 것</dt><dd>업무가 누구에게 넘어가는지, 일정의 선후관계와 간트가 어떻게 연결되는지, 변경이 어느 계획에 영향을 주는지 봅니다.</dd></div><div><dt>남길 것</dt><dd>바꾼 조건, 달라진 결과, 내 문서에 반영할 판단. 그림을 움직였다는 사실만으로 검토나 승인이 완료되지는 않습니다.</dd></div></dl>
    </article>
    <article class="guide-menu">
      <div class="guide-menu-head"><h3><a href="#guide-first-lab">사용 안내</a></h3><p>“화면에서 어디를 누르고, 어떻게 돌아오지?”</p></div>
      <dl class="guide-menu-meta"><div><dt>누를 순서</dt><dd>이 페이지의 차례 → 필요한 작업 → 실제 화면 링크 → 원래 교재 탭으로 돌아가기</dd></div><div><dt>확인할 것</dt><dd>검색 조건, 자료 시점, 파일 보관 방법을 확인합니다. 처음에는 아래 첫 조회 예시 하나만 따라 해도 됩니다.</dd></div><div><dt>남길 것</dt><dd>별도의 사용 안내 과제는 없습니다. 막혔던 작업을 해결하고 진행 중인 문서를 계속 작성합니다.</dd></div></dl>
    </article>
    <article class="guide-menu">
      <div class="guide-menu-head"><h3><a href="resources.html">자료실</a></h3><p>“양식이나 인쇄본을 내 파일로 갖고 싶다.”</p></div>
      <dl class="guide-menu-meta"><div><dt>누를 순서</dt><dd>현재 자료의 교재·워크북 PDF, 또는 「편집할 문서 양식」 → 「양식 보기」·「원본 내려받기」</dd></div><div><dt>확인할 것</dt><dd>문서 ID와 이름, 현재 자료 시점, 기존 작성본이 있는지 확인합니다. 양식은 작성 예제가 들어 있는 답안이 아니라 빈 틀입니다.</dd></div><div><dt>남길 것</dt><dd>자신의 작업 폴더에 원본과 작성본을 구분해 보관합니다. 다음 단원에서는 같은 문서의 새 버전을 만듭니다.</dd></div></dl>
    </article>
  </div>
</section>

<section class="guide-section" id="guide-first-lab" aria-labelledby="guide-first-title">
  <p class="guide-eyebrow">함께 하는 첫 실습 · S0</p>
  <h2 id="guide-first-title">정산 한 건을, 설명 가능한 메모로.</h2>
  <p>질문은 하나입니다. <strong>“ST001의 222,440원은 어떻게 계산했고, 누구에게 줄 돈인가?”</strong> 아래는 교재와 함께 보는 안내 예시입니다. 직접 수행할 때에는 같은 순서로 ST002와 TX002001을 확인하게 됩니다.</p>
  <div class="guide-step-list">
    <article class="guide-step" id="guide-step-1">
      <span class="guide-step-number" aria-hidden="true">01</span>
      <div class="guide-step-content"><p class="guide-step-context">교재 · 업무 이해</p><h3>읽고 나서, 조회할 질문을 정합니다.</h3>
      <p>0단원 본문에서 정산과 대사의 차이를 읽습니다. <strong>정산은 지급할 금액을 계산하는 일</strong>이고, <strong>대사는 서로 다른 자료의 금액을 비교하는 일</strong>입니다. 본문 아래 「이 단원의 단계별 실습 시작하기」를 누르면 한 업무를 세 화면으로 나눠 수행합니다.</p>
      <p>실습 목차에서 「정산 한 건의 금액을 따라 읽기」를 선택하고 「2. 근거·예제」를 엽니다. S05 업무절차를 읽은 뒤 「ST001 함께 조회」를 누릅니다. 지금은 “정산금이 맞는가?”라는 질문을 ERP에 가져가는 순간입니다.</p>
      <p><a class="guide-inline-link" href="learn.html?unit=0&amp;view=practice&amp;step=settlement&amp;phase=evidence">교재의 ST001 조회 단계로 이동 →</a></p>
      <figure class="guide-screen"><a href="tour-media/read-04.webp" target="_blank" rel="noopener" aria-label="안내 화면을 원본 크기로 열기"><img src="tour-media/read-04.webp" width="1040" height="640" loading="lazy" decoding="async" alt="0단원 본문 아래의 ‘이 단원의 단계별 실습 시작하기’ 버튼에 안내 표시가 있는 실제 교재 화면"></a><figcaption>본문을 먼저 읽고, 아래 버튼으로 실제 자료를 사용하는 실습에 들어갑니다.</figcaption></figure>
      </div>
    </article>
    <article class="guide-step" id="guide-step-2">
      <span class="guide-step-number" aria-hidden="true">02</span>
      <div class="guide-step-content"><p class="guide-step-context">ERP · 조건 입력</p><h3>정산번호를 조건으로 한 건만 찾습니다.</h3>
      <p>교재의 링크로 열면 「가맹점 정산」과 조회 조건이 이미 선택되어 있습니다. 직접 찾는 연습을 하려면 다음 순서로 누르세요. <strong>위쪽 큰 검색칸이 아니라, 아래쪽 「정확히 일치」 조건</strong>을 사용합니다.</p>
      <ol class="guide-clicks"><li>ERP에서 「가맹점 정산」 메뉴를 선택합니다.</li><li>「초기화」를 눌러 이전 검색어와 조건을 지웁니다.</li><li>「정확히 일치」의 첫 번째 선택칸에서 <strong>정산번호</strong>를 고릅니다.</li><li>바로 옆 조건값 칸에 <strong>ST001</strong>을 입력하고 「조회」를 누릅니다.</li></ol>
      <p><a class="guide-inline-link" href="erp.html?menu=settlements&amp;field=정산번호&amp;value=ST001" target="_blank" rel="noopener">ST001 조건으로 ERP 새 탭 열기 ↗</a></p>
      <aside class="guide-note"><strong>확인 지점</strong><p>자료가 S0일 때 「검색 결과 1건」과 지급예정액 222,440원이 보이면 같은 예시를 찾은 것입니다. 검색 결과가 다르면 숫자를 임의로 맞추지 말고 자료 시점과 조건부터 확인하세요.</p></aside>
      </div>
    </article>
    <article class="guide-step" id="guide-step-3">
      <span class="guide-step-number" aria-hidden="true">03</span>
      <div class="guide-step-content"><p class="guide-step-context">ERP · 목록과 상세</p><h3>합계의 뜻과 계산 근거를 읽습니다.</h3>
      <p>ST001 행을 왼쪽부터 읽습니다. 거래금액에서 취소와 수수료를 빼고, 부호가 있는 조정금액을 더하면 지급예정액이 됩니다. 금액은 모두 원 단위입니다.</p>
      <div class="guide-calculation" aria-label="ST001 지급예정액 계산"><span>거래 <strong>241,000</strong></span><span>− 취소 <strong>13,000</strong></span><span>− 수수료 <strong>4,560</strong></span><span>+ 조정 <strong>−1,000</strong></span><span class="guide-calculation-result">= 지급예정 <strong>222,440원</strong></span></div>
      <p>첫 열의 <strong>ST001</strong>을 누르면 「상세·연관 기록」이 열립니다. 구성 거래와 조정 근거를 살펴보고 S05와 대조합니다. 상세 창을 닫아도 방금 사용한 검색 조건은 유지됩니다.</p>
      <figure class="guide-screen"><a href="tour-media/erp-05.webp" target="_blank" rel="noopener" aria-label="안내 화면을 원본 크기로 열기"><img src="tour-media/erp-05.webp" width="1040" height="640" loading="lazy" decoding="async" alt="S0 ERP 가맹점 정산 화면. 정산번호 ST001을 조회한 결과 1건과 지급예정액 222,440원이 표시되어 있다"></a><figcaption>검색 조건 → 전체 결과 건수 → 해당 행의 금액 → 식별자 상세 순으로 읽습니다.</figcaption></figure>
      <aside class="guide-note"><strong>222,440원은 회사 매출이나 프로젝트 비용이 아닙니다.</strong><p>이 값은 해당 정산 건의 가맹점 지급예정액입니다. S04의 회사 현금 440백만원, S01의 프로젝트 자금 한도 132백만원과 주인·용도가 다릅니다. 금액 옆에는 단위와 기준일, 무엇을 위한 금액인지 함께 적으세요.</p></aside>
      </div>
    </article>
    <article class="guide-step" id="guide-step-4">
      <span class="guide-step-number" aria-hidden="true">04</span>
      <div class="guide-step-content"><p class="guide-step-context">교재 · G00 초안</p><h3>“확인했다”를 다른 사람이 다시 찾을 수 있게 씁니다.</h3>
      <p>교재 탭으로 돌아와 「조회 기록을 G00 업무 파악 메모로 묶기」의 「3. 작성·검토」를 엽니다. 「웹에서 양식 작성하기 · 선택 사항」을 펼쳐 <strong>G00_업무파악_작성용초안.md</strong>를 선택한 뒤 「양식 열기 / 이어 쓰기」를 누릅니다. 파일로 작성하는 방법은 <a href="#guide-save">아래 작성본 보관 안내</a>에서 선택할 수 있습니다.</p>
      <div class="guide-example"><p class="guide-example-label">조회 근거 대장에 남기는 부분 예시</p><p><strong>확인한 사실</strong><br>S0 / 가맹점 정산 / 정산번호=ST001. 정산일은 2026-09-30이며 지급예정액은 222,440원이다. 거래−취소−수수료+조정의 계산 결과와 일치한다. 조정의 업무 근거는 S05에서 확인한다.</p><p><strong>나의 해석·다음 행동</strong><br>이 금액을 가맹점에 지급할 예정인 금액으로 구분한다. 다음에는 같은 절차로 ST002를 조회하고, 불일치 거래 TX002001에서 차이의 사유와 담당자를 확인한다.</p></div>
      <p>자료 기준일은 화면에서 함께 확인해 기록합니다. 위 문장은 정산일과 구분해 읽으세요. 아직 하지 않은 추가 조회나 담당자 회신을 “확인 완료”라고 적지 않습니다.</p>
      <p><a class="guide-inline-link" href="learn.html?unit=0&amp;view=practice&amp;step=draft&amp;phase=practice">G00 작성 단계로 이동 →</a></p>
      <figure class="guide-screen"><a href="tour-media/write-03.webp" target="_blank" rel="noopener" aria-label="안내 화면을 원본 크기로 열기"><img src="tour-media/write-03.webp" width="1040" height="640" loading="lazy" decoding="async" alt="교재 안에서 G00 업무 파악 메모의 조회 근거 대장 표를 편집하며 확인한 사실을 적는 실제 화면"></a><figcaption>교재 안의 작성 영역입니다. 화면 예시는 담당자 근거를 적는 칸이며, 정산 조회도 같은 방식으로 사실과 해석을 구분해 기록합니다.</figcaption></figure>
      </div>
    </article>
    <article class="guide-step" id="guide-step-5">
      <span class="guide-step-number" aria-hidden="true">05</span>
      <div class="guide-step-content"><p class="guide-step-context">교재 · 검토와 수정</p><h3>숫자를 옮긴 뒤, 의미를 검토합니다.</h3>
      <p>「메모를 검토·수정하고 헌장 단원으로 넘기기」의 「2. 근거·예제」에는 운영담당 박다은과 재무담당 최민석의 검토 질문이 있습니다. 혼자 공부한다면 그 관점으로 초안을 다시 읽고, 수업에서는 역할을 나누어 서로 검토합니다.</p>
      <ul class="guide-checklist"><li><strong>운영 관점:</strong> 업무 흐름과 담당자를 원천대로 읽었는가? 불일치를 무조건 프로그램 결함으로 단정하지 않았는가?</li><li><strong>재무 관점:</strong> 가맹점 정산금, 회사 현금, 프로젝트 자금을 구분했는가? 단위와 기준일이 있는가?</li><li><strong>다음 작성자 관점:</strong> 자료 단계, 메뉴, 검색 조건, 행 ID가 있어 같은 기록을 다시 찾을 수 있는가?</li></ul>
      <div class="guide-example"><p class="guide-example-label">검토 의견을 반영하는 방법</p><p><strong>수정 전</strong> “회사 현금 440백만원을 프로젝트 예산으로 쓴다.”</p><p><strong>수정 후</strong> “440백만원은 2026년 9월 30일 회사 현금이다. 프로젝트 자금 한도는 S01의 132백만원으로 구분하며, 상세 기준선은 계획 검토 후 별도 승인한다.”</p><p><strong>근거와 처리</strong> S04·S01·S17을 대조하고 G00의 「세 가지 돈과 기준일」을 수정한다. 초안 v0.1을 보존하고 수정본 v0.2를 만든다.</p></div>
      <p>이미 정확하게 작성했다면 일부러 오류를 만들 필요는 없습니다. 검토 기록에 충족한 문단과 근거 위치를 남기면 됩니다. 제공된 검토 질문을 적용한 연습이며, 실제 담당자에게 회신을 받은 기록과는 구분합니다.</p>
      <p><a class="guide-inline-link" href="learn.html?unit=0&amp;view=practice&amp;step=review&amp;phase=evidence">0단원 검토 질문 읽기 →</a></p>
      </div>
    </article>
    <article class="guide-step" id="guide-step-6">
      <span class="guide-step-number" aria-hidden="true">06</span>
      <div class="guide-step-content"><p class="guide-step-context">내 작업 폴더 · 다음 업무</p><h3>파일을 남기고, 헌장에 쓸 근거를 넘깁니다.</h3>
      <p>이 예시를 따라온 다음에는 0단원의 나머지 항목도 차례대로 수행하세요. <strong>ST002와 TX002001은 직접 확인할 자료</strong>입니다. 사람과 업무 흐름, 회사의 돈까지 설명할 수 있고 검토 질문을 처리했다면 G00 작성본을 파일로 보관합니다.</p>
      <ul class="guide-checklist"><li>사업을 시작하는 이유 → S01</li><li>상위 범위와 인수 조건 → S03</li><li>PM과 검토자·승인자의 권한 → S02</li><li>목표 측정 기간과 업무 경계 → S17</li></ul>
      <p>이 자료들이 1단원 D01 헌장의 입력이 됩니다. <strong>0단원의 메모 검토 완료와 프로젝트 헌장 승인은 서로 다른 일</strong>입니다. G00에 임의의 스폰서 승인번호를 만들지 않습니다.</p>
      <p><a class="guide-inline-link" href="learn.html?unit=1&amp;view=chapter">다음 업무, 프로젝트 헌장 읽기 →</a></p>
      </div>
    </article>
  </div>
</section>

<section class="guide-section" id="guide-save" aria-labelledby="guide-save-title">
  <p class="guide-eyebrow">작성본 보관</p>
  <h2 id="guide-save-title">작성 방법은 하나를 고르고, 파일은 직접 보관하세요.</h2>
  <p>웹 작성과 파일 편집은 같은 양식을 사용하는 두 가지 방법입니다. 두 곳에 같은 내용을 다시 쓸 필요는 없습니다. 문서 본문을 작성한 곳을 정하고, 워크북에는 사용한 문서와 항목 위치만 연결해도 됩니다.</p>
  <div class="guide-options">
    <article><h3>웹 안에서 작성할 때</h3><ol><li>교재의 「3. 작성·검토」에서 「웹에서 양식 작성하기 · 선택 사항」을 펼칩니다.</li><li>문서를 고르고 「양식 열기 / 이어 쓰기」를 누릅니다. 표의 칸에서 내용을 작성합니다. 문단이나 행을 더 고치려면 「원문으로 편집 · 행 추가와 자유 서술」을 펼칩니다.</li><li>이동하기 전에 「작성본 내려받기」를 누르고 실제 다운로드 파일을 확인합니다.</li><li>다음에 이어 쓸 때 같은 양식을 선택하고 「이 문서의 작성본 불러오기」로 보관한 파일을 엽니다.</li></ol></article>
    <article><h3>내 편집기에서 작성할 때</h3><ol><li>교재의 「파일로 작성할 양식 내려받기」 또는 자료실에서 양식을 받습니다.</li><li>Markdown 편집기로 원본을 열거나 「양식 보기」의 표를 문서 편집기에 복사합니다.</li><li>원본을 보존하고 프로젝트·문서·버전을 구분해 저장합니다. 예: <code>MP-01_G00_한지우_v0.1.md</code>.</li><li>검토 의견을 반영하면 v0.2로 보관합니다. 다음 단원에서 필요한 문장을 찾아 이어 씁니다.</li></ol><p><a href="templates/{g00}" download>G00 편집용 원본 내려받기 ↓</a></p></article>
  </div>
  <aside class="guide-note"><strong>웹 초안은 자동 저장되지 않습니다.</strong><p>작성 내용은 페이지 메모리에만 있습니다. 새로고침, 다른 페이지 이동, 탭 닫기 전에 파일을 내려받으세요. 브라우저가 기억하는 자료 시점·읽던 위치와 내 작성본은 별개입니다. ERP의 「CSV 내보내기」는 조회 결과를 보관하는 기능이며 작성 문서를 저장하는 버튼이 아닙니다.</p></aside>
</section>

<section class="guide-section" id="guide-next" aria-labelledby="guide-next-title">
  <p class="guide-eyebrow">다음 자료로 이동</p>
  <h2 id="guide-next-title">다음 화면은 열 수 있어도, 다음 자료는 순서대로.</h2>
  <p>회사의 기록은 프로젝트가 진행되며 추가됩니다. 처음부터 종료 결과를 보고 계획을 쓰지 않도록 자료를 시점별로 나눴습니다. 각 단원의 인계 안내에 따라 <strong>현재 업무의 작성·검토를 마친 뒤</strong> 다음 자료를 여세요.</p>
  <ol class="guide-stages"><li><strong>S0</strong><span>착수 전</span></li><li><strong>S0A</strong><span>헌장 승인</span></li><li><strong>S1</strong><span>분야 계획</span></li><li><strong>S1A</strong><span>통합 승인·킥오프</span></li><li><strong>S2</strong><span>실행·변경 분석</span></li><li><strong>S3</strong><span>변경 승인</span></li><li><strong>S4</strong><span>검수·종료</span></li></ol>
  <p>교재 위쪽의 「현재 자료」를 펼쳐 「조회할 자료」를 선택하고 「선택한 자료 열기」를 누릅니다. 설치나 서버 실행은 필요하지 않습니다. 같은 사이트를 연 다른 탭도 같은 시점으로 갱신됩니다. 개인 학습은 완료 기준을 대조하고, 수업에서는 강사가 안내한 시점을 사용하세요.</p>
  <p>시점 선택은 공개된 수업 자료의 순서를 맞추는 기능입니다. 버튼을 눌렀다고 여러분의 문서가 승인되거나 학습 평가를 통과하는 것은 아닙니다. 승인 실습에서는 승인 기준·권한·근거 기록을 별도로 확인합니다.</p>
  <p><a class="guide-inline-link" href="pathway.html">Level 1 완료 기준과 다음 레벨 살펴보기 →</a></p>
</section>

<section class="guide-section" id="guide-faq" aria-labelledby="guide-faq-title">
  <p class="guide-eyebrow">문제 해결</p>
  <h2 id="guide-faq-title">멈춘 지점에서 바로 해결하기.</h2>
  <div class="guide-faq">
    <details><summary>검색 결과가 0건입니다. 무엇부터 확인하나요?</summary><div><p>자료 시점 → 메뉴 → 「초기화」 → 조건 항목 → 조건값 순서로 확인합니다. S0의 가맹점 정산에서 첫 조건을 정산번호, 값을 ST001로 입력하면 예시 한 건을 찾을 수 있습니다. 통합검색에 이전 글자가 남아 있거나 두 번째 조건이 설정되어 있으면 모든 조건을 만족하는 행만 나옵니다.</p><p>기록 번호의 앞글자도 구분하세요. 사람은 P, 원천 문서는 S, 정산 배치는 ST, 거래는 TX입니다.</p></div></details>
    <details><summary>S0에서 예산·기준선이나 구매 자료가 비어 있습니다.</summary><div><p>S0는 착수 전이므로 상세 승인 기준선, 비용 실적, 발주·검수 결과가 아직 없는 것이 정상입니다. S01의 자금 한도와 승인된 상세 기준선은 다른 자료입니다. 빈 화면을 “프로젝트 예산 0원 확정”이라고 쓰지 마세요. 해당 단원의 계획·실행 시점에서 다시 조회합니다.</p></div></details>
    <details><summary>교재 예시와 ERP의 숫자 또는 문서가 다릅니다.</summary><div><p>교재와 ERP가 같은 자료 시점인지 먼저 확인합니다. 이 안내의 정산 예시는 S0 기준입니다. 다른 기기나 새 브라우저에서는 S0부터 열릴 수 있습니다. 「이후 공개」 또는 「자료 미공개」는 현재 시점에 아직 없는 자료라는 뜻입니다. 미래 자료를 먼저 열어 숫자를 맞추지 말고 교재의 인계 순서를 확인하세요.</p></div></details>
    <details><summary>표에는 50행인데 검색 결과는 더 많습니다.</summary><div><p>목록은 한 번에 최대 50건씩 표시합니다. 「다음 50건」으로 다음 페이지를 보세요. 「검색 결과」의 전체 건수와 지금 표시된 행 수를 구분합니다. 「CSV 내보내기」는 현재 검색 조건에 맞는 결과 전체를 저장합니다. 이 수업의 표본은 내보내기 제한 10,000건보다 작습니다.</p></div></details>
    <details><summary>작성한 내용이 새로고침 후 사라졌습니다.</summary><div><p>웹 초안은 서버나 브라우저 저장소에 자동 보관되지 않습니다. 미리 내려받은 작성본이 있다면 해당 양식을 고른 뒤 「이 문서의 작성본 불러오기」로 다시 엽니다. 아직 내보내지 않은 초안은 복원할 수 없습니다. 다음부터는 작업을 마치거나 이동하기 전에 「작성본 내려받기」와 파일 생성 여부를 확인하세요.</p></div></details>
    <details><summary>시각화만 끝내면 해당 문서도 완성된 건가요?</summary><div><p>그림은 관계와 영향을 확인하는 도구입니다. 무엇을 바꿨고 결과가 왜 달라졌는지 해석한 다음, 교재로 돌아와 문서의 해당 항목과 검토 기록을 보완합니다. 예를 들어 간트 막대가 바뀌었다면 작업의 선후관계와 완료일에 어떤 영향이 생겼는지 일정 문서에 설명합니다. 실습에서 움직인 결과는 실제 회사 기록이나 승인 상태를 바꾸지 않습니다.</p></div></details>
    <details><summary>SQL을 모르거나 로컬 서버를 실행할 수 없어도 되나요?</summary><div><p>이 공개 웹사이트에서는 브라우저만 있으면 됩니다. ERP의 업무 메뉴와 검색 화면으로 Level 1을 진행할 수 있고, SQL은 같은 데이터를 직접 조회해 보고 싶은 학습자의 선택 경로입니다. 화면이 열리지 않으면 인터넷 연결과 주소를 확인한 뒤 새로고침하세요. 별도 로컬 배포팩을 내려받은 경우에만 그 팩의 실행 안내를 따릅니다.</p></div></details>
  </div>
</section>

<section class="guide-section" id="guide-reference" aria-label="ERP 상세 참고 설명">
  <details class="guide-reference"><summary>전체 ERP 참고 설명</summary><div class="guide-reference-body"><p>필드의 뜻, 검색과 SQL, 전표 부호 등 더 자세한 설명이 필요할 때 펼쳐 읽으세요.</p>{manual_html}</div></details>
</section>
<section class="guide-finish" aria-labelledby="guide-finish-title"><h2 id="guide-finish-title">이제, 첫 질문을 가지고 교재로 돌아가세요.</h2><p>“내가 개선할 업무는 무엇이고, 이 사실을 어디서 확인할 수 있을까?”<br>이 질문으로 읽기 시작하면 화면의 메뉴가 해야 할 일과 연결됩니다.</p><a class="button primary" href="learn.html?unit=0&amp;view=chapter">0단원 본문 열기 →</a><a class="guide-inline-link" href="index.html#outcome-lab">문서와 시각화 결과 예시 보기 →</a></section>
</div>
</div>
</div>'''
