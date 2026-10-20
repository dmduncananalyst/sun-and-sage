"""Integrate the saved multilingual site into the actual website checkout locally."""
import json
from pathlib import Path
import shutil
from .site import ROOT,CONFIG,pages,integration,strip_integration,place_selector,build,set_html_language,copy_if_changed

def install(root=ROOT):
    cache=json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
    listing=pages(root)
    backup=root/'.translation-state/source-before-language-selector'
    for path in listing:
        target=root/path;source=target.read_text(encoding='utf-8')
        saved=backup/path;saved.parent.mkdir(exist_ok=True,parents=True)
        if not saved.exists():saved.write_text(source,encoding='utf-8')
        source=set_html_language(strip_integration(source),'en')
        # Explicit document root keeps source pages usable from both a local
        # HTTP server and an index.html opened directly from Explorer.
        import re
        prefix='../'*path.count('/') or './'
        source=re.sub(r'<base\b[^>]*href=["\']/["\'][^>]*>',f'<base href="{prefix}">',source,flags=re.I)
        if not re.search(r'<base\b',source,re.I):
            source=re.sub(r'<head\b[^>]*>',lambda m:m[0]+f'<base href="{prefix}">',source,count=1,flags=re.I)
        else:
            base=re.search(r'<base\b[^>]*>',source,re.I)[0]
            source=re.sub(r'<base\b[^>]*>','',source,flags=re.I)
            source=re.sub(r'<head\b[^>]*>',lambda m:m[0]+base,source,count=1,flags=re.I)
        head,selector=integration(path,'en',cache)
        if '</head>' not in source:raise RuntimeError('Missing head: '+path)
        updated=place_selector(source.replace('</head>',head+'</head>',1),selector)
        if updated!=target.read_text(encoding='utf-8'):target.write_text(updated,encoding='utf-8')
    print(f'Installed visible language selector in {len(listing)} English website pages, including index.html.',flush=True)
    result=build(root)
    shutil.copytree(root/'dist/blog',root/'blog',dirs_exist_ok=True,copy_function=copy_if_changed)
    for lang in CONFIG['languages']:
        if lang=='en':continue
        destination=root/lang
        if destination.exists() and not (destination/'index.html').exists():raise RuntimeError('Unexpected existing language directory: '+lang)
        shutil.copytree(root/'dist'/lang,destination,dirs_exist_ok=True,copy_function=copy_if_changed)
    shutil.copytree(root/'dist/assets/locales',root/'assets/locales',dirs_exist_ok=True,copy_function=copy_if_changed)
    for source in (root/'dist').glob('sitemap*.xml'):shutil.copy2(source,root/source.name)
    report={'english_source_pages_integrated':len(listing),'root_language_directories':[x for x in CONFIG['languages'] if x!='en'],'saved_translations':len(cache),'local_only':True,'published':False,'committed':False}
    (root/'multilingual/source-integration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':install()
