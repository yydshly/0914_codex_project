"use strict";
const scenarios = {
  bug: { prompt: "查明登录按钮没有反应的原因，修复问题，补充回归测试，并提交 PR 供我审核。", examples: ["保存登录问题的描述、目标仓库和验收要求，等待执行。", "获取网站代码，准备依赖和测试环境，让代理可以复现问题。", "模型判断应读取哪些文件；代理读取登录逻辑、修改代码，再把命令结果交给模型。", "运行相关测试，整理修复说明与代码差异，按要求提交 PR；仍需人工审核。"] },
  feature: { prompt: "给订单页面增加 CSV 导出功能，保持现有权限规则，补充测试，并提交 PR 供我审核。", examples: ["保存导出格式、权限约束、仓库和测试要求。", "获取项目代码，启动所需服务，配置测试数据与依赖。", "模型分析页面、接口和权限逻辑；代理修改文件、运行命令，必要时用浏览器检查。", "验证导出结果和权限规则，展示测试输出，提交可审查的代码改动。"] },
  alert: { prompt: "指定 CI 工作流失败时，分析日志和对应提交，说明原因；可复现且范围明确时尝试修复并提交 PR。", examples: ["配置好的 GitHub 事件触发自动化；平台接收事件并生成任务，按条件过滤和去重。", "准备对应仓库环境，让代理能够获取实际日志、代码及复现所需依赖。", "代理取得日志与测试结果，模型分析原因；必要时修改代码并再次执行命令。", "报告原因、复现过程和验证结果；若完成修复，再按要求交付 PR。自动触发不保证自动修好。"] }
};
const steps = [
  {owner:"管理服务",title:"先把需求存成一条任务",description:"网页或集成入口发送要求后，后台保存内容、作者和状态。如果同一会话已有工作，新的要求进入队列。",principle:"技术点：任务生命周期属于服务端，网页是输入与查看入口。"},
  {owner:"管理服务 + 沙箱后端",title:"为任务准备一套开发环境",description:"后台创建或恢复独立沙箱，获取仓库、准备依赖与服务。Supervisor 管理启动，Bridge 连回后台等待任务。",principle:"技术点：预构建、文件快照或持久沙箱恢复，减少重复的环境准备。"},
  {owner:"代理程序 + 模型 + 工具",title:"模型判断，代理调用工具执行",description:"OpenCode 或 Claude Agent 把上下文交给模型，按返回的工具调用读写文件、执行命令，再把结果交回模型。这是多轮执行过程。",principle:"技术点：模型提供推理，程序执行操作；Bridge 持续把文字、工具调用与状态回传。"},
  {owner:"代理执行，平台记录，你来验收",title:"交付可以检查的结果",description:"代理按要求运行验证、整理改动，平台记录结果和产物，并可配合创建 PR。后续要求继续进入会话。",principle:"技术点：任务完成状态不等于代码一定正确，需结合测试、差异与实际结果验收。"}
];
let currentStep=0;
const $=id=>document.getElementById(id);
const stepButtons=[...document.querySelectorAll('[data-step]')];
function renderStep(index, focus=false){
  currentStep=index;
  const step=steps[index], scenario=scenarios[$('scenario').value];
  stepButtons.forEach((button,i)=>{button.classList.toggle('active',i===index);button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;});
  $('step-panel').setAttribute('aria-labelledby',`step-tab-${index}`);
  $('step-owner').textContent=step.owner;$('step-title').textContent=step.title;$('step-description').textContent=step.description;
  $('step-example').textContent=scenario.examples[index];$('step-principle').textContent=step.principle;$('step-count').textContent=`步骤 ${index+1} / 4`;
  $('next-step').textContent=index===3?'回到第一步 ↺':'下一步 →';$('task-prompt').textContent=scenario.prompt;
  if(focus)stepButtons[index].focus();
}
stepButtons.forEach((button,index)=>{
  button.addEventListener('click',()=>renderStep(index));
  button.addEventListener('keydown',event=>{let next=index;if(['ArrowDown','ArrowRight'].includes(event.key))next=(index+1)%4;else if(['ArrowUp','ArrowLeft'].includes(event.key))next=(index+3)%4;else if(event.key==='Home')next=0;else if(event.key==='End')next=3;else return;event.preventDefault();renderStep(next,true);});
});
$('next-step').addEventListener('click',()=>renderStep((currentStep+1)%4));
$('scenario').addEventListener('change',()=>renderStep(currentStep));

