---
layout: default
title: Home
---

<div class="radar-intro" markdown="1">

**Early warning on AI and agentic AI, for people who have to make decisions about it.** Twice a day this reads research feeds, vendor announcements, developer communities and trending repositories, scores everything 0–10 for significance, and publishes only what clears the bar — with background research attached. Most days that means a handful of items out of several hundred.

</div>

<div class="byline" markdown="1">

Curated by **Bruno Coelho** — Head of AI Engineering, APAC & Middle East; Head of Technology & Innovation. The bar is set for engineering substance over press-release framing: what changes an architecture decision, a build-versus-buy call, or a risk assessment.

</div>

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
  <li><a href="scoring">How items are scored</a> — the 0–10 significance scale and where the bar sits</li>
  <li><a href="scrapers">Where it looks</a> — research feeds, vendor blogs, communities, trending repositories</li>
  <li><a href="configuration">How it is configured</a> — sources, thresholds, providers</li>
</ul>

<p class="colophon">Built on <a href="https://github.com/Thysrael/Horizon">Horizon</a> (MIT), running on GitHub Actions with Claude doing the scoring and background research. Source and configuration: <a href="https://github.com/blessedcarrot/Horizon">blessedcarrot/Horizon</a>.</p>

