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
    "tourmind-com/Tourmind-Booking-Skills",
    "tourmind-com/Hotel-Booking-AI-MCP",
    "tourmind-com/Tourmind-Booking-MCP",
)
DEMO_ASSET_DIR = ROOT / "docs" / "assets" / "demo"
HERO_ASSET = ROOT / "docs" / "assets" / "hero" / "tourmind-booking-skills.png"
OSS_ASSET_BASE = "https://skilloss.tourmind.com/skills/tourmind-booking/v1"
HERO_ASSET_URL = f"{OSS_ASSET_BASE}/hero/tourmind-booking-skills.png"
DEMO_ASSET_URLS = (
    f"{OSS_ASSET_BASE}/demo/search-en.gif",
    f"{OSS_ASSET_BASE}/demo/detail-en.gif",
    f"{OSS_ASSET_BASE}/demo/pay-en.gif",
)
HERO_TARGET = "https://tourmind.com/user/skill-token"
PRODUCT_PAGE_URL = "https://tourmind.com/skills"


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
                    self.assertTrue(
                        f"]({link})" in text or f'href="{link}"' in text,
                        f"{readme.name} must link to {link}",
                    )
                for repository in REPOSITORIES:
                    self.assertIn(repository, text)
                self.assertIn(PRODUCT_PAGE_URL, text)
                self.assertNotIn("https://tourmind.com/skill)", text)
                self.assertNotIn('https://tourmind.com/skill"', text)

    def test_english_readme_marketing_header(self) -> None:
        text = READMES[0].read_text(encoding="utf-8")
        self.assertIn("TourMind Booking Skills", text)
        self.assertIn("Let Your Agent Book Hotels Worldwide", text)
        self.assertIn("Bring Your Customers Into Intelligent Travel", text)
        self.assertIn(f'href="{PRODUCT_PAGE_URL}">Product Page</a>', text)
        self.assertIn("<span>Live Demo</span>", text)
        self.assertIn('href="https://tourmind.com">Company</a>', text)
        self.assertIn("ClawHub_installs-1.4k", text)
        self.assertIn(
            "](https://clawhub.ai/tourmind/skills/hotel-booking-ai)", text
        )
        self.assertIn("github/v/release/tourmind-com/Tourmind-Booking-Skills", text)
        self.assertIn("github/license/tourmind-com/Tourmind-Booking-Skills", text)
        self.assertFalse(HERO_ASSET.exists())
        self.assertRegex(
            text,
            rf'(?s)<a href="{re.escape(HERO_TARGET)}">\s*'
            rf'<img alt="[^"]+" src="{re.escape(HERO_ASSET_URL)}" '
            rf'style="width: 100%"\s*/>\s*</a>',
        )

    def test_installation_is_client_neutral(self) -> None:
        for readme in READMES:
            with self.subTest(readme=readme.name):
                text = readme.read_text(encoding="utf-8")
                self.assertIn("WorkBuddy", text)
                self.assertIn("OpenAI Codex", text)
                self.assertIn("Claude Code", text)
                self.assertIn("CLIENT_SKILLS_DIR", text)
                self.assertNotIn("~/.codex/skills/tourmind-booking", text)

    def test_demo_gifs_are_oss_hosted_not_distributed(self) -> None:
        self.assertFalse(DEMO_ASSET_DIR.exists())
        for readme in READMES:
            with self.subTest(readme=readme.name):
                text = readme.read_text(encoding="utf-8")
                self.assertNotIn("docs/assets/demo", text)
                for asset_url in DEMO_ASSET_URLS:
                    self.assertEqual(text.count(asset_url), 2)

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
            "batch_query_room_rates",
            "check_room_availability",
            "create_booking",
            "query_booking",
            "cancel_booking",
            "pay_order",
        )
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                self.assertIn(endpoint, text)

    def test_official_skill_identity(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("# TourMind Booking Skill", skill_text)
        self.assertIn("### TourMind Booking Skill is ready", skill_text)
        self.assertIn("name: tourmind-booking", skill_text)
        self.assertIn('display_name: "TourMind Hotel Booking"', metadata)
        self.assertIn("$tourmind-booking", metadata)
        self.assertNotIn("booking_test", skill_text)
        self.assertNotIn("tourmind-booking-test", metadata)

    def test_final_confirmation_includes_child_occupancy(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("{children_per_room}", text)
        self.assertIn("{children_ages_per_room_or_not_applicable}", text)
        self.assertIn("When there are no children", text)

    def test_batch_rate_client_concurrency_limit(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        reference_text = (ROOT / "references" / "parameter_guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("up to three `batch_query_room_rates` requests concurrently", skill_text)
        self.assertIn("never exceed three concurrent requests", skill_text)
        self.assertIn("at most three concurrent batch requests per client", reference_text)
        self.assertNotIn("Do not wrap this endpoint in another client-side concurrency pool", reference_text)

    def test_api_base_url_is_production(self) -> None:
        documents = (
            SKILL,
            ROOT / "references" / "parameter_guide.md",
            *READMES,
        )
        for document in documents:
            with self.subTest(document=document.name):
                text = document.read_text(encoding="utf-8")
                self.assertIn("https://api.tourmind.com", text)
                self.assertNotIn("http://39.108.114.224:9028", text)

    def test_rate_reason_codes_have_explicit_scope(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        reference_text = (ROOT / "references" / "parameter_guide.md").read_text(
            encoding="utf-8"
        )
        for text in (skill_text, reference_text):
            self.assertIn("`query_room_rates` responses", text)
            self.assertIn("`batch_query_room_rates.data.results[]` items", text)
            self.assertIn("`invalid_request` may also", text)

    def test_missing_hotel_business_permission_keeps_token(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        reference_text = (ROOT / "references" / "parameter_guide.md").read_text(
            encoding="utf-8"
        )
        for text in (skill_text, reference_text):
            self.assertIn("HOTEL_BUSINESS_PERMISSION_REQUIRED", text)
            self.assertIn("HTTP 403", text)
        self.assertIn("Do not delete or replace the token", skill_text)
        self.assertIn("do not retry the request", skill_text)
        self.assertIn("Keep the token file", reference_text)

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
