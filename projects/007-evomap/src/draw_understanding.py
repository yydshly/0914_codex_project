"""Render one editable SVG and matching PNG from shared diagram primitives."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 1800, 1760
BG, INK, MUTED = '#f4f7fc', '#172840', '#52647d'
BLUE, LINE, WHITE = '#2855db', '#d5dfed', '#ffffff'
FONT_DIR = Path('C:/Windows/Fonts')
image = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(image)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">AI 技能与经验沉淀：值得参考的产品方向</title>',
       '<desc id="desc">任务触发检索，AI 使用技能执行，验证结果后把经验回写本地经验库。由个人复用扩展到团队共享，再探索群体智能；收益仍需要对照验证。</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

def box(x, y, w, h, fill=WHITE, stroke=LINE, radius=18):
    draw.rounded_rectangle((x, y, x+w, y+h), radius, fill, stroke, 2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x, y, value, size=28, color=INK, bold=False):
    font = ImageFont.truetype(str(FONT_DIR / ('msyhbd.ttc' if bold else 'msyh.ttc')), size)
    width = draw.textlength(value, font=font)
    if x + width > W - 40:
        raise ValueError(f'Text exceeds canvas: {value}')
    draw.text((x, y), value, font=font, fill=color, anchor='lt')
    svg.append(f'<text x="{x}" y="{y+size*.88}" font-family="Microsoft YaHei, PingFang SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')

def arrow(points, color=BLUE, width=4):
    draw.line(points, fill=color, width=width, joint='curve')
    x,y = points[-1]; px,py=points[-2]
    if x == px:
        direction = 1 if y > py else -1
        head = [(x,y),(x-9,y-15*direction),(x+9,y-15*direction)]
    else:
        direction = 1 if x > px else -1
        head = [(x,y),(x-15*direction,y-9),(x-15*direction,y+9)]
    draw.polygon(head,fill=color)
    coords=' '.join(f'{a},{b}' for a,b in points)
    headcoords=' '.join(f'{a},{b}' for a,b in head)
    svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/><polygon points="{headcoords}" fill="{color}"/>')

text(64, 45, 'EVOMAP / EVOLVER    ·    我们的理解', 24, BLUE, True)
text(64, 100, '让 AI 的做事经验，成为可复用的能力资产', 51, INK, True)
text(64, 178, '群体智能愿景：探索类似 RAG 的经验检索与沉淀，让多个 Agent 复用。', 30, MUTED)
box(64, 250, 1672, 82, '#e7eefc', '#e7eefc', 12)
text(91, 273, '有参考价值：可以先从“技能 + 本地经验库”做起，再验证是否值得扩展。', 31, BLUE, True)

box(64, 370, 810, 150)
text(90, 395, '多 Agent：组织这一次的能力协作', 30, INK, True)
text(90, 448, '谁分析、谁执行、谁审查，怎样合并结果。', 27, MUTED)
box(904, 370, 832, 150)
text(930, 395, '经验沉淀：让下一次有方法可借鉴', 30, BLUE, True)
text(930, 448, '留下做法、条件、成败与验证依据。', 27, MUTED)

text(64, 563, '01   一次任务怎样变成可复用经验', 29, INK, True)
xs = [64,410,756,1102,1448]
steps = [
    ('提出任务','需求、错误、环境','明确这次要做什么'),
    ('检索与匹配','找技能和相关案例','判断适用条件'),
    ('AI + 工具执行','读取方法、调用工具','在当前项目中做事'),
    ('验证结果','检查是否满足要求','用实际结果判断'),
    ('沉淀反馈','记录成功与失败','更新经验和版本'),
]
for i,(title,line1,line2) in enumerate(steps):
    x=xs[i]
    box(x,619,280,158,'#ffffff',BLUE if i in (1,4) else LINE,14)
    text(x+20,641,title,30,BLUE if i in (1,4) else INK,True)
    text(x+20,694,line1,24,MUTED)
    text(x+20,733,line2,23,MUTED)
    if i<4: arrow([(x+286,698),(xs[i+1]-12,698)])

arrow([(550,865),(550,792)])
text(580,805,'读取可用经验',24,BLUE)
arrow([(1588,788),(1588,854)])
text(1250,805,'回写结果与适用边界',24,BLUE)

box(64,870,1672,280,WHITE,BLUE,18)
text(92,894,'本地技能与经验库',32,BLUE,True)
text(454,900,'文件、JSON / JSONL 或数据库都可以；数据库主要负责保存和查找。',25,MUTED)
columns=[
    (92,'技能与方法','操作说明、脚本、工具入口','Gene：可复用的策略'),
    (650,'使用条件与版本','什么时候适用、依赖什么环境','让检索结果更容易判断'),
    (1200,'案例、成败与验证','执行结果、失败原因、验收记录','Capsule 与事件：案例和过程'),
]
for x,title,line1,line2 in columns:
    text(x,967,title,29,INK,True)
    text(x,1022,line1,25,MUTED)
    text(x,1070,line2,24,MUTED)

text(64,1203,'02   从一个可落地的产品起点，逐步扩展',29,INK,True)
for x,num,title,body in [
    (64,'A','个人技能经验库','让自己的 AI 少重复摸索'),
    (644,'B','团队与跨 Agent 共享','让不同执行者复用经验'),
    (1224,'C','探索群体智能','验证协作能否提高整体能力'),
]:
    box(x,1257,512,142,'#edf2fc','#edf2fc',14)
    text(x+22,1279,num,30,BLUE,True)
    text(x+70,1279,title,29,INK,True)
    text(x+22,1339,body,26,MUTED)
arrow([(588,1328),(631,1328)])
arrow([(1168,1328),(1211,1328)])

box(64,1451,1672,218,'#142852','#142852',18)
text(92,1478,'参考的是这套产品思路；实际收益还要用任务证明。',34,WHITE,True)
text(92,1541,'值得借鉴：可检索的方法、适用条件、执行记录，以及持续更新的反馈。',27,'#d0ddf5')
text(92,1592,'验证价值：相同模型与任务下，成功率是否提高，总成本与人工干预是否减少？',27,'#d0ddf5')
text(64,1700,'研究归纳 · 本地落地路线为我们的产品化建议，非官方部署架构；群体超级智能仍是愿景。',23,MUTED)

OUT.mkdir(exist_ok=True)
svg.append('</svg>')
(OUT/'product-understanding.svg').write_text('\n'.join(svg),encoding='utf-8')
image.save(OUT/'product-understanding.png', optimize=True)
print(f'Saved diagram: {W} x {H}')
