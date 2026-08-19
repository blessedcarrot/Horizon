---
layout: item
title: "Random Splits Inflate Financial News NLP Benchmarks 1.1x-6.5x"
date: 2026-08-19 21:56:30 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.17223"
source: "arXiv cs.CL"
edition_url: "/2026/08/19/2156-summary-en.html"
edition_title: "2026-08-19 21:56 UTC"
enriched: true
---
An empirical audit of 16 model architectures for financial-news direction prediction, spanning TF-IDF, MiniLM, FinBERT, fine-tuned RoBERTa-large and DeBERTa-v3-large, and LLM probes of Llama-3 and Qwen2.5, found that random train-test splits inflate MCC scores by 1.1x to 6.5x compared to chronological splits, with the inflation tracking model capacity and feature richness. The audit used a 49,799-article corpus, and found that end-to-end FinBERT fine-tuning re-amplifies rather than closes this leakage gap, with a size-matched inflation ratio of 1.75x. Under strict chronological evaluation, only merger and acquisition \(M&amp;A\) event coverage retained a positive, statistically significant signal \(TF-IDF MCC of 0.138 train-only, 0.068 under train-plus-validation refit, permutation p &lt; 10^-3\), and this signal did not transfer to a separate 2009-2020 U.S. news corpus, indicating it is specific to the 2024-2025 European-tilted M&amp;A dataset used rather than a general predictor. The paper is a preprint and the authors call for leakage audits to become a required disclosure for financial-NLP benchmarks.

rss · arXiv cs.CL · Aug 19, 04:00

**「Background」** Financial-news direction prediction is a widely used NLP benchmark for evaluating whether text signals precede price moves, and reported performance gains are often taken as evidence that a model captures predictive information. Random train-test splitting is a standard machine learning practice, but for time-ordered financial data it can let a model see future vocabulary, events, or stale correlations during training that would not be available in a real deployment, a problem known as temporal leakage.

**「Who is exposed」** This concerns organisations or teams that develop, benchmark, or purchase financial-news NLP models for trading, risk scoring, or research signals, particularly where model evaluation relied on randomly shuffled train-test splits rather than strict chronological holdout. Teams should check their own backtesting and evaluation pipelines for split methodology, and treat benchmark-reported accuracy or MCC figures for financial-news classifiers with caution unless chronological evaluation and refit procedures are explicitly documented. The finding is bounded to the financial-news direction prediction niche and to the architectures and corpora tested; it does not establish that all financial NLP benchmarks are affected, but it demonstrates the failure mode is present across a wide range of model types including modern LLMs.

**「Mitigation」** There is no software fix since this is a methodological flaw in evaluation design rather than a software defect; the compensating control is to require chronological train-test splitting and leakage audits as a standard disclosure when validating financial-news NLP models, and to treat any performance claim based on random splits as unverified until re-tested chronologically.

**Tags**: `#temporal leakage`, `#financial NLP`, `#benchmark validity`, `#model evaluation`, `#LLM fine-tuning`
