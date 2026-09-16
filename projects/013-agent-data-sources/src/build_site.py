"""Package the research page using the checked-in inventory, without network access."""
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/dist'


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.labels = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        self.refs.extend(attrs[k] for k in ('src', 'href') if k in attrs)
        self.labels.extend(attrs[k] for k in ('for', 'aria-labelledby') if k in attrs)


def main():
    inventory = json.loads((ROOT/'notes/source-inventory.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT/'notes/source-manifest.json').read_text(encoding='utf-8'))
    assert len({r['id'] for r in inventory}) == len(inventory)
    refs = {r['id'] for r in evidence}
    for row in inventory:
        assert not row['tested']
        for coverage in row['coverage'].values():
            assert set(coverage['evidence']) <= refs
            assert len(coverage['evidence']) == len(coverage['evidence_urls'])
            assert 'access' in coverage and coverage['access']['upstream']
            for method in coverage['access']['methods']:
                assert set(method['evidence']) <= refs
                assert len(method['evidence']) == len(method['evidence_urls'])
        for method in row['direct_access']:
            assert set(method['evidence']) <= refs
    files = {name: ROOT/'web'/name for name in ('index.html', 'style.css', 'main.js')}
    files.update({'notes/'+p.name:p for p in (ROOT/'notes').iterdir() if p.suffix in ('.json', '.md')})
    files['README.md'] = ROOT/'README.md'
    files['assets/agent-data-sources-guide.png'] = ROOT/'assets/agent-data-sources-guide.png'
    for name, source in files.items():
        if source.is_symlink(): raise ValueError(f'Unexpected symlink: {source}')
        target=OUT/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    public_evidence=[{k:r[k] for k in ('id','title','url')} for r in evidence]
    payload=json.dumps({'inventory':inventory,'evidence':public_evidence},ensure_ascii=False)
    (OUT/'data.js').write_text('window.RESEARCH_DATA = '+payload.replace('</','<\\/')+';\n',encoding='utf-8')
    parser=References();parser.feed((OUT/'index.html').read_text(encoding='utf-8'))
    assert len(parser.ids)==len(set(parser.ids)), 'Duplicate HTML IDs'
    for label in parser.labels:
        assert label in parser.ids or label=='detail-title', f'Missing label: {label}'
    for ref in parser.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        if not url.path:
            assert not url.fragment or url.fragment in parser.ids, f'Missing anchor: {ref}'
        else:
            target=(OUT/unquote(url.path)).resolve()
            assert target.is_relative_to(OUT.resolve()) and target.is_file(), f'Missing asset: {ref}'
    print(f'Built {len(files)+1} files; {len(inventory)} entries, {len(evidence)} evidence pages; references verified.')


if __name__=='__main__': main()
