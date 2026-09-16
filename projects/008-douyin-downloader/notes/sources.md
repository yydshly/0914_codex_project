# 固定版本、来源与证据

- 上游：<https://github.com/jiji262/douyin-downloader>
- 研究日期：2026-09-16
- Commit：`125ddf4d7196b7a18fe3a0258cc746503c9d1c57`（2026-09-16）
- 标题：`fix(douyin): 同步桌面版合集双来源与 series 失败判据`
- 包版本 2.0.0；pyproject 声明 Python >=3.9，部分说明仍写 3.8+。
- MIT 许可原样保留在 [UPSTREAM-LICENSE.txt](UPSTREAM-LICENSE.txt)。未引入完整上游代码。

## 固定源码索引

| 主题 | 固定版本证据 |
| --- | --- |
| 功能与风控 | [README](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/README.md) |
| 版本分工 | [AGENTS.md](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/AGENTS.md) |
| 登录 | [cookie_fetcher.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/tools/cookie_fetcher.py) |
| 接口、签名、回复与浏览器 | [api_client.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/api_client.py) |
| 搜索热榜 | [discovery.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/discovery.py) |
| 评论采集 | [comments_collector.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/comments_collector.py) |
| 选源、跳过、画质 | [downloader_base.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/downloader_base.py) |
| 文件传输 | [file_manager.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/storage/file_manager.py) |
| 主页回补 | [user_downloader.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/user_downloader.py) |
| 转写主流程 | [transcript_manager.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/core/transcript_manager.py) |
| 本地转写与 SRT | [whisper_transcribe.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/cli/whisper_transcribe.py) |
| HTTP 服务 | [app.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/server/app.py) |
| 内存任务 | [jobs.py](https://github.com/jiji262/douyin-downloader/blob/125ddf4d7196b7a18fe3a0258cc746503c9d1c57/server/jobs.py) |
| 桌面版发布 | [Desktop 0.11.5](https://github.com/jiji262/douyin-downloader/releases/tag/desktop-v0.11.5) |

## 证据层级

**源码核对：**确认代码存在及调用路径，不证明端点接受请求。**作者披露：**风控日期、部分端点可用和桌面效果未独立验证。**研究推论：**素材库、AI 分析等是扩展用途。**本项目验证：**仅指研究网页与构建，见 verification.md。

## 文档与代码需要区别的地方

1. 最高画质不仅比较码率，还比较分辨率，并有原画来源探测。
2. 回复自动采集只取第一页。
3. README 关于去重有不同表述；当前 `_should_download` 受重下缺失文件等配置影响，可能查询历史。
4. 旧环境中验证过主页兜底，不等于新风控下验证过。
5. 公开服务不启用下载历史数据库；任务状态又是内存保存，不能等同于桌面档案。
