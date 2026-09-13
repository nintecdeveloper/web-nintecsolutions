"""Check tracked files and all reachable Git blobs without printing secret values."""
import base64,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
patterns=[('private-key',r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----'),('provider-secret',r'\b(?:sb_secret_|sk_live_|sk_test_|ghp_|gho_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{16,}'),('aws-access',r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),('google-api',r'\bAIza[A-Za-z0-9_-]{30,}'),('secret-assignment',r'''(?i)(?:service_role_key|service_role|private_key|client_secret|access_token|refresh_token|vercel_token|github_token|api_secret)\s*["']?\s*[:=]\s*["']([A-Za-z0-9_./+=-]{20,})["']''')]
issues=[];count=0

def scan(label,data):
 global count
 count+=1
 if b'\0' in data:return
 text=data.decode('utf-8',errors='replace')
 for name,pattern in patterns:
  if re.search(pattern,text):issues.append((label,name))
 for token in re.findall(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',text):
  try:
   part=token.split('.')[1];payload=json.loads(base64.urlsafe_b64decode(part+'='*((-len(part))%4)))
   if payload.get('role')!='anon':issues.append((label,'non-anonymous JWT'))
  except Exception:issues.append((label,'unclassified JWT'))
 for url in re.findall(r'https?://[^\s"<>]+',text):
  if re.search(r'https?://[^/@\s]+:[^/@\s]+@',url):issues.append((label,'credential in URL'))
paths=git('ls-files','-z').decode().split('\0')
for name in filter(None,paths):
 if any(p.startswith('.env') or p in ['.git-credentials','.netrc','credentials.json'] for p in Path(name).parts):issues.append((name,'tracked private filename'))
 p=ROOT/name
 if p.is_file():scan(name,p.read_bytes())
# Read every unique reachable blob, including files deleted from the current tree.
objects=git('rev-list','--objects','--all').splitlines()
for entry in objects:
 oid=entry.split(b' ',1)[0].decode()
 if git('cat-file','-t',oid).strip()==b'blob':scan('history:'+oid[:12],git('cat-file','blob',oid))
# Also inspect new files intended for the next commit, excluding ignored local files.
for name in filter(None,git('ls-files','--others','--exclude-standard','-z').decode().split('\0')):
 p=ROOT/name
 if p.is_file():scan(name,p.read_bytes())
if issues:
 for label,kind in sorted(set(issues)):print('FAIL:',label,kind)
 sys.exit(1)
print(f'PASS: {count} tracked/new files and historical blobs checked; no matching sensitive credentials. Public Supabase publishable/anon configuration is not a private key.')
