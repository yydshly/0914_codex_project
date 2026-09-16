"""Verify deployed public files against a local build, without accessing Douyin."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from urllib.request import Request, urlopen
from build_site import FILES, OUT, ROOT

BASE = 'https://yydshly.github.io/0914_codex_project/'
SLUG = '008-douyin-downloader/'
TEXT_SUFFIXES = {'.html', '.css', '.js', '.svg', '.md', '.txt'}

def fetch(url):
    request = Request(url, headers={'User-Agent': 'Research-deployment-verifier', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=45) as response:
        return response.status, response.read()

def verify(name, version):
    target = OUT / name
    expected = target.read_bytes()
    status, actual = fetch(BASE + SLUG + name + '?verify=' + version)
    if target.suffix in TEXT_SUFFIXES:
        actual = actual.replace(b'\r\n', b'\n')
        expected = expected.replace(b'\r\n', b'\n')
    if status != 200 or actual != expected:
        raise AssertionError(f'Deployed file differs: {name} (HTTP {status})')
    return {'path': name, 'status': status, 'sha256': hashlib.sha256(actual).hexdigest()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        files = list(pool.map(lambda name: verify(name, args.version), FILES))
    repo = ROOT.parents[1]
    projects = json.loads((repo / 'projects.json').read_text(encoding='utf-8'))['projects']
    selected = set(json.loads((repo / 'pages.json').read_text(encoding='utf-8'))['projects'])
    entries = [''] + [f"{p['id']}-{p['slug']}/" for p in projects if p['id'] in selected]
    statuses = []
    for path in entries:
        status, body = fetch(BASE + path + '?verify=' + args.version)
        if status != 200:
            raise AssertionError(f'Entry failed: {path}')
        if not path and SLUG.encode() not in body:
            raise AssertionError('Research index does not link the new page')
        statuses.append({'path': path or '/', 'status': status})
    report = {'version': args.version, 'url': BASE + SLUG, 'files': files, 'entries': statuses}
    output = ROOT / '.cache' / 'deployment-verification.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Verified {len(files)} deployed files by content and {len(entries)} entrypoints. Report: {output}')

if __name__ == '__main__':
    main()
