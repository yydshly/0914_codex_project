# 来源与服务总表

核查日期：2026-09-16。这是公开资料中具名来源与能力的登记，不是实测可用清单。

**获取方式：**查看 [API / MCP / RSS / 数据集与不确定项](access-methods.md)，逐来源、逐接入商记录调用方式、确认程度和授权条件。

**阅读口径：**“原始平台”说明数据内容来自哪里；“数据/搜索/采集服务”说明通过谁获取；“模型/处理/操作工具”不是数据来源。名称已合并，如 Rednote / Red Book / Xiaohongshu → 小红书。

- 文档列示 / 文档示例：官方文档明确提及，未做付费调用。
- 接口目录列示：有具体接口入口，未验证权限、成功率或字段完整度。
- 官网列示 / 官网提及：营销页可见，完整接口范围尚待核实。
- 即将上线：仅规划；状态冲突：同站不同位置的说明不一致。
- “—”只表示本次证据未确认，不表示绝对不支持。

**边界：**Financial、Scholar、Digital Asset Prices 是接口/能力名称，不能擅自补成某家具体供应商；同一原始平台出现多家接入，不意味着数据相互独立。

## 搜索与网页获取

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Brave Search | 搜索/回答服务；网页、新闻、图片及搜索上下文 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | — | — |
| Tavily | 搜索/回答服务；网页搜索与相关内容 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/tavily-search-api) | — |
| Serper | 搜索/回答服务；Google 搜索结果访问 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | — | — |
| Perplexity | 搜索/回答服务；带引用的联网回答 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/perplexity-api) | — |
| Parallel | 搜索/回答服务；网页搜索 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | — | — |
| Exa | 搜索/回答服务；语义搜索与网页内容 | 文档列示 [AK03](https://docs.agentkey.app/capabilities/search) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/exa) | — |
| Firecrawl | 采集/提取服务；网页正文转 Markdown | 文档列示 [AK04](https://docs.agentkey.app/capabilities/scrape) | 接口目录列示 [AI02](https://aisa.one/api), [AI04](https://aisa.one/api/firecrawl) · [接口入口](https://aisa.one/api/firecrawl) | — |
| Jina Reader | 采集/提取服务；URL 转 Markdown | 文档列示 [AK04](https://docs.agentkey.app/capabilities/scrape) | — | — |
| Bright Data | 采集/提取服务；网页访问，AgentKey 文档所述 unlock 返回 HTML | 文档列示 [AK04](https://docs.agentkey.app/capabilities/scrape) | 即将上线 [AI02](https://aisa.one/api) | — |
| Oxylabs | 搜索结果采集服务；本目录所列接口查询 AI 搜索回答及引用；非其完整产品能力 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/oxylabs) | — |
| BytePlus SearchInfinity | 搜索/提取服务；实时网页搜索与正文提取 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/byteplus) | — |
| Anthropic Web Search | 联网回答服务；搜索后的回答及引用 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/anthropic-websearch) | — |
| OpenAI Web Search | 联网回答服务；搜索后的回答及引用 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/openai-websearch) | — |

