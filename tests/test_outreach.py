import json
import tempfile
import unittest
from pathlib import Path
from agent.auto_outreach import run_auto_outreach


class OutreachTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.private = self.root.parent / 'business-private'
        self.private.mkdir()
        self.source = self.private / 'LEADS_2026-10-27.json'
        self.queue = self.private / 'outreach_queue.json'

    def source_data(self, leads):
        self.source.write_text(json.dumps({'leads': leads}), encoding='utf-8')

    def run_job(self, **kwargs):
        return run_auto_outreach(root=self.root, **kwargs)

    def test_missing_source_writes_nothing(self):
        self.assertEqual(self.run_job()['status'], 'blocked_missing_source')
        self.assertFalse(self.queue.exists())

    def test_private_drafts_not_ready(self):
        self.source_data([{'id': 'L01', 'name': 'Example'}])
        result = self.run_job()
        self.assertEqual(result['total_leads'], 1)
        self.assertEqual(result['status'], 'drafts_only_requires_authorization')
        self.assertEqual(result['leads'][0]['approval_status'], 'not_requested')
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertIn('CHƯA GỬI', (self.private / 'outreach_drafts.txt').read_text(encoding='utf-8'))

    def test_rerun_preserves_progress_and_removed_leads(self):
        self.source_data([{'id': 'L01', 'name': 'Old'}, {'id': 'L02', 'name': 'Other'}])
        initial = self.run_job()
        initial['leads'][0].update(status='replied', sent_at='2026-10-28', notes='Keep', deposit=123)
        self.queue.write_text(json.dumps(initial), encoding='utf-8')
        self.source_data([{'id': 'L01', 'name': 'Updated', 'status': 'researched_not_contacted'}])
        result = self.run_job()
        first, removed = result['leads']
        self.assertEqual((first['name'], first['status'], first['sent_at'], first['notes'], first['deposit']),
                         ('Updated', 'replied', '2026-10-28', 'Keep', 123))
        self.assertFalse(removed['in_current_source'])
        self.assertEqual(result['total_leads'], 1)

    def test_invalid_source_does_not_overwrite_queue(self):
        self.source_data([{'id': 'L01', 'name': 'Example'}])
        self.run_job()
        before = self.queue.read_bytes()
        self.source_data([{'id': 'L01', 'name': 'One'}, {'id': 'L01', 'name': 'Two'}])
        with self.assertRaises(ValueError):
            self.run_job()
        self.assertEqual(self.queue.read_bytes(), before)

    def test_injected_output_cannot_be_public(self):
        self.source_data([])
        with self.assertRaises(ValueError):
            self.run_job(queue_file=self.root / 'docs' / 'queue.json')

    def test_injected_paths(self):
        alternate = self.private / 'input.json'
        alternate.write_text('{"leads": []}', encoding='utf-8')
        self.run_job(leads_file=alternate, queue_file=self.private / 'custom.json',
                     dispatch_file=self.private / 'custom.txt')
        self.assertTrue((self.private / 'custom.json').exists())
        self.assertFalse(self.queue.exists())


if __name__ == '__main__':
    unittest.main()
