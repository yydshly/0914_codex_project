"""Write study documentation and an exact specimen index."""
from pathlib import Path
from catalog_data import rows, TYPE_GROUPS

ROOT=Path(__file__).resolve().parents[1]
DOCS={
'README.md':'''# 005 · Diagram Design：图形设计规范与效果展厅

让 AI 根据文字、数据或旧图源文件，按设计规范生成可编辑的 HTML/SVG，并导出 PNG。覆盖架构、流程、层级、数据模型、时间规划、策略关系和数值统计七类 40 种基础图型；支持品牌样式、分步动画及 draw.io / Mermaid / Excalidraw 重绘。适合研究说明、方案汇报、教学和流程交接。

[在线研究展厅](https://yydshly.github.io/0914_codex_project/005-diagram-design/) · [所有绘图与下载](https://yydshly.github.io/0914_codex_project/005-diagram-design/drawings.html) · [全部绘图记录](notes/drawings.md) · [详细理解](notes/analysis.md) · [绘图技术原理](notes/drawing-technology.md) · [按类型分类](notes/taxonomy.md) · [完整图型清单](notes/gallery.md) · [实验记录](notes/experiments.md) · [上游](https://github.com/cathrynlavery/diagram-design)

## 一图理解：原理、选型与绘图方法

![Diagram Design 第二版理解总览：技术流程、语义模式、40种基础图型、57组示例、绘图步骤、工具分工与验证范围](assets/diagram-design-overview-v2.png)

[第二版高清 PNG](assets/diagram-design-overview-v2.png) · [第二版可编辑 SVG](assets/diagram-design-overview-v2.svg) · [第一版 PNG](assets/diagram-design-overview.png) · [第一版 SVG](assets/diagram-design-overview.svg)

图型、表现方式与输入来源是三个可组合维度。比如：Mermaid 源文件 → 提取流程关系 → 重绘为深色流程图 → 添加分步动画 → HTML 演示或静态 PNG 分享。主要产物是矢量图代码，PNG 是渲染后的图片。

## 所有绘制的图有哪些？

- **两版理解总览**：第一版梳理原理、分类、步骤和用途；第二版补全选图问题、8 种语义模式、17 组扩展示例、工具分工与验证边界。
- **八版中文案例**：研究流程蓝色、橙色、深色、完整解释页面、管理者三阶段概览、16:9 幻灯片、手绘线条、边注强调；每版均提供 HTML / SVG / PNG。
- **辅助图片**：八例联系表；蓝色案例的研究流程封面副本。封面副本和联系表不另计原创图型。
- **上游原版**：57 组、155 个 HTML，原样归档，保留作者和许可，内容不属于本次原创。

完整名称、表达内容、格式、尺寸与文件入口见[全部绘图清单](notes/drawings.md)。

## 中文研究案例

![中文流程：资料、提取、核实、图规格、生成与检查交付](assets/research-workflow.png)

这张图由本次 AI 按 Diagram Design 规范编写，是我们的建议研究流程；不表示库已经实现自动分析代码到交付的整条流水线。

## 本次成果

| 内容 | 实际范围 |
|---|---|
| 原版全量效果 | 57组、155个HTML：49组三版本，8个单独版本 |
| 中文图型导航 | 架构与部署、流程与交互、层级与组织、数据模型与依赖、时间与工作规划、策略与关系分析、数值与统计 |
| 理解总览 | 两版 SVG / PNG：原理、分类、绘图方法、工具分工和验证边界 |
| 中文对照案例 | 蓝色、橙色、深色、完整页面、三阶段概览、16:9幻灯片、手绘线条、边注，共8版 |
| 导入实验 | 同一份6节点5关系，用Mermaid、draw.io、Excalidraw源文件跑上游提取器 |
| 导出 | 8组HTML/SVG/PNG；常规PNG 2560×1440，幻灯片3200×1800 |
| 清单与检查 | 155个原版与8个案例通过self_check及标签遮挡检查；模块元数据导出与检查 |
| 工具对照 | Fireworks、Archify、Graphify的定位、原理和我们该如何使用 |

**57组是示例组数，不是57个独立图型或绘图引擎。** 按固定Skill图型表和原版样例核对：40个基础图型、11个派生示例、3个动画、3个导入重绘。分为七类，可按类型和示例层级筛选。原版示例保留英文与原始样式；中文案例是本次AI创作。

展厅部署为 GitHub Pages 静态研究页面，也可本地运行：切换的是已保存结果，没有在线模型、实时绘图和自动仓库扫描服务。

## 能力、输入与输出

输入可以是用户描述、整理好的系统关系、数据或支持的图形源文件。事实由用户或外部AI确认；Skill帮助选择图型、读取规范、编写布局。脚本辅助提取结构与检查；浏览器完成渲染。

输出以单文件HTML和内联SVG为基础，可导出PNG。完整版包含页面摘要等外围内容；PNG/SVG单图导出不包含这些内容。原版可引用Google Fonts，单文件并不保证字体完全离线一致。

## 与过去研究的关系

- **Fireworks**：最直接的同类，JSON绘图、连线路由、工程规则与图片交付是我们已验证的重点。
- **Archify**：更适合点击探索架构、上下游、路径、源码关联与模型差异。
- **Graphify**：更上游的关系提取和图查询。
- **Diagram Design**：适合把确认后的内容整理成面向读者、风格一致的图和解释页面。

建议组合仍未接通，没有跨工具效率排名。当前优先验证中文规范、复杂信息的取舍与旧图重绘对研究交付的价值。

## 版本与许可

| 项目 | 内容 |
|---|---|
| 固定提交 | `ce9344c52cb9be811de187bf2a6d58c712c9c9fe` |
| 插件版本 | 2.6.23（Skill metadata另写2.6） |
| 日期 | 2026-09-16 |
| 上游许可 | [MIT，Cathryn Lavery](upstream/LICENSE) |
| 第三方素材 | [图标及商标来源](upstream/THIRD_PARTY_LICENSES.md) |
| 本次方式 | 本地复制所需Skill与示例；未全局安装插件 |
| 线上地址 | https://yydshly.github.io/0914_codex_project/005-diagram-design/ |

## 复现

从研究总仓库根目录运行。构建展厅只需Python标准库，已保存的图形与PNG可以直接复用。

```powershell
python projects/005-diagram-design/src/build.py
python projects/005-diagram-design/src/verify_site.py
python -m http.server 8785 --bind 127.0.0.1 --directory projects/005-diagram-design/web/dist
```

打开 <http://127.0.0.1:8785/>；也可以直接打开本地HTML。

重新制作案例与导入、检查实验：

```powershell
python projects/005-diagram-design/src/make_cases.py
python projects/005-diagram-design/src/experiments.py
python projects/005-diagram-design/src/export_cases.py
python projects/005-diagram-design/src/build.py
```

`export_cases.py`需要已安装Playwright、Chromium和Pillow。本次复用了现有环境，没有安装新系统依赖。它只渲染独立图形资产，不是展厅截图。`verify_site.py`额外使用Pillow和Node进行资产与语法检查。

## 验证边界

- 三个简单源文件核对了节点ID、名称和关系；不代表复杂或不受支持的语法全部可靠。
- 全量原版运行了结构与标签遮挡检查；没有逐张目视验收155个原版文件。
- 8张中文PNG导出并核对像素尺寸，已查看联系表；不保证其他设备字体相同。
- 完成静态资源、脚本语法和输出完整性检查；另用 Chromium 验证七个导航面板、分类筛选、版本切换、八个案例、绘图清单与手机端宽度。不是全套跨浏览器测试。
- 没有验证网站自动品牌提取、全局Profile管理、安装兼容性或真实业务事实。

## 目录

- `upstream/`：固定版本所需原版Skill、示例、检查工具与许可。
- `web/`：展厅源码；`web/dist/`为可重新生成的静态输出。
- `src/`：本次构建、案例、实验、导出和检查程序。
- `inputs/`：三类源文件与内容说明。
- `cases/`：本次中文HTML、SVG、PNG。
- `evidence/`：提取器结果、检查、清单与PNG记录。
- `notes/`：原理、区别、场景、扩展、样式与图型清单。
- `assets/`：两版理解总览的 SVG/PNG、研究流程封面与案例联系表。

[返回总索引](../../README.md)
''',
'notes/analysis.md':'''# Diagram Design：我们的理解

## 结论

Diagram Design把选图、信息取舍、品牌样式、布局、检查和导出封装成Agent Skill、参考文档、HTML/SVG模板与Python辅助脚本。价值集中在把已经理解的内容变成清晰、统一、可交付的图形。

它和此前研究的Fireworks高度重叠；对我们新增的价值主要是产品策略与数据图形、旧图重绘、完整解释页面、品牌配色及按受众调整表达。没有证据证明它整体优于Fireworks，没有完成效率或读者理解率的跨工具评测。

## 固定研究版本与统计

上游提交 `ce9344c52cb9be811de187bf2a6d58c712c9c9fe`，插件清单版本2.6.23。README、核心Skill、图库的统计口径不完全一致。实际收录57组、155个HTML，49组三版本与8个单独版本。包含派生布局、特定领域案例和动画，不能理解成57类独立绘图引擎。

原版文件保存在 `upstream/skills/diagram-design/`。只保留研究需要的Skill及两项仓库检查工具，没有复制整个仓库的维护系统。

## 能力与场景

| 能力 | 适合场景 | 实现与限制 |
|---|---|---|
| 系统、流程、组织和数据平台图 | 项目架构、流程交接、数据治理 | AI选择图型、编写内容与布局 |
| 产品策略图 | 用户旅程、需求切片、优先级、情景规划 | 不自动调查真实用户或证明评分 |
| 数据比较图 | 趋势、分布、比例、流量和增减 | 数据与口径由用户或外部分析提供 |
| 浅色/深色/完整页面 | 文档、网页、汇报 | 摘要不包含在单图导出中 |
| 三类源文件导入 | 旧技术图、文档Mermaid、白板整理 | 提取结构后重绘，不保留原坐标和样式 |
| 品牌样式 | 系列研究、客户内容 | 可按网站提取规范或手动配置；本次仅手动配色 |
| 动画、终端、手绘与批注 | 顺序讲解、开发者文章、解释性边注 | 不能等同于通用动画视频系统 |
| HTML/SVG/PNG | 页面、矢量资产、汇报图片 | 字体与渲染环境影响输出 |
| 模块元数据清单 | 可追溯的功能树 | 导出现有属性，不自动发现源码 |

## 原理：谁在做什么

1. **事实来自用户、资料或外部AI。** 本库依赖宿主模型；不会独立理解任意项目并保证结论真实。
2. **Skill负责路由。** 判断是否值得画图，选择语义模式与图型，按需加载规范。
3. **语义模式负责含义。** 队列、规则轨迹、信任边界等描述行为；图型再决定排布。
4. **设计系统负责一致性。** 背景、正文、次要文字、焦点等颜色角色；节点密度、间距、字体与连线约束。
5. **AI负责实现。** 按模板编写HTML/CSS/SVG；部分类型提供参数与坐标公式，但仍需作者执行，不等于已有统一自动布局程序。
6. **提取器负责读源文件。** 输出节点、关系、分组、方向及复杂度提示，本身不生成重绘成品。
7. **脚本与人工分别检查。** self_check检查无障碍标记、外部引用和动画结构；verify-geometry用启发式规则找部分标签遮挡。不能证明业务含义或覆盖所有视觉问题。
8. **浏览器负责渲染。** HTML直接打开，SVG保存矢量，PNG按画布和比例渲染。

### 八种语义模式

队列与瓶颈、固定语义槽位的阶段框架、散乱输入到结构化产物、双路径策略轨迹、安全路径、治理控制目录、补偿性安全分层、可追溯模块分解。它们和布局是不同维度，不能相加为图型数量。

### 导入的四个调整维度

- 格式：HTML、SVG、PNG、HTML+PNG。
- 尺寸：文档、16:9/4:3幻灯片、社交图片、横向打印等；同时影响字阶。
- 详细程度：faithful、balanced、simplified；存在节点预算，超出需要分区或拆图。
- 受众：工程师、混合受众、管理者；主要改变措辞，不自动决定事实删减。

本次用一个简单六节点流程作可核实基准，不能推导出任意复杂导入都可靠。

## 历史研究对照

| 工具 | 核心职责 | 我们的用途 |
|---|---|---|
| Graphify | 从受支持源码/资料抽取关系、建图与查询 | 陌生项目的事实线索、路径与影响分析 |
| Archify | 架构交互探索、来源链接、路径与模型差异 | 讲解交接、探索上下游 |
| Fireworks | 技术图生成、路由、风格、工程约束 | 工程技术配图与多格式交付 |
| Diagram Design | 信息取舍、视觉布局、品牌、旧图重绘 | 面向读者的研究配图 |

Fireworks历史研究覆盖33个图型与领域条目、12种风格；15项原生JSON生成，18项AI按规范绘制后导出，后者含3项近似适配。已有合规JSON时，一部分流程可以不调用模型。数量不是独立专用引擎数量。

Archify已研究五类图、源码定位、上下游/路径、模型差异；比较的是已提供的两个规格，不能等同于自动解读Git diff。

Graphify的FastAPI历史实验使用代码解析提取关系；静态关系不等于运行轨迹。这次没有重跑旧项目，比较以固定研究记录为准，不断言最新版本缺少某功能。

Video TalkCraft、纸艺剧场与Vibe Motion侧重有时间轴的动画或视频。Diagram Design默认提供静态图与解释页面。

## 对我们的意义与扩展方向

我们持续研究GitHub项目，反复需要解释能力、原理、输入输出和使用场景。它可以提供统一中文配图规范，以及把复杂材料拆成总览和细节的方法。

1. **中文字体与研究主题**：固定字号、术语和配色，检查长标题与跨平台字体。
2. **领域模板**：沉淀研究流程、Agent、审批与数据链路。
3. **同题比较**：同一份有来源资料分别出图，记录修改次数、时间与读者任务完成情况。
4. **关系提取到图形**：Graphify → 人/AI核实 → Diagram Design或Fireworks；需要实体映射与来源保留。
5. **随内容更新**：稳定ID、变更检测与审核；尚未实现。
6. **知识关联**：借助模块元数据扩展到文档、代码和负责人导航；完整系统需要额外开发。

目前完成的是研究展厅和受控案例，没有接通自动化流水线，也没有量化成本或商业回报结论。

## 来源

- [上游固定版本](https://github.com/cathrynlavery/diagram-design/tree/ce9344c52cb9be811de187bf2a6d58c712c9c9fe)
- [核心规范](../upstream/skills/diagram-design/SKILL.md)
- [Fireworks历史研究](https://yydshly.github.io/0915_codex_project/003-fireworks-tech-graph/)
- [Archify历史研究](https://yydshly.github.io/0909_codex_project/projects/003-archify/)
- [Graphify历史研究](https://yydshly.github.io/0911_codex_project/009-graphify/)
''',
'notes/experiments.md':'''# 实验与验证

## 全量原版示例

57组、155个HTML：49组三版本，另8个单独示例。上游 `self_check.py` 155/155通过，仓库 `verify-geometry.py` 155/155通过。原版未修改，逐文件SHA-256已保存。

前者检查SVG可访问性、外部引用、控制器等；后者主要检查特定矩形标签被节点覆盖。两项通过不是完整视觉或事实验收。没有逐张目视验收原版155文件。

## 三种源文件等价提取

输入：原始资料 → 提取关系 → 核实事实 → 整理图规格 → 生成图形 → 检查与导出。

| 格式 | 上游提取器 | 结果 |
|---|---|---|
| Mermaid .mmd | mermaid_extract.py | 6节点5关系，ID、名称、起终点与预期一致 |
| draw.io原始XML | drawio_extract.py | 同上 |
| Excalidraw JSON | excalidraw_extract.py | 同上；绑定文字被合并到节点 |

保存了stdout/stderr、JSON结构与Markdown摘要。本次没有使用压缩draw.io、PNG/SVG嵌入图、复杂Mermaid分支或复杂白板。

提取成功不等于自动重绘。中文结果由本次AI根据同一份内容与规范编写；案例生成脚本是本研究代码，不是上游新增的通用渲染器。

## 八个中文实验

蓝色、橙色、深色三版仅改变颜色角色；完整页面增加摘要；三阶段概览成对归并六个节点并记录ledger；16:9幻灯片重新布局；手绘按上游滤镜仅处理形状；边注增加解释而不改变业务关系。

8例都通过结构与标签遮挡检查。配色手动指定，未运行网站抓取和全局Profile管理。

## 导出与视觉检查

独立SVG经Playwright/Chromium两倍渲染。7张PNG是2560×1440，幻灯片3200×1800，逐一回读尺寸验证。字体使用本机Microsoft YaHei及后备栈；不保证其他平台相同。

已查看八例PNG联系表，文字完整，无明显裁切。完整页面的PNG与蓝色版图形相同，是单图导出的预期行为；摘要在HTML中查看。

## 模块清单

读取上游 `example-tree-block-decomposition.html` 的现有data-block-*属性，按export-registry规范输出JSON，并运行上游verify-block-registry检查。导出程序由本次编写，元数据来自原版，未验证示例代码路径在真实项目中存在。

## 展厅检查

静态入口、引用、全量样例覆盖、哈希、8组下载、两版总览、SVG XML、PNG尺寸和JS语法检查。新增绘图清单覆盖155个原版文件与24个案例文件。Chromium 实测七个导航面板、分类筛选、主题版本切换、八个案例入口及独立清单；390px手机视口没有整页横向溢出。已查看桌面与手机端总览截图。未完成所有示例逐一交互和多浏览器测试。

## 原始证据

- [全量检查](../evidence/verification.json)
- [网页交互检查](../evidence/browser-check.json)
- [导入总记录](../evidence/import-summary.json)
- [保真清单](../evidence/fidelity-ledger.json)
- [PNG记录](../evidence/png-export.json)
- [模块元数据](../evidence/block-registry.json)
- [案例联系表](../assets/case-contact-sheet.jpg)
'''
}

