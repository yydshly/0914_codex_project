const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
let tab = '2d', effect = 'spotlight', threePlaying = false, threeFrame = 0, threeStart = 0;
let storyPlaying = false, storyFrame = 0, storyStart = 0, effectPlaying = !reduceMotion, curtainPlaying = !reduceMotion;
let threeReady = false, threeFallback = false, effectReady = false, effectWait;
const sceneBridge = () => $('#scene-3d').contentWindow?.__SCENE_3D_EXPORT__;
const effectWindow = () => $('#effect-frame').contentWindow;
const announce = (text) => { $('#live-status').textContent = text; };

function pauseAll() {
  $$('video').forEach(v => v.pause());
  threePlaying = false; storyPlaying = false;
  $('#play-3d').textContent = '播放场景'; $('#play-story').textContent = '播放示意';
  try { effectWindow()?.gsap?.globalTimeline.pause(); effectWindow()?.noLoop?.(); } catch {}
}
function switchTab(value, updateHash = true) {
  if (!['2d','3d','effects','srt'].includes(value)) value = '2d';
  pauseAll(); tab = value;
  $$('[data-tab]').forEach(b => { const active = b.dataset.tab === tab; b.setAttribute('aria-selected', String(active)); b.tabIndex = active ? 0 : -1; });
  $$('.panel').forEach(p => p.hidden = p.id !== `panel-${tab}`);
  if (updateHash) history.replaceState(null, '', `#${tab}`);
  if (tab === '3d') loadThree();
  if (tab === 'effects') { if (!$('#effect-frame').getAttribute('src')) loadEffect(); else applyEffectPlayback(); }
  if (tab === 'srt') renderStory();
}
$$('[data-tab]').forEach(button => {
  button.addEventListener('click', () => switchTab(button.dataset.tab));
  button.addEventListener('keydown', e => {
    const buttons = $$('[data-tab]'), i = buttons.indexOf(button);
    let target;
    if (e.key === 'ArrowRight') target = buttons[(i + 1) % buttons.length];
    if (e.key === 'ArrowLeft') target = buttons[(i + buttons.length - 1) % buttons.length];
    if (e.key === 'Home') target = buttons[0];
    if (e.key === 'End') target = buttons.at(-1);
    if (target) { e.preventDefault(); target.focus(); switchTab(target.dataset.tab); }
  });
});
addEventListener('hashchange', () => switchTab(location.hash.slice(1), false));
$$('[data-play-video]').forEach(button => {
  const video = document.getElementById(button.dataset.playVideo);
  button.addEventListener('click', () => {
    if (video.paused) { if (video.ended) video.currentTime = 0; video.play().catch(() => announce('请使用视频内的播放按钮。')); }
    else video.pause();
  });
  video.addEventListener('play', () => button.textContent = '暂停动画');
  video.addEventListener('pause', () => button.textContent = '播放动画');
  video.addEventListener('ended', () => button.textContent = '重新播放');
});
$$('[data-replay-video]').forEach(b => b.addEventListener('click', () => { const v = document.getElementById(b.dataset.replayVideo); v.currentTime = 0; v.play().catch(() => {}); }));
$$('[data-speed-video]').forEach(s => s.addEventListener('change', () => { document.getElementById(s.dataset.speedVideo).playbackRate = Number(s.value); }));

