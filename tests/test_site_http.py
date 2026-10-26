"""HTTP smoke test for the locally hosted static website."""
import functools
import http.server
import json
from pathlib import Path
import threading
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1] / 'docs'

class WebsiteHTTPTest(unittest.TestCase):
    def test_site_and_json_serve(self):
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f'http://127.0.0.1:{server.server_port}'
            with urllib.request.urlopen(base + '/index.html', timeout=5) as response:
                html = response.read().decode('utf-8')
                self.assertIn('CineTech AI', html)
            with urllib.request.urlopen(base + '/data/published.json', timeout=5) as response:
                payload = json.load(response)
                self.assertIn('items', payload)
        finally:
            server.shutdown()
            server.server_close()
