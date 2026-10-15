"""Translation policy: only checked-in public English is eligible for Google."""
import hashlib, html, json, re, time
from html.parser import HTMLParser
from pathlib import Path
LANGUAGES={'es','fa','zh-CN','hy','ko','tl','te','ru','ar'}
PROTECTED=re.compile(r'Dominique Duncan-Nelson|DommyDom|RISE\s*[×x]\s*REAL|https?://[^\s<>]+|[\w.+-]+@[\w.-]+\.[A-Za-z]+|\+?\d[\d() .-]{7,}\d',re.I)
titles_path=Path(__file__).with_name('project-titles.json')
if titles_path.exists():
    titles=json.loads(titles_path.read_text(encoding='utf-8'))
    if titles:PROTECTED=re.compile(PROTECTED.pattern+'|'+ '|'.join(re.escape(t) for t in sorted(titles,key=len,reverse=True)),re.I)
class TextOnly(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def plain(value):
    p=TextOnly();p.feed(value);return ''.join(p.parts)
def protected_html(text):
    parts=[];last=0
    for m in PROTECTED.finditer(text):
        parts.extend([html.escape(text[last:m.start()]),'<span translate="no">'+html.escape(m[0])+'</span>']);last=m.end()
    return ''.join(parts)+html.escape(text[last:])
class PolicyError(Exception):pass
class Service:
    def __init__(self,allowed,store,provider,daily_limit=250000):self.allowed=set(allowed);self.store=store;self.provider=provider;self.daily_limit=daily_limit
    def translate(self,payload,client):
        if not isinstance(payload,dict) or set(payload)!={'target','texts'}:raise PolicyError('Invalid request')
        target=payload['target'];texts=payload['texts']
        if target not in LANGUAGES or not isinstance(texts,list) or not 1<=len(texts)<=60:raise PolicyError('Invalid language or batch')
        if any(not isinstance(t,str) or len(t)>12000 for t in texts) or sum(map(len,texts))>30000:raise PolicyError('Request too large')
        # Unknown text is never forwarded: this also excludes visitor-entered information.
        results={t:t for t in texts};pending=[]
        for text in dict.fromkeys(texts):
            if text not in self.allowed:continue
            key=hashlib.sha256((target+'\0'+text).encode()).hexdigest();cached=self.store.get(key)
            if cached is not None:results[text]=cached
            else:pending.append((text,key))
        # Every request is rate limited, including cache hits. Durable reservation precedes Google.
        self.store.reserve(client,sum(len(t) for t,_ in pending),self.daily_limit)
        if pending:
            values=self.provider(target,[protected_html(t) for t,_ in pending])
            if len(values)!=len(pending):raise RuntimeError('Incomplete provider response')
            for (text,key),value in zip(pending,values):
                value=plain(value)
                if not value:raise RuntimeError('Empty provider response')
                self.store.put(key,value);results[text]=value
        return {'translations':[results[t] for t in texts]}
