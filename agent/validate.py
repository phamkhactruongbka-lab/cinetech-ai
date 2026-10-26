"""Fail closed on malformed research, products and publication data."""
import logging
try:
    from .common import ROOT, read, https_url
except ImportError:
    from common import ROOT, read, https_url
from datetime import datetime
def require(condition, message):
    if not condition:
        raise ValueError(message)
def timestamp(value):
    try:
        return isinstance(value, str) and datetime.fromisoformat(value).tzinfo is not None
    except ValueError:
        return False
def validate(data):
    require(isinstance(data, dict) and isinstance(data.get('items'), list), 'items must be a list')
    for item in data['items']:
        require(isinstance(item, dict), 'item must be an object')
        require(isinstance(item.get('title'), str) and bool(item['title'].strip()), 'title required')
        require(https_url(item.get('url')), 'HTTPS source required')
        require(item.get('status') == 'needs_review', 'research must remain unapproved')
    return len(data['items'])
def validate_catalog(data):
    require(isinstance(data, dict) and data.get('schema_version') == 1 and isinstance(data.get('products'), list), 'invalid catalog')
    ids = set()
    for p in data['products']:
        require(isinstance(p, dict), 'product must be an object')
        for field in ('id', 'name', 'category', 'source_name'):
            require(isinstance(p.get(field), str) and bool(p[field].strip()), field + ' required')
        require(p['id'] not in ids, 'duplicate product id'); ids.add(p['id'])
        require(https_url(p.get('source_url')), 'invalid product source')
        require(timestamp(p.get('verified_at')), 'verification timestamp required')
        require(p.get('affiliate_url') is None or https_url(p['affiliate_url']), 'invalid affiliate URL')
    return len(data['products'])
def validate_public(data):
    require(isinstance(data, dict) and isinstance(data.get('items'), list), 'invalid publication')
    ids = set()
    for p in data['items']:
        require(isinstance(p, dict), 'invalid article')
        for field in ('id', 'headline', 'draft', 'approved_by'):
            require(isinstance(p.get(field), str) and bool(p[field].strip()), field + ' required')
        require(p['id'] not in ids, 'duplicate article'); ids.add(p['id'])
        require(p.get('status') == 'approved' and timestamp(p.get('approved_at')), 'human approval required')
        require(https_url(p.get('source_url')), 'invalid source')
    return len(data['items'])
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info('Research: %s; catalog: %s; published: %s', validate(read(ROOT/'data/research.json')), validate_catalog(read(ROOT/'docs/data/products.json')), validate_public(read(ROOT/'docs/data/published.json')))
    except (ValueError, OSError, TypeError) as exc:
        logging.error('Validation failed: %s', exc)
        raise SystemExit(1)
