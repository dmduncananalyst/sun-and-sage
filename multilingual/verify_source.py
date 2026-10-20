"""Verify selectors and saved language routes in the actual website source tree."""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from .site import ROOT,CONFIG,pages,inventory,key

def main():
    print('Checking source inventory and saved translations...',flush=True)
    listing,texts=inventory()
    cache=json.loads((ROOT/'multilingual/translations.json').read_text(encoding='utf-8'))
    checked=0
    for language in CONFIG['languages']:
        def read(path):
            return path,(ROOT/(language if language!='en' else '')/path).read_text(encoding='utf-8')
        with ThreadPoolExecutor(max_workers=16) as pool: sources=list(pool.map(read,listing))
        for path,source in sources:
            assert source.count('id="dd-language"')==1,(language,path,'visible selector')
            assert source.count('id="dommydom-locale"')==1,(language,path,'configuration')
            assert re.search(r'<a\b[^>]*class=["\'][^"\']*\bdd-search\b[^"\']*["\'][^>]*>.*?</a>\s*<!-- dommydom-i18n:selector:start -->',source,re.S),(language,path,'selector immediately beside Search')
            selector=re.search(r'<select id="dd-language".*?</select>',source,re.S)
            assert selector and selector[0].count('<option ')==10,(language,path,'language choices')
            cfg=re.search(r'<script id="dommydom-locale" type="application/json">(.*?)</script>',source,re.S)
            assert cfg and json.loads(cfg[1])['language']==language,(language,path,'correct language')
            checked+=1
        print(f'Checked {language}: {len(listing)} source pages',flush=True)
    missing={lang:sum(key(t,lang) not in cache for t in texts) for lang in CONFIG['languages'] if lang!='en'}
    assert not any(missing.values()),missing
    for lang in CONFIG['languages']:
        assert (ROOT/f'sitemap-{lang}.xml').exists(),lang
        if lang!='en':assert (ROOT/f'assets/locales/{lang}.js').exists(),lang
    report={'actual_website_source':True,'english_pages_with_visible_selector':len(listing),'language_pages_checked':checked,'language_choices':10,'missing_saved_segments':missing,'local_only':True,'published':False}
    (ROOT/'multilingual/source-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
