"""Verify provenance, static files, JS syntax, experiments and actual rendered media."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web/dist'
checks=[]

def check(label,condition,detail=''):
    if not condition: raise AssertionError(label+': '+str(detail))
    checks.append({'check':label,'passed':True,'detail':detail})

inventory=json.loads((ROOT/'notes/inventory.json').read_text(encoding='utf-8'))
paths=set(inventory['source_paths'])
cards=inventory['cards']
check('108 catalog entries',len(cards)==108 and len({c['slug'] for c in cards})==108)
for c in cards:
    for path in [f"references/cards/{c['slug']}.md",f"template/cards/{c['slug']}.tsx",f"demos/{c['slug']}/index.html"]:
        assert path in paths,path
check('108 complete recipe/code/demo mappings',True)
checked=0
for entry in inventory['snapshot']:
    if entry['path'].startswith('gallery/'): continue # original 2 MB gallery is cache-only
    p=ROOT/'upstream'/entry['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],str(p)
    checked+=1
manifest=json.loads((ROOT/'notes/demo-manifest.json').read_text())
for entry in manifest['files']:
    p=WEB/'vendor'/entry['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],str(p)
check('Upstream and demo files unchanged',True,f'{checked+len(manifest["files"])} hashes')
for name in ['LICENSE','THIRD_PARTY_NOTICES.md']:
    check('License copy '+name,(ROOT/'upstream'/name).read_bytes()==(WEB/'vendor'/name).read_bytes())

class Assets(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.scripts=[];self.current=None;self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        for k in ['src','href','poster']:
            if a.get(k): self.refs.append(a[k])
        if tag=='script' and not a.get('src'): self.current=[]
    def handle_data(self,data):
        if self.current is not None:self.current.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.current is not None:
            self.scripts.append(''.join(self.current));self.current=None

htmls=list(WEB.rglob('*.html'));inline_count=0
for path in htmls:
    parser=Assets();parser.feed(path.read_text(encoding='utf-8'))
    assert len(parser.ids)==len(set(parser.ids)),f'duplicate ID {path}'
    for ref in parser.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc or not url.path: continue
        target=(path.parent/unquote(url.path)).resolve()
        assert target.is_relative_to(WEB.resolve()) and target.exists(),f'{path}: missing {ref}'
    for script in parser.scripts:
        if not script.strip(): continue
        with tempfile.TemporaryDirectory() as folder:
            js=Path(folder)/'inline.js';js.write_text(script,encoding='utf-8')
            cp=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
            assert cp.returncode==0,cp.stderr
        inline_count+=1
for path in [WEB/'app.js',*list((WEB/'vendor/demos/_lib').glob('*.js'))]:
    cp=subprocess.run(['node','--check',str(path)],capture_output=True,text=True)
    assert cp.returncode==0,cp.stderr
check('HTML entrypoints, resources and JavaScript syntax',True,f'{len(htmls)} pages; {inline_count} inline scripts')
app=(WEB/'app.js').read_text(encoding='utf-8')
parser=Assets();parser.feed((WEB/'index.html').read_text(encoding='utf-8'))
for id_ in re.findall(r"\$\('([^']+)'\)",app):
    if id_.endswith('-'):continue
    assert id_ in parser.ids,id_
check('App DOM bindings exist',True)
report=json.loads((WEB/'experiments.json').read_text(encoding='utf-8'))
check('Controlled experiments',len(report['results'])==10 and all(x['passed'] for x in report['results']),'10/10 expected outcomes, synthetic ASR words')
video=WEB/'assets/number-counter.mp4'
check('Rendered MP4 exists',video.is_file())
cp=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=codec_name,width,height,avg_frame_rate,nb_read_frames,duration','-of','json',str(video)],capture_output=True,text=True,check=True)
stream=json.loads(cp.stdout)['streams'][0]
check('Actual MP4 dimensions and frame count',stream['width']==960 and stream['height']==540 and int(stream['nb_read_frames'])==86 and stream['avg_frame_rate']=='30/1',stream)
render={'status':'passed','component':'number-counter','commit':inventory['commit'],'width':stream['width'],'height':stream['height'],'frames':int(stream['nb_read_frames']),'fps':30,'duration':round(float(stream['duration']),3),'codec':stream['codec_name'],'audio':False,'note':'Original component, placeholder host, no narration. Not end-to-end production.'}
(WEB/'render-result.json').write_text(json.dumps(render,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'notes/verification.json').write_text(json.dumps({'date':'2026-09-15','browser_ui_tested':False,'checks':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks_passed':len(checks),'catalog':len(cards),'media':render,'browser_ui_tested':False},ensure_ascii=False,indent=2))
