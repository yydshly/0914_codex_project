(() => {
  'use strict';
  const scenarios = window.MIRO_SCENARIOS;
  const state = { scenario: 'pricing', strategy: 'baseline', step: 0, actor: 1, round: 3, question: 0, view: 'timeline', event: 0 };
  const $ = id => document.getElementById(id);
  const esc = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const current = () => scenarios[state.scenario];
  const stageNames = ['关系图谱', '角色与环境', '多轮互动', '记录与报告', '角色访谈'];
  const positions = [[300,55],[475,112],[475,257],[300,317],[125,257],[125,112]];
  let playback = null;
  function stop() { if (playback) clearInterval(playback); playback = null; $('play').textContent = '播放流程'; }
  function graph() {
    const scenario = current();
    const active = state.step === 2 ? scenario.events[state.strategy].slice(0,state.round+1).map(e=>e.actor) : [state.actor];
    const grid = '<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#284651"/></pattern></defs><rect width="600" height="400" fill="url(#dots)"/>';
    const lines = positions.map(([x,y],i)=>`<line class="graph-edge ${active.includes(i)?'active-edge':''}" x1="300" y1="200" x2="${x}" y2="${y}"/>`).join('');
    const cross = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]].map(([a,b])=>`<line class="graph-edge" stroke-dasharray="4 7" x1="${positions[a][0]}" y1="${positions[a][1]}" x2="${positions[b][0]}" y2="${positions[b][1]}" opacity=".55"/>`).join('');
    const nodes = scenario.actors.map((actor,i)=>`<g class="node ${state.actor===i?'selected':''}" data-actor="${i}" tabindex="0" role="button" aria-label="查看${esc(actor.name)}的角色设定" aria-pressed="${state.actor===i}" transform="translate(${positions[i][0]},${positions[i][1]})"><circle r="30"/><text class="initial" y="7">${esc(actor.name.slice(0,1))}</text><text y="51">${esc(actor.name)}</text>${state.step>0?`<text class="node-label" y="69">${esc(actor.group)}</text>`:''}${active.includes(i)&&state.step===2?'<circle class="signal" cx="25" cy="-23" r="5"/>':''}</g>`).join('');
    $('world').innerHTML = grid+cross+lines+`<circle class="core" cx="300" cy="200" r="49"/><text class="core-text" x="300" y="205">${esc(scenario.core)}</text>`+nodes;
    $('world-label').textContent = stageNames[state.step];
    $('world').querySelectorAll('[data-actor]').forEach(node=>{
      const choose=()=>{stop();state.actor=Number(node.dataset.actor);renderProfile();graph();if(state.step===4)renderStage();$('world').querySelector(`[data-actor="${state.actor}"]`).focus({preventScroll:true});};
      node.addEventListener('click',choose);
      node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();choose();}});
    });
  }
  function renderProfile() {
    const actor=current().actors[state.actor];
    $('role-name').textContent=actor.name; $('role-avatar').textContent=actor.name.slice(0,1);
    $('role-group').textContent=actor.group; $('role-motive').textContent=actor.motive; $('role-evidence').textContent=actor.proof;
  }
  function header(title, description, badge='预设教学示例') { return `<div class="stage-header"><div><h3>${title}</h3><p>${description}</p></div><span class="stage-badge">${badge}</span></div>`; }
  function renderStage() {
    const scenario=current(), report=scenario.reports[state.strategy], actor=scenario.actors[state.actor];
    let html='';
    if(state.step===0) html=header('01 · 把文档里的“谁与谁”，组织成关系','先建立背景，才有角色行动的依据。')+`<div class="stage-grid"><div class="relation-list">${scenario.relations.map(r=>`<div>${esc(r)}</div>`).join('')}<div>本例包含 ${scenario.actors.length} 个虚构角色<span>不代表原版默认人数</span></div></div><div class="stage-callout"><h4>原版如何实现</h4><p>文档解析提取文本，通过 Zep 构建实体关系图谱。当前解析器支持 PDF、Markdown 与 TXT。</p><p>左侧是资料名称示意；本页没有上传、解析这些文件。</p></div></div>`;
    if(state.step===1) html=header('02 · 给角色背景，也给互动一个环境','人设、活跃程度与可用动作，共同影响模拟过程。')+`<div class="config-grid"><article><span>角色设定</span><b>${scenario.actors.length} 个教学角色</b><p>点击关系图，查看各自的动机与所需证据。</p></article><article><span>仿真动作</span><b>发布 / 反馈 / 传播</b><p>原版按平台提供发帖、评论、转发、关注等不同动作。</p></article><article><span>当前情景</span><b>${esc(scenario.strategies[state.strategy])}</b><p>${esc(scenario.strategyNotes[state.strategy])}</p></article></div><p class="small" style="margin-top:15px">原版的人设与仿真参数由模型结合资料生成；本页只展示机制，不运行 OASIS 环境。</p>`;
    if(state.step===2) {
      html=header('03 · 同一段互动，换一种方式看','对话看具体回应，信息流图看引用路径；点击记录查看身份、输入与行动。')+`<div class="view-switch" role="group" aria-label="互动展示方式">${[['timeline','事件时间轴'],['dialogue','角色对话'],['map','信息流图']].map(([key,label])=>`<button data-view="${key}" aria-pressed="${state.view===key}">${label}</button>`).join('')}</div><div class="round-control"><label for="round">教学轮次</label><input id="round" type="range" min="0" max="3" step="1" value="${state.round}" aria-valuetext="第 ${state.round+1} 轮，共 4 轮"><output id="round-output" for="round">${state.round+1} / 4</output></div><div class="timeline" id="timeline"></div><div id="interaction-view"></div><p class="small" style="margin-top:15px">本例是 4 条人工编写事件的回放。对话不是在线群聊，图中箭头是教学设定的引用关系，不是测得的因果影响。原版多角色可在同一轮行动；报告负责事后分析，通常不负责下达下一轮剧情。</p>`;
    }
    if(state.step===3) html=header('04 · 从记录提炼问题，而非直接宣布未来','报告应能回到材料、角色和动作记录中寻找依据。')+`<div class="report-grid"><article><h4>示例观察</h4><p>${esc(report.finding)}</p></article><article><h4>需要关注的风险</h4><p>${esc(report.risk)}</p></article><article><h4>回到现实怎样验证</h4><p>${esc(report.verify)}</p></article></div><button class="button secondary" id="download" style="margin-top:22px">下载本情景教学报告 ↓</button><p class="small" style="margin-top:12px">原版 ReportAgent 可调用检索与角色采访工具生成报告。本例报告为预先编写，未调用该工具链。</p>`;
    if(state.step===4) html=header('05 · 向一个角色追问“为什么”','切换人物和问题，理解虚拟访谈可以提供什么。')+`<div class="interview-layout"><div class="interview-controls"><label for="interview-actor">访谈对象</label><select id="interview-actor">${scenario.actors.map((a,i)=>`<option value="${i}" ${state.actor===i?'selected':''}>${esc(a.name)} · ${esc(a.group)}</option>`).join('')}</select><div class="question-buttons" role="group" aria-label="选择访谈问题">${['最关心什么？','什么会影响你？','需要什么证据？'].map((q,i)=>`<button data-question="${i}" aria-pressed="${state.question===i}">${q}</button>`).join('')}</div></div><div class="quote"><span>${esc(actor.name)} · 预设回答</span><p id="interview-answer">${esc([actor.motive,actor.influence,actor.proof][state.question])}</p><span>可用于启发真实访谈问题，不能替代真实用户反馈。</span></div></div>`;
    $('stage').innerHTML=html;
    if(state.step===2){renderTimeline();$('round').addEventListener('input',event=>{stop();state.round=Number(event.target.value);state.event=Math.min(state.event,state.round);$('round-output').textContent=`${state.round+1} / 4`;event.target.setAttribute('aria-valuetext',`第 ${state.round+1} 轮，共 4 轮`);renderTimeline();graph();});$('stage').querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{stop();state.view=button.dataset.view;renderStage();$('stage').querySelector(`[data-view="${state.view}"]`).focus({preventScroll:true});}));}
    if(state.step===3)$('download').addEventListener('click',downloadReport);
    if(state.step===4){
      $('interview-actor').addEventListener('change',event=>{stop();state.actor=Number(event.target.value);renderProfile();graph();renderStage();$('interview-actor').focus({preventScroll:true});});
      $('stage').querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>{stop();state.question=Number(button.dataset.question);renderStage();$('stage').querySelector(`[data-question="${state.question}"]`).focus({preventScroll:true});}));
    }
  }
  function renderTimeline(){
    const scenario=current();
    $('timeline').innerHTML=scenario.events[state.strategy].map((event,i)=>i<=state.round?`<article class="post ${i===state.round?'current':''}"><div class="post-meta"><span>第 ${i+1} 轮</span><span>${esc(event.action)}</span></div><b>${esc(scenario.actors[event.actor].name)}</b><p>${esc(event.text)}</p></article>`:`<article class="post hidden-round"><div class="post-meta">第 ${i+1} 轮</div><b>尚未展开</b><p>向右拖动轮次，查看后续预设回应。</p></article>`).join('');
    $('timeline').hidden=state.view!=='timeline';
    renderInteraction();
  }
  function renderInteraction(){
    const scenario=current(),events=scenario.events[state.strategy],meta=window.MIRO_INTERACTIONS[state.scenario][state.strategy];
    const visible=events.slice(0,state.round+1);
    const privateEvent=i=>state.scenario==='story'&&state.strategy==='baseline'&&(i===0||i===3);
    if(state.view==='timeline'){$('interaction-view').innerHTML='';return;}
    const record=(event,i)=>`<button class="dialogue-message ${privateEvent(i)?'private-message':''}" data-event="${i}" aria-pressed="${state.event===i}"><span class="message-meta">第 ${i+1} 轮 · ${esc(event.action)} · ${privateEvent(i)?'私人想法 · 仅观众可见':'公开互动'}</span><strong>${esc(scenario.actors[event.actor].name)}</strong><span class="message-text">${esc(event.text)}</span><span class="message-reference">${meta[i].from===null?'独立记录 / 初始信息':`回应或引用第 ${meta[i].from+1} 轮`}</span></button>`;
    let content='';
    if(state.view==='dialogue')content=`<div class="dialogue-feed" aria-label="预设角色对话">${visible.map(record).join('')}</div>`;
    if(state.view==='map'){
      const nodes=visible.map((event,i)=>{const y=32+i*115;return `<g class="flow-record ${state.event===i?'selected':''}" data-event="${i}" tabindex="0" role="button" aria-pressed="${state.event===i}" aria-label="第${i+1}轮，${esc(scenario.actors[event.actor].name)}，${esc(event.action)}"><rect x="145" y="${y}" width="400" height="80" rx="10"/><text x="164" y="${y+28}">0${i+1} · ${esc(scenario.actors[event.actor].name)} · ${esc(event.action)}</text><text class="flow-caption" x="164" y="${y+56}">${privateEvent(i)?'私人想法，不进入其他角色的信息流':esc(event.text.length>23?event.text.slice(0,23)+'…':event.text)}</text></g>`;}).join('');
      const edges=meta.slice(0,visible.length).map((m,i)=>{if(m.from===null)return '';const start=72+m.from*115,end=72+i*115,x=60+i*16;return `<path class="flow-arrow" d="M145 ${start} H${x} V${end} H140" marker-end="url(#flow-tip)"/>`;}).join('');
      content=`<div class="flow-map-wrap"><p>箭头：较早记录 → 引用它的后续记录。没有连线的记录独立展示；私人想法不向他人传播。</p><div class="flow-map-scroll" tabindex="0" role="region" aria-label="可横向滚动的信息流图"><svg class="flow-map" viewBox="0 0 580 ${visible.length*115+20}" role="group" aria-label="教学事件引用图，点选节点查看完整内容"><defs><marker id="flow-tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#69e1c4"/></marker></defs>${edges}${nodes}</svg></div><p class="map-hint">窄屏可左右滑动查看，点选节点阅读完整内容。</p></div>`;
    }
    const i=Math.min(state.event,state.round),event=events[i],actor=scenario.actors[event.actor],m=meta[i];
    $('interaction-view').innerHTML=`<div class="interaction-layout">${content}<aside class="event-explanation" aria-label="选中记录的解释"><span class="eyebrow">第 ${i+1} 轮 · 教学设定</span><h4>${esc(actor.name)}为什么这样做？</h4><dl><dt>身份与关注点</dt><dd>${esc(actor.motive)}</dd><dt>此刻掌握的信息</dt><dd>${esc(m.sees)}</dd><dt>行动 / 表达</dt><dd>${esc(event.text)}</dd><dt>进入下一轮的内容</dt><dd>${esc(m.change)}</dd></dl><p class="tiny-note">这是作者给出的情境解释，不是读取模型的内部思考。原版中，模型按角色上下文选择行动，环境保存行动结果，再供后续角色观察。</p></aside></div>`;
    $('interaction-view').querySelectorAll('[data-event]').forEach(node=>{
      const choose=()=>{stop();state.event=Number(node.dataset.event);state.actor=events[state.event].actor;renderProfile();graph();renderInteraction();$('interaction-view').querySelector(`[data-event="${state.event}"]`).focus({preventScroll:true});};
      node.addEventListener('click',choose);
      if(node.tagName.toLowerCase()==='g')node.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose();}});
    });
  }
  function downloadReport(){
    const scenario=current(),report=scenario.reports[state.strategy];
    const content=`# MiroFish 能力展示：教学报告\n\n> 人工编写的虚构教学示例。未调用模型、Zep 或 OASIS；不是实际模拟输出，不代表预测结果。\n\n## 场景\n${scenario.title}\n\n${scenario.question}\n\n## 情景\n${scenario.strategies[state.strategy]}\n${scenario.strategyNotes[state.strategy]}\n\n## 预设互动记录\n${scenario.events[state.strategy].map((e,i)=>`${i+1}. ${scenario.actors[e.actor].name}（${e.action}）：${e.text}`).join('\n')}\n\n## 示例观察\n${report.finding}\n\n## 风险\n${report.risk}\n\n## 现实验证\n${report.verify}\n\n上游仓库：https://github.com/666ghj/MiroFish\n研究版本：39d849138ef254f6c737ab4c4705e5545dbe31d4\n`;
    const url=URL.createObjectURL(new Blob(['\uFEFF',content],{type:'text/markdown;charset=utf-8'}));
    const link=document.createElement('a');link.href=url;link.download=`mirofish-${state.scenario}-${state.strategy}-teaching-report.md`;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function render(){
    const scenario=current();
    $('scenario-title').textContent=scenario.title;$('scenario-description').textContent=scenario.description;$('scenario-question').textContent=scenario.question;
    $('materials').innerHTML=scenario.materials.map(name=>`<div class="file">${esc(name)}</div>`).join('');
    for(const option of $('strategy').options)option.textContent=scenario.strategies[option.value];
    $('strategy').value=state.strategy;$('strategy-note').textContent=scenario.strategyNotes[state.strategy];
    document.querySelectorAll('[data-scenario]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.scenario===state.scenario)));
    document.querySelectorAll('[data-step]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.step)===state.step)));
    $('step-counter').textContent=`0${state.step+1} / 05`;$('previous').disabled=state.step===0;$('next').disabled=state.step===4;
    graph();renderProfile();renderStage();
  }
  document.querySelectorAll('[data-scenario]').forEach(button=>button.addEventListener('click',()=>{stop();Object.assign(state,{scenario:button.dataset.scenario,strategy:'baseline',step:0,actor:1,round:3,question:0});render();}));
  document.querySelectorAll('[data-step]').forEach(button=>button.addEventListener('click',()=>{stop();state.step=Number(button.dataset.step);render();}));
  $('strategy').addEventListener('change',event=>{stop();state.strategy=event.target.value;render();});
  $('next').addEventListener('click',()=>{stop();state.step=Math.min(4,state.step+1);render();});
  $('previous').addEventListener('click',()=>{stop();state.step=Math.max(0,state.step-1);render();});
  $('reset').addEventListener('click',()=>{stop();Object.assign(state,{strategy:'baseline',step:0,actor:1,round:3,question:0});render();});
  $('play').addEventListener('click',()=>{if(playback){stop();return;}if(state.step===4){state.step=0;render();}$('play').textContent='暂停播放';playback=setInterval(()=>{state.step=Math.min(4,state.step+1);render();if(state.step===4)stop();},4500);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  const base='https://github.com/666ghj/MiroFish/blob/39d849138ef254f6c737ab4c4705e5545dbe31d4/';
  const sources=[['项目说明','README-ZH.md'],['文档解析','backend/app/utils/file_parser.py'],['知识图谱','backend/app/services/graph_builder.py'],['角色生成','backend/app/services/oasis_profile_generator.py'],['环境配置','backend/app/services/simulation_config_generator.py'],['双平台仿真','backend/scripts/run_parallel_simulation.py'],['报告工具','backend/app/services/report_agent.py']];
  $('source-links').innerHTML=sources.map(([label,path])=>`<a href="${base+path}" target="_blank" rel="noopener">${label} ↗</a>`).join('');
  function openInteraction(view){stop();state.step=2;state.view=view;state.event=0;render();$('stage').scrollIntoView({behavior:'auto',block:'start'});}
  document.querySelectorAll('[data-open-view]').forEach(button=>button.addEventListener('click',()=>{location.hash=button.dataset.openView;openInteraction(button.dataset.openView);}));
  render();
  if(['#dialogue','#map'].includes(location.hash))openInteraction(location.hash.slice(1));
})();
