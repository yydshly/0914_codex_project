"""Render a deterministic Chinese architecture poster as PNG and editable SVG.

Requires Pillow; uses Microsoft YaHei on Windows. The exported assets are tracked,
so the webpage build does not require fonts or Pillow.
"""
from pathlib import Path
import html
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 2400, 2640
INK, MUTED, TEAL, NAVY = '#142d40', '#506676', '#006b7b', '#112f44'
LINE, PAPER, CORAL = '#d5e1e8', '#f5f8fa', '#a63f32'
FONT = Path('C:/Windows/Fonts/msyh.ttc')
BOLD = Path('C:/Windows/Fonts/msyhbd.ttc')
im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="抖音采集：能力、原理与边界">', f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def rect(x, y, w, h, fill, stroke=None, radius=18):
    d.rounded_rectangle((x, y, x+w, y+h), radius=radius, fill=fill, outline=stroke, width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="2"/>')

def text(x, y, value, size=30, color=INK, bold=False):
    d.text((x,y), value, font=font(size,bold), fill=color, anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(value)}</text>')

def para(x, y, value, width, size=29, color=MUTED, bold=False, leading=None):
    lines=[]
    for part in value.split('\n'):
        line=''
        for char in part:
            if line and d.textlength(line+char,font=font(size,bold)) > width:
                lines.append(line); line=char
            else: line+=char
        lines.append(line)
    step=leading or int(size*1.65)
    for index,line in enumerate(lines): text(x,y+index*step,line,size,color,bold)
    return y+len(lines)*step

def arrow(x1,y1,x2,y2,color=TEAL,both=False):
    d.line((x1,y1,x2,y2),fill=color,width=4)
    svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="4" fill="none"/>')
    def head(ax,ay,bx,by):
        angle=math.atan2(by-ay,bx-ax)
        pts=[(bx,by),(bx-16*math.cos(angle-.45),by-16*math.sin(angle-.45)),(bx-16*math.cos(angle+.45),by-16*math.sin(angle+.45))]
        d.polygon(pts,fill=color)
        svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="{color}"/>')
    head(x1,y1,x2,y2)
    if both: head(x2,y2,x1,y1)

def section(y,num,title,subtitle=''):
    text(80,y,num,28,TEAL,True);text(150,y-4,title,40,INK,True)
    if subtitle: text(150,y+56,subtitle,26,MUTED)

text(80,55,'RESEARCH / 008',26,TEAL,True)
text(80,105,'抖音内容采集：能力、原理与边界',68,INK,True)
text(82,197,'douyin-downloader  ·  源码研究  ·  2026-09-16  ·  commit 125ddf4',27,MUTED)
rect(80,265,1090,142,'#e5f0f2')
text(112,290,'公开 Python 版',34,TEAL,True)
text(112,345,'接口直连为主；浏览器辅助登录与主页兜底',29,INK)
rect(1200,265,1120,142,'#e9edf3')
text(1232,290,'Douzy 桌面版 · 独立发行',34,INK,True)
text(1232,345,'部分请求由内置抖音页面代发；专用代码未完整公开',28,INK)

section(456,'01','一次采集，谁与谁交互？')
# Four outer nodes plus a shared backend; arrows indicate distinct data stages.
rect(80,550,530,178,'#ffffff',LINE)
text(114,578,'你与账号 A',35,INK,True)
para(114,632,'浏览器打开抖音并完成登录\n账号提供访问身份',470,28)
rect(910,550,560,470,NAVY)
text(951,589,'Python 下载程序',43,'#ffffff',True)
para(951,672,'构造请求与分页\n筛选、去重与选源\n传输文件、校验与归档\n记录任务及失败原因',474,32,'#d9e8f0',leading=65)
rect(1810,550,510,178,'#ffffff',LINE)
text(1842,578,'抖音业务服务器',34,INK,True)
para(1842,637,'校验会话、权限与请求环境\n返回结构化业务数据',445,27)
arrow(610,628,910,628)
text(642,580,'读取 Cookie',27,TEAL,True)
text(646,651,'会话相关信息',25,MUTED)
arrow(1470,604,1810,604)
text(1500,561,'关键词／作品 ID',25,TEAL)
arrow(1810,704,1470,704)
para(1502,736,'列表、评论、作品资料\n及媒体地址',290,25)
rect(1810,842,510,178,'#ffffff',LINE)
text(1842,870,'媒体服务器 / CDN',33,INK,True)
para(1842,927,'提供视频、图片、音频\n或直播流数据',445,27)
arrow(1470,881,1810,881)
text(1504,834,'按媒体地址请求文件',25,TEAL)
arrow(1810,978,1470,978)
text(1538,930,'媒体数据返回',25,MUTED)
rect(80,842,530,178,'#ffffff',LINE)
text(114,870,'本地文件与记录',34,INK,True)
para(114,927,'媒体、JSON、文字、历史\n按作者与内容组织',470,27)
arrow(910,927,610,927)
text(668,876,'处理后保存',27,TEAL,True)
text(640,952,'不从博主手机取文件',24,MUTED)
rect(80,1050,2240,80,'#e5f0f2')
text(112,1074,'账号 A 是访问身份；博主 B 是查询目标。登录过 ≠ 所有请求都经过浏览器。',31,TEAL,True)

rect(80,1157,2240,153,'#ffffff',LINE)
text(113,1180,'浏览器参与的两条路径',30,INK,True)
text(113,1238,'公开版：打开主页 → 监听作品列表 → 交回 Python',28,MUTED)
text(1210,1238,'桌面版：Python → 内置页面校验与请求 → 交回后端',27,MUTED)

section(1361,'02','能力如何变成输出？','以下是设计产出，不代表本次完成了在线采集')
cards=[
('搜索与热榜','网页接口 → 分页、去重','JSONL 结果与时间快照'),
('视频、图集与音乐','详情 → 媒体选源 → 文件传输','视频／图片／音频与元数据'),
('评论与二级回复','作品 ID → 评论分页 → JSON','回复自动流程仅取第一页'),
('直播与回放','读取可用播放源 → 保存','录制／回放；直播有实验性限制'),
('语音转文字','音轨 → 转写服务或本地模型','TXT／JSON；独立脚本可输出 SRT'),
('任务与归档','并发、限速、重试、历史','下载任务接口、文件清单与通知')]
for i,(title,body,result) in enumerate(cards):
    col,row=i%3,i//3;x=80+col*755;y=1470+row*212
    rect(x,y,730,186,'#ffffff',LINE)
    text(x+28,y+23,title,33,INK,True)
    text(x+28,y+81,body,27,MUTED)
    text(x+28,y+131,result,25,TEAL)

section(1935,'03','结果与意义')
for x,title,desc in [(80,'素材归档','把分散内容整理为本地资料'),(835,'内容研究','为选题、反馈与文本分析提供材料'),(1590,'二次开发','复用解析、采集、队列与存储')]:
    text(x+4,2010,title,34,INK,True);text(x+4,2066,desc,27,MUTED)
text(84,2130,'扩展链路：发现 → 筛选 → 下载与采集 → 转写 → AI 分析 / 长期监测（需另接系统）',29,TEAL,True)

rect(80,2210,2240,293,'#fff0ec')
text(112,2239,'04  使用边界：有代码 ≠ 当前稳定可用',37,CORAL,True)
para(114,2313,'• CLI 多项核心接口受风控限制\n• 主页兜底尚未验证新门禁\n• 桌面页面桥接未独立实测',1050,29,INK,leading=49)
para(1240,2313,'• 无水印是优选来源，不是擦除画面\n• 服务任务在内存，重启会丢失\n• 采集结果不保证全量或完整',1030,29,INK,leading=49)
text(83,2540,'依据公开源码与作者说明；未登录实测，不展示成功率。服务器按职责示意，不代表实际部署拓扑。',25,MUTED)
text(83,2590,'来源：github.com/jiji262/douyin-downloader     |     研究文档与网页：008-douyin-downloader',23,MUTED)
svg.append('</svg>')
OUT.mkdir(parents=True,exist_ok=True)
im.save(OUT/'douyin-overview.png',optimize=True)
(OUT/'douyin-overview.svg').write_text('\n'.join(svg),encoding='utf-8')
print(f'Created PNG and SVG: {W} × {H}; PNG bytes: {(OUT/"douyin-overview.png").stat().st_size}')
