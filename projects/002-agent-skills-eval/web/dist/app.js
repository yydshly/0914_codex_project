import { renderPrinciple } from './principle.mjs';
import { presets, refund, labels, csvCompare, toolGrade } from './model.mjs';
const main = document.querySelector('main');
const source = 'https://github.com/darkrishabh/agent-skills-eval/blob/b60eebe3c6edaa917a284e13b9b0e9fa00f1c957/src/';
const state = { scene: 'refund', refund: { ...presets[0] }, equalData: false, tool: { tool: 'lookup', city: 'Shanghai', count: 1 } };
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const heading = (kicker, title, subtitle, badge='交互式研究') => `<div class="pagehead"><div><div class="eyebrow">${kicker}</div><h1>${title}</h1><p class="lead">${subtitle}</p></div><span class="badge blue">${badge}</span></div>`;
const checks = list => `<div class="check-list">${list.map(c=>`<details class="check-row"><summary><span class="${c.pass?'pass':'fail'}">${c.pass?'✓':'×'}</span>${esc(c.name)}</summary><p>${esc(c.evidence)}</p></details>`).join('')}</div>`;
const metrics = (a,b,caption='教学示例差值') => `<div class="score-strip"><div class="metric"><div class="metric-label">未加载 Skill</div><div class="metric-value">${a}<small>%</small></div></div><div class="metric"><div class="metric-label">加载 Skill</div><div class="metric-value">${b}<small>%</small></div></div><div class="metric"><div class="metric-label">${caption}</div><div class="metric-value">${b-a>0?'+':''}${b-a}<small>百分点</small></div></div></div>`;
function answerCard(name, answer, list, enhanced) { return `<article class="answer-card ${enhanced?'enhanced':''}"><header class="answer-head"><span>${name}</span><span>${list.filter(c=>c.pass).length} / ${list.length} 通过</span></header><div class="answer-body"><div class="answer-tag">预设示例回答 · 非模型实测</div><h3>${labels[answer.decision]}</h3><p><b>依据</b><br>${esc(answer.basis)}</p><p><b>下一步</b><br>${esc(answer.next)}</p></div>${checks(list)}</article>`; }

function demo() {
  main.innerHTML = heading('THE EVALUATION LAB', '一份 Skill，究竟改变了什么？', '测试题和标准已预先准备好。这里演示运行后的回答与评分；网页本身不调用模型。') +
    `<div class="scene-tabs" role="group" aria-label="选择演示场景">${[['refund','退款客服'],['csv','数据分析'],['tool','工具调用']].map(([id,name],i)=>`<button type="button" data-scene="${id}" class="${state.scene===id?'active':''}" aria-pressed="${state.scene===id}"><span>0${i+1}</span>${name}</button>`).join('')}</div><div id="scene"></div>`;
  if(state.scene==='refund') refundScene(); else if(state.scene==='csv') csvScene(); else toolScene();
}
function refundScene() {
  const s=state.refund;
  document.querySelector('#scene').innerHTML=`<div class="lab"><section class="panel"><div class="panel-pad"><div class="panel-title"><h2>订单与任务</h2><span>可调整</span></div><div class="field"><label for="preset">选择典型场景</label><select id="preset">${presets.map(p=>`<option value="${p.id}" ${s.id===p.id?'selected':''}>${p.name}</option>`).join('')}<option value="custom" ${s.id==='custom'?'selected':''}>自定义条件</option></select></div><div class="field"><div class="field-head"><label for="days">已收货天数</label><output id="day-output">${s.days===null?'未知':s.days+' 天'}</output></div><input id="days" type="range" min="0" max="40" step="1" value="${s.days??3}" ${s.days===null?'disabled':''}><div class="range-ends"><span>当天</span><span>40 天</span></div><label class="check-label"><input type="checkbox" id="unknown" ${s.days===null?'checked':''}>未提供收货时间</label></div><label class="check-label"><input id="opened" type="checkbox" ${s.opened?'checked':''}>商品已拆封</label><label class="check-label"><input id="quality" type="checkbox" ${s.quality?'checked':''}>申请原因为质量问题</label><label class="check-label"><input id="photo" type="checkbox" ${s.photo?'checked':''}>已提供损坏照片</label></div><div class="policy"><h3>本场景的虚构商家政策</h3><p><b>普通申请</b> · 7 天内（含第 7 天），商品未拆封。</p><p><b>质量问题</b> · 30 天内，有照片凭证，拆封不影响申请。</p><p>信息不足应补充；助理无退款执行权限。</p></div></section><section class="lab-right"><div class="notice"><span class="icon">ⓘ</span><div><b>教学模拟：预设回答 + 本地规则评分。</b>本页不调用 AI；基线回答刻意展示常见错误，不代表任何模型的实际表现。</div></div><div id="refund-result" aria-live="polite" aria-atomic="false"></div><details class="panel panel-pad skill-box"><summary>这份 Skill 增加了哪些工作步骤？</summary><ol><li>先识别申请原因，优先检查质量问题的专门条款。</li><li>逐项检查日期、商品状态与凭证，不补写缺失信息。</li><li>按“结论、依据、下一步”给建议，不声称已经执行退款。</li></ol></details></section></div>`;
  updateRefund();
}
function updateRefund() {
  const r=refund(state.refund);
  document.querySelector('#refund-result').innerHTML=metrics(r.baselineScore,r.skillScore)+`<div class="answers">${answerCard('未加载 Skill',r.baseline,r.baselineChecks,false)}${answerCard('加载 Skill',r.skill,r.skillChecks,true)}</div><p class="teaching-note">${r.baselineScore===r.skillScore?'两组在这个示例中表现相同：模型本来就会的任务，Skill 未必带来额外收益。':'本例展示工作步骤如何帮助避免遗漏。示例差值由预设回答决定，不能用它估计真实模型增益。'} 点击每条评分可查看依据。</p>`;
}

