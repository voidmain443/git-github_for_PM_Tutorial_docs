import assert from 'node:assert/strict';
import {EXAMPLE_CASE, DOCUMENT_EXAMPLES, EXAMPLE_SOURCES, EXAMPLE_ACTIVITIES, EXAMPLE_EVM, EXAMPLE_ALTERNATIVES} from '../ERP/document-examples.mjs';
import {schedule, workdayDate, earnedValue} from '../ERP/visual-model.mjs';

const sum=(rows,key)=>rows.reduce((total,row)=>total+row[key],0);
const million=1000000;
const original=JSON.stringify({EXAMPLE_ACTIVITIES,EXAMPLE_ALTERNATIVES,EXAMPLE_EVM});
assert.equal(EXAMPLE_CASE.id,'PREVIEW-02');
assert.match(EXAMPLE_CASE.notice,/MP-01.*아니며/);
assert.match(EXAMPLE_CASE.approvalNotice,/검토 초안/);
assert.match(EXAMPLE_CASE.policyNotice,/내부 정책/);
assert.equal(EXAMPLE_CASE.moneyUnit,'KRW');
assert.equal(EXAMPLE_CASE.budget+EXAMPLE_CASE.managementReserve,EXAMPLE_CASE.fundingLimit);
assert.equal(sum(EXAMPLE_ACTIVITIES,'budget'),EXAMPLE_CASE.budget);
assert.ok(EXAMPLE_ACTIVITIES.every(a=>Number.isInteger(a.budget)&&a.budget>0));
const baseline=schedule(EXAMPLE_ACTIVITIES);
assert.equal(baseline.finish,22);
assert.deepEqual(baseline.critical,['A','B','D','F','H','I']);
assert.deepEqual(baseline.activities.filter(a=>a.float>0).map(a=>[a.id,a.float]),[['C',1],['E',3],['G',2]]);
assert.equal(workdayDate(EXAMPLE_CASE.startDate,baseline.finish-1),EXAMPLE_CASE.baselineFinish);
for(const [id,alternative] of Object.entries(EXAMPLE_ALTERNATIVES)){
 const model=schedule(alternative.activities);
 assert.equal(model.finish,alternative.duration,id+' duration must derive from its network');
 assert.equal(workdayDate(EXAMPLE_CASE.startDate,model.finish-1),alternative.finish,id+' end date must derive from its calendar');
 assert.equal(alternative.duration-baseline.finish,alternative.durationDelta,id+' duration delta');
 assert.equal(sum(alternative.activities,'budget'),alternative.budget,id+' WBS budget sum');
 assert.equal(alternative.budget-EXAMPLE_CASE.budget,alternative.costDelta,id+' budget delta');
 for(const activity of model.activities){
  assert.equal(activity.startDate,workdayDate(EXAMPLE_CASE.startDate,activity.es),id+' '+activity.id+' start date must use that view');
  assert.equal(activity.finishDate,workdayDate(EXAMPLE_CASE.startDate,activity.ef-1),id+' '+activity.id+' finish date must use that view');
 }
}
assert.equal(EXAMPLE_ALTERNATIVES.current.budget,EXAMPLE_ALTERNATIVES.base.budget,'Forecast does not overwrite the approved budget.');
assert.equal(EXAMPLE_ALTERNATIVES.proposed.duration,24);
assert.equal(EXAMPLE_ALTERNATIVES.proposedForecast.duration,25);
assert.equal(EXAMPLE_ALTERNATIVES.proposedForecast.estimate,EXAMPLE_ALTERNATIVES.current.estimate+EXAMPLE_ALTERNATIVES.proposed.costDelta);
assert.equal(EXAMPLE_ACTIVITIES.find(a=>a.id==='D').duration,6,'Original duration is preserved.');
assert.ok(!EXAMPLE_ACTIVITIES.some(a=>a.id==='J'),'Unapproved activity is absent from baseline.');
assert.equal(EXAMPLE_ALTERNATIVES.proposed.activities.find(a=>a.id==='J').predecessors[0],'H');
assert.equal(EXAMPLE_ALTERNATIVES.proposed.activities.find(a=>a.id==='I').predecessors[0],'J');

