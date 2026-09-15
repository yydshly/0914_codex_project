import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {buildMotionSceneProps, resolveMotionSceneContext, getMotionDurationInFrames} from '../upstream/create-vibe-motion/packages/template/motion/timeline.js';
import {normalizeAudioTrackManifest, removeMissingAudioTracks} from '../upstream/create-vibe-motion/packages/template/remotion/audioTrackManifest.js';

const results = [];
function check(name, actual, expected) {
  const passed = JSON.stringify(actual) === JSON.stringify(expected);
  results.push({name, actual, expected, passed});
}
check('默认 3 秒 × 30fps = 90 帧', getMotionDurationInFrames({fps: 30}), 90);
const frame45 = buildMotionSceneProps({frame: 45, fps: 30});
buildMotionSceneProps({frame: 3, fps: 30});
buildMotionSceneProps({frame: 80, fps: 30});
check('乱序请求后同帧参数不变', buildMotionSceneProps({frame: 45, fps: 30}), frame45);
check('非循环超范围停在最后一帧', buildMotionSceneProps({frame: 95, fps: 30}).frame, 89);
check('循环模式对总帧数取余', buildMotionSceneProps({frame: 95, fps: 30, loop: true}).frame, 5);
check('本模板 1920×1080 请求被限制为 1280×1080', resolveMotionSceneContext({videoWidth: 1920, videoHeight: 1080}).layout, {videoWidth: 1280, videoHeight: 1080});
const manifest = normalizeAudioTrackManifest({compositions: {demo: [
  {id:'voice', src:'voice.wav', startFrame:30, durationInFrames:60, volume:0.8},
  {id:'missing', src:'missing.wav', startFrame:0, durationInFrames:90}
]}});
check('音轨保存独立起点、时长和音量', [manifest.compositions.demo[0].startFrame, manifest.compositions.demo[0].durationInFrames, manifest.compositions.demo[0].volume], [30,60,0.8]);
const clean = removeMissingAudioTracks({manifest, availablePaths: new Set(['voice.wav'])});
check('移除缺失音频的引用', [clean.removedTrackCount, clean.manifest.compositions.demo.map(x=>x.src)], [1,['voice.wav']]);
writeFileSync(new URL('../notes/probe-2d-results.json', import.meta.url), JSON.stringify({scope:'Upstream pure functions only; no React rendering or audible playback', results},null,2)+'\n');
assert.ok(results.every(x=>x.passed));
console.log(`${results.length} source-level checks passed`);
