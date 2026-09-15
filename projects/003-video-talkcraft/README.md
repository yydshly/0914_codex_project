# 003 · Video TalkCraft：口播视频制作 Skill

**摘要：将口播稿、成品配音和素材组织为逐字同步的动效视频及可编辑工程；可复用到培训、产品讲解与系列口播，统一表达风格并支持局部修改。**

它是一套供 Agent 执行的制作规范、动效配方和工具。Agent 理解文案、设计分镜并选择组件，语音识别与对齐脚本提供时间表，Remotion 根据代码渲染画面，最后检查和审片。画廊展示可复用的组件效果；“最适合哪种效果”仍需要结合内容、素材、时长和全片风格判断。

[查看理解图原图](assets/video-talkcraft-workflow.png) · [可缩放 SVG](assets/video-talkcraft-workflow.svg) · [完整制作模型](notes/production-model.md)

![Video TalkCraft 理解图：输入、分镜选卡、组装输出、一致性与修改回退](assets/video-talkcraft-workflow.png)

## 对我的意义

- **制作培训、教学和产品说明**：以声音为主线，把数字、对比、流程和真实截图安排到对应的讲解位置，减少逐帧手调。
- **沉淀系列口播的制作方式**：复用动效组件与全片风格，同时检查每镜声画配合和镜头之间的衔接。
- **方便后续更新**：保留分镜、时间表、素材来源与工程；局部变化可以重渲受影响镜头，换配音或公共样式则重新判断影响范围。
- **帮助选择投入方向**：先用一条短片验证素材、质量与制作成本，再决定是否扩大使用。本研究已做单组件渲染，完整多镜头口播仍待实测。

## 如何真正用起来

