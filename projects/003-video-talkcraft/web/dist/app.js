const COMMIT='8829ca31fb8aeb1b850e85e47a7d7584c349bc4a';
const REPO='https://github.com/Vincentwei1021/video-talkcraft';
const ORIGIN='https://vincentwei1021.github.io/video-talkcraft/';
const examples=[
 {id:'number-counter',name:'数字滚动',group:'数据表达',input:'一个目标数值、单位与说明文字；人物视频可选。',how:'数字先快后慢增长，落定时轻微放大；另一种形式是逐位滚轮。',limit:'数字落定时机需要重新对齐你的配音，长数字要检查排版。'},
 {id:'highlighter-sweep',name:'荧光笔划重点',group:'强调标注',input:'一句话及其中需要强调的短语。',how:'色带沿文字扫过，引导观众把注意力放到关键词。',limit:'必须核对文字实际宽度；不能让标注扫到邻近文字。'},
 {id:'evidence-scroll-tour',name:'网页证据巡游',group:'截图叙事',input:'真实网页的长截图，以及要停靠的区域坐标。',how:'在长截图上滚动、减速与停靠，讲到哪里就展示哪里。',limit:'演示页面用于说明运动；生产时要换成真实证据截图。'},
 {id:'host-shrink-to-chip',name:'人物缩成角标',group:'人物合成',input:'与口播同步的人物视频；干净背景或透明素材更易合成。',how:'人物从主体位置收缩成圆窗，在画面下角继续口播。',limit:'这里不生成数字人和口型。圆窗可保留背景，轮廓贴角需抠像。'},
 {id:'split-compare-slider',name:'滑动分屏对比',group:'多素材表达',input:'两份需要对比的图片或视频。',how:'分界移动，逐步揭示两侧差异。',limit:'两份素材要有可比性，裁切不能遮掉需要比较的区域。'},
 {id:'shape-wipe-transition',name:'形状遮罩转场',group:'镜头衔接',input:'相邻两镜的画面和预定的切换时间。',how:'形状覆盖画面，在遮挡过程中完成场景替换。',limit:'转场峰值需要对词锚，避免吞掉上一镜的关键数字。'}
];
const $=id=>document.getElementById(id);
function selectDemo(example){
 document.querySelectorAll('.effect-button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.id===example.id)));
 $('demo-name').textContent=example.name;
 $('demo-frame').title='原版动效演示：'+example.name;
 $('demo-frame').src='vendor/demos/'+example.id+'/index.html?embed=1&controls=1';
 $('original-link').href='vendor/demos/'+example.id+'/index.html';
 $('source-link').href=REPO+'/blob/'+COMMIT+'/template/cards/'+example.id+'.tsx';
 for(const key of ['input','how','limit']) $('demo-'+key).textContent=example[key];
}
examples.forEach((example,i)=>{
 const button=document.createElement('button');button.className='effect-button';button.dataset.id=example.id;
 button.innerHTML='<span class="num">0'+(i+1)+'</span><span><strong>'+example.name+'</strong><small>'+example.group+'</small></span>';
 button.addEventListener('click',()=>selectDemo(example));$('effect-list').append(button);
});
selectDemo(examples[0]);

document.querySelectorAll('[data-source]').forEach(a=>{a.href=REPO+'/blob/'+COMMIT+'/'+a.dataset.source;a.target='_blank';a.rel='noopener';});
const mockText='用户从一万增长到十万';
Array.from(mockText).forEach((char,i)=>{const span=document.createElement('span');span.className='word';span.textContent=char;span.dataset.start=(.5+i*.3).toFixed(2);$('words').append(span);});
let isPlaying=false,lastTick=0,requestId=0;
function updateTimeline(){
 const time=Number($('time-slider').value),offset=Number($('offset').value),frame=Math.floor(time*30),t=frame/30;
 $('time-value').textContent=time.toFixed(2)+'s';
 document.querySelectorAll('.word').forEach(span=>{const start=Number(span.dataset.start);span.classList.toggle('active',t>=start&&t<start+.3);});
 const progress=Math.max(0,Math.min(1,(t-(1.4+offset))/1.5+1e-9));
 const eased=1-Math.pow(1-progress,4);
 $('counter').textContent=Math.round(10000+90000*eased).toLocaleString('en-US');
 $('result-tag').textContent=progress>=1?'落定十万':progress>0?'计数中':'等待计数';
 $('beat-status').textContent=offset===0?'落定 2.90s · 相对偏差 0.00s，符合默认阈值。':'落定 3.20s · 相对偏差 0.30s，超过 0.10s 阈值。';
}
function stop(){isPlaying=false;cancelAnimationFrame(requestId);$('play').textContent='播放示意';}
function tick(now){if(!isPlaying)return;if(!lastTick)lastTick=now;const next=Math.min(4,Number($('time-slider').value)+(now-lastTick)/1000);lastTick=now;$('time-slider').value=next;updateTimeline();if(next>=4){stop();return;}requestId=requestAnimationFrame(tick);}
$('play').addEventListener('click',()=>{if(isPlaying){stop();return;}if(Number($('time-slider').value)>=4)$('time-slider').value=0;isPlaying=true;lastTick=0;$('play').textContent='暂停';requestId=requestAnimationFrame(tick);});
$('reset').addEventListener('click',()=>{stop();$('time-slider').value=0;updateTimeline();});
$('time-slider').addEventListener('input',()=>{stop();updateTimeline();});$('offset').addEventListener('change',updateTimeline);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});updateTimeline();

