"""Compatible development provider utilities. No provider calls on import or render."""
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import time
from urllib.request import Request, build_opener, HTTPRedirectHandler
from .workflow import normal

LOCALES = ['es', 'fa', 'hy', 'zh-CN', 'ko', 'tl', 'te', 'ru', 'ar']
PROTECTED = re.compile(r'Paper Trail|PaperTrail|DommyDom|StartWeb7|Google Translate|Google|QuickBooks|Xero|Gmail|Microsoft 365 / Outlook|https?://[^\s<>]+|[\w.+-]+@[\w.-]+\.[A-Za-z]+|\$[\d,.]+|\b\d[\d,.]*(?:%|\b)')

def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def atomic(path, data):
    path = Path(path)
    if path.exists() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        for attempt in range(6):
            try:
                os.replace(temporary, path)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(.1 * 2 ** attempt)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def budget_warning(value):
    # Compatibility with former callers; owner removed custom monetary warnings.
    return None

class Node:
    def __init__(self, tag='', attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []
    def find(self, predicate):
        found = [self] if predicate(self) else []
        for child in self.children:
            if isinstance(child, Node):
                found.extend(child.find(predicate))
        return found
    def text(self):
        return normal(''.join(child.text() if isinstance(child, Node) else child for child in self.children))

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        before = len(self.stack)
        self.handle_starttag(tag, attrs)
        del self.stack[before:]
    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break
    def handle_data(self, value):
        self.stack[-1].children.append(value)

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('Translation redirects are not allowed')

def protected_html(source):
    # Google supports translate="no" spans. Never send executable markup.
    parts, previous = [], 0
    for match in PROTECTED.finditer(source):
        parts.extend([html.escape(source[previous:match.start()]), '<span translate="no">' + html.escape(match[0]) + '</span>'])
        previous = match.end()
    parts.append(html.escape(source[previous:]))
    return ''.join(parts)

class PlainResult(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(value)
    def handle_data(self, value):
        self.parts.append(value)

def google_translate(locale, sources, project, token):
    from .connection import PROJECT, private_path
    if project != PROJECT or locale not in LOCALES or not sources or len(sources) > 50:
        raise ValueError('Translation scope is invalid')
    if any(not isinstance(s, str) or not s.strip() or len(s) > 30000 for s in sources):
        raise ValueError('Invalid translation source')
    # Separate incremental ledger: never reconstruct or reset historical balances.
    path = private_path('DOMMYDOM_TRANSLATION_REQUEST_DB', 'restored-requests.sqlite3')
    path.parent.mkdir(parents=True, exist_ok=True)
    database = sqlite3.connect(path, timeout=30)
    identifier = digest(project + '\0' + locale + '\0' + '\0'.join(sources))
    keys = [digest(project + '\0' + locale + '\0' + s) for s in sources]
    try:
        database.executescript('CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, locale TEXT, characters INTEGER, status TEXT, created REAL, response TEXT); CREATE TABLE IF NOT EXISTS segments(id TEXT PRIMARY KEY, request TEXT);')
        database.execute('BEGIN IMMEDIATE')
        prior = database.execute('SELECT status,response FROM requests WHERE id=?', (identifier,)).fetchone()
        if prior:
            if prior[0] == 'complete':
                return json.loads(prior[1])
            raise RuntimeError('Previous translation request is uncertain; reconcile before retrying')
        if any(database.execute('SELECT 1 FROM segments WHERE id=?', (key,)).fetchone() for key in keys):
            raise RuntimeError('A source was already reserved; refusing duplicate translation')
        database.execute('INSERT INTO requests VALUES(?,?,?,?,?,NULL)', (identifier, locale, sum(map(len, sources)), 'reserved', time.time()))
        database.executemany('INSERT INTO segments VALUES(?,?)', [(key, identifier) for key in keys])
        database.commit()
        payload = dict(contents=[protected_html(s) for s in sources], mimeType='text/html', sourceLanguageCode='en', targetLanguageCode=locale, model=f'projects/{project}/locations/global/models/general/nmt')
        url = f'https://translation.googleapis.com/v3/projects/{project}/locations/global:translateText'
        request = Request(url, data=json.dumps(payload).encode(), headers={'Authorization':'Bearer ' + token, 'Content-Type':'application/json', 'x-goog-user-project':project})
        try:
            with build_opener(NoRedirect()).open(request, timeout=90) as response:
                result = json.load(response)
            values = [''.join(PlainResult(row['translatedText']).parts) for row in result['translations']]
            if len(values) != len(sources) or any(not value.strip() for value in values):
                raise ValueError('Incomplete translation response')
            for source, value in zip(sources, values):
                if any(match[0] not in value for match in PROTECTED.finditer(source)):
                    raise ValueError('Protected brand, URL or number was altered')
            with database:
                database.execute("UPDATE requests SET status='complete',response=? WHERE id=?", (json.dumps(values), identifier))
            return values
        except BaseException as error:
            with database:
                database.execute("UPDATE requests SET status='uncertain' WHERE id=? AND status!='complete'", (identifier,))
            status = ' HTTP ' + str(error.code) if hasattr(error, 'code') else ''
            raise RuntimeError('Google translation failed' + status + '; request retained for reconciliation, not retried') from None
    finally:
        database.close()
