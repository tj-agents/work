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


def sample_element(body_value, extra=""):
    params = {
        "macroParams": {"theme": {"value": "dark"}, "__bodyContent": {"value": body_value}},
        "macroMetadata": {"macroId": {"value": "old-id"}, "title": "Diagram"},
    }
    return (f'<div data-type="extension" data-extension-key="example-mermaid" {extra}'
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


def params_of(element):
    return json.loads(element["data-parameters"])


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
        page.write_text("<p>before</p>\n  {{auth-flow}}\n<p>after</p>", encoding="utf-8-sig")
        sample.write_text("<p>copied with its paragraph</p>" + LIST_SAMPLE, encoding="utf-8-sig")
        render_mermaid.main([str(page), str(sample), str(out)])
        lines = out.read_text(encoding="utf-8").split("\n")
        self.assertEqual((lines[0], lines[2]), ("<p>before</p>", "<p>after</p>"))
        self.assertTrue(lines[1].startswith("  <div "))
        [element] = parse(lines[1])
        self.assertEqual((element["data-extension-key"], element["data-extension-type"], element["data-layout"]),
                         ("example-mermaid", "example.type", "wide"))
        params = params_of(element)
        self.assertEqual(params["macroParams"]["theme"], {"value": "dark"})
        self.assertNotEqual(params["macroMetadata"]["macroId"]["value"], "old-id")
        [entry] = json.loads(params["macroParams"]["__bodyContent"]["value"])
        self.assertEqual(entry["body"], 'flowchart LR\r\n  a["it\'s A & B"] --> b')
        self.assertGreater(entry["date"], 1)

    def test_only_a_placeholder_on_its_own_line_is_replaced_and_others_fail(self):
        existing = "<p>A{{Decision}} stays text</p>"
        self.assertEqual(self.render(existing), existing)
        self.diagram("D1", "flowchart LR\n  a --> b")
        self.assertEqual(len(parse(self.render("<p>x</p>\r\n{{D1}}\r\n"))), 1)
        with self.assertRaisesRegex(SystemExit, "own line: D1"):
            self.render("<p>{{D1}}</p>")

    def test_plain_string_body_is_replaced_with_the_source(self):
        self.diagram("D1", "flowchart TD\n  x --> y\n")
        [element] = parse(self.render("{{D1}}", sample_element("old source")))
        self.assertEqual(params_of(element)["macroParams"]["__bodyContent"]["value"], "flowchart TD\n  x --> y")

    def test_unrecognised_json_body_fails_instead_of_being_overwritten(self):
        self.diagram("D1", "flowchart TD\n  x --> y")
        with self.assertRaisesRegex(SystemExit, "unrecognised"):
            self.render("{{D1}}", sample_element(json.dumps({"body": "old"})))
        [element] = parse(self.render("{{D1}}", sample_element(json.dumps([{"body": "a"}, {"body": "b"}]))))
        self.assertEqual(json.loads(params_of(element)["macroParams"]["__bodyContent"]["value"]),
                         [{"body": "flowchart TD\r\n  x --> y"}])
        [element] = parse(self.render("{{D1}}", sample_element("null")))
        self.assertEqual(params_of(element)["macroParams"]["__bodyContent"]["value"], "flowchart TD\n  x --> y")

    def test_every_macro_gets_a_fresh_id_and_drops_instance_ids(self):
        self.diagram("D1", "flowchart LR\n  a --> b")
        sample = sample_element(json.dumps([{"body": "old"}]), extra='data-local-id="abc" hidden ')
        elements = parse(self.render("{{D1}}\n{{D1}}", sample)) + parse(self.render("{{D1}}", sample))
        self.assertEqual(len({params_of(e)["macroMetadata"]["macroId"]["value"] for e in elements}), 3)
        for element in elements:
            self.assertNotIn("data-local-id", element)
            self.assertIn("hidden", element)

    def test_byte_order_mark_is_not_part_of_the_source(self):
        self.diagram("D1", "flowchart LR\n  a --> b", encoding="utf-8-sig")
        [element] = parse(self.render("{{D1}}"))
        [entry] = json.loads(params_of(element)["macroParams"]["__bodyContent"]["value"])
        self.assertTrue(entry["body"].startswith("flowchart"))

    def test_missing_diagram_and_unusable_sample_name_the_problem(self):
        with self.assertRaisesRegex(SystemExit, r"\{\{nope\}\}"):
            self.render("{{nope}}")
        with self.assertRaisesRegex(SystemExit, "found 0"):
            render_mermaid.read_sample("<p>no macro here</p>")
        with self.assertRaisesRegex(SystemExit, "found 2"):
            render_mermaid.read_sample(LIST_SAMPLE + LIST_SAMPLE)


if __name__ == "__main__":
    unittest.main()
