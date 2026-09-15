"""Package explicitly selected static demos into one GitHub Pages artifact."""

import argparse
import html
import json
from pathlib import Path
import shutil

from catalog import ROOT, folder, load_projects


def build(output):
    projects = {p['id']: p for p in load_projects()}
    selected = json.loads((ROOT / 'pages.json').read_text(encoding='utf-8'))['projects']
    if not selected or len(selected) != len(set(selected)):
        raise ValueError('pages.json must select unique project IDs')
    output = output.resolve()
    if output.exists():
        raise ValueError(f'Use a new output directory to prevent stale published files: {output}')
    sources = []
    for pid in selected:
        project = projects[pid]
        source = ROOT / folder(project) / 'web' / 'dist'
        if not (source / 'index.html').is_file():
            raise ValueError(f'No static entrypoint for project {pid}')
        if any(p.is_symlink() for p in source.rglob('*')):
            raise ValueError(f'Symbolic links cannot be published: {pid}')
        sources.append((project, source))
    output.mkdir(parents=True)
    cards = []
    for project, source in sources:
        slug = Path(folder(project)).name
        shutil.copytree(source, output / slug)
        esc = html.escape
        cards.append(f'''<article><span class="number">{esc(project['id'])}</span>
<h2><a href="./{slug}/">{esc(project['name'])}</a></h2>
<p>{esc(project['summary'])}</p><div class="links"><a href="./{slug}/">打开网页演示 →</a>
<a href="{esc(project['repo'], quote=True)}">上游源库 ↗</a></div></article>''')
    page = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GitHub 项目研究集 · 网页演示</title>
<meta name="description" content="GitHub 项目的能力研究、原理说明与交互演示。">
<style>*{box-sizing:border-box}body{margin:0;font-family:system-ui,'Microsoft YaHei',sans-serif;background:#f4f6fa;color:#182d52}main{max-width:1040px;margin:auto;padding:64px 24px}header{margin-bottom:36px}h1{font-size:32px;line-height:1.4}p{font-size:16px;line-height:1.9;color:#5f6e84}article{background:white;border:1px solid #dce3ed;border-radius:12px;padding:28px;margin:20px 0}h2{font-size:22px;line-height:1.6}a{color:#335deb;text-underline-offset:4px}.number{font-size:14px;color:#687b95}.links{display:flex;gap:24px;flex-wrap:wrap}footer{font-size:14px;color:#687b95;margin-top:36px}a:focus-visible{outline:3px solid #335deb;outline-offset:5px}@media(max-width:600px){main{padding:32px 18px}article{padding:22px}}</style>
</head><body><main><header><h1>GitHub 项目研究集</h1><p>从能力说明到实际场景，打开网页探索每个项目。</p></header>'''
    page += '\n'.join(cards)
    page += '''<footer><a href="https://github.com/yydshly/0914_codex_project">查看研究仓库与完整索引 ↗</a></footer></main></body></html>'''
    (output / 'index.html').write_text(page, encoding='utf-8', newline='\n')
    (output / '.nojekyll').touch()
    print(f'Packaged {len(sources)} demo(s) into {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    build(args.output)
