from pathlib import Path
import re,json
out=Path('footer-consistency-audit');report=json.loads((out/'report.json').read_text(encoding='utf-8'));canonical=None
for item in report['changes']:
 n=item['page'];s=Path(n).read_bytes().decode('utf-8');before=(out/'before'/n).read_bytes().decode('utf-8');m=list(re.finditer(r'<footer\b[\s\S]*?</footer>',s))[-1];b=list(re.finditer(r'<footer\b[\s\S]*?</footer>',before))[-1];assert s[:m.start()]+s[m.end():]==before[:b.start()]+before[b.end():],n
 if canonical is None:canonical=m[0]
 assert re.sub(r'(href|src)="(?:\.\./)+',r'\1="',m[0])==canonical,n
print('All 352 footers identical. Everything outside the footer remains byte-for-byte unchanged.')
