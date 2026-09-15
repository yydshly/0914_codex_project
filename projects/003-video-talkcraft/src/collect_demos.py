"""Vendor six untouched upstream HTML demos and their shared assets."""
from collect_upstream import ROOT, REPO, COMMIT, fetch
import concurrent.futures
import hashlib
import json
import shutil

selected = ['number-counter','highlighter-sweep','evidence-scroll-tour',
            'host-shrink-to-chip','split-compare-slider','shape-wipe-transition']
tree = json.loads((ROOT/'.cache/tree.json').read_text())['tree']
paths = [x['path'] for x in tree if x['type']=='blob' and x['path'].startswith('demos/_lib/')]
paths += [f'demos/{slug}/index.html' for slug in selected]
target_root = ROOT/'web/dist/vendor'

def download(path):
    target=target_root/path
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(fetch(f'https://raw.githubusercontent.com/{REPO}/{COMMIT}/{path}'))
    return {'path':path,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    manifest=list(pool.map(download,paths))
for name in ['LICENSE','THIRD_PARTY_NOTICES.md']:
    shutil.copyfile(ROOT/'upstream'/name, target_root/name)
(ROOT/'notes/demo-manifest.json').write_text(json.dumps({'commit':COMMIT,'files':manifest},indent=2)+'\n',encoding='utf-8')
print(f'Collected {len(manifest)} files, {sum(x["bytes"] for x in manifest):,} bytes. Original files unchanged.')
