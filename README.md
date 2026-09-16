# GitHub 项目研究集

记录值得研究的优秀 GitHub 项目：理解设计思路、复现关键能力、沉淀实践笔记，并按需提供 Web 演示。

这里是研究总仓库。每个子项目独立保存源码实验、研究记录和图片；本页提供摘要和有序入口。

## 项目索引

编号是永久标识；展示顺序由 `projects.json` 的 `order` 决定。调整顺序不需要重命名目录。

<!-- PROJECT_INDEX:START -->
| 顺序 | 编号 | 项目 | 源库 | 能力摘要 | 状态 | 演示 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 001 | [语音驱动纸艺剧场](projects/001-audio-locked-paper-theatre/README.md) | [audio\-locked\-paper\-theatre](https://github.com/jay-yangPY/audio-locked-paper-theatre) | 画板是舞台，物品是演员，代码是动作脚本，音频时间轴是演出节拍。用于培训视频制作、教学微课、科普与产品说明，附四个有声演示和场景指南。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/001-audio-locked-paper-theatre/) |
| 2 | 002 | [Agent Skills Eval：Skill 能力校验引擎](projects/002-agent-skills-eval/README.md) | [agent\-skills\-eval](https://github.com/darkrishabh/agent-skills-eval) | 读取已编写的 Skill 与测试标准，自动调用模型、评分并对比有无 Skill 的效果，为校验能力 Skill 提供底层评测引擎。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/) |
| 3 | 003 | [Video TalkCraft：口播视频制作 Skill](projects/003-video-talkcraft/README.md) | [video\-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | 将口播稿、成品配音和素材组织为逐字同步的动效视频及可编辑工程；可复用到培训、产品讲解与系列口播，统一表达风格并支持局部修改。附输入准备、选卡原理与一致性指南。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/003-video-talkcraft/) |
| 4 | 004 | [Vibe Motion：AI 驱动的代码动画工具集](projects/004-vibe-motion/README.md) | [vibe\-motion](https://github.com/vibe-motion) | 把 AI 编写代码与动画引擎连接，让二维、三维和动效成为可编辑、可复用、可批量渲染的工程，适合教学、产品讲解与数据展示；附技术引导图、交互示例及 SRT 语义分镜原理。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/004-vibe-motion/) |
| 5 | 005 | [Diagram Design：图形设计规范与效果展厅](projects/005-diagram-design/README.md) | [diagram\-design](https://github.com/cathrynlavery/diagram-design) | 让 AI 将文字、数据或旧图源文件绘制为可编辑 HTML/SVG 并导出 PNG，覆盖七类 40 种基础图型，支持品牌、动画和三格式重绘；附 57 组 155 个原版示例、8 版中文案例、2 版理解总览及完整绘图清单。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/005-diagram-design/) |
<!-- PROJECT_INDEX:END -->

## 项目预览

<!-- PROJECT_PREVIEWS:START -->
### 001 · 语音驱动纸艺剧场

画板是舞台，物品是演员，代码是动作脚本，音频时间轴是演出节拍。用于培训视频制作、教学微课、科普与产品说明，附四个有声演示和场景指南。

#### 理解图一：音频驱动动画的实现架构

画板是舞台，物品是演员，代码是动作脚本，音频时间轴是演出节拍。看清时间戳、动作规则、图层与视频合成之间的关系。

![讲稿、音频时间轴、动作脚本与独立图层共同驱动逐帧渲染的架构图](projects/001-audio-locked-paper-theatre/assets/audio-animation-architecture.png)

#### 理解图二：意义与使用场景

从培训视频制作、英语教学、学科微课到技术科普与产品说明，直观了解适用场景、制作流程及扩展边界。

![纸艺剧场的意义、八类代表用途、制作流程与能力边界](projects/001-audio-locked-paper-theatre/assets/library-overview.png)

#### 演示效果

![三条会议记录经纸艺机器整理为行动摘要](projects/001-audio-locked-paper-theatre/assets/cover.jpg)

[研究记录](projects/001-audio-locked-paper-theatre/README.md) · [上游仓库](https://github.com/jay-yangPY/audio-locked-paper-theatre) · [在线演示](https://yydshly.github.io/0914_codex_project/001-audio-locked-paper-theatre/)

标签：培训视频 / 教学微课 / MiniMax / 音频时间轴 / 纸艺动画

### 002 · Agent Skills Eval：Skill 能力校验引擎

读取已编写的 Skill 与测试标准，自动调用模型、评分并对比有无 Skill 的效果，为校验能力 Skill 提供底层评测引擎。

![Skill 能力校验闭环：用户与 AI 准备、评测引擎自动验证、人工复核后修改再测](projects/002-agent-skills-eval/assets/skill-validation-workflow.png)

[研究记录](projects/002-agent-skills-eval/README.md) · [上游仓库](https://github.com/darkrishabh/agent-skills-eval) · [在线演示](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/)

标签：Agent Skills / 自动评测 / LLM Judge / 可复现实验

### 003 · Video TalkCraft：口播视频制作 Skill

将口播稿、成品配音和素材组织为逐字同步的动效视频及可编辑工程；可复用到培训、产品讲解与系列口播，统一表达风格并支持局部修改。附输入准备、选卡原理与一致性指南。

![Video TalkCraft 理解图：输入、选卡分镜、组装输出、三层一致性、八项约束与修改回退](projects/003-video-talkcraft/assets/video-talkcraft-workflow.png)

[研究记录](projects/003-video-talkcraft/README.md) · [上游仓库](https://github.com/Vincentwei1021/video-talkcraft) · [在线演示](https://yydshly.github.io/0914_codex_project/003-video-talkcraft/)

标签：口播视频 / Remotion / 音画同步 / 动效研究

### 004 · Vibe Motion：AI 驱动的代码动画工具集

把 AI 编写代码与动画引擎连接，让二维、三维和动效成为可编辑、可复用、可批量渲染的工程，适合教学、产品讲解与数据展示；附技术引导图、交互示例及 SRT 语义分镜原理。

![Vibe Motion 技术引导图：二维、三维、动效技能及 SRT 语义分镜到代码渲染视频的实现原理](projects/004-vibe-motion/assets/technology-map.png)

[研究记录](projects/004-vibe-motion/README.md) · [上游仓库](https://github.com/vibe-motion) · [在线演示](https://yydshly.github.io/0914_codex_project/004-vibe-motion/)

标签：代码动画 / Three\.js / Remotion / Agent Skills

### 005 · Diagram Design：图形设计规范与效果展厅

让 AI 将文字、数据或旧图源文件绘制为可编辑 HTML/SVG 并导出 PNG，覆盖七类 40 种基础图型，支持品牌、动画和三格式重绘；附 57 组 155 个原版示例、8 版中文案例、2 版理解总览及完整绘图清单。

#### 理解总览：原理、选型与绘图方法

第二版总览解释这个库怎样绘图、如何选图、静态与动画及旧图重绘的关系，并汇总现有验证与扩展方向；两版原图和全部案例均可在项目页下载。

![Diagram Design 的技术流程、七类四十种图型、语义模式、绘图步骤、工具分工和验证范围](projects/005-diagram-design/assets/diagram-design-overview-v2.png)

#### 八种中文表达与视觉效果

同一份内容，比较配色、完整页面、详细程度、尺寸、手绘线条和边注；PNG为单图导出。

![中文研究流程的边注、蓝色、深色、概览、完整页面单图、橙色、手绘与幻灯片效果](projects/005-diagram-design/assets/case-contact-sheet.jpg)

#### 演示效果

![按 Diagram Design 规范编写的中文研究流程：资料、提取、核实、图规格、生成和检查交付](projects/005-diagram-design/assets/research-workflow.png)

[研究记录](projects/005-diagram-design/README.md) · [上游仓库](https://github.com/cathrynlavery/diagram-design) · [在线演示](https://yydshly.github.io/0914_codex_project/005-diagram-design/)

标签：图形设计 / HTML/SVG / Agent Skill / 旧图重绘 / 中文配图
<!-- PROJECT_PREVIEWS:END -->

## 开始研究

需要 Python 3.10 或更新版本，无第三方依赖。在仓库根目录运行：

```sh
python scripts/catalog.py add example-repo --name "示例项目" --repo "https://github.com/owner/example-repo" --summary "一句话说明值得研究的能力"
```

命令会分配下一个编号、创建研究目录、登记元信息并刷新首页。上述名称和地址仅为命令示例，请替换为真实项目。

1. 在新项目的 `README.md` 中填写研究目标、运行步骤和结论。
2. 在 `assets/` 放置截图，将相对仓库根目录的图片路径填入 `projects.json` 的 `cover`，并填写 `cover_alt`。
3. 修改摘要、状态、展示顺序或演示地址后，运行 `python scripts/catalog.py sync`。

## 仓库结构

```text
projects.json                 # 唯一项目登记表：编号、排序、摘要、图片、演示地址
projects/                     # 正式研究项目，使用 001-slug 格式
templates/project/            # 子项目模板，不占正式编号
docs/                         # 维护规范与部署说明
scripts/catalog.py            # 新建项目、生成首页、检查一致性
.github/workflows/check.yml   # 自动检查目录与首页索引
```

## 维护指南

- [项目组织与编号规则](docs/CONVENTIONS.md)
- [多个 Web 演示的部署约定](docs/DEPLOYMENT.md)
- [研究记录模板](templates/project/README.md)

## 来源与许可

各研究项目需注明上游仓库、研究版本及原始许可证。引入上游代码、图片或其他素材时保留其许可与署名；本仓库中的研究记录不改变上游项目的许可。
