"""Build the local study gallery from preserved upstream assets and authored content."""
from pathlib import Path
import hashlib
import json
import re
import shutil
from catalog_data import rows, TYPE_GROUPS
from deliverables import inventory_markdown, inventory_html

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'upstream/skills/diagram-design'
OUT = ROOT / 'web/dist'
COMMIT = 'ce9344c52cb9be811de187bf2a6d58c712c9c9fe'

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL/'assets', OUT/'vendor', dirs_exist_ok=True)
    for filename in ('LICENSE','THIRD_PARTY_LICENSES.md'):
        shutil.copy2(ROOT/'upstream'/filename, OUT/'vendor'/filename)
    for file in (ROOT/'web').glob('*'):
        if file.is_file():
            shutil.copy2(file, OUT/file.name)
    (ROOT/'notes/drawings.md').write_text(inventory_markdown(),encoding='utf-8')
    for sub in ('cases','evidence','inputs','assets','notes'):
        if (ROOT/sub).exists():
            shutil.copytree(ROOT/sub, OUT/sub, dirs_exist_ok=True)
    (OUT/'drawings.html').write_text(inventory_html(),encoding='utf-8')
    # Published notes retain working source links without duplicating the source tree.
    source_url='https://github.com/yydshly/0914_codex_project/blob/main/projects/005-diagram-design/upstream/'
    for note in (OUT/'notes').glob('*.md'):
        content=note.read_text(encoding='utf-8')
        content=content.replace('../upstream/skills/diagram-design/assets/','../vendor/')
        content=content.replace('../upstream/',source_url)
        note.write_text(content,encoding='utf-8')
    specimens = []
    for item in rows():
        variants = []
        for suffix, label in [('', '浅色'),('-dark','深色'),('-full','完整页面')]:
            name = f'example-{item["id"]}{suffix}.html'
            if (SKILL/'assets'/name).exists():
                raw = (SKILL/'assets'/name).read_bytes()
                variants.append(dict(id=suffix or 'light', label=label, path='vendor/'+name,
                                     sha256=hashlib.sha256(raw).hexdigest()))
        assert variants, item
        item['variants'] = variants
        item['source'] = f'https://github.com/cathrynlavery/diagram-design/blob/{COMMIT}/skills/diagram-design/assets/example-{item["id"]}.html'
        specimens.append(item)
    actual = set(p.name for p in (SKILL/'assets').glob('example-*.html'))
    indexed = {Path(v['path']).name for item in specimens for v in item['variants']}
    assert actual == indexed, (actual-indexed, indexed-actual)
    taxonomy=[dict(name=name,question=question,baseIds=keys.split(),baseCount=len(keys.split()),exampleCount=sum(s['category']==name for s in specimens)) for name,question,keys in TYPE_GROUPS]
    data = dict(version='2.6.23', commit=COMMIT, groups=len(specimens), htmlFiles=len(actual), taxonomy=taxonomy, specimens=specimens)
    write_json(OUT/'catalog.json',data)
    write_json(ROOT/'notes/inventory.json',data)
    # Embedded data allows the gallery to work when index.html is opened as a local file.
    (OUT/'catalog.js').write_text('window.DIAGRAM_CATALOG='+json.dumps(data, ensure_ascii=False)+';\n',encoding='utf-8')
    report=ROOT/'evidence/verification.json'
    if report.exists():
        checks=json.loads(report.read_text(encoding='utf-8'))
        summary=f"{checks['upstream_self_check_pass']} / {checks['upstream_count']} 个上游示例通过结构检查，{checks['upstream_geometry_pass']} / {checks['upstream_count']} 通过标签遮挡检查；{len(checks['cases'])} 个中文案例通过同样检查并导出 PNG。三种简单源文件的节点与关系已核对一致。"
        page=(OUT/'index.html').read_text(encoding='utf-8')
        page=re.sub(r'(<p id="verification-summary">).*?(</p>)',lambda m:m.group(1)+summary+m.group(2),page,flags=re.S)
        (OUT/'index.html').write_text(page,encoding='utf-8')
    print(f'Built {len(specimens)} groups / {len(actual)} original HTML specimens at {OUT}')

if __name__ == '__main__':
    main()