function loadThree() {
  const frame = $('#scene-3d');
  if (frame.getAttribute('src')) return;
  frame.src = frame.dataset.src;
  let attempts = 0;
  const check = setInterval(() => {
    if (sceneBridge()?.isReady()) {
      clearInterval(check); threeReady = true;
      sceneBridge().setFrame(0); $('#loading-3d').hidden = true;
      $('#play-3d').disabled = false; $('#camera-3d').disabled = false; $('#frame-3d').disabled = false;
      announce('三维场景已就绪，可以播放或拖动时间轴。');
    } else if (++attempts >= 100) {
      clearInterval(check); $('#loading-3d').textContent = '三维加载未完成，可点击下方观看渲染视频。';
    }
  }, 100);
}
function setThreeFrame(f) {
  threeFrame = Math.max(0, Math.min(89, Math.floor(f)));
  if (threeReady) sceneBridge().setFrame(threeFrame);
  $('#frame-3d').value = threeFrame; $('#frame-3d-value').textContent = `${threeFrame} / 89`;
}
$('#play-3d').addEventListener('click', () => {
  threePlaying = !threePlaying; threeStart = performance.now() - threeFrame / 30 * 1000;
  $('#play-3d').textContent = threePlaying ? '暂停场景' : '播放场景';
});
$('#frame-3d').addEventListener('input', e => { threePlaying = false; $('#play-3d').textContent = '播放场景'; setThreeFrame(Number(e.target.value)); });
$('#camera-3d').addEventListener('click', () => {
  const toggle = $('#scene-3d').contentDocument.querySelector('[data-free-camera-toggle]');
  if (!toggle) return; toggle.click();
  const active = toggle.getAttribute('aria-pressed') === 'true';
  $('#camera-3d').setAttribute('aria-pressed', String(active)); $('#camera-3d').textContent = active ? '恢复动画视角' : '自由视角';
});
$('#fallback-button').addEventListener('click', () => {
  threeFallback = !threeFallback; threePlaying = false; $('#play-3d').textContent = '播放场景';
  $('#scene-3d').hidden = threeFallback; $('#fallback-3d').hidden = !threeFallback;
  $('#loading-3d').hidden = threeFallback || threeReady;
  $('#play-3d').disabled = threeFallback || !threeReady; $('#camera-3d').disabled = threeFallback || !threeReady; $('#frame-3d').disabled = threeFallback || !threeReady;
  $('#fallback-button').textContent = threeFallback ? '返回实时三维' : '观看渲染视频';
  if (threeFallback) $('#fallback-3d').play().catch(() => {}); else $('#fallback-3d').pause();
});

