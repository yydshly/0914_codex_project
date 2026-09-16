# 能力与源码对应

版本固定为 `39d849138ef254f6c737ab4c4705e5545dbe31d4`。本次查阅源码，没有执行上游完整链路。

| 能力 | 固定版本文件 | 本展示对应 |
| --- | --- | --- |
| 文本提取 | `backend/app/utils/file_parser.py` | 资料文件名示意，未实现上传或解析 |
| 知识图谱 | `backend/app/services/graph_builder.py` | 六角色关系示意，非真实提取结果 |
| 角色设定 | `backend/app/services/oasis_profile_generator.py` | 预设动机、影响因素和证据需求 |
| 仿真配置 | `backend/app/services/simulation_config_generator.py` | 两种人工编写的情景分支 |
| 双平台模拟 | `backend/scripts/run_parallel_simulation.py` | 四轮预设事件回放，未启动 OASIS |
| 报告生成 | `backend/app/services/report_agent.py` | 预设观察、风险和验证建议，可导出 |
| 角色采访 | `run_parallel_simulation.py` 中 Interview 命令 | 18 个角色各有 3 个预设回答，非模型生成 |

## 已核对的实现细节

- `FileParser.SUPPORTED_EXTENSIONS` 包含 `.pdf`、`.md`、`.markdown`、`.txt`；不宣称支持 DOCX。
- 双平台脚本定义不同动作集。Twitter 包含发帖、点赞、转发、引用、关注等；Reddit 额外包含评论、踩、搜索、趋势和静音等。
- 双平台脚本支持模拟结束后保持环境，以及单个和批量角色采访。动作发生在仿真环境，不是在真实社交平台发布内容。
- ReportAgent 定义 `insight_forge`、`panorama_search`、`quick_search`、`interview_agents` 等工具。
- 配置生成代码包含 `narrative_direction` 和 `initial_posts`；`scheduled_events` 在查阅的事件解析路径中设为空列表。不能仅依据 README 的动态干预愿景，宣称已核实任意时刻注入任何变量的完整功能。
- 角色生成器支持区分个人与抽象群体实体；这些模型角色不能自动等同统计抽样得到的真人群体。

## 角色定制与模型数量

`OasisAgentProfile` 保存简介、详细人设、职业、兴趣等字段；Twitter 导出路径把 bio 与 persona 组合成 `user_char`，用于模型系统提示。配置生成器另生成活跃程度、立场、影响力、时长、初始帖子等仿真配置。这属于提示词、上下文与参数定制，不是为每个身份训练或微调新模型。

双平台脚本通过 `ModelFactory.create` 创建模型对象，分别把 `model` 传入 `generate_twitter_agent_graph` 和 `generate_reddit_agent_graph`。因此多个 Agent 可共用同一个模型配置；可选 `LLM_BOOST_*` 配置允许另一路模型服务用于并行平台。需要多角色与多次调用，不要求多个模型品牌或多个用户账户。

人设与上下文的分离不保证认知偏差独立。多个角色可能仍共享底层模型的知识与偏好。图解见 `assets/mirofish-workflow.svg`，可通过 `src/draw_workflow.py` 重新生成。

## 价值判断

值得探索的是利益相关者清单、公告盲点、传播分歧、调研提纲与人物动机一致性。课堂或团队讨论可用本展示先理解原理，再决定是否投入 API 成本进行真实运行。

多轮交互可能帮助呈现反馈过程，但本次没有与直接问模型做效果对照，不能宣称已测得增益。README 中的高保真、千人规模和预测万物属于项目主张，不能作为本子项目实测结论。

## 教学数据

三个案例均为原创虚构内容。每个案例有 6 个角色、2 种情景、每种情景 4 条事件与 1 份预设报告。访谈回答按角色固定，不随情景重新推理。角色间的虚线表示概念关联，不计算影响强度。

所有分支和回复均写在 `web/scenarios.js`。切换只读取对应数据；播放只改变步骤。页面不发送用户资料，不请求模型，也不将模拟频率当作现实发生概率。
