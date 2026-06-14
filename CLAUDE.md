# Knowledge Curator

A GitHub Pages project that generates a weekly curated reading digest from RSS feeds using Claude AI.

## Architecture

```
curator.py          # Main script: fetch feeds → score via Claude → write markdown
sources.yaml        # RSS feed definitions, organized by domain
prompt_template.md  # Claude scoring prompt (edit to tune domains/criteria)
requirements.txt    # Python deps: anthropic, feedparser, mkdocs-material, pyyaml
mkdocs.yml          # MkDocs config (Material theme, deploys to GitHub Pages)
docs/
  index.md          # Site homepage
  reading-list.md   # Static reading list
  digests/
    index.md        # Auto-updated index of all weekly digests
    YYYY-MM-DD.md   # Generated weekly digest files
vault/digests/      # Mirror of docs/digests/ for Obsidian
.github/workflows/
  weekly.yml        # GitHub Actions: runs every Sunday 8am UTC
```

## Workflow

Every Sunday at 8am UTC, the GitHub Actions workflow:
1. Runs `curator.py` → fetches RSS feeds, scores via Claude API, writes `docs/digests/YYYY-MM-DD.md` and appends a link to `docs/digests/index.md`
2. Commits and pushes the new digest files
3. Runs `mkdocs build --strict`
4. Deploys `./site` to the `gh-pages` branch via `peaceiris/actions-gh-pages`

The site is served from the `gh-pages` branch at: https://tydavis76.github.io/knowledge-curator/

## Local Development

```bash
pip install -r requirements.txt

# Test digest generation without calling Claude
python curator.py --dry-run

# Override date
python curator.py --date 2026-06-15

# Preview site locally
mkdocs serve
```

## Secrets Required

- `ANTHROPIC_API_KEY` — set in GitHub repo Settings → Secrets → Actions

## Common Issues

### `mkdocs build --strict` fails with nav warning
The nav in `mkdocs.yml` must reference actual files, not directories.
- Correct: `Digests: digests/index.md`
- Wrong: `Digests: digests/`

`docs/digests/index.md` is the digest listing page; it must exist before the workflow runs.

### Push rejected (fetch first)
The workflow commits to remote during its run. Always pull before pushing locally:
```bash
git pull --rebase origin main
git push origin main
```

### Stale `.git/HEAD.lock`
If a git process crashed, remove the lock:
```bash
rm .git/HEAD.lock
```

### Duplicate entries in digests/index.md
`curator.py` checks `if link not in index_text` before appending, so re-running on the same date is safe. If duplicates appear, manually remove the extra line and commit.

## Tuning

- **Sources:** edit `sources.yaml` — no code changes needed
- **Scoring criteria / output format:** edit `prompt_template.md`
- **Site structure:** edit `mkdocs.yml`

## Deployment

To manually trigger a full rebuild and deploy:
- GitHub Actions → Weekly Knowledge Digest → Run workflow

To rebuild the site only (without regenerating the digest), a separate deploy-only workflow could be added — not yet implemented.
