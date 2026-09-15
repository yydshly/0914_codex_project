// Mechanism probes against the unmodified upstream library. No real LLM calls.
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync, copyFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  loadSkill, runEval, evaluateSkills, gradeOutputs, buildBenchmark,
  OpenAICompatibleProvider,
} from '../upstream/dist/index.js';

const root = fileURLToPath(new URL('../', import.meta.url));
const artifacts = path.join(root, 'artifacts');
mkdirSync(path.join(artifacts, 'runs'), { recursive: true });
const runDir = mkdtempSync(path.join(artifacts, 'runs', 'probe-'));
const observations = [];
const execFileAsync = promisify(execFile);
const source = JSON.parse(readFileSync(path.join(root, 'upstream-source.json'), 'utf8').replace(/^\uFEFF/, ''));

function provider(label, respond, capabilities = { systemRole: true, attachments: false }) {
  const calls = [];
  const p = {
    name: label, model: label, capabilities, calls,
    async complete(user) { return p.completeChat({ user }); },
    async completeChat(args) {
      calls.push(structuredClone(args));
      const value = await respond(args, calls.length);
      return {
        provider: label, model: label, output: '', latencyMs: 0,
        inputTokens: 0, outputTokens: 0, costUsd: 0,
        ...(typeof value === 'string' ? { output: value } : value),
      };
    },
  };
  return p;
}

function judge(label = 'synthetic-keyword-judge') {
  return provider(label, ({ user }) => {
    const rubric = JSON.parse(user.split('Assertions:\n')[1].split('\nModel output:')[0].trim());
    const output = user.split('Model output:\n')[1]?.split('\nOutput files:')[0] ?? '';
    return JSON.stringify({ assertion_results: rubric.map(text => ({
      text, passed: output.includes('February: 18'),
      evidence: 'Synthetic literal check for February: 18; not an LLM judgment.',
    })) });
  });
}

function fixture(name, evals, instructions = 'This instruction is irrelevant to CSV analysis.') {
  const dir = path.join(runDir, 'fixtures', name);
  mkdirSync(path.join(dir, 'evals', 'files'), { recursive: true });
  writeFileSync(path.join(dir, 'SKILL.md'), `---\nname: ${name}\ndescription: Controlled research fixture.\n---\n${instructions}\n`);
  writeFileSync(path.join(dir, 'evals', 'files', 'input.csv'), 'month,revenue\nJanuary,12\nFebruary,18\n');
  writeFileSync(path.join(dir, 'evals', 'evals.json'), JSON.stringify({ skill_name: name, evals }, null, 2));
  return loadSkill(dir, { strict: true });
}

async function run(skill, target, evaluator = judge(), modes = ['with_skill', 'without_skill']) {
  return runEval({
    skill, eval: skill.evals[0], modes,
    target: { model: target.model, provider: target },
    judge: { model: evaluator.model, provider: evaluator },
    workspace: path.join(runDir, skill.name), iteration: 1,
  });
}

async function probe(id, title, action) {
  try {
    const observed = await action();
    observations.push({ id, title, verified: true, observed });
    console.log(`VERIFIED ${id}: ${title}`);
  } catch (error) {
    observations.push({ id, title, verified: false, error: String(error.stack ?? error) });
    process.exitCode = 1;
    console.error(`FAILED ${id}: ${error.message}`);
  }
}

const csvTask = {
  id: 'csv', prompt: 'Find the highest revenue month from the task data.',
  files: ['evals/files/input.csv'], assertions: ['The output identifies February with revenue 18.'],
};

