"""Draw one exportable Chinese workflow infographic (PNG and SVG)."""
from pathlib import Path
from html import escape
import math
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
W,H=2200,4400
SHIFT=0
model=json.loads((ROOT/'notes/production-model.json').read_text(encoding='utf-8'))
S=1.5
im=Image.new('RGB',(int(W*S),int(H*S)),'#f3f6fb')
d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>Video TalkCraft：完整制作与一致性模型</title><desc>输入、七步制作、输出与词锚示例；三层一致性、八项生产约束、三种正确，以及变更传播与失败回退。已有规范和研究建议分别标明。</desc><rect width="{W}" height="{H}" fill="#f3f6fb"/>']
INK='#17233e'; MUTED='#53647c'; BLUE='#3158d5'; TEAL='#087c79'; LINE='#d5deed'; AMBER='#a56a16'
FONT='C:/Windows/Fonts/msyh.ttc'; BOLD='C:/Windows/Fonts/msyhbd.ttc'
font_cache={}
def font(size,bold=False):
    key=(size,bold)
    if key not in font_cache:font_cache[key]=ImageFont.truetype(BOLD if bold else FONT,round(size*S))
    return font_cache[key]
def measure(s,size=28,bold=False):return d.textlength(s,font=font(size,bold))/S
def text(x,y,s,size=28,color=INK,bold=False):
    y+=SHIFT
    assert x>=0 and y>=0 and x+measure(s,size,bold)<=W-35 and y+size<H-15,(x,y,s)
    d.text((x*S,y*S),s,font=font(size,bold),fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" dominant-baseline="text-before-edge">{escape(s)}</text>')
def para(x,y,s,width,size=28,color=MUTED,line=43,bold=False):
    for source in s.split('\n'):
        row=''
        for ch in source:
            if row and measure(row+ch,size,bold)>width:
                text(x,y,row,size,color,bold);y+=line;row=ch
            else:row+=ch
        if row:text(x,y,row,size,color,bold)
        y+=line
    return y
def rect(x,y,w,h,fill='#ffffff',stroke=LINE,r=20):
    y+=SHIFT
    d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),radius=r*S,fill=fill,outline=stroke,width=round(2*S))
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def line(x1,y1,x2,y2,color=LINE,width=3):
    y1+=SHIFT;y2+=SHIFT
    d.line((x1*S,y1*S,x2*S,y2*S),fill=color,width=round(width*S))
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
def arrow(x1,y1,x2,y2,color=BLUE,width=4):
    line(x1,y1,x2,y2,color,width)
    a=math.atan2(y2-y1,x2-x1); length=14
    p=[(x2,y2+SHIFT),(x2-length*math.cos(a-.48),y2+SHIFT-length*math.sin(a-.48)),(x2-length*math.cos(a+.48),y2+SHIFT-length*math.sin(a+.48))]
    d.polygon([(x*S,y*S) for x,y in p],fill=color)
    svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{color}"/>')
def section(y,num,title,note):
    text(70,y,num,34,BLUE,True);text(140,y,title,36,INK,True)
    text(2130-measure(note,24),y+9,note,24,MUTED)
def card(x,y,w,h,kicker,title,body,color=BLUE,fill='#ffffff'):
    rect(x,y,w,h,fill)
    text(x+28,y+23,kicker,23,color,True)
    text(x+28,y+64,title,33,INK,True)
    end=para(x+28,y+110,body,w-56,27,MUTED,40)
    assert end-40+27<=y+h-12,(title,end-40+27,y+h)

text(70,44,'VIDEO TALKCRAFT  /  完整制作模型 · 修订版 02',25,BLUE,True)
text(70,99,'从一份口播稿，到一条动效视频',65,INK,True)
text(70,193,'你提供内容与声音；AI Agent 按 Skill 规范设计分镜，调用现成组件，再渲染与验收。',30,MUTED)

section(263,'01','我们给它什么？','配音与数字人生成由外部工具完成')
card(70,325,670,270,'必需输入','口播稿 ＋ 对应配音','文稿：要讲什么、每句说什么。\n音频：真人录音或已生成的配音。\n两者内容应一致，声音决定节奏。')
card(765,325,670,270,'按需输入','人物视频 ＋ 视觉素材','出镜讲话：提供口型同步的视频。\n图片、录屏、截图、实拍按镜头准备；\n缺少的素材可在制作阶段采集。')
card(1460,325,670,270,'建议说明','用途、画幅与风格','例如：横屏产品介绍、竖屏科普。\n指定受众、配色、必须呈现的事实。\n也可直接点名想使用的动效卡。')
arrow(1100,610,1100,641)

