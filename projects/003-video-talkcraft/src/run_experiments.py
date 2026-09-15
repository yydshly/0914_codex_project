"""Controlled tests of the original alignment and beat-checking code; no ASR inference."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.cache/pydeps'))
spec=importlib.util.spec_from_file_location('upstream_timestamps', ROOT/'upstream/scripts/timestamps_cpu.py')
aligner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aligner)
OUT=ROOT/'notes/experiments'
OUT.mkdir(parents=True,exist_ok=True)
results=[]

def words(text,offset=0):
    return [{'text':ch,'start':round(.5+i*.3+offset,3),'end':round(.7+i*.3+offset,3)} for i,ch in enumerate(text)]

def run(name,text,asr,check,conclusion):
    with contextlib.redirect_stdout(io.StringIO()):
        result=aligner.align([text],asr)
    check(result)
    (OUT/(name+'.json')).write_text(json.dumps({'script':text,'mock_asr_words':asr,'output':result},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    results.append({'id':name,'passed':True,'match':result['sentences'][0]['match'],'conclusion':conclusion})
    return result

def require(condition):
    assert condition

baseline='用户从一万增长到十万'
exact=run('exact',baseline,words(baseline),lambda r:require(r['sentences'][0]['match']==1),
          '完全匹配时，直接使用输入词表的时间。')
run('homophone','这个插件很好用',words('这个差件很好用'),lambda r:require(r['sentences'][0]['match']==1),
    '拼音相同的识别错字仍能成为锚点；match 不是转写正确率。')
mixed='今天发布TalkCraft工具很好用'
asr=[{'text':c,'start':round(.5+i*.3+(1.6 if i>=4 else 0),3),'end':round(.7+i*.3+(1.6 if i>=4 else 0),3)} for i,c in enumerate('今天发布工具很好用')]
mixed_result=run('latin-interpolation',mixed,asr,
    lambda r:require(r['sentences'][0]['match']==1 and any(w['text']=='TalkCraft' for w in r['sentences'][0]['words'])),
    '英文品牌词完全缺失时仍可插值补齐，中文锚点覆盖率仍为 100%。')
run('low-coverage','今天发布全新工具',words('今天再看明天新闻'),
    lambda r:require(not r['sentences'][0]['ok']), '锚点覆盖不足会标记听核。')
run('global-shift',baseline,words(baseline,2),lambda r:require(r['sentences'][0]['match']==1),
    '所有词时间整体错后 2 秒，match 仍是 100%；覆盖率不能证明声学时间准确。')
try:
    with contextlib.redirect_stdout(io.StringIO()): aligner.align(['甲乙丙'],words('xyz'))
except SystemExit:
    results.append({'id':'no-anchors','passed':True,'conclusion':'完全无匹配锚点时退出，不伪造整句对齐结果。'})
else:
    raise AssertionError('Expected no-anchor failure')

env={**os.environ,'PYTHONUTF8':'1'}
ts=OUT/'timestamps.json'
ts.write_text(json.dumps(mixed_result,ensure_ascii=False),encoding='utf-8')
subprocess.run([sys.executable,str(ROOT/'upstream/scripts/make_timing.py'),str(ts),str(OUT/'timing.json')],check=True,env=env,capture_output=True)
timing=json.loads((OUT/'timing.json').read_text(encoding='utf-8'))
assert ''.join(x['ch'] for x in timing['scenes'][0]['chars'])==mixed
results.append({'id':'timing-expansion','passed':True,'conclusion':'整段英文 token 被展开为逐字母时间，保持全文字符与时间表一一对应。'})

ts.write_text(json.dumps(exact,ensure_ascii=False),encoding='utf-8')
anchor=next(w['start'] for w in exact['sentences'][0]['words'] if w['text']=='十')
for name,offset,end,expected in [('beat-correct',0,5,0),('beat-off-by-300ms',.3,5,1),('beat-tail-too-short',0,anchor+.2,1)]:
    beat=[{'t':round(anchor+offset,3),'anchor':'十万','sentence':0,'what':'数字落定'}]
    bp=OUT/(name+'-beats.json'); sp=OUT/(name+'-shots.json')
    bp.write_text(json.dumps(beat,ensure_ascii=False),encoding='utf-8')
    sp.write_text(json.dumps([{'id':'s1','start':0,'end':end}]),encoding='utf-8')
    cp=subprocess.run([sys.executable,str(ROOT/'upstream/scripts/beat_lint.py'),str(bp),str(ts),'--shots',str(sp)],env=env,capture_output=True,text=True,encoding='utf-8')
    assert (cp.returncode==0)==(expected==0),cp.stdout+cp.stderr
    results.append({'id':name,'passed':True,'expected_exit':'pass' if expected==0 else 'reject','actual_exit':cp.returncode,'output':cp.stdout.strip()})

report={'date':'2026-09-15','method':'人为构造带时间的 ASR 词表，运行固定版本的上游原始脚本。未运行语音模型，不代表真实音频精度。',
        'dependencies':{'python':sys.version.split()[0],'pypinyin':'0.55.0','zhconv':'1.4.3'},'results':results}
(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'web/dist/experiments.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
