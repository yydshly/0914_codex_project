"""Build a reviewed source register from public-document evidence (no API calls)."""
import json
from pathlib import Path
from urllib.parse import urljoin
from access_methods import annotate_access, write_access_notes

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-16'
records = {}
EVIDENCE = {r['id']: r for r in json.loads((ROOT / 'notes/source-manifest.json').read_text(encoding='utf-8'))}


def add(name, category, kind, provides, platform, status, refs, note='', cleanup=''):
    row = records.setdefault(name, dict(name=name, category=category, kind=kind, provides=provides, coverage={}, cleanup=cleanup))
    row['coverage'][platform] = dict(status=status, evidence=refs, note=note, provides=provides)
    if cleanup:
        row['cleanup'] = cleanup


def ak(name, category, kind, provides, refs=('AK01',), status='官网列示', note='', cleanup=''):
    add(name, category, kind, provides, 'AgentKey', status, list(refs), note, cleanup)


for name, purpose in [
    ('Brave Search', '网页、新闻、图片及搜索上下文'), ('Tavily', '网页搜索与相关内容'),
    ('Serper', 'Google 搜索结果访问'), ('Perplexity', '带引用的联网回答'),
    ('Parallel', '网页搜索'), ('Exa', '语义搜索与网页内容')]:
    ak(name, '搜索与网页获取', '搜索/回答服务', purpose, ('AK03',), '文档列示', cleanup='保留原始链接；搜索摘要与已读取正文分开；生成回答不当作原始证据')
for name, purpose in [('Firecrawl','网页正文转 Markdown'),('Jina Reader','URL 转 Markdown'),('Bright Data','网页访问，AgentKey 文档所述 unlock 返回 HTML')]:
    ak(name, '搜索与网页获取', '采集/提取服务', purpose, ('AK04',), '文档列示', cleanup='提取正文后仍需去重、补时间和来源；HTML 需另行解析')

social = [
    ('X / Twitter','帖子、账号、趋势'),('Reddit','社区帖子与评论'),('YouTube','视频、频道；文档提及转录文本'),
    ('LinkedIn','职业账号与公司信息'),('TikTok','短视频与创作者内容'),('抖音','短视频、趋势'),
    ('知乎','问答与文章'),('Bilibili','视频与创作者评论'),('Threads','帖子与讨论'),('皮皮虾','社区短视频'),
    ('微信','公众号文章'),('Lemon8','生活方式内容'),('微博','话题与帖子'),('Instagram','账号与媒体帖子'),
    ('小红书','笔记、产品评价'),('快手','短视频与创作者内容'),('Facebook','页面与公开帖子'),('Pinterest','Pins 与视觉内容'),
    ('Discord','社区频道，具体访问范围待核'),('Telegram','频道与群组，具体访问范围待核'),
    ('Snapchat','公开故事与账号'),('Twitch','直播与频道资料'),('Product Hunt','产品发布与讨论')]
doc_social = {'X / Twitter','Reddit','YouTube','LinkedIn','TikTok','Instagram','Threads','Lemon8'}
for name, purpose in social:
    ak(name, '社交与内容平台', '原始内容平台', purpose, ('AK01','AK05') if name in doc_social else ('AK01',),
       '文档列示' if name in doc_social else '官网列示',
       '平台名不等于上游接口商名；实际字段、授权和历史范围待核', '按平台+内容ID去重；保留评论父子关系；统一时间与指标口径')
for name, purpose in [('Tushare','中国市场数据'),('Yahoo Finance','行情与新闻'),('FRED','美国宏观时间序列'),
                      ('Finnhub','市场数据与披露'),('Alpha Vantage','股票、外汇与指标')]:
    ak(name, '金融与链上', '数据服务/数据库', purpose, cleanup='统一代码、交易所、币种、时区、频率及复权口径')
ak('Digital Asset Prices', '金融与链上', '能力分类（供应商未披露）', '数字资产参考价格', note='官网名称是能力标签，不能据此推断具体数据商')
for name, purpose in [('淘宝','商品、价格与评价'),('京东','商品与价格'),('Amazon','商品与榜单'),('1688','批发商品'),
                     ('抖音电商','店铺商品目录'),('TikTok Shop','商品与店铺'),('贝壳','房产挂牌')]:
    ak(name, '电商与房产', '原始平台', purpose, cleanup='统一商品/SKU、币种、规格和采集时间；价格快照不能直接合并')
