"""Research overview v2: explicit selection guidance, evidence, and tool boundaries."""
from pathlib import Path
import json
import re
from PIL import Image
from playwright.sync_api import sync_playwright
from catalog_data import TYPE_GROUPS, rows, EXTRAS
from draw_overview import parts, rect, text, lines, line, icon, NAVY, INK, MUTED, TEAL, BLUE, ORANGE

ROOT = Path(__file__).resolve().parents[1]
W,H = 2400,4110

def heading(y,n,title,sub):
    rect(90,y-38,56,52,TEAL,r=10)
    text(101,y,n,29,'white',700)
    text(168,y,title,39,NAVY,700)
    text(168,y+46,sub,27,MUTED)

def card(x,y,w,h,title,body,color=TEAL):
    rect(x,y,w,h,'#ffffff','#d4e0e7',14)
    rect(x,y,6,h,color,r=2)
    text(x+27,y+46,title,32,color,700)
    lines(x+27,y+95,body,27,INK,42)

def main():
    parts.clear()
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
    parts.append('<title id="title">Diagram Design 全景指南 · 第二版</title><desc id="desc">原理、八种语义模式、七类四十种图型、十七组扩展示例、绘图方法、历史工具分工、实验与扩展路线。</desc>')
    parts.append('<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#087e8b"/></marker></defs>')
    parts.append('<g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">')
    rect(0,0,W,H,'#f4f7f9',r=0)
    rect(0,0,W,270,NAVY,r=0)
    rect(90,45,8,46,'#64d6c6',r=3)
    text(122,79,'DIAGRAM DESIGN  /  从理解到交付',30,'#94e0d7',700)
    text(90,158,'一张图看懂：原理、选型与绘图方法',64,'white',700)
    text(93,222,'主要产物是可编辑的 HTML / SVG 图形代码；PNG 是浏览器渲染后的图片。',32,'#d7e7ed')
    text(1930,79,'研究总览 · 优化版 02',27,'#94e0d7',700)
    text(1930,122,'固定版本 v2.6.23',25,'#d7e7ed')
    text(1930,162,'40 基础 / 57 示例 / 155 文件',24,'#d7e7ed')

    heading(334,'01','三条使用路径，三个可组合的维度','创建新图、添加动画、导入重绘可以衔接使用；先区分内容结构、呈现方式与输入来源。')
    card(90,407,720,162,'图形类型｜表达什么关系',['架构、流程、层级、策略、数值等','按问题选图；七类共 40 种基础图型。'])
    card(840,407,720,162,'表现方式｜怎样讲清楚',['默认静态；按需分步显示或播放动画','主题、品牌、手绘、批注与细节量可调整。'],BLUE)
    card(1590,407,720,162,'输入来源｜根据什么来画',['描述 / 数据，或已有图的可解析源文件','draw.io · Mermaid · Excalidraw'],ORANGE)
    rect(90,591,2220,62,'#e0f1ef',r=10)
    text(117,632,'组合示例：Mermaid 源文件 → 提取关系 → 重绘流程图 → 深色主题 + 分步动画 → HTML 演示 / 静态 PNG 分享',30,TEAL,600)

    heading(727,'02','原理：事实 → 语义 → 布局 → 图形代码 → 渲染','AI 负责理解与编写；库提供 Skill 规范、模板和辅助脚本；浏览器执行代码，把图画出来。')
    pipeline=[('输入与提取',['描述 / 数据由 AI 整理','旧图经 Python 解析','产出节点、边与分组']),('语义与选图',['确认行为、状态与风险','选择语义模式和图型','控制层级与信息密度']),('布局与样式',['计算坐标、间距和路径','使用模板 / 部分公式','设置字体、颜色与品牌']),('代码与动画',['SVG：图元、标签、连线','HTML / CSS：页面样式','可选 JS / CSS 控制动画']),('检查与输出',['脚本检查 + 人工核对','浏览器渲染与预览','交付 HTML / SVG / PNG'])]
    for i,(title,body) in enumerate(pipeline):
        x=90+i*451
        rect(x,803,416,192,'white','#d4e0e7',14)
        text(x+20,846,f'{i+1:02}  {title}',31,TEAL,700)
        lines(x+20,892,body,25,INK,37)
        if i<4:line(x+421,900,x+440,900,TEAL,3,True)
    rect(90,1016,1095,170,'#eaf0f6',r=12)
    text(115,1057,'几何图：按坐标放图元，按关系连线',29,INK,700)
    rect(118,1087,170,63,'white',BLUE,8);text(147,1129,'接口服务',27,BLUE,600)
    line(298,1118,367,1118,TEAL,3,True)
    rect(386,1087,164,63,'white',TEAL,8);text(425,1129,'数据库',27,TEAL,600)
    lines(590,1095,['x / y 定位；rect / text / path 构成图','布局仍包含 AI / 作者决策与人工调整。'],25,MUTED,39)
    rect(1210,1016,1100,170,'#eaf0f6',r=12)
    text(1236,1057,'数据图：把数值映射为长度、位置、面积或带宽',29,INK,700)
    for i,h in enumerate([17,34,68]):
        rect(1243+i*69,1165-h,43,h,TEAL,r=3)
        text(1241+i*69,1156-h,str([50,100,200][i]),19,MUTED)
    lines(1495,1095,['零起点柱状图：柱高 = 数值 ÷ 最大值 × 可用高度','核对单位、刻度、负值与比例，避免视觉误导。'],25,MUTED,39)
    rect(90,1208,2220,179,'white','#d4e0e7',14)
    text(116,1251,'补充：8 种语义模式负责“讲什么行为”，图型负责“怎么排布”',30,INK,700)
    lines(116,1301,[
        '队列与瓶颈 → 数据流　｜　阶段语义槽位 → 多角色过程　｜　散乱输入变为结构化产物 → 数据流　｜　双路径策略轨迹 → 流程图',
        '安全路径 → 架构　｜　治理控制目录 → 分层　｜　补偿性安全分层 → 分层　｜　可追溯模块分解 → 层级树',
    ],26,MUTED,42)

    heading(1463,'03','按问题选图：七类、40 种基础图型，全量列出','七类是本研究的导航分类；语义模式、动画、输入格式和主题版本，都属于不同统计维度。')
    rect(90,1539,2220,68,NAVY,r=12)
    text(116,1585,'40 基础图型 + 11 派生示例 + 3 动画演示 + 3 导入重绘 = 57 示例组',37,'white',700)
    text(1850,1582,'共 155 个 HTML 文件',26,'#bfd7e1')
    catalog=rows()
    questions=['组件怎样连接、运行在哪里？','先做什么、谁交互、怎样变化？','怎样拆解、包含、分层与分工？','实体、表、类和模块怎样关联？','何时发生、进度与体验怎样规划？','怎样定位、归因、比较与授权？','数量、趋势、分布和流量如何变化？']
    for i,((name,_,keys),question) in enumerate(zip(TYPE_GROUPS,questions)):
        y=1630+i*94
        rect(90,y,2220,85,'white' if i%2==0 else '#e7eff3',r=10)
        icon(i,145,y+4)
        text(227,y+34,name,30,INK,700)
        base=keys.split();total=sum(r['category']==name for r in catalog)
        text(227,y+68,f'{len(base)} 基础 / {total} 示例',24,MUTED)
        text(575,y+31,question,24,TEAL,600)
        labels=[next(r['name'] for r in catalog if r['id']==key) for key in base]
        text(575,y+68,' · '.join(labels),27,INK)
    rect(90,2312,2220,182,'#fff7ed','#ebdac8',12)
    text(116,2354,'17 组扩展示例，也能逐一找到归属',29,ORANGE,700)
    lines(116,2397,[
        '派生 11：令牌刷新时序、平台总览纵向、数据湖、蜂群、气泡、排名变化、山脊、坡度、可追溯模块树、四象限情景矩阵、终端循环。',
        '动画 3：策略轨迹、队列瓶颈、安全路径。　导入 3：draw.io、Mermaid、Excalidraw 重绘。',
        '版本口径：49 组三版本 × 3 + 8 个单独版本 = 155 文件；浅色、深色与完整页面不增加基础图型。',
    ],25,INK,39)

    heading(2569,'04','实际绘图：六步完成，核对后再交付','首次使用先确定品牌与中文字体；内容复杂时拆分总览和细节，保留事实来源与合并说明。')
    instructions=[('提供事实','节点、边、原始数据、单位和资料来源。'),('明确读者','读者是谁？看完要理解或决定什么？'),('选择表达','先确定行为含义，再选择图型与方向。'),('设定约束','格式、尺寸、细节量、受众与品牌样式。'),('生成与核对','核对事实、数字、连线、字重、遮挡和字体。'),('迭代与输出','按反馈调整；保存源文件与内容取舍记录。')]
    for i,(title,body) in enumerate(instructions):
        x=90+(i%3)*750;y=2648+(i//3)*115
        rect(x,y,720,97,'white','#d4e0e7',12)
        text(x+23,y+36,f'{i+1}  {title}',30,TEAL,700)
        text(x+23,y+76,body,26,INK)
    rect(90,2894,2220,122,NAVY,r=14)
    text(116,2935,'需求模板',26,'#94e0d7',700)
    text(300,2935,'“基于这些资料 / 源文件，为【受众】解释【问题】，选用【图型】，输出【尺寸、格式、主题】；',29,'white')
    text(300,2982,'必须保留【关键事实与关系】，可合并【次要细节】，列出删减项与待核实项。”',29,'white')

    heading(3091,'05','与我们研究过的工具，怎样分工？','依据已有研究记录比较职责；这些工具有能力重叠，下面的流程是可扩展方案，尚未自动接通。')
    for x,title,body,color in [
        (90,'Graphify',['提取关系、建图与查询','适合寻找项目事实线索','静态关系需结合实际核实'],TEAL),
        (651,'Archify',['交互探索架构、路径与差异','适合上下游探索与交接','帮助定位来源与查看关联'],BLUE),
        (1212,'Fireworks',['技术图生成与工程约束','适合工程配图及格式交付','部分流程有原生生成器'],BLUE),
        (1773,'Diagram Design',['信息取舍、版式、品牌与重绘','适合研究说明与面向读者的汇报','与 Fireworks 有较多重叠'],ORANGE),
    ]:card(x,3167,537,191,title,body,color)
    rect(90,3378,2220,59,'#e0f1ef',r=10)
    text(116,3417,'我们的组合方向：资料 / 代码 → 提取关系 → 人 / AI 核实 → 选图与图形制作 → 按读者调整 → 发布研究说明',29,TEAL,600)

    heading(3512,'06','价值、证据与下一步：知道能做什么，也知道验证到哪里','直接用途：研究配图、方案汇报、教学解释、流程交接和旧图整理；判断质量要同时看内容与画面。')
    card(90,3590,720,244,'已完成的研究验证',[
        '155 个原版：结构 / 部分遮挡检查通过。',
        '8 个中文案例：生成、导出并目视检查。',
        '3 种简单输入：均提取 6 节点、5 关系。',
        '复杂导入与逐张原版视觉验收尚未覆盖。',
    ])
    card(840,3590,720,244,'交付时怎样选格式',[
        'HTML：页面阅读，可承载交互 / 动画。',
        'SVG：独立矢量图，可编辑、放大清晰。',
        'PNG：静态像素图，便于插入文档。',
        '单图导出不含页面外围摘要；检查字体。',
    ],BLUE)
    card(1590,3590,720,244,'扩展建议 · 按优先级推进',[
        '① 固定中文字体、术语、配色与模板。',
        '② 接入关系来源，保留稳定 ID 与证据。',
        '③ 批量更新、版本对比与人工审核。',
        '④ 同题比较耗时、修改次数与理解效果。',
    ],ORANGE)
    lines(94,3880,[
        '能力边界：检查通过不证明业务事实正确；旧图重绘保留内容结构的目标需逐项核对，不保证原坐标、样式或复杂语法完整还原。',
        '当前展厅展示已保存的示例，切换不调用模型；本库依赖宿主 AI，不是独立模型服务，也没有覆盖所有图型的通用自动布局引擎。',
    ],26,MUTED,42)
    line(90,3954,2310,3954)
    text(94,3998,'来源：cathrynlavery/diagram-design · 插件清单 v2.6.23 · ce9344c52cb9 · MIT ｜ 本地固定版本研究 · 2026-09-16',25,MUTED)
    text(94,4045,'阅读路径：分清维度 → 理解技术 → 按问题选型 → 提供内容与约束 → 核对与交付 → 逐步扩展',27,TEAL,600)
    parts.append('</g></svg>')
    svg=ROOT/'assets/diagram-design-overview-v2.svg'
    svg.write_text('\n'.join(parts),encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':W,'height':H},device_scale_factor=1.5)
        page.goto(svg.as_uri());page.evaluate('document.fonts.ready')
        bounds=page.locator('text').evaluate_all('els=>els.map(e=>{const b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height}})')
        overflow=[b['text'] for b in bounds if b['x']<0 or b['x']+b['w']>W-65 or b['y']+b['h']>H-20]
        overlaps=[]
        for i,a in enumerate(bounds):
            for b in bounds[i+1:]:
                if min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>1 and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>1:
                    overlaps.append([a['text'],b['text']])
        if overflow or overlaps:
            print(json.dumps({'overflow':overflow,'overlap':overlaps},ensure_ascii=False))
        assert not overflow and not overlaps
        page.locator('svg').screenshot(path=str(svg.with_suffix('.png')))
        browser.close()
    size=Image.open(svg.with_suffix('.png')).size
    assert size==(3600,6165)
    assert sum(len(k.split()) for _,_,k in TYPE_GROUPS)==40 and len(catalog)==57 and len(EXTRAS)==17
    report={'revision':2,'png_size':size,'text_count':len(bounds),'text_overlaps':overlaps,'text_overflow':overflow,'base_types':40,'example_groups':57,'sources':['notes/analysis.md','notes/taxonomy.md','notes/experiments.md','upstream/skills/diagram-design/SKILL.md']}
    (ROOT/'evidence/overview-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
