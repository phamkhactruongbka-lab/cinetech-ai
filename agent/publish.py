"""Explicit local human approval; not called by scheduled workflows."""
import argparse
try:
    from .common import ROOT, read, save, now
    from .validate import require, validate_public, https_url
except ImportError:
    from common import ROOT, read, save, now
    from validate import require, validate_public, https_url
def approve(drafts, published, article_id, reviewer):
    require(bool(reviewer.strip()), 'reviewer required')
    validate_public(published)
    matches = [d for d in drafts['drafts'] if d.get('id') == article_id]
    require(len(matches) == 1, 'draft id missing or ambiguous')
    item = dict(matches[0])
    require(item.get('status') == 'needs_human_review' and https_url(item.get('source_url')), 'invalid draft')
    item.update(status='approved', approved_by=reviewer.strip(), approved_at=now())
    result = {'updated_at': now(), 'items': [p for p in published['items'] if p['id'] != article_id] + [item]}
    validate_public(result)
    return result
def main():
    parser = argparse.ArgumentParser(description='Duyệt bản nháp sau khi đọc nguồn và kiểm tra bản quyền.')
    parser.add_argument('--id', required=True)
    parser.add_argument('--reviewer')
    parser.add_argument('--confirm-reviewed', action='store_true')
    parser.add_argument('--withdraw', action='store_true')
    args = parser.parse_args()
    path = ROOT/'docs/data/published.json'
    current = read(path)
    if args.withdraw:
        validate_public(current)
        require(any(p['id'] == args.id for p in current['items']), 'published id not found')
        result = {'updated_at': now(), 'items': [p for p in current['items'] if p['id'] != args.id]}
    else:
        if not args.confirm_reviewed or not args.reviewer:
            parser.error('--reviewer and --confirm-reviewed required after human review')
        result = approve(read(ROOT/'data/drafts.json'), current, args.id, args.reviewer)
    save(path, result)
    print('Updated local publication file; deploy separately.')
if __name__ == '__main__':
    main()
