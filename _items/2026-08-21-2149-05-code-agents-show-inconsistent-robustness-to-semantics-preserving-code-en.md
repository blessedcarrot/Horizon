---
layout: item
title: "Code Agents Show Inconsistent Robustness to Semantics-Preserving Code Rewrites"
date: 2026-08-21 21:49:37 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.18389"
source: "arXiv cs.SE"
edition_url: "/2026/08/21/2149-summary-en.html"
edition_title: "2026-08-21 21:49 UTC"
enriched: true
---
Researchers evaluated two agentic scaffolds \(mini-SWE agent and OpenCode\), each backed by one of four frontier models \(Claude Opus 4.5, Kimi K2.5, MiniMax M2.5, and Qwen 3.6-27B\), on issue-resolution tasks drawn from SWE-bench Verified and SWE-bench Pro. Repository code was rewritten using semantics-preserving transformations, including control-flow rewrites, dead-code injection, and identifier renaming, and each agent was run multiple times on both unperturbed and perturbed variants of the same instance to produce paired resolve-rate estimates. Across 16 model-scaffold-dataset configurations, the study found a mean resolve-rate drop of up to 6.7 percentage points in the most affected configurations, with statistically significant degradation in 6 of the 16 configurations. Robustness rankings did not hold across scaffolds: Qwen was among the most robust under mini-SWE agent on SWE-bench Verified but the most brittle under OpenCode, and the simpler mini-SWE agent scaffold was more robust overall than OpenCode. The paper is a preprint \(arXiv, cross-listed\) and does not indicate independent replication or vendor disclosure status.

rss · arXiv cs.SE · Aug 21, 04:00

**「Background」** AI code agents are increasingly used to autonomously resolve repository-level software issues, and their evaluation typically relies on fixed benchmarks such as SWE-bench, which assumes that a model&\#x27;s resolve rate reflects genuine problem-solving competence rather than sensitivity to incidental code phrasing. It is generally assumed that transformations which preserve program semantics, such as renaming variables or rewriting control flow, should not materially affect an agent&\#x27;s ability to locate and fix a bug, since the underlying logic is unchanged.

**「Exposure」** This affects organisations deploying agentic coding tools built on the specific scaffolds and models tested, mini-SWE agent or OpenCode paired with Claude Opus 4.5, Kimi K2.5, MiniMax M2.5, or Qwen 3.6-27B, for repository-level automation such as automated issue resolution or bug triage. Teams should check which scaffold and model combination they run in production, since robustness does not transfer predictably between scaffolds even for the same underlying model. Exposure is demonstrated only on SWE-bench Verified and SWE-bench Pro tasks in a research setting; whether the same degradation pattern appears on other codebases, languages, or agent architectures is not established by this study.

**「Mitigation」** No fix is proposed in the paper; the authors report the phenomenon as a benchmarking finding rather than a patched vulnerability. Organisations relying on code agents may reduce risk by testing agent reliability against superficial code variants of their own repositories before deployment and by preferring the simpler scaffold configuration shown here to be comparatively more robust, pending further independent verification.

**Tags**: `#code agents`, `#robustness evaluation`, `#LLM benchmarking`, `#software engineering automation`, `#agentic AI`
