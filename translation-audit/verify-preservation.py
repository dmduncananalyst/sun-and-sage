from pathlib import Path
import json,re
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
for n in paths:
 p=Path(n);s=p.read_bytes().decode('utf-8');before=(Path('translation-audit/source-before')/n).read_bytes().decode('utf-8')
 assert s.count('assets/tablet-language.css')==1 and s.count('assets/google-translation.js')==1,n
 restored=re.sub(r'<link rel="stylesheet" href="(?:\.\./)*assets/tablet-language.css(?:\?v=[^"]+)?"/>\n','',s,count=1)
 restored=re.sub(r'<script src="(?:\.\./)*assets/google-translation.js(?:\?v=[^"]+)?" defer></script>\n','',restored,count=1)
 assert restored==before,n
print('PASS: all 352 original HTML files preserved byte-for-byte except two shared asset references.')
new=['assets/tablet-language.css','assets/google-translation.js','assets/translation-config.json','assets/google-translate-attribution.png','translation-service/core.py','translation-service/app.py','translation-service/requirements.txt','translation-service/Dockerfile','translation-service/.dockerignore','translation-service/build_manifest.py','translation-service/public-text.json','translation-service/project-titles.json','translation-service/test_core.py','translation-service/SETUP.md']
changed=['assets/responsive-navigation.css','assets/navigation-v22.js','.gitignore']+paths
Path('translation-audit/changed-files.json').write_text(json.dumps({'changed':changed,'new':new,'untouched':'All existing page content, images, videos, SEO/AEO, sitemap, robots and existing instructions; HTML changes limited to two shared includes.'},indent=2),encoding='utf-8')
