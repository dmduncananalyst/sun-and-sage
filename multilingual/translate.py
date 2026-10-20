"""Explicit paid build operation. Never imported into browser code."""
import json
import os
from .cloud import Cloud, cost_units
from .site import ROOT, CONFIG, inventory, key

def main():
    if os.environ.get('DOMMYDOM_ALLOW_PAID_TRANSLATION')!='true':
        raise RuntimeError('Paid translation disabled; access, baseline and safeguards must be verified first')
    cloud=Cloud();cloud.preflight()
    listing,texts=inventory()
    path=ROOT/'multilingual/translations.json'
    cache=json.loads(path.read_text(encoding='utf-8'))
    missing=[(language,text) for language in CONFIG['languages'] if language!='en' for text in texts if key(text,language) not in cache]
    print(json.dumps({'pages':len(listing),'missing':len(missing),'maximum_additional_usd':sum(cost_units(len(t)) for _,t in missing)/1_000_000}))
    for language,text in missing:
        cache[key(text,language)]=cloud.translate(text,language)
        # Persist after every success; the Firestore cache survives interrupted CI commits.
        temp=path.with_suffix('.tmp')
        temp.write_text(json.dumps(cache,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        temp.replace(path)
    print('Saved all website translations')

if __name__=='__main__':main()
