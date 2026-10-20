/* Progressive enhancement: every article remains available without JavaScript. */
(function(root){
 'use strict';
 const normalize=value=>String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
 const matches=(item,query,category)=> (!category||item.category===category)&&normalize(query).split(/\s+/).every(term=>normalize(item.search).includes(term));
 if(typeof module!=='undefined'&&module.exports){module.exports={normalize,matches};return}
 const lang=document.documentElement.lang;
 const nouns={ca:['article','articles'],es:['artículo','artículos'],en:['article','articles'],nl:['artikel','artikelen']}[lang]||['article','articles'];
 const feed=document.querySelector('.j-feed');if(!feed)return;
 const search=feed.querySelector('#journal-search'),cards=[...feed.querySelectorAll('[data-journal-card]')],buttons=[...feed.querySelectorAll('[data-journal-filter]')];
 let category='';
 function update(){let count=0;for(const card of cards){const show=matches(card.dataset,search.value,category);card.hidden=!show;if(show)count++}feed.querySelector('#journal-count').textContent=`${count} ${nouns[count===1?0:1]}`;feed.querySelector('#journal-empty').hidden=count!==0;buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.journalFilter===category)))}
 feed.querySelectorAll('[data-journal-controls]').forEach(el=>el.hidden=false);
 buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.journalFilter;update()}));
 search.addEventListener('input',update);
 feed.querySelector('#journal-reset').addEventListener('click',()=>{search.value='';category='';update();search.focus()});
})(typeof window!=='undefined'?window:globalThis);