await probe('E01', '附件不对称可制造虚假的 Skill 增益', async () => {
  const skill = fixture('attachment-confound', [csvTask]);
  // Deliberately ignores system / Skill instructions and only reads task data.
  const target = provider('synthetic-csv-reader', ({ user }) => user.includes('February,18') ? 'February: 18' : 'No task data');
  const result = await evaluateSkills({
    root: skill.dir, workspace: path.join(runDir, 'confound-report'), baseline: true,
    target: { model: target.model, provider: target }, judge: { model: 'synthetic-keyword-judge', provider: judge() },
    workspaceLayout: 'iteration', strict: true, onEvent() {},
    reportTitle: '机制演示：模拟响应，无真实模型；附件不对称导致的虚假增益',
  });
  const benchmark = JSON.parse(readFileSync(result.skills[0].benchmarkPath, 'utf8'));
  assert.equal(benchmark.run_summary.delta.pass_rate, 1);
  assert.equal(target.calls[0].user.includes('February,18'), true);
  assert.equal(target.calls[1].user.includes('February,18'), false);
  copyFileSync(result.reportPath, path.join(artifacts, 'mechanism-demo.html'));
  copyFileSync(result.skills[0].benchmarkPath, path.join(artifacts, 'attachment-benchmark.json'));
  return { withSkill: 1, withoutSkill: 0, deltaPercentagePoints: 100, targetReadsSkill: false,
    explanation: 'Synthetic scores. Input-data availability alone accounts for the entire difference.' };
});

await probe('E02', '相同任务数据放入 prompt 后，虚假增益消失', async () => {
  const skill = fixture('equal-inputs', [{ ...csvTask, files: [], prompt: `${csvTask.prompt}\nmonth,revenue\nJanuary,12\nFebruary,18` }]);
  const target = provider('synthetic-csv-reader', ({ user }) => user.includes('February,18') ? 'February: 18' : 'No task data');
  const result = await run(skill, target);
  assert.equal(target.calls[0].user, target.calls[1].user);
  const rates = Object.values(result.modes).map(m => m.grading.summary.pass_rate);
  assert.deepEqual(rates, [1, 1]);
  return { rates, deltaPercentagePoints: 0, identicalUserInput: true };
});

await probe('E03', '只有工具检查时不调用 AI 裁判', async () => {
  const evaluator = provider('must-not-run', () => { throw new Error('Judge unexpectedly called'); });
  const result = await gradeOutputs({ modelOutput: '', assertions: [],
    toolCalls: [{ type: 'function', function: { name: 'lookup', arguments: '{"city":"Shanghai"}' }, parsedArguments: { city: 'Shanghai' } }],
    toolAssertions: [
      { type: 'tool-called', name: 'lookup' },
      { type: 'tool-arg-equals', name: 'lookup', path: 'city', value: 'Shanghai' },
      { type: 'tool-not-called', name: 'delete' },
      { type: 'tool-call-count', name: 'lookup', min: 1, max: 1 },
      { type: 'tool-arg-equals', name: 'lookup', path: 'city', value: 'Beijing' },
    ], judge: { model: evaluator.model, provider: evaluator },
  });
  assert.equal(evaluator.calls.length, 0);
  assert.deepEqual(result.grading.summary, { passed: 4, failed: 1, total: 5, pass_rate: 0.8 });
  return { ...result.grading.summary, judgeCalls: evaluator.calls.length };
});

await probe('E04', '裁判 JSON 无法解析时重试一次并判失败', async () => {
  const evaluator = provider('malformed-judge', () => 'not-json');
  const result = await gradeOutputs({ modelOutput: 'Correct output', assertions: ['Correct'], judge: { model: evaluator.model, provider: evaluator } });
  assert.equal(evaluator.calls.length, 2);
  assert.equal(result.grading.summary.failed, 1);
  return { attempts: evaluator.calls.length, ...result.grading.summary };
});

await probe('E05', '裁判给出 PASS 但没有证据，仍计为通过', async () => {
  const evaluator = provider('unsupported-pass', () => JSON.stringify({ assertion_results: [{ passed: true }] }));
  const result = await gradeOutputs({ modelOutput: 'Wrong output', assertions: ['Must be correct'], judge: { model: evaluator.model, provider: evaluator } });
  assert.equal(result.grading.summary.pass_rate, 1);
  assert.equal(result.grading.assertion_results[0].evidence, 'judge did not provide concrete evidence');
  return result.grading;
});

