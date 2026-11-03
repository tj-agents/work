import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/teams/utility/message/scripts/teams_message.py"
SPEC = importlib.util.spec_from_file_location("teams_message", SCRIPT)
TEAMS_MESSAGE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TEAMS_MESSAGE
SPEC.loader.exec_module(TEAMS_MESSAGE)


def messages(text):
    return [(problem.line, problem.message) for problem in TEAMS_MESSAGE.check_message(text)]


class CheckMessageTests(unittest.TestCase):
    def test_a_message_with_link_text_and_code_spans_passes(self):
        text = "I've been working on [these two pages](https://example.com/pr/412), the `OrderSummary` grid changed."
        self.assertEqual(messages(text), [])

    def test_a_raw_url_is_rejected(self):
        self.assertEqual(messages("PR is in https://example.com/pr/412 now"), [(1, "raw URL; write it as [link text](url)")])

    def test_link_text_that_is_the_url_is_rejected(self):
        self.assertEqual(
            messages("[https://example.com/pr/412](https://example.com/pr/412) is in"),
            [(1, "link text is a raw URL; describe the target instead")],
        )

    def test_urls_inside_code_spans_and_command_fences_are_allowed(self):
        text = "Run this against `https://example.com`:\n```\ncurl https://example.com/health\n```\nThanks."
        self.assertEqual(messages(text), [])

    def test_headings_lists_quotes_bold_and_em_dashes_are_reported_with_their_lines(self):
        text = "# Update\n- one\n2. two\n> quoted\nthis is **bold**\nwait — no"
        self.assertEqual(
            messages(text),
            [(1, "heading"), (2, "list item"), (3, "list item"), (4, "blockquote"), (5, "bold"), (6, "em dash")],
        )

    def test_a_fenced_whole_message_is_rejected(self):
        self.assertEqual(messages("```\nhello there\n```"), [(1, "the whole message is fenced; fence only a command")])

    def test_an_unclosed_fence_is_rejected(self):
        self.assertEqual(messages("Run:\n```\nmake test"), [(2, "unclosed code fence")])

    def test_an_empty_message_is_rejected(self):
        self.assertEqual(messages("  \n "), [(1, "empty message")])


class MainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def run_main(self, text):
        path = Path(self.temp.name) / "draft.md"
        path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = TEAMS_MESSAGE.main(["--path", str(path)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_a_clean_draft_passes_with_its_character_count(self):
        self.assertEqual(self.run_main("see [the page](https://example.com)\r\n"), (0, "Teams message OK (35 chars).\n", ""))

    def test_a_broken_draft_fails_naming_each_line(self):
        code, stdout, stderr = self.run_main("hi\nsee https://example.com")
        self.assertEqual((code, stdout), (1, ""))
        self.assertIn("draft.md:2: raw URL", stderr)

    def test_a_missing_draft_fails(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = TEAMS_MESSAGE.main(["--path", str(Path(self.temp.name) / "missing.md")])
        self.assertEqual(code, 1)
        self.assertIn("Cannot read draft", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
