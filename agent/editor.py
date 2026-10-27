"""Create stable source-attributed drafts; never publish."""
import hashlib
import logging
try:
    from .common import ROOT, read, save
    from .validate import validate, require, https_url
except ImportError:
    from common import ROOT, read, save
    from validate import validate, require, https_url

MAX_DRAFTS = 200

def validate_drafts(data):
    require(isinstance(data, dict) and isinstance(data.get('drafts'), list), 'drafts must be a list')
    ids = set()
    require(len(data['drafts']) <= MAX_DRAFTS, 'draft queue exceeds 200; archive manually before continuing')
    for item in data['drafts']:
        require(isinstance(item, dict), 'draft must be an object')
        for field in ('id', 'headline', 'draft'):
            require(isinstance(item.get(field), str) and bool(item[field].strip()), field + ' required')
        require(item['id'] not in ids, 'duplicate draft id')
        ids.add(item['id'])
        require(item.get('status') == 'needs_human_review', 'draft must remain unapproved')
        require(https_url(item.get('source_url')), 'invalid draft source')
    return len(ids)

def update_drafts(data, path):
    """Keep every existing edit; a full queue defers new entries without eviction."""
    candidates = make_drafts(data)
    existing = read(path) if path.exists() else {'drafts': []}
    validate_drafts(existing)  # Fail before any write, including malformed JSON.
    result = dict(existing)
    result['drafts'] = list(existing['drafts'])
    ids = {item['id'] for item in result['drafts']}
    for item in candidates:
        if item['id'] not in ids and len(result['drafts']) < MAX_DRAFTS:
            result['drafts'].append(item)
            ids.add(item['id'])
    validate_drafts(result)
    save(path, result)
    return result
def make_drafts(data):
    validate(data)
    return [{'id': hashlib.sha256((i['url'] + '\n' + i['title']).encode()).hexdigest()[:16],
             'headline': i['title'], 'source_url': i['url'], 'source': i.get('source', ''),
             'status': 'needs_human_review', 'draft': 'Tiêu đề từ nguồn: ' + i['title'] + '. Hãy đọc bài gốc; đây không phải bài đánh giá trải nghiệm.'}
            for i in data['items'][:10]]
def main():
    drafts = update_drafts(read(ROOT/'data/research.json'), ROOT/'data/drafts.json')
    logging.info('Preserved/created %d drafts; nothing published', len(drafts['drafts']))
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
