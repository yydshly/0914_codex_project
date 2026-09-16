// Original Dashy app, with local-only demonstration endpoints added in front.
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const root = path.resolve(__dirname, '..');
const revision = '6c56436d5f044d3c53371891c9d9a8c8df8c4606';
const upstream = path.join(root, '.cache', 'source', `dashy-${revision}`);
process.env.USER_DATA_DIR = path.join(root, 'user-data');
const app = require(path.join(upstream, 'services', 'app.js'));
let requests = 0;
let sampleOnline = false;
const json = (res, status, data) => {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(data));
};
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1:8060');
  if (url.pathname === '/demo-api/metrics') {
    requests += 1;
    return json(res, 200, {
      source: '本机实时数据',
      freeMemory: `${(os.freemem() / 1024 ** 3).toFixed(1)} GB`,
      totalMemory: `${(os.totalmem() / 1024 ** 3).toFixed(1)} GB`,
      uptime: `${Math.floor(process.uptime())} 秒`,
      requests: `${requests} 次`,
      updatedAt: new Date().toLocaleTimeString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false }),
    });
  }
  if (url.pathname === '/demo-api/healthy') return json(res, 200, { status: '正常', demo: true });
  if (url.pathname === '/demo-api/sample') return json(res, sampleOnline ? 200 : 503, { status: sampleOnline ? '正常' : '维护中', demo: true });
  if (url.pathname === '/demo-api/state') return json(res, 200, { online: sampleOnline });
  if (url.pathname === '/demo-api/toggle' && req.method === 'POST') {
    if (req.headers.origin && req.headers.origin !== 'http://127.0.0.1:8060') return json(res, 403, { error: 'Local demo only' });
    sampleOnline = !sampleOnline;
    return json(res, 200, { online: sampleOnline });
  }
  app(req, res);
});
server.listen(8060, '127.0.0.1', () => {
  fs.writeFileSync(path.join(root, '.cache', 'server.pid'), String(process.pid));
  console.log('Dashy original app: http://127.0.0.1:8060/');
});
server.on('error', (error) => { console.error(error.message); process.exit(1); });
