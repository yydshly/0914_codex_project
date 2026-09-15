# 15 项动效技能目录

固定版本：`cb3c905e4bc362e02e040035b5c88b13fdd54cf4`。依据目录、README和各SKILL.md；记录的是文档能力，不代表全部实测通过。完整来源见 [sources.md](sources.md)。

| 技能 | 用途 / 输入 | 输出与依赖 |
| --- | --- | --- |
| [ruler-progress-render](../upstream/skills/ruler-progress-render/SKILL.md) | 尺子进度；文字与进度参数 | 外部尺子项目；Remotion；默认透明 MOV |
| [claude-typer](../upstream/skills/claude-typer/SKILL.md) | 提示词的 CLI 打字演示 | 远端 Remotion composition；默认透明 MOV，需联网 |
| [fisheye-motion](../upstream/skills/fisheye-motion/SKILL.md) | 图片的鱼眼、摩尔纹、暗角和聚焦推镜 | 外部 WebGL/React/Remotion 工程与视频 |
| [procedural-fish-render](../upstream/skills/procedural-fish-render/SKILL.md) | 程序化游鱼 | 拉取外部项目，按其命令渲染视频 |
| [pixel2motion](../upstream/skills/pixel2motion/SKILL.md) | 从 Logo 栅格图建立可动效化矢量结构 | SVG、独立 HTML、运动规范、几何与运动检查 |
| [brand-launch-video-star](../upstream/skills/brand-launch-video-star/SKILL.md) | 官网、真实产品素材、品牌宣传需求 | 通常15–30秒发布片、素材来源、叙事和时间轴 |
| [remotion-candlestick](../upstream/skills/remotion-candlestick/SKILL.md) | 金融数据的动态 K 线展示 | Remotion/Canvas 图表动画，数据获取需联网 |
| [light-spotlight-render](../upstream/skills/light-spotlight-render/SKILL.md) | 聚光灯扫字，文字与灯光参数 | Python生成自包含SVG动画HTML；视频需额外渲染 |
| [printed-curtain-render](../upstream/skills/printed-curtain-render/SKILL.md) | 图片、文字织入可交互线帘 | p5.js HTML目录、物理参数面板 |
| [remotion-3d-ticker](../upstream/skills/remotion-3d-ticker/SKILL.md) | 图片列、方向、速度 | Remotion三维照片滚动墙；需图片素材 |
| [remotion-vinyl-player](../upstream/skills/remotion-vinyl-player/SKILL.md) | 封面、曲目信息 | 黑胶转动、文字滚动；视觉播放器不等于生成音乐 |
| [threejs-earth-render](../upstream/skills/threejs-earth-render/SKILL.md) | 城市位置、地球航线 | 外部Three.js/Puppeteer项目，GIF/MP4/PNG序列 |
| [3d-chladni-render](../upstream/skills/3d-chladni-render/SKILL.md) | 粒子、模态、音频驱动参数 | 外部三维声沙项目，MP4或透明ProRes MOV |
| [wechat-2d-render](../upstream/skills/wechat-2d-render/SKILL.md) | 微信聊天与视频气泡演示 | 外部微信动效项目，Remotion视频与透明输出 |
| [disney-animation-rule-skill](../upstream/skills/disney-animation-rule-skill/SKILL.md) | 动画节奏与表现力改进 | 动画十二原则的设计/工程指导；不是独立渲染器 |

## 复用边界

- HTML、SVG、MP4、MOV、PNG序列的交付方式不同。
- 安装技能不等于安装全部效果引擎；部分技能会另拉仓库或调用远端站点。
- 视觉规范不能保证成片质量，仍须核对素材、可读性与观看效果。
- 这些技能使用不同后端，没有统一的调用和输出接口。
- 各模块和素材分别记录许可，不能用组织公开状态代替许可判断。

## 首轮提出的验证建议

后续已运行聚光灯和文字线帘，见 [网页补充研究](gallery.md)。以下保留首轮计划。

以下是研究建议，尚未执行：先验证聚光灯文字的中文HTML，再测照片滚动墙或尺子组件，随后制作一个真实产品镜头，最后用双镜头SRT验证auto-motion的空白保留、跨镜风格和失败重试。根据样本结果决定是否接入001或003的音频制作链路。

