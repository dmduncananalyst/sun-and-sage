"""Compatible durable accounting, without custom monetary warnings or cutoffs.

Historical snapshots remain recorded; no historical balance is invented or reset.
Google billing, IAM and quotas are never modified. Explicit callers authorize jobs.
"""
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
import json
import sqlite3
import time
import uuid

PROJECT = 'project-2e0d7d9d-d482-4fcf-b6d'

class Budget:
    def __init__(self, path):
        self.path = str(path)
        self.read_only = False
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as c:
            c.executescript('CREATE TABLE IF NOT EXISTS snapshot(id INTEGER PRIMARY KEY CHECK(id=1), data TEXT); CREATE TABLE IF NOT EXISTS reservations(id TEXT PRIMARY KEY, site TEXT, chars INTEGER, created REAL, result TEXT);')

    @contextmanager
    def db(self):
        c = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        c.row_factory = sqlite3.Row
        try:
            yield c
        finally:
            if c.in_transaction:
                c.rollback()
            c.close()

    def validate(self, snapshot, now=None, preparation=False):
        if snapshot.get('project') != PROJECT:
            raise ValueError('Google project mismatch')
        if snapshot.get('all_jobs_use_counter') is False and not preparation:
            raise ValueError('Shared accounting configuration requires review')

    def reconcile(self, snapshot):
        self.validate(snapshot)
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            if c.execute("SELECT count(*) FROM reservations WHERE result='reserved'").fetchone()[0]:
                raise ValueError('Resolve pending reservations before reconciliation')
            c.execute('INSERT OR REPLACE INTO snapshot VALUES(1,?)', (json.dumps(snapshot),))
            c.commit()

    def _quote(self, c, chars):
        if type(chars) is not int or chars < 0:
            raise ValueError('Invalid character count')
        row = c.execute('SELECT data FROM snapshot WHERE id=1').fetchone()
        if row:
            self.validate(json.loads(row[0]))
        return dict(allowed=True, reason='Owner-authorized incremental usage; no custom spending cap', project=PROJECT, characters=chars, estimated_incremental_usd=str(Decimal(chars) * 20 / 1000000), actual_charges_usd=None, soft_warning=False)

    def quote(self, chars):
        with self.db() as c:
            return self._quote(c, chars)

    def reserve(self, site, chars, request_id=None):
        if site not in {'paper-trail', 'dommydom', 'startweb7'} or type(chars) is not int or chars <= 0:
            raise ValueError('Invalid site or batch')
        identifier = request_id or uuid.uuid4().hex
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            quote = self._quote(c, chars)
            c.execute('INSERT INTO reservations VALUES(?,?,?,?,?)', (identifier, site, chars, time.time(), 'reserved'))
            c.commit()
        return {**quote, 'reservation': identifier}

    def finish(self, reservation, result):
        if result not in {'complete', 'partial', 'uncertain'}:
            raise ValueError('Invalid reservation outcome')
        with self.db() as c:
            c.execute('UPDATE reservations SET result=? WHERE id=?', (result, reservation))

    def status(self):
        with self.db() as c:
            row = c.execute('SELECT data FROM snapshot WHERE id=1').fetchone()
            return dict(snapshot=json.loads(row[0]) if row else None, reservations=[dict(r) for r in c.execute('SELECT * FROM reservations ORDER BY created')], historical_account_usage='Unknown; restored accounting does not claim an opening zero')

class ExistingBudget(Budget):
    def __init__(self, path, read_only=False):
        resolved = Path(path).resolve(strict=True)
        if not resolved.is_file():
            raise ValueError('Existing accounting database required')
        self.path, self.read_only = str(resolved), read_only

    @contextmanager
    def db(self):
        mode = 'ro' if self.read_only else 'rw'
        c = sqlite3.connect(Path(self.path).as_uri() + '?mode=' + mode, uri=True, timeout=30, isolation_level=None)
        c.row_factory = sqlite3.Row
        try:
            if self.read_only:
                c.execute('PRAGMA query_only=ON')
            yield c
        finally:
            if c.in_transaction:
                c.rollback()
            c.close()
