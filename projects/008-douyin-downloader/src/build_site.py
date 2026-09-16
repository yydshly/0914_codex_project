"""Build the offline research guide and validate public references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web' / 'dist'
FILES = {n: ROOT / 'web' / n for n in ('index.html', 'style.css', 'main.js', 'favicon.svg')}
FILES['assets/douyin-overview.png'] = ROOT / 'assets' / 'douyin-overview.png'
FILES['assets/douyin-overview.svg'] = ROOT / 'assets' / 'douyin-overview.svg'
for name in ('understanding.md', 'capabilities.md', 'sources.md', 'verification.md', 'UPSTREAM-LICENSE.txt', 'image-production.md'):
    FILES['notes/' + name] = ROOT / 'notes' / name

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], []
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
            raise ValueError(f'Missing or invalid source: {source}')
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if actual != set(FILES) or any(p.is_symlink() for p in OUT.rglob('*')):
        raise ValueError('Unexpected public output files')
    page = References()
    page.feed((OUT / 'index.html').read_text(encoding='utf-8'))
    if len(page.ids) != len(set(page.ids)):
        raise ValueError('Duplicate HTML IDs')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            if url.fragment and url.fragment not in page.ids:
                raise ValueError(f'Invalid section: {ref}')
        else:
            target = (OUT / unquote(url.path)).resolve()
            if not target.is_relative_to(OUT.resolve()) or not target.is_file():
                raise ValueError(f'Invalid local asset: {ref}')
    print(f'Built {len(FILES)} files; assets, whitelist and anchors verified.')

if __name__ == '__main__':
    main()
