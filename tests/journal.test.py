"""Four-locale editorial publication, translation completeness and draft isolation."""
from pathlib import Path
from unittest.mock import patch
import html,json,re,sys,subprocess,os,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import journal
from journal_i18n import Translation,source_date
from i18n import LOCALES,locale_path
articles=journal.load_articles(True);images=json.loads((ROOT/'src/journal/images.json').read_text())
assert {str(i) for i in range(1,17)}<={a['id'] for a in articles}
assert len(articles)==len(journal.load_articles())
assert len({a['coverageSlot'] for a in articles if int(a['id'])<=8})==8
for a in articles:
 assert a['status']=='published' and a['datePublished']
 assert sum(len(b['text'].split()) for b in a['body'])>=400
 assert 3<=sum(b['type']=='h2' for b in a['body'])<=5
 assert 2<=len(a['relatedIds'])<=3
 if a['cover']:
  im=images[a['cover']];assert im['rightsStatus']=='verified' and im['sourcePage'].startswith('https://')
  assert im['licenseUrl'].startswith('https://') and im['creator'] and im['caption'] and im['alt']
  for v in im['variants']:assert (ROOT/'src'/v['src'].lstrip('/')).is_file()
assert {a['cover'] for a in articles if a['cover']}<=set(images)
for lang in LOCALES:
 t=Translation(lang,articles,images)
 for a in articles:
  for text in [a[k] for k in ['title','seoTitle','metaDescription','excerpt','context']]+[b['text'] for b in a['body']]:
   translated=t.tr(text);assert translated.strip()
   if lang!='ca':assert translated!=text,(lang,text)
  assert sum(len(t.tr(b['text']).split()) for b in a['body'])>=330,(lang,a['id'])
 if lang!='ca':
  try:t.tr('Un text nou sense traducció')
  except ValueError:pass
  else:raise AssertionError('Missing translation must stop the build')
with tempfile.TemporaryDirectory(prefix='nintec-journal-test-') as tmp:
 preview=Path(tmp)/'preview';prod=Path(tmp)/'production';env={**os.environ,'SITE_ORIGIN':'https://www.nintecsolutions.com'}
 for target,args in [(preview,[]),(prod,['--production'])]:
  subprocess.run([sys.executable,'build.py','--output',str(target),*args],cwd=ROOT,env=env,check=True)
  for lang in LOCALES:
   t=Translation(lang,articles,images)
   for a in articles:
    path=locale_path(journal.url(a),lang);doc=(target/path.lstrip('/')/'index.html').read_text()
    assert f'<html lang="{lang}">' in doc and doc.count('<h1>')==1
    assert f'rel="canonical" href="https://www.nintecsolutions.com{path}"' in doc
    assert 'content="'+('index, follow, max-image-preview:large' if target==prod else 'noindex, follow')+'"' in doc
    for l in LOCALES:
     equiv=locale_path(journal.url(a),l)
     assert f'hreflang="{l}" href="https://www.nintecsolutions.com{equiv}"' in doc
     assert f'href="{equiv}?lang={l}"' in doc
    for b in a['body']:assert html.escape(t.tr(b['text']),quote=False) in doc
    for source in a['sources']:
     assert source_date(source,lang) in doc
     assert html.escape(source['url'],quote=True) in doc
    if a.get('eventDateLabel'):assert t.tr(a['eventDateLabel']) in doc
    schemas=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',doc)[1]);schema=schemas[0]
    assert schema['headline']==t.tr(a['title']) and schema['inLanguage']==lang and schema['datePublished']==a['datePublished']
    assert schema['url']=='https://www.nintecsolutions.com'+path
    assert schemas[1]['@type']=='BreadcrumbList'
    assert 'JOURNAL_BOOTSTRAP' not in doc and 'JOURNAL_SCHEMA' not in doc
    messages=json.loads(re.search(r'id="i18n-messages">(.*?)</script>',doc)[1]);assert messages
   dates=re.findall(r'<time datetime="([^"]+)">',(target/locale_path('/blog/arxiu/',lang).lstrip('/')/'index.html').read_text())
   assert dates==sorted([a['eventDate'] for a in articles],reverse=True)
  assert len(list(target.rglob('index.html')))==32+len(journal.paths(articles))
  ca_home=(target/'blog/index.html').read_text()
  opening=ca_home.split('class="j-opening">',1)[1].split('</section>',1)[0]
  assert opening.index('mistral-large-4-control-ia-europa')<opening.index('google-respostes-ia-clics-web')<opening.index('gemini-robotics-ia-mon-fisic')
  assert 'Les últimes tres setmanes' not in ca_home
  subprocess.run([sys.executable,'tests/validate.py',str(target)],cwd=ROOT,check=True)
 assert '<loc>' not in (preview/'sitemap.xml').read_text()
 assert len(ET.parse(prod/'sitemap.xml').findall('.//{*}loc'))==20+len(journal.paths(articles))
 refused=subprocess.run([sys.executable,'build.py','--production','--journal-preview','--output',str(Path(tmp)/'unsafe')],cwd=ROOT,env=env,capture_output=True)
 assert refused.returncode!=0 and not (Path(tmp)/'unsafe').exists()
 # Test draft exclusion on an isolated content fixture, never the working source.
 fixture=Path(tmp)/'fixture';content=fixture/'src/journal/content';content.mkdir(parents=True)
 for a in articles:
  a=dict(a)
  if a['id']=='1':a['status']='draft';a['datePublished']=None
  (content/(a['id']+'.json')).write_text(json.dumps(a))
 with patch.object(journal,'ROOT',fixture):
  assert len(journal.load_articles())==len(articles)-1 and len(journal.load_articles(True))==len(articles)
  assert not any('claude-sonnet' in p for p in journal.paths(journal.load_articles()))
print(f'PASS: {4*len(articles)} complete article editions, {len(journal.paths(articles))} Journal routes, four-locale selectors/SEO/schema, source dates, licensed images, publication order and draft exclusion')
