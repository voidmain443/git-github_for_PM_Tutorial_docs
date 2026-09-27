/* Original educational example data. No MP-01 facts, learner records, or live approvals. */
export const EXAMPLE_CASE = {
  id: 'PREVIEW-02', company: '가상회사 루멘페이', title: '가맹점 정산 대사·예외처리 개선',
  label: '독립 가상 사례 · 검토 초안', moneyUnit: 'KRW', displayMoneyUnit: '백만원',
  notice: '이 사례의 회사·인물·근거·수치는 문서의 작성과 검토를 비교하기 위해 만든 PREVIEW-02 전용 자료입니다. 본 교재 MP-01의 원천자료·미래 결과·정답이 아니며 ERP 단계나 학습자 작성물을 변경하지 않습니다.',
  approvalNotice: 'BL-01은 사례 내부에서 이미 승인되었다고 가정한 비교 기준입니다. 아래의 문서와 CR-02는 검토 초안이며 실제 서명·승인 또는 새로운 기준선 발효를 뜻하지 않습니다.',
  policyNotice: '권한 분리, 증빙 365일 보관, 보고 주기와 상정 기준은 이 가상회사의 교육용 내부 정책입니다. 특정 법률·금융 규정의 요구사항으로 제시하지 않습니다.',
  startDate: '2026-11-02', baselineFinish: '2026-12-01', statusDate: '2026-11-13',
  budget: 120000000, fundingLimit: 150000000, managementReserve: 30000000,
  calendar: {id: 'CAL-P02', name: 'PREVIEW-02 프로젝트 달력', weekdays: [1, 2, 3, 4, 5], hoursPerDay: 8, holidays: [], startDate: '2026-11-02', rule: '월~금, 하루 8시간, 본 사례 기간에 별도 휴무 없음. FS 관계, 리드·래그 0. 시작 경계 ES=0은 11월 2일 업무 시작이며 종료일은 EF번째 영업일의 업무 종료다.'},
};

export const EXAMPLE_REFERENCES = [
  {id: 'REF-PM2', title: 'European Commission · PM² Artefacts', url: 'https://pm2.europa.eu/pm2-artefacts_en', accessed: '2026-09-27', usedFor: '헌장·작업계획·상태보고·변경요청과 리스크·결정·이슈·변경 로그를 연결하는 문서 체계 참고.', limits: '원문 양식을 복사하지 않았습니다. 아래 열 구성과 회사 정책은 본 교재의 교육 설계이며 PM²가 모든 조직에 요구하는 고정 양식이라고 주장하지 않습니다.'},
  {id: 'REF-GAO', title: 'U.S. GAO · Schedule Assessment Guide (GAO-16-89G)', url: 'https://www.gao.gov/products/gao-16-89g', accessed: '2026-09-27', usedFor: '일정의 작업·선후관계·자원·달력 근거, 실적에 따른 예측, 기준선 보존과 변경 영향 검토를 함께 보여 주는 설계 참고.', limits: '민간 금융회사에 적용되는 법규가 아닙니다. 이 작은 네트워크는 교육용이며 조직 전체 통합 일정의 규모나 모든 위험을 모형화하지 않습니다.'},
];

export const EXAMPLE_SOURCES = [
  {id: 'P02-S01', title: '업무 관찰·사업 요청', detail: '2026-10-19~23 관찰한 예외 40건의 처리시간 평균은 12분이다. 일평균 대사 대상 2,000건 중 예외 60건(3%)을 처리한다. 대사 원본과 담당자 판단이 흩어져 재확인에 시간이 든다. 원본 금액·이체 기능을 바꾸지 않고 조회와 예외처리 기록을 통합해 달라는 요청이다.'},
  {id: 'P02-S02', title: '권한·증빙 내부 정책', detail: '예외 처리자는 처리 근거를 작성하고 별도의 운영 검토자가 확인한다. 자신이 작성한 예외를 스스로 확정할 수 없다. 읽기 전용 원천의 파일 해시, 처리자, 검토자, 시각, 판정 사유를 남기며 처리 이력을 365일 보관한다. 범위·예산·완료일의 기준선 변경은 PM 영향분석과 재무·운영 검토 후 스폰서에게 상정한다.'},
  {id: 'P02-S03', title: '추정·자원·완료조건 합의', detail: 'A~I의 기간·선행·예산·자원은 아래 부속 일정표의 값으로 제공한다. B와 C, D와 E, F와 G는 각각 다른 전담 자원을 사용하므로 병행 가능하다. 작업 예산 합계는 120백만원이며 작업별 소요기간 동안 계획가치를 균등 배분한다. 자원 수를 늘리면 기간이 자동 단축된다고 가정하지 않는다.'},
  {id: 'P02-BL01', title: '비교용 승인 기준선 BL-01', detail: '사례 내부 가정: 2026-10-30 기준선 BL-01 승인 기록에 따라 A~I, 22영업일, 완료일 2026-12-01, 원가기준선 120백만원을 사용한다. 총 자금 한도 150백만원 중 관리예비비 30백만원은 원가기준선 밖에서 스폰서가 관리한다. 이 기록은 가상의 비교 입력이며 현재 문서의 승인란을 대신하지 않는다.'},
  {id: 'P02-EV01', title: '11월 13일 완료 증거·원가 마감', detail: 'A·B·C·E는 확인된 인도물에 대해 100% EV를 인정한다. D는 동일 예산가치 6백만원의 구성요소 6개 중 2개가 코드·단위검증 증거와 함께 수용되어 12백만원을 인정한다. 나머지 F~I는 0이다. 합계 EV 42백만원, 발생원가 AC 47백만원. 현금 지급 22백만원, 미지급 10백만원, 내부 배부원가 15백만원을 별도로 대조한다.'},
  {id: 'P02-FC01', title: '잔여 작업 재추정', detail: 'D는 실제 경과 3영업일에 2개 구성요소를 수용했고 잔여 4영업일을 예상한다. 총기간 전망을 6일에서 7일로 두면 완료일은 12월 2일이다. 잔여원가 ETC 82백만원을 작업 책임자가 재추정하여 AC 47 + ETC 82 = EAC 129백만원이다. 이는 승인 예산이 아닌 현재 전망이다.'},
  {id: 'P02-CR02', title: '예외 증빙 묶음 추출 변경요청', detail: '운영부가 11월 12일 RQ-06을 요청했다. 화면별 열람 대신 최대 200건의 CSV·원본 해시 목록·검토 기록을 묶어서 추출하는 기능이다. H 완료 후 J 구현·독립검증 2일, I는 J 후에 수행하며 증분예산 12백만원이다. 기존 처리·검토 권한 분리는 유지한다. 11월 13일 현재 승인 대기이며 기존 기준선에는 포함되지 않는다.'},
  {id: 'P02-REV01', title: '가상 검토 회의 메모', detail: '운영 책임자는 처리시간의 대상·측정기간을 보완하고, 재무 책임자는 원가·현금과 기준선·예측을 분리하며, QA는 검증 완료 증거를 구체화하라고 요청했다. 응답 내용은 문서의 검토표에 기록되어 있다. 검토 의견 반영은 승인과 다르다.'},
];

