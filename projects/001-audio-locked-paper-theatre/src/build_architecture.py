"""Draw the audio-clock / objects / animation-code architecture."""
from pathlib import Path
from html import escape
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
W,H=1600,1760
PAPER='#f5f1e6';INK='#213f39';MUTED='#5b7067';GREEN='#267b69';ORANGE='#aa6631';BORDER='#cfd8ca'
im=Image.new('RGB',(W,H),PAPER);draw=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">音频时间轴怎样驱动画板对象</title><desc id="desc">讲稿和分镜分别驱动语音合成、对象准备与动作编排。真实时间戳提供时间依据。渲染器读取时间、动作规则和独立图层，逐帧绘制画面，再与原始音轨合成视频。</desc><rect width="1600" height="1760" fill="{PAPER}"/>']
def rect(x,y,w,h,fill,stroke=BORDER):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=14,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def text(x,y,value,size=27,color=INK,bold=False,maxw=None):
    font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',size)
    if maxw:assert draw.textlength(value,font=font)<=maxw,(value,maxw)
    draw.text((x,y),value,font=font,fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y+size*.9}" font-size="{size}" font-weight="{700 if bold else 400}" font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif" fill="{color}">{escape(value)}</text>')
def arrow(points,color=GREEN):
    draw.line(points,fill=color,width=4)
    svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="4"/>')
    x,y=points[-1];px,py=points[-2];a=atan2(y-py,x-px)
    pts=[(x,y),(x+14*cos(a+pi*.84),y+14*sin(a+pi*.84)),(x+14*cos(a-pi*.84),y+14*sin(a-pi*.84))]
    draw.polygon(pts,fill=color);svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')
def card(x,y,title,subtitle,lines,fill='#fffdf7',height=180,accent=GREEN):
    rect(x,y,430,height,fill)
    text(x+24,y+22,title,34,accent,True,maxw=384)
    text(x+24,y+76,subtitle,27,INK,True,maxw=384)
    for i,item in enumerate(lines):text(x+24,y+119+i*36,item,25,MUTED,maxw=385)

text(72,47,'PAPER THEATRE / 音频驱动动画架构',25,GREEN,True)
text(72,104,'声音给时间，代码让物品演出',56,INK,True)
text(72,188,'画板是舞台，物品是演员，代码是动作脚本，音频时间轴是演出节拍。',29,MUTED)
for i,(a,b) in enumerate([('画板 / 舞台','场景与空间关系'),('物品 / 演员','可独立控制的图层'),('代码 / 动作脚本','路径、状态与遮挡'),('时间轴 / 演出节拍','统一的时间参数 t')]):
    x=72+370*i;rect(x,253,344,98,'#e5ecdf');text(x+21,269,a,28,GREEN,True);text(x+21,310,b,24,MUTED)
text(72,381,'制作准备：把“演什么”和“何时演”对应起来',30,INK,True)

card(72,441,'讲稿与分镜','确定讲解内容和画面含义',['例：小球进入盒子，表现 in'])
card(577,441,'语音合成','本地使用 MiniMax',['生成真实配音与句级时间戳'])
card(1082,441,'锁定音频结果','音轨文件 + 句子起止时间',['制作端保留最终配音节奏'],fill='#f2e8d9',accent=ORANGE)
arrow([(503,531),(568,531)]);arrow([(1008,531),(1073,531)],ORANGE)

arrow([(287,621),(287,742)]);text(84,664,'准备角色与素材',24,GREEN)
arrow([(397,621),(397,687),(792,687),(792,742)]);text(550,649,'把语义编成动作规则',24,GREEN)
arrow([(1297,621),(1297,742)],ORANGE);text(1323,662,'时间依据',24,ORANGE)
arrow([(1297,705),(962,705),(962,742)],ORANGE);text(914,649,'校准动作时段',24,ORANGE)

card(72,753,'独立对象与场景','舞台 + 演员',['球、盒子、桌子、词卡、字幕','位置、尺寸、图层顺序与遮罩'],height=208)
card(577,753,'动作脚本','代码规定怎样演',['何时开始、持续多久、走哪条路','移动、缩放、显隐、组合与遮挡'],height=208)
card(1082,753,'音频主时间轴','统一时间 t',['时间戳用于安排动作边界','离线导出：t = 帧序号 ÷ 帧率'],fill='#f2e8d9',height=208,accent=ORANGE)

text(72,1022,'逐帧执行',30,INK,True)
arrow([(287,961),(287,1180),(568,1180)]);text(326,1136,'对象与图层',24,GREEN)
arrow([(792,961),(792,1100)]);text(816,1016,'动作规则',24,GREEN)
arrow([(1297,961),(1297,1180),(1016,1180)],ORANGE);text(1093,1136,'当前时间 t',24,ORANGE)
card(577,1111,'逐帧渲染器','状态 = 动作规则（对象，t）',['计算这一刻的位置、大小与透明度','按图层与遮罩绘制当前画面'],fill='#e5ecdf',height=208)
text(591,1348,'本地：Pillow · 1920 × 1080 · 24 fps',23,MUTED)
arrow([(792,1378),(792,1430)]);text(821,1382,'连续画面帧',24,GREEN)

arrow([(1512,531),(1550,531),(1550,1532),(1016,1532)],ORANGE)
text(1101,1454,'固定音轨直接加入合成',25,ORANGE,True)
card(577,1441,'音画合成与验证','FFmpeg → 有声 MP4',['检查同步、对象关系与完整播放'],height=180)
rect(72,1320,430,301,'#fffdf7')
text(97,1346,'小球进入盒子时',30,GREEN,True)
text(97,1398,'时间 t → 算出球的位置',25,maxw=381)
text(97,1441,'图层顺序 → 前壁遮住球',25,maxw=381)
text(97,1484,'同一时间 → 得到同一画面',25,maxw=381)
text(97,1539,'修改配音后，重新安排时间线。',23,MUTED,maxw=381)

text(72,1662,'上游 Skill 提供制作规范、模板和验证工具；本图以本地复现说明各工具如何配合。',25,MUTED)
text(72,1706,'音频提供时间依据，分镜与代码负责语义表达。观众答题、拖拽等交互需另加逻辑。',25,MUTED)
svg.append('</svg>')
(ROOT/'assets/audio-animation-architecture.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(ROOT/'assets/audio-animation-architecture.png')
print('Saved architecture PNG and SVG.')
