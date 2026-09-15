export function renderPrinciple(source) {
  return `<div class="pagehead"><div><div class="eyebrow">先理解它负责哪一步</div><h1>把准备好的 Skill，拿来自动考试。</h1><p class="lead">agent-skills-eval 读取你提供的测试题和评分标准，调用模型作答、评分，并生成效果报告。</p></div><span class="badge blue">能力与流程</span></div>
  <section class="capability-summary" aria-label="核心能力">
    <div><span class="small-label">你提供</span><h2>Skill + 测试题 + 标准</h2><p>再指定被测模型与裁判模型。</p></div>
    <div><span class="small-label">这个库执行</span><h2>自动运行与评分</h2><p>开启对照后，分别测有 / 无 Skill。</p></div>
    <div><span class="small-label">你得到</span><h2>结果、依据与差异</h2><p>查看哪里失败，修改后再次测试。</p></div>
  </section>
  <section class="panel wide-panel understanding"><h2>可作为“校验能力 Skill”的底层评测引擎。</h2><p>校验 Skill 可以说明验证流程，调用 agent-skills-eval 执行测试，再汇总结果。仓库本身提供评测程序；本研究展示这种组合方式，未另行实现完整封装。</p><p><b>完整开发流程：</b>用户确定能力范围，用户或 AI 设计场景与测试，用户确认标准并准备好 Skill，再交给库验证。需求分析、场景生成和测试设计属于库外准备。</p></section>
  <figure class="panel guide-figure"><a href="./assets/skill-validation-workflow.png" target="_blank" rel="noreferrer" aria-label="打开完整流程引导图"><img src="./assets/skill-validation-workflow.png" width="1536" height="1024" alt="完整校验流程：用户与 AI 准备范围、场景、测试和 Skill；agent-skills-eval 运行有无 Skill 的对照并评分；人工复核后修改再测。"></a><figcaption>蓝色区域是库的实际能力；橙色与绿色区域由用户与 AI 在库外完成。<a href="./assets/skill-validation-workflow.png" download>下载引导图</a></figcaption></figure>
  <div class="section-top"><div class="eyebrow">从需求到验证</div><h2>完整流程：谁做什么？</h2><p>测试可以先设计，也可以在开发过程中补充。启动评测前，Skill 与测试用例都需要准备好。</p></div>
  <section class="workflow-group"><div class="workflow-label"><span class="badge yellow">库外准备</span><span>用户与 AI 协作完成</span></div><div class="flow">${[
    ['01','用户确定能力范围','例如：根据商家政策给出退款建议；不直接执行转账。'],
    ['02','用户 / AI 梳理场景','找出普通申请、超期、信息缺失、质量问题等情况。AI 协助是可选的。'],
    ['03','设计并确认测试','用户或 AI 起草题目、输入与通过条件，业务负责人确认标准是否正确。'],
    ['04','用户 / AI 编写 Skill','把工作步骤写成 SKILL.md。它指导模型怎样做；测试检查模型是否做到了。']
  ].map(([n,t,p])=>`<article class="flow-card"><div class="flow-num">${n}</div><h3>${t}</h3><p>${p}</p></article>`).join('')}</div></section>
  <section class="workflow-group library-work"><div class="workflow-label"><span class="badge blue">这个库的核心能力</span><span>准备好内容后，自动执行</span></div><div class="split"><article class="flow-card"><div class="flow-num">05</div><h3>运行测试，让目标模型作答</h3><p>读取 Skill 和测试用例，调用你指定的模型。开启基线对照后，同一任务分别加载与不加载 Skill，得到两组输出。</p></article><article class="flow-card"><div class="flow-num">06</div><h3>按标准评分，生成对比报告</h3><p>语义要求由裁判模型判断；工具名称、参数和次数由程序检查。保存逐条结果、回答、耗时和 Token，并汇总差异。</p></article></div></section>
  <section class="review-step"><span class="flow-num">07</span><div><h3>人复核结果，修改 Skill 或测试，再跑一轮</h3><p>确认失败是 Skill 的问题、测试标准的问题，还是裁判误判。这个库提供评测依据；改写 Skill 和最终业务验收仍需另外完成。</p></div></section>
  <section class="panel wide-panel"><div class="panel-title"><h2>用“退款客服”串起整个过程</h2><span class="badge yellow">示意案例</span></div><p class="lead">下面的题目与回答用于解释流程，没有调用真实模型。</p><div class="table-wrap"><table><thead><tr><th>步骤</th><th>具体内容</th><th>谁负责</th></tr></thead><tbody>
    <tr><td>能力范围</td><td>根据政策判断能否申请退款；信息不足时先询问。</td><td>用户定义</td></tr>
    <tr><td>场景与题目</td><td>政策要求收货后 7 天内且未拆封。用户只说“商品未拆封”，没提供日期。</td><td>用户 / AI 设计</td></tr>
    <tr><td>Skill 指令</td><td>判断退款前，检查收货日期；缺少信息时不得直接认定符合条件。</td><td>用户 / AI 编写</td></tr>
    <tr><td>测试标准</td><td>① 指出缺少收货日期；② 不直接判定可以退款。</td><td>用户确认，可由 AI 起草</td></tr>
    <tr><td>运行与评分</td><td>假设模型回答“未拆封，可以退款”。库将回答交给裁判，按上面两条标准检查。</td><td>库调度模型和裁判</td></tr>
    <tr><td>复核与改进</td><td>查看失败依据，调整 Skill 的检查步骤；用相同测试再次验证。</td><td>人复核，库负责复跑</td></tr>
  </tbody></table></div><div class="link-row"><button class="button-link" data-goto-scene="refund" data-preset="missing">演示这道“信息不足”测试题</button><a class="source-small" href="${source}run-eval.ts" target="_blank" rel="noreferrer">查看上游执行流程 ↗</a></div></section>
  <section class="panel wide-panel"><h2>“写 Skill”与“设计测试”，是两份不同的内容。</h2><div class="split"><div><h3>Skill：告诉 AI 怎么做</h3><p>例如：“先确认收货日期，再检查期限；信息缺失时先询问。”这是工作手册，交给被测模型执行。</p></div><div><h3>测试：检查 AI 有没有做到</h3><p>例如：“不给收货日期，观察回答是否追问。”题目交给被测模型，评分条件用于事后检查。</p></div></div><p class="lead">它的用途是验证技能效果，适用于客服、写作、分析和代码任务，不限于代码自动测试。</p></section>
  <div class="split section-top"><section class="panel wide-panel"><span class="badge blue">AI 裁判</span><h2 style="margin-top:18px">检查语义要求</h2><p>例如：“回答是否明确指出缺少日期？”裁判模型根据条件和输出给出通过 / 失败与依据。</p><p>实际使用时，标准要写清必要事实；裁判结果仍需要抽查。</p><a class="source-small" href="${source}grade.ts" target="_blank" rel="noreferrer">评分模块 ↗</a></section><section class="panel wide-panel"><span class="badge green">程序检查</span><h2 style="margin-top:18px">检查确定的工具规则</h2><p>例如：“是否调用 lookup，city 参数是否为 Shanghai？”这类检查无需裁判模型。</p><p>检查到工具请求，不代表工具已经执行成功。</p><button class="button-link" data-goto-scene="tool">演示工具检查</button></section></div>
  <div class="dark-panel"><div class="split"><div><h2>最终分数说明什么？</h2><p>一个用例有 4 条检查，3 条通过，就是 75%。报告帮助你找到失败项，比较 Skill 修改前后的表现。</p></div><div><code>通过率 = 通过条件数 ÷ 总条件数<br>对照差值 = 有 Skill 均值 − 无 Skill 均值</code><p>解释差值前，要确认两组任务数据一致、评分标准合理，并抽查裁判。分数不能直接替代完整业务验收。</p></div></div></div>`;
}
