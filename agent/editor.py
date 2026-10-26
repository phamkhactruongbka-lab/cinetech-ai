"""Create stable source-attributed drafts; never publish."""
import hashlib
import logging
try:
    from .common import ROOT, read, save
    from .validate import validate
except ImportError:
    from common import ROOT, read, save
    from validate import validate
def make_drafts(data):
    validate(data)
    return [{'id': hashlib.sha256((i['url'] + '\n' + i['title']).encode()).hexdigest()[:16],
             'headline': i['title'], 'source_url': i['url'], 'source': i.get('source', ''),
             'status': 'needs_human_review', 'draft': 'Tiêu đề từ nguồn: ' + i['title'] + '. Hãy đọc bài gốc; đây không phải bài đánh giá trải nghiệm.'}
            for i in data['items'][:10]]
def main():
    drafts = make_drafts(read(ROOT/'data/research.json'))
    save(ROOT/'data/drafts.json', {'drafts': drafts})
    logging.info('Created %d drafts; nothing published', len(drafts))
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
