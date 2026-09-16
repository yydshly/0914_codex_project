# 多个 Web 演示的部署约定

## 当前状态

已配置统一的 GitHub Actions 发布流程 `.github/workflows/pages.yml`。`pages.json` 显式选择要发布的项目编号，目前为 `001` 至 `013`；`scripts/build_pages.py` 将各项目的 `web/dist/` 打包到 `_site/<编号-slug>/`，并生成站点导航页。001、005、006、007、008、009、010、011、012、013 在 CI 中从源码构建，其余项目沿用已登记的静态产物。

发布状态以 GitHub Actions 部署成功且网页实际可访问为准。只有经过访问验证的演示地址才写入 `projects.json`，并同步到仓库索引。

已验证的在线入口：[演示导航页](https://yydshly.github.io/0914_codex_project/) · [001：语音驱动纸艺剧场](https://yydshly.github.io/0914_codex_project/001-audio-locked-paper-theatre/) · [002：Skill 能力校验](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/) · [003：Video TalkCraft](https://yydshly.github.io/0914_codex_project/003-video-talkcraft/)。003 于 2026-09-16 发布，导读采用专门整理的输入、制作、输出与一致性理解图。

006 于 2026-09-16 发布并验证：[Dashy 能力与原理研究页](https://yydshly.github.io/0914_codex_project/006-dashy/)。引导图采用能力架构全景图和原版工作台实拍；已核对线上页面与全部静态资源。

## GitHub Pages 地址规划

008 Douyin Downloader 已整理为抖音信息的获取与整理层，涵盖搜索热榜、评论、媒体下载、转写与归档。研究文档、交互网页和 PNG/SVG 全景图已发布至 [在线导读](https://yydshly.github.io/0914_codex_project/008-douyin-downloader/)；12 个文件逐项比对一致，总导航和八个项目入口验证通过。页面定位于获取与整理层，不登录抖音，也不把原理演示当下载实测。

007 于 2026-09-16 发布并验证：[EvoMap 理解手册](https://yydshly.github.io/0914_codex_project/007-evomap/)。内容围绕群体智能愿景、类似 RAG 的经验检索与沉淀、多 Agent 复用和执行反馈展开；已核对全部 7 个静态文件内容，并确认原有研究入口可访问。

GitHub Pages 每个仓库最多有一个站点，可把多个静态演示放在同一站点的不同子目录：

```text
https://yydshly.github.io/0914_codex_project/
├── 001-example-repo/
└── 002-another-repo/
```

以上子项目路径是规划示例，并非已上线地址。每个演示沿用稳定的项目目录名；调整首页顺序不改变链接。

009 MiroFish 于 2026-09-16 发布并验证：[能力与原理展示](https://yydshly.github.io/0914_codex_project/009-mirofish/)。包括能力全景图、处理原理、Unity 历史案例与预设交互教学。17 个文件内容逐项核对一致（文本统一换行后比较），导航和九个项目入口均可访问；未运行原版模型后端或验证预测效果。

## 添加后续演示

1. 在子项目 `web/` 中维护网页，准备可直接托管的 `web/dist/index.html` 及其静态资源；需要构建的项目在工作流打包前增加相应构建步骤。
2. 使用相对资源路径或正确的子目录前缀，单页导航优先使用 hash。
3. 将该项目编号加入 `pages.json`，提交并推送到 main。只发布清单明确选择的项目，不自动公开所有本地演示。
4. 工作流一次性上传完整 `_site/`，确保每次部署保留所有已选择的演示。
5. 仓库 Settings → Pages 的发布来源应为 GitHub Actions。
6. 等部署成功并确认网页和资源可访问，再写入 `projects.json` 的 `demo`，运行 `python scripts/catalog.py sync` 并提交。

本地可运行 `python scripts/build_pages.py --output <新的输出目录>` 检查打包。脚本拒绝覆盖已有目录，避免陈旧文件混入发布包。

不要让多个流程分别部署局部产物到同一个 Pages 站点：后一次部署会替换站点内容。单页应用需要考虑静态托管下的深层路由刷新，可采用 hash 路由或生成实际静态页面。

## 带后端的项目

GitHub Pages 托管静态 HTML、CSS 和 JavaScript。需要服务端、数据库或后台任务的研究项目，另行部署后端，并在子项目文档中记录服务地址、配置和运行方式；演示入口仍可统一收录到首页。

006 Dashy 同时发布研究页与“我的数字工作台”在线交互演示。研究页内嵌工作台，并提供独立打开入口；支持搜索、主题、布局、卡片编辑与浏览器本地保存、组件和工作区。CI 从固定上游版本构建到 `workbench/` 子目录。Node 服务、真实探测、代理及配置写盘由本机完整版提供；在线内存数据与状态切换分别标为固定示例和浏览器模拟，不请求访问者的本机 API。

## 官方参考

- [GitHub Pages 简介与限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

010 Graft 已接入统一构建与发布清单，打包交互导读、PNG/SVG 引导图和研究笔记。部署已成功，11 个静态文件逐项核对一致，总导航与十个项目入口均可访问；[在线导读](https://yydshly.github.io/0914_codex_project/010-graft/)已登记到仓库索引。能力定位为扫描源码构建索引、指导 AI 查找，构建原理待研究。

011 Background Agents 已发布并验证：[在线研究导读](https://yydshly.github.io/0914_codex_project/011-background-agents/)。包含能力、入口、执行流程、AI 接入、Codex 关系、PNG/SVG 总览图与理解汇总。13 个静态文件逐项核对一致，总导航及全部 11 个项目入口可访问；已关联仓库索引和项目说明。此次只发布研究网页，未部署 Open-Inspect 后端或执行沙箱。

012 Future AGI 于 2026-09-16 发布并验证：[AI 能力检测与评测研究](https://yydshly.github.io/0914_codex_project/012-future-agi/)。内容定位为检测和评估 AI 应用的能力与表现，说明七类检测方式，并明确根本原理需后期深入研究、实际效果待实测。21 个静态文件逐项核对一致，总导航摘要与 12 个项目入口可访问；正式地址已登记到项目索引。


013 AgentKey / AIsa / TikHub 数据来源研究已加入统一发布流程。包含研究摘要、引导图、73 条非“仅规划”的分类名录、148 条完整登记、获取方式、清理规则和逐条官方依据。已发布并验证：[在线研究导读](https://yydshly.github.io/0914_codex_project/013-agent-data-sources/)。首次上线 17 个静态文件逐项核对一致，总导航和全部 13 个项目入口可访问；不调用付费业务接口。
