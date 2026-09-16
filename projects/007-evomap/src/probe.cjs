'use strict';
// Calls the original upstream modules. Fixtures below are synthetic, not Hub assets.
const fs = require('fs');
const path = require('path');
const assert = require('node:assert/strict');
const upstream = path.resolve(__dirname, '../.cache/upstream');
const { selectGene, selectCapsule } = require(path.join(upstream, 'src/gep/selector'));
const { computeAssetId, verifyAssetId, SCHEMA_VERSION } = require(path.join(upstream, 'src/gep/contentHash'));
const { buildGepPrompt } = require(path.join(upstream, 'src/gep/prompt'));
const seed = JSON.parse(fs.readFileSync(path.join(upstream, 'assets/gep/genes.seed.json'), 'utf8'));
// Upstream selection tests use the same deterministic control for random drift.
Math.random = () => 0.99;
const selected = selectGene(seed.genes, ['log_error', 'test_failure'], { driftEnabled: false });
assert.ok(selected.selected);
assert.equal(selected.selected.category, 'repair');
const miss = selectGene(seed.genes, ['zz_unrelated_74392'], { driftEnabled: false });
// Do not assume an arbitrary signal cannot match a large starter pool.
// A separate controlled pool provides the actual negative control.
const controlledMiss = selectGene([{ type: 'Gene', id: 'research_exact_only',
  category: 'repair', signals_match: ['log_error'], strategy: ['inspect'],
  validation: ['node --version'] }], ['zz_unrelated_74392'], { driftEnabled: false });
assert.equal(controlledMiss.selected, null);
const fixture = {
  type: 'Capsule', id: 'research_upload_timeout_example',
  trigger: ['research_upload_timeout'], gene: 'research_chunk_upload',
  summary: 'Synthetic example only: evaluate chunked upload and bounded retries.',
  confidence: 0.9,
};
assert.equal(selectCapsule([fixture], ['research_upload_timeout']).id, fixture.id);
const hashed = { ...fixture, asset_id: computeAssetId(fixture) };
assert.equal(verifyAssetId(hashed), true);
const changed = { ...hashed, summary: 'Changed after hashing' };
assert.equal(verifyAssetId(changed), false);
const nonsense = { type: 'Gene', id: 'research_nonsense', strategy: ['2 + 2 = 5'] };
nonsense.asset_id = computeAssetId(nonsense);
assert.equal(verifyAssetId(nonsense), true);
const prompt = buildGepPrompt({
  nowIso: '2026-09-16T00:00:00.000Z', context: 'RESEARCH_ONLY_NO_EXECUTION: inspect a synthetic upload timeout.',
  signals: ['log_error', 'test_failure'], selector: { selected: selected.selected.id },
  parentEventId: null, selectedGene: selected.selected, capsuleCandidates: '(none)',
  genesPreview: JSON.stringify([selected.selected]), capsulesPreview: '[]',
  capabilityCandidatesPreview: '(none)', externalCandidatesPreview: '(none)',
  hubMatchedBlock: '', cycleId: 'RESEARCH-001', recentHistory: '', failedCapsules: [],
  hubLessons: [], strategyPolicy: null, initialUserPrompt: null,
});
assert.equal(typeof prompt, 'string');
assert.ok(prompt.includes('RESEARCH_ONLY_NO_EXECUTION'));
assert.ok(prompt.includes(selected.selected.id));
const result = {
  synthetic_fixture: true, random_control: 'Math.random returns 0.99 (selection only; not a production run)', upstream_version: require(path.join(upstream, 'package.json')).version,
  sdk_schema: SCHEMA_VERSION, seed_gene_count: seed.genes.length,
  checks: {
    error_signals_select_repair: selected.selected.id,
    controlled_unrelated_signal_selects_nothing: controlledMiss.selected === null,
    full_seed_unrelated_signal_selected: miss.selected?.id || null,
    full_seed_unrelated_drift_mode: miss.driftMode || null,
    matching_capsule_retrieved: fixture.id,
    original_hash_valid: verifyAssetId(hashed), tampered_hash_valid: verifyAssetId(changed),
    nonsense_with_valid_hash_accepted: verifyAssetId(nonsense),
    prompt_is_text: typeof prompt === 'string', prompt_contains_context_and_gene: true,
  },
  prompt_chars: prompt.length,
  limitation: 'No LLM execution, code repair, Hub validation, publication, or token savings measured.',
};
fs.writeFileSync(path.join(__dirname, '../.cache/generated-prompt.txt'), prompt);
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
