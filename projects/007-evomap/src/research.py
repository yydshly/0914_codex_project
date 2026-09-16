"""Reproduce bounded offline checks; use --bootstrap to fetch pinned upstream first."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache'
UPSTREAM = CACHE / 'upstream'
COMMIT = '31b0691acd97ba18878019312e646f1f2d970d43'
REPO = 'https://github.com/EvoMap/evolver.git'


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()
    CACHE.mkdir(exist_ok=True)
    if args.bootstrap:
        if not (UPSTREAM / '.git').exists():
            subprocess.run(['git', 'clone', '--no-checkout', REPO, str(UPSTREAM)], check=True)
        subprocess.run(['git', '-C', str(UPSTREAM), 'fetch', '--depth', '1', 'origin', COMMIT], check=True)
        subprocess.run(['git', '-C', str(UPSTREAM), 'checkout', '--detach', COMMIT], check=True)
        subprocess.run([shutil.which('npm.cmd') or shutil.which('npm'), 'ci', '--ignore-scripts', '--omit=dev', '--no-audit', '--no-fund'], cwd=UPSTREAM, check=True)
    if not UPSTREAM.exists():
        raise SystemExit('Run python src/research.py --bootstrap first.')
    head = run(['git', 'rev-parse', 'HEAD'], cwd=UPSTREAM, check=True).stdout.strip()
    if head != COMMIT:
        raise SystemExit(f'Unexpected commit: {head}')
    notes = ROOT / 'notes'
    notes.mkdir(exist_ok=True)
    (notes / 'UPSTREAM-LICENSE.txt').write_bytes((UPSTREAM / 'LICENSE').read_bytes())
    package = json.loads((UPSTREAM / 'package.json').read_text(encoding='utf-8'))
    print('Auditing tracked source files...', flush=True)
    tracked = run(['git', 'ls-files', 'src'], cwd=UPSTREAM, check=True).stdout.splitlines()
    js_files = [UPSTREAM / name for name in tracked if name.endswith('.js')]
    obfuscated = [p.relative_to(UPSTREAM).as_posix() for p in js_files if re.search(r'\b_0x[0-9a-f]+\b', p.read_text(encoding='utf-8'))]
    evidence = {
        'upstream': REPO, 'commit': COMMIT, 'version': package['version'],
        'declared_license': package['license'], 'node_engine': package['engines']['node'],
        'package_lock_sha256': hashlib.sha256((UPSTREAM / 'package-lock.json').read_bytes()).hexdigest(),
        'src_js_files': len(js_files), 'files_with_obfuscation_marker': len(obfuscated),
        'obfuscation_heuristic': 'Identifier matching _0x[0-9a-f]+; a heuristic, not decompilation.',
        'obfuscated_paths': obfuscated,
        'sdk_version': json.loads((UPSTREAM / 'node_modules/@evomap/gep-sdk/package.json').read_text())['version'],
    }
    (notes / 'source-audit.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    # Do not pass through API keys, GitHub tokens, or user runtime configuration.
    allowed = {'PATH', 'PATHEXT', 'SYSTEMROOT', 'WINDIR', 'COMSPEC'}
    env = {k: v for k, v in os.environ.items() if k.upper() in allowed}
    home = CACHE / 'test-home'
    home.mkdir(exist_ok=True)
    env.update({
        'HOME': str(home), 'USERPROFILE': str(home), 'APPDATA': str(home), 'LOCALAPPDATA': str(home),
        'TEMP': str(home), 'TMP': str(home), 'EVOLVER_REPO_ROOT': str(UPSTREAM),
        'WORKSPACE_DIR': str(UPSTREAM), 'MEMORY_DIR': str(home / 'memory'),
        'EVOLUTION_DIR': str(home / 'evolution'), 'GEP_ASSETS_DIR': str(home / 'gep'),
        'A2A_HUB_URL': '', 'EVOLVER_AUTO_ISSUE': 'false', 'EVOLVER_VALIDATOR_ENABLED': 'false',
        'EVOLVER_ATP_AUTOBUY': 'false', 'WORKER_ENABLED': '0', 'EVOLVE_BRIDGE': '0',
        'EVOLVER_DEVICE_ID': 'research-synthetic-device',
    })
    node = shutil.which('node')
    common = [node, '--permission', f'--allow-fs-read={ROOT}', f'--allow-fs-write={CACHE}',
              '--require', str(ROOT / 'src/offline-guard.cjs')]
    # One process per suite keeps upstream environment/cache state independent.
    summaries = []
    for test in ['contentHash', 'selector', 'prompt']:
        print(f'Running {test}...', flush=True)
        command = common + ['--test', '--experimental-test-isolation=none', '--test-reporter=tap', f'test/{test}.test.js']
        proc = run(command, cwd=UPSTREAM, env=env, timeout=60)
        output = proc.stdout + proc.stderr
        (notes / f'test-{test}.txt').write_text(output, encoding='utf-8')
        summaries.append({'suite': test, 'exit_code': proc.returncode,
                          'summary': re.findall(r'^# (?:tests|pass|fail|skipped) .+$', output, re.M)})
    proc = run(common + [str(ROOT / 'src/probe.cjs')], cwd=UPSTREAM, env=env, timeout=30)
    (notes / 'probe-output.txt').write_text(proc.stdout + proc.stderr, encoding='utf-8')
    summaries.append({'suite': 'research-probe', 'exit_code': proc.returncode})
    (notes / 'test-summary.json').write_text(json.dumps({'node': run([node, '--version']).stdout.strip(), 'runs': summaries}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summaries, indent=2))
    print(proc.stdout[-3000:])
    if any(s['exit_code'] for s in summaries):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
