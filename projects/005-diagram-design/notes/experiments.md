# 实验与验证

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
