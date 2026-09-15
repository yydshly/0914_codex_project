"""Exercise the upstream 3D export API, then encode its PNGs with FFmpeg."""
import hashlib
import io
import json
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8044'

def export(endpoint, body):
    request = urllib.request.Request(BASE + endpoint, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read()

def main():
    assets = ROOT / 'assets'
    frames = ROOT / '.cache' / 'frames'
    frames.mkdir(parents=True, exist_ok=True)
    data = export('/export/sequence', {'startFrame': 0, 'endFrame': 89, 'renderScale': 1})
    archive = zipfile.ZipFile(io.BytesIO(data))
    names = archive.namelist()
    expected = [f'frame-{i:04d}.png' for i in range(90)]
    assert names == expected, names
    for name in names:
        (frames / name).write_bytes(archive.read(name))
    cover = archive.read('frame-0045.png')
    (assets / 'cover.png').write_bytes(cover)
    # A second browser launch renders frame 45 independently of frames 0..44.
    repeated = export('/export/frame', {'frame': 45, 'renderScale': 1})
    (ROOT / '.cache' / 'repeat-45.png').write_bytes(repeated)
    negative = export('/export/frame', {'frame': -9, 'renderScale': 1})
    oversized = export('/export/frame', {'frame': 999, 'renderScale': 1})
    checks = {'frame45_separate_browser_matches_sequence': repeated == cover,
              'negative_frame_clamps_to_zero': negative == archive.read('frame-0000.png'),
              'oversized_frame_clamps_to_last': oversized == archive.read('frame-0089.png')}
    video = assets / 'demo-3d.mp4'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '30', '-i', str(frames / 'frame-%04d.png'), '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', str(video)], check=True)
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(video)], text=True))
    result = {'date': '2026-09-16', 'sequence_entries': len(names), 'checks': checks,
              'sha256_frame45': hashlib.sha256(cover).hexdigest(), 'media': probe,
              'scope': 'Unmodified upstream 3D template; PNG/ZIP via upstream API; MP4 encoding added by this research. No AI generation or audio.'}
    (ROOT / 'notes' / 'render-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'frames': len(names), 'checks': checks, 'video': str(video)}, ensure_ascii=False))
    assert all(checks.values()), 'See render-results.json for failed assumptions'

if __name__ == '__main__':
    main()
