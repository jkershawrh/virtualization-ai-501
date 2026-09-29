from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REQUEST_VERSION = "demo-story.redhat-intel.com/virtualization-ai-501/qualification-request/v1"
RESPONSE_VERSION = "demo-story.redhat-intel.com/virtualization-ai-501/qualification-response/v1"
EVIDENCE_VERSION = "demo-story.redhat-intel.com/virtualization-ai-501/evidence/v1"
POLICY = json.loads((Path(__file__).parents[1] / "contracts/qualification-policy.json").read_text())
REQUEST_FIELDS = {"schema_version", "request_id", "requested_by", "fleet", "envelope", "trials", "evidence_snapshot"}
FORBIDDEN_KEYS = {"api_key", "apikey", "password", "secret", "token", "authorization", "bearer"}
JOURNEY = ("DISCOVER", "BASELINE", "MIGRATE", "DISRUPT", "CORRELATE", "QUALIFY", "HANDOFF")
REQUIRED_LIVE_KINDS = {"OPENSHIFT", "KUBEVIRT", "VM", "MIGRATION", "DISRUPTION", "CPU_PLACEMENT", "INFERENCE", "TELEMETRY", "CONTINUITY"}
COUNTERS: Counter[str] = Counter()
LOCK = threading.Lock()


class ContractError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_sha256(value: object) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def contains_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in FORBIDDEN_KEYS or contains_forbidden_key(item) for key, item in value.items())
    return isinstance(value, list) and any(contains_forbidden_key(item) for item in value)


def validate_request(value: object) -> dict:
    if not isinstance(value, dict) or set(value) != REQUEST_FIELDS:
        raise ContractError("request fields do not match qualification-request/v1")
    if contains_forbidden_key(value) or value["schema_version"] != REQUEST_VERSION:
        raise ContractError("request is forbidden or has an unsupported schema")
    if not isinstance(value["request_id"], str) or len(value["request_id"]) < 8:
        raise ContractError("request_id is invalid")
    fleet = value["fleet"]
    if not isinstance(fleet, dict) or set(fleet) != {"namespace", "inference_service", "virtual_machines"}:
        raise ContractError("fleet identity is incomplete")
    vms = fleet["virtual_machines"]
    if not isinstance(vms, list) or len(vms) < 3 or len({vm.get("name") for vm in vms if isinstance(vm, dict)}) != len(vms):
        raise ContractError("at least three distinct virtual machines are required")
    for vm in vms:
        if not isinstance(vm, dict) or set(vm) != {"name", "node", "architecture", "cpu_vendor"} or vm["architecture"] != "amd64" or not all(vm.values()):
            raise ContractError("VM placement evidence is malformed")
    envelope = value["envelope"]
    if not isinstance(envelope, dict) or set(envelope) != {"max_p95_ms", "min_success_rate", "max_concurrency", "max_cpu_saturation_pct"}:
        raise ContractError("qualification envelope is malformed")
    trials = value["trials"]
    if not isinstance(trials, list) or {trial.get("kind") for trial in trials if isinstance(trial, dict)} != {"BASELINE", "MIGRATION", "DISRUPTION"}:
        raise ContractError("exactly the baseline, migration, and disruption trial classes are required")
    trial_fields = {"kind", "concurrency", "requests", "success_rate", "p95_ms", "cpu_saturation_pct", "containment_breaches", "correlation_complete", "state_continuity"}
    if any(set(trial) != trial_fields for trial in trials):
        raise ContractError("trial evidence is malformed")
    evidence = value["evidence_snapshot"]
    if not isinstance(evidence, list) or not evidence:
        raise ContractError("evidence_snapshot is required")
    if any(item.get("request_id") != value["request_id"] for item in evidence):
        raise ContractError("evidence correlation identity mismatch")
    return value


def ledger_path() -> Path:
    return Path(os.getenv("LEDGER_PATH", "/tmp/virtualization-ai-501-evidence.jsonl"))


def load_ledger(path: Path | None = None) -> list[dict]:
    selected = path or ledger_path()
    return [] if not selected.exists() else [json.loads(line) for line in selected.read_text().splitlines() if line.strip()]


def append_records(records: list[dict]) -> None:
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with LOCK:
        with path.open("a", encoding="utf-8") as stream:
            for record in records:
                stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())


def source_state(payload: dict) -> str:
    mode = os.getenv("ADAPTER_MODE", "rehearsal").lower()
    if mode == "rehearsal":
        return "REHEARSAL"
    if mode != "live":
        return "OFFLINE"
    live = [item for item in payload["evidence_snapshot"] if item.get("source_state") == "LIVE" and item.get("freshness") == "FRESH"]
    kinds = {item.get("kind") for item in live}
    observed_vms = {item.get("payload", {}).get("vm") for item in live if item.get("kind") == "VM"}
    fleet_vms = {vm["name"] for vm in payload["fleet"]["virtual_machines"]}
    return "LIVE" if REQUIRED_LIVE_KINDS.issubset(kinds) and fleet_vms.issubset(observed_vms) else "OFFLINE"


