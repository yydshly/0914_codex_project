"""Chinese navigation for the pinned upstream specimens; names do not imply independent engines."""
ROWS = '''architecture|系统与工程|系统架构|组件怎样协作，数据如何流动|项目介绍、技术方案、系统总览
it-state|系统与工程|IT 现状|部门、遗留系统与现代化阶段|改造前的现状盘点
sequence|系统与工程|时序图|参与者按什么顺序交换消息|接口调用、认证、异常处理
sequence-oauth|扩展与表达|令牌刷新时序|请求遇到 401 后如何刷新与重试|带条件分支的时序示例，不是完整 OAuth 授权流程
state|系统与工程|状态机|哪些事件让对象切换状态|订单、审批、任务生命周期
er|系统与工程|实体关系|概念实体、字段与关系|业务数据模型
db-schema|系统与工程|数据库结构|物理表、类型、约束和外键|数据库设计与交接
dependency|系统与工程|依赖图|扇入、层级和循环依赖|模块依赖分析
deployment|系统与工程|部署图|软件运行在哪里|区域、主机、实例与边界
uml-class|系统与工程|UML 类图|类、操作与类型关系|软件对象设计
high-level|数据平台|平台总览|数据平台端到端的组成|平台汇报、全局架构
high-level-vertical|扩展与表达|平台总览 · 纵向|同一类平台内容的纵向排布|竖向阅读和长文
datalake|数据平台|数据湖|湖内存储、计算与访问层|数据平台分层说明
medallion|数据平台|分层数据存储|不同质量等级的数据怎样衔接|数据治理、分层加工
data-flow|数据平台|数据流|数据经过哪些角色和处理步骤|加工管道、责任分工
dp-integration|数据平台|平台集成|数据源、平台核心与消费者|集成方案
dp-security-matrix|数据平台|权限矩阵|角色对组件有什么访问权限|权限沟通与审核
flowchart|流程与组织|流程图|条件和分支决定下一步|业务逻辑、操作步骤
process|流程与组织|多角色过程|每一步由谁处理、输入输出是什么|跨部门交接、质量检查
swimlane|流程与组织|泳道图|流程如何跨越责任边界|协作流程、审批交接
org-chart|流程与组织|组织与路由|谁负责、向谁汇报或升级|组织关系、Agent 分工
tree|流程与组织|层级树|整体怎样拆成子项|功能拆解、结构目录
nested|流程与组织|嵌套关系|范围、容器与包含关系|权限范围、系统边界
layers|流程与组织|分层结构|抽象层、控制层的上下关系|技术栈、治理控制
loop|流程与组织|循环与飞轮|反馈怎样回流并积累状态|改进循环、共享记忆
timeline|产品与策略|时间线|关键事件发生的先后|发展历程、阶段计划
gantt|产品与策略|甘特图|任务的时间、阶段与重叠|项目计划、进度说明
quadrant|产品与策略|四象限|对象在两个维度上的位置|优先级、方案定位
wardley|产品与策略|Wardley 地图|价值链与组件演进阶段|自建采购讨论、战略分析
kanban|产品与策略|看板|工作处于什么状态|在制品、阻塞与阶段分布
journey|产品与策略|用户旅程|每个阶段的动作与感受|产品体验分析
story-map|产品与策略|用户故事地图|主干活动如何切成发布批次|需求规划、版本边界
fishbone|产品与策略|鱼骨图|哪些类别的原因共同影响结果|问题归因、复盘
venn|产品与策略|韦恩图|集合之间的交集|概念比较、能力边界
pyramid|产品与策略|金字塔与漏斗|层级或逐级流失|优先层次、转化说明
bar|数据比较|柱状图|不同类别的数量差异|指标对比
line|数据比较|折线图|连续时间上的变化|趋势讲解
scatter|数据比较|散点图|分布和变量关联|样本分布、相关性说明
treemap|数据比较|矩形树图|部分占整体的面积比例|组成结构
radar|数据比较|雷达图|多个维度的评分差异|能力画像、方案比较
polar|数据比较|极坐标图|周期类别的量级变化|循环周期中的比较
sankey|数据比较|桑基图|数量如何分流与汇合|流量、资源去向
waterfall|数据比较|瀑布图|正负贡献如何改变总量|预算、人员或指标增减
beeswarm|扩展与表达|蜂群图|每个样本在一维数轴的位置|分布展示，散点图的派生形式
bubble|扩展与表达|气泡图|位置和面积共同编码数值|三变量比较，散点图的派生形式
bump|扩展与表达|排名变化图|名次怎样随阶段变化|排名追踪，折线图的派生形式
ridgeline|扩展与表达|山脊图|多组分布的形状差异|分布比较，折线类扩展
slopegraph|扩展与表达|坡度图|两个时点之间的变化|前后比较，折线类扩展
tree-block-decomposition|扩展与表达|可追溯模块树|模块的输入、输出、约束和实现位置|结构化元数据与清单导出
quadrant-consultant|扩展与表达|四象限 · 情景矩阵|两个驱动因素组合成四种情景|战略讨论与情景规划
loop-terminal|扩展与表达|循环 · 终端风格|终端窗口中的循环解释|开发者内容；不走品牌配置体系
policy-trace-animated|动画与导入|策略轨迹动画|两条规则路径何时产生分歧|按步骤讲解规则执行
queue-animated|动画与导入|队列瓶颈动画|输入、等待和有限处理能力|排队与吞吐机制讲解
paved-road-animated|动画与导入|安全路径动画|允许路径、禁止入口与信任边界|部署和访问策略说明
import-drawio|动画与导入|draw.io 重绘示例|保留结构内容，重新组织画面|将已有技术草图用于文档
import-mermaid|动画与导入|Mermaid 重绘示例|从声明的节点关系重新排版|将文档中的图形用于展示
import-excalidraw|动画与导入|Excalidraw 重绘示例|从白板源文件整理出清晰关系|白板讨论成果整理'''