1. **安装上游完整 Skill**：将 [上游仓库链接](https://github.com/Vincentwei1021/video-talkcraft) 交给支持 Skill 的 Agent 安装。本子项目只保留研究所需的源码快照，不能代替完整安装包。安装入口见固定版本的 [快速开始](https://github.com/Vincentwei1021/video-talkcraft/blob/8829ca31fb8aeb1b850e85e47a7d7584c349bc4a/README.md#-快速开始)。
2. **准备输入**：确定受众、目标、画幅与风格；提供一致的口播稿和成品配音。只有文案时先录音或借助外部工具生成配音；需要出镜时提供同步人物视频，按镜头准备图片、实拍与证据截图。
3. **先做样板镜**：让 Agent 整理事实与素材、生成时间表和分镜、说明选卡理由，先输出一镜有声预览，确认后完成其余镜头。
4. **逐层复核后交付**：核对全片口径、镜内声画和跨镜衔接；检查技术正确、表达正确和观看有效，再保留成片、可编辑工程与来源记录。

可直接交给已安装 Skill 的 Agent 的需求示例（素材路径请换成自己的）：

```text
用 video-talkcraft 制作一条约 30 秒的产品功能讲解。
受众是首次使用的同事，目标是让他们理解一个功能解决什么问题。
口播稿为 script.txt，成品配音为 voiceover.wav，真实产品截图在 assets/。
横屏 16:9，本次不需要人物出镜，保持统一字体、主题色和数据口径。
先检查稿音一致性和素材，再给出分镜、词锚与选卡理由。
优先表达清楚、阅读来得及；先交付一镜有声样板供确认，再完成全片。
最终交付视频、Remotion 工程、素材来源与检查记录；缺失项单独说明。
```

**复用边界**：文案不是完整输入；本库不自带 TTS 或数字人生成模型，也没有已验证的“自动选出最优效果”保证。人物是否抠像取决于呈现方式：圆形窗口可保留背景，轮廓贴角需要抠像。

## 项目信息

| 项目 | 内容 |
| --- | --- |
| 上游仓库 | [上游仓库](https://github.com/Vincentwei1021/video-talkcraft) |
| 研究版本 / Commit | `8829ca31fb8aeb1b850e85e47a7d7584c349bc4a` |
| 上游许可证 | [PolyForm Noncommercial 1.0.0](upstream/LICENSE) |
| 研究范围 | 源码研究、六例 HTML 展示、对齐实验与单组件渲染 |
| 研究状态 | 本次范围已完成，完整口播生产与真实语音精度未验证 |
| 开始日期 | 2026-09-15 |
| 演示 | [本地研究页面](http://127.0.0.1:8033/)，需启动下述本地服务；未在线发布 |

## 先看什么

- **一图总览**：[输入 → 内部制作 → 输出（高清 PNG）](assets/video-talkcraft-workflow.png) · [可缩放 SVG](assets/video-talkcraft-workflow.svg)。包含选卡、分镜、声画对齐、三层一致性、八项制作约束，以及修改与失败后的回退。

- **看能力**：切换数字滚动、荧光笔、网页巡游、人物角标、对比分屏、形状转场。六例保持上游代码，包含本地依赖与素材。
- **懂原理**：拖动模拟播放头，对比词锚对齐与延后 0.30 秒。此区域无声音，仅作机制说明。
- **查证据**：10 项控制实验、真实单组件 MP4、108 套动效源码索引。
- **评估价值**：[原理研究](notes/architecture.md)、[价值与边界](notes/value.md)、[实验记录](notes/experiments.md)。
- **完整制作模型**：[一致性、遗漏项与制作闭环](notes/production-model.md)。区分技术正确、表达正确和观看有效，并标明上游已有机制、流程规范与研究建议。

本页是研究展示，不是上传稿件即可生成长片的服务。没有运行 TTS、数字人生成、真实语音模型或完整工作台。

![上游数字组件实际渲染帧；人物为模板占位](assets/cover.jpg)

[播放实际渲染短片](web/dist/assets/number-counter.mp4) · [媒体核验结果](web/dist/render-result.json)

## 输入与输出

通常输入为文字稿与一致的成品配音。人物视频可选，出镜时须与配音同步；图片、实拍和截图按镜头需要准备或采集。圆形人物窗可保留背景，轮廓贴角需要抠像。绿幕有现成处理配方，无绿幕分割在上游文档中仍列为候选，需要验证样片。

输出为 Remotion 工程与渲染视频；工作台的图层拆解依赖源工程结构，不支持把任意 MP4 还原成可编辑工程。

## 快速运行

在本子项目目录执行（Python 3.10+，展示无需安装依赖）：

```sh
python -m http.server 8033 --bind 127.0.0.1 --directory web/dist
```

打开 [本地研究页面](http://127.0.0.1:8033/)。六个演示、研究内容和数据由本地提供，其余动效的在线演示与源码链接需要联网。通过 HTTP 打开，避免直接双击文件时 JSON 读取受限。

### 重跑算法实验

```sh
python -m pip install --target .cache/pydeps pypinyin==0.55.0 zhconv==1.4.3
python -X utf8 src/run_experiments.py
```

输入是人为构造的 ASR 词表，执行上游原始脚本，不下载语音模型；依赖只装入本项目缓存。

### 重渲原始组件

```sh
cd src/render-example
npm ci
npm run render
```

需要 Node.js；Remotion 首次可能下载浏览器。输出 `web/dist/assets/number-counter.mp4`，960×540、30 fps、86 帧，无声音。灰色人物为原始占位图形，不是数字人生成。

本机运行使用已安装的 Chrome，避免首次下载等待。在同一目录可运行已验证命令：

```powershell
node node_modules/@remotion/cli/remotion-cli.js render index.tsx NumberCounter ../../web/dist/assets/number-counter.mp4 --concurrency=1 --codec=h264 --crf=18 --browser-executable='C:/Program Files/Google/Chrome/Application/chrome.exe'
```

其他机器请改为自己的 Chromium/Chrome 路径，或使用上述默认下载方式。

### 校验来源与展示

```sh
python -X utf8 src/verify.py
```

检查源文件哈希、108 项映射、本地资源、JavaScript 语法与实验结果。视频存在时核对实际帧数和尺寸；不代替浏览器视觉检查或成片审片。

### 同步研究文档、网页与总览图

新增制作模型以 [production-model.json](notes/production-model.json) 为共同内容来源。修改后执行：

```sh
python -X utf8 src/sync_production_model.py
python -X utf8 src/draw_workflow.py
python -X utf8 src/verify.py
```

第一步更新详细文档和网页章节，第二步生成 PNG、SVG 并同步到网页资源。制图脚本需要 Pillow 与本机中文字体；当前图像为 3300×6600 像素。新增研究说明不增加真实长片验证的覆盖范围。

## 架构与关键实现

稿件 + 配音 → 预剪 → 识别词表 → 文本对齐与插值 → 逐字时间表 → SHOTBOOK 分镜 → 动效组件 → 分镜缓存 → 混入整条音轨 → 验收。

详细模块、源码链接与证据分级见 [architecture.md](notes/architecture.md)。

## 实验与结论

| 问题 | 结果 | 结论 |
| --- | --- | --- |
| 108 套是否有对应实现 | 配方、组件、HTML 演示与画廊均 108 项 | 本版本索引完整，不代表全部已渲染测过 |
| 英文缺失是否降低 match | TalkCraft 缺失，match 仍 1.0 | 中文覆盖率不代表英文声学精度 |
| 全时间轴错后 2 秒 | match 仍 1.0 | 对齐覆盖不校验绝对时间 |
| 动效错后 0.30 秒 | beat_lint 拒绝 | 能发现相对时间表的错位 |
| 镜尾只剩 0.20 秒 | beat_lint 拒绝 | 能检查关键动效停留不足 |

10 项实验均符合预期（其中包含预期拒绝的输入），记录在 [results.json](notes/experiments/results.json)。性能与真实语音精度未作本机测量。GitHub 简介写 109，固定版本的源码目录与 README 为 108；以文件树为准。

## 局限与后续计划

- 尚未验证：真实语音识别误差、人物抠像、完整长片、混音验收、工作台拆解、多镜头性能。
- 发布修订已在浏览器检查首屏摘要、理解图和使用说明；尚未完成所有交互、移动端及完整成片的自动化测试。检查范围见实验记录。
- 研究最值得复用的是时间契约、动效参数、局部重渲和有覆盖说明的检查。
- 与 [001 · 语音驱动纸艺剧场](../001-audio-locked-paper-theatre/README.md)相通的是声音时间轴；本项目侧重通用动效与生产流程，没有将两者合并。

## 目录说明

- `src/`：采集、实验、验证脚本，以及有锁文件的 Remotion 小工程。
- `notes/`：原理、价值、原始实验数据与文件哈希清单。
- `upstream/`：固定版本的原始源码与文档，保持原始字节。
- `web/dist/`：可直接托管的展示页面、数据和媒体；`vendor/` 保留原版演示。
- `.cache/`：忽略提交的下载缓存与 Python 依赖。

## 来源与引用

- 来源与 SHA-256 记录在 [inventory.json](notes/inventory.json) 与 [demo-manifest.json](notes/demo-manifest.json)。采集脚本固定 commit，不随 main 漂移。
- 保留 [原作许可](upstream/LICENSE)、[第三方说明](upstream/THIRD_PARTY_NOTICES.md)、[素材来源](web/dist/vendor/demos/_lib/media/ATTRIBUTION.md)、[音效来源](web/dist/vendor/demos/_lib/sfx/ATTRIBUTION.md)。
- 作者声明非商业使用免费，工具商用需要事先授权，产出视频归创作者；研究记录不改变上游许可。
- 本研究通过总仓库的 GitHub Pages 流程发布静态展示；完整视频制作仍在本机或相应运行环境中执行。

---

[返回总索引](../../README.md)
