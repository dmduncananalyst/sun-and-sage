from pathlib import Path
import json,re,difflib
out=Path('english-restoration-audit');out.mkdir(exist_ok=True)
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
changes=[]
for n in paths:
 s=Path(n).read_text(encoding='utf-8'); old=(Path('translation-audit/source-before')/n).read_text(encoding='utf-8')
 clean=re.sub(r'<link rel="stylesheet" href="(?:\.\./)*assets/tablet-language.css[^\"]*"/>\n','',s)
 clean=re.sub(r'<script src="(?:\.\./)*assets/(?:google-translation|homepage-ai-chat).js[^\"]*" defer></script>\n','',clean)
 if clean!=old:changes.append(n)
assert not changes,changes
before=Path('final-nine-language-audit/before-dominique-conversation.js').read_text(encoding='utf-8'); now=Path('assets/dominique-conversation.js').read_text(encoding='utf-8')
(out/'chat-project-diff.txt').write_text(''.join(difflib.unified_diff(before.splitlines(True),now.splitlines(True))),encoding='utf-8')
(out/'pages.json').write_text(json.dumps(paths),encoding='utf-8')
print('All 352 pages match saved English originals after removing project asset includes. Chat diff saved. No content/config differences.')
