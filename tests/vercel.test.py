"""Validate both Vercel build modes and routing contracts, without deploying."""
import json,os,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from seo import WIX_ALIASES,LEGACY_ALIASES,PRODUCTION_ORIGIN
config=json.loads((ROOT/'vercel.json').read_text());out=ROOT/'dist'
assert config['framework'] is None and config['outputDirectory']=='dist'
assert 'routes' not in config and not config.get('trailingSlash')
# No catch-all rewrite can turn missing pages into a 200 response.
assert len(config['rewrites'])==40
assert not any('*' in r['source'] or '(' in r['source'] for r in config['rewrites'])
for env_name in ['preview','production']:
 env={**os.environ,'VERCEL_ENV':env_name}
 subprocess.run([sys.executable,'scripts/build_vercel.py'],cwd=ROOT,env=env,check=True)
 subprocess.run([sys.executable,'tests/validate.py'],cwd=ROOT,check=True)
 for r in config['rewrites']:
  f=out/r['destination'].lstrip('/');assert f.is_file()
  html=f.read_text();assert f'rel="canonical" href="{PRODUCTION_ORIGIN}{r["source"]}"' in html
  if env_name=='preview':assert 'content="noindex, follow"' in html
 assert (out/'404.html').is_file() and 'noindex, follow' in (out/'404.html').read_text()
 assert len(ET.parse(out/'sitemap.xml').findall('.//{*}loc'))==28
 assert 'Sitemap: '+PRODUCTION_ORIGIN+'/sitemap.xml' in (out/'robots.txt').read_text()
 assert not (out/'_redirects').exists() and not (out/'_headers').exists()
 for source,target in {**LEGACY_ALIASES,**WIX_ALIASES}.items():
  for old in ['/'+source]+([] if source.endswith('.html') else ['/'+source+'/']):
   matches=[r for r in config['redirects'] if r['source']==old and not r.get('has')]
   assert len(matches)==1 and matches[0]['destination']==target and matches[0]['statusCode']==301
   assert (out/urlsplit(target).path.lstrip('/')/'index.html').is_file()
 apex=[r for r in config['redirects'] if r['source']=='/:path*'][0]
 assert apex['has']==[{'type':'host','value':'nintecsolutions.com'}]
 assert apex['destination']==PRODUCTION_ORIGIN+'/:path*' and apex['statusCode']==301
 assert not any(r['source']==r['destination'] for r in config['redirects'])
 print('PASS:',env_name,'40 static routes; public SEO origin; noindex policy; native 404 file; legacy redirects; sitemap/robots')
# Environment and secret paths are ignored even in nested directories.
for name in ['.env','.env.local','.env.production','src/.env.local','credentials.json','private/customer.csv','secrets/key','auth.pem','.vercel/project.json']:
 assert subprocess.run(['git','check-ignore','-q',name],cwd=ROOT).returncode==0,name
print('PASS: private-file ignore rules')
