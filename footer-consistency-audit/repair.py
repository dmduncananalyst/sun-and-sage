from pathlib import Path
import re,json,hashlib,os
out=Path('footer-consistency-audit');out.mkdir(exist_ok=True)
paths=list(dict.fromkeys(json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']))
canonical=list(re.finditer(r'<footer\b[\s\S]*?</footer>',Path('index.html').read_bytes().decode('utf-8')))[-1][0];canonical=canonical.replace('<footer class="ss22-footer">','<footer class="ss22-footer" id="dd-site-footer">')
groups={};report=[]
for n in paths:
 p=Path(n);s=p.read_bytes().decode('utf-8');matches=list(re.finditer(r'<footer\b[\s\S]*?</footer>',s));assert matches,n;m=matches[-1];old=m[0];key=hashlib.sha256(old.encode()).hexdigest();groups.setdefault(key,[]).append(n)
 f=canonical
 if p.parent!=Path('.') and not re.search(r'<base\b',s):
  prefix=os.path.relpath(Path.cwd(),p.parent.resolve()).replace('\\','/')+'/'
  f=re.sub(r'(href|src)="(?!https?:|tel:|mailto:|#)([^"]+)"',lambda m:m[1]+'="'+prefix+m[2]+'"',f)
 backup=out/'before'/n;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(s.encode('utf-8'))
 s=s[:m.start()]+f+s[m.end():];p.write_bytes(s.encode('utf-8'));report.append({'page':n,'changed':old!=f})
(out/'report.json').write_text(json.dumps({'pages':len(paths),'prior_variants':groups,'changes':report},indent=2),encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8');s+='''
/* One shared footer composition across every page, isolated from page skins. */
html:root body.ss18 footer#dd-site-footer#dd-site-footer{display:block!important;width:100%!important;max-width:none!important;box-sizing:border-box!important;margin:0!important;padding:44px max(24px,calc((100% - 1440px)/2)) 0!important;background:#48533e!important;color:#fff!important;font:400 14px/1.7 Arial,sans-serif!important;}
html:root body.ss18 #dd-site-footer .footerGrid{display:grid!important;grid-template-columns:1.25fr 1fr!important;gap:40px!important;max-width:1440px!important;margin:0 auto!important;padding:0 0 36px!important;}
html:root body.ss18 #dd-site-footer .footerGrid>section{margin:0!important;padding:0!important;border:0!important;background:transparent!important;}
html:root body.ss18 #dd-site-footer h3{font:400 24px/1.4 Arial,sans-serif!important;color:#fff!important;margin:0 0 20px!important;text-align:left!important;}
html:root body.ss18 #dd-site-footer a{color:inherit!important;background:transparent!important;box-shadow:none!important;transform:none!important;font:inherit!important;text-transform:none!important;letter-spacing:normal!important;}
html:root body.ss18 #dd-site-footer .cityLinks{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:4px 20px!important;}
html:root body.ss18 #dd-site-footer .cityLinks a{font-size:13px!important;min-height:30px!important;display:flex!important;align-items:center!important;padding:0!important;text-decoration:none!important;}
html:root body.ss18 #dd-site-footer .footerGrid>.direct{border-left:1px solid #ffffff38!important;padding-left:40px!important;text-align:center!important;}
html:root body.ss18 #dd-site-footer .direct h3{text-align:center!important;}
html:root body.ss18 #dd-site-footer .ddn-contact-lockup{display:flex!important;flex-direction:column!important;align-items:center!important;gap:5px!important;}
html:root body.ss18 #dd-site-footer .ddn-contact-lockup strong{font:500 19px/1.5 Arial,sans-serif!important;}
html:root body.ss18 #dd-site-footer .ddn-phone-pair{display:flex!important;justify-content:center!important;gap:20px!important;flex-wrap:wrap!important;}
html:root body.ss18 #dd-site-footer .legal{display:flex!important;align-items:center!important;justify-content:center!important;flex-wrap:wrap!important;gap:18px!important;margin:0 calc(-1 * max(24px,calc((100vw - 1440px)/2)))!important;padding:24px!important;background:#fff!important;color:#343c32!important;font:400 11px/1.6 Arial,sans-serif!important;text-align:center!important;}
html:root body.ss18 #dd-site-footer .legal img{display:block!important;object-fit:contain!important;height:auto!important;max-height:70px!important;margin:0!important;}
html:root body.ss18 #dd-site-footer .legal .riseFooter{width:120px!important;}
html:root body.ss18 #dd-site-footer .legal .complianceMarks{width:120px!important;}
@media(max-width:700px){html:root body.ss18 #dd-site-footer .footerGrid{grid-template-columns:1fr!important;gap:28px!important;}html:root body.ss18 #dd-site-footer .footerGrid>.direct{border-left:0!important;border-top:1px solid #ffffff38!important;padding:28px 0 0!important;}html:root body.ss18 #dd-site-footer .cityLinks{grid-template-columns:repeat(2,minmax(0,1fr))!important;}html:root body.ss18 #dd-site-footer .cityLinks a{min-height:40px!important;}}
''';p.write_text(s,encoding='utf-8');print('Standardized',len(paths),'page footers; prior variants:',len(groups))
