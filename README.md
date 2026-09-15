# GitHub 项目研究集

记录值得研究的优秀 GitHub 项目：理解设计思路、复现关键能力、沉淀实践笔记，并按需提供 Web 演示。

这里是研究总仓库。每个子项目独立保存源码实验、研究记录和图片；本页提供摘要和有序入口。

## 项目索引

编号是永久标识；展示顺序由 `projects.json` 的 `order` 决定。调整顺序不需要重命名目录。

<!-- PROJECT_INDEX:START -->
暂无研究项目。添加首个项目后，这里会自动生成有序索引。
<!-- PROJECT_INDEX:END -->

## 项目预览

<!-- PROJECT_PREVIEWS:START -->
待添加项目摘要和截图。
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
