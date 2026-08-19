---
layout: item
title: "LLM Prompting Recovers Institution-Specific PHI Missed by De-identification Tools"
date: 2026-08-19 21:56:30 +0000
lang: en
theme: practice
theme_name: "Practice"
score: 7.0
link: "https://arxiv.org/abs/2608.17051"
source: "arXiv cs.CL"
edition_url: "/2026/08/19/2156-summary-en.html"
edition_title: "2026-08-19 21:56 UTC"
enriched: true
---
Researchers benchmarked eight LLMs against two purpose-built de-identification systems \(Stanford TiDE, OpenMed PII\) and two pattern-based baselines on 100 annotated pediatric oncology notes from Texas Children&\#x27;s Hospital, containing 5,322 PHI spans. Under a HIPAA-aligned baseline prompt the LLMs already outperformed the purpose-built tools \(best F1=0.918 vs. TiDE&\#x27;s 0.779\), with the advantage concentrated in contextually determined PHI categories such as hospital abbreviations, building names, and internal codes. Adding explicit instructions naming the institutional categories the model had missed recovered 79% \(48 of 61\) of those misses, and a further instruction discouraging over-redaction restored precision without sacrificing recall. Testing 14 multi-agent and ensemble configurations found none beat calibrated single-pass prompting \(F1 0.906-0.907\), and the LLM outputs also surfaced 414 candidate annotation gaps in the gold-standard labels, of which re-annotation confirmed 227 as genuine PHI spans that the original human annotation had missed. Against this corrected reference, the final prompt reached recall=0.981 and F1=0.907.

rss · arXiv cs.CL · Aug 19, 04:00

**「Background」** De-identification of clinical notes for secondary research use typically relies on purpose-built NLP systems trained to detect HIPAA-defined PHI categories like names, dates, and addresses. These systems and the human annotations used to evaluate them tend to struggle with institutionally situated PHI, information whose identifying status depends on local context, such as a building name or an internal patient code that only carries risk within a specific hospital&\#x27;s operational vocabulary.

**「What This Changes」** Teams building de-identification pipelines for clinical text can treat institution-specific prompt engineering, rather than model architecture or agentic orchestration, as the primary lever for closing coverage gaps: naming the specific local categories a model misses in the prompt recovered most of those misses in this study. The finding that LLM outputs surfaced annotation gaps the human gold standard had missed suggests LLMs can also be used to audit and improve existing de-identification benchmarks and reference annotations, not just to replace the detection system itself. This applies specifically to single institution deployments where local naming conventions \(buildings, codes, abbreviations\) are known and can be enumerated in a prompt; the calibrated single-pass approach was also cheaper and as effective as more complex multi-agent ensembles.

**「Caveats」** The evaluation is limited to 100 pediatric oncology notes from one institution, so generalization to other specialties, note types, or hospitals with different local naming conventions is unverified. LLM inference also costs more per note than the purpose-built systems it outperformed, a tradeoff the authors frame as buying reference-standard auditing capability rather than raw cost savings.

**Tags**: `#de-identification`, `#clinical NLP`, `#LLM prompting`, `#healthcare data privacy`, `#benchmark evaluation`
