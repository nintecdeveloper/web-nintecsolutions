from pathlib import Path
import shutil,json,html,os,hashlib,argparse,re
from urllib.parse import urlsplit
from cycle import render_cycle
from i18n import LOCALES,translate,localize,locale_path,selector
from seo import PRODUCTION_ORIGIN,PREVIEW_ORIGIN,structured_data,breadcrumbs,sharing,redirects
ROOT=Path(__file__).parent.resolve();SRC=ROOT/'src'
parser=argparse.ArgumentParser(description='Build the existing trilingual static website.')
parser.add_argument('--production',action='store_true',help='Generate the verified public www domain and indexable marketing pages.')
parser.add_argument('--output',type=Path,default=ROOT/'dist')
args=parser.parse_args();PRODUCTION=args.production or os.environ.get('SITE_ENV')=='production';OUT=args.output.resolve()
if OUT in (ROOT,SRC) or OUT in ROOT.parents or OUT==SRC or SRC in OUT.parents:raise ValueError('Unsafe output directory')
ORIGIN=os.environ.get('SITE_ORIGIN',PRODUCTION_ORIGIN if PRODUCTION else PREVIEW_ORIGIN).rstrip('/')
u=urlsplit(ORIGIN)
if u.scheme!='https' or not u.netloc or u.path or u.query or u.fragment:raise ValueError('SITE_ORIGIN must be an HTTPS origin without a path')
if PRODUCTION and ORIGIN!=PRODUCTION_ORIGIN:raise ValueError('Production origin must match the verified www domain; update seo.py only after verifying a domain change')
pages=json.loads((SRC/'pages.json').read_text());PAGE_PATHS=['/' if k=='index' else '/'+k+'/' for k in pages]
versions={f:hashlib.sha256((SRC/f).read_bytes()).hexdigest()[:12] for f in ['style.css','app.js','api.js','cycle-player.js']}
RUNTIME_KEYS=json.loads((SRC/'locales/runtime.json').read_text())
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
 if p.is_dir():shutil.rmtree(p)
 else:p.unlink()
# Publish only optimized images plus the original logo used by structured data.
(OUT/'assets').mkdir()
for p in (SRC/'assets').iterdir():
 if p.suffix=='.webp' or p.name in ('social-card.png','favicon.png','logo-mark.png'):shutil.copy(p,OUT/'assets'/p.name)
