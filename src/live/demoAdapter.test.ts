import { afterEach, expect, it, vi } from 'vitest'
import './demoAdapter'
import { getAdapter } from './adapters'

afterEach(() => vi.unstubAllGlobals())

it.each([
  'https://presentation.example/',
  'https://labs.example/labs/order-501/proxy/tool/story/?act=3&scene=0',
])('keeps qualification POST beneath the presentation at %s', async (base) => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ decision: 'ALLOW_REVIEW' }) })
  vi.stubGlobal('fetch', fetchMock)
  const adapter = getAdapter('qualification-pass')!
  await adapter.load(new AbortController().signal)
  const [path, options] = fetchMock.mock.calls[0]
  const resolved = new URL(path, base)
  expect(resolved.pathname).toBe(new URL('api/v1/qualifications', base).pathname)
  expect(options.method).toBe('POST')
  expect(JSON.parse(options.body).request_id).toBeTruthy()
})
