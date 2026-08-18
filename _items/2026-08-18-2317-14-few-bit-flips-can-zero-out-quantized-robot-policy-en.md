---
layout: item
title: "Few Bit Flips Can Zero Out Quantized Robot Policy Success"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.15475"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
Researchers demonstrate a bit-flip attack against quantized Vision-Language-Action \(VLA\) models, showing that a small number of gradient-selected INT8 bit flips, delivered in a manner consistent with Rowhammer-style hardware faults, can reduce closed-loop task success to 0%. The required number of flips depends heavily on the action-decoding head: direct regression and token-based policies break with 1 to 5 flips, while the flow-matching policies tested \(including pi-zero\) needed roughly 100 to 300 flips, or about 100 flips once the researchers&\#x27; fixed-direction manifold-escape loss was applied. Hundreds of random bit flips, by contrast, were harmless, indicating the attack depends on precise weight selection rather than general fault density. On a direct-head model, protecting 3.1% of weights preserved 60% success at 100 flips, and protecting 5.3% raised the open-loop break threshold from 3 to 100 flips. In physical robot trials, emulated 100-flip attacks produced 0 of 20 successes versus 14 of 20 clean and 16 of 20 with global random flips, and the work is presented as a laboratory demonstration with code released as ancillary material.

rss · arXiv cs.AI · Aug 18, 04:00

**「The assumption under test」** Quantization to INT8 is widely used to make VLA models deployable on embedded robot hardware, and the safety case for such deployments has generally rested on model-level accuracy evaluations rather than on the integrity of the underlying memory bits. Rowhammer-style fault injection has been studied for years as a way to flip bits in DRAM without direct write access, but its implications for embodied AI action generation, where a single corrupted layer can directly cause physical actuation failure, had not been previously demonstrated.

**「Who should check their setup」** This applies to organisations running quantized VLA models for robotic control, particularly where the model is deployed on shared or physically accessible hardware where Rowhammer-class memory fault injection is feasible. Exposure varies by action-decoding architecture: systems using direct regression or token-based action heads are far more vulnerable \(needing only 1 to 5 targeted bit flips\) than those using flow-matching policies \(needing roughly 100 to 300\). Teams should check which action-head family their deployed model uses, whether the deployment hardware has Rowhammer mitigations, and whether any weight-criticality or bit-level protection has been applied to action-generating layers. The attack requires an adversary capable of inducing targeted bit flips in device memory, a real but non-trivial precondition that is not present in every deployment.

**「What reduces the risk」** The paper&\#x27;s own partial mitigation, protecting a small fraction of weights \(3.1% to 5.3% in the direct-head case\), meaningfully raises the flip budget needed to break the model and preserves majority task success under attack, but this is a research proposal rather than a deployed or vendor-shipped fix. Compensating controls in the meantime include standard hardware-level Rowhammer defenses \(ECC memory, refresh-rate hardening\) and avoiding co-located, untrusted workloads on the same memory hardware as safety-critical action models.

**Tags**: `#adversarial-robustness`, `#VLA-models`, `#hardware-security`, `#model-quantization`, `#robotics-safety`
