# 来源与证据索引

研究日期：2026-09-16。源码固定在提交 c02ffdd8d0575cba4ab07743f67b508bd20206c0。在线产品文档是当日阅读状态，内容可能随产品更新。

S 表示已下载核对的文件；T 表示目录树定位；D 表示官方文档。本次为静态研究，不把源码存在或文档描述写成运行验证。

## 固定版本源码

### S01

**产品定位、模块、SDK、路线图与遥测说明** — [README.md](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/README.md)

文件大小：25121 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S02

**开源核心许可证** — [LICENSE](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/LICENSE)

文件大小：11308 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S03

**企业目录许可范围** — [LICENSE-EE](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/LICENSE-EE)

文件大小：850 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S04

**版权与许可说明** — [NOTICE](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/NOTICE)

文件大小：614 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S05

**安装条件、依赖组、服务配置** — [INSTALLATION.md](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/INSTALLATION.md)

文件大小：26274 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S06

**当前服务编排与镜像变量** — [docker-compose.yml](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/docker-compose.yml)

文件大小：52183 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S07

**后端镜像构建** — [Dockerfile.oss](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/Dockerfile.oss)

文件大小：1388 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S08

**OTLP采集到ClickHouse路径** — [fi-collector/README.md](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/fi-collector/README.md)

文件大小：8943 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S09

**网关功能与配置说明** — [agentcc-gateway/README.md](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/agentcc-gateway/README.md)

文件大小：48898 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S10

**模型路由与健康目标选择** — [agentcc-gateway/internal/routing/router.go](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/agentcc-gateway/internal/routing/router.go)

文件大小：5518 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S11

**防护前后置、同步异步和策略** — [agentcc-gateway/internal/guardrails/engine.go](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/agentcc-gateway/internal/guardrails/engine.go)

文件大小：7971 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S12

**内置注入检测的规则范围** — [agentcc-gateway/internal/guardrails/injection/injection.go](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/agentcc-gateway/internal/guardrails/injection/injection.go)

文件大小：9850 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S13

**企业模块存在与部署门控** — [futureagi/tfc/ee_loader.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/tfc/ee_loader.py)

文件大小：1195 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S14

**优化运行创建服务** — [futureagi/model_hub/services/optimization_service.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/model_hub/services/optimization_service.py)

文件大小：2110 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S15

**优化后台任务** — [futureagi/model_hub/tasks/optimisation_runner.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/model_hub/tasks/optimisation_runner.py)

文件大小：1424 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S16

**函数型评测执行** — [futureagi/agentic_eval/core_evals/fi_evals/function/function_evaluator.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/agentic_eval/core_evals/fi_evals/function/function_evaluator.py)

文件大小：4264 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S17

**规则模板与模型评测执行** — [futureagi/agentic_eval/core_evals/fi_evals/llm/custom_prompt_evaluator/evaluator.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/agentic_eval/core_evals/fi_evals/llm/custom_prompt_evaluator/evaluator.py)

文件大小：25053 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S18

**聊天服务抽象接口** — [futureagi/simulate/services/chat_engine.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/simulate/services/chat_engine.py)

文件大小：3598 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S19

**聊天记录、模拟任务与评测触发** — [futureagi/simulate/tasks/chat_sim.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/simulate/tasks/chat_sim.py)

文件大小：27875 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S20

**部署遥测配置** — [futureagi/tfc/deployment_telemetry/config.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/tfc/deployment_telemetry/config.py)

文件大小：4036 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S21

**优化入口的企业依赖** — [futureagi/model_hub/views/develop_optimiser.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/model_hub/views/develop_optimiser.py)

文件大小：27797 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S22

**提示词优化任务的企业依赖** — [futureagi/model_hub/tasks/prompt_template_optimizer.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/model_hub/tasks/prompt_template_optimizer.py)

文件大小：27521 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S23

**提示词版本适配为被测Agent** — [futureagi/simulate/services/prompt_based_agent_adapter.py](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/simulate/services/prompt_based_agent_adapter.py)

文件大小：15023 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

### S24

**镜像上下文排除规则** — [.dockerignore](https://github.com/future-agi/future-agi/blob/c02ffdd8d0575cba4ab07743f67b508bd20206c0/.dockerignore)

文件大小：4816 字节；SHA-256 见 [机器可读清单](source-manifest.json)。

## T01

[优化器目录（固定提交）](https://github.com/future-agi/future-agi/tree/c02ffdd8d0575cba4ab07743f67b508bd20206c0/futureagi/ee/agent_opt/optimizers)

目录树未截断；六种算法文件名与位置已核对。本轮未下载或运行该企业目录的实现。路径见 [目录记录](optimizer-paths.json)。

## 官方产品文档

### D01

[运行追踪](https://docs.futureagi.com/docs/observe)

### D02

[评测机制](https://docs.futureagi.com/docs/evaluation/concepts/eval-types)

### D03

[对话与语音模拟](https://docs.futureagi.com/docs/simulation)

### D04

[数据集与实验](https://docs.futureagi.com/docs/dataset)

### D05

[模型网关](https://docs.futureagi.com/docs/command-center)

### D06

[提示词优化](https://docs.futureagi.com/docs/optimization)

### D07

[优化算法差异](https://docs.futureagi.com/docs/optimization/concepts/choosing-an-optimizer)

### D08

[Protect与产品可用范围](https://docs.futureagi.com/docs/protect)

### D09

[评测循环与CI/CD入口](https://docs.futureagi.com/docs/evaluation)

## 来源保存与许可

2026-09-16 补充分析手段研究：另核对 7 份固定版本源码，路径、链接、字节数和哈希见 [analysis-method-sources.json](analysis-method-sources.json)，包括函数指标、grounded similarity、注册入口、失败聚类、错误定位和轨迹配置。对应的判断与官方文档链接集中在[分析手段笔记](analysis-methods.md)。24 份基础文件与这 7 份补充文件分别保留清单。

选定文件的原始字节保存在被Git忽略的 .cache/upstream/，保留许可证和版权文件。研究成果只发布本项目撰写的分析、来源链接和哈希清单。阅读材料下载器不执行上游代码。

能力数量、框架数量和性能数字在不同页面可能不同，本研究不将其作为已验证指标，也未沿用上游竞品对比表。