function csvScene() {
  document.querySelector('#scene').innerHTML=`<div class="lab"><section class="panel"><div class="panel-pad"><div class="panel-title"><h2>对照实验条件</h2><span>E01 / E02</span></div><div class="switch-buttons"><button data-equal="false" class="${!state.equalData?'active':''}" aria-pressed="${!state.equalData}">原库附件路径<br><small>只有加载 Skill 一组拿到数据</small></button><button data-equal="true" class="${state.equalData?'active':''}" aria-pressed="${state.equalData}">让两组获得相同数据<br><small>将 CSV 写入共同的任务提示词</small></button></div></div><div class="policy"><h3>任务</h3><p>找出收入最高的月份。</p><div class="code-block">month,revenue<br>January,12<br>February,18</div><p>Skill 正文与数据分析无关。模拟执行器完全不读取 Skill。</p></div></section><section class="lab-right"><div class="notice"><span>ⓘ</span><div><b>已复现实验的交互重放。</b>数据来自本地确定性实验 E01 / E02，不是模型实测。切换条件可看到数据不对称如何影响分差。</div></div><div id="csv-result" aria-live="polite"></div></section></div>`;
  const r=csvCompare(state.equalData);
  document.querySelector('#csv-result').innerHTML=metrics(r.baseline,r.skill,'机制实验差值')+`<div class="data-grid"><div class="panel panel-pad"><h3>未加载 Skill</h3><span class="badge ${state.equalData?'green':'yellow'}">${state.equalData?'得到任务 CSV':'没有任务 CSV'}</span><div class="code-block">${r.baselineOutput}</div><p class="teaching-note">${state.equalData?'有数据，因此给出最高月份。':'没有数据，无法完成题目。'}</p></div><div class="panel panel-pad"><h3>加载 Skill</h3><span class="badge green">得到任务 CSV</span><div class="code-block">${r.skillOutput}</div><p class="teaching-note">只读取数据，不使用 Skill 指令。</p></div></div><div class="panel wide-panel"><h2>${state.equalData?'输入公平后，虚假的增益消失了。':'这 100 个百分点，来自数据，不是 Skill。'}</h2><p class="lead">${state.equalData?'同一个执行器、同一份数据，两组均为 100%。前一个实验的差异全部来自附件可用性。':'如果实验组有 CSV，而基线组没有，分数差异无法全部归因于技能内容。一个不读取 Skill 的执行器也能得到“提升”。'}</p><div class="big-insight">评测原则：让两组使用相同的任务数据、工具和预算，只改变 Skill 上下文。</div><a class="source-small" href="${source}run-eval.ts#L181-L187" target="_blank" rel="noreferrer">查看上游附件加载代码 ↗</a></div>`;
}

