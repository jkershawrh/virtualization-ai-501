# Journey acceptance matrix

| Stage | Learner action | Required proof | Fail-closed result |
|---|---|---|---|
| DISCOVER | Inventory namespace, VM/VMI fleet, service, nodes, CPU dependencies, and evidence sources | Distinct identities and source state | Invalid contract or `ABSTAIN` on unknown evidence |
| BASELINE | Declare and run the normal-load envelope | Current inference and telemetry measurements | `REFUSE` on known SLO/capacity breach |
| MIGRATE | Observe externally executed placement change | Destination VM/node/CPU, inference, state, and correlation continuity | `ABSTAIN` when continuity is incomplete |
| DISRUPT | Exercise bounded failure | Unaffected clients remain inside the envelope; zero containment breaches | `REFUSE` on containment or envelope breach |
| CORRELATE | Join request, VM, CPU, event, inference, and telemetry identities | One complete evidence graph and reloadable ledger | `ABSTAIN` on a broken link |
| QUALIFY | Evaluate deterministic ordered policy | Policy version, matched rule, `ALLOW_REVIEW`/`REFUSE`/`ABSTAIN` | No model or adapter override |
| HANDOFF | Review immutable artifacts and reclaim | Digests, scans, SBOM, signature, provenance, journey, restart, zero residue | All Launchpad authority stays false |

## Release status

- Presenter scenes: 7 (green)
- Presenter duration: 5–7 minutes (green)
- Lab duration: 75–90 minutes (green)
- Architecture-to-proof continuity: same fleet/evidence/policy path (green)
- Fallback labeling: `REHEARSAL`/`OFFLINE` (green)
- Live destination evidence: not observed (blocking activation, honest factory candidate)
