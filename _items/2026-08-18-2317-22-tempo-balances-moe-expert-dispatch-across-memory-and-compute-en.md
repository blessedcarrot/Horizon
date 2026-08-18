---
layout: item
title: "TEMPO Balances MoE Expert Dispatch Across Memory and Compute Regimes"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: practice
theme_name: "Practice"
score: 8.0
link: "https://arxiv.org/abs/2608.13057"
source: "arXiv cs.CL"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
This paper measures expert-parallel \(EP\) MoE dispatch cost on two datacenter GPU generations and finds it is bimodal rather than linear in tokens or activated experts as assumed by existing dispatchers \(EPLB, LPLB, UltraEP, METRO\). Below roughly 156-168 tokens \(n\*\), cost is dominated by HBM weight streaming and scales with activated replicas, not token count; above that threshold, grouped GEMM rounds tokens into 128-tile blocks, so splitting an expert adds padded compute. The authors model this with a max-affine cost function and show that on recorded decode batches, different dispatch proxies disagree by 1.4-1.6x in modeled block time \(p95 up to 1.7x\), with the winning proxy flipping depending on regime. They formalize per-batch dispatch as a fixed-charge makespan problem \(NP-hard in general, polynomial in degenerate cases\) and present TEMPO, a millisecond-scale makespan-aware dispatcher integrated into SGLang out-of-process. On an 8-GPU testbed, TEMPO stays within 1% of the best fixed baseline everywhere and beats it by up to 15.5% when regimes mix; end-to-end on a second testbed, Qwen3-235B gains 4-6% throughput and about 15.6% lower p99 latency in the regime where TEMPO is expected to win, while DeepSeek-V3, which is communication-dominated, shows only the mechanism&\#x27;s overhead with no gain.

rss · arXiv cs.CL · Aug 18, 04:00

**「Background」** In expert-parallel MoE serving, each transformer layer must wait for the slowest GPU to finish its assigned experts before proceeding, so load balancing across GPUs directly affects tail latency and throughput. Existing dispatchers assign work by balancing either token counts or activated-expert counts per GPU, implicitly assuming per-GPU cost scales linearly with whichever quantity they balance.

**「What this changes」** Teams operating large MoE inference deployments with expert parallelism can use the paper&\#x27;s phase diagram to predict, before deployment, whether a makespan-aware dispatcher like TEMPO will help their specific model and batch profile, rather than assuming any load balancer improvement is universal. It also gives a concrete diagnostic \(the n\* threshold and max-affine cost model\) for checking whether a deployment sits in the memory-bound, compute-bound, or mixed regime, which existing token- or expert-count balancing heuristics do not distinguish. The practical payoff \(4-6% throughput, ~15.6% p99 latency reduction\) is shown specifically for Qwen3-235B in a regime-mixing configuration; deployments dominated by communication, like the tested DeepSeek-V3 setup, should not expect gains from this technique alone.

**「Caveats」** Results are measured on two specific datacenter GPU testbeds \(an 8-GPU microbenchmark and a separate end-to-end testbed\) with two specific models, so the exact thresholds, percentages, and win margins may not transfer to other GPU generations, interconnects, or MoE architectures. The paper itself frames the contribution as a predictive phase diagram rather than a guaranteed win, and explicitly reports a case \(DeepSeek-V3, communication-dominated\) where the mechanism adds cost without measurable benefit.

**Tags**: `#mixture-of-experts`, `#GPU inference`, `#load balancing`, `#expert-parallel serving`, `#LLM systems`
