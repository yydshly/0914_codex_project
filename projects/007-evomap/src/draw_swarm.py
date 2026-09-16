"""Draw the original swarm explainer as matching editable SVG and PNG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'assets'
W, H = 1800, 2220
BG, INK, MUTED, BLUE, GREEN = '#f4f7fc', '#172840', '#52647d', '#2855db', '#176b5a'
image = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(image)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">蜂群：按需组织 Agent，让经验跨任务复用</title>',
       '<desc id="desc">蜂群属于多 Agent 协作。按能力组队，提供技能经验，执行后审查、返工或汇总交付，并记录结果。角色、能力、经验分别表示负责什么、能做什么、如何做得更好。本图为概念归纳，未验证 EvoMap 云端蜂群效果。</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

def box(x, y, w, h, fill='#ffffff', stroke='#d5dfed'):
    draw.rounded_rectangle((x, y, x+w, y+h), 18, fill, stroke, 2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x, y, value, size=28, color=INK, bold=False, max_width=None):
    font = ImageFont.truetype('C:/Windows/Fonts/'+('msyhbd.ttc' if bold else 'msyh.ttc'), size)
    width = draw.textlength(value, font=font)
    if width > (max_width if max_width is not None else W-40-x):
        raise ValueError('Text exceeds allotted width: '+value)
    draw.text((x, y), value, font=font, fill=color, anchor='lt')
    svg.append(f'<text x="{x}" y="{y+size*.88}" font-family="Microsoft YaHei, PingFang SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')

def arrow(points, color=BLUE):
    draw.line(points, fill=color, width=4, joint='curve')
    x,y=points[-1]; px,py=points[-2]
    if x==px:
        d=1 if y>py else -1
        head=[(x,y),(x-9,y-15*d),(x+9,y-15*d)]
    else:
        d=1 if x>px else -1
        head=[(x,y),(x-15*d,y-9),(x-15*d,y+9)]
    draw.polygon(head,fill=color)
    coords=' '.join(f'{a},{b}' for a,b in points)
    heads=' '.join(f'{a},{b}' for a,b in head)
    svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/><polygon points="{heads}" fill="{color}"/>')

text(64,42,'EVOMAP · SWARM    /    蜂群理解图',24,BLUE,True)
text(64,98,'按需组织 Agent，让经验跨任务复用',52,INK,True)
text(64,180,'蜂群属于多 Agent 协作，强调围绕目标组队、协调、审查与迭代。',29,MUTED)

for x,title,line1,line2 in [
    (64,'能力：能做什么','模型、工具、运行环境与权限','会读部署说明，不等于能访问服务器'),
    (632,'角色：这次负责什么','协调、执行、审查、汇总','岗位随任务变化，不必永久固定'),
    (1200,'经验：如何做得更好','技能方法、适用条件与历史案例','按需检索，并在当前环境重新验证')]:
    box(x,257,536,170)
    text(x+24,280,title,31,BLUE,True,max_width=488)
    text(x+24,337,line1,25,MUTED,max_width=488)
    text(x+24,379,line2,23,MUTED,max_width=488)

text(64,474,'01   “按需赋能”要拆成两个动作',29,INK,True)
box(64,529,810,170)
text(90,552,'按能力选 Agent',31,BLUE,True)
text(90,608,'从可用参与者中找适合当前任务的执行者。',27,MUTED)
text(90,653,'可以由平台派单，也可以由 Agent 认领。',25,MUTED)
box(904,529,832,170,'#eaf5f1','#c7dfd5')
text(930,552,'按需提供技能与经验',31,GREEN,True)
text(930,608,'补充方法、案例、约束和任务上下文。',27,MUTED)
text(930,653,'仍需具备执行工具与权限，并验证是否适用。',25,MUTED)

text(64,745,'02   一次任务：组队 → 执行 → 审查 → 交付',29,INK,True)
xs=[64,410,756,1102,1448]
steps=[('提出目标','明确要交付什么','定义验收标准'),('规划与组队','拆分任务、匹配能力','分配这次的角色'),('Agent 执行','分工、探索或接力','用工具完成工作'),('检查与审查','核对证据与结果','判断是否要返工'),('汇总与交付','整合通过的结果','接受最终验收')]
for i,(title,a,b) in enumerate(steps):
    x=xs[i]; box(x,811,280,165)
    text(x+20,834,title,29,BLUE,True,max_width=240)
    text(x+20,888,a,23,MUTED,max_width=240)
    text(x+20,931,b,23,MUTED,max_width=240)
    if i<4: arrow([(x+289,891),(xs[i+1]-12,891)])
arrow([(1242,986),(1242,1030),(896,1030),(896,986)])
text(965,1048,'未通过：修改后重验',24,BLUE)
arrow([(550,1158),(550,991)],GREEN)
text(235,1070,'检索适用的方法与案例',24,GREEN)
arrow([(1588,987),(1588,1158)],GREEN)
text(1285,1100,'记录成败与适用条件',24,GREEN)

box(64,1170,1672,210,'#eaf5f1','#a8cfbe')
text(92,1195,'共享技能与经验库',33,GREEN,True)
text(92,1255,'留下方法、使用条件、执行案例、失败原因与验证记录。',28,MUTED)
text(92,1311,'本次团队可以借鉴过去；本次结果也可以供下次任务、其他 Agent 复用。',28,MUTED)

text(64,1430,'03   “蜂后 / 工蜂”是岗位比喻，不是固定身份',29,INK,True)
for x,title,body in [(64,'协调者','拆任务、组织参与者'),(494,'执行者','研究、编程、测试'),(924,'审查者','核对结果、要求返工'),(1354,'汇总者','整合产物、形成交付')]:
    box(x,1487,382,132)
    text(x+22,1509,title,30,INK,True,max_width=338)
    text(x+22,1565,body,25,MUTED,max_width=338)

text(64,1665,'04   不只沉淀工种技能，也积累流程与组织反馈',29,INK,True)
for x,title,a,b in [
    (64,'方法沉淀','怎样做事：策略与执行案例','跨角色复用，仍需验证适用性'),
    (632,'流程沉淀','怎样接力：可复用流程模板','留下步骤、角色和交接约定'),
    (1200,'组织反馈','怎样组队：协同与编排记录','为后续选人和选流程提供依据')]:
    box(x,1720,536,170,'#eaf5f1','#c7dfd5')
    text(x+24,1744,title,31,GREEN,True,max_width=488)
    text(x+24,1800,a,25,MUTED,max_width=488)
    text(x+24,1846,b,24,MUTED,max_width=488)
box(64,1945,1672,172,'#142852','#142852')
text(92,1970,'协作组织当下的工作；经验沉淀连接前后多次任务。',33,'#ffffff',True)
text(92,2028,'平台还描述：任务通信、超时候补、预算并发控制，以及贡献结算。',26,'#d0ddf5')
text(92,2072,'上述为平台文档与概念归纳；不等于本地库独立具备全部能力，云端收益尚未实测。',25,'#d0ddf5')
text(64,2160,'独立研究概念图 · 依据官方 Swarm 文档与我们的理解归纳，并非官方部署架构。',23,MUTED)
OUT.mkdir(exist_ok=True)
svg.append('</svg>')
(OUT/'swarm-understanding.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
image.save(OUT/'swarm-understanding.png',optimize=True)
print(f'Saved swarm diagram: {W} x {H}')