export const EXAMPLE_ACTIVITIES = [
  {id: 'A', name: '요구·대사 규칙 합의', wbs: '1.1', duration: 3, predecessors: [], owner: '서도윤 · 업무분석', resources: 'BA 1·운영 1', budget: 6000000, evidence: 'RQ-01~05 및 대사 키·허용차 합의 기록', startDate: '2026-11-02', finishDate: '2026-11-04'},
  {id: 'B', name: '원천 매핑·정합성 설계', wbs: '1.2', duration: 4, predecessors: ['A'], owner: '한재민 · 데이터', resources: '데이터 2', budget: 12000000, evidence: '3개 원천 매핑표·샘플 합계 대조', startDate: '2026-11-05', finishDate: '2026-11-10'},
  {id: 'C', name: '역할·증빙 통제 설계', wbs: '1.3', duration: 3, predecessors: ['A'], owner: '임세린 · 보안', resources: '보안 1·BA 1', budget: 6000000, evidence: '처리자/검토자 권한표·증빙 저장 규칙', startDate: '2026-11-05', finishDate: '2026-11-09'},
  {id: 'D', name: '조회·예외처리 구현', wbs: '1.4', duration: 6, predecessors: ['B', 'C'], owner: '오승현 · 개발', resources: '개발 3', budget: 36000000, evidence: '동일 예산가치 구성요소 6개·단위검증 기록', startDate: '2026-11-11', finishDate: '2026-11-18'},
  {id: 'E', name: '시험 데이터·절차 준비', wbs: '1.5', duration: 3, predecessors: ['B'], owner: '장유나 · QA', resources: 'QA 2', budget: 6000000, evidence: '마스킹 표본 1,000건·48개 시험 시나리오', startDate: '2026-11-11', finishDate: '2026-11-13'},
  {id: 'F', name: '통합·대사 검증', wbs: '1.6', duration: 4, predecessors: ['D', 'E'], owner: '장유나 · QA', resources: 'QA 3·개발 1', budget: 16000000, evidence: '합계 대조·예외 분류·재처리 48개 시험 결과', startDate: '2026-11-19', finishDate: '2026-11-24'},
  {id: 'G', name: '권한·증빙 독립 점검', wbs: '1.7', duration: 2, predecessors: ['D'], owner: '임세린 · 보안', resources: '보안 2', budget: 8000000, evidence: '자기승인 차단·무권한 조회 차단·해시 재현 점검', startDate: '2026-11-19', finishDate: '2026-11-20'},
  {id: 'H', name: '업무 인수시험', wbs: '1.8', duration: 3, predecessors: ['F', 'G'], owner: '윤태경 · 정산운영', resources: '운영 3·QA 2', budget: 18000000, evidence: '운영자 3명의 독립 수행·중대 결함 0건 확인', startDate: '2026-11-25', finishDate: '2026-11-27'},
  {id: 'I', name: '운영 이관·종료 정리', wbs: '1.9', duration: 2, predecessors: ['H'], owner: '강지우 · PM', resources: '운영 2·개발 1·PM 1', budget: 12000000, evidence: '운영 책임 인계·백아웃 절차·잔여항목·비용 마감', startDate: '2026-11-30', finishDate: '2026-12-01'},
];

export const EXAMPLE_EVM = {
  asOf: '2026-11-13', moneyUnit: 'KRW', baselineId: 'BL-01', pv: 48000000, ev: 42000000, ac: 47000000, bac: 120000000,
  cash: 22000000, payable: 10000000, internalAllocation: 15000000,
  etc: 82000000, bottomUpEac: 129000000, currentFinish: '2026-12-02', forecastDevelopmentDays: 7,
  basis: 'PV는 각 활동 예산을 기준선 소요 영업일에 균등 배분한다. EV는 시간 경과가 아닌 수용된 인도물의 사전 가중치로 측정한다.',
  cautions: ['EAC= BAC/(EV/AC)는 현재 원가효율이 계속된다는 조건부 추정이다. 아래 잔여작업 재추정 EAC와 같을 필요가 없다.', 'SPI는 가치 비율이다. 0.875를 일정 지연률이나 완료 날짜로 직접 바꾸지 않는다.', '현금 22 + 미지급 10 + 내부 배부원가 15 = 발생원가 47백만원이다. 가맹점 정산대금은 이 프로젝트 원가에 들어 있지 않다.'],
  phases: [
    {date: '2026-11-06', workday: 5, pv: 16000000, ev: 12000000, ac: 17000000, cash: 8000000, status: '마감 실적'},
    {date: '2026-11-13', workday: 10, pv: 48000000, ev: 42000000, ac: 47000000, cash: 22000000, status: '현재 마감'},
    {date: '2026-11-20', workday: 15, pv: 82000000, ev: null, ac: null, cash: null, status: '기준선 계획만 존재'},
    {date: '2026-11-27', workday: 20, pv: 108000000, ev: null, ac: null, cash: null, status: '기준선 계획만 존재'},
    {date: '2026-12-01', workday: 22, pv: 120000000, ev: null, ac: null, cash: null, status: '기준선 계획만 존재'},
  ],
  workPackages: [
    {activity: 'A', wbs: '1.1', pv: 6000000, ev: 6000000, ac: 6200000, accepted: '요구·규칙 합의 1/1', evidence: 'EV-A01 · 11/04'},
    {activity: 'B', wbs: '1.2', pv: 12000000, ev: 12000000, ac: 12600000, accepted: '원천 매핑 3/3', evidence: 'EV-B01 · 11/10'},
    {activity: 'C', wbs: '1.3', pv: 6000000, ev: 6000000, ac: 6200000, accepted: '역할·증빙 설계 1/1', evidence: 'EV-C01 · 11/06'},
    {activity: 'D', wbs: '1.4', pv: 18000000, ev: 12000000, ac: 15000000, accepted: '수용된 구성요소 2/6', evidence: 'EV-D01~02 · 11/13'},
    {activity: 'E', wbs: '1.5', pv: 6000000, ev: 6000000, ac: 7000000, accepted: '표본·시험절차 1/1', evidence: 'EV-E01 · 11/13'},
    {activity: 'F~I', wbs: '1.6~1.9', pv: 0, ev: 0, ac: 0, accepted: '미착수', evidence: '해당 없음'},
  ],
  costBridge: [
    {category: '외부 용역', ac: 22000000, cash: 14000000, payable: 8000000, internalAllocation: 0},
    {category: '환경·도구', ac: 10000000, cash: 8000000, payable: 2000000, internalAllocation: 0},
    {category: '내부 인력 배부', ac: 15000000, cash: 0, payable: 0, internalAllocation: 15000000},
  ],
};

