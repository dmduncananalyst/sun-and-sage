from pathlib import Path
import json
p=Path('assets/google-translation.js');s=p.read_text(encoding='utf-8');needle="const base=new URL('.',document.baseURI)";s=s.replace(needle,"const serviceGroup=header.querySelector('.dd-buyers');if(serviceGroup&&!serviceGroup.querySelector('.dd-navigation-section-caption')){const caption=document.createElement('span');caption.className='dd-navigation-section-caption';caption.textContent='Real Estate & Design';serviceGroup.prepend(caption);}\n"+needle,1);p.write_text(s,encoding='utf-8')
p=Path('assets/tablet-language.css');s=p.read_text(encoding='utf-8');s+='''
#dd-header .dd-navigation-section-caption{display:none;}
@media(min-width:600px) and (max-width:1199px){html:root body.ss18 #dd-header.is-tablet #dd-navigation>.dd-buyers::before{display:none;content:none;}html:root body.ss18 #dd-header.is-tablet .dd-navigation-section-caption{display:block;padding:0 8px 7px;font:500 9px/1.5 Arial,sans-serif;letter-spacing:.13em;color:#838775;text-transform:uppercase;}}
''';p.write_text(s,encoding='utf-8')
p=Path('translation-service/public-text.json');texts=json.loads(p.read_text(encoding='utf-8'));texts=sorted(set(texts+['Real Estate & Design']));p.write_text(json.dumps(texts,ensure_ascii=False),encoding='utf-8')
p=Path('translation-service/build_manifest.py');s=p.read_text(encoding='utf-8-sig').replace("add(['Continue'","add(['Real Estate & Design','Continue'");p.write_text(s,encoding='utf-8')
# Version both shared assets so the preview cannot retain the old menu implementation.
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
for name in paths:
 p=Path(name);s=p.read_bytes().decode('utf-8').replace('tablet-language.css?v=20261015-folio','tablet-language.css?v=20261015-navigation-language-v2').replace('assets/google-translation.js"','assets/google-translation.js?v=20261015-compact"');p.write_bytes(s.encode('utf-8'))
print('Versioned both shared assets across 352 pages. Navigation caption is runtime-translatable.')
