"""Private Google API adapter. Shared transactional ledger reserves BEFORE every call.

An uncertain request is never automatically retried or refunded. This intentionally
fails closed after timeouts so concurrent builds and communications cannot double bill.
"""
import datetime as dt
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
import os
import sys
from .site import CONFIG, key

def cost_units(characters):
    # USD millionths, conservatively ignoring free-tier credits.
    return int((Decimal(characters)*Decimal(str(CONFIG['translation_usd_per_million_characters']))).to_integral_value(rounding=ROUND_CEILING))

def reserve_math(spent, amount):
    if amount < 0 or spent + amount > int(CONFIG['monthly_limit_usd']*1_000_000):
        raise RuntimeError('Monthly translation limit reached; no API request sent')
    return spent+amount

class Cloud:
    def __init__(self):
        import google.auth
        from google.auth.transport.requests import AuthorizedSession
        from google.cloud import firestore
        self.project=os.environ.get('GOOGLE_CLOUD_PROJECT') or CONFIG['google_project_id']
        if not self.project or self.project.startswith('appgprj_'):
            raise RuntimeError('Existing GOOGLE_CLOUD_PROJECT and authenticated Google Cloud identity are required')
        credentials, _=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'],quota_project_id=self.project)
        self.http=AuthorizedSession(credentials)
        self.admin_http=AuthorizedSession(credentials.with_quota_project(None))
        self.db=firestore.Client(project=self.project,credentials=credentials)
        self.firestore=firestore

    def preflight(self):
        # Read-only checks; never enables APIs, changes quotas, or creates projects.
        services=['translate.googleapis.com','firestore.googleapis.com']
        for service in services:
            r=self.http.get(f'https://serviceusage.googleapis.com/v1/projects/{self.project}/services/{service}',timeout=30)
            r.raise_for_status()
            if r.json().get('state')!='ENABLED': raise RuntimeError(service+' is not enabled')
        r=self.admin_http.get(f'https://cloudbilling.googleapis.com/v1/projects/{self.project}/billingInfo',timeout=30)
        r.raise_for_status()
        if not r.json().get('billingEnabled'): raise RuntimeError('Existing project billing is not enabled')
        supported=self.http.get(f'https://translation.googleapis.com/v3/projects/{self.project}/locations/global/supportedLanguages',timeout=30)
        supported.raise_for_status()
        available={item['languageCode'] for item in supported.json().get('languages',[]) if item.get('supportTarget')}
        if not set(CONFIG['languages']).issubset(available):
            raise RuntimeError('Requested translation languages not confirmed by provider: '+','.join(set(CONFIG['languages'])-available))
        # Require a deliberate monthly baseline, including other existing translation usage.
        month=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m')
        baseline=self.db.collection('dommydom_budget_baselines').document(month).get()
        if not baseline.exists or baseline.to_dict().get('verified') is not True:
            raise RuntimeError('Verified existing monthly translation-spend baseline missing; paid requests disabled')

    def execute(self, identifier, units, operation, private=False, service='translation'):
        collection='dommydom_private_cache' if private else 'dommydom_translation_cache'
        request=self.db.collection(collection).document(identifier)
        month=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m')
        budget=self.db.collection('dommydom_spend').document(month+'-'+service)
        baseline=self.db.collection('dommydom_budget_baselines').document(month)
        @self.firestore.transactional
        def reserve(transaction):
            existing=request.get(transaction=transaction)
            state=budget.get(transaction=transaction)
            base=baseline.get(transaction=transaction)
            if not base.exists or base.to_dict().get('verified') is not True:
                raise RuntimeError('Unverified monthly spending baseline')
            if existing.exists:
                data=existing.to_dict()
                if data['status']=='complete': return data['result']
                raise RuntimeError('Request already reserved or uncertain; manual reconciliation required')
            if service!='translation':
                limit=int(os.environ.get('VOICE_MONTHLY_LIMIT_MICROUSD','0'))
                if not limit: raise RuntimeError('Voice spending has not been authorized/configured')
                spent=(state.to_dict() or {}).get('reserved_microusd',0)
                total=spent+units
                if total>limit: raise RuntimeError('Voice monthly limit reached')
            else:
                spent=(state.to_dict() or {}).get('reserved_microusd',0)
                total=reserve_math(spent+base.to_dict().get('translation_microusd',0),units)
                total-=base.to_dict().get('translation_microusd',0)
            transaction.set(budget,{'reserved_microusd':spent+units,'updated':self.firestore.SERVER_TIMESTAMP})
            transaction.set(request,{'status':'reserved','units':units,'service':service,'created':self.firestore.SERVER_TIMESTAMP})
            if service=='translation' and total+base.to_dict().get('translation_microusd',0)>=CONFIG['warning_usd']*1_000_000:
                transaction.set(self.db.collection('dommydom_budget_warnings').document(month),{'threshold_usd':15,'created':self.firestore.SERVER_TIMESTAMP})
                print('::warning::DommyDom monthly translation reservations reached $15',file=sys.stderr)
            return None
        cached=reserve(self.db.transaction())
        if cached is not None:return cached
        # No library retry: an ambiguous failure keeps its reservation and blocks repetition.
        result=operation()
        request.update({'status':'complete','result':result})
        return result

    def translate(self,text,target,source='en',scope='website'):
        if target==source:return text
        if target not in CONFIG['languages'] or source not in CONFIG['languages']:
            raise ValueError('Unsupported language')
        if not text or len(text)>20000: raise ValueError('Text must contain 1–20000 characters')
        identifier=hashlib.sha256((scope+'\0'+key(text,target,source)).encode()).hexdigest()
        def operation():
            r=self.http.post(f'https://translation.googleapis.com/v3/projects/{self.project}/locations/global:translateText',json={'contents':[text],'mimeType':'text/plain','sourceLanguageCode':source,'targetLanguageCode':target,'model':f'projects/{self.project}/locations/global/models/general/nmt'},timeout=45)
            r.raise_for_status()
            return r.json()['translations'][0]['translatedText']
        return self.execute(identifier,cost_units(len(text)),operation,private=scope!='website')

    def voices(self):
        r=self.http.get('https://texttospeech.googleapis.com/v1/voices',timeout=30)
        r.raise_for_status();return r.json().get('voices',[])

    def speak(self,text,locale,scope):
        if len(text)>600 or len(text.encode('utf-8'))>3000:
            return {'audio':None,'fallback':'browser-voice-or-captions','locale':locale,'text':text}
        # Discover real deployed voice availability. No invented Persian/Armenian voice.
        voices=[v for v in self.voices() if locale in v.get('languageCodes',[]) and '-Standard-' in v['name']]
        if not voices:return {'audio':None,'fallback':'browser-voice-or-captions','locale':locale,'text':text}
        rate=os.environ.get('TTS_STANDARD_MICROUSD_PER_CHAR')
        if not rate:raise RuntimeError('Verified TTS price required before synthesis')
        identifier=hashlib.sha256((scope+locale+text+'tts').encode()).hexdigest()
        def operation():
            r=self.http.post('https://texttospeech.googleapis.com/v1/text:synthesize',json={'input':{'text':text},'voice':{'languageCode':locale,'name':voices[0]['name']},'audioConfig':{'audioEncoding':'MP3'}},timeout=30)
            r.raise_for_status();return {'audio':r.json()['audioContent'],'locale':locale}
        units=int((Decimal(rate)*len(text)).to_integral_value(rounding=ROUND_CEILING))
        return self.execute(identifier,units,operation,True,'voice')
