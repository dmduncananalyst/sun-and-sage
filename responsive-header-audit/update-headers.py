from pathlib import Path
import json,re
out=Path('responsive-header-audit');records=json.loads((out/'headers-before.json').read_text())
for r in records:
 p=Path(r['page']);s=p.read_bytes().decode();h=r['oldHeader'];updated=h.replace('ss22-','dd-').replace('ddn-contact-strip','dd-contact-strip').replace('ddn-wordmark','dd-signature-image');assert s.count(h)==1;p.write_bytes(s.replace(h,updated,1).encode())
p=Path('assets/home-hero-fit.js');s=p.read_text(encoding='utf-8-sig');assert "getElementById('ss22-header')" in s;p.write_text(s.replace("getElementById('ss22-header')","getElementById('dd-header')"),encoding='utf-8');print('Isolated',len(records),'headers; retained the existing hero header-height measurement.')
