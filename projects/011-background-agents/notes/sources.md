# 固定版本与来源索引

研究基准：[4c470da615eaecbf8f64b0ae5a04666c99b4c536](https://github.com/ColeMurray/background-agents/tree/4c470da615eaecbf8f64b0ae5a04666c99b4c536)。

以下为静态阅读定位：行号及 SHA-256 直接从该提交的 Git 对象生成，不代表运行测试通过。
上游许可证为 MIT，版权属于 Open-Inspect Contributors。本项目笔记为中文研究整理；未将完整上游代码复制进正式研究目录。

## S01

**项目名称、功能与单租户边界** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/README.md)

- `# Background Agents: Open-Inspect`：[L1](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/README.md#L1)
- `No per-user repository access validation`：[L38](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/README.md#L38)
- `Ad-hoc sets`：[L172](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/README.md#L172)

## S02

**运行流程、会话与环境恢复** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/HOW_IT_WORKS.md)

- `## How Prompts Flow`：[L381](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/HOW_IT_WORKS.md#L381)
- `## The Agent`：[L459](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/HOW_IT_WORKS.md#L459)
- `## The Sandbox Lifecycle`：[L240](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/HOW_IT_WORKS.md#L240)

## S03

**任务排队、分发与并发认领** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts)

- `async processMessageQueue`：[L365](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts#L365)
- `getProcessingMessage()`：[L383](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts#L383)
- `startMessageProcessing(`：[L505](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts#L505)
- `spawnSandbox()`：[L450](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts#L450)
- `queueDepth >= MAX_UNFINISHED_PROMPTS`：[L851](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/message-queue.ts#L851)

## S04

**断线存活与代理调用** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/bridge.py)

- `prompt tasks must survive WS disconnects`：[L625](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/bridge.py#L625)
- `await self.harness.run_prompt`：[L709](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/bridge.py#L709)
- `harness must not emit execution_complete`：[L699](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/bridge.py#L699)

## S05

**代理统一接口** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/base.py)

- `class HarnessId`：[L30](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/base.py#L30)
- `class AgentHarness`：[L115](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/base.py#L115)
- `class TurnOutcome`：[L79](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/base.py#L79)

## S06

**运行层与模型兼容性** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts)

- `HARNESS_IDS`：[L23](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L23), [L24](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L24), [L26](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L26), [L61](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L61)
- `modelFamilies: ["anthropic"]`：[L52](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L52)
- `checkHarnessCompatibility`：[L6](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L6), [L113](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L113), [L164](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/harnesses.ts#L164)

## S07

**子会话的深度、仓库与基准分支** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/routes/session-child-spawn.ts)

- `MAX_SPAWN_DEPTH = 2`：[L47](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/routes/session-child-spawn.ts#L47)
- `child sessions are single-repo by design`：[L139](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/routes/session-child-spawn.ts#L139)
- `Child sessions must use the same repository`：[L147](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/routes/session-child-spawn.ts#L147)
- `spawnContext.baseBranch`：[L254](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/routes/session-child-spawn.ts#L254)

## S08

**PR 创建时的身份选择** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/pull-request-service.ts)

- `input.promptingAuth ?? appAuth`：[L365](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/pull-request-service.ts#L365)
- `sourceControlProvider.createPullRequest`：[L370](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/session/pull-request-service.ts#L370)

## S09

**自动化种类、间隔与失败暂停** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md)

- `Linear Event`：[L16](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L16)
- `15 minutes`：[L348](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L348), [L353](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L353), [L480](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L480)
- `3 consecutive`：[L455](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L455)
- `scheduled automations only`：[L69](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AUTOMATIONS.md#L69)

## S10

**Node 容器部署与单实例假设** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CONTROL_PLANE_CONTAINER.md)

- `one Node process`：[L4](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CONTROL_PLANE_CONTAINER.md#L4)
- `The web app is not part of the stack`：[L21](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CONTROL_PLANE_CONTAINER.md#L21)
- `Two processes at once`：[L173](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CONTROL_PLANE_CONTAINER.md#L173)

## S11

**沙箱供应商工厂** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts)

- `case "daytona"`：[L172](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts#L172)
- `case "e2b"`：[L180](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts#L180)
- `case "modal"`：[L182](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts#L182)
- `case "vercel"`：[L174](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts#L174)
- `case "opencomputer"`：[L176](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/provider-factory.ts#L176)

## S12

**Modal 状态恢复能力声明** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/modal-provider.ts)

- `supportsSnapshots: true`：[L90](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/modal-provider.ts#L90)
- `supportsPersistentResume: false`：[L92](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/modal-provider.ts#L92)

## S13

**Daytona 状态恢复能力声明** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/daytona-provider.ts)

- `supportsSnapshots: false`：[L61](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/daytona-provider.ts#L61)
- `supportsPersistentResume: true`：[L63](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/daytona-provider.ts#L63)

## S14

**E2B 状态恢复能力声明** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/e2b-provider.ts)

- `supportsSnapshots: false`：[L192](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/e2b-provider.ts#L192)
- `supportsPersistentResume: true`：[L195](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/e2b-provider.ts#L195)

## S15

**Vercel 状态恢复能力声明** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/vercel/provider.ts)

- `supportsSnapshots: true`：[L86](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/vercel/provider.ts#L86)
- `supportsPersistentResume: false`：[L88](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/vercel/provider.ts#L88)

## S16

**OpenComputer 状态恢复能力声明** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/opencomputer-provider.ts)

- `supportsSnapshots: true`：[L77](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/opencomputer-provider.ts#L77)
- `supportsPersistentResume: true`：[L79](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/control-plane/src/sandbox/providers/opencomputer-provider.ts#L79)

## S17

**复用指令与技能版本** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/MANAGED_SKILLS.md)

- `Managed skills give agents`：[L3](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/MANAGED_SKILLS.md#L3)
- `permission boundary`：[L11](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/MANAGED_SKILLS.md#L11)

## S18

**上游许可证** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/LICENSE)

- `MIT License`：[L1](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/LICENSE#L1)
- `Copyright`：[L3](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/LICENSE#L3)

## S19

**Node 最低版本** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/package.json)

- `"node": ">=22.13.0"`：[L50](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/package.json#L50)

## S20

**单会话待完成任务上限** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/types/prompts.ts)

- `MAX_UNFINISHED_PROMPTS = 50`：[L5](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/shared/src/types/prompts.ts#L5)

## S21

**部署指南** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/SETUP_GUIDE.md)

- `Full Self-Hosted Deployment`：[L193](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/SETUP_GUIDE.md#L193)

## S22

**模型与供应商目录** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AVAILABLE_MODELS.md)

- `## Harnesses`：[L16](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AVAILABLE_MODELS.md#L16)
- `## OpenAI`：[L47](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AVAILABLE_MODELS.md#L47)
- `## OpenCode Go`：[L91](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AVAILABLE_MODELS.md#L91)
- `## DeepSeek`：[L157](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/AVAILABLE_MODELS.md#L157)

## S23

**Claude 程序、SDK 与认证配置** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md)

- `Settings > Provider Accounts`：[L42](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L42), [L70](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L70)
- `claude`：[L48](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L48), [L94](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L94), [L101](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L101), [L102](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L102), [L140](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L140), [L149](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L149), [L180](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L180), [L198](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L198)
- `ANTHROPIC_API_KEY`：[L25](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L25), [L26](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L26), [L98](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/CLAUDE_AGENT.md#L98)

## S24

**OpenAI 账号与 API Key 接入** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/OPENAI_MODELS.md)

- `Use API key`：[L42](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/OPENAI_MODELS.md#L42), [L50](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/OPENAI_MODELS.md#L50)
- `access-token`：[L64](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/docs/OPENAI_MODELS.md#L64)

## S25

**OpenCode 服务运行方式** · [原始文件](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/opencode.py)

- `opencode serve`：[L26](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/opencode.py#L26)
- `HTTP/SSE`：[L24](https://github.com/ColeMurray/background-agents/blob/4c470da615eaecbf8f64b0ae5a04666c99b4c536/packages/sandbox-runtime/src/sandbox_runtime/harness/opencode.py#L24)
