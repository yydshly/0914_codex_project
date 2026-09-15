"""Static gallery integrity and video metadata checks; browser QA is recorded separately."""
import hashlib
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'web/dist'
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,val in attrs:
            if key in ['src','href','data-src'] and val: self.links.append(val)
def main():
    for entry in json.loads((ROOT/'notes/gallery-files.json').read_text(encoding='utf-8')):
        assert hashlib.sha256((OUT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    for entry in json.loads((ROOT/'notes/web-source-manifest.json').read_text(encoding='utf-8'))['files']:
        assert hashlib.sha256((ROOT/entry['local']).read_bytes()).hexdigest()==entry['sha256'],entry['local']
    for html in OUT.rglob('*.html'):
        parser=Links();parser.feed(html.read_text(encoding='utf-8'))
        for link in parser.links:
            parts=urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path: continue
            assert (html.parent/unquote(parts.path)).is_file(),(html,link)
    for p in ['index.js','src/sceneControls.js']:
        assert (OUT/'demos/three'/p).read_bytes()==(ROOT/'src/demo-3d'/p).read_bytes()
    subprocess.run(['node','--check',str(OUT/'app.js')],check=True)
    video=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(OUT/'media/demo-2d.mp4')],text=True))
    assert len(video['streams'])==1
    v=video['streams'][0]
    assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames']))==(1080,810,'30/1',150)
    storyboard=json.loads((OUT/'data/storyboard.json').read_text(encoding='utf-8'))
    assert storyboard['model_called'] is False
    assert [(s['start'],s['end']) for s in storyboard['scenes']]==[(0,4),(4,8),(8,12)]
    assert len((OUT/'data/example.srt').read_text(encoding='utf-8').strip().split('\n\n'))==3
    print('Gallery OK: local links, source/output hashes, original 3D scene, 150-frame 2D MP4, and preauthored 3-shot SRT')
if __name__=='__main__':main()
