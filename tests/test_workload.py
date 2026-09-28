import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workload.app import ContractError, evaluate, load_ledger, metrics_text, validate_request

ROOT = Path(__file__).resolve().parents[1]


def request(name="qualified-fleet-request.json"):
    return json.loads((ROOT / "contracts/examples" / name).read_text())


class QualificationAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.ledger = Path(self.temp.name) / "qualification.jsonl"
        self.env = patch.dict(os.environ, {"ADAPTER_MODE": "rehearsal", "LEDGER_PATH": str(self.ledger)}, clear=True)
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def test_complete_fleet_earns_human_promotion_review_only(self):
        response, evidence = evaluate(request())
        self.assertEqual(response["decision"], "ALLOW_REVIEW")
        self.assertEqual(response["reason_codes"], ["QUALIFICATION_ENVELOPE_SATISFIED"])
        self.assertEqual(response["source_state"], "REHEARSAL")
        self.assertEqual(response["qualification"]["status"], "PASS")
        self.assertTrue(response["authority"]["human_promotion_required"])
        self.assertFalse(response["authority"]["promotion_performed"])
        self.assertEqual([item["state"] for item in evidence], ["DISCOVER", "BASELINE", "MIGRATE", "DISRUPT", "CORRELATE", "QUALIFY", "HANDOFF"])

    def test_capacity_breach_refuses(self):
        response, _ = evaluate(request("capacity-breach-request.json"))
        self.assertEqual(response["decision"], "REFUSE")
        self.assertIn("CAPACITY_ENVELOPE_BREACH", response["reason_codes"])

    def test_missing_correlation_abstains(self):
        response, _ = evaluate(request("correlation-gap-request.json"))
        self.assertEqual(response["decision"], "ABSTAIN")
        self.assertIn("CORRELATION_INCOMPLETE", response["reason_codes"])

    def test_missing_trial_or_duplicate_vm_is_invalid(self):
        payload = request()
        payload["trials"] = payload["trials"][:-1]
        with self.assertRaises(ContractError):
            validate_request(payload)
        payload = request()
        payload["fleet"]["virtual_machines"][1]["name"] = payload["fleet"]["virtual_machines"][0]["name"]
        with self.assertRaises(ContractError):
            validate_request(payload)

    def test_live_requires_direct_platform_placement_inference_and_telemetry_evidence(self):
        payload = request()
        for item in payload["evidence_snapshot"]:
            item["source_state"] = "LIVE"
        with patch.dict(os.environ, {"ADAPTER_MODE": "live", "LEDGER_PATH": str(self.ledger)}, clear=True):
            self.assertEqual(evaluate(payload)[0]["source_state"], "LIVE")
            reduced = copy.deepcopy(payload)
            reduced["evidence_snapshot"] = [item for item in reduced["evidence_snapshot"] if item["kind"] != "CPU_PLACEMENT"]
            self.assertEqual(evaluate(reduced)[0]["source_state"], "OFFLINE")

    def test_ledger_survives_reload_and_contains_digests(self):
        _, evidence = evaluate(request())
        reloaded = load_ledger(self.ledger)
        self.assertEqual(len(reloaded), len(evidence))
        self.assertTrue(all(item["digest"].startswith("sha256:") for item in reloaded))

    def test_secret_fields_are_rejected(self):
        payload = request()
        payload["token"] = "forbidden"
        with self.assertRaises(ContractError):
            validate_request(payload)

    def test_metrics_are_counts_without_authored_performance_values(self):
        text = metrics_text()
        self.assertIn("qualification_decisions_total", text)
        self.assertNotIn("p95", text.lower())


if __name__ == "__main__":
    unittest.main()
