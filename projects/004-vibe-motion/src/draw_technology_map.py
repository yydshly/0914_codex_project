"""Draw a source-grounded technical diagram as a high-resolution PNG and editable SVG."""
from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
W,H,S=2400,2520,1.5
BG='#f4f7fb'; INK='#142238'; MUTED='#52647b'; LINE='#d5dfec'
BLUE='#275ed6'; TEAL='#087e88'; PURPLE='#7749bd'; AMBER='#a46a0b'
im=Image.new('RGB',(int(W*S),int(H*S)),BG);d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>Vibe Motion 技术能力、效果与实现原理</title><desc>二维React与Remotion；三维Three.js和WebGL；动效技能调用Remotion、GSAP、p5.js等；SRT经过模型分镜、代码生成、HyperFrames渲染与FFmpeg拼接。</desc><rect width="{W}" height="{H}" fill="{BG}"/>']
fonts={}
def font(size,bold=False):
    key=size,bold
    if key not in fonts:fonts[key]=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',round(size*S))
    return fonts[key]
def width(s,size=30,bold=False):return d.textlength(s,font=font(size,bold))/S
def text(x,y,s,size=30,color=INK,bold=False):
    assert x>=0 and y>=0 and x+width(s,size,bold)<W-35 and y+size<H-20,(x,y,s)
    d.text((x*S,y*S),s,font=font(size,bold),fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" dominant-baseline="text-before-edge" fill="{color}">{escape(s)}</text>')
def para(x,y,s,w,size=30,color=MUTED,line=46,bold=False):
    for src in s.split('\n'):
        current=''
        for ch in src:
            if current and width(current+ch,size,bold)>w:
                text(x,y,current,size,color,bold);y+=line;current=ch
            else:current+=ch
        if current:text(x,y,current,size,color,bold)
        y+=line
    return y
def rect(x,y,w,h,fill='white',stroke=LINE,r=16):
    d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),radius=r*S,fill=fill,outline=stroke,width=round(2*S))
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def line(x1,y1,x2,y2,color=LINE,weight=2):
    d.line((x1*S,y1*S,x2*S,y2*S),fill=color,width=round(weight*S))
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{weight}"/>')
def arrow(x1,y1,x2,y2,color=BLUE):
    line(x1,y1,x2,y2,color,4)
    a=math.atan2(y2-y1,x2-x1);p=[(x2,y2),(x2-14*math.cos(a-.5),y2-14*math.sin(a-.5)),(x2-14*math.cos(a+.5),y2-14*math.sin(a+.5))]
    d.polygon([(x*S,y*S) for x,y in p],fill=color)
    svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{color}"/>')

text(75,42,'VIBE MOTION  /  PROJECT 004 · 技术总览',26,BLUE,True)
text(75,99,'代码如何变成动画与视频',68,INK,True)
text(75,197,'二维 / 三维是画面维度；动效 Skills 是复用方式；SRT 是内容与时间输入。它们可以组合。',32,MUTED)

for x,k,t,b in [(75,'输入','需求与素材','文字、图片、数据、风格、时长'),(855,'创作','AI 或开发者编写代码','定义对象、构图、运动和时间轴'),(1635,'交付','运行、渲染与编码','得到交互网页、帧序列或视频')]:
    rect(x,268,690,157,'#ffffff')
    text(x+25,286,k,24,BLUE,True);text(x+25,323,t,35,INK,True);text(x+25,377,b,27,MUTED)
arrow(781,345,835,345);arrow(1561,345,1615,345)

text(95,479,'能力入口',27,MUTED,True);text(470,479,'技术与实现原理',27,MUTED,True)
text(1350,479,'能做出什么效果',27,MUTED,True);text(1850,479,'输出与本次验证',27,MUTED,True)

def row(y,num,title,subtitle,repo,color,tech,steps,effects,output,proof):
    rect(75,y,2250,330)
    rect(75,y,337,330,{'01':'#edf3ff','02':'#eaf8f7','03':'#f4effb'}[num],LINE)
    text(101,y+28,num,29,color,True);text(101,y+77,title,43,INK,True)
    para(101,y+142,subtitle,285,28,color,43)
    para(101,y+242,repo,285,23,MUTED,34)
    line(1305,y+28,1305,y+302);line(1808,y+28,1808,y+302)
    text(450,y+32,tech,36,color,True)
    end=para(450,y+98,steps,810,30,MUTED,47);assert end<=y+321
    end=para(1345,y+35,effects,418,31,INK,50);assert end<y+260
    text(1345,y+265,'效果由场景代码与素材决定',24,MUTED)
    end=para(1848,y+36,output,433,31,INK,48);assert end<y+205
    rect(1843,y+214,447,87,'#f3f6fa',LINE,9)
    para(1860,y+229,proof,408,24,MUTED,34)

