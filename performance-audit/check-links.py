import json,urllib.request,concurrent.futures,re,time
from pathlib import Path
root=Path.cwd();data=json.loads((root/'performance-audit/inventory.json').read_text());urls=sorted({a['url'] for r in data['references'] for a in r['links'] if a['url'].startswith('https://')})
def check(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; website link audit)'})
  with urllib.request.urlopen(req,timeout=20) as res:
   text=res.read(180000).decode('utf-8',errors='replace');title=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
   return {'url':url,'status':res.status,'destination':res.url,'title':re.sub(r'\s+',' ',title[1]).strip() if title else '', 'content_type':res.headers.get('Content-Type')}
 except Exception as e:return {'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: results=list(pool.map(check,urls))
(root/'performance-audit/link-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
