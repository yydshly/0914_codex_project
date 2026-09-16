# Background Agents 中文交互导读

原生 HTML / CSS / JavaScript 静态网页，无需安装前端依赖。用于解释上游平台，不包含上游平台的后台服务或真实模型调用。

## 内容

- 网页、管理服务、代理程序、模型与工具的分工。
- 具体能力和网页、Slack、GitHub、Linear、自动化、Webhook 入口。
- 修复问题、增加功能、CI 失败排查三个教学场景与四步任务流程。
- OpenCode / Claude Agent 与模型渠道的接入说明；Claude 路径仅允许 Anthropic。
- 与当前 Codex 的关系、可借鉴的技术及前后端实现表。
- 总览图弹窗、PNG / SVG 下载、研究笔记和固定版本证据下载。
- [我们的理解汇总](../notes/understanding.md)：围绕此前讨论的问题，解释系统形态、分工、接入与技术价值。

## 本地运行

在总仓库根目录执行：

```powershell
python projects/011-background-agents/src/build_site.py
python -m http.server 8097 --bind 127.0.0.1 --directory projects/011-background-agents/web/dist
```

打开 [本地网页](http://127.0.0.1:8097/)，也可以直接打开 `dist/index.html`。

构建产物位于 `web/dist`，被版本控制忽略。资源使用相对路径，可复制整个产物目录到静态托管服务。当前未配置本项目的公网发布。

页面核心内容可离线阅读；外部源码链接需联网。关闭 JavaScript 后显示默认案例，正文和图示仍可访问。接入选择器只展示说明，不收集或保存账号凭据。

## 维护

修改 `index.html`、`style.css`、`main.js` 后重新构建并刷新网页。研究依据固定在上游提交 `4c470da615eaecbf8f64b0ae5a04666c99b4c536`；升级结论时需同步核对研究笔记。

[验证记录](../notes/web-verification.md)
