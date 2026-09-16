# Future AGI：从执行记录到质量判断

研究日期：2026-09-16。固定提交：`c02ffdd8d0575cba4ab07743f67b508bd20206c0`。本页综合此前文档与源码研究；没有部署平台、调用评测模型或实测收益。

研究定位：核心能力是检测和评估 AI 应用的能力与表现。本页为检测方式与初步实现思路；底层判分、诊断及优化的根本原理仍需后期深入研究。详见[理解汇总](understanding.md)。

## 先区分三个问题

- **记录什么？** AI 应用的可见执行过程：问题、回答、检索片段、工具调用及结果、耗时、Token、错误状态与成本信息。应用埋点覆盖到哪里，才观察到哪里；这些不等于模型内部思维。
- **评什么？** 正确性、忠实性、完整性、安全性、语气、指令遵循、工具选择和任务完成等业务角度。
- **怎么评？** 用规则、参考比较、向量、模型判断、调查式评测与执行匹配，将证据转换为分数、分类或判断。不同角度可以采用多种方法。

## 数据怎么进入平台

业务请求可以经过 Go 模型网关到模型服务，获得路由、缓存、故障切换与配置的输入输出防护。运行记录是另一条路径：应用 SDK / traceAI 埋点 → OpenTelemetry / OTLP → fi-collector 接收和批处理 → ClickHouse 分析存储。

Trace 串起一次任务，Span 记录模型、检索和工具等步骤。React 展示、Django 业务、PostgreSQL 元数据及 Temporal 等后台任务组件共同支持管理与分析。仅接模型网关不会自动捕获所有业务工具步骤。详见[架构研究](architecture.md)。

输入也可以来自上传的数据集、人工参考与模拟对话。Simulate 通过场景和画像产生多轮文本或语音材料，随后再评分；模拟本身不是评分算法。

## 七类分析手段

