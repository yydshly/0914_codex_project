(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const data = window.DIAGRAM_CATALOG;
  let current = data.specimens[0], variant = 'light';
  const categories = data.taxonomy;
  for (const category of categories) {const option=document.createElement('option');option.value=category.name;option.textContent=category.name+' · '+category.exampleCount+'组';$('category').append(option);}
  for (const kind of ['基础图型','派生示例','动画演示','导入重绘']) {const option=document.createElement('option');option.value=kind;option.textContent=kind+' · '+data.specimens.filter(x=>x.kind===kind).length+'组';$('kind').append(option);}
  function showExample(item) {
    current=item;
    if (!item.variants.some(v=>v.id===variant)) variant='light';
    const selected=item.variants.find(v=>v.id===variant);
    $('type-category').textContent=item.category+' / '+item.kind+(item.family===item.id?'':' / 归入：'+item.familyName);
    $('type-name').textContent=item.name;
    $('type-question').textContent=item.question;
    $('type-use').textContent='适用：'+item.use;
    $('preview').src=selected.path;
    $('preview').title=item.name+' · '+selected.label;
    $('open-example').href=selected.path;
    $('download-example').href=selected.path;
    $('source-example').href=item.source.replace(/example-[^/]+\.html$/, selected.path.split('/').pop());
    $('variants').replaceChildren();
    for (const v of item.variants) {const b=document.createElement('button');b.textContent=item.variants.length===1?'特殊版本':v.label;b.setAttribute('aria-pressed',String(v.id===variant));b.addEventListener('click',()=>{variant=v.id;showExample(current);});$('variants').append(b);}
    for(const b of $('type-list').querySelectorAll('button')) b.setAttribute('aria-pressed',String(b.dataset.id===item.id));
  }
  function filter(){
    const q=$('search').value.trim().toLowerCase(), category=$('category').value,kind=$('kind').value;
    const items=data.specimens.filter(x=>(category==='all'||category===x.category)&&(kind==='all'||kind===x.kind)&&[x.name,x.id,x.question,x.use,x.familyName].join(' ').toLowerCase().includes(q));
    $('type-list').replaceChildren();
    for(const item of items){const b=document.createElement('button');b.dataset.id=item.id;b.setAttribute('aria-pressed',String(current.id===item.id));b.append(document.createTextNode(item.name));const s=document.createElement('small');s.textContent=item.kind+' · '+item.variants.length+' 版';b.append(s);b.addEventListener('click',()=>showExample(item));$('type-list').append(b);}
    $('count').textContent=items.length+' / '+data.groups+' 组示例';$('empty').hidden=items.length>0;
  }
  $('search').addEventListener('input',filter);
  function refilter(){filter();const first=$('type-list').querySelector('button');if(first&&!$('type-list').querySelector('[aria-pressed="true"]'))showExample(data.specimens.find(x=>x.id===first.dataset.id));}
  $('category').addEventListener('change',refilter);$('kind').addEventListener('change',refilter);
  for(const group of categories){
    const card=document.createElement('article');card.className='text-card taxonomy-card';
    const title=document.createElement('h3');title.textContent=group.name;
    const counts=document.createElement('p');counts.className='eyebrow';counts.textContent=group.baseCount+' 基础图型 / '+group.exampleCount+' 组示例';
    const question=document.createElement('p');question.textContent=group.question;
    card.append(counts,title,question);
    for(const baseOnly of [true,false]){
      const items=data.specimens.filter(x=>x.category===group.name&&(x.kind==='基础图型')===baseOnly);if(!items.length)continue;
      const label=document.createElement('h4');label.textContent=baseOnly?'基础图型':'派生、动画与导入示例';card.append(label);
      const links=document.createElement('div');links.className='type-chips';
      for(const item of items){const button=document.createElement('button');button.textContent=item.name;button.title=item.question;button.addEventListener('click',()=>{$('category').value=item.category;$('kind').value='all';$('search').value='';filter();showExample(item);location.hash='gallery';});links.append(button);}card.append(links);
    }
    $('taxonomy-cards').append(card);
  }
  const cases=[
    ['research-blue','研究流程 · 蓝色','六节点的中文流程，用于项目研究与交付说明。','完整保留六节点、五关系；采用本研究的蓝色与中文字体规范。'],
    ['research-orange','同结构 · 橙色','保持内容、坐标与字号，仅改变颜色角色。','本次手动配色实验，未运行网站品牌抓取。'],
    ['research-dark','同结构 · 深色','相同流程在深色背景上的对照。','内容与坐标不变，调整文字、边框与焦点颜色。'],
    ['research-full','完整解释页面','图形配合标题、摘要与边界说明。','下载 PNG / SVG 只包含图形，不包含页面外的摘要。'],
    ['research-executive','概览 · 三阶段','将六个操作整理为三个阶段，面向快速阅读。','资料＋提取→理解资料；核实＋规格→确认表达；绘图＋导出→制作交付。没有删除源节点含义。'],
    ['research-slide','幻灯片 · 16:9','相同六节点改为适合演示的横向单行结构。','画布 1600×900；重新排布，不是只拉伸原图。'],
    ['research-sketchy','手绘线条','给节点与线条增加轻微位移，保留清晰文字。','依据上游手绘图元，固定噪声种子；结构与内容不变。'],
    ['research-annotation','边注强调','用边缘批注指出需要注意的阶段。','新增说明属于本研究的解释，虚线引导不表示业务流程关系。']
  ];
  function showCase(c){$('case-title').textContent=c[1];$('case-description').textContent=c[2];$('case-ledger').textContent=c[3];$('case-preview').src='cases/'+c[0]+'.html';$('case-preview').title=c[1];$('case-links').replaceChildren();for(const [ext,label] of [['html','放大查看'],['svg','下载 SVG'],['png','下载 PNG']]){const a=document.createElement('a');a.href='cases/'+c[0]+'.'+ext;a.textContent=label;if(ext==='html'){a.target='_blank';a.rel='noopener';}else a.download='';$('case-links').append(a);}for(const b of $('case-selector').children)b.setAttribute('aria-pressed',String(b.dataset.id===c[0]));}
  for(const c of cases){const b=document.createElement('button');b.dataset.id=c[0];b.textContent=c[1];b.addEventListener('click',()=>showCase(c));$('case-selector').append(b);}
  function route(){const id=location.hash.slice(1)||'overview';const valid=document.querySelector('.panel#'+CSS.escape(id))?id:'overview';for(const section of document.querySelectorAll('.panel'))section.hidden=section.id!==valid;for(const a of document.querySelectorAll('.navigation a')){const active=a.hash==='#'+valid;a.classList.toggle('selected',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}}
  window.addEventListener('hashchange',route);
  filter();showExample(current);showCase(cases[0]);route();
})();
