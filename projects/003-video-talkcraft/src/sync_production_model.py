"""Render the same research additions into Markdown and the static website."""
from pathlib import Path
from html import escape as e
import json

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'notes/production-model.json').read_text(encoding='utf-8'))
web=ROOT/'web/dist'
md=['# 从效果库到可靠制作：一致性与生产闭环','',data['scope'],'',
    '## 1. 三层一致性','',
    '全片约束先于分镜与选卡，镜内协调和跨镜衔接贯穿实现与复核。一致性不等于所有画面相同。','']
for c in data['consistency']:
    md += [f"### {c['name']}",'',c['question'],'',c['rule'],'',f"例子：{c['example']}",'',f"证据范围：{c['evidence']}。",'']
md += ['## 2. 八个需要展开的方面','']
for i,c in enumerate(data['criteria'],1):
    md += [f"### {i}. {c['name']}",'',c['question'],'',c['detail'],'',f"证据范围：{c['evidence']}。",'']
md += ['## 3. 三种正确不等价','']
for c in data['correctness']:md += [f"- **{c['name']}**：{c['detail']}{c['boundary']}"]
md += ['','例如：数字在正确时刻出现，但把“增长到十万”写成“增长了十万”，技术正确并不能推出表达正确。',
       '数字与含义都对，但停留短得读不清，也不能推出观看有效。','','## 4. 修改如何传播','',
       '| 修改 | 影响范围 | 返回路径 |','| --- | --- | --- |']
for c in data['changes']:md.append(f"| {c['change']} | {c['impact']} | {c['return']} |")
md += ['','这是结合现有缓存机制整理的复核指南，不是宣称仓库具备完整的自动依赖追踪系统。','','## 5. 失败回到对应步骤','']
for c in data['failures']:md += [f"- **{c['problem']}**：{c['return']}"]
md += ['','## 6. 四层完整模型','',
       '1. 目标与约束：受众、事实、风格、时长、素材与资源。',
       '2. 制作过程：预剪、对齐、分镜、选卡、组装、渲染。',
       '3. 过程产物：来源、时间表、分镜表、代码、缓存、检查记录。',
       '4. 反馈与返工：定位根因、更新受影响产物、局部与全片复核。',
       '', '这些层构成持续反馈关系，不能只在导出后才考虑一致性。', '', '## 来源与验证边界','']
for s in data['sources']:md.append(f"- [{s['label']}](../upstream/{s['path']})")
md += ['', '原有10项控制实验与单组件渲染没有新增为全片实验。本次补充是源码核对和研究模型整理。',
       '', '[返回研究入口](../README.md) · [查看汇总图](../assets/video-talkcraft-workflow.png)','']
(ROOT/'notes/production-model.md').write_text('\n'.join(md),encoding='utf-8')

h=['<!-- PRODUCTION_MODEL:START -->', '<section id="consistency" class="research-section">',
   '<div class="section-title"><h2>03 / 一致性：全片、局部与镜头之间</h2><span>先定全片规则，再受约束地分镜与选卡</span></div>',
   '<p class="lede">各镜头分别好看，不代表整片协调。一致性允许有目的的变化，但变化须服务同一表达目标。</p><div class="consistency-grid">']
for c in data['consistency']:
    h += [f'<article class="consistency-card"><h3>{e(c["name"])}</h3><p>{e(c["question"])}</p><p>{e(c["rule"])}</p><p class="case-example">{e(c["example"])}</p><small>{e(c["evidence"])}</small></article>']
h += ['</div><h3>技术正确、表达正确、观看有效，是三件事</h3><div class="correctness-grid">']
for c in data['correctness']:h += [f'<div><strong>{e(c["name"])}</strong><p>{e(c["detail"])}</p><small>{e(c["boundary"])}</small></div>']
h += ['</div><p class="notice">声画同步但把“增长到十万”写成“增长了十万”，仍是表达错误。事实正确但来不及读清，也不代表观看有效。</p></section>',
      '<section id="production" class="research-section"><div class="section-title"><h2>04 / 从做出来，到做对与可修改</h2><span>已有规范、自动机制与研究建议分别标明</span></div>',
      f'<p class="lede">{e(data["scope"])}</p><div class="production-grid">']
for i,c in enumerate(data['criteria'],1):
    h += [f'<article class="production-card"><span class="pill">{i:02d} · {e(c["kind"])}</span><h3>{e(c["name"])}</h3><p><strong>{e(c["question"])}</strong></p><p>{e(c["detail"])}</p><small>{e(c["evidence"])}</small></article>']
h += ['</div><h3>改了什么，哪些结果需要重做？</h3><p>下表是复核指南；现有邻镜缓存与音轨指纹不等于完整自动依赖追踪。</p><div class="table-scroll"><table><thead><tr><th>修改</th><th>影响范围</th><th>返回路径</th></tr></thead><tbody>']
for c in data['changes']:h += [f'<tr><td>{e(c["change"])}</td><td>{e(c["impact"])}</td><td>{e(c["return"])}</td></tr>']
h += ['</tbody></table></div><h3>失败时回到根因所在步骤</h3><div class="return-grid">']
for c in data['failures']:h += [f'<article><h4>{e(c["problem"])}</h4><p>{e(c["return"])}</p></article>']
h += ['</div><p class="notice"><strong>完整模型：</strong>目标与约束 → 制作过程 → 过程产物 → 反馈与返工。修改后更新受影响产物，再做局部、跨镜与全片复核。</p><div class="sources">']
for s in data['sources']:h += [f'<a data-source="{e(s["path"])}">{e(s["label"])}</a>']
h += ['</div></section><section id="overview" class="research-section"><div class="section-title"><h2>05 / 一图汇总</h2><span>输入、制作、一致性、回退与交付</span></div>',
      '<p class="lede">沿主流程阅读，再看贯穿约束和返工路径。点击图片可查看高清版本。</p>',
      '<figure class="workflow-figure"><a href="assets/video-talkcraft-workflow.png" target="_blank" rel="noopener"><img src="assets/video-talkcraft-workflow.png" loading="lazy" width="3300" height="6600" alt="Video TalkCraft 完整制作模型：输入与输出、七步制作、三层一致性、八项约束、技术与表达及观看三种正确，以及修改和失败的回退路径"></a><figcaption>包含已有机制与研究建议；完整多镜头口播制作尚未实测。</figcaption></figure>',
      '<div class="control-row"><a class="btn" href="assets/video-talkcraft-workflow.png" download>下载高清 PNG</a><a class="btn" href="assets/video-talkcraft-workflow.svg" target="_blank" rel="noopener">打开可缩放 SVG</a></div></section>',
      '<!-- PRODUCTION_MODEL:END -->']
page=web/'index.html'
content=page.read_text(encoding='utf-8')
start,end='<!-- PRODUCTION_MODEL:START -->','<!-- PRODUCTION_MODEL:END -->'
block='\n'.join(h)
if start in content:
    a,rest=content.split(start,1);_,b=rest.split(end,1);content=a+block+b
else:
    marker='  <section id="value" class="research-section">'
    assert marker in content
    content=content.replace(marker,block+'\n'+marker,1)
content=content.replace('03 / 价值：','06 / 价值：').replace('04 / 验证：','07 / 验证：').replace('05 / 108 套','08 / 108 套')
page.write_text(content,encoding='utf-8')
print('Updated production-model.md and website from production-model.json.')
