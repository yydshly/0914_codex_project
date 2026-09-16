"""Create the Chinese research overview as an editable SVG and a high-resolution PNG."""
from pathlib import Path
from html import escape
import json
from playwright.sync_api import sync_playwright
from catalog_data import TYPE_GROUPS, rows

ROOT = Path(__file__).resolve().parents[1]
W, H = 2000, 3370
NAVY, INK, MUTED = '#102d42', '#183b50', '#587080'
TEAL, BLUE, ORANGE = '#087e8b', '#2862ca', '#c8612d'
parts = []

def rect(x,y,w,h,fill,stroke='none',r=16):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')

def text(x,y,value,size=28,color=INK,weight=400):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')

def lines(x,y,values,size=27,color=MUTED,gap=42):
    for i,value in enumerate(values): text(x,y+i*gap,value,size,color)

def line(x1,y1,x2,y2,color='#cedbe3',width=2,arrow=False):
    parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')

def section(y,num,title,subtitle):
    rect(90,y-35,52,48,TEAL,r=10)
    text(101,y,num,27,'#ffffff',700)
    text(162,y,title,37,NAVY,700)
    text(162,y+42,subtitle,25,MUTED)

def icon(kind,x,y):
    c=TEAL
    if kind in (0,2,3):
        line(x+20,y+20,x+20,y+66,c,3)
        line(x-15,y+50,x+55,y+50,c,3)
        for xx,yy in [(x+2,y),(x-33,y+50),(x+37,y+50)]:rect(xx,yy,36,25,'#e2f1f1',c,5)
        if kind==3: line(x+3,y+74,x+51,y+74,c,3)
    elif kind==1:
        for i in range(3):
            rect(x-32+i*34,y+24,25,30,'#e2f1f1',c,4)
            if i<2:line(x-7+i*34,y+39,x+2+i*34,y+39,c,3)
    elif kind==4:
        for i,v in enumerate([58,74,43]):rect(x-30+i*14,y+9+i*23,v,13,c,r=3)
    elif kind==5:
        line(x+13,y,x+13,y+78,c,2);line(x-30,y+39,x+56,y+39,c,2)
        for xx,yy in [(x-15,y+18),(x+29,y+57)]:parts.append(f'<circle cx="{xx}" cy="{yy}" r="9" fill="{c}"/>')
    else:
        for i,h in enumerate([29,57,77]):rect(x-28+i*28,y+80-h,19,h,c,r=3)

