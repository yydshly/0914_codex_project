# 官方证据与复核方法

查阅日期：2026-09-16。所有能力描述均为公开文档证据，不代表真实请求成功。

| 编号 | 官方页面 | 本次使用范围 |
| --- | --- | --- |
| AK01 | [AgentKey 官网](https://agentkey.app/) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK02 | [AgentKey 文档总览](https://docs.agentkey.app/) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK03 | [AgentKey search](https://docs.agentkey.app/capabilities/search) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK04 | [AgentKey scrape](https://docs.agentkey.app/capabilities/scrape) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK05 | [AgentKey social](https://docs.agentkey.app/capabilities/social) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK06 | [AgentKey crypto](https://docs.agentkey.app/capabilities/crypto) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK07 | [AgentKey finance](https://docs.agentkey.app/capabilities/finance) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK08 | [AgentKey business](https://docs.agentkey.app/capabilities/business) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK09 | [AgentKey ecommerce](https://docs.agentkey.app/capabilities/ecommerce) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI01 | [AIsa 官网](https://aisa.one/) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI02 | [AIsa API 目录](https://aisa.one/api) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI03 | [AIsa 产品说明](https://aisa.one/llms.txt) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI04 | [AIsa Firecrawl](https://aisa.one/api/firecrawl) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI05 | [AIsa Jina Embeddings & Rerank](https://aisa.one/api/embeddings-rerank-api) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI06 | [AIsa 文档总览](https://aisa.one/docs/guides) | 产品定位、目录或获取方式；本地快照状态 200 |
| TH01 | [TikHub 官网](https://tikhub.io/) | 产品定位、目录或获取方式；本地快照状态 200 |
| TH02 | [TikHub API 目录](https://tikhub.io/api-reference) | 产品定位、目录或获取方式；本地快照状态 200 |
| TH03 | [TikHub 文档索引](https://docs.tikhub.io/) | 产品定位、目录或获取方式；本地快照状态 200 |
| TH04 | [TikHub 数据集](https://tikhub.io/datasets) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK10 | [AgentKey API 调用模型](https://docs.agentkey.app/api-reference/introduction) | 产品定位、目录或获取方式；本地快照状态 200 |
| AK11 | [AgentKey 身份认证](https://docs.agentkey.app/authentication) | 产品定位、目录或获取方式；本地快照状态 200 |
| AI07 | [AIsa 接口与接入方式](https://aisa.one/docs/by-interface) | 产品定位、目录或获取方式；本地快照状态 200 |
| TH05 | [TikHub MCP 平台映射](https://tikhub.io/mcp) | 产品定位、目录或获取方式；本地快照状态 200 |
| DR01 | [YouTube 官方 Atom 与推送通知](https://developers.google.com/youtube/v3/guides/push_notifications) | 产品定位、目录或获取方式；本地快照状态 200 |
| DR02 | [FRED 官方 API](https://fred.stlouisfed.org/docs/api/fred/) | 产品定位、目录或获取方式；网页阅读工具已核查；本地快照超时，未生成原件摘要 |

## 复核方式

读取公开网页的脚本位于 `src/fetch_sources.py`，只请求上述文档地址。页面原件和解析文本保存在被忽略的 `.cache/`；校验摘要、最终地址、时间和状态保存在 [source-manifest.json](source-manifest.json)。

来源登记由 `src/build_inventory.py` 生成。它核对 AIsa 接口卡片名称与顺序，并分别保留 Coming Soon；官网变更时需人工重审，不能将自动抓取结果直接视为有效能力。

本次没有注册账号、保存密钥、购买套餐、调用付费数据、安装插件或运行任何上游安装指令。

## 已发现的不一致

1. AIsa 的 Semrush 同时列出具体接口和 Coming Soon，来源表保留冲突。
2. AIsa 官网的 API、模型、Skills 总数与技术页面的接口/供应商统计口径不同，不作为独立数据源数量使用。
3. TikHub 首页宣称 16 个平台；公开 API 展示页、文档导航的分组不一致。本表逐名登记，不强行凑齐宣传数字；TikTok Shop 作为电商子产品单列。
4. AgentKey 官网社交目录比社交说明页更长，新增名称保留“官网列示”等级，未推定每项接口已可用。
5. AgentKey 首页与文档对超额计费表述不完全一致；本研究不据此给出价格承诺。
6. TikHub 首页以公开数据为主，但 Creator 等接口要求账号 Cookie，不能把所有端点视为无账号可访问。

## 范围与完整性

覆盖 AgentKey 首页及七个能力分类、AIsa API 总目录全部具名卡片与规划名单、TikHub 文档导航中具名内容平台；不声称枚举登录后动态目录、每个端点、底层未披露供应商或所有模型版本。
搜索服务可检索大量网站，不能据此将整个互联网登记为已接入的独立来源。品牌 logo、页脚社交链接、客户与投资方不算数据源。

项目是商业服务研究，不是三家开源代码库的复现；未复制上游源码，未对服务许可作推断。
