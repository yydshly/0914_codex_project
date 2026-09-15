"""Download fixed upstream source assets for the interactive gallery (no remote demo media)."""
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMMIT='cb3c905e4bc362e02e040035b5c88b13fdd54cf4'
tree=json.loads((ROOT/'.cache/skills-tree.json').read_text(encoding='utf-8'))['tree']
records=[]
for entry in tree:
    p=entry['path']
    if entry['type']!='blob': continue
    if not (p in ['light-spotlight-render/assets/light_spotlight_template.html','light-spotlight-render/scripts/render_light_spotlight.py','remotion-3d-ticker/assets/VerticalTicker.tsx','printed-curtain-render/scripts/create_printed_curtain.py'] or p.startswith('printed-curtain-render/assets/printed-curtain-template/')): continue
    target=ROOT/'upstream/skills'/p
    target.parent.mkdir(parents=True,exist_ok=True)
    url=f'https://raw.githubusercontent.com/vibe-motion/skills/{COMMIT}/{p}'
    subprocess.run(['curl.exe','-fLsS','--retry','3','--connect-timeout','15','--max-time','60',url,'-o',str(target)],check=True)
    records.append({'path':p,'local':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'url':f'https://github.com/vibe-motion/skills/blob/{COMMIT}/{p}'})
    print(p,flush=True)
(ROOT/'notes/web-source-manifest.json').write_text(json.dumps({'commit':COMMIT,'files':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
