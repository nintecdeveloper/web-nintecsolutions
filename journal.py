"""Small static editorial renderer. Drafts require an explicit local preview flag."""
from pathlib import Path
from datetime import datetime
import html,json,math,re,hashlib,shutil
from seo import PRODUCTION_ORIGIN
from i18n import LOCALES,locale_path,selector,translate
from journal_i18n import Translation,Localizer
ROOT=Path(__file__).resolve().parent
CATEGORIES=['Models i productes','Empreses i mercat','Seguretat i societat','Recerca i infraestructura']
TYPES={'news':'Notícia','analysis':'Anàlisi','context':'Context'}
E=lambda x:html.escape(str(x),quote=True)

def load_articles(include_drafts=False):
 articles=[json.loads(p.read_text()) for p in sorted((ROOT/'src/journal/content').glob('*.json'))]
 ids={a['id'] for a in articles};slugs=set()
 assert len(ids)==len(articles),'Duplicate editorial ID'
 for a in articles:
  assert a['id'] in ids and a['slug'] not in slugs and re.fullmatch('[a-z0-9-]+',a['slug'])
  slugs.add(a['slug']);assert a['locale']=='ca' and a['category'] in CATEGORIES and a['type'] in TYPES
  assert a['status'] in ['draft','published']
  for field in ['eventDate','coverageSlot','verifiedAt']:datetime.fromisoformat(a[field])
  if a['status']=='published':
   assert a['datePublished'],'Published articles need their actual publication timestamp'
   assert datetime.fromisoformat(a['datePublished']).tzinfo,'Publication timestamp needs timezone'
  else:assert a['datePublished'] is None,'Do not backdate a draft'
  if a.get('dateModified'):assert a['datePublished'] and a['dateModified']>=a['datePublished']
  assert set(a['relatedIds'])<=ids and a['id'] not in a['relatedIds']
  assert all(b['type'] in ['p','h2'] for b in a['body'])
  assert all(s['url'].startswith('https://') for s in a['sources'])
  for b in a['body']:assert all(0<=i<len(a['sources']) for i in b.get('sources',[]))
 return [a for a in articles if include_drafts or a['status']=='published']

def base_paths(articles):
 return ['/blog/','/blog/arxiu/','/blog/criteri-editorial/']+[url(a) for a in articles] if articles else []
def paths(articles):return [locale_path(p,l) for p in base_paths(articles) for l in LOCALES]
def url(a):return '/blog/'+a['slug']+'/'
def date(value):
 d=datetime.fromisoformat(value);months=['gener','febrer','març','abril','maig','juny','juliol','agost','setembre','octubre','novembre','desembre']
 return f'{d.day} {months[d.month-1]} {d.year}'
def minutes(a):return math.ceil(sum(len(b['text'].split()) for b in a['body'])/220)
def nav_link(lang='ca',active=False):
 labels={'ca':'Actualitat IA','es':'Actualidad IA','en':'AI Journal','nl':'AI-nieuws'}
 return f'<a class="journal-nav" href="{locale_path("/blog/",lang)}"'+(' aria-current="page"' if active else '')+f'>{labels[lang]}</a>'
def credit(im):
 edits='Mida adaptada; fotografia retallada.' if im['fit']=='cover' else 'Mida adaptada, sense retall.'
 return f'<a href="{E(im["sourcePage"])}">{E(im["creator"])}</a> · <a href="{E(im["licenseUrl"])}">{E(im["licenseName"])}</a>. {E(im["permissionNotice"])} {edits}'
def picture(a,images,large=False):
 if not a['cover']:
  return '<div class="j-type-cover" aria-label="Dues prioritats del mercat: interfície i cost"><span>DUES PRIORITATS</span><strong>La resposta.<br>El que costa.</strong><span>GPT-6 / HAIKU 5.5</span></div>'
 im=images[a['cover']];srcset=', '.join(v['src']+' '+str(v['width'])+'w' for v in im['variants'])
 return f'<figure class="j-picture j-{E(im["fit"])}"><img src="{im["src"]}" srcset="{srcset}" sizes="{("(max-width: 700px) 100vw, 850px" if large else "(max-width: 700px) 90vw, 600px")}" width="{im["width"]}" height="{im["height"]}" alt="{E(im["alt"])}" loading="{("eager" if large else "lazy")}" decoding="async"'+(' fetchpriority="high"' if large else '')+f'><figcaption>{E(im["caption"])} <span>{credit(im)}</span></figcaption></figure>'
