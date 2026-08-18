---
layout: item
title: "State-Semantic Injection Proposed as New Attack Vector for Embodied Agents"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.16806"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
The paper proposes state-semantic injection as an attack vector against LLM-driven embodied agents, targeting the natural-language state representations \(scene descriptions, object attributes, spatial relations, execution feedback\) that these systems feed into their planning models. It frames this as an extension of prompt injection to the state channel rather than the instruction channel, relevant to architectures such as SayCan, Code as Policies, ProgPrompt, and VoxPoser, and to vision-language-action models like PaLM-E, RT-2, and GR00T N1. The abstract available here describes the architectural background and motivation for the attack surface but does not itself contain the reported experimental results, attack success rates, or the specific agent implementations tested, so the strength of empirical validation cannot be assessed from this excerpt alone.

rss · arXiv cs.AI · Aug 18, 04:00

**「Why state summaries are trusted inputs」** LLM-driven embodied agent architectures such as SayCan, Code as Policies, and VoxPoser rely on natural-language or programmatic summaries of scene state, object attributes, spatial relations, and execution feedback to ground task planning before handing off to skill libraries or motion controllers. These state representations are generally treated as internal telemetry produced by perception pipelines rather than as untrusted input, so they are typically passed to the planning LLM without the kind of adversarial filtering applied to user-facing prompts. This assumption holds only as long as the perception-to-state pipeline cannot be manipulated by an outside party, an assumption the paper&\#x27;s proposed attack vector calls into question.

**「Who Is Exposed」** Exposure applies to teams building or deploying LLM-driven robotic or embodied agents that convert perception output \(scene graphs, object lists, spatial descriptions, sensor summaries\) into natural-language state text before passing it to an LLM for planning. Organizations using or adapting architectures in the SayCan, Code as Policies, ProgPrompt, or VoxPoser family, or vision-language-action models like PaLM-E, RT-2, or GR00T N1, should check whether their state-generation pipeline treats perception-derived text as trusted input to the planner without validation or sanitization. Systems where state descriptions originate from sensors, third-party perception modules, or shared/multi-agent environments are the most plausible targets, since an adversary able to influence perceived scene content could potentially inject instructions through that channel rather than through the user prompt.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/html/2601.20334">Demonstration-Free Robotic Control via LLM Agents</a></li>
<li><a href="https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1605405/full">Frontiers | Agentic LLM-based robotic systems for real-world applications: a review on their agenticness and ethics</a></li>
<li><a href="https://arxiv.org/html/2606.30111">Automating the Design of Embodied Agent Architectures</a></li>

</ul>
</details>

**Tags**: `#prompt injection`, `#embodied agents`, `#LLM agent security`, `#robotics`, `#adversarial attacks`