def main():
    for name,content in DOCS.items():
        path=ROOT/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8',newline='\n')
    lines=['# 全量示例索引','', '57组示例，155个HTML。派生布局和特殊版本单独列出；不是独立引擎数量。','', '| 分类 | 图形 | 表达的问题 | 适用场景 | 版本 |','|---|---|---|---|---|']
    for r in rows():
        triple=(ROOT/'upstream/skills/diagram-design/assets'/f'example-{r["id"]}-dark.html').exists()
        lines.append(f'| {r["category"]} | [{r["name"]}](../upstream/skills/diagram-design/assets/example-{r["id"]}.html) | {r["question"]} | {r["use"]} | '+('浅色/深色/完整' if triple else '特殊版本')+' |')
    (ROOT/'notes/gallery.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    items=rows()
    lines=['# 按图形类型分类','','基础图型依照固定版本SKILL的40项选择表。七类与归属是本研究的导航分类，按主要表达对象分组，不排斥跨场景使用。','','40基础 + 11派生 + 3动画 + 3导入 = 57组。浅色、深色和完整页面是视觉版本，不增加图型数量。','', '| 类别 | 基础图型数 | 含扩展的示例组数 | 基础图型 |','|---|---:|---:|---|']
    for name,question,keys in TYPE_GROUPS:
        group=[x for x in items if x['category']==name]
        lines.append(f'| {name} | {len(keys.split())} | {len(group)} | '+ '、'.join(x['name'] for x in group if x['kind']=='基础图型')+' |')
    lines.extend(['','## 17个扩展示例怎样归类？','','“归入”表示本研究的阅读导航关系，不表示上游存在继承式渲染器API。导入示例根据最终图形归类，输入格式本身不是图型。','','| 扩展示例 | 层级 | 归入基础图型 |','|---|---|---|'])
    for item in items:
        if item['kind']!='基础图型':lines.append(f'| {item["name"]} | {item["kind"]} | {item["familyName"]} |')
    (ROOT/'notes/taxonomy.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Wrote README, analysis, experiments and complete specimen index')

if __name__=='__main__':main()
