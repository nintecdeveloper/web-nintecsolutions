/* Public Supabase project configuration retained from the supplied current website. */
(function(root){
'use strict';
const URL="https://wrifaepwlcfxzyuyfhgt.supabase.co";
const KEY="sb_publishable_rjXhjcahZ2bn_JUlfid-Cg_M9oZgzbS";
const SLOTS=['09:00','09:30','10:00','10:30','11:00','11:30','15:00','15:30','16:00','16:30'];
function madridNow(now=new Date()){
 const parts=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now).map(p=>[p.type,p.value]));
 return {date:parts.year+'-'+parts.month+'-'+parts.day,minutes:Number(parts.hour)*60+Number(parts.minute)};
}
function businessDays(now=new Date()){
 const local=madridNow(now), date=new Date(local.date+'T12:00:00Z'),days=[];
 while(days.length<12){
  if(date.getUTCDay()!==0&&date.getUTCDay()!==6){
   const iso=date.toISOString().slice(0,10);
   days.push({date:iso,label:new Intl.DateTimeFormat('ca-ES',{weekday:'long',day:'numeric',month:'long',timeZone:'UTC'}).format(date),short:new Intl.DateTimeFormat('ca-ES',{weekday:'short',timeZone:'UTC'}).format(date),number:date.getUTCDate(),slots:SLOTS.map(time=>{const [h,m]=time.split(':').map(Number);return {time,taken:iso===local.date&&h*60+m<=local.minutes+60}})});
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
async function availability(now=new Date()){
 const days=businessDays(now);
 const rows=await request('rpc/get_franges_ocupades',{_desde:days[0].date,_fins:days[days.length-1].date});
 if(!Array.isArray(rows)||rows.some(r=>typeof r.data!=='string'||typeof r.hora!=='string'))throw new Error('invalid availability');
 const taken=new Set(rows.map(r=>r.data+' '+r.hora.slice(0,5)));
 return days.map(d=>({...d,slots:d.slots.map(s=>({...s,taken:s.taken||taken.has(d.date+' '+s.time)}))}));
}
async function reserve(contact,date,time,suggestion=''){
 if(!contact.nom?.trim()||!contact.cognoms?.trim()||!contact.email?.trim())throw new Error('contact');
 if(!date&&!suggestion.trim())throw new Error('selection');
 if(date){
  const days=await availability();const day=days.find(d=>d.date===date);const slot=day?.slots.find(s=>s.time===time);
  if(!slot||slot.taken){const e=new Error('conflict');e.status=409;throw e;}
 }
 const payload={};for(const k of ['nom','cognoms','empresa','email','telefon','missatge'])payload[k]=String(contact[k]||'').trim();
 payload.data=date||null;payload.hora=date?time+':00':null;payload.suggeriment_horari=suggestion.trim();
 await request('reserves_auditoria',payload);return payload;
}
async function subscribe(email){if(!email.trim())throw new Error('email');await request('leads_compliance',{email:email.trim()})}
root.NintecAPI={businessDays,madridNow,availability,reserve,subscribe};
})(typeof window!=='undefined'?window:globalThis);
