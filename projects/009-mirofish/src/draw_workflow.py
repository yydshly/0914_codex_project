"""Create an editable mechanism diagram grounded in the pinned upstream source."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
W, H = 1600, 1830
INK, MUTED, ACCENT = '#202944', '#667089', '#4255c4'
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
         '<title id="title">MiroFish：从使用场景、资料和角色定制，到多智能体互动与输出</title>',
         '<desc id="desc">部署网页和后端，配置模型与 Zep。用户输入资料和问题；系统抽取实体关系，生成角色档案与环境配置；OASIS 调度多个角色观察、行动和更新上下文；最后输出互动记录、分析报告与角色访谈。同一模型可以驱动多个角色，不需要为角色训练新模型。结论需人工和现实验证。</desc>',
         '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L8 4.5 L0 9" fill="none" stroke="#7782c0" stroke-width="1.5"/></marker></defs>',
         '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC","Segoe UI",sans-serif}</style>',
         f'<rect width="{W}" height="{H}" fill="#fafaff"/>']

def rect(x, y, w, h, fill='#fff', stroke='#dce0ef', radius=6):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

def text(x, y, value, size=24, color=INK, weight=400):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>')

def lines(x, y, values, size=23, color=MUTED, gap=35):
    for i, value in enumerate(values):
        text(x, y+i*gap, value, size, color)

def arrow(x1,y1,x2,y2):
    parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#7782c0" stroke-width="2.3" marker-end="url(#arrow)"/>')

def step(y, h, number, title, sub):
    rect(45,y,990,h)
    rect(65,y+21,48,40,'#e8ecfb','#e8ecfb',8)
    text(75,y+50,number,23,ACCENT,700)
    text(132,y+51,title,28,INK,700)
    text(132,y+83,sub,20,ACCENT)

rect(45,12,1510,4,ACCENT,ACCENT,0)
text(45,45,'MIROFISH / 多智能体社会推演',20,ACCENT,700)
text(45,103,'把资料变成角色，让角色互动，再分析过程。',42,INK,700)
text(45,144,'你提供问题与背景；系统组织“谁知道什么、关心什么、看见什么、接着做什么”。',25,MUTED)

cases=[('舆情与公关','公告可能引发哪些疑问？'),('产品与收费','不同用户在意什么变化？'),('规则与政策讨论','哪些群体的顾虑被遗漏？'),('故事与人物推演','人物动机会怎样碰撞？')]
for i,(title,body) in enumerate(cases):
    x=45+i*382
    rect(x,179,364,100,'#f0eff9','#dedcec')
    text(x+20,216,title,25,INK,700)
    text(x+20,253,body,21,MUTED)

rect(45,300,1510,138,'#eef0fb','#d8dcef')
text(69,336,'先搭运行环境',25,'#6548a5',700)
lines(69,375,['MiroFish 网页 + Python 后端','提供操作入口，编排各个步骤'],22,'#52617a',32)
lines(535,375,['大模型 API + Zep 服务','模型负责生成与判断，Zep 管理图谱与记忆'],22,'#52617a',32)
lines(1150,375,['OASIS 仿真引擎','提供虚拟社交环境'],22,'#52617a',32)

step(467,157,'01','你提供：背景资料 + 明确的问题','定制入口是“资料与需求”，而不只是随便给一个话题')
lines(76,581,['例：上传旧套餐、新方案、用户反馈；提出“改价可能引发哪些反应？”'],23)
text(76,608,'材料可以是 PDF / Markdown / TXT。资料越少，越容易依赖模型补全。',21,MUTED)
arrow(540,627,540,646)

step(653,157,'02','系统整理：人物、组织、事件与关系','从材料抽取实体，建立知识图谱，准备角色的背景依据')
lines(76,768,['例：产品团队 → 提供订阅 → 老用户；行业作者 → 传播信息 → 潜在用户'],22)
text(76,795,'关系图帮助组织背景，不等于已经知道真实的因果关系。',21,MUTED)
arrow(540,813,540,831)

step(839,238,'03','AI 定制：角色档案 + 环境参数','结合实体资料补充人设，再根据需求生成活动与情景配置')
roles=[('老用户','关注已有权益与长期承诺'),('企业采购','关注预算、续约与迁移'),('产品团队','解释变更与回应问题')]
for i,(title,body) in enumerate(roles):
    x=70+i*316
    rect(x,945,299,80,'#edf0fc','#d6def2',8)
    text(x+14,976,title,24,ACCENT,700)
    text(x+14,1007,body,20,MUTED)
text(76,1055,'同时生成：活跃程度、发言频率、初始帖子、模拟时长等。上方角色为机制示例。',21,MUTED)
arrow(540,1080,540,1098)

step(1106,255,'04','多个角色互动：观察 → 判断 → 行动 → 下一轮','在 Twitter / Reddit 风格的虚拟环境中，由 OASIS 调度')
loop=[('看到信息','背景 / 当前可见帖子'),('按角色判断','身份 + 目标 + 上下文'),('采取行动','发帖 / 评论 / 转发等')]
for i,(title,body) in enumerate(loop):
    x=70+i*316
    rect(x,1211,283,80,'#f6f7fc','#dbe0ee',8)
    text(x+14,1242,title,24,INK,700)
    text(x+14,1273,body,20,MUTED)
    if i<2: arrow(x+289,1251,x+310,1251)
text(76,1325,'保存动作记录，更新可用上下文与时序记忆，再进入下一轮。',22,ACCENT,600)
text(76,1350,'可以赞同、质疑、转述或不回应；不要求所有角色都辩论，也不要求同时发言。',20,MUTED)
arrow(540,1364,540,1382)

step(1390,192,'05','输出：互动记录 + 分析报告 + 可继续访谈的角色','ReportAgent 检索模拟信息、调用工具并可采访角色')
lines(76,1507,['你可以检查：谁提出什么问题 → 谁回应 → 哪些疑问仍未解决。',
                '你还可以追问角色、核对报告依据，形成待验证的风险与改进建议。'],23)

rect(1060,467,495,188)
text(1083,507,'只给一个问题就可以吗？',26,INK,700)
lines(1083,550,['标准路径是“材料 + 问题”。','从材料识别角色，再由模型补充设定。','仅凭话题构造角色，更容易脱离现实。'],22,gap=34)

rect(1060,677,495,250)
text(1083,719,'“定制身份”具体是什么？',26,INK,700)
lines(1083,763,['生成姓名 / 简介 / 背景 / 详细人设，','以及立场、活动频率等配置。','人设会进入角色提示词和上下文。'],22,gap=36)
rect(1080,865,455,43,'#eeeafa','#eeeafa',7)
text(1094,894,'这是配置角色，不是训练一个新模型。',21,ACCENT,700)

rect(1060,949,495,354)
text(1083,991,'需要多个不同的 AI 吗？',26,INK,700)
text(1083,1031,'需要多个 Agent，不必用多种大模型。',22,ACCENT,600)
rect(1179,1055,263,55,'#eef0fb','#d8dcef',8)
text(1201,1091,'同一个大模型 API',25,'#4255c4',700)
for x,title in [(1090,'角色 A'),(1247,'角色 B'),(1404,'角色 C')]:
    arrow(1310,1113,x+60,1140)
    rect(x,1148,126,49,'#eef0fc','#d2d9f2',7)
    text(x+21,1180,title,23,ACCENT,600)
lines(1083,1236,['同一模型，多次调用，不同人设与上下文。','代码也支持可选的第二套模型服务配置。'],21,gap=33)

rect(1060,1325,495,257)
text(1083,1367,'哪些工作仍然需要人？',26,INK,700)
lines(1083,1412,['提供可靠资料与明确问题；','检查角色是否遗漏、设定是否失真；','调整输入或配置后重新运行；','用真实访谈、数据和实验检验结论。'],22,gap=36)

rect(45,1611,1510,124,'#eceffa','#cdd6ed')
text(70,1654,'适合得到：可能的反应路径、分歧和遗漏问题，供方案评审与真实调研使用。',27,ACCENT,700)
text(70,1696,'多个角色可以共享同一个模型的偏差。模拟讨论、报告完整度与角色数量，都不能自动证明预测准确。',24,INK)
text(45,1775,'机制示意，非实际运行记录。依据固定版本 39d849138ef2：角色生成器、配置生成器、双平台脚本、ReportAgent。',19,MUTED)
text(45,1808,'本地展示中的案例发言仍为预设教学内容；这张图解释原版的构建与使用链路。',19,MUTED)
parts.append('</svg>')
(ROOT/'assets'/'mirofish-workflow.svg').write_text('\n'.join(parts),encoding='utf-8')
print('Created assets/mirofish-workflow.svg')
