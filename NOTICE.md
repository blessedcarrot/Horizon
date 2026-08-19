# Notice and attribution

NEWS-Radar is built on a fork of [Thysrael/Horizon](https://github.com/Thysrael/Horizon),
released under the MIT License. Upstream's copyright notice is retained unmodified in
`LICENSE` and travels with every file derived from it, as MIT requires.

## Derived from Horizon

- `src/` — the pipeline engine: scrapers, orchestration, AI client, enrichment,
  summariser, storage, MCP server. Approximately 12,769 lines, carrying about 61 lines
  of local patches (three model-compatibility fixes and one publishing bug fix).
- `docs/` layouts and configuration inherited at fork time, since substantially rewritten.
- `profiles/tech-news`, `profiles/tech-blog`, `profiles/finance-news`,
  `profiles/ai-creator` — upstream's example profiles, retained because upstream tests
  depend on them. Not used in production routing.

## Original work

- `scripts/check_run_health.py` — run health checking: log parsing, funnel reporting,
  GitHub annotations, digest footer, failure severity.
- `scripts/notify_telegram.py` — notification delivery.
- `profiles/critical-infrastructure`, `profiles/reliability-assurance`,
  `profiles/business-markets`, `profiles/practice`, `profiles/horizon-research` — the
  five-theme editorial taxonomy and its scoring rubrics.
- `.github/workflows/` — scheduling, health gating, notification, self-test.
- `docs/` — the published site, its layouts, the item and commentary collections, the
  method page, and `STYLE.md`.
- `data/config.github.json` — source selection, thresholds, routing, cadence.

## Licence

Upstream code remains under the MIT License, reproduced in `LICENSE`. Original work in
this repository is the work of its author. Any redistribution of the derived portions
must retain upstream's copyright and permission notice.
