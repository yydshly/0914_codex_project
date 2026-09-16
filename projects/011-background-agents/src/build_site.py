"""Package the static Background Agents study page and validate local references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/dist'
FILES = {name: ROOT/'web'/name for name in ('index.html','style.css','main.js','favicon.svg')}
for name in ('understanding.md','capabilities.md','architecture.md','deployment.md','sources.md','evidence.json'):
    FILES['notes/'+name] = ROOT/'notes'/name
for name in ('background-agents-overview.png','background-agents-overview.svg','background-agents-overview-preview.png'):
    FILES['assets/'+name] = ROOT/'assets'/name

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.labels = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('href','src'):
            if key in attrs: self.refs.append(attrs[key])
        for key in ('aria-controls','aria-labelledby','for'):
            if key in attrs: self.labels.extend(attrs[key].split())

def main():
    for name,source in FILES.items():
        if source.is_symlink() or not source.is_file(): raise ValueError(f'Missing or invalid source: {source}')
        target=OUT/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    actual={p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if actual != set(FILES) or any(p.is_symlink() for p in OUT.rglob('*')): raise ValueError('Unexpected output files')
    page=References()
    page.feed((OUT/'index.html').read_text(encoding='utf-8'))
    if len(page.ids)!=len(set(page.ids)): raise ValueError('Duplicate HTML IDs')
    for label in page.labels:
        if label not in page.ids: raise ValueError(f'Invalid control reference: {label}')
    for ref in page.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        if not url.path:
            if url.fragment and url.fragment not in page.ids: raise ValueError(f'Invalid anchor: {ref}')
        else:
            target=(OUT/unquote(url.path)).resolve()
            if not target.is_relative_to(OUT.resolve()) or not target.is_file(): raise ValueError(f'Invalid asset: {ref}')
    print(f'Built {len(FILES)} files; local assets, anchors and control references verified.')

if __name__=='__main__': main()
