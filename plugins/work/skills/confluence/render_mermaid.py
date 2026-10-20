import argparse
import json
import re
import time
import uuid
from pathlib import Path


def macro(source: str) -> str:
    if re.search(r"[\"'&]", source):
        raise ValueError("keep Mermaid free of quotes and ampersands")
    body = [{"body": source.replace("\n", "\r\n"), "date": int(time.time() * 1000)}]
    params = {
        "macroParams": {
            "look": {"value": "classic"},
            "theme": {"value": "default"},
            "alignment": {"value": "left"},
            "__bodyContent": {"value": json.dumps(body, ensure_ascii=False)},
        },
        "macroMetadata": {"macroId": {"value": str(uuid.uuid4())}, "schemaVersion": {"value": "1"}, "title": "Mermaid diagram"},
    }
    return ('<div data-type="extension" data-extension-key="confluence-mermaid-macro" '
            'data-extension-type="com.atlassian.confluence.macro.core" data-layout="default" '
            f"data-parameters='{json.dumps(params, ensure_ascii=False)}'></div>")


def render(text: str, diagrams: Path) -> str:
    return re.sub(r"\{\{(\w+)\}\}",
                  lambda match: macro((diagrams / f"{match.group(1)}.mmd").read_text(encoding="utf-8").rstrip()),
                  text)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Replace {{NAME}} placeholders with Confluence Mermaid macros.")
    parser.add_argument("page", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--diagrams", type=Path)
    args = parser.parse_args(argv)
    diagrams = args.diagrams or args.page.parent / "diagrams"
    args.out.write_text(render(args.page.read_text(encoding="utf-8"), diagrams), encoding="utf-8")


if __name__ == "__main__":
    main()
