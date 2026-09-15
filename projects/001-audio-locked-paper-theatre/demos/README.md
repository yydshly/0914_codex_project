# 科普、教学培训与英语微课

新增 [英语微课堂](../web/english.html)：89 秒中英双语位置词教学，含跟读停顿与三道网页练习。[查看完整说明与素材提示](english/README.md)。[全部能力与场景](../web/guide.html)。

## 科普：DNS 如何找到网站

- [观看视频](dns/output/demo.mp4) / [本地播放页](../web/dns.html) / [完整文稿](dns/script.json) / [关键帧](dns/output/contact-sheet.jpg)。
- 声音约 59 秒，成片约 61 秒，1080p、24 fps。
- 用查询卡与返回卡表现设备、递归解析器、根服务器、顶级域服务器和权威服务器之间的关系。
- 先演示缓存检查，再展示无可用缓存时的查询路线；随后将网页传输与 DNS 查询分开呈现。
- 适用于互联网基础课、技术科普、产品原理介绍。
- 内容依据：[Cloudflare DNS 服务器类型](https://www.cloudflare.com/learning/dns/dns-server-types/)、[IANA 示例域名](https://www.iana.org/help/example-domains)。画面使用保留的 example.com；未查询或声明其真实 IP。为了突出核心过程，省略别名、多地址、DNSSEC 和连接握手等细节。

## 教学培训：把模糊需求变成可执行任务

- [观看视频](task-training/output/demo.mp4) / [本地播放页](../web/task-training.html) / [完整文稿](task-training/script.json) / [关键帧](task-training/output/contact-sheet.jpg)。
- 声音约 73 秒，成片约 74 秒，1080p、24 fps。
- 先展示“尽快整理客户反馈”的模糊之处，再逐项补齐负责人、交付物、期限和验收标准。
- 展示发起方和接收者的复述交接，并加入“尽快优化首页”的练习。
- 播放页的“暂停做练习”会暂停在问题处，“揭晓练习答案”从答案段继续。
- 适用于新人入职、团队协作、任务交接与管理培训。本片为自编通用沟通范例，不代表特定组织的规章制度。

## 实现与复现

两段配音均由 MiniMax `speech-2.8-hd`、`male-qn-jingying` 生成。使用供应商返回的真实句级时间戳编排动画，句内动作由制作代码设计，不声称逐词对齐。

```sh
python src/series_render.py dns
python src/series_render.py task-training
python src/verify.py --episode dns
python src/verify.py --episode task-training
python src/build_series_pages.py
python src/serve.py
```

已有音轨和素材可以离线重复渲染，不会再次请求 MiniMax。两段成片各保留字幕、原始配音、时间线、审核帧、解码与音轨校验报告。

本次属于上游方法的可运行复现，没有声称通过其全部长片生产门禁或独立审核。

## 素材与完整生图提示

电脑与夹板由本次内置 imagegen 生成，透明 PNG 已复制到各自的 `assets/`。文字、卡片、连线、移动请求与勾选状态使用程序绘制；DNS 解析器沿用本项目先前生成的纸艺机器。字体使用运行电脑上的微软雅黑，不分发字体文件。无背景音乐。

### 电脑素材

路径：`dns/assets/computer.png`。

> Transparent independent papercraft prop for editorial science explainer animation: one exquisite compact desktop computer with a rounded pale sky-blue cardboard monitor and warm cream keyboard, front-facing orthographic view. Monitor has a flat EMPTY off-white rectangular screen with ample usable space to add text later, no reflections obscuring the blank screen. Tactile folded paper edges, layered cardstock, soft studio light, sophisticated educational magazine style. Entire monitor and keyboard visible with generous margins, genuinely transparent alpha background, no text, no letters, no logo, no characters, no other objects, square canvas. Calm blue and cream palette with a tiny ochre status light.

### 夹板素材

路径：`task-training/assets/clipboard.png`。

> Transparent independent papercraft prop for a polished employee-training animation: one beautiful warm coral-red clipboard with a brushed golden paper clip, holding a blank ivory sheet with absolutely NO writing or lines. Straight-on orthographic front view, perfectly upright vertical rectangle, tactile layered cardstock and folded edges, soft contact shadows, refined editorial illustration. Empty paper area large and clear, entire clipboard and clip contained with generous transparent margins, alpha transparent background, no letters, no numbers, no checkboxes, no background scene, square canvas. Coral, cream and golden ochre palette.
