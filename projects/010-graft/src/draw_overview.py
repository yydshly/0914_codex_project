"""Render the source-grounded Graft overview to matching PNG and editable SVG."""
from pathlib import Path
from html import escape
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 2600, 3740
BG, INK, MUTED = '#f4f7fc', '#17263f', '#536580'
BLUE, TEAL, PURPLE, AMBER = '#2955d9', '#08736c', '#7752ad', '#9a5a17'
LINE, WHITE, DARK = '#d5dfed', '#ffffff', '#152540'
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">Graft 能力与初步研究全景图：构建原理待研究</title>',
       '<desc id="desc">八项能力；基础结构与可选语义双路径；函数关系解析；任务检索；缓存更新；输出和效果；已验证限制。依据固定版本源码与两个隔离原函数探针。</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc', size)

def box(x,y,w,h,fill=WHITE,stroke=LINE,r=16):
    d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x,y,s,size=28,color=INK,bold=False):
    width=d.textlength(s,font=font(size,bold))
    if x+width>W-35: raise ValueError(f'Text exceeds canvas: {s}')
    d.text((x,y),s,font=font(size,bold),fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')

def para(x,y,s,width,size=28,color=MUTED,bold=False,leading=None,bottom=None):
    lines=[]
    for p in s.split('\n'):
        line=''
        for ch in p:
            if line and d.textlength(line+ch,font=font(size,bold))>width:
                lines.append(line);line=ch
            else:line+=ch
        lines.append(line)
    step=leading or round(size*1.55)
    if bottom is not None and y+(len(lines)-1)*step+size>bottom:
        raise ValueError(f'Text exceeds panel: {s}')
    for i,line in enumerate(lines):text(x,y+i*step,line,size,color,bold)
    return y+len(lines)*step

def arrow(x1,y1,x2,y2,color=BLUE,width=4):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    a=math.atan2(y2-y1,x2-x1)
    pts=[(x2,y2),(x2-15*math.cos(a-.45),y2-15*math.sin(a-.45)),(x2-15*math.cos(a+.45),y2-15*math.sin(a+.45))]
    d.polygon(pts,fill=color)
    svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"/><polygon points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')

def section(y,n,title,note=''):
    box(80,y,58,50,BLUE,BLUE,9);text(90,y+5,n,29,WHITE,True)
    text(158,y-1,title,38,INK,True)
    if note:text(158,y+55,note,25,MUTED)

def mini(x,y,w,title,body,color=BLUE,h=166):
    box(x,y,w,h)
    compact=h<150
    text(x+24,y+(16 if compact else 22),title,28 if compact else 31,color,True)
    para(x+24,y+(57 if compact else 75),body,w-48,25 if compact else 27,
         leading=35 if compact else None,bottom=y+h-(10 if compact else 18))

# Title and central thesis.
box(0,0,W,262,DARK,DARK,0)
text(80,36,'GRAFT  /  能力与初步研究全景图',28,'#a9beed',True)
text(80,92,'扫描源码、构建代码索引，指导 AI 查找',62,WHITE,True)
text(84,185,'当前能力理解已整理  ·  构建原理待研究  ·  下方机制保留为初步线索  ·  效果待实测',31,'#cad6ee')
text(1900,41,'0.18.0  /  f9e6539',26,'#cad6ee')

section(303,'01','能做什么：八项能力，从找代码到理解修改影响')
capabilities=[
 ('定位代码','按任务返回相关位置和片段','find_code / ask'),
 ('接口轮廓','先看签名，再决定是否读实现','file_api / skeleton'),
 ('调用与影响','追踪上下游，分析改动波及范围','trace_calls / callers / blast'),
 ('完整搜索','正则命中按所属符号组织','find_all / grep'),
 ('地图与可视化','目录热点、关系图、文件层级','repo_map / map / viz'),
 ('检查与更新','报告漂移，查询前刷新结构','check_freshness / check'),
 ('用途与概念说明','深度模式补充业务含义和关键片段','build --deep（可选模型）'),
 ('助手集成','通过 CLI、MCP 和宿主接入使用','init / mcp（宿主能力不同）'),
]
for i,(title,body,cmd) in enumerate(capabilities):
    x=80+(i%4)*615;y=377+(i//4)*150
    box(x,y,595,133)
    text(x+22,y+17,title,30,INK,True)
    text(x+22,y+61,body,26,MUTED)
    text(x+22,y+99,cmd,22,BLUE)

section(714,'02','地图怎样建立：结构分析与语义说明是两条路径','扫描范围内源码；不要求从目标项目 main 函数出发，也不执行目标程序。')
box(80,812,2440,284,'#eaf0ff','#cbd8f9')
text(109,834,'基础结构层  /  本地解析，不调用模型',30,BLUE,True)
struct=[('源码范围','枚举文件、语言与忽略规则\n读源码，计算内容哈希'),('语法解析','Tree-sitter 生成语法树\n提取定义与待解析引用'),('关联解析','根据导入、作用域与类型\n连接调用、引用和继承'),('保存与索引','结构图＋文件卡片\n分词缓存＋关系查询入口')]
for i,(title,body) in enumerate(struct):
    x=110+i*606
    mini(x,892,561,title,body,BLUE,170)
    if i<3:arrow(x+566,976,x+597,976)
box(80,1116,2440,215,'#f2edf9','#dcd0ed')
text(109,1140,'可选语义层  /  --deep，使用配置的模型并产生相应费用',30,PURPLE,True)
para(111,1197,'符号说明：按文件批量发送“源码＋目标定义” → 模型返回用途与关键行号 → 从原源码截取 crux → 按内容哈希缓存',2360,28,INK,bottom=1240)
para(111,1250,'概念说明：文件摘要 → 合成为系统 / API / 跨文件概念 → 互相链接的 Markdown 节点；基础模式不会自动写出业务用途。',2360,27,MUTED,bottom=1306)

section(1390,'03','函数如何关联：先发现调用，再判断它指向谁')
box(80,1470,1195,412)
text(110,1495,'示例：导入别名不会只按名字相同连接',30,BLUE,True)
box(110,1550,1135,98,'#f0f4fa','#f0f4fa',8)
text(130,1569,'import { issueToken as createToken } from "./token";',26,INK)
text(130,1611,'function login(user) { return createToken(user.id); }',26,INK)
mini(110,1680,325,'提取线索','调用者 login\n调用名 createToken',BLUE,132)
mini(507,1680,335,'解析目标','追踪 ./token 导入\n还原名称 issueToken',BLUE,132)
mini(914,1680,331,'建立关系','login ─calls→\nissueToken',TEAL,132)
arrow(441,1748,493,1748);arrow(849,1748,900,1748)
text(112,1842,'关系：包含 / 调用 / 导入 / 引用 / 实现 / 继承',26,MUTED)
box(1295,1470,1225,412)
text(1325,1495,'复杂度来自“目标消歧”，不只是统计函数数目',30,INK,True)
para(1327,1555,'同名函数 → 结合文件、导入、作用域；唯一跨文件匹配可能标为推断。\n对象方法 → 利用接收者类型、赋值线索、继承与部分重载规则。\n动态调用 → 目标不明确时可能跳过；无连线不等于没有关系。',1160,28,leading=48,bottom=1723)
para(1327,1739,'每个节点记录：名称 / 类型 / 所属类、路径 / 行号 / 签名、导出信息 / 哈希，以及可选 summary / crux / 状态。',1160,27,leading=43,bottom=1830)
text(1327,1842,'边带来源可信度；可选 LSP 语言服务补充更精确的关系。',26,TEAL)

section(1932,'04','任务怎样变成上下文：先定位，再沿关系查，再控制输出')
query=[('任务与范围','问题关键词 / 代码标识符\n可限制目录与返回数量'),('匹配与排序','词项匹配、IDF / BM25\n图排序补充关联节点'),('组织阅读内容','位置、接口、关键片段\n需要时读取定义或原文件'),('助手执行与验证','模型理解 → 修改 → 测试\nGraft 提供导航与上下文')]
for i,(title,body) in enumerate(query):
    x=80+i*615
    mini(x,2010,565,title,body,TEAL,181)
    if i<3:arrow(x+572,2100,x+603,2100,TEAL)
box(80,2220,2440,112,'#e7f3f0','#cce4de')
text(110,2240,'两种查询路径',28,TEAL,True)
text(374,2240,'“谁调用 X”可沿结构边查找；普通问题用词项匹配作为起点，再用 Personalized PageRank 排序。',27,INK)
text(110,2286,'输出优先取已有 crux；定义读取受 80 行限制。缓存及筛选减少上下文，不改变模型参数，也不依赖每次调用模型重写结果。',27,MUTED)

section(2390,'05','代码变化怎样处理：解析缓存与语义缓存分开维护')
cache=[('没有变化','查询先检查文件指纹。\n没有发现变化时复用图谱；\n避免每次重新解析。',BLUE),('源码已变化','构建读取并计算内容哈希。\n未变文件复用解析，变化的重新提取；\n已有语义说明可能标为 stale。',PURPLE),('更新失败或未重写摘要','结构刷新不会自动调用模型。\n刷新失败可带提示使用旧图谱；\n关键逻辑仍需回到当前源码核对。',AMBER)]
for i,(title,body,color) in enumerate(cache):
    x=80+i*821
    mini(x,2465,798,title,body,color,222)

section(2750,'06','产出与效果：减少无关阅读，保留继续追查的入口')
effects=[('直接得到的产物','结构图 wiring.json、文件卡片与检索缓存；\n可选概念 Markdown 和符号用途说明；\nCLI / MCP 查询结果及本地图谱视图。',BLUE),('预期价值与适用场景','少走搜索弯路，少读整份无关文件；\n更早发现关联调用方和待检查测试。\n适合跨文件维护、重构和项目熟悉。',TEAL),('作者报告 ≠ 本项目实测','50 道 SWE-bench 题：修复 27 → 33 道。\n双方都成功的题：Token 减少 23%。\n作者自测口径；本项目未复现收益。',PURPLE)]
for i,(title,body,color) in enumerate(effects):
    x=80+i*821
    mini(x,2824,798,title,body,color,225)

section(3110,'07','真实边界：使用前要知道的六件事')
box(80,3185,2440,340,'#fff7ec','#eed9ba')
limits=[
 ('中文查询有明确限制','原分词函数对纯中文返回空词项；外层助手可先转英文关键词或代码标识符。'),
 ('过期片段可能被选中','隔离探针中，stale 节点仍可返回旧 crux；结构新鲜不代表语义缓存已更新。'),
 ('说明与关键片段有截断','符号说明输入最多 18,000 字符；文件摘要 24,000。关键片段实际存储上限 12 行。'),
 ('关系图存在覆盖盲点','动态派发、反射、语言支持差异都可能造成遗漏；推断关系也需要验证。'),
 ('“节省 Token”是估计值','源码以字符数 ÷ 4 估算，再与相关文件全文比较；不是实际账单或真实分词计数。'),
 ('已有验证的范围有限','已核对源码并运行两个隔离原函数探针；未完整建图、接入模型或做收益 A/B 实验。'),
]
for i,(title,body) in enumerate(limits):
    col=i%3;row=i//3;x=111+col*805;y=3210+row*153
    text(x,y,title,29,AMBER,True)
    para(x,y+48,body,746,26,INK,leading=40,bottom=y+138)

text(82,3567,'理解定位：Graft 侧重“找哪些代码＋提供关系”；Caveman 侧重“精简已选材料”。两者有重合，叠加收益仍需验证。',28,INK,True)
text(82,3630,'依据：trailhq/Graft · 固定提交 f9e65396e638e517aecae0d731017f53084d70ed · 研究日期 2026-09-16',25,MUTED)
text(82,3675,'源码：graph/build、extract、resolve、enrich、types；ask/ask、index-file；ai/crux；context/savings。图为原创机制归纳，非运行截图。',24,MUTED)
svg.append('</svg>')
OUT.mkdir(parents=True,exist_ok=True)
im.save(OUT/'graft-overview.png',optimize=True)
(OUT/'graft-overview.svg').write_text('\n'.join(svg),encoding='utf-8')
im.resize((1040,1496),Image.Resampling.LANCZOS).save(OUT/'graft-overview-preview.png',optimize=True)
print(f'Created {W} x {H} PNG and SVG; PNG: {(OUT/"graft-overview.png").stat().st_size:,} bytes')
