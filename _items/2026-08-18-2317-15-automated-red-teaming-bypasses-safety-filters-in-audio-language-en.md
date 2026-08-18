---
layout: item
title: "Automated red-teaming bypasses safety filters in audio-language models"
date: 2026-08-18 23:17:09 +0000
lang: en
theme: reliability-assurance
theme_name: "Reliability & Assurance"
score: 7.0
link: "https://arxiv.org/abs/2608.15578"
source: "arXiv cs.AI"
edition_url: "/2026/08/18/2317-summary-en.html"
edition_title: "2026-08-18 23:17 UTC"
enriched: true
---
Researchers present ARENA, a closed-loop automated red-teaming framework that pairs text queries with audio inputs to elicit harmful behavior from large audio-language models even when the text alone is judged safe. The controller is trained on a 2,000-case text-audio dataset, using MD-Judge for training rewards and a separate Llama Guard 3 evaluator to label final outcomes. On 520 held-out AdvBench objectives, ARENA reports frame/prompt success rates of 87.9/100.0% on Audio Flamingo 3, 71.5/96.3% on Qwen2-Audio, 68.1/100.0% on MiMo-Audio, and 75.4/98.5% on GPTAudio. Ablation results indicate that feedback-based refinement and audio-variant search account for a substantial share of the attack discovery gains. The work is a research demonstration; no disclosure timeline or vendor remediation status is given.

rss · arXiv cs.AI · Aug 18, 04:00

**「Why text-only safety checks were assumed sufficient」** Large audio-language models extend safety review beyond text prompts by accepting speech, music, and environmental sound as direct inputs, but most existing red-teaming and content filters were built around text-only threat models. The assumption was that a text query judged safe in isolation would remain safe when paired with audio, since safety classifiers typically inspect transcribed or textual signals rather than the joint text-audio combination. ARENA tests this assumption directly by training a controller to find audio variants that push jointly benign-looking text-audio pairs toward harmful outputs, using MD-Judge for training feedback and a separate Llama Guard 3 evaluator to label final results.

**「Who is exposed」** This affects organisations deploying large audio-language models, specifically Audio Flamingo 3, Qwen2-Audio, MiMo-Audio, and GPTAudio as tested, or systems built on similar joint text-audio architectures with text-only safety filtering. Exposure is limited to voice or audio-interface products where the safety layer screens the text transcript or prompt rather than the full multimodal input; text-only chat systems are not implicated. Teams should check whether their safety evaluation pipeline inspects audio content jointly with text, or relies solely on transcribed or text-side moderation, since that is the specific gap the attack exploits.

**「Mitigation」** No fix is described for the affected models; the paper does not report vendor patches or disclosure outcomes. A compensating control is to evaluate safety filters against joint audio-text inputs rather than text-only transcripts, and to treat audio-grounded red-teaming as a required part of pre-deployment testing for any LALM-based product.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2608.15578">ARENA: Automated Red - Teaming for Large Audio Language Models</a></li>

</ul>
</details>

**Tags**: `#red-teaming`, `#audio-language-models`, `#multimodal-safety`, `#jailbreaks`, `#AI-security`
