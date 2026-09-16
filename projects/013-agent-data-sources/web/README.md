# 数据来源研究网页

原生 HTML/CSS/JavaScript，沿用总仓库静态研究网页结构。来源数据由本项目已经核查的 JSON 生成，不调用三家业务接口。

## 阅读入口

- 来源目录：名称/能力搜索，按平台、类别、证据状态筛选；规划项目默认隐藏。
- 获取方式：API、MCP、RSS/Atom、Webhook、数据集与浏览器扩展；来源详情区分接入商调用方式、原站采集机制、授权与尚不确定项。目录可按获取方式筛选。
- 三家对比：产品定位、获取、清理、搜索分析与操作的区别。
- 数据处理：五步流程、平台与我们的分工、九类数据的清理建议。
- 证据与边界：25 个官方资料链接、已发现的状态冲突和研究材料下载。

每个来源可展开查看各平台分别提供什么、文档依据、核查备注和清理建议。网页不将目录列示显示为“实测可用”。

## 本地构建与阅读

在总仓库根目录运行：

```powershell
python projects/013-agent-data-sources/src/build_site.py
python -m http.server 8130 --bind 127.0.0.1 --directory projects/013-agent-data-sources/web/dist
```

打开 http://127.0.0.1:8130/ 。也可直接打开 `dist/index.html`，数据已嵌入本地文件，无需联网加载。外部证据链接需联网。

维护源码：`index.html`、`style.css`、`main.js`；构建读取 `notes/source-inventory.json` 与 `notes/source-manifest.json`。修改后重新运行构建。产物放在被忽略的 `web/dist/`。

网页通过仓库统一 GitHub Pages 流程发布；`pages.json` 登记 013，工作流从本项目源码构建并与其他项目一起打包。正式地址：[在线研究导读](https://yydshly.github.io/0914_codex_project/013-agent-data-sources/)，已通过发布和访问核验。

默认打开“研究导读”，展示研究摘要、三家分工、引导图和 73 条非“仅规划”的分类名录；原有 `#sources`、`#access` 等链接保留。引导图与文字摘要支持下载；完整目录包含 148 条登记，规划条目默认隐藏。
