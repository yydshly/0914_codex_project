"""Package the research page; check local resources, anchors and labels."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/dist'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.labels = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        self.refs.extend(attrs[k] for k in ('href', 'src') if k in attrs)
        for key in ('aria-controls', 'aria-labelledby', 'for'):
            self.labels.extend(attrs.get(key, '').split())

def main():
    files = {p.name:p for p in (ROOT/'web').iterdir()
             if p.is_file() and p.suffix in {'.html','.css','.js','.svg'}}
    files.update({'notes/'+p.name:p for p in (ROOT/'notes').iterdir()
                  if p.suffix in {'.md','.json'}})
    files.update({'assets/'+p.name:p for p in (ROOT/'assets').iterdir()
                  if p.is_file() and p.suffix in {'.png','.svg'}})
    files['src/scenarios.json'] = ROOT/'src/scenarios.json'
    files['README.md'] = ROOT/'README.md'
    for name, source in files.items():
        if source.is_symlink():
            raise ValueError(f'Symlink rejected: {source}')
        dest = OUT/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if actual != set(files):
        raise ValueError('Unexpected output files')
    page = References()
    page.feed((OUT/'index.html').read_text(encoding='utf-8'))
    if len(page.ids) != len(set(page.ids)):
        raise ValueError('Duplicate IDs')
    for label in page.labels:
        if label not in page.ids:
            raise ValueError(f'Invalid label/control: {label}')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            if url.fragment and url.fragment not in page.ids:
                raise ValueError(f'Invalid anchor: {ref}')
        else:
            target = (OUT/unquote(url.path)).resolve()
            if not target.is_relative_to(OUT.resolve()) or not target.is_file():
                raise ValueError(f'Invalid local reference: {ref}')
    print(f'Built {len(files)} files; local assets, anchors and controls checked.')

if __name__ == '__main__':
    main()
