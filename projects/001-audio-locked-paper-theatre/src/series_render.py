"""Two distinct audio-led science and training storyboards, rendered at 1080p."""
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from PIL import Image,ImageDraw
from render import font,txt,box,ease,lerp,place,card
from synthesize import stamp

ROOT=Path(__file__).resolve().parents[1]
W,H,FPS=1920,1080,24
INK="#243c43"
MUTED="#7a8583"
BLUE="#356f94"
CORAL="#bf604c"
GREEN="#327b68"
GOLD="#b08430"

def arrow(im,a,b,color=BLUE,width=4):
    d=ImageDraw.Draw(im)
    d.line([a,b],fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    points=[b,(b[0]-15*math.cos(angle-.5),b[1]-15*math.sin(angle-.5)),(b[0]-15*math.cos(angle+.5),b[1]-15*math.sin(angle+.5))]
    d.polygon(points,fill=color)

def label(im,x,y,w,text,color=BLUE,bg="#e3edf0",size=26):
    box(im,(x,y,x+w,y+51),bg,9)
    txt(im,(x+w/2,y+25),text,size,color,True,"mm")

def tick(im,x,y,color=GREEN):
    ImageDraw.Draw(im).line([(x-10,y),(x-2,y+9),(x+15,y-13)],fill=color,width=5)

def packet(im,a,b,p,text,color=BLUE):
    if not 0<=p<=1:return
    p=ease(p)
    x,y=lerp(a[0],b[0],p),lerp(a[1],b[1],p)
    box(im,(x-36,y-18,x+36,y+18),"#fffdf6",7,color,2)
    txt(im,(x,y),text,20,color,True,"mm")

class Episode:
    def __init__(self,slug):
        self.slug=slug
        self.root=ROOT/"demos"/slug
        self.assets=self.root/"assets"
        self.out=self.root/"output"
        self.out.mkdir(exist_ok=True)
        self.meta=json.loads((self.assets/"voice-metadata.json").read_text(encoding="utf-8"))
        raw=json.loads((self.assets/"provider-subtitles.json").read_text(encoding="utf-8"))
        self.cues=[{"id":i,"start":x["time_begin"]/1000,"end":x["time_end"]/1000,"text":x["text"],"caption":re.sub(r"[。！？]+$","",x["text"])} for i,x in enumerate(raw)]
        assert len(self.cues)==13
        assert [c["text"] for c in self.cues]==self.meta["transcript"]
        self.s=[c["start"] for c in self.cues]
        self.duration=math.ceil((self.meta["duration"]+1.5)*FPS)/FPS
        self.color=BLUE if slug=="dns" else CORAL
        self.title="输入网址后，电脑怎样找到网站？" if slug=="dns" else "把一句模糊需求，变成可执行任务"
        self.subtitle="DNS：从一个好记的名字，到可以连接的网络地址。" if slug=="dns" else "新人培训 / 任务交接：负责人、交付物、期限、验收标准。"
        name="computer.png" if slug=="dns" else "clipboard.png"
        self.prop=Image.open(self.assets/name).convert("RGBA").resize((430,430),Image.Resampling.LANCZOS)
        self.machine=Image.open(ROOT/"assets/paper-machine.png").convert("RGBA").resize((375,375),Image.Resampling.LANCZOS)
        self.bg=self.background()

    def background(self):
        im=Image.new("RGBA",(W,H),"#eee9dd" if self.slug=="dns" else "#f0e6db")
        d=ImageDraw.Draw(im)
        for y in range(0,H,5):
            for x in range((y%7)*2,W,23):d.point((x,y),fill="#dfdacf")
        kind="SCIENCE / 科普演示" if self.slug=="dns" else "LEARNING / 教学培训"
        txt(im,(80,55),"PAPER THEATRE   /   "+kind,23,self.color,True)
        txt(im,(80,114),self.title,59,INK,True)
        txt(im,(84,213),self.subtitle,27,MUTED)
        label(im,1580,55,260,"02 · DNS" if self.slug=="dns" else "03 · 任务交接",self.color)
        box(im,(65,278,1855,875),"#faf8f0",22,"#d5d4c7",2)
        box(im,(65,916,1855,1018),INK,18)
        txt(im,(80,1035),"AUDIO-LOCKED PAPER THEATRE",17,MUTED)
        txt(im,(1835,1035),"MiniMax 配音 · 独立图层 · 逐句编排",17,MUTED,anchor="ra")
        return im

    def phase(self,t):
        return max(0,max((i for i,c in enumerate(self.cues) if c["start"]<=t),default=0))

    def render(self,t):
        im=self.bg.copy()
        (self.dns if self.slug=="dns" else self.training)(im,t)
        d=ImageDraw.Draw(im)
        d.line((83,898,1837,898),fill="#d7d5c8",width=5)
        d.line((83,898,83+1754*min(1,t/self.duration),898),fill=self.color,width=5)
        txt(im,(1820,223),f"{int(t):02d} / {round(self.duration):02d} s",22,MUTED,anchor="ra")
        cue=next((c for c in self.cues if c["start"]<=t<=c["end"]),None)
        if cue:
            text=cue["caption"]
            size=36
            while font(size).getlength(text)>1635:size-=1
            txt(im,(960,966),text,size,"#fffdf5",anchor="mm")
        else:
            txt(im,(960,966),"·  ·  ·" if t<self.meta["duration"] else "名字变地址，再去取网页" if self.slug=="dns" else "把任务说清楚，让行动有依据",30,"#d5e3db",anchor="mm")
        return im.convert("RGB")

    def dns(self,im,t):
        n=self.phase(t);s=self.s
        section="01  名字与地址" if n<4 else "02  查询与返回" if n<9 else "03  连接与缓存"
        txt(im,(105,307),section,25,BLUE,True)
        if n<2:
            place(im,self.prop,225,365)
            typed="example.com"[:min(11,int(t*8)+1)]
            txt(im,(440,506),typed,28,BLUE,True,"mm")
            txt(im,(440,550),"查找网站…",20,MUTED,anchor="mm")
            label(im,246,361,390,"example.com",BLUE,size=31)
            q=ease((t-s[1])/.7) if n else 0
            txt(im,(1165,455),"网址是名字",55,INK,True,"mm")
            txt(im,(1165,549),"网络地址在哪里？",43,BLUE,True,"mm")
            if q:
                arrow(im,(739,567),(874,567))
                label(im,993,652,360,"名字 ≠ 网络地址",BLUE)
            txt(im,(960,831),"示例域名：example.com",23,MUTED,anchor="mm")
            return
        place(im,self.prop,98,363)
        txt(im,(313,494),"example.com",27,BLUE,True,"mm")
        got_address=n>=9 or (n==8 and t>s[8]+3.4)
        screen="网页已打开" if n>=10 else "正在连接…" if n==9 else "已找到地址" if got_address else "正在查找…"
        txt(im,(313,542),screen,23,GREEN if got_address else MUTED,anchor="mm")
        label(im,112,356,395,"example.com",BLUE,size=29)
        txt(im,(310,779),"你的设备 / 浏览器",27,INK,True,"mm")
        p=ease((t-s[2])/.8)
        place(im,self.machine,671,392+35*(1-p),p)
        if p==1:txt(im,(858,595),"DNS",19,GREEN,True,"mm")
        txt(im,(858,778),"递归解析器",28,GREEN,True,"mm")
        # Device communicates with the resolver; each referral returns to it.
        arrow(im,(530,555),(656,555),BLUE)
        if n==2:
            packet(im,(534,555),(650,555),(t-s[2]-.4)/1.3,"查询")
            txt(im,(1437,473),"查号服务",53,INK,True,"mm")
            txt(im,(1437,565),"帮你找到网络地址",32,MUTED,anchor="mm")
        if n==3:
            for x,title in [(190,"设备缓存"),(744,"解析器缓存")]:
                label(im,x,677,240,title,GREEN,"#e3eddf",25)
                d=ImageDraw.Draw(im);d.ellipse((x+88,634,x+118,664),outline=GOLD,width=4)
                d.line((x+114,660,x+127,674),fill=GOLD,width=4)
            txt(im,(1425,465),"有可用缓存？",46,INK,True,"mm")
            txt(im,(1425,552),"命中 → 可以直接使用",30,GREEN,True,"mm")
            txt(im,(1425,622),"未命中 → 继续查询",30,CORAL,True,"mm")
        if 4<=n<=8:
            names=[("根服务器","指向顶级域服务器"),(".com 顶级域服务器","指向权威服务器"),("权威服务器","返回该域名的地址记录")]
            active=min(2,max(0,n-5))
            for i,(title,desc) in enumerate(names):
                x,y=1302,355+i*142
                a=ease((t-s[4]-.14*i)/.5)
                tile=card(440,112,"#e8f0f1" if i==active and n>=5 else "#fffdf5")
                txt(tile,(23,15),title,29,BLUE,True)
                txt(tile,(23,65),desc,23,MUTED)
                place(im,tile,x+30*(1-a),y,a)
            if n==4:
                label(im,703,355,320,"没有可用缓存，开始查找",CORAL,"#f2e5dc",22)
            if 5<=n<=7:
                i=n-5
                a,b=(1051,500+i*26),(1284,406+i*142)
                arrow(im,a,b,BLUE)
                fraction=(t-s[n])/(self.cues[n]["end"]-s[n])
                if n==7:
                    packet(im,a,b,min(1,fraction*1.4),"查询",BLUE)
                elif fraction<.46:
                    packet(im,a,b,fraction/.46,"查询",BLUE)
                else:
                    backa=(b[0],b[1]+24);backb=(a[0],a[1]+24)
                    arrow(im,backa,backb,GREEN)
                    packet(im,backa,backb,(fraction-.46)/.54,"指引" if n<7 else "记录",GREEN)
                label(im,698,355,340,["问根服务器","问 .com 服务器","问权威服务器"][i],BLUE,size=24)
            if n==8:
                arrow(im,(1285,700),(1050,606),GREEN)
                arrow(im,(657,592),(528,592),GREEN)
                q=(t-s[8])/(self.cues[8]["end"]-s[8])
                if q<.48:packet(im,(1285,700),(1050,606),q/.48,"地址",GREEN)
                else:packet(im,(657,592),(528,592),(q-.48)/.52,"地址",GREEN)
                if got_address:label(im,120,692,380,"已得到网站地址",GREEN,"#e2eddf",27)
        if n>=9:
            server=card(430,270,"#e8edf0")
            txt(server,(215,58),"网站服务器",40,BLUE,True,"mm")
            for k in range(3):
                box(server,(36,106+k*41,392,134+k*41),"#fffdf5",6)
                ImageDraw.Draw(server).ellipse((55,114+k*41,66,125+k*41),fill=GREEN)
            place(im,server,1310,423)
            txt(im,(1518,759),"提供网页内容",26,INK,True,"mm")
            # Web connection bypasses the DNS resolver, using the lower lane.
            label(im,1070,744,215,"直接连接网站" if n<11 else "网页内容返回",BLUE,"#e6eef0",23)
            arrow(im,(524,812),(1286,812),BLUE) if n<11 else arrow(im,(1286,812),(524,812),GREEN)
            if n==9:
                packet(im,(524,812),(1286,812),(t-s[9])/(self.cues[9]["end"]-s[9]),"请求",BLUE)
            if n==10:
                label(im,700,348,320,"缓存 · 在有效期内使用",GREEN,"#e2eddf",23)
                packet(im,(540,554),(651,554),(t-s[10])/(self.cues[10]["end"]-s[10]),"查询",BLUE)
            if n>=11:
                label(im,706,354,300,"DNS：找地址",GREEN,"#e2eddf",26)
                label(im,1315,354,426,"网站：给内容",BLUE,"#e3edf0",26)
                q=(t-s[n])/(self.cues[n]["end"]-s[n])
                packet(im,(1286,812),(532,812),q,"网页",GREEN)
        footer="简化示意：不展示别名、多地址和连接握手等细节" if n<9 else "DNS 查询与网页传输，是两个不同的过程"
        txt(im,(960,845),footer,22,MUTED,anchor="mm")

    def training(self,im,t):
        n=self.phase(t);s=self.s
        headings=["负责人","交付物","期限","验收标准"]
        values=["小林","一份客户反馈表","本周五 15:00 前","包含问题、影响和建议"]
        colors=[BLUE,GREEN,GOLD,CORAL]
        section="01  发现模糊点" if n<3 else "02  补齐四要素" if n<9 else "03  复述与练习"
        txt(im,(105,307),section,25,CORAL,True)
        if n<9:
            place(im,self.prop,106,373)
            txt(im,(321,489),"任务单",37,CORAL,True,"mm")
            for i,h in enumerate(headings):
                y=553+i*43
                txt(im,(258,y),h,23,colors[i] if n>=i+3 else MUTED)
                if n>=i+3:tick(im,231,y+17,colors[i])
                else:box(im,(222,y+6,239,y+24),None,2,"#a99e93",2)
            label(im,143,764,357,"需求 → 任务",CORAL,"#f0e0d7",27)
        if n==0:
            tile=card(1070,258)
            txt(tile,(55,39),"收到一句需求",26,MUTED)
            txt(tile,(55,107),"“尽快整理一下客户反馈”",51,CORAL,True)
            place(im,tile,643,428)
            txt(im,(1160,751),"可以直接开始了吗？",31,INK,True,"mm")
        elif n in [1,2]:
            for i,h in enumerate(headings):
                x,y=666+(i%2)*540,382+(i//2)*206
                a=ease((t-s[1]-.25*i)/.5)
                tile=card(480,162)
                txt(tile,(28,20),h,26,colors[i],True)
                txt(tile,(240,98),"？",59,CORAL,True,"mm")
                place(im,tile,x,y+25*(1-a),a)
            txt(im,(1180,827),"先补齐四项，再开始执行",28,INK,True,"mm")
        elif 3<=n<=6:
            active=n-3
            for i,(h,v) in enumerate(zip(headings,values)):
                y=368+i*111
                tile=card(1060,92)
                txt(tile,(30,25),f"0{i+1}  {h}",28,colors[i],True)
                if i<=active:
                    a=ease((t-s[i+3])/.65)
                    txt(tile,(324+round(60*(1-a)),25),v,32,INK,True)
                    if a>.9:tick(tile,1007,44,colors[i])
                else:txt(tile,(326,29),"待明确",28,"#adb1a7")
                place(im,tile,667,y)
                if i==active:ImageDraw.Draw(im).rounded_rectangle((659,y-5,1735,y+99),12,outline=colors[i],width=4)
        elif n in [7,8]:
            tile=card(1070,403)
            label(tile,27,22,1015,"一项可以交接的任务",GREEN,"#e2eddf",29)
            lines=[("小林",BLUE),("周五 15:00 前，提交客户反馈表",INK),("必须包含：问题 / 影响 / 建议",CORAL)]
            for i,(text,col) in enumerate(lines):
                a=ease((t-s[7]-.18*i)/.65)
                txt(tile,(53,121+i*79),text,41 if i!=1 else 38,col,True)
            place(im,tile,652+55*(1-ease((t-s[7])/.8)),371,ease((t-s[7])/.8))
            for i,h in enumerate(headings):label(im,681+i*260,810,230,h,colors[i],"#eee8da",23)
        elif n==9:
            place(im,self.prop,743,347,1,.74)
            txt(im,(902,472),"交接",31,CORAL,True,"mm")
            for i,h in enumerate(headings):txt(im,(854,520+i*26),h,17,MUTED)
            left=card(520,215);right=card(590,280)
            txt(left,(30,23),"发起方",27,CORAL,True)
            txt(left,(30,88),"请你复述一下",41,INK,True)
            txt(left,(30,147),"接下来怎么做。",34,MUTED)
            txt(right,(30,25),"接收者",27,GREEN,True)
            for i,line in enumerate(["我负责整理反馈表，","周五 15:00 前提交，","包含问题、影响和建议。"]):txt(right,(30,85+i*57),line,32,INK,True)
            place(im,left,147,431)
            a=ease((t-s[9]-1.1)/.8)
            place(im,right,1180,399+35*(1-a),a)
            arrow(im,(691,553),(798,553),CORAL)
            arrow(im,(1091,553),(1161,553),GREEN)
            label(im,665,781,590,"让对方复述，确认双方理解一致",GREEN,"#e2eddf",27)
        else:
            label(im,118,362,205,"练习一下",CORAL,"#f1e1d7",27)
            txt(im,(960,456),"“尽快优化首页”",59,INK,True,"mm")
            txt(im,(960,540),"这句话，还缺哪些信息？",32,MUTED,anchor="mm")
            for i,h in enumerate(headings):
                x=140+i*435
                tile=card(385,167)
                reveal=n>=11 and t>=s[11]+i*1.05
                txt(tile,(192,43),f"0{i+1}",23,colors[i],True,"mm")
                txt(tile,(192,107),h if reveal else "？",37 if reveal else 53,colors[i] if reveal else "#b1aca1",True,"mm")
                place(im,tile,x,605)
            if n==10:txt(im,(960,827),"可以暂停视频，先自己想一想",27,CORAL,True,"mm")
            else:txt(im,(960,827),"负责人明确 · 交付物具体 · 期限清楚 · 验收可检查",26,GREEN,True,"mm")

    def evidence(self):
        assert all(a["end"]<=b["start"] for a,b in zip(self.cues,self.cues[1:]))
        assert self.cues[-1]["end"]<=self.meta["duration"]+.05
        assert hashlib.sha256((self.assets/"narration.mp3").read_bytes()).hexdigest()==self.meta["sha256"]
        timeline={"duration":self.duration,"audio_duration":self.meta["duration"],"fps":FPS,"cues":self.cues,
                  "timing_precision":"MiniMax sentence boundaries. Actions within a sentence use authored timing.","title":self.title}
        (self.assets/"timeline.json").write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding="utf-8")
        srt="\n\n".join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['caption']}" for i,c in enumerate(self.cues))+"\n"
        (self.out/"captions.srt").write_text(srt,encoding="utf-8")
        times=[(c["start"]+c["end"])/2 for c in self.cues]
        # Include both outgoing and return legs of the DNS queries.
        if self.slug=="dns":times+= [self.s[5]+.7,self.s[6]+2.8,self.s[8]+3.8]
        times=sorted(times)
        sheet=Image.new("RGB",(1280,math.ceil(len(times)/2)*390),"#ede8dc")
        for i,t in enumerate(times):
            frame=self.render(t)
            frame.save(self.out/f"frame-{t:05.1f}.jpg",quality=91)
            x,y=(i%2)*640,(i//2)*390
            sheet.paste(frame.resize((640,360),Image.Resampling.LANCZOS),(x,y))
            txt(sheet,(x+16,y+363),f"{t:.1f} s",18,INK)
        sheet.save(self.out/"contact-sheet.jpg",quality=88)
        cover=self.s[7]+1.9 if self.slug=="task-training" else self.s[7]+1.4
        self.render(cover).resize((1280,720),Image.Resampling.LANCZOS).save(self.assets/"cover.jpg",quality=90)
        print(f"{self.slug}: {len(times)} evidence frames saved",flush=True)

    def encode(self):
        path=self.out/"demo.mp4"
        cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","pipe:0",
             "-i",str(self.assets/"narration.mp3"),"-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p","-threads","3",
             "-af","apad","-t",str(self.duration),"-c:a","aac","-b:a","192k","-movflags","+faststart",str(path)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for frame in range(round(self.duration*FPS)):
                proc.stdin.write(self.render(frame/FPS).tobytes())
                if frame%(FPS*10)==0:print(f"{self.slug}: {frame/FPS:.0f}/{self.duration:.1f}s",flush=True)
        finally:proc.stdin.close()
        assert proc.wait()==0,"Video encoding failed"
        print(f"Saved {path}",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("episode",choices=["dns","task-training"])
    p.add_argument("--frames-only",action="store_true")
    args=p.parse_args()
    ep=Episode(args.episode)
    ep.evidence()
    if not args.frames_only:ep.encode()
