---
layout: item
title: "Edge-IIoTset Benchmark Leaks Labels Through a Serialisation Artifact"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 8.0
link: "https://arxiv.org/abs/2608.15761"
source: "arXiv cs.LG"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
A study of the Edge-IIoTset benchmark, widely used to report machine-learning intrusion detection results for industrial IoT, finds that near-perfect accuracy figures largely reflect a preprocessing artifact rather than genuine attack detection. Four of seven categorical columns that the dataset&\#x27;s own preprocessing recipe instructs researchers to one-hot encode separate attack from normal traffic with 1.0000 accuracy on their own, because a placeholder value for an absent protocol field is serialised as the string &quot;0&quot; in normal-traffic files and &quot;0.0&quot; in attack files. Under 5-fold by 3-repeat cross-validation, five of six standard classifiers reach exactly 1.0000 accuracy and the sixth reaches 0.99998; label, ordinal and frequency encoding all leak the same way. Once the artifact is corrected, naive Bayes accuracy drops by 0.3005 macro-F1 and the strongest remaining model settles at 0.9503. The authors rebuild the benchmark from raw captures as AgriEdge \(1,276,122 rows, five devices with full attribution\), where no column separates the classes above 0.0288 accuracy, and a leave-one-device-out test shows random forest performance falling from 0.9988 to 0.5083 balanced accuracy at the perception/actuation boundary.

rss · arXiv cs.LG · Aug 18, 04:00

**「Background」** Edge-IIoTset has served as the reference benchmark for evaluating machine-learning intrusion detection systems in industrial IoT settings, and papers reporting scores above 99% on it have been treated as evidence that such models generalise to real attack detection. The dataset&\#x27;s distributed preprocessing recipe, followed uncritically by downstream researchers, was assumed to produce features reflecting network behaviour rather than artifacts of how the data files were built.

**「Who Is Affected」** This affects any organisation or researcher that trained, validated, or cited intrusion detection performance against the Edge-IIoTset benchmark using its standard preprocessing recipe, including one-hot, label, ordinal or frequency encoding of the flagged categorical columns. Teams should check whether models deployed in production, or claims made about IDS efficacy in vendor material or research, rely on Edge-IIoTset accuracy figures, and whether their own preprocessing pipeline reproduces the placeholder-string difference between normal and attack branches described here. Exposure is limited to work built directly on this dataset&\#x27;s curated subsets; it does not indicate a flaw in deployed intrusion detection systems generally.

**「Mitigation」** The authors provide a corrected preprocessing protocol that removes the leaking placeholder artifact, and a rebuilt benchmark, AgriEdge, constructed from raw captures with uniform parsing and full device attribution. Organisations relying on Edge-IIoTset results should re-audit their training and evaluation pipelines against the corrected protocol or migrate benchmarking to AgriEdge before citing or acting on prior accuracy claims.

**Tags**: `#benchmark contamination`, `#intrusion detection`, `#IIoT security`, `#dataset leakage`, `#ML evaluation methodology`
