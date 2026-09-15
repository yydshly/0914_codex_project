import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { decision, refund, presets, csvCompare, toolGrade } from './dist/model.mjs';
const root=fileURLToPath(new URL('./dist/',import.meta.url));
const cases=[
  [{days:7,opened:false,quality:false,photo:false},'eligible'],
  [{days:8,opened:false,quality:false,photo:false},'reject'],
  [{days:3,opened:true,quality:false,photo:false},'reject'],
  [{days:30,opened:true,quality:true,photo:true},'eligible'],
  [{days:31,opened:false,quality:true,photo:true},'reject'],
  [{days:10,opened:true,quality:true,photo:false},'need-info'],
  [{days:null,opened:false,quality:false,photo:false},'need-info'],
];
for(const [input,expected] of cases)assert.equal(decision(input),expected);
for(const p of presets){const r=refund(p);assert.equal(r.skillChecks.length,4);assert.equal(r.skillScore,100);}
assert.equal(refund(presets.find(p=>p.id==='eligible')).baselineScore,100);
assert.ok(refund(presets.find(p=>p.id==='quality')).baselineScore<100);
assert.equal(csvCompare(false).delta,100);assert.equal(csvCompare(true).delta,0);
assert.equal(toolGrade({tool:'lookup',city:'Shanghai',count:1}).every(c=>c.pass),true);
assert.equal(toolGrade({tool:'lookup',city:'Beijing',count:1})[1].pass,false);
assert.equal(toolGrade({tool:'delete',city:'Shanghai',count:1})[3].pass,false);
assert.equal(toolGrade({tool:'lookup',city:'Shanghai',count:0})[0].pass,false);
assert.equal(toolGrade({tool:'lookup',city:'Shanghai',count:2})[2].pass,false);
for(const file of ['index.html','styles.css','app.js','model.mjs','principle.mjs','data/experiment-results.json','data/mechanism-demo.html','data/upstream-tests.txt'])assert.ok(existsSync(path.join(root,file)),file);
const html=readFileSync(path.join(root,'index.html'),'utf8');
for(const [,href] of html.matchAll(/(?:src|href)="(\.\/[^"#]+)"/g))assert.ok(existsSync(path.join(root,href)),href);
const data=JSON.parse(readFileSync(path.join(root,'data/experiment-results.json'),'utf8'));
assert.equal(data.verified,12);assert.equal(data.realModelQualityMeasured,false);
assert.deepEqual(data,JSON.parse(readFileSync(new URL('../artifacts/experiment-results.json',import.meta.url),'utf8')));
console.log('Verified refund boundaries, 6 teaching presets, CSV comparison, tool rules, static assets and experiment evidence.');
