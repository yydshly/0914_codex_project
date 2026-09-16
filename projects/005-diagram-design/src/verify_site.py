"""Check the gallery's local references, inventory coverage and deliverables."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib
import json
import re
from collections import Counter
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'web/dist'

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)

def main():
    data=json.loads((OUT/'catalog.json').read_text(encoding='utf-8'))
    assert len(data['specimens'])==57 and sum(len(x['variants']) for x in data['specimens'])==155
    assert Counter(x['kind'] for x in data['specimens'])=={'基础图型':40,'派生示例':11,'动画演示':3,'导入重绘':3}
    bases={x['id'] for x in data['specimens'] if x['kind']=='基础图型'}
    skill=(ROOT/'upstream/skills/diagram-design/SKILL.md').read_text(encoding='utf-8')
    guide=skill.split('### Visual-type guide')[1].split('Rules of thumb:')[0]
    declared=set(re.findall(r'references/type-([a-z-]+)\.md',guide))
    assert bases==declared,(bases-declared,declared-bases)
    assert len(data['taxonomy'])==7 and sum(g['baseCount'] for g in data['taxonomy'])==40 and sum(g['exampleCount'] for g in data['taxonomy'])==57
    assert all(x['family'] in bases for x in data['specimens'])
    links=Links()
    for name in ('index.html','drawings.html'):
        links.feed((OUT/name).read_text(encoding='utf-8'))
    for link in links.links:
        p=urlsplit(link)
        if p.scheme or p.netloc or not p.path:continue
        assert (OUT/unquote(p.path)).is_file(),link
    drawings=(OUT/'drawings.html').read_text(encoding='utf-8')
    assert len(re.findall(r'href="vendor/example-[^"]+\.html"',drawings))==155
    assert len(re.findall(r'href="cases/research-[^"]+\.(?:html|svg|png)"',drawings))==24
    for name,size in [('diagram-design-overview',(3000,5055)),('diagram-design-overview-v2',(3600,6165))]:
        assert Image.open(OUT/'assets'/f'{name}.png').size==size
        ET.fromstring((OUT/'assets'/f'{name}.svg').read_text(encoding='utf-8'))
    for item in data['specimens']:
        for v in item['variants']:
            path=OUT/v['path'];assert path.is_file(),path
            assert hashlib.sha256(path.read_bytes()).hexdigest()==v['sha256'],path
    for file in (ROOT/'cases').glob('*.html'):
        for ext in ('html','svg','png'):
            assert (OUT/'cases'/file.with_suffix('.'+ext).name).is_file()
        node=ET.fromstring(file.with_suffix('.svg').read_text(encoding='utf-8'));w,h=map(int,node.attrib['viewBox'].split()[2:])
        assert Image.open(file.with_suffix('.png')).size==(w*2,h*2)
    for name in ('app.js','catalog.js'):
        checked=subprocess.run(['node','--check',str(OUT/name)],capture_output=True,text=True)
        assert checked.returncode==0,checked.stderr
    result={'groups':57,'basic_types':40,'derived_examples':11,'animated_examples':3,'import_examples':3,'taxonomy_categories':7,'upstream_type_table_match':'passed','original_html_files':155,'chinese_cases':8,'local_references':'passed','original_hashes':'passed','case_svg_xml':'passed','png_dimensions':'passed','javascript_syntax':'passed','authored_overviews':2,'inventory_links':'155 upstream + 24 authored case files','browser_interactions':'recorded separately in browser-check.json'}
    (ROOT/'evidence/site-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
