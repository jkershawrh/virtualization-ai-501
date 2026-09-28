import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, RefResolver
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def load_json(relative: str):
    return json.loads((CONTRACTS / relative).read_text())


class QualificationContractTests(unittest.TestCase):
    def validate(self, schema: str, example: str):
        evidence = load_json("evidence-record.schema.json")
        resolver = RefResolver((CONTRACTS / schema).as_uri(), load_json(schema), store={evidence["$id"]: evidence, "evidence-record.schema.json": evidence})
        errors = sorted(Draft202012Validator(load_json(schema), format_checker=FormatChecker(), resolver=resolver).iter_errors(load_json(example)), key=lambda error: list(error.path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def test_examples_satisfy_501_schemas(self):
        for stem in ("qualified-fleet", "capacity-breach", "correlation-gap"):
            self.validate("qualification-request.schema.json", f"examples/{stem}-request.json")
            self.validate("qualification-response.schema.json", f"examples/{stem}-response.json")

    def test_policy_is_deterministic_and_never_promotes(self):
        policy = load_json("qualification-policy.json")
        self.assertEqual([rule["priority"] for rule in policy["rules"]], sorted(rule["priority"] for rule in policy["rules"]))
        self.assertEqual(policy["default_decision"], "ABSTAIN")
        self.assertFalse(policy["authority"]["automated_promotion"])
        self.assertFalse(policy["authority"]["factory_may_certify"])

    def test_openapi_exposes_read_only_qualification_boundary(self):
        spec = yaml.safe_load((CONTRACTS / "openapi.yaml").read_text())
        self.assertEqual(set(spec["paths"]), {"/api/v1/qualifications", "/api/v1/qualifications/{request_id}", "/metrics", "/healthz"})


if __name__ == "__main__":
    unittest.main()
