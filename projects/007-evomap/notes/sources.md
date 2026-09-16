# 来源、版本与证据

研究日期 2026-09-16。网站持续变化，仓库证据固定于以下版本。

## 版本

- 上游：[EvoMap/evolver](https://github.com/EvoMap/evolver)。
- Commit：`31b0691acd97ba18878019312e646f1f2d970d43`。
- 提交时间：2026-09-05T00:25:04+08:00。
- 包版本 1.94.0；声明 Node >=22.12；本次 Node v22.15.0。
- 锁定的 GEP SDK 1.12.1。
- 锁文件 SHA-256：`78aa0e1c60c6cdd119232ea6e12afdd83f84589a1664b88d44f4c8c8b375b826`。
- [机器审查清单](source-audit.json)。

## 固定源码入口

| 材料 | 用途 |
| --- | --- |
| [中文 README](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/README.zh-CN.md#L155) | 基础模式和宿主分工 |
| [包配置](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/package.json) | 版本、Node、依赖与许可声明 |
| [本地路径](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/src/gep/paths.js#L194) | 运行资产和随包种子分离 |
| [种子 Gene](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/assets/gep/genes.seed.json) | 真实步骤、限制、验证命令 |
| [选择器测试](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/test/selector.test.js) | 匹配、偏好、多语言、禁止、兜底 |
| [兜底测试](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/test/selector.test.js#L425) | 有意设计的 distilled_fallback |
| [哈希测试](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/test/contentHash.test.js) | 一致性与 SDK 转发 |
| [提示词测试](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/test/prompt.test.js) | 结构与上下文保留 |
| [分发测试](https://github.com/EvoMap/evolver/blob/31b0691acd97ba18878019312e646f1f2d970d43/test/evolveDispatch.test.js) | 基础输出与 bridge；只阅读未运行 |

缓存中 SDK 的 `src/contentHash.js` 是可读实现，其版本由上游锁文件确定。未把该 SDK 代码复制进研究仓库。

## 官方平台资料

- [博客](https://evomap.ai/zh/blog)：用户给出的入口。
- [平台参考](https://evomap.ai/llms.txt)：概念与接口目录，属于官方描述。
- [用户指南](https://evomap.ai/zh/wiki/02-for-human-users)：提问、反馈和悬赏。
- [Evolver 说明](https://evomap.ai/zh/wiki/34-evolver)：整体循环。
- [GEP 说明](https://evomap.ai/zh/wiki/16-gep-protocol)：资产与交换。
- [多 Agent 介绍](https://evomap.ai/zh/capabilities/multi-agent)：协作能力。
- [蜂群文档](https://evomap.ai/zh/wiki/10-swarm)：2026-09-16 查阅，用于任务拆解、认领、调度和协作模式的描述。新增蜂群章节与理解图采用“能力、角色、经验”解释框架，属于我们的概念归纳；未进行云端蜂群实测。
- [群体超级智能文章](https://evomap.ai/zh/blog/toward-collective-superintelligence)：方向愿景，未作为已交付能力证明。

## 文档与代码差异

1. README 写 Node >=18，包配置写 >=22.12，复现采用后者。
2. 官网整体循环容易读成客户端独立完成所有修改；固定版本 README 对基础模式明确说明提示与宿主执行分工。其他 solo／proxy 路径需单独核实。
3. 网站早前材料的 schema 版本和本次 SDK 1.12.1 不同，不能默认为同一发布快照。

## 许可与可审计性

该 commit 的包配置声明 GPL-3.0-or-later，根 LICENSE 是 GPL v3 文本，保存在 [UPSTREAM-LICENSE.txt](UPSTREAM-LICENSE.txt)。README 公告未来转为 source-available；此处记录原文与版本，不推断未来许可。

202 个已跟踪 src JavaScript 文件中，57 个命中 `_0x[0-9a-f]+` 标识符启发式，覆盖关键模块。该检测不是反编译或完整安全审计；可下载不能直接理解为全部代码可读。

上游 checkout 和依赖只保存在本机缓存。研究仓库保留版本、链接、许可、自己的实验脚本和验证输出，合成例子不冒充官方资产或生产任务。
