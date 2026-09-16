"""Build only the public Dashy study page; never publish runtime or local APIs."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web' / 'dist'
PUBLIC_ASSETS = (
    'dashy-capability-overview.png',
    'dashy-capability-overview.svg',
    'cover.png',
    'edit-item.png',
    'workspace.png',
)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'assets').mkdir(exist_ok=True)
    for name in ('index.html', 'style.css', 'main.js'):
        shutil.copy2(ROOT / 'web' / name, OUT / name)
    for name in PUBLIC_ASSETS:
        shutil.copy2(ROOT / 'assets' / name, OUT / 'assets' / name)
    shutil.copy2(ROOT / 'user-data' / 'conf.yml', OUT / 'config-example.yml')
    expected = {'index.html', 'style.css', 'main.js', 'config-example.yml'} | {'assets/' + n for n in PUBLIC_ASSETS}
    actual = {str(p.relative_to(OUT)).replace('\\', '/') for p in OUT.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'Unexpected public output; inspect before publishing: {actual ^ expected}')
    if any(p.is_symlink() for p in OUT.rglob('*')):
        raise ValueError('Public output must not contain symlinks')
    print(json.dumps({'files': len(actual), 'bytes': sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()), 'output': str(OUT)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
