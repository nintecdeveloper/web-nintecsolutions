"""Generate/check Vercel routing from the existing production SEO policy."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from seo import redirects,PRODUCTION_ORIGIN
from i18n import LOCALES,locale_path

def configuration():
 pages=json.loads((ROOT/'src/pages.json').read_text())
 paths=[locale_path('/' if k=='index' else '/'+k+'/',lang) for k in pages for lang in LOCALES]
 pairs=[line.split()[:2] for line in redirects(paths,True).splitlines() if line.startswith('/')]
 # Host-specific versions first: old paths on the apex go straight to final www.
 apex=[{'type':'host','value':'nintecsolutions.com'}]
 rules=[{'source':old,'destination':PRODUCTION_ORIGIN+new,'statusCode':301,'has':apex} for old,new in pairs]
 rules += [{'source':'/:path*','destination':PRODUCTION_ORIGIN+'/:path*','statusCode':301,'has':apex}]
 rules += [{'source':old,'destination':new,'statusCode':301} for old,new in pairs]
 headers=[{'source':'/(.*)','headers':[{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'},{'key':'Permissions-Policy','value':'camera=(), microphone=(), geolocation=()'}]},
 {'source':'/(.*)','missing':[{'type':'host','value':'www.nintecsolutions.com'}],'headers':[{'key':'X-Robots-Tag','value':'noindex, follow'}]},
 {'source':'/assets/(.*)','headers':[{'key':'Cache-Control','value':'public, max-age=86400'}]}]
 for key,meta in pages.items():
  if not meta.get('indexable',True):
   for lang in LOCALES:
    headers.append({'source':locale_path('/'+key+'/',lang),'headers':[{'key':'X-Robots-Tag','value':'noindex, follow'}]})
 for lang in LOCALES:
  headers.append({'source':locale_path('/',lang)+'404.html','headers':[{'key':'X-Robots-Tag','value':'noindex, follow'}]})
 return {'$schema':'https://openapi.vercel.sh/vercel.json','framework':None,'installCommand':'','buildCommand':'python3 scripts/build_vercel.py','outputDirectory':'dist','cleanUrls':False,'redirects':rules,'headers':headers,'rewrites':[{'source':p,'destination':p+'index.html'} for p in paths]}
if __name__=='__main__':
 config=configuration();path=ROOT/'vercel.json'
 if '--check' in sys.argv:
  assert json.loads(path.read_text())==config,'Vercel configuration drift; run python3 scripts/vercel_config.py'
  print('PASS: Vercel rules match source SEO policy')
 else:path.write_text(json.dumps(config,indent=2)+'\n')
