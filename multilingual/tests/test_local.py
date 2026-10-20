import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from multilingual import local_generate as local
from multilingual.site import key

class LocalGenerationTests(unittest.TestCase):
    def test_batching_preserves_content_and_provider_bounds(self):
        texts=['a'*2000,'b'*2000,'c'*2000,'d'*6000]
        groups=list(local.batches(texts))
        self.assertEqual([t for group in groups for t in group],texts)
        self.assertEqual(list(map(len,groups)),[2,1,1])
        with self.assertRaises(ValueError):list(local.batches(['a'*30001]))

    def test_durable_reservation_blocks_duplicate_paid_requests(self):
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder)
            with patch.object(local,'STATE',state),patch.object(local,'DB',state/'cache.db'):
                local.initialize();local.reserve('es',['Hello world'],True)
                with self.assertRaisesRegex(RuntimeError,'duplicate'):local.reserve('es',['Hello world'],True)
                with local.connect() as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM requests').fetchone()[0],1)
                    self.assertEqual(db.execute('SELECT status FROM segments').fetchone()[0],'reserved')

    def test_checkpoint_keeps_completed_translations_after_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder);output=state/'translations.json';output.write_text('{}')
            with patch.object(local,'STATE',state),patch.object(local,'DB',state/'cache.db'),patch.object(local,'OUTPUT',output):
                local.initialize();identifier=local.reserve('es',['Hello world'],True)
                with local.connect() as db:db.execute("UPDATE segments SET status='complete',result='Hola mundo'")
                local.checkpoint()
                self.assertEqual(json.loads(output.read_text())[key('Hello world','es')],'Hola mundo')

    def test_override_is_explicit_and_normal_limit_remains_enforced(self):
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder)
            with patch.object(local,'STATE',state),patch.object(local,'DB',state/'cache.db'):
                local.initialize()
                with patch.object(local,'cost_units',return_value=21_000_000):
                    with self.assertRaisesRegex(RuntimeError,'Monthly limit'):local.reserve('es',['Hello world'],False)
                    self.assertTrue(local.reserve('es',['Hello world'],True))
