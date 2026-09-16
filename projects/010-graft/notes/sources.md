# 来源与核对范围

- 研究日期：2026-09-16。
- 上游：[trailhq/Graft](https://github.com/trailhq/Graft)。
- GitHub API 读取的 main 提交：f9e65396e638e517aecae0d731017f53084d70ed。
- [固定版本 package.json](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/package.json)：包名、0.18.0、MIT、Node.js ≥20；不代表已验证 npm 安装。
- [README](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/README.md)：公开能力、可视化、基础与深度模式、作者基准。
- [MCP 工具实现](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/mcp/tools.ts)：查询参数、结果范围、刷新入口。
- [刷新实现](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/refresh.ts)：结构层刷新及失败降级。
- [概念构建](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/context/build.ts)：摘要、节点合成、缓存。
- [符号说明维护](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/enrich.ts)：内容哈希、就绪与过期状态。
- [Changelog](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/CHANGELOG.md)：版本背景及解析限制补充。
- [检索排序](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/ask/ask.ts)：词项匹配、BM25、图排序及文件组织。
- [结构构建](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/build.ts)：解析缓存、哈希及关系构建。
- [关系解析](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/resolve.ts)：作用域、导入、类型线索及未解析关系。
- [变化指纹](https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/src/graph/fingerprint.ts)：快速检查和哈希检查边界。

正文为原创归纳，未复制上游程序或素材。历史研究路径保存在本地子项目的 notes/related-research.md。关键源码核对不等于全仓审计；未运行上游、未测节省率，也未宣称安装接入完成。
