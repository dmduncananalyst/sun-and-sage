"""Authenticated private communications backend. Deploy separately from GitHub Pages.

Identity Platform/Firebase ID tokens, Firestore membership and private GCS objects.
No public paid translation endpoint. No audio or conversation data in static output.
"""
import asyncio
import base64
import datetime as dt
import hashlib
import json
import os
import uuid
from decimal import Decimal, ROUND_CEILING
from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .cloud import Cloud
from .site import CONFIG

LOCALES={'en':'en-US','es':'es-US','fa':'fa-IR','hy':'hy-AM','zh-CN':'cmn-CN','ko':'ko-KR','tl':'fil-PH','te':'te-IN','ru':'ru-RU','ar':'ar-XA'}
STT_LOCALES={**LOCALES,'ar':'ar-SA','zh-CN':'cmn-Hans-CN'}
app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
app.add_middleware(CORSMiddleware,allow_origins=[CONFIG['origin']],allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type'])
_cloud=None

def cloud():
    global _cloud
    if _cloud is None:_cloud=Cloud()
    return _cloud

def authenticate(token):
    from google.oauth2 import id_token
    from google.auth.transport.requests import Request
    audience=os.environ.get('FIREBASE_PROJECT_ID')
    if not audience:raise HTTPException(503,'Identity provider is not configured')
    try:
        claims=id_token.verify_firebase_token(token,Request(),audience=audience)
        if claims.get('iss')!='https://securetoken.google.com/'+audience:raise ValueError()
        if not claims.get('email_verified'):raise ValueError()
        return claims['sub']
    except Exception:raise HTTPException(401,'A verified signed-in account is required')

def user(header):
    if not header or not header.startswith('Bearer '):raise HTTPException(401,'Sign in required')
    return authenticate(header[7:])

def room_access(room_id,uid):
    if not room_id.isalnum() or len(room_id)>64:raise HTTPException(400,'Invalid conversation')
    room=cloud().db.collection('dommydom_rooms').document(room_id)
    data=room.get().to_dict()
    if not data or uid not in data.get('participants',{}):raise HTTPException(403,'Conversation access denied')
    return room,data

class Room(BaseModel):
    recipient_uid:str=Field(min_length=1,max_length=128)
    language:str='en'
    recipient_language:str='en'

class Message(BaseModel):
    id:str=Field(pattern=r'^[a-zA-Z0-9-]{8,64}$')
    text:str=Field(min_length=1,max_length=10000)
    language:str='en'

class Preference(BaseModel):
    language:str

def language(code):
    if code not in LOCALES:raise HTTPException(400,'Unsupported language')
    return code

@app.middleware('http')
async def private_headers(request,call_next):
    response=await call_next(request)
    response.headers['Cache-Control']='no-store'
    response.headers['X-Robots-Tag']='noindex, nofollow, noarchive'
    return response

@app.post('/rooms')
def create_room(body:Room,authorization:str=Header(default='')):
    uid=user(authorization);language(body.language);language(body.recipient_language)
    # Only the business operator may initiate conversations with another account.
    if uid!=os.environ.get('DOMMYDOM_OPERATOR_UID'):raise HTTPException(403,'Operator access required')
    identifier=uuid.uuid4().hex
    cloud().db.collection('dommydom_rooms').document(identifier).set({'participants':{uid:body.language,body.recipient_uid:body.recipient_language},'created':cloud().firestore.SERVER_TIMESTAMP})
    return {'id':identifier}

@app.post('/rooms/{room_id}/language')
def set_preference(room_id:str,body:Preference,authorization:str=Header(default='')):
    uid=user(authorization);room,data=room_access(room_id,uid);language(body.language)
    # FieldPath prevents user IDs from becoming dotted field expressions.
    from google.cloud.firestore_v1.field_path import FieldPath
    room.update({FieldPath('participants',uid).to_api_repr():body.language})
    return {'language':body.language}

def save_message(room_id,uid,body):
    language(body.language);room,data=room_access(room_id,uid)
    ref=room.collection('messages').document(body.id)
    original={'sender':uid,'original':body.text,'language':body.language,'created':cloud().firestore.SERVER_TIMESTAMP,'translations':{},'status':'pending'}
    from google.api_core.exceptions import AlreadyExists
    try:ref.create(original)
    except AlreadyExists:
        prior=ref.get().to_dict()
        if prior['sender']!=uid or prior['original']!=body.text or prior['language']!=body.language:raise HTTPException(409,'Message ID already used')
        if prior.get('status')=='complete':return prior
    result={}
    try:
        for target in set(data['participants'].values()):
            result[target]=cloud().translate(body.text,target,body.language,scope='room:'+room_id)
        ref.update({'translations':result,'status':'complete'})
    except Exception:
        ref.update({'translations':result,'status':'translation-unavailable'})
    return ref.get().to_dict()

@app.post('/rooms/{room_id}/messages')
def send_message(room_id:str,body:Message,authorization:str=Header(default='')):
    return save_message(room_id,user(authorization),body)

@app.get('/rooms/{room_id}/messages')
def messages(room_id:str,authorization:str=Header(default='')):
    uid=user(authorization);room,data=room_access(room_id,uid)
    rows=room.collection('messages').order_by('created',direction=cloud().firestore.Query.DESCENDING).limit(100).stream()
    return {'language':data['participants'][uid],'messages':[{'id':r.id,**r.to_dict()} for r in rows]}

@app.post('/rooms/{room_id}/messages/{message_id}/speak')
def speak_message(room_id:str,message_id:str,authorization:str=Header(default='')):
    uid=user(authorization);room,data=room_access(room_id,uid)
    if not message_id.replace('-','').isalnum():raise HTTPException(400,'Invalid message')
    item=room.collection('messages').document(message_id).get().to_dict()
    if not item:raise HTTPException(404,'Message not found')
    target=data['participants'][uid]
    text=item.get('translations',{}).get(target)
    if not text:raise HTTPException(409,'Translated text not available')
    return cloud().speak(text,LOCALES[target],'room:'+room_id)

def speech_settings(code):
    language(code)
    # Explicit validated deployment configuration is mandatory: support varies by region/model.
    mappings=json.loads(os.environ.get('STT_VERIFIED_LANGUAGE_CONFIG','{}'))
    if code not in mappings:raise HTTPException(503,'Speech language/model/region has not been verified for this deployment')
    item=mappings[code]
    if not all(item.get(k) for k in ['region','model','locale']):raise HTTPException(503,'Incomplete speech configuration')
    return item

def reserve_speech(identifier,seconds):
    rate=os.environ.get('STT_MICROUSD_PER_MINUTE')
    if not rate:raise HTTPException(503,'Verified speech pricing is required')
    units=int((Decimal(rate)*Decimal(seconds)/60).to_integral_value(rounding=ROUND_CEILING))
    return cloud().execute(identifier,units,lambda:{'reserved_seconds':seconds},True,'voice')

class Voice(BaseModel):
    id:str=Field(pattern=r'^[a-zA-Z0-9-]{8,64}$')
    language:str='en'
    pcm_base64:str=Field(max_length=2600000)

@app.post('/rooms/{room_id}/voice')
def voice_message(room_id:str,body:Voice,authorization:str=Header(default='')):
    uid=user(authorization);room,_=room_access(room_id,uid);settings=speech_settings(body.language)
    try:audio=base64.b64decode(body.pcm_base64,validate=True)
    except ValueError:raise HTTPException(400,'Invalid recording')
    # Signed 16-bit mono PCM at 16kHz, maximum 60 seconds; do not trust client duration.
    if not audio or len(audio)>1920000 or len(audio)%2:raise HTTPException(400,'Recording must be 16kHz PCM, at most 60 seconds')
    bucket=os.environ.get('DOMMYDOM_PRIVATE_AUDIO_BUCKET')
    if not bucket:raise HTTPException(503,'Private audio bucket is not configured')
    from google.cloud import speech_v2,storage
    from google.api_core.client_options import ClientOptions
    client=speech_v2.SpeechClient(client_options=ClientOptions(api_endpoint=settings['region']+'-speech.googleapis.com'))
    digest=hashlib.sha256(audio).hexdigest()
    prior=room.collection('messages').document(body.id).get().to_dict()
    expected_object=f'rooms/{room_id}/{uid}/{digest}.pcm'
    if prior:
        if prior.get('sender')==uid and prior.get('audio_object')==expected_object:
            return prior
        raise HTTPException(409,'Message ID already used; no new speech request sent')
    identifier=hashlib.sha256((room_id+uid+body.language+digest+'stt').encode()).hexdigest()
    def transcribe():
        reserve_speech(identifier+'reservation',len(audio)/32000)
        response=client.recognize(request={'recognizer':f'projects/{cloud().project}/locations/{settings["region"]}/recognizers/_','config':{'explicit_decoding_config':{'encoding':'LINEAR16','sample_rate_hertz':16000,'audio_channel_count':1},'language_codes':[settings['locale']],'model':settings['model']},'content':audio},retry=None,timeout=65)
        return ' '.join(r.alternatives[0].transcript for r in response.results if r.alternatives)
    transcript=cloud().execute(identifier,0,transcribe,True,'voice')
    storage_client=storage.Client(project=cloud().project)
    object_name=expected_object
    blob=storage_client.bucket(bucket).blob(object_name)
    from google.api_core.exceptions import PreconditionFailed
    try:blob.upload_from_string(audio,content_type='application/octet-stream',if_generation_match=0)
    except PreconditionFailed:pass
    result=save_message(room_id,uid,Message(id=body.id,text=transcript or '[No speech recognized]',language=body.language))
    room.collection('messages').document(body.id).update({'audio_object':object_name})
    return result

@app.get('/rooms/{room_id}/messages/{message_id}/recording')
def recording(room_id:str,message_id:str,authorization:str=Header(default='')):
    uid=user(authorization);room,_=room_access(room_id,uid)
    if not message_id.replace('-','').isalnum():raise HTTPException(400,'Invalid message')
    data=room.collection('messages').document(message_id).get().to_dict() or {}
    name=data.get('audio_object')
    if not name or not name.startswith('rooms/'+room_id+'/'):raise HTTPException(404,'Recording unavailable')
    from google.cloud import storage
    from fastapi.responses import Response
    audio=storage.Client(project=cloud().project).bucket(os.environ['DOMMYDOM_PRIVATE_AUDIO_BUCKET']).blob(name).download_as_bytes()
    return Response(audio,media_type='application/octet-stream',headers={'Cache-Control':'no-store','X-Robots-Tag':'noindex'})

@app.get('/capabilities')
def capabilities(authorization:str=Header(default='')):
    user(authorization)
    voices=cloud().voices()
    configured=json.loads(os.environ.get('STT_VERIFIED_LANGUAGE_CONFIG','{}'))
    return {code:{'translation':True,'speech_to_text_configured':code in configured,'cloud_standard_voice':any(LOCALES[code] in v['languageCodes'] and '-Standard-' in v['name'] for v in voices),'fallback':'available browser voice, otherwise translated captions'} for code in LOCALES}

@app.websocket('/rooms/{room_id}/call')
async def call(socket:WebSocket,room_id:str):
    # Token is the first frame, never a query string or URL logged by a proxy.
    if socket.headers.get('origin')!=CONFIG['origin']:
        await socket.close(code=1008);return
    await socket.accept()
    tasks=[]
    try:
        hello=await asyncio.wait_for(socket.receive_json(),10)
        uid=await asyncio.to_thread(authenticate,hello.get('token',''))
        room,data=await asyncio.to_thread(room_access,room_id,uid)
        code=data['participants'][uid];settings=speech_settings(code)
        from google.cloud import speech_v2
        from google.api_core.client_options import ClientOptions
        client=speech_v2.SpeechAsyncClient(client_options=ClientOptions(api_endpoint=settings['region']+'-speech.googleapis.com'))
        session=uuid.uuid4().hex
        await asyncio.to_thread(reserve_speech,session,60)
        queue=asyncio.Queue(maxsize=20)
        start=asyncio.get_running_loop().time()
        sent=0
        async def requests():
            yield speech_v2.StreamingRecognizeRequest(recognizer=f'projects/{cloud().project}/locations/{settings["region"]}/recognizers/_',streaming_config=speech_v2.StreamingRecognitionConfig(config=speech_v2.RecognitionConfig(explicit_decoding_config=speech_v2.ExplicitDecodingConfig(encoding='LINEAR16',sample_rate_hertz=16000,audio_channel_count=1),language_codes=[settings['locale']],model=settings['model']),streaming_features=speech_v2.StreamingRecognitionFeatures(interim_results=True)))
            while True:
                chunk=await queue.get()
                if chunk is None:return
                yield speech_v2.StreamingRecognizeRequest(audio=chunk)
        async def recognize():
            responses=await client.streaming_recognize(requests=requests(),retry=None)
            async for response in responses:
                for result in response.results:
                    if not result.alternatives:continue
                    text=result.alternatives[0].transcript
                    await socket.send_json({'type':'caption','text':text,'final':result.is_final,'language':code})
                    if result.is_final and text.strip():
                        body=Message(id=uuid.uuid4().hex,text=text,language=code)
                        await asyncio.to_thread(save_message,room_id,uid,body)
        async def receive_audio():
            nonlocal sent
            while True:
                chunk=await socket.receive_bytes()
                if len(chunk)>16000 or len(chunk)%2:raise ValueError('Invalid PCM frame')
                sent+=len(chunk)
                if sent>1920000:raise ValueError('Call segment reached 60 seconds; reconnect to continue')
                await queue.put(chunk)
        async def deliver():
            # Durable Firestore relay works across Cloud Run replicas. Deliver only new peer speech.
            seen=set();joined=dt.datetime.now(dt.timezone.utc)
            while True:
                await asyncio.sleep(.5)
                await asyncio.to_thread(room_access,room_id,uid)
                rows=await asyncio.to_thread(lambda:list(room.collection('messages').order_by('created',direction=cloud().firestore.Query.DESCENDING).limit(20).stream()))
                for row in reversed(rows):
                    item=row.to_dict()
                    if row.id in seen or item['sender']==uid or item.get('created',joined)<joined:continue
                    target=item.get('translations',{}).get(code)
                    if not target:continue
                    seen.add(row.id)
                    await socket.send_json({'type':'translation','id':row.id,'original':item['original'],'text':target,'language':code})
                    try:
                        audio=await asyncio.to_thread(cloud().speak,target,LOCALES[code],'room:'+room_id)
                        await socket.send_json({'type':'audio','id':row.id,**audio})
                    except Exception:await socket.send_json({'type':'audio-unavailable','id':row.id,'text':target,'locale':LOCALES[code]})
        tasks=[asyncio.create_task(f()) for f in [recognize,receive_audio,deliver]]
        done,_=await asyncio.wait(tasks,timeout=60,return_when=asyncio.FIRST_COMPLETED)
        for task in done:task.result()
        await socket.send_json({'type':'segment-ended','reconnect':True})
    except (WebSocketDisconnect,asyncio.CancelledError):pass
    except Exception:
        try:await socket.send_json({'type':'error','message':'Voice translation unavailable. Original calling and text messaging remain available.'})
        except Exception:pass
    finally:
        for task in tasks:task.cancel()
        if tasks:await asyncio.gather(*tasks,return_exceptions=True)
        try:await socket.close()
        except Exception:pass
