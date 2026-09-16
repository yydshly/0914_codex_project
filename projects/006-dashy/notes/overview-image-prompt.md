# Dashy 总览图生成提示词

原计划：内置 image_gen，使用下列完整提示词尝试两次，两次均因网络错误失败，未获得图像输出。没有调用需要 API 密钥的 CLI 备选方式。

最终交付：程序绘制的可编辑 SVG，并使用 Sharp 导出 2400 × 3300 PNG；内容与布局源文件为 `../src/build_overview.py`，导出脚本为 `../src/render_overview.cjs`。最终稿另补入可选 REST 配置 API 与桌面唤起未实测的说明。

以下提示词保留为内容与视觉需求记录，不代表最终图片由图像模型生成。

```text
Use case: infographic-diagram.
Create ONE finished high-resolution Chinese educational infographic, intended as a complete reference poster for a GitHub project study. Requested canvas 3072 x 3840 pixels, portrait 4:5; maximize legibility. All Chinese text must be accurate and crisp, with a professional Chinese sans-serif typeface. Do not use a screenshot background. Use a polished editorial technical infographic style: warm off-white background, dark navy headings, teal for native capabilities, blue for integrations/data, amber for conditions and limits, thin clear arrows, small consistent vector-like icons. Dense but spacious enough to read, with a strong top-to-bottom hierarchy, clean alignment, no overlapping labels, no decorative filler. One integrated poster, not multiple separate images. The reader should understand both capabilities and boundaries without prior technical knowledge.
Title: “Dashy 能力与实现全景图”
Subtitle: “用网页构建桌面式工作台：统一入口、集中信息、组织交互”
Prominent thesis pill: “应用入口 + 动态看板 + 配置编辑”
Small secondary line: “桌面式体验 ≠ 操作系统桌面控制”

Compose the poster in six clearly numbered horizontal zones, with related cards within zones. The two largest zones should be capability overview and architecture. All information below must appear, using the exact concise labels and copy provided; typography hierarchy and short lines are essential.

ZONE 01 — “它提供什么”
An elegant simplified browser-window illustration with a search bar, 3 navigation tiles (NAS, 文档, 代码仓库), a small clock card, a metric card and colored service dots. Label this as “界面示意”. Next to it show six capability cards in a 2×3 grid:
“统一导航” — “链接卡片 / 分组 / 多页面 / 图标与标签”
“快速查找” — “即时搜索 / 快捷键 / 外部搜索引擎”
“动态信息” — “时钟、天气、RSS、日历 / 自托管服务数据”
“状态检查” — “HTTP 响应与耗时 / ICMP Ping / 可配置轮询”
“工作视图” — “普通首页 / 精简页 / iframe 工作区与弹窗”
“个性化配置” — “主题与 CSS / 布局与排序 / 可视化编辑”
Small supporting row: “还支持：多语言 · 响应式界面 · 可选 PWA 基础离线访问”
Tiny important qualification under status card or row: “页面轮询不能等同于全天候监控与告警系统”

ZONE 02 — “它怎样实现”
A large, visually dominant architecture flow, with explicit boundaries:
Left input box “配置与偏好” containing “conf.yml：页面、分组、链接、组件” and “localStorage：当前浏览器偏好”.
Arrow labelled “读取 / 解析 / 合并” leads to central box “浏览器中的 Dashy” with “Vue 3 + Vuex + Vue Router” and “生成界面 · 搜索过滤 · 响应点击”.
From this central box draw three clean, separately labelled outgoing branches:
A. “打开网址” → box “目标应用网页” with “新标签页 / 当前页 / 允许时用 iframe 嵌入”.
B. “组件请求 API” → box “外部服务与数据” with “天气 / NAS / Nextcloud / Pi-hole / Proxmox 等”.
C. “需要后端能力” → box “Node.js + Express” with “HTTP / Ping 探测 · CORS 代理 · 配置写盘”.
Arrow from backend to external services labelled “探测 / 代理请求”.
A separate return arrow from backend to conf.yml labelled “保存到磁盘”.
Below diagram include a two-column save legend:
“保存到本地 → localStorage → 仅当前浏览器”
“保存到磁盘 → 后端接口 → 服务器 YAML 文件”
Short build note: “Vite 负责构建；核心配置通常不需要数据库”
Clear ownership line: “Dashy 组织入口与展示；具体业务功能仍由原应用提供”

ZONE 03 — “用一个 NAS 例子看懂”
Four connected steps with small concrete pictograms:
“点击 NAS 卡片” → “打开 NAS 自己的管理页”
“状态灯变绿” → “Dashy 探测地址得到正常响应”
“显示剩余容量” → “组件通过 NAS API 读取数据”
“上传或删除文件” → “由 NAS 管理页或专门接口执行”
Use four compact horizontal paired rows, not a misleading sequential chain across all four. Add an amber sentence: “只添加网址，不会自动获得文件管理权限”

ZONE 04 — “网页产品与桌面软件，支持到哪里”
A compact 5-row comparison matrix with columns “目标” “支持方式 / 边界”, green dots for native, amber for conditional, red for not native:
“网页应用” | “链接打开；对方允许时可嵌入”
“桌面应用启动” | “条件支持：专用协议链接 + 已安装 + 浏览器允许”
“桌面应用窗口嵌入” | “不原生支持”
“直接执行 .exe / 命令” | “不原生支持；需额外本地桥接程序”
“控制软件、点击按钮、自动化” | “不原生支持；需另接自动化工具”
Footnote below: “专用链接由浏览器与操作系统唤起应用，软件仍在独立窗口运行”

ZONE 05 — “扩展、认证与部署”
Three same-height cards:
“接入外部服务”
“现成组件 → 配置地址与密钥”
“通用 API / iframe → 对接更多内容”
“自定义 Vue 组件 → 扩展展示与交互”
“账号与配置”
“内置账号 / OIDC / Keycloak / 代理认证”
“可配置角色与编辑权限”
“导入导出 / 可选加密备份与恢复”
“部署方式”
“Docker / Node.js 自托管”
“纯静态托管仅覆盖部分能力”
“探测、代理、写盘等需要服务端”
An amber slim boundary band:
“目标服务仍有自己的权限；Dashy 登录不会自动登录所有应用”
“跨域、嵌入策略、网络可达性与 API 权限会影响接入效果”

ZONE 06 — “我们已经验证了什么”
Teal check row: “搜索过滤 ✓   时钟与本机数据刷新 ✓   HTTP 状态变化 ✓   编辑表单 ✓   iframe 工作区 ✓”
Small plain sentence: “演示中的状态切换按钮是额外编写的示例；Dashy 原生负责嵌入面板、探测并显示状态。”
Small scope sentence: “未完整实测：外部账号接入、认证、云备份、配置写盘”
Bottom concluding value statement, as an attractive wide quiet footer:
“适合：个人起始页 · 家庭服务器门户 · 团队工具导航 · 轻量信息总览”
Footer source line in readable small text: “依据：Dashy 4.6.14 源码、官方文档与本机演示｜github.com/Lissy93/dashy｜研究日期：2026-09-16”

Must not imply that Dashy installs/manages desktop software, automatically controls linked systems, inherently executes OS commands, includes our custom status-toggle button, or provides full monitoring/alerting. Do not describe frontend-only login as full backend protection. No invented features, fake dashboard measurements, fake product logos, unlabelled synthetic screenshots, or meaningless tiny text. Distinguish native functions, conditional integrations, and externally added components visually. Make this a thoughtfully composed, finished visual explanation with excellent Chinese typesetting, not a wall of prose.
```