def meta(a):
 return f'<p class="j-meta"><span>{E(TYPES[a["type"]])}</span> · {minutes(a)} min de lectura · '+(f'<time datetime="{E(a["datePublished"])}">{date(a["datePublished"])}</time>' if a['datePublished'] else 'En preparació')+'</p>'
def card(a,images,kind='list',heading='h3'):
 return f'<article class="j-card j-card-{kind}" data-journal-card data-category="{E(a["category"])}" data-search="{E(a["title"]+" "+a["excerpt"]+" "+" ".join(a["tags"]))}">'+picture(a,images,kind=='lead')+f'<div class="j-card-copy"><p class="j-kicker">{E(a["category"])}</p><{heading}><a href="{url(a)}">{E(a["title"])}</a></{heading}><p class="j-excerpt">{E(a["excerpt"])}</p>{meta(a)}</div></article>'
def timeline(articles):
 rows=[]
 for a in sorted(articles,key=lambda a:a['eventDate'],reverse=True):
  rows.append(f'<li><time datetime="{a["eventDate"]}">{date(a["eventDate"])}</time><div><span>{E(a["category"])}</span><a href="{url(a)}">{E(a["title"])} <b aria-hidden="true">↗</b></a></div></li>')
 return '<ol class="j-timeline">'+''.join(rows)+'</ol>'
def home(articles,images):
 by={a['id']:a for a in articles};ordered=[by[i] for i in ['7','6','8','2','3','5','1','4'] if i in by]+[a for a in articles if a['id'] not in ['7','6','8','2','3','5','1','4']]
 hero=''.join(card(a,images,'lead' if i==0 else 'secondary','h2') for i,a in enumerate(ordered[:3]))
 filters=''.join(f'<button type="button" data-journal-filter="{E(c)}" aria-pressed="{str(i==0).lower()}">{E(c or "Tot")}</button>' for i,c in enumerate(['']+CATEGORIES))
 analysis=''.join(f'<a href="{url(a)}"><span>ANÀLISI · {minutes(a)} MIN</span><h3>{E(a["title"])}</h3><b aria-hidden="true">↗</b></a>' for a in articles if a['type']=='analysis')
 return f'''<div class="wrap j-wrap"><header class="j-masthead"><div class="j-edition"><span>NINTEC JOURNAL</span><a href="/blog/arxiu/">Arxiu ↗</a></div><h1>La intel·ligència artificial,<br><em>amb context.</em></h1><p>Models, empreses, seguretat i idees per entendre què està canviant.</p></header><section aria-label="Selecció editorial" class="j-opening">{hero}</section><section class="j-feed" aria-labelledby="j-feed-title"><div class="j-section-head"><h2 id="j-feed-title">Explora l’actualitat</h2><div class="j-search" data-journal-controls hidden><label for="journal-search">Cerca un tema</label><input type="search" id="journal-search" placeholder="Models, agents, xips…" autocomplete="off"></div></div><div class="j-filters" role="group" aria-label="Filtra per tema" data-journal-controls hidden>{filters}</div><p id="journal-count" class="j-count" role="status" aria-live="polite">{len(articles)} articles</p><div class="j-feed-grid">{''.join(card(a,images) for a in ordered)}</div><div id="journal-empty" class="j-empty" hidden><h3>No hem trobat cap article.</h3><p>Prova un altre terme o torna a veure tots els temes.</p><button class="button secondary" type="button" id="journal-reset">Neteja els filtres</button></div></section><section class="j-analysis" aria-labelledby="analysis-title"><p class="j-kicker">UNA MIRADA MÉS LLARGA</p><h2 id="analysis-title">Més enllà de l’anunci.</h2><div>{analysis}</div></section><section class="j-archive-summary" aria-labelledby="archive-title"><div><p class="j-kicker">28 SETEMBRE — 19 OCTUBRE 2026</p><h2 id="archive-title">Les últimes tres setmanes d’IA</h2><p>La cronologia dels fets, amb cada anunci al seu lloc.</p><a class="text-link" href="/blog/arxiu/">Consulta l’arxiu ↗</a></div>{timeline(articles)}</section><aside class="j-policy-note"><strong>Informació amb procedència.</strong><p>Distingim fets, anuncis corporatius i anàlisi. Fonts visibles, imatges acreditades i dates sense artificis.</p><a href="/blog/criteri-editorial/">El nostre criteri editorial ↗</a></aside></div>'''
