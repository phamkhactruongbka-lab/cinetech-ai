"""Run checks and prepare drafts/reports; never publish or contact customers."""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent.harness import run as run_harness
from agent.report_generator import generate_report
from agent.auto_outreach import run_auto_outreach

def run_autonomous_pipeline(collect=False):
    result = {'timestamp': datetime.now(timezone(timedelta(hours=7))).isoformat(),
              'status': 'success', 'publication_performed': False,
              'email_sent': False, 'steps': {}}
    for name, command in (
        ('python_tests', [sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'tests', '-q']),
        ('dom_tests', ['node', 'tests/test_dom.cjs']),
    ):
        try:
            check = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                   encoding='utf-8', errors='replace', timeout=120)
            result['steps'][name] = {'status': 'PASS' if check.returncode == 0 else 'FAIL',
                                    'returncode': check.returncode,
                                    'output': (check.stdout + check.stderr)[-8000:]}
        except (OSError, subprocess.TimeoutExpired) as exc:
            result['steps'][name] = {'status': 'FAIL', 'error': str(exc)}
        if result['steps'][name]['status'] != 'PASS':
            result['status'] = 'failed'
            break
    if result['status'] == 'success':
        try:
            harness = run_harness(collect=collect)
            result['steps']['harness'] = harness
            if harness['status'] != 'success':
                result['status'] = 'failed'
            else:
                result['steps']['sales_preparation'] = run_auto_outreach()
        except (OSError, ValueError, TypeError, KeyError) as exc:
            result['status'] = 'failed'
            result['steps']['preparation'] = {'status': 'FAIL', 'error': str(exc)}
    try:
        generate_report()
        result['steps']['reporting'] = {'status': 'DRAFT_ONLY', 'sent': False}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result['status'] = 'failed'
        result['steps']['reporting'] = {'status': 'FAIL', 'error': str(exc)}
    destination = ROOT / 'reports/autopilot-latest.json'
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Autopilot ' + result['status'] + '; no publication or email sent.')
    return result

if __name__ == '__main__':
    raise SystemExit(0 if run_autonomous_pipeline('--collect' in sys.argv)['status'] == 'success' else 1)