await probe('E06', '无评分条件时，目标调用出错仍可显示 100%', async () => {
  const skill = fixture('ungraded-error', [{ id: 'error', prompt: 'Do something' }]);
  const target = provider('error-target', () => ({ output: '', error: 'Controlled upstream failure' }));
  const evaluator = provider('unused-judge', () => 'not used');
  const result = await run(skill, target, evaluator, ['with_skill']);
  assert.match(result.modes.with_skill.rawOutput, /^ERROR:/);
  assert.deepEqual(result.modes.with_skill.grading.summary, { passed: 0, failed: 0, total: 0, pass_rate: 1 });
  assert.equal(evaluator.calls.length, 0);
  return { rawOutput: result.modes.with_skill.rawOutput, ...result.modes.with_skill.grading.summary };
});

await probe('E07', '裁判结果按数组位置匹配，未验证条件文本对应关系', async () => {
  const evaluator = provider('reordered-judge', () => JSON.stringify({ assertion_results: [
    { text: 'B', passed: true, evidence: 'Evidence for B' },
    { text: 'A', passed: false, evidence: 'Evidence for A' },
  ] }));
  const result = await gradeOutputs({ modelOutput: 'B only', assertions: ['A', 'B'], judge: { model: evaluator.model, provider: evaluator } });
  assert.equal(result.grading.assertion_results[0].text, 'A');
  assert.equal(result.grading.assertion_results[0].passed, true);
  assert.equal(result.grading.assertion_results[0].evidence, 'Evidence for B');
  return result.grading;
});

await probe('E08', '已有 assertions 时，预期答案及原任务不会自动传给裁判', async () => {
  const skill = fixture('judge-context', [{ id: 'context', prompt: 'TASK_CONTEXT_7be2',
    expected_output: 'EXPECTED_ANSWER_a91c', assertions: ['Check factual accuracy.'] }]);
  const evaluator = provider('capture-judge', () => JSON.stringify({ assertion_results: [{ passed: false, evidence: 'Unknown' }] }));
  const result = await run(skill, provider('static-target', () => 'ANSWER_f4d1'), evaluator, ['with_skill']);
  const prompt = result.modes.with_skill.judgePrompt;
  assert.ok(prompt.includes('ANSWER_f4d1'));
  assert.ok(!prompt.includes('TASK_CONTEXT_7be2'));
  assert.ok(!prompt.includes('EXPECTED_ANSWER_a91c'));
  return { seesModelOutput: true, seesOriginalTask: false, seesExpectedOutput: false };
});

await probe('E09', '没有 assertions 时 expected_output 会成为一条评分条件', async () => {
  const skill = fixture('expected-fallback', [{ id: 'fallback', prompt: 'Summarize.', expected_output: 'EXPECTED_ANSWER_a91c' }]);
  const evaluator = provider('capture-judge', () => JSON.stringify({ assertion_results: [{ passed: true, evidence: 'Synthetic response' }] }));
  const result = await run(skill, provider('static-target', () => 'EXPECTED_ANSWER_a91c'), evaluator, ['with_skill']);
  assert.match(result.modes.with_skill.grading.assertion_results[0].text, /EXPECTED_ANSWER_a91c/);
  return { totalAssertions: result.modes.with_skill.grading.summary.total };
});

