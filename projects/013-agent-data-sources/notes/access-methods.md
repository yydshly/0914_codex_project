# 获取方式：API、MCP、RSS 与其他路径

核查日期：2026-09-16。将“我们怎样调用接入商”与“接入商怎样获得原始数据”分开。未调用真实业务接口。

## 先看结论

**我们怎么调用、后台怎么采集、实测是否成功，是三个独立问题。后台采集未披露，不影响确认对外 API 的调用方式。**

当前148项中：46项至少在一家接入商有来源级接口目录；26项仅确认统一接入或来源宣称；1项上线状态冲突；75项只有规划记录。前两项均不代表已完成实际调用。

| 方式 | 用途 | 不能据此推断 |
| --- | --- | --- |
| API | 程序按参数请求数据或运行任务 | 聚合商 API 不等于原始平台官方 API |
| MCP | 让 AI 发现和调用工具，常包装 API | 不是新数据源；API 存在不保证有对应 MCP 工具 |
| RSS / Atom | 订阅来源发布的更新条目 | 不能默认包含全文、评论、搜索和历史全量 |
| Webhook | 来源有更新时推送到回调服务 | 不等于历史批量抓取；需要接收端 |
| 网页提取 | 从 URL 获取 HTML 或提取正文 | 本地调用仍可通过 API；这是另一层面的采集方式 |
| 数据集下载 | 获得特定范围的批量快照或定期更新 | 不等于实时 API；覆盖、时间和字段看购买项 |
| SDK / 浏览器扩展 / Skill | 提供调用封装、操作界面或任务步骤 | 不是独立原始来源，不会自动扩展权限 |

## 三家总结

- AgentKey：统一网关 API 与 MCP；需要 master key。仅官网列名的来源仍需发现具体工具。
- AIsa：有具体 HTTP API，模型和数据路径分开。MCP 是独立目录，不能把所有 API 家族默认标为 MCP 已接入；业务动作可能另需 OAuth。
- TikHub：HTTP API / Python SDK；MCP 目录有具名平台与 others 分组；部分来源另有数据集和浏览器扩展。TikTok Creator 明确要求账户 Cookie。
- RSS：未确认这三家为清单中来源提供 RSS/Atom 订阅。另核实 YouTube 官方 Atom/Webhook 路径，仅适合频道更新；不能当作评论或字幕接口。
- 原始平台是否提供官方开放 API、聚合商是否实际使用它，均需独立证据；未披露的地方标为不确定。

## 逐来源、逐接入商登记

下列 API/MCP 描述有的仅确认了平台统一入口，具体来源级工具仍待核，详见“确认程度”。完整结构化字段保存在 [source-inventory.json](source-inventory.json)。

