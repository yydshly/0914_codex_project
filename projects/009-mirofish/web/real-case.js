(() => {
  'use strict';
  const plans = {
    price: ['费用降下来，信任顾虑是否仍然存在？','观察承担费用的角色与未直接承担费用的角色，是否提出不同反对理由。不能预设降价一定有效或无效。','如果主要疑问仍指向长期规则，就追加条款与沟通方案的验证，不把“便宜了”当成问题已解决。'],
    terms: ['规则保障说清楚后，哪些疑问仍未被回答？','检查角色是否能理解适用版本、存量项目与未来变更边界；继续追问计量、执行与可信度问题。','把最难理解或最不可信的承诺交给真实客户和相关负责人核实，形成可兑现的说明与规则。'],
    model: ['改回订阅，会把顾虑转移到哪里？','探索预算可预期性、席位价格与功能价值的讨论。此方案是实验候选，不能因为后来真的取消费用就预设它最优。','把讨论转成真实报价访谈与成本核算；模拟态度不能替代客户的续约行为和公司的经营约束。']
  };
  function show(key) {
    const values = plans[key];
    document.getElementById('case-plan-result').replaceChildren(...['待检验的假设','在模拟记录中检查什么','可能改变的实际工作'].map((label,index)=>{
      const article=document.createElement('article');
      const title=document.createElement('h4');title.textContent=label;
      const body=document.createElement('p');body.textContent=values[index];
      article.append(title,body);return article;
    }));
    document.querySelectorAll('[data-plan]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.plan===key)));
  }
  document.querySelectorAll('[data-plan]').forEach(button=>button.addEventListener('click',()=>show(button.dataset.plan)));
  show('price');
})();