官方[评测类型](https://docs.futureagi.com/docs/evaluation/concepts/eval-types)分为 Code Eval、LLM-as-Judge、Agent Evaluator。下面七类是便于理解的研究归纳，不能当作官方七种引擎。

| 手段 | 实现过程 | 主要作用与边界 |
| --- | --- | --- |
| 规则与函数 | 输入字段 → 正则、解析、比较等函数 → 结果 | 检查格式、明确条件；纯规则无需 LLM，但函数型评测也可依赖嵌入等模型 |
| 参考比较 | 实际结果 + 参考 → 文本差异、检索命中与排名分数 | BLEU、ROUGE、编辑距离；Recall@K、Precision@K、NDCG、MRR 等。需可信参考，不代表事实一定正确 |
| 向量相似度 | 文本 → Embedding → 余弦相似度或距离 | 衡量语义接近；“7 天退款”和“30 天退款”可能很相似，仍有事实差异 |
| 模型裁判 | 标准、回答、上下文及示例 → 模板 → 模型 → 结构化结果 | 对忠实性、语气等作判断；有成本、误判与波动，需人工校准 |
| Agent 调查 | 多轮分析 → 工具或知识查询 → 综合判断 | 可补齐证据；本轮仅确认产品文档，没有独立核验完整实现 |
| 工具匹配 | 实际工具名和参数 + 预期调用 → 匹配评分 | 名称与参数完整匹配 1，只匹配名称 0.5，否则 0；总分除以两边较大的调用数。匹配不代表接口执行成功 |
| 轨迹匹配 | 实际步骤序列 + 预期轨迹 → 顺序或集合比较 | strict / unordered / subset / superset 等模式；需要合理预期，不同模式须按具体计分实现解释 |

主要源码：[functions.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/agentic_eval/core_evals/fi_evals/function/functions.py)、[模型评测器](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/agentic_eval/core_evals/fi_evals/llm/custom_prompt_evaluator/evaluator.py)。补充：[工具调用准确性](https://docs.futureagi.com/docs/evaluation/builtin/tool-call-accuracy)、[轨迹匹配](https://docs.futureagi.com/docs/evaluation/builtin/trajectory-match)、[Ground Truth](https://docs.futureagi.com/docs/evaluation/concepts/ground-truth)。

已读工具匹配实现逐个选择尚未使用的预期调用，并非对真实业务结果作验证；因此应额外核对工具返回值与最终回答。轨迹的 strict 模式具有前缀计分细节，unordered 等集合比较模式也不能简单解释为逐步骤完整验证。

## 分数之后的四类处理

1. **组合评分。** 子评分归一化到 0–1 后，以平均、加权平均、最小值、最大值或通过率等汇总。关键业务错误宜另设门槛，避免平均分掩盖问题。[文档](https://docs.futureagi.com/docs/evaluation/concepts/composite-evals)
2. **错误定位。** 对符合条件的失败评测，将输入、标准、结果与解释交给分析 Agent，返回 `selected_input_key` 和 `error_analysis`。所读路径需启用，且排除代码型和组合评测。输出是待核实的解释，并非因果证明。[源码](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/model_hub/services/error_localizer_service.py)、[文档](https://docs.futureagi.com/docs/evaluation/concepts/error-localization)
3. **已有失败的聚类。** 每批最多取 500 条尚未聚类的失败结果，先尝试提炼标准化失败短语，再向量化，与项目、评测名和目标类型范围内的中心匹配；加入旧组或创建新组。提炼经企业边界调用，失败可退回原始描述。相似问题分组便于排查，但不是同一根因的证明。[源码](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/tracer/utils/eval_clustering.py)
4. **Error Feed 主动扫描。** 抽样 Trace，分析潜在错误并整理成 Issue，可以发现尚未被评测标为失败的问题。它与第三项的输入和触发条件不同。官方文档标为 Cloud / Enterprise，默认采样为 0，需要配置开启。[文档](https://docs.futureagi.com/docs/error-feed)、[分析流程](https://docs.futureagi.com/docs/error-feed/concepts/trace-error-analysis)

运行分析还包括按时间、模型等维度查看延迟、Token、成本和错误率。这些指标用于定位“慢、贵、不稳定”，不能单独作为业务能力分数。

## 怎样回到改进

失败案例进入数据集 → 人工修改或自动搜索提示词 / 示例配置 → 同一批样本与标准比较基线和候选 → 独立样本验收 → 新版本继续产生运行记录。

优化器通过生成候选、运行评分、选择和反馈推进搜索。已有六种算法思路：Random、Bayesian、ProTeGi、Meta-Prompt、PromptWizard、GEPA。它们调整提示词或示例配置，不等于更新基础模型权重；平台部分路径依赖企业模块。见[算法选择](https://docs.futureagi.com/docs/optimization/concepts/choosing-an-optimizer)与[部署边界](deployment-and-boundaries.md)。

## 一个完整例子：退款客服

资料写“7 天内且未使用”，回答“30 天内都可退”，退款接口实际返回失败，客服却回复“已退款”。

- JSON 检查只能说明返回结构合法。
- 向量相似度可能很高，仍不能确认政策正确。
- 政策忠实性评测要对照 7 天与未使用两个条件。
- 工具匹配检查是否选对退款工具与参数；轨迹检查是否先查订单。
- 结果一致性检查必须读真实工具返回值，确认没有虚假成功承诺。
- 将失败纳入测试集，再修改提示词、业务代码或工具流程；用相同标准验收。

这是研究者设计的教学例子，未运行真实退款流程。

## 图与证据

- [技术总览 PNG](../assets/future-agi-technical-overview.png) / [SVG](../assets/future-agi-technical-overview.svg)
- [基础来源索引](sources.md)：24 份基础文件与官方文档。
- [补充源码清单](analysis-method-sources.json)：7 份固定版本文件的地址、字节数和哈希。

网页、图、笔记使用同一理解框架；其中产品文档能力与关键源码阅读不应解释为已完成全部实现审计或实际效果验证。