function toolScene() {
  const t=state.tool;
  document.querySelector('#scene').innerHTML=`<div class="lab"><section class="panel"><div class="panel-pad"><div class="panel-title"><h2>模拟工具请求</h2><span>修改参数</span></div><div class="field"><label for="tool-name">工具名称</label><select id="tool-name">${['lookup','search','delete'].map(v=>`<option ${t.tool===v?'selected':''}>${v}</option>`).join('')}</select></div><div class="field"><label for="tool-city">city 参数</label><select id="tool-city">${['Shanghai','Beijing'].map(v=>`<option ${t.city===v?'selected':''}>${v}</option>`).join('')}</select></div><div class="field"><label for="tool-count">调用次数</label><select id="tool-count">${[0,1,2,3].map(v=>`<option value="${v}" ${t.count===v?'selected':''}>${v} 次</option>`).join('')}</select></div></div><div class="policy"><h3>业务任务</h3><p>查询上海的信息。应调用一次 lookup，city=Shanghai，禁止 delete。</p><p>此处只生成本地示例记录，不执行任何工具。</p></div></section><section class="lab-right"><div class="notice"><span>ⓘ</span><div><b>确定性规则演示。</b>本页用本地规则检查模拟请求，与原库的工具断言思路一致；无需 AI 裁判。</div></div><div id="tool-result" aria-live="polite"></div></section></div>`;
  updateTool();
}
function updateTool() {
  const list=toolGrade(state.tool), passed=list.filter(c=>c.pass).length;
  document.querySelector('#tool-result').innerHTML=`<div class="panel panel-pad tool-result"><div class="panel-title"><h2>工具请求检查</h2><span class="badge ${passed===4?'green':'yellow'}">${passed} / 4 通过</span></div><div class="code-block">${esc(JSON.stringify({name:state.tool.tool,arguments:{city:state.tool.city},callCount:state.tool.count},null,2))}</div>${checks(list)}</div><div class="big-insight"><b>请求正确 ≠ 任务已经完成。</b><br>原库默认只记录模型提出的工具调用。E10 实验中，工具规则通过，但没有执行工具，也没有任何工具结果回传。</div><a class="source-small" href="${source}grade.ts" target="_blank" rel="noreferrer">查看工具断言实现 ↗</a>`;
}

function principle() { main.innerHTML = renderPrinciple(source); }

