"""Run upstream text extractors and checkers; retain exact results for the study."""
from pathlib import Path
import concurrent.futures
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'upstream/skills/diagram-design'
EVIDENCE=ROOT/'evidence'

def dump(name,data):
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def run(script,*args):
    proc=subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
    return {'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def main():
    results=[]
    for kind,ext in [('mermaid','mmd'),('drawio','drawio'),('excalidraw','excalidraw')]:
        script=SKILL/'scripts'/f'{kind}_extract.py'
        result=run(script,ROOT/'inputs'/f'research.{ext}','--json')
        dump(f'{kind}-result.json',result)
        if result['exit_code']==0:
            obj=json.loads(result['stdout']);dump(f'{kind}-ir.json',obj)
            model=obj['diagrams'][0] if kind=='mermaid' else obj['pages'][0] if kind=='drawio' else obj['scene']
            expected=json.loads((ROOT/'inputs/research-content.json').read_text(encoding='utf-8'))
            assert {n['id']:n['label'] for n in model['nodes']}=={n['id']:n['name'] for n in expected['nodes']},model
            assert {(e['source'],e['target']) for e in model['edges']}=={(e['from'],e['to']) for e in expected['edges']},model
        digest=run(script,ROOT/'inputs'/f'research.{ext}')
        (EVIDENCE/f'{kind}-digest.md').write_text(digest['stdout'] or digest['stderr'],encoding='utf-8')
        results.append({'format':kind,'input':f'inputs/research.{ext}','result':f'{kind}-ir.json','exit_code':result['exit_code'],'nodes':6,'edges':5,'content_equivalence_checked':True,'digest':digest['stdout']})
    dump('import-summary.json',results)
    assert all(x['exit_code']==0 for x in results),results
    checker=load_module('diagram_self_check',SKILL/'scripts/self_check.py')
    geometry=load_module('diagram_geometry',ROOT/'upstream/scripts/verify-geometry.py')
    upstream=[]
    for file in sorted((SKILL/'assets').glob('example-*.html')):
        upstream.append({'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'self_check':checker.verify(file),'geometry':geometry.check(file)})
    cases=[]
    for file in sorted((ROOT/'cases').glob('*.html')):
        cases.append({'file':file.name,'self_check':checker.verify(file),'geometry':geometry.check(file)})
    class Registry(HTMLParser):
        def __init__(self):super().__init__();self.blocks=[]
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if 'data-block-id' in a:self.blocks.append({k.removeprefix('data-block-'):v for k,v in attrs if k.startswith('data-block-')})
    file=SKILL/'assets/example-tree-block-decomposition.html';r=Registry();r.feed(file.read_text(encoding='utf-8'))
    dump('block-registry.json',{'source':file.name,'blocks':r.blocks})
    block_check=run(ROOT/'upstream/scripts/verify-block-registry.py',file)
    report={'scope':'fixed upstream 2.6.23; original specimens plus eight AI-authored Chinese cases',
            'upstream_count':len(upstream),'upstream_self_check_pass':sum(not x['self_check'] for x in upstream),
            'upstream_geometry_pass':sum(not x['geometry'] for x in upstream),'upstream':upstream,
            'cases':cases,'imports':{'count':3,'passed':sum(x['exit_code']==0 for x in results)},'block_registry_check':block_check,
            'limits':['Source specimens preserved without edits even if an upstream check reports an issue.','Checks do not validate business facts.','Whole gallery browser interactions not tested.','PNG visual inspection is limited to authored diagram assets.']}
    dump('verification.json',report)
    assert all(not x['self_check'] and not x['geometry'] for x in cases),cases
    print(json.dumps({k:v for k,v in report.items() if k in ['upstream_count','upstream_self_check_pass','upstream_geometry_pass','imports']},ensure_ascii=False))

if __name__=='__main__':main()
