---
tags: [dashboard]
---

# Knowledge Curator

> Automated weekly digest of high-signal content across AI systems, distributed systems, economics, complexity science, and philosophy.

## How It Works

Every Sunday at 8am UTC, a GitHub Action:

1. Fetches articles from [configured RSS feeds](https://github.com/tydavis76/knowledge-curator/blob/main/sources.yaml) published in the past 7 days
2. Sends them to Claude (claude-sonnet-4-6) with a [scoring prompt](https://github.com/tydavis76/knowledge-curator/blob/main/prompt_template.md) tuned for architectural durability
3. Publishes the result here and commits it to `vault/digests/` for Obsidian

## Digest Sections

| Section | Signal | Time |
|---|---|---|
| 🔴 Read This Week | High priority, clear architectural value | < 30 min each |
| 🟡 Weekend Deep Dive | High depth, slower burn | 45+ min |
| 🔵 Cross-Domain Spark | Outside primary domains, high leverage | varies |
| 🗄️ Archive Reference | Worth keeping, not urgent | varies |

## Recent Digests

See the [Digests](digests/) section in the nav for all weekly issues.

## Tuning

- **Sources:** edit [`sources.yaml`](https://github.com/tydavis76/knowledge-curator/blob/main/sources.yaml) — no code changes required
- **Scoring criteria:** edit [`prompt_template.md`](https://github.com/tydavis76/knowledge-curator/blob/main/prompt_template.md) — adjust domains, filtering rules, output format
- **Manual trigger:** use [workflow_dispatch](https://github.com/tydavis76/knowledge-curator/actions) on the GitHub Actions tab
