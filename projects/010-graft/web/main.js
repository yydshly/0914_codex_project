'use strict';
const upstream = 'https://github.com/trailhq/Graft/blob/f9e65396e638e517aecae0d731017f53084d70ed/';
document.querySelectorAll('[data-source]').forEach(a => { a.href = upstream + a.dataset.source; a.target = '_blank'; a.rel = 'noopener noreferrer'; });
// Original teaching corpus. These selections illustrate concepts, not Graft's ranking algorithm.
const files = [
  {id:'login',path:'routes/login.ts',label:'登录入口',symbol:'login()',x:20,y:15,signature:'export async function login(req: LoginRequest): Promise<string>',crux:'const user = await authenticate(req.email, req.password);\nreturn issueToken(user.id);',full:'import { issueToken } from "../auth/token";\nimport { authenticate } from "../users/authenticate";\n\nexport async function login(req: LoginRequest): Promise<string> {\n  const user = await authenticate(req.email, req.password);\n  return issueToken(user.id);\n}',why:'入口调用签发函数。签发接口改变时，要检查这里传入的参数。'},
  {id:'token',path:'auth/token.ts',label:'Token 签发',symbol:'issueToken()',x:50,y:40,signature:'export function issueToken(userId: string): string',crux:'return jwt.sign({ sub: userId }, SECRET, {\n  expiresIn: TOKEN_TTL_SECONDS,\n});',full:'import jwt from "jsonwebtoken";\nimport { SECRET, TOKEN_TTL_SECONDS } from "../config/auth";\n\nexport function issueToken(userId: string): string {\n  if (!userId) throw new Error("Missing user ID");\n  return jwt.sign({ sub: userId }, SECRET, {\n    expiresIn: TOKEN_TTL_SECONDS,\n  });\n}',why:'签发函数读取有效期配置。查看片段可以发现传给 JWT 库的参数，但还需要验证单位与需求。'},
  {id:'config',path:'config/auth.ts',label:'有效期配置',symbol:'TOKEN_TTL',x:80,y:15,signature:'export const TOKEN_TTL_SECONDS: number\nexport const SECRET: string',crux:'export const TOKEN_TTL_SECONDS = 60;',full:'export const TOKEN_TTL_SECONDS = 60;\nexport const SECRET = process.env.JWT_SECRET ?? "";\n\nif (!SECRET) {\n  throw new Error("JWT_SECRET is required");\n}',why:'示例有效期设为 60 秒。它是掉线问题的调查线索，不足以单独证明生产环境的根因。'},
  {id:'middleware',path:'auth/middleware.ts',label:'请求校验',symbol:'requireAuth()',x:80,y:72,signature:'export function requireAuth(token: string): JwtPayload',crux:'const payload = jwt.verify(token, SECRET);\nreturn payload as JwtPayload;',full:'import jwt, { JwtPayload } from "jsonwebtoken";\nimport { SECRET } from "../config/auth";\n\nexport function requireAuth(token: string): JwtPayload {\n  const payload = jwt.verify(token, SECRET);\n  if (typeof payload === "string") {\n    throw new Error("Invalid payload");\n  }\n  return payload;\n}',why:'校验端读取同一认证配置，并检查 Token。它没有直接调用签发函数；这类关联需要沿配置与业务流程理解。'},
  {id:'test',path:'tests/token.test.ts',label:'签发测试',symbol:'test()',x:20,y:72,signature:'test("issues a token for a user", () => void)',crux:'const token = issueToken("user-42");\nexpect(typeof token).toBe("string");',full:'import { test, expect } from "vitest";\nimport { issueToken } from "../auth/token";\n\ntest("issues a token for a user", () => {\n  const token = issueToken("user-42");\n  expect(typeof token).toBe("string");\n});',why:'测试直接调用签发函数，因此接口修改需要检查它。当前断言只检查类型，修复过期问题还需要补充有效期测试。'},
  {id:'catalog',path:'shop/catalog.ts',label:'商品目录',symbol:'listProducts()',x:50,y:92,signature:'export function listProducts(): Product[]',crux:'return products.filter(product => product.visible);',full:'const products: Product[] = [];\n\nexport function listProducts(): Product[] {\n  return products.filter(product => product.visible);\n}',why:'这个教学样例没有记录商品目录与认证代码的连接，因此本次任务未优先选取。真实项目仍需检查索引覆盖。'},
];
const relations = [['login','token'],['test','token'],['token','config'],['middleware','config']];
const tasks = {
  expiry:{ids:['config','token','middleware','test'],selected:'config',hint:'从过期配置查起，沿关系查看签发与校验。'},
  refactor:{ids:['token','login','test'],selected:'token',hint:'从签发函数向上追踪调用者，检查参数与测试。'},
  overview:{ids:['login','token','config','middleware'],selected:'login',hint:'沿登录入口、签发和配置理解流程，再查看后续请求校验。'},
};
let task='expiry', selected='config', depth='crux';
const $ = id => document.getElementById(id);
const lineCount = value => value.split('\n').length;
function pressed(selector, key, value) { document.querySelectorAll(selector).forEach(b => b.setAttribute('aria-pressed', String(b.dataset[key] === value))); }
function renderCode(){
  const file=files.find(f=>f.id===selected);
  $('code-title').textContent=file.path;
  $('code').textContent=file[depth];
  $('shown-lines').textContent=lineCount(file[depth]);
  $('total-lines').textContent=`该文件完整示例 ${lineCount(file.full)} 行`;
  $('depth-note').textContent={signature:'了解接口形状。接口轮廓可以帮助决定是否还需读取实现。',crux:'先读与理解有关的局部逻辑。片段可能不包含所有前提。',full:'展开完整示例，核对导入、检查条件和返回路径。'}[depth];
  $('why').textContent=file.why;
  document.querySelectorAll('[data-file]').forEach(b=>{b.classList.toggle('selected',b.dataset.file===selected); b.setAttribute('aria-pressed',String(b.dataset.file===selected));});
}
function renderTask(){
  const current=tasks[task];
  $('task-hint').textContent=current.hint;
  $('file-count').textContent=`${files.length} 个`;
  $('file-list').replaceChildren(); $('nodes').replaceChildren();
  files.forEach(f=>{
    const relevant=current.ids.includes(f.id);
    const button=document.createElement('button');button.type='button';button.className=`file-btn${relevant?' relevant':''}`;button.dataset.file=f.id;button.textContent=f.path;button.addEventListener('click',()=>{selected=f.id;renderCode();});$('file-list').append(button);
    const node=document.createElement('button');node.type='button';node.className=`node${relevant?' relevant':''}`;node.style.left=f.x+'%';node.style.top=f.y+'%';node.dataset.file=f.id;node.setAttribute('aria-label',f.label+'，'+f.path);node.append(document.createTextNode(f.label));const small=document.createElement('small');small.textContent=f.symbol;node.append(small);node.addEventListener('click',()=>{selected=f.id;renderCode();});$('nodes').append(node);
  });
  $('edges').replaceChildren();
  relations.forEach(([a,b])=>{const from=files.find(f=>f.id===a),to=files.find(f=>f.id===b);const path=document.createElementNS('http://www.w3.org/2000/svg','path');const dx=(to.x-from.x)*5,dy=(to.y-from.y)*3.5,len=Math.hypot(dx,dy);const margin=44;path.setAttribute('d',`M${from.x*5+dx/len*margin},${from.y*3.5+dy/len*margin} L${to.x*5-dx/len*margin},${to.y*3.5-dy/len*margin}`);path.classList.add('edge');if(current.ids.includes(a)&&current.ids.includes(b))path.classList.add('lit');$('edges').append(path);});
  pressed('[data-task]','task',task);renderCode();
}
document.querySelectorAll('[data-task]').forEach(b=>b.addEventListener('click',()=>{task=b.dataset.task;selected=tasks[task].selected;renderTask();}));
document.querySelectorAll('[data-depth]').forEach(b=>b.addEventListener('click',()=>{depth=b.dataset.depth;pressed('[data-depth]','depth',depth);renderCode();}));
const steps=[
  {kicker:'输入 / SOURCE FILES',title:'确定哪些源码进入索引',description:'按项目范围枚举源码，结合 Git 文件可见性与支持的语言。构建时读取源码并计算哈希；未变化文件复用之前的解析结果。忽略项或不支持的内容不会自动成为图谱知识。',example:'routes/login.ts\nauth/token.ts\nconfig/auth.ts\n        ↓\n源码内容 + 路径 + 内容哈希',source:'src/graph/build.ts'},
  {kicker:'解析 / TREE-SITTER',title:'将源码拆成可定位的符号',description:'语法解析器把代码变成语法树。提取器识别函数、类、定义位置和调用表达式，生成符号节点及待解析关系。它根据语法结构工作，不需要让模型先通读每个文件。',example:'function issueToken(userId) { … }\n        ↓\n类型：函数\n名称：issueToken\n位置：auth/token.ts\n签名：issueToken(userId: string)',source:'src/graph/extract.ts'},
  {kicker:'关联 / NODES & EDGES',title:'把“调用了谁”连成图',description:'通过作用域、导入路径、名称及可用类型线索，将调用关联到具体符号。不同语言的解析精度不同，无法确定的关系可能被跳过。可选语言服务增强可补充更精确的关系。',example:'login() ─calls→ issueToken()\nissueToken() ─references→ TOKEN_TTL\ntest() ─calls→ issueToken()\n        ↓\n结构图：graft/.graph/wiring.json',source:'src/graph/resolve.ts'},
  {kicker:'选择 / RETRIEVAL',title:'词项匹配与图结构共同排序',description:'关系类问题可以沿调用边查找；其他查询匹配名称、签名和说明等内容，再结合图排序组织相关位置。限制路径和返回数量，并考虑不同文件，避免只拿到同一文件的一堆相近片段。',example:'任务：token expiry\n        ↓\n匹配名称 / 签名 / 说明\n        +\n图关系排序与相关节点\n        ↓\n少量相关位置与来源',source:'src/ask/ask.ts'},
  {kicker:'组织 / CONTEXT',title:'按需要决定返回多少内容',description:'返回位置、接口轮廓、关键片段或完整定义。结果大小是可以控制的；获得线索后，助手可以继续查询或读取源码。这里减少的是进入模型的无关内容，而非让程序完全不读文件。',example:'接口：issueToken(userId: string)\n片段：expiresIn: TOKEN_TTL_SECONDS\n来源：auth/token.ts + 行号\n关系：login() / test() 调用它\n        ↓\n模型可用的局部上下文',source:'src/mcp/tools.ts'},
  {kicker:'使用 / CODING AGENT',title:'编程助手拿到上下文，继续工作',description:'CLI 或 MCP 将查询结果交给助手；模型结合任务判断、修改并测试。Graft 提供代码知识和导航能力，功能是否修好仍由源码、执行结果与验收标准决定。',example:'用户任务\n   ↓\n助手调用 Graft 工具\n   ↓\n相关上下文 → 模型理解与修改\n   ↓\n源码复核 / 测试 / 验收',source:'src/mcp/server.ts'},
];
function renderStep(index){const s=steps[index];pressed('[data-step]','step',String(index));$('step-kicker').textContent=s.kicker;$('step-title').textContent=s.title;$('step-description').textContent=s.description;$('step-example').textContent=s.example;$('step-source').href=upstream+s.source;}
document.querySelectorAll('[data-step]').forEach(b=>b.addEventListener('click',()=>renderStep(Number(b.dataset.step))));
const freshness={
  clean:{structure:'复用现有图谱',summary:'未变内容可复用',text:'轻量检查没有发现变化时，可以直接使用现有结构。如果从未生成过深度摘要，它仍然不存在；不需要为每次查询再付一次摘要费用。',code:'检查文件指纹 → 未发现变化 → 查询图谱'},
  changed:{structure:'重新解析变更，复用其余结果',summary:'已有说明可能标记过期',text:'结构刷新可以在本地完成。模型摘要依赖代码含义，变化后需要重新生成才能更新；自动结构刷新不会顺便调用模型把所有摘要改写。',code:'内容哈希变化 → 更新结构 → 摘要 stale / pending'},
  failed:{structure:'可能继续使用旧图谱',summary:'不能保证与源码一致',text:'源码存在刷新失败的降级路径，会附带提示并尝试使用已有图谱。此时必须关注提示、排查原因，必要时直接读源码，而非默认结果是最新的。',code:'刷新失败 → 返回提示 → 现存图谱（如可用）'},
};
function renderFresh(key){const f=freshness[key];pressed('[data-fresh]','fresh',key);$('structure-state').textContent=f.structure;$('summary-state').textContent=f.summary;$('fresh-explanation').textContent=f.text;$('fresh-code').textContent=f.code;document.querySelector('.fresh-card').dataset.state=key;}
document.querySelectorAll('[data-fresh]').forEach(b=>b.addEventListener('click',()=>renderFresh(b.dataset.fresh)));
const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){document.querySelectorAll('.rail nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}});},{rootMargin:'-10% 0px -65% 0px'});document.querySelectorAll('section[id]').forEach(section=>observer.observe(section));
renderTask();renderStep(0);renderFresh('clean');
