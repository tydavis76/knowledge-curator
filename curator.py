#!/usr/bin/env python3
"""
curator.py — Weekly knowledge digest generator.

Fetches RSS feeds defined in sources.yaml, scores articles via Claude API,
and writes a markdown digest to docs/digests/ and vault/digests/.

Usage:
    python curator.py              # Full run (requires ANTHROPIC_API_KEY)
    python curator.py --dry-run    # Fetch feeds only, skip Claude call, write placeholder digest
    python curator.py --date 2025-06-15  # Override output date (default: today)
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import anthropic
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent
SOURCES_FILE = REPO_ROOT / "sources.yaml"
PROMPT_FILE = REPO_ROOT / "prompt_template.md"
DOCS_DIGESTS = REPO_ROOT / "docs" / "digests"
VAULT_DIGESTS = REPO_ROOT / "vault" / "digests"

# ---------------------------------------------------------------------------
# Feed ingestion
# ---------------------------------------------------------------------------

def load_sources(path: Path) -> list[dict]:
    """Return flat list of {name, url, tier, domain} dicts."""
    with open(path) as f:
        config = yaml.safe_load(f)

    sources = []
    for domain, feeds in config.get("feeds", {}).items():
        for feed in feeds:
            sources.append({
                "name": feed["name"],
                "url": feed["url"],
                "tier": feed.get("tier", "weekly"),
                "domain": domain,
            })
    return sources


def fetch_articles(sources: list[dict], since_days: int = 7) -> list[dict]:
    """Fetch and filter articles published within the last `since_days` days."""
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=since_days)
    articles = []
    seen_urls: set[str] = set()

    for source in sources:
        print(f"  Fetching: {source['name']} ({source['url']})", flush=True)
        try:
            feed = feedparser.parse(source["url"])
        except Exception as e:
            print(f"    WARNING: failed to fetch {source['url']}: {e}", flush=True)
            continue

        for entry in feed.entries:
            url = normalize_url(getattr(entry, "link", ""))
            if not url or url in seen_urls:
                continue

            published = parse_date(entry)
            if published and published < cutoff:
                continue  # Too old

            seen_urls.add(url)
            articles.append({
                "title": getattr(entry, "title", "(no title)").strip(),
                "url": url,
                "source": source["name"],
                "domain": source["domain"],
                "published": published.isoformat() if published else None,
                "summary": _truncate(getattr(entry, "summary", ""), 300),
            })

    print(f"  → {len(articles)} articles after dedup/date filter", flush=True)
    return articles


def normalize_url(url: str) -> str:
    """Strip utm params and trailing slashes for dedup."""
    url = url.split("?")[0].rstrip("/")
    return url


def parse_date(entry) -> datetime | None:
    """Try published_parsed then updated_parsed; return UTC datetime or None."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                import time as _time
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def _truncate(text: str, max_chars: int) -> str:
    text = re.sub(r"<[^>]+>", "", text)  # strip HTML tags
    text = " ".join(text.split())
    return text[:max_chars] + ("…" if len(text) > max_chars else "")


# ---------------------------------------------------------------------------
# Claude scoring
# ---------------------------------------------------------------------------

BATCH_SIZE = 50  # articles per API call


def format_articles_for_prompt(articles: list[dict]) -> str:
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(
            f"{i}. [{a['title']}]({a['url']})\n"
            f"   Source: {a['source']} | Domain: {a['domain']}\n"
            f"   Published: {a['published'] or 'unknown'}\n"
            f"   Summary: {a['summary'] or '(none)'}\n"
        )
    return "\n".join(lines)


def score_articles(articles: list[dict], week_date: str, dry_run: bool) -> dict:
    """Send articles to Claude API; return parsed JSON digest dict."""
    if dry_run:
        print("  [dry-run] Skipping Claude API call.", flush=True)
        return _placeholder_digest(week_date, articles)

    prompt_template = PROMPT_FILE.read_text()
    client = anthropic.Anthropic()

    # Process in batches; merge results
    merged: dict[str, list] = {
        "read_this_week": [],
        "weekend_deep_dive": [],
        "cross_domain_spark": [],
        "archive_reference": [],
    }

    for batch_start in range(0, len(articles), BATCH_SIZE):
        batch = articles[batch_start : batch_start + BATCH_SIZE]
        article_text = format_articles_for_prompt(batch)
        prompt = prompt_template.replace("{ARTICLES}", article_text)

        print(
            f"  Scoring batch {batch_start + 1}–{batch_start + len(batch)} "
            f"of {len(articles)} via Claude…",
            flush=True,
        )

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        parsed = _parse_json_response(raw)

        for key in merged:
            merged[key].extend(parsed.get(key, []))

    # Cross-domain spark should be exactly 1 item
    if len(merged["cross_domain_spark"]) > 1:
        merged["cross_domain_spark"] = merged["cross_domain_spark"][:1]

    merged["week"] = week_date
    return merged


def _parse_json_response(raw: str) -> dict:
    """Extract JSON from Claude response; fall back gracefully."""
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse failed ({e}). Raw response saved to /tmp/curator_raw.txt", flush=True)
        Path("/tmp/curator_raw.txt").write_text(raw)
        return {"read_this_week": [], "weekend_deep_dive": [], "cross_domain_spark": [], "archive_reference": []}


