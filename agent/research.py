"""CineTech research collector. Standard library only; no AI API required."""
import json
import logging
try:
    from .common import save, https_url
except ImportError:
    from common import save, https_url
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'research.json'
MAX_BYTES = 2_000_000
QUERIES = ['phim chiếu rạp Việt Nam', 'phim mới ra mắt điện ảnh']

def collect():
    items = []
    for query in QUERIES:
        params = urllib.parse.urlencode({'q': query, 'hl': 'vi', 'gl': 'VN', 'ceid': 'VN:vi'})
        url = 'https://news.google.com/rss/search?' + params
        request = urllib.request.Request(url, headers={'User-Agent': 'CineTechAIResearch/0.1 (personal educational project)'})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise ValueError("RSS exceeds size limit")
                root = ET.fromstring(raw)
            for item in root.findall('./channel/item')[:15]:
                title = (item.findtext('title') or '').strip()
                link = (item.findtext('link') or '').strip()
                if not title or not https_url(link):
                    continue
                source_el = item.find('source')
                source = (source_el.text or '').strip() if source_el is not None else ''
                raw_date = item.findtext('pubDate') or ''
                try:
                    date = parsedate_to_datetime(raw_date).astimezone(timezone.utc).isoformat()
                except (TypeError, ValueError, OverflowError):
                    date = ''
                items.append({'title': title, 'url': link, 'source': source, 'published_at': date, 'query': query, 'status': 'needs_review'})
        except (OSError, ET.ParseError, ValueError) as exc:
            logging.warning('RSS query %d unavailable: %s', QUERIES.index(query) + 1, exc)
    seen = set()
    seen_urls = set()
    unique = []
    for item in items:
        key = re.sub(r'\W+', '', item['title'].casefold())
        if key and key not in seen and item['url'] not in seen_urls:
            seen.add(key)
            seen_urls.add(item['url'])
            unique.append(item)
    unique.sort(key=lambda x: x['published_at'], reverse=True)
    return unique[:30]

def main():
    records = collect()
    if not records:
        print('No fresh items. Keeping previous research.json if present.')
        return
    payload = {'updated_at': datetime.now(timezone.utc).isoformat(), 'items': records}
    save(OUT, payload)
    logging.info('Saved %d private research headlines', len(records))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    main()
