/* Public research catalog; no network data calls, credentials or tracking. */
const PROVIDERS = ['AgentKey', 'AIsa', 'TikHub'];
const PAGE_SIZE = 16;
const ENTRY_LABELS={confirmed:'来源接口已列出',declared:'统一入口 / 来源待定位',conflict:'上线状态冲突',planned:'仅规划'};
const ALIASES = {'小红书':'rednote red book xiaohongshu','抖音':'douyin','微信':'wechat 公众号 视频号','Bilibili':'b站 哔哩哔哩','微博':'weibo','知乎':'zhihu','快手':'kuaishou','皮皮虾':'pipixia','西瓜视频':'xigua','今日头条':'toutiao','淘宝':'taobao','京东':'jd.com','贝壳':'beike','X / Twitter':'推特'};

function filterInventory(rows, {query='', platform='', category='', status='', method='', entry='', planned=false}={}) {
  const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return rows.filter(row => {
    if (category && row.category !== category) return false;
    const coverage = platform ? [row.coverage[platform]].filter(Boolean) : Object.values(row.coverage);
    const eligible=coverage.filter(c=>(planned || c.status !== '即将上线') && (!status || c.status === status) && (!entry || c.access.entry_state===entry));
    if (!eligible.length) return false;
    if(method==='待核') {
      if(!eligible.some(c=>!c.access.methods.length || c.status==='状态冲突' || c.access.methods.some(m=>/待核|待发现/.test(m.certainty))))return false;
    } else if(method && !eligible.some(c=>c.access.methods.some(m=>m.kind===method)) && !(row.direct_access||[]).some(m=>m.kind===method)) return false;
    const haystack = [row.name, ALIASES[row.name] || '', row.category, row.kind, row.provides, ...eligible.flatMap(c=>[c.provides,...c.access.methods.map(m=>m.kind)]),...(row.direct_access||[]).map(m=>m.kind)].join(' ').toLocaleLowerCase();
    return terms.every(term=>haystack.includes(term));
  });
}
if (typeof module !== 'undefined') module.exports = {filterInventory};

