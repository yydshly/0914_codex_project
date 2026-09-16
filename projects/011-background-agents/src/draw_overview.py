"""Create a source-grounded Chinese overview as a PNG and editable SVG."""
from pathlib import Path
from html import escape
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 2400, 3320
BG, INK, MUTED = '#f4f6fa', '#182b44', '#53657b'
NAVY, BLUE, TEAL, PURPLE = '#142b47', '#245bce', '#087b79', '#7446aa'
WHITE, LINE, AMBER = '#ffffff', '#d8e0ea', '#945315'
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">Background Agents / Open-Inspect：能力、前后端、代理和模型接入总览</title>',
       '<desc id="desc">网页或集成入口提交任务，管理服务持久化与调度，独立沙箱中由 OpenCode 或 Claude Agent 执行；代理调用外部模型，交付代码、测试与可审核 PR。支持 OpenAI/Codex 模型，但固定研究版本没有原生 Codex CLI 适配。附可复用技术与部署边界。</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc', size)

def box(x,y,w,h,fill=WHITE,stroke=LINE,r=20):
    d.rounded_rectangle((x,y,x+w,y+h), radius=r, fill=fill, outline=stroke, width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x,y,s,size=32,color=INK,bold=False,max_width=None):
    tw=d.textlength(s,font=font(size,bold))
    if x+tw>W-40 or (max_width is not None and tw>max_width):
        raise ValueError(f'Text exceeds allowed width: {s} ({tw})')
    d.text((x,y),s,font=font(size,bold),fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')

def para(x,y,s,width,size=32,color=MUTED,bold=False,leading=None,bottom=None):
    lines=[]
    for p in s.split('\n'):
        line=''
        for char in p:
            if line and d.textlength(line+char,font=font(size,bold))>width:
                lines.append(line); line=char
            else:
                line+=char
        lines.append(line)
    step=leading or round(size*1.55)
    if bottom is not None and y+(len(lines)-1)*step+size>bottom:
        raise ValueError(f'Text exceeds panel: {s}')
    for i,line in enumerate(lines):
        text(x,y+i*step,line,size,color,bold,max_width=width)
    return y+len(lines)*step

def arrow(x1,y1,x2,y2,color=BLUE,width=4):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    a=math.atan2(y2-y1,x2-x1)
    pts=[(x2,y2),(x2-17*math.cos(a-.45),y2-17*math.sin(a-.45)),(x2-17*math.cos(a+.45),y2-17*math.sin(a+.45))]
    d.polygon(pts,fill=color)
    svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"/><polygon points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')

def item(x,y,title,body,width=980,color=BLUE):
    text(x,y,title,34,color,True,max_width=width)
    return para(x,y+52,body,width,30,INK,leading=44,bottom=y+147)

# Identity and central meaning.
box(0,0,W,390,NAVY,NAVY,0)
text(100,43,'BACKGROUND AGENTS  /  OPEN-INSPECT',30,'#aac8f3',True)
text(100,105,'把 AI 编程组织成可派发、可跟踪的后台任务',62,WHITE,True,max_width=2200)
text(103,193,'仓库名：background-agents     系统名：Open-Inspect     交付形态：可自行部署的 Web 应用',30,'#d1deef')
box(100,258,2200,90,'#244463','#244463',14)
text(136,282,'配置代理与模型  →  选择仓库、创建任务  →  后台执行  →  查看结果、审核代码',38,WHITE,True,max_width=2120)

# Entrypoints.
text(100,442,'01  使用入口｜从哪里派任务',42,INK,True)
entries=[
    (100,'网页前端 · Next.js','新建会话、选仓库与模型、输入需求\n看进度、追加要求、查看代码差异',BLUE),
    (850,'协作入口 · 需要配置集成','Slack 私聊 / @机器人；Linear 工单\nGitHub PR 自动审查 / 评论 @机器人',TEAL),
    (1600,'自动化入口 · Automations','定时任务、认证 Webhook\nGitHub 事件、Sentry 告警、Slack 消息',PURPLE),
]
for x,title,body,color in entries:
    box(x,520,700,205)
    text(x+28,548,title,34,color,True,max_width=644)
    para(x+28,610,body,644,29,INK,leading=47,bottom=702)
arrow(790,744,790,798)
arrow(850,798,850,744,TEAL)
text(904,755,'网页 ↔ 后台：HTTP 请求 + WebSocket 实时进度；外部系统通过各自集成接入',28,MUTED)

# Backend.
box(100,820,2200,335,'#eaf1ff','#c6d7f5')
text(137,849,'02  管理服务｜先保存任务，再安排执行',43,BLUE,True)
text(139,916,'身份与凭据管理     会话与任务队列     沙箱创建 / 停止 / 恢复     事件与结果记录',33,INK)
text(139,976,'同一会话的追加要求排队执行；多个独立会话可并行，状态保存在服务端。',32,INK)
box(134,1037,2132,82,WHITE,'#c6d7f5',12)
text(155,1059,'实现：Cloudflare Workers + Durable Objects / SQLite + D1；或 Node 容器 + SQLite + S3 兼容存储',29,BLUE,max_width=2090)
arrow(790,1170,790,1235)
arrow(850,1235,850,1170,TEAL)
text(909,1185,'任务下发 / 执行事件回传（WebSocket）',30,MUTED)

# Execution and model are intentionally different panels.
box(100,1255,1440,630,'#e9f5f1','#bcded3')
text(135,1285,'03  执行环境｜每个会话的独立沙箱',41,TEAL,True)
text(138,1350,'Supervisor：准备环境、管理进程    Bridge：连接后台、转发执行事件',29,INK)
text(138,1406,'代理程序：每个会话选择一种，负责模型与工具之间的执行循环',30,TEAL,True)
box(136,1460,658,156)
text(162,1484,'OpenCode（默认）',37,BLUE,True)
para(162,1535,'启动 opencode serve\n可调用项目目录中的多家模型',602,29,INK,leading=38,bottom=1606)
box(820,1460,680,156)
text(847,1484,'Claude Agent',37,PURPLE,True)
para(847,1535,'Claude Agent SDK 驱动 claude 程序\n仅使用 Anthropic 模型',624,29,INK,leading=38,bottom=1606)
text(139,1648,'代理可以使用的工具能力',34,TEAL,True)
text(142,1710,'读写代码     运行命令 / 测试     Git 操作',34,INK)
text(142,1767,'浏览器操作 / 截图     MCP 扩展     派发子任务',34,INK)
text(142,1830,'沙箱后端：Modal / Daytona / E2B / Vercel / OpenComputer',27,MUTED)

box(1630,1255,670,630,'#f2ecf9','#d9c8e9')
text(1662,1289,'04  模型服务｜提供推理',36,PURPLE,True,max_width=606)
para(1662,1355,'通过 API Key 或项目支持的账号授权连接；模型在外部服务端运行。',606,29,INK,leading=43,bottom=1460)
text(1662,1475,'OpenAI / Codex 模型',32,PURPLE,True)
text(1662,1528,'Anthropic Claude · xAI Grok',30,INK)
text(1662,1581,'OpenCode Zen / Go 渠道',30,INK)
text(1662,1634,'Kimi / MiniMax / Qwen / GLM 等',28,INK)
text(1662,1687,'Z.AI Coding Plan · DeepSeek',29,INK)
box(1660,1753,610,97,WHITE,'#d9c8e9',12)
para(1680,1770,'模型决定下一步；代理程序\n调用工具执行实际操作。',566,29,PURPLE,True,leading=40,bottom=1842)
arrow(1548,1510,1620,1510,PURPLE)
arrow(1620,1570,1548,1570,PURPLE)

# Outputs.
arrow(815,1900,815,1970,TEAL)
text(864,1915,'执行结果回到平台，供网页与集成入口查看',30,MUTED)
box(100,1995,2200,230)
text(137,2024,'05  交付什么｜把“执行了”变成“可以检查”',41,INK,True)
outcomes=[(140,'代码成果','代码差异、分支、待审核 PR',BLUE),
          (895,'验证材料','测试输出、构建结果、按需截图',TEAL),
          (1645,'任务记录','进度、日志、说明与后续会话',PURPLE)]
for x,title,body,color in outcomes:
    text(x,2095,title,33,color,True)
    text(x,2150,body,29,INK)

# Reusable insights and Codex relation.
box(100,2310,1080,550)
text(135,2343,'值得你研究的技术',40,BLUE,True)
item(138,2415,'长任务与网页连接分离','用户离开后仍可处理；回来按任务编号取结果。',980)
item(138,2545,'统一代理接口与工具循环','开始、停止、继续、回传事件，统一对接不同代理。',980)
item(138,2675,'隔离环境与复用','每项工作独立；镜像预构建、文件快照或暂停恢复。',980)
box(1220,2310,1080,550,'#edf2fa','#d3deef')
text(1255,2343,'与当前 Codex 环境的关系',40,INK,True)
item(1258,2415,'能力有重叠：都能让 AI 执行开发任务','本库的价值在于可自行部署、定制和组织团队流程。',980,TEAL)
item(1258,2545,'能用 Codex 模型 ≠ 原生 Codex 程序','该版本通过 OpenCode 接入 OpenAI；代理类型\n只有 opencode / claude，没有原生 Codex CLI 适配。',980,PURPLE)
item(1258,2700,'当前状态：我们在用 Codex 研究它','已保存研究材料；尚未部署或接入当前 Codex。',980,BLUE)

# Deployment and essential limits.
box(100,2930,2200,210,'#fff5e8','#eed9bc')
text(137,2958,'落地要准备什么',35,AMBER,True)
text(139,3016,'网页与管理服务 + 模型凭据 + 沙箱后端 + 仓库权限 + 项目依赖 / 启动脚本',32,INK)
para(139,3070,'边界：面向单租户可信团队；子代理限父会话主仓库、派生深度受限；后台执行不保证任务正确或无限运行。',2110,28,AMBER,bottom=3124)
text(102,3190,'依据：ColeMurray/background-agents · 4c470da615ea · 2026-09-16 · 原创机制归纳，非运行截图；未实测模型与云沙箱。',25,MUTED)
text(102,3240,'详细证据：研究子项目 011 / notes/sources.md；模型目录、harnesses.ts、队列、Bridge、子会话与部署文档。',25,MUTED)

svg.append('</svg>')
OUT.mkdir(parents=True,exist_ok=True)
im.save(OUT/'background-agents-overview.png',optimize=True)
(OUT/'background-agents-overview.svg').write_text('\n'.join(svg),encoding='utf-8')
im.resize((1200,1660),Image.Resampling.LANCZOS).save(OUT/'background-agents-overview-preview.png',optimize=True)
print(f'Created {W}x{H} overview PNG, SVG and preview.')