const providers={
  openai:{name:'OpenAI / Codex 模型',auth:'API Key，或项目支持的 ChatGPT 账号授权。',config:'部署密钥 / Settings → Provider Accounts；创建会话时选择模型和认证。',boundary:'使用 Codex 模型，不等于启动 Codex CLI 或控制 Codex 桌面软件。'},
  anthropic:{name:'Anthropic Claude',auth:'ANTHROPIC_API_KEY；在 OpenCode 路径中使用 API Key。',config:'配置 Anthropic API Key；创建会话时选择 Claude 模型。',boundary:'Claude 订阅账号授权适用于 Claude Agent 路径，不适用于 OpenCode 的 Anthropic 接入。'},
  xai:{name:'xAI Grok',auth:'XAI_API_KEY，或项目支持的 SuperGrok 账号授权。',config:'Settings → Models 启用；密钥或 Provider Accounts 配置认证。',boundary:'模型可用性取决于账号权益和渠道；项目中默认需要启用该模型组。'},
  zen:{name:'OpenCode Zen / Go',auth:'OPENCODE_API_KEY；Go 还需要对应渠道的有效订阅。',config:'在全局或仓库密钥配置凭据，并在 Settings → Models 启用。',boundary:'这是模型服务渠道，可提供 Kimi、MiniMax、Qwen、GLM 等；不是增加了一种代理程序。'},
  zai:{name:'Z.AI Coding Plan',auth:'ZHIPU_API_KEY。',config:'在全局或仓库密钥配置凭据，并在 Settings → Models 启用。',boundary:'该渠道接入 GLM 模型。仍由 OpenCode 负责执行代理流程。'},
  deepseek:{name:'DeepSeek',auth:'DEEPSEEK_API_KEY。',config:'在全局或仓库密钥配置凭据，并在 Settings → Models 启用。',boundary:'使用项目目录中支持的 DeepSeek 模型；模型权限与实际可用性需验证。'}
};
let lastOpenCodeProvider='openai';
function renderConnection(){
  const claude=$('harness').value==='claude',provider=$('provider');
  if(claude)provider.value='anthropic';
  [...provider.options].forEach(option=>{option.disabled=claude&&option.value!=='anthropic';});
  const data=providers[provider.value];
  $('runner-name').textContent=claude?'Claude Agent 程序':'OpenCode 程序';$('provider-name').textContent=data.name;
  $('compatibility-note').textContent=claude?'Claude Agent 仅支持 Anthropic 模型，其余模型选项已禁用。':'OpenCode 可使用项目模型目录中的多个提供商。';
  $('connection-title').textContent=claude?'通过 SDK 运行 Claude 代理':`运行 OpenCode，调用${provider.value==='openai'?' OpenAI 模型':` ${data.name}`}`;
  $('connection-description').textContent=claude?'平台通过 Claude Agent SDK 在沙箱中启动 claude 程序，由它调用模型并使用工具。每个会话选择一个固定的代理运行层。':'平台在沙箱中启动 opencode serve，由它执行代理流程。模型提供推理，文件与命令操作由代理工具完成。';
  $('auth-method').textContent=claude?'ANTHROPIC_API_KEY，或项目支持的 Claude 账号授权。':data.auth;
  $('config-location').textContent=claude?'部署密钥或 Settings → Provider Accounts → Claude；创建会话时选择 Claude Agent。':data.config;
  $('connection-boundary').textContent=claude?'此路径实际运行代理程序；不是打开桌面聊天窗口、模拟鼠标输入。':data.boundary;
}
$('harness').addEventListener('change',()=>{if($('harness').value==='claude')lastOpenCodeProvider=$('provider').value;else $('provider').value=lastOpenCodeProvider;renderConnection();});
$('provider').addEventListener('change',()=>{lastOpenCodeProvider=$('provider').value;renderConnection();});
const dialog=$('overview-dialog');
$('open-overview').addEventListener('click',()=>{dialog.showModal();document.body.style.overflow='hidden';});
$('close-overview').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{document.body.style.overflow='';});
dialog.addEventListener('click',event=>{const bounds=dialog.getBoundingClientRect();if(event.clientX<bounds.left||event.clientX>bounds.right||event.clientY<bounds.top||event.clientY>bounds.bottom)dialog.close();});
renderStep(0);renderConnection();