if (typeof document !== 'undefined') {
  const data = window.RESEARCH_DATA;
  const $ = id=>document.getElementById(id);
  const records = data.inventory;
  let page=1;
  const el=(tag,text,cls)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;};
  const link=(text,url)=>{const a=el('a',text);if(!/^https:\/\//.test(url))throw Error('Invalid evidence link');a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;};
  function badge(status) {
    const cls=status==='即将上线'?'planned':status==='状态冲突'?'conflict':status.startsWith('官网')?'claim':'';
    return el('span',status,'status '+cls);
  }
  const categories=[...new Set(records.map(r=>r.category))];
  categories.forEach(category=>{const option=el('option',category);option.value=category;$('category').append(option);});
  $('total-count').textContent=records.length;
  document.querySelectorAll('[data-entry-count]').forEach(node=>node.textContent=records.filter(r=>r.entry_state===node.dataset.entryCount).length);

  function filterState(){return {query:$('query').value,platform:$('platform').value,category:$('category').value,status:$('status').value,method:$('method').value,entry:$('entry').value,planned:$('planned').checked};}
  function renderRows(){
    const matched=filterInventory(records,filterState());
    const priority={confirmed:0,declared:1,conflict:2,planned:3};
    const chosenProvider=$('platform').value;
    matched.sort((a,b)=>priority[chosenProvider?a.coverage[chosenProvider].access.entry_state:a.entry_state]-priority[chosenProvider?b.coverage[chosenProvider].access.entry_state:b.entry_state]);
    const pages=Math.max(1,Math.ceil(matched.length/PAGE_SIZE));
    page=Math.min(page,pages);
    $('result-count').textContent=`找到 ${matched.length} 条 · 共 ${records.length} 条登记`;
    $('source-rows').replaceChildren();
    matched.slice((page-1)*PAGE_SIZE,page*PAGE_SIZE).forEach(row=>{
      const tr=el('tr');
      const name=el('td');
      const button=el('button',row.name,'source-name');button.type='button';button.addEventListener('click',()=>openDetail(row));name.append(button,el('span',row.category,'row-kind'));
      const selectedProvider=$('platform').value;
      const description=selectedProvider?row.coverage[selectedProvider].provides:row.provides;
      const desc=el('td',description,'row-desc');
      const covers=selectedProvider?[row.coverage[selectedProvider]]:Object.values(row.coverage);
      const kinds=[...new Set(covers.flatMap(c=>c.access.methods.map(m=>m.kind)))];
      desc.append(el('span',kinds.length?'经服务：'+kinds.join(' · '):'获取入口：尚未确认','access-line'));
      if(row.direct_access.length)desc.append(el('span','另有原站：'+row.direct_access.map(m=>m.kind).join(' · '),'access-direct'));
      const explicit=Object.entries(row.coverage).filter(([p,c])=>(!selectedProvider||selectedProvider===p)&&c.access.entry_state==='confirmed').map(([p])=>p);
      if(explicit.length)desc.append(el('span','已列来源接口：'+explicit.join(' / '),'access-confirmed'));
      else desc.append(el('span',ENTRY_LABELS[selectedProvider?row.coverage[selectedProvider].access.entry_state:row.entry_state],'access-caution'));
      tr.append(name,desc);
      PROVIDERS.forEach(p=>{const td=el('td');td.dataset.platform=p;td.append(row.coverage[p]?badge(row.coverage[p].status):el('span','—','dash'));tr.append(td);});
      $('source-rows').append(tr);
    });
    $('empty').hidden=matched.length!==0;
    document.querySelector('.source-table').hidden=matched.length===0;
    $('page-label').textContent=matched.length?`第 ${page} / ${pages} 页 · 每页 ${PAGE_SIZE} 条`:'没有匹配结果';
    $('previous').disabled=page<=1;
    $('next').disabled=page>=pages;
  }
  function resetFilters(){ $('filters').reset();page=1;renderRows(); }
  $('filters').addEventListener('submit',event=>event.preventDefault());
  $('filters').addEventListener('reset',()=>{page=1;setTimeout(renderRows,0);});
  $('query').addEventListener('input',()=>{page=1;renderRows();});
  ['platform','category','status','planned','method','entry'].forEach(id=>$(id).addEventListener('change',()=>{
    if ((id==='status'&&$('status').value==='即将上线') || (id==='category'&&$('category').value==='规划来源')) $('planned').checked=true;
    if(id==='planned'&&!$('planned').checked){if($('status').value==='即将上线')$('status').value='';if($('category').value==='规划来源')$('category').value='';}
    if(id==='entry'&&$('entry').value==='planned')$('planned').checked=true;
    if(id==='planned'&&!$('planned').checked&&$('entry').value==='planned')$('entry').value='';
    page=1;renderRows();
  }));
  $('empty-reset').addEventListener('click',resetFilters);
  $('show-confirmed').addEventListener('click',()=>{resetFilters();$('entry').value='confirmed';renderRows();});
  ['previous','next'].forEach(id=>$(id).addEventListener('click',()=>{page+=id==='next'?1:-1;renderRows();document.querySelector('.results-bar').scrollIntoView({block:'start'});}));

  function openDetail(row){
    const content=$('detail-content');content.replaceChildren();
    const title=el('h2',row.name);title.id='detail-title';content.append(title,el('p',`${row.kind} · ${row.category}`,'detail-meta'));
    content.append(el('p',`${row.id} · 核查 ${row.checked_on} · 未实测业务接口`,'detail-note'));
    PROVIDERS.forEach(provider=>{
      const section=el('section',undefined,'detail-provider');
      const head=el('h3',provider);section.append(head);
      const c=row.coverage[provider];
      if(!c){section.append(el('p','本次资料未确认该平台接入此来源；不等于绝对不支持。'));content.append(section);return;}
      head.append(badge(c.status));section.append(el('p',c.provides));
      const a=c.access;
      section.append(el('p','对外接入：'+ENTRY_LABELS[a.entry_state],a.entry_state==='confirmed'?'access-confirmed':'detail-note'));
      const methods=el('div',undefined,'detail-methods');
      methods.append(el('h4','我们如何获取'));
      if(!a.methods.length)methods.append(el('p','尚未确认获取入口，不能视为已接入 API 或 RSS。'));
      a.methods.forEach(m=>{const item=el('div',undefined,'method-item');item.append(el('strong',m.kind+' · '+m.certainty),el('p',m.detail));m.evidence.forEach((ref,i)=>item.append(link(ref+' 依据 ↗',m.evidence_urls[i])));methods.append(item);});
      if(a.example){methods.append(el('h4','文档中的具体请求入口'),el('code',a.example.verb+' '+a.example.url,'feed-template'),el('p',a.example.purpose),link('请求入口依据 ↗',a.example.evidence_url));}
      methods.append(el('h4','授权与账号条件'),el('p',a.authorization),el('h4','返回内容'),el('p',a.output));
      const background=el('details',undefined,'upstream-details');background.append(el('summary','后台采集与其他方式（不影响上述入口的确认）'),el('h4','原始数据如何取得'),el('p',a.upstream),el('h4','RSS / Atom'),el('p',a.rss));methods.append(background);
      if(a.unknowns.length)methods.append(el('h4','尚不确定'),el('p',a.unknowns.join(' ')));
      section.append(methods);
      if(c.note)section.append(el('p',c.note,'detail-note'));
      c.evidence.forEach((ref,i)=>section.append(link(`${ref} 官方依据 ↗`,c.evidence_urls[i])));
      if(c.detail_url)section.append(link('具体接口入口 ↗',c.detail_url));
      content.append(section);
    });
    const direct=el('section',undefined,'detail-cleanup');direct.append(el('h3','原站直连：与上述三家分开看'),el('p',row.direct_access_note));row.direct_access.forEach(m=>{direct.append(el('h4',m.kind),el('p',m.detail));m.evidence.forEach((ref,i)=>direct.append(link(ref+' 官方依据 ↗',m.evidence_urls[i])));});content.append(direct);
    const cleanup=el('section',undefined,'detail-cleanup');cleanup.append(el('h3','后续清理建议'),el('p',row.cleanup));content.append(cleanup);
    $('source-detail').showModal();
  }
  $('close-detail').addEventListener('click',()=>$('source-detail').close());
  $('source-detail').addEventListener('click',event=>{if(event.target===$('source-detail')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();}});

  function showView(){
    const valid=['overview','sources','access','compare','process','evidence'];
    const view=valid.includes(location.hash.slice(1))?location.hash.slice(1):'overview';
    valid.forEach(id=>$(id).hidden=id!==view);
    document.querySelectorAll('[data-view]').forEach(a=>{if(a.dataset.view===view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    document.title=`${{overview:'研究导读',sources:'来源目录',access:'获取方式',compare:'三家对比',process:'数据处理',evidence:'证据与边界'}[view]} · 数据来源研究`;
  }
  window.addEventListener('hashchange',()=>{showView();window.scrollTo(0,0);});
  document.querySelectorAll('button[data-platform]').forEach(button=>button.addEventListener('click',()=>{resetFilters();$('platform').value=button.dataset.platform;$('planned').checked=button.dataset.platform==='AIsa';renderRows();location.hash='sources';}));
  categories.forEach(category=>{
    const listed=records.filter(row=>row.category===category && row.entry_state!=='planned');
    if(!listed.length)return;
    const section=el('article');section.append(el('h3',category),el('p',`${listed.length} 条登记 · 含来源、服务或能力`,'source-map-count'));
    const names=el('div',undefined,'source-map-names');
    listed.forEach(row=>{const button=el('button',row.name);button.type='button';button.addEventListener('click',()=>openDetail(row));names.append(button);});
    section.append(names);$('source-map').append(section);
  });

  const cleaning=[
    ['网页 / 文章','提取正文，保留出处。','保留标题、作者、发布时间、正文和链接；去掉导航、重复段落。原始 HTML 或响应单独留存。','抽查正文有没有被误删；确认每条记录都有来源与采集时间。','正文提取可交给 Firecrawl / Jina Reader；跨网页去重与完整性检查仍需我们负责。'],
    ['帖子 / 笔记','用平台与内容 ID 识别记录。','统一时间、编码和语言字段，原文与翻译分开保存；转发与原帖保留关系。','重复获取不增加相同记录；不能把引用、转发或不同版本直接合并。','同一笔记从两家服务获取，通常仍是一份原始内容，不是两个独立证据。'],
    ['评论 / 回复','保留关系，检查分页。','保留评论 ID、父评论 ID、作者标识与分页游标；标记已抓取页数和是否截断。','评论与回复的关系完整；未取完分页时不能称为“全部评论”。','点赞最多的评论可能不代表总体意见。清理数据与判断样本代表性是两件事。'],
    ['视频 / 音频','元数据不等于完整内容。','元数据、媒体地址、字幕分别保存；如需机器转写或 OCR，另存结果并标注生成方式。','能区分标题、官方字幕、自动转写和 AI 摘要；必要时抽查原片。','获取视频详情，不一定获取了画面中的信息，也不代表拿到了逐字稿。'],
    ['商品 / 房产','保留规格与价格快照。','商品、SKU、规格、地区、币种和价格采集时间分开；不同报价保留各自来源。','相同名称、不同规格不误合并；不同货币不直接比较。','昨天和今天的价格是两次观测，不能在去重时把价格变化抹掉。'],
    ['金融 / 链上','先统一数据口径。','记录交易所、代码、网络、币种、时区和数据频率；历史行情与即时行情分开。','同名资产不同链不混合；复权与原价、不同时间粒度不直接拼接。','拿到价格之后，仍要知道这是哪个市场、哪个时间点、哪种计价单位。'],
    ['企业 / 人员','匹配实体，保留冲突。','优先使用稳定标识；记录更新日期和来源间差异。没有字段就保留未知。','同名不直接合并；不能把“数据未提供”写成“该信息不存在”。','企业注册记录、数据库估算和模型推断的证据强度不同，应分开标注。'],
    ['搜索 / 回答','把材料与生成结论分开。','候选链接、已读取全文、引用片段、生成结论分别存储；维护结论到原文的连接。','重要结论能够返回具体原文，而非只指向另一份 AI 摘要。','带引用的回答有助于研究，但仍需核对引用是否真正支持那条结论。'],
    ['天气 / 地理','区分观测与预测。','统一经纬度、单位、时区和预测批次，记录数据来自观测、再分析还是预测模型。','历史观测不混为预测；不同坐标和预测发布时间不能无条件合并。','同一天的天气预测可能多次更新，需要保留每次预测的出具时间。']
  ];
  function chooseCleaning(index){
    document.querySelectorAll('[data-cleaning]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.cleaning)===index)));
    const [name,title,steps,check,example]=cleaning[index];const detail=$('cleaning-detail');
    detail.replaceChildren(el('p',name,'eyebrow'),el('h3',title),el('h4','建议处理'),el('p',steps),el('h4','验收重点'),el('p',check),el('p',example,'example'));
  }
  cleaning.forEach((item,index)=>{const button=el('button',item[0]);button.dataset.cleaning=index;button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>chooseCleaning(index));$('cleaning-options').append(button);});
  data.evidence.forEach(ref=>{const a=link('',ref.url);a.append(el('span',ref.id,'ref-id'),el('span',ref.title+' ↗'));$('evidence-list').append(a);});
  document.querySelectorAll('[data-evidence-count]').forEach(node=>node.textContent=data.evidence.length);
  chooseCleaning(0);renderRows();showView();
}
