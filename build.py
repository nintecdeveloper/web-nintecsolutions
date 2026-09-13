from pathlib import Path
import shutil,json,html,os,hashlib
from cycle import render_cycle
from i18n import LOCALES,translate,localize,locale_path,selector
ROOT=Path(__file__).parent; SRC=ROOT/'src'; OUT=ROOT/'dist'
ORIGIN=os.environ.get('SITE_ORIGIN','https://nintec360-redisseny.ijubany.chatgpt.site').rstrip('/')
pages=json.loads((SRC/'pages.json').read_text())
# Refresh styles when their content changes, including for returning visitors.
STYLE_VERSION=hashlib.sha256((SRC/'style.css').read_bytes()).hexdigest()[:12]
APP_VERSION=hashlib.sha256((SRC/'app.js').read_bytes()).hexdigest()[:12]
CYCLE_VERSION=hashlib.sha256((SRC/'cycle-player.js').read_bytes()).hexdigest()[:12]
I18N_VERSION=hashlib.sha256((SRC/'i18n.js').read_bytes()).hexdigest()[:12]
API_VERSION=hashlib.sha256((SRC/'api.js').read_bytes()).hexdigest()[:12]
RUNTIME_KEYS=json.loads((SRC/'locales/runtime.json').read_text())
PAGE_PATHS=['/' if key=='index' else '/'+key+'/' for key in pages]
OUT.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_dir(): shutil.rmtree(p)
 else:p.unlink()
shutil.copytree(SRC/'assets',OUT/'assets');shutil.copy(SRC/'style.css',OUT/'style.css');shutil.copy(SRC/'app.js',OUT/'app.js');shutil.copy(SRC/'api.js',OUT/'api.js')
shutil.copy(SRC/'cycle-player.js',OUT/'cycle-player.js')
shutil.copy(SRC/'i18n.js',OUT/'i18n.js')
for key,meta in pages.items():
 path='/' if key=='index' else '/'+key+'/'
 content=(SRC/(key+'.html')).read_text()
 if '{{CYCLE_WHEEL}}' in content:
  wheel,details=render_cycle(SRC,key)
  content=content.replace('{{CYCLE_WHEEL}}',wheel).replace('{{CYCLE_DETAILS}}',details)
 nav=(SRC/'header.html').read_text().replace('data-page="'+key+'"','aria-current="page"')
 footer=(SRC/'footer.html').read_text()
 structured={'@context':'https://schema.org','@type':'Organization','name':'Nintec Solutions','legalName':'NINTEC DIGITAL SOLUTIONS, S.L.','url':ORIGIN,'email':'info@nintecsolutions.com','telephone':'+34684766844','address':{'@type':'PostalAddress','streetAddress':'Av. Ernest Lluch, 32, Torre TCM2, Planta 1, Porta 1.17','addressLocality':'Mataró','postalCode':'08302','addressRegion':'Barcelona','addressCountry':'ES'}}
 title=html.escape(meta['title']); desc=html.escape(meta['description'],quote=True)
 doc=f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{ORIGIN}{path}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:locale" content="ca_ES"><meta property="og:site_name" content="Nintec Solutions"><meta property="og:url" content="{ORIGIN}{path}"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#5c39d9"><link rel="icon" href="/assets/logo-mark.png"><link rel="stylesheet" href="/style.css?v={STYLE_VERSION}"><script defer src="/api.js?v={API_VERSION}"></script><script defer src="/cycle-player.js?v={CYCLE_VERSION}"></script><script defer src="/app.js?v={APP_VERSION}"></script><script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">Salta al contingut</a>{nav}<main id="main">{content}</main>{footer}</body></html>'''
 for lang in LOCALES:
  translated=localize(doc,lang,PAGE_PATHS,ORIGIN)
  translated=translated.replace('<span id="language-slot"></span>',selector(path,lang))
  alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{locale_path(path,l)}">' for l in LOCALES)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}">'
  messages=json.dumps({k:translate(k,lang) for k in RUNTIME_KEYS},ensure_ascii=False).replace('<','\\u003c')
  bootstrap=f'<script type="application/json" id="i18n-messages">{messages}</script><script src="/i18n.js?v={I18N_VERSION}"></script>'
  translated=translated.replace('</title>','</title>'+alternates+bootstrap)
  target=OUT/locale_path(path,lang).lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(translated)
aliases={'index.dc.html':'/','nintec-360.dc.html':'/nintec360/','contacte.dc.html':'/contacte/','equip.dc.html':'/equip/','nintec-finance.dc.html':'/finance/','nintec-compliance.dc.html':'/compliance/','politica-privacitat.dc.html':'/privacitat/','politica-cookies.dc.html':'/cookies/','termes-condicions.dc.html':'/termes/','nintec-360':'/nintec360/','nintec-finance':'/finance/','nintec-compliance':'/compliance/'}
(OUT/'_redirects').write_text('\n'.join('/'+a+' '+b+' 301' for a,b in aliases.items())+'\n')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join('<url><loc>'+ORIGIN+locale_path(path,lang)+'</loc>'+''.join('<xhtml:link rel="alternate" hreflang="'+other+'" href="'+ORIGIN+locale_path(path,other)+'"/>' for other in LOCALES)+'</url>' for path in PAGE_PATHS for lang in LOCALES)+'</urlset>')
for lang in LOCALES:
 error=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{translate("Pàgina no trobada · Nintec",lang)}</title><link rel="stylesheet" href="/style.css"><meta name="robots" content="noindex"></head><body><main class="wrap section"><p class="eyebrow">404</p><h1>{translate("Aquesta pàgina no hi és.",lang)}</h1><a class="button" href="{locale_path("/",lang)}">{translate("Torna a Nintec360 →",lang)}</a></main></body></html>'
 target=OUT/('' if lang=='ca' else lang)/'404.html';target.write_text(error)
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n')
print(f'Built {len(pages)*len(LOCALES)} pages in CA, ES and EN at {OUT}')
