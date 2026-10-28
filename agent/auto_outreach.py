"""Prepare private drafts from researched leads. Never sends messages."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIR = ROOT.parent / 'business-private'
QUEUE_FILE = PRIVATE_DIR / 'outreach_queue.json'
DISPATCH_FILE = PRIVATE_DIR / 'outreach_drafts.txt'


def _read_leads(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict) or not isinstance(data.get('leads'), list):
        raise ValueError('Expected an object with a leads list')
    seen = set()
    for lead in data['leads']:
        if not isinstance(lead, dict) or not isinstance(lead.get('id'), str) or not lead['id'].strip():
            raise ValueError('Each lead needs a nonempty string ID')
        if lead['id'] in seen:
            raise ValueError('Duplicate lead ID')
        seen.add(lead['id'])
    return data['leads']


def run_auto_outreach(*, root=None, private_dir=None, leads_file=None,
                      queue_file=None, dispatch_file=None):
    """Merge progress by ID; injected paths must remain private and distinct."""
    root = Path(root or ROOT).resolve()
    private = Path(private_dir or root.parent / 'business-private').resolve()
    source = Path(leads_file or private / 'LEADS_2026-10-27.json').resolve()
    queue = Path(queue_file or private / 'outreach_queue.json').resolve()
    drafts = Path(dispatch_file or private / 'outreach_drafts.txt').resolve()
    paths = (source, queue, drafts)
    if len(set(paths)) != 3 or any(p.is_relative_to(root) or not p.is_relative_to(private) for p in paths):
        raise ValueError('Distinct paths must remain in the private directory outside repository')
    if not source.exists():
        return {'total_leads': 0, 'status': 'blocked_missing_source'}
    researched = _read_leads(source)
    for lead in researched:
        if not isinstance(lead.get('name'), str) or not lead['name'].strip():
            raise ValueError('Researched lead needs a name')
    previous = _read_leads(queue) if queue.exists() else []
    by_id = {lead['id']: dict(lead) for lead in previous}
    for lead in researched:
        old = by_id.get(lead['id'], {})
        merged = {**lead, **old}
        for key in ('name', 'source', 'sector', 'social', 'email', 'evidence', 'checked_on', 'angle', 'priority'):
            if key in lead:
                merged[key] = lead[key]
        merged.setdefault('status', 'researched_not_contacted')
        merged.setdefault('approval_status', 'not_requested')
        merged['draft_status'] = 'needs_human_review'
        by_id[lead['id']] = merged
    active_ids = {lead['id'] for lead in researched}
    for lead in by_id.values():
        lead['in_current_source'] = lead['id'] in active_ids
    result = {
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'status': 'drafts_only_requires_authorization',
        'total_leads': len(researched),
        'retained_leads': len(by_id),
        'leads': list(by_id.values()),
    }
    text = ['BẢN NHÁP NỘI BỘ — CHƯA GỬI',
            'Cần duyệt người nhận, kênh, nội dung và chỉ thị gửi rõ ràng trước khi liên hệ.',
            'Trạng thái do người vận hành ghi nhận; chương trình không xác nhận đã gửi.']
    for lead in researched:
        item = by_id[lead['id']]
        text.extend(['', f"[{item['id']}] {item['name']}",
                     f"Trạng thái: {item['status']}",
                     f"Ý tưởng cần duyệt: {item.get('angle', 'Chưa xác định nhu cầu')}",
                     f"Xin chào {item['name']}, bên mình hỗ trợ biên soạn nội dung sản phẩm. "
                     'Anh/chị có nhu cầu trao đổi với người phụ trách nội dung không?'])
    queue.parent.mkdir(parents=True, exist_ok=True)
    drafts.parent.mkdir(parents=True, exist_ok=True)
    queue.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    drafts.write_text('\n'.join(text) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    summary = run_auto_outreach()
    print(f"{summary['status']}: {summary['total_leads']} leads; no messages sent")
