/* Landing previews only: no ERP connection, learner records or MP-01 facts. */
export const PREVIEW_CASE = Object.freeze({
  id: 'PREVIEW-01',
  title: '정산 알림 개선',
  label: '미리보기용 별도 가상 사례',
  notice: 'PREVIEW-01은 결과물의 읽는 법을 보여 주는 별도 가상 사례입니다. 본 교재 MP-01의 원천자료·정답·승인 기록과 연결되지 않습니다.',
  status: '검토용 예시 · 승인 또는 목표 달성 기록 아님',
  moneyUnit: '백만원',
  durationUnit: '영업일',
  source: '미리보기용으로 구성한 입력 조건',
});

export const CASES = {
  charter: {
    id: 'charter',
    label: '헌장: 무엇을, 어디까지, 누가',
    unit: 1,
    lessonLink: 'learn.html?unit=1&view=practice&step=charter-3&phase=evidence',
    workbookLink: 'visual.html?lab=charter',
    beforeText: '정산 알림을 빠르고 편리하게 개선한다. 필요한 기능은 개발하면서 정하고, PM이 상황에 맞게 결정한다.',
    afterText: '발송 상태를 확인하는 데 걸린 시간을 건당 평균 3분 이하로 줄이는 것을 목표로 한다. 운영책임자가 인계 후 10영업일 동안 확인 건 전체를 측정한다. 범위와 승인권한은 아래처럼 구분해 검토한다.',
    question: '다른 사람이 이 헌장만 읽고 성공 조건·작업 경계·결정권자를 같은 뜻으로 이해할 수 있나요?',
    goals: [{
      id: 'G1', label: '발송 상태 확인 시간', baseline: 8, target: 3, unit: '분/건',
      baselineBasis: '가상 사전 표본 20건의 평균',
      owner: '운영책임자', period: '인계 후 10영업일',
      population: '측정 기간의 발송 상태 확인 건 전체',
      measurement: '발송 상태 조회 시작부터 확인 결과 기록 완료까지의 소요시간을 분 단위로 기록해 산술평균한다.',
      status: '검토할 목표값 · 달성값 아님',
    }],
    scope: {
      included: ['기존 알림의 발송 상태 조회', '실패 알림의 수동 재발송 요청', '확인·재발송 요청 이력 기록'],
      excluded: ['정산 금액·수수료 계산 변경', '가맹점 대금 이체', '전체 ERP 교체'],
    },
    authority: [
      {role: 'PM', responsibility: '작업을 조정하고 범위·일정 변경의 영향을 분석해 상정한다.'},
      {role: '운영책임자', responsibility: '업무 범위·측정 방법·운영 인수 조건을 검토한다.'},
      {role: '스폰서', responsibility: '헌장과 기준선 변경의 최종 승인 여부를 결정한다.'},
    ],
    notes: [
      '8분과 3분은 PREVIEW-01의 가상 현황과 목표다. 단순한 전후 달성 실적이 아니다.',
      '기능 범위와 목표의 적정성은 검토 대상이다. 미리보기를 조작해도 헌장이 승인되지는 않는다.',
    ],
    actions: ['현황과 목표를 구분한다.', '포함·제외 범위와 측정 책임을 연결한다.', '검토 의견을 반영해 승인 요청 근거를 만든다.'],
  },
  schedule: {
    id: 'schedule',
    label: '일정: 날짜 목록에서 연결된 계획으로',
    unit: 3,
    lessonLink: 'learn.html?unit=3&view=practice&step=6.5&phase=evidence',
    workbookLink: 'visual.html?lab=schedule',
    beforeText: '요구사항은 먼저 정리하고, 개발과 검수는 다음 주에 진행한다. 마지막에 인계하면 된다. 개발이 늦어질 때 전체 완료일이 얼마나 바뀌는지는 아직 계산하지 않았다.',
    afterText: '선후관계와 기간을 함께 놓으면 전체 소요기간은 9영업일이다. 개발을 4일에서 6일로 바꾸면 주공정이 2일 늘어 전체는 11영업일이 된다. 검수 준비의 여유시간은 별도로 확인한다.',
    question: '어떤 작업의 지연이 완료 시점을 바꾸며, 다른 작업의 여유시간과 어떻게 다른가요?',
    notes: [
      '모든 연결은 종료 후 시작(FS)이며 리드·래그는 0이다. 검수 준비와 개발은 동시에 진행할 수 있다고 가정한다.',
      '0은 착수 경계, 2는 2영업일이 지난 경계다. 날짜·휴일·자원 제약은 반영하지 않은 상대 일정이다.',
      '기간 변경의 계산 결과이며 실제 일정 변경 승인이나 자원 확보를 뜻하지 않는다.',
    ],
    actions: ['활동을 선후관계로 연결한다.', '네트워크와 간트에서 주공정·여유시간을 읽는다.', '개발 기간을 바꿔 전체 완료 시점의 영향을 확인한다.'],
  },
  change: {
    id: 'change',
    label: '성과: 쓴 돈과 끝낸 일을 구분하기',
    unit: 8,
    lessonLink: 'learn.html?unit=8&view=practice&step=7.4&phase=evidence',
    workbookLink: 'visual.html?lab=change',
    beforeText: '총예산 100백만원 중 45백만원을 썼으니 진척률도 45%다. 돈을 절반보다 적게 썼으므로 예산은 괜찮을 것 같다.',
    afterText: '실제원가 AC는 45백만원이지만, 완료한 작업의 예산가치 EV는 40백만원이다. 계획가치 PV 50백만원보다 10백만원 적다. 현재 원가효율이 계속되면 완료예상원가는 112.5백만원이므로 원인과 대응 대안을 검토한다.',
    question: '실제원가·완료한 작업의 가치·계획가치를 나누어 설명하고, 추가 확인이 필요한 판단을 구분할 수 있나요?',
    inputs: {pv: 50, ev: 40, ac: 45, bac: 100},
    decisionFlow: ['측정 기준과 실제 작업 완료 근거 확인', '일정·원가 편차 원인 분석', '대응 대안의 범위·일정·원가 영향 비교', '기준선 변경이 필요하면 승인 요청'],
    notes: [
      '모든 금액은 백만원이다. AC는 발생한 실제원가이며 현금 지급액과 같다고 가정하지 않는다.',
      'EV/BAC 40%는 예산가치 기준 진척이다. 업무 건수나 작업시간의 40%라는 뜻은 아니다.',
      'EAC = BAC/CPI는 현재 원가효율이 잔여 작업에도 지속된다는 가정의 추정값이다. 확정 비용이나 승인된 새 예산이 아니다.',
      'SPI는 가치의 비율이다. SPI 0.80만으로 완료일이 20% 늦어진다고 해석하지 않는다.',
    ],
    actions: ['PV·EV·AC를 서로 다른 막대로 읽는다.', 'SPI·CPI와 예산가치 기준 진척을 계산한다.', '편차 원인을 확인한 뒤 대응 대안과 변경 승인 필요성을 판단한다.'],
  },
};