## 社交与内容平台

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| X / Twitter | 原始内容平台；帖子、账号、趋势 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/twitter-api) | 文档列示 [TH03](https://docs.tikhub.io/) |
| Reddit | 原始内容平台；社区帖子与评论 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/reddit-api) | 文档列示 [TH03](https://docs.tikhub.io/) |
| YouTube | 原始内容平台；视频、频道；文档提及转录文本 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/youtube-search-api) | 文档列示 [TH03](https://docs.tikhub.io/) |
| LinkedIn | 原始内容平台；职业账号与公司信息 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | 即将上线 [AI02](https://aisa.one/api) | 文档列示 [TH03](https://docs.tikhub.io/) |
| TikTok | 原始内容平台；短视频与创作者内容 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 抖音 | 原始内容平台；短视频、趋势 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 知乎 | 原始内容平台；问答与文章 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Bilibili | 原始内容平台；视频与创作者评论 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Threads | 原始内容平台；帖子与讨论 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 皮皮虾 | 原始内容平台；社区短视频 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 微信 | 原始内容平台；公众号文章 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Lemon8 | 原始内容平台；生活方式内容 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 微博 | 原始内容平台；话题与帖子 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Instagram | 原始内容平台；账号与媒体帖子 | 文档列示 [AK01](https://agentkey.app/), [AK05](https://docs.agentkey.app/capabilities/social) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/instagram-api) | 文档列示 [TH03](https://docs.tikhub.io/) |
| 小红书 | 原始内容平台；笔记、产品评价 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 快手 | 原始内容平台；短视频与创作者内容 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Facebook | 原始内容平台；页面与公开帖子 | 官网列示 [AK01](https://agentkey.app/) | 即将上线 [AI02](https://aisa.one/api) | — |
| Pinterest | 原始内容平台；Pins 与视觉内容 | 官网列示 [AK01](https://agentkey.app/) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/pinterest-api) | — |
| Discord | 原始内容平台；社区频道，具体访问范围待核 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Telegram | 原始内容平台；频道与群组，具体访问范围待核 | 官网列示 [AK01](https://agentkey.app/) | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| Snapchat | 原始内容平台；公开故事与账号 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Twitch | 原始内容平台；直播与频道资料 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Product Hunt | 原始内容平台；产品发布与讨论 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| 西瓜视频 | 原始平台；视频与账号接口 | — | — | 文档列示 [TH03](https://docs.tikhub.io/) |
| 今日头条 | 原始平台；文章、内容与账号接口 | — | — | 文档列示 [TH03](https://docs.tikhub.io/) |

## 金融与链上

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Tushare | 数据服务/数据库；中国市场数据 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Yahoo Finance | 数据服务/数据库；行情与新闻 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| FRED | 数据服务/数据库；美国宏观时间序列 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Finnhub | 数据服务/数据库；市场数据与披露 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Alpha Vantage | 数据服务/数据库；股票、外汇与指标 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Digital Asset Prices | 能力分类（供应商未披露）；数字资产参考价格 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Chainbase | 链上数据服务；钱包余额等链上数据 | 文档示例 [AK06](https://docs.agentkey.app/capabilities/crypto) | — | — |
| Polymarket | 预测市场平台；事件、市场价格与订单簿 | 文档列示 [AK06](https://docs.agentkey.app/capabilities/crypto) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/polymarket) | — |
| Kalshi | 预测市场平台；事件、市场价格与订单簿 | 文档列示 [AK06](https://docs.agentkey.app/capabilities/crypto) | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/kalshi) | — |
| ENS | 链上命名系统；名称与地址解析 | 文档列示 [AK06](https://docs.agentkey.app/capabilities/crypto) | — | — |
| Space ID | 链上命名系统；名称与地址解析 | 文档列示 [AK06](https://docs.agentkey.app/capabilities/crypto) | — | — |
| Financial | 接口分类（供应商未披露）；行情、财报、新闻及 SEC 披露 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/financial-api) | — |
| EDINET | 披露系统；日本财务披露检索与文档 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/edinet-api) | — |
| CoinGecko | 数据服务；数字资产价格、历史与市场数据 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/coingecko) | — |

## 电商与房产

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| 淘宝 | 原始平台；商品、价格与评价 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| 京东 | 原始平台；商品与价格 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| Amazon | 原始平台；商品与榜单 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| 1688 | 原始平台；批发商品 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| 抖音电商 | 原始平台；店铺商品目录 | 官网列示 [AK01](https://agentkey.app/) | — | — |
| TikTok Shop | 原始平台；商品与店铺 | 官网列示 [AK01](https://agentkey.app/) | 官网提及 [AI01](https://aisa.one/) | 文档列示 [TH03](https://docs.tikhub.io/) |
| 贝壳 | 原始平台；房产挂牌 | 官网列示 [AK01](https://agentkey.app/) | — | — |

## 企业与营销

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Crunchbase | 企业数据库；公司与融资信息 | 官网列示 [AK01](https://agentkey.app/) | 即将上线 [AI02](https://aisa.one/api) | — |
| Similarweb | 网站分析服务；流量、受众、渠道和关键词 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/similarweb) | — |
| Ahrefs | SEO 数据服务；域名、流量与关键词指标 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/ahrefs) | — |
| Semrush | SEO 数据服务；关键词、反向链接与竞品指标 | — | 状态冲突 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/semrush) | — |
| DataForSEO | 搜索/营销数据服务；SERP、关键词、反向链接等多类接口 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/dataforseo) | — |
| Apollo | 商业数据与操作服务；公司、人员、联系人与 CRM 对象 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/apollo) | — |
| WaveInflu | 创作者数据服务；创作者联系方式与相似达人发现 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/waveinflu) | — |
| CNPJá | 企业登记查询服务；巴西企业登记资料 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/cnpja) | — |

## 模型与处理工具

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Chat | 模型网关；文本与多模态生成；不是原始数据来源 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/chat-api) | — |
| Jina Embeddings & Rerank | 向量/排序服务；文本向量化与检索结果重排序 | — | 接口目录列示 [AI02](https://aisa.one/api), [AI05](https://aisa.one/api/embeddings-rerank-api) · [接口入口](https://aisa.one/api/embeddings-rerank-api) | — |
| Matching Markets | 跨源匹配服务；匹配 Polymarket 与 Kalshi 体育市场 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/matching-markets) | — |

## 学术研究

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Scholar | 接口分类（供应商未披露）；论文及研究资料检索，作者、年份、引用等 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/scholar-api) | — |

## 业务操作工具

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| AgentMail | 邮件服务；邮箱、邮件、草稿、收发操作；不是公共资料库 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/agentmail) | — |

## 天气与地理

| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |
| --- | --- | --- | --- | --- |
| Open-Meteo | 数据服务；天气、历史、气候、空气质量及地理编码 | — | 接口目录列示 [AI02](https://aisa.one/api) · [接口入口](https://aisa.one/api/openmeteo) | — |

## AIsa 尚未上线与矛盾项

目录共出现 80 个 Coming Soon 名称，其中 Semrush 同时存在接口入口，单独标为冲突。以下保留完整名单，不计入已列接口数量。[官方目录](https://aisa.one/api)

Google Places、Google Ads、Facebook、Shopee、Lazada、AliExpress、Yelp、Stack Exchange、Quora、同花顺、LinkedIn、ZoomInfo、People Data Labs、Clearbit、Lusha、Coresignal、Crustdata、RocketReach、LeadIQ、Datagma、SMARTe、Aviato、Hunter、Findymail、Prospeo、Icypeas、ContactOut、Wiza、BetterContact、FullEnrich、LeadMagic、Dropcontact、Enrow、Upcell、Limadata、Emailable、DeBounce、BounceBan、Catch-all Verifier、ClearoutPhone、SureConnect、Trestle、HG Insights、Beauhurst、HitHorizons、Enigma、CB Insights、NBS Japan、Firmable、Owler、Crunchbase、PitchBook、Dealroom、Harmonic.ai、BuiltWith、Sumble、Openmart、Bombora、Demandbase、TrustRadius、Warmly、Leadfeeder、RB2B、Snitcher、MadKudu、Crossbeam、The Swarm、Semrush、Adbeat、Google News、Google PageSpeed、Upriver、Google Maps、Google Shopping、Modash、Upfluence、Influencer Club、Bright Data、Apify、Hacker News。

## 逐条核查备注与后续清理

机器可读版：[source-inventory.json](source-inventory.json)。以下备注区分官网提及、权限条件和数据处理责任。

- **R001 Brave Search**：。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R002 Tavily**：AIsa：目录有接口入口；尚未调用验证。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R003 Serper**：。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R004 Perplexity**：AIsa：目录有接口入口；尚未调用验证。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R005 Parallel**：。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R006 Exa**：AIsa：目录有接口入口；尚未调用验证。清理建议：保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据。
- **R007 Firecrawl**：AIsa：目录有接口入口；尚未调用验证。清理建议：提取正文后仍需去重、补时间和来源；HTML 需另行解析。
- **R008 Jina Reader**：。清理建议：提取正文后仍需去重、补时间和来源；HTML 需另行解析。
- **R009 Bright Data**：AIsa：不得计入当前已接入能力。清理建议：提取正文后仍需去重、补时间和来源；HTML 需另行解析。
- **R010 X / Twitter**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：目录有接口入口；尚未调用验证。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R011 Reddit**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：目录有接口入口；尚未调用验证。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R012 YouTube**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：目录有接口入口；尚未调用验证。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R013 LinkedIn**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：不得计入当前已接入能力。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R014 TikTok**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R015 抖音**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R016 知乎**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R017 Bilibili**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R018 Threads**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R019 皮皮虾**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R020 微信**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R021 Lemon8**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R022 微博**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R023 Instagram**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：目录有接口入口；尚未调用验证。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R024 小红书**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R025 快手**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R026 Facebook**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；AIsa：不得计入当前已接入能力。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R027 Pinterest**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；AIsa：目录有接口入口；尚未调用验证。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R028 Discord**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R029 Telegram**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核；TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R030 Snapchat**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R031 Twitch**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R032 Product Hunt**：AgentKey：平台名不等于上游接口商名；实际字段、授权和历史范围待核。清理建议：按平台+内容ID去重；保留评论父子关系；统一时间与指标口径。
- **R033 Tushare**：。清理建议：统一代码、交易所、币种、时区、频率及复权口径。
- **R034 Yahoo Finance**：。清理建议：统一代码、交易所、币种、时区、频率及复权口径。
- **R035 FRED**：。清理建议：统一代码、交易所、币种、时区、频率及复权口径。
- **R036 Finnhub**：。清理建议：统一代码、交易所、币种、时区、频率及复权口径。
- **R037 Alpha Vantage**：。清理建议：统一代码、交易所、币种、时区、频率及复权口径。
- **R038 Digital Asset Prices**：AgentKey：官网名称是能力标签，不能据此推断具体数据商。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R039 淘宝**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R040 京东**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R041 Amazon**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R042 1688**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R043 抖音电商**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R044 TikTok Shop**：TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据；AIsa：官网声称有此数据；当前 API 总目录未找到对应独立入口，列待核，不推定全量 TikTok 数据支持。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R045 贝壳**：。清理建议：统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并。
- **R046 Crunchbase**：AIsa：不得计入当前已接入能力。清理建议：统一企业实体；保留事件日期与数据来源。
- **R047 Chainbase**：AgentKey：文档给出 Chainbase/GetAccountBalance 示例，非完整供应商目录。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R048 Polymarket**：AIsa：目录有接口入口；尚未调用验证。清理建议：核对结算规则与到期时间；名称相似不代表同一事件。
- **R049 Kalshi**：AIsa：目录有接口入口；尚未调用验证。清理建议：核对结算规则与到期时间；名称相似不代表同一事件。
- **R050 ENS**：AgentKey：目标系统已列示，具体接口供应商未披露。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R051 Space ID**：AgentKey：目标系统已列示，具体接口供应商未披露。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R052 西瓜视频**：TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R053 今日头条**：TikHub：部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据。清理建议：按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间。
- **R054 Similarweb**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R055 Chat**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R056 Jina Embeddings & Rerank**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R057 Oxylabs**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R058 BytePlus SearchInfinity**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R059 Anthropic Web Search**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R060 OpenAI Web Search**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R061 Ahrefs**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R062 Semrush**：AIsa：同一目录既有19个接口入口，又在下方标 Coming Soon；以具体接口为候选，保留冲突待核。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R063 Financial**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R064 EDINET**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R065 Scholar**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R066 Matching Markets**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R067 CoinGecko**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R068 DataForSEO**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R069 Apollo**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R070 AgentMail**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R071 WaveInflu**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R072 Open-Meteo**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
- **R073 CNPJá**：AIsa：目录有接口入口；尚未调用验证。清理建议：按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本。
