---
layout: item
title: "Benchmark Finds Cross-Lingual Safety Gaps in LLMs for Indian Languages"
date: 2026-08-21 21:49:37 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.18131"
source: "arXiv cs.AI"
edition_url: "/2026/08/21/2149-summary-en.html"
edition_title: "2026-08-21 21:49 UTC"
enriched: true
---
Researchers introduce INCLUDE, a benchmark of 2,604 prompts across English, Hindi, Bengali, Marathi, Tamil, and Hinglish designed to measure Indian-centric socio-cultural bias in LLM outputs. Testing ten open- and closed-source models produced 14,988 bias scores, showing that safety behavior varies substantially by language rather than holding constant across them. Bengali produced the highest average bias score among open-source models, while English showed a reversal: lowest bias in open-source models but highest bias in closed-source models. The abstract as supplied does not report specific failure rates by model name or disclosure status, and the paper is a new arXiv submission that has not been independently replicated.

rss · arXiv cs.AI · Aug 21, 04:00

**「Why English-centric safety training was trusted」** Safety alignment for most widely deployed LLMs is trained and evaluated predominantly on English data, on the assumption that resulting guardrails transfer reasonably well to other languages the model can process. This assumption underpins deployment of voice assistants and dialogue systems in linguistically diverse markets, including India, where systems are expected to serve users in multiple regional languages without separate safety validation for each.

**「Who should check their language coverage」** Organizations deploying LLM-based voice assistants, chatbots, or dialogue systems to users who interact in Hindi, Bengali, Marathi, Tamil, or Hinglish are in scope, particularly if safety evaluation was only performed in English before launch. Both open-source and closed-source model deployments are affected, though the study found the direction of the effect differs: open-source models showed lower bias in English and higher in Bengali, while closed-source models showed the reverse pattern with English producing the highest bias. Teams should check which languages their safety evaluation suite actually covers and whether bias or harm testing has been repeated per deployed language rather than assumed to generalize from English results.

**「What reduces the risk」** No fix is implied by the paper itself; INCLUDE is presented as a diagnostic benchmark rather than a remediation. The practical compensating control is to run per-language bias and safety evaluation, including for code-mixed languages like Hinglish, before relying on English-trained safety alignment to hold in other deployment languages.

**Tags**: `#LLM safety alignment`, `#multilingual NLP`, `#bias benchmarking`, `#cross-lingual robustness`, `#non-English deployment risk`
