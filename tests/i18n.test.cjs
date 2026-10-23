'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {resolve,pathFor}=require('../src/i18n.js');
const url=path=>new URL(path,'https://example.com');
test('URL language wins over saved preference on every route',()=>{
 for(const lang of ['ca','es','en','nl'])for(const saved of [null,'ca','es','en','nl','invalid']){
  const path=(lang==='ca'?'':'/'+lang)+'/casos/?source=mail#retail';
  const result=resolve(url(path),saved);
  assert.equal(result.lang,lang);assert.equal(result.redirect,false);
  assert.equal(result.target.href,url(path).href);
 }
});
test('legacy lang parameters cannot conflict with HTML, canonical or selected route',()=>{
 for(const lang of ['ca','es','en','nl'])for(const query of ['ca','es','en','nl','unknown']){
  const path=(lang==='ca'?'':'/'+lang)+'/nintec360/';
  const result=resolve(url(path+'?lang='+query+'&utm_source=test#control'),'en');
  assert.equal(result.lang,lang);assert.equal(result.redirect,false);
  assert.equal(result.target.pathname,path);assert.equal(result.target.search,'?utm_source=test');
  assert.equal(result.target.hash,'#control');
 }
 assert.equal(pathFor('/en/','ca'),'/');assert.equal(pathFor('/es/contacte/','en'),'/en/contacte/');
});
test('every runtime message and t() call has a reviewed translation',()=>{
 const keys=new Set(JSON.parse(fs.readFileSync(__dirname+'/../src/locales/runtime.json','utf8')));
 for(const file of ['app.js','cycle-player.js','lead-modal.js']){
  const source=fs.readFileSync(__dirname+'/../src/'+file,'utf8');
  for(const m of source.matchAll(/\bt\((['"])(.*?)\1/g))assert.ok(keys.has(m[2]),file+': '+m[2]);
 }
 for(const lang of ['es','en','nl']){
  const d=JSON.parse(fs.readFileSync(__dirname+'/../src/locales/'+lang+'.json','utf8'));
  for(const key of keys){assert.ok(d[key.trim()],lang+': '+key);assert.deepEqual([...key.matchAll(/\{\w+\}/g)].map(m=>m[0]).sort(),[...d[key.trim()].matchAll(/\{\w+\}/g)].map(m=>m[0]).sort());}
 }
});
test('calendar labels follow the chosen locale while booking dates and times stay unchanged',()=>{
 const context={Intl,Date};vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/../src/api.js','utf8'),context);
 const api=context.NintecAPI,now=new Date('2026-09-11T08:15:00Z');
 const sets=['ca-ES','es-ES','en-GB','nl-NL'].map(l=>api.businessDays(now,l));
 assert.match(sets[0][0].label,/divendres/);assert.match(sets[1][0].label,/viernes/);assert.match(sets[2][0].label,/Friday/);assert.match(sets[3][0].label,/vrijdag/);
 for(const set of sets)assert.equal(JSON.stringify(set.map(d=>({date:d.date,slots:d.slots}))),JSON.stringify(sets[0].map(d=>({date:d.date,slots:d.slots}))));
});
test('preference routing survives disabled storage and localises native validation',()=>{
 for(const lang of ['ca','es','en','nl']){
  const listeners={},messages=lang==='ca'?{}:JSON.parse(fs.readFileSync(__dirname+'/../src/locales/'+lang+'.json','utf8'));
  const doc={documentElement:{lang},getElementById:()=>({textContent:JSON.stringify(messages)}),addEventListener:(name,fn)=>listeners[name]=fn};
  const context={URL,document:doc,location:{href:'https://example.com/'+(lang==='ca'?'':lang+'/')},localStorage:{getItem:()=>{throw Error('blocked')}},history:{},window:{}};
  vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/../src/i18n.js','utf8'),context);
  let message;listeners.invalid({target:{type:'email',validity:{typeMismatch:true},setCustomValidity:m=>message=m}});
  assert.equal(message,lang==='ca'?'Escriu una adreça de correu electrònic vàlida.':messages['Escriu una adreça de correu electrònic vàlida.']);
 }
});
