/* Accessible inline usage help. All copy is rendered by the existing i18n build. */
(()=>{
 'use strict';
 let active=null,pointerFocus=false;
 function close(){if(!active)return;active.button.setAttribute('aria-expanded','false');active.tip.hidden=true;active=null;}
 function open(button,pinned=false){
  close();const tip=document.getElementById(button.getAttribute('aria-describedby'));
  if(!tip)return;
  active={button,tip,pinned};tip.hidden=false;button.setAttribute('aria-expanded','true');
  position();
 }
 function position(){
  if(!active)return;const {button,tip}=active;
  const box=button.getBoundingClientRect(),width=Math.min(300,window.innerWidth-32);
  tip.style.width=width+'px';tip.style.left=Math.max(16,Math.min(box.left-width/2,window.innerWidth-width-16))+'px';
  const height=tip.getBoundingClientRect().height;
  tip.style.top=(box.top-height-10>=16?box.top-height-10:Math.min(box.bottom+10,window.innerHeight-height-16))+'px';
 }
 for(const wrapper of document.querySelectorAll('.pricing-info')){
  const button=wrapper.querySelector('button');
  wrapper.addEventListener('pointerenter',event=>{if(event.pointerType==='mouse'&&active?.button!==button)open(button)});
  wrapper.addEventListener('pointerleave',()=>{if(active?.button===button&&!active.pinned&&!button.matches(':focus-visible'))close()});
  button.addEventListener('pointerdown',()=>{pointerFocus=true});
  button.addEventListener('focus',()=>{if(!pointerFocus)open(button)});
  button.addEventListener('blur',()=>{if(active?.button===button)close()});
  button.addEventListener('click',()=>{pointerFocus=false;if(active?.button===button){if(active.pinned)close();else active.pinned=true;}else open(button,true)});
 }
 document.addEventListener('keydown',event=>{if(event.key==='Escape')close()});
 document.addEventListener('pointerdown',event=>{if(active&&!event.target.closest('.pricing-info'))close()});
 document.addEventListener('scroll',position,true);window.addEventListener('resize',close);
 for(const detail of document.querySelectorAll('.pricing-usage'))detail.addEventListener('toggle',()=>{if(!detail.open&&active&&detail.contains(active.button))close()});
})();
