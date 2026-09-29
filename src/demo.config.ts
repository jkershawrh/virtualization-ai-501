import type { DemoConfig } from './types'

const technicalTopology = {
  boundary: { label: 'Namespaced qualification boundary', detail: 'read-only evidence evaluation; no cluster mutation or promotion authority' },
  entry: { id: 'human', kind: 'authority', label: 'Human reviewer', detail: 'sets the envelope and owns promotion' },
  primaryPath: [
    { id: 'fleet', kind: 'kubevirt', label: 'VM inference fleet', detail: 'distinct VirtualMachine and VMI identities', edgeLabel: 'generate load' },
    { id: 'inference', kind: 'service', label: 'Inference service', detail: 'execution identity and returned request evidence', edgeLabel: 'infer' },
    { id: 'telemetry', kind: 'evidence', label: 'Correlated telemetry', detail: 'request, VM, migration, disruption, CPU, and continuity', edgeLabel: 'correlate' },
    { id: 'policy', kind: 'policy', label: 'Deterministic policy', detail: 'ALLOW_REVIEW · REFUSE · ABSTAIN', endpoint: 'POST /api/v1/qualifications', edgeLabel: 'qualify' },
  ],
  supportPath: [
    { id: 'migration', kind: 'event', label: 'Migration trial', detail: 'externally executed and directly observed', edgeLabel: 'change placement' },
    { id: 'disruption', kind: 'event', label: 'Disruption trial', detail: 'bounded failure with containment evidence', edgeLabel: 'stress boundary' },
    { id: 'ledger', kind: 'data', label: 'Durable ledger', detail: 'digest-bearing qualification journey', edgeLabel: 'preserve' },
  ],
  optionalPath: { id: 'launchpad', kind: 'external', label: 'Launchpad', detail: 'independent certification and promotion remain outside the factory', edgeLabel: 'proposed handoff' },
}

