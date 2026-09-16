# Graft 能力、原理与效果全景图

当前理解为“扫描源码并构建索引与关系图，指导 AI 查找相关代码”；构建原理待研究。图中机制部分保留为初步源码阅读线索，不代表研究完成。

- `graft-overview.png`：2600 × 3740 高清图片。
- `graft-overview.svg`：保留文字和图形的可缩放版本，中文字体优先使用微软雅黑。
- `graft-overview-preview.png`：1040 × 1496 预览。
- 生成方式：在仓库根目录运行 `python projects/010-graft/src/draw_overview.py`，需要 Pillow 与 Windows 微软雅黑字体。

图示为原创机制归纳，研究日期 2026-09-16，依据 Graft 0.18.0 的固定提交 `f9e65396e638e517aecae0d731017f53084d70ed`，不是软件运行截图。导入别名示例为解释关系解析的教学代码。

## 依据与验证口径

- 能力、建图、语义说明、检索和限制见[真实源码实现分析](../notes/implementation-audit.md)及[来源清单](../notes/sources.md)。
- 纯中文分词与过期 crux 的结果见[原函数隔离探针](../notes/source-probes.json)；这些探针不代表完整建图或模型调用测试。
- 作者基准来自[固定提交 README](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/README.md)：50 道 SWE-bench 题中修复数量 27 → 33；Token 减少 23% 的统计范围是两组都成功解决的题。本项目未复现该基准，不能直接外推为用户仓库的收益。
- Caveman 的比较仅说明工作环节；没有测试组合使用的节省量。

版面已检查段落边界并渲染检查 PNG；SVG 已通过 XML 解析验证。不同查看器的字体回退可能改变 SVG 的字形，固定展示优先使用 PNG。
