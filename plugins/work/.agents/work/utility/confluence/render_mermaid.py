import argparse
import copy
import html
import html.parser
import json
import re
import time
import uuid
from pathlib import Path

PLACEHOLDER = re.compile(r"^([ \t]*)\{\{([\w.-]+)\}\}[ \t]*\r?$", re.MULTILINE)
ANY_PLACEHOLDER = re.compile(r"\{\{([\w.-]+)\}\}")
INSTANCE_ATTRIBUTES = {"id", "data-local-id"}


class BodiedMacros(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("data-type") != "extension":
            return
        try:
            params = json.loads(attributes.get("data-parameters") or "")
        except ValueError:
            return
        if isinstance(params, dict) and isinstance(params.get("macroParams"), dict) \
                and "__bodyContent" in params["macroParams"]:
            self.found.append({"tag": tag, "attributes": attributes, "params": params})


def read_sample(text: str) -> dict:
    parser = BodiedMacros()
    parser.feed(text)
    if len(parser.found) != 1:
        raise SystemExit(f"sample: expected exactly one Confluence macro with a body, found {len(parser.found)}")
    return parser.found[0]


def new_body(value, source: str) -> str:
    try:
        entries = json.loads(value)
    except (TypeError, ValueError):
        return source
    if not isinstance(entries, (list, dict)):
        return source
    if isinstance(entries, list) and entries and isinstance(entries[0], dict) and "body" in entries[0]:
        entry = dict(entries[0], body=source.replace("\n", "\r\n"))
        if "date" in entry:
            entry["date"] = int(time.time() * 1000)
        return json.dumps([entry], ensure_ascii=False)
    raise SystemExit("sample: unrecognised __bodyContent format")


def macro(sample: dict, source: str) -> str:
    params = copy.deepcopy(sample["params"])
    body = params["macroParams"]["__bodyContent"]
    body["value"] = new_body(body.get("value"), source)
    if not isinstance(params.get("macroMetadata"), dict):
        params["macroMetadata"] = {}
    params["macroMetadata"]["macroId"] = {"value": str(uuid.uuid4())}
    attributes = {name: value for name, value in sample["attributes"].items() if name not in INSTANCE_ATTRIBUTES}
    attributes["data-parameters"] = json.dumps(params, ensure_ascii=False)
    rendered = " ".join(name if value is None else f'{name}="{html.escape(value, quote=True)}"'
                        for name, value in attributes.items())
    return f"<{sample['tag']} {rendered}></{sample['tag']}>"


def render(text: str, sample: dict, diagrams: Path) -> str:
    def replace(match):
        path = diagrams / f"{match.group(2)}.mmd"
        if not path.is_file():
            raise SystemExit(f"{{{{{match.group(2)}}}}}: no diagram at {path}")
        return match.group(1) + macro(sample, path.read_text(encoding="utf-8-sig").rstrip())
    inline = ANY_PLACEHOLDER.findall(PLACEHOLDER.sub("", text))
    stranded = sorted({name for name in inline if (diagrams / f"{name}.mmd").is_file()})
    if stranded:
        raise SystemExit(f"put each placeholder on its own line: {', '.join(stranded)}")
    return PLACEHOLDER.sub(replace, text)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Replace {{NAME}} lines with the site's Mermaid macro.")
    parser.add_argument("page", type=Path, help="page HTML; diagrams are read from diagrams/NAME.mmd beside it")
    parser.add_argument("sample", type=Path, help="one Mermaid macro element copied from an existing page")
    parser.add_argument("out", type=Path)
    args = parser.parse_args(argv)
    sample = read_sample(args.sample.read_text(encoding="utf-8-sig"))
    page = args.page.read_text(encoding="utf-8-sig")
    args.out.write_text(render(page, sample, args.page.parent / "diagrams"), encoding="utf-8")


if __name__ == "__main__":
    main()
