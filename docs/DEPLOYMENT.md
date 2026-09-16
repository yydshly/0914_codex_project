# 多个 Web 演示的部署约定

## 当前状态

已配置统一的 GitHub Actions 发布流程 `.github/workflows/pages.yml`。`pages.json` 显式选择要发布的项目编号，目前为 `001` 至 `006`；`scripts/build_pages.py` 将各项目的 `web/dist/` 打包到 `_site/<编号-slug>/`，并生成站点导航页。001、005、006 在 CI 中从源码构建，其余项目沿用已登记的静态产物。

发布状态以 GitHub Actions 部署成功且网页实际可访问为准。只有经过访问验证的演示地址才写入 `projects.json`，并同步到仓库索引。

已验证的在线入口：[演示导航页](https://yydshly.github.io/0914_codex_project/) · [001：语音驱动纸艺剧场](https://yydshly.github.io/0914_codex_project/001-audio-locked-paper-theatre/) · [002：Skill 能力校验](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/) · [003：Video TalkCraft](https://yydshly.github.io/0914_codex_project/003-video-talkcraft/)。003 于 2026-09-16 发布，导读采用专门整理的输入、制作、输出与一致性理解图。

006 于 2026-09-16 发布并验证：[Dashy 能力与原理研究页](https://yydshly.github.io/0914_codex_project/006-dashy/)。引导图采用能力架构全景图和原版工作台实拍；已核对线上页面与全部静态资源。

## GitHub Pages 地址规划

GitHub Pages 每个仓库最多有一个站点，可把多个静态演示放在同一站点的不同子目录：

```text
https://yydshly.github.io/0914_codex_project/
├── 001-example-repo/
└── 002-another-repo/
```

以上子项目路径是规划示例，并非已上线地址。每个演示沿用稳定的项目目录名；调整首页顺序不改变链接。

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

006 Dashy 发布的是研究展示页，包含架构总览、原版截图、能力与意义、接入边界和本机启动说明。原版 Dashy 的 Node 服务、探测、代理及配置写盘仍由本机演示提供，不会随静态页面发布。公开页面不请求访问者的本机 API。

## 官方参考

- [GitHub Pages 简介与限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
