"""One explicit inventory for authored diagrams and preserved upstream examples."""
from pathlib import Path
from html import escape
from catalog_data import rows

ROOT=Path(__file__).resolve().parents[1]
CASES=[
    ('research-blue','中文研究流程 · 蓝色','资料 → 提取 → 核实 → 图规格 → 生成 → 检查交付；六节点、五关系。'),
    ('research-orange','同结构 · 橙色','保持内容、坐标和字号，仅调整颜色角色。'),
    ('research-dark','同结构 · 深色','保持内容与布局，调整深色背景下的对比度。'),
    ('research-full','完整解释页面','图形配标题、摘要与边界说明；SVG/PNG 仅导出图形。'),
    ('research-executive','管理者概览 · 三阶段','将六个节点成对归并为理解资料、确认表达、制作交付，保留归并记录。'),
    ('research-slide','幻灯片 · 16:9','同一六节点流程重新排成横向单行，画布 1600×900。'),
    ('research-sketchy','手绘线条','给形状和连线添加轻微手绘效果，文字保持清晰。'),
    ('research-annotation','边注强调','增加解释性批注；批注引导线不表示业务关系。'),
]
OVERVIEWS=[
    ('diagram-design-overview-v2','理解总览 · 第二版（推荐）','补全按问题选图、8 种语义模式、17 组扩展示例、历史工具分工、验证范围与扩展次序。','3600×6165'),
    ('diagram-design-overview','理解总览 · 第一版','原理、三个维度、七类图型、绘图六步、交付格式、场景与扩展方向。','3000×5055'),
]

def inventory_markdown():
    out=['# 全部绘图与交付清单','',
         '本次 AI 编写 **8 版中文案例 + 2 版理解总览图**；另原样归档 **57 组上游示例、155 个 HTML 文件**。同内容的主题、尺寸与详略版本不代表新的独立图型。','',
         '## 本次绘制：两版理解总览','',
         '| 图 | 内容 | PNG 尺寸 | 文件 |','|---|---|---|---|']
    for key,title,description,size in OVERVIEWS:
        out.append(f'| {title} | {description} | {size} | [PNG](../assets/{key}.png) · [SVG](../assets/{key}.svg) |')
    out+=['','## 本次绘制：八版中文研究流程','',
          '| 图 | 展示内容 | 文件 |','|---|---|---|']
    for key,title,description in CASES:
        links=' · '.join(f'[{ext.upper()}](../cases/{key}.{ext})' for ext in ('html','svg','png'))
        out.append(f'| {title} | {description} | {links} |')
    out+=['','中文案例 PNG 通常为 2560×1440，幻灯片版为 3200×1800；8 组共 24 个 HTML/SVG/PNG 文件。完整页面的单图 PNG 与蓝色版相同，页面摘要只在 HTML 中显示。','',
          '## 辅助图片与输入','',
          '- [八例联系表](../assets/case-contact-sheet.jpg)：八张中文 PNG 的缩略汇总，便于比较。',
          '- [研究流程封面](../assets/research-workflow.png)：蓝色案例 PNG 的副本，不另计新图。',
          '- 三种导入实验源文件：[Mermaid](../inputs/research.mmd)、[draw.io](../inputs/research.drawio)、[Excalidraw](../inputs/research.excalidraw)。它们表达同一份六节点、五关系内容。','',
          '## 原样归档：57 组上游示例','',
          '来自 Cathryn Lavery / diagram-design 固定提交 ce9344c52cb9，保留 MIT 许可；这些图不是本次原创。40 基础 + 11 派生 + 3 动画 + 3 导入 = 57 组。','',
          '| 分类 | 示例 | 层级 | 解决的问题 | 原版文件 |','|---|---|---|---|---|']
    for item in rows():
        variants=[]
        for suffix,label in [('', '浅色 / 单独版本'),('-dark','深色'),('-full','完整页面')]:
            file=f'example-{item["id"]}{suffix}.html'
            if (ROOT/'upstream/skills/diagram-design/assets'/file).exists():
                variants.append(f'[{label}](../upstream/skills/diagram-design/assets/{file})')
        out.append(f'| {item["category"]} | {item["name"]} | {item["kind"]} | {item["question"]} | {" · ".join(variants)} |')
    out+=['','总计 49 组三版本 × 3 + 8 个单独版本 = 155 个 HTML 文件；原版内容和样式未经修改。',
          '', '[图型分类](taxonomy.md) · [研究原理](analysis.md) · [验证记录](experiments.md)', '']
    return '\n'.join(out)

