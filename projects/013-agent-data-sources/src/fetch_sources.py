"""Cache public documentation only; never call paid data or account APIs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
import argparse
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'AK01': ('AgentKey 官网', 'https://agentkey.app/'),
    'AK02': ('AgentKey 文档总览', 'https://docs.agentkey.app/'),
    **{f'AK{i:02}': (f'AgentKey {name}', f'https://docs.agentkey.app/capabilities/{name}')
       for i, name in enumerate(['search', 'scrape', 'social', 'crypto', 'finance', 'business', 'ecommerce'], 3)},
    'AI01': ('AIsa 官网', 'https://aisa.one/'),
    'AI02': ('AIsa API 目录', 'https://aisa.one/api'),
    'AI03': ('AIsa 产品说明', 'https://aisa.one/llms.txt'),
    'AI04': ('AIsa Firecrawl', 'https://aisa.one/api/firecrawl'),
    'AI05': ('AIsa Jina Embeddings & Rerank', 'https://aisa.one/api/embeddings-rerank-api'),
    'AI06': ('AIsa 文档总览', 'https://aisa.one/docs/guides'),
    'TH01': ('TikHub 官网', 'https://tikhub.io/'),
    'TH02': ('TikHub API 目录', 'https://tikhub.io/api-reference'),
    'TH03': ('TikHub 文档索引', 'https://docs.tikhub.io/'),
    'TH04': ('TikHub 数据集', 'https://tikhub.io/datasets'),
    'AK10': ('AgentKey API 调用模型', 'https://docs.agentkey.app/api-reference/introduction'),
    'AK11': ('AgentKey 身份认证', 'https://docs.agentkey.app/authentication'),
    'AI07': ('AIsa 接口与接入方式', 'https://aisa.one/docs/by-interface'),
    'TH05': ('TikHub MCP 平台映射', 'https://tikhub.io/mcp'),
    'DR01': ('YouTube 官方 Atom 与推送通知', 'https://developers.google.com/youtube/v3/guides/push_notifications'),
    'DR02': ('FRED 官方 API', 'https://fred.stlouisfed.org/docs/api/fred/'),
}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
        self.links = []
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if self.skip:
            return
        if tag in ('h1', 'h2', 'h3', 'p', 'div', 'li', 'tr', 'br'):
            self.parts.append('\n')
        if tag == 'a':
            self.anchor = [dict(attrs).get('href', ''), []]

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        if not self.skip and tag == 'a' and self.anchor:
            self.links.append({'href': self.anchor[0], 'text': ''.join(self.anchor[1]).strip()})
            self.anchor = None

    def handle_data(self, value):
        if not self.skip:
            self.parts.append(value)
            if self.anchor:
                self.anchor[1].append(value)


def fetch(item):
    sid, (title, url) = item
    record = {'id': sid, 'title': title, 'url': url, 'checked_at': datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=35) as response:
            body = response.read()
            record.update(status=response.status, final_url=response.url, sha256=sha256(body).hexdigest(), bytes=len(body))
        raw = body.decode('utf-8', errors='replace')
        (ROOT / '.cache' / f'{sid}.raw').write_bytes(body)
        if '<html' in raw[:1000].lower() or '<!doctype' in raw[:1000].lower():
            reader = Reader()
            reader.feed(raw)
            content = '\n'.join(line.strip() for line in ''.join(reader.parts).splitlines() if line.strip())
            (ROOT / '.cache' / f'{sid}.links.json').write_text(json.dumps(reader.links, ensure_ascii=False, indent=2), encoding='utf-8')
        else:
            content = raw
        (ROOT / '.cache' / f'{sid}.txt').write_text(content, encoding='utf-8')
    except Exception as error:
        record.update(status='error', error=str(error))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', choices=list(SOURCES))
    args = parser.parse_args()
    (ROOT / '.cache').mkdir(exist_ok=True)
    selected = {sid: value for sid, value in SOURCES.items() if not args.ids or sid in args.ids}
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, selected.items()))
    manifest = ROOT / 'notes' / 'source-manifest.json'
    previous = {r['id']: r for r in json.loads(manifest.read_text(encoding='utf-8'))} if args.ids and manifest.exists() else {}
    previous.update({r['id']:r for r in records})
    manifest.write_text(json.dumps(list(previous.values()), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for record in records:
        print(record['id'], record['status'], record['title'])


if __name__ == '__main__':
    main()
