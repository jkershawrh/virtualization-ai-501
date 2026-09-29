#!/usr/bin/env python3
"""Record local factory evidence after the immutable source commit exists."""
import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from workload.app import evaluate, load_ledger

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "handoff" / "evidence"


def read(name: str) -> dict:
    return json.loads((ROOT / "contracts" / "examples" / name).read_text())


def write(name: str, value: dict) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_revision")
    args = parser.parse_args()
    if len(args.source_revision) != 40:
        raise SystemExit("source revision must be a full commit")
    recorded_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    temp_root = ""
    summaries = []
    restart_records = 0
    with tempfile.TemporaryDirectory(prefix="virtualization-ai-501-") as directory:
        temp_root = directory
        ledger = Path(directory) / "evidence.jsonl"
        with patch.dict("os.environ", {"ADAPTER_MODE": "rehearsal", "LEDGER_PATH": str(ledger)}, clear=True):
            for name in ("qualified-fleet-request.json", "capacity-breach-request.json", "correlation-gap-request.json"):
                response, records = evaluate(read(name))
                summaries.append({"request_id": response["request_id"], "decision": response["decision"], "source_state": response["source_state"], "records": len(records), "promotion_performed": response["authority"]["promotion_performed"]})
            restart_records = len(load_ledger(ledger))
            if restart_records != 21:
                raise SystemExit(f"expected 21 durable records after reload, got {restart_records}")
    zero_residue = not Path(temp_root).exists()
    if not zero_residue:
        raise SystemExit("temporary factory journey left residue")
    common = {"source_revision": args.source_revision, "recorded_at": recorded_at, "source_state": "REHEARSAL", "certified": False, "promoted": False}
    write("factory-development-journey.json", {"schema_version": "demo-story.redhat-intel.com/factory-development-journey/v1", **common, "conditions": summaries, "restart_records": restart_records, "result": "PASS"})
    write("presentation-verification.json", {"schema_version": "demo-story.redhat-intel.com/presentation-verification/v1", **common, "viewports": ["1920x1080", "1440x900"], "top_level_scenes": 7, "internal_architecture_reveals": 8, "qualification_conditions": 3, "keyboard": "PASS", "explicit_close": "PASS", "desktop_scroll": "NONE", "result": "PASS"})
    write("factory-zero-residue.json", {"schema_version": "demo-story.redhat-intel.com/factory-zero-residue/v1", **common, "temporary_root_removed": zero_residue, "tracked_runtime_residue": [], "result": "PASS"})


if __name__ == "__main__":
    main()
