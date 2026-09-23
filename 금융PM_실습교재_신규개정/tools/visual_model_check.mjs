import assert from 'node:assert/strict';
import fs from 'node:fs';
import {readSchedule,schedule,workdayDate,earnedValue,readAlternatives} from '../ERP/visual-model.mjs';
const source=new URL('../02_원천문서/S1/S06.md',import.meta.url);
const model=readSchedule(fs.readFileSync(source,'utf8'));
const before=JSON.stringify(model),base=schedule(model.activities);
const change=(id,extra)=>model.activities.map(a=>({...a,duration:a.duration+(a.id===id?extra:0)}));
assert.equal(base.finish,60);
assert.deepEqual(base.critical,['A','B','D','E','F','G']);
assert.deepEqual(base.activities.find(a=>a.id==='C'),{...model.activities[2],es:20,ef:35,lf:40,ls:25,float:5,critical:false});
assert.equal(schedule(change('C',5)).finish,60);
assert.deepEqual(schedule(change('C',5)).critical,['A','B','C','D','E','F','G']);
assert.equal(schedule(change('C',6)).finish,61);
assert.equal(schedule(change('D',5)).finish,65);
assert.equal(schedule(model.activities,{'D>E':3}).finish,63);
assert.equal(schedule(model.activities,{'D>E':-3}).finish,57);
assert.equal(schedule(model.activities,{'D>E':-5}).finish,55);
assert.equal(schedule(model.activities,{'D>E':-8}).finish,55); // C still blocks E.
assert.equal(schedule([...model.activities].reverse()).finish,60); // Topology, not array order.
assert.equal(JSON.stringify(model),before);
assert.equal(workdayDate(model.start,0),'2026-10-19');
assert.equal(workdayDate(model.start,4),'2026-10-23');
assert.equal(workdayDate(model.start,5),'2026-10-26');
assert.equal(workdayDate(model.start,59),'2027-01-08');
assert.equal(workdayDate(model.start,64),'2027-01-15');
assert.throws(()=>schedule([{id:'A',duration:1,predecessors:['B']},{id:'B',duration:1,predecessors:['A']}]));
assert.throws(()=>schedule([{id:'A',duration:1,predecessors:['X']}]));
assert.throws(()=>schedule([{id:'A',duration:0,predecessors:[]}]))
assert.throws(()=>readSchedule('자료 없음'));
assert.throws(()=>workdayDate('2026-10-18',0));
assert.throws(()=>schedule(model.activities,{'X>E':2}));
const ev=earnedValue(60000000,50000000,58000000);
assert.equal(ev.sv,-10000000);assert.equal(ev.cv,-8000000);assert.equal(ev.spi,5/6);assert.equal(ev.cpi,25/29);
assert.equal(earnedValue(0,0,0).spi,null);
const alternatives=readAlternatives(fs.readFileSync(new URL('../02_원천문서/S2/S11.md',import.meta.url),'utf8'),{end_date:'2027-01-22'});
assert.deepEqual(alternatives.map(a=>[a.cost,a.days,a.end]),[[0,0,'2027-01-22'],[8000000,5,'2027-01-29'],[12000000,0,'2027-01-22']]);
console.log('Visual model verified: source network, float, parallel critical paths, leads/lags, calendar, EVM and alternatives.');
