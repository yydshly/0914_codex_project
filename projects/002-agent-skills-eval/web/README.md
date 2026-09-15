# Skill 评测实验室 · 网页演示

中文交互式研究页，提供三个场景、工作原理和实验结论。纯静态 HTML/CSS/JavaScript，无依赖，不调用模型或业务接口。

**[在线访问：Skill 评测实验室](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/)** · [所有已发布演示](https://yydshly.github.io/0914_codex_project/)

## 本地打开

在本目录运行：

```powershell
node serve.mjs
```

打开终端显示的 Local 地址。服务器只绑定本机地址，端口自动分配；关闭进程后地址失效。建议通过 HTTP 打开，以便“实验结论”读取 JSON 记录。

## 演示内容

1. **退款客服**：六种常见任务，支持修改天数、拆封、质量问题和照片条件；左右对照预设回答，并展开四条评分依据。
2. **数据分析**：重放已验证的 E01/E02，切换附件是否对称，观察虚假增益如何产生和消失。
3. **工具调用**：修改工具名称、城市和次数，观察确定性断言；强调请求提出与执行成功的区别。
4. **能力与流程（默认入口）**：区分库外的范围确定、场景与测试设计、Skill 编写，库内的自动运行与评分，以及人工复核；用退款信息缺失案例串起整个流程。
5. **实验结论**：读取真实离线实验记录，提供原始 JSON、上游 HTML 报告和测试日志。

退款客服使用自拟政策与预设回答，基线刻意展示常见错误；该交互不是原库或真实模型的在线运行。工具场景用浏览器本地代码说明断言逻辑。页面显式标注这些边界，任何演示分数都不能当作真实模型提升率。

## 维护与验证

静态页面直接维护在 dist/；本目录 .gitignore 显式保留它，覆盖总仓库对生成目录的忽略规则。没有构建步骤。

```powershell
node --check dist/app.js
node --check dist/model.mjs
node check.mjs
```

check.mjs 校验退款边界、六个示例、数据对照和工具规则，以及证据文件与研究结果的一致性。本次没有执行浏览器截图或交互测试。

如果重新运行研究实验，请将上一级 artifacts/ 中的 experiment-results.json、mechanism-demo.html 和 upstream-tests.txt 同步到 dist/data/。

## 托管状态

已通过 GitHub Pages 发布。总仓库 `.github/workflows/pages.yml` 统一打包 `pages.json` 中选择的项目，把本目录 dist/ 放到站点的 002-agent-skills-eval/ 子目录。推送网页修改到 main 后会自动重新部署。所有资源使用相对地址、导航使用页面锚点，兼容子目录部署。

部署成功后，已验证线上入口、脚本、样式、引导图与实验数据内容和本地提交文件一致。GitHub 仓库保存源码；GitHub Pages 地址提供可实际打开的网页。`.openai/hosting.json` 保留静态目录说明，本项目当前使用 GitHub Pages 托管。

源码与证据基于研究版本 b60eebe；原库报告及源代码的许可见 [上游 MIT 许可证](../upstream/LICENSE)。