def qualify(payload: dict) -> tuple[str, list[str], str, str]:
    trials = payload["trials"]
    envelope = payload["envelope"]
    if any(not trial["correlation_complete"] for trial in trials):
        return "ABSTAIN", ["CORRELATION_INCOMPLETE"], "abstain-correlation-incomplete", "INCOMPLETE"
    if any(not trial["state_continuity"] for trial in trials):
        return "ABSTAIN", ["STATE_CONTINUITY_INCOMPLETE"], "abstain-state-continuity-incomplete", "INCOMPLETE"
    if any(trial["containment_breaches"] for trial in trials):
        return "REFUSE", ["FAILURE_CONTAINMENT_BREACH"], "refuse-failure-containment", "FAIL"
    if any(trial["success_rate"] < envelope["min_success_rate"] or trial["p95_ms"] > envelope["max_p95_ms"] for trial in trials):
        return "REFUSE", ["SLO_ENVELOPE_BREACH", "CAPACITY_ENVELOPE_BREACH"], "refuse-slo-envelope", "FAIL"
    if any(trial["concurrency"] > envelope["max_concurrency"] or trial["cpu_saturation_pct"] > envelope["max_cpu_saturation_pct"] for trial in trials):
        return "REFUSE", ["CAPACITY_ENVELOPE_BREACH"], "refuse-capacity-envelope", "FAIL"
    return "ALLOW_REVIEW", ["QUALIFICATION_ENVELOPE_SATISFIED"], "allow-human-promotion-review", "PASS"


def make_records(payload: dict, state: str, decision: str, reasons: list[str]) -> list[dict]:
    now = utc_now()
    records = []
    for journey_state in JOURNEY:
        base = {"schema_version": EVIDENCE_VERSION, "evidence_id": str(uuid.uuid4()), "request_id": payload["request_id"], "state": journey_state, "kind": "DECISION", "source": "qualification-adapter", "source_state": state, "observed_at": now, "freshness": "FRESH" if state != "OFFLINE" else "UNKNOWN", "payload": {"decision": decision, "reason_codes": reasons}}
        base["digest"] = canonical_sha256(base)
        records.append(base)
    return records


def evaluate(value: object) -> tuple[dict, list[dict]]:
    payload = validate_request(value)
    state = source_state(payload)
    decision, reasons, rule, status = qualify(payload)
    records = make_records(payload, state, decision, reasons)
    append_records(records)
    qualification = {"status": status, "fleet_size": len(payload["fleet"]["virtual_machines"]), "trial_results": payload["trials"], "envelope": payload["envelope"]}
    response = {"schema_version": RESPONSE_VERSION, "request_id": payload["request_id"], "decision": decision, "reason": reasons[0].replace("_", " ").title(), "source_state": state, "reason_codes": reasons, "policy": {"id": POLICY["policy_id"], "version": POLICY["version"], "matched_rules": [rule]}, "authority": {"human_promotion_required": True, "promotion_performed": False, "certification_performed": False, "llm_authority": "NONE"}, "qualification": qualification, "evidence": records}
    with LOCK:
        COUNTERS[decision] += 1
        COUNTERS["ledger_records"] += len(records)
    return response, records


def metrics_text() -> str:
    with LOCK:
        counts = dict(COUNTERS)
    lines = ["# HELP virtualization_ai_501_qualification_decisions_total Deterministic qualification decision counts.", "# TYPE virtualization_ai_501_qualification_decisions_total counter"]
    for decision in ("ALLOW_REVIEW", "REFUSE", "ABSTAIN"):
        lines.append(f'virtualization_ai_501_qualification_decisions_total{{decision="{decision}"}} {counts.get(decision, 0)}')
    lines.extend(["# HELP virtualization_ai_501_ledger_records_total Durable evidence records written.", "# TYPE virtualization_ai_501_ledger_records_total counter", f"virtualization_ai_501_ledger_records_total {counts.get('ledger_records', 0)}", ""])
    return "\n".join(lines)


class Handler(BaseHTTPRequestHandler):
    server_version = "virtualization-ai-501/1"

    def send_json(self, status: int, value: object) -> None:
        encoded = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self.send_json(200, {"status": "ok", "mode": os.getenv("ADAPTER_MODE", "rehearsal").upper(), "authority": "HUMAN_PROMOTION_REQUIRED"})
        elif self.path == "/metrics":
            encoded = metrics_text().encode(); self.send_response(200); self.send_header("Content-Type", "text/plain; version=0.0.4"); self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)
        elif self.path.startswith("/api/v1/qualifications/"):
            request_id = self.path.rsplit("/", 1)[-1]; records = [record for record in load_ledger() if record.get("request_id") == request_id]; self.send_json(200 if records else 404, {"request_id": request_id, "evidence": records} if records else {"error": "request not found"})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/v1/qualifications":
            self.send_json(404, {"error": "not found"}); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 131072:
                raise ContractError("request body length is invalid")
            response, _ = evaluate(json.loads(self.rfile.read(length))); self.send_json(200, response)
        except (ContractError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc), "decision": "REFUSE"})

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    ThreadingHTTPServer(("0.0.0.0", int(os.getenv("ADAPTER_PORT", "8080"))), Handler).serve_forever()


if __name__ == "__main__":
    main()
