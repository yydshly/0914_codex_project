"""Collect a pinned, attributed source snapshot for this research (stdlib only)."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Vincentwei1021/video-talkcraft'
COMMIT = '8829ca31fb8aeb1b850e85e47a7d7584c349bc4a'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'TalkCraft-Research/1.0'})
    with urllib.request.urlopen(req, timeout=60) as res:
        return res.read()

def collect():
    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    tree_path = cache / 'tree.json'
    if not tree_path.exists():
        tree_path.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{COMMIT}?recursive=1'))
    tree = json.loads(tree_path.read_text())['tree']
    paths = {x['path'] for x in tree if x['type'] == 'blob'}
    selected = ['number-counter', 'highlighter-sweep', 'evidence-scroll-tour',
                'host-shrink-to-chip', 'split-compare-slider', 'shape-wipe-transition']
    wanted = ['LICENSE', 'THIRD_PARTY_NOTICES.md', 'README.md', 'SKILL.md',
              'scripts/timestamps_cpu.py', 'scripts/make_timing.py', 'scripts/voice_trim.py',
              'scripts/render_shots.mjs', 'scripts/beat_lint.py', 'scripts/motion_check.py',
              'scripts/sfx_check.py', 'scripts/card_lint.py', 'scripts/preflight.py',
              'template/motion-systems/camera.tsx', 'template/motion-systems/life.tsx',
              'references/host-footage.md', 'references/taxonomy.md', 'references/review-protocol.md',
              'workbench/README.md']
    wanted += [f'template/cards/{s}.tsx' for s in selected]
    wanted += [f'references/cards/{s}.md' for s in selected]
    wanted += ['gallery/index.html']
    def download(path):
        target = ROOT / ('.cache' if path.startswith('gallery/') else 'upstream') / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(fetch(f'https://raw.githubusercontent.com/{REPO}/{COMMIT}/{path}'))
        return {'path': path, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        manifest = list(pool.map(download, wanted))
    html = (cache / 'gallery/index.html').read_text(encoding='utf-8')
    match = re.search(r'const CARDS\s*=\s*', html)
    cards, _ = json.JSONDecoder().raw_decode(html[match.end():])
    (cache / 'gallery-cards.json').write_text(json.dumps(cards, ensure_ascii=False), encoding='utf-8')
    catalog = [{k: c.get(k) for k in ['slug', 'zhName', 'category', 'title', 'usage', 'energy']} for c in cards]
    out = ROOT / 'web/dist'
    out.mkdir(parents=True, exist_ok=True)
    counts = {name: len([p for p in paths if re.fullmatch(pattern, p)]) for name, pattern in {
        'recipes': r'references/cards/[^/]+\.md', 'components': r'template/cards/[^/]+\.tsx',
        'demos': r'demos/[^/]+/index\.html'}.items()}
    inventory = {'commit': COMMIT, 'repo': f'https://github.com/{REPO}', 'date': '2026-09-15',
                 'counts': counts, 'cards': catalog, 'snapshot': manifest,
                 'source_paths': sorted(p for p in paths if re.fullmatch(r'(references/cards/[^/]+\.md|template/cards/[^/]+\.tsx|demos/[^/]+/index\.html)', p))}
    (ROOT / 'notes/inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (out / 'catalog.json').write_text(json.dumps({k: inventory[k] for k in ['commit','repo','date','counts','cards']}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'commit': COMMIT, 'counts': counts, 'gallery_count': len(cards), 'sample_keys': list(cards[0]), 'selected': selected}, ensure_ascii=False))

if __name__ == '__main__':
    collect()
