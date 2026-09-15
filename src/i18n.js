/* Language routing and runtime copy. All page content is translated at build time. */
(function(root){
 'use strict';
 const languages=['ca','es','en','nl'],key='nintec-language';
 function basePath(path){return path.replace(/^\/(es|en|nl)(?=\/|$)/,'')||'/'}
 function pathFor(path,lang){return (lang==='ca'?'':'/'+lang)+basePath(path)}
 function resolve(url,saved){
  const explicit=url.searchParams.get('lang'),prefix=url.pathname.match(/^\/(es|en|nl)(?:\/|$)/)?.[1];
  const lang=languages.includes(explicit)?explicit:prefix||(languages.includes(saved)?saved:'ca');
  const target=new URL(url);target.pathname=pathFor(url.pathname,lang);target.searchParams.delete('lang');
  return {lang,target,save:languages.includes(explicit),redirect:target.pathname!==url.pathname};
 }
 if(typeof module!=='undefined'&&module.exports){module.exports={resolve,pathFor};return}
 let saved;try{saved=localStorage.getItem(key)}catch{}
 const current=new URL(location.href),route=resolve(current,saved);
 if(route.save){try{localStorage.setItem(key,route.lang)}catch{}}
 if(route.redirect){location.replace(route.target.href);return}
 if(current.searchParams.has('lang'))history.replaceState(null,'',route.target.href);
 const lang=document.documentElement.lang||'ca';
 const messages=JSON.parse(document.getElementById('i18n-messages')?.textContent||'{}');
 const t=(text,vars={})=>(messages[text]??text).replace(/\{(\w+)\}/g,(_,name)=>String(vars[name]??'{'+name+'}'));
 root.NintecI18n={lang,locale:{ca:'ca-ES',es:'es-ES',en:'en-GB',nl:'nl-NL'}[lang],t};
 document.addEventListener('DOMContentLoaded',()=>{
  const picker=document.querySelector('.language-picker');
  document.querySelectorAll('[data-language]').forEach(link=>{
   const dest=new URL(link.href);dest.hash=location.hash;link.href=dest.href;
   link.addEventListener('click',()=>{try{localStorage.setItem(key,link.dataset.language)}catch{}});
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&picker?.open){picker.open=false;picker.querySelector('summary').focus()}});
  document.addEventListener('click',event=>{if(picker?.open&&!picker.contains(event.target))picker.open=false});
 });
 // Override browser-language validation messages with the selected website language.
 document.addEventListener('invalid',event=>{
  const input=event.target,v=input.validity;if(!v)return;
  let message='';
  if(v.valueMissing)message=input.type==='checkbox'?'Accepta la política de privacitat per continuar.':'Escriu aquest camp.';
  else if(v.typeMismatch&&input.type==='email')message='Escriu una adreça de correu electrònic vàlida.';
  else if(v.patternMismatch||v.tooShort||v.tooLong||v.badInput)message='Revisa el format d’aquest camp.';
  if(message)input.setCustomValidity(t(message));
 },true);
 for(const name of ['input','change'])document.addEventListener(name,event=>event.target.setCustomValidity?.(''));
})(typeof window!=='undefined'?window:globalThis);
