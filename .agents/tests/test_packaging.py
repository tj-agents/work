from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SKILLS = {
    "ask", "ask-person", "ask-the-team", "ask-infra",
    "draft-comment", "respond-comments", "explaining-code", "confluence",
}
DEPENDENCIES = {"base-agents/base", "base-agents/machine"}


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PackagingTests(unittest.TestCase):
    def test_employer_detection_is_required(self):
        tier = load("plugins/work/tier.json")
        self.assertEqual(tier["schema_version"], 3)
        self.assertEqual(tier["applies"], "stack-present")
        self.assertEqual(tier["detect"], {"fact": "employer"})
        self.assertEqual(tier["owner_repository"], ["tj-agents/work"])
        for host in ("claude", "codex"):
            manifest = load(f"plugins/work/.{host}-plugin/plugin.json")
            self.assertNotIn("hooks", manifest)
        self.assertFalse((ROOT / ".agents/hooks").exists())

    def test_clipboard_dependency_is_in_both_install_contracts(self):
        selection = load("plugins/work/selection.json")
        self.assertEqual(set(selection["dependencies"]), DEPENDENCIES)
        harness = load("plugins/work/harness.json")
        self.assertEqual(harness["plugin"], "work-agents/work")
        self.assertEqual(set(harness["requires"]["plugins"]), DEPENDENCIES | {"work-agents/work"})
        marketplaces = {item["id"]: item["repository"] for item in harness["requires"]["marketplaces"]}
        self.assertEqual(marketplaces, {"work-agents": "tj-agents/work", "base-agents": "tj-agents/core"})
        self.assertEqual(harness["requires"]["hooks"], [])

    def test_all_hosts_ship_the_same_complete_skill_family(self):
        authored = {}
        source = ROOT / ".agents/work/utility"
        for path in source.rglob("SKILL.md"):
            name = "-".join(path.parent.relative_to(source).parts)
            authored[name] = path.read_text(encoding="utf-8")
        self.assertEqual(set(authored), EXPECTED_SKILLS)
        for output in ("plugins/work/skills", ".claude/skills", ".codex/skills"):
            directory = ROOT / output
            generated = list(directory.rglob("SKILL.md"))
            self.assertEqual(len(generated), len(EXPECTED_SKILLS))
            for path in generated:
                content = path.read_text(encoding="utf-8")
                name = re.search(r"^name: (.+)$", content, re.MULTILINE).group(1)
                target = re.search(r"canonical definition\]\(([^)]+)\)", content).group(1)
                self.assertEqual((path.parent / target).resolve().read_text(encoding="utf-8"), authored[name])

    def test_payload_contains_no_employer_routes_or_provider_commands(self):
        for path in (ROOT / "plugins/work").rglob("*"):
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8").lower()
            for forbidden in ("infonetica", "thread.v2", "corbin taylor", "duediligence dev", "tommyseery-inf", "ab#", "az role assignment", "az rest", "cris-preaward", "cris-diligence"):
                self.assertNotIn(forbidden, content, str(path))

    def test_qualified_skill_references_resolve_to_payload_or_dependency(self):
        for path in (ROOT / "plugins/work/skills").rglob("SKILL.md"):
            content = path.read_text(encoding="utf-8")
            references = re.findall(r"`([a-z][a-z0-9-]*):([a-z][a-z0-9-]*)`", content)
            for namespace, name in references:
                if namespace == "work":
                    self.assertIn(name, EXPECTED_SKILLS, str(path))
                else:
                    self.assertEqual((namespace, name), ("machine", "clip"), str(path))
                    self.assertIn("base-agents/machine", load("plugins/work/selection.json")["dependencies"])


if __name__ == "__main__":
    unittest.main()
