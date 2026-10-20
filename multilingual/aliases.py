"""Local-compatible redirects for the canonical blog archive, in every locale."""
import html
from pathlib import Path

def write_aliases(root, listing, languages, origin):
    for language in languages:
        prefix=language+'/' if language!='en' else ''
        for path in listing:
            if not path.startswith('blog-') or '/' in path:continue
            target='../'+path
            destination=Path(root)/prefix/'blog'/path[5:]
            destination.parent.mkdir(parents=True,exist_ok=True)
            canonical=origin+'/'+prefix+path
            destination.write_text('<!doctype html><html lang="'+language+'"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+html.escape(canonical)+'"><meta http-equiv="refresh" content="0;url='+target+'"><title>DommyDom</title></head><body><a href="'+target+'">DommyDom</a><script>location.replace(new URL('+repr(target)+',location.href).href+location.search+location.hash)</script></body></html>',encoding='utf-8')

if __name__=='__main__':
    from .site import ROOT,pages,CONFIG
    write_aliases(ROOT,pages(),['en'],CONFIG['origin'])
