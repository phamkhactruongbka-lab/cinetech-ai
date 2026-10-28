"""Evidence-based local reports. Email is sent only by explicit caller action."""
import json
import math
import os
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_TIMEZONE = timezone(timedelta(hours=7))
PUBLIC_URL = 'https://phamkhactruongbka-lab.github.io/cinetech-ai/'


def read_object(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(value, dict):
            raise ValueError('JSON root must be an object')
        return value, None
    except (OSError, ValueError) as exc:
        return {}, str(exc)


def item_count(data, key):
    values = data.get(key)
    return len(values) if isinstance(values, list) else None


def probe_public_site():
    """Report independent observed page and public JSON results, never defaults."""
    result = {'http_status': None, 'published_count': None, 'errors': []}
    for suffix in ('', 'data/published.json'):
        try:
            request = urllib.request.Request(PUBLIC_URL + suffix, headers={'User-Agent': 'CineTechReport/1.0'})
            with urllib.request.urlopen(request, timeout=10) as response:
                status = response.status
                if not suffix:
                    result['http_status'] = status
                else:
                    if status != 200:
                        raise ValueError('publication endpoint HTTP ' + str(status))
                    raw = response.read(1_000_001)
                    if len(raw) > 1_000_000:
                        raise ValueError('publication endpoint exceeds size limit')
                    payload = json.loads(raw)
                    if not isinstance(payload, dict) or not isinstance(payload.get('items'), list):
                        raise ValueError('invalid publication JSON')
                    result['published_count'] = len(payload['items'])
        except (OSError, ValueError, TypeError) as exc:
            result['errors'].append(('public JSON' if suffix else 'website') + ': ' + str(exc))
    return result


def money(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        return f'{value:,.0f} VNĐ'
    return 'Chưa có dữ liệu hợp lệ'


def generate_report():
    cashflow, cash_error = read_object(ROOT/'data/cashflow.json')
    local, local_error = read_object(ROOT/'docs/data/published.json')
    catalog, catalog_error = read_object(ROOT/'docs/data/products.json')
    public = probe_public_site()
    now = datetime.now(LOCAL_TIMEZONE)
    milestone = cashflow.get('survival_milestone', {})
    milestone = milestone if isinstance(milestone, dict) else {}
    actual = cashflow.get('actual', {})
    actual = actual if isinstance(actual, dict) else {}
    collected = milestone.get('current_cash_available')
    target = milestone.get('minimum_cash_required')
    valid_amounts = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in (collected, target))
    shortfall = max(0, target - collected) if valid_amounts else None
    deadline_text = milestone.get('deadline_cash_collected')
    try:
        deadline = date.fromisoformat(deadline_text)
        deadline_display = f'{deadline.strftime("%d/%m/%Y")} (Còn {max(0, (deadline - now.date()).days)} ngày)'
    except (TypeError, ValueError):
        deadline_display = 'Chưa có ngày hợp lệ trong dữ liệu'
    def count_text(value):
        return str(value) if value is not None else 'Chưa xác minh'
    http_text = ('HTTP ' + str(public['http_status']) + ' (probe thực tế)') if public['http_status'] is not None else 'Chưa xác minh được HTTP'
    errors = [e for e in (cash_error, local_error, catalog_error) if e] + public['errors']
    documents = '\n'.join('- ' + filename + ': ' + ('Có file cục bộ; chưa đánh giá chất lượng' if (ROOT/'sales'/filename).is_file() else 'Chưa tìm thấy')
                          for filename in ('SERVICE_KIT.md', 'SAMPLE_PORTFOLIO.md', 'LEADS_TRACKER.md'))
    report_content = f'''BÁO CÁO TIẾN ĐỘ CINETECH AI
Thời điểm: {now.strftime('%d/%m/%Y %H:%M:%S')} (UTC+7)

1. TÀI CHÍNH THEO DỮ LIỆU KHAI BÁO
Nguồn: data/cashflow.json; cập nhật: {cashflow.get('updated_at', 'không rõ')}.
Chưa đối soát ngân hàng, hóa đơn hoặc kiểm toán độc lập.
- Mục tiêu thực thu tối thiểu: {money(target)}
- Tiền mặt khả dụng khai báo: {money(collected)}
- Khoản còn thiếu theo dữ liệu: {money(shortfall)}
- Chi phí đã phát sinh khai báo: {money(actual.get('expenses_incurred'))}
- Hạn chót tiền về: {deadline_display}
- Mục tiêu bán hàng khai báo: {money(milestone.get('experimental_sales_target'))}

2. VẬN HÀNH
- Website {PUBLIC_URL}: {http_text}
- Số mục bài viết trong file cục bộ: {count_text(item_count(local, 'items'))}
- Số mục bài viết tại endpoint công khai: {count_text(public['published_count'])}
- Số sản phẩm trong catalog cục bộ: {count_text(item_count(catalog, 'products'))}; chưa đối chiếu lại nguồn trong lượt báo cáo này.
- HTTP phản hồi không xác nhận toàn bộ chức năng hoặc chất lượng nội dung.

3. TÀI LIỆU BÁN HÀNG
{documents}

4. HÀNH ĐỘNG TIẾP THEO
- Đối chiếu nguồn, duyệt nội dung; kiểm tra cơ hội bán hàng và cập nhật số liệu thực thu.
- Báo cáo này chỉ lưu cục bộ; việc gửi email cần hành động riêng.

Lỗi hoặc dữ liệu chưa đọc được: {chr(10).join(errors) if errors else 'Không ghi nhận lỗi đọc/probe trong lượt này.'}
'''
    reports_dir = ROOT/'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir/f'report_{now.strftime("%Y%m%d")}.txt'
    report_path.write_text(report_content, encoding='utf-8')
    (reports_dir/'latest_email_draft.txt').write_text(report_content, encoding='utf-8')
    print(f'Báo cáo đã lưu: {report_path}; chưa gửi email.')
    return report_content


def load_env_file():
    env_file = ROOT/'.env'
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        except OSError:
            pass


def try_send_email(content, recipient='truong.arsenal.91@gmail.com'):
    """Explicit send operation; False means not confirmed sent, including refusal."""
    try:
        load_env_file()
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASSWORD')
        if not smtp_user or not smtp_pass:
            print('Thiếu cấu hình SMTP; chưa gửi email.')
            return False
        smtp_port = int(os.getenv('SMTP_PORT', '465'))
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = '[CineTech AI] Báo cáo ' + datetime.now(LOCAL_TIMEZONE).strftime('%d/%m/%Y')
        msg['From'] = smtp_user
        msg['To'] = recipient
        with smtplib.SMTP_SSL(os.getenv('SMTP_HOST', 'smtp.gmail.com'), smtp_port, timeout=15) as server:
            server.login(smtp_user, smtp_pass)
            refused = server.sendmail(smtp_user, [recipient], msg.as_string())
            if refused:
                print('Máy chủ từ chối người nhận; chưa gửi email.')
                return False
        print('Máy chủ SMTP đã chấp nhận email; chưa xác nhận giao đến hộp thư.')
        return True
    except Exception as exc:
        print('Không xác nhận gửi email: ' + type(exc).__name__)
        return False


if __name__ == '__main__':
    generate_report()
