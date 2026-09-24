import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {readCostFacts,readRiskFacts,riskOutcomes,proposalScores} from '../ERP/visual-extra.mjs';
const source=id=>readFileSync(new URL(`../02_원천문서/S1/${id}.md`,import.meta.url),'utf8');
const sum=values=>values.reduce((s,x)=>s+x,0),near=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} differs from ${b}`);
const facts=readRiskFacts(source('S07'));
assert.deepEqual(facts.map(r=>[r.id,r.p,r.cost,r.days]),[['K01',.3,10e6,5],['K02',.2,20e6,10]]);
const base=riskOutcomes(.3,.2,10e6,20e6,10e6);
near(base.emv,7e6);near(base.covered,.8);near(base.excess,2.6e6);
assert.deepEqual(base.rows.map(r=>r.loss),[0,10e6,20e6,30e6]);
// Boundary probabilities and each reserve threshold exercise the distribution,
// including inclusive coverage when loss equals the reserve.
for(const p of [0,.3,1])for(const q of [0,.2,1])for(const reserve of [0,10e6,20e6,30e6]){
 const result=riskOutcomes(p,q,10e6,20e6,reserve);
 near(sum(result.rows.map(r=>r.p)),1);near(result.emv,p*10e6+q*20e6);
 assert.ok(result.covered>=-1e-8&&result.covered<=1+1e-8);
 assert.ok(result.excess>=0);
 if(reserve===30e6)near(result.covered,1);
}
for(const invalid of [-.1,1.1,NaN])assert.throws(()=>riskOutcomes(invalid,.2,10e6,20e6,10e6));
const cost=readCostFacts(source('S06'),source('S19'));
assert.deepEqual(cost.costs,[8e6,52e6,48e6,12e6]);
assert.deepEqual(cost.cash,[8e6,44e6,28e6,30e6]);
near(sum(cost.costs)-sum(cost.cash),cost.reserve);
near(sum(cost.costs)+cost.management,132e6);
for(let shift=0;shift<=cost.deferred;shift+=1e6){
 const revised=cost.cash.map((v,i)=>v+(i===2?shift:i===3?-shift:0));
 near(sum(revised),110e6);assert.ok(revised.every(v=>v>=0));
}
assert.throws(()=>readCostFacts('',source('S19')));
assert.throws(()=>readRiskFacts(''));
const scores=proposalScores([{scores:[90,80,80]},{scores:[70,70,100]}],[.5,.3,.2]);
assert.deepEqual(scores.map(s=>s.total),[85,76]);
assert.throws(()=>proposalScores([{scores:[90,80,80]}],[.6,.3,.2]));
console.log('Extra visual models: risk boundaries, source facts, payment conservation and proposal scores passed.');