const testNames={'exact':'完全匹配','homophone':'同音错字','latin-interpolation':'英文词缺失插值','low-coverage':'低覆盖率','global-shift':'整体时间偏移','no-anchors':'无匹配锚点','timing-expansion':'逐字符展开','beat-correct':'正确节拍','beat-off-by-300ms':'节拍延后 0.30 秒','beat-tail-too-short':'镜尾仅剩 0.20 秒'};
fetch('experiments.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
 const passed=data.results.filter(x=>x.passed).length;$('experiment-summary').textContent=passed+' / '+data.results.length+' 项符合预期';
 for(const item of data.results){const tr=document.createElement('tr');for(const text of [testNames[item.id]||item.id,item.passed?'符合预期':'未通过',item.conclusion||(item.expected_exit==='reject'?'检测器按预期拒绝该输入。':'检测器按预期通过该输入。')]){const td=document.createElement('td');td.textContent=text;tr.append(td);}$('experiment-rows').append(tr);}
}).catch(()=>{$('experiment-summary').textContent='实验数据未加载，请通过本地服务打开。';});
fetch('render-result.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{if(data.status==='passed'){$('render-proof').hidden=false;$('render-meta').textContent=data.width+' × '+data.height+' · '+data.frames+' 帧 · '+data.fps+' fps · '+data.duration+' 秒';}}).catch(()=>{});

let allCards=[];
function renderCatalog(){
 const query=$('search').value.trim().toLowerCase(),category=$('category').value;
 const cards=allCards.filter(c=>(!category||c.category===category)&&[c.zhName,c.slug,c.title,c.usage].join(' ').toLowerCase().includes(query));
 $('catalog-count').textContent=cards.length+' / '+allCards.length+' 套';$('catalog').replaceChildren();
 for(const card of cards){const article=document.createElement('article');article.className='catalog-item';
 const label=document.createElement('span');label.className='pill';label.textContent=card.category;
 const title=document.createElement('h3');title.textContent=card.zhName;
 const slug=document.createElement('code');slug.textContent=card.slug;
 const links=document.createElement('div');links.className='links';
 for(const [text,url] of [['原版演示',ORIGIN+'demos/'+card.slug+'/index.html'],['源码',REPO+'/blob/'+COMMIT+'/template/cards/'+card.slug+'.tsx'],['配方',REPO+'/blob/'+COMMIT+'/references/cards/'+card.slug+'.md']]){const a=document.createElement('a');a.textContent=text;a.href=url;a.target='_blank';a.rel='noopener';links.append(a);}
 article.append(label,title,slug,links);$('catalog').append(article);
 }
 if(!cards.length){const p=document.createElement('p');p.textContent='没有匹配的效果，试试其他名称或清空筛选。';$('catalog').append(p);}
}
fetch('catalog.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
 allCards=data.cards;for(const category of [...new Set(allCards.map(c=>c.category))]){const option=document.createElement('option');option.value=category;option.textContent=category;$('category').append(option);}renderCatalog();
}).catch(()=>{$('catalog-count').textContent='目录数据未加载，请通过本地服务打开。';});
$('search').addEventListener('input',renderCatalog);$('category').addEventListener('change',renderCatalog);
