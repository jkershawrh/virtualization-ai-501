import unittest
from pathlib import Path


class EmbeddedWorkspaceTests(unittest.TestCase):
    def test_embedded_main_can_shrink_and_scroll_instead_of_clipping_controls(self):
        css = (Path(__file__).resolve().parents[1] / 'src/theme.css').read_text()
        main = css.split('.live-workspace-main {', 1)[1].split('}', 1)[0]
        self.assertIn('min-height: 0', main)
        self.assertIn('overflow-y: auto', main)