def article(a,articles,images):
 paragraphs=[]
 for b in a['body']:
  refs=''.join(f' <a class="j-source-inline" href="{E(a["sources"][i]["url"])}">[{E(a["sources"][i]["publisher"])}]</a>' for i in b.get('sources',[]))
  paragraphs.append(f'<{b["type"]}>{E(b["text"])}{refs}</{b["type"]}>')
 sources=''.join(f'<li><a href="{E(s["url"])}">{E(s["title"])} ↗</a><span>{E(s["publisher"])} · {date(s["publishedAt"])} · {dict(primary="Font primària",reporting="Informació periodística",research="Publicació científica")[s["sourceType"]]}</span></li>' for s in a['sources'])
 by={x['id']:x for x in articles};related=''.join(card(by[i],images,'related') for i in a['relatedIds'] if i in by)
 modified=f'<p>Actualització editorial: {date(a["dateModified"])}</p>' if a.get('dateModified') else ''
 return f'''<div class="wrap j-wrap"><nav class="j-breadcrumb" aria-label="Fil d’Ariadna"><a href="/?lang=ca">Inici</a><span>/</span><a href="/blog/">Actualitat IA</a><span>/</span><span>{E(TYPES[a['type']])}</span></nav><article class="j-article"><header class="j-article-head"><p class="j-kicker">{E(a['category'])} / {E(TYPES[a['type']])}</p><h1>{E(a['title'])}</h1><p class="j-deck">{E(a['excerpt'])}</p><div class="j-byline"><a href="/blog/criteri-editorial/">{E(a['author']['name'])}</a>{meta(a)}<p>Data dels fets: <time datetime="{a['eventDate']}">{date(a['eventDate'])}</time> · Fonts comprovades: {date(a['verifiedAt'])}</p>{modified}</div></header><div class="j-article-cover">{picture(a,images,True)}</div><div class="j-reading"><aside class="j-context"><strong>Per situar la notícia</strong><p>{E(a['context'])}</p></aside>{''.join(paragraphs)}<section class="j-sources" aria-labelledby="sources-title"><h2 id="sources-title">Fonts i referències</h2><ul>{sources}</ul><p>Preparat amb assistència d’IA. <a href="/blog/criteri-editorial/">Criteri editorial i correccions</a>.</p></section></div></article><section class="j-related"><div class="j-section-head"><h2>Per continuar llegint</h2><a href="/blog/">Tota l’actualitat ↗</a></div><div>{related}</div></section></div>'''
