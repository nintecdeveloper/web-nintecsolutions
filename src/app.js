'use strict';
const menu=document.querySelector('.menu-toggle');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('.site-header').classList.toggle('menu-open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu?.setAttribute('aria-expanded','false');document.querySelector('.site-header').classList.remove('menu-open')}});
// The circle explains the complete client lifecycle. No production data is used.
document.querySelectorAll('[data-cycle]').forEach(cycle=>{
 const buttons=[...cycle.querySelectorAll('[data-cycle-step]')];
 function select(button){
  for(const item of buttons){const active=item===button;item.setAttribute('aria-selected',String(active));item.tabIndex=active?0:-1;document.getElementById(item.getAttribute('aria-controls')).hidden=!active;}
  cycle.dataset.activeStep=button.dataset.cycleStep;
 }
 for(const button of buttons){
  button.addEventListener('click',()=>select(button));
  button.addEventListener('keydown',event=>{
   const current=buttons.indexOf(button);let next;
   if(['ArrowRight','ArrowDown'].includes(event.key))next=(current+1)%buttons.length;
   if(['ArrowLeft','ArrowUp'].includes(event.key))next=(current+buttons.length-1)%buttons.length;
   if(event.key==='Home')next=0;
   if(event.key==='End')next=buttons.length-1;
   if(next!==undefined){event.preventDefault();select(buttons[next]);buttons[next].focus();}
  });
 }
});
const compliance=document.getElementById('compliance-form');
compliance?.addEventListener('submit',async e=>{e.preventDefault();if(!compliance.reportValidity())return;const button=compliance.querySelector('button'),status=document.getElementById('compliance-status');if(button.disabled)return;button.disabled=true;button.textContent='Enviant…';status.textContent='';try{await NintecAPI.subscribe(document.getElementById('compliance-email').value);status.textContent='Gràcies! Hem rebut el teu email i t’avisarem quan estigui disponible.';status.className='success-text';compliance.reset();button.textContent='Sol·licitud rebuda ✓'}catch{status.textContent='No s’ha pogut enviar. Torna-ho a provar o escriu a info@nintecsolutions.com.';status.className='error';button.disabled=false;button.textContent='Torna-ho a provar ↗'}});
if(document.getElementById('booking')){
 const el=id=>document.getElementById(id);let days=[],start=0,selectedDate=null,selectedTime=null,ready=false,loading=false,busy=false,contact={};
 function step(value){for(const s of ['contact','calendar','confirm'])el(s+'-step').hidden=s!==value;document.querySelectorAll('.booking-steps li').forEach((li,i)=>{const n=['contact','calendar','confirm'].indexOf(value);if(i===n)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');li.classList.toggle('complete',i<n)});const heading=el(value+'-step').querySelector('h2');heading.tabIndex=-1;heading.focus({preventScroll:true});el('booking').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'})}
 function selection(){const alt=el('alternative').checked;el('suggestion-field').hidden=!alt;el('suggestion').required=alt;const available=ready&&days.some(d=>d.date===selectedDate&&d.slots.some(s=>s.time===selectedTime&&!s.taken));el('confirm-booking').disabled=busy||(alt?!el('suggestion').value.trim():!available);el('confirm-booking').textContent=busy?'Enviant…':alt?'Envia la proposta ↗':'Confirma la reserva ↗';el('selection-summary').textContent=alt?'Proposta d’horari pendent de confirmació.':available?days.find(d=>d.date===selectedDate).label+' · '+selectedTime+' · 30 minuts':'Selecciona un dia i una hora.'}
 function draw(){
  el('days').replaceChildren();el('slots').replaceChildren();el('prev-days').disabled=loading||start===0;el('next-days').disabled=loading||start+5>=days.length;
  if(!ready){el('month-label').textContent='';el('day-label').textContent=loading?'Consultant la disponibilitat…':'El calendari no està disponible.';selection();return}
  el('month-label').textContent=new Intl.DateTimeFormat('ca-ES',{month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(days[start].date+'T12:00:00Z'));
  for(const d of days.slice(start,start+5)){const b=document.createElement('button');b.type='button';b.className='day-button';b.disabled=d.slots.every(s=>s.taken)||busy;b.setAttribute('aria-label',d.label);b.setAttribute('aria-pressed',String(d.date===selectedDate));const small=document.createElement('span');small.textContent=d.short;const num=document.createElement('strong');num.textContent=d.number;b.append(small,num);b.addEventListener('click',()=>{selectedDate=d.date;selectedTime=null;el('alternative').checked=false;draw()});el('days').append(b)}
  const day=days.find(d=>d.date===selectedDate);el('day-label').textContent=day?day.label:'Tria un dia per veure les hores.';
  for(const s of day?.slots||[]){const b=document.createElement('button');b.type='button';b.className='slot-button';b.textContent=s.time;b.disabled=s.taken||busy;b.setAttribute('aria-label',s.time+(s.taken?' — no disponible':''));b.setAttribute('aria-pressed',String(s.time===selectedTime));b.addEventListener('click',()=>{selectedTime=s.time;el('alternative').checked=false;draw()});el('slots').append(b)}selection();
 }
 async function load(){loading=true;ready=false;el('availability-status').className='';el('availability-status').textContent='Consultant la disponibilitat real…';el('retry-availability').hidden=true;draw();try{days=await NintecAPI.availability();ready=true;start=Math.min(start,Math.max(0,days.length-5));el('availability-status').textContent='Disponibilitat actualitzada. Les hores ocupades estan desactivades.'}catch{el('availability-status').textContent='No hem pogut consultar el calendari. Torna-ho a provar o proposa un horari perquè el revisem.';el('availability-status').className='error';el('retry-availability').hidden=false}finally{loading=false;draw()}}
 el('contact-form').addEventListener('submit',e=>{e.preventDefault();if(!e.target.reportValidity())return;contact=Object.fromEntries(new FormData(e.target));for(const field of ['nom','cognoms'])if(!contact[field].trim()){el(field).setCustomValidity('Escriu aquest camp.');el(field).reportValidity();return}step('calendar');load()});
 for(const field of ['nom','cognoms'])el(field).addEventListener('input',()=>el(field).setCustomValidity(''));
 el('back-contact').addEventListener('click',()=>{if(!busy)step('contact')});el('retry-availability').addEventListener('click',load);
 el('prev-days').addEventListener('click',()=>{start=Math.max(0,start-5);draw()});el('next-days').addEventListener('click',()=>{start=Math.min(days.length-5,start+5);draw()});
 el('alternative').addEventListener('change',()=>{if(el('alternative').checked){selectedDate=null;selectedTime=null}draw()});el('suggestion').addEventListener('input',selection);
 el('confirm-booking').addEventListener('click',async()=>{
  if(busy||el('confirm-booking').disabled)return;
  const alt=el('alternative').checked,suggestion=alt?el('suggestion').value.trim():'',date=alt?null:selectedDate,time=alt?null:selectedTime;
  busy=true;el('booking-error').hidden=true;el('back-contact').disabled=true;el('alternative').disabled=true;el('suggestion').disabled=true;draw();
  try{const payload=await NintecAPI.reserve(contact,date,time,suggestion);el('confirmation-title').textContent=alt?'Proposta rebuda.':'Reserva registrada.';el('confirmation-message').textContent=alt?'Gràcies, '+payload.nom+'. Revisarem el teu horari i et contactarem per confirmar-lo.':payload.nom+', hem registrat la teva reserva. L’equip et contactarà per email o telèfon per concretar la reunió.';el('confirmation-details').replaceChildren();const fields={'Nom':payload.nom+' '+payload.cognoms,'Empresa':payload.empresa,'Email':payload.email,'Telèfon':payload.telefon,...(alt?{'Horari proposat':suggestion}:{'Dia':days.find(d=>d.date===date)?.label||date,'Hora':time+' · 30 minuts · Barcelona'})};for(const[label,value]of Object.entries(fields)){if(!value)continue;const row=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;row.append(dt,dd);el('confirmation-details').append(row)}step('confirm')}
  catch(error){el('booking-error').hidden=false;el('booking-error').textContent=error.status===409?'Aquesta hora ja no està disponible. Hem actualitzat el calendari; tria’n una altra.':'No hem pogut confirmar la sol·licitud. No es mostra com a reservada. Si la connexió s’ha interromput durant l’enviament, contacta amb nosaltres abans de repetir-lo.';selectedTime=null;if(!alt)await load()}
  finally{busy=false;el('back-contact').disabled=false;el('alternative').disabled=false;el('suggestion').disabled=false;draw()}
 });
}
