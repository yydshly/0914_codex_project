"""Record CLI provenance and generate the source index from pinned local evidence."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / 'notes/inventory.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for repo in manifest['repositories']:
    name, commit = repo['name'], repo['commit']
    if not name.startswith('create-'):
        continue
    paths = [f'packages/{name}/package.json', f'packages/{name}/bin/{name}.mjs', 'scripts/sync-template-to-cli.mjs']
    for p in paths:
        if any(x['repo'] == name and x['path'] == p for x in manifest['files']):
            continue
        data = subprocess.check_output(['git','-C',str(ROOT / '.cache' / name),'show',f'{commit}:{p}'])
        target = ROOT / 'upstream' / name / p
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        manifest['files'].append({'repo':name,'path':p,'local':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'url':f"{repo['url']}/blob/{commit}/{p}"})
    repo['selected_file_count'] = sum(x['repo'] == name for x in manifest['files'])
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines = ['# 来源、版本与许可记录','','研究日期：2026-09-16。以下为固定版本源码观察，不是法律意见或授权结论。','','## 固定版本','','| 仓库 | Commit | 选取文件数 |','| --- | --- | --- |']
for r in manifest['repositories']:
    lines.append(f"| [{r['name']}]({r['url']}) | [{r['commit']}]({r['url']}/tree/{r['commit']}) | {r['selected_file_count']} |")
lines += ['', '## 许可与署名', '',
          '- create-vibe-motion 和 create-vibe-motion-3d 的 CLI package.json 均声明 MIT；所检查的固定版本文件树没有独立 LICENSE。保留包元信息与来源，未补写许可证文本。',
          '- auto-motion 和 skills 的所查树未发现统一 LICENSE 文件，因此不将其概括为全部 MIT。',
          '- printed-curtain-render 原引擎注明 Jason Labbe / Dynamic ropes 2、CC BY-SA 4.0，保留 [NOTICE](../upstream/skills/printed-curtain-render/assets/printed-curtain-template/NOTICE.txt)。',
          '- 3d-chladni-render 的预览素材注明 Lykno、CC BY-NC 4.0；本研究未下载或重新发布该预览GIF。',
          '- 本地三维示例由原始脚手架生成，场景作者归上游项目；封面与MP4是本机运行其模板得到的结果。第三方依赖许可保存在安装包中。',
          '- 当前仅完成本地研究，没有推送或部署。本研究记录不改变上游或素材许可。', '', '## 快照说明', '',
          'upstream 是精简研究快照，不是完整安装包；未收集的脚本、图片、样式和依赖仍需从固定版本上游获取。可运行的三维工程在 src/demo-3d。', '',
          'inventory.json 保存每个文件的固定commit链接与SHA-256。src/collect_sources.py 默认复用清单中的commit；新机器可从GitHub获取固定版本，Windows需curl.exe与联网。', '',
          '两个脚手架最初由浅克隆获取；auto-motion的大型克隆传输未完成，已终止并改用GitHub API与原始文件获取研究所需文本，避免下载无关媒体。', '', '## 文件证据索引', '', '| 文件 | 固定上游源码 |', '| --- | --- |']
for f in manifest['files']:
    lines.append(f"| [{f['repo']}/{f['path']}](../{f['local']}) | [源码]({f['url']}) |")
(ROOT / 'notes/sources.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f"Recorded {len(manifest['files'])} source files")
