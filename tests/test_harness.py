import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent.common import ROOT, read, save
from agent.editor import MAX_DRAFTS, make_drafts, update_drafts
from agent.harness import run

ITEM = {'title': 'Fixture', 'url': 'https://example.org/news', 'status': 'needs_review'}

class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        save(self.root/'data/research.json', {'items': [ITEM]})
        save(self.root/'docs/data/published.json', {'items': []})
        save(self.root/'docs/data/products.json', {'schema_version': 1, 'products': []})

    def test_manual_edits_and_old_entries_survive_reruns(self):
        path = self.root/'data/drafts.json'
        original = update_drafts({'items': [ITEM]}, path)
        original['drafts'][0].update(headline='Edited title', draft='Original human prose', notes='retain')
        save(path, original)
        update_drafts({'items': [ITEM]}, path)
        self.assertEqual(read(path), original)
        update_drafts({'items': []}, path)
        self.assertEqual(read(path), original)

    def test_invalid_existing_drafts_never_overwritten(self):
        path = self.root/'data/drafts.json'
        for invalid in ('{bad json', '{"drafts":[{"id":"broken"}]}'):
            path.parent.mkdir(exist_ok=True)
            path.write_text(invalid)
            report = run(self.root)
            self.assertEqual(report['status'], 'failed')
            self.assertEqual(path.read_text(), invalid)
            self.assertEqual(report['stages'][-1]['stage'], 'prepare_drafts')

    def test_bound_defers_new_drafts_without_losing_edits(self):
        path = self.root/'data/drafts.json'
        prototype = make_drafts({'items': [ITEM]})[0]
        queue = {'drafts': [dict(prototype, id=str(i), draft='Edited '+str(i)) for i in range(MAX_DRAFTS)]}
        save(path, queue)
        report = run(self.root)
        self.assertEqual(read(path), queue)
        self.assertEqual(report['stages'][1]['deferred'], 1)

    def test_success_has_timestamps_and_never_changes_publication(self):
        pub = self.root/'docs/data/published.json'
        before = pub.read_bytes()
        with patch('agent.research.collect', side_effect=AssertionError('network not requested')):
            report = run(self.root)
        self.assertEqual(report['status'], 'success')
        self.assertFalse(report['publication_performed'])
        self.assertIn('finished_at', report)
        self.assertEqual(pub.read_bytes(), before)
        self.assertEqual(read(self.root/'evidence/harness-latest.json'), report)

    def test_invalid_publication_fails(self):
        save(self.root/'docs/data/published.json', {'items': make_drafts({'items': [ITEM]})})
        report = run(self.root)
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['stages'][-1]['stage'], 'validate_public')

    def test_failed_collect_preserves_old_research(self):
        path = self.root/'data/research.json'
        before = path.read_bytes()
        with patch('agent.research.collect', return_value=[]):
            report = run(self.root, collect=True)
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(path.read_bytes(), before)

    def test_cli_review_queue_and_reject_traversal(self):
        shutil.copytree(ROOT/'agent', self.root/'agent', ignore=shutil.ignore_patterns('__pycache__'))
        draft = make_drafts({'items': [ITEM]})[0]
        draft['draft'] = 'Reviewed editorial text'
        save(self.root/'data/review_queue.json', {'drafts': [draft]})
        def command(*args):
            return subprocess.run([sys.executable, str(self.root/'agent/publish.py'), '--id', draft['id'],
                                   '--reviewer', 'Human', '--confirm-reviewed', *args],
                                  cwd=self.root.parent, capture_output=True, text=True)
        failed = command('--drafts', '../outside.json')
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(read(self.root/'docs/data/published.json')['items'], [])
        result = command('--drafts', 'data/review_queue.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(read(self.root/'docs/data/published.json')['items'][0]['draft'], draft['draft'])

    def test_cli_failure_exit_and_report(self):
        shutil.copytree(ROOT/'agent', self.root/'agent', ignore=shutil.ignore_patterns('__pycache__'))
        save(self.root/'data/research.json', {'items': [{'title': 'Unsafe', 'url': 'http://example.org'}]})
        result = subprocess.run([sys.executable, str(self.root/'agent/harness.py')],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(read(self.root/'evidence/harness-latest.json')['status'], 'failed')
        self.assertFalse((self.root/'data/drafts.json').exists())

if __name__ == '__main__':
    unittest.main()
