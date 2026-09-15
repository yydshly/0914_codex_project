"""Deterministic, audio-locked paper theatre. Pillow frames -> FFmpeg H.264."""
import argparse
from array import array
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
from synthesize import stamp

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
W, H, FPS = 1920, 1080, 24
INK = "#223d37"
MUTED = "#718078"
TEAL = "#287d70"
CORAL = "#ce634d"
GOLD = "#bf8b2d"
raw = json.loads((ASSETS / "provider-subtitles.json").read_text(encoding="utf-8"))
meta = json.loads((ASSETS / "voice-metadata.json").read_text(encoding="utf-8"))
CUES = [{"id": i, "start": x["time_begin"] / 1000, "end": x["time_end"] / 1000,
         "text": x["text"], "caption": re.sub(r"[。！？]+$", "", x["text"])} for i, x in enumerate(raw)]
assert len(CUES) == 12, "This storyboard requires the twelve authored sentence cues."
assert [x["text"] for x in CUES] == meta["transcript"], "Provider transcript differs from the storyboard."
DURATION = math.ceil((meta["duration"] + 1.4) * FPS) / FPS
S = [x["start"] for x in CUES]

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc", size)

def txt(im, xy, text, size=30, color=INK, bold=False, anchor=None):
    ImageDraw.Draw(im).text(xy, text, font=font(size,bold), fill=color, anchor=anchor)

def box(im, bounds, fill, radius=12, outline=None, width=1):
    ImageDraw.Draw(im).rounded_rectangle(tuple(round(x) for x in bounds), radius, fill=fill, outline=outline, width=width)

def ease(v):
    v = max(0, min(1, v))
    return v*v*(3-2*v)

def lerp(a,b,p):
    return a+(b-a)*p

def place(im, asset, x, y, opacity=1, scale=1):
    if opacity <= 0 or scale <= 0: return
    if scale != 1:
        asset = asset.resize((max(1,round(asset.width*scale)),max(1,round(asset.height*scale))), Image.Resampling.LANCZOS)
    if opacity < 1:
        asset = asset.copy()
        asset.putalpha(asset.getchannel("A").point(lambda a:round(a*opacity)))
    im.alpha_composite(asset, (round(x),round(y)))

def card(w,h,bg="#fffdf5"):
    im = Image.new("RGBA",(w+16,h+18))
    box(im,(7,10,w+7,h+10),(58,65,47,25),10)
    box(im,(0,0,w,h),bg,10,"#d8d6c6",2)
    return im

def note(index, compact=False):
    titles = ["周五发布新版", "小林负责上线", "先修复登录问题"]
    small = ["什么时候？", "谁来负责？", "上线前要做什么？"]
    cols = [GOLD,TEAL,CORAL]
    w,h = (460,110) if compact else (485,260)
    im = card(w,h)
    d = ImageDraw.Draw(im)
    d.rectangle((0,16,6,h-16),fill=cols[index])
    if compact:
        txt(im,(26,16),f"0{index+1}",22,cols[index],True)
        txt(im,(78,35),titles[index],34,INK,True)
    else:
        box(im,(28,25,102,62),["#f2e4bb","#d9eae1","#f5dfd6"][index],7)
        txt(im,(65,44),f"0{index+1}",23,cols[index],True,"mm")
        txt(im,(30,96),titles[index],43,INK,True)
        txt(im,(30,185),small[index],26,MUTED)
    return im

NOTES = [note(i) for i in range(3)]
SMALL = [note(i,True) for i in range(3)]
MACHINE = Image.open(ASSETS / "paper-machine.png").convert("RGBA").resize((490,490),Image.Resampling.LANCZOS)

def summary(active=-1):
    im = card(475,398)
    box(im,(22,21,453,77),"#deece2",6)
    txt(im,(43,33),"行动摘要",34,TEAL,True)
    ImageDraw.Draw(im).line([(407,49),(417,59),(437,36)],fill=TEAL,width=4)
    rows = [("时间","周五发布",GOLD),("负责人","小林",TEAL),("前置条件","修复登录问题",CORAL)]
    for i,(label,value,col) in enumerate(rows):
        y=108+i*88
        if active == i:
            box(im,(18,y-9,454,y+68),"#fbefd1",7,col,3)
        txt(im,(32,y),label,22,MUTED)
        txt(im,(167,y+8),value,32,col,True)
        if i<2: ImageDraw.Draw(im).line((30,y+71,445,y+71), fill="#e7e5d8",width=2)
    return im

SUMMARIES=[summary(i) for i in [-1,0,1,2]]

PCM = array("h", subprocess.check_output(["ffmpeg","-v","error","-i",str(ASSETS/"narration.mp3"),"-f","s16le","-ac","1","-ar","8000","pipe:1"]))
LEVELS = [min(1,math.sqrt(sum(v*v for v in PCM[i:i+160])/max(1,len(PCM[i:i+160])))/6500) for i in range(0,len(PCM),160)]

