"""Verify research evidence and delivery artifacts, without model calls."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def main():
    inventory = json.loads((ROOT / 'notes/inventory.json').read_text(encoding='utf-8'))
    assert len(inventory['repositories']) == 4
    for entry in inventory['files']:
        assert hashlib.sha256((ROOT / entry['local']).read_bytes()).hexdigest() == entry['sha256'], entry['local']
    skills = next(r for r in inventory['repositories'] if r['name'] == 'skills')['skill_entries']
    assert len(skills) == 15
    skill_doc = (ROOT / 'notes/skills.md').read_text(encoding='utf-8')
    assert all(p in skill_doc for p in skills)
    for p in ['index.js','index.html','src/sceneControls.js','scripts/export-api.mjs']:
        assert (ROOT / 'src/demo-3d' / p).read_bytes() == (ROOT / 'upstream/create-vibe-motion-3d/packages/template' / p).read_bytes(), p
    # Research documents only: upstream snapshot intentionally omits supporting resources.
    for doc in [ROOT / 'README.md', *sorted((ROOT / 'notes').glob('*.md'))]:
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'):
                continue
            path = unquote(link.split('#')[0])
            assert (doc.parent / path).exists(), (doc.name, link)
    probes = json.loads((ROOT / 'notes/probe-2d-results.json').read_text(encoding='utf-8'))
    assert len(probes['results']) == 7 and all(x['passed'] for x in probes['results'])
    render = json.loads((ROOT / 'notes/render-results.json').read_text(encoding='utf-8'))
    assert render['sequence_entries'] == 90 and all(render['checks'].values())
    assert hashlib.sha256((ROOT / 'assets/cover.png').read_bytes()).hexdigest() == render['sha256_frame45']
    media = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json', str(ROOT / 'assets/demo-3d.mp4')], text=True))
    assert len(media['streams']) == 1
    video = media['streams'][0]
    assert (video['width'],video['height'],video['avg_frame_rate'],int(video['nb_read_frames'])) == (2048,1152,'30/1',90)
    assert abs(float(media['format']['duration'])-3) < 0.01
    print(f"Verified {len(inventory['files'])} source hashes, 15 skills, 7 2D checks, 3 3D checks, document links and 90-frame MP4")

if __name__ == '__main__':
    main()
