from pathlib import Path
import shutil,json,html,os
ROOT=Path(__file__).parent; SRC=ROOT/'src'; OUT=ROOT/'dist'
ORIGIN=os.environ.get('SITE_ORIGIN','https://nintec360-redisseny.ijubany.chatgpt.site').rstrip('/')
pages=json.loads((SRC/'pages.json').read_text())
OUT.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_dir(): shutil.rmtree(p)
 else:p.unlink()
shutil.copytree(SRC/'assets',OUT/'assets');shutil.copy(SRC/'style.css',OUT/'style.css');shutil.copy(SRC/'app.js',OUT/'app.js');shutil.copy(SRC/'api.js',OUT/'api.js')
for key,meta in pages.items():
 path='/' if key=='index' else '/'+key+'/'
 content=(SRC/(key+'.html')).read_text()
 nav=(SRC/'header.html').read_text().replace('data-page="'+key+'"','aria-current="page"')
 footer=(SRC/'footer.html').read_text()
 structured={'@context':'https://schema.org','@type':'Organization','name':'Nintec Solutions','legalName':'NINTEC DIGITAL SOLUTIONS, S.L.','url':ORIGIN,'email':'info@nintecsolutions.com','telephone':'+34684766844','address':{'@type':'PostalAddress','streetAddress':'Av. Ernest Lluch, 32, Torre TCM2, Planta 1, Porta 1.17','addressLocality':'Mataró','postalCode':'08302','addressRegion':'Barcelona','addressCountry':'ES'}}
 title=html.escape(meta['title']); desc=html.escape(meta['description'],quote=True)
 doc=f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{ORIGIN}{path}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:locale" content="ca_ES"><meta property="og:site_name" content="Nintec Solutions"><meta property="og:url" content="{ORIGIN}{path}"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#5c39d9"><link rel="icon" href="/assets/logo-mark.png"><link rel="stylesheet" href="/style.css"><script defer src="/api.js"></script><script defer src="/app.js"></script><script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">Salta al contingut</a>{nav}<main id="main">{content}</main>{footer}</body></html>'''
 target=OUT/'index.html' if key=='index' else OUT/key/'index.html';target.parent.mkdir(exist_ok=True);target.write_text(doc)
aliases={'index.dc.html':'/','nintec-360.dc.html':'/nintec360/','contacte.dc.html':'/contacte/','equip.dc.html':'/equip/','nintec-finance.dc.html':'/finance/','nintec-compliance.dc.html':'/compliance/','politica-privacitat.dc.html':'/privacitat/','politica-cookies.dc.html':'/cookies/','termes-condicions.dc.html':'/termes/','nintec-360':'/nintec360/','nintec-finance':'/finance/','nintec-compliance':'/compliance/'}
(OUT/'_redirects').write_text('\n'.join('/'+a+' '+b+' 301' for a,b in aliases.items())+'\n')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+('/' if k=='index' else '/'+k+'/')+'</loc></url>' for k in pages)+'</urlset>')
(OUT/'404.html').write_text('<!doctype html><html lang="ca"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pàgina no trobada · Nintec</title><link rel="stylesheet" href="/style.css"><main class="wrap section"><p class="eyebrow">404</p><h1>Aquesta pàgina no hi és.</h1><a class="button" href="/">Torna a Nintec360 →</a></main></html>')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n')
print(f'Built {len(pages)} pages at {OUT}')
