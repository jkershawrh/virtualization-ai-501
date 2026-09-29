# Virtualization + AI 501 — Qualify a Governed VM Inference Fleet

This private factory workspace extends the exact Virtualization + AI 401 source revision `0672f307bf48eae2803958e290997d8c046b5c42`. It adds a materially distinct qualification contract for fleet-scale inference on OpenShift Virtualization: multiple VM clients, baseline/migration/disruption trials, directly evidenced workload placement and CPU dependency, declared SLO/capacity/concurrency envelopes, state and evidence continuity, failure containment, correlated telemetry, deterministic policy, and human-controlled promotion review.

## Honest source state

The default is `REHEARSAL`. The factory session did not directly observe live OpenShift, KubeVirt VM state, migration, disruption, Intel Xeon placement, inference execution, or correlated telemetry. The adapter can emit `LIVE` only when fresh current-session evidence includes every required kind and every declared VM identity; otherwise it emits `OFFLINE`.

Quantitative values in checked-in fixtures exercise the contract and UI. They are not production performance claims.

## Two separate experiences

- The seven-scene Triforce-style presentation fits a 5–7 minute presenter path and ends with an explicit close and one lab handoff.
- The Showroom lab is a separate 75–90 minute build/break/qualify/restart/reclaim experience.

Both use the same `DISCOVER → BASELINE → MIGRATE → DISRUPT → CORRELATE → QUALIFY → HANDOFF` evidence journey.

## Factory boundary

The adapter evaluates supplied evidence and appends a durable ledger. It has no infrastructure mutation, automatic remediation, certification, ordering, or promotion authority. Launchpad independently owns source approval, trusted rendering, destination artifact review, live-seat testing, capacity graduation, reclaim verification, certification, promotion, and publication.

## Verification

`npm run check` validates the reviewed blueprint, Python contract/factory tests, Helm rendering, React tests, production build, and offline assets. `npm run test:visual` verifies browser behavior, keyboard access, and viewport fit. The release workflow additionally runs `npm audit`, a zero High/Critical image scan gate, SPDX SBOM generation, OIDC keyless signing, SLSA provenance attestation, and exact-digest pulls for Linux/AMD64 images.
