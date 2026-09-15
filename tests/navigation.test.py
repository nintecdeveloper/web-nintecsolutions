"""Four-locale navigation and complete build-time Dutch catalogue contract."""
from pathlib import Path
from html.parser import HTMLParser
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from i18n import LOCALES,locale_path
class Navigation(HTMLParser):
 def __init__(self,text):
  super().__init__();self.nav=False;self.links=[];self.logos=[];self.languages={};self.current=None;self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='nav' and d.get('id')=='navigation':self.nav=True
  if t=='a':
   if 'brand' in d.get('class','').split():self.logos.append(d['href'])
   if 'data-language' in d:self.languages[d['data-language']]=d['href']
   if self.nav and 'nav-contact' not in d.get('class',''):self.current=[d,''];self.links.append(self.current)
 def handle_data(self,d):
  if self.current:self.current[1]+=d
 def handle_endtag(self,t):
  if t=='a':self.current=None
  if t=='nav':self.nav=False
labels={'ca':['Inici','Qui som','Nintec360','Casos reals'],'es':['Inicio','Quiénes somos','Nintec360','Casos reales'],'en':['Home','About us','Nintec360','Real cases'],'nl':['Home','Over ons','Nintec360','Praktijkvoorbeelden']}
pages=json.loads((ROOT/'src/pages.json').read_text())
for lang in LOCALES:
 for key in pages:
  route=locale_path('/' if key=='index' else '/'+key+'/',lang)
  p=Navigation((ROOT/'dist'/route.lstrip('/')/'index.html').read_text())
  assert [a[1] for a in p.links]==labels[lang],route
  assert [a[0]['href'] for a in p.links]==[locale_path(s,lang) for s in ['/','/equip/','/nintec360/','/casos/']],route
  assert p.logos==[locale_path('/',lang)]*2,route
  assert p.languages=={l:locale_path('/' if key=='index' else '/'+key+'/',l)+'?lang='+l for l in LOCALES},route
  active=[a[0]['href'] for a in p.links if a[0].get('aria-current')=='page']
  assert active==([route] if key in ['index','equip','nintec360','casos'] else []),route
nl=json.loads((ROOT/'src/locales/nl.json').read_text());en=json.loads((ROOT/'src/locales/en.json').read_text())
assert set(nl)==set(en)
assert all(isinstance(v,str) and v.strip() for v in nl.values())
print('PASS: 40 pages; exact menu order; active navigation; locale home logos; reciprocal selectors; complete Dutch catalogue')
