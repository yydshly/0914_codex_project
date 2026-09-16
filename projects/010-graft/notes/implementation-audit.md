# Graft 源码阅读笔记：从函数记录到按需上下文

> 当前结论：扫描源码并构建索引与关系图，指导 AI 查找相关代码。构建原理待研究。以下为初步源码阅读与局部探针线索，保留供后续验证，不代表完整构建流程已研究清楚。

核对版本：0.18.0，提交 `f9e65396e638e517aecae0d731017f53084d70ed`。日期：2026-09-16。

方法：追踪固定版本源码的实际调用和数据结构，并对原始分词函数及代码片段选择函数做隔离探针。未安装完整 Graft、未建真实仓库图谱、未调用模型，因此不把本次称为端到端效果验证。

## 结论

Graft 的基础是“符号元数据＋代码关系图＋检索器”；深度模式再添加模型生成的用途说明和概念节点。函数数量是附带统计，函数的业务能力不是基础解析器自动确定的。

它不从被分析项目的 main 函数开始执行，而是枚举源码、解析定义和引用，再在查询阶段选择有关节点。不要把 Graft 自己的 CLI 入口与目标项目的分析起点混为一谈。

## 1. 真实构建调用链

```text
src/cli.ts：build 命令
  ├─ 启用 --deep 时：engine.init()
  │    └─ buildContext()：文件摘要 → 概念合成
  └─ engine.graph({ llm: deep })
       └─ buildGraph()
            ├─ walkDir / listSourceStats：枚举范围内源码
            ├─ 读文件并计算哈希：相同内容复用解析缓存
            ├─ extractFile / extractContainer / extractGeneric
            ├─ resolveEdges：将待解析引用连接到节点
            ├─ enrichGraph：复用/标记/生成语义说明
            ├─ 可选 enrichWithLsp：语言服务补充关系
            └─ writeGraph / writeAskIndex / writeCards
```

