# EvoMap 理解手册

用“愿景、方案、证据”三个层次解释 EvoMap，涵盖经验复用与多 Agent 协作的区别、蜂群理解图、角色与能力的区别、五步交互案例、研究证据和下一阶段的对照实验。蜂群章节可通过 `#swarm` 直接访问。

页面是独立研究导读，不是 EvoMap 产品界面，不连接模型、账户、Agent 或 Hub。所有案例步骤仅切换本地说明。没有模拟收益曲线或编造业务成功率。

## 构建与阅读

在总仓库根目录运行：

```powershell
python projects/007-evomap/src/build_site.py
python -m http.server 8077 --bind 127.0.0.1 --directory projects/007-evomap/web/dist
```

访问 [本机导读](http://127.0.0.1:8077/)。也可以打开生成的 `dist/index.html`，页面主要内容和交互无需网络；外部来源链接需要联网。

源码是 `index.html`、`style.css`、`main.js`。构建脚本只复制这三个文件、两份明确列出的实验摘要，以及三张理解图各自的 PNG 与 SVG，共 11 个文件，排除源码缓存、环境配置和依赖。`dist/` 可重新构建，不进入版本管理。

产品方向图使用 `src/draw_understanding.py` 生成，蜂群理解图使用 `src/draw_swarm.py` 生成。修改或重绘需要 Pillow 和微软雅黑字体；CI 直接使用已生成的 PNG 和 SVG。图示为我们的概念归纳，来源与证据边界在网页对应章节说明。

新增“几个 AI 一起做网站”的汇总引导图，由 `src/draw_swarm_quickstart.py` 生成；网页入口为 `#swarm-quickstart`，同时通过 `projects.json.preview_images` 接入仓库首页 README。它用具体例子说明任务协作和长期经验复用，非云端运行截图。

已部署：[在线理解手册](https://yydshly.github.io/0914_codex_project/007-evomap/)。项目已加入统一 GitHub Pages 发布清单。推送到 main 后，工作流运行 `src/build_site.py`，与其他研究页面一起部署。

2026-09-16 首版部署成功，首版线上 7 个静态文件均返回 HTTP 200，并核对与本地构建内容一致（文本统一换行符后比较）；同时验证总导航与 001–007 全部入口可访问。后续加入蜂群理解图与汇总引导图，当前构建白名单为 11 个文件。

## 验证范围

- JavaScript 语法检查通过。
- 页面本地资源、章节锚点、重复 ID 与产物白名单检查通过。
- 本机入口返回 HTTP 200。
- 页面提供键盘可操作的按钮、章节导航、动态区域提示与窄屏布局规则。
- 未执行浏览器交互、截图或视觉 QA；不把静态检查表述成跨设备验证。
