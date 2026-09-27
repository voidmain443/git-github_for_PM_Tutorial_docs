import assert from 'node:assert/strict';
import {PREVIEW_CASE, CASES, calculateSchedule, calculatePerformance} from '../ERP/outcome-model.mjs';

assert.equal(PREVIEW_CASE.id, 'PREVIEW-01');
assert.match(PREVIEW_CASE.notice, /별도 가상 사례/);
assert.match(PREVIEW_CASE.notice, /MP-01.*연결되지 않습니다/);
assert.match(PREVIEW_CASE.status, /승인 또는 목표 달성 기록 아님/);
assert.deepEqual(Object.keys(CASES), ['charter', 'schedule', 'change']);
for (const [id, preview] of Object.entries(CASES)) {
  assert.equal(preview.id, id);
  assert.equal(preview.lessonLink, ({charter:'learn.html?unit=1&view=practice&step=charter-3&phase=evidence',schedule:'learn.html?unit=3&view=practice&step=6.5&phase=evidence',change:'learn.html?unit=8&view=practice&step=7.4&phase=evidence'})[preview.id]);
  assert.equal(preview.workbookLink, `visual.html?lab=${id}`);
  assert.ok(preview.beforeText && preview.afterText && preview.question);
  assert.ok(preview.notes.length >= 2 && preview.actions.length === 3);
}
const goal = CASES.charter.goals[0];
assert.deepEqual([goal.baseline, goal.target, goal.unit], [8, 3, '분/건']);
assert.equal(goal.owner, '운영책임자');
assert.equal(goal.period, '인계 후 10영업일');
assert.match(goal.status, /달성값 아님/);
assert.deepEqual(CASES.charter.authority.map(a => a.role), ['PM', '운영책임자', '스폰서']);

const base = calculateSchedule();
assert.equal(base.finish, 9);
assert.deepEqual(base.critical, ['A', 'B', 'D', 'E']);
assert.deepEqual(base.activities.map(a => [a.id, a.es, a.ef, a.ls, a.lf, a.float]), [
  ['A', 0, 2, 0, 2, 0], ['B', 2, 6, 2, 6, 0], ['C', 2, 5, 3, 6, 1],
  ['D', 6, 8, 6, 8, 0], ['E', 8, 9, 8, 9, 0],
]);
assert.deepEqual(base.links.filter(a => a.critical).map(a => `${a.source}>${a.target}`), ['A>B', 'B>D', 'D>E']);
const changed = calculateSchedule(6);
assert.equal(changed.finish, 11);
assert.equal(changed.finish - base.finish, 2);
assert.equal(changed.activities.find(a => a.id === 'C').float, 3);
assert.deepEqual(changed.critical, ['A', 'B', 'D', 'E']);
// Equal branches are both critical; shortening development cannot shorten the other branch.
assert.deepEqual(calculateSchedule(3).critical, ['A', 'B', 'C', 'D', 'E']);
assert.deepEqual(calculateSchedule(2).critical, ['A', 'C', 'D', 'E']);
assert.equal(calculateSchedule(2).finish, 8);
assert.equal(base.unit, '영업일');
assert.equal(base.origin, 0);
assert.match(CASES.schedule.notes.join(' '), /자원 제약은 반영하지 않은/);
for (const bad of [0, -1, 1.5, 21, NaN, Infinity, '6', null]) assert.throws(() => calculateSchedule(bad), RangeError);
base.activities[0].duration = 100;
base.activities[1].predecessors.push('E');
assert.equal(calculateSchedule().finish, 9, 'Returned arrays cannot mutate future results.');

const originalInputs = JSON.stringify(CASES.change.inputs);
const performance = calculatePerformance(CASES.change.inputs);
assert.equal(performance.spi, 0.8);
assert.equal(performance.cpi, 8 / 9);
assert.equal(performance.eac, 112.5);
assert.equal(performance.progress, 40);
assert.equal(performance.costShare, 45);
assert.equal(performance.plannedProgress, 50);
assert.equal(performance.sv, -10);
assert.equal(performance.cv, -5);
assert.equal(performance.vac, -12.5);
assert.equal(performance.unit, '백만원');
assert.equal(performance.display.spi, '0.80');
assert.equal(performance.display.cpi, '0.89');
assert.equal(performance.display.eac, 112.5, 'EAC uses raw CPI, not the displayed 0.89.');
assert.equal(JSON.stringify(CASES.change.inputs), originalInputs);
assert.match(CASES.change.notes.join(' '), /현금 지급액과 같다고 가정하지 않는다/);
assert.match(CASES.change.notes.join(' '), /현재 원가효율이 잔여 작업에도 지속/);
const empty = calculatePerformance({pv: 0, ev: 0, ac: 0});
assert.equal(empty.spi, null);
assert.equal(empty.cpi, null);
assert.equal(empty.eac, null);
assert.equal(empty.display.spi, '—');
assert.equal(calculatePerformance({ev: 0}).eac, null);
for (const invalid of [{pv: -1}, {ev: 101}, {pv: 101}, {bac: 0}, {ac: NaN}, {bac: Infinity}, {ev: '40'}]) {
  assert.throws(() => calculatePerformance(invalid), RangeError);
}

console.log('Outcome previews verified: isolated scenario, charter responsibilities, CPM/float/critical paths, EVM units and rounding.');
