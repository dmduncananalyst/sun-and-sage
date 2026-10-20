"""Explicit local generation with durable deduplication and no release operations.

The initial-generation spending override is an explicit CLI switch, separate from
the future automated workflow's normal monthly limit. No Firestore is required.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import sqlite3
import threading
import time
from .site import ROOT, CONFIG, inventory, key
from .cloud import cost_units

STATE=ROOT/'.translation-state'
DB=STATE/'local-cache.sqlite3'
OUTPUT=ROOT/'multilingual/translations.json'
WRITE_LOCK=threading.Lock()

class ClosingConnection(sqlite3.Connection):
    def __exit__(self,*args):
        try:return super().__exit__(*args)
        finally:self.close()

def connect():
    db=sqlite3.connect(DB,timeout=60,factory=ClosingConnection)
    db.execute('PRAGMA busy_timeout=60000')
    return db

def initialize():
    STATE.mkdir(exist_ok=True)
    with connect() as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('CREATE TABLE IF NOT EXISTS segments (hash TEXT PRIMARY KEY, language TEXT NOT NULL, source TEXT NOT NULL, result TEXT, status TEXT NOT NULL, request TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, language TEXT NOT NULL, characters INTEGER NOT NULL, reserved_microusd INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, error TEXT)')
        # Recover only requests whose complete provider results are already saved.
        # A local checkpoint failure is not an ambiguous provider call.
        db.execute("UPDATE requests SET status='complete',error=NULL WHERE status='uncertain' AND EXISTS (SELECT 1 FROM segments WHERE segments.request=requests.id) AND NOT EXISTS (SELECT 1 FROM segments WHERE segments.request=requests.id AND segments.status!='complete')")

def checkpoint():
    with WRITE_LOCK:
        cache=json.loads(OUTPUT.read_text(encoding='utf-8'))
        with connect() as db:
            cache.update(dict(db.execute("SELECT hash,result FROM segments WHERE status='complete'")))
        temp=OUTPUT.with_suffix('.tmp')
        temp.write_text(json.dumps(cache,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        # Windows/OneDrive scanners can briefly hold the destination open. Retry
        # only the local file operation; never repeat the paid translation request.
        for attempt in range(9):
            try:temp.replace(OUTPUT);break
            except PermissionError:
                if attempt==8:raise
                time.sleep(min(.05*(2**attempt),2))

def batches(texts,max_characters=5000,max_segments=100):
    batch=[];size=0
    for text in texts:
        if len(text)>30000:raise ValueError('Segment exceeds provider request limit')
        if batch and (size+len(text)>max_characters or len(batch)>=max_segments):
            yield batch;batch=[];size=0
        batch.append(text);size+=len(text)
    if batch:yield batch

def reserve(language,texts,override):
    identifier=hashlib.sha256((language+'\0'+'\0'.join(key(t,language) for t in texts)).encode()).hexdigest()
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        # A completed/uncertain segment must never be billed again under another batch ID.
        for text in texts:
            prior=db.execute('SELECT status FROM segments WHERE hash=?',(key(text,language),)).fetchone()
            if prior:raise RuntimeError('Segment already cached or reserved; refusing duplicate request')
        month=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m')
        amount=cost_units(sum(map(len,texts)))
        spent=db.execute('SELECT COALESCE(SUM(reserved_microusd),0) FROM requests WHERE created LIKE ?',(month+'%',)).fetchone()[0]
        if not override and spent+amount>CONFIG['monthly_limit_usd']*1_000_000:raise RuntimeError('Monthly limit reached')
        db.execute('INSERT INTO requests VALUES (?,?,?,?,?,?,NULL)',(identifier,language,sum(map(len,texts)),amount,'reserved',dt.datetime.now(dt.timezone.utc).isoformat()))
        db.executemany('INSERT INTO segments VALUES (?,?,?,NULL,?,?)',[(key(text,language),language,text,'reserved',identifier) for text in texts])
    return identifier

def worker(language,texts,override):
    import google.auth
    from google.auth.transport.requests import AuthorizedSession
    project=CONFIG['google_project_id']
    credentials,_=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'],quota_project_id=project)
    session=AuthorizedSession(credentials)
    with connect() as db:
        done={r[0] for r in db.execute("SELECT hash FROM segments WHERE status='complete'")}
        uncertain=db.execute("SELECT COUNT(*) FROM segments WHERE language=? AND status!='complete'",(language,)).fetchone()[0]
    if uncertain:raise RuntimeError(f'{language}: prior uncertain requests require reconciliation; no retries sent')
    with WRITE_LOCK:existing=json.loads(OUTPUT.read_text(encoding='utf-8'))
    missing=[text for text in texts if key(text,language) not in done and key(text,language) not in existing]
    groups=list(batches(missing));completed=0
    for group in groups:
        identifier=reserve(language,group,override)
        try:
            response=session.post(f'https://translation.googleapis.com/v3/projects/{project}/locations/global:translateText',json={'contents':group,'mimeType':'text/plain','sourceLanguageCode':'en','targetLanguageCode':language,'model':f'projects/{project}/locations/global/models/general/nmt'},timeout=90)
            response.raise_for_status()
            results=response.json()['translations']
            if len(results)!=len(group):raise RuntimeError('Unexpected translation response length')
            with connect() as db:
                for text,item in zip(group,results):
                    value=html.unescape(item['translatedText'])
                    if not value.strip():raise RuntimeError('Provider returned empty translation')
                    db.execute("UPDATE segments SET result=?,status='complete' WHERE hash=?",(value,key(text,language)))
                db.execute("UPDATE requests SET status='complete' WHERE id=?",(identifier,))
            checkpoint();completed+=len(group)
            if completed==len(missing) or completed%500<len(group):print(f'{language}: {completed}/{len(missing)} new segments saved',flush=True)
        except BaseException as error:
            with connect() as db:db.execute("UPDATE requests SET status='uncertain',error=? WHERE id=? AND status!='complete'",(type(error).__name__,identifier))
            # No automatic retry of any ambiguous paid operation.
            raise
    return language,completed

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--authorized-initial-generation',action='store_true',required=True)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    initialize()
    lock=STATE/'generation.lock'
    descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    os.write(descriptor,str(os.getpid()).encode());os.close(descriptor)
    try:
        print('Scanning English source files for local generation...',flush=True)
        listing,texts=inventory()
        print(f'Local-only generation: {len(listing)} pages; {len(texts)} unique source segments; nine languages.',flush=True)
        print('Initial generation authorized above automated monthly threshold. No commit, push, publication or deployment.',flush=True)
        (STATE/'initial-generation-authorization.json').write_text(json.dumps({'authorized':True,'local_only':True,'monthly_threshold_override_for_this_run':True,'timestamp':dt.datetime.now(dt.timezone.utc).isoformat()}))
        failures=[]
        with ThreadPoolExecutor(max_workers=min(max(args.workers,1),9)) as pool:
            jobs={pool.submit(worker,language,texts,args.authorized_initial_generation):language for language in CONFIG['languages'] if language!='en'}
            for job in as_completed(jobs):
                try:print('Completed:',job.result(),flush=True)
                except BaseException as error:failures.append((jobs[job],type(error).__name__,str(error)));print('Generation paused for',jobs[job],type(error).__name__,flush=True)
        checkpoint()
        with connect() as db:
            counts=dict(db.execute("SELECT language,COUNT(*) FROM segments WHERE status='complete' GROUP BY language"))
            requests=db.execute('SELECT COUNT(*),COALESCE(SUM(characters),0),COALESCE(SUM(reserved_microusd),0) FROM requests').fetchone()
        report={'local_only':True,'published':False,'languages':counts,'source_segments':len(texts),'requests':requests[0],'source_characters_sent_or_reserved':requests[1],'gross_reserved_usd':requests[2]/1_000_000,'failures':failures,'initial_generation_override_authorized':True}
        (ROOT/'multilingual/local-generation-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2),flush=True)
        if failures:raise RuntimeError('Some languages could not finish; saved work is preserved')
    finally:
        lock.unlink(missing_ok=True)

if __name__=='__main__':main()
