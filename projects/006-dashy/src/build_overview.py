"""Create the editable, deterministic Chinese Dashy capability poster."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'dashy-capability-overview.svg'
W, H = 2400, 3300
navy, ink, muted = '#122c41', '#264457', '#647887'
teal, blue, amber, red = '#087e82', '#356dcc', '#a56913', '#aa4f49'
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Dashy 能力与实现全景图</title><desc>Dashy 的能力地图、配置驱动架构、NAS 示例、网页与桌面应用边界、部署扩展和验证范围。</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto-start-reverse"><path d="M0 1 L8 5 L0 9" fill="none" stroke="context-stroke" stroke-width="1.6"/></marker></defs>
<rect width="2400" height="3300" fill="#f6f8fa"/>
<g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">''']

def rect(x,y,w,h,fill='#fff',stroke='#dce5ec',r=22):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x,y,s,size=30,color=ink,weight=400):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>')

def lines(x,y,items,size=29,color=ink,gap=44):
    for i,s in enumerate(items): text(x,y+i*gap,s,size,color)

def path(d,color=blue,width=4,arrow=True):
    parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')

def section(n,title,y,sub=''):
    rect(96,y-39,65,54,navy,navy,14)
    text(109,y,n,30,'#fff',700)
    text(186,y,title,44,navy,700)
    if sub: text(2304-len(sub)*25,y-2,sub,25,muted)

# Header
rect(0,0,W,278,navy,navy,0)
text(96,123,'Dashy',100,'#fff',800)
text(459,119,'能力与实现全景图',73,'#fff',700)
text(101,183,'用网页构建桌面式工作台：统一入口、集中信息、组织交互',36,'#d6e8ee')
rect(96,213,698,44,'#255166','#255166',12)
text(120,245,'应用入口 + 动态看板 + 配置编辑',29,'#c7f4ef',700)
text(856,246,'桌面式体验 ≠ 操作系统桌面控制',30,'#ffdfa2',600)

# Capabilities
section('01','它提供什么',340,'原生功能与可选能力')
cards=[
('统一导航',['链接卡片 / 分组 / 多页面','图标与标签 / 多种打开方式'],teal),
('快速查找',['即时搜索 / 标签筛选 / 快捷键','外部搜索引擎 / 自定义搜索前缀'],teal),
('动态信息',['时钟、天气、RSS、日历','自托管服务数据 / 通用 API 组件'],blue),
('状态检查',['HTTP 响应与耗时 / ICMP Ping','按需启用 / 可配置检查间隔'],blue),
('工作视图',['普通首页 / 精简起始页','iframe 工作区 / 弹窗内嵌网页'],teal),
('个性化配置',['主题与 CSS / 布局、尺寸、排序','可视化编辑 / 原始配置编辑'],teal),
]
for i,(title,body,col) in enumerate(cards):
    x=96+(i%3)*744; y=376+(i//3)*178
    rect(x,y,720,158)
    rect(x+22,y+25,7,105,col,col,3)
    text(x+49,y+48,title,35,col,700)
    lines(x+49,y+94,body,29,gap=40)
text(98,756,'还支持：多语言 · 响应式界面 · 可选 PWA 基础离线访问',29,muted)
text(98,798,'边界：页面轮询不能等同于独立运行的全天候监控与告警系统。',28,amber)

# Architecture
section('02','它怎样实现',867,'配置驱动界面，接口连接数据')
rect(96,906,540,226,'#eef7f7','#bfdcdd')
text(124,954,'配置与偏好',37,teal,700)
lines(124,1004,['conf.yml','页面 / 分组 / 链接 / 组件','localStorage：浏览器偏好'],29,gap=46)
rect(838,906,640,226,'#edf3fe','#c8d7f3')
text(870,954,'浏览器中的 Dashy',37,blue,700)
lines(870,1004,['Vue 3 + Vuex + Vue Router','生成界面 / 搜索过滤 / 响应点击','编辑数据 / 组件刷新 / 链接跳转'],29,gap=46)
rect(1680,906,624,150)
text(1712,953,'目标应用网页',36,navy,700)
lines(1712,996,['新标签页 / 当前页','对方允许时，用 iframe 嵌入'],28,gap=37)
rect(1680,1102,624,256)
text(1712,1152,'外部服务与数据',36,blue,700)
lines(1712,1200,['天气 / NAS / Nextcloud','Pi-hole / Proxmox / 其他 API','目标系统负责实际业务与权限'],29,gap=49)
rect(838,1190,640,168,'#eef7f7','#bfdcdd')
text(870,1239,'Node.js + Express',37,teal,700)
lines(870,1284,['HTTP / Ping 探测 · CORS 代理','配置写盘 · 系统信息'],29,gap=43)
path('M 636 1024 L 824 1024',teal)
text(653,985,'读取 / 解析',24,teal)
text(673,1072,'合并偏好',24,teal)
path('M 1478 974 L 1666 974',blue)
text(1518,947,'打开网址',24,blue)
path('M 1478 1083 L 1579 1083 L 1579 1168 L 1666 1168',blue)
text(1509,1058,'组件请求 API',22,blue)
path('M 1158 1132 L 1158 1176',teal)
text(1192,1171,'需要后端能力',23,teal)
path('M 1478 1297 L 1666 1297',teal)
text(1504,1269,'探测 / 代理',23,teal)
path('M 838 1278 L 366 1278 L 366 1146',teal)
text(432,1247,'写回 YAML 配置',28,teal,600)
text(100,1409,'保存到本地 → 当前浏览器 localStorage',28,ink)
text(1000,1409,'保存到磁盘 → 后端接口 → 服务器 YAML',28,ink)
text(100,1453,'Vite 负责构建；核心配置通常不需要数据库。Dashy 组织入口与展示，业务由原应用提供。',28,muted)

# Concrete example
section('03','用一个 NAS 例子看懂',1540)
examples=[('点击 NAS 卡片','打开 NAS 自己的管理网页'),('状态灯变绿','探测地址得到正常响应'),('显示剩余容量','组件通过 NAS API 读取'),('上传或删除文件','由 NAS 页面或专门接口执行')]
for i,(a,b) in enumerate(examples):
    x=96+(i%2)*1128;y=1580+(i//2)*105
    rect(x,y,1080,87)
    text(x+26,y+52,a,31,navy,700)
    path(f'M {x+326} {y+43} L {x+402} {y+43}',teal,3)
    text(x+430,y+52,b,29)
text(100,1814,'只添加一个网址，不会自动获得 NAS 的文件管理权限。',29,amber,600)

# Boundary table
section('04','网页产品与桌面软件，支持到哪里',1900)
rect(96,1935,2208,439,'#fff','#dce5ec',18)
rect(96,1935,2208,64,'#e8eef4','#e8eef4',18)
text(128,1978,'目标',30,navy,700)
text(767,1978,'支持方式 / 边界',30,navy,700)
rows=[
('● 原生','网页应用','链接打开；对方允许时可嵌入',teal),
('● 条件','桌面应用启动','专用协议链接 + 已安装 + 浏览器允许',amber),
('● 扩展','桌面应用窗口嵌入','不原生支持；无法直接把本机软件窗口放进 iframe',red),
('● 扩展','直接执行 .exe / 命令','不原生支持；需额外本地桥接程序',red),
('● 扩展','软件控制与自动化','不原生支持；需另接应用 API 或自动化工具',red),
]
for i,(badge,a,b,col) in enumerate(rows):
    y=1999+i*75
    if i%2==1: rect(98,y,2204,75,'#f8fafc','#f8fafc',0)
    text(128,y+49,badge,27,col,600)
    text(309,y+49,a,30,navy,600)
    text(767,y+49,b,29)
text(100,2416,'专用链接由浏览器与操作系统唤起应用，桌面软件仍在独立窗口中运行。',28,muted)

# Integration, access, deployment
section('05','扩展、认证与部署',2502)
details=[
('接入外部服务',['现成组件：配置地址与密钥','通用 API / iframe：对接更多内容','自定义 Vue 组件：扩展展示与交互','数据刷新需要可访问的数据源'],blue),
('账号与配置',['内置账号 / OIDC / Keycloak','代理认证 / 角色与编辑权限','导入导出 / 可选 REST 配置 API','可选加密备份与恢复'],teal),
('部署方式',['Docker / Node.js 自托管','纯静态托管仅覆盖部分能力','探测、代理、写盘需要服务端','PWA 离线不等于外部服务可用'],navy),
]
for i,(title,body,col) in enumerate(details):
    x=96+i*744
    rect(x,2540,720,253)
    text(x+28,2591,title,35,col,700)
    lines(x+28,2639,body,28,gap=41)
rect(96,2820,2208,109,'#fff3df','#eed8b2',18)
text(123,2862,'目标服务仍有自己的权限；Dashy 登录不会自动登录所有应用。',29,amber,600)
text(123,2902,'认证的保护范围取决于配置；跨域、嵌入策略、网络可达性与 API 权限都会影响接入效果。',27,amber)

# Evidence and footer
section('06','我们已经验证了什么',3007)
text(100,3053,'已验证：搜索过滤 · 时钟与本机数据刷新 · HTTP 状态变化 · 编辑表单 · iframe 工作区',29,teal,600)
text(100,3097,'演示中的状态切换按钮为额外编写；Dashy 原生负责嵌入面板、探测并显示状态。',28,ink)
text(100,3139,'未完整实测：外部账号接入、认证、云备份、配置写盘、桌面软件唤起。',27,muted)
rect(0,3180,W,120,navy,navy,0)
text(96,3229,'适合：个人起始页 · 家庭服务器门户 · 团队工具导航 · 轻量信息总览',34,'#fff',600)
text(96,3272,'依据：Dashy 4.6.14 源码、官方文档与本机演示  |  github.com/Lissy93/dashy  |  2026-09-16',25,'#c6d8e2')
parts.append('</g></svg>')
OUT.write_text('\n'.join(parts),encoding='utf-8')
print(OUT)