const extension = {id: 'J', name: '증빙 묶음 추출·독립검증', wbs: '1.10', duration: 2, predecessors: ['H'], owner: '오승현·임세린', resources: '개발 2·보안 1', budget: 12000000, evidence: 'RQ-06: 200건 추출·권한·해시 목록 검증'};
export const EXAMPLE_ALTERNATIVES = {
  base: {id: 'base', label: '승인 기준선 BL-01', status: '사례 내부 승인 가정', activities: EXAMPLE_ACTIVITIES, budget: 120000000, finish: '2026-12-01', duration: 22, costDelta: 0, durationDelta: 0},
  current: {id: 'current', label: '현재 실적을 반영한 전망', status: '예측 · 기준선 아님', activities: EXAMPLE_ACTIVITIES.map(a => ({...a, duration: a.id === 'D' ? 7 : a.duration})), budget: 120000000, estimate: 129000000, finish: '2026-12-02', duration: 23, costDelta: 0, durationDelta: 1},
  proposed: {id: 'proposed', label: 'CR-02 변경 기준선 후보', status: '미승인 제안', activities: [...EXAMPLE_ACTIVITIES.filter(a => a.id !== 'I'), extension, {...EXAMPLE_ACTIVITIES.find(a => a.id === 'I'), predecessors: ['J']}], budget: 132000000, finish: '2026-12-03', duration: 24, costDelta: 12000000, durationDelta: 2},
  proposedForecast: {id: 'proposedForecast', label: '현재 지연 + CR-02를 반영한 전망', status: '조건부 예측 · 승인 시에도 재확인', activities: [...EXAMPLE_ACTIVITIES.filter(a => a.id !== 'I').map(a => ({...a, duration: a.id === 'D' ? 7 : a.duration})), extension, {...EXAMPLE_ACTIVITIES.find(a => a.id === 'I'), predecessors: ['J']}], budget: 132000000, estimate: 141000000, finish: '2026-12-04', duration: 25, costDelta: 12000000, durationDelta: 3},
};

// Dates belong to each view; a forecast must never silently retain baseline dates.
const datesByView = {
  current: {D: ['2026-11-11', '2026-11-19'], F: ['2026-11-20', '2026-11-25'], G: ['2026-11-20', '2026-11-23'], H: ['2026-11-26', '2026-11-30'], I: ['2026-12-01', '2026-12-02']},
  proposed: {J: ['2026-11-30', '2026-12-01'], I: ['2026-12-02', '2026-12-03']},
  proposedForecast: {D: ['2026-11-11', '2026-11-19'], F: ['2026-11-20', '2026-11-25'], G: ['2026-11-20', '2026-11-23'], H: ['2026-11-26', '2026-11-30'], J: ['2026-12-01', '2026-12-02'], I: ['2026-12-03', '2026-12-04']},
};
for (const [view, dates] of Object.entries(datesByView)) {
  EXAMPLE_ALTERNATIVES[view].activities = EXAMPLE_ALTERNATIVES[view].activities.map(a => dates[a.id] ? {...a, startDate: dates[a.id][0], finishDate: dates[a.id][1]} : {...a});
}

const src = (...ids) => EXAMPLE_SOURCES.filter(s => ids.includes(s.id));
const columns = (...pairs) => pairs.map(([key, label]) => ({key, label}));
const control = (documentId, version, asOf, reviewedBy) => ({documentId, version, asOf, preparedBy: '강지우 · 프로젝트 매니저', reviewedBy, decisionAuthority: '백서진 · 스폰서 / 사업총괄', status: '검토 초안 · 승인되지 않음', classification: '교육용 가상 자료', projectId: 'PREVIEW-02'});
const risks = [
  {id: 'RSK-01', event: '원천 파일 지연으로 당일 대사가 누락될 수 있다.', owner: '한재민', response: '도착 시각·누락 목록을 표시하고 운영자가 미수신을 종료 상태와 구분한다.', trigger: '예정 시각 후 30분 미수신', source: 'P02-S01'},
  {id: 'RSK-02', event: '처리자가 자신의 예외 판정을 확정하면 검토 통제가 무력화된다.', owner: '임세린', response: '서버에서 역할·사용자 일치 검사를 하고 G의 부정 시험으로 확인한다.', trigger: '자기승인 시험 1건이라도 성공', source: 'P02-S02'},
  {id: 'RSK-03', event: '인수시험 인력의 운영 업무 중복으로 H가 지연될 수 있다.', owner: '윤태경', response: '운영자 3명의 시험 시간을 사전 예약하고 11/20에 배정 상태를 재확인한다.', trigger: '시험 3영업일 전 인력 미확보', source: 'P02-S03'},
];