async function evidence() {
  main.innerHTML=heading('EVIDENCE & LIMITS','流程跑通了，分数还要看依据。','将已复现的程序行为，与尚未测量的真实模型效果分开。','固定版本研究')+`<div class="evidence-summary"><div class="panel"><span class="metric-label">上游自带测试</span><strong>15 / 15</strong><p>覆盖加载、评分与模拟接口集成等行为。</p></div><div class="panel"><span class="metric-label">机制观测复现</span><strong>12 / 12</strong><p>包括成功路径和评测缺陷，不代表业务能力通过。</p></div><div class="panel"><span class="metric-label">真实模型效果</span><strong>尚未测量</strong><p>没有真实模型提升率或人工评分一致率。</p></div></div><div class="panel table-wrap" id="evidence-table"><p class="panel-pad">正在读取本地实验记录…</p></div><section class="panel wide-panel"><h2>优先修正什么？</h2><div class="split"><div><h3>让对照公平</h3><p>两组获得相同任务数据；不要将“是否看见附件”带来的差异当作 Skill 增益。</p><h3>让空测试显式失败</h3><p>没有用例、没有检查条件或目标调用出错，都应单独标记。</p></div><div><h3>让裁判有足够信息</h3><p>提供原任务与预期答案，核对每条条件和证据的对应关系。</p><h3>让业务完成有独立验证</h3><p>工具请求被提出，不代表工具执行成功；验收实际产物。</p></div></div><div class="link-row"><a class="button-link" href="./data/experiment-results.json" download>下载实验记录</a><a class="source-small" href="./data/mechanism-demo.html" target="_blank" rel="noreferrer">查看原库生成的报告 ↗</a><a class="source-small" href="./data/upstream-tests.txt" target="_blank" rel="noreferrer">查看上游测试日志 ↗</a></div></section>`;
  const descriptions={E01:'忽略 Skill 的模拟执行器：100% 对 0%，差异来自附件。',E02:'两组获得相同数据后：100% 对 100%，差值归零。',E03:'5 条规则中 4 条通过；裁判调用 0 次。',E04:'尝试 2 次后，将无法解析的评分判失败。',E05:'缺少 evidence，passed=true 仍被计为通过。',E06:'目标报错；0 条检查，报告通过率仍为 100%。',E07:'B 的判断与证据被按位置绑定到了 A。',E08:'有断言时，裁判未自动获得原任务与预期答案。',E09:'预期答案自动成为 1 条检查条件。',E10:'1 次请求，无工具结果消息，断言仍通过。',E11:'用例均值 50%；整体条件通过率 10%。',E12:'没有发现 Skill，退出码仍为 0。'};
  try {
    const response=await fetch('./data/experiment-results.json');if(!response.ok) throw Error();const data=await response.json();
    if(location.hash!=='#evidence') return;
    document.querySelector('#evidence-table').innerHTML=`<table><thead><tr><th>编号</th><th>已验证的行为</th><th>观测结果</th></tr></thead><tbody>${data.observations.map(o=>`<tr><td>${esc(o.id)}</td><td>${esc(o.title)}</td><td>${esc(descriptions[o.id]??'查看原始记录')}</td></tr>`).join('')}</tbody></table>`;
  } catch {const target=document.querySelector('#evidence-table');if(target)target.innerHTML='<p class="error-box">实验记录未能加载，请刷新页面重试。场景演示仍可使用。</p>';}
}

function render() {
  const page=['demo','principle','evidence'].includes(location.hash.slice(1))?location.hash.slice(1):'principle';
  document.querySelectorAll('[data-page]').forEach(a=>{if(a.dataset.page===page)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  if(page==='demo')demo();else if(page==='principle')principle();else evidence();
}
document.addEventListener('click', e=>{
  const scene=e.target.closest('[data-scene]');if(scene){state.scene=scene.dataset.scene;demo();document.querySelector(`[data-scene="${state.scene}"]`).focus();}
  const equal=e.target.closest('[data-equal]');if(equal){state.equalData=equal.dataset.equal==='true';csvScene();document.querySelector(`[data-equal="${state.equalData}"]`).focus();}
  const goto=e.target.closest('[data-goto-scene]');if(goto){state.scene=goto.dataset.gotoScene;if(goto.dataset.preset)state.refund={...presets.find(p=>p.id===goto.dataset.preset)};if(location.hash==='#demo')demo();else location.hash='demo';}
});
document.addEventListener('input',e=>{
  if(e.target.id==='days'){state.refund.days=Number(e.target.value);state.refund.id='custom';document.querySelector('#preset').value='custom';document.querySelector('#day-output').textContent=state.refund.days+' 天';updateRefund();}
});
document.addEventListener('change',e=>{
  const id=e.target.id;
  if(id==='preset'){if(e.target.value!=='custom'){state.refund={...presets.find(p=>p.id===e.target.value)};refundScene();document.querySelector('#preset').focus();}}
  if(['unknown','opened','quality','photo'].includes(id)){
    if(id==='unknown'){state.refund.days=e.target.checked?null:Number(document.querySelector('#days').value);document.querySelector('#days').disabled=e.target.checked;document.querySelector('#day-output').textContent=e.target.checked?'未知':state.refund.days+' 天';}
    else state.refund[id]=e.target.checked;
    state.refund.id='custom';document.querySelector('#preset').value='custom';updateRefund();
  }
  if(id.startsWith('tool-')){state.tool[{ 'tool-name':'tool','tool-city':'city','tool-count':'count'}[id]]=id==='tool-count'?Number(e.target.value):e.target.value;updateTool();}
});
window.addEventListener('hashchange',()=>{render();main.focus({preventScroll:true});window.scrollTo(0,0);});
render();