section(654,'A','贯穿全流程的三层一致性','已有规范与部分机制；不等于自动保证全片质量')
for i,c in enumerate(model['consistency']):
    card(70+i*695,713,670,250,'从全片约束到镜内协调',c['name'],c['short'],TEAL,'#eef8f6')
arrow(1100,977,1100,1008,TEAL)
SHIFT=360
section(666,'02','内部如何处理、选择、划分和组装？','选择依赖 Agent 的设计判断，并非保证最优')
card(70,734,1010,253,'STEP 1 · 先稳定素材','预剪与输入检查','真人录音可先剪口水词、重说和过长停顿；先预览剪辑报告。\n如果人物与声音来自同次录制，用同一剪辑表同步裁切。\n检查人物帧率、画幅、音画时长及素材文件。')
card(1120,734,1010,253,'STEP 2 · 建立共同时间轴','识别 → 文本匹配 → 逐字时间表','默认 FireRed ASR（可换 Whisper）识别带时间的词表。\n与原稿做繁简、数字及拼音匹配；缺失字符在锚点间插值。\n产出每句、每字的起止时间；低匹配覆盖率标记人工听核。')
arrow(1086,860,1114,860)
arrow(1625,1000,1625,1028)
line(575,1013,1625,1013,BLUE,3)
arrow(575,1013,575,1030)

card(70,1045,1010,290,'STEP 3 · 按语义划分','把文案变成 SHOTBOOK 分镜表','按完整信息段落分镜，不机械地“一句一个新元素”。\n每镜明确：表达意图、主视觉、素材、背景／主体／文字层。\n找出数字、转折、结论等语义拍，把动作落点绑定到词锚。\n限制同屏主角数量，避免堆字、遮脸与过快切换。')
card(1120,1045,1010,290,'STEP 4 · 按输入和表达意图选卡','从 108 套配方中挑选合适效果','先看素材类型：人物、视频、图片、截图，还是纯文字。\n再看表达：数字→计数／图表；差异→对比；证据→巡游。\n读适用条件与已知问题，复核全片风格和阅读时间。\n研究建议：先清楚和适配，再追求丰富，不必处处强动效。')
arrow(1086,1190,1114,1190)
arrow(1625,1350,1625,1380)

rect(70,1395,2060,367,'#eaf0ff','#c5d3f1')
text(100,1419,'STEP 5 · 组装成可编辑的视频工程',24,BLUE,True)
text(100,1461,'复制动效源码，改内容、定位置、对时间',35,INK,True)
line(750,1533,750,1718,'#c5d3f1',2);line(1440,1533,1440,1718,'#c5d3f1',2)
text(100,1538,'代码与参数',29,INK,True)
para(100,1586,'复制对应的 Remotion / TSX 组件。\n换数字、文字、图片、颜色和字号；\n保留关键缓动、回弹与运动结构。',610,28,MUTED,43)
text(790,1538,'图层与镜头',29,INK,True)
para(790,1586,'组合素材、人物、字幕、动效和音效。\n安排入场、停留、降权和退场；\n相机缓推拉，转场连接前后镜头。',610,28,MUTED,43)
text(1480,1538,'时间与逐帧计算',29,INK,True)
para(1480,1586,'当前帧 → 时间 → 动画进度 → 画面。\n开始／落定／转场峰值对应词锚；\n先做代表样板镜，再继续其余镜头。',610,28,MUTED,43)
arrow(1100,1778,1100,1806)

card(70,1823,1010,230,'STEP 6 · 生成视频文件','按镜头渲染 ＋ 混入整条音轨','Remotion 把组件逐帧渲染，视频段缓存后拼装。\n修改时重渲受影响镜头及必要邻镜；声音整轨混入。\n核对每段与全片帧数，减少拼接导致的错位。')
card(1120,1823,1010,230,'STEP 7 · 修正后交付','机器检查 ＋ 独立审片','检查词锚偏差、镜尾停留、静止／抖动和音效。\n审看排版、遮挡、叙事，修正问题后重渲对应部分。\n对齐覆盖率不是声学精度，检查通过也不保证美感。')
arrow(1086,1938,1114,1938)
arrow(1100,2069,1100,2098)