TYPE_GROUPS = [
    ('架构与部署', '系统由什么组成，组件如何连接，软件部署在哪里？', 'architecture it-state high-level deployment dp-integration'),
    ('流程与交互', '先做什么、怎样分支、谁与谁交互、状态如何变化？', 'flowchart sequence state swimlane process data-flow loop'),
    ('层级与组织', '整体如何分层、拆解、包含和分配责任？', 'nested tree org-chart layers medallion pyramid'),
    ('数据模型与依赖', '实体、表、类与模块之间有什么结构关系？', 'er db-schema uml-class dependency'),
    ('时间与工作规划', '何时发生、工作处于哪一步、怎样规划版本和体验？', 'timeline gantt kanban story-map journey'),
    ('策略与关系分析', '如何定位、归因、比较集合与检查权限？', 'quadrant wardley fishbone venn dp-security-matrix'),
    ('数值与统计', '数量、趋势、分布、比例与流量如何变化？', 'bar line scatter treemap radar polar sankey waterfall'),
]

# Base types follow the pinned SKILL.md selection table. Parent links are the
# study's navigation mapping, not a claim of an upstream renderer inheritance API.
EXTRAS = {
    'high-level-vertical': ('high-level', '派生示例'),
    'datalake': ('architecture', '派生示例'),
    'sequence-oauth': ('sequence', '派生示例'),
    'tree-block-decomposition': ('tree', '派生示例'),
    'quadrant-consultant': ('quadrant', '派生示例'),
    'loop-terminal': ('loop', '派生示例'),
    'beeswarm': ('scatter', '派生示例'),
    'bubble': ('scatter', '派生示例'),
    'bump': ('line', '派生示例'),
    'ridgeline': ('line', '派生示例'),
    'slopegraph': ('line', '派生示例'),
    'policy-trace-animated': ('flowchart', '动画演示'),
    'queue-animated': ('data-flow', '动画演示'),
    'paved-road-animated': ('architecture', '动画演示'),
    'import-drawio': ('architecture', '导入重绘'),
    'import-mermaid': ('flowchart', '导入重绘'),
    'import-excalidraw': ('flowchart', '导入重绘'),
}

def rows():
    items=[dict(zip(('id','domain','name','question','use'), line.split('|'))) for line in ROWS.splitlines()]
    base={key:category for category,_,keys in TYPE_GROUPS for key in keys.split()}
    names={item['id']:item['name'] for item in items}
    assert len(base)==40 and len(EXTRAS)==17 and set(base).isdisjoint(EXTRAS)
    assert set(names)==set(base)|set(EXTRAS)
    for item in items:
        parent,kind=EXTRAS.get(item['id'],(item['id'],'基础图型'))
        item.update(category=base[parent],kind=kind,family=parent,familyName=names[parent])
    return items
