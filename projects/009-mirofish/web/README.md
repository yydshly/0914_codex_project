# MiroFish 能力实验室

独立中文交互教学页。从总仓库根目录运行：

```powershell
python projects/009-mirofish/src/build_site.py
python -m http.server 8079 --bind 127.0.0.1 --directory projects/009-mirofish/web/dist
```

入口为 http://127.0.0.1:8079/ ，也可直接打开构建后的 `dist/index.html`。页面无第三方前端依赖，不调用模型。

- `index.html`：展厅、原版截图、源码与边界。
- `style.css`：桌面、平板、手机布局与减少动态效果设置。
- `scenarios.js`：三个完整虚构案例。
- `main.js`：场景、情景分支、流程、角色选择、轮次回放、访谈和导出。
- `real-case.js`：Unity 真实案例的三种候选实验方案。历史事实有来源，候选假设不是模型结果。

构建仅包含前端文件、两张原版截图与公开说明，同时检查本地引用、章节锚点、重复 ID、意外产物和符号链接。缓存和密钥不会进入发布包。

已登记到统一构建流程，本次尚未发布。不能把规划的 GitHub Pages 路径当作可用链接。
