"""Strict build-time localisation: one shared set of templates, reviewed catalogues."""
import html,json,re
from html.parser import HTMLParser
from urllib.parse import urlsplit,urlunsplit
from pathlib import Path
LOCALES=('ca','es','en','nl')
ROOT=Path(__file__).parent
CATALOGUES={lang:json.loads((ROOT/'src/locales'/f'{lang}.json').read_text()) for lang in ('es','en','nl')}
def translate(text,lang):
 if lang=='ca' or not text.strip():return text
 key=text.strip()
 if key not in CATALOGUES[lang]:raise ValueError(f'Missing {lang} translation: {key!r}')
 return text[:len(text)-len(text.lstrip())]+CATALOGUES[lang][key]+text[len(text.rstrip()):]
def locale_path(path,lang):return ('' if lang=='ca' else '/'+lang)+path
class Localizer(HTMLParser):
 def __init__(self,lang,paths,origin):
  super().__init__(convert_charrefs=True);self.lang=lang;self.paths=paths;self.origin=origin;self.out=[];self.skip=0
 def link(self,url):
  u=urlsplit(url)
  if (not u.netloc or (u.scheme+'://'+u.netloc)==self.origin) and u.path in self.paths:
   return urlunsplit((u.scheme,u.netloc,locale_path(u.path,self.lang),u.query,u.fragment))
  return url
 def handle_decl(self,d):self.out.append('<!'+d+'>')
 def handle_starttag(self,tag,attrs):
  data=dict(attrs);out=[]
  for k,v in attrs:
   if v is None:out.append(k);continue
   if k in ('alt','title','placeholder','aria-label'):v=translate(v,self.lang)
   elif tag=='html' and k=='lang':v=self.lang
   elif k=='href':v=self.link(v)
   elif tag=='meta' and k=='content':
    if data.get('name')=='description' or data.get('property') in ('og:title','og:description'):v=translate(v,self.lang)
    elif data.get('property')=='og:locale':v={'ca':'ca_ES','es':'es_ES','en':'en_GB','nl':'nl_NL'}[self.lang]
    elif data.get('property')=='og:url':v=self.link(v)
   out.append(k+'="'+html.escape(v,quote=True)+'"')
  self.out.append('<'+tag+(' '+' '.join(out) if out else '')+'>')
  if tag in ('script','style'):self.skip+=1
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):
  self.out.append('</'+tag+'>')
  if tag in ('script','style'):self.skip-=1
 def handle_data(self,text):self.out.append(text if self.skip else html.escape(translate(text,self.lang),quote=False))
 def handle_comment(self,text):self.out.append('<!--'+text+'-->')
def localize(doc,lang,paths,origin):
 p=Localizer(lang,paths,origin);p.feed(doc);return ''.join(p.out)
def selector(path,lang):
 label=translate('Idioma del lloc web',lang)
 links=''.join(f'<a href="{locale_path(path,l)}?lang={l}" lang="{l}" hreflang="{l}" data-language="{l}"'+(' aria-current="true"' if l==lang else '')+f'>{l.upper()} <span>{name}</span></a>' for l,name in [('ca','Català'),('es','Español'),('en','English'),('nl','Nederlands')])
 return f'<details class="language-picker"><summary aria-label="{label}: {lang.upper()}">{lang.upper()} <span aria-hidden="true">⌄</span></summary><nav aria-label="{label}">{links}</nav></details>'
