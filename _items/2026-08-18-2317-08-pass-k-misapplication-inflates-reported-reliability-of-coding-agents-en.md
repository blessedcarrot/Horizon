---
layout: item
title: "Pass@k Misapplication Inflates Reported Reliability of Coding Agents"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.14711"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
A paper finds that current implementations of the pass@k benchmark for AI coding agents set n to the number of unit tests in a single submission rather than the number of independent rollout attempts, conflating test-suite size with attempt independence. In a synthetic multi-rollout benchmark, this misapplication inflates reported reliability scores by 0.85 to 0.97 in absolute terms \(0.96-0.98 reported versus 0.00-0.12 corrected\), and a cheap single-rollout proxy fails to substitute for repeated runs \(Spearman rho = 0.417\). The authors propose reliability@k, applying the same estimator with n as independent rollouts and c as fully-passing rollouts per task-agent pair, and additionally propose security-adjusted reliability@k, which counts only rollouts that are both functionally correct and free of high-severity insecure code patterns. A preliminary 5-task SWE-bench Verified pilot found macro-averaged hidden-test pass rate of 0.80 versus strict task resolution of 0.20, and an initial live-API test with three agents found the security adjustment did not change rankings under the scanner and threshold used, so the authors present it as a proposed complementary lens requiring better-powered future evaluation.

rss · arXiv cs.AI · Aug 18, 04:00

**「Background」** Pass@k, originally defined by Chen et al. \(2021\) for single-function code completion, has been adopted broadly across agentic coding benchmarks as a shorthand for how reliably an agent solves a task across repeated attempts. Organisations selecting or evaluating coding agents often treat published pass@k figures as a proxy for real-world reliability without checking how the underlying n and c values were actually computed.

**「Exposure」** This affects any team that selects, ranks, or reports on coding agents using published pass@k scores from current agentic benchmarks, since the paper demonstrates the metric as commonly implemented can overstate reliability by up to 0.97 absolute in a synthetic setting and shows a similar gap \(0.80 hidden-test pass rate versus 0.20 strict resolution\) in a small real-repository pilot. To check exposure, teams should inspect whether a benchmark&\#x27;s pass@k computes n from independent rollout attempts or from the number of unit tests in a single submission, and should treat single-rollout proxies as unreliable substitutes for repeated-run evaluation. The security-adjusted variant is relevant to teams relying on functional-correctness benchmarks as a proxy for code security, though its ranking impact was only tested with three agents in a preliminary live-API run.

**「Mitigation」** The paper proposes reliability@k as a corrected, properly specified replacement for pass@k, and security-adjusted reliability@k as a complementary check on code security, but both are newly proposed metrics rather than deployed fixes, and the security-adjusted variant&\#x27;s discriminative power still needs evaluation at larger scale. Teams evaluating coding agents in the meantime should request or reproduce independent-rollout-based reliability figures rather than relying on vendor-reported pass@k as published.

**Tags**: `#benchmark validity`, `#coding agents`, `#reliability measurement`, `#security evaluation`, `#agentic AI`
