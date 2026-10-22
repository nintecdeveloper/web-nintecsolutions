/* Shared, opt-in conversion dialog. Native dialog provides focus trapping and Escape. */
(function(){
 'use strict';
 const dialog=document.getElementById('lead-modal');
 if(!dialog||typeof dialog.showModal!=='function')return;
 const booking=document.getElementById('lead-booking');
 let trigger=null;
 document.addEventListener('click',event=>{
  const link=event.target.closest('a[data-lead-cta]');
  if(!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  event.preventDefault();trigger=link;
  if(!dialog.open){const params=new URLSearchParams(location.search);const context={page:location.pathname,cta:link.textContent.trim(),utm:{}};for(const key of ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'])if(params.has(key))context.utm[key]=params.get(key).slice(0,150);booking.dataset.context=JSON.stringify(context);}
  if(!dialog.open){dialog.showModal();document.documentElement.classList.add('lead-open');booking.dispatchEvent(new Event('booking:open'));document.getElementById('lead-full-name').focus({preventScroll:true});}
 });
 dialog.querySelector('.lead-close').addEventListener('click',()=>dialog.close());
 let outside=false;
 const isOutside=e=>{const r=dialog.getBoundingClientRect();return e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom};
 dialog.addEventListener('pointerdown',e=>{outside=e.target===dialog&&isOutside(e)});
 dialog.addEventListener('click',e=>{if(outside&&e.target===dialog&&isOutside(e))dialog.close();outside=false});
 dialog.addEventListener('close',()=>{document.documentElement.classList.remove('lead-open');trigger?.focus({preventScroll:true})});
})();
