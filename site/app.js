const panel = document.querySelector('#panel');
const content = document.querySelector('#panel-content');
const data = {
  gpa: {title:'GPA / 项目水平评分', intro:'分数不是奖项承诺。它把评审基线、证据覆盖和当前材料质量放在同一张表里。2026 官方评审规则发布后，权重会随版本更新。', items:[['04','创新','证据是否能证明机制与效果，而不是只写“先进”'],['03','成长','调研、试验、知识应用与学生真实贡献'],['02','团队','分工、投入、协作与答辩中的掌握度']]},
  gold: {title:'GOLD / 国金差距诊断', intro:'把“想拿金奖”拆成一组可以补齐、核验、复盘的证据动作。先修 P0 闸门，再谈表达上限。', items:[['P0','先过资格','赛道、组别、成员、IP、往届获奖项目'],['P1','补强闭环','痛点—技术—验证—客户/社会成效'],['P2','压缩表达','让每一页只有一个评委能复述的结论']]},
  map: {title:'MAP / 材料完整性地图', intro:'每个数字、专利、客户、实验、荣誉都需要一条回到原始材料的路径。图片版文件会进入视觉复核，而不是被文本解析误判为空。', items:[['01','主张','这句话究竟想让评委相信什么？'],['02','来源','文件、页码、日期、单位、测试条件'],['03','动作','谁在什么时候补齐、复核或删掉？']]},
  camp: {title:'CAMP / 阶段化备赛训练', intro:'GPS 根据比赛阶段和剩余时间排训练：校赛重事实与表达，省赛重证据密度，网评重材料一致性，现场赛重掌握度与问辩。', items:[['DAY 01','冻结','资格 / IP / 成员贡献 / 原始数据'],['DAY 02','成型','一页一结论，逐项对应证据 ID'],['DAY 03','上场','逐页来源、视觉 QA、盲答辩']]}
};
function openPanel(key){
  const d=data[key]; if(!d)return;
  content.innerHTML=`<p class="eyebrow" style="color:#b7d36b">GPS MODULE / ${key.toUpperCase()}</p><h3>${d.title}</h3><p>${d.intro}</p><div class="panel-grid">${d.items.map(x=>`<div class="panel-item"><b>${x[0]}</b><span>${x[1]}</span><small>${x[2]}</small></div>`).join('')}</div><a class="panel-cta" href="https://github.com/leewayworks/guochuang-gps" target="_blank" rel="noreferrer">在 GitHub 查看能力模块 ↗</a>`;
  panel.classList.add('open'); panel.setAttribute('aria-hidden','false');
}
document.querySelectorAll('[data-panel]').forEach(el=>el.addEventListener('click',()=>openPanel(el.dataset.panel)));
function closePanel(){panel.classList.remove('open');panel.setAttribute('aria-hidden','true')}
document.querySelector('.panel-close').addEventListener('click',closePanel);
panel.addEventListener('click',e=>{if(e.target===panel)closePanel()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closePanel()});