section(2120,'03','最后输出什么？','视频成品 ＋ 可编辑工程 ＋ 制作记录')
card(70,2180,670,237,'成片效果','配音驱动的解说视频','MP4：动态字卡、数据图表、素材画面、\n字幕、转场、音效；人物出镜可选。\n横屏或竖屏，以项目设定为准。',TEAL)
card(765,2180,670,237,'可继续修改','工程与动效素材','Remotion 工程、镜头代码及参数。\n可接工作台微调；符合契约才可拆轨。\n工作台还可导出透明背景动效片段。',TEAL)
card(1460,2180,670,237,'可检查与追溯','分镜、时间表与来源','保留 SHOTBOOK、逐字时间、节拍表、\n素材来源及检查／审片记录。\n换口播时，需更新配音和时间表。',TEAL)

rect(70,2450,2060,285,'#17233e','#17233e')
text(100,2475,'贯穿示例｜“用户从一万，增长到了十万。”',34,'#ffffff',True)
text(100,2537,'输入',26,'#9db6f7',True)
para(100,2580,'稿件 ＋ 对应配音\n假设“十万”从 3.2s 开始',530,27,'#dce5f8',43)
arrow(670,2601,717,2601,'#9db6f7')
text(750,2537,'选择与组装',26,'#9db6f7',True)
para(750,2580,'选数字滚动卡，设置目标十万\n2.2s 开始计数 → 3.2s 落定',620,27,'#dce5f8',43)
arrow(1410,2601,1457,2601,'#9db6f7')
text(1490,2537,'观众看到',26,'#9db6f7',True)
para(1490,2580,'说到“十万”时数字到位并强调\n字幕同步，随后停留让人读清',570,27,'#dce5f8',43)
text(100,2682,'时间为机制示意；真正制作必须读取你的配音时间，不能照抄这组秒数。',23,'#a8badc')

SHIFT=0
section(3135,'B','还需核对的八个方面','标注为建议／整理／评估的部分，不是新实现的自动能力')
for i,c in enumerate(model['criteria']):
    x=70+(i%4)*525;y=3200+(i//4)*215
    rect(x,y,485,195)
    text(x+24,y+18,c['kind'],20,AMBER,True)
    text(x+24,y+53,f"{i+1:02d}  {c['name']}",28,INK,True)
    end=para(x+24,y+103,c['short'],437,24,MUTED,36)
    assert end-36+24<=y+184,(c['name'],end)

rect(70,3655,2060,192,'#edf2fc','#c5d3f1')
text(100,3675,'三种正确不等价：技术通过 ≠ 表达准确 ≠ 观众理解',31,BLUE,True)
for i,c in enumerate(model['correctness']):
    x=100+i*680
    text(x,3733,c['name'],28,INK,True)
    para(x,3776,c['boundary'],610,26,MUTED,38)
section(3890,'C','修改与失败：回到根因，再更新受影响产物','研究整理｜结合已有缓存与返修规范，非完备依赖追踪')
for i,(title,body) in enumerate([
    ('改内容或素材','静态文字改动 → 布局／语义复核。\n换人物或截图 → 重量测口型与坐标。\n必要时覆盖转场邻镜，再渲染复核。'),
    ('换配音或全局设定','换配音／预剪 → 重新对齐与定时。\n改主题／画幅 → 全部受影响场景。\n旧缓存、旧验收不能直接沿用。'),
    ('按失败类型回退','错位回对齐；拥挤回分镜与布局。\n素材缺失回采集；运行报错修实现。\n事实或叙事错误回稿件与全片设计。')]):
    card(70+i*695,3950,670,255,'影响范围决定返工范围',title,body,TEAL)
text(70,4240,'完整闭环：目标与约束 → 制作过程 → 过程产物 → 反馈返工 → 局部、跨镜与全片复核',31,INK,True)
text(70,4300,'依据：固定版本 8829ca31 · SKILL.md / review-protocol.md / 时间与渲染脚本 · 研究建议已作区分',23,MUTED)
text(70,4340,'验证边界：仅做过10项机制实验与单组件渲染，尚未验证完整多镜头口播片。成本、素材权利及交付仍需核对。',23,MUTED)

svg.append('</svg>')
out=ROOT/'assets'
out.mkdir(exist_ok=True)
im.save(out/'video-talkcraft-workflow.png',optimize=True)
(out/'video-talkcraft-workflow.svg').write_text('\n'.join(svg),encoding='utf-8')
public=ROOT/'web/dist/assets'
public.mkdir(parents=True,exist_ok=True)
for ext in ['png','svg']:
    shutil.copyfile(out/f'video-talkcraft-workflow.{ext}',public/f'video-talkcraft-workflow.{ext}')
print(f'Saved {im.width}×{im.height} PNG and scalable SVG.')
