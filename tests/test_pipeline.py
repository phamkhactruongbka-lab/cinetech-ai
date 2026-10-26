import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent import research
from agent.common import save, https_url
from agent.editor import make_drafts
from agent.publish import approve
from agent.validate import validate, validate_catalog, validate_public

ITEM = {'title': 'Tiêu đề kiểm thử', 'url': 'https://example.org/news', 'source': 'Fixture', 'status': 'needs_review'}
class PipelineTests(unittest.TestCase):
    def feed(self, xml):
        with patch('urllib.request.urlopen', side_effect=lambda *a, **kw: io.BytesIO(xml.encode())):
            return research.collect()
    def test_duplicate_title_and_url(self):
        xml = '<rss><channel><item><title>A</title><link>https://example.org/a</link></item><item><title>A</title><link>https://example.org/b</link></item><item><title>B</title><link>https://example.org/a</link></item></channel></rss>'
        self.assertEqual(len(self.feed(xml)), 1)
    def test_empty_feed(self):
        self.assertEqual(self.feed('<rss><channel/></rss>'), [])
    def test_malformed_feed(self):
        self.assertEqual(self.feed('<rss>'), [])
    def test_unsafe_feed(self):
        self.assertEqual(self.feed('<rss><channel><item><title>A</title><link>javascript:alert(1)</link></item></channel></rss>'), [])
    def test_timeout(self):
        with patch('urllib.request.urlopen', side_effect=TimeoutError('timeout')) as opener:
            self.assertEqual(research.collect(), [])
            self.assertEqual(opener.call_args.kwargs['timeout'], 20)
    def test_oversized_feed(self):
        self.assertEqual(self.feed('x' * (research.MAX_BYTES + 1)), [])
    def test_fallback_keeps_previous_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'research.json'; out.write_text('previous')
            with patch.object(research, 'OUT', out), patch.object(research, 'collect', return_value=[]):
                research.main()
            self.assertEqual(out.read_text(), 'previous')
    def test_new_data_written_privately(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'research.json'
            with patch.object(research, 'OUT', out), patch.object(research, 'collect', return_value=[ITEM]):
                research.main()
            self.assertEqual(validate(json.loads(out.read_text(encoding='utf-8'))), 1)
    def test_approval_required_and_with_content_snapshot(self):
        drafts = {'drafts': make_drafts({'items': [ITEM]})}
        pending = drafts['drafts'][0]; original = copy.deepcopy(pending)
        with self.assertRaises(ValueError): validate_public({'items': [pending]})
        with self.assertRaises(ValueError): approve(drafts, {'items': []}, pending['id'], '')
        with self.assertRaises(ValueError): approve(drafts, {'items': []}, 'missing', 'Tester')
        result = approve(drafts, {'items': []}, pending['id'], 'Tester')
        self.assertEqual(validate_public(result), 1)
        self.assertEqual(pending, original)
        pending['draft'] = 'changed after approval'
        self.assertNotEqual(result['items'][0]['draft'], pending['draft'])
        self.assertEqual(len(approve(drafts, result, pending['id'], 'Tester')['items']), 1)
    def test_stable_ids(self):
        self.assertEqual(make_drafts({'items':[ITEM]}), make_drafts({'items':[ITEM]}))
    def test_empty_drafts(self):
        self.assertEqual(make_drafts({'items':[]}), [])
    def test_url_validation(self):
        for value in (None, 'javascript:alert(1)', 'http://example.org', 'https://user:pass@example.org', 'https://example.org:bad', 'https://example.org/ a'):
            self.assertFalse(https_url(value))
    def test_catalog(self):
        p = {'id':'fixture','name':'Fixture only','category':'test','source_name':'Fixture','source_url':'https://example.org','verified_at':'2026-10-26T00:00:00+00:00','affiliate_url':None}
        self.assertEqual(validate_catalog({'schema_version':1,'products':[p]}),1)
        for key,value in [('verified_at',''),('source_url','http://example.org'),('affiliate_url','javascript:1')]:
            bad = dict(p); bad[key] = value
            with self.assertRaises(ValueError): validate_catalog({'schema_version':1,'products':[bad]})
    def test_atomic_utf8_write(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'test.json'; save(out, {'title':'Tiếng Việt'}); save(out, {'title':'Mới'})
            self.assertEqual(json.loads(out.read_text(encoding='utf-8')), {'title':'Mới'})
            self.assertEqual(len(list(Path(folder).iterdir())),1)
