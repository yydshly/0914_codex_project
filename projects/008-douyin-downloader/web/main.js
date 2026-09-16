'use strict';
const paths = {
  direct: {
    title: '公开 Python 版：登录后，通常由程序直接请求', status: '源码已核对',
    steps: [['浏览器登录', '你在抖音网页完成登录，建立会话。'], ['读取 Cookie', '程序获得会话与浏览器相关信息。'], ['Python 发请求', '携带参数、请求头和签名，访问网页接口。'], ['平台返回数据', '接受请求后，返回搜索、评论或作品资料。']],
    key: '登录过 ≠ 后续请求都经过浏览器',
    detail: '这是公开版的主要路径。Cookie 能提供会话信息，但不能保证通过平台的环境校验与风控。'
  },
  fallback: {
    title: '公开版主页兜底：让真实网页先取得作品列表', status: '新门禁下未验证',
    steps: [['Python 启动浏览器', 'Playwright 打开作者主页，必要时等待人工验证。'], ['网页加载与滚动', '真实页面请求更多主页作品。'], ['监听页面响应', '读取作品列表，也可从页面提取作品 ID。'], ['交回 Python', '复用作品数据；需要时补取详情，再组织下载。']],
    key: '针对主页的兜底，不是所有功能的通用浏览器模式',
    detail: '此路径主要服务 post 模式。作者说明尚未验证它能否应对最新风控；打开浏览器本身不代表一定获取成功。'
  },
  desktop: {
    title: 'Douzy 桌面版：特定请求交给内置抖音页面', status: '作者说明 · 未独立实测',
    steps: [['Python 安排任务', '将受限接口的请求交给页面桥接。'], ['内置页面代发', '在真实抖音网页运行环境中发送请求。'], ['平台进行校验', '网页 SDK 提供动态环境信息，平台决定是否接受。'], ['结果交回后端', 'Python 继续分页、整理资料并传输媒体。']],
    key: '浏览器负责页面环境，Python 负责采集与归档',
    detail: '桌面版独立发行。公开库有桥接调用位置，但没有完整的桌面专用实现，不能仅凭共享后端推断桌面版所有功能。'
  }
};
const buttons = [...document.querySelectorAll('[data-mode]')];
function showPath(mode) {
  const data = paths[mode];
  if (!data) return;
  for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
  document.getElementById('route-title').textContent = data.title;
  document.getElementById('route-status').textContent = data.status;
  const route = document.getElementById('route');
  route.replaceChildren(...data.steps.map(([title, description], index) => {
    const item = document.createElement('li');
    const number = document.createElement('span'); number.className = 'step-no'; number.textContent = String(index + 1);
    const label = document.createElement('strong'); label.textContent = title;
    const body = document.createElement('p'); body.textContent = description;
    item.append(number, label, body); return item;
  }));
  document.getElementById('route-key').textContent = data.key;
  document.getElementById('route-detail').textContent = data.detail;
}
for (const button of buttons) button.addEventListener('click', () => showPath(button.dataset.mode));
