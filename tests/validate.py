from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1];dist=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'dist';errors=[];pages=list(dist.rglob('index.html'))
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.sources=[];self.h1=0;self.title=0;self.lang=None;self.canonical=0;self.description=0;self.labels=[];self.fields=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id'in d:self.ids.append(d['id'])
  if tag=='html':self.lang=d.get('lang')
  if tag=='a'and'href'in d:self.links.append(d['href'])
  if tag=='img':
   if 'alt'not in d:errors.append('Image missing alt')
   self.sources.append(d.get('src',''))
  if tag=='script'and'src'in d:self.sources.append(d['src'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title+=1
  if tag=='link'and d.get('rel')=='canonical':self.canonical+=1
  if tag=='meta'and d.get('name')=='description':self.description+=1
  if tag=='label'and'for'in d:self.labels.append(d['for'])
  if tag in ('input','textarea')and d.get('type')!='checkbox':self.fields.append(d.get('id'))
parsed={}
for path in pages:
 p=Page();p.feed(path.read_text());parsed[path]=p
 if p.h1!=1 or p.title!=1 or p.lang!=('es' if path.relative_to(dist).parts[0]=='es' else 'en' if path.relative_to(dist).parts[0]=='en' else 'ca') or p.canonical!=1 or p.description!=1:errors.append(f'{path}: metadata/headings')
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{path}: duplicate IDs')
 for field in p.fields:
  if field not in p.labels:errors.append(f'{path}: label {field}')
for path,p in parsed.items():
 for link in p.links+p.sources:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if not u.path:target=path
  else:
   target=dist/unquote(u.path.lstrip('/'))
   if u.path.endswith('/'):target=target/'index.html'
  if not target.exists():errors.append(f'{path}: missing {link}');continue
  if u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(f'{path}: missing anchor {link}')
ET.parse(dist/'sitemap.xml')
assert len(pages)==30
assert not errors,'\n'.join(errors)
print(f'PASS: {len(pages)} pages; internal links/anchors/assets; one h1/title/canonical/description per page; lang matches route; form labels; unique IDs; valid sitemap XML.')
print('Homepage bytes:',(dist/'index.html').stat().st_size,'Shared JS bytes:',sum((dist/f).stat().st_size for f in ['app.js','api.js']))