const effectInfo = {
  spotlight: ['聚光灯文字揭示','让文字被光扫亮','用一束摆动的聚光灯揭示文字。输入文案，调整灯光和颜色，就能得到可运行的网页动效。','文案、摆幅、灯光大小、颜色与周期。','上游脚本生成 SVG + GSAP 动画 HTML。','可直接预览的网页。转成视频需另加渲染步骤。','修改文字后点击“应用文字”，观察同一动效如何复用。','运行上游生成脚本，网页另加文字编辑、播放控制及本地依赖。','light-spotlight-render'],
  curtain: ['可交互的印字线帘','把文字织进会动的线','文字随独立丝线一起拉伸、折叠和散开。在画面中移动鼠标或触摸，试着把帘子拨开。','文字或图片、布料色、墨色和物理参数。','上游脚本生成 p5.js 物理模拟；指针影响丝线运动。','可以离线运行的互动网页，适合探索触摸与物理动效。','鼠标移动可以拨动线帘；点击“恢复线帘”重新开始。','使用上游引擎与文字参数。改编来源：Jason Labbe / Dynamic ropes 2，CC BY-SA 4.0；未上传图片。','printed-curtain-render']
};
function applyEffectPlayback() {
  if (!effectReady) return;
  const active = tab === 'effects';
  if (effect === 'spotlight') {
    if (active && effectPlaying) effectWindow().gsap.globalTimeline.play(); else effectWindow().gsap.globalTimeline.pause();
    $('#play-effect').textContent = effectPlaying ? '暂停动效' : '播放动效';
  } else {
    if (active && curtainPlaying) effectWindow().loop(); else effectWindow().noLoop();
    $('#pause-curtain').textContent = curtainPlaying ? '暂停模拟' : '继续模拟';
  }
}
function loadEffect() {
  clearInterval(effectWait); effectReady = false;
  const data = effectInfo[effect];
  ['effect-title','effect-headline','effect-description','effect-input','effect-making','effect-output','effect-tip','effect-provenance'].forEach((id, i) => document.getElementById(id).textContent = data[i]);
  $('#effect-source').href = `https://github.com/vibe-motion/skills/tree/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/${data[8]}`;
  $('#spotlight-controls').hidden = effect !== 'spotlight'; $('#curtain-controls').hidden = effect !== 'curtain';
  $$('[data-effect]').forEach(b => { const selected = b.dataset.effect === effect; b.classList.toggle('selected', selected); b.setAttribute('aria-pressed', String(selected)); });
  $('#effect-frame').title = data[0]; $('#effect-frame').src = `demos/${effect}/index.html`;
  $('#effect-loading').textContent = '正在准备动效…'; $('#effect-loading').hidden = false;
  let tries = 0;
  effectWait = setInterval(() => {
    const w = effectWindow();
    if ((effect === 'spotlight' && w?.gsap && w.document.querySelector('#mainSVG')) || (effect === 'curtain' && w?.__PRINTED_CURTAIN_READY__)) {
      clearInterval(effectWait); effectReady = true; $('#effect-loading').hidden = true;
      if (effect === 'spotlight') updateSpotlight();
      applyEffectPlayback();
    } else if (++tries > 100) { clearInterval(effectWait); $('#effect-loading').textContent = '动效未能加载，请重新选择示例。'; }
  }, 100);
}
$$('[data-effect]').forEach(b => b.addEventListener('click', () => { effect = b.dataset.effect; loadEffect(); }));
function updateSpotlight() {
  if (!effectReady || effect !== 'spotlight') return;
  const value = $('#spotlight-text').value.trim() || 'VIBE MOTION';
  const weight = [...value].reduce((sum, char) => sum + (char.charCodeAt(0) > 255 ? 1 : .62), 0);
  effectWindow().document.querySelectorAll('svg text').forEach(t => { t.textContent = value; t.setAttribute('font-size', Math.min(118, 700 / Math.max(weight, 1))); });
}
$('#apply-text').addEventListener('click', () => { updateSpotlight(); announce('聚光灯文字已更新。'); });
$('#spotlight-text').addEventListener('keydown', e => { if (e.key === 'Enter') updateSpotlight(); });
$('#play-effect').addEventListener('click', () => { effectPlaying = !effectPlaying; applyEffectPlayback(); });
$('#reset-curtain').addEventListener('click', () => { if (effectReady && effect === 'curtain') { effectWindow().resetScene(); effectWindow().redraw?.(); } });
$('#pause-curtain').addEventListener('click', () => { curtainPlaying = !curtainPlaying; applyEffectPlayback(); });
const skills = [['尺子进度','ruler-progress-render'],['CLI打字动画','claude-typer'],['鱼眼聚焦','fisheye-motion'],['程序化游鱼','procedural-fish-render'],['Logo矢量与动效','pixel2motion'],['品牌发布片','brand-launch-video-star'],['动态K线图','remotion-candlestick'],['聚光灯扫字','light-spotlight-render'],['可交互线帘','printed-curtain-render'],['三维照片墙','remotion-3d-ticker'],['黑胶唱片机','remotion-vinyl-player'],['地球航线','threejs-earth-render'],['三维声沙粒子','3d-chladni-render'],['微信聊天','wechat-2d-render'],['动画十二原则','disney-animation-rule-skill']];
for (const [label, slug] of skills) {
  const a = document.createElement('a'); a.href = `https://github.com/vibe-motion/skills/tree/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/${slug}`; a.target = '_blank'; a.rel = 'noreferrer'; a.append(document.createTextNode(`${label} ↗`)); const small = document.createElement('small'); small.textContent = slug; a.append(small); $('#skills-grid').append(a);
}

