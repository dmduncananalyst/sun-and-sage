from pathlib import Path
import json
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
for n in paths:
 p=Path(n);s=p.read_bytes().decode('utf-8');s=s.replace('assets/tablet-language.css"','assets/tablet-language.css?v=20261015-folio"');p.write_bytes(s.encode('utf-8'))
print('Versioned the shared stylesheet on all 352 pages to prevent stale preview CSS.')
