# 来源、版本与许可记录

研究日期：2026-09-16。以下为固定版本源码观察，不是法律意见或授权结论。

## 固定版本

| 仓库 | Commit | 选取文件数 |
| --- | --- | --- |
| [create-vibe-motion](https://github.com/vibe-motion/create-vibe-motion) | [2657ae9abadb89714bdabf0d3aef210e60ce1223](https://github.com/vibe-motion/create-vibe-motion/tree/2657ae9abadb89714bdabf0d3aef210e60ce1223) | 32 |
| [create-vibe-motion-3d](https://github.com/vibe-motion/create-vibe-motion-3d) | [b88aa9999ab37b6202b5d7370a91e85ded0e1919](https://github.com/vibe-motion/create-vibe-motion-3d/tree/b88aa9999ab37b6202b5d7370a91e85ded0e1919) | 13 |
| [auto-motion](https://github.com/vibe-motion/auto-motion) | [17ead629d010f7e5495f645d46fafd6876482c32](https://github.com/vibe-motion/auto-motion/tree/17ead629d010f7e5495f645d46fafd6876482c32) | 7 |
| [skills](https://github.com/vibe-motion/skills) | [cb3c905e4bc362e02e040035b5c88b13fdd54cf4](https://github.com/vibe-motion/skills/tree/cb3c905e4bc362e02e040035b5c88b13fdd54cf4) | 17 |

## 许可与署名

- create-vibe-motion 和 create-vibe-motion-3d 的 CLI package.json 均声明 MIT；所检查的固定版本文件树没有独立 LICENSE。保留包元信息与来源，未补写许可证文本。
- auto-motion 和 skills 的所查树未发现统一 LICENSE 文件，因此不将其概括为全部 MIT。
- printed-curtain-render 原引擎注明 Jason Labbe / Dynamic ropes 2、CC BY-SA 4.0，保留 [NOTICE](../upstream/skills/printed-curtain-render/assets/printed-curtain-template/NOTICE.txt)。
- 3d-chladni-render 的预览素材注明 Lykno、CC BY-NC 4.0；本研究未下载或重新发布该预览GIF。
- 本地三维示例由原始脚手架生成，场景作者归上游项目；封面与MP4是本机运行其模板得到的结果。第三方依赖许可保存在安装包中。
- 当前仅完成本地研究，没有推送或部署。本研究记录不改变上游或素材许可。

## 快照说明

upstream 是精简研究快照，不是完整安装包；未收集的脚本、图片、样式和依赖仍需从固定版本上游获取。可运行的三维工程在 src/demo-3d。

inventory.json 保存每个文件的固定commit链接与SHA-256。src/collect_sources.py 默认复用清单中的commit；新机器可从GitHub获取固定版本，Windows需curl.exe与联网。

两个脚手架最初由浅克隆获取；auto-motion的大型克隆传输未完成，已终止并改用GitHub API与原始文件获取研究所需文本，避免下载无关媒体。

## 文件证据索引

| 文件 | 固定上游源码 |
| --- | --- |
| [create-vibe-motion/README.md](../upstream/create-vibe-motion/README.md) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/README.md) |
| [create-vibe-motion/package.json](../upstream/create-vibe-motion/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/package.json) |
| [create-vibe-motion/packages/template/AGENTS.md](../upstream/create-vibe-motion/packages/template/AGENTS.md) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/AGENTS.md) |
| [create-vibe-motion/packages/template/eslint.config.js](../upstream/create-vibe-motion/packages/template/eslint.config.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/eslint.config.js) |
| [create-vibe-motion/packages/template/motion/Scene.jsx](../upstream/create-vibe-motion/packages/template/motion/Scene.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/Scene.jsx) |
| [create-vibe-motion/packages/template/motion/composition-id.js](../upstream/create-vibe-motion/packages/template/motion/composition-id.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/composition-id.js) |
| [create-vibe-motion/packages/template/motion/config.js](../upstream/create-vibe-motion/packages/template/motion/config.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/config.js) |
| [create-vibe-motion/packages/template/motion/plugin.js](../upstream/create-vibe-motion/packages/template/motion/plugin.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/plugin.js) |
| [create-vibe-motion/packages/template/motion/project.js](../upstream/create-vibe-motion/packages/template/motion/project.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/project.js) |
| [create-vibe-motion/packages/template/motion/render-presets/default.json](../upstream/create-vibe-motion/packages/template/motion/render-presets/default.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/render-presets/default.json) |
| [create-vibe-motion/packages/template/motion/timeline.js](../upstream/create-vibe-motion/packages/template/motion/timeline.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/motion/timeline.js) |
| [create-vibe-motion/packages/template/package.json](../upstream/create-vibe-motion/packages/template/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/package.json) |
| [create-vibe-motion/packages/template/public/.vibe-motion/audio-tracks.json](../upstream/create-vibe-motion/packages/template/public/.vibe-motion/audio-tracks.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/public/.vibe-motion/audio-tracks.json) |
| [create-vibe-motion/packages/template/remotion.config.js](../upstream/create-vibe-motion/packages/template/remotion.config.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion.config.js) |
| [create-vibe-motion/packages/template/remotion/AudioTracks.jsx](../upstream/create-vibe-motion/packages/template/remotion/AudioTracks.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/AudioTracks.jsx) |
| [create-vibe-motion/packages/template/remotion/CompositionRoot.jsx](../upstream/create-vibe-motion/packages/template/remotion/CompositionRoot.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/CompositionRoot.jsx) |
| [create-vibe-motion/packages/template/remotion/ProjectRoot.jsx](../upstream/create-vibe-motion/packages/template/remotion/ProjectRoot.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/ProjectRoot.jsx) |
| [create-vibe-motion/packages/template/remotion/StudioAudioDropTarget.jsx](../upstream/create-vibe-motion/packages/template/remotion/StudioAudioDropTarget.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/StudioAudioDropTarget.jsx) |
| [create-vibe-motion/packages/template/remotion/VideoComposition.jsx](../upstream/create-vibe-motion/packages/template/remotion/VideoComposition.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/VideoComposition.jsx) |
| [create-vibe-motion/packages/template/remotion/audioTrackManifest.js](../upstream/create-vibe-motion/packages/template/remotion/audioTrackManifest.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/audioTrackManifest.js) |
| [create-vibe-motion/packages/template/remotion/index.jsx](../upstream/create-vibe-motion/packages/template/remotion/index.jsx) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/index.jsx) |
| [create-vibe-motion/packages/template/remotion/pluginRuntime.js](../upstream/create-vibe-motion/packages/template/remotion/pluginRuntime.js) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/remotion/pluginRuntime.js) |
| [create-vibe-motion/packages/template/scaffold-manifest.json](../upstream/create-vibe-motion/packages/template/scaffold-manifest.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scaffold-manifest.json) |
| [create-vibe-motion/packages/template/scaffold-template-package.json](../upstream/create-vibe-motion/packages/template/scaffold-template-package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scaffold-template-package.json) |
| [create-vibe-motion/packages/template/scripts/remotion-browser-executable.mjs](../upstream/create-vibe-motion/packages/template/scripts/remotion-browser-executable.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scripts/remotion-browser-executable.mjs) |
| [create-vibe-motion/packages/template/scripts/remotion-cli.mjs](../upstream/create-vibe-motion/packages/template/scripts/remotion-cli.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scripts/remotion-cli.mjs) |
| [create-vibe-motion/packages/template/scripts/remotion-ensure-browser.mjs](../upstream/create-vibe-motion/packages/template/scripts/remotion-ensure-browser.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scripts/remotion-ensure-browser.mjs) |
| [create-vibe-motion/packages/template/scripts/remotion-render-demo.mjs](../upstream/create-vibe-motion/packages/template/scripts/remotion-render-demo.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scripts/remotion-render-demo.mjs) |
| [create-vibe-motion/packages/template/scripts/remotion-render.mjs](../upstream/create-vibe-motion/packages/template/scripts/remotion-render.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/template/scripts/remotion-render.mjs) |
| [create-vibe-motion-3d/README.md](../upstream/create-vibe-motion-3d/README.md) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/README.md) |
| [create-vibe-motion-3d/package.json](../upstream/create-vibe-motion-3d/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/package.json) |
| [create-vibe-motion-3d/packages/template/README.md](../upstream/create-vibe-motion-3d/packages/template/README.md) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/README.md) |
| [create-vibe-motion-3d/packages/template/index.html](../upstream/create-vibe-motion-3d/packages/template/index.html) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/index.html) |
| [create-vibe-motion-3d/packages/template/index.js](../upstream/create-vibe-motion-3d/packages/template/index.js) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/index.js) |
| [create-vibe-motion-3d/packages/template/package.json](../upstream/create-vibe-motion-3d/packages/template/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/package.json) |
| [create-vibe-motion-3d/packages/template/scaffold-manifest.json](../upstream/create-vibe-motion-3d/packages/template/scaffold-manifest.json) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/scaffold-manifest.json) |
| [create-vibe-motion-3d/packages/template/scaffold-template-package.json](../upstream/create-vibe-motion-3d/packages/template/scaffold-template-package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/scaffold-template-package.json) |
| [create-vibe-motion-3d/packages/template/scripts/export-api.mjs](../upstream/create-vibe-motion-3d/packages/template/scripts/export-api.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/scripts/export-api.mjs) |
| [create-vibe-motion-3d/packages/template/src/sceneControls.js](../upstream/create-vibe-motion-3d/packages/template/src/sceneControls.js) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/template/src/sceneControls.js) |
| [auto-motion/AGENTS.md](../upstream/auto-motion/AGENTS.md) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/AGENTS.md) |
| [auto-motion/PROMPT.md](../upstream/auto-motion/PROMPT.md) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/PROMPT.md) |
| [auto-motion/README.md](../upstream/auto-motion/README.md) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/README.md) |
| [auto-motion/auto-test/run.sh](../upstream/auto-motion/auto-test/run.sh) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/auto-test/run.sh) |
| [auto-motion/auto-test/transcription.srt](../upstream/auto-motion/auto-test/transcription.srt) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/auto-test/transcription.srt) |
| [auto-motion/auto-test/validate.sh](../upstream/auto-motion/auto-test/validate.sh) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/auto-test/validate.sh) |
| [auto-motion/exampleFolder/run-claude-ai.sh](../upstream/auto-motion/exampleFolder/run-claude-ai.sh) | [源码](https://github.com/vibe-motion/auto-motion/blob/17ead629d010f7e5495f645d46fafd6876482c32/exampleFolder/run-claude-ai.sh) |
| [skills/3d-chladni-render/SKILL.md](../upstream/skills/3d-chladni-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/3d-chladni-render/SKILL.md) |
| [skills/README.md](../upstream/skills/README.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/README.md) |
| [skills/brand-launch-video-star/SKILL.md](../upstream/skills/brand-launch-video-star/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/brand-launch-video-star/SKILL.md) |
| [skills/claude-typer/SKILL.md](../upstream/skills/claude-typer/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/claude-typer/SKILL.md) |
| [skills/disney-animation-rule-skill/SKILL.md](../upstream/skills/disney-animation-rule-skill/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/disney-animation-rule-skill/SKILL.md) |
| [skills/fisheye-motion/SKILL.md](../upstream/skills/fisheye-motion/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/fisheye-motion/SKILL.md) |
| [skills/light-spotlight-render/SKILL.md](../upstream/skills/light-spotlight-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/light-spotlight-render/SKILL.md) |
| [skills/pixel2motion/SKILL.md](../upstream/skills/pixel2motion/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/pixel2motion/SKILL.md) |
| [skills/printed-curtain-render/SKILL.md](../upstream/skills/printed-curtain-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/printed-curtain-render/SKILL.md) |
| [skills/printed-curtain-render/assets/printed-curtain-template/NOTICE.txt](../upstream/skills/printed-curtain-render/assets/printed-curtain-template/NOTICE.txt) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/printed-curtain-render/assets/printed-curtain-template/NOTICE.txt) |
| [skills/procedural-fish-render/SKILL.md](../upstream/skills/procedural-fish-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/procedural-fish-render/SKILL.md) |
| [skills/remotion-3d-ticker/SKILL.md](../upstream/skills/remotion-3d-ticker/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/remotion-3d-ticker/SKILL.md) |
| [skills/remotion-candlestick/SKILL.md](../upstream/skills/remotion-candlestick/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/remotion-candlestick/SKILL.md) |
| [skills/remotion-vinyl-player/SKILL.md](../upstream/skills/remotion-vinyl-player/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/remotion-vinyl-player/SKILL.md) |
| [skills/ruler-progress-render/SKILL.md](../upstream/skills/ruler-progress-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/ruler-progress-render/SKILL.md) |
| [skills/threejs-earth-render/SKILL.md](../upstream/skills/threejs-earth-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/threejs-earth-render/SKILL.md) |
| [skills/wechat-2d-render/SKILL.md](../upstream/skills/wechat-2d-render/SKILL.md) | [源码](https://github.com/vibe-motion/skills/blob/cb3c905e4bc362e02e040035b5c88b13fdd54cf4/wechat-2d-render/SKILL.md) |
| [create-vibe-motion/packages/create-vibe-motion/package.json](../upstream/create-vibe-motion/packages/create-vibe-motion/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/create-vibe-motion/package.json) |
| [create-vibe-motion/packages/create-vibe-motion/bin/create-vibe-motion.mjs](../upstream/create-vibe-motion/packages/create-vibe-motion/bin/create-vibe-motion.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/packages/create-vibe-motion/bin/create-vibe-motion.mjs) |
| [create-vibe-motion/scripts/sync-template-to-cli.mjs](../upstream/create-vibe-motion/scripts/sync-template-to-cli.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion/blob/2657ae9abadb89714bdabf0d3aef210e60ce1223/scripts/sync-template-to-cli.mjs) |
| [create-vibe-motion-3d/packages/create-vibe-motion-3d/package.json](../upstream/create-vibe-motion-3d/packages/create-vibe-motion-3d/package.json) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/create-vibe-motion-3d/package.json) |
| [create-vibe-motion-3d/packages/create-vibe-motion-3d/bin/create-vibe-motion-3d.mjs](../upstream/create-vibe-motion-3d/packages/create-vibe-motion-3d/bin/create-vibe-motion-3d.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/packages/create-vibe-motion-3d/bin/create-vibe-motion-3d.mjs) |
| [create-vibe-motion-3d/scripts/sync-template-to-cli.mjs](../upstream/create-vibe-motion-3d/scripts/sync-template-to-cli.mjs) | [源码](https://github.com/vibe-motion/create-vibe-motion-3d/blob/b88aa9999ab37b6202b5d7370a91e85ded0e1919/scripts/sync-template-to-cli.mjs) |
