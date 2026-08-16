---
layout: default
title: Home
---

<div class="radar-intro" markdown="1">

**Early-warning radar for AI and agentic-AI developments.** Every 12 hours it pulls from research feeds, vendor blogs, developer communities and trending repositories, scores each item 0–10 for significance with Claude, and publishes only what clears the bar — with background research attached.

<a class="rss-btn" href="{{ '/feed-en.xml' | relative_url }}">
<svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path fill="currentColor" d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"/></svg>
Subscribe
</a>

</div>

<h2 class="section-label">Run log</h2>

<ul class="run-log">
  {% assign en_posts = site.posts | where: "lang", "en" %}
  {% for post in en_posts limit:30 %}
    <li class="run-entry">
      <a href="{{ post.url | relative_url }}">
        <span class="run-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <span class="run-time">{{ post.date | date: "%H:%M" }} UTC</span>
        <span class="run-meta">
          <span class="run-count{% if post.items == 0 %} zero{% endif %}">{{ post.items | default: 0 }}</span> flagged
          <span class="run-sep">/</span> {{ post.analyzed | default: 0 }} analysed
        </span>
      </a>
    </li>
  {% else %}
    <li class="run-entry empty"><em>No runs published yet.</em></li>
  {% endfor %}
</ul>

<h2 class="section-label">How it works</h2>

<div class="pipeline" markdown="1">

`fetch` → `dedupe` → `score 0–10` → `threshold` → `enrich` → `publish`

</div>

<ul class="doc-links">
  <li><a href="configuration">Configuration</a> — providers, sources, filtering, environment substitution</li>
  <li><a href="scrapers">Scrapers</a> — how content is collected from GitHub, Hacker News, RSS and Reddit</li>
  <li><a href="scoring">Scoring</a> — how items are analysed and rated 0–10</li>
</ul>

<details class="lang-alt">
<summary>中文</summary>

欢迎来到 [Horizon](https://github.com/thysrael/Horizon)，一个 AI 驱动的信息聚合系统。本站内容以英文发布。

<ul class="run-log">
  {% assign zh_posts = site.posts | where: "lang", "zh" %}
  {% for post in zh_posts limit:10 %}
    <li class="run-entry">
      <a href="{{ post.url | relative_url }}">
        <span class="run-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <span class="run-time">{{ post.date | date: "%H:%M" }} UTC</span>
      </a>
    </li>
  {% else %}
    <li class="run-entry empty"><em>暂无内容</em></li>
  {% endfor %}
</ul>

</details>