export const demoConfig: DemoConfig = {
  id: 'virtualization-ai-501',
  title: 'Qualify a Governed VM Inference Fleet',
  subtitle: 'Migration, disruption, placement, capacity, and continuity become one reviewable evidence case',
  event: 'Virtualization + AI 501',
  audience: 'Virtualization, AI platform, performance, and lab operations teams',
  cta: 'Decide whether the candidate has earned human promotion review.',
  brand: { primary: { name: 'Red Hat', logo: '/logos/redhat.svg', alt: 'Red Hat' }, partner: { name: 'Intel', logo: '/logos/intel.png', alt: 'Intel' }, attribution: 'Red Hat × Intel' },
  acts: [
    { id: 'discover', label: '01', title: 'DISCOVER', scenes: [
      { id: 'discover', type: 'intro', beat: 'ordinary-world', eyebrow: 'DISCOVER · REHEARSAL', title: 'One healthy VM does not qualify a fleet', subtitle: 'Scale introduces placement, concurrency, migration, disruption, continuity, and containment dependencies.', speakerPrompt: 'State REHEARSAL. LIVE requires directly observed OpenShift, KubeVirt, VM, inference, CPU placement, migration, disruption, telemetry, and continuity evidence.' },
    ] },
    { id: 'baseline', label: '02', title: 'BASELINE', scenes: [
      { id: 'baseline', type: 'guided-architecture', beat: 'system-reveal', eyebrow: 'BASELINE', title: 'Every claim needs an owner and an evidence path', body: 'Reveal the causal boundary before showing a result.', layers: [
        { id: 'fleet-q', component: 'Fleet identity', tone: 'primary', question: 'What exactly is under qualification?', answer: 'Distinct VM, VMI, namespace, service, and node identities.', detail: 'Unknown or duplicate identity blocks the run.', activeNodeIds: ['human', 'fleet'] },
        { id: 'cpu-q', component: 'Placement', tone: 'partner', question: 'Where did each workload execute?', answer: 'Node, architecture, and CPU vendor are direct evidence.', detail: 'Intel Xeon is never inferred from an image or label alone.', activeNodeIds: ['fleet', 'telemetry'] },
        { id: 'scale-q', component: 'Envelope', tone: 'success', question: 'What counts as enough capacity?', answer: 'The reviewer declares SLO, concurrency, and CPU boundaries first.', detail: 'Observed measurements are evaluated; presentation copy supplies none.', activeNodeIds: ['human', 'inference', 'policy'] },
        { id: 'authority-q', component: 'Authority', tone: 'partner', question: 'Who may promote the result?', answer: 'Only a human after independent Launchpad gates.', detail: 'The adapter, model, and factory cannot certify or promote.', activeNodeIds: ['policy', 'ledger', 'launchpad'] },
      ], technicalTopology, speakerPrompt: 'Keep evidence collection, deterministic policy, and promotion authority visibly separate.' },
    ] },
    { id: 'migrate', label: '03', title: 'MIGRATE', scenes: [
      { id: 'migrate', type: 'reframe', beat: 'stakes', eyebrow: 'MIGRATE', title: 'A migration event is not a qualification result', before: 'The VMI moved', after: 'Placement + inference + state + correlation remained continuous', detail: 'The changed condition must survive the same declared envelope.', speakerPrompt: 'Migration is externally executed; this adapter only evaluates supplied evidence.' },
    ] },
    { id: 'disrupt', label: '04', title: 'DISRUPT', scenes: [
      { id: 'disrupt', type: 'live-journey', beat: 'live-proof', eyebrow: 'DISRUPT · REHEARSAL', title: 'Run three fleet outcomes through one contract', body: 'The evidence case accumulates instead of replacing earlier results.', cta: 'Run qualification conditions', nodes: [
        { id: 'fleet', label: 'Fleet baseline', detail: 'identity + placement', tone: 'primary' },
        { id: 'migration', label: 'Migration', detail: 'service continuity', tone: 'primary' },
        { id: 'disruption', label: 'Disruption', detail: 'failure containment', tone: 'partner' },
        { id: 'telemetry', label: 'Correlation', detail: 'one evidence graph', tone: 'success' },
        { id: 'policy', label: 'Qualification', detail: 'human review only', tone: 'success' },
      ], technicalTopology, steps: [
        { id: 'qualified', title: 'Envelope satisfied', detail: 'All three trials preserve containment, correlation, and state continuity.', adapterId: 'qualification-pass', activeNode: 4, activeNodeIds: ['fleet', 'inference', 'migration', 'disruption', 'telemetry', 'policy', 'ledger'], resultFields: [{ key: 'decision', label: 'Decision' }, { key: 'reason', label: 'Reason' }, { key: 'source_state', label: 'Source' }] },
        { id: 'capacity', title: 'Capacity boundary crossed', detail: 'The observed trial breaches the declared envelope and is refused.', adapterId: 'qualification-capacity', activeNode: 4, activeNodeIds: ['fleet', 'inference', 'telemetry', 'policy', 'ledger'], resultFields: [{ key: 'decision', label: 'Decision' }, { key: 'reason', label: 'Reason' }, { key: 'source_state', label: 'Source' }] },
        { id: 'correlation', title: 'Evidence chain breaks', detail: 'Missing correlation prevents a trustworthy fleet conclusion.', adapterId: 'qualification-correlation', activeNode: 4, activeNodeIds: ['migration', 'disruption', 'telemetry', 'policy', 'ledger'], resultFields: [{ key: 'decision', label: 'Decision' }, { key: 'reason', label: 'Reason' }, { key: 'source_state', label: 'Source' }] },
      ], speakerPrompt: 'Explain why REFUSE and ABSTAIN are distinct operational outcomes.' },
    ] },
    { id: 'correlate', label: '05', title: 'CORRELATE', scenes: [
      { id: 'correlate', type: 'mechanisms', beat: 'root-cause', eyebrow: 'CORRELATE', title: 'Continuity is a chain, not a green dashboard', mechanisms: [
        { id: 'identity', label: 'Identity', claim: 'VM → node → CPU → request', detail: 'The workload and placement records bind to the same request.', tone: 'primary' },
        { id: 'state', label: 'State', claim: 'before → change → after', detail: 'Migration and restart preserve an inspectable ledger.', tone: 'success' },
        { id: 'containment', label: 'Containment', claim: 'failure stays bounded', detail: 'A disruption cannot leak across the declared fleet boundary.', tone: 'partner' },
      ], speakerPrompt: 'No metric is trusted unless its identity and correlation path survive the changed condition.' },
    ] },
    { id: 'qualify', label: '06', title: 'QUALIFY', scenes: [
      { id: 'qualify', type: 'comparison', beat: 'trials', eyebrow: 'QUALIFY', title: 'Policy turns evidence into a bounded recommendation', columns: [
        { label: 'Complete + inside envelope', value: 'ALLOW_REVIEW', detail: 'Eligible for human promotion review only', tone: 'success' },
        { label: 'Known boundary breach', value: 'REFUSE', detail: 'SLO, capacity, or containment failed', tone: 'danger' },
        { label: 'Evidence incomplete', value: 'ABSTAIN', detail: 'Correlation or state continuity is missing', tone: 'partner' },
      ], speakerPrompt: 'No recommendation changes Launchpad catalog or runtime state.' },
    ] },
    { id: 'handoff', label: '07', title: 'HANDOFF', scenes: [
      { id: 'handoff', type: 'evidence-payoff', beat: 'transformation', eyebrow: 'HANDOFF', title: 'A candidate is immutable before it becomes certifiable', adapterIds: ['qualification-pass', 'qualification-capacity', 'qualification-correlation'], fallbackLine: 'Run all three REHEARSAL conditions to populate the evidence payoff', evidenceFields: [{ key: 'decision', label: 'Decision' }, { key: 'reason', label: 'Reason' }, { key: 'source_state', label: 'Source' }], line1: 'DISCOVER → BASELINE → MIGRATE → DISRUPT → CORRELATE → QUALIFY → HANDOFF remains durable.', line2: 'Launchpad still owns trusted rendering, live seats, capacity graduation, certification, and promotion.', cta: 'Continue in the separate 75–90 minute Showroom lab →', speakerPrompt: 'Close presentation. Offer one deliberate lab handoff; do not imply orderability.' },
    ] },
  ],
  journeyHandoffs: [{ depth: 'lab', title: 'Qualify a VM inference fleet lab', duration: '75–90 minutes', question: 'Can the learner build, stress, qualify, restart, and reclaim the evidence case?', technology: 'OpenShift Virtualization · Linux/AMD64 · correlated telemetry · deterministic policy', instruction: 'Use the separate Showroom lab and stop at the factory-candidate handoff.' }],
}
