"""Strict, build-time Journal translations. Missing copy stops the build."""
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import html,json,re
from i18n import LOCALES,CATALOGUES,locale_path
ROOT=Path(__file__).parent
MONTHS={
 'ca':'gener febrer març abril maig juny juliol agost setembre octubre novembre desembre'.split(),
 'es':'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split(),
 'en':'January February March April May June July August September October November December'.split(),
 'nl':'januari februari maart april mei juni juli augustus september oktober november december'.split()}
def date(value,lang):
 d=datetime.fromisoformat(value);return f'{d.day} {MONTHS[lang][d.month-1]} {d.year}'
class Translation:
 def __init__(self,lang,articles,images):
  self.lang=lang;self.catalog={**CATALOGUES.get(lang,{}),**(json.loads((ROOT/'src/journal/locales'/f'{lang}.json').read_text()) if lang!='ca' else {})}
  # Official source titles, names and licence identifiers are retained verbatim.
  names={'JOURNAL_BOOTSTRAP','/','Nintec Solutions','NINTEC JOURNAL','GPT-6 / HAIKU 5.5'}
  for im in images.values():
   if 'i col·laboradors' not in im['creator']:names.add(im['creator'])
   if im['licenseName'].startswith('CC BY'):names.add(im['licenseName'])
  for a in articles:
   for s in a['sources']:
    names.update([s['publisher'],'['+s['publisher']+']'])
    if s['title'] not in self.catalog:names.add(s['title'])
  for name in names:self.catalog.setdefault(name,name)
  for a in articles:
   for source in a['sources']:
    title=source['title'];self.catalog[title+' ↗']=self.tr(title)+' ↗'
    kind={'primary':'Font primària','reporting':'Informació periodística','research':'Publicació científica'}[source['sourceType']]
    self.catalog[f'{source["publisher"]} · {date(source["publishedAt"],"ca")} · {kind}']=f'{source["publisher"]} · {date(source["publishedAt"],lang)} · {self.tr(kind)}'
   for key in ['eventDate','verifiedAt','datePublished','dateModified']:
    if a.get(key):self.catalog[date(a[key],'ca')]=date(a[key],lang)
   self.catalog['· Fonts comprovades: '+date(a['verifiedAt'],'ca')]=['· Fonts comprovades: ','· Fuentes comprobadas: ','· Sources checked: ','· Bronnen gecontroleerd: '][LOCALES.index(lang)]+date(a['verifiedAt'],lang)
   if a.get('dateModified'):self.catalog['Actualització editorial: '+date(a['dateModified'],'ca')]=['Actualització editorial: ','Actualización editorial: ','Editorial update: ','Redactionele update: '][LOCALES.index(lang)]+date(a['dateModified'],lang)
   kind={'news':'Notícia','analysis':'Anàlisi','context':'Context'}[a['type']]
   self.catalog[a['category']+' / '+kind]=self.tr(a['category'])+' / '+self.tr(kind)
   search=a['title']+' '+a['excerpt']+' '+' '.join(a['tags'])
   # Search the complete translated heading and summary; no hidden CA keywords.
   self.catalog[search]=self.tr(a['title'])+' '+self.tr(a['excerpt'])
  for n in range(1,61):
   read={'ca':f'· {n} min de lectura ·','es':f'· {n} min de lectura ·','en':f'· {n} min read ·','nl':f'· {n} min leestijd ·'}[lang]
   self.catalog[f'· {n} min de lectura ·']=read
   self.catalog[f'· {n} min de lectura · En preparació']=read+' '+self.tr('En preparació')
   self.catalog[f'ANÀLISI · {n} MIN']={'ca':'ANÀLISI','es':'ANÁLISIS','en':'ANALYSIS','nl':'ANALYSE'}[lang]+f' · {n} MIN'
  n=len(articles);self.catalog[f'{n} articles']=f'{n} '+{'ca':'articles','es':'artículos','en':'articles','nl':'artikelen'}[lang]
 def tr(self,text):
  if self.lang=='ca' or not text.strip():return text
  key=text.strip()
  if key not in self.catalog:raise ValueError(f'Missing Journal {self.lang} translation: {key!r}')
  return text[:len(text)-len(text.lstrip())]+self.catalog[key]+text[len(text.rstrip()):]
class Localizer(HTMLParser):
 def __init__(self,translation,paths,origin):
  super().__init__(convert_charrefs=True);self.t=translation;self.paths=paths;self.origin=origin;self.out=[];self.skip=0
 def link(self,url):
  u=urlsplit(url)
  if (not u.netloc or u.scheme+'://'+u.netloc==self.origin) and u.path in self.paths:
   query=urlencode([(k,self.t.lang if k=='lang' else v) for k,v in parse_qsl(u.query)])
   return urlunsplit((u.scheme,u.netloc,locale_path(u.path,self.t.lang),query,u.fragment))
  return url
 def handle_decl(self,d):self.out.append('<!'+d+'>')
 def handle_starttag(self,tag,attrs):
  data=dict(attrs);out=[]
  for k,v in attrs:
   if v is None:out.append(k);continue
   if k in ('alt','title','placeholder','aria-label','data-search'):v=self.t.tr(v)
   elif tag=='html' and k=='lang':v=self.t.lang
   elif k=='href':v=self.link(v)
   elif tag=='meta' and k=='content':
    if data.get('name')=='description' or data.get('property') in ('og:title','og:description','og:image:alt'):v=self.t.tr(v)
    elif data.get('property')=='og:locale':v={'ca':'ca_ES','es':'es_ES','en':'en_GB','nl':'nl_NL'}[self.t.lang]
    elif data.get('property')=='og:url':v=self.link(v)
   out.append(k+'="'+html.escape(v,quote=True)+'"')
  self.out.append('<'+tag+(' '+' '.join(out) if out else '')+'>')
  if tag in ('script','style'):self.skip+=1
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
 def handle_endtag(self,t):
  self.out.append('</'+t+'>')
  if t in ('script','style'):self.skip-=1
 def handle_data(self,text):self.out.append(text if self.skip else html.escape(self.t.tr(text),quote=False))
 def handle_comment(self,text):self.out.append('<!--'+text+'-->')
 def schema(self,value,key=None):
  if isinstance(value,list):return [self.schema(v,key) for v in value]
  if isinstance(value,dict):return {k:self.schema(v,k) for k,v in value.items()}
  if isinstance(value,str):
   if key=='inLanguage':return self.t.lang
   if key in ('headline','name','description','caption','creditText'):return self.t.tr(value)
   if key in ('url','item','mainEntityOfPage'):return self.link(value)
  return value
 def render(self,doc):self.feed(doc);return ''.join(self.out)
