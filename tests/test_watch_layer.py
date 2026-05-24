import tempfile
import unittest
from pathlib import Path

from content_ops.watch_layer import decide_wake, scan_content_package


class WatchLayerTests(unittest.TestCase):
    def test_topic_research_change_wakes_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "topic_research.md").write_text("new source signal\n", encoding="utf-8")
            decision = decide_wake(scan_content_package(root))
            self.assertTrue(decision["wakeAgent"])
            self.assertEqual(decision["nextAction"], "wake_agent")

    def test_wechat_failure_requests_safe_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wechat_api.failed").write_text("draft upload failed\n", encoding="utf-8")
            decision = decide_wake(scan_content_package(root))
            self.assertTrue(decision["wakeAgent"])
            self.assertEqual(decision["nextAction"], "wake_agent_for_safe_retry")

    def test_draft_only_change_keeps_agent_sleeping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "article.html").write_text("<p>draft</p>\n", encoding="utf-8")
            decision = decide_wake(scan_content_package(root))
            self.assertFalse(decision["wakeAgent"])
            self.assertEqual(decision["nextAction"], "keep_sleeping")


if __name__ == "__main__":
    unittest.main()

