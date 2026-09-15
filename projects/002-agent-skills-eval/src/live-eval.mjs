// Optional real-model run. Never runs inference without an explicit --run flag.
import { readFileSync, mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { evaluateSkills, loadSkill, OpenAICompatibleProvider } from '../upstream/dist/index.js';

const root = fileURLToPath(new URL('../', import.meta.url));
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Optional live evaluation. Set EVAL_BASE_URL, EVAL_API_KEY, EVAL_TARGET, EVAL_JUDGE, then run npm run live -- --run. EVAL_REPEATS defaults to 5 (1–10). This makes billable API calls. No inference was run.');
} else {
  if (args.length !== 1 || args[0] !== '--run') throw new Error('Only --run is supported.');
  const required = ['EVAL_BASE_URL', 'EVAL_API_KEY', 'EVAL_TARGET', 'EVAL_JUDGE'];
  const missing = required.filter(key => !process.env[key]);
  if (missing.length) throw new Error(`Missing environment variables: ${missing.join(', ')}`);
  const repeats = Number(process.env.EVAL_REPEATS ?? 5);
  if (!Number.isInteger(repeats) || repeats < 1 || repeats > 10) throw new Error('EVAL_REPEATS must be an integer from 1 to 10.');
  const skillDir = path.join(root, 'fixtures/refund-review');
  const skill = loadSkill(skillDir, { strict: true });
  if (!skill.evals.length || skill.evals.some(e => e.files?.length || !e.assertions?.length)) {
    throw new Error('Live fixture must contain cases, self-contained assertions and no asymmetric file attachments.');
  }
  const options = { baseUrl: process.env.EVAL_BASE_URL, apiKey: process.env.EVAL_API_KEY, timeoutMs: 120000 };
  const target = new OpenAICompatibleProvider({ ...options, model: process.env.EVAL_TARGET });
  const judge = new OpenAICompatibleProvider({ ...options, model: process.env.EVAL_JUDGE });
  mkdirSync(path.join(root, 'artifacts/live'), { recursive: true });
  const workspace = mkdtempSync(path.join(root, 'artifacts/live/run-'));
  const iterations = [];
  for (let i = 0; i < repeats; i++) {
    console.log(`Live iteration ${i + 1}/${repeats}; ${skill.evals.length} cases, two modes.`);
    const result = await evaluateSkills({ root: skillDir, workspace, baseline: true, strict: true,
      workspaceLayout: 'iteration', concurrency: 2,
      target: { model: target.model, provider: target }, judge: { model: judge.model, provider: judge },
      reportTitle: `Refund Skill — real-model evaluation ${i + 1}`, onEvent() {},
    });
    const benchmark = JSON.parse(readFileSync(result.skills[0].benchmarkPath, 'utf8'));
    iterations.push({ iteration: result.iteration, passed: result.passed, failed: result.failed,
      report: path.relative(workspace, result.reportPath).replaceAll('\\', '/'), ...benchmark.run_summary });
  }
  const summary = { generatedAt: new Date().toISOString(), realModelQualityMeasured: true,
    target: target.model, judge: judge.model, repeats, evalsPerIteration: skill.evals.length,
    params: 'Provider defaults; no cross-model sampling parameters forced.',
    protocolLimitations: ['Fixed with-skill-first order in upstream runner.', 'Six hand-authored pilot cases are not a representative business benchmark.', 'No human calibration or significance test is performed by this script.'],
    meanPassRateDelta: iterations.reduce((sum, run) => sum + run.delta.pass_rate, 0) / repeats, iterations };
  writeFileSync(path.join(workspace, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log(`Saved reports and summary to ${workspace}`);
}