def policy():
 return '''<div class="wrap j-wrap"><nav class="j-breadcrumb" aria-label="Fil d’Ariadna"><a href="/blog/">Actualitat IA</a><span>/</span><span>Criteri editorial</span></nav><header class="j-article-head"><p class="j-kicker">NINTEC JOURNAL</p><h1>El context també<br>té una procedència.</h1><p class="j-deck">Com preparem les peces d’Actualitat IA.</p></header><div class="j-reading j-policy"><h2>Qui hi ha darrere</h2><p>Nintec Solutions és responsable d’aquesta secció. L’autoria organitzativa és Equip editorial de Nintec Solutions. Aquesta edició s’ha preparat amb assistència d’intel·ligència artificial per a la recerca, la redacció i la implementació; no representa entrevistes ni proves pròpies dels productes.</p><h2>Fets, anuncis i anàlisi</h2><p>Enllacem les fonts que sostenen les afirmacions. Un comunicat confirma què anuncia una empresa; una millora de rendiment que declara el fabricant s’atribueix al fabricant. Identifiquem les peces d’anàlisi i no presentem una lectura editorial com un resultat mesurat.</p><h2>Dates que expliquen què ha passat</h2><p>La data dels fets situa l’anunci. La data de publicació correspon al moment real en què la peça es publica a Nintec. L’arxiu inicial cobreix el període del 28 de setembre al 19 d’octubre de 2026: no simula publicacions anteriors. Els esborranys indiquen «En preparació» i queden fora del sitemap públic.</p><h2>Imatges i actualitzacions</h2><p>Utilitzem fotografies, figures de recerca i materials amb una base d’ús documentada. Els peus identifiquen les imatges d’arxiu i els prototips, amb crèdit i llicència. No generem fotografies per il·lustrar les notícies. Una actualització substancial ha d’incorporar la data i una explicació del canvi.</p><h2>Correccions i contacte</h2><p>Si detectes un error, escriu a <a href="mailto:info@nintecsolutions.com?subject=Correcci%C3%B3%20Nintec%20Journal">info@nintecsolutions.com</a> amb l’enllaç de l’article i la informació que proposes contrastar. La secció no ofereix recomanacions d’inversió ni garanties sobre productes.</p><a class="text-link" href="/blog/">Torna a Actualitat IA ↗</a></div></div>'''
