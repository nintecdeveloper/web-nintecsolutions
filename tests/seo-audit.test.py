"""Audit emitted production HTML and real local HTTP responses, never deploy."""
import json,sys,threading,functools,urllib.request,urllib.error
from pathlib import Path
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from collections import defaultdict
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from seo import retired_paths,PRODUCTION_ORIGIN
from i18n import LOCALES,locale_path,translate
out=Path(sys.argv[1]).resolve()
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.lang='';self.title='';self.h1='';self.meta={};self.canonical=[];self.alternates={};self.hrefs=[];self.title_open=False;self.h1_open=False;self.h1_count=0;self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='html':self.lang=d.get('lang','')
  if t=='title':self.title_open=True
  if t=='h1':self.h1_open=True;self.h1_count+=1
  if t=='br' and self.h1_open:self.h1+=' '
  if t=='meta':self.meta[d.get('name',d.get('property'))]=d.get('content')
  if t=='a':self.hrefs.append(d.get('href',''))
  if t=='link' and d.get('rel')=='canonical':self.canonical.append(d['href'])
  if t=='link' and d.get('rel')=='alternate':self.alternates[d['hreflang']]=d['href']
 def handle_data(self,d):
  if self.title_open:self.title+=d
  if self.h1_open:self.h1+=d
 def handle_endtag(self,t):
  if t=='title':self.title_open=False
  if t=='h1':self.h1_open=False
pages={}
for f in out.rglob('index.html'):
 path='/'+str(f.relative_to(out)).removesuffix('index.html');pages[path]=Page(f.read_text())
config=json.loads((ROOT/'vercel.json').read_text());rewrites={r['source'] for r in config['rewrites']}
assert rewrites==set(pages)
for path in retired_paths():
 assert path not in pages and path not in rewrites
 assert not any(r['source']==path for r in config['redirects']),path
 assert not (out/path.lstrip('/')).is_file(),path
for key in ['title','h1','description']:
 seen={}
 for path,p in pages.items():
  value=p.meta['description'] if key=='description' else getattr(p,key)
  identity=(p.lang,' '.join(value.split()))
  assert identity not in seen,(key,path,seen.get(identity));seen[identity]=path
for path,p in pages.items():
 assert p.h1_count==1,path
 assert p.canonical==[PRODUCTION_ORIGIN+path],path
 base=path[3:] if path.startswith(('/es/','/en/','/nl/')) else path
 assert p.alternates=={**{l:PRODUCTION_ORIGIN+locale_path(base,l) for l in LOCALES},'x-default':PRODUCTION_ORIGIN+base}
 for lang in LOCALES:
  equivalent=locale_path(base,lang);assert equivalent in pages
  assert pages[equivalent].alternates[p.lang]==PRODUCTION_ORIGIN+path
 assert not any('lang=' in href for href in p.hrefs),path
 for href in p.hrefs:
  assert href.split('?')[0].split('#')[0] not in retired_paths(),(path,href)
 legal=base in ['/privacitat/','/cookies/','/termes/']
 assert p.meta['robots'].startswith('noindex' if legal else 'index'),path
home=json.loads((ROOT/'src/pages.json').read_text())['index']
for lang in LOCALES:
 p=pages[locale_path('/',lang)]
 assert p.title==translate(home['title'],lang)
 assert p.meta['description']==translate(home['description'],lang)
 assert p.meta['og:title']==p.title and p.meta['twitter:title']==p.title
 assert p.meta['og:description']==p.meta['description']
sitemap=ET.parse(out/'sitemap.xml');urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
assert len(urls)==len(set(urls))==96
assert set(urls)=={PRODUCTION_ORIGIN+path for path,p in pages.items() if p.meta['robots'].startswith('index')}
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(out)))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
base='http://127.0.0.1:'+str(server.server_address[1])
def request(path):
 try:r=urllib.request.urlopen(base+path)
 except urllib.error.HTTPError as e:r=e
 return r.code,r.read().decode()
try:
 for path in retired_paths()+['/not-a-real-page/']:
  status,_=request(path);assert status==404,(path,status)
 for lang in LOCALES:
  path=locale_path('/',lang)
  for query in ['', '?lang=ca','?lang=en','?lang=nl&utm_source=seo-audit']:
   status,body=request(path+query);p=Page(body)
   assert status==200 and p.lang==lang
   assert p.title==pages[path].title and p.canonical==[PRODUCTION_ORIGIN+path]
 for path in ['/robots.txt','/sitemap.xml']:assert request(path)[0]==200
 assert 'Allow: /' in request('/robots.txt')[1]
 assert 'Disallow: /' not in request('/robots.txt')[1]
finally:server.shutdown();server.server_close();thread.join()
print(f'PASS: {len(pages)} localized pages; unique title/description/H1 per language; reciprocal real alternates; clean links; new Home metadata; {len(retired_paths())} retired URLs return HTTP 404 in static hosting; query canonicals; 96 indexable URLs; robots/sitemap HTTP 200')
