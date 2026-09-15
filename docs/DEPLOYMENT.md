# 多个 Web 演示的部署约定

## 当前状态

已配置统一的 GitHub Actions 发布流程 `.github/workflows/pages.yml`。`pages.json` 显式选择要发布的项目编号，目前为 `002`；`scripts/build_pages.py` 将各项目的 `web/dist/` 打包到 `_site/<编号-slug>/`，并生成站点导航页。

发布状态以 GitHub Actions 部署成功且网页实际可访问为准。只有经过访问验证的演示地址才写入 `projects.json`，并同步到仓库索引。

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

## 官方参考

- [GitHub Pages 简介与限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
