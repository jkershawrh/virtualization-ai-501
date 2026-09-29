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


if __name__ == "__main__":
    unittest.main()
