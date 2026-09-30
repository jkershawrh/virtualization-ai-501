import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/virtualization-ai-501"


class PackagingTests(unittest.TestCase):
    def test_chart_expresses_governance_without_secret_values(self):
        rendered = "\n".join(path.read_text() for path in (CHART / "templates").glob("*"))
        for term in ("NetworkPolicy", "nodeSelector", "serviceAccountName", "ServiceMonitor", "/metrics", "secretKeyRef", "PersistentVolumeClaim", "LEDGER_PATH"):
            self.assertIn(term, rendered)
        self.assertNotIn("kind: Secret", rendered)
        self.assertIn("automountServiceAccountToken: false", rendered)
        self.assertIn("podSelector: {}", rendered)

    def test_published_values_are_absent_or_exact_release_receipts(self):
        path = CHART / "values.published.yaml"
        if path.exists():
            import re, yaml
            values = yaml.safe_load(path.read_text())
            for component in ("operationsAdapter", "presentation"):
                self.assertRegex(values[component]["image"]["digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertNotIn("TO_BE_FILLED", path.read_text())

    def test_launchpad_flat_image_values_override_nested_defaults(self):
        workload = "ghcr.io/example/virt501-adapter@sha256:" + "a" * 64
        presentation = "ghcr.io/example/virt501-presentation@sha256:" + "b" * 64
        render = subprocess.run(
            [
                "helm", "template", "virtualization-ai-501", str(CHART),
                "--set-string", f"workload_image={workload}",
                "--set-string", f"presentation_image={presentation}",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn(f'image: "{workload}"', render.stdout)
        self.assertIn(f'image: "{presentation}"', render.stdout)


if __name__ == "__main__":
    unittest.main()
