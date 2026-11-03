"""Check a drafted Teams message against the Teams message rules.

Run as `python3 -B teams_message.py --path <file>` (`python` on Windows). Exits 0 and prints the
character count when the draft passes; otherwise reports each problem by line and exits 1.
"""

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

_FENCE = re.compile(r"^\s*```")
_CODE_SPAN = re.compile(r"`[^`\n]+`")
_LINK = re.compile(r"\[(?P<label>[^\]\n]+)\]\((?P<url>https?://[^\s)]+)\)")
_URL = re.compile(r"https?://\S+")
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_BLOCKQUOTE = re.compile(r"^\s*>")
_BOLD = re.compile(r"\*\*|__")
_EM_DASH = "—"


class Problem(NamedTuple):
    line: int
    message: str


def _prose_problems(number: int, line: str) -> list[Problem]:
    problems: list[Problem] = []
    prose = _CODE_SPAN.sub("", line)
    for link in _LINK.finditer(prose):
        if _URL.match(link["label"].strip()):
            problems.append(Problem(number, "link text is a raw URL; describe the target instead"))
    if _URL.search(_LINK.sub("", prose)):
        problems.append(Problem(number, "raw URL; write it as [link text](url)"))
    if _HEADING.match(prose):
        problems.append(Problem(number, "heading"))
    if _LIST_ITEM.match(prose):
        problems.append(Problem(number, "list item"))
    if _BLOCKQUOTE.match(prose):
        problems.append(Problem(number, "blockquote"))
    if _BOLD.search(prose):
        problems.append(Problem(number, "bold"))
    if _EM_DASH in prose:
        problems.append(Problem(number, "em dash"))
    return problems


def check_message(text: str) -> list[Problem]:
    lines = text.split("\n")
    if not text.strip():
        return [Problem(1, "empty message")]
    if len(lines) > 1 and _FENCE.match(lines[0]) and lines[-1].strip() == "```":
        return [Problem(1, "the whole message is fenced; fence only a command")]
    problems: list[Problem] = []
    fence_start: int | None = None
    for number, line in enumerate(lines, start=1):
        if _FENCE.match(line):
            fence_start = number if fence_start is None else None
        elif fence_start is None:
            problems.extend(_prose_problems(number, line))
    if fence_start is not None:
        problems.append(Problem(fence_start, "unclosed code fence"))
    return problems


def read_draft(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").rstrip()


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a Teams message draft before it is copied.")
    parser.add_argument("--path", required=True, type=Path, help="Path to the UTF-8 draft file.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    path: Path = parse_args(argv).path
    try:
        text = read_draft(path)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Cannot read draft {path}: {error}", file=sys.stderr)
        return 1
    problems = check_message(text)
    for problem in problems:
        print(f"{path}:{problem.line}: {problem.message}", file=sys.stderr)
    if problems:
        return 1
    print(f"Teams message OK ({len(text)} chars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