ak('Crunchbase', '企业与营销', '企业数据库', '公司与融资信息', cleanup='统一企业实体；保留事件日期与数据来源')
ak('Chainbase', '金融与链上', '链上数据服务', '钱包余额等链上数据', ('AK06',), '文档示例', note='文档给出 Chainbase/GetAccountBalance 示例，非完整供应商目录')
for name in ['Polymarket', 'Kalshi']:
    ak(name, '金融与链上', '预测市场平台', '事件、市场价格与订单簿', ('AK06',), '文档列示', cleanup='核对结算规则与到期时间；名称相似不代表同一事件')
for name in ['ENS', 'Space ID']:
    ak(name, '金融与链上', '链上命名系统', '名称与地址解析', ('AK06',), '文档列示', note='目标系统已列示，具体接口供应商未披露')

# TikHub documentation navigation is deeper than the homepage's headline count.
th = dict(social)
th.update({'西瓜视频':'视频与账号接口','今日头条':'文章、内容与账号接口','TikTok Shop':'商品、店铺、商品评论'})
th_names = ['TikTok','抖音','小红书','西瓜视频','Lemon8','Bilibili','皮皮虾','微信','微博','YouTube',
            'Reddit','Instagram','Threads','X / Twitter','Telegram','LinkedIn','快手','今日头条','知乎','TikTok Shop']
for name in th_names:
    add(name, '电商与房产' if name == 'TikTok Shop' else '社交与内容平台', '原始平台', th[name], 'TikHub',
        '文档列示', ['TH03'], '部分 Creator/商业分析接口需账号 Cookie；不能统一视为公开匿名数据',
        '按内容ID去重；分页完整性检查；平台指标映射；保留原始返回和采集时间')

# Every linked API family in AIsa's public catalog; descriptions below are our short annotations.
aisa_rows = [
('Similarweb','企业与营销','网站分析服务','流量、受众、渠道和关键词'),
('Chat','模型与处理工具','模型网关','文本与多模态生成；不是原始数据来源'),
('Jina Embeddings & Rerank','模型与处理工具','向量/排序服务','文本向量化与检索结果重排序'),
('X / Twitter','社交与内容平台','原始内容平台','帖子、账号与搜索；另有需 OAuth 的写操作'),
('Reddit','社交与内容平台','原始内容平台','社区、帖子、评论'),
('Instagram','社交与内容平台','原始内容平台','账号、帖子、评论和 Reels'),
('Pinterest','社交与内容平台','原始内容平台','Pins、账号与画板'),
('Tavily','搜索与网页获取','搜索/提取服务','搜索、提取、抓取与站点 URL 发现'),
('Firecrawl','搜索与网页获取','采集/提取服务','网页正文、HTML 解析、批量与异步抓取'),
('Exa','搜索与网页获取','搜索/回答服务','语义搜索、正文与带来源回答'),
('Oxylabs','搜索与网页获取','搜索结果采集服务','本目录所列接口查询 AI 搜索回答及引用；非其完整产品能力'),
('BytePlus SearchInfinity','搜索与网页获取','搜索/提取服务','实时网页搜索与正文提取'),
('Anthropic Web Search','搜索与网页获取','联网回答服务','搜索后的回答及引用'),
('OpenAI Web Search','搜索与网页获取','联网回答服务','搜索后的回答及引用'),
('Ahrefs','企业与营销','SEO 数据服务','域名、流量与关键词指标'),
('Semrush','企业与营销','SEO 数据服务','关键词、反向链接与竞品指标'),
('Financial','金融与链上','接口分类（供应商未披露）','行情、财报、新闻及 SEC 披露'),
('EDINET','金融与链上','披露系统','日本财务披露检索与文档'),
('YouTube','社交与内容平台','原始内容平台','视频、频道、播放列表搜索'),
('Scholar','学术研究','接口分类（供应商未披露）','论文及研究资料检索，作者、年份、引用等'),
('Kalshi','金融与链上','预测市场平台','预测事件、价格与交易数据'),
('Perplexity','搜索与网页获取','联网回答服务','联网回答、研究与引用'),
('Polymarket','金融与链上','预测市场平台','事件、订单簿、交易与钱包相关数据'),
('Matching Markets','模型与处理工具','跨源匹配服务','匹配 Polymarket 与 Kalshi 体育市场'),
('CoinGecko','金融与链上','数据服务','数字资产价格、历史与市场数据'),
('DataForSEO','企业与营销','搜索/营销数据服务','SERP、关键词、反向链接等多类接口'),
('Apollo','企业与营销','商业数据与操作服务','公司、人员、联系人与 CRM 对象'),
('AgentMail','业务操作工具','邮件服务','邮箱、邮件、草稿、收发操作；不是公共资料库'),
('WaveInflu','企业与营销','创作者数据服务','创作者联系方式与相似达人发现'),
('Open-Meteo','天气与地理','数据服务','天气、历史、气候、空气质量及地理编码'),
('CNPJá','企业与营销','企业登记查询服务','巴西企业登记资料'),
]
aliases = {'Twitter':'X / Twitter','Youtube':'YouTube','Tavily Search':'Tavily','EDINET API':'EDINET','Agent Mail':'AgentMail'}
ai_text = (ROOT / '.cache/AI02.txt').read_text(encoding='utf-8').splitlines()
links = json.loads((ROOT / '.cache/AI02.links.json').read_text(encoding='utf-8'))
endpoint_links = [x for x in links if x['href'].startswith('/api/') and 'endpoint' in x['text']]
assert len(endpoint_links) == len(aisa_rows), (len(endpoint_links),len(aisa_rows))
for (name, category, kind, purpose), link in zip(aisa_rows, endpoint_links):
    # Ordering follows the reviewed official catalog; retain each exact evidence target.
    checked_text = link['text'][2:] if link['href']=='/api/edinet-api' and link['text'].startswith('MP') else link['text']
    assert any(checked_text.startswith(n) for n in [name]+[k for k,v in aliases.items() if v==name]), (name,link)
    refs = ['AI02'] + (['AI04'] if name == 'Firecrawl' else ['AI05'] if name == 'Jina Embeddings & Rerank' else [])
    note = '目录有接口入口；尚未调用验证'
    if name == 'Semrush':
        note = '同一目录既有19个接口入口，又在下方标 Coming Soon；以具体接口为候选，保留冲突待核'
    add(name, category, kind, purpose, 'AIsa', '状态冲突' if name=='Semrush' else '接口目录列示', refs, note)
    records[name]['coverage']['AIsa']['detail_url'] = urljoin('https://aisa.one', link['href'])

