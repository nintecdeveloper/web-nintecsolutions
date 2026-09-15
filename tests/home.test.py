"""Corporate home and product must keep distinct responsibilities in every locale."""
from pathlib import Path
from html.parser import HTMLParser
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from i18n import LOCALES,locale_path
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.sections=[];self.links=[];self.cycle=False;self.ids=set();self.steps=0;self.in_steps=False;self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='section':self.sections.append(d.get('class',''))
  if t=='a':self.links.append(d.get('href'))
  if 'data-cycle' in d:self.cycle=True
  if 'id' in d:self.ids.add(d['id'])
  if t=='ol' and d.get('class')=='home-journey':self.in_steps=True
  if t=='li' and self.in_steps:self.steps+=1
 def handle_endtag(self,t):
  if t=='ol':self.in_steps=False
expected=['corporate-hero','home-bridge','home-concept','home-capabilities','proof-section','home-ecosystem','home-team','cta-section']
for lang in LOCALES:
 root=ROOT/'dist'/locale_path('/',lang).lstrip('/')
 home=Page((root/'index.html').read_text());product=Page((root/'nintec360/index.html').read_text())
 assert len(home.sections)==8
 assert all(key in section.split() for key,section in zip(expected,home.sections))
 assert home.steps==4 and not home.cycle and product.cycle
 assert {'control','campanyes','regles','adaptacio','canals','seguretat'}<=product.ids
 assert not {'control','regles','adaptacio','canals','seguretat'}&home.ids
 for path in ['/nintec360/','/finance/','/compliance/','/equip/','/contacte/','/casos/']:
  assert locale_path(path,lang) in home.links
 assert 'campaign-section' not in ' '.join(home.sections)
 assert all(f'nintec360-tab-{i}' in product.ids for i in range(7))
print('PASS: corporate hierarchy, four conceptual steps, product deep sections and six-stage cycle, four locales, solution links')
