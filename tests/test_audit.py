import unittest
from pathlib import Path

from content_ops.audit import audit_summary, run_audit


class AuditTests(unittest.TestCase):
    def test_finish_up_audit_passes(self):
        root = Path(__file__).resolve().parents[1]
        results = run_audit(root)
        self.assertEqual(audit_summary(results)["status"], "pass")

    def test_public_sample_keeps_private_env_out_of_repo(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / ".env").exists())
        self.assertTrue((root / ".env.example").exists())


if __name__ == "__main__":
    unittest.main()
