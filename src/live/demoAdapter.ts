import qualifiedRequest from '../../contracts/examples/qualified-fleet-request.json'
import capacityRequest from '../../contracts/examples/capacity-breach-request.json'
import correlationRequest from '../../contracts/examples/correlation-gap-request.json'
import qualifiedResponse from '../../contracts/examples/qualified-fleet-response.json'
import capacityResponse from '../../contracts/examples/capacity-breach-response.json'
import correlationResponse from '../../contracts/examples/correlation-gap-response.json'
import { createJsonAdapter, registerAdapter } from './adapters'

const cases = [
  ['qualification-pass', qualifiedRequest, qualifiedResponse],
  ['qualification-capacity', capacityRequest, capacityResponse],
  ['qualification-correlation', correlationRequest, correlationResponse],
] as const

for (const [id, body, data] of cases) {
  registerAdapter(createJsonAdapter({ id, url: '/api/v1/qualifications', method: 'POST', body, timeoutMs: 2_500, rehearsal: { data, collectedAt: '2026-09-28T12:05:00.000Z' } }))
}