const story = [
  ['01 / 汇总','把信息，汇聚到一起。','先把分散的信息汇总起来。'],
  ['02 / 排序','先做重要的事情。','再按重要程度排出优先级。'],
  ['03 / 安排','让每项任务，有自己的时间。','最后，把任务安排到时间轴上。']
];
const smooth = x => { x = Math.max(0, Math.min(1, x)); return x*x*(3-2*x); };
const mix = (a,b,t) => a + (b-a)*t;
function renderStory() {
  const shot = Math.min(2, Math.floor(storyFrame / 120));
  const local = (storyFrame % 120) / 119;
  $('#story-number').textContent = story[shot][0]; $('#story-heading').textContent = story[shot][1]; $('#story-subtitle').textContent = story[shot][2];
  const pad = n => String(n).padStart(2, '0');
  $('#story-time').textContent = `00:${pad(shot*4)} — 00:${pad((shot+1)*4)}`;
  $('#story-frame').value = storyFrame; $('#story-frame-value').textContent = `${(storyFrame/30).toFixed(1)} / 12.0 秒`;
  $$('[data-shot]').forEach(b => { const active = Number(b.dataset.shot) === shot; b.classList.toggle('active', active); b.setAttribute('aria-pressed', String(active)); });
  const box = $('.story-objects'), w = box.clientWidth, h = box.clientHeight;
  $('#story-track').style.opacity = shot === 2 ? smooth(local*3) : 0;
  for (let i=0;i<3;i++) {
    const card = $(`#card-${i}`), t = smooth((local - .12 - i*.06)*2.6);
    let x,y,rot,width;
    if (shot === 0) {
      x=mix([.03,.51,.27][i],.1,t); y=mix([.12,.03,.66][i],.07+i*.31,t); rot=mix([-9,8,-5][i],0,t); width=mix(.43,.8,t);
    } else if (shot === 1) {
      x=.1; y=mix(.07+i*.31,.07+[0,2,1][i]*.31,t); rot=0; width=.8;
    } else {
      x=mix(.1,[.05,.3,.53][i],t); y=mix(.07+[0,2,1][i]*.31,.17+i*.26,t); rot=0; width=mix(.8,.42,t);
    }
    card.style.width=`${width*100}%`; card.style.transform=`translate(${x*w}px,${y*h}px) rotate(${rot}deg)`;
    card.querySelector('.card-index').textContent = shot === 1 && local>.5 ? ['高','低','中'][i] : String(i+1).padStart(2,'0');
  }
}
$('#play-story').addEventListener('click', () => {
  if (storyFrame >= 359) storyFrame = 0;
  storyPlaying=!storyPlaying; storyStart=performance.now()-storyFrame/30*1000;
  $('#play-story').textContent=storyPlaying?'暂停示意':'播放示意';
});
$('#restart-story').addEventListener('click', () => { storyFrame=0; storyPlaying=true; storyStart=performance.now(); $('#play-story').textContent='暂停示意'; renderStory(); });
$('#story-frame').addEventListener('input', e => { storyPlaying=false; storyFrame=Number(e.target.value); $('#play-story').textContent='播放示意'; renderStory(); });
$$('[data-shot]').forEach(b => b.addEventListener('click', () => { storyPlaying=false; storyFrame=Number(b.dataset.shot)*120; $('#play-story').textContent='播放示意'; renderStory(); }));
addEventListener('resize', () => { if(tab==='srt') renderStory(); });
document.addEventListener('visibilitychange', () => { if(document.hidden) pauseAll(); });
let lastTick=-1;
function tick(now) {
  const frame=Math.floor(now/1000*30);
  if(frame!==lastTick) {
    lastTick=frame;
    if(threePlaying && tab==='3d') setThreeFrame(Math.floor((now-threeStart)/1000*30)%90);
    if(storyPlaying && tab==='srt') {
      storyFrame=Math.min(359,Math.floor((now-storyStart)/1000*30)); renderStory();
      if(storyFrame>=359) {storyPlaying=false; $('#play-story').textContent='重新播放';}
    }
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
switchTab(location.hash.slice(1)||'2d', false);
