"""Bounded deterministic agent pipeline. No LLM, paid API, or publication step."""
import argparse
import logging
from pathlib import Path
try:
    from .common import ROOT, now, read, save
    from .editor import make_drafts, update_drafts
    from .validate import require, validate, validate_catalog, validate_public
    from . import research
except ImportError:
    from common import ROOT, now, read, save
    from editor import make_drafts, update_drafts
    from validate import require, validate, validate_catalog, validate_public
    import research

def run(root=ROOT, collect=False, report_path=None):
    root = Path(root).resolve()
    report_path = Path(report_path) if report_path else root/'evidence/harness-latest.json'
    report = {'started_at': now(), 'status': 'running', 'mode': 'deterministic_no_llm',
              'collect_requested': collect, 'publication_performed': False, 'stages': []}
    stage = 'collect' if collect else 'validate_research'
    try:
        if collect:
            records = research.collect()
            require(bool(records), 'No fresh RSS items; existing research preserved')
            payload = {'updated_at': now(), 'items': records}
            validate(payload)
            save(root/'data/research.json', payload)
            report['stages'].append({'stage': stage, 'count': len(records), 'status': 'ok'})
        stage = 'validate_research'
        payload = read(root/'data/research.json')
        count = validate(payload)
        report['stages'].append({'stage': stage, 'count': count, 'status': 'ok'})
        stage = 'prepare_drafts'
        result = update_drafts(payload, root/'data/drafts.json')
        ids = {d['id'] for d in result['drafts']}
        deferred = sum(d['id'] not in ids for d in make_drafts(payload))
        report['stages'].append({'stage': stage, 'count': len(ids), 'deferred': deferred, 'status': 'ok'})
        for stage, filename, validator in (
            ('validate_public', 'docs/data/published.json', validate_public),
            ('validate_catalog', 'docs/data/products.json', validate_catalog),
        ):
            count = validator(read(root/filename))
            report['stages'].append({'stage': stage, 'count': count, 'status': 'ok'})
        report['status'] = 'success'
    except (ValueError, OSError, TypeError, KeyError) as exc:
        report['status'] = 'failed'
        report['stages'].append({'stage': stage, 'status': 'failed', 'error': str(exc)})
    report['finished_at'] = now()
    save(report_path, report)
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collect', action='store_true', help='Collect fresh RSS before validation; fail if none are returned')
    parser.add_argument('--report', default='evidence/harness-latest.json')
    args = parser.parse_args()
    try:
        path = (ROOT/args.report).resolve()
        require(path.is_relative_to((ROOT/'evidence').resolve()) and path.suffix == '.json',
                'report must be a JSON path inside evidence/')
        report = run(collect=args.collect, report_path=path)
        print('Harness ' + report['status'] + '; report: ' + str(path))
        return 0 if report['status'] == 'success' else 1
    except (ValueError, OSError) as exc:
        logging.error('Harness failed: %s', exc)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
