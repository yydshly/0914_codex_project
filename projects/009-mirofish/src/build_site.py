"""Build the independent MiroFish teaching exhibit; publish only explicit files."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web' / 'dist'
FILES = {name: ROOT / 'web' / name for name in
         ('index.html', 'style.css', 'scenarios.js', 'main.js', 'real-case.js', 'favicon.svg')}
FILES.update({f'assets/{name}': ROOT / 'assets' / name for name in
              ('upstream-screen-3.png', 'upstream-screen-6.png', 'mirofish-workflow.png', 'mirofish-workflow.svg',
               'mirofish-capabilities.png', 'mirofish-capabilities.svg')})
FILES.update({f'evidence/{name}': ROOT / 'notes' / name for name in
              ('UPSTREAM-LICENSE.txt', 'sources.json', 'real-run.md', 'unity-seed.md', 'unity-experiment.md')})


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        self.refs.extend(attrs[key] for key in ('href', 'src') if key in attrs)


def main():
    if OUT.is_symlink():
        raise ValueError('Output directory cannot be a symlink')
    if OUT.exists() and any(p.is_symlink() for p in OUT.rglob('*')):
        raise ValueError('Unexpected symlink in output')
    for name, source in FILES.items():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Invalid source: {source}')
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if actual != set(FILES):
        raise ValueError(f'Unexpected public files: {actual - set(FILES)}')
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
                raise ValueError(f'Missing section: {ref}')
        else:
            target = (OUT / unquote(url.path)).resolve()
            if not target.is_relative_to(OUT.resolve()) or not target.is_file():
                raise ValueError(f'Invalid local reference: {ref}')
    print(f'Built {len(FILES)} public files; references, anchors and output allowlist OK.')


if __name__ == '__main__':
    main()
