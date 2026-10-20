from pathlib import Path
import html.parser
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/work/utility/confluence/render_mermaid.py"
spec = importlib.util.spec_from_file_location("render_mermaid", SCRIPT)
render_mermaid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mermaid)


class Macros(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("data-extension-key") == "confluence-mermaid-macro":
            self.found.append(json.loads(attributes["data-parameters"]))


def parse(text):
    parser = Macros()
    parser.feed(text)
    return parser.found


class RenderMermaidTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name)
        (self.root / "diagrams").mkdir()
        (self.root / "diagrams/D1.mmd").write_text("flowchart LR\n  a[Erm’s side] --> b\n", encoding="utf-8")

    def test_placeholder_becomes_a_parseable_macro_with_crlf_source(self):
        page = self.root / "page.html"
        out = self.root / "out.html"
        page.write_text("<p>before</p>{{D1}}<p>after</p>", encoding="utf-8")
        render_mermaid.main([str(page), str(out)])
        text = out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("<p>before</p>") and text.endswith("<p>after</p>"))
        [params] = parse(text)
        [body] = json.loads(params["macroParams"]["__bodyContent"]["value"])
        self.assertEqual(body["body"], "flowchart LR\r\n  a[Erm’s side] --> b")
        self.assertIsInstance(body["date"], int)

    def test_every_render_gets_a_fresh_macro_id(self):
        first = parse(render_mermaid.render("{{D1}}{{D1}}", self.root / "diagrams"))
        second = parse(render_mermaid.render("{{D1}}", self.root / "diagrams"))
        ids = [params["macroMetadata"]["macroId"]["value"] for params in first + second]
        self.assertEqual(len(set(ids)), 3)

    def test_quotes_and_ampersands_are_refused(self):
        for source in ('a["x"]', "a[it's]", "a[x & y]"):
            with self.subTest(source=source):
                (self.root / "diagrams/D2.mmd").write_text(source, encoding="utf-8")
                with self.assertRaises(ValueError):
                    render_mermaid.render("{{D2}}", self.root / "diagrams")

    def test_diagrams_directory_can_be_overridden(self):
        other = self.root / "other"
        other.mkdir()
        (other / "D1.mmd").write_text("flowchart TD\n  x --> y", encoding="utf-8")
        page = self.root / "page.html"
        out = self.root / "out.html"
        page.write_text("{{D1}}", encoding="utf-8")
        render_mermaid.main([str(page), str(out), "--diagrams", str(other)])
        [params] = parse(out.read_text(encoding="utf-8"))
        self.assertIn("x --> y", params["macroParams"]["__bodyContent"]["value"])


if __name__ == "__main__":
    unittest.main()
