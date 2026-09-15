"""Collect a small, commit-pinned research snapshot; never execute agent instructions."""
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS = ['create-vibe-motion', 'create-vibe-motion-3d', 'auto-motion', 'skills']

def fetch(url):
    return subprocess.check_output(['curl.exe', '-fLsS', '--retry', '3', '--connect-timeout', '15', '--max-time', '60', '-H', 'User-Agent: vibe-motion-research', url])

def main():
    previous = ROOT / 'notes' / 'inventory.json'
    pins = {r['name']: r['commit'] for r in json.loads(previous.read_text(encoding='utf-8'))['repositories']} if previous.exists() else {}
    manifest = {'date': '2026-09-16', 'repositories': [], 'files': []}
    for repo in REPOS:
        local = ROOT / '.cache' / repo
        if repo.startswith('create-') and (local / '.git').exists():
            commit = pins.get(repo) or subprocess.check_output(['git', '-C', str(local), 'rev-parse', 'HEAD'], text=True).strip()
            paths = subprocess.check_output(['git', '-C', str(local), 'ls-tree', '-r', '--name-only', commit], text=True).splitlines()
            read = lambda p: subprocess.check_output(['git', '-C', str(local), 'show', f'{commit}:{p}'])
        else:
            commit = pins.get(repo)
            if not commit:
                info = json.loads(fetch(f'https://api.github.com/repos/vibe-motion/{repo}/commits/main'))
                commit = info['sha']
            tree = json.loads(fetch(f'https://api.github.com/repos/vibe-motion/{repo}/git/trees/{commit}?recursive=1'))
            if tree.get('truncated'):
                raise RuntimeError('Incomplete tree')
            paths = [x['path'] for x in tree['tree'] if x['type'] == 'blob']
            read = lambda p: fetch(f'https://raw.githubusercontent.com/vibe-motion/{repo}/{commit}/{p}')
        licenses = [p for p in paths if Path(p).name.lower().startswith(('license', 'copying', 'notice'))]
        selected = [p for p in paths if p in licenses or p in ['README.md', 'package.json', 'PROMPT.md', 'AGENTS.md']
                    or (repo.startswith('create-') and (p == f'packages/{repo}/package.json' or p.startswith(f'packages/{repo}/bin/') or p == 'scripts/sync-template-to-cli.mjs'))
                    or (repo.startswith('create-') and p.startswith('packages/template/') and Path(p).suffix in ['.js', '.jsx', '.mjs', '.json', '.html', '.md'])
                    or (repo == 'auto-motion' and (p in ['exampleFolder/run-claude-ai.sh', 'auto-test/validate.sh', 'auto-test/run.sh', 'auto-test/transcription.srt']))
                    or (repo == 'skills' and p.endswith('/SKILL.md'))]
        entry = {'name': repo, 'url': f'https://github.com/vibe-motion/{repo}', 'commit': commit, 'license_files': licenses,
                 'skill_entries': [p for p in paths if p.endswith('/SKILL.md')], 'selected_file_count': len(selected)}
        manifest['repositories'].append(entry)
        for p in selected:
            data = read(p)
            target = ROOT / 'upstream' / repo / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            manifest['files'].append({'repo': repo, 'path': p, 'local': target.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(data).hexdigest(),
                                      'url': f'https://github.com/vibe-motion/{repo}/blob/{commit}/{p}'})
        print(repo, commit, len(selected), flush=True)
        (ROOT / 'notes' / 'inventory.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'notes' / 'inventory.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