def main():
    ROOT.joinpath('assets').mkdir(exist_ok=True)
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
    parts.append('<title id="title">Diagram Design 一图总览：原理、分类与绘图方法</title><desc id="desc">中文研究信息图，包含三种可组合维度、HTML与SVG技术流程、七类四十种基础图型、五十七组示例的构成及实际绘图步骤。</desc>')
    parts.append('<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#087e8b"/></marker></defs>')
    parts.append('<g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">')
    rect(0,0,W,H,'#f5f7f8',r=0)
    rect(0,0,W,290,NAVY,r=0)
    rect(90,47,8,48,'#56d3c1',r=3)
    text(120,82,'DIAGRAM DESIGN  /  研究总览',28,'#8cddd5',600)
    text(90,165,'从内容与关系，到可编辑的图',64,'#ffffff',700)
    text(92,223,'AI 理解与编写  ×  设计规范与模板  ×  浏览器渲染',33,'#d5e5ec')
    text(1510,84,'固定研究版本  v2.6.23',23,'#b7ced9')
    text(1510,127,'40 基础图型 / 57 示例组',23,'#b7ced9')

    section(360,'01','先分清三个维度，它们可以组合','“创建新图、添加动画、导入重绘”是使用路径；图型、表现方式和输入来源分别回答不同问题。')
    for x,title,sub,ls,color in [
        (90,'画什么结构？','图形类型',['架构、流程、层级、时序、统计……','按要解释的关系选图，共 40 种基础图型。'],TEAL),
        (707,'怎样呈现？','表现方式',['静态图，或分步 / 播放动画','配色、深浅主题、细节量与页面格式可调整。'],BLUE),
        (1324,'根据什么画？','输入来源',['文字 / 数据，或已有图的源文件','draw.io · Mermaid · Excalidraw'],ORANGE),
    ]:
        rect(x,427,586,201,'#ffffff','#d9e3e8')
        rect(x,427,586,7,color,r=0)
        text(x+26,477,title,34,INK,700);text(x+348,475,sub,25,color,600)
        lines(x+26,535,ls,23,gap=40)
    rect(90,651,1820,57,'#e6f2f2',r=10)
    text(115,689,'组合示例：Mermaid 源文件  →  提取流程关系  →  重绘深色流程图  →  添加分步动画  →  导出静态 PNG',27,TEAL,600)

    section(785,'02','技术原理：AI 写图形代码，浏览器把代码画出来','库提供 Skill 指令、参考文档、模板、解析与检查脚本；宿主大模型负责理解、取舍和编写。')
    steps=[('内容输入',['新图：描述 / 表格 / 数据','旧图：文本 / XML / JSON']),('整理与设计',['确认节点、关系与分组','选择图型、布局、样式']),('编写图形代码',['SVG：形状 / 文字 / 箭头','HTML + CSS：页面与样式']),('检查与渲染',['结构、几何与人工核对','浏览器显示并导出文件'])]
    for i,(title,ls) in enumerate(steps):
        x=90+i*467
        rect(x,859,419,160,'#ffffff','#d9e3e8')
        text(x+23,905,f'{i+1:02}  {title}',30,TEAL,700)
        lines(x+23,950,ls,24,gap=37)
        if i<3:line(x+428,936,x+455,936,TEAL,3,True)
    rect(90,1044,892,188,'#edf2f7')
    text(115,1087,'坐标 → 图元 → 连线',28,INK,700)
    rect(120,1116,165,69,'#ffffff',BLUE,9);text(138,1160,'接口服务',26,BLUE,600)
    line(291,1150,391,1150,TEAL,3,True)
    rect(412,1116,145,69,'#ffffff',TEAL,9);text(442,1160,'数据库',26,TEAL,600)
    lines(593,1127,['x / y 决定位置','rect / text / path 组成图','布局规则 + AI / 作者决策'],22,gap=34)
    rect(1008,1044,902,188,'#edf2f7')
    text(1035,1087,'数值 → 长度 / 位置 / 面积 / 带宽',28,INK,700)
    for i,h in enumerate([18,36,72]):
        rect(1041+i*67,1207-h,42,h,TEAL,r=3)
        text(1040+i*67,1197-h,str([50,100,200][i]),18,MUTED)
    lines(1280,1127,['示例：柱高 = 数值 ÷ 最大值 × 可用高度','折线 / 散点映射坐标；桑基图映射带宽','刻度、单位、负值与比例需要核对。'],23,gap=34)
    text(93,1276,'旧图重绘：解析内容后重新排版；动画：在图形之上加入可选 JS / CSS 控制，并保留静态表达。',25,MUTED)

    section(1358,'03','七类图型：按你要解释的问题选择','下列七类是本研究按主要表达对象整理的导航；基础图型来自固定版本的 40 项选择表。')
    rect(90,1429,1820,75,NAVY,r=10)
    text(118,1478,'40 基础图型  +  11 派生示例  +  3 动画演示  +  3 导入重绘  =  57 示例组',36,'#ffffff',700)
    catalog=rows()
    for i,(name,question,keys) in enumerate(TYPE_GROUPS):
        y=1528+i*96
        rect(90,y,1820,86,'#ffffff' if i%2==0 else '#eaf0f3',r=10)
        icon(i,145,y+5)
        text(227,y+36,name,29,INK,700)
        base=keys.split();total=sum(r['category']==name for r in catalog)
        text(227,y+69,f'{len(base)} 种基础 · {total} 组示例',21,MUTED)
        labels=[next(r['name'] for r in catalog if r['id']==key) for key in base]
        text(570,y+51,' · '.join(labels),25,INK)
    text(100,2233,'派生示例：如气泡、蜂群、坡度、数据湖等；动画和导入示例仍可归入相应的基础图型。',24,MUTED)
    text(100,2270,'57 组共 155 个 HTML 示例文件；浅色、深色和完整页面等版本，不增加基础图型数量。',24,MUTED)

    section(2348,'04','怎么画：先明确内容，再选择表达','将这套 Skill 用在支持的 AI 工作环境中，提供真实内容与约束；按以下步骤逐轮生成、核对和修改。')
    instructions=[
        ('提供事实','列出节点、关系、数据、单位和来源。'),
        ('明确受众','说明谁来看、看完要理解什么。'),
        ('选择图型','结构用架构，步骤用流程，趋势用折线。'),
        ('设置输出','确定格式、尺寸、细节量、受众与配色。'),
        ('生成并核对','检查事实、比例、连线、遮挡与可读性。'),
        ('修改与交付','保留可编辑源文件，导出所需格式。'),
    ]
    for i,(title,body) in enumerate(instructions):
        x=90+(i%3)*617;y=2421+(i//3)*115
        rect(x,y,586,100,'#ffffff','#d9e3e8',12)
        text(x+19,y+38,f'{i+1}  {title}',28,TEAL,700)
        text(x+19,y+76,body,23,INK)
    rect(90,2671,1820,143,'#102d42',r=14)
    text(117,2713,'可以这样提需求',24,'#8cddd5',700)
    text(117,2758,'“将这些系统关系画成中文架构图，面向非技术同事，16:9、蓝色；保留核心关系，',28,'#ffffff')
    text(117,2799,'说明合并项，输出 HTML、SVG 和 PNG。”',26,'#ffffff')

    section(2875,'05','交付、用途与扩展方向','对我们最直接的价值：把研究资料、旧图和讨论结果，整理成统一、清晰、可复用的视觉说明。')
    for x,title,ls in [
        (90,'输出什么',['HTML：浏览器展示，可承载交互 / 动画','SVG：可编辑矢量图，放大清晰','PNG：像素图片，适合文档与分享']),
        (707,'适合用在哪里',['研究笔记与技术方案配图','流程交接、教学说明、管理汇报','旧图整理、品牌统一、演示材料']),
        (1324,'可以怎样扩展〔建议〕',['接入真实数据与代码关系提取','加入团队图型、品牌与中文模板','批量生成、事实校验、版本对比']),
    ]:
        rect(x,2948,586,191,'#ffffff','#d9e3e8',12)
        text(x+23,2992,title,29,INK,700);lines(x+23,3038,ls,23,gap=36)
    text(94,3190,'边界：检查通过不等于事实正确；旧图重绘不保证原布局；PNG 是静态的，SVG / PNG 单图导出不含页面外围摘要。',24,MUTED)
    text(94,3232,'当前展厅展示预先保存的示例，切换分类与版本不会实时调用 AI；图型库也不等同于通用自动布局引擎。',24,MUTED)
    line(90,3262,1910,3262)
    text(92,3303,'来源：cathrynlavery/diagram-design · v2.6.23 · ce9344c52cb9  |  本地研究整理 · 2026-09-16',23,MUTED)
    text(92,3337,'阅读路径：分清维度 → 理解原理 → 选择图型 → 提供内容与约束 → 核对 → 交付',22,TEAL,600)
    parts.append('</g></svg>')
    svg=ROOT/'assets/diagram-design-overview.svg'
    svg.write_text('\n'.join(parts),encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':W,'height':H},device_scale_factor=1.5)
        page.goto(svg.as_uri());page.evaluate('document.fonts.ready')
        overflow=page.locator('text').evaluate_all('(els)=>els.map(e=>({text:e.textContent,b:e.getBBox()})).filter(v=>v.b.x<0||v.b.x+v.b.width>1980||v.b.y+v.b.height>3370).map(v=>v.text)')
        assert not overflow,overflow
        overlaps=page.locator('text').evaluate_all('''els=>{
          const a=els.map(e=>({text:e.textContent,b:e.getBBox()}));const hits=[];
          for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){
            const p=a[i].b,q=a[j].b;
            if(Math.min(p.x+p.width,q.x+q.width)-Math.max(p.x,q.x)>1 &&
               Math.min(p.y+p.height,q.y+q.height)-Math.max(p.y,q.y)>1)
               hits.push([a[i].text,a[j].text]);
          }return hits;
        }''')
        assert not overlaps,overlaps
        page.locator('svg').screenshot(path=str(svg.with_suffix('.png')))
        browser.close()
    print(json.dumps({'svg':str(svg),'png':str(svg.with_suffix('.png')),'size':[3000,5055],'text_elements':sum('<text ' in p for p in parts),'overflow':overflow},ensure_ascii=False))

if __name__=='__main__':main()
