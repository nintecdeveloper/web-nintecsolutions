const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const source=readFileSync('src/home-explorer.js','utf8');
function setup(hash='') {
  const groups=[6,4].map((count,g)=>{
    const panels=Array.from({length:count},(_,i)=>({id:`g${g}-${i}`,hidden:false}));
    const choices=panels.map(p=>({dataset:{choice:p.id},attrs:{},events:{},focused:false,
      setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f},focus(){this.focused=true}}));
    return {choices,panels,classList:{add(){}},querySelectorAll(){return choices},querySelector(s){return panels.find(p=>'#'+p.id===s)}};
  });
  const events=[];const location={hash};
  vm.runInNewContext(source,{document:{querySelectorAll(){return groups}},window:{addEventListener(k,f){events.push(f)}},location});
  return {groups,events,location};
}
function visible(g){return g.panels.filter(p=>!p.hidden).map(p=>p.id)}
test('click selection isolates the two explorers and keeps the matching state accessible',()=>{
 const {groups:[a,b]}=setup();let prevented=false;
 a.choices[2].events.click({preventDefault(){prevented=true}});
 assert.ok(prevented);assert.deepEqual(visible(a),['g0-2']);assert.deepEqual(visible(b),['g1-0']);
 assert.equal(a.choices[2].attrs['aria-current'],'true');assert.equal(a.choices[2].attrs['aria-controls'],'g0-2');
 assert.equal(a.choices[0].attrs['aria-current'],'false');
});
test('keyboard supports wraparound and Home/End without trapping Tab',()=>{
 const {groups:[a]}=setup();const event=key=>({key,preventDefault(){}});
 a.choices[0].events.keydown(event('ArrowUp'));assert.deepEqual(visible(a),['g0-5']);assert.ok(a.choices[5].focused);
 a.choices[5].events.keydown(event('Home'));assert.deepEqual(visible(a),['g0-0']);
 a.choices[0].events.keydown(event('End'));assert.deepEqual(visible(a),['g0-5']);
 a.choices[5].events.keydown({key:'Tab',preventDefault(){assert.fail('Tab must remain native')}});
});
test('direct links and hash navigation reveal the requested example',()=>{
 const s=setup('#g1-2');assert.deepEqual(visible(s.groups[1]),['g1-2']);
 s.location.hash='#g0-4';s.events.forEach(f=>f());assert.deepEqual(visible(s.groups[0]),['g0-4']);
});
