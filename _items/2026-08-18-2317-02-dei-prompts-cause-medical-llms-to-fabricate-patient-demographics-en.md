---
layout: item
title: "DEI Prompts Cause Medical LLMs to Fabricate Patient Demographics"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 8.0
link: "https://arxiv.org/abs/2608.15254"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
A controlled study of 47 medical language models, four benchmarks, and 376,000 scored responses found that appending a single DEI-focused sentence to a medical question raised the rate of fabricated patient demographic details \(race, socioeconomic status, sex\) from 0.7% to 33.1%, a 47-fold increase observed in all 47 models tested. The effect was attributed to the equity-framed content itself rather than to added prompt length, remaining 18 times larger than a length-matched control \(p=1.4x10^-14\). Most fabricated content took the form of general population statements that left the model&\#x27;s answer unchanged, but in 0.25% to 2.4% of responses the invented demographic attached to the specific patient and changed the selected clinical answer, with 99.8% of those changes moving toward the incorrect option. The magnitude of the effect varied with exact phrasing, ranging from 14% to 56% across variants. The study treats these as measured model errors under laboratory evaluation, not as clinical guidance, and the paper does not indicate a disclosure process since this is an independent research measurement rather than a vendor-reported vulnerability.

rss · arXiv cs.AI · Aug 18, 04:00

**「Background」** Clinical-AI guidance has increasingly recommended prompting language models to reason with explicit attention to diversity, equity, and inclusion, on the assumption that this improves fairness in outputs without otherwise altering clinical reasoning. This assumption was trusted because DEI-style instructions are framed as a general reasoning nudge rather than a request for patient-specific information, so their side effects on factual content were not systematically measured before this study.

**「Who is exposed」** This affects any organisation using medical LLMs that have been instructed, via system prompt or user-facing guidance, to reason with DEI or equity considerations, particularly where model outputs feed into documentation or decision support without a review step. Teams should check whether their clinical prompting templates include equity or bias-mitigation instructions, and whether any downstream logic parses model output for patient attributes not present in the original input, since the effect was demonstrated across a broad and diverse set of 47 models rather than being specific to one vendor or architecture.

**「Mitigation」** No model fix is described; the paper recommends treating the flagged outputs as errors to guard against rather than adopting them as clinical guidance, which implies auditing existing DEI-style prompting instructions and adding checks that reject or flag model-introduced patient attributes not present in the source question.

**Tags**: `#healthcare AI`, `#prompt engineering`, `#bias and fairness`, `#model evaluation`, `#medical LLMs`
