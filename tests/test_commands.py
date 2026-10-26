import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from agent.editor import make_drafts
ROOT = Path(__file__).resolve().parents[1]
class CommandTests(unittest.TestCase):
    def test_cli_approval_withdraw_and_sitemap(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            shutil.copytree(ROOT/'agent',root/'agent',ignore=shutil.ignore_patterns('__pycache__'))
            (root/'data').mkdir(); (root/'docs/data').mkdir(parents=True)
            draft=make_drafts({'items':[{'title':'Fixture','url':'https://example.org','status':'needs_review'}]})[0]
            (root/'data/drafts.json').write_text(json.dumps({'drafts':[draft]}))
            pub=root/'docs/data/published.json'; pub.write_text('{"items":[]}')
            def run(*args):
                return subprocess.run([sys.executable,'-X','utf8',*args],cwd=root,capture_output=True,text=True,encoding='utf-8')
            result=run('agent/publish.py','--id',draft['id'])
            self.assertNotEqual(result.returncode,0); self.assertEqual(json.loads(pub.read_text()),{'items':[]})
            result=run('agent/publish.py','--id',draft['id'],'--reviewer','Tester','--confirm-reviewed')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(pub.read_text())['items'][0]['status'],'approved')
            result=run('agent/publish.py','--id',draft['id'],'--withdraw')
            self.assertEqual(result.returncode,0,result.stderr); self.assertEqual(json.loads(pub.read_text())['items'],[])
            result=run('agent/configure_site.py','--url','https://example.org/project/')
            self.assertEqual(result.returncode,0,result.stderr)
            from xml.etree import ElementTree as ET
            links=[el.text for el in ET.parse(root/'docs/sitemap.xml').findall('.//{*}loc')]
            self.assertEqual(len(links),4); self.assertIn('https://example.org/project/lien-he.html',links)
            self.assertIn('https://example.org/project/sitemap.xml',(root/'docs/robots.txt').read_text())
            self.assertNotEqual(run('agent/configure_site.py','--url','javascript:1').returncode,0)
