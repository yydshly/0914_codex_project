# 英语微课堂：Where is the ball?

[打开课堂](../../web/english.html) · [观看 MP4](output/demo.mp4) · [能力与场景总览](../../web/guide.html)

## 课堂内容

面向初学者，用同一颗小球在盒子里、桌面上和桌子下的运动，解释物体位置用法 in / on / under。目标是看懂位置，并能用 “The ball is … the …” 说出完整句子。

课堂结构：看物体 → 听解释和例句 → 跟读停顿 → 拆分句子 → 看图作答 → 用身边物品迁移练习。页面另有三道固定答案选择题、即时解释和本轮得分；没有录音、发音评分、个人学习档案或自适应教学。

适合用作课堂导入、难点讲解、暂停提问和课后复习单元。视频可以放进教师已有的 PPT；这次没有生成可编辑 PPT。

## 真实输出

- MiniMax `speech-2.8-hd` / `male-qn-jingying`，中英混合合成，语速参数 0.90。
- 原始声音 87.480 秒，23 条供应商句级时间戳；合成时加入 3 次 2.5 秒跟读停顿和 2 次 3 秒作答停顿。配音落盘后保持原样。
- 成片 89.000 秒、1920×1080、24 fps、H.264 / AAC。
- 全片解码通过，无黑屏；成片与原始音频相关系数 0.999955；原配音哈希保持不变。
- 检查实际渲染关键帧中盒子的前壁遮挡、球与桌面接触、桌下位置和题目隐藏答案。详见 [QA 报告](output/qa-report.json) 和 [关键帧](output/contact-sheet.jpg)。
- 动画由自编 Pillow / FFmpeg 合成；句内动作是人工编排，不声称逐词对齐或完成上游独立审核。

## 素材与语法依据

例句与脚本自行编写。位置用法参考 [British Council 儿童英语位置介词](https://learnenglishkids.britishcouncil.org/grammar-vocabulary/grammar-practice/prepositions-place)，未复制其练习题。

小球、文字、词卡、网页练习图使用程序基本图形。桌子和盒子由内置 ImageGen 生成；生成后保留透明图层，按固定几何位置组合。

### 桌子完整生成提示

输出：[assets/table.png](assets/table.png)

```text
One isolated papercraft classroom table for a beginner English prepositions lesson. Straight-on front orthographic view, completely level rectangular horizontal tabletop, two vertical sturdy legs at far left and far right, unobstructed empty space underneath. Warm honey-gold cardboard, subtle hand-crafted paper texture and folded edges. No perspective tilt, no other objects, no text, no ball, no background, genuine transparent alpha background. Table is wide and low, centered in square canvas with generous margin. The tabletop top edge must be visually straight and flat so a separately animated ball can rest on it. Refined editorial cut-paper illustration, soft studio lighting.
```

### 盒子完整生成提示

输出：[assets/box.png](assets/box.png)

```text
One isolated OPEN TOP rectangular blue papercraft storage box, no lid, for an English lesson illustrating a ball IN a box. Straight front view with very slight elevated view to see into the opening, flat rectangular front wall and clean open rectangular upper cavity. Broad short box with pale blue inside and medium sky-blue front wall. Orthographic, handmade layered cardstock with subtle fibers and folded edges, soft studio lighting. Single object centered with generous margins on genuine transparent alpha background. No writing, no text, no logos, no other objects, no ball. Top opening and front wall clearly separate to allow a composited ball to sit behind the front wall.
```

## 复现

在子项目目录运行，复用已有声音，不会重复调用付费合成。

```sh
python src/english_render.py
python src/verify.py --episode english
python src/build_series_pages.py
python src/build_guide.py
python src/serve.py
```

修改讲稿时需要重新生成并锁定音频，再调整时间线。文稿见 [script.json](script.json)，停顿见 [pauses.json](pauses.json)；密钥不存入本项目。