row(531,'01','二维动画','平面元素 + 时间轴','create-vibe-motion',BLUE,
    'React + Remotion',
    'React / HTML / CSS / SVG 描述画面。\nRemotion 提供帧号、时间轴和视频制作能力。\n代码按帧计算位置、角度、缩放和透明度。\n浏览器绘制每帧，再编码为视频。',
    '文字与卡片运动\n图表、进度条、字幕\n二维转场与讲解画面',
    '可编辑工程\nMP4 / 按配置导出\n可管理成品音频',
    '已实测：5 秒卡片视频\n150 帧，30fps，无音轨')
row(884,'02','三维动画','空间物体 + 灯光相机','create-vibe-motion-3d',TEAL,
    'Three.js → WebGL',
    'Three.js 描述几何、材质、灯光和相机。\nWebGL 是此场景使用的底层图形接口。\n按帧计算物体与相机状态，浏览器绘制。\nPuppeteer 抓帧；FFmpeg 可再编码为视频。',
    '旋转物体与镜头移动\n地球航线、三维粒子\n空间层次与光影',
    '交互三维场景\n原生 PNG / ZIP 帧序列\n额外编码 → MP4',
    '已实测：3 秒三维样片\n90 帧，同帧重复导出一致')
row(1237,'03','动效技能','制作方法 + 模板脚本','vibe-motion/skills',PURPLE,
    '按效果选择技术，可跨二维与三维',
    'Remotion：按视频帧组织组件与动效。\nGSAP：控制属性随时间变化，本身不负责绘图。\nSVG / DOM / Canvas / WebGL：呈现画面。\np5.js：封装绘图，可配合物理模拟。',
    '聚光灯：SVG + GSAP\n线帘：p5.js + 物理模拟\n也有照片墙、Logo、K线',
    '按技能分别交付\nHTML / SVG / 视频等\n不是统一的视频引擎',
    '已运行：聚光灯、线帘\n共 15 项技能，非全部实测')

text(75,1625,'04',34,AMBER,True);text(152,1623,'SRT 自动成片：让模型决定“这句话怎样演”',40,INK,True)
text(75,1687,'SRT 提供文案与时间戳；语义分镜、视觉方案和代码实现依赖模型判断。',30,MUTED)
boxes=[
    ('SRT 字幕','说什么 / 何时说','已有时间轴的文案\n字幕空白也要保留'),
    ('调度模型','理解语义、拆镜头','Codex 依据任务说明\n分配镜头文案与时长'),
    ('Claude Code','设计效果、编写代码','按镜头逐个执行\n生成 HTML 动画工程'),
    ('HyperFrames','渲染每个镜头','执行动画代码\n输出单镜头 MP4'),
    ('FFmpeg','按顺序拼接','镜头视频 → final.mp4\n当前默认静音画面')
]
for i,(title,label,body) in enumerate(boxes):
    x=75+i*459
    rect(x,1752,414,228,'#fff9ed','#e8d6b5')
    text(x+22,1775,title,34,AMBER,True)
    text(x+22,1827,label,28,INK,True)
    para(x+22,1877,body,370,27,MUTED,40)
    if i<4:arrow(x+421,1863,x+452,1863,AMBER)

rect(75,2007,2250,102,'#eaf0f8',LINE,12)
text(103,2027,'语义例子',26,BLUE,True)
text(288,2025,'“把信息汇总起来” → 设计散卡片归位 → 编写位置变化代码 → 渲染成镜头',30,INK,True)
text(288,2070,'这是表达方式的示意；同一句话可有不同视觉方案，不是固定关键词套模板。',26,MUTED)

rect(75,2144,2250,197,'#13253c','#13253c',16)
text(104,2170,'代码视频的关键原则',26,'#b9d582',True)
text(104,2214,'画面状态 = f（帧号，参数，素材）',41,'#ffffff',True)
text(104,2281,'同一帧应可独立计算，方便拖动、乱序渲染和局部重渲。实时物理动效未必自动满足这一约定。',28,'#becbdc')
line(1185,2174,1185,2254,'#425267',2)
text(1230,2177,'AI：理解、设计、写代码',30,'#ffffff',True)
text(1230,2223,'引擎：执行、绘制、输出',30,'#ffffff',True)

text(75,2375,'验证边界',25,AMBER,True)
text(245,2375,'完整 auto-motion 尚未实跑；网页 SRT 部分为预先编写的流程示意。配音、音乐和逐字字幕需另行处理。',25,MUTED)
text(75,2426,'来源：github.com/vibe-motion · 四个核心仓库固定版本源码 / 本地实验记录',24,MUTED)
text(75,2465,'研究日期：2026-09-16     /     实现路线按所研究版本整理，并非所有模块必须同时使用。',24,MUTED)

svg.append('</svg>')
(ROOT/'assets/technology-map.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(ROOT/'assets/technology-map.png',optimize=True)
print(f'Created {im.width}x{im.height} PNG and editable SVG')
