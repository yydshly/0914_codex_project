"""Validate the encoded deliverable, original audio, and provider timing evidence."""
from array import array
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--episode",choices=["dns","task-training","english"])
args=parser.parse_args()
if args.episode:ROOT=ROOT/"demos"/args.episode
video=ROOT/("output/demo.mp4" if args.episode else "output/paper-theatre-demo.mp4")
voice=ROOT/"assets/narration.mp3"
timeline=json.loads((ROOT/"assets/timeline.json").read_text(encoding="utf-8"))
meta=json.loads((ROOT/"assets/voice-metadata.json").read_text(encoding="utf-8"))

def pcm(path):
    return array("h",subprocess.check_output(["ffmpeg","-v","error","-i",str(path),"-vn","-ac","1","-ar","8000","-f","s16le","pipe:1"]))

probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)],text=True))
v=next(s for s in probe["streams"] if s["codec_type"]=="video")
a=next(s for s in probe["streams"] if s["codec_type"]=="audio")
assert (v["width"],v["height"])==(1920,1080)
assert v["codec_name"]=="h264" and a["codec_name"]=="aac"
assert abs(float(probe["format"]["duration"])-timeline["duration"])<.15
decode=subprocess.run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"],capture_output=True,text=True)
assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
black=subprocess.run(["ffmpeg","-hide_banner","-i",str(video),"-vf","blackdetect=d=0.1:pix_th=0.08","-an","-f","null","-"],capture_output=True,text=True)
assert "black_start:" not in black.stderr
original,encoded=pcm(voice),pcm(video)
n=min(len(original),len(encoded))
start=800
x,y=original[start:n],encoded[start:n]
dot=sum(i*j for i,j in zip(x,y))
correlation=dot/math.sqrt(sum(i*i for i in x)*sum(j*j for j in y))
assert correlation>.97,f"Audio correspondence too low: {correlation}"
assert hashlib.sha256(voice.read_bytes()).hexdigest()==meta["sha256"]
cues=timeline["cues"]
assert all(c["end"]>c["start"] for c in cues)
assert all(x["end"]<=y["start"] for x,y in zip(cues,cues[1:]))
report={"status":"PASS","video":{"resolution":"1920x1080","fps":v["r_frame_rate"],"duration":float(probe["format"]["duration"]),"size_bytes":video.stat().st_size},
        "full_decode":"PASS","black_intervals":0,"original_voice_sha256_unchanged":True,"source_to_encoded_audio_correlation":round(correlation,6),
        "sentence_cues":len(cues),"sentence_timestamps_source":"MiniMax","audio_speed_changed":False,"added_tail_hold_seconds":round(timeline["duration"]-meta["duration"],3),
        "scope":"Local audio-locked demonstration, not an upstream full-episode certification.",
        "limitations":["Within-sentence actions use authored subdivisions; no word-level alignment claim.","Content and animation are authored; this is not a live DNS query or task-execution service.","Visual QA is manual review of actual rendered frames; no independent steward certification."]}
(ROOT/"output/qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [video,voice,ROOT/"output/captions.srt"]}
(ROOT/"output/sha256.json").write_text(json.dumps(hashes,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=True,indent=2))
