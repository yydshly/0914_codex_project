# 校验能力流程图生成记录

交付图片：[完整流程图](../assets/skill-validation-workflow.png)。使用内置 image_gen 生成，并进行一次定向编辑，修正第三阶段多余字符及反馈箭头的起点。图中“可封装的校验 Skill”是建议的组合方式，不表示上游已经提供该封装。

## 初始提示词

Create ONE polished Chinese educational infographic, a complete workflow diagram for agent-skills-eval. High resolution landscape approximately 3:2, clear typography, white background, navy #182d52 text, blue #335deb for the library's actual scope, restrained amber for human preparation, green for review. Flat diagram, precise arrows, generous whitespace, no people or decorations, no fake logos. All text is simplified Chinese and must be legible and accurate. This is a technical explanatory diagram, not a webpage screenshot.

Main title exactly: "如何实现一个“校验能力”的 Skill？"
Subtitle exactly: "agent-skills-eval 提供自动评测引擎，可作为校验 Skill 的底层工具"

The diagram has THREE clear horizontal zones stacked vertically, with connected numbered steps. Top zone labeled "① 准备阶段｜用户与 AI 协作，库外完成". Four equal compact boxes from left to right with arrows:
"明确能力范围" with small subtext "用户：要做什么、不能做什么"
"分析业务场景" with subtext "用户 / AI：正常、异常、边界情况"
"设计并确认测试" with subtext "用户 / AI 起草；用户确认题目和标准"
"编写待测 Skill" with subtext "用户 / AI：写出工作步骤"
Under this row a short note: "测试设计与 Skill 编写可以交替进行；评测前两者都需准备好。"

Middle zone is the most prominent BLUE outlined container labeled "② 自动验证｜agent-skills-eval 的实际能力". Left small input stack labeled "输入" with three chips: "待测 SKILL.md", "测试任务与数据", "预期结果 / 评分标准".
From that stack arrows into a central two-branch model diagram, top branch "加载 Skill → 目标模型 → 回答 A", bottom branch "不加载 Skill → 同一目标模型 → 回答 B". Clearly mark below "开启基线对照时运行两组".
Both branches connect to a scoring box labeled "按既定标准检查" with two lines "语义要求 → AI 裁判" and "工具名称 / 参数 / 次数 → 程序".
Then arrow into output report box labeled "输出评测报告" with small lines "逐条通过 / 失败及依据" and "对比质量、耗时与 Token".
At bottom inside blue container short important note exactly: "对照需保持任务数据一致；当前版本的附件加载存在两组不对称问题。"

Bottom zone labeled "③ 复核与迭代｜用户决定如何改进". Arrow from report into "人工复核" → "修改 Skill 或测试" → "再次运行评测". A clear feedback arrow loops from rerun toward blue container input, labelled "重复验证". Below this zone place a small narrow example ribbon:
"退款示例：未提供收货日期 → 标准要求先追问 → 若直接答“可以退款”，应判失败"
No fabricated performance percentages.

Finally a visually distinct but short bottom caption, font large enough to read:
"可封装的校验 Skill = 校验流程说明 + 调用评测引擎 + 汇总结果"
And second caption smaller: "仓库本身是评测程序；不内置需求分析、场景生成、测试设计或自动改写 Skill。"
Ensure the optional wrapping caption is clearly a possible architecture, not a claim that the repo already ships a complete validation Skill. Keep exactly one complete image, no multiple panels of alternative designs.

## 定向编辑

保留内容与布局，删除绿色第三阶段标题中多余的“三”字样；将蓝色反馈线起点从“人工复核”调整到“再次运行评测”，沿三个框的下方返回“输入”，保留人工复核→修改 Skill 或测试→再次运行评测的正向箭头。
