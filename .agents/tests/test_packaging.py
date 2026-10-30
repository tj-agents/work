from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SKILLS = {
    "ask", "ask-person", "ask-the-team", "ask-infra",
    "draft-comment", "respond-comments", "confluence",
}
DEPENDENCIES = {
    "tj-agents/base",
    "tj-agents/cli",
    "tj-agents/engineering",
    "tj-agents/docs",
}

ENGINEERING_SKILLS = {
    "address-bug", "address-debt", "address-mistake", "feature", "plan-execution",
}


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

    def test_shared_dependencies_are_in_both_install_contracts(self):
        selection = load("plugins/work/selection.json")
        self.assertEqual(set(selection["dependencies"]), DEPENDENCIES)
        harness = load("plugins/work/harness.json")
        self.assertEqual(harness["plugin"], "tj-agents/work")
        self.assertEqual(set(harness["requires"]["plugins"]), DEPENDENCIES | {"tj-agents/work"})
        marketplaces = {item["id"]: item["repository"] for item in harness["requires"]["marketplaces"]}
        self.assertEqual(
            marketplaces,
            {
                "tj-agents": "tj-agents/marketplace",
            },
        )
        self.assertEqual(harness["requires"]["hooks"], [])

    def test_pending_review_helper_has_a_narrow_package_grant(self):
        harness = load("plugins/work/harness.json")
        permissions = harness["requires"]["permissions"]
        source_script = "${PLUGIN_ROOT}/.agents/work/skills/draft-comment/scripts/post_pending_review.py"
        packaged_script = "${PLUGIN_ROOT}/skills/draft-comment/scripts/post_pending_review.py"
        self.assertEqual(
            permissions["claude_allow"],
            [
                f"Bash(python -B {source_script}:*)",
                f"PowerShell(python -B {source_script}:*)",
                f"Bash(python3 -B {source_script}:*)",
                f"PowerShell(python3 -B {source_script}:*)",
                f"Bash(python -B {packaged_script}:*)",
                f"PowerShell(python -B {packaged_script}:*)",
                f"Bash(python3 -B {packaged_script}:*)",
                f"PowerShell(python3 -B {packaged_script}:*)",
            ],
        )
        self.assertEqual(len(permissions["codex_prefix_rules"]), 1)
        grant = permissions["codex_prefix_rules"][0]
        self.assertEqual(grant["match"], [["python", "-B", source_script], ["python", "-B", packaged_script]])
        self.assertEqual(grant["not_match"], [["python", packaged_script]])
        self.assertEqual(grant["pattern"][1:], ["-B", [source_script, packaged_script]])
        self.assertTrue((ROOT / "plugins/work/.agents/work/skills/draft-comment/scripts/post_pending_review.py").is_file())
        self.assertTrue((ROOT / "plugins/work/skills/draft-comment/scripts/post_pending_review.py").is_file())

    def test_all_hosts_ship_the_same_complete_skill_family(self):
        authored = {}
        source = ROOT / ".agents/work"
        for path in source.rglob("SKILL.md"):
            content = path.read_text(encoding="utf-8")
            name = re.search(r"^name: (.+)$", content, re.MULTILINE).group(1)
            authored[name] = content
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
                elif namespace == "engineering":
                    self.assertIn(name, ENGINEERING_SKILLS, str(path))
                    self.assertIn("tj-agents/engineering", load("plugins/work/selection.json")["dependencies"])
                else:
                    self.assertEqual((namespace, name), ("cli", "clip"), str(path))
                    self.assertIn("tj-agents/cli", load("plugins/work/selection.json")["dependencies"])


if __name__ == "__main__":
    unittest.main()
