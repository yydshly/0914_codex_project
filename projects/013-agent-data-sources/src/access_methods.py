"""Evidence-bounded acquisition methods. Unknown upstream collection is explicit."""

TH_MCP = {
    'TikTok':'tiktok', 'TikTok Shop':'tiktok', '抖音':'douyin', 'Instagram':'instagram',
    '小红书':'xiaohongshu', '微博':'weibo', 'Bilibili':'bilibili', 'YouTube':'youtube',
    '快手':'kuaishou', '知乎':'zhihu', 'LinkedIn':'linkedin', 'Reddit':'reddit',
    '微信':'wechat', 'X / Twitter':'twitter', 'Threads':'threads',
    'Lemon8':'others', '皮皮虾':'others', '西瓜视频':'others', '今日头条':'others',
}
TH_DATASETS = {'TikTok','TikTok Shop','抖音','Bilibili','Instagram','LinkedIn','小红书','X / Twitter','微信','快手','YouTube'}
TH_EXTENSION = {'TikTok','抖音','Instagram','X / Twitter','Bilibili'}
UNKNOWN_UPSTREAM = '未披露到该来源的具体采集链路；不能判断是原站官方 API、授权数据、网页抓取还是其他方式。'
UNKNOWN_RSS = '本次资料未确认经此接入商提供 RSS/Atom；不等于原始来源没有订阅源。'


def method(kind, detail, evidence, certainty='文档列示'):
    return dict(kind=kind, detail=detail, evidence=evidence, certainty=certainty)


