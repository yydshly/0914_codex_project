"""Render the research synthesis as a high-resolution PNG and editable SVG."""
from pathlib import Path
from html import escape
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 2400, 4310
BG, INK, MUTED = '#f3f6fb', '#142237', '#53647a'
BLUE, TEAL, PURPLE, ORANGE = '#1739d2', '#087975', '#7144a5', '#a34b20'
WHITE, LINE = '#ffffff', '#d7e0ed'
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">Future AGI：从运行证据到质量改进的技术原理总览</title>',
       '<desc id="desc">汇总业务输入、请求与遥测两条路径、七类分析手段、组合评分、错误定位与聚类、提示词优化及独立验证；区分源码证据、文档能力和实际运行效果。</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc', size)

def box(x, y, w, h, fill=WHITE, stroke=LINE, r=18):
    d.rounded_rectangle((x, y, x+w, y+h), radius=r, fill=fill, outline=stroke, width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x, y, value, size=32, color=INK, bold=False, width=None):
    length = d.textlength(value, font=font(size, bold))
    if x+length > W-35 or (width is not None and length > width):
        raise ValueError(f'Text overflow: {value}')
    d.text((x, y), value, font=font(size, bold), fill=color, anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')

def para(x, y, value, width, size=30, color=MUTED, bold=False, leading=46, bottom=None):
    lines = []
    for paragraph in value.split('\n'):
        line = ''
        for char in paragraph:
            if line and d.textlength(line+char, font=font(size, bold)) > width:
                lines.append(line)
                line = char
            else:
                line += char
        lines.append(line)
    if bottom is not None and y+(len(lines)-1)*leading+size > bottom:
        raise ValueError(f'Panel overflow: {value}')
    for i, line in enumerate(lines):
        text(x, y+i*leading, line, size, color, bold, width)
    return y+len(lines)*leading

def arrow(x1, y1, x2, y2, color=BLUE):
    d.line((x1, y1, x2, y2), fill=color, width=4)
    angle = math.atan2(y2-y1, x2-x1)
    pts = [(x2,y2), (x2-18*math.cos(angle-.45),y2-18*math.sin(angle-.45)),
           (x2-18*math.cos(angle+.45),y2-18*math.sin(angle+.45))]
    d.polygon(pts, fill=color)
    svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="4"/><polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')

def heading(y, number, title, hint, color=BLUE):
    text(100, y, number, 36, color, True)
    text(185, y-2, title, 43, INK, True)
    if hint:
        text(185, y+60, hint, 29, MUTED)

# Meaning: observation and evaluation are distinct operations.
box(0, 0, W, 325, INK, INK, 0)
text(100, 40, 'FUTURE AGI  /  能力 × 技术原理', 31, '#aabaff', True)
text(100, 102, '检测 AI 的能力与表现：记录、评测、诊断', 60, WHITE, True, 2200)
text(104, 193, '对象是 AI 应用：模型 + 提示词 + 知识检索 + 工具；观察可见执行过程，不读取模型内部思维。', 32, '#d7e0f6')
text(104, 259, '主线：采集证据 → 多种方法评测 → 诊断与归类 → 修改 / 优化 → 固定样本复测', 34, WHITE, True)

heading(375, '01', '准备证据与标准', '记录本身不产生质量结论；判断需要业务标准和可核对的证据。')
inputs = [
    ('真实运行', '问题、回答、检索片段、工具入参与结果\nSpan 耗时、Token、错误状态及成本信息'),
    ('数据集与人工标准', '上传样本 / 生产失败案例 / 参考答案\n业务规则、预期工具调用、人工认可的判断'),
    ('模拟用户 · Simulate', '场景 + 用户画像 → 多轮文本 / 语音对话\n生成测试材料，再交给同一套评测流程'),
]
for i, (title, body) in enumerate(inputs):
    x = 100+i*748
    box(x, 490, 704, 177)
    text(x+27, 514, title, 34, BLUE, True)
    para(x+27, 572, body, 650, 28, INK, leading=41, bottom=651)

heading(711, '02', '接入与存储：模型请求、运行记录是两条路径', '', TEAL)
box(100, 788, 2200, 400)
text(134, 820, '业务请求', 31, TEAL, True)
text(370, 817, '你的 AI 应用', 34, INK, True)
arrow(676, 839, 753, 839, TEAL)
text(790, 817, '可选 Go 模型网关', 34, INK, True)
arrow(1207, 839, 1290, 839, TEAL)
text(1330, 817, '模型服务', 34, INK, True)
text(1630, 821, '统一入口 / 路由 / 缓存 / 故障切换', 28, MUTED)
text(790, 873, '请求前后可配置 Guardrails：规则 / 检测器 → 阻断、脱敏或记录', 29, MUTED)
text(134, 948, '运行记录', 31, BLUE, True)
text(370, 945, 'SDK / traceAI 埋点', 33, INK, True)
arrow(702, 968, 776, 968)
text(805, 945, 'OpenTelemetry / OTLP', 32, INK, True)
arrow(1220, 968, 1286, 968)
text(1320, 945, 'fi-collector', 33, INK, True)
arrow(1570, 968, 1644, 968)
text(1680, 945, 'ClickHouse 分析', 33, INK, True)
text(370, 1001, 'Trace 串起一次任务；Span 记录模型、检索和工具步骤。采集器接收、批处理，再写入分析存储。', 30, MUTED)
box(132, 1074, 2136, 81, '#f0f5fb', '#f0f5fb', 10)
text(156, 1097, '平台支撑：React 展示 · Django 业务 · PostgreSQL 元数据 · Temporal 等任务组件 · 缓存 / 队列 / 对象存储', 28, INK)

arrow(1200, 1202, 1200, 1244)
heading(1270, '03', '核心：怎样从记录得到“好不好”的判断', '评测角度 = 正确性 / 有依据 / 安全 / 语气 / 工具使用；实现手段如下。')
text(185, 1380, '官方三种类型：Code Eval、LLM-as-Judge、Agent Evaluator；下面七项是研究归纳，非七种官方引擎。', 28, MUTED)

methods = [
    ('A  规则与函数检查', '字段 / 文本 / 数值 → 条件或函数 → 通过 / 失败',
     '正则、包含判断、JSON 合法性、数值条件。\n擅长明确要求；格式通过不代表事实正确。', BLUE),
    ('B  与参考答案或标注比较', '实际结果 + 标准参考 → 差异 / 命中 / 排名分数',
     'BLEU / ROUGE / 编辑距离；检索 Recall@K、MRR 等。\n依赖可信参考；文字重合度不等于语义正确。', BLUE),
    ('C  向量相似度', '文本 → Embedding 向量 → 余弦相似度 / 距离',
     '衡量语义接近，依赖嵌入模型。\n“7 天退款”和“30 天退款”可能相似，但事实不同。', BLUE),
    ('D  模型裁判 · LLM-as-Judge', '标准 + 回答 + 上下文 → 评测提示词 → 模型判断',
     '解析结构化分数、分类或理由；可加入示例校准。\n适合忠实性、语气等；有费用、波动与误判。', PURPLE),
    ('E  Agent 调查式评测〔文档〕', '待核实问题 → 多轮推理 / 工具查询 → 综合判断',
     '可补查政策、知识库等证据再下结论。\n依赖工具与资料；本次未独立核验完整实现。', PURPLE),
    ('F  工具调用匹配', '实际工具名与参数 对照 预期调用 → 匹配得分',
     '完整匹配 1；只匹配名称 0.5；未匹配 0。\n总分 ÷ 两边较大调用数；匹配不证明业务成功。', TEAL),
    ('G  执行轨迹匹配', '实际步骤序列 对照 预期轨迹 → 顺序 / 集合比较',
     '支持 strict、unordered、subset、superset 模式。\n查漏步骤、顺序与冗余；预期流程须符合业务。', TEAL),
    ('怎样组合使用？以退款为例', '格式规则 + 政策忠实性 + 工具匹配 + 结果一致性',
     '资料写 7 天，回答写 30 天：需要政策检查。\n退款接口失败却说成功：需核对真实工具结果。', ORANGE),
]
for i, (title, pipeline, body, color) in enumerate(methods):
    x, y = 100+(i%2)*1120, 1440+(i//2)*263
    box(x, y, 1080, 241)
    box(x, y, 8, 241, color, color, 2)
    text(x+30, y+25, title, 34, color, True, 1020)
    text(x+30, y+83, pipeline, 29, INK, True, 1020)
    para(x+30, y+137, body, 1020, 29, MUTED, leading=43, bottom=y+226)

arrow(1200, 2498, 1200, 2538)
heading(2564, '04', '结果与诊断：发现问题，还要知道问题集中在哪', '输出依评测器而异：分数 / 是否通过 / 分类 / 解释；诊断结论需要证据复核。')
diagnostics = [
    ('组合评分 · Composite', '子评分归一化 → 加权 / 平均 / 最小 / 最大 / 通过率。\n严重错误宜单设门槛，避免被平均分掩盖。', BLUE),
    ('错误定位 · Error Localization', '失败评测 + 标准 + 输入 → Agent 返回问题字段与分析。\n需启用；所读路径排除代码型与组合评测。', PURPLE),
    ('失败聚类 · 已评测结果', '失败描述 → 可选提炼 → 向量化 → 近邻中心归类。\n聚合相似问题，便于排查；相似不等于同一根因。', TEAL),
    ('主动扫描 · Error Feed〔云端 / 企业〕', '抽样 Trace → 分析潜在错误 → 汇总 Issue。\n可扫描尚未标为失败的记录；默认采样为 0。', ORANGE),
]
for i, (title, body, color) in enumerate(diagnostics):
    x, y = 100+(i%2)*1120, 2682+(i//2)*194
    box(x, y, 1080, 174)
    text(x+28, y+23, title, 32, color, True, 1024)
    para(x+28, y+78, body, 1024, 29, INK, leading=43, bottom=y+162)

arrow(1200, 3065, 1200, 3105)
heading(3130, '05', '从诊断回到改进：用相同标准比较新旧版本', '', BLUE)
box(100, 3210, 2200, 354, '#eaf0ff', '#c8d4fc')
text(140, 3242, '失败案例 → 数据集 → 人工修改 / 提示词优化 → 实验对比 → 独立样本验收', 40, BLUE, True, 2120)
text(142, 3317, '自动优化原理：生成候选提示词 / 示例配置 → 运行样本 → 评分 → 保留更好候选 → 反馈下一轮', 32, INK)
text(142, 3381, '六种搜索思路：Random / Bayesian / ProTeGi / Meta-Prompt / PromptWizard / GEPA', 32, INK)
text(142, 3442, '实验同时看质量、耗时、Token、费用与严重错误；生产统计帮助定位“错、慢、贵”。', 32, INK)
text(142, 3504, '验收后再投入使用，持续采集新记录。优化提示词不等于训练模型权重；部分平台优化实现依赖企业模块。', 29, ORANGE)

heading(3620, '06', '落地场景与适用边界', 'RAG：分开检查检索与生成  ·  客服 / Agent：核对执行与承诺  ·  版本升级：质量、成本、延迟回归')
box(100, 3740, 2200, 283)
limits = [
    ('记录边界', '只记录已接入的可见步骤。\n网关不能代替应用内部埋点。'),
    ('判断边界', '人工样本校准裁判与阈值。\n诊断推测、模拟行为均需复核。'),
    ('运行边界', '完整平台依赖多种基础服务。\n语音、模型、工具另有成本。'),
    ('许可与防护', '核心 Apache-2.0；ee/ 企业许可。\n规则防护不保证拦截未知变体。'),
]
for i, (title, body) in enumerate(limits):
    x = 134+i*545
    text(x, 3773, title, 34, BLUE, True)
    para(x, 3835, body, 502, 29, INK, leading=46, bottom=3966)

box(100, 4070, 2200, 160, INK, INK, 16)
text(134, 4097, '证据：固定源码 c02ffdd8（2026-09-15）+ 官方文档；研究整理于 2026-09-16。', 29, WHITE)
text(134, 4148, '当前为能力、检测方式与初步实现思路；根本原理需后期深入研究，实际检测效果尚未实测。', 28, '#c6d4ee')

OUT.mkdir(exist_ok=True)
im.save(OUT/'future-agi-technical-overview.png', optimize=True)
im.resize((1200, H//2), Image.Resampling.LANCZOS).save(OUT/'future-agi-technical-overview-preview.png', optimize=True)
(OUT/'future-agi-technical-overview.svg').write_text('\n'.join(svg+['</svg>']), encoding='utf-8')
print(f'Rendered {W} × {H} PNG, SVG and preview; text bounds checked.')
