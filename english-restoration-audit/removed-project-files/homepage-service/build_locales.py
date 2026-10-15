"""Authorized admin-only Google batch builder. Dry-run is the default; never deployed as an HTTP route."""
import argparse,json,sys,time
from pathlib import Path
from html.parser import HTMLParser
from localization import LANGUAGES,NOTICE,key,protect,sources,plan
ROOT=Path(__file__).resolve().parent.parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.text=[]
 def handle_data(self,s):self.text.append(s)
def plain(value):p=Text();p.feed(value);return ''.join(p.text)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--approve-billable',action='store_true');parser.add_argument('--project');args=parser.parse_args()
 catalog=json.loads((ROOT/'homepage-service/homepage-source.json').read_text(encoding='utf-8'));print(json.dumps(plan(catalog),indent=2))
 if not args.approve_billable:return
 if not args.project:parser.error('An approved non-secret Google project ID is required')
 # Imports and all external operations occur only after the explicit authorization flag.
 import google.auth
 from google.auth.transport.requests import AuthorizedSession
 credentials,_=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-translation']);http=AuthorizedSession(credentials)
 supported=http.get(f'https://translation.googleapis.com/v3/projects/{args.project}/locations/global/supportedLanguages',params={'displayLanguageCode':'en'},timeout=20);supported.raise_for_status();codes={x['languageCode'] for x in supported.json()['languages']}
 if any(lang not in codes and not(lang=='zh-CN' and 'zh' in codes) for lang in LANGUAGES):raise RuntimeError('An approved locale is not supported by this project. No substitution performed.')
 cache=ROOT/'homepage-service/.google-cache';cache.mkdir(exist_ok=True)
 for lang in LANGUAGES:
  translated={};pending=[]
  for source in sources(catalog,lang):
   path=cache/(key(lang+'\0'+source)+'.json')
   if path.exists():translated[source]=json.loads(path.read_text(encoding='utf-8'))
   else:pending.append(source)
  for start in range(0,len(pending),30):
   batch=pending[start:start+30];response=http.post(f'https://translation.googleapis.com/v3/projects/{args.project}/locations/global:translateText',json={'sourceLanguageCode':'en','targetLanguageCode':lang,'mimeType':'text/html','contents':[protect(s) for s in batch]},timeout=30);response.raise_for_status();values=response.json()['translations'];assert len(values)==len(batch)
   for source,item in zip(batch,values):
    value=plain(item['translatedText']);assert value.strip();translated[source]=value;(cache/(key(lang+'\0'+source)+'.json')).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
  notice=NOTICE.replace('[language]',LANGUAGES[lang][1]);pack={'provider':'google-cloud-translation','sourceVersion':catalog['version'],'target':lang,'strings':{s:translated[s] for s in catalog['strings']},'ui':{k:translated[v] for k,v in catalog['ui'].items()},'notice':translated[notice],'generatedAt':int(time.time())}
  (ROOT/'assets/homepage-locales'/f'{lang}.json').write_text(json.dumps(pack,ensure_ascii=False),encoding='utf-8')
 print('Nine cached homepage packs generated. They remain inactive until matching AI chat and lead delivery are verified and configuration is approved.')
if __name__=='__main__':main()
