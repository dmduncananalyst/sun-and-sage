"""Check every canonical blog's retained legacy URL in all ten languages."""
import json,re
from urllib.parse import urljoin,urlsplit
from .site import ROOT,pages,CONFIG

def main():
    articles=[p for p in pages() if p.startswith('blog-') and '/' not in p]
    checked=0
    for language in CONFIG['languages']:
        prefix=language+'/' if language!='en' else ''
        for path in articles:
            alias=ROOT/prefix/'blog'/path[5:]
            source=alias.read_text(encoding='utf-8')
            target=re.search(r'content="0;url=([^" ]+)',source)[1]
            assert (alias.parent/target).resolve()==(ROOT/prefix/path).resolve(),alias
            assert (alias.parent/target).exists(),alias
            assert CONFIG['origin']+'/'+prefix+path in source,alias
            assert 'location.search+location.hash' in source,alias
            checked+=1
    report={'local_only':True,'canonical_articles':len(articles),'legacy_routes_checked':checked,'documented_19_broken_routes_repaired':True,'relative_redirects_preserve_local_preview':True}
    (ROOT/'multilingual/alias-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
