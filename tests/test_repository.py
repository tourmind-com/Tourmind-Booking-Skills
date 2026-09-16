from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EXPECTED_SKILLS = {"tourmind-booking", "flight-booking-ai"}


def read_frontmatter(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise AssertionError(f"Missing YAML frontmatter: {path}")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise AssertionError(f"Unterminated YAML frontmatter: {path}")
    return parts[1]


def frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+)", frontmatter, re.MULTILINE)
    if not match:
        raise AssertionError(f"Missing frontmatter field: {key}")
    return match.group(1).strip()


class RepositoryStructureTests(unittest.TestCase):
    def test_expected_skills_are_discoverable(self) -> None:
        discovered = {
            path.parent.name
            for path in SKILLS_ROOT.glob("*/SKILL.md")
        }
        self.assertEqual(discovered, EXPECTED_SKILLS)
        self.assertFalse((ROOT / "SKILL.md").exists())

    def test_skill_names_match_their_directories(self) -> None:
        for skill_name in EXPECTED_SKILLS:
            skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
            frontmatter = read_frontmatter(skill_path)
            self.assertEqual(frontmatter_value(frontmatter, "name"), skill_name)
            self.assertIn("description:", frontmatter)

    def test_skill_versions_stay_synchronized(self) -> None:
        versions = set()
        for skill_name in EXPECTED_SKILLS:
            frontmatter = read_frontmatter(SKILLS_ROOT / skill_name / "SKILL.md")
            versions.add(frontmatter_value(frontmatter, "version"))
        self.assertEqual(len(versions), 1)

    def test_local_markdown_references_exist(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for skill_name in EXPECTED_SKILLS:
            skill_dir = SKILLS_ROOT / skill_name
            content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            for target in link_pattern.findall(content):
                target_path = target.split("#", 1)[0]
                if (
                    not target_path
                    or "://" in target_path
                    or target_path.startswith("mailto:")
                    or "{" in target_path
                    or "}" in target_path
                ):
                    continue
                self.assertTrue(
                    (skill_dir / target_path).is_file(),
                    f"Broken local reference in {skill_name}: {target}",
                )

    def test_flight_runtime_documentation_is_english_only(self) -> None:
        cjk_pattern = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
        flight_dir = SKILLS_ROOT / "flight-booking-ai"
        for path in flight_dir.rglob("*.md"):
            self.assertIsNone(
                cjk_pattern.search(path.read_text(encoding="utf-8")),
                f"Chinese text found in flight runtime documentation: {path}",
            )


if __name__ == "__main__":
    unittest.main()
