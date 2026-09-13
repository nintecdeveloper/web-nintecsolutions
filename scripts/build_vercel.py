"""Static Vercel build; the public canonical origin stays fixed in Preview."""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/vercel_config.py'),'--check'],cwd=ROOT,check=True)
env=dict(os.environ)
env['SITE_ORIGIN']='https://www.nintecsolutions.com'
subprocess.run([sys.executable,str(ROOT/'build.py'),'--production'],cwd=ROOT,env=env,check=True)
# Vercel reads vercel.json, not Cloudflare/Netlify control files.
for name in ['_redirects','_headers']:(ROOT/'dist'/name).unlink()
# Protect Preview HTML too, including custom Preview domains; sitemap and SEO URLs stay public.
if os.environ.get('VERCEL_ENV')!='production':
 for path in (ROOT/'dist').rglob('*.html'):
  path.write_text(path.read_text().replace('content="index, follow, max-image-preview:large"','content="noindex, follow"'))
print('PASS: Vercel static output ready; environment='+os.environ.get('VERCEL_ENV','preview (local default)'))
