import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class FactoryTests(unittest.TestCase):
    def test_required_501_assets_exist(self):
        required = ["contracts/qualification-request.schema.json", "contracts/qualification-response.schema.json", "contracts/qualification-policy.json", "charts/virtualization-ai-501/Chart.yaml", "showroom/content/modules/ROOT/pages/01-discover.adoc", "showroom/content/modules/ROOT/pages/07-handoff-reclaim.adoc", "handoff/launchpad-handoff.yaml", ".github/workflows/release-images.yml"]
        self.assertEqual([name for name in required if not (ROOT / name).exists()], [])

    def test_presentation_has_exactly_seven_scenes_and_honest_metrics(self):
        config = (ROOT / "src/demo.config.ts").read_text()
        self.assertEqual(config.count("type:"), 7)
        for required in ("DISCOVER", "BASELINE", "MIGRATE", "DISRUPT", "CORRELATE", "QUALIFY", "HANDOFF", "REHEARSAL"):
            self.assertIn(required, config)
        self.assertNotIn("LIVE Intel Xeon", config)

    def test_blueprint_pins_exact_401_foundation(self):
        blueprint = yaml.safe_load((ROOT / "demo-blueprint.yaml").read_text())
        self.assertEqual(blueprint["source"]["revision"], "0672f307bf48eae2803958e290997d8c046b5c42")
        self.assertEqual(blueprint["status"], "approved")
        self.assertFalse(blueprint["authority"]["factory_may_certify"])

    def test_handoff_is_standard_noncertifying_zero_seat_receipt(self):
        handoff = yaml.safe_load((ROOT / "handoff/launchpad-handoff.yaml").read_text())
        self.assertEqual(handoff["schema_version"], "demo-story.redhat-intel.com/launchpad-handoff/v1")
        self.assertTrue(all(value is False for value in handoff["factory_receipt"]["authority"].values()))
        self.assertEqual(handoff["proposed_launchpad_intake"]["certification_proposal"]["max_workshop_seats"], 0)
        self.assertFalse(handoff["factory_receipt"]["authority"]["orderable"])

    def test_fixtures_are_rehearsal_and_never_promote(self):
        for path in sorted((ROOT / "public/fixtures").glob("*.json")):
            data = json.loads(path.read_text())
            if path.name.endswith("-request.json"):
                self.assertTrue(data["evidence_snapshot"])
                self.assertTrue(all(item["source_state"] == "REHEARSAL" for item in data["evidence_snapshot"]))
            else:
                self.assertEqual(data["source_state"], "REHEARSAL")
                self.assertFalse(data["authority"]["promotion_performed"])


if __name__ == "__main__":
    unittest.main()
