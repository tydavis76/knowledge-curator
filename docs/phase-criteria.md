# Phase Completion Criteria

**Companion to [`architecture.md`](architecture.md).** This document turns the §13 build sequence into verifiable completion conditions for autonomous execution (Claude Code's `/goal` command) and for human/CI verification.

Internal doc — excluded from the published MkDocs site (see `mkdocs.yml`).

---

## How to use this with `/goal`

`/goal` works best when fed **one measurable condition per invocation**. After each turn a checker model evaluates whether the condition holds and only releases control when it does. So:

- Drive execution **task-by-task**, not phase-by-phase. Paste a single task's **Done when** line as the goal.
- A condition is only usable if a command can decide it. Every task below pairs its **Done when** with a **Verify** command and an **Expected** result.
- Phase **Exit gates** are for human/CI sign-off — they aggregate task conditions and are not meant to be a single `/goal` invocation.

**Not `/goal`-checkable (human sign-off required):** semantic-quality conditions cannot be decided by an automated checker and must not be used as goal conditions. These are flagged inline with ⚠. The structural parts of those tasks (sections present, forbidden phrases absent, schema valid) *are* checkable and are split out.

**Test paths are illustrative.** The codebase does not exist yet; `tests/...` paths name where the verifying test should live. Part of each task is writing that test.

---

## Global gates (apply to every task)

A task is done only if its own condition holds **and** the repo-wide checks are green:

```bash
ruff check .
mypy app/
pytest --cov=app
# once the frontend exists:
cd frontend && npm run test && npm run build
```

All commands exit 0. Each task's **Done when** is *in addition* to these.

---

## Phase 0 — Personal MVP — SHIPPED

Delivered in simplified, stack-free form (script + MkDocs + Actions). Retro criteria, verifiable against the current repo:

**Done when:** `python curator.py --dry-run` writes `docs/digests/<date>.md`, updates `docs/digests/index.md` and `docs/index.md`, mirrors to `vault/digests/`, and `mkdocs build --strict` exits 0.

**Verify:**

```bash
python curator.py --dry-run --date 2026-06-15
test -f docs/digests/2026-06-15.md && grep -q "2026-06-15" docs/digests/index.md
mkdocs build --strict
```

**Expected:** digest + index + dashboard written; mirror file present; `mkdocs build --strict` exits 0.

**Exit gate:** all above pass; weekly GitHub Actions cron runs `curator.py` and deploys to GitHub Pages without manual steps.

---

## Phase 1 — Multi-User Alpha

### Task 1.1 — FastAPI Foundation
**Done when:** `/health` returns 200, a request with a valid Clerk JWT resolves to a `users` row, and a request with a missing/invalid token returns 401.
**Verify:**
```bash
pytest tests/api/test_health.py tests/api/test_auth.py
curl -fsS -o /dev/null -w '%{http_code}' localhost:8000/health   # → 200
```
**Expected:** pytest exit 0; health → 200; protected route → 401 without token, 200 with a valid one.

### Task 1.2 — Celery Job Infrastructure
**Done when:** Celery Beat enqueues the feed-fetch and digest tasks on schedule, a worker consumes them, and task results are recorded in the result backend.
**Verify:**
```bash
pytest tests/worker/test_schedule.py tests/worker/test_tasks.py
celery -A app.worker inspect ping        # → pong from worker
celery -A app.worker inspect scheduled   # → feed-fetch + digest tasks listed
```
**Expected:** pytest exit 0; worker responds to ping; scheduled tasks present.

### Task 1.3 — Core API Endpoints
**Done when:** `/digests`, `/digests/{id}`, `/articles/{id}/feedback`, `/preferences`, `/sources` each return the documented schema and reject unauthorized access, covered by integration tests.
**Verify:**
```bash
pytest tests/api/test_digests.py tests/api/test_feedback.py \
       tests/api/test_preferences.py tests/api/test_sources.py
```
**Expected:** pytest exit 0; each endpoint returns its §8.1 schema; cross-user access returns 403/404.

### Task 1.4 — Next.js Shell
**Done when:** the authenticated three-panel shell (NavPanel + main + EdgePanel) renders, panels collapse, and unauthenticated users are redirected to sign-in.
**Verify:**
```bash
cd frontend && npm run test
npx playwright test e2e/shell.spec.ts
```
**Expected:** unit + Playwright exit 0; shell renders for signed-in user; redirect for anonymous.

### Task 1.5 — Digest UI
**Done when:** a digest fetched from the API renders with correct tier ordering (🔴🟡🔵🗄️), the summary-style toggle switches styles, and a feedback click issues the optimistic `POST /articles/{id}/feedback`.
**Verify:**
```bash
cd frontend && npm run test
npx playwright test e2e/digest.spec.ts
```
**Expected:** Playwright exit 0; tiers ordered; toggle works; feedback request observed in network mock.

### Task 1.6 — Article Lifecycle (Queue & Library)
**Done when:** a single article transitions `surfaced → queued → in_progress → completed`, and at every step it appears in exactly one of This Week / Queue / Library with no duplication.
**Verify:**
```bash
pytest tests/services/test_lifecycle.py tests/api/test_status.py
```
**Expected:** pytest exit 0; status transitions persist with timestamps; a parametrized test asserts each view contains the article in exactly one state and never two.

### Task 1.7 — Email Delivery
**Done when:** digest generation triggers a Resend send whose payload contains the digest's tier sections and a working deep-link back to the web app.
**Verify:**
```bash
pytest tests/services/test_notification.py    # Resend client mocked
```
**Expected:** pytest exit 0; send invoked once per digest; HTML contains tier headers + deep-link; plain-text fallback present.

### Task 1.8 — User Preferences UI
**Done when:** a user can select domains, cadence, summary style, and delivery, and saving issues `PATCH /preferences` that persists to `user_preferences`.
**Verify:**
```bash
cd frontend && npm run test
npx playwright test e2e/preferences.spec.ts
pytest tests/api/test_preferences.py::test_patch_persists
```
**Expected:** all exit 0; round-trip read-after-write returns the saved values.

### Phase 1 — Exit gate
All of: 1.1–1.8 done conditions hold; global gates green; a beta user receives a personalized digest end-to-end (cron → generate → persist → email + web render); `mkdocs build --strict` still exits 0.

---

## Phase 2 — Edge Intelligence + Challenge Layer

### Task 2.1 — EdgeReportGraph
**Done when (structural):** invoking `EdgeReportGraph` for a digest writes a non-null `digests.edge_report`, inserts ≥1 `skill_durability` row, the report contains all four required H2 sections, and contains none of the forbidden phrases (§7.3).
**Verify:**
```bash
pytest tests/graphs/test_edge_report.py
```
**Expected:** pytest exit 0; four `##` sections present; forbidden-phrase scan finds none; `skill_durability` populated.
⚠ **Not `/goal`-checkable:** whether the report is *non-generic / domain-specific* (§15 risk) — human review of the first reports required.

### Task 2.2 — WebSocket Infrastructure
**Done when:** a client connects with a JWT, receives streamed chunks for a test message, and re-establishes the connection after a forced drop.
**Verify:**
```bash
pytest tests/api/test_ws.py
```
**Expected:** pytest exit 0; auth rejected without JWT; chunks received in order; reconnect succeeds.

### Task 2.3 — ChallengeGraph
**Done when:** submitting an answer streams an evaluation and, on completion, inserts the expected `graph_nodes`/`graph_edges` and one `progression_events` row, and marks the challenge `completed`.
**Verify:**
```bash
pytest tests/graphs/test_challenge.py
```
**Expected:** pytest exit 0; stream emits chunks; DB deltas match fixture; challenge status `completed`.
⚠ **Not `/goal`-checkable:** evaluation pedagogical quality — A/B against satisfaction signal (§15).

### Task 2.4 — Challenge UI
**Done when:** a user opens a challenge, submits an answer, and sees streamed evaluation with rendered citations.
**Verify:**
```bash
npx playwright test e2e/challenge.spec.ts
```
**Expected:** Playwright exit 0; streaming text renders progressively; citations are links.

### Task 2.5 — Knowledge Graph (Backend)
**Done when:** graph CRUD endpoints work, and `GET /graph/export` returns both valid JSON and Obsidian-compatible markdown for a user's graph.
**Verify:**
```bash
pytest tests/api/test_graph.py
```
**Expected:** pytest exit 0; export JSON parses; markdown export validates; gap query returns sparse-area suggestions.

### Task 2.6 — Knowledge Graph (Frontend)
**Done when:** the D3 canvas renders nodes/edges for a user, a node click opens detail, and the frontier line animates.
**Verify:**
```bash
npx playwright test e2e/graph.spec.ts
```
**Expected:** Playwright exit 0; node count matches fixture; detail popover opens on click.

### Task 2.7 — Edge Panel
**Done when:** the right panel renders live edge score, skill-map summary, this-week's challenge, and path progress from the API.
**Verify:**
```bash
cd frontend && npm run test
npx playwright test e2e/edge-panel.spec.ts
```
**Expected:** all exit 0; panel values match API fixture.

### Task 2.8 — ExploreGraph
**Done when:** standard search returns cited corpus results with Signal scores, and a deep-research request completes as an async job and returns a synthesized, cited report.
**Verify:**
```bash
pytest tests/graphs/test_explore.py
```
**Expected:** pytest exit 0; standard results carry score + citations; deep-research job reaches `complete` and returns citations.

### Task 2.9 — Learning Paths
**Done when:** `POST /paths/generate` returns a sequenced path whose items match the §4.3 schema, and item completion updates `learning_paths.progress`.
**Verify:**
```bash
pytest tests/api/test_paths.py
```
**Expected:** pytest exit 0; generated items validate against schema; progress recomputes on completion.

### Task 2.10 — Markdown Export
**Done when:** a Pro user gets `GET /digests/{id}/markdown` with Obsidian-compatible YAML frontmatter; a non-Pro user gets 403.
**Verify:**
```bash
pytest tests/api/test_export.py
```
**Expected:** pytest exit 0; frontmatter parses (date/week/tags/domains); free tier → 403.

### Task 2.11 — Progression & Edge Score
**Done when:** reading completion, correct challenge, and survived review each append a `progression_events` row and recompute `user_progression.edge_score`; weekly rhythm increments on a newly engaged week.
**Verify:**
```bash
pytest tests/services/test_progression.py
```
**Expected:** pytest exit 0; event deltas match table in §4.5; edge_score = sum of event deltas; rhythm counts distinct engaged ISO weeks.

### Task 2.12 — ReviewGraph + Spaced Repetition
**Done when:** `compute_sm2` reproduces canonical SM-2 outputs for known input vectors, decayed concepts resurface in `GET /review/due`, a correct review lengthens the interval, and an incorrect one resets it to 1 day.
**Verify:**
```bash
pytest tests/services/test_sm2.py tests/graphs/test_review.py
```
**Expected:** pytest exit 0; SM-2 matches reference vectors; due query returns only past-due concepts; interval grows on correct, resets on incorrect.

### Phase 2 — Exit gate
All of: 2.1–2.12 structural conditions hold; global gates green; a user can complete a challenge → graph updates → edge score moves → concept later resurfaces for review; the ⚠ quality items have passed first-100 human review before any monetization.

---

## Phase 3 — Monetization & Growth

### Task 3.1 — Billing
**Done when:** Stripe (test mode) subscription create/upgrade/cancel works and the tier-gate middleware blocks Pro-only features for free users.
**Verify:**
```bash
pytest tests/api/test_billing.py        # Stripe test keys
```
**Expected:** pytest exit 0; webhook updates `users.tier`; free user hitting a Pro route → 402/403.

### Task 3.2 — Onboarding Flow
**Done when:** completing the 4-step onboarding populates `user_preferences` and `user_edge_profiles` and triggers a first digest generation.
**Verify:**
```bash
npx playwright test e2e/onboarding.spec.ts
```
**Expected:** Playwright exit 0; both tables populated; first-digest job enqueued.

### Task 3.3 — Team Tier
**Done when:** an org with seats can be created, a shared digest is visible to members, and a digest card posts to a configured Slack channel.
**Verify:**
```bash
pytest tests/api/test_team.py tests/services/test_slack.py
```
**Expected:** pytest exit 0; seat limits enforced; Slack client invoked with digest card payload.

### Task 3.4 — Observability
**Done when:** a deliberately raised error reaches Sentry (test DSN) and the cost-tracking middleware logs Claude token usage per request.
**Verify:**
```bash
pytest tests/middleware/test_cost_tracking.py
```
**Expected:** pytest exit 0; token usage logged with request_id; Sentry capture invoked on raised error.

### Task 3.5 — Public Landing Page
**Done when:** the marketing site builds and meets baseline SEO/perf thresholds.
**Verify:**
```bash
cd frontend && npm run build
npx lighthouse https://localhost:3000 --only-categories=performance,seo --chrome-flags="--headless" --output=json | \
  jq '.categories.performance.score >= 0.9 and .categories.seo.score >= 0.9'
```
**Expected:** build exit 0; Lighthouse performance ≥ 0.9 and SEO ≥ 0.9.

### Phase 3 — Exit gate
All of: 3.1–3.5 done conditions hold; global gates green; a new user can sign up → onboard → receive a digest → upgrade to Pro → access Pro features, fully self-serve.