def annotate_access(inventory, evidence):
    for row in inventory:
        name = row['name']
        row['direct_access'] = []
        row['direct_access_note'] = '原站直连 API、RSS/Atom 或下载方式尚未逐项核查；不能从聚合平台名称推定。'
        for provider, c in row['coverage'].items():
            state = 'planned' if c['status']=='即将上线' else 'conflict' if c['status']=='状态冲突' else 'confirmed' if provider=='TikHub' or (provider=='AIsa' and c['status']=='接口目录列示') else 'declared'
            a = dict(methods=[], upstream=UNKNOWN_UPSTREAM, rss=UNKNOWN_RSS,
                     authorization='待核实', output='按具体接口返回字段确定', unknowns=[], entry_state=state)
            c['access'] = a
            if c['status'] == '即将上线':
                a.update(authorization='未上线/待核', output='待核', upstream='未确认上线，获取链路也未确认。')
                a['unknowns'] = ['无已确认获取入口，不能按当前可调用接口计入。']
                continue
            if provider == 'AgentKey':
                basis = '平台入口已确认，来源级工具待核' if c['status'].startswith('官网') else '分类文档列示，具体工具待发现'
                a['methods'] = [
                    method('API', '平台声明提供 API；公开参考主要描述 MCP 工具契约，确切 REST 路径与请求格式需到控制台核对。不能据官网列名推定端点。', ['AK02','AK10','AK11'], basis),
                    method('MCP', '通过 AgentKey MCP 调用工具；具体来源和操作以发现/描述结果为准。', ['AK02','AK10'], basis),
                ]
                a['authorization'] = 'AgentKey master key 与相应额度；来源是否另有权限要求，需查看具体工具。'
                a['unknowns'] = ['尚未发现并执行该来源的具体工具，字段、分页、成功率与费用未验证。']
            elif provider == 'AIsa':
                if c['status'] == '官网提及':
                    a['methods'] = [method('API','官网提及数据能力，但未找到对应独立端点；API 获取路径待核。',['AI01','AI07'],'来源级入口待核')]
                else:
                    a['methods'] = [method('API','调用 AIsa 的对应 HTTP API；具体入口见本条接口链接。',['AI02','AI07'],'来源接口已列出' if state=='confirmed' else '接口已列出，但上线状态有冲突')]
                a['authorization'] = 'AIsa API key；业务动作可能另外需要 OAuth 或委托凭证。'
                a['unknowns'] = ['该来源 MCP 覆盖需查 AIsa 实时 MCP 目录，不能由 HTTP API 存在推定。']
                if name == 'X / Twitter':
                    a['authorization'] = '读取使用 AIsa key；发帖、点赞、关注等写操作还需对应 OAuth 授权。'
                if c['status'] == '状态冲突':
                    a['unknowns'].append('Semrush 目录有端点也有 Coming Soon；调用前需核对端点状态。')
            else:
                a['methods'] = [method('API','通过 TikHub 的 HTTP API，或其 Python SDK 调用；SDK 是调用封装，不是独立来源。',['TH01','TH03'],'来源接口已列出')]
                a['authorization'] = 'TikHub API token（Bearer）；特殊端点是否需要额外账号凭证须逐项查看。'
                a['output'] = '实时接口主要返回 JSON；不保证每项都含全文、媒体文件或全部评论。'
                a['upstream'] = '文档按 Web/App/Creator 等分组；这些名称不能证明原站官方开放 API，底层采集机制与授权链路尚未逐项披露或核验。'
                if name in TH_MCP:
                    slug=TH_MCP[name]
                    a['methods'].append(method('MCP',f'官方 MCP 目录映射到 {slug} 服务；端点 https://mcp.tikhub.io/{slug}/mcp 。具体工具需再发现。',['TH05']))
                else:
                    a['unknowns'].append('Telegram 在 API 文档中存在，但本次 MCP 目录未找到明确映射；MCP 方式不确定。')
                if name in TH_DATASETS:
                    a['methods'].append(method('数据集下载','购买所需数据集后导出 CSV、JSON、JSONL 或 Parquet；不是实时接口，具体对象、日期与更新周期看数据集。',['TH04']))
                if name in TH_EXTENSION:
                    a['methods'].append(method('浏览器扩展','TikHub 浏览器侧栏可用于采集/分析，仍需自己的 TikHub key；不是自动获得任意页面数据。',['TH01']))
                if name=='TikTok':
                    a['authorization'] += ' TikTok Creator 接口明确要求账户 Cookie，不是只用 API key 就能读取任意创作者后台。'
                    a['methods'][0]['evidence'].append('TH02')
            if name in ('Firecrawl','Jina Reader','Bright Data'):
                a['upstream'] = '网页抓取/正文提取服务：输入目标 URL，经供应商服务取得内容；更底层请求或反爬实现未核查。'
                a['output'] = 'Bright Data 在 AgentKey 所列 unlock 路径返回原始 HTML。' if name=='Bright Data' else '正文/Markdown 等；具体输出格式取决于接口与参数。'
            elif name in ('Brave Search','Tavily','Serper','Exa','Parallel','Perplexity','BytePlus SearchInfinity','OpenAI Web Search','Anthropic Web Search','Oxylabs'):
                a['upstream'] = '搜索/联网回答服务；搜索结果、网页正文与模型生成回答的性质不同。更底层索引或采集方式未逐项核查。'
            elif row['category']=='模型与处理工具':
                a['upstream'] = '输入材料交给模型、向量/排序或匹配工具处理；不属于新增原始信息采集。'
            elif name=='AgentMail':
                a['upstream'] = '操作已创建或获授权的邮箱与邮件；不是公共网页信息采集。'
            for m in a['methods']:
                m['evidence_urls']=[evidence[r]['url'] for r in m['evidence']]

        if name=='YouTube':
            row['direct_access']=[method('RSS/Atom','YouTube 官方频道更新使用 Atom；可获上传及标题/描述更新通知，不包括完整评论、字幕或全部历史数据。',['DR01']),
                                  method('Webhook','官方 PubSubHubbub 推送：订阅频道 topic，准备可接收通知的回调服务。',['DR01'])]
            row['direct_access_note']='这是原站直连方式，不是已证实由 AgentKey/AIsa/TikHub 转发的 RSS。Topic 模板：https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID；需替换真实频道 ID。'
        elif name=='FRED':
            row['direct_access']=[method('原站 API','FRED 官方提供系列、观测值与发布数据 API；密钥与调用条件按官方版本文档另行配置。',['DR02'])]
            row['direct_access_note']='可另行评估直接使用 FRED 官方 API；这不证明 AgentKey 后台实际采用这条路径。RSS/Atom 尚未核查。'
        for m in row['direct_access']:
            m['evidence_urls']=[evidence[r]['url'] for r in m['evidence']]
        states={c['access']['entry_state'] for c in row['coverage'].values()}
        row['entry_state']=next(state for state in ['confirmed','conflict','declared','planned'] if state in states)

    # Published paths from existing evidence; illustrative requests only, never executed here.
    examples = {
        ('TikTok','TikHub'): dict(verb='GET', url='https://api.tikhub.io/api/v1/tiktok/app/v3/fetch_one_video', purpose='按 aweme_id 获取视频资料', evidence='TH02'),
        ('Firecrawl','AIsa'): dict(verb='POST', url='https://api.aisa.one/apis/v1/firecrawl/scrape', purpose='提交目标 URL，提取网页正文；完整请求参数见接口说明', evidence='AI04'),
        ('Jina Embeddings & Rerank','AIsa'): dict(verb='POST', url='https://api.aisa.one/v1/rerank', purpose='按查询对候选文档排序；完整请求参数见接口说明', evidence='AI05'),
    }
    for row in inventory:
        for provider,c in row['coverage'].items():
            example=examples.get((row['name'],provider))
            c['access']['example']=dict(example, evidence_url=evidence[example['evidence']]['url']) if example else None


