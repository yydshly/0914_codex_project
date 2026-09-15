"""Create a shareable Chinese overview diagram as PNG and editable SVG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
W,H=1600,2100
PAPER='#f5f1e6'; INK='#213f39'; MUTED='#576b62'; GREEN='#287c69'; GOLD='#a7752e'; LINE='#d5dacc'
im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">Audio-Locked Paper Theatre：意义、场景与实现原理</title><desc id="desc">以音频为主时间轴，将知识编排为独立对象的可控动画；八类用途、六步制作流程，以及英语位置词实例。PPT和智能辅导需外部工具。</desc>']
def rect(x,y,w,h,fill,rad=0,stroke=None):
    d.rounded_rectangle((x,y,x+w,y+h),radius=rad,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
def line(x1,y1,x2,y2,fill=LINE,width=2):
    d.line((x1,y1,x2,y2),fill=fill,width=width)
    svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{fill}" stroke-width="{width}" fill="none"/>')
def circle(x,y,r,fill):
    d.ellipse((x-r,y-r,x+r,y+r),fill=fill)
    svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
def text(x,y,s,size=26,fill=INK,bold=False,maxw=None):
    f=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',size)
    if maxw:assert d.textlength(s,font=f)<=maxw,(s,d.textlength(s,font=f),maxw)
    d.text((x,y),s,font=f,fill=fill,anchor='lt')
    svg.append(f'<text x="{x}" y="{y+size*.9}" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}">{escape(s)}</text>')
def arrow(x1,y1,x2,y2):
    line(x1,y1,x2,y2,GREEN,3)
    line(x2-8,y2-7,x2,y2,GREEN,3);line(x2-8,y2+7,x2,y2,GREEN,3)
def heading(y,num,title,detail):
    rect(72,y,51,43,GREEN,8);text(81,y+6,num,27,'#ffffff',True)
    text(141,y+2,title,34,INK,True)
    text(1518-d.textlength(detail,font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',23)),y+9,detail,23,MUTED)

rect(0,0,W,H,PAPER)
text(72,54,'AUDIO-LOCKED PAPER THEATRE  /  一图读懂',24,GREEN,True)
text(72,104,'用声音定节奏，把知识演出来',60,INK,True)
text(72,187,'定位：一套有声解释视频的制作流程、结构化模板与验证工具。',28,MUTED)
line(72,245,1528,245)

heading(279,'01','它的意义','让值得解释的关系变得可见')
values=[('看懂抽象关系','把位置、因果、结构、流程','变成对象的移动与状态变化。'),('控制讲解节奏','说到哪里，画面演到哪里；','让声音与关键动作相互配合。'),('复用与修改内容','保留脚本、素材和动作规则；','便于重渲染与系列内容制作。')]
for i,(title,a,b) in enumerate(values):
    x=72+i*494;rect(x,348,468,145,'#e5ecdf',14)
    text(x+24,369,title,30,GREEN,True);text(x+24,418,a,25,maxw=425);text(x+24,452,b,25,maxw=425)

heading(532,'02','它可以用在哪里？','8 类代表用途 · 可延展到更多知识领域')
cases=[('学习与复习','概念辨析 · 错题讲解','知识回顾 · 学习方法'),('英语与语言','位置词 · 语序与句型','构词分析 · 情景对话'),('课堂与课程','课前导入 · 难点微课','实验预讲 · 暂停提问'),('科普与技术','DNS · 程序执行','科学原理 · 系统架构'),('企业与岗位培训','入职流程 · 任务交接','业务步骤 · 错误纠正'),('产品与客户教育','功能原理 · 使用流程','新手上手 · 常见问题'),('研究与知识传播','论文方法 · 数据故事','报告说明 · 文化讲解'),('课件与材料扩展','视频嵌入 PPT · 讲义','可编辑课件需额外工具')]
for i,(title,a,b) in enumerate(cases):
    x=72+(i%4)*370;y=600+(i//4)*162
    rect(x,y,344,143,'#fffdf7',12,LINE)
    text(x+19,y+19,title,28,INK,True,maxw=309)
    text(x+19,y+65,a,24,MUTED,maxw=309);text(x+19,y+99,b,24,MUTED,maxw=309)
text(72,929,'选题判断：有没有一个“演出来，比只说出来更容易懂”的过程？',28,GREEN,True)

heading(996,'03','实现原理：音频是主时间轴','工作流编排 + 外部工具 + 可控渲染')
steps=[('讲解设计','确定知识目标','编写口播与分镜'),('锁定声音','生成最终配音','取得真实时间戳'),('拆成对象','准备独立图层','登记位置与关系'),('编排动作','以音频时间为准','控制移动与遮挡'),('逐帧合成','计算每一帧画面','合入音频与字幕'),('验证交付','检查同步与关系','解码、导出视频')]
for i,(title,a,b) in enumerate(steps):
    x=72+i*247;rect(x,1075,222,162,'#fffdf7',12,LINE)
    text(x+18,1091,f'{i+1:02}',22,GREEN,True)
    text(x+18,1124,title,30,INK,True)
    text(x+18,1170,a,23,MUTED,maxw=190);text(x+18,1204,b,23,MUTED,maxw=190)
    if i<5:arrow(x+226,1153,x+239,1153)
text(72,1265,'每一帧 = 在音频时间 t，按既定规则绘制所有对象的当前状态。',28,GREEN,True)

rect(72,1321,1456,350,'#e9eee3',16)
text(99,1345,'以英语课为例：同一颗球，三个位置；对象独立移动，配合讲解。',29,INK,True)
timeline=[('14.4 秒 · in','The ball is in the box.'),('28.5 秒 · on','The ball is on the table.'),('40.7 秒 · under','The ball is under the table.')]
for i,(label,sentence) in enumerate(timeline):
    x=101+i*485;text(x,1403,label,27,GREEN,True)
    cx=x+200
    line(x+105,1589,x+296,1589,'#bfcbbb',3)
    if i==0:
        rect(cx-81,1488,164,99,'#abcddd',3)
        circle(cx,1507,32,'#d57c54')
        rect(cx-81,1520,164,68,'#73aac4',3)
    else:
        rect(cx-100,1507,200,15,'#bf9657',3)
        rect(cx-86,1522,12,66,'#a67b41',1);rect(cx+74,1522,12,66,'#a67b41',1)
        circle(cx,1479 if i==1 else 1560,28,'#d57c54')
    text(x,1613,sentence,25,INK,maxw=450)
    if i<2:arrow(x+385,1480,x+441,1480)

heading(1714,'04','看清边界，再组合扩展','方法可复用，应用功能按需接入')
text(72,1784,'仓库核心',27,GREEN,True);text(247,1784,'制作规范、生产模板与验证器；音频、图像、渲染依赖配套工具。',27,maxw=1260)
text(72,1832,'本地复现',27,GREEN,True);text(247,1832,'MiniMax 配音与句级时间戳 → Pillow 图层动画 → FFmpeg 成片。',27,maxw=1260)
text(72,1880,'另加功能',27,GREEN,True);text(247,1880,'网页答题是额外交互；可编辑 PPT、发音评分、个性辅导需其他模块。',27,maxw=1260)
rect(72,1941,1456,69,'#e5ecdf',10)
text(96,1961,'能把内容演清楚，是表达能力；是否真正学会，还要通过复述、练习与应用检验。',27,INK,True,maxw=1410)
text(72,2043,'来源：github.com/jay-yangPY/audio-locked-paper-theatre · 上游文档与本地四个样例',21,MUTED)
text(72,2074,'场景为适用性归纳；本地动画按句级时间编排，不声称逐词对齐。  /  2026-09-15',18,MUTED)
svg.append('</svg>')
(ROOT/'assets/library-overview.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(ROOT/'assets/library-overview.png')
print('Saved assets/library-overview.png and assets/library-overview.svg')