def _placeholder_digest(week_date: str, articles: list[dict]) -> dict:
    """Minimal digest for dry-run — first article per section."""
    def _item(a: dict) -> dict:
        return {
            "title": a["title"],
            "url": a["url"],
            "source": a["source"],
            "why": "[dry-run placeholder]",
            "domain": a["domain"],
            "estimated_minutes": 10,
        }

    buckets = list(articles[:4]) if articles else []
    return {
        "week": week_date,
        "read_this_week": [_item(a) for a in buckets[:1]],
        "weekend_deep_dive": [_item(a) for a in buckets[1:2]],
        "cross_domain_spark": [_item(a) for a in buckets[2:3]],
        "archive_reference": [_item(a) for a in buckets[3:4]],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

SECTION_META = {
    "read_this_week": ("🔴 Read This Week", "High signal, under 30 min each"),
    "weekend_deep_dive": ("🟡 Weekend Deep Dive", "High depth, 45+ min"),
    "cross_domain_spark": ("🔵 Cross-Domain Spark", "One item outside your primary domains"),
    "archive_reference": ("🗄️ Archive Reference", "Noteworthy but not urgent"),
}


def render_markdown(digest: dict) -> str:
    week = digest.get("week", "unknown")
    try:
        display_date = datetime.strptime(week, "%Y-%m-%d").strftime("%B %-d, %Y")
    except ValueError:
        display_date = week

    lines = [
        f"---",
        f"date: {week}",
        f"tags: [digest, weekly]",
        f"---",
        f"",
        f"# Weekly Knowledge Digest — {display_date}",
        f"",
    ]

    for key, (heading, subtitle) in SECTION_META.items():
        items = digest.get(key, [])
        lines.append(f"## {heading}")
        lines.append(f"*{subtitle}*")
        lines.append("")

        if not items:
            lines.append("*No qualifying articles this week.*")
            lines.append("")
            continue

        for item in items:
            domain_display = item.get("domain", "").replace("_", " ").title()
            lines.append(f"### [{item['title']}]({item['url']})")
            lines.append(
                f"**Source:** {item['source']} | **Domain:** {domain_display} | "
                f"**~{item.get('estimated_minutes', '?')} min**"
            )
            lines.append("")
            lines.append(f"*Why it matters:* {item.get('why', '')}")
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_digest(markdown: str, week_date: str) -> tuple[Path, Path]:
    filename = f"{week_date}.md"

    docs_path = DOCS_DIGESTS / filename
    vault_path = VAULT_DIGESTS / filename

    DOCS_DIGESTS.mkdir(parents=True, exist_ok=True)
    VAULT_DIGESTS.mkdir(parents=True, exist_ok=True)

    docs_path.write_text(markdown)
    vault_path.write_text(markdown)

    # Update digests/index.md with a link to this digest
    index_path = DOCS_DIGESTS / "index.md"
    if index_path.exists():
        index_text = index_path.read_text()
        link = f"- [{week_date}]({week_date}.md)"
        if link not in index_text:
            # Parse display date for the link label
            from datetime import datetime
            label = datetime.strptime(week_date, "%Y-%m-%d").strftime("%B %-d, %Y")
            link = f"- [{label}]({week_date}.md)"
            index_text = index_text.rstrip() + f"\n{link}\n"
            index_path.write_text(index_text)

    return docs_path, vault_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate weekly knowledge digest")
    parser.add_argument("--dry-run", action="store_true", help="Skip Claude API call")
    parser.add_argument("--date", default=None, help="Override output date (YYYY-MM-DD)")
    parser.add_argument("--since-days", type=int, default=7, help="Look back N days for articles (default: 7)")
    args = parser.parse_args()

    week_date = args.date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    print(f"\n=== Knowledge Curator — {week_date} ===\n")

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Use --dry-run to skip Claude.", file=sys.stderr)
        sys.exit(1)

    print("Step 1: Loading sources…")
    sources = load_sources(SOURCES_FILE)
    print(f"  {len(sources)} feeds loaded")

    print(f"\nStep 2: Fetching articles (last {args.since_days} days)…")
    articles = fetch_articles(sources, since_days=args.since_days)

    if not articles:
        print("  No articles found. Exiting.")
        sys.exit(0)

    print("\nStep 3: Scoring with Claude…")
    digest = score_articles(articles, week_date, dry_run=args.dry_run)

    print("\nStep 4: Rendering markdown…")
    markdown = render_markdown(digest)

    print("\nStep 5: Writing output…")
    docs_path, vault_path = write_digest(markdown, week_date)
    print(f"  docs:  {docs_path}")
    print(f"  vault: {vault_path}")

    total = sum(
        len(digest.get(k, []))
        for k in ("read_this_week", "weekend_deep_dive", "cross_domain_spark", "archive_reference")
    )
    print(f"\nDone. {total} articles surfaced from {len(articles)} fetched.\n")


if __name__ == "__main__":
    main()
