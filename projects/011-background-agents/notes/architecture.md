# 技术原理与源码核对

全部依据固定在研究提交，具体行号见 [来源索引](sources.md)。本页为静态调用链分析。

## 一条任务怎样执行

1. 网页或集成入口把内容、作者、附件与模型选项送入控制服务。
2. 会话消息进入持久化队列。`processMessageQueue()` 检查会话状态、停止确认、预算和正在运行的消息，再取下一条待处理任务。
3. 分发前校验模型与运行层兼容性及认证条件。没有沙箱连接时，异步请求启动沙箱；消息保持待处理，避免把一次 HTTP 请求长时间挂住。
4. 有连接时通过 `startMessageProcessing()` 认领执行，再把指令与作者信息发给沙箱。这也说明不能把同一会话的多用户输入理解为同时执行。
5. Bridge 接收 prompt，以异步任务运行，通过 `harness.run_prompt()` 调用代理运行层。
6. 代理执行模型与工具交互，产生文本、工具调用和步骤事件。Bridge 转发事件，并负责统一发出 `execution_complete`。
7. 控制服务持久化与展示状态；如果要求创建 PR，进入分支推送和代码托管服务调用流程。

依据：[S03](sources.md#s03)、[S04](sources.md#s04)、[S05](sources.md#s05)、[S08](sources.md#s08)。

## 为什么断开网页还能执行

首先，消息状态放在服务端；浏览器是任务的观察与输入入口。其次，沙箱 Bridge 将正在执行的 prompt 与连接生命周期分离：WebSocket 关闭时会取消一部分连接相关任务，但 prompt 刻意不加入该取消集合。临时网络问题走重连，认证失效或会话终止有单独退出路径。

这能支持“暂时断连继续工作”的设计结论，不能证明主机崩溃、沙箱被杀或存储失效时任务都能无损恢复。[S03](sources.md#s03)、[S04](sources.md#s04)

## 谁负责什么

| 层次 | 责任 | 实现位置 |
| --- | --- | --- |
| 网页与 Bot | 收集需求、展示结果、连接既有协作入口 | `packages/web`、`slack-bot`、`github-bot`、`linear-bot` |
| 控制服务 | 身份、会话、队列、沙箱生命周期、结果记录 | `packages/control-plane` |
| Supervisor | 准备仓库与环境、管理代理相关进程 | `packages/sandbox-runtime/.../supervisor.py` |
| Bridge | 收发指令与执行事件、调用运行层、处理轮次完成 | `packages/sandbox-runtime/.../bridge.py` |
| Harness | 用统一接口调用具体编程代理 | `.../harness/base.py`、`opencode.py`、`claude.py` |
| 沙箱供应商 | 创建隔离计算环境、提供相应恢复能力 | `control-plane/src/sandbox/providers` |

`Harness` 是模型和工具循环的运行适配层。该版本只有 `opencode` 与 `claude` 两种可部署标识；模型名单和运行层名单不是同一回事。OpenCode 路径对模型家族更通用，Claude 路径限制为 Anthropic；选择还要通过认证兼容性校验。[S05](sources.md#s05)、[S06](sources.md#s06)

## 如何减少环境准备时间

- 全新环境：创建沙箱、获取仓库、运行 provisioning 脚本、启动运行服务，再启动代理。
- 预构建：提前保存仓库和安装过的依赖，新会话从近期基线开始，再同步代码。
- 续接会话：恢复已保存文件状态，或恢复同一持久沙箱，避免每次重新安装。
- 提前预热：用户开始输入时即可发起环境准备。

两类 hook 分工：`setup.sh` 处理安装准备，预构建或快照恢复时通常跳过；`start.sh` 用于每次非构建启动，存在但失败会使启动失败。恢复文件不保证内存中的服务仍在，所以仍有运行服务启动阶段。[S01](sources.md#s01)、[S02](sources.md#s02)

| 后端 | 代码声明支持文件快照 | 代码声明支持持久沙箱恢复 | 依据 |
| --- | --- | --- | --- |
| Modal | 是 | 否 | S12 |
| Daytona | 否 | 是 | S13 |
| E2B | 否 | 是 | S14 |
| Vercel Sandbox | 是 | 否 | S15 |
| OpenComputer | 是 | 是 | S16 |

表格来自适配器的能力标志，不能当作实际服务可用性或性能测试。尤其 OpenComputer 当前同时声明两种能力，不应仅根据概览文档把它概括为只有快照。

## 三种并行 / 协同机制

| 方式 | 工作环境 | 适合场景 | 边界 |
| --- | --- | --- | --- |
| 多仓库会话 | 一个沙箱中并排多个仓库 | 前后端协调修改 | 各仓库分别交付 PR |
| 主子会话 | 子会话各自有独立沙箱 | 同库独立子任务 | 子任务单仓库、限定父主仓库、深度有限 |
| 定时任务 fan-out | 每个目标仓库一个会话 | 同一维护任务批量执行 | 文档只对 scheduled automations 开放多仓库分发 |

`handleSpawnChild()` 的 `MAX_SPAWN_DEPTH = 2` 在创建前检查；还检查累计子任务数并读取并发限制配置。创建输入使用 `spawnContext.baseBranch`，因此不能假定父代理刚编辑的未提交文件已经出现在子沙箱。[S07](sources.md#s07)、[S09](sources.md#s09)

## PR 身份与文档差异

当前 `pull-request-service.ts` 使用 `input.promptingAuth ?? appAuth` 选择认证，再调用 `createPullRequest`。这与 README 提及的 App 回退一致。部分文档及类注释仍描述缺少用户 OAuth 时返回手动 PR 链接，存在表述滞后。

本研究结论限于：该执行路径存在 App 身份创建 PR 的回退；不能统一宣称所有 PR 都以用户本人名义创建，也不能把旧注释当作当前唯一行为。[S08](sources.md#s08)

## 系统边界

Cloudflare 部署使用 Workers、会话 Durable Objects/SQLite 与共享 D1；容器部署用 Node 进程、卷上的 SQLite、S3 兼容对象存储替代相关平台组件。容器文档明确当前恢复逻辑依赖单实例，不支持直接让多个活跃控制服务共享同一数据目录。[S10](sources.md#s10)

GitHub App 的安装范围构成共享仓库访问边界；用户角色控制与会话授权不能替代逐用户仓库访问校验。部署定位是同一组织内互信成员使用。[S01](sources.md#s01)
