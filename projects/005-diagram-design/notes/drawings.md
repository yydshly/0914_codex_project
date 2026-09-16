# 全部绘图与交付清单

本次 AI 编写 **8 版中文案例 + 2 版理解总览图**；另原样归档 **57 组上游示例、155 个 HTML 文件**。同内容的主题、尺寸与详略版本不代表新的独立图型。

## 本次绘制：两版理解总览

| 图 | 内容 | PNG 尺寸 | 文件 |
|---|---|---|---|
| 理解总览 · 第二版（推荐） | 补全按问题选图、8 种语义模式、17 组扩展示例、历史工具分工、验证范围与扩展次序。 | 3600×6165 | [PNG](../assets/diagram-design-overview-v2.png) · [SVG](../assets/diagram-design-overview-v2.svg) |
| 理解总览 · 第一版 | 原理、三个维度、七类图型、绘图六步、交付格式、场景与扩展方向。 | 3000×5055 | [PNG](../assets/diagram-design-overview.png) · [SVG](../assets/diagram-design-overview.svg) |

## 本次绘制：八版中文研究流程

| 图 | 展示内容 | 文件 |
|---|---|---|
| 中文研究流程 · 蓝色 | 资料 → 提取 → 核实 → 图规格 → 生成 → 检查交付；六节点、五关系。 | [HTML](../cases/research-blue.html) · [SVG](../cases/research-blue.svg) · [PNG](../cases/research-blue.png) |
| 同结构 · 橙色 | 保持内容、坐标和字号，仅调整颜色角色。 | [HTML](../cases/research-orange.html) · [SVG](../cases/research-orange.svg) · [PNG](../cases/research-orange.png) |
| 同结构 · 深色 | 保持内容与布局，调整深色背景下的对比度。 | [HTML](../cases/research-dark.html) · [SVG](../cases/research-dark.svg) · [PNG](../cases/research-dark.png) |
| 完整解释页面 | 图形配标题、摘要与边界说明；SVG/PNG 仅导出图形。 | [HTML](../cases/research-full.html) · [SVG](../cases/research-full.svg) · [PNG](../cases/research-full.png) |
| 管理者概览 · 三阶段 | 将六个节点成对归并为理解资料、确认表达、制作交付，保留归并记录。 | [HTML](../cases/research-executive.html) · [SVG](../cases/research-executive.svg) · [PNG](../cases/research-executive.png) |
| 幻灯片 · 16:9 | 同一六节点流程重新排成横向单行，画布 1600×900。 | [HTML](../cases/research-slide.html) · [SVG](../cases/research-slide.svg) · [PNG](../cases/research-slide.png) |
| 手绘线条 | 给形状和连线添加轻微手绘效果，文字保持清晰。 | [HTML](../cases/research-sketchy.html) · [SVG](../cases/research-sketchy.svg) · [PNG](../cases/research-sketchy.png) |
| 边注强调 | 增加解释性批注；批注引导线不表示业务关系。 | [HTML](../cases/research-annotation.html) · [SVG](../cases/research-annotation.svg) · [PNG](../cases/research-annotation.png) |

中文案例 PNG 通常为 2560×1440，幻灯片版为 3200×1800；8 组共 24 个 HTML/SVG/PNG 文件。完整页面的单图 PNG 与蓝色版相同，页面摘要只在 HTML 中显示。

## 辅助图片与输入

- [八例联系表](../assets/case-contact-sheet.jpg)：八张中文 PNG 的缩略汇总，便于比较。
- [研究流程封面](../assets/research-workflow.png)：蓝色案例 PNG 的副本，不另计新图。
- 三种导入实验源文件：[Mermaid](../inputs/research.mmd)、[draw.io](../inputs/research.drawio)、[Excalidraw](../inputs/research.excalidraw)。它们表达同一份六节点、五关系内容。

## 原样归档：57 组上游示例

来自 Cathryn Lavery / diagram-design 固定提交 ce9344c52cb9，保留 MIT 许可；这些图不是本次原创。40 基础 + 11 派生 + 3 动画 + 3 导入 = 57 组。

