from pathlib import Path
import re,json,shutil
from concurrent.futures import ThreadPoolExecutor
out=Path('buy-menu-chat-refinement-audit');out.mkdir(exist_ok=True)
for n in ['buy-a-home.html','assets/buy-with-dominique.css','assets/dominique-conversation.js','assets/dominique-conversation.css','assets/responsive-navigation.css']:shutil.copy2(n,out/('before-'+Path(n).name))
p=Path('buy-a-home.html');s=p.read_bytes().decode();s,n=re.subn(r'<div class="dd-buy-location">.*?</div>','',s,count=1,flags=re.S);assert n==1;p.write_bytes(s.encode())
p=Path('assets/dominique-conversation.js');s=p.read_text(encoding='utf-8');s=re.sub(r'  const brandLogoUrl = .*?;\n','',s,count=1);s,n=re.subn(r'        <div class="sunConversation__brand">.*?</div>\n','',s,count=1);assert n==1;p.write_text(s,encoding='utf-8')
p=Path('assets/dominique-conversation.css');s=p.read_text(encoding='utf-8');s+='\n/* Keep the existing close control aligned after removing dialog logos. */\n.sunConversation .sunConversation__top{justify-content:flex-end;}\n';p.write_text(s,encoding='utf-8')
paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html'];pattern=r'<div class="dd-feature dd-search"><button class="dd-feature-trigger"[^>]*>(.*?)</button><div class="dd-panel"><div class="dd-panel-content"><a href="([^"]+)">Personalized Home Search</a></div></div></div>'
def update(n):
 p=Path(n);s=p.read_bytes().decode();s,k=re.subn(pattern,lambda m:'<a class="dd-search dd-feature-trigger" href="'+m[2]+'">'+m[1]+'</a>',s,count=1,flags=re.S);assert k==1,n;p.write_bytes(s.encode());return n
with ThreadPoolExecutor(max_workers=8) as pool:changed=list(pool.map(update,paths))
(out/'updated-search-headers.json').write_text(json.dumps(changed,indent=2));print('Removed duplicate Buy block and dialog logos; made Search direct in',len(changed),'headers.')
