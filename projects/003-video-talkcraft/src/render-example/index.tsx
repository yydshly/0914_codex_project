import React from 'react';
import {Composition, registerRoot} from 'remotion';
import NumberCounter, {meta} from '../../upstream/template/cards/number-counter';

// 原始模板未改动；灰色人物轮廓为上游示意占位，不是数字人生成结果。
registerRoot(() => <Composition id="NumberCounter" component={NumberCounter}
  width={meta.width} height={meta.height} fps={meta.fps} durationInFrames={meta.durationInFrames}/>);
