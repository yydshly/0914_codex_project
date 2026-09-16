"""Build a source-grounded, editable overview of MiroFish capabilities."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
W, H = 1800, 2480
INK, MUTED, ACCENT = '#202944', '#667089', '#4255c4'
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
 '<title id="title">MiroFish 能力全景：场景、输入、内部原理、输出与价值边界</title>',
 '<desc id="desc">多智能体社会模拟应用。资料与问题经过文档解析、知识图谱、角色与环境配置，进入模型决策和 OASIS 环境执行的多轮循环，最终呈现关系图、角色档案、互动记录、状态、报告和对话。官方案例包括舆情和红楼梦；市场调研等为可设计用途。模拟不等于真实调研或已验证预测。</desc>',
 '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#6475cd"/></marker><marker id="light" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#7764c5"/></marker></defs>',
 '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC","Segoe UI",sans-serif}a:hover text{text-decoration:underline}</style>',
 f'<rect width="{W}" height="{H}" fill="#fafaff"/>']

def rect(x,y,w,h,fill='#fff',stroke='#dce0ef',r=6):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')

def txt(x,y,s,size=24,color=INK,weight=400,maxw=None):
    maxw = maxw if maxw is not None else W-x-48
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" data-max-width="{maxw}">{escape(s)}</text>')

def lines(x,y,items,size=23,color=MUTED,gap=35,maxw=None):
    for i,s in enumerate(items): txt(x,y+gap*i,s,size,color,maxw=maxw)

def arrow(x1,y1,x2,y2,light=False):
    col,mark=('#7764c5','light') if light else ('#6475cd','arrow')
    parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{col}" stroke-width="2.5" marker-end="url(#{mark})"/>')

def section(y,n,title,sub):
    rect(48,y-28,40,36,'#e6eafa','#e6eafa',3)
    txt(54,y-2,n,22,ACCENT,700,30)
    txt(104,y,title,30,INK,700)
    txt(520,y-1,sub,22,MUTED)

rect(48,18,1704,4,ACCENT,ACCENT,0)
txt(48,53,'MIROFISH  /  CAPABILITY MAP',21,ACCENT,700)
txt(1510,53,'研究图解 / 009',21,MUTED,600,240)
txt(48,118,'从一份资料，到一群角色的可能反应',49,INK,700)
txt(50,166,'多智能体社会模拟应用  ·  用知识图谱组织背景，用大模型驱动角色，用仿真环境承接行动',26,MUTED)

section(222,'01','可以用在哪些场景？','前两项有官方演示；后三项是基于机制可设计的用途，效果需验证')
cases=[
 ('舆情与公关','官方演示',['事件材料 + 公开反馈','模拟公告后的各方反应','观察争议与信息传播']),
 ('故事后续推演','官方演示',['已有章节 + 人物关系','探索人物选择与冲突','示例：《红楼梦》前 80 回']),
 ('市场调研辅助','可设计用途',['产品资料 + 客户访谈','探索需求、顾虑与拒绝理由','形成待真人验证的假设']),
 ('产品与价格评审','可设计用途',['功能 / 定价方案 + 反馈','观察各类用户的潜在反应','发现解释缺口与改进线索']),
 ('规则与政策讨论','可设计用途',['规则草案 + 各方约束','探索群体冲突与适应行为','寻找可能遗漏的利益诉求'])]
for i,(title,tag,body) in enumerate(cases):
    x=48+i*344
    rect(x,248,328,200)
    rect(x+20,248,48,4,ACCENT if i<2 else '#8860b8',ACCENT if i<2 else '#8860b8',0)
    txt(x+20,283,tag,19,ACCENT if i<2 else '#7652aa',600,288)
    txt(x+20,324,title,27,INK,700,288)
    lines(x+20,361,body,20,gap=30,maxw=288)

section(505,'02','输入什么？','标准入口：上传背景资料，再用自然语言描述要探索的问题')
inputs=[
 ('A  背景资料',['新闻、事件时间线、报告、公开评论','产品说明、客户访谈、竞品资料','小说章节、人物小传、关系与世界设定'],
  '文件：PDF / TXT / Markdown'),
 ('B  明确的问题',['“发布这份回应，各方会如何反应？”','“新价格可能引起哪些购买顾虑？”','“这个秘密公开后，人物会如何选择？”'],
  '写清事件、对象与要观察的变化'),
 ('C  情境与约束',['在资料或需求中说明时间点与已知事实','说明谁知道什么、各方目标与限制','比较方案时分别运行，控制其余条件'],
  '资料缺口可能被模型补全，需人工检查')]
for i,(title,body,foot) in enumerate(inputs):
    x=48+i*573
    rect(x,533,558,198)
    txt(x+22,573,title,27,INK,700,514)
    lines(x+22,611,body,22,gap=32,maxw=514)
    txt(x+22,708,foot,20,ACCENT,600,514)

section(788,'03','内部怎样处理？','把“背景关系”转换为“角色行动”，再由行动结果进入下一轮')
rect(48,816,1704,750,'#eceefa','#eceefa',20)
txt(76,852,'准备阶段  /  从材料建立模拟起点',21,'#654aa2',600)
pre=[
 ('1  文档解析',['提取文本，整理输入内容','材料是角色与推演的背景依据']),
 ('2  图谱与记忆 · Zep',['抽取实体、关系，建立可检索背景','支持 GraphRAG 与时序记忆']),
 ('3  角色与环境配置 · LLM',['生成简介、人设、立场等角色设定','配置活跃度、时长、初始帖子等'])]
for i,(title,body) in enumerate(pre):
    x=76+i*554
    rect(x,876,518,143,'#ffffff','#d3d9ec',12)
    txt(x+20,914,title,26,'#202944',700,478)
    lines(x+20,956,body,22,'#596780',gap=33,maxw=478)
    if i<2:arrow(x+525,948,x+545,948,True)
parts.append('<path d="M1445 1022 V1041 H614 V1058" fill="none" stroke="#7764c5" stroke-width="2.5" marker-end="url(#light)"/>')
rect(76,1070,1074,327,'#f6f7ff','#cfd5eb',12)
txt(98,1106,'多轮互动循环  /  活跃角色按当前可见信息行动',25,'#202944',700)
loop=[('观察','角色背景与记忆','当前可见帖子 / 环境信息'),('决策 · 大模型','人设 + 上下文 → 选择行动','同一模型可驱动多个角色'),('执行 · OASIS','发帖、评论、转发等','也可以不行动')]
for i,(title,a,b) in enumerate(loop):
    x=98+i*346
    rect(x,1133,311,131,'#e5eafa','#e5eafa',10)
    txt(x+17,1170,title,26,ACCENT,700,277)
    lines(x+17,1209,[a,b],20,INK,gap=30,maxw=277)
    if i<2:arrow(x+317,1198,x+337,1198,True)
txt(115,1338,'共享环境保存行动结果；可用信息与记忆更新 → 其他角色在后续轮次观察',23,'#52617a',maxw=1000)
parts.append('<path d="M1049 1271 V1300 H252 V1274" fill="none" stroke="#7764c5" stroke-width="2.5" marker-end="url(#light)"/>')
txt(416,1375,'不是每人都发言，也不是所有角色都知道一切',21,'#654aa2',600,690)

rect(1174,1070,550,468,'#ffffff','#d3d9ec',12)
txt(1196,1110,'几个容易混淆的分工',26,'#202944',700,506)
lines(1196,1153,['角色 = 档案 / 人设 + 上下文 + 可用动作','大模型：生成设定、选择行动、分析结果','OASIS：执行动作，管理虚拟社交环境','Zep：组织知识关系与记忆检索','MiroFish：编排流程，提供网页与接口'],22,'#596780',gap=38,maxw=506)
rect(1196,1340,506,171,'#f0edfa','#d9d0ed',10)
lines(1212,1373,['多个 Agent ≠ 必须使用多种模型','角色定制 ≠ 为每个角色训练模型','社交模拟 ≠ 完整的现实 / 剧情引擎','报告通常负责事后分析，不是剧情导演'],21,'#614888',gap=36,maxw=474)

arrow(613,1400,613,1417,True)
rect(76,1426,1074,112,'#e5eafa','#e5eafa',12)
txt(98,1465,'模拟后的分析 · ReportAgent',28,ACCENT,700)
txt(98,1507,'检索模拟信息 / 调用工具 / 采访角色 → 生成报告，并支持后续追问',24,INK,maxw=1030)
arrow(900,1569,900,1589)

section(1630,'04','最终看到什么？','原版是图谱 + 记录 + 报告 + 对话的组合，图不是唯一输出')
outputs=[
 ('关系图谱','图形节点与连线',['看人物、组织、事件之间的关联','用于理解背景，不直接证明因果']),
 ('角色档案','人设与配置详情',['看每个角色的背景、立场和设定','用于检查角色是否偏离资料']),
 ('互动记录','时间线 / 动作列表',['看谁在何时发帖、评论或转发','用于追踪讨论过程与信息变化']),
 ('运行状态','进度与动作计数',['看轮次进展、平台状态和动作数量','用于监控运行，不代表预测准确率']),
 ('分析报告','按章节组织的文字报告',['阅读模拟现象、解释和推演结论','可回到记录核查，不是确定的未来']),
 ('深度互动','角色聊天 / 报告问答',['问角色为什么这样回应','问报告依据是什么、还有什么遗漏'])]
for i,(title,form,body) in enumerate(outputs):
    x=48+(i%3)*573; y=1660+(i//3)*178
    rect(x,y,558,159)
    rect(x,y+20,3,35,ACCENT,ACCENT,0)
    txt(x+22,y+39,title,28,INK,700,245)
    txt(x+262,y+37,form,20,ACCENT,600,274)
    lines(x+22,y+85,body,23,gap=35,maxw=514)

section(2056,'05','怎样理解它的价值？','用模拟形成可检查的假设，再回到现实验证')
rect(48,2085,832,215,'#edf0fc','#d2d9f2')
txt(72,2127,'能帮助你做的事',28,ACCENT,700)
lines(72,2171,['发现被遗漏的群体、顾虑和沟通缺口；探索可能的反应路径。','设计不同方案的模拟，形成访谈问题、评审线索与创作方向。','知识库侧重“资料说了什么”；它进一步探索“角色可能怎么做”。'],23,INK,gap=39,maxw=784)
rect(902,2085,850,215,'#f5effa','#e0d4eb')
txt(926,2127,'不能由模拟直接推出的结论',28,'#75519a',700)
lines(926,2171,['模拟客户不等于真实市场样本，角色数量不等于代表性。','舆情推演不等于全网实时监测；故事推演不保证成稿小说。','反复出现的结果不自动等于现实概率，准确性需对照验证。'],23,'#695976',gap=39,maxw=802)

txt(48,2344,'运行依赖：MiroFish 前端与 Python 后端 + 大模型 API + Zep 服务；仿真引擎采用 OASIS。',23,MUTED)
txt(48,2382,'源码能力归纳，非本次实测输出。固定版本 39d849138ef2 · 查阅 2026-09-16 · 本地演示发言为预设教学内容。',21,MUTED)
base='https://github.com/666ghj/MiroFish/blob/39d849138ef254f6c737ab4c4705e5545dbe31d4/'
links=[('官方说明与案例','README-ZH.md'),('角色与配置','backend/app/services/oasis_profile_generator.py'),('仿真执行','backend/scripts/run_parallel_simulation.py'),('报告与对话界面','frontend/src/components/Step5Interaction.vue')]
for i,(label,path) in enumerate(links):
    parts.append(f'<a href="{base+path}" target="_blank" rel="noopener">')
    txt(48+i*420,2428,label+' ↗',21,ACCENT,600,390)
    parts.append('</a>')
parts.append('</svg>')
(ROOT/'assets'/'mirofish-capabilities.svg').write_text('\n'.join(parts),encoding='utf-8')
print('Created assets/mirofish-capabilities.svg (1800 × 2480)')