def background():
    im=Image.new("RGBA",(W,H),"#efe8d8")
    d=ImageDraw.Draw(im)
    # A repeatable subtle paper grain; the stage never moves.
    for y in range(0,H,4):
        for x in range((y%5)*3,W,19):
            d.point((x,y),fill="#e1d9c8")
    txt(im,(80,55),"PAPER THEATRE   /   纸艺剧场",23,TEAL,True)
    txt(im,(80,111),"三条记录，一张行动摘要",65,INK,True)
    txt(im,(84,210),"从零散信息，到看得见的行动。",27,MUTED)
    box(im,(1570,60,1840,113),"#e1e6d4",25)
    txt(im,(1705,86),"01   ·   会议记录",24,INK,True,"mm")
    box(im,(65,278,1855,875),"#f8f6ec",22,"#d6d3bf",2)
    d.line((105,810,1815,810), fill="#e2dfd0",width=2)
    box(im,(65,916,1855,1018),INK,18)
    txt(im,(80,1035),"AUDIO-LOCKED PAPER THEATRE",17,MUTED)
    txt(im,(1835,1035),"MiniMax 配音  ·  独立纸艺图层",17,MUTED,anchor="ra")
    return im

BG=background()

def render(t):
    im=BG.copy()
    d=ImageDraw.Draw(im)
    p=t/DURATION
    d.line((83,898,1837,898),fill="#dad4c0",width=5)
    d.line((83,898,83+1754*p,898),fill=TEAL,width=5)
    txt(im,(1814,221),f"{int(t):02d} / {int(DURATION):02d} s",22,MUTED,anchor="ra")
    section=0 if t<S[5] else 1 if t<S[7] else 2
    labels=["01  留下记录","02  提取重点","03  形成行动"]
    for i,label in enumerate(labels):
        x=111+575*i
        txt(im,(x,303),label,24,TEAL if i==section else "#a4aaa0",i==section)

    contract=ease((t-S[4])/1.05)
    for i in range(3):
        appear=ease((t-S[i+1])/0.65)
        if not appear: continue
        if contract==0:
            place(im,NOTES[i],155+i*561,435+40*(1-appear),appear)
        elif contract<1:
            # Transition each full card into its compact archive position.
            asset=NOTES[i].resize((round(lerp(501,476,contract)),round(lerp(278,128,contract))),Image.Resampling.LANCZOS)
            place(im,asset,lerp(155+i*561,148,contract),lerp(435,380+i*131,contract),appear)
        else:
            place(im,SMALL[i],148,380+i*131,appear)
    if t<S[1]:
        txt(im,(960,506),"一场会，留下了什么？",49,INK,True,"mm")
        txt(im,(960,583),"时间  /  负责人  /  前置条件",29,MUTED,anchor="mm")
    if S[4] <= t < S[5]:
        q=ease((t-S[4]-.5)/.5)
        txt(im,(1130,499),"记录齐了，",49,INK,True,"mm")
        txt(im,(1130,576),"重点还没站出来。",49,CORAL,True,"mm")
    if t>=S[5]:
        arrival=ease((t-S[5])/.7)
        place(im,MACHINE,721,309+32*(1-arrival),arrival)
        if t>S[5]+.7 and not S[7]<=t<S[7]+1.9:
            txt(im,(966,777),"信息整理机",26,TEAL,True,"mm")
        # One document at a time follows a path into the measured upper slot.
        for i in range(3):
            begin=S[5]+.75+i*.79
            travel=(t-begin)/.74
            if 0<travel<1:
                q=ease(min(1,travel/.64))
                x=lerp(200,827,q)
                y=lerp(390+i*110,358,q)
                scale=lerp(.70,.55,q)
                if travel>.64: y=lerp(358,475,ease((travel-.64)/.36))
                layer=Image.new("RGBA",(W,H))
                place(layer,SMALL[i],x,y,1,scale)
                # Hard slot mask: material disappears below the upper opening.
                layer.paste((0,0,0,0),(785,463,1215,875))
                im.alpha_composite(layer)
        if S[6] <= t < S[7]:
            part=min(2,int((t-S[6])/(CUES[6]["end"]-S[6])*3))
            labels2=["时间","负责人","前置条件"]
            values=["周五","小林","修复登录"]
            box(im,(892,553,1046,595),"#d9eee7",5)
            txt(im,(969,574),values[part],21,TEAL,True,"mm")
            txt(im,(1434,430),"从原文里，找到",31,MUTED,anchor="mm")
            txt(im,(1434,500),labels2[part],52,INK,True,"mm")
            # Deterministic target highlight; no generated text or circle.
            y=380+part*131
            d=ImageDraw.Draw(im)
            d.rounded_rectangle((140,y-6,619,y+116),12,outline=[GOLD,TEAL,CORAL][part],width=4)
            for k in range(3):
                box(im,(1302+k*92,573,1366+k*92,583),TEAL if k<=part else "#dce2d4",5)
        if t>=S[7]:
            output=ease((t-S[7])/.9)
            depart=ease((t-S[7]-.9)/.85)
            if depart<1:
                # The receipt originates at the registered lower output port.
                asset=SUMMARIES[0]
                scale=lerp(.36,1,depart)
                x=lerp(879,1289,depart)
                y=lerp(680-152*(1-output),371,depart)
                layer=Image.new("RGBA",(W,H))
                place(layer,asset,x,y,1,scale)
                if depart==0: layer.paste((0,0,0,0),(721,278,1215,679))
                im.alpha_composite(layer)
            else:
                active=-1
                if S[8]<=t<CUES[8]["end"]:
                    active=min(2,int((t-S[8])/(CUES[8]["end"]-S[8])*3))
                place(im,SUMMARIES[active+1],1289,371)
            if t>S[7]+2:
                d=ImageDraw.Draw(im)
                d.line((1180,624,1260,624),fill=TEAL,width=4)
                d.polygon([(1260,624),(1247,616),(1247,632)],fill=TEAL)
        if t>=S[9]:
            txt(im,(384,777),"原始记录 · 保留",24,TEAL,True,"mm")
        if t>=S[10]:
            txt(im,(705,842),"真实口播",21,TEAL,True,"mm")
            for k in range(42):
                at=round((t-1.05+k*.05)/.02)
                amp=LEVELS[at] if 0<=at<len(LEVELS) else 0
                hh=3+amp*18
                x=796+k*7
                ImageDraw.Draw(im).line((x,842-hh,x,842+hh),fill=TEAL,width=3)
            txt(im,(1240,842),"画面跟随声音",21,INK,True,"mm")
        elif t>=S[7]:
            txt(im,(967,842),"原始记录  →  提取关键信息  →  行动摘要",24,MUTED,anchor="mm")

    cue=next((c for c in CUES if c["start"]<=t<=c["end"]),None)
    if cue:
        text=cue["caption"]
        size=36
        while font(size).getlength(text)>1640: size-=1
        txt(im,(960,966),text,size,"#fffdf3",False,"mm")
    else:
        # Preserve real pauses instead of holding an outdated caption.
        txt(im,(960,966),"·  ·  ·" if t<meta["duration"] else "先有声音，再让画面把意思演出来",30,"#c4d7c7",False,"mm")
    return im.convert("RGB")

