import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const manifest = JSON.parse(readFileSync(path.join(root, 'upstream-source.json'), 'utf8').replace(/^\uFEFF/, ''));
for (const file of manifest.files) {
  const digest = createHash('sha256').update(readFileSync(path.join(root, 'upstream', file.path))).digest('hex');
  if (digest !== file.sha256) throw new Error(`Upstream file changed: ${file.path}`);
}
console.log(`Verified ${manifest.files.length} unchanged files at ${manifest.commit}`);
