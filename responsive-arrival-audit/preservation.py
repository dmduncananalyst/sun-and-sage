from pathlib import Path
import json,re
paths=json.loads(Path('english-restoration-audit/pages.json').read_text());count=0
for n in paths:
 s=Path(n).read_bytes().decode();assert s.count('data-dd-arrival="mode"')==1 and s.count('data-dd-arrival="layout"')==1,n
 clean=re.sub(r'<script data-dd-arrival="(?:mode|layout)">.*?</script>','',s,flags=re.S)
 clean=re.sub(r'<link rel="stylesheet" href="(?:\.\./)*assets/tablet-navigation.css[^\"]*"/>\n','',clean)
 original=(Path('translation-audit/source-before')/n).read_bytes().decode();assert clean==original,n;count+=1
print('PASS:',count,'pages preserve original content outside shared navigation CSS and early responsive initialization.')
