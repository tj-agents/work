import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/work/utility/draft-comment/scripts/post_pending_review.py"


def load_script():
    spec = importlib.util.spec_from_file_location("post_pending_review", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PostPendingReviewTests(unittest.TestCase):
    def setUp(self):
        self.module = load_script()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.payload_path = Path(self.temporary_directory.name) / "payload.json"

    def write_payload(self, payload):
        self.payload_path.write_text(json.dumps(payload), encoding="utf-8")

    def run_main(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = self.module.main(["owner/repo", "42", str(self.payload_path)])
        return status, stdout.getvalue(), stderr.getvalue()

    def test_refuses_event_before_calling_github(self):
        self.write_payload({"event": "COMMENT"})
        with mock.patch.object(self.module, "gh_json") as gh_json:
            status, _, stderr = self.run_main()
        self.assertEqual(1, status)
        self.assertIn("must not contain event", stderr)
        gh_json.assert_not_called()

    def test_refuses_a_non_pending_response(self):
        self.write_payload({"body": "Finding"})
        with mock.patch.object(
            self.module,
            "gh_json",
            side_effect=[[], {"id": 42, "html_url": "https://example.test/review", "state": "COMMENTED"}],
        ):
            status, _, stderr = self.run_main()
        self.assertEqual(1, status)
        self.assertIn("did not create a PENDING review", stderr)

    def test_refuses_to_add_to_an_existing_pending_review(self):
        self.write_payload({"body": "Finding"})
        with mock.patch.object(self.module, "gh_json", return_value=[{"state": "PENDING"}]) as gh_json:
            status, _, stderr = self.run_main()
        self.assertEqual(1, status)
        self.assertIn("pending review already exists", stderr)
        gh_json.assert_called_once()

    def test_prints_the_pending_review_id_and_url(self):
        self.write_payload({"body": "Finding"})
        with mock.patch.object(
            self.module,
            "gh_json",
            side_effect=[[], {"id": 42, "html_url": "https://example.test/review", "state": "PENDING"}],
        ):
            status, stdout, stderr = self.run_main()
        self.assertEqual(0, status)
        self.assertEqual("Pending review 42: https://example.test/review\n", stdout)
        self.assertEqual("", stderr)
