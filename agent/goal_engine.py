"""Record actual execution and next steps; a plan never guarantees revenue."""
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent.autopilot import run_autonomous_pipeline

def execute_goal_cycle():
    result = run_autonomous_pipeline()
    stamp = datetime.now(timezone(timedelta(hours=7))).isoformat()
    entry = f'\n## {stamp}\n- Execution: {result["status"]}; details: reports/autopilot-latest.json.\n- No automatic publication or customer messages; report is a draft.\n- Next: verify sourced prospects, approve outreach scope, deliver paid work, record actual receipts.\n- Target: 550,000 VND available by 20/11/2026; not achieved by running this script.\n'
    with (ROOT/'GOAL_EXECUTION_LOG.md').open('a', encoding='utf-8') as stream:
        stream.write(entry)
    report = ROOT.parent/'BAO_CAO_TIEN_DO.md'
    if report.exists():
        with report.open('a', encoding='utf-8') as stream:
            stream.write(f'\n| {stamp} | Chu kỳ tự động | {result["status"]} | Xem reports/autopilot-latest.json; không tự đăng/gửi thư, không xác nhận thêm doanh thu |\n')
    return result

if __name__ == '__main__':
    raise SystemExit(0 if execute_goal_cycle()['status'] == 'success' else 1)
