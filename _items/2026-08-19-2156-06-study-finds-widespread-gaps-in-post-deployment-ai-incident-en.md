---
layout: item
title: "Study Finds Widespread Gaps in Post-Deployment AI Incident Compliance"
date: 2026-08-19 21:56:30 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2605.16281"
source: "arXiv cs.SE"
edition_url: "/2026/08/19/2156-summary-en.html"
edition_title: "2026-08-19 21:56 UTC"
enriched: true
---
This study codes real-world AI incidents from the AI Incident Database, covering 2020 to 2026, against nine post-deployment obligations drawn from the EU AI Act, the NIST AI Risk Management Framework, and the GDPR. It finds that 77.1% of incidents lack evidence of EU AI Act post-market monitoring and 99.6% lack documented Data-Protection Impact Assessment evidence, with 9.8% of incidents non-compliant under two or more regimes simultaneously. The most notable finding is a large gap between incidents detected through internal monitoring versus those detected externally: compliance evidence was present in 87.5% of internally detected incidents versus only 5.3% of externally detected ones under the EU AI Act, and 95.8% versus 58.1% under NIST. The paper proposes a four-phase Proactive AI Governance Compliance Framework \(PAGCF\) covering pre-deployment assessment, continuous monitoring, incident preparedness, and cross-framework verification.

rss · arXiv cs.SE · Aug 19, 04:00

**「The obligations being tested」** Post-deployment governance frameworks such as the EU AI Act&\#x27;s post-market monitoring duty \(Article 72\), the NIST AI Risk Management Framework, and GDPR&\#x27;s Data Protection Impact Assessment requirement are built on the assumption that organisations will detect and document AI failures themselves once systems are in use. These obligations rely on providers maintaining internal monitoring plans and impact assessments as part of technical documentation, with the expectation that this internal visibility functions as the primary safeguard rather than external discovery of harm. The AI Incident Database, an independently maintained public registry of real-world AI harms since 2020, offered the researchers a body of documented cases against which to test whether that assumption holds.

**「Who Is Affected」** This concerns any organisation deploying AI systems that fall under the EU AI Act, relies on the NIST AI Risk Management Framework as a governance reference, or processes personal data subject to GDPR impact assessment requirements. Organisations that depend primarily on internal monitoring to catch AI system failures, rather than treating external reports, user complaints, or media coverage as a primary detection channel, are most exposed to the compliance and documentation gap described here. Relevant checks include whether post-market monitoring logs exist and are retrievable for deployed systems, whether Data-Protection Impact Assessments are completed and current, and whether incident response procedures assume internal detection will catch problems before external parties do.

**「Mitigation」** There is no software fix here since this is a governance and documentation gap rather than a technical vulnerability. The paper&\#x27;s proposed PAGCF framework, and more generally strengthening continuous monitoring capacity and maintaining retrievable compliance documentation for post-market monitoring, incident reporting, and impact assessments, are offered as compensating practices, though these have not been independently validated for effectiveness.

<details><summary>References</summary>
<ul>
<li><a href="https://artificialintelligenceact.eu/article/72/">Article 72: Post-Market Monitoring by Providers and Post-Market Monitoring Plan for High-Risk AI Systems | EU Artificial Intelligence Act</a></li>
<li><a href="https://incidentdatabase.ai/">Welcome to the Artificial Intelligence Incident Database</a></li>

</ul>
</details>

**Tags**: `#AI governance`, `#regulatory compliance`, `#incident reporting`, `#post-deployment monitoring`, `#empirical study`
