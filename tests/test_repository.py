from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
READMES = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "README.ja.md",
    ROOT / "README.es.md",
)
REPOSITORIES = (
    "tourmind-com/Hotel-Booking-AI",
    "tourmind-com/Tourmind-Booking-Skill",
    "tourmind-com/Hotel-Booking-AI-MCP",
    "tourmind-com/Tourmind-Booking-MCP",
)
DEMO_ASSETS = (
    ROOT / "docs" / "assets" / "demo" / "search-en.gif",
    ROOT / "docs" / "assets" / "demo" / "detail-en.gif",
    ROOT / "docs" / "assets" / "demo" / "pay-en.gif",
)
DEMO_READMES = (READMES[0], READMES[2], READMES[3])
DEMO_DISPLAY_WIDTH = 720


class RepositoryContractTests(unittest.TestCase):
    def test_skill_frontmatter_and_version(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        top_level_keys = {
            match.group(1)
            for line in frontmatter.splitlines()
            if (match := re.match(r"^([a-z][a-z0-9_-]*):", line))
        }
        self.assertEqual(top_level_keys, {"name", "description"})
        self.assertRegex(frontmatter, r"(?m)^name: tourmind-booking$")
        self.assertRegex(text, r"\*\*Skill version:\*\* `\d+\.\d+\.\d+`")
        self.assertLess(len(text.splitlines()), 500)

    def test_skill_references_exist(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        local_markdown_links = re.findall(r"\[[^]]+\]\(([^):]+\.md)\)", text)
        self.assertTrue(local_markdown_links)
        for relative_path in local_markdown_links:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_localized_readmes_and_navigation(self) -> None:
        expected_links = (
            "README.md",
            "README.zh-CN.md",
            "README.ja.md",
            "README.es.md",
        )
        for readme in READMES:
            with self.subTest(readme=readme.name):
                text = readme.read_text(encoding="utf-8")
                for link in expected_links:
                    self.assertIn(f"]({link})", text)
                for repository in REPOSITORIES:
                    self.assertIn(repository, text)

    def test_installation_is_client_neutral(self) -> None:
        for readme in READMES:
            with self.subTest(readme=readme.name):
                text = readme.read_text(encoding="utf-8")
                self.assertIn("WorkBuddy", text)
                self.assertIn("OpenAI Codex", text)
                self.assertIn("Claude Code", text)
                self.assertIn("CLIENT_SKILLS_DIR", text)
                self.assertNotIn("~/.codex/skills/tourmind-booking", text)

    def test_english_demo_assets_exist_and_are_linked(self) -> None:
        for asset in DEMO_ASSETS:
            with self.subTest(asset=asset.name):
                self.assertTrue(asset.is_file())
                self.assertGreater(asset.stat().st_size, 0)
                self.assertLessEqual(asset.stat().st_size, 8_000_000)
                relative_path = asset.relative_to(ROOT).as_posix()
                for readme in DEMO_READMES:
                    self.assertIn(relative_path, readme.read_text(encoding="utf-8"))

    def test_english_demos_are_centered_and_resized(self) -> None:
        for readme in DEMO_READMES:
            text = readme.read_text(encoding="utf-8")
            with self.subTest(readme=readme.name):
                self.assertEqual(text.count('<div align="center">'), 3)
                for asset in DEMO_ASSETS:
                    relative_path = re.escape(asset.relative_to(ROOT).as_posix())
                    self.assertRegex(
                        text,
                        rf'(?s)<div align="center">\s*'
                        rf'<a href="{relative_path}">\s*'
                        rf'<img src="{relative_path}" alt="[^"]+" '
                        rf'width="{DEMO_DISPLAY_WIDTH}"\s*/>\s*'
                        rf'</a>\s*</div>',
                    )

    def test_openai_interface_metadata(self) -> None:
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "TourMind Hotel Booking"', metadata)
        self.assertIn("short_description:", metadata)
        self.assertIn("$tourmind-booking", metadata)

    def test_required_endpoints_are_documented(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        endpoints = (
            "check_skill_update",
            "search_location",
            "search_hotels",
            "get_hotel_detail",
            "query_room_rates",
            "check_room_availability",
            "create_booking",
            "query_booking",
            "cancel_booking",
            "pay_order",
        )
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                self.assertIn(endpoint, text)

    def test_credentials_are_not_tracked(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertNotIn("skill_token.txt", tracked)
        self.assertFalse(any(path.endswith("user_key.txt") for path in tracked))


if __name__ == "__main__":
    unittest.main()
