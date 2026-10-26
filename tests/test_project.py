import json,unittest
from pathlib import Path
from agent.validate import validate
from agent.research import collect
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def test_seed_data(self):
  self.assertGreaterEqual(validate(json.loads((ROOT/'data/research.json').read_text(encoding='utf-8'))),0)
 def test_no_network_does_not_crash(self):
  with patch('urllib.request.urlopen',side_effect=OSError('offline')):
   self.assertEqual(collect(),[])
 def test_site_files(self):
  for file in ['index.html','app.js','style.css','chooser.js']:
   self.assertTrue((ROOT/'docs'/file).is_file())
 def test_reject_insecure_link(self):
  with self.assertRaises(ValueError):validate({'items':[{'title':'Fake','url':'javascript:alert(1)','status':'needs_review'}]})
if __name__=='__main__':unittest.main()