await probe('E10', '内置 Provider 记录工具调用后结束，没有工具执行回合', async () => {
  const requests = [];
  const server = createServer(async (req, res) => {
    let body = '';
    for await (const chunk of req) body += chunk;
    requests.push(JSON.parse(body));
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ choices: [{ message: { content: null, tool_calls: [
      { id: 'call-1', type: 'function', function: { name: 'lookup', arguments: '{"city":"Shanghai"}' } },
    ] } }], usage: { prompt_tokens: 10, completion_tokens: 5 } }));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const target = new OpenAICompatibleProvider({ baseUrl: `http://127.0.0.1:${server.address().port}/v1`, apiKey: '', model: 'local-stub' });
    const skill = fixture('tool-loop', [{ id: 'tool', prompt: 'Look up Shanghai.',
      tools: [{ type: 'function', function: { name: 'lookup', parameters: { type: 'object' } } }],
      tool_assertions: [{ type: 'tool-called', name: 'lookup' }],
    }]);
    const result = await run(skill, target, provider('unused-judge', () => 'unused'), ['with_skill']);
    assert.equal(requests.length, 1);
    assert.equal(result.modes.with_skill.rawOutput, '');
    assert.equal(result.modes.with_skill.grading.summary.pass_rate, 1);
    return { httpRequests: requests.length, capturedToolCalls: result.modes.with_skill.toolCalls.length,
      finalText: '', passRate: 1, toolResultMessages: requests.flatMap(r => r.messages).filter(m => m.role === 'tool').length };
  } finally { await new Promise(resolve => server.close(resolve)); }
});

await probe('E11', '不同统计口径：用例平均 50%，检查条件整体通过率 10%', async () => {
  const benchmark = buildBenchmark([
    { mode: 'with_skill', passRate: 1, durationMs: 0, tokens: 0 },
    { mode: 'with_skill', passRate: 0, durationMs: 0, tokens: 0 },
  ]);
  const skill = fixture('aggregation', [
    { id: 'one', prompt: 'one', assertions: ['one pass'] },
    { id: 'nine', prompt: 'nine', assertions: Array.from({ length: 9 }, (_, i) => `failure ${i}`) },
  ]);
  const evaluator = provider('aggregation-judge', ({ user }) => {
    const rubric = JSON.parse(user.split('Assertions:\n')[1].split('\nModel output:')[0].trim());
    return JSON.stringify({ assertion_results: rubric.map(text => ({ text, passed: text === 'one pass', evidence: 'Controlled outcome' })) });
  });
  const result = await evaluateSkills({ root: skill.dir, workspace: path.join(runDir, 'aggregation-result'),
    target: { model: 'static', provider: provider('static', () => 'output') },
    judge: { model: evaluator.model, provider: evaluator }, report: false, onEvent() {},
  });
  const actual = JSON.parse(readFileSync(result.skills[0].benchmarkPath, 'utf8'));
  assert.equal(actual.run_summary.with_skill.pass_rate.mean, benchmark.run_summary.with_skill.pass_rate.mean);
  assert.equal(result.skills[0].passRate, 0.1);
  return { benchmarkMean: 0.5, overallAssertionPassRate: 0.1, passed: result.passed, failed: result.failed };
});

await probe('E12', 'CLI 没有发现任何 Skill 时仍返回成功退出码', async () => {
  const empty = path.join(runDir, 'empty-skills');
  mkdirSync(empty);
  const { stdout } = await execFileAsync(process.execPath, [
    path.join(root, 'upstream/dist/cli.js'), empty, '--workspace', path.join(runDir, 'empty-result'),
    '--base-url', 'http://127.0.0.1:1/v1', '--api-key-env', 'RESEARCH_DUMMY_KEY', '--no-report', '--log-format', 'silent',
  ], { env: { ...process.env, RESEARCH_DUMMY_KEY: 'local-test-only' }, timeout: 10000 });
  const result = JSON.parse(stdout);
  assert.equal(result.skills.length, 0);
  assert.equal(result.failed, 0);
  return { exitCode: 0, skills: 0, passed: result.passed, failed: result.failed };
});

const summary = {
  generatedAt: new Date().toISOString(), upstreamCommit: source.commit,
  node: process.version, platform: `${process.platform}/${process.arch}`,
  methodology: 'Deterministic synthetic providers and one loopback HTTP stub; no external model inference.',
  realModelQualityMeasured: false, total: observations.length,
  verified: observations.filter(o => o.verified).length, observations,
};
writeFileSync(path.join(artifacts, 'experiment-results.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(`${summary.verified}/${summary.total} mechanism observations verified. Synthetic scores are not model-quality measurements.`);