const activities = [
  {id: 'A', label: '요구 정의', duration: 2, predecessors: []},
  {id: 'B', label: '개발', duration: 4, predecessors: ['A']},
  {id: 'C', label: '검수 준비', duration: 3, predecessors: ['A']},
  {id: 'D', label: '통합 검증', duration: 2, predecessors: ['B', 'C']},
  {id: 'E', label: '인계', duration: 1, predecessors: ['D']},
];

/** CPM for this preview's fixed network. Durations are integer workdays. */
export function calculateSchedule(developmentDays = 4) {
  if (!Number.isInteger(developmentDays) || developmentDays < 1 || developmentDays > 20) {
    throw new RangeError('개발 기간은 1~20 사이의 정수 영업일이어야 합니다.');
  }
  const rows = activities.map(a => ({...a, predecessors: [...a.predecessors], duration: a.id === 'B' ? developmentDays : a.duration}));
  const map = new Map(rows.map(a => [a.id, a]));
  for (const row of rows) {
    row.es = Math.max(0, ...row.predecessors.map(id => map.get(id).ef));
    row.ef = row.es + row.duration;
  }
  const finish = Math.max(...rows.map(a => a.ef));
  for (const row of [...rows].reverse()) {
    const successors = rows.filter(a => a.predecessors.includes(row.id));
    row.lf = successors.length ? Math.min(...successors.map(a => a.ls)) : finish;
    row.ls = row.lf - row.duration;
    row.float = row.ls - row.es;
    row.critical = row.float === 0;
  }
  return {
    activities: rows,
    finish,
    critical: rows.filter(a => a.critical).map(a => a.id),
    links: rows.flatMap(a => a.predecessors.map(from => ({source: from, target: a.id, critical: map.get(from).critical && a.critical && map.get(from).ef === a.es}))),
    unit: PREVIEW_CASE.durationUnit,
    origin: 0,
  };
}

/** Inputs and monetary outputs are in millions of KRW, ratios are unitless. */
export function calculatePerformance({pv = 50, ev = 40, ac = 45, bac = 100} = {}) {
  if (![pv, ev, ac, bac].every(value => Number.isFinite(value) && value >= 0) || bac <= 0 || ev > bac || pv > bac) {
    throw new RangeError('금액은 유한한 0 이상의 수이며 BAC는 양수, PV·EV는 BAC 이하여야 합니다.');
  }
  const spi = pv ? ev / pv : null;
  const cpi = ac ? ev / ac : null;
  const eac = cpi > 0 ? bac / cpi : null;
  const progress = ev / bac * 100;
  const costShare = ac / bac * 100;
  const plannedProgress = pv / bac * 100;
  const round = (value, digits) => value === null ? null : Number(value.toFixed(digits));
  return {
    pv, ev, ac, bac, spi, cpi, eac, progress, costShare, plannedProgress,
    sv: ev - pv, cv: ev - ac,
    vac: eac === null ? null : bac - eac,
    unit: PREVIEW_CASE.moneyUnit,
    display: {
      spi: spi === null ? '—' : spi.toFixed(2), cpi: cpi === null ? '—' : cpi.toFixed(2),
      eac: round(eac, 1), progress: round(progress, 1), costShare: round(costShare, 1),
      sv: round(ev - pv, 1), cv: round(ev - ac, 1), vac: eac === null ? null : round(bac - eac, 1),
    },
  };
}
