# Background Agents 能力与实现总览图

- `background-agents-overview.png`：2400 × 3320 高清图片，适合保存、阅读和分享。
- `background-agents-overview.svg`：保留文字与结构的可缩放版本，优先使用微软雅黑字体。
- `background-agents-overview-preview.png`：1200 × 1660 预览。

图为原创机制归纳，不是软件截图。内容基于 `ColeMurray/background-agents` 的固定提交 `4c470da615eaecbf8f64b0ae5a04666c99b4c536`，研究日期 2026-09-16。

## 阅读顺序

1. 顶部先理解产品形态：可自行部署的 Web 应用，配置 AI 并派发开发任务。
2. 由上往下看入口、管理服务、执行环境和结果交付。
3. 右侧模型面板与左侧代理程序分开：模型提供推理，程序执行工具操作。
4. 底部解释可复用技术、Codex 关系、部署条件与能力边界。

## 依据

见 [25 项固定版本来源](../notes/sources.md)与[实现笔记](../notes/architecture.md)。

- 入口、开发工具与多仓库：S01–S02。
- 队列、事件回传和代理接口：S03–S06。
- 子任务与 PR：S07–S08。
- 自动化、部署和五种沙箱后端：S09–S16。
- 模型渠道、认证与实际代理程序：S22–S25。
- “没有原生 Codex CLI 适配”依据 S06 的固定版本代理目录；不将项目对 Codex 模型的支持扩写为支持 Codex 桌面应用或 CLI。

尚未运行真实模型、云沙箱或端到端任务。具体模型调用权限由账号与渠道决定，图不承诺某次任务成功或服务始终可用。

## 复现与检查

在研究总仓库根目录运行：

```powershell
python projects/011-background-agents/src/draw_overview.py
```

需要 Pillow 和 Windows 微软雅黑字体。生成程序同时输出 PNG 与 SVG，并检查文本宽度和段落底边；预览图经过视觉检查，SVG 经过 XML 解析检查。不同系统的 SVG 字体回退可能改变字形，固定展示优先使用 PNG。
