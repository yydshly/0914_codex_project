"""Package only the EvoMap understanding page and public experiment summaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web' / 'dist'
FILES = {
    'index.html': ROOT / 'web' / 'index.html',
    'style.css': ROOT / 'web' / 'style.css',
    'main.js': ROOT / 'web' / 'main.js',
    'assets/product-understanding.png': ROOT / 'assets' / 'product-understanding.png',
    'assets/product-understanding.svg': ROOT / 'assets' / 'product-understanding.svg',
    'evidence/test-summary.json': ROOT / 'notes' / 'test-summary.json',
    'evidence/probe-output.txt': ROOT / 'notes' / 'probe-output.txt',
}

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])

def main():
    for name, source in FILES.items():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Invalid source: {source}')
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if actual != set(FILES) or any(p.is_symlink() for p in OUT.rglob('*')):
        raise ValueError('Unexpected files in public output')
    page = References()
    page.feed((OUT / 'index.html').read_text(encoding='utf-8'))
    if len(page.ids) != len(set(page.ids)):
        raise ValueError('Duplicate page IDs')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            if url.fragment and url.fragment not in page.ids:
                raise ValueError(f'Missing section: {ref}')
        elif not (OUT / url.path).resolve().is_relative_to(OUT.resolve()) or not (OUT / url.path).is_file():
            raise ValueError(f'Invalid local reference: {ref}')
    print(f'Built {len(FILES)} public files; local references and section links OK.')

if __name__ == '__main__':
    main()
