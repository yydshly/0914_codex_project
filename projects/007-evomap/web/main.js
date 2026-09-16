'use strict';
const steps = [
{title:'A 遇到上传超时，需要找出原因', explain:'执行 Agent 查看错误日志、文件大小和接口限制。首先要弄清楚问题发生的条件。', a:['分析现场','读取日志与代码，确认故障。'], hub:['尚无本次经验','保存可供查询的方法与案例。'], b:['还未参与','它以后可能遇到类似问题。'],active:['a'],lesson:['看清分工：','处理代码的是执行 Agent，网页只是入口。']},
{title:'A 尝试修改，并检查是否真的有效',explain:'在这个假设案例中，A 尝试分块上传与有限次数重试。测试需要确认上传成功，且不会丢失或重复数据。',a:['执行与测试','在自己的项目中修改代码并验收。'],hub:['等待验证结果','尚未形成可以分享的本次案例。'],b:['还未参与','不会自动得到 A 的内部思考过程。'],active:['a'],lesson:['关键门槛：','听起来合理的建议，需要经过真实执行和验收。']},
{title:'把成功经历整理成别人能读懂的材料',explain:'Gene 写清楚适用条件和做法；Capsule 保存这一次修改与结果；事件记录说明过程。按授权配置发布后，其他 Agent 才能查询。',a:['整理经验','把步骤、环境与验证结果写清楚。'],hub:['保存经验资产','记录方法、案例和可追踪的结果。'],b:['可查询经验','遇到相关问题时，才会去寻找材料。'],active:['a','hub'],lesson:['“继承”的载体：','流动的是步骤、代码或记录，不是把 A 的模型参数复制给 B。']},
{title:'B 找到候选方案，但还要判断是否适用',explain:'B 在另一个项目遇到超时，查询后拿到候选经验。它仍要检查接口版本、文件大小、权限和运行环境。',a:['本轮任务结束','之前验证过的方法留下了记录。'],hub:['返回候选经验','匹配结果也可能包含备用策略。'],b:['阅读并适配','判断方法是否适合自己的任务。'],active:['hub','b'],lesson:['需要区分：','检索到了材料，尚不代表材料已经解决 B 的问题。']},
{title:'B 重新验证，结果成为下一轮的反馈',explain:'B 应用适合的部分并运行自己的测试。成功、失败和适用条件都值得记录，使后续选择有更多依据。',a:['经验得到后续使用','也可能暴露原方案未考虑的边界。'],hub:['积累反馈','哪些环境有效、哪些条件下失败。'],b:['执行与验收','依据任务结果决定保留或放弃。'],active:['b','hub'],lesson:['这里的“进化”：','经验和选择依据持续变化；整体质量是否提高，还需要对照实验。']}
];
let index=0;
const buttons=[...document.querySelectorAll('[data-step]')];
function renderStep(next) {
 index=Math.max(0,Math.min(steps.length-1,next));
 const step=steps[index];
 document.getElementById('step-count').textContent='第 '+(index+1)+' / '+steps.length+' 步';
 document.getElementById('step-title').textContent=step.title;
 document.getElementById('step-explain').textContent=step.explain;
 for (const actor of ['a','hub','b']) {
   document.getElementById(actor+'-title').textContent=step[actor][0];
   document.getElementById(actor+'-text').textContent=step[actor][1];
   document.getElementById('actor-'+actor).classList.toggle('active',step.active.includes(actor));
 }
 const lesson=document.getElementById('step-lesson');
 const label=document.createElement('b');label.textContent=step.lesson[0];
 lesson.replaceChildren(label,document.createTextNode(step.lesson[1]));
 buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
 document.getElementById('prev-step').disabled=index===0;
 document.getElementById('next-step').disabled=index===steps.length-1;
}
buttons.forEach(button=>button.addEventListener('click',()=>renderStep(Number(button.dataset.step))));
document.getElementById('prev-step').addEventListener('click',()=>renderStep(index-1));
document.getElementById('next-step').addEventListener('click',()=>renderStep(index+1));
