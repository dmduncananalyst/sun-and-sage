"""Read-only inventory and whole-site rendering smoke test; no Google API calls.

Synthetic strings test the renderer only. They are never saved as translations.
"""
import json
import re
from .site import ROOT,CONFIG,inventory,key,render
from .cloud import cost_units

def main():
    listing,texts=inventory()
    cache=json.loads((ROOT/'multilingual/translations.json').read_text(encoding='utf-8'))
    missing={lang:sum(key(text,lang) not in cache for text in texts) for lang in CONFIG['languages'] if lang!='en'}
    complete=not any(missing.values())
    smoke=cache if complete else {key(text,lang):f'[{lang}] '+text for lang in CONFIG['languages'] if lang!='en' for text in texts}
    checked=0
    for path in listing:
        source=(ROOT/path).read_text(encoding='utf-8')
        for lang in CONFIG['languages']:
            output=render(source,path,lang,smoke,listing)
            assert output.count('hreflang=')==11,(path,lang,'hreflang')
            assert output.count('rel="canonical"')==1,(path,lang,'canonical')
            assert re.search(r'<html\b[^>]*\blang="'+re.escape(lang)+'"',output),(path,lang,'html language')
            checked+=1
    connection=json.loads((ROOT/'multilingual/cloud-status.json').read_text()) if (ROOT/'multilingual/cloud-status.json').exists() else {}
    generation=json.loads((ROOT/'multilingual/local-generation-report.json').read_text()) if (ROOT/'multilingual/local-generation-report.json').exists() else {}
    report={'english_pages':len(listing),'english_blogs':sum(p.startswith('blog-') for p in listing),'unique_source_segments':len(texts),'source_characters_per_language':sum(map(len,texts)),'real_saved_translation_segments':len(cache),'missing_segments_by_language':missing,'saved_translation_render_checks_passed':checked if complete else 0,'synthetic_render_checks_passed':0 if complete else checked,'synthetic_text_saved':False,'google_cloud_authenticated':connection.get('authenticated',False),'real_translation_coverage_complete':complete,'linguistic_review_by_native_speakers':False,'end_to_end_call_verified':False,'translation_api_requests':generation.get('requests',0),'local_only':True,'published':False}
    (ROOT/'multilingual/verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
