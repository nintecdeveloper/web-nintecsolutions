from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,sys,xml.etree.ElementTree as ET
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.meta={};self.links=[];self.images=[];self.scripts=[];self.title='';self.graph=[];self.tag='';self.buffer='';self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='meta':self.meta[d.get('name',d.get('property'))]=d.get('content')
  if t=='link':self.links.append(d)
  if t=='img':self.images.append(d)
  if t=='script' and 'src' in d:self.scripts.append(d['src'].split('?')[0])
  if t=='title' or (t=='script' and d.get('type')=='application/ld+json'):self.tag=t;self.buffer=''
 def handle_data(self,d):
  if self.tag:self.buffer+=d
 def handle_endtag(self,t):
  if t==self.tag:
   if t=='title':self.title=self.buffer
   else:self.graph=json.loads(self.buffer)['@graph']
   self.tag=''
for root,production in [(Path(sys.argv[1]),False),(Path(sys.argv[2]),True)]:
 origin='https://www.nintecsolutions.com' if production else 'https://nintec360-redisseny.ijubany.chatgpt.site'
 titles=set();descs=set();expected=set()
 for f in root.rglob('index.html'):
  route='/'+str(f.relative_to(root)).removesuffix('index.html');p=Page(f.read_text());lang=route.split('/')[1] if route.startswith(('/es/','/en/')) else 'ca'
  assert (lang,p.title) not in titles,(route,'duplicate title');titles.add((lang,p.title))
  desc=p.meta['description'];assert (lang,desc) not in descs,(route,'duplicate description');descs.add((lang,desc))
  assert [x['href'] for x in p.links if x.get('rel')=='canonical']==[origin+route]
  alternates={x['hreflang']:x['href'] for x in p.links if x.get('rel')=='alternate'}
  assert set(alternates)=={'ca','es','en','x-default'}
  base=route[3:] if route.startswith(('/es/','/en/')) else route
  for lang,prefix in [('ca',''),('es','/es'),('en','/en'),('x-default','')]:assert alternates[lang]==origin+prefix+base
  legal=base in ['/privacitat/','/cookies/','/termes/'];indexable=production and not legal
  assert p.meta['robots'].startswith('index,' if indexable else 'noindex,')
  if indexable:expected.add(origin+route)
  assert p.meta['og:url']==origin+route and p.meta['twitter:card']=='summary_large_image'
  assert p.meta['og:image']==origin+'/assets/brand/social-card.png'
  types={x['@type'] for x in p.graph};assert {'Organization','WebSite','WebPage'}<=types
  assert ('BreadcrumbList' in types)==(base!='/')
  assert ('Service' in types)==(base in ['/nintec360/','/finance/'])
  assert not any(k in json.dumps(p.graph) for k in ['aggregateRating','priceCurrency','reviewCount'])
  for img in p.images:
   assert all(k in img for k in ['width','height','alt'])
   for entry in img.get('srcset','').split(','):
    if entry.strip():assert (root/entry.strip().split()[0].lstrip('/')).is_file()
  assert ('/api.js' in p.scripts)==(base in ['/contacte/','/compliance/'])
  assert ('/cycle-player.js' in p.scripts)==(base in ['/','/nintec360/'])
  assert '/i18n.js' not in p.scripts
 sitemap=ET.parse(root/'sitemap.xml');locs={x.text for x in sitemap.findall('.//{*}loc')};assert locs==expected
 assert len(locs)==(21 if production else 0)
 assert 'Disallow: /' not in (root/'robots.txt').read_text()
 for line in (root/'_redirects').read_text().splitlines():
  old,new,status=line.split();assert status=='301' and old!=new
  if not new.startswith('https:'):assert (root/urlsplit(new).path.lstrip('/')/'index.html').is_file(),new
 for f in root.rglob('404.html'):assert 'noindex, follow' in f.read_text()
 print('PASS SEO:',root.name,'30 routes, metadata, reciprocal locales, schema, images, script budgets, sitemap, robots, redirects, 404 markup')
