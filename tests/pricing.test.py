"""Pricing and retired sections stay coherent across every configured locale."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from i18n import LOCALES,locale_path,translate
from seo import redirects
pages=json.loads((ROOT/'src/pages.json').read_text())
assert 'pricing' in pages and not set(('equip','finance','compliance'))&pages.keys()
rules={line.split()[0]:line.split()[1] for line in redirects([],True).splitlines()}
for lang in LOCALES:
 path=locale_path('/pricing/',lang)
 text=(ROOT/'dist'/path.lstrip('/')/'index.html').read_text()
 assert translate('Una solució que creix amb tu.',lang) in text
 assert translate('Tria el teu punt de partida. Nosaltres adaptem Nintec360 a les necessitats del teu negoci.',lang) in text
 assert f'href="{locale_path("/contacte/",lang)}"' in text
 assert text.count('class="pricing-usage"')==5
 assert text.count('role="tooltip"')==16
 assert text.count('<details>')>=5
 assert text.split('<main')[1].split('</main>')[0].count('data-lead-cta')==6
 for price in ['299 €','499 €','799 €','1.499 €']:assert price in text
 for name in ['starter','basic','pro','premium','enterprise']:assert f'id="{name}"' in text
 for retired in ('equip','finance','compliance'):
  base=locale_path('/'+retired+'/',lang)
  assert not (ROOT/'dist'/base.lstrip('/')).exists()
  for old in (base,base.rstrip('/'),base+'index.html'):assert old not in rules
for f in (ROOT/'dist').rglob('*.html'):
 text=f.read_text()
 for forbidden in ('Nintec Finance','Nintec Compliance','home-ecosystem','/equip/','/finance/','/compliance/'):
  assert forbidden not in text,(f,forbidden)
print('PASS: Pricing translations, contact links, retired routes and absence of removed sections across all public HTML and four languages')
# Verify exact per-plan allowances and the shared audit form contract.
from html.parser import HTMLParser
class Usage(HTMLParser):
 def __init__(self,source):
  super().__init__();self.plan=None;self.capture=False;self.values={};self.inputs={};self.feed(source)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='details' and d.get('class')=='pricing-usage':self.plan=d['data-plan'];self.values[self.plan]=[]
  if tag=='strong' and self.plan:self.capture=True
  if tag=='input' and d.get('id','').startswith('lead-'):self.inputs[d['id']]=d
 def handle_data(self,text):
  if self.capture:self.values[self.plan].append(text)
 def handle_endtag(self,tag):
  if tag=='strong':self.capture=False
  if tag=='details':self.plan=None
for lang in LOCALES:
 text=(ROOT/'dist'/locale_path('/pricing/',lang).lstrip('/')/'index.html').read_text()
 usage=Usage(text)
 assert usage.values['starter']==['1','150','600','250']
 assert usage.values['basic']==[translate(n,lang) for n in ['1','300','1.000','500']]
 assert usage.values['pro']==[translate(n,lang) for n in ['2','500','1.600','800']]
 assert usage.values['premium']==[translate(n,lang) for n in ['3','1.000','3.000','1.500']]
 assert usage.values['enterprise']==[translate('Volum adaptat a mida',lang)]
 for key in ('lead-full-name','lead-email'):assert 'required' in usage.inputs[key]
 for key in ('lead-empresa','lead-telefon'):assert 'required' not in usage.inputs[key]
 assert 'name="missatge"' not in text
 contact=(ROOT/'dist'/locale_path('/contacte/',lang).lstrip('/')/'index.html').read_text()
 assert 'name="missatge"' not in contact
 assert '<input type="checkbox" required' in text
 assert '/pricing.js?' in text
print('PASS: exact usage, custom Enterprise, optional company/phone, required name/email/privacy, no automation question in either form; all locales')