def write_access_notes(root, inventory):
    text = ['# 获取方式：API、MCP、RSS 与其他路径', '',
            '核查日期：2026-09-16。将“我们怎样调用接入商”与“接入商怎样获得原始数据”分开。未调用真实业务接口。', '',
            '## 先看结论', '',
            '**我们怎么调用、后台怎么采集、实测是否成功，是三个独立问题。后台采集未披露，不影响确认对外 API 的调用方式。**', '',
            '当前148项中：46项至少在一家接入商有来源级接口目录；26项仅确认统一接入或来源宣称；1项上线状态冲突；75项只有规划记录。前两项均不代表已完成实际调用。', '',
            '| 方式 | 用途 | 不能据此推断 |', '| --- | --- | --- |',
            '| API | 程序按参数请求数据或运行任务 | 聚合商 API 不等于原始平台官方 API |',
            '| MCP | 让 AI 发现和调用工具，常包装 API | 不是新数据源；API 存在不保证有对应 MCP 工具 |',
            '| RSS / Atom | 订阅来源发布的更新条目 | 不能默认包含全文、评论、搜索和历史全量 |',
            '| Webhook | 来源有更新时推送到回调服务 | 不等于历史批量抓取；需要接收端 |',
            '| 网页提取 | 从 URL 获取 HTML 或提取正文 | 本地调用仍可通过 API；这是另一层面的采集方式 |',
            '| 数据集下载 | 获得特定范围的批量快照或定期更新 | 不等于实时 API；覆盖、时间和字段看购买项 |',
            '| SDK / 浏览器扩展 / Skill | 提供调用封装、操作界面或任务步骤 | 不是独立原始来源，不会自动扩展权限 |', '',
            '## 三家总结', '',
            '- AgentKey：统一网关 API 与 MCP；需要 master key。仅官网列名的来源仍需发现具体工具。',
            '- AIsa：有具体 HTTP API，模型和数据路径分开。MCP 是独立目录，不能把所有 API 家族默认标为 MCP 已接入；业务动作可能另需 OAuth。',
            '- TikHub：HTTP API / Python SDK；MCP 目录有具名平台与 others 分组；部分来源另有数据集和浏览器扩展。TikTok Creator 明确要求账户 Cookie。',
            '- RSS：未确认这三家为清单中来源提供 RSS/Atom 订阅。另核实 YouTube 官方 Atom/Webhook 路径，仅适合频道更新；不能当作评论或字幕接口。',
            '- 原始平台是否提供官方开放 API、聚合商是否实际使用它，均需独立证据；未披露的地方标为不确定。', '',
            '## 逐来源、逐接入商登记', '',
            '下列 API/MCP 描述有的仅确认了平台统一入口，具体来源级工具仍待核，详见“确认程度”。完整结构化字段保存在 [source-inventory.json](source-inventory.json)。', '',
            '| 来源 | 接入商 | 我们获取的方式 | 确认程度 | 授权与条件 |', '| --- | --- | --- | --- | --- |']
    for row in inventory:
        for provider,c in row['coverage'].items():
            a=c['access']; ways=' / '.join(m['kind'] for m in a['methods']) or '未确认入口（规划）'
            certainty='；'.join(dict.fromkeys(m['certainty'] for m in a['methods'])) or '即将上线'
            refs=' '.join(f'[{sid}]({url})' for sid,url in dict((sid,url) for m in a['methods'] for sid,url in zip(m['evidence'],m['evidence_urls'])).items())
            text.append(f'| {row["name"]} | {provider} | {ways} | {certainty} {refs} | {a["authorization"]} |')
    text += ['', '## 单独核实的原站直连路径', '']
    for row in inventory:
        if not row['direct_access']: continue
        text += [f'### {row["name"]}', '', row['direct_access_note'], '']
        for m in row['direct_access']:
            text.append(f'- **{m["kind"]}**：{m["detail"]} '+ ' '.join(f'[{sid}]({url})' for sid,url in zip(m['evidence'],m['evidence_urls'])))
        text.append('')
    text += ['## 明确尚不确定的部分', '',
             '1. 三家每个来源背后的实际采集方式、具体上游数据商及原站授权链路。',
             '2. 仅官网列示或规划中的来源，能否发现并成功调用对应工具。',
             '3. 除本页列出两种原站直连示例外，其余来源的官方 API / RSS / 下载路径未逐项核查。',
             '4. 每个接口的授权范围、限流、历史覆盖、分页完整性、具体费用。',
             '5. Telegram 对应 TikHub MCP 的映射；AIsa 每个 API 对应的 MCP 状态。', '',
             '不确定不等于没有能力，也不等于可以默认使用。以上缺口不影响本轮公开资料整理，但实际接入前需要针对选定来源补查。']
    (root/'notes/access-methods.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
