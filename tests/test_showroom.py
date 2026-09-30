import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "showroom/content/modules/ROOT/pages"


class ShowroomTests(unittest.TestCase):
    def test_lab_is_separate_and_follows_75_to_90_minute_qualification_journey(self):
        expected = ["01-discover.adoc", "02-baseline.adoc", "03-migrate.adoc", "04-disrupt.adoc", "05-correlate.adoc", "06-qualify.adoc", "07-handoff-reclaim.adoc"]
        self.assertTrue(all((PAGES / name).exists() for name in expected))
        joined = "\n".join((PAGES / name).read_text() for name in expected)
        for term in ("75–90 minutes", "ALLOW_REVIEW", "REFUSE", "ABSTAIN", "HUMAN_PROMOTION_REQUIRED", "zero residue", "REHEARSAL", "restart"):
            self.assertIn(term, joined)

    def test_supplemental_roadshow_was_not_copied(self):
        files = [path for path in (ROOT / "showroom").rglob("*") if path.is_file()]
        self.assertLess(len(files), 20)
        self.assertFalse(any("2026_spring" in path.as_posix() for path in files))

    def test_journey_is_executable_truthful_and_participant_safe(self):
        pages = "\n".join(path.read_text() for path in sorted(PAGES.glob("*.adoc")))
        for heading in ("Show", "Learn", "Do", "Prove"):
            self.assertIn(f"== {heading}", pages)
        self.assertGreaterEqual(pages.count('role="execute"'), 10)
        for contract in ("/healthz", "/metrics", "/api/v1/qualifications", "llm_authority", "source_state"):
            self.assertIn(contract, pages)
        self.assertIn("PRESENTATION_URL", pages)
        self.assertNotIn("SHOWROOM_URL", pages)
        self.assertIn("VirtualMachines", pages)
        self.assertIn("PersistentVolumeClaims", pages)
        self.assertIn("Virtualization + AI 401", pages)
        self.assertIn("fleet", pages.lower())
        self.assertIn("Launchpad owns namespace reclamation", pages)
        self.assertNotIn("uninstall the helm release", pages.lower())


if __name__ == "__main__":
    unittest.main()