// Recompute PV independently from the activity budgets and elapsed workdays.
for(const period of EXAMPLE_EVM.phases){
 const pv=baseline.activities.reduce((total,a)=>total+a.budget*Math.max(0,Math.min(a.duration,period.workday-a.es))/a.duration,0);
 assert.equal(period.pv,pv,period.date+' planned value must agree with the baseline allocation');
 assert.equal(period.date,workdayDate(EXAMPLE_CASE.startDate,period.workday-1));
 if(period.date>EXAMPLE_EVM.asOf)assert.deepEqual([period.ev,period.ac,period.cash],[null,null,null],'Future periods contain plans, not fabricated actuals.');
}
const current=EXAMPLE_EVM.phases.find(p=>p.date===EXAMPLE_EVM.asOf);
for(const field of ['pv','ev','ac','cash'])assert.equal(current[field],EXAMPLE_EVM[field],field+' period and summary agree');
for(const field of ['pv','ev','ac'])assert.equal(sum(EXAMPLE_EVM.workPackages,field),EXAMPLE_EVM[field],field+' package evidence reconciles');
for(const row of EXAMPLE_EVM.costBridge)assert.equal(row.cash+row.payable+row.internalAllocation,row.ac,row.category+' cost bridge');
for(const field of ['ac','cash','payable','internalAllocation'])assert.equal(sum(EXAMPLE_EVM.costBridge,field),EXAMPLE_EVM[field],field+' bridge and total agree');
assert.equal(EXAMPLE_EVM.cash+EXAMPLE_EVM.payable+EXAMPLE_EVM.internalAllocation,EXAMPLE_EVM.ac);
assert.equal(EXAMPLE_EVM.ac+EXAMPLE_EVM.etc,EXAMPLE_EVM.bottomUpEac);
assert.equal(EXAMPLE_EVM.bottomUpEac,EXAMPLE_ALTERNATIVES.current.estimate);
assert.equal(EXAMPLE_EVM.currentFinish,EXAMPLE_ALTERNATIVES.current.finish);
assert.equal(EXAMPLE_EVM.forecastDevelopmentDays,EXAMPLE_ALTERNATIVES.current.activities.find(a=>a.id==='D').duration);
const evm=earnedValue(EXAMPLE_EVM.pv,EXAMPLE_EVM.ev,EXAMPLE_EVM.ac);
assert.equal(evm.sv,-6*million);assert.equal(evm.cv,-5*million);
assert.equal(evm.spi,.875);assert.equal(evm.cpi,42/47);
assert.equal(EXAMPLE_EVM.ev/EXAMPLE_EVM.bac*100,35);
assert.equal((EXAMPLE_EVM.ac/EXAMPLE_EVM.bac*100).toFixed(2),'39.17');
assert.equal((EXAMPLE_EVM.bac/evm.cpi/million).toFixed(2),'134.29');
assert.notEqual(EXAMPLE_EVM.bac/evm.cpi,EXAMPLE_EVM.bottomUpEac,'Efficiency forecast and bottom-up estimate are different methods.');
const charter=DOCUMENT_EXAMPLES.charter.visual;
assert.equal((charter.baselineMinutes-charter.targetMinutes)*charter.dailyExceptions*charter.monthlyWorkdays/60,charter.potentialCapacityHours);
assert.equal(charter.potentialCapacityHours,140);
assert.match(DOCUMENT_EXAMPLES.charter.sections.find(s=>s.id==='outcomes').paragraphs.join(' '),/현금 절감이 확정되었다는 뜻은 아니다/);
const sourceIds=new Set(EXAMPLE_SOURCES.map(s=>s.id));
assert.equal(sourceIds.size,EXAMPLE_SOURCES.length);
for(const [id,doc] of Object.entries(DOCUMENT_EXAMPLES)){
 assert.equal(doc.id,id);assert.equal(doc.control.projectId,EXAMPLE_CASE.id);
 assert.match(doc.control.status,/승인되지 않음/);
 assert.ok(doc.summary&&doc.decisionRequest&&doc.before.missing.length>=3);
 assert.ok(doc.sections.length>=4&&doc.reviewComments.length>=3&&doc.revisionHistory.length>=2);
 assert.equal(new Set(doc.sections.map(s=>s.id)).size,doc.sections.length,id+' section IDs are unique');
 assert.ok(doc.sources.length>0&&doc.sources.every(s=>sourceIds.has(s.id)&&s.id.startsWith('P02-')));
 assert.ok(doc.revisionHistory.every(r=>r.date<=doc.control.asOf),id+' revision history does not contain future events');
 for(const section of doc.sections){
  if(!section.table)continue;
  const {columns,rows}=section.table;
  assert.ok(columns.length>0&&rows.length>0);
  for(const row of rows)assert.ok(columns.every(c=>Object.hasOwn(row,c.key)),id+'/'+section.id+' table has every visible column');
 }
}
assert.equal(JSON.stringify({EXAMPLE_ACTIVITIES,EXAMPLE_ALTERNATIVES,EXAMPLE_EVM}),original,'Validation calculations never mutate example inputs.');
console.log('Document examples verified: source separation, CPM/calendar for four views, evidence/budget/cash reconciliation, EVM, forecast distinction and traceable document tables.');