def build(out,src,versions,header,footer,bootstrap,scripts,articles,production=False):
 if not articles:return []
 images=json.loads((src/'journal/images.json').read_text())
 for a in articles:
  if a['cover']:
   im=images[a['cover']];assert im['rightsStatus']=='verified'
   for v in im['variants']:assert (src/v['src'].lstrip('/')).is_file()
 shutil.copytree(src/'assets/journal',out/'assets/journal')
 for f in ['journal.css','journal.js']:shutil.copy(src/f,out/f)
 header=header.replace('<a class="nav-contact"',nav_link(active=True)+'<a class="nav-contact"')
 site_paths=['/' if k=='index' else '/'+k+'/' for k in json.loads((src/'pages.json').read_text())]+base_paths(articles)
 translations={lang:Translation(lang,articles,images) for lang in LOCALES}
 runtime_keys=json.loads((src/'locales/runtime.json').read_text())
 docs=[('/blog/','Actualitat IA — Nintec Journal','Notícies i anàlisi d’intel·ligència artificial: models, agents, empreses, seguretat, recerca i infraestructura, amb fonts i context.',home(articles,images),None),('/blog/arxiu/','Arxiu d’actualitat IA | Nintec Journal','La cronologia dels anuncis i les anàlisis d’Actualitat IA, ordenada per la data dels fets.',f'<div class="wrap j-wrap"><header class="j-article-head"><p class="j-kicker">NINTEC JOURNAL / ARXIU</p><h1>Les últimes tres<br>setmanes d’IA.</h1><p class="j-deck">28 de setembre — 19 d’octubre de 2026</p><p>Ordenat per la data dels fets. La data de cada publicació figura a la seva pàgina.</p></header>{timeline(articles)}<a class="text-link" href="/blog/">Torna a la portada ↗</a></div>',None),('/blog/criteri-editorial/','Criteri editorial | Nintec Journal','Autoria, fonts, dates, imatges i correccions: com preparem l’actualitat i l’anàlisi d’intel·ligència artificial a Nintec Solutions.',policy(),None)]
 docs += [(url(a),a['seoTitle'],a['metaDescription'],article(a,articles,images),a) for a in articles]
 origin=PRODUCTION_ORIGIN;org={'@type':'Organization','name':'Nintec Solutions','url':origin,'logo':{'@type':'ImageObject','url':origin+'/assets/brand/nintec-logo-horizontal-light.svg'}}
 draft_edition=any(a['status']=='draft' for a in articles)
 for path,title,description,content,a in docs:
  image=images[a['cover']] if a and a['cover'] else None
  image_url=origin+(image['src'] if image else '/assets/brand/social-card.png')
  indexed=production and not draft_edition and (not a or a['status']=='published')
  schema={'@context':'https://schema.org','@type':('NewsArticle' if a['type']=='news' else 'BlogPosting') if a else ('CollectionPage' if path!='/blog/criteri-editorial/' else 'AboutPage'),'headline':a['title'] if a else title,'name':title,'description':description,'mainEntityOfPage':origin+path,'url':origin+path,'inLanguage':'ca','publisher':org}
  if a:
   schema.update(author={'@type':a['author']['type'],'name':a['author']['name'],'url':a['author']['url']},wordCount=sum(len(b['text'].split()) for b in a['body']))
   for key in ['datePublished','dateModified']:
    if a.get(key):schema[key]=a[key]
   if image:schema['image']={'@type':'ImageObject','url':image_url,'width':image['width'],'height':image['height'],'caption':image['caption'],'creditText':image['creator'],'license':image['licenseUrl']}
  elif path!='/blog/criteri-editorial/':schema['mainEntity']={'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':origin+url(item),'name':item['title']} for i,item in enumerate(articles)]}
  crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Inici','item':origin+'/'},{'@type':'ListItem','position':2,'name':'Actualitat IA','item':origin+'/blog/'}]+([{'@type':'ListItem','position':3,'name':a['title'] if a else title,'item':origin+path}] if path!='/blog/' else [])}
  banner='<div class="j-preview">Vista prèvia · Edició en preparació · No publicada</div>' if draft_edition else ''
  ogdates=''.join(f'<meta property="article:{"published_time" if k=="datePublished" else "modified_time"}" content="{E(a[k])}">' for k in ['datePublished','dateModified'] if a and a.get(k))
  doc=f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="robots" content="{'index, follow, max-image-preview:large' if indexed else 'noindex, follow'}"><link rel="canonical" href="{origin}{path}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="{'article' if a else 'website'}"><meta property="og:url" content="{origin}{path}"><meta property="og:site_name" content="Nintec Journal"><meta property="og:locale" content="ca_ES"><meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{E(image['alt'] if image else 'Nintec Solutions')}"><meta name="twitter:card" content="summary_large_image">{ogdates}<link rel="icon" href="/assets/brand/nintec-icon.svg"><link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png"><link rel="stylesheet" href="/style.css?v={versions['style.css']}"><link rel="stylesheet" href="/journal.css?v={hashlib.sha256((src/'journal.css').read_bytes()).hexdigest()[:12]}"><script type="application/ld+json">JOURNAL_SCHEMA</script>JOURNAL_BOOTSTRAP{scripts}<script defer src="/journal.js?v={hashlib.sha256((src/'journal.js').read_bytes()).hexdigest()[:12]}"></script></head><body class="journal-page"><a class="skip" href="#main">Salta al contingut</a>{header}{banner}<main id="main">{content}</main>{footer}</body></html>'''
  for lang in LOCALES:
   localizer=Localizer(translations[lang],site_paths,origin)
   localized=localizer.render(doc).replace('<span id="language-slot"></span>',selector(path,lang))
   graph=localizer.schema([schema,crumbs])
   if a:graph[0]['wordCount']=sum(len(translations[lang].tr(b['text']).split()) for b in a['body'])
   messages=json.dumps({k:translate(k,lang) for k in runtime_keys},ensure_ascii=False).replace('<','\\u003c')
   localized_bootstrap=re.sub(r'(<script type="application/json" id="i18n-messages">).*?(</script>)',lambda m:m[1]+messages+m[2],bootstrap,flags=re.S)
   localized=localized.replace('JOURNAL_SCHEMA',json.dumps(graph,ensure_ascii=False).replace('<','\\u003c')).replace('JOURNAL_BOOTSTRAP',localized_bootstrap)
   alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{origin}{locale_path(path,l)}">' for l in LOCALES)+f'<link rel="alternate" hreflang="x-default" href="{origin}{path}">'
   localized=localized.replace('</head>',alternates+'</head>')
   target=out/locale_path(path,lang).lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(localized)
 return paths(articles)
