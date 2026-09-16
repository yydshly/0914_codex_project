# 从教学展示到真实 MiroFish 运行

这是一份原版复现指南。本次未完成原版启动、API 调用或真实模拟。

## 环境与版本

上游说明要求 Node.js 18+、Python 3.11–3.12 和 uv。实际安装还应核对固定版本依赖文件。本展示只需 Python 3.10+ 构建，因此本页能运行不代表本机满足原版后端要求。

```powershell
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
git checkout 39d849138ef254f6c737ab4c4705e5545dbe31d4
Copy-Item .env.example .env
```

在自己的 `.env` 中配置 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL_NAME` 和 `ZEP_API_KEY`。不要将密钥放到前端展示页、文档或提交到仓库。所选模型需兼容项目使用的调用格式。

```powershell
npm run setup:all
npm run dev
```

按上游 README，前端默认 http://localhost:3000，后端默认 http://localhost:5001。也有 Docker 部署方式，见固定版本 README。

## 最小实验

1. 准备可公开的 PDF、Markdown 或 TXT 材料，明确时间、人物、组织与已知事实。
2. 提一个有边界的问题，例如“收费公告遗漏了哪些角色关心的问题”。
3. 检查图谱的遗漏、重复和错误实体，以及人设是否偏离资料。
4. 从少量角色和少量轮次开始。官方提醒消耗较大，建议先尝试少于 40 轮。
5. 保存输入、模型、参数、初始帖子、角色配置、动作日志、报告和访谈回答。
6. 检查报告引用，区分材料事实、模拟事件和报告推断。

这可以验证链路运行，不能证明预测准确。

## 验证实际价值

- 与同一模型直接分析资料比较，保持材料与预算可比。
- 使用事件发生前的资料，预测可核对的后续结果，避免答案泄露。
- 预先定义关注点覆盖率、错误陈述、无依据推断、评审质量、成本与耗时。
- 多次独立运行检查稳定性，不将模拟频率直接转换成现实概率。
- 通过真实访谈或实验分别测量理解程度、态度和实际行为。
- 记录社交平台结构、活动参数和人设抽样，并做敏感性分析。

数值销量、市场价格、事件概率需要额外数据、方法和校准；本次没有相应验证证据。

## 来源

- [固定版本中文 README](https://github.com/666ghj/MiroFish/blob/39d849138ef254f6c737ab4c4705e5545dbe31d4/README-ZH.md)
- [固定版本仿真脚本](https://github.com/666ghj/MiroFish/blob/39d849138ef254f6c737ab4c4705e5545dbe31d4/backend/scripts/run_parallel_simulation.py)
- [OASIS 上游](https://github.com/camel-ai/oasis)
