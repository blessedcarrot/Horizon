---
layout: item
title: "DAG-Structured Multi-Agent System Fixes LLM Failures on Clinical Trial Coding"
date: 2026-08-19 21:56:30 +0000
lang: en
theme: practice
theme_name: "Practice"
score: 7.0
link: "https://arxiv.org/abs/2608.16890"
source: "arXiv cs.AI"
edition_url: "/2026/08/19/2156-summary-en.html"
edition_title: "2026-08-19 21:56 UTC"
enriched: true
---
A new arXiv paper reports that single-shot LLM code generation for clinical trial dataset creation fails completely: across 11 attempts with five frontier models, none produced a valid subject-level analysis dataset \(ADSL\) under CDISC standards. The authors introduce GxP-Agent, a multi-agent system that encodes regulatory process ordering as a directed acyclic graph, splitting monolithic dataset generation into 15 domain-specific nodes handled by worker agents with pharmaverse skill context, validation gates, and conditional retry. On CDISC-Bench, a new execution-based benchmark built from the FDA pilot submission CDISCPilot01 \(254 subjects, 49 ground-truth ADSL variables\), GxP-Agent with Claude Sonnet 4.6 reaches 100% structural match \(49/49 variables, 254 correct records\) across three independent runs, versus 59.2% for the best retrieval-augmented baseline and 0% for single-agent or flat multi-agent approaches. The same DAG topology lets a weaker model, GPT-4.1, reach 59.2% mean structural match, up from 0% under every other architecture tested. The approach also generalizes to adverse events \(ADAE\), a 9-node branching DAG with 55 variables and 1,191 records, achieving 100% structural match on the first attempt.

rss · arXiv cs.AI · Aug 19, 04:00

**「Background」** Clinical trial programming converts study protocols into analysis-ready datasets that follow CDISC standards, a step required before regulatory submission and one that is currently a manual bottleneck for pharmaceutical companies. This work treats that domain as a stress test for LLM code generation under strict, auditable correctness requirements rather than open-ended coding tasks.

**「What this changes」** The paper is a data point that monolithic LLM code generation can fail totally, not just partially, on structured tasks with rigid domain schemas and process ordering, even for frontier models. The fix it demonstrates, encoding known domain process knowledge as an explicit graph topology with per-node validation gates rather than relying on LLM reasoning to sequence steps, is a pattern teams building agents for other compliance-heavy or schema-heavy generation tasks \(finance, healthcare records, structured regulatory filings\) could adapt. It also shows that decomposition via topology can let a weaker, cheaper model match performance that only a stronger model achieves under simpler architectures, which matters for cost-sensitive deployments.

**「Caveats」** This is a single arXiv preprint with results not independently verified, evaluated on one narrow domain \(CDISC clinical trial datasets\) and one benchmark built from a single FDA pilot submission. The abstract does not detail the retry logic or validation gate design, and the 15-node DAG structure is specific to ADSL generation, so the effort needed to build an equivalent process DAG for a different domain is unclear.

**Tags**: `#LLM agents`, `#clinical trial programming`, `#benchmark`, `#multi-agent systems`, `#regulatory compliance`
