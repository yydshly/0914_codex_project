# GitHub 项目研究集

记录值得研究的优秀 GitHub 项目：理解设计思路、复现关键能力、沉淀实践笔记，并按需提供 Web 演示。

这里是研究总仓库。每个子项目独立保存源码实验、研究记录和图片；本页提供摘要和有序入口。

## 项目索引

编号是永久标识；展示顺序由 `projects.json` 的 `order` 决定。调整顺序不需要重命名目录。

<!-- PROJECT_INDEX:START -->
| 顺序 | 编号 | 项目 | 源库 | 能力摘要 | 状态 | 演示 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 002 | [Agent Skills Eval：Skill 能力校验引擎](projects/002-agent-skills-eval/README.md) | [agent\-skills\-eval](https://github.com/darkrishabh/agent-skills-eval) | 读取已编写的 Skill 与测试标准，自动调用模型、评分并对比有无 Skill 的效果，为校验能力 Skill 提供底层评测引擎。 | 已完成 | [在线演示](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/) |
<!-- PROJECT_INDEX:END -->

## 项目预览

<!-- PROJECT_PREVIEWS:START -->
### 002 · Agent Skills Eval：Skill 能力校验引擎

读取已编写的 Skill 与测试标准，自动调用模型、评分并对比有无 Skill 的效果，为校验能力 Skill 提供底层评测引擎。

![Skill 能力校验闭环：用户与 AI 准备、评测引擎自动验证、人工复核后修改再测](projects/002-agent-skills-eval/assets/skill-validation-workflow.png)

[研究记录](projects/002-agent-skills-eval/README.md) · [上游仓库](https://github.com/darkrishabh/agent-skills-eval) · [在线演示](https://yydshly.github.io/0914_codex_project/002-agent-skills-eval/)

标签：Agent Skills / 自动评测 / LLM Judge / 可复现实验
<!-- PROJECT_PREVIEWS:END -->

## 开始研究

需要 Python 3.10 或更新版本，无第三方依赖。在仓库根目录运行：

```sh
python scripts/catalog.py add example-repo --name "示例项目" --repo "https://github.com/owner/example-repo" --summary "一句话说明值得研究的能力"
```

命令会分配下一个编号、创建研究目录、登记元信息并刷新首页。上述名称和地址仅为命令示例，请替换为真实项目。

1. 在新项目的 `README.md` 中填写研究目标、运行步骤和结论。
2. 在 `assets/` 放置截图，将相对仓库根目录的图片路径填入 `projects.json` 的 `cover`，并填写 `cover_alt`。
3. 修改摘要、状态、展示顺序或演示地址后，运行 `python scripts/catalog.py sync`。

## 仓库结构

```text
projects.json                 # 唯一项目登记表：编号、排序、摘要、图片、演示地址
projects/                     # 正式研究项目，使用 001-slug 格式
templates/project/            # 子项目模板，不占正式编号
docs/                         # 维护规范与部署说明
scripts/catalog.py            # 新建项目、生成首页、检查一致性
.github/workflows/check.yml   # 自动检查目录与首页索引
```

## 维护指南

- [项目组织与编号规则](docs/CONVENTIONS.md)
- [多个 Web 演示的部署约定](docs/DEPLOYMENT.md)
- [研究记录模板](templates/project/README.md)

## 来源与许可

各研究项目需注明上游仓库、研究版本及原始许可证。引入上游代码、图片或其他素材时保留其许可与署名；本仓库中的研究记录不改变上游项目的许可。
