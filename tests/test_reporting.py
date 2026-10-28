import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock
from agent import report_generator as reporting


class Response(io.BytesIO):
    status = 200


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch_root = patch.object(reporting, 'ROOT', self.root)
        self.patch_root.start()
        self.addCleanup(self.patch_root.stop)
        (self.root/'data').mkdir()
        (self.root/'docs/data').mkdir(parents=True)
        (self.root/'data/cashflow.json').write_text(json.dumps({
            'updated_at': '2026-10-28', 'survival_milestone': {
                'current_cash_available': 100000, 'minimum_cash_required': 550000,
                'deadline_cash_collected': '2026-11-20'}, 'actual': {'expenses_incurred': 12000}}))
        (self.root/'docs/data/published.json').write_text('{"items": [{}, {}]}')
        (self.root/'docs/data/products.json').write_text('{"products": []}')

    def test_failed_probe_never_claims_http200_or_public_count(self):
        with patch.object(reporting.urllib.request, 'urlopen', side_effect=TimeoutError('timed out')) as opener, \
             patch.object(reporting, 'try_send_email') as send:
            report = reporting.generate_report()
        self.assertNotIn('HTTP 200', report)
        self.assertIn('endpoint công khai: Chưa xác minh', report)
        self.assertIn('file cục bộ: 2', report)
        self.assertIn('100,000 VNĐ', report)
        self.assertIn('12,000 VNĐ', report)
        self.assertIn('Chưa đối soát', report)
        self.assertTrue(all(c.kwargs['timeout'] == 10 for c in opener.call_args_list))
        send.assert_not_called()
        self.assertEqual((self.root/'reports/latest_email_draft.txt').read_text(encoding='utf-8'), report)

    def test_observed_public_count_separate_from_local(self):
        with patch.object(reporting.urllib.request, 'urlopen', side_effect=[Response(b'<html>'), Response(b'{"items": [{}]}')]):
            report = reporting.generate_report()
        self.assertIn('HTTP 200 (probe thực tế)', report)
        self.assertIn('endpoint công khai: 1', report)
        self.assertIn('file cục bộ: 2', report)

    def test_bad_public_json_does_not_infer_zero(self):
        with patch.object(reporting.urllib.request, 'urlopen', side_effect=[Response(b'ok'), Response(b'broken')]):
            result = reporting.probe_public_site()
        self.assertEqual(result['http_status'], 200)
        self.assertIsNone(result['published_count'])
        self.assertTrue(result['errors'])

    def test_timezone_and_calendar_days(self):
        class Clock(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2026, 10, 27, 18, 30, tzinfo=timezone.utc).astimezone(tz)
        with patch.object(reporting, 'datetime', Clock), \
             patch.object(reporting.urllib.request, 'urlopen', side_effect=TimeoutError()):
            report = reporting.generate_report()
        self.assertIn('28/10/2026 01:30:00 (UTC+7)', report)
        self.assertIn('Còn 23 ngày', report)
        self.assertTrue((self.root/'reports/report_20261028.txt').exists())

    def test_bad_cashflow_does_not_assert_zero_balance(self):
        (self.root/'data/cashflow.json').write_text('broken')
        with patch.object(reporting.urllib.request, 'urlopen', side_effect=TimeoutError()):
            report = reporting.generate_report()
        self.assertIn('Tiền mặt khả dụng khai báo: Chưa có dữ liệu hợp lệ', report)
        self.assertNotIn('Hết vốn hoàn toàn', report)

    def test_email_missing_configuration_and_bad_port_return_false(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(reporting.try_send_email('draft'))
        with patch.dict(os.environ, {'SMTP_USER': 'test@example.org', 'SMTP_PASSWORD': 'fixture', 'SMTP_PORT': 'bad'}, clear=True):
            self.assertFalse(reporting.try_send_email('draft'))

    def test_email_refusal_and_transport_failure_return_false(self):
        with patch.dict(os.environ, {'SMTP_USER': 'test@example.org', 'SMTP_PASSWORD': 'fixture'}, clear=True):
            with patch('smtplib.SMTP_SSL') as smtp:
                smtp.return_value.__enter__.return_value.sendmail.return_value = {'recipient': (550, b'rejected')}
                self.assertFalse(reporting.try_send_email('draft'))
                self.assertEqual(smtp.call_args.kwargs['timeout'], 15)
            with patch('smtplib.SMTP_SSL', side_effect=TimeoutError()):
                self.assertFalse(reporting.try_send_email('draft'))

    def test_email_only_returns_true_when_smtp_accepts(self):
        with patch.dict(os.environ, {'SMTP_USER': 'test@example.org', 'SMTP_PASSWORD': 'fixture'}, clear=True), patch('smtplib.SMTP_SSL') as smtp:
            smtp.return_value.__enter__.return_value.sendmail.return_value = {}
            self.assertTrue(reporting.try_send_email('draft'))


if __name__ == '__main__':
    unittest.main()
