"""Read-only inventory and whole-site rendering smoke test; no Google API calls.

Synthetic strings test the renderer only. They are never saved as translations.
"""
import json
from .site import ROOT,CONFIG,inventory,key,render
from .cloud import cost_units

def main():
    listing,texts=inventory()
    cache=json.loads((ROOT/'multilingual/translations.json').read_text(encoding='utf-8'))
    smoke={key(text,lang):f'[{lang}] '+text for lang in CONFIG['languages'] if lang!='en' for text in texts}
    checked=0
    for path in listing:
        source=(ROOT/path).read_text(encoding='utf-8')
        for lang in CONFIG['languages']:
            output=render(source,path,lang,smoke,listing)
            assert output.count('hreflang=')==11,(path,lang,'hreflang')
            assert output.count('rel="canonical"')==1,(path,lang,'canonical')
            assert f'<html lang="{lang}"' in output,(path,lang,'html language')
            checked+=1
    missing={lang:sum(key(text,lang) not in cache for text in texts) for lang in CONFIG['languages'] if lang!='en'}
    report={'english_pages':len(listing),'english_blogs':sum(p.startswith('blog-') for p in listing),'unique_source_segments':len(texts),'source_characters_per_language':sum(map(len,texts)),'maximum_initial_nmt_usd_before_credits':sum(cost_units(len(t)) for t in texts)*9/1_000_000,'real_saved_translation_segments':len(cache),'missing_segments_by_language':missing,'synthetic_render_checks_passed':checked,'synthetic_text_saved':False,'google_cloud_authenticated':False,'real_translation_verified':False,'end_to_end_call_verified':False,'paid_requests_made':0,'monthly_translation_limit_usd':CONFIG['monthly_limit_usd']}
    (ROOT/'multilingual/verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