export const DOCUMENT_EXAMPLES = {
  charter: {
    id: 'charter', title: '프로젝트 헌장', subtitle: '사업 필요를 범위·측정·권한으로 바꾸는 검토 문서', unit: 1, workbookLink: 'visual.html?lab=charter',
    control: control('P02-CH-001', '0.3', '2026-10-27', '윤태경 · 정산운영 / 홍유빈 · 재무 / 임세린 · 보안'),
    summary: '루멘페이 정산운영팀은 원천 거래·정산 결과·회계 반영 자료를 개별 파일로 대조하고 있다. 예외 건의 처리 근거와 확인 주체가 분리되어 재확인 시간이 늘어난다. 본 프로젝트는 원천을 읽기 전용으로 연결하고 예외 분류·처리·독립 검토·증빙 추적을 하나의 업무 흐름으로 묶는다. 정산금 계산이나 대금 이체 엔진은 변경하지 않는다.',
    decisionRequest: '스폰서에게 사업 목적·초기 범위·PM 권한·자금 한도 150백만원에 대한 헌장 승인을 요청한다. 작업비 120백만원과 12월 1일 완료는 계획 후보이며 상세 기준선은 별도 통합 검토 후 승인한다. 이 초안에 승인 서명은 없다.',
    before: {title: '작성 전 · 실행 판단이 어려운 메모', paragraphs: ['정산 업무를 자동화해서 시간을 줄인다. 12월 초까지 개발하고 필요한 기능은 개발하면서 정한다. 예산은 150백만원이며 PM이 운영과 협의해 추진한다.'], missing: ['어떤 거래·예외가 대상인지 불명확하다.', '처리시간을 누가 언제 측정하는지 없다.', '정산금 변경·자동 이체의 제외 경계가 없다.', 'PM의 조정 권한과 승인권자의 결정 권한이 섞여 있다.']},
    visual: {type: 'charter', baselineMinutes: 12, targetMinutes: 5, dailyExceptions: 60, monthlyWorkdays: 20, potentialCapacityHours: 140, workflow: [{id: 'read', label: '원천 조회', owner: '시스템', note: '거래·정산·회계 자료 / 읽기 전용'}, {id: 'match', label: '대사·예외 분류', owner: '시스템', note: '차이·누락·중복을 식별'}, {id: 'prepare', label: '처리 근거 작성', owner: '운영 처리자', note: '사유·증빙·조치 제안'}, {id: 'review', label: '독립 검토', owner: '다른 운영 검토자', note: '자기승인 차단'}, {id: 'retain', label: '결과·증빙 보관', owner: '운영 책임자', note: '해시·이력 365일 / 내부 정책'}], scopeBoundary: '정산금 변경·대금 이체·ERP 교체는 제외'},
    sections: [
      {id: 'outcomes', title: '1. 성공 조건과 측정 책임', paragraphs: ['목표는 아직 달성 결과가 아니다. 12분→5분 목표가 실현되고 예외량이 유지되면 월 140시간의 처리 여력이 생긴다는 산술 추정이다. 인력 감축 또는 현금 절감이 확정되었다는 뜻은 아니다.'], table: {columns: columns(['id', '목표'], ['current', '현황·근거'], ['target', '목표·측정'], ['owner', '확인 책임']), rows: [
        {id: 'G-01 처리시간', current: '표본 40건 평균 12분 / P02-S01', target: '인계 후 10영업일의 예외 처리 전체 건 평균 ≤ 5분. 작업 개시~검토 제출 소요를 기록한다.', owner: '윤태경 · 운영'},
        {id: 'G-02 증빙 추적', current: '원본·처리 메모·검토 의견이 별도 보관됨 / P02-S01', target: '인수 표본 1,000건 중 예외 건 전체에서 원본 해시·처리자·검토자·시각·사유를 재현한다.', owner: '장유나 · QA'},
        {id: 'G-03 권한 분리', current: '파일 공유로 처리·검토 구분이 어려움 / P02-S02', target: '처리자의 자기승인 및 무권한 조회 시험에서 허용 0건.', owner: '임세린 · 보안'},
      ]}},
      {id: 'scope', title: '2. 범위와 인수 연결', table: {columns: columns(['id', '요구'], ['deliverable', '인도물·WBS'], ['acceptance', '인수 조건'], ['evidence', '검증·담당']), rows: [
        {id: 'RQ-01 원천 연결', deliverable: '거래·정산·회계 원천 매핑 / 1.2·1.4', acceptance: '표본 1,000건의 건수·원본 금액 합계가 입력 자료와 일치하고 원본은 변경하지 않는다.', evidence: 'F 대조 시험 · QA'},
        {id: 'RQ-02 예외 처리', deliverable: '차이·누락·중복 분류 및 처리 이력 / 1.4', acceptance: '처리자는 근거를 작성하고 다른 검토자가 확인한다. 반려 시 수정 이력이 남는다.', evidence: 'F 기능 시험·H 업무 시험 · 운영'},
        {id: 'RQ-03 증빙 보관', deliverable: '파일 해시·역할·시각·사유 조회 / 1.3·1.4', acceptance: '365일 보관 설정과 무권한 차단을 점검한다. 실제 365일 경과 시험은 설정·정책 검토로 대체한다.', evidence: 'G 통제 점검 · 보안'},
        {id: 'RQ-04 재현 가능성', deliverable: '대사 규칙·시험 데이터 / 1.1·1.5·1.6', acceptance: '동일 표본과 규칙 버전으로 재실행한 예외 분류·합계가 동일하다.', evidence: 'F 재실행 시험 · QA'},
        {id: 'RQ-05 운영 인수', deliverable: '운영 절차·교육·되돌림 계획 / 1.8·1.9', acceptance: '운영자 3명이 독립 수행하고 중대 결함 0건, 미결 항목은 소유자·기한을 지정한다.', evidence: 'H 인수·I 인계 · 운영'},
      ]}, bullets: ['제외: 정산금·수수료 산식 변경, 가맹점 대금 이체, 신규 금융상품, 회사 전체 ERP 교체.', '증빙 일괄 추출과 외부 전송은 초기 범위에 포함하지 않는다. 필요하면 범위·권한·비용을 별도 변경 심의한다.']},
      {id: 'governance', title: '3. 누가 작성·검토·결정하는가', table: {columns: columns(['name', '사람·역할'], ['responsibility', '책임과 권한'], ['handoff', '문서·후속 사용처']), rows: [
        {name: '강지우 · PM', responsibility: '작업 조정·영향분석·검토 상정. 범위·자금·기준선의 단독 변경권은 없다.', handoff: '헌장 → 통합 계획·변경요청'},
        {name: '윤태경 · 정산운영', responsibility: '업무 경계와 목표 측정 검토, 인수 판단 및 운영 편익 추적.', handoff: 'RQ·인수기준·편익 측정 인계'},
        {name: '홍유빈 · 재무', responsibility: '발생원가·미지급·현금을 대조하고 자금 한도와 원가 전망을 검토.', handoff: '원가 기준선·월별 자금 소요'},
        {name: '오승현 / 장유나 · 개발 / QA', responsibility: '구현 결과와 독립 검증 증거를 각각 책임진다.', handoff: '구성요소·시험·결함 기록'},
        {name: '임세린 · 보안', responsibility: '조회 권한·처리/검토 분리·증빙 보관 설정의 점검 의견 제공.', handoff: '통제 설계·G 점검 결과'},
        {name: '백서진 · 스폰서', responsibility: '헌장 및 범위·완료일·원가 기준선 변경의 승인 여부 결정.', handoff: '결정 기록 → 기준선 발효 여부'},
      ]}},
      {id: 'boundaries', title: '4. 주요 일정·자금·전제', table: {columns: columns(['item', '항목'], ['value', '계획 후보'], ['basis', '근거·확정 조건']), rows: [
        {item: '착수 / 업무 인수 / 종료', value: '11/02 / 11/27 / 12/01', basis: 'P02-S03 네트워크 후보. 상세 일정·자원 검토 후 확정'},
        {item: '작업비 / 관리예비비 / 자금 한도', value: '120 / 30 / 150백만원', basis: '작업비 기준선은 별도 승인. 관리예비비는 스폰서 통제'},
        {item: '전제', value: '원천 3종의 읽기 권한과 마스킹 표본 제공', basis: '원천 소유자 확인 후 B·E 착수. 미확보 시 PM에게 상정'},
        {item: '운영 제약', value: '기존 정산·이체 운영 중단 없이 병행 검증', basis: '대금 처리 변경 없음. 이관 중단 조건·되돌림 절차는 계획에서 상세화'},
      ]}},
      {id: 'risks', title: '5. 초기 위험과 대응 소유자', table: {columns: columns(['id', '위험'], ['event', '사건·영향'], ['owner', '책임'], ['response', '대응'], ['trigger', '상정 신호']), rows: risks}},
      {id: 'handoff', title: '6. 계획 단계와 종료 이후에 넘길 것', paragraphs: ['헌장 승인 후 요구사항 추적표는 각 요구의 WBS·검증 활동을 확정한다. 일정계획은 자원 가용성·의존성·달력을 재검토하고, 재무는 작업비와 월별 지급 시점을 분리한다. 모든 기준선은 이 헌장 하나로 자동 승인되지 않는다.', '종료 시 운영 책임자에게 측정 정의·조회 경로·미결 항목을 인계한다. 운영 인수 후 10영업일의 처리시간을 측정하고 목표 미달 원인·후속 조치를 기록한다. 종료보고와 편익 확인일을 동일시하지 않는다.']},
    ],
    reviewComments: [
      {id: 'CH-R01', reviewer: '윤태경 · 운영', comment: '시간 단축이라고만 쓰면 측정 대상이 서로 달라집니다.', response: 'G-01에 예외 처리 전체 건·인계 후 10영업일·평균 계산과 확인 책임을 추가했다.', status: '초안 반영 · 재검토 요청'},
      {id: 'CH-R02', reviewer: '홍유빈 · 재무', comment: '150백만원이 작업비인지 총 자금 한도인지 구분해 주세요.', response: '작업비 후보 120·관리예비비 30·총 한도 150을 구분하고 기준선 별도 승인을 명시했다.', status: '초안 반영 · 승인 대기'},
      {id: 'CH-R03', reviewer: '임세린 · 보안', comment: '예외 판정과 실제 자금 이체를 같은 권한처럼 표현하면 안 됩니다.', response: '범위에서 금액 변경·이체를 제외하고 처리/검토 분리를 요구 및 시험 조건에 연결했다.', status: '초안 반영 · 재검토 요청'},
    ],
    revisionHistory: [{version: '0.1', date: '2026-10-23', change: '사업 요청을 바탕으로 목적·범위 초안 작성', by: '강지우'}, {version: '0.2', date: '2026-10-26', change: '운영·재무·보안 검토 의견 등록', by: '강지우'}, {version: '0.3', date: '2026-10-27', change: '측정·제외 경계·자금 상태·권한 구분 반영', by: '강지우'}],
    sources: src('P02-S01', 'P02-S02', 'P02-S03', 'P02-REV01'),
  },
  schedule: {
    id: 'schedule', title: '통합 일정·기준선 검토서', subtitle: '인도물·담당·선후관계·비용이 연결된 실행 계획', unit: 3, workbookLink: 'visual.html?lab=schedule',
    control: control('P02-SCH-001', '1.1-review', '2026-11-13', '오승현 · 개발 / 장유나 · QA / 윤태경 · 운영'),
    summary: '기준선 BL-01은 요구·설계 이후 개발과 시험 준비를 병행하고, 통합 시험과 보안 점검을 모두 마친 뒤 업무 인수에 들어가는 구조다. 최장 경로 A→B→D→F→H→I는 22영업일이며 12월 1일 종료를 계획했다. 11월 13일 개발의 잔여 기간 재추정으로 현재 종료 전망은 12월 2일이다. 기준선은 지우지 않고 계획·현재 전망·추가 요구의 영향을 나란히 검토한다.',
    decisionRequest: '작업 책임자에게 잔여기간·자원 가용성의 재확인을 요청한다. 현재 예측 1일 지연은 보고하되 기준선 변경으로 처리하지 않는다. CR-02의 추가 2일은 별도 승인 여부가 결정될 때까지 후보 네트워크에만 보관한다.',
    before: {title: '작성 전 · 달력에 이름만 적은 목록', paragraphs: ['11월 초 요구사항과 설계를 정리한다. 개발은 11월 중순, 검증은 11월 말에 한다. 12월 1일에 끝내면 된다. 증빙 추출을 추가해도 개발팀이 조정할 수 있을 것 같다.'], missing: ['원천 매핑과 권한 설계 중 무엇을 기다려야 하는지 없다.', '개발 완료와 프로젝트 종료가 구분되지 않는다.', '자원·완료 증거·WBS·비용 연결이 없다.', '실적 지연과 미승인 범위 추가가 같은 날짜로 덮인다.']},
    visual: {type: 'schedule', startDate: '2026-11-02', calendar: EXAMPLE_CASE.calendar, activities: EXAMPLE_ACTIVITIES, alternatives: EXAMPLE_ALTERNATIVES, baselineId: 'BL-01', currentDate: '2026-11-13', baselineDuration: 22, baselineBudget: 120000000},
    sections: [
      {id: 'basis', title: '1. 일정의 계산 조건', paragraphs: [EXAMPLE_CASE.calendar.rule, '기간은 활동의 소요 영업일이며 공수와 다르다. 병행 경로의 담당자는 서로 달라 배정 충돌이 없다는 P02-S03 가정을 사용한다. 이 가정을 바꾸면 자원 검토를 다시 해야 한다. 날짜 강제 고정, 숨은 대기시간 또는 관계가 없는 임의 막대를 사용하지 않는다.'], bullets: ['주공정: A→B→D→F→H→I, 총 22영업일.', '기준선 총여유: C 1일, E 3일, G 2일. 총여유를 개별 활동마다 중복으로 소모할 수 있는 공짜 기간으로 보지 않는다.', '일정·원가 기준선은 P02-BL01과 연결한다. 보고 기준일 이후의 막대는 미래 실적이 아닌 계획 또는 예측이다.']},
      {id: 'activities', title: '2. 활동·WBS·담당·예산 연결', table: {columns: columns(['id', '활동'], ['name', '작업'], ['wbs', 'WBS'], ['duration', '영업일'], ['predecessorsText', 'FS 선행'], ['owner', '책임'], ['budgetText', '예산']), rows: EXAMPLE_ACTIVITIES.map(a => ({...a, predecessorsText: a.predecessors.join(', ') || '없음', budgetText: `${a.budget / 1000000}백만원`}))}},
      {id: 'delivery', title: '3. 완료를 판단할 증거', table: {columns: columns(['id', '활동'], ['resources', '계획 자원'], ['startDate', '기준선 시작'], ['finishDate', '기준선 종료'], ['evidence', '완료 증거']), rows: EXAMPLE_ACTIVITIES}},
      {id: 'milestones', title: '4. 기준선·현재 전망·변경 후보', table: {columns: columns(['view', '구분'], ['end', '종료일'], ['days', '총 영업일'], ['budget', '원가 기준선'], ['meaning', '해석']), rows: [
        {view: 'BL-01 기준선', end: '2026-12-01', days: 22, budget: '120백만원', meaning: '사례 내부 승인 가정 / 비교 기준'},
        {view: '현재 전망', end: '2026-12-02', days: 23, budget: '120백만원 유지', meaning: 'D 잔여 4일을 반영. EAC 129백만원은 별도 원가 전망'},
        {view: 'CR-02 계획 후보', end: '2026-12-03', days: 24, budget: '132백만원 제안', meaning: '기준선 + H→J 2일→I. 미승인 범위 추가'},
        {view: '현재 지연 + CR-02 전망', end: '2026-12-04', days: 25, budget: '132백만원 제안', meaning: '관측된 지연 1일과 범위 추가 2일을 모두 반영. EAC 141백만원'},
      ]}},
      {id: 'control', title: '5. 업데이트와 변경 통제', paragraphs: ['매주 금요일 작업 책임자는 실제 완료일·수용 증거·잔여 기간을 제출한다. PM은 네트워크를 재계산하고 기준선 대비 종료 전망·주공정·자원 충돌을 보고한다. 완료되지 않은 과거 계획을 미래의 확정 실적처럼 표시하지 않는다.', 'CR-02가 승인되면 결정 ID·효력일을 확인한 후 새로운 버전을 만든다. BL-01은 보존하며 WBS 1.10·RQ-06·활동 J·원가 증분 12백만원·시험 및 인계 조건을 함께 갱신한다. 거절 또는 보류되면 현재 전망은 관리하되 J는 실행 계획에 투입하지 않는다.']},
      {id: 'risk', title: '6. 일정 위험·확인할 전제', table: {columns: columns(['id', '항목'], ['event', '위험'], ['owner', '책임'], ['trigger', '확인 시점·신호'], ['response', '대응']), rows: [risks[2], {id: 'AS-S01', event: 'F 통합시험과 G 보안점검의 자원이 서로 독립적으로 배정된다.', owner: '장유나·임세린', trigger: '11/16 자원 배정 재확인', response: '중복 배정 시 기간을 임의 축소하지 않고 네트워크·완료 전망을 재산정한다.'}, {id: 'AS-S02', event: '미승인 J를 H와 병행하면 H에서 확인한 배포본이 바뀔 수 있다.', owner: '오승현', trigger: 'CR-02 압축안 제안 시', response: '본 안은 H 후 J로 정의한다. 병행안은 독립 자원·재시험·환경 분리 근거를 갖춘 별도 대안으로 제출한다.'}]}},
    ],
    reviewComments: [
      {id: 'SCH-R01', reviewer: '장유나 · QA', comment: '시험 시작이 개발만 기다리는 것으로 보입니다. 데이터·권한 점검 조건도 필요합니다.', response: 'F는 D·E 후, H는 F·G 후로 연결하고 완료 증거를 활동표에 적었다.', status: '반영 · 네트워크 대조 완료'},
      {id: 'SCH-R02', reviewer: '윤태경 · 운영', comment: '12월 3일이 새로 승인된 날짜로 읽힙니다.', response: 'BL-01 12/01, 현재 전망 12/02, 변경 계획 후보 12/03, 결합 전망 12/04를 분리했다.', status: '반영 · CR-02 결정 대기'},
      {id: 'SCH-R03', reviewer: '오승현 · 개발', comment: '7일은 지난 3일과 남은 4일을 합친 전망입니다. 7일이 더 남은 것은 아닙니다.', response: 'D 총기간 전망 7일, 기준일 현재 잔여 4일로 표시했다.', status: '반영 · 다음 주 재추정'},
    ],
    revisionHistory: [{version: '1.0', date: '2026-10-30', change: 'BL-01 비교 기준 입력: 22일·120백만원', by: '가상 승인 기록 P02-BL01'}, {version: '1.1-review', date: '2026-11-13', change: '현재 지연·CR-02 후보를 기준선과 분리해 검토', by: '강지우'}],
    sources: src('P02-S02', 'P02-S03', 'P02-BL01', 'P02-EV01', 'P02-FC01', 'P02-CR02'),
  },
  change: {
    id: 'change', title: '주간 성과·변경 의사결정 패키지', subtitle: '성과 근거 → 원인 → 전망 → 대안 → 결정 요청', unit: 8, workbookLink: 'visual.html?lab=change',
    control: control('P02-STS-002 / CR-02', '0.4', '2026-11-13', '홍유빈 · 재무 / 윤태경 · 운영 / 오승현 · 개발 / 장유나 · QA'),
    summary: '완료한 작업의 예산가치 EV는 42백만원으로 계획가치 PV 48백만원에 6백만원 미달한다. 발생원가 AC 47백만원을 EV와 비교하면 원가편차는 −5백만원이다. 개발의 대사 키 정규화 재작업으로 계획된 3개 구성요소 중 2개가 수용되었으며 완료 전망은 1영업일 늦다. 별도 요청인 증빙 묶음 추출(CR-02)은 이 편차의 원인이 아니므로 현재 성과와 분리해 판단한다.',
    decisionRequest: '11월 16일 스폰서에게 CR-02를 이번 범위에 포함할지 결정해 달라고 요청한다. 포함할 경우 기준선 후보는 132백만원·12월 3일이며, 현재 재작업 지연과 잔여원가를 포함한 실행 전망은 141백만원·12월 4일이다. PM 권고는 운영 필요성을 인정하되 추가 범위·재무 전망·인수 조건을 함께 심의하는 것이다. 승인 전 발주·작업 지시·기준선 변경은 하지 않는다.',
    before: {title: '작성 전 · 숫자만 있고 결정이 없는 보고', paragraphs: ['120백만원 중 47백만원을 사용했으므로 39% 진행했다. 개발이 조금 늦지만 전체 일정은 괜찮다. 증빙 추출 기능을 넣으면 운영이 좋아질 것 같으니 추가한다.'], missing: ['사용한 돈을 완료 진척과 혼동한다.', '편차의 원인·수용 증거·잔여 전망이 없다.', '현재 지연과 신규 변경의 효과가 섞여 있다.', '승인권자·요청 기한·실행 조건이 없다.']},
    visual: {type: 'change', ...EXAMPLE_EVM, alternatives: EXAMPLE_ALTERNATIVES},
    sections: [
      {id: 'status', title: '1. 이번 주 관리 요약', table: {columns: columns(['area', '영역'], ['status', '상태'], ['fact', '관찰된 사실'], ['action', '조치·책임·기한']), rows: [
        {area: '일정', status: '주의', fact: '기준선 12/01 → 현재 전망 12/02. D 구성요소 2/6 수용.', action: '오승현: 잔여 4일·재작업 종료 조건을 11/16 확인'},
        {area: '원가', status: '주의', fact: 'CV −5백만원. 잔여 재추정 EAC 129 > BAC 120.', action: '홍유빈: ETC 82의 작업별 근거를 11/16 대조'},
        {area: '범위', status: '결정 대기', fact: 'RQ-06 증빙 묶음 추출은 현재 기준선 밖.', action: '강지우: CR-02 영향·인수 조건을 11/16 상정'},
        {area: '품질·통제', status: '검증 준비', fact: '48개 시험 절차 준비. 통합·권한 시험 F·G는 미착수.', action: '장유나·임세린: 시험 통과를 미리 단정하지 않고 증거 확보 후 보고'},
        {area: '운영 인수', status: '계획 유지', fact: '운영자 3명 인수시험 배정 예정. 실제 가용성은 재확인 대상.', action: '윤태경: 11/20에 H 배정과 업무 대체 인력 확인'},
      ]}},
      {id: 'evm', title: '2. 가치·발생원가·현금을 구분한다', paragraphs: ['금액 단위는 백만원이다. PV 48은 기준일까지 하기로 한 작업의 예산가치, EV 42는 확인된 완료 작업의 예산가치, AC 47은 실제 발생원가다. 따라서 예산가치 기준 진척은 EV/BAC=35%이며 원가 발생률 AC/BAC=39.17%와 다르다.'], table: {columns: columns(['metric', '지표'], ['formula', '산식'], ['value', '값'], ['meaning', '의미·한계']), rows: [
        {metric: 'SV / CV', formula: 'EV−PV / EV−AC', value: '−6 / −5백만원', meaning: '일정가치 미달 / 같은 완료가치에 더 많은 원가 발생'},
        {metric: 'SPI / CPI', formula: '42/48 / 42/47', value: '0.875 / 0.8936', meaning: '가치 비율. 종료일은 네트워크로 별도 예측'},
        {metric: '효율 지속 EAC', formula: '120 ÷ (42/47)', value: '134.29백만원', meaning: '현재 원가효율이 잔여 작업에도 지속된다는 민감도 참고'},
        {metric: '잔여 재추정 EAC', formula: 'AC 47 + ETC 82', value: '129백만원', meaning: '책임자 재추정의 운영 전망. 승인 예산이 아님'},
        {metric: '현금·발생 대조', formula: '지급 22 + 미지급 10 + 내부배부 15', value: 'AC 47백만원', meaning: '가맹점 정산금·회사 매출과 구분. 미지급을 지급 시 재비용 처리하지 않음'},
      ]}},
      {id: 'evidence', title: '3. 완료 증거와 원가의 부속 명세', table: {columns: columns(['activity', '활동'], ['wbs', 'WBS'], ['pvText', 'PV'], ['evText', 'EV'], ['acText', 'AC'], ['accepted', '완료 판단'], ['evidence', '증거 ID']), rows: EXAMPLE_EVM.workPackages.map(r => ({...r, pvText: r.pv / 1000000, evText: r.ev / 1000000, acText: r.ac / 1000000}))}, paragraphs: ['A·B·C·E는 사전 정의한 인도물 수용에 대해 0/100 방식으로 EV를 인정했다. D는 6개 구성요소에 각각 6백만원의 가치를 배정했으며, 코딩 시간이 아니라 수용 증거 2건으로 EV 12백만원을 계산했다. 남은 활동의 EV·AC는 0이며 미래 실적을 채워 넣지 않았다.']},
      {id: 'alternatives', title: '4. CR-02 대안과 전체 영향', table: {columns: columns(['option', '선택'], ['scope', '범위·운영 영향'], ['budget', '기준선 예산'], ['forecast', '현재 실적 포함 전망'], ['condition', '결정 조건']), rows: [
        {option: 'A. 현 범위 유지', scope: 'RQ-01~05 유지. 증빙은 화면별 조회하며 묶음 추출은 후속 과제로 남김.', budget: '120백만원 유지', forecast: 'EAC 129백만원 / 12/02', condition: '현재 원가편차·1일 지연 조치 필요. 변경을 거절해도 편차는 사라지지 않음'},
        {option: 'B. 이번 프로젝트에 포함', scope: 'RQ-06·WBS 1.10·J 2일 추가. 기존 처리/검토 권한을 유지.', budget: '132백만원 후보 (+12)', forecast: 'EAC 141백만원 / 12/04', condition: '스폰서 승인·자원·인수조건 확인. 기준선 후보 완료일 12/03과 전망 12/04 구분'},
        {option: 'C. 별도 후속 릴리스로 분리', scope: '이번 프로젝트는 A와 동일. RQ-06 수요·우선순위를 후속 투자 검토에 인계.', budget: '이번 프로젝트 120백만원', forecast: '이번 프로젝트 129백만원 / 12/02', condition: '후속 예산·일정은 미산정. 이번 12백만원을 별도 릴리스 확정 견적으로 재사용하지 않음'},
      ]}, paragraphs: ['관리예비비 30백만원은 자동으로 쓸 수 있는 작업 예산이 아니다. B안의 증분 12백만원이 승인되면 원가기준선 후보는 132, 남은 관리예비비는 18, 총 자금 한도는 150백만원이다. EAC 141은 변경 후 후보 기준선보다 여전히 9백만원 높다. 이 전망을 숨기기 위해 이전 기준선이나 AC를 수정하지 않는다.']},
      {id: 'acceptance', title: '5. 추가 범위의 인수·영향 추적', table: {columns: columns(['item', '추적 항목'], ['value', '변경 후보 내용'], ['owner', '확인 책임']), rows: [
        {item: '요구 / WBS / 활동', value: 'RQ-06 → 1.10 → J. H 종료 후 J, J 종료 후 I.', owner: '강지우 · PM'},
        {item: '기능 인수', value: '최대 200건 선택 추출에서 CSV 건수·금액·해시 목록과 화면 조회가 일치.', owner: '장유나 · QA'},
        {item: '권한·정보 통제', value: '허용된 검토자만 추출. 처리자 자기승인 우회 및 무권한 추출 0건. 추출자·시각·대상 ID를 기록.', owner: '임세린 · 보안'},
        {item: '운영 인계', value: '증빙 묶음 확인·재조회·실패 재시도 절차를 I의 인계 자료에 추가.', owner: '윤태경 · 운영'},
        {item: '후속 문서', value: '승인 시 요구 추적표·WBS·일정·원가·품질·운영이관 자료를 같은 결정 ID로 갱신.', owner: '강지우 · PM'},
      ]}},
      {id: 'decision', title: '6. 결정·조치 대장', table: {columns: columns(['id', 'ID'], ['request', '요청·조치'], ['owner', '결정/실행 책임'], ['due', '기한'], ['status', '상태']), rows: [
        {id: 'DEC-02', request: 'CR-02 A/B/C 중 선택 및 B 선택 시 자금·일정·인수조건 확인', owner: '백서진 · 스폰서', due: '2026-11-16', status: '승인 대기 · 결정값 없음'},
        {id: 'ACT-11', request: 'D 재작업 원인과 잔여 4일 근거 재확인', owner: '오승현 · 개발', due: '2026-11-16', status: '진행 중'},
        {id: 'ACT-12', request: 'ETC 82백만원의 잔여 작업·단가·기지급 중복 여부 대조', owner: '홍유빈 · 재무', due: '2026-11-16', status: '검토 요청'},
        {id: 'ACT-13', request: '승인 후에만 새 버전 발효, BL-01 보존 및 관련 문서 배포', owner: '강지우 · PM', due: '결정일 다음 영업일', status: '조건부 후속 조치'},
      ]}},
    ],
    reviewComments: [
      {id: 'STS-R01', reviewer: '홍유빈 · 재무', comment: '47백만원 사용률을 진척률로 적으면 수용된 업무를 설명하지 못합니다.', response: '진척 35%, 원가 발생률 39.17%, 현금 22백만원을 분리하고 PV·EV·AC 부속 명세를 연결했다.', status: '반영 · 수치 대조 완료'},
      {id: 'STS-R02', reviewer: '윤태경 · 운영', comment: '추출 기능을 넣으면 현재 지연까지 자동 해결되는 것처럼 읽힙니다.', response: 'D 재작업 1일과 CR-02 추가 2일을 분리하고 12/04 결합 전망을 명시했다.', status: '반영 · 결정 대기'},
      {id: 'STS-R03', reviewer: '장유나 · QA', comment: '추가 기능의 인수 기준과 보안 점검 책임이 없습니다.', response: '200건 추출 정합성·권한·이력 조건과 QA/보안 소유자를 연결했다.', status: '반영 · 승인 후 시험계획 갱신'},
    ],
    revisionHistory: [{version: '0.1', date: '2026-11-12', change: 'CR-02 접수 및 변경 경계 정의', by: '강지우'}, {version: '0.3', date: '2026-11-13', change: 'EV·원가 마감과 잔여 예측·대안 영향 통합', by: '강지우'}, {version: '0.4', date: '2026-11-13', change: '검토 의견 반영. 기준선·전망·현금·승인 대기를 분리', by: '강지우'}],
    sources: src('P02-S02', 'P02-BL01', 'P02-EV01', 'P02-FC01', 'P02-CR02', 'P02-REV01'),
  },
};

