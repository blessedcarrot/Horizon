---
layout: item
title: "LiquidAI Releases Q4_0 GGUFs Trained via Quantization-Aware Distillation"
date: 2026-08-19 21:56:30 +0000
lang: en
theme: practice
theme_name: "Practice"
score: 7.0
link: "https://huggingface.co/blog/LiquidAI/qad"
source: "Hugging Face Blog"
edition_url: "/2026/08/19/2156-summary-en.html"
edition_title: "2026-08-19 21:56 UTC"
enriched: true
---
LiquidAI released Q4\_0 GGUF checkpoints for four LFM2.5 models \(230M, 350M, 1.2B-Instruct, 2.6B\) trained with quantization-aware distillation \(QAD\), where a high-precision teacher distills directly into the quantized student rather than quantizing after training. The checkpoints keep the same memory footprint and decode throughput as standard Q4\_0 GGUFs but retain 96.5-97.4% of BF16 accuracy across a benchmark suite covering GPQA Diamond, MMLU-Pro, IFEval, IFBench, Multi-IF, BFCLv4, and a scale-appropriate math eval \(GSM8K or AIME25\), averaged over five repeats. On real edge hardware \(MacBook Pro, NucBox EVO-X2, Samsung Galaxy S26 Ultra, Raspberry Pi 5\), the 230M/350M QAD Q4\_0 checkpoints match Q5\_K\_M quality at 4-33% higher decode throughput, and the 1.2B/2.6B checkpoints match Q4\_K\_M quality at 3-14% higher throughput, also matching Unsloth&\#x27;s UD-Q4\_K\_XL PTQ checkpoint where comparable. The checkpoints are available now on Hugging Face and run with llama.cpp or any GGUF Q4\_0-compatible runtime.

rss · Hugging Face Blog · Aug 19, 13:48

**「Background」** Post-training quantization \(PTQ\) to formats like GGUF Q4\_0 shrinks model memory footprint and speeds up inference, but it typically costs some accuracy relative to the original BF16 or F16 weights, and that gap tends to grow as models get smaller. Quantization-aware distillation addresses this by training the quantized model directly against a higher-precision teacher, rather than quantizing an already-trained model after the fact. LFM2.5 is Liquid AI&\#x27;s edge-oriented model family, spanning sizes from 230M to 2.6B parameters, targeting deployment on constrained hardware such as laptops, mini-PCs, phones, and single-board computers.

**「What This Changes」** Teams deploying small LFM2.5 models on edge or CPU-constrained hardware can swap in these QAD Q4\_0 checkpoints directly, in place of standard PTQ Q4\_0 or even higher-bit quantizations like Q5\_K\_M or Q4\_K\_M, to get comparable quality at lower memory and higher throughput. This is specifically useful for on-device inference scenarios \(phones, Raspberry Pi, mini PCs\) where model size and decode speed are hard constraints and where PTQ accuracy loss has been the blocker to using the smallest quantization tier. It does not apply beyond the four released LFM2.5 sizes, since QAD requires training-time access to a teacher model, not a drop-in quantization recipe for arbitrary existing models.

**「Caveats」** All numbers are self-reported by LiquidAI with no independent verification, and the source excerpt does not give exact per-benchmark score deltas or variance beyond the aggregate retention percentages. Hardware throughput comparisons are limited to the four listed devices and to llama.cpp-based GGUF inference; results may not generalize to other runtimes or quantization formats.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/blog/LiquidAI/qad">LFM 2 . 5 Q4\_0 Checkpoints from Quantization - Aware Distillation</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#model-distillation`, `#open-weight-release`, `#LLM-benchmarks`, `#edge-inference`
