'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {matches}=require('../src/journal.js'),{resolve}=require('../src/i18n.js');
test('editorial search combines accents, multiple words and a selected category',()=>{
 const article={category:'Recerca i infraestructura',search:'SynthID Bio: proteïnes i procedència'};
 assert.equal(matches(article,'proteines procedencia',''),true);
 assert.equal(matches(article,'synthid','Models i productes'),false);
 assert.equal(matches(article,'inexistent',''),false);
 assert.equal(matches(article,'','Recerca i infraestructura'),true);
});
test('Journal language switching preserves the article across all four locales',()=>{
 const path='/blog/synthid-bio-proteines-ia-procedencia/';
 for(const from of ['ca','es','en','nl'])for(const to of ['ca','es','en','nl']){
  const route=resolve(new URL('https://www.nintecsolutions.com'+(from==='ca'?'':'/'+from)+path+'?lang='+to),'es');
  assert.equal(route.lang,to);assert.equal(route.target.pathname,(to==='ca'?'':'/'+to)+path);assert.equal(route.save,true);
 }
});
