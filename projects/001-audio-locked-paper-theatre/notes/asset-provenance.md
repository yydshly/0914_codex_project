# 素材与来源

- `assets/paper-machine.png`：本次使用内置 imagegen 生成，原生透明背景。完整素材复制到子项目保存；没有引用上游节目素材。
- 原始生成提示：Use case: stylized-concept. Asset type: isolated transparent cut-paper prop for a sophisticated editorial animation. Create one beautiful friendly mint-teal papercraft document summarizing machine, orthographic straight front view, symmetrical clean silhouette, entirely contained with generous transparent margin. Handmade layered cardboard material, tactile paper fibers, folded beveled edges, subtle realistic contact shadows, warm cream faceplate, ochre brass little dial, two small coral buttons. Large dark horizontal paper input opening toward upper half, small wide horizontal output opening near bottom, one small translucent pale aqua window at center. The machine fills about 75 percent of a square canvas. Elegant editorial magazine art direction, not cartoon face, no eyes, no character, no writing, no letters, no logos, no background scene, no documents sticking out; documents will be independent animated layers. Genuine alpha-transparent background. Soft upper-left studio lighting. Each slot is a clean black horizontal rectangular opening suitable for registering a deterministic clip mask. Entire machine fully visible without cropped edges.
- 中文文字、记录卡、摘要、进度线、目标框、舞台：本项目程序绘制。
- 字体：运行电脑上的 Microsoft YaHei，仅渲染到视频，不分发字体文件。其他环境需要配置可用的中文字体路径。
- 配音：MiniMax `speech-2.8-hd`，系统音色 `male-qn-jingying`，生成速度 0.94；具体请求见 `assets/tts-request.json`。渲染阶段保持原始配音速度，尾部添加约 1.4 秒静音停留。
- 字幕：MiniMax 返回的真实音频句级时间戳，保存在 `assets/provider-subtitles.json`。句内动作采用导演编排的细分时间，未声称逐词对齐。
- 文稿、会议记录、摘要均为本次演示自编。机器表示一个整理过程；没有实时调用摘要模型。
- 配乐：本样例未添加背景音乐。
- 方法参考：[audio-locked-paper-theatre](https://github.com/jay-yangPY/audio-locked-paper-theatre)，研究 Commit `cb75aeea55b9eed0c299be1761810d8643a106c9`，MIT。未复制上游源码或私有音视频素材。
