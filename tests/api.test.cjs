const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(__dirname+'/../src/api.js','utf8');
let calls=[],rows=[],status=200,fail=false;
const context={Date,Intl,Set,AbortController,setTimeout,clearTimeout,fetch:async(url,options)=>{calls.push({url,...options,payload:JSON.parse(options.body)});if(fail)throw new Error('offline');const isRPC=url.includes('/rpc/');return {ok:isRPC?status===200:status<400,status,text:async()=>isRPC?JSON.stringify(rows):''}}};
vm.createContext(context);vm.runInContext(source,context);const api=context.NintecAPI;
(async()=>{
 const madrid=api.madridNow(new Date('2026-09-08T22:15:00Z'));assert.equal(madrid.date,'2026-09-09');assert.equal(madrid.minutes,15);
 const winter=api.madridNow(new Date('2026-01-08T22:15:00Z'));assert.equal(winter.minutes,23*60+15);
 const days=api.businessDays(new Date('2026-09-11T08:15:00Z'));assert.equal(days.length,6);assert.equal(days.at(-1).date,'2026-09-18');assert.equal(days[0].date,'2026-09-11');assert.equal(days[1].date,'2026-09-14');assert.equal(days[0].slots.find(x=>x.time==='11:00').taken,true);assert.equal(days[0].slots.find(x=>x.time==='11:30').taken,false);
 rows=[{data:'2026-09-14',hora:'09:30:00'}];const available=await api.availability(new Date('2026-09-11T08:15:00Z'));assert.equal(available[1].slots.find(x=>x.time==='09:30').taken,true);assert.equal(calls.at(-1).payload._desde,'2026-09-11');assert.ok(calls.at(-1).payload._fins);
 fail=true;await assert.rejects(()=>api.availability());fail=false;
 rows=null;await assert.rejects(()=>api.availability());rows=[{invalid:'bad response'}];await assert.rejects(()=>api.availability());rows=[];
 for(const [date,count,last] of [['2026-09-07T08:00:00Z',10,'2026-09-18'],['2026-09-12T08:00:00Z',5,'2026-09-18'],['2026-09-13T22:30:00Z',10,'2026-09-25'],['2026-12-31T08:00:00Z',7,'2027-01-08']]){const range=api.businessDays(new Date(date));assert.equal(range.length,count);assert.equal(range.at(-1).date,last);}
 const contact={nom:'  Prova ',cognoms:'Local ',empresa:'Test',email:'test@example.invalid',telefon:'',missatge:'QA'};
 const futureDay=(await api.availability())[2],future=futureDay.date,freeTime=futureDay.slots.find(s=>!s.taken).time;calls=[];await api.reserve(contact,future,freeTime);assert.equal(calls.length,2);assert.ok(calls[0].url.endsWith('/rpc/get_franges_ocupades'));assert.ok(calls[1].url.endsWith('/reserves_auditoria'));assert.equal(calls[1].payload.nom,'Prova');assert.equal(calls[1].payload.hora,freeTime+':00');assert.equal(Object.keys(calls[1].payload).sort().join(','),'cognoms,data,email,empresa,hora,missatge,nom,suggeriment_horari,telefon');
 rows=[{data:future,hora:freeTime+':00'}];calls=[];await assert.rejects(()=>api.reserve(contact,future,freeTime),e=>e.status===409);assert.equal(calls.length,1);rows=[];
 const schedule=await api.availability(new Date('2026-10-19T05:00:00Z'));
 const repeat=await api.availability(new Date('2026-10-20T05:00:00Z'),'nl-NL');
 const quantities=new Set(),patterns=new Set();
 for(const d of schedule){const blocks=d.slots.filter(s=>s.blocked);assert.ok(blocks.length>=2&&blocks.length<=4);assert.ok(blocks.every(s=>s.taken));quantities.add(blocks.length);patterns.add(blocks.map(s=>s.time).join(','));const same=repeat.find(x=>x.date===d.date);if(same)assert.equal(same.slots.filter(s=>s.blocked).map(s=>s.time).join(','),blocks.map(s=>s.time).join(','));}
 assert.equal(quantities.size,3);assert.ok(patterns.size>5);
 // Artificial limits never cap bookings or hide otherwise available slots.
 for(let month=0;month<12;month++){
  rows=[];const day=(await api.availability(new Date(Date.UTC(2027,month,4,5))))[2];
  const blocks=day.slots.filter(s=>s.blocked),morning=blocks.filter(s=>s.time<'12:00');
  assert.ok(blocks.length>=2&&blocks.length<=4);
  assert.ok(morning.length>0&&morning.length<blocks.length);
  assert.ok(Math.abs(morning.length-(blocks.length-morning.length))<=1);
  const minutes=t=>Number(t.slice(0,2))*60+Number(t.slice(3));
  for(let i=1;i<blocks.length;i++)assert.notEqual(minutes(blocks[i].time)-minutes(blocks[i-1].time),30);
  assert.equal(day.slots.filter(s=>!s.taken).length,10-blocks.length);
  assert.ok(day.slots.every(s=>s.taken===(s.blocked||s.reserved||s.restricted)));
  rows=day.slots.slice(0,7).map(s=>({data:day.date,hora:s.time+':00'}));
  const occupied=(await api.availability(new Date(Date.UTC(2027,month,4,5)))).find(d=>d.date===day.date);
  assert.equal(occupied.slots.filter(s=>s.reserved).length,7);
  assert.ok(occupied.slots.slice(0,7).every(s=>s.taken));
  assert.ok(occupied.slots.filter(s=>s.blocked).length<=4);
 }
 rows=[];

 const blockedTime=futureDay.slots.find(s=>s.blocked).time;calls=[];await assert.rejects(()=>api.reserve(contact,future,blockedTime),e=>e.status===409);assert.equal(calls.length,1);
 calls=[];await api.reserve(contact,null,null,'  Dijous a la tarda  ');assert.equal(calls.length,1);assert.equal(calls[0].payload.data,null);assert.equal(calls[0].payload.hora,null);assert.equal(calls[0].payload.suggeriment_horari,'Dijous a la tarda');
 await assert.rejects(()=>api.reserve(contact,null,null,''));status=500;await assert.rejects(()=>api.reserve(contact,null,null,'dijous'));status=200;
 calls=[];await api.reserve({...contact,cognoms:''},null,null,'dijous');assert.equal(calls[0].payload.cognoms,'');
 const beyond=new Date();beyond.setDate(beyond.getDate()+21);calls=[];await assert.rejects(()=>api.reserve(contact,beyond.toISOString().slice(0,10),'09:00'),e=>e.status===409);assert.equal(calls.length,1);
 calls=[];await api.subscribe(' test@example.invalid ');assert.ok(calls[0].url.endsWith('/leads_compliance'));assert.equal(calls[0].payload.email,'test@example.invalid');
 console.log('PASS: Madrid timezone (summer/winter), current and next calendar week, one-hour notice, occupied slots, RPC contract, fail-closed availability, invalid responses, fresh recheck, reservation payload, conflict blocks insert, alternative slot payload, failed writes, Compliance payload. All writes used a local fake transport; zero live test submissions.');
})().catch(e=>{console.error(e);process.exitCode=1});
