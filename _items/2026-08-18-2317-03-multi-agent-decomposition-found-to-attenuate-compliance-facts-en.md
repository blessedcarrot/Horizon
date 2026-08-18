---
layout: item
title: "Multi-Agent Decomposition Found to Attenuate Compliance Facts"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 8.0
link: "https://arxiv.org/abs/2608.16055"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
A new benchmark called Fiducia-bench measures whether financial agents escalate, abstain, or leave an audit trail as required by policy, rather than simply whether they complete a task. Across a 626-episode experiment covering 100 KYC/AML task variants, two models, and three architectures, a 32B open-weights model attenuated 0% of policy-relevant facts discovered mid-task under a single-loop baseline, 56% under a fixed pipeline, and 85% under an orchestrator-subagent architecture, all measured at constraint distance 2. A stronger model, gpt-4.1-mini, attenuated only 3-6% of facts under the same conditions, indicating the effect scales inversely with model capability. The same handoff-attenuation mechanism was shown to cause both under-escalation, when a dropped fact was a risk signal, and over-escalation, when the dropped fact was exculpating. The benchmark, tasks, and verification harness are released as open-source; this is a single paper&\#x27;s laboratory result pending independent replication.

rss · arXiv cs.AI · Aug 18, 04:00

**「Background」** Many organisations assume that governance properties validated at the single-agent level, such as correctly escalating suspicious activity or abstaining from unauthorized actions, carry over automatically when that agent is split into a pipeline or orchestrator-subagent architecture for scalability or specialization. This assumption underlies common multi-agent designs in regulated domains like KYC/AML, where escalation obligations and audit trails are legally required rather than optional features.

**「Who Is Exposed」** Organisations running multi-agent financial or compliance workflows, particularly orchestrator-subagent designs where one component discovers a fact and a different component is obligated to act on it, should check whether their architecture passes policy-relevant facts across handoff boundaries intact. Exposure is highest for pipeline and orchestrator designs built on smaller or weaker models; the paper&\#x27;s own data shows a stronger model \(gpt-4.1-mini\) attenuated far fewer facts, suggesting risk is not uniform across model choice. Teams that assume architecture changes are governance-neutral, and that audit or escalation logic tested on a single-agent baseline still holds after decomposition, are the direct audience for this finding. The result is specific to constraint distance 2 in this benchmark&\#x27;s KYC/AML tasks and has not been shown to generalize to other domains or distances.

**「Mitigation」** No fix is proposed beyond the benchmark itself; the authors&\#x27; contribution is a diagnostic tool \(Fiducia-bench, open-source\) rather than a corrective mechanism. Compensating controls suggested by the findings include using stronger models at handoff points, explicitly re-verifying policy-relevant facts at each component boundary, and testing governance behavior after decomposition rather than assuming single-agent test results transfer.

**Tags**: `#multi-agent systems`, `#AI governance`, `#financial compliance`, `#benchmark`, `#KYC/AML`
