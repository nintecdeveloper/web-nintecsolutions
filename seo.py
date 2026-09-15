"""SEO metadata and deployment policy for the existing static site."""
import html,json
from i18n import translate,locale_path
PRODUCTION_ORIGIN='https://www.nintecsolutions.com'
PREVIEW_ORIGIN='https://nintec360-redisseny.ijubany.chatgpt.site'
LEGACY_ALIASES={'index.dc.html':'/','nintec-360.dc.html':'/nintec360/','contacte.dc.html':'/contacte/','equip.dc.html':'/equip/','nintec-finance.dc.html':'/finance/','nintec-compliance.dc.html':'/compliance/','politica-privacitat.dc.html':'/privacitat/','politica-cookies.dc.html':'/cookies/','termes-condicions.dc.html':'/termes/','nintec-360':'/nintec360/','nintec-finance':'/finance/','nintec-compliance':'/compliance/'}
# Confirmed by the public Wix page titles on 2026-09-13. Do not infer from slugs.
WIX_ALIASES={'the-card':'/es/finance/','privacy-policy':'/es/nintec360/','accessibility-statement':'/es/nintec360/#canals','blank':'/es/nintec360/#canals','blank-1':'/es/nintec360/#canals','blank-2':'/es/nintec360/#canals','blank-3':'/es/nintec360/','blank-4':'/es/nintec360/','blank-6':'/es/nintec360/','help-center':'/es/compliance/','blank-5':'/es/compliance/','blank-7':'/es/compliance/','blank-8':'/es/compliance/','blank-9':'/es/privacitat/','blank-10':'/es/cookies/','blank-11':'/es/termes/#titular'}
def structured_data(key,meta,lang,path,origin):
 url=origin+locale_path(path,lang);org=origin+'/#organization';site=origin+'/#website'
 graph=[{'@type':'Organization','@id':org,'name':'Nintec Solutions','legalName':'Nintec Digital Solutions SL','url':origin+'/','logo':origin+'/assets/brand/nintec-icon.png','email':'info@nintecsolutions.com','telephone':'+34684766844','sameAs':['https://www.linkedin.com/company/nintec-solutions'],'address':{'@type':'PostalAddress','streetAddress':'Av. Ernest Lluch, 32, Torre TCM2, Planta 1, Porta 1.17','addressLocality':'Mataró','postalCode':'08302','addressRegion':'Barcelona','addressCountry':'ES'}},
 {'@type':'WebSite','@id':site,'url':origin+'/','name':'Nintec Solutions','publisher':{'@id':org},'inLanguage':['ca','es','en','nl']},
 {'@type':'WebPage','@id':url+'#webpage','url':url,'name':translate(meta['title'],lang),'description':translate(meta['description'],lang),'isPartOf':{'@id':site},'about':{'@id':org},'inLanguage':lang}]
 if key!='index':
  graph[-1]['breadcrumb']={'@id':url+'#breadcrumb'}
  graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':translate('Inici',lang),'item':origin+locale_path('/',lang)},{'@type':'ListItem','position':2,'name':translate(meta['label'],lang),'item':url}]})
 if key in ('nintec360','finance'):
  graph.append({'@type':'Service','@id':url+'#service','name':meta['label'],'description':translate(meta['description'],lang),'provider':{'@id':org},'url':url})
  graph[2]['about']={'@id':url+'#service'}
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
def breadcrumbs(meta,lang,path):
 return f'<nav class="wrap breadcrumbs" aria-label="{translate("Ruta de navegació",lang)}"><a href="{locale_path("/",lang)}">{translate("Inici",lang)}</a><span aria-hidden="true">/</span><span aria-current="page">{translate(meta["label"],lang)}</span></nav>'
def sharing(meta,lang,path,origin):
 image=origin+'/assets/brand/social-card.png'
 return f'<meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Nintec Solutions"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(translate(meta["title"],lang),quote=True)}"><meta name="twitter:description" content="{html.escape(translate(meta["description"],lang),quote=True)}"><meta name="twitter:image" content="{image}"><meta name="twitter:image:alt" content="Nintec Solutions">'
def redirects(paths,production):
 rules={}
 for old,new in {**LEGACY_ALIASES,**(WIX_ALIASES if production else {})}.items():
  rules['/'+old]=new
  if not old.endswith('.html'):rules['/'+old+'/']=new
 for path in paths:
  rules[path+'index.html']=path
  if path!='/':rules[path.rstrip('/')]=path
 lines=[f'{old} {new} 301' for old,new in rules.items() if old!=new]
 # Domain-level redirects belong to the existing provider. These are portable
 # edge rules for an eventual static deployment, not DNS/hosting changes.
 if production:lines=['http://nintecsolutions.com/* '+PRODUCTION_ORIGIN+'/:splat 301','https://nintecsolutions.com/* '+PRODUCTION_ORIGIN+'/:splat 301','http://www.nintecsolutions.com/* '+PRODUCTION_ORIGIN+'/:splat 301']+lines
 return '\n'.join(lines)+'\n'
