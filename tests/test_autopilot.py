import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
from agent import autopilot
from agent.ceo_auto_approval import auto_review_and_publish

class AutopilotTests(unittest.TestCase):
    def test_legacy_approval_does_not_publish(self):
        with patch('pathlib.Path.write_text') as write:
            self.assertEqual(auto_review_and_publish(), [])
            write.assert_not_called()

    def test_failed_tests_stop_preparation(self):
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(autopilot, 'ROOT', Path(folder)), \
             patch.object(autopilot.subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='failed')), \
             patch.object(autopilot, 'run_harness') as harness, \
             patch.object(autopilot, 'run_auto_outreach') as outreach, \
             patch.object(autopilot, 'generate_report'):
            result = autopilot.run_autonomous_pipeline()
            self.assertEqual(result['status'], 'failed')
            harness.assert_not_called()
            outreach.assert_not_called()
            self.assertFalse(result['publication_performed'])
            self.assertFalse(result['email_sent'])

    def test_harness_failure_is_not_success(self):
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(autopilot, 'ROOT', Path(folder)), \
             patch.object(autopilot.subprocess, 'run', return_value=SimpleNamespace(returncode=0, stdout='', stderr='')), \
             patch.object(autopilot, 'run_harness', return_value={'status':'failed'}), \
             patch.object(autopilot, 'run_auto_outreach') as outreach, \
             patch.object(autopilot, 'generate_report'):
            result = autopilot.run_autonomous_pipeline()
            self.assertEqual(result['status'], 'failed')
            self.assertEqual(result['steps']['reporting']['status'], 'DRAFT_ONLY')
            outreach.assert_not_called()