for f in versions:shutil.copy(SRC/f,OUT/f)
# Inline the small locale bootstrap: preserve preference before painting without
# a blocking JavaScript download. Application and circle scripts remain deferred.
locale_script=(SRC/'i18n.js').read_text().replace('</script','<\\/script')
verification=os.environ.get('GOOGLE_SITE_VERIFICATION','').strip()
for key,meta in pages.items():
 path='/' if key=='index' else '/'+key+'/'
 content=(SRC/(key+'.html')).read_text()
 has_cycle='{{CYCLE_WHEEL}}' in content
 if has_cycle:
  wheel,details=render_cycle(SRC,key);content=content.replace('{{CYCLE_WHEEL}}',wheel).replace('{{CYCLE_DETAILS}}',details)
 nav=(SRC/'header.html').read_text().replace('data-page="'+key+'"','aria-current="page"');footer=(SRC/'footer.html').read_text()
 title=html.escape(meta['title']);desc=html.escape(meta['description'],quote=True)
 for lang in LOCALES:
  url=ORIGIN+locale_path(path,lang);indexable=PRODUCTION and meta.get('indexable',True)
  robots='index, follow, max-image-preview:large' if indexable else 'noindex, follow'
  base=f'<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{ORIGIN}{path}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:locale" content="ca_ES"><meta property="og:site_name" content="Nintec Solutions"><meta property="og:url" content="{ORIGIN}{path}"><meta name="theme-color" content="#5c39d9"><link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon.png"><link rel="stylesheet" href="/style.css?v={versions["style.css"]}"></head><body><a class="skip" href="#main">Salta al contingut</a>{nav}<main id="main">{content}</main>{footer}</body></html>'
  doc=localize(base,lang,PAGE_PATHS,ORIGIN).replace('<span id="language-slot"></span>',selector(path,lang))
  if key!='index':doc=doc.replace('<main id="main">','<main id="main">'+breadcrumbs(meta,lang,path))
  alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{locale_path(path,l)}">' for l in LOCALES)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}">'
  messages=json.dumps({k:translate(k,lang) for k in RUNTIME_KEYS},ensure_ascii=False).replace('<','\\u003c')
  bootstrap=f'<script type="application/json" id="i18n-messages">{messages}</script><script>{locale_script}</script>'
  scripts=(f'<script defer src="/api.js?v={versions["api.js"]}"></script>' if key in ('contacte','compliance') else '')+(f'<script defer src="/cycle-player.js?v={versions["cycle-player.js"]}"></script>' if has_cycle else '')+f'<script defer src="/app.js?v={versions["app.js"]}"></script>'
  extra=f'<meta name="robots" content="{robots}">'+alternates+sharing(meta,lang,path,ORIGIN)+f'<script type="application/ld+json">{structured_data(key,meta,lang,path,ORIGIN)}</script>'+bootstrap+scripts
  if PRODUCTION and verification:extra+=f'<meta name="google-site-verification" content="{html.escape(verification,quote=True)}">'
  doc=doc.replace('</head>',extra+'</head>')
  target=OUT/locale_path(path,lang).lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc)
all_paths=[locale_path(p,l) for p in PAGE_PATHS for l in LOCALES]
(OUT/'_redirects').write_text(redirects(all_paths,PRODUCTION))
# Allow crawling to read noindex; private access remains the security boundary.
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n'+('Sitemap: '+ORIGIN+'/sitemap.xml\n' if PRODUCTION else '# Private review: no indexable URLs; pages carry noindex.\n'))
entries=[]
if PRODUCTION:
 for key,meta in pages.items():
  if not meta.get('indexable',True):continue
  path='/' if key=='index' else '/'+key+'/'
  alternatives=''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{ORIGIN}{locale_path(path,l)}"/>' for l in LOCALES)+f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}"/>'
  for lang in LOCALES:entries.append(f'<url><loc>{ORIGIN}{locale_path(path,lang)}</loc>{alternatives}</url>')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join(entries)+'</urlset>')
for lang in LOCALES:
 error=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{translate("Pàgina no trobada · Nintec",lang)}</title><meta name="robots" content="noindex, follow"><link rel="icon" href="/assets/favicon.png"><link rel="stylesheet" href="/style.css?v={versions["style.css"]}"></head><body><main class="wrap section"><a class="brand" href="{locale_path("/",lang)}">Nintec Solutions</a><p class="eyebrow">404</p><h1>{translate("Aquesta pàgina no hi és.",lang)}</h1><div class="actions"><a class="button" href="{locale_path("/",lang)}">{translate("Torna a Nintec360 →",lang)}</a><a class="text-link" href="{locale_path("/contacte/",lang)}">{translate("Reserva una auditoria ↗",lang)}</a></div></main></body></html>'
 (OUT/('' if lang=='ca' else lang)/'404.html').write_text(error)
headers='/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n'
if not PRODUCTION:headers+='  X-Robots-Tag: noindex, follow\n'
for key,meta in pages.items():
 if not meta.get('indexable',True):
  for lang in LOCALES:headers+=locale_path('/'+key+'/',lang)+'\n  X-Robots-Tag: noindex, follow\n'
headers+='/assets/*\n  Cache-Control: public, max-age=86400\n'
(OUT/'_headers').write_text(headers)
print(f'Built 30 pages; {len(entries)} sitemap URLs; {"production" if PRODUCTION else "private review"}; {ORIGIN}; output={OUT}')
