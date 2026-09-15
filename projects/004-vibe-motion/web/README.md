# Vibe Motion 动画研究网页

以“动画成为可编辑、可复用、可批量渲染的代码工程”为入口，用技术总览图串起意义与原理。下方四个标签页展示二维真实视频、三维原始场景、两个上游动效实例、SRT语义分镜说明。

[打开 GitHub Pages 在线网页](https://yydshly.github.io/0914_codex_project/004-vibe-motion/)

## 本地查看

在子项目目录运行：

```powershell
python -m http.server 8045 --bind 127.0.0.1 --directory web/dist
```

打开 [动画研究室](http://127.0.0.1:8045/)；各分类可用 #2d、#3d、#effects、#srt 直达。

## 内容与资源

- index.html / style.css / app.js：研究展示源码。
- credits.html：上游来源、调整说明和验证边界。
- dist/：已打包的静态文件，资源使用相对路径，可以放在现有GitHub Pages子目录。
- dist/demos/three：原始场景与本地Three.js；仅调整iframe布局，不改变场景代码。
- dist/demos/spotlight：原生成脚本产物；GSAP本地化，外层提供文字和播放控制。
- dist/demos/curtain：原文字线帘与p5.js；保留NOTICE和原引擎文件。
- dist/data：预先编写的SRT与分镜数据，不是模型生成记录。

## 重新打包

在子项目目录运行：

```powershell
python -X utf8 src/build_gallery.py
python -X utf8 src/verify_gallery.py
```

需要已渲染的 assets/demo-2d.mp4 和 assets/demo-3d.mp4、src/demo-3d 安装后的Three.js依赖、upstream/skills内补充的生成脚本与模板，以及dist/vendor中GSAP 3.12.2的原始文件。脚本不部署站点，不调用大模型。

### 重新渲染二维样片

在 src/demo-2d 安装锁定依赖后：

```powershell
npm ci --ignore-scripts --no-audit --no-fund
node node_modules/@remotion/cli/remotion-cli.js render remotion/index.jsx Motion30fps ../../assets/demo-2d.mp4 --props=gallery-props.json --codec=h264 --pixel-format=yuv420p --concurrency=1 --muted --browser-executable='C:/Program Files/Google/Chrome/Application/chrome.exe'
```

修改浏览器路径为本机位置。样片1080×810、150帧、30fps、5秒、无音轨。工程沿用上游脚手架，仅通过gallery-props.json修改参数。

## GitHub Pages 发布

004 已加入总仓库 pages.json。main 分支推送后，由 .github/workflows/pages.yml 将本目录 dist/ 与其他项目的网页一起打包，部署至 GitHub Pages 的 /0914_codex_project/004-vibe-motion/ 子路径。静态资源使用相对路径，图、视频、Three.js、GSAP 与 p5.js 随站点一同发布。

GitHub Pages 托管效果展示与研究说明；此页面不调用模型、不接收 SRT 自动生成视频。真实 auto-motion 需要独立的模型与渲染执行环境。
