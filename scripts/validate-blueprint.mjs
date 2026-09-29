#!/usr/bin/env node
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'

const path = resolve(process.argv[2] ?? 'demo-blueprint.yaml')
const text = await readFile(path, 'utf8')
const errors = []
for (const section of ['status: approved', 'source:', 'intent:', 'architecture:', 'operational_pattern:', 'evidence:', 'decisions:', 'ai_assessment:', 'story_mapping:']) if (!text.includes(section)) errors.push(`Missing ${section}`)
for (const state of ['DISCOVER', 'BASELINE', 'MIGRATE', 'DISRUPT', 'CORRELATE', 'QUALIFY', 'HANDOFF']) if (!text.includes(state)) errors.push(`Missing journey state ${state}`)
for (const term of ['ALLOW_REVIEW', 'REFUSE', 'ABSTAIN', 'needed: false', 'action_authority: none', 'factory_may_certify: false', 'factory_may_promote: false']) if (!text.includes(term)) errors.push(`Missing safety term ${term}`)
if (errors.length) { errors.forEach((error) => console.error(`ERROR ${error}`)); process.exit(1) }
console.log(`Blueprint structure is valid: ${path}`)