依据：[CLI](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/cli.ts#L486)、[引擎](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/engine.ts#L82)、[buildGraph](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/build.ts#L151)。部分源码旧注释仍写 .context / graph.json；本次以写入实现为准，实际结构文件为 graft/.graph/wiring.json。

## 2. 每个函数到底记录什么

[NodeV1](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/types.ts) 包含：

| 字段 | 实际作用 |
| --- | --- |
| id / name / kind / owner | 区分文件、函数、类、方法等，方法可记录所属类 |
| path / span | 文件位置与定义起止行 |
| signature / exported | 源码签名与导出标记；不保证推断出所有缺省类型 |
| origin / body_hash | 提取来源与定义内容哈希 |
| body_text | 用于检索的代码体文本；磁盘主图会去掉这项，检索缓存保存分词结果 |
| summary_state / summary / crux | 说明状态、模型用途说明、关键代码片段 |

基础提取将 summary_state 初始化为 pending，summary、crux 为空。旧的可复用说明可能被后续缓存流程带回，不能把“这次没调用模型”误认为“图上一定没说明”。

[extractFile](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/extract.ts#L387) 先创建文件节点，然后遍历语法树中的定义和引用。[writeGraph](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/write.ts#L35) 按稳定顺序保存节点和边，避免每次输出顺序随意变化。

## 3. 调用关系是如何判断的

边存 source、target、relation、confidence。结构关系包括 contains、calls、imports、references、implements、extends。

[resolveName](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/resolve.ts#L357) 的普通名字匹配分支先找同文件唯一结果，否则寻找语言可达范围内的跨文件唯一结果；后者标为 inferred。成员调用另走接收者类型、方法名及继承关系等规则。无法确定的调用可能跳过。

所以关系图中有“直接提取”和“规则推断”的区别；它没有运行程序逐次记录调用，也不能保证完整识别动态行为。

## 4. “函数能力”怎样生成

深度模式的符号说明由 [ChatCruxSummarizer.describeFile](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ai/crux.ts) 生成：

1. 按文件合并需要更新的定义，向模型提交带行号源码及目标定义列表。
2. 要求模型通过 record_symbols 返回每个目标的用途说明和关键行范围。
3. 程序按返回行号从真实源码截取代码，不让模型重写这一段代码。
4. 根据 id 与 body_hash 缓存结果；缺失定义可补问一次。

这不是“每个函数必定单独请求一次模型”。正常按文件批量请求，失败或缺项可能追加请求。

源码中的细节：提示词建议关键片段约 8 行，但 [buildCrux](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/enrich.ts#L287) 实际上限为 12 行。符号说明请求截取文件前 18,000 字符；另一路文件摘要上限为 24,000 字符，大文件后部可能不在模型输入中。这限制了说明的完整性。

概念层另有流程：[summarize.ts](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ai/summarize.ts) 生成文件摘要，[synthesize.ts](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ai/synthesize.ts) 将它们组合为系统、文件或跨文件概念，不是每个函数对应一篇 Markdown。

## 5. 问题如何变成相关代码

[ask.ts](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ask/ask.ts#L1316) 先尝试结构意图，失败或不适用时进入词项检索。

单作用域路径中，名称匹配权重为 3、路径匹配权重为 2，签名/摘要/代码体使用 BM25 等计算。词项结果作为 Personalized PageRank 的起点，在关系图中寻找关联节点；该图排序将可遍历关系视为无向连接，便于同时找到调用方和被调用方。普通查询还会对测试文件降权，询问测试时另行处理。

源码基础混合分为“归一化词项分＋0.5 × 图分”，再乘排序系数。最终还有文件分组、跨文件结果选择、作用域处理，因此不能把这个公式当成完整排名算法。

## 6. 为什么模型收到的内容变少

检索只选择部分位置；接口工具只给签名；源码输出优先使用已有 crux。没有关键片段或显式要求 full 时，按定义范围读取源码，并受 80 行截断限制。因此 full 表示完整定义方向的读取模式，不保证无限制返回整个文件。

节省发生在“输出给模型的上下文”这一步。构建本身仍读取文件；默认模式没有用另一个模型压缩每次查询结果。

[savings.ts](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/context/savings.ts#L25) 将字符数除以 4 粗估 Token，再比较相关文件全文与当前输出。这是特定假设下的估计，不是真实 tokenizer 计数，更不是实际账单节省率。

## 7. 两个原函数探针发现

探针读取固定版本原函数、用 Node 去除 TypeScript 类型后执行；分词直接运行原实现，片段选择测试使用合成图谱与模拟磁盘读取。完整输出：[source-probes.json](source-probes.json)。脚本：[probe_source.mjs](../src/probe_source.mjs)，需要本地 .cache/graft-source-f9e6539 源码缓存。

### 中文问题不会自动变成英文语义

[tokenize](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ask/index-file.ts#L38) 只保留 a-z 和数字，拆分驼峰并过滤停用词。

| 原输入 | 原函数结果 |
| --- | --- |
| 登录凭证在哪里生成 | 空列表 |
| token 为什么很快过期 | token |
| token expiry | token、expiry |
| issueToken | issue、token |

因此不能将此前中文教学任务理解为该版本可以原样完成中文语义检索。实际接入时，外层助手可以将中文意图转为英文关键词或代码标识符；这一步不在这个分词函数内。这里验证的是分词行为，未运行整个检索路径。

### 过期关键片段仍可能被选择

enrichGraph 在定义变化时可以保留旧 crux 并标记 stale，而 [inlineSource](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ask/ask.ts#L1275) 选择 crux 时没有检查 summary_state。

合成 stale 节点的探针中，full=false 返回旧片段；full=true 则走源码读取分支。它证明这个局部选择分支存在风险，尚未证明所有真实命令场景都会遇到。也说明“结构刷新完成”不能保证返回的缓存关键片段一定来自最新源码。

## 对前面解释的修正

- “位置、接口、用途、关系”是整体可提供的信息；用途并非基础模式默认已有。
- 查询涉及关键词和关系排序，不等于模型理解任意自然语言；当前中文分词存在明确限制。
- 结构缓存与模型语义缓存不同，语义过期还可能影响返回片段。
- 网页是预设教学导读，不能作为上述上游行为的运行证据。
