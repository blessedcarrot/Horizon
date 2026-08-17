---
layout: default
title: Home
---

<div class="radar-intro" markdown="1">

**Early warning on AI, for the people who have to decide what to do about it.** Each day this reads research feeds, vendor announcements, developer communities and trending repositories — several hundred items — and publishes the few that would change a decision. Each one carries the reasoning, not just the news: what it changes, for whom, and what would have to be true for it to matter.

</div>

<div class="byline" markdown="1">

Curated by **Bruno Coelho** — technology leadership across Europe, Asia-Pacific and the Middle East, from strategy through execution. The bar is judgement, not novelty: an item earns a place here when it would change an architecture, an investment case, or a risk position.

</div>

<a class="rss-btn" href="{{ '/subscribe' | relative_url }}">
<svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path fill="currentColor" d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"/></svg>
Subscribe
</a>

</div>

<h2 class="section-label">Commentary</h2>

{% assign takes = site.commentary | where_exp: "c", "c.title" | sort: "date" | reverse %}
{% if takes.size > 0 %}
<ul class="take-list">
  {% for take in takes limit:4 %}
    <li class="take">
      <a href="{{ take.url | relative_url }}">
        <span class="take-title">{{ take.title }}</span>
        <span class="take-meta">{{ take.date | date: "%d %b" }}{% if take.theme %} · {{ take.theme }}{% endif %}</span>
      </a>
    </li>
  {% endfor %}
</ul>
{% else %}
<p class="take-empty">Nothing written yet. The radar surfaces items; the reading gets added here.</p>
{% endif %}

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
  <li><a href="scoring">How items are scored</a> — the 0–10 significance scale and where the bar sits</li>
  <li><a href="scrapers">Where it looks</a> — research feeds, vendor blogs, communities, trending repositories</li>
  <li><a href="configuration">How it is configured</a> — sources, thresholds, providers</li>
</ul>


