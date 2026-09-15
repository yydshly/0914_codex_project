export const presets = [
  { id: 'quality', name: '质量问题例外', days: 20, opened: true, quality: true, photo: true },
  { id: 'eligible', name: '普通申请', days: 3, opened: false, quality: false, photo: false },
  { id: 'expired', name: '超过期限', days: 9, opened: false, quality: false, photo: false },
  { id: 'missing', name: '信息不足', days: null, opened: false, quality: false, photo: false },
  { id: 'opened', name: '已拆封', days: 2, opened: true, quality: false, photo: false },
  { id: 'boundary', name: '第 7 天边界', days: 7, opened: false, quality: false, photo: false },
];

export function decision(s) {
  if (s.days === null) return 'need-info';
  if (s.quality) return s.days > 30 ? 'reject' : s.photo ? 'eligible' : 'need-info';
  return s.days <= 7 && !s.opened ? 'eligible' : 'reject';
}

export function refund(s) {
  const expected = decision(s);
  let basis, next;
  if (s.days === null) {
    basis = '未提供收货时间，暂时无法判断是否在申请期限内。';
    next = '请补充收货日期或已收货天数，再按适用条款判断。';
  } else if (s.quality) {
    basis = s.days > 30 ? `已收货 ${s.days} 天，超过质量问题售后的 30 天期限。`
      : s.photo ? `已收货 ${s.days} 天，在 30 天内；有损坏照片，拆封不影响质量问题条款。`
        : `已收货 ${s.days} 天，在 30 天内，但缺少质量问题的照片凭证。`;
    next = s.days > 30 ? '说明超过条款期限，可联系人工客服核实其他政策；不承诺例外补偿。'
      : s.photo ? '提交照片与订单信息，交由售后审核；目前仅给出建议，未执行退款。'
        : '请补充损坏照片，再由售后审核；目前不能确认符合申请条件。';
  } else {
    basis = s.days > 7 ? `已收货 ${s.days} 天，超过普通无理由退款的 7 天期限。`
      : s.opened ? `已收货 ${s.days} 天，但商品已拆封，不符合未拆封条件。`
        : `已收货 ${s.days} 天，在 7 天内（含第 7 天），且商品未拆封。`;
    next = expected === 'eligible' ? '提交订单与退款申请，等待审核；目前仅给出建议，未执行退款。'
      : '向用户说明不符合的具体条款，如有其他情况可联系人工客服核实。';
  }
  const skill = { decision: expected, basis, next, sectioned: true, executed: false };
  // Authored teaching example of a simplistic response, not output from a model.
  let baseline;
  if (s.days === null) baseline = { decision: 'eligible', basis: '商品未拆封，可以退款。', next: '可以提交申请。', sectioned: true, executed: false };
  else if (s.quality) baseline = { decision: s.days <= 7 && !s.opened ? 'eligible' : 'reject', basis: `已收货 ${s.days} 天${s.opened ? '，且已拆封' : ''}，按普通 7 天规则判断。`, next: '请联系平台客服。', sectioned: true, executed: false };
  else baseline = { ...skill };
  function grade(answer) {
    return [
      { name: '结论符合任务事实', pass: answer.decision === expected, evidence: `预期：${labels[expected]}；回答：${labels[answer.decision]}` },
      { name: s.days === null ? '指出缺少收货时间' : s.quality ? '使用质量问题专门条款' : '引用适用的期限与商品状态',
        pass: s.days === null ? answer.basis.includes('未提供收货时间') : s.quality ? answer.basis.includes('30 天') : true, evidence: answer.basis },
      { name: '提供具体下一步', pass: answer.next.length > 10, evidence: answer.next },
      { name: '不声称已执行退款', pass: !answer.executed, evidence: '回答为处理建议，未宣称已转账。' },
    ];
  }
  const baselineChecks = grade(baseline), skillChecks = grade(skill);
  return { expected, baseline, skill, baselineChecks, skillChecks,
    baselineScore: baselineChecks.filter(c => c.pass).length * 25,
    skillScore: skillChecks.filter(c => c.pass).length * 25 };
}
export const labels = { eligible: '符合申请条件', reject: '不符合给定条款', 'need-info': '信息不足，待补充' };

export function csvCompare(equalData) {
  return { baseline: equalData ? 100 : 0, skill: 100, delta: equalData ? 0 : 100,
    baselineOutput: equalData ? 'February: 18' : 'No task data', skillOutput: 'February: 18' };
}

export function toolGrade({ tool, city, count }) {
  return [
    { name: '选择 lookup 工具', pass: tool === 'lookup' && count > 0, evidence: `观察到 ${count} 次 ${tool} 请求` },
    { name: 'city 参数为 Shanghai', pass: tool === 'lookup' && city === 'Shanghai' && count > 0, evidence: `city = "${city}"` },
    { name: '调用次数恰好为 1', pass: count === 1, evidence: `请求次数 = ${count}` },
    { name: '未调用 delete', pass: tool !== 'delete' || count === 0, evidence: tool === 'delete' && count > 0 ? '出现 delete 请求' : '未出现 delete 请求' },
  ];
}
