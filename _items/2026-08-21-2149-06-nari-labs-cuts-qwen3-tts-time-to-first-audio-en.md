---
layout: item
title: "Nari Labs cuts Qwen3-TTS time-to-first-audio to 34ms on H100"
date: 2026-08-21 21:49:37 +0000
lang: en
theme: practice
theme_name: "Practice"
score: 7.0
link: "https://nari-labs.com/blog/qwen3-tts-speed-cost-frontier/"
source: "toebee"
edition_url: "/2026/08/21/2149-summary-en.html"
edition_title: "2026-08-21 21:49 UTC"
enriched: true
---
Nari Labs published an optimized implementation of Qwen3-TTS, an open-source text-to-speech model, achieving 34ms p95 time-to-first-audio \(TTFA\) at a sustained load of 10 requests per second on a single H100 GPU. The team states that existing open-source serving stacks for this class of model, including vLLM-Omni and SGLang-Omni, are often too slow for production use and run into problems with realtime playback when pushed toward low latency. They open-sourced both the implementation and the benchmark harness, along with a methodology writeup describing how the speedup was achieved.

hackernews · toebee · Aug 21, 15:51 · [Discussion](https://news.ycombinator.com/item?id=49389952)

**「Background」** Qwen3-TTS is an open-source text-to-speech model series from Alibaba&\#x27;s Qwen team, supporting streaming speech generation and voice cloning. In realtime voice applications, time-to-first-audio \(TTFA\) determines how quickly a user hears a response after speaking, and existing open-source serving stacks such as vLLM-Omni and SGLang-Omni often struggle to hit low TTFA without breaking realtime playback. Nari Labs, a group building open-source TTS tooling, set out to optimize Qwen3-TTS specifically for this latency bottleneck.

**「Practical impact」** Teams building realtime voice agents or conversational AI pipelines on server-side GPU infrastructure now have a reference implementation and benchmark for sub-50ms TTFA with an open-source TTS model, rather than having to reverse-engineer serving optimizations from scratch or accept the higher latencies reported for existing Omni-serving stacks. This is most relevant to teams already running Qwen3-TTS or considering it, and to anyone benchmarking their own voice pipeline&\#x27;s TTFA against a concrete, reproducible number on H100. It does not address on-device or edge deployment, which multiple commenters flagged as the harder unsolved problem for mobile and low-power use cases.

**「Limits」** The 34ms figure is specific to one model \(Qwen3-TTS\), one GPU \(H100\), and one load condition \(10 req/s\); it does not establish general applicability to other TTS models or to CPU, mobile, or edge hardware. A practitioner comment also notes that in their own experience with a different omni voice model, pushing TTFA well below 200ms ran into a hard quality wall, suggesting latency and output quality may trade off in ways not fully characterized in this report.

**「Community reaction」** One commenter who has run local voice agents for a year reported never getting below roughly 200ms TTFA on a comparable model without sacrificing quality, and argued there is a quality ceiling many TTS models hit regardless of latency tuning. Another practitioner emphasized that the bigger unsolved problem is cheap, fast on-device inference on phones rather than H100-class hardware, and a third noted that GPT-Realtime-2&\#x27;s eagerness to respond suggests real gains could come from latency engineering like this rather than architectural changes.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/QwenLM/Qwen3-TTS?pubDate=20260331">GitHub - QwenLM/Qwen3-TTS: Qwen3-TTS is an open-source series ...</a></li>

</ul>
</details>

**Tags**: `#text-to-speech`, `#latency-optimization`, `#open-source`, `#inference-serving`, `#voice-agents`
