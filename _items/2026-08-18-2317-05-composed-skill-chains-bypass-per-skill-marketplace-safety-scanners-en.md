---
layout: item
title: "Composed skill chains bypass per-skill marketplace safety scanners"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 8.0
link: "https://arxiv.org/abs/2608.16246"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
Researchers present CompoSkill, a framework demonstrating that LLM agent skills which individually pass marketplace safety scanners can be chained into risky compositions that the scanners fail to catch. Using a dual attacker design, a white-box attacker with knowledge of the victim&\#x27;s installed skill pool and a black-box attacker that only knows a role profile and builds a Skill Composition Graph from top marketplace skills, the authors evaluate on CompoSkill-Bench, a benchmark of 1,140 records spanning five threats and six scenarios on OpenClaw and Nanobot. Reported risk Chain Formation Rates reach up to 83.3% in the white-box setting and 80.6% in the black-box setting, with existing skill scanners blocking only a limited fraction of these compositions. The study also reports a bridge-bonus-then-hop-decay pattern, where a bridge skill raises attack success but success declines once a chain exceeds three hops. This is laboratory research using a constructed benchmark rather than an observed incident in a live marketplace.

rss · arXiv cs.AI · Aug 18, 04:00

**「Per-skill certification in agent marketplaces」** Agent marketplaces that let autonomous AI agents install third-party skills typically rely on a scanner that inspects each skill in isolation and certifies the whole ecosystem safe once every individual package passes review. This model assumes that safety is a property of each node in the skill pool, so operators running platforms like OpenClaw or lightweight alternatives such as Nanobot have generally trusted that passing per-skill scans is sufficient to greenlight deployment for long-horizon, multi-step agent workflows.

**「Who is affected」** This concerns operators of agent marketplaces or long-horizon multi-agent deployments that rely on per-skill safety scanning as their primary certification gate, including systems built on or resembling OpenClaw and Nanobot. Organizations should check whether their safety review process evaluates skills only in isolation or also inspects how outputs, capabilities, and side effects can be chained across multiple installed or discoverable skills. Exposure is greatest for platforms that allow agents to autonomously select and combine skills at runtime without a composition-level risk check, and narrower for systems that restrict agents to a small, manually vetted, non-combinable skill set.

**「Mitigation」** No fix is described beyond the paper&\#x27;s implicit recommendation to move certification from node-level scanning to path-level analysis, such as modeling skill composition graphs and screening for high-risk chains rather than only individual packages; compensating controls include limiting chain length, restricting agent autonomy to compose skills freely, and monitoring for bridge-skill patterns that enable longer risky chains.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/HKUDS/nanobot">GitHub - HKUDS/ nanobot : Ultra-lightweight, open -source, self-hosted...</a></li>
<li><a href="https://www.hostinger.com/in/tutorials/openclaw-alternatives/">8 best OpenClaw alternatives for personal AI agents</a></li>

</ul>
</details>

**Tags**: `#agent security`, `#skill marketplaces`, `#compositional risk`, `#LLM agents`, `#supply chain attack`