def inventory_html():
    esc=escape
    out=['<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>全部绘图清单 · Diagram Design</title><meta name="description" content="2版理解总览、8版中文案例和57组155个原版示例的完整内容与下载清单。"><link rel="stylesheet" href="style.css"></head><body><main class="reading">',
         '<p><a href="index.html#overview">← 返回研究总览</a></p><h1>全部绘图与交付清单</h1>',
         '<p>本次绘制 8 版中文案例、2 版理解总览；原样归档 57 组上游示例、155 个 HTML。配色、尺寸、详略版本不增加基础图型数量。</p>',
         '<h2>两版理解总览</h2><div class="two-column">']
    for key,title,description,size in OVERVIEWS:
        out.append(f'<article class="text-card"><h3>{esc(title)}</h3><a href="assets/{key}.svg" target="_blank" rel="noopener"><img class="overview-image" loading="lazy" src="assets/{key}.png" alt="{esc(description)}"></a><p>{esc(description)}</p><p>PNG：{size}</p><div class="links"><a href="assets/{key}.png" download>下载 PNG</a><a href="assets/{key}.svg" download>下载 SVG</a></div></article>')
    out+=['</div><h2>八版中文研究流程</h2><div class="table-scroll"><table><thead><tr><th>图</th><th>展示内容</th><th>文件</th></tr></thead><tbody>']
    for key,title,description in CASES:
        links=' · '.join(f'<a href="cases/{key}.{ext}"'+(' download' if ext!='html' else '')+f'>{ext.upper()}</a>' for ext in ('html','svg','png'))
        out.append(f'<tr><td>{esc(title)}</td><td>{esc(description)}</td><td>{links}</td></tr>')
    out+=['</tbody></table></div><p>共 24 个 HTML/SVG/PNG 文件。常规 PNG 为 2560×1440，幻灯片为 3200×1800；完整页面单图与蓝色图相同，外围摘要在 HTML 查看。</p>',
          '<p><a href="assets/case-contact-sheet.jpg">八例联系表</a> · <a href="assets/research-workflow.png">蓝色图封面副本</a> · <a href="inputs/research.mmd" download>Mermaid 输入</a> · <a href="inputs/research.drawio" download>draw.io 输入</a> · <a href="inputs/research.excalidraw" download>Excalidraw 输入</a></p>',
          '<h2>57 组上游原版：40 基础 + 11 派生 + 3 动画 + 3 导入</h2><p>以下图形来自 Cathryn Lavery / diagram-design 固定提交 ce9344c52cb9，保留原始内容与样式；详见 <a href="vendor/LICENSE">MIT 许可</a>。使用 <a href="index.html#gallery">图形展厅</a>按类型筛选。</p>',
          '<div class="table-scroll"><table><thead><tr><th>分类</th><th>示例</th><th>层级</th><th>说明</th><th>文件</th></tr></thead><tbody>']
    for item in rows():
        variants=[]
        for suffix,label in [('', '浅色 / 单独版'),('-dark','深色'),('-full','完整页')]:
            file=f'example-{item["id"]}{suffix}.html'
            if (ROOT/'upstream/skills/diagram-design/assets'/file).exists():
                variants.append(f'<a href="vendor/{file}">{label}</a>')
        out.append('<tr>'+''.join(f'<td>{esc(item[k])}</td>' for k in ('category','name','kind','question'))+f'<td>{" · ".join(variants)}</td></tr>')
    out+=['</tbody></table></div><p>49 组三版本 × 3 + 8 个单独版本 = 155 文件。动画演示保留原控制器；SVG/PNG 是单图导出。</p><p><a href="index.html#evidence">查看验证范围与来源</a> · <a href="notes/drawings.md" download>下载 Markdown 清单</a></p></main></body></html>']
    return '\n'.join(out)
