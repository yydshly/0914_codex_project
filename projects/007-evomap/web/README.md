# EvoMap 理解手册

用“愿景、方案、证据”三个层次解释 EvoMap，涵盖经验复用与多 Agent 协作的区别、五步交互案例、角色分工、研究证据和下一阶段的对照实验。

页面是独立研究导读，不是 EvoMap 产品界面，不连接模型、账户、Agent 或 Hub。所有案例步骤仅切换本地说明。没有模拟收益曲线或编造业务成功率。

## 构建与阅读

在总仓库根目录运行：

```powershell
python projects/007-evomap/src/build_site.py
python -m http.server 8077 --bind 127.0.0.1 --directory projects/007-evomap/web/dist
```

访问 [本机导读](http://127.0.0.1:8077/)。也可以打开生成的 `dist/index.html`，页面主要内容和交互无需网络；外部来源链接需要联网。

源码是 `index.html`、`style.css`、`main.js`。构建脚本只复制这三个文件、两份明确列出的实验摘要，以及理解图的 PNG 与 SVG，排除源码缓存、环境配置和依赖。`dist/` 可重新构建，不进入版本管理。

理解图来源于本研究的产品方向归纳，使用 `src/draw_understanding.py` 生成。修改或重绘需要 Pillow 和微软雅黑字体；图已在本地打开检查文字与排版。

项目已加入统一 GitHub Pages 发布清单。推送到 main 后，工作流运行 `src/build_site.py`，与其他研究页面一起部署。上线并验证可访问后，再把在线入口登记到 `projects.json`。

## 验证范围

- JavaScript 语法检查通过。
- 页面本地资源、章节锚点、重复 ID 与产物白名单检查通过。
- 本机入口返回 HTTP 200。
- 页面提供键盘可操作的按钮、章节导航、动态区域提示与窄屏布局规则。
- 未执行浏览器交互、截图或视觉 QA；不把静态检查表述成跨设备验证。
