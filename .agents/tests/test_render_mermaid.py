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


def sample_element(body_value):
    params = {
        "macroParams": {"theme": {"value": "dark"}, "__bodyContent": {"value": body_value}},
        "macroMetadata": {"macroId": {"value": "old-id"}, "title": "Diagram"},
    }
    return ('<div data-type="extension" data-extension-key="example-mermaid" '
            'data-extension-type="example.type" data-layout="wide" '
            f"data-parameters='{json.dumps(params)}'></div>")


LIST_SAMPLE = sample_element(json.dumps([{"body": "old", "date": 1}]))


class Macros(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("data-type") == "extension":
            self.found.append(attributes)


def parse(text):
    parser = Macros()
    parser.feed(text)
    return parser.found


class RenderMermaidTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name)
        self.diagrams = self.root / "diagrams"
        self.diagrams.mkdir()

    def diagram(self, name, source, encoding="utf-8"):
        (self.diagrams / f"{name}.mmd").write_text(source, encoding=encoding)

    def render(self, text, sample=LIST_SAMPLE):
        return render_mermaid.render(text, render_mermaid.read_sample(sample), self.diagrams)

    def test_cli_copies_the_sample_shape_with_new_body_date_and_id(self):
        self.diagram("auth-flow", 'flowchart LR\n  a["it\'s A & B"] --> b\n')
        page = self.root / "page.html"
        sample = self.root / "sample.html"
        out = self.root / "out.html"
        page.write_text("<p>before</p>{{auth-flow}}<p>after</p>", encoding="utf-8")
        sample.write_text(LIST_SAMPLE, encoding="utf-8")
        render_mermaid.main([str(page), str(sample), str(out)])
        text = out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("<p>before</p>") and text.endswith("<p>after</p>"))
        [element] = parse(text)
        self.assertEqual((element["data-extension-key"], element["data-extension-type"], element["data-layout"]),
                         ("example-mermaid", "example.type", "wide"))
        params = json.loads(element["data-parameters"])
        self.assertEqual(params["macroParams"]["theme"], {"value": "dark"})
        self.assertNotEqual(params["macroMetadata"]["macroId"]["value"], "old-id")
        [entry] = json.loads(params["macroParams"]["__bodyContent"]["value"])
        self.assertEqual(entry["body"], 'flowchart LR\r\n  a["it\'s A & B"] --> b')
        self.assertGreater(entry["date"], 1)

    def test_plain_string_body_is_replaced_with_the_source(self):
        self.diagram("D1", "flowchart TD\n  x --> y\n")
        [element] = parse(self.render("{{D1}}", sample_element("old source")))
        params = json.loads(element["data-parameters"])
        self.assertEqual(params["macroParams"]["__bodyContent"]["value"], "flowchart TD\n  x --> y")

    def test_every_macro_gets_a_fresh_id(self):
        self.diagram("D1", "flowchart LR\n  a --> b")
        elements = parse(self.render("{{D1}}{{D1}}")) + parse(self.render("{{D1}}"))
        ids = {json.loads(e["data-parameters"])["macroMetadata"]["macroId"]["value"] for e in elements}
        self.assertEqual(len(ids), 3)

    def test_byte_order_mark_is_not_part_of_the_source(self):
        self.diagram("D1", "flowchart LR\n  a --> b", encoding="utf-8-sig")
        [element] = parse(self.render("{{D1}}"))
        [entry] = json.loads(json.loads(element["data-parameters"])["macroParams"]["__bodyContent"]["value"])
        self.assertTrue(entry["body"].startswith("flowchart"))

    def test_missing_diagram_and_unusable_sample_name_the_problem(self):
        with self.assertRaisesRegex(SystemExit, r"\{\{nope\}\}"):
            self.render("{{nope}}")
        with self.assertRaisesRegex(SystemExit, "sample"):
            render_mermaid.read_sample("<p>no macro here</p>")


if __name__ == "__main__":
    unittest.main()
