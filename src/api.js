/* Public Supabase project configuration retained from the supplied current website. */
(function(root){
'use strict';
const URL="https://wrifaepwlcfxzyuyfhgt.supabase.co";
const KEY="sb_publishable_rjXhjcahZ2bn_JUlfid-Cg_M9oZgzbS";
const SLOTS=['09:00','09:30','10:00','10:30','11:00','11:30','15:00','15:30','16:00','16:30'];
// Date-seeded availability limits, not customer bookings. Stable across reloads,
// visitors, locales and the final availability recheck; never written to the CRM.
function dailyBlocks(date){
 let seed=2166136261;
 for(const char of 'nintec-capacity-v1:'+date)seed=Math.imul(seed^char.charCodeAt(0),16777619)>>>0;
 const random=()=>{seed=(seed+0x6D2B79F5)>>>0;let n=seed;n=Math.imul(n^(n>>>15),n|1);n^=n+Math.imul(n^(n>>>7),n|61);return ((n^(n>>>14))>>>0)/4294967296};
 const count=2+Math.floor(random()*3), shuffled=[...SLOTS];
 for(let i=shuffled.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]]}
 return new Set(shuffled.slice(0,count));
}
function madridNow(now=new Date()){
 const parts=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now).map(p=>[p.type,p.value]));
 return {date:parts.year+'-'+parts.month+'-'+parts.day,minutes:Number(parts.hour)*60+Number(parts.minute)};
}
function businessDays(now=new Date(),locale='ca-ES'){
 const local=madridNow(now), date=new Date(local.date+'T12:00:00Z'),days=[];
 const end=new Date(date);end.setUTCDate(end.getUTCDate()+13-(end.getUTCDay()+6)%7);
 while(date<=end){
  if(date.getUTCDay()!==0&&date.getUTCDay()!==6){
   const iso=date.toISOString().slice(0,10);
   days.push({date:iso,label:new Intl.DateTimeFormat(locale,{weekday:'long',day:'numeric',month:'long',timeZone:'UTC'}).format(date),short:new Intl.DateTimeFormat(locale,{weekday:'short',timeZone:'UTC'}).format(date),number:date.getUTCDate(),slots:SLOTS.map(time=>{const [h,m]=time.split(':').map(Number);return {time,taken:iso===local.date&&h*60+m<=local.minutes+60}})});
  }date.setUTCDate(date.getUTCDate()+1);
 }return days;
}
async function request(path,payload){
 const ctrl=new AbortController(), timer=setTimeout(()=>ctrl.abort(),15000);
 try{
  const response=await fetch(URL+'/rest/v1/'+path,{method:'POST',headers:{'Content-Type':'application/json','apikey':KEY,'Prefer':'return=minimal'},body:JSON.stringify(payload),signal:ctrl.signal});
  if(!response.ok){const error=new Error(response.status===409?'conflict':'request');error.status=response.status;throw error;}
  const text=await response.text();return text?JSON.parse(text):null;
 }finally{clearTimeout(timer)}
}
async function availability(now=new Date(),locale='ca-ES'){
 const days=businessDays(now,locale);
 const rows=await request('rpc/get_franges_ocupades',{_desde:days[0].date,_fins:days[days.length-1].date});
 if(!Array.isArray(rows)||rows.some(r=>typeof r.data!=='string'||typeof r.hora!=='string'))throw new Error('invalid availability');
 const taken=new Set(rows.map(r=>r.data+' '+r.hora.slice(0,5)));
 return days.map(d=>{const blocked=dailyBlocks(d.date);return {...d,slots:d.slots.map(s=>({...s,blocked:blocked.has(s.time),taken:s.taken||blocked.has(s.time)||taken.has(d.date+' '+s.time)}))}});
}
async function reserve(contact,date,time,suggestion=''){
 if(!contact.nom?.trim()||!contact.email?.trim())throw new Error('contact');
 if(!date&&!suggestion.trim())throw new Error('selection');
 if(date){
  const days=await availability();const day=days.find(d=>d.date===date);const slot=day?.slots.find(s=>s.time===time);
  if(!slot||slot.taken){const e=new Error('conflict');e.status=409;throw e;}
 }
 const payload={};for(const k of ['nom','cognoms','empresa','email','telefon','missatge'])payload[k]=String(contact[k]||'').trim();
 payload.data=date||null;payload.hora=date?time+':00':null;payload.suggeriment_horari=suggestion.trim();
 await request('reserves_auditoria',payload);return payload;
}
// Preserve the full entered name across the existing nom/cognoms columns.
function splitName(value){
 const name=String(value||'').trim().replace(/\s+/g,' '),index=name.indexOf(' ');
 if(!name||(index<0?name.length>100:index>100||name.slice(index+1).length>150))throw new Error('name');
 return index<0?{nom:name,cognoms:''}:{nom:name.slice(0,index),cognoms:name.slice(index+1)};
}
async function lead(contact,context={}){
 const names=splitName(contact.fullName);
 if(!contact.telefon?.trim()||!contact.email?.trim())throw new Error('contact');
 const tracking={page:String(context.page||'').slice(0,300),cta:String(context.cta||'').slice(0,200),utm:{}};
 for(const key of ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'])if(context.utm?.[key])tracking.utm[key]=String(context.utm[key]).slice(0,150);
 return reserve({...names,email:contact.email,telefon:contact.telefon,missatge:'Sol·licitud d’informació · '+JSON.stringify(tracking)},null,null,'Contacte comercial sense cita.');
}
async function subscribe(email){if(!email.trim())throw new Error('email');await request('leads_compliance',{email:email.trim()})}
root.NintecAPI={businessDays,madridNow,availability,reserve,subscribe,splitName,lead};
})(typeof window!=='undefined'?window:globalThis);
