import argparse
import html
import html.parser
import json
import re
import time
import uuid
from pathlib import Path


class FirstBodiedMacro(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if self.attributes is None and attributes.get("data-type") == "extension":
            try:
                params = json.loads(attributes.get("data-parameters", ""))
            except ValueError:
                return
            if "__bodyContent" in params.get("macroParams", {}):
                self.attributes = attributes


def read_sample(text: str) -> dict:
    parser = FirstBodiedMacro()
    parser.feed(text)
    if parser.attributes is None:
        raise SystemExit("sample: no Confluence macro element with a body")
    return parser.attributes


def macro(sample: dict, source: str) -> str:
    params = json.loads(sample["data-parameters"])
    body = params["macroParams"]["__bodyContent"]
    try:
        entries = json.loads(body["value"])
    except (TypeError, ValueError):
        entries = None
    if isinstance(entries, list) and entries and isinstance(entries[0], dict) and "body" in entries[0]:
        entry = dict(entries[0], body=source.replace("\n", "\r\n"))
        if "date" in entry:
            entry["date"] = int(time.time() * 1000)
        body["value"] = json.dumps([entry], ensure_ascii=False)
    else:
        body["value"] = source
    params.setdefault("macroMetadata", {})["macroId"] = {"value": str(uuid.uuid4())}
    attributes = dict(sample, **{"data-parameters": json.dumps(params, ensure_ascii=False)})
    rendered = " ".join(f'{name}="{html.escape(value, quote=True)}"' for name, value in attributes.items())
    return f"<div {rendered}></div>"


def render(text: str, sample: dict, diagrams: Path) -> str:
    def replace(match):
        path = diagrams / f"{match.group(1)}.mmd"
        if not path.is_file():
            raise SystemExit(f"{{{{{match.group(1)}}}}}: no diagram at {path}")
        return macro(sample, path.read_text(encoding="utf-8-sig").rstrip())
    return re.sub(r"\{\{([\w.-]+)\}\}", replace, text)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Replace {{NAME}} placeholders with the site's Mermaid macro.")
    parser.add_argument("page", type=Path, help="page HTML; diagrams are read from diagrams/NAME.mmd beside it")
    parser.add_argument("sample", type=Path, help="one Mermaid macro element copied from an existing page")
    parser.add_argument("out", type=Path)
    args = parser.parse_args(argv)
    sample = read_sample(args.sample.read_text(encoding="utf-8-sig"))
    page = args.page.read_text(encoding="utf-8-sig")
    args.out.write_text(render(page, sample, args.page.parent / "diagrams"), encoding="utf-8")


if __name__ == "__main__":
    main()
