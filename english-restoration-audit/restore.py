from pathlib import Path
import re,json,shutil
root=Path.cwd(); out=root/'english-restoration-audit'; recovery=out/'removed-project-files';recovery.mkdir(exist_ok=True)
css=Path('assets/tablet-language.css').read_text(encoding='utf-8')
# Retain the entire navigation cascade, including its current proportions and interactions.
def filter_css(src):
 src=re.sub(r'/\*.*?\*/','',src,flags=re.S); result='';pos=0
 while pos<len(src):
  start=src.find('{',pos)
  if start<0:break
  header=src[pos:start].strip();depth=1;i=start+1
  while depth:
   if src[i]=='{':depth+=1
   elif src[i]=='}':depth-=1
   i+=1
  body=src[start+1:i-1]
  if header.startswith('@media'):
   body=filter_css(body)
   if body.strip():result+=header+'{\n'+body+'}\n'
  elif not any(x in header for x in ['dd-language','dd-translation','dd-translated','dd-homepage-language','dd-home-ai']):result+=header+'{'+body+'}\n'
  pos=i
 return result
nav=filter_css(css)
nav+='\n/* Match the existing Neighborhoods dropdown font; tablet main labels only. */\n@media(min-width:600px) and (max-width:1199px){\nhtml:root body.ss18 #dd-header.is-tablet #dd-navigation>a,html:root body.ss18 #dd-header.is-tablet #dd-navigation>.dd-group>a,html:root body.ss18 #dd-header.is-tablet #dd-navigation>a[aria-current=page],html:root body.ss18 #dd-header.is-tablet #dd-navigation>.dd-group>a[aria-current=page],html:root body.ss18 #dd-header.is-tablet #dd-navigation>.dd-group.is-open>a{font-family:Arial,Helvetica,sans-serif!important;}\n}\n'
Path('assets/tablet-navigation.css').write_text('/* Preserved approved navigation styling. English-only. */\n'+nav,encoding='utf-8')
paths=json.loads((out/'pages.json').read_text())
for n in paths:
 p=Path(n);s=p.read_bytes().decode('utf-8');s=s.replace('assets/tablet-language.css?v=20261015-navigation-language-v2','assets/tablet-navigation.css?v=20261015-english')
 s=re.sub(r'<script src="(?:\.\./)*assets/(?:google-translation|homepage-ai-chat).js[^\"]*" defer></script>\r?\n','',s)
 assert 'tablet-language.css' not in s,n
 p.write_bytes(s.encode('utf-8'))
shutil.copy2('assets/dominique-conversation.js',out/'before-restoration-conversation.js')
Path('assets/dominique-conversation.js').write_bytes(Path('final-nine-language-audit/before-dominique-conversation.js').read_bytes())
removed=[]
for n in ['assets/tablet-language.css','assets/google-translation.js','assets/translation-config.json','assets/google-translate-attribution.png','assets/homepage-chat-ui.json','assets/homepage-ai-chat.js','assets/homepage-locales','homepage-service','translation-service']:
 source=(root/n).resolve(); assert source.is_relative_to(root)
 if source.exists():
  target=recovery/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(source),str(target));removed.append(n)
(out/'removed-files.json').write_text(json.dumps(removed,indent=2))
print('Restored original chat script; removed project includes from 352 pages; archived inactive project files; retained navigation cascade with tablet font-family correction only.')
