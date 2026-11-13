import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

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
        text = "I've finished [AuthZ design](https://example.com/101) and [Worker rollout](https://example.com/102), `example-service` changed."
        self.assertEqual(messages(text), [])

    def test_generic_or_plural_link_text_is_rejected(self):
        for label in ("here", "This link", "these two pages", "both docs", "all of them"):
            with self.subTest(label=label):
                self.assertEqual(
                    messages(f"see [{label}](https://example.com/101)"),
                    [(1, f"link text '{label}' must name one target, such as its page title")],
                )

    def test_link_text_that_only_starts_like_a_plural_word_passes(self):
        self.assertEqual(messages("see [Allocation design](https://example.com/101)"), [])

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
        copy = "copy_windows" if TEAMS_MESSAGE.IS_WINDOWS else "copy_posix"
        patcher = mock.patch.object(TEAMS_MESSAGE, copy, return_value="Copied 35 chars, 0 code spans, 1 links.")
        self.copy = patcher.start()
        self.addCleanup(patcher.stop)

    def run_main(self, text):
        path = Path(self.temp.name) / "draft.md"
        path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = TEAMS_MESSAGE.main(["--path", str(path)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_a_clean_draft_is_copied_once_and_the_copy_result_is_reported(self):
        result = self.run_main("see [the page](https://example.com)\r\n")
        self.assertEqual(result, (0, "Copied 35 chars, 0 code spans, 1 links.\n", ""))
        self.copy.assert_called_once_with("see [the page](https://example.com)")

    def test_a_broken_draft_never_reaches_the_clipboard(self):
        code, stdout, stderr = self.run_main("hi\nsee https://example.com")
        self.assertEqual((code, stdout), (1, ""))
        self.assertIn("draft.md:2: raw URL", stderr)
        self.copy.assert_not_called()

    def test_a_failed_copy_is_reported_and_exits_non_zero(self):
        self.copy.side_effect = TEAMS_MESSAGE.ClipboardError("Clipboard verification failed: links did not round-trip.")
        self.assertEqual(
            self.run_main("see [the page](https://example.com)"),
            (1, "", "Clipboard verification failed: links did not round-trip.\n"),
        )

    def test_a_missing_draft_fails(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = TEAMS_MESSAGE.main(["--path", str(Path(self.temp.name) / "missing.md")])
        self.assertEqual(code, 1)
        self.assertIn("Draft file not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