| 来源 | 接入商 | 我们获取的方式 | 确认程度 | 授权与条件 |
| --- | --- | --- | --- | --- |
| Brave Search | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Tavily | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Tavily | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Serper | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Perplexity | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Perplexity | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Parallel | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Exa | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Exa | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Firecrawl | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Firecrawl | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Jina Reader | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Bright Data | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Bright Data | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| X / Twitter | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| X / Twitter | TikHub | API / MCP / 数据集下载 / 浏览器扩展 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| X / Twitter | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | 读取使用 AIsa key；发帖、点赞、关注等写操作还需对应 OAuth 授权。 |
| Reddit | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Reddit | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Reddit | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| YouTube | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| YouTube | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| YouTube | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| LinkedIn | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| LinkedIn | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| LinkedIn | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| TikTok | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| TikTok | TikHub | API / MCP / 数据集下载 / 浏览器扩展 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH02](https://tikhub.io/api-reference) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 TikTok Creator 接口明确要求账户 Cookie，不是只用 API key 就能读取任意创作者后台。 |
| 抖音 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 抖音 | TikHub | API / MCP / 数据集下载 / 浏览器扩展 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 知乎 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 知乎 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Bilibili | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Bilibili | TikHub | API / MCP / 数据集下载 / 浏览器扩展 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Threads | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Threads | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 皮皮虾 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 皮皮虾 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 微信 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 微信 | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Lemon8 | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Lemon8 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 微博 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 微博 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Instagram | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Instagram | TikHub | API / MCP / 数据集下载 / 浏览器扩展 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Instagram | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| 小红书 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 小红书 | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 快手 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 快手 | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Facebook | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Facebook | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Pinterest | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Pinterest | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Discord | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Telegram | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Telegram | TikHub | API | 来源接口已列出 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Snapchat | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Twitch | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Product Hunt | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Tushare | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Yahoo Finance | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| FRED | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Finnhub | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Alpha Vantage | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Digital Asset Prices | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 淘宝 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 京东 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Amazon | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 1688 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 抖音电商 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| TikTok Shop | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| TikTok Shop | TikHub | API / MCP / 数据集下载 | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) [TH04](https://tikhub.io/datasets) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| TikTok Shop | AIsa | API | 来源级入口待核 [AI01](https://aisa.one/) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| 贝壳 | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Crunchbase | AgentKey | API / MCP | 平台入口已确认，来源级工具待核 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Crunchbase | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Chainbase | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Polymarket | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Polymarket | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Kalshi | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Kalshi | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| ENS | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| Space ID | AgentKey | API / MCP | 分类文档列示，具体工具待发现 [AK02](https://docs.agentkey.app/) [AK10](https://docs.agentkey.app/api-reference/introduction) [AK11](https://docs.agentkey.app/authentication) | AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。 |
| 西瓜视频 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| 今日头条 | TikHub | API / MCP | 来源接口已列出；文档列示 [TH01](https://tikhub.io/) [TH03](https://docs.tikhub.io/) [TH05](https://tikhub.io/mcp) | TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。 |
| Similarweb | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Chat | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Jina Embeddings & Rerank | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Oxylabs | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| BytePlus SearchInfinity | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Anthropic Web Search | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| OpenAI Web Search | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Ahrefs | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Semrush | AIsa | API | 接口已列出，但上线状态有冲突 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Financial | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| EDINET | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Scholar | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Matching Markets | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| CoinGecko | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| DataForSEO | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Apollo | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| AgentMail | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| WaveInflu | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Open-Meteo | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| CNPJá | AIsa | API | 来源接口已列出 [AI02](https://aisa.one/api) [AI07](https://aisa.one/docs/by-interface) | AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。 |
| Google Places | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Google Ads | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Shopee | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Lazada | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| AliExpress | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Yelp | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Stack Exchange | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Quora | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| 同花顺 | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| ZoomInfo | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| People Data Labs | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Clearbit | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Lusha | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Coresignal | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Crustdata | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| RocketReach | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| LeadIQ | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Datagma | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| SMARTe | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Aviato | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Hunter | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Findymail | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Prospeo | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Icypeas | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| ContactOut | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Wiza | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| BetterContact | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| FullEnrich | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| LeadMagic | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Dropcontact | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Enrow | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Upcell | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Limadata | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Emailable | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| DeBounce | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| BounceBan | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Catch-all Verifier | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| ClearoutPhone | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| SureConnect | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Trestle | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| HG Insights | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Beauhurst | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| HitHorizons | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Enigma | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| CB Insights | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| NBS Japan | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Firmable | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Owler | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| PitchBook | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Dealroom | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Harmonic.ai | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| BuiltWith | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Sumble | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Openmart | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Bombora | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Demandbase | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| TrustRadius | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Warmly | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Leadfeeder | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| RB2B | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Snitcher | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| MadKudu | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Crossbeam | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| The Swarm | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Adbeat | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Google News | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Google PageSpeed | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Upriver | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Google Maps | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Google Shopping | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Modash | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Upfluence | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Influencer Club | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Apify | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |
| Hacker News | AIsa | 未确认入口（规划） | 即将上线  | 未上线/待核 |

## 单独核实的原站直连路径

### YouTube

这是原站直连方式，不是已证实由 AgentKey/AIsa/TikHub 转发的 RSS。Topic 模板：https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID；需替换真实频道 ID。

- **RSS/Atom**：YouTube 官方频道更新使用 Atom；可获上传及标题/描述更新通知，不包括完整评论、字幕或全部历史数据。 [DR01](https://developers.google.com/youtube/v3/guides/push_notifications)
- **Webhook**：官方 PubSubHubbub 推送：订阅频道 topic，准备可接收通知的回调服务。 [DR01](https://developers.google.com/youtube/v3/guides/push_notifications)

### FRED

可另行评估直接使用 FRED 官方 API；这不证明 AgentKey 后台实际采用这条路径。RSS/Atom 尚未核查。

- **原站 API**：FRED 官方提供系列、观测值与发布数据 API；密钥与调用条件按官方版本文档另行配置。 [DR02](https://fred.stlouisfed.org/docs/api/fred/)

## 明确尚不确定的部分

1. 三家每个来源背后的实际采集方式、具体上游数据商及原站授权链路。
2. 仅官网列示或规划中的来源，能否发现并成功调用对应工具。
3. 除本页列出两种原站直连示例外，其余来源的官方 API / RSS / 下载路径未逐项核查。
4. 每个接口的授权范围、限流、历史覆盖、分页完整性、具体费用。
5. Telegram 对应 TikHub MCP 的映射；AIsa 每个 API 对应的 MCP 状态。

不确定不等于没有能力，也不等于可以默认使用。以上缺口不影响本轮公开资料整理，但实际接入前需要针对选定来源补查。
