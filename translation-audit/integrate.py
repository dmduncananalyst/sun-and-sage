from pathlib import Path
import json,re
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
for name in paths:
 p=Path(name);s=p.read_bytes().decode('utf-8');backup=Path('translation-audit/source-before')/name;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(p.read_bytes())
 # Existing pages use a base element for nested content, or explicit root-relative prefixes.
 prefix='' if re.search(r'<base\b',s) or p.parent==Path('.') else '../'*len(p.parent.parts)
 s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}assets/tablet-language.css"/>\n</head>',1)
 s=s.replace('</body>',f'<script src="{prefix}assets/google-translation.js" defer></script>\n</body>',1)
 p.write_bytes(s.encode('utf-8'))
print('Integrated shared assets on',len(paths),'pages; existing HTML content preserved.')