add('TikTok Shop','电商与房产','原始平台','商品与店铺','AIsa','官网提及',['AI01'],
    '官网声称有此数据；当前 API 总目录未找到对应独立入口，列待核，不推定全量 TikTok 数据支持')

planned = []
for line in ai_text:
    if line.endswith('Coming Soon'):
        name = line[:-len('Coming Soon')].strip()
        planned.append(name)
        normalized = {'Google Maps':'Google Maps', 'Bright Data':'Bright Data'}.get(name, name)
        if normalized == 'Semrush':
            continue
        add(normalized,'规划来源','规划服务','详见官方规划目录；未确认已上线','AIsa','即将上线',['AI02'],
            '不得计入当前已接入能力')

inventory = list(records.values())
for i, row in enumerate(inventory, 1):
    row['id'] = f'R{i:03}'
    row['checked_on'] = DATE
    row['tested'] = False
    if not row['cleanup']:
        row['cleanup'] = '按实际返回字段制定清理规则；保存来源、时间、原始记录和转换版本'
    for coverage in row['coverage'].values():
        coverage['evidence_urls'] = [EVIDENCE[sid]['url'] for sid in coverage['evidence']]

annotate_access(inventory, EVIDENCE)
write_access_notes(ROOT, inventory)
(ROOT / 'notes/source-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def evidence_cell(cov):
    if not cov:
        return '—'
    refs = ', '.join(f'[{sid}]({EVIDENCE[sid]["url"]})' for sid in cov['evidence'])
    detail = f' · [接口入口]({cov["detail_url"]})' if cov.get('detail_url') else ''
    return f'{cov["status"]} {refs}{detail}'


lines = ['# 来源与服务总表', '', f'核查日期：{DATE}。这是公开资料中具名来源与能力的登记，不是实测可用清单。', '',
         '**获取方式：**查看 [API / MCP / RSS / 数据集与不确定项](access-methods.md)，逐来源、逐接入商记录调用方式、确认程度和授权条件。', '',
         '**阅读口径：**“原始平台”说明数据内容来自哪里；“数据/搜索/采集服务”说明通过谁获取；“模型/处理/操作工具”不是数据来源。名称已合并，如 Rednote / Red Book / Xiaohongshu → 小红书。', '',
         '- 文档列示 / 文档示例：官方文档明确提及，未做付费调用。',
         '- 接口目录列示：有具体接口入口，未验证权限、成功率或字段完整度。',
         '- 官网列示 / 官网提及：营销页可见，完整接口范围尚待核实。',
         '- 即将上线：仅规划；状态冲突：同站不同位置的说明不一致。',
         '- “—”只表示本次证据未确认，不表示绝对不支持。', '',
         '**边界：**Financial、Scholar、Digital Asset Prices 是接口/能力名称，不能擅自补成某家具体供应商；同一原始平台出现多家接入，不意味着数据相互独立。', '']
categories = list(dict.fromkeys(r['category'] for r in inventory if r['category']!='规划来源'))
for category in categories:
    lines += [f'## {category}', '', '| 来源/服务 | 类型与可获取内容 | AgentKey | AIsa | TikHub |', '| --- | --- | --- | --- | --- |']
    for row in inventory:
        if row['category'] != category:
            continue
        lines.append('| '+ ' | '.join([row['name'],row['kind']+'；'+row['provides']]+[evidence_cell(row['coverage'].get(p)) for p in ['AgentKey','AIsa','TikHub']])+' |')
    lines += ['']
lines += ['## AIsa 尚未上线与矛盾项', '',
          f'目录共出现 {len(planned)} 个 Coming Soon 名称，其中 Semrush 同时存在接口入口，单独标为冲突。以下保留完整名单，不计入已列接口数量。[官方目录](https://aisa.one/api)', '',
          '、'.join(planned)+'。', '', '## 逐条核查备注与后续清理', '',
          '机器可读版：[source-inventory.json](source-inventory.json)。以下备注区分官网提及、权限条件和数据处理责任。', '']
for row in inventory:
    if row['category']=='规划来源':
        continue
    notes = '；'.join(f'{p}：{c["note"]}' for p,c in row['coverage'].items() if c['note'])
    lines += [f'- **{row["id"]} {row["name"]}**：{notes}。清理建议：{row["cleanup"]}。']
(ROOT/'notes/sources-inventory.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

refs = ['# 官方证据与复核方法', '', f'查阅日期：{DATE}。所有能力描述均为公开文档证据，不代表真实请求成功。', '',
        '| 编号 | 官方页面 | 本次使用范围 |', '| --- | --- | --- |']
for sid, item in EVIDENCE.items():
    retrieval = '网页阅读工具已核查；本地快照超时，未生成原件摘要' if item.get('web_reviewed') and item['status']=='error' else f'本地快照状态 {item["status"]}'
    refs.append(f'| {sid} | [{item["title"]}]({item["url"]}) | 产品定位、目录或获取方式；{retrieval} |')
refs += ['', '## 复核方式', '',
         '读取公开网页的脚本位于 `src/fetch_sources.py`，只请求上述文档地址。页面原件和解析文本保存在被忽略的 `.cache/`；校验摘要、最终地址、时间和状态保存在 [source-manifest.json](source-manifest.json)。', '',
         '来源登记由 `src/build_inventory.py` 生成。它核对 AIsa 接口卡片名称与顺序，并分别保留 Coming Soon；官网变更时需人工重审，不能将自动抓取结果直接视为有效能力。', '',
         '本次没有注册账号、保存密钥、购买套餐、调用付费数据、安装插件或运行任何上游安装指令。', '',
         '## 已发现的不一致', '',
         '1. AIsa 的 Semrush 同时列出具体接口和 Coming Soon，来源表保留冲突。',
         '2. AIsa 官网的 API、模型、Skills 总数与技术页面的接口/供应商统计口径不同，不作为独立数据源数量使用。',
         '3. TikHub 首页宣称 16 个平台；公开 API 展示页、文档导航的分组不一致。本表逐名登记，不强行凑齐宣传数字；TikTok Shop 作为电商子产品单列。',
         '4. AgentKey 官网社交目录比社交说明页更长，新增名称保留“官网列示”等级，未推定每项接口已可用。',
         '5. AgentKey 首页与文档对超额计费表述不完全一致；本研究不据此给出价格承诺。',
         '6. TikHub 首页以公开数据为主，但 Creator 等接口要求账号 Cookie，不能把所有端点视为无账号可访问。', '',
         '## 范围与完整性', '',
         '覆盖 AgentKey 首页及七个能力分类、AIsa API 总目录全部具名卡片与规划名单、TikHub 文档导航中具名内容平台；不声称枚举登录后动态目录、每个端点、底层未披露供应商或所有模型版本。',
         '搜索服务可检索大量网站，不能据此将整个互联网登记为已接入的独立来源。品牌 logo、页脚社交链接、客户与投资方不算数据源。', '',
         '项目是商业服务研究，不是三家开源代码库的复现；未复制上游源码，未对服务许可作推断。']
(ROOT/'notes/sources.md').write_text('\n'.join(refs)+'\n',encoding='utf-8')
stats = {'registered_entries':len(inventory), 'aisa_linked_api_families':len(aisa_rows), 'aisa_coming_soon_labels':len(planned),
         'per_platform_entries':{p:sum(p in r['coverage'] for r in inventory) for p in ['AgentKey','AIsa','TikHub']},
         'tested_endpoints':0}
(ROOT/'notes/inventory-stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print(json.dumps(stats, ensure_ascii=False))
