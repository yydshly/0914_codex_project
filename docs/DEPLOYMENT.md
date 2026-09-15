# 多个 Web 演示的部署约定

## 当前状态

初始化阶段只建立研究目录与部署约定，尚未发布网站。实际有可运行的 Web 项目后，再配置构建和发布流程。

## GitHub Pages 地址规划

GitHub Pages 每个仓库最多有一个站点，可把多个静态演示放在同一站点的不同子目录：

```text
https://yydshly.github.io/0914_codex_project/
├── 001-example-repo/
└── 002-another-repo/
```

以上子项目路径是规划示例，并非已上线地址。每个演示沿用稳定的项目目录名；调整首页顺序不改变链接。

## 后续接入步骤

1. 各项目在自己的 `web/` 中维护源码、依赖和构建说明。
2. 设置应用资源基础路径为 `/0914_codex_project/001-example-repo/`，替换为实际编号和名称；同时检查路由前缀。
3. 用统一 GitHub Actions 流程分别构建需要发布的项目，将每个静态产物放到 `_site/<编号-slug>/`，根目录准备一个导航页。
4. 一次性上传完整 `_site/` 并部署到 GitHub Pages；每次部署都包含所有已上线项目的产物。
5. 在仓库 Settings → Pages 中选择 GitHub Actions 作为发布来源。
6. 确认页面、资源和刷新路径可访问后，将真实地址写入 `projects.json` 的 `demo` 并运行 `sync`。

不要让多个流程分别部署局部产物到同一个 Pages 站点：后一次部署会替换站点内容。单页应用需要考虑静态托管下的深层路由刷新，可采用 hash 路由或生成实际静态页面。

## 带后端的项目

GitHub Pages 托管静态 HTML、CSS 和 JavaScript。需要服务端、数据库或后台任务的研究项目，另行部署后端，并在子项目文档中记录服务地址、配置和运行方式；演示入口仍可统一收录到首页。

## 官方参考

- [GitHub Pages 简介与限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