| 分类 | 示例 | 层级 | 解决的问题 | 原版文件 |
|---|---|---|---|---|
| 架构与部署 | 系统架构 | 基础图型 | 组件怎样协作，数据如何流动 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-architecture.html) · [深色](../upstream/skills/diagram-design/assets/example-architecture-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-architecture-full.html) |
| 架构与部署 | IT 现状 | 基础图型 | 部门、遗留系统与现代化阶段 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-it-state.html) · [深色](../upstream/skills/diagram-design/assets/example-it-state-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-it-state-full.html) |
| 流程与交互 | 时序图 | 基础图型 | 参与者按什么顺序交换消息 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-sequence.html) · [深色](../upstream/skills/diagram-design/assets/example-sequence-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-sequence-full.html) |
| 流程与交互 | 令牌刷新时序 | 派生示例 | 请求遇到 401 后如何刷新与重试 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-sequence-oauth.html) · [深色](../upstream/skills/diagram-design/assets/example-sequence-oauth-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-sequence-oauth-full.html) |
| 流程与交互 | 状态机 | 基础图型 | 哪些事件让对象切换状态 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-state.html) · [深色](../upstream/skills/diagram-design/assets/example-state-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-state-full.html) |
| 数据模型与依赖 | 实体关系 | 基础图型 | 概念实体、字段与关系 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-er.html) · [深色](../upstream/skills/diagram-design/assets/example-er-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-er-full.html) |
| 数据模型与依赖 | 数据库结构 | 基础图型 | 物理表、类型、约束和外键 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-db-schema.html) · [深色](../upstream/skills/diagram-design/assets/example-db-schema-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-db-schema-full.html) |
| 数据模型与依赖 | 依赖图 | 基础图型 | 扇入、层级和循环依赖 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-dependency.html) · [深色](../upstream/skills/diagram-design/assets/example-dependency-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-dependency-full.html) |
| 架构与部署 | 部署图 | 基础图型 | 软件运行在哪里 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-deployment.html) · [深色](../upstream/skills/diagram-design/assets/example-deployment-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-deployment-full.html) |
| 数据模型与依赖 | UML 类图 | 基础图型 | 类、操作与类型关系 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-uml-class.html) · [深色](../upstream/skills/diagram-design/assets/example-uml-class-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-uml-class-full.html) |
| 架构与部署 | 平台总览 | 基础图型 | 数据平台端到端的组成 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-high-level.html) · [深色](../upstream/skills/diagram-design/assets/example-high-level-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-high-level-full.html) |
| 架构与部署 | 平台总览 · 纵向 | 派生示例 | 同一类平台内容的纵向排布 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-high-level-vertical.html) · [深色](../upstream/skills/diagram-design/assets/example-high-level-vertical-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-high-level-vertical-full.html) |
| 架构与部署 | 数据湖 | 派生示例 | 湖内存储、计算与访问层 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-datalake.html) · [深色](../upstream/skills/diagram-design/assets/example-datalake-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-datalake-full.html) |
| 层级与组织 | 分层数据存储 | 基础图型 | 不同质量等级的数据怎样衔接 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-medallion.html) · [深色](../upstream/skills/diagram-design/assets/example-medallion-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-medallion-full.html) |
| 流程与交互 | 数据流 | 基础图型 | 数据经过哪些角色和处理步骤 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-data-flow.html) · [深色](../upstream/skills/diagram-design/assets/example-data-flow-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-data-flow-full.html) |
| 架构与部署 | 平台集成 | 基础图型 | 数据源、平台核心与消费者 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-dp-integration.html) · [深色](../upstream/skills/diagram-design/assets/example-dp-integration-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-dp-integration-full.html) |
| 策略与关系分析 | 权限矩阵 | 基础图型 | 角色对组件有什么访问权限 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-dp-security-matrix.html) · [深色](../upstream/skills/diagram-design/assets/example-dp-security-matrix-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-dp-security-matrix-full.html) |
| 流程与交互 | 流程图 | 基础图型 | 条件和分支决定下一步 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-flowchart.html) · [深色](../upstream/skills/diagram-design/assets/example-flowchart-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-flowchart-full.html) |
| 流程与交互 | 多角色过程 | 基础图型 | 每一步由谁处理、输入输出是什么 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-process.html) · [深色](../upstream/skills/diagram-design/assets/example-process-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-process-full.html) |
| 流程与交互 | 泳道图 | 基础图型 | 流程如何跨越责任边界 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-swimlane.html) · [深色](../upstream/skills/diagram-design/assets/example-swimlane-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-swimlane-full.html) |
| 层级与组织 | 组织与路由 | 基础图型 | 谁负责、向谁汇报或升级 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-org-chart.html) · [深色](../upstream/skills/diagram-design/assets/example-org-chart-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-org-chart-full.html) |
| 层级与组织 | 层级树 | 基础图型 | 整体怎样拆成子项 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-tree.html) · [深色](../upstream/skills/diagram-design/assets/example-tree-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-tree-full.html) |
| 层级与组织 | 嵌套关系 | 基础图型 | 范围、容器与包含关系 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-nested.html) · [深色](../upstream/skills/diagram-design/assets/example-nested-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-nested-full.html) |
| 层级与组织 | 分层结构 | 基础图型 | 抽象层、控制层的上下关系 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-layers.html) · [深色](../upstream/skills/diagram-design/assets/example-layers-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-layers-full.html) |
| 流程与交互 | 循环与飞轮 | 基础图型 | 反馈怎样回流并积累状态 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-loop.html) · [深色](../upstream/skills/diagram-design/assets/example-loop-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-loop-full.html) |
| 时间与工作规划 | 时间线 | 基础图型 | 关键事件发生的先后 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-timeline.html) · [深色](../upstream/skills/diagram-design/assets/example-timeline-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-timeline-full.html) |
| 时间与工作规划 | 甘特图 | 基础图型 | 任务的时间、阶段与重叠 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-gantt.html) · [深色](../upstream/skills/diagram-design/assets/example-gantt-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-gantt-full.html) |
| 策略与关系分析 | 四象限 | 基础图型 | 对象在两个维度上的位置 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-quadrant.html) · [深色](../upstream/skills/diagram-design/assets/example-quadrant-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-quadrant-full.html) |
| 策略与关系分析 | Wardley 地图 | 基础图型 | 价值链与组件演进阶段 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-wardley.html) · [深色](../upstream/skills/diagram-design/assets/example-wardley-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-wardley-full.html) |
| 时间与工作规划 | 看板 | 基础图型 | 工作处于什么状态 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-kanban.html) · [深色](../upstream/skills/diagram-design/assets/example-kanban-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-kanban-full.html) |
| 时间与工作规划 | 用户旅程 | 基础图型 | 每个阶段的动作与感受 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-journey.html) · [深色](../upstream/skills/diagram-design/assets/example-journey-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-journey-full.html) |
| 时间与工作规划 | 用户故事地图 | 基础图型 | 主干活动如何切成发布批次 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-story-map.html) · [深色](../upstream/skills/diagram-design/assets/example-story-map-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-story-map-full.html) |
| 策略与关系分析 | 鱼骨图 | 基础图型 | 哪些类别的原因共同影响结果 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-fishbone.html) · [深色](../upstream/skills/diagram-design/assets/example-fishbone-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-fishbone-full.html) |
| 策略与关系分析 | 韦恩图 | 基础图型 | 集合之间的交集 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-venn.html) · [深色](../upstream/skills/diagram-design/assets/example-venn-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-venn-full.html) |
| 层级与组织 | 金字塔与漏斗 | 基础图型 | 层级或逐级流失 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-pyramid.html) · [深色](../upstream/skills/diagram-design/assets/example-pyramid-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-pyramid-full.html) |
| 数值与统计 | 柱状图 | 基础图型 | 不同类别的数量差异 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-bar.html) · [深色](../upstream/skills/diagram-design/assets/example-bar-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-bar-full.html) |
| 数值与统计 | 折线图 | 基础图型 | 连续时间上的变化 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-line.html) · [深色](../upstream/skills/diagram-design/assets/example-line-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-line-full.html) |
| 数值与统计 | 散点图 | 基础图型 | 分布和变量关联 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-scatter.html) · [深色](../upstream/skills/diagram-design/assets/example-scatter-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-scatter-full.html) |
| 数值与统计 | 矩形树图 | 基础图型 | 部分占整体的面积比例 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-treemap.html) · [深色](../upstream/skills/diagram-design/assets/example-treemap-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-treemap-full.html) |
| 数值与统计 | 雷达图 | 基础图型 | 多个维度的评分差异 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-radar.html) · [深色](../upstream/skills/diagram-design/assets/example-radar-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-radar-full.html) |
| 数值与统计 | 极坐标图 | 基础图型 | 周期类别的量级变化 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-polar.html) · [深色](../upstream/skills/diagram-design/assets/example-polar-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-polar-full.html) |
| 数值与统计 | 桑基图 | 基础图型 | 数量如何分流与汇合 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-sankey.html) · [深色](../upstream/skills/diagram-design/assets/example-sankey-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-sankey-full.html) |
| 数值与统计 | 瀑布图 | 基础图型 | 正负贡献如何改变总量 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-waterfall.html) · [深色](../upstream/skills/diagram-design/assets/example-waterfall-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-waterfall-full.html) |
| 数值与统计 | 蜂群图 | 派生示例 | 每个样本在一维数轴的位置 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-beeswarm.html) · [深色](../upstream/skills/diagram-design/assets/example-beeswarm-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-beeswarm-full.html) |
| 数值与统计 | 气泡图 | 派生示例 | 位置和面积共同编码数值 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-bubble.html) · [深色](../upstream/skills/diagram-design/assets/example-bubble-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-bubble-full.html) |
| 数值与统计 | 排名变化图 | 派生示例 | 名次怎样随阶段变化 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-bump.html) · [深色](../upstream/skills/diagram-design/assets/example-bump-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-bump-full.html) |
| 数值与统计 | 山脊图 | 派生示例 | 多组分布的形状差异 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-ridgeline.html) · [深色](../upstream/skills/diagram-design/assets/example-ridgeline-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-ridgeline-full.html) |
| 数值与统计 | 坡度图 | 派生示例 | 两个时点之间的变化 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-slopegraph.html) · [深色](../upstream/skills/diagram-design/assets/example-slopegraph-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-slopegraph-full.html) |
| 层级与组织 | 可追溯模块树 | 派生示例 | 模块的输入、输出、约束和实现位置 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-tree-block-decomposition.html) · [深色](../upstream/skills/diagram-design/assets/example-tree-block-decomposition-dark.html) · [完整页面](../upstream/skills/diagram-design/assets/example-tree-block-decomposition-full.html) |
| 策略与关系分析 | 四象限 · 情景矩阵 | 派生示例 | 两个驱动因素组合成四种情景 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-quadrant-consultant.html) |
| 流程与交互 | 循环 · 终端风格 | 派生示例 | 终端窗口中的循环解释 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-loop-terminal.html) |
| 流程与交互 | 策略轨迹动画 | 动画演示 | 两条规则路径何时产生分歧 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-policy-trace-animated.html) |
| 流程与交互 | 队列瓶颈动画 | 动画演示 | 输入、等待和有限处理能力 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-queue-animated.html) |
| 架构与部署 | 安全路径动画 | 动画演示 | 允许路径、禁止入口与信任边界 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-paved-road-animated.html) |
| 架构与部署 | draw.io 重绘示例 | 导入重绘 | 保留结构内容，重新组织画面 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-import-drawio.html) |
| 流程与交互 | Mermaid 重绘示例 | 导入重绘 | 从声明的节点关系重新排版 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-import-mermaid.html) |
| 流程与交互 | Excalidraw 重绘示例 | 导入重绘 | 从白板源文件整理出清晰关系 | [浅色 / 单独版本](../upstream/skills/diagram-design/assets/example-import-excalidraw.html) |

总计 49 组三版本 × 3 + 8 个单独版本 = 155 个 HTML 文件；原版内容和样式未经修改。

[图型分类](taxonomy.md) · [研究原理](analysis.md) · [验证记录](experiments.md)
