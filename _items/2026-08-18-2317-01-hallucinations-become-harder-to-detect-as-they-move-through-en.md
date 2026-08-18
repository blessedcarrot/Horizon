---
layout: item
title: "Hallucinations Become Harder to Detect as They Move Through Agent Pipelines"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 8.0
link: "https://arxiv.org/abs/2608.14588"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
A laboratory study models how hallucinations injected into a multi-agent LLM pipeline change form as they pass through stages, moving from raw factual errors to derived computations, then narrative prose, then editorially approved conclusions, becoming progressively harder to catch. The authors formalize this as a first-order Markov process with measured per-boundary escape probabilities of 24.6%, 48.3%, and 89.3%, and test it on 346 automatically injected hallucinations in a 4-agent financial analysis pipeline built on FinanceBench. Using gpt-4o as detector, detection accuracy drops from 72.0% at Stage 1 to 50.9% at Stage 4, with 23.7% of hallucinations surviving completely undetected in the final output; even the strongest model tested, Qwen3.5-397B-A17B, shows a projected Stage 4 detection ceiling of roughly 60-65%. The study also finds that inserting verification gates between stages using the same RAG verification tool cuts hallucination survival from 58.4% to 16.2%, compared to only a 2.3 percentage point improvement from checking once at the end of the pipeline.

rss · arXiv cs.AI · Aug 18, 04:00

**「Background」** Multi-agent LLM pipelines chain specialized agents \(extraction, computation, narrative generation, editorial review\) without verification at each handoff, on the assumption that a later agent or a final review step will catch errors introduced upstream. This assumption underlies many production designs for tasks like financial analysis, where speed and modularity are prioritized over per-stage checking, and where end-of-pipeline review is often treated as sufficient quality control.

**「Exposure」** This concerns any organization running sequential multi-agent LLM architectures, particularly in financial analysis or other domains where raw data passes through multiple transformation stages before reaching a human reviewer or downstream decision system. Teams should check whether their pipelines rely on a single verification pass at the end rather than checks placed at each stage boundary, and whether their review process assumes that errors remain in an easily checkable form as they move through the pipeline. The findings come from a controlled experiment on one financial pipeline design and one benchmark \(FinanceBench\) with injected hallucinations, so exposure is demonstrated in that setting rather than confirmed across arbitrary pipeline architectures or domains.

**「Mitigation」** The study&\#x27;s own results indicate that placing verification gates at early stage boundaries, particularly the first handoff where 75.4% of hallucinations are still catchable, is substantially more effective than end-of-pipeline checking alone, which produced only a 2.3 percentage point improvement in the tested pipeline. No universal fix is claimed; the authors present this as a resource-allocation strategy for verification effort rather than a deployed tool.

**Tags**: `#multi-agent systems`, `#hallucination detection`, `#LLM pipelines`, `#financial AI`, `#error propagation`
