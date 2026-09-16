"""Create an original, example-first README guide as SVG and PNG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'assets'
W,H = 1600,1780
BG,INK,MUTED,BLUE,GREEN = '#f4f7fc','#172840','#52647d','#2855db','#176b5a'
im=Image.new('RGB',(W,H),BG)
d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
 '<title id="title">一眼看懂蜂群：几个 AI 一起做完一个网站</title>',
 '<desc id="desc">目标交给协调者，按能力分工。设计、编程、测试按依赖交接，失败返工，掉线改派，预算限制资源。通过验收后交付，把方法、流程与协作记录留给下一次。概念示例，尚未实测 EvoMap 云端蜂群收益。</desc>',
 f'<rect width="{W}" height="{H}" fill="{BG}"/>']

def box(x,y,w,h,fill='#fff',stroke='#d5dfed'):
 d.rounded_rectangle((x,y,x+w,y+h),18,fill,stroke,2)
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x,y,s,size=27,color=INK,bold=False,width=None):
 font=ImageFont.truetype('C:/Windows/Fonts/'+('msyhbd.ttc' if bold else 'msyh.ttc'),size)
 if d.textlength(s,font=font)>(width if width else W-45-x): raise ValueError(s)
 d.text((x,y),s,font=font,fill=color,anchor='lt')
 svg.append(f'<text x="{x}" y="{y+size*.88}" font-family="Microsoft YaHei,PingFang SC,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')

def arrow(points,color=BLUE):
 d.line(points,fill=color,width=4,joint='curve')
 x,y=points[-1]; px,py=points[-2]
 if x==px:
  sign=1 if y>py else -1; head=[(x,y),(x-8,y-14*sign),(x+8,y-14*sign)]
 else:
  sign=1 if x>px else -1; head=[(x,y),(x-14*sign,y-8),(x-14*sign,y+8)]
 d.polygon(head,fill=color)
 coords=' '.join(f'{a},{b}' for a,b in points); heads=' '.join(f'{a},{b}' for a,b in head)
 svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="4"/><polygon points="{heads}" fill="{color}"/>')

text(64,40,'EVOMAP / SWARM · 下次从这张图看起',23,BLUE,True)
text(64,95,'蜂群：几个 AI，一起把一件事做完',48,INK,True)
text(64,169,'把它想成一支临时 AI 团队：有人分工，有人做，有人检查，还能留下经验。',27,MUTED)
box(64,238,1472,98,'#142852','#142852')
text(90,265,'你的目标：帮我做一个网站，而且登录功能要能正常使用。',33,'#fff',True)
arrow([(800,346),(800,383)])
box(64,397,1472,112)
text(90,420,'协调者：拆任务、找合适的 AI，约定交付内容和验收方法',31,BLUE,True)
text(90,467,'按需组队＝谁适合、谁有空，就安排谁；角色是本次岗位，不是永久身份。',25,MUTED)
arrow([(800,519),(800,567)])
for x,title,a,b in [
 (64,'设计 AI','画页面、说明布局','交出：页面方案与交互说明'),
 (576,'编程 AI','把页面和登录功能做出来','交出：可运行的网站'),
 (1088,'测试 AI','检查登录是否真的可用','交出：通过结果或问题清单')]:
 box(x,580,448,178)
 text(x+24,604,title,32,BLUE,True,width=400)
 text(x+24,662,a,25,MUTED,width=400)
 text(x+24,710,b,24,MUTED,width=400)
arrow([(522,667),(563,667)])
arrow([(1034,667),(1075,667)])
arrow([(1312,768),(1312,805),(800,805),(800,768)])
text(675,824,'按钮没反应？交回修改，再测一次。',25,BLUE)
text(64,794,'通信＝交接方案、产物和问题',24,MUTED)
text(64,831,'此例按依赖接力；独立工作可以并行。',22,MUTED)
for x,title,a,b in [
 (64,'有人掉线怎么办？','尝试换一个合适的 AI 接手','这叫失败改派'),
 (576,'怎样避免一直做下去？','限制花费、并发和重试次数','这叫预算与运行控制'),
 (1088,'通过验收后交付','你拿到网站和验证结果','这是期望产出，非本研究实测')]:
 box(x,904,448,152,'#eaf5f1' if x==1088 else '#fff','#c7dfd5' if x==1088 else '#d5dfed')
 text(x+24,927,title,28,GREEN if x==1088 else INK,True,width=400)
 text(x+24,980,a,24,MUTED,width=400)
 text(x+24,1021,b,22,MUTED,width=400)
arrow([(1498,768),(1498,892)],GREEN)
arrow([(1312,1066),(1312,1149)],GREEN)
text(64,1101,'任务结束，再把可复用的内容留下来',30,GREEN,True)
box(64,1163,1472,238,'#eaf5f1','#a8cfbe')
text(90,1188,'共享经验：下次先查已有做法，再结合当前任务验证',30,GREEN,True)
for x,title,a,b in [
 (90,'方法：怎么做','登录问题的修复步骤','适用条件与失败记录'),
 (583,'流程：怎么配合','设计 → 编程 → 测试','各步骤要交接什么'),
 (1076,'反馈：怎么组织','哪种配合与安排有用','给下次选人选流程作参考')]:
 text(x,1252,title,28,INK,True,width=432)
 text(x,1302,a,24,MUTED,width=432)
 text(x,1345,b,24,MUTED,width=432)
arrow([(64,1265),(30,1265),(30,451),(53,451)],GREEN)
box(64,1455,1472,195,'#142852','#142852')
text(90,1483,'记住：当下能协作，以后有经验可复用。',36,'#fff',True)
text(90,1544,'能力＝能做什么    ·    角色＝这次负责什么    ·    经验＝怎样做得更好',27,'#d0ddf5')
text(90,1597,'技能说明不会自动带来工具或权限；“工种都有技能”只是其中一部分。',25,'#d0ddf5')
text(64,1691,'本图为机制示例，非运行截图。EvoMap 云端蜂群的效果尚未实测。',25,MUTED)
text(64,1735,'蜂群属于多 Agent 协作；完整平台能力不能等同于 Evolver 本地库。',23,MUTED)
OUT.mkdir(exist_ok=True)
svg.append('</svg>')
(OUT/'swarm-quickstart.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
im.save(OUT/'swarm-quickstart.png',optimize=True)
print(f'Saved swarm quickstart: {W} x {H}')