// Explicit aliases for the document renderer. These are data, not learner state.
DOCUMENT_EXAMPLES.charter.visual.trace = [
  {requirement: 'RQ-01 원천 연결', deliverable: '1.2 매핑·1.4 조회', evidence: 'F: 1,000건 건수·금액 일치', owner: 'QA · 장유나'},
  {requirement: 'RQ-02 예외 처리', deliverable: '1.4 분류·처리·검토', evidence: 'F·H: 처리/검토 분리·반려 이력', owner: '운영 · 윤태경'},
  {requirement: 'RQ-03 증빙 보관', deliverable: '1.3 통제·1.4 증빙 조회', evidence: 'G: 365일 설정·자기승인 차단', owner: '보안 · 임세린'},
  {requirement: 'RQ-04 재현 가능성', deliverable: '1.5 표본·1.6 통합검증', evidence: 'F: 같은 입력의 같은 분류·합계', owner: 'QA · 장유나'},
  {requirement: 'RQ-05 운영 인수', deliverable: '1.8 인수·1.9 인계', evidence: 'H·I: 3명 독립 수행·중대 결함 0', owner: '운영 · 윤태경'},
];
DOCUMENT_EXAMPLES.charter.visual.gate = {request: '헌장 승인 요청', authority: '백서진 · 스폰서', status: '검토 초안 · 결정 대기', condition: '목적·범위·측정·PM 권한·자금 한도 확인. 상세 기준선은 별도 승인.'};
DOCUMENT_EXAMPLES.schedule.visual.currentActivities = EXAMPLE_ALTERNATIVES.current.activities;
DOCUMENT_EXAMPLES.schedule.visual.proposedActivities = EXAMPLE_ALTERNATIVES.proposed.activities;
DOCUMENT_EXAMPLES.schedule.visual.proposedCurrentActivities = EXAMPLE_ALTERNATIVES.proposedForecast.activities;
DOCUMENT_EXAMPLES.change.visual.periods = EXAMPLE_EVM.phases;
