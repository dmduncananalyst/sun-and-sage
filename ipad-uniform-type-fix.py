from pathlib import Path
import json
out=Path('ipad-uniform-type-audit');out.mkdir(exist_ok=True)
p=Path('assets/tablet-navigation.css');s=p.read_text();(out/'before-tablet-navigation.css').write_bytes(p.read_bytes())
s=s.split('/* Match the existing Neighborhoods dropdown font; tablet main labels only. */')[0]
s+='''/* One consistent type treatment for every tablet navigation label, matching Sell With Dominique. */
@media(min-width:600px) and (max-width:1199px){
 html:root body.ss18 #dd-header.is-tablet #dd-navigation#dd-navigation#dd-navigation a{
  font:400 13px/1.5 Arial,sans-serif!important;
  letter-spacing:0!important;
  text-transform:none!important;
 }
}
'''
p.write_text(s,encoding='utf-8')
for n in json.loads(Path('english-restoration-audit/pages.json').read_text()):
 p=Path(n);s=p.read_bytes();s=s.replace(b'tablet-navigation.css?v=20261015-english',b'tablet-navigation.css?v=20261015-uniform-type');p.write_bytes(s)