def evidence():
    (ASSETS/"timeline.json").write_text(json.dumps({"duration":DURATION,"fps":FPS,"audio_duration":meta["duration"],"cues":CUES,
        "timing_precision":"provider sentence boundaries; within-sentence actions are authored subdivisions, not word alignment"},ensure_ascii=False,indent=2),encoding="utf-8")
    for kind in ["captions","narration"]:
        srt="\n\n".join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['caption'] if kind=='captions' else c['text']}" for i,c in enumerate(CUES))+"\n"
        (OUT/f"{kind}.srt").write_text(srt,encoding="utf-8")
    # Actual voice duration drives every scene and the frame count.
    assert all(a["end"]<=b["start"] for a,b in zip(CUES,CUES[1:]))
    assert CUES[-1]["end"]<=meta["duration"]+.05
    assert hashlib.sha256((ASSETS/"narration.mp3").read_bytes()).hexdigest()==meta["sha256"]
    times=[1,4.4,7.3,10.2,14.3,17.6,21.0,23.6,26.0,27.4,30.7,35.3,40,45]
    sheet=Image.new("RGB",(1280,math.ceil(len(times)/2)*390),"#efe8d8")
    for i,t in enumerate(times):
        frame=render(t)
        frame.save(OUT/f"frame-{t:05.1f}.jpg",quality=91)
        thumb=frame.resize((640,360),Image.Resampling.LANCZOS)
        x,y=(i%2)*640,(i//2)*390
        sheet.paste(thumb,(x,y))
        ImageDraw.Draw(sheet).text((x+16,y+364),f"{t:.1f} s",font=font(18),fill=INK)
    sheet.save(OUT/"contact-sheet.jpg",quality=88)
    render(35.3).resize((1280,720),Image.Resampling.LANCZOS).save(ASSETS/"cover.jpg",quality=88)
    print("Evidence frames and provider-aligned subtitles saved.",flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--frames-only",action="store_true")
    args=parser.parse_args()
    evidence()
    if args.frames_only:return
    output=OUT/"paper-theatre-demo.mp4"
    cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","pipe:0",
        "-i",str(ASSETS/"narration.mp3"),"-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p","-threads","4",
        "-af","apad","-t",str(DURATION),"-c:a","aac","-b:a","192k","-movflags","+faststart",str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(round(DURATION*FPS)):
            proc.stdin.write(render(n/FPS).tobytes())
            if n%(FPS*5)==0: print(f"Rendered {n/FPS:.0f}/{DURATION:.1f}s",flush=True)
    finally:
        proc.stdin.close()
    if proc.wait()!=0: raise SystemExit("FFmpeg render failed")
    print(str(output),flush=True)

if __name__=="__main__":main()
