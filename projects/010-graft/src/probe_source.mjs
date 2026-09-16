// Isolated probes of exact upstream functions, not an end-to-end Graft run.
import { readFileSync, writeFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { runInNewContext } from 'node:vm';
import { resolve } from 'node:path';
const root = resolve('.cache/graft-source-f9e6539/src');
const index = readFileSync(resolve(root, 'ask/index-file.ts'), 'utf8');
const tokenizeSource = index.slice(index.indexOf('const STOP ='), index.indexOf('/** Term-frequency count map. */')).replace('export function', 'function');
const tokenize = runInNewContext(stripTypeScriptTypes(tokenizeSource) + '\ntokenize');
const queries = ['登录凭证在哪里生成', 'token 为什么很快过期', 'token expiry', 'issueToken'];
const result = {
  commit: 'f9e65396e638e517aecae0d731017f53084d70ed',
  scope: 'Exact tokenizer and inlineSource functions; fixture dependencies, no full Graft build or model calls.',
  tokenizer: queries.map(query => ({ query, tokens: Array.from(tokenize(query)) })),
};
const ask = readFileSync(resolve(root, 'ask/ask.ts'), 'utf8');
const parseSpan = ask.slice(ask.indexOf('function parseSpan('), ask.indexOf('/** Read the source lines'));
const inlineSource = ask.slice(ask.indexOf('function inlineSource('), ask.indexOf('/** Every repo-relative file path'));
const inline = runInNewContext(stripTypeScriptTypes(parseSpan + inlineSource) + '\ninlineSource', {
  // Stub only the disk reader so the original selection branch is isolated.
  sliceSpan: () => 'FRESH_SOURCE_FIXTURE',
});
const node = {path:'example.ts',span:'L1-L3',summary_state:'stale',crux:{code:'OLD_CRUX_FIXTURE'}};
result.staleCrux = [false, true].map(full => {
  const hits = [{pointer:'example.ts:L1-L3'}];
  inline('.', hits, {nodes:[node]}, full);
  return {full, output:hits[0].code};
});
const report = JSON.stringify(result, null, 2) + '\n';
writeFileSync('projects/010-graft/notes/source-probes.json', report);
console.log(report);
