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
 assert text.count('data-gift-minutes hidden')==5
 assert text.count('<details>')>=5
 assert 'data-lead-cta' not in text.split('<main')[1].split('</main>')[0]
 for price in ['299 €','499 €','799 €','1.499 €']:assert price in text
 for name in ['starter','basic','pro','premium','enterprise']:assert f'id="{name}"' in text
 for retired in ('equip','finance','compliance'):
  base=locale_path('/'+retired+'/',lang)
  assert not (ROOT/'dist'/base.lstrip('/')).exists()
  for old in (base,base.rstrip('/'),base+'index.html'):assert rules[old]==locale_path('/',lang)
for f in (ROOT/'dist').rglob('*.html'):
 text=f.read_text()
 for forbidden in ('Nintec Finance','Nintec Compliance','home-ecosystem','home-team','/equip/','/finance/','/compliance/'):
  assert forbidden not in text,(f,forbidden)
print('PASS: Pricing translations, contact links, retired routes and absence of removed sections across all public HTML and four languages')
