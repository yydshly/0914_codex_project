"""Beginner English micro-lesson with spatial animation, sentence cards and pauses."""
from functools import lru_cache
import json
import math
import re
from PIL import Image,ImageDraw
from series_render import Episode,ROOT,INK,MUTED,BLUE,GREEN,CORAL,GOLD,label
from render import font,txt,box,place,ease,lerp,card

def ball_image():
    im=Image.new("RGBA",(106,106))
    d=ImageDraw.Draw(im)
    d.ellipse((6,9,100,103),fill=(107,67,23,32))
    d.ellipse((4,2,98,96),fill="#df8547",outline="#b56637",width=3)
    d.arc((13,10,89,88),205,330,fill="#f3b875",width=4)
    d.ellipse((25,18,40,29),fill="#f9d29b")
    return im

BALL=ball_image()

class EnglishEpisode(Episode):
    def __init__(self):
        self.slug="english"
        self.root=ROOT/"demos/english"
        self.assets=self.root/"assets"
        self.out=self.root/"output"
        self.out.mkdir(exist_ok=True)
        self.meta=json.loads((self.assets/"voice-metadata.json").read_text(encoding="utf-8"))
        raw=json.loads((self.assets/"provider-subtitles.json").read_text(encoding="utf-8"))
        normalize=lambda x:re.sub(r"[^\w]","",x).lower()
        assert len(raw)==len(self.meta["transcript"])==23
        assert all(normalize(x["text"])==normalize(y) for x,y in zip(raw,self.meta["transcript"]))
        self.cues=[{"id":i,"start":c["time_begin"]/1000,"end":c["time_end"]/1000,"text":c["text"],"caption":c["text"].rstrip("。") } for i,c in enumerate(raw)]
        self.s=[c["start"] for c in self.cues]
        self.duration=math.ceil((self.meta["duration"]+1.5)*24)/24
        self.title="Where is the ball?"
        self.table=Image.open(self.assets/"table.png").convert("RGBA").resize((500,500),Image.Resampling.LANCZOS)
        self.container=Image.open(self.assets/"box.png").convert("RGBA").resize((440,293),Image.Resampling.LANCZOS)
        self.bg=self.background()

    def background(self):
        im=Image.new("RGBA",(1920,1080),"#f1e9d9")
        d=ImageDraw.Draw(im)
        for y in range(0,1080,5):
            for x in range((y%7)*3,1920,21):d.point((x,y),fill="#e5dcca")
        txt(im,(80,55),"PAPER CLASSROOM / 英语微课堂",24,GREEN,True)
        txt(im,(80,106),"Where is the ball?",72,INK,True)
        txt(im,(84,210),"位置介词 · in / on / under · 看懂、跟读、自己说",29,MUTED)
        label(im,1550,61,285,"04 · 英语启蒙",GREEN,"#e1eadb",26)
        box(im,(65,278,1855,875),"#fcfaf2",22,"#d6d3c4",2)
        box(im,(65,916,1855,1018),INK,18)
        txt(im,(80,1035),"AUDIO-LOCKED PAPER THEATRE",17,MUTED)
        txt(im,(1835,1035),"MiniMax 中英配音 · 含跟读停顿",17,MUTED,anchor="ra")
        return im

    def position(self,t):
        n=self.phase(t)
        if n<3:return "intro"
        if n<7:return "in"
        if n<11:return "on"
        if n<17:return "under"
        if n<19:return "on"
        if n<21:return "in"
        if n==21:return ["in","on","under"][min(2,int((t-self.s[21])/(self.cues[21]["end"]-self.s[21])*3))]
        return "under"

    def draw_scene(self,im,t):
        n=self.phase(t);s=self.s
        positions={"intro":(570,557),"in":(330,604),"on":(795,482),"under":(795,688)}
        key=self.position(t)
        x,y=positions[key]
        transitions={3:"intro",7:"in",11:"on",17:"under",19:"on"}
        alpha=ease((t-s[3])/.6) if n>=3 else 0
        if alpha:
            ImageDraw.Draw(im).line((149,731,1032,731),fill="#e2dac7",width=3)
            place(im,self.table,545,342,alpha)
            place(im,self.container,110,488,alpha)
            txt(im,(331,830),"box / 盒子",25,BLUE,True,"mm")
            txt(im,(795,830),"table / 桌子",25,GOLD,True,"mm")
        if n in transitions:
            q=ease((t-s[n])/.8)
            old=positions[transitions[n]]
            x,y=lerp(old[0],x,q),lerp(old[1],y,q)-math.sin(q*math.pi)*90
        # The ball is one independent layer. The box front is a physical occluder.
        place(im,BALL,x-53,y-53)
        if key=="in" and n>=3:
            foreground=self.container.copy()
            foreground.paste((0,0,0,0),(0,0,440,127))
            place(im,foreground,110,488,alpha)
        if n<3:
            txt(im,(570,659),"ball / 球",34,CORAL,True,"mm")
        return key

    def render(self,t):
        im=self.bg.copy();n=self.phase(t);s=self.s
        txt(im,(105,306),"01  看位置、跟着读" if n<15 else "02  拼出句子" if n<17 else "03  看图说英语",25,GREEN,True)
        key=self.draw_scene(im,t)
        colors={"in":BLUE,"on":GOLD,"under":GREEN,"intro":CORAL}
        is_question=n in [17,19]
        right=card(681,413)
        if n<3:
            txt(right,(340,99),"in · on · under",53,GREEN,True,"mm")
            txt(right,(340,176),"三个词，说清楚位置",32,INK,True,"mm")
            txt(right,(340,278),"看图 → 听例句 → 跟读 → 作答",24,MUTED,anchor="mm")
        else:
            word="Your turn" if is_question else key
            meaning="看图回答，先不要看答案" if is_question else {"in":"在……里面 / inside","on":"在……表面上 / on the surface","under":"在……下面 / below"}[key]
            txt(right,(340,89),word,62 if is_question else 80,colors[key],True,"mm")
            txt(right,(340,163),meaning,26,INK,anchor="mm")
            parts=["The ball is", "___" if is_question else key,"the box." if key=="in" else "the table."]
            xs=[25,278,432];widths=[237,138,222]
            for i,(text,x,w) in enumerate(zip(parts,xs,widths)):
                q=ease((t-s[15]-i*.38)/.5) if n==15 else 1
                yy=228+round(35*(1-q))
                box(right,(x,yy,x+w,yy+76),["#eceade","#e0ecdf","#eceade"][i],8)
                txt(right,(x+w/2,yy+38),text,31 if i!=1 else 34,colors[key] if i==1 else INK,True,"mm")
                txt(right,(x+w/2,344),["物体 + is","位置","参照物"][i],21,MUTED,anchor="mm")
            if is_question:txt(right,(340,391),"可以暂停，完整说出句子",21,CORAL,True,"mm")
        place(im,right,1084,371)
        # Provider-generated silent pauses are part of the locked voice master.
        active=next((c for c in self.cues if c["start"]<=t<=c["end"]),None)
        paused_repeat=n in [6,10,14] and t>self.cues[n]["end"]
        paused_question=n in [17,19] and t>self.cues[n]["end"]
        if paused_repeat or paused_question:
            remaining=max(0,s[n+1]-t)
            prompt="Your turn · 请跟读" if paused_repeat else "Think and say · 想一想，说一说"
            label(im,330,355,585,prompt+f"  {math.ceil(remaining)}",GREEN,"#e1eadb",27)
        elif n in [5,6,9,10,13,14]:
            label(im,397,355,435,"Listen and repeat · 听一听，跟着读",GREEN,"#e1eadb",21)
        if n>=21:txt(im,(960,850),"本课只讲物体的位置用法。试着用完整句子描述身边的物体。",22,MUTED,anchor="mm")
        d=ImageDraw.Draw(im)
        d.line((83,898,1837,898),fill="#d9d2c1",width=5)
        d.line((83,898,83+1754*min(1,t/self.duration),898),fill=GREEN,width=5)
        txt(im,(1820,223),f"{int(t):02d} / {round(self.duration):02d} s",22,MUTED,anchor="ra")
        if active:
            text=active["caption"];size=37
            while font(size).getlength(text)>1650:size-=1
        else:text="请跟读刚才的句子" if paused_repeat else "先自己回答，再看答案" if paused_question else "·  ·  ·" if t<self.meta["duration"] else "Look around. Where is it?";size=34
        txt(im,(960,966),text,size,"#fffdf5",anchor="mm")
        return im.convert("RGB")

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument("--frames-only",action="store_true");args=parser.parse_args()
    lesson=EnglishEpisode();lesson.evidence()
    if not args.frames_only:lesson.encode()
