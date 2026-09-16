# 抖音采集原理 · 网页导读

独立研究页，不是上游产品界面。三种路径切换仅改变本地说明，不调用抖音接口，不采集账号或 Cookie。文件名和步骤均为结构示例。

在总仓库根目录：

```powershell
python projects/008-douyin-downloader/src/build_site.py
python -m http.server 8088 --bind 127.0.0.1 --directory projects/008-douyin-downloader/web/dist
```

打开 <http://127.0.0.1:8088/>，或直接打开 `dist/index.html`。无前端依赖；文字、交互和图片离线可用，来源链接需联网。

包括路径切换、身份解释、功能原理、输出结构、全景图、效果边界和文档下载。构建脚本按白名单复制网页、图片与文档，校验资源和锚点。`dist/` 不进入版本控制，使用相对路径，可接总仓库 GitHub Pages。未验证上线前不登记 demo URL。
