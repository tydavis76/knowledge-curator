# Signal — Complete Architecture Design Document
## AI-Native Edge Intelligence Platform

**Version:** 1.0  
**Status:** Ready for Implementation  
**Intended audience:** Engineering agents, technical leads, implementation teams  
**Document scope:** Full system — UX, frontend, backend, AI layer, infrastructure, data models, build sequence

---

## Table of Contents

1. [Product Vision & Positioning](#1-product-vision--positioning)
2. [Core UX Philosophy](#2-core-ux-philosophy)
3. [User Journeys & Screen Flows](#3-user-journeys--screen-flows)
4. [Feature Specification](#4-feature-specification)
5. [System Architecture](#5-system-architecture)
6. [Data Models](#6-data-models)
7. [AI Layer Design](#7-ai-layer-design)
8. [API Specification](#8-api-specification)
9. [Frontend Architecture](#9-frontend-architecture)
10. [Infrastructure & DevOps](#10-infrastructure--devops)
11. [Cost Model](#11-cost-model)
12. [Security & Privacy](#12-security--privacy)
13. [Build Sequence & Agent Task Breakdown](#13-build-sequence--agent-task-breakdown)
14. [Architecture Decision Records](#14-architecture-decision-records)
15. [Open Questions & Risks](#15-open-questions--risks)

---

## 1. Product Vision & Positioning

### The Problem

Knowledge workers in technical fields face three compounding problems that no existing tool solves together:

1. **Volume overload** — Content volume in AI, distributed systems, economics, and adjacent fields exceeds what any human can track. Existing aggregators optimize for completeness, not signal quality.

2. **Hype vs. durability confusion** — The majority of content in fast-moving fields is ephemeral. Identifying knowledge with a 5-year shelf life requires editorial judgment that generic tools don't provide.

3. **No learning strategy in the context of AI** — As AI commoditizes technical execution, professionals lack guidance on which skills remain durable and what to study to maintain their edge. No tool answers: *"Given what AI can now do in my domain, what should I learn this week that still matters?"*

### Why Existing Tools Fall Short

| Tool | What it does well | What it misses |
|---|---|---|
| Perplexity | Real-time cited search, Spaces, scheduled queries | Optimizes for recency not durability; digest is a news briefing not a learning strategy; no edge analysis |
| Claude | Long-form synthesis, persistent Projects, artifact creation | Reactive — you must bring the question; no proactive learning agenda |
| Gemini | Deep Research, cross-document synthesis, NotebookLM | No persistent learning model; no edge intelligence |
| Readwise / Matter | Reading capture, highlights, spaced repetition | No curation; no AI synthesis; no edge analysis |
| Feedly / Substack | Feed aggregation | No scoring, no synthesis, no learning layer |

**All existing tools share one structural limitation: they are query-response loops. You come to them with a question. Signal inverts this in a critical dimension: Signal comes to you with a challenge.**

### Positioning

**Signal is an AI-native learning environment for technical professionals who want to stay ahead of — not just keep up with — AI.**

It curates high-signal content across a user's chosen domains, synthesizes it into digestible formats, and continuously advises them on how to identify, measure, and sharpen their cognitive edge as AI capabilities evolve.

The north star interaction: a user opens Signal and it already knows what they should think about today — not just what happened, but what it means for how they should spend their learning time, and a specific challenge that pushes them to engage actively rather than consume passively.

### Competitive Moat

The curation layer is table-stakes and will be commoditized. The defensible moat is:

1. **Edge intelligence depth** — Personalized, domain-specific analysis of skill durability vs. AI encroachment. Requires significant prompt engineering, domain expertise encoding, and user model development. Hard to replicate generically.

2. **The Socratic interaction model** — Signal asks users questions before delivering synthesis. This is a fundamentally different interaction model that creates learning outcomes, not just information delivery. No competitor has this.

3. **The knowledge graph** — User's learning accumulates as a visible, navigable graph. Reading an article adds nodes and edges. The graph is the long-term product — it represents months of a user's intellectual development and creates high switching cost.

4. **Curated source library** — A maintained, quality-tiered source library per domain, with editorial scoring, is real ongoing work that creates durable value. Perplexity indexes everything; Signal curates.

---

## 2. Core UX Philosophy

### Design Principles

**1. The environment is a workbench, not a feed.**
Signal looks like a senior engineer's research environment, not a content platform. Information density is high. Decoration is absent. Every element earns its place.

**2. Active beats passive.**
Every digest item has a challenge attached — a question Signal asks the user to answer before revealing its synthesis. Reading becomes generative, not consumptive. This is the Socratic dimension borrowed from the best pedagogy and applied to professional learning.

**3. Proactive beats reactive.**
Signal surfaces relevant content, poses questions, and updates the user's edge map without being asked. The user doesn't have to come with a question. Signal has already thought about what matters.

**4. The graph is the product.**
The user's knowledge graph — concepts, connections, gaps, the frontier where AI is encroaching — is the long-term value artifact. It should always be visible, always evolving, and always meaningful.

**5. Citedness builds trust.**
Every claim Signal makes is sourced. Every synthesis links to its inputs. Perplexity taught users to expect citations; Signal inherits that expectation and meets it.

**6. Dark, dense, precise.**
The visual register is a high-end terminal dashboard translated to web. Dark mode default. Monospace for data and metadata. Readable serif for synthesis text. Single accent color used with restraint. No gradients, no illustrations, no stock photography.

### Visual Design System

**Palette**
```
--bg-base:        #0D0F12   /* near-black canvas */
--bg-surface:     #141720   /* card and panel backgrounds */
--bg-elevated:    #1C2030   /* modals, dropdowns */
--border:         #2A2F3D   /* all borders */
--text-primary:   #E8EAF0   /* primary readable text */
--text-secondary: #8B92A8   /* metadata, labels */
--text-muted:     #4A5068   /* timestamps, deemphasized */
--accent:         #5B8DEF   /* single accent — selection, links, active states */
--tier-red:       #E05252   /* Read This Week */
--tier-amber:     #D4922A   /* Weekend Deep Dive */
--tier-blue:      #4A9EBD   /* Cross-Domain Spark */
--tier-gray:      #4A5068   /* Archive */
--success:        #4CAF82
--warning:        #D4922A
--error:          #E05252
```

**Typography**
```
Display:  "Söhne" or "Inter" — tight tracking, medium weight, used sparingly
Body:     "Lora" (serif) — synthesis text, summaries, edge reports
Mono:     "JetBrains Mono" — scores, metadata, domain tags, timestamps
UI:       "Inter" — navigation, buttons, labels
```

**Signature element:** The edge frontier line — a subtle animated curve on the knowledge graph that shows where AI capability is advancing into the user's domain. It moves slowly over time as the edge report updates it. It is the one motion element in the entire interface.

### Layout Architecture

Three persistent panels, collapsible:

```
┌─────────────────────────────────────────────────────────────────┐
│  SIGNAL                          [Domain filters]    [Profile]  │
├──────────┬──────────────────────────────────┬───────────────────┤
│          │                                  │                   │
│  NAV     │  MAIN CONTENT AREA               │  EDGE PANEL       │
│          │                                  │                   │
│ This Week│  [Context-dependent:             │  Edge Score       │
│  Queue   │   Digest / Queue / Library /     │  Streak / Rhythm  │
│  Library │   Explore / Graph / Challenge /  │  Skill Map        │
│  Explore │   Learning Path]                 │  This Week's      │
│  Graph   │                                  │  Challenge        │
│  Paths   │                                  │  Due for Review   │
│          │                                  │  Learning Path    │
│  ──────  │                                  │  Progress         │
│  Sources │                                  │  ──────────────   │
│  Settings│                                  │  Recent Activity  │
│          │                                  │                   │
└──────────┴──────────────────────────────────┴───────────────────┘
```

The right edge panel is always visible on desktop — it is the persistent reminder of why the user is here. On mobile it collapses to a bottom sheet.

### Information Architecture — The Article Lifecycle

The three primary nav destinations (**This Week**, **Queue**, **Library**) are not separate stores — they are three lenses over a single per-user article lifecycle. An article has exactly one status per user and moves through states; it is never copied between destinations.

```
Article status pipeline (per user):

  surfaced ──→ queued ──→ in_progress ──→ completed
                  │                          │
                  └──────→ dismissed         └──→ feeds knowledge graph
                                                  + spaced repetition
```

- **This Week** — the current digest. A time-bounded view of newly *surfaced* items. This is intake. The digest *fills* the queue; it does not contain articles permanently.
- **Queue** — the working set. Every item the user has saved (`queued` or `in_progress`), across all digests, regardless of which digest surfaced it. This is what a manually-maintained "Reading List" was trying to be, but auto-populated by save actions and ordered by signal score + age.
- **Library** — the record. All `completed` items. This is what feeds the knowledge graph and the spaced-repetition system.

The mental model is single-threaded: **the digest fills the queue, the queue is what you work through, completion feeds the graph.** A digest from three weeks ago still exists in the archive view, but anything saved from it lives in the queue independent of its origin digest. This eliminates the "where does an article live?" ambiguity entirely — it lives in exactly one place determined by its status.

---

## 3. User Journeys & Screen Flows

### 3.1 Onboarding Flow

```
Landing Page
    │
    ▼
[Sign Up] → Clerk Auth
    │
    ▼
Step 1: Domain Selection
    ├── Taxonomy tree (expandable)
    ├── Search domains
    ├── Select 1-N domains
    └── Drag to weight/prioritize
    │
    ▼
Step 2: Role & Experience Context
    ├── Current role (select)
    ├── Years in primary domain (slider)
    ├── AI tools currently in use (multi-select)
    └── Primary learning goal (select)
    │
    ▼
Step 3: Edge Profile Questionnaire
    ├── 5 questions, one at a time, conversational UI
    ├── "What tasks do you currently hand off to AI?"
    ├── "What feels irreplaceable in your work?"
    ├── "What skill are you most worried AI will make obsolete?"
    ├── "What would you most like to understand better?"
    └── "How much time can you invest in learning per week?"
    │
    ▼
Step 4: Digest Preferences
    ├── Cadence (daily / weekly / monthly toggles)
    ├── Summary style (live preview of each style)
    └── Delivery (web / email / markdown export)
    │
    ▼
First Digest Generation (async, ~2 min)
    └── Loading state with progress indicators
    │
    ▼
Dashboard — First Visit
    ├── Welcome card: "Here's what Signal found for you"
    ├── First challenge surfaced immediately
    └── Edge map initialized with onboarding data
```

### 3.2 Weekly Digest Flow (Returning User)

```
User arrives (Sunday morning, post-generation)
    │
    ▼
Dashboard — Digest View
    ├── "New digest ready" banner
    ├── Edge Report summary card (right panel updates)
    └── Digest document renders in main area
    │
    ▼
User reads Digest
    ├── Scans tier headers (🔴 🟡 🔵 🗄️)
    ├── Expands article cards for summaries
    ├── Clicks challenge prompt on any item
    │       │
    │       ▼
    │   Challenge Modal
    │       ├── Signal poses a question about the article
    │       ├── User types or speaks their answer
    │       ├── Signal evaluates and responds with synthesis
    │       ├── Reveals full cliff-notes summary
    │       └── Updates knowledge graph with new node
    │
    ├── Clicks article → opens source in split view or new tab
    ├── Thumbs up / skip / thumbs down (inline, subtle)
    ├── "Save to Queue" → status: surfaced → queued
    ├── "Mark read" → status: → completed (feeds graph + review)
    ├── "Dismiss" → status: → dismissed (won't resurface)
    └── "Add to learning path" action on any item
```

### 3.3 Queue & Library Flow

```
Queue Tab  (working set — queued + in_progress items)
    │
    ├── List ordered by signal score + age
    ├── Filterable by domain, tier, estimated time
    ├── Click item → opens in reader → status: queued → in_progress
    ├── Inline progress: "in progress" badge, time remaining
    ├── "Mark read" → status: → completed
    │       └── Triggers: graph update, edge score delta,
    │                     concept nodes scheduled for spaced review
    └── "Dismiss" → status: → dismissed

Library Tab  (completed record)
    │
    ├── All completed items, reverse chronological
    ├── Each shows: completion date, concepts extracted, challenge status
    ├── Filterable by domain, date range, "has open challenge"
    ├── Click → see concepts added to graph, related items
    └── "Review" → triggers spaced-repetition challenge on the concept
```

### 3.4 Explore Mode Flow

```
Explore Tab
    │
    ├── Search bar (Perplexity-style, cited answers)
    │       ├── Query against curated source library
    │       ├── Results include Signal score + durability score
    │       └── "Add to digest" / "Add to path" actions
    │
    ├── Domain browsing
    │       ├── All articles in a domain, sorted by signal score
    │       └── Filterable by tier, time range, source
    │
    └── "Deep Research" mode
            ├── Multi-source synthesis on a topic
            ├── User-provided context injected
            └── Output saved as artifact to knowledge base
```

### 3.5 Knowledge Graph Flow

```
Graph Tab
    │
    ▼
Graph Canvas
    ├── Nodes: concepts learned (from articles, challenges, paths)
    ├── Edges: conceptual relationships
    ├── Color coding:
    │       ├── Dense clusters = user strengths
    │       ├── Sparse nodes = gaps
    │       └── Red frontier line = AI encroachment boundary
    │
    ├── Click node → see source articles, related concepts, challenge history
    ├── Hover edge → see why these concepts are connected
    ├── "Suggest gaps" → Signal identifies sparse areas and recommends content
    └── Export graph as markdown or JSON
```

### 3.6 Challenge Flow (Core Interaction)

```
Challenge triggered (from digest item, edge report, or proactively by Signal)
    │
    ▼
Challenge Card
    ├── Question posed by Signal (domain-specific, Socratic)
    ├── Context: "Based on [article/concept]..."
    ├── Input: text area (or voice on mobile)
    └── [Submit Answer] button
    │
    ▼
Signal evaluates answer
    ├── Acknowledges what user got right
    ├── Surfaces gaps or misconceptions
    ├── Provides synthesis (the "reveal")
    ├── Cites sources for every claim
    ├── Suggests follow-up reading
    └── Updates knowledge graph
    │
    ▼
User can:
    ├── Accept synthesis and continue
    ├── Push back ("I disagree because...")
    │       └── Signal engages, maintains position or updates
    ├── Ask for deeper explanation
    └── Add to learning path
```

---

## 4. Feature Specification

### 4.1 Digest Engine

**Inputs:** User domain list + weights, curated source library, articles from last period, user feedback history, user edge profile

**Processing:**
1. Fetch all articles from configured sources for period
2. Deduplicate by URL normalization + title embedding similarity (pgvector cosine distance)
3. Extract full text via Readability extraction; fall back to excerpt
4. Score articles via Claude API (see AI Layer §7.1)
5. Bucket into tiers: Read Now / Weekend Deep Dive / Cross-Domain Spark / Archive / Filtered
6. Generate cliff-notes summary per article in user's chosen style
7. Generate one challenge question per Read Now and Deep Dive article
8. Render digest to markdown + HTML

**Digest tiers:**
- 🔴 **Read This Week** — Signal score ≥ 8.0, estimated < 30 min. Maximum 5 items.
- 🟡 **Weekend Deep Dive** — Signal score ≥ 7.0, estimated 45+ min. Maximum 3 items.
- 🔵 **Cross-Domain Spark** — Highest cross-domain leverage score regardless of primary domain. Exactly 1 item.
- 🗄️ **Archive Reference** — Signal score 5–7, noteworthy but low urgency. Maximum 10 items, collapsed by default.

### 4.2 Explore Mode

Perplexity-inspired cited search against the curated source library and ingested article corpus. Key differences from Perplexity:

- Searches Signal's curated corpus first, web second
- Every result includes Signal score + durability score + domain tag
- Results can be added to digest, learning path, or knowledge graph
- "Deep Research" mode triggers a multi-source synthesis job (async, ~60 sec)
- User's edge profile is injected into search context to bias results toward their domains

### 4.3 Edge Intelligence Layer

**A. Weekly Edge Report**

Generated alongside each digest. Analyzes the week's AI capability announcements through the lens of the user's specific domain profile and role.

Required sections:
```
## Edge Report — Week of [Date]

### What Changed This Week in AI (Your Domains Only)
[Domain-specific capability advances. No generic "AI is advancing" statements.
Every claim grounded in a specific article from the digest.]

### Skill Durability Update
[Any shifts in durability assessment for skills in user's domain.
Include specific skill names, not categories.]

### Your Edge This Week
[Concrete capabilities, judgment calls, or knowledge areas that remain
distinctly human in the user's domain. Be specific.]

### One Thing to Do
[Single actionable recommendation: one article to read, one concept
to study, one skill to practice. Specific, not general.]
```

**B. Skill Durability Map**

Persistent visualization per user. Updated monthly from aggregate edge report analysis.

Data structure per skill:
```json
{
  "skill": "distributed consensus protocol design",
  "domain": "distributed-systems",
  "durability_score": 8.5,
  "ai_encroachment_rate": "low",
  "trend": "stable",
  "rationale": "Requires operational intuition from production failure experience that AI cannot acquire from text alone",
  "last_updated": "2025-06-15"
}
```

Rendered as a force-directed graph where node size = durability, color = encroachment rate, position = user familiarity (set via self-assessment during onboarding and updated by challenge performance).

**C. Learning Path Generator**

On demand or triggered by edge report. User states a goal; Signal generates a sequenced reading list.

Path item schema:
```json
{
  "title": "Designing Data-Intensive Applications — Chapters 5-7",
  "type": "book_section",
  "url": null,
  "estimated_minutes": 180,
  "prerequisites": ["basic-distributed-systems", "cap-theorem"],
  "why_durable": "Kleppmann's replication and consistency treatment is foundational theory, not framework-specific",
  "concepts_introduced": ["replication-lag", "read-your-writes", "monotonic-reads"],
  "challenge_unlocked": true
}
```

### 4.4 Knowledge Graph

Built incrementally from user interactions:

**Node creation triggers:**
- User completes a challenge (concept node added)
- User marks article as read (article node added, concept nodes extracted)
- User adds item to learning path (path node added)
- User completes a learning path item (concept nodes from item added)

**Edge creation triggers:**
- Claude extracts relationships between concepts when adding nodes
- User explicitly links two concepts ("connect these")
- Learning path prerequisites create edges

**Graph persistence:** Stored in PostgreSQL as adjacency list + node metadata. Rendered client-side with D3 force-directed layout. Exported as markdown (Obsidian-compatible) or JSON.

### 4.5 Progression & Retention (Game Layer)

The game layer exists to drive retention and — more importantly — actual learning retention. Every mechanic is tied to a real signal of intellectual progress (mastery, recall, edge growth), never to vanity or compulsion. The target user is a senior professional; mechanics that read as infantilizing (hearts, leagues, confetti, cosmetic badges) are deliberately excluded. The Edge Score is the single central score; everything else feeds it honestly.

**A. Spaced Repetition (the core retention mechanic)**

Concept nodes in the knowledge graph carry a `familiarity` score that *decays over time* on an expanding-interval schedule (SM-2-style). When a concept's familiarity decays below threshold, Signal surfaces a short review challenge on it — turning the graph from a passive record into an active retention tool.

```
Concept learned → familiarity high → decays over days/weeks
    → drops below threshold → surfaced as "Due for Review"
    → user completes review challenge
        → correct: familiarity restored, next interval lengthens
        → incorrect: familiarity reset, interval shortens
```

Review intervals follow expanding steps (1d → 3d → 7d → 16d → 35d → ...), adjusted per-concept by performance. This is the one Duolingo mechanic with strong learning-science backing, applied to professional concepts instead of vocabulary.

**B. Adaptive Challenge Difficulty (Brilliant's mastery model)**

Challenges scale with demonstrated mastery per domain. Consecutive correct answers on a concept escalate difficulty (`intermediate → advanced → expert`); misses step it back down. Uses the existing `challenges.difficulty` field and per-node `familiarity`; selection logic reads recent performance to pick the next challenge's depth.

**C. Consistency Rhythm (the forgiving streak)**

A weekly-cadence consistency mechanic, explicitly *not* a punishing daily chain. Tracks engagement weeks, not days: "Engaged 6 of the last 8 weeks." This respects a professional's real schedule and avoids the dark-pattern dynamic where the streak becomes the goal instead of the learning. No streak-freeze purchases, no loss-aversion guilt mechanics.

**D. Edge Score as the Central Progression Signal**

The Edge Score (already in the design) is the unifying "score." It moves on real progress events:
- Completing a reading (`completed` status) → small increment
- Completing a challenge correctly → increment scaled by difficulty
- A concept surviving spaced review → increment (retention proven)
- A concept failing review → no penalty, but familiarity decay reflected
- Edge report identifying a strengthened skill → increment

**Explicitly excluded:** leaderboards, leagues, competitive social mechanics (perverse incentives for this audience; contradict a tool about *your* personal edge), hearts/lives (punishing), and meaningless cosmetic badges.

**Event source:** Every game-layer event is driven by the article lifecycle (§2 IA) and challenge completions. The `completed` transition and challenge evaluation are the two events that feed progression — which is why the IA cleanup is a prerequisite for this layer.

### 4.6 Source Library

Platform-maintained. Quality tiers:

**Tier A** — Architectural case studies, peer-reviewed papers with production context, research from major labs (DeepMind, MSR, CMU, Stanford AI Lab), established engineering blogs (Netflix, Uber, Meta, Cloudflare). High signal, low noise.

**Tier B** — Quality newsletters, mid-tier engineering blogs, quality journalism (Quanta, Aeon). Good signal, some noise.

**Tier C** — General tech news (TLDR, Hacker News top). Situational signal. Filtered aggressively; used mainly for AI capability tracking.

Initial source library (domain-organized):

```yaml
ai_systems:
  tier_a:
    - {name: "Ahead of AI", url: "https://magazine.sebastianraschka.com/feed"}
    - {name: "Latent Space", url: "https://www.latent.space/feed"}
    - {name: "DeepMind Research", url: "https://deepmind.google/research/publications/rss.xml"}
  tier_b:
    - {name: "The Batch", url: "https://read.deeplearning.ai/the-batch/rss/"}
    - {name: "Import AI", url: "https://importai.substack.com/feed"}
  tier_c:
    - {name: "TLDR AI", url: "https://tldr.tech/ai/rss"}

distributed_systems:
  tier_a:
    - {name: "ACM Queue", url: "https://queue.acm.org/rss/feeds/queuecontent.xml"}
    - {name: "Netflix Tech Blog", url: "https://netflixtechblog.com/feed"}
    - {name: "Cloudflare Blog", url: "https://blog.cloudflare.com/rss/"}
    - {name: "Uber Engineering", url: "https://www.uber.com/en-US/blog/engineering/rss/"}

economics_finance:
  tier_a:
    - {name: "Marginal Revolution", url: "https://marginalrevolution.com/feed"}
    - {name: "Epsilon Theory", url: "https://www.epsilontheory.com/feed/"}
  tier_b:
    - {name: "Money Stuff (Matt Levine)", url: "https://www.bloomberg.com/authors/ARbTQlRLRjE/matt-levine.rss"}

science_complexity:
  tier_a:
    - {name: "Quanta Magazine", url: "https://www.quantamagazine.org/feed/"}
    - {name: "Santa Fe Institute", url: "https://www.santafe.edu/news-center/news/rss.xml"}

philosophy_foundations:
  tier_a:
    - {name: "Aeon Essays", url: "https://aeon.co/feed.rss"}

crypto_protocols:
  tier_a:
    - {name: "a16z crypto", url: "https://a16zcrypto.com/feed/"}
    - {name: "Ethereum Research", url: "https://ethresear.ch/latest.rss"}
```

### 4.7 Output Formats

**Web Dashboard** — Primary. Responsive. Dark mode only (no toggle — it's a design choice, not a preference).

**Email Digest** — HTML email mirroring web digest structure. Plain-text fallback. Sent at user-configured time. Challenge links deep-link back to web app.

**Markdown Export (Pro)** — Obsidian-compatible with YAML frontmatter. Standard markdown only. Written to user-configured export path or downloadable.

```markdown
---
date: 2025-06-15
week: 2025-W24
tags: [digest, weekly, distributed-systems, ai-architecture]
domains: [distributed-systems, ai-agent-architecture]
signal_items: 5
edge_score_delta: +0.3
---

# Weekly Digest — June 15, 2025
...
```

**Slack (Team tier)** — Digest summary card posted to configured channel. Challenge posted as a thread. Edge report posted to separate channel.

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│  Next.js 14 (App Router)  │  Mobile Web  │  Email Client           │
└──────────────────┬──────────────────────────────────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────────────────────────────────┐
│                         API LAYER                                   │
│                    FastAPI (Python 3.12)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐   │
│  │  Auth       │  │  REST API   │  │  WebSocket               │   │
│  │  (Clerk     │  │  /api/v1/*  │  │  (live challenge updates) │   │
│  │  middleware)│  │             │  │                           │   │
│  └─────────────┘  └─────────────┘  └──────────────────────────┘   │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────────────┐
        │          │                  │
┌───────▼──┐ ┌─────▼──────┐  ┌───────▼────────────────────────────┐
│PostgreSQL│ │   Redis     │  │         JOB LAYER                  │
│+pgvector │ │  (cache +   │  │   Celery Workers + Celery Beat     │
│          │ │   queue)    │  │                                    │
└───────┬──┘ └─────────────┘  │  ┌─────────────────────────────┐  │
        │                     │  │    LANGGRAPH AGENT LAYER     │  │
        │                     │  │                              │  │
        │                     │  │  DigestGraph                 │  │
        │                     │  │  ChallengeGraph              │  │
        │                     │  │  EdgeReportGraph             │  │
        │                     │  │  ReviewGraph                 │  │
        │                     │  │  ExploreGraph                │  │
        │                     │  │                              │  │
        │                     │  │  (Anthropic Claude API)      │  │
        │                     │  └─────────────────────────────┘  │
        │                     └────────────────────────────────────┘
        │
┌───────▼─────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                              │
│  Anthropic API  │  Clerk Auth  │  Resend Email  │  RSS Sources     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Service Decomposition

**`api` service** — FastAPI. Stateless. Handles all HTTP/WebSocket traffic. Scales horizontally. No direct LLM calls — delegates to job layer via Celery tasks.

**`worker` service** — Celery workers. Each async job invokes a LangGraph graph as the AI processing unit. CPU/IO bound. Scales by adding worker instances.

**`scheduler` service** — Celery Beat. Single instance. Enqueues digest generation and feed ingestion jobs on schedule. Reads user preferences to determine per-user schedule.

**`ingestion` service** (Phase 2) — Dedicated feed fetcher running continuously. Pre-fetches and caches article content so DigestGraph doesn't block on network I/O. Reduces digest generation time from ~5 min to ~90 sec.

**LangGraph graphs** — Five graphs (DigestGraph, ChallengeGraph, EdgeReportGraph, ReviewGraph, ExploreGraph) encapsulate all AI workflows. Each graph owns its state schema, node logic, conditional routing, and retry/fallback behavior. Celery tasks are thin wrappers that invoke a graph and persist the result. See §7 for full graph specifications.

### 5.3 Data Flow — DigestGraph (Weekly Digest Generation)

Celery Beat enqueues one `generate_digest` task per user in the weekly cohort. Each Celery task invokes `DigestGraph` — a LangGraph `StateGraph` that owns the full digest workflow with explicit state, conditional routing, and per-node retry logic.

```
DigestGraph — StateGraph

State schema:
  user_id, period_start, period_end, user_context
  raw_articles: list[Article]
  deduped_articles: list[Article]
  scored_articles: list[ScoredArticle]
  filtered_articles: list[ScoredArticle]       # tier ≠ filtered
  summaries: dict[article_id, Summaries]
  challenges: dict[article_id, str]
  edge_report: str
  digest_markdown: str
  digest_html: str
  status: str
  errors: list[str]

Nodes:
  fetch_articles      → query DB for user domains, last 7 days
  deduplicate         → pgvector cosine similarity, threshold 0.92
  score_articles      → Claude claude-sonnet-4-6, batch 30; JSON parse + validate
  check_score_quality → conditional: retry if <3 read_now articles and unfetched content exists
  generate_summaries  → Claude claude-haiku parallel fan-out, one call per tier-1/2 article
  generate_challenges → Claude claude-sonnet-4-6, one challenge per tier-1/2 article
  generate_edge_report → Claude claude-sonnet-4-6, requires scored_articles + summaries
  render_digest       → Jinja2 → markdown + HTML
  persist             → write digests table + user export path
  notify              → Resend email + Slack + WebSocket push

Edges:
  START → fetch_articles
  fetch_articles → deduplicate
  deduplicate → score_articles
  score_articles → check_score_quality
  check_score_quality → generate_summaries        (if quality OK)
  check_score_quality → score_articles            (retry with broader batch)
  check_score_quality → render_digest             (if max retries hit — degrade gracefully)
  generate_summaries → generate_challenges        (fan-out complete)
  generate_challenges → generate_edge_report
  generate_edge_report → render_digest
  render_digest → persist
  persist → notify
  notify → END

Retry policy (per node):
  score_articles:       3 attempts, exponential backoff, jitter
  generate_summaries:   2 attempts per article; failed articles skipped, logged to errors
  generate_edge_report: 2 attempts; on failure, digest renders without edge report + flag set
  notify:               3 attempts; email failure non-blocking
```

### 5.4 Data Flow — ChallengeGraph (Real-time Challenge Evaluation)

Triggered by WebSocket message. Runs in-process (not Celery) to minimize latency. Streams output nodes back to client as they complete.

```
ChallengeGraph — StateGraph

State schema:
  challenge_id, user_id, user_answer
  challenge_context: Challenge          # question, article, domain
  user_edge_profile: EdgeProfile
  evaluation: str                       # streamed
  gaps: list[str]                       # streamed
  synthesis: str                        # streamed
  follow_up: str                        # streamed
  graph_delta: GraphDelta               # nodes/edges to add
  progression_delta: float              # edge score increment

Nodes:
  load_context        → fetch challenge + article + edge profile from DB
  evaluate_answer     → Claude claude-sonnet-4-6 streaming; emits chunks via WebSocket
  extract_graph_delta → Claude claude-haiku; extracts concept nodes from synthesis
  update_graph        → write graph_nodes + graph_edges to DB
  update_progression  → write progression_events, update user_progression.edge_score
  complete_challenge  → mark challenge completed, update user_articles status if applicable

Edges:
  START → load_context
  load_context → evaluate_answer
  evaluate_answer → extract_graph_delta     (after stream completes)
  extract_graph_delta → update_graph
  update_graph → update_progression
  update_progression → complete_challenge
  complete_challenge → END

Streaming: evaluate_answer emits WebSocket chunks per sentence group.
           Frontend renders each chunk as it arrives (EvaluationStream.tsx).
```

---

## 6. Data Models

### 6.1 PostgreSQL Schema

```sql
-- ============================================================
-- USERS & AUTH
-- ============================================================

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_id        VARCHAR(255) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    tier            VARCHAR(20) NOT NULL DEFAULT 'free',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_preferences (
    user_id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    domains             JSONB NOT NULL DEFAULT '[]',
    domain_weights      JSONB NOT NULL DEFAULT '{}',
    digest_cadence      VARCHAR(20) DEFAULT 'weekly',
    summary_style       VARCHAR(20) DEFAULT 'technical',
    delivery_channels   JSONB DEFAULT '["web"]',
    email_send_time     TIME DEFAULT '08:00:00',
    markdown_export_path TEXT,
    slack_webhook_url   TEXT,
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_edge_profiles (
    user_id                 UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    role                    VARCHAR(100),
    experience_years        SMALLINT,
    ai_tools_in_use         TEXT[],
    learning_goal           VARCHAR(100),
    weekly_time_budget_min  SMALLINT DEFAULT 120,
    ai_delegated_tasks      TEXT[],
    irreplaceable_skills    TEXT[],
    worried_skills          TEXT[],
    onboarding_responses    JSONB DEFAULT '{}',
    updated_at              TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SOURCE LIBRARY
-- ============================================================

CREATE TABLE sources (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    url             VARCHAR(2048) UNIQUE NOT NULL,
    feed_url        VARCHAR(2048),
    domains         TEXT[] NOT NULL,
    quality_tier    CHAR(1) NOT NULL DEFAULT 'B',
    is_platform     BOOLEAN DEFAULT TRUE,
    active          BOOLEAN DEFAULT TRUE,
    avg_signal_score NUMERIC(3,1),
    last_fetched_at TIMESTAMPTZ,
    fetch_failures  SMALLINT DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_sources (
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    source_id   UUID REFERENCES sources(id) ON DELETE CASCADE,
    active      BOOLEAN DEFAULT TRUE,
    added_at    TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, source_id)
);

-- ============================================================
-- ARTICLES
-- ============================================================

CREATE TABLE articles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID REFERENCES sources(id),
    url             VARCHAR(2048) UNIQUE NOT NULL,
    url_normalized  VARCHAR(2048) UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    content         TEXT,
    excerpt         TEXT,
    author          VARCHAR(255),
    published_at    TIMESTAMPTZ,
    fetched_at      TIMESTAMPTZ DEFAULT NOW(),
    word_count      INTEGER,
    estimated_minutes SMALLINT,
    embedding       vector(1536),
    domains_detected TEXT[]
);

CREATE INDEX articles_published_at_idx ON articles(published_at DESC);
CREATE INDEX articles_embedding_idx ON articles USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE article_scores (
    article_id              UUID REFERENCES articles(id) ON DELETE CASCADE,
    user_id                 UUID REFERENCES users(id) ON DELETE CASCADE,
    signal_score            NUMERIC(3,1),
    durability_score        NUMERIC(3,1),
    architectural_impact    NUMERIC(3,1),
    cross_domain_score      NUMERIC(3,1),
    digest_tier             VARCHAR(20),
    why_it_matters          TEXT,
    summary_technical       TEXT,
    summary_narrative       TEXT,
    summary_bullet          TEXT,
    summary_socratic        TEXT,
    challenge_question      TEXT,
    scored_at               TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (article_id, user_id)
);

CREATE TABLE article_feedback (
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id  UUID REFERENCES articles(id) ON DELETE CASCADE,
    digest_id   UUID,
    signal      SMALLINT NOT NULL CHECK (signal IN (-1, 0, 1)),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, article_id)
);

-- Article lifecycle: single source of truth for per-user article status.
-- This_Week / Queue / Library are VIEWS over this table, not separate stores.
CREATE TABLE user_articles (
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id      UUID REFERENCES articles(id) ON DELETE CASCADE,
    status          VARCHAR(20) NOT NULL DEFAULT 'surfaced',
                    -- surfaced | queued | in_progress | completed | dismissed
    source_digest_id UUID REFERENCES digests(id),  -- which digest surfaced it
    surfaced_at     TIMESTAMPTZ DEFAULT NOW(),
    queued_at       TIMESTAMPTZ,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    dismissed_at    TIMESTAMPTZ,
    PRIMARY KEY (user_id, article_id)
);

CREATE INDEX user_articles_status_idx ON user_articles(user_id, status);
CREATE INDEX user_articles_queue_idx ON user_articles(user_id, status, queued_at DESC)
    WHERE status IN ('queued', 'in_progress');


-- ============================================================
-- DIGESTS
-- ============================================================

CREATE TABLE digests (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES users(id) ON DELETE CASCADE,
    period_start        DATE NOT NULL,
    period_end          DATE NOT NULL,
    cadence             VARCHAR(20) NOT NULL,
    status              VARCHAR(20) DEFAULT 'pending',
    article_count       SMALLINT DEFAULT 0,
    rendered_markdown   TEXT,
    rendered_html       TEXT,
    edge_report         TEXT,
    generation_ms       INTEGER,
    claude_tokens_used  INTEGER,
    generated_at        TIMESTAMPTZ,
    opened_at           TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX digests_user_period_idx ON digests(user_id, period_start DESC);

-- ============================================================
-- CHALLENGES
-- ============================================================

CREATE TABLE challenges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id      UUID REFERENCES articles(id),
    digest_id       UUID REFERENCES digests(id),
    question        TEXT NOT NULL,
    domain          VARCHAR(100),
    difficulty      VARCHAR(20) DEFAULT 'intermediate',
    status          VARCHAR(20) DEFAULT 'pending',
    user_answer     TEXT,
    evaluation      TEXT,
    synthesis       TEXT,
    follow_up       TEXT,
    concepts_added  TEXT[],
    completed_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- KNOWLEDGE GRAPH
-- ============================================================

CREATE TABLE graph_nodes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    label       VARCHAR(255) NOT NULL,
    domain      VARCHAR(100),
    node_type   VARCHAR(50),  -- concept, article, book, path_item
    familiarity NUMERIC(3,1) DEFAULT 5.0,  -- 1-10, updated by challenge performance
    source_url  TEXT,
    -- Spaced repetition scheduling (SM-2 style)
    review_interval_days SMALLINT DEFAULT 1,
    review_ease     NUMERIC(3,2) DEFAULT 2.50,  -- ease factor
    review_due_at   TIMESTAMPTZ,                -- when this concept resurfaces
    review_count    SMALLINT DEFAULT 0,
    last_reviewed_at TIMESTAMPTZ,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, label)
);

CREATE INDEX graph_nodes_review_due_idx ON graph_nodes(user_id, review_due_at)
    WHERE node_type = 'concept' AND review_due_at IS NOT NULL;

CREATE TABLE graph_edges (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    source_id   UUID REFERENCES graph_nodes(id) ON DELETE CASCADE,
    target_id   UUID REFERENCES graph_nodes(id) ON DELETE CASCADE,
    relationship VARCHAR(100),  -- "prerequisite", "related", "applies", "contradicts"
    weight      NUMERIC(3,1) DEFAULT 1.0,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, source_id, target_id)
);

-- ============================================================
-- LEARNING PATHS
-- ============================================================

CREATE TABLE learning_paths (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    goal        TEXT NOT NULL,
    domains     TEXT[],
    items       JSONB NOT NULL DEFAULT '[]',
    status      VARCHAR(20) DEFAULT 'active',
    progress    NUMERIC(3,1) DEFAULT 0.0,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SKILL DURABILITY MAP
-- ============================================================

CREATE TABLE skill_durability (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID REFERENCES users(id) ON DELETE CASCADE,
    skill                   VARCHAR(255) NOT NULL,
    domain                  VARCHAR(100),
    durability_score        NUMERIC(3,1),
    ai_encroachment_rate    VARCHAR(20),  -- low, medium, high, critical
    trend                   VARCHAR(20),  -- stable, declining, rising
    rationale               TEXT,
    user_familiarity        NUMERIC(3,1),
    last_updated            TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, skill)
);

-- ============================================================
-- PROGRESSION & RETENTION (GAME LAYER)
-- ============================================================

-- Single central progression signal per user
CREATE TABLE user_progression (
    user_id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    edge_score          NUMERIC(6,1) DEFAULT 0.0,
    weeks_engaged       SMALLINT DEFAULT 0,      -- consistency rhythm
    last_engaged_week   DATE,                    -- ISO week of last activity
    current_rhythm      SMALLINT DEFAULT 0,      -- consecutive engaged weeks
    concepts_mastered   SMALLINT DEFAULT 0,      -- familiarity >= 8 and reviewed >= 3
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Append-only log of progression events (auditable, drives edge_score)
CREATE TABLE progression_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    event_type  VARCHAR(40) NOT NULL,
                -- reading_completed | challenge_correct | review_survived |
                -- review_failed | skill_strengthened
    delta       NUMERIC(5,1) NOT NULL DEFAULT 0,
    ref_id      UUID,                            -- article/challenge/node id
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX progression_events_user_idx ON progression_events(user_id, created_at DESC);

-- ============================================================
-- EXPLORE / SEARCH
-- ============================================================

CREATE TABLE explore_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    query       TEXT NOT NULL,
    mode        VARCHAR(20) DEFAULT 'standard',  -- standard, deep_research
    result      TEXT,
    sources     JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.2 Redis Key Schema

```
# Digest generation job status
digest:status:{digest_id}           → "pending|generating|complete|failed"
digest:progress:{digest_id}         → "1/8" (step/total)

# Article content cache (24h TTL)
article:content:{url_hash}          → {title, content, excerpt}

# User session data
session:challenges:{user_id}        → list of pending challenge IDs

# Rate limiting
ratelimit:api:{user_id}             → request count
ratelimit:claude:{user_id}          → token count (daily)

# Feed fetch locks (prevent duplicate fetches)
lock:feed:{source_id}               → 1 (TTL: 1h)

# WebSocket connection registry
ws:connections:{user_id}            → connection_id
```

---

## 7. AI Layer Design

### 7.0 LangGraph Architecture Overview

All AI workflows are implemented as LangGraph `StateGraph` instances. Each graph:
- Owns a typed state schema (TypedDict)
- Declares nodes as plain Python async functions
- Declares edges including conditional routing
- Handles retries, fallbacks, and partial failure within the graph — not in the caller
- Is invoked by a thin Celery task (for async jobs) or directly (for real-time WebSocket flows)

**Why LangGraph over a flat pipeline:**
- State is explicit and inspectable at every node boundary — debugging a failed digest means reading the state snapshot, not re-running the whole pipeline
- Conditional routing (retry scoring if too few high-signal articles, degrade gracefully if edge report fails) is first-class, not bolted-on exception handling
- Parallelism via `fan_out` edges for summary generation across articles is built-in
- Graph state checkpointing (LangGraph's persistence layer) enables resuming a failed digest from the last successful node without reprocessing

**Graph inventory:**

| Graph | Trigger | Execution | Primary models |
|---|---|---|---|
| `DigestGraph` | Celery task (weekly/daily) | Async, ~90–180 sec | Sonnet (scoring, challenges, edge), Haiku (summaries) |
| `ChallengeGraph` | WebSocket message | Real-time streaming, ~5–15 sec | Sonnet (eval), Haiku (graph extraction) |
| `EdgeReportGraph` | Celery task (post-digest) | Async, ~30 sec | Sonnet |
| `ReviewGraph` | WebSocket or Celery | Real-time or async | Haiku |
| `ExploreGraph` | HTTP request | Async, ~15–60 sec | Sonnet (deep research), Haiku (standard search) |

**LangGraph persistence:** Use LangGraph's built-in `SqliteSaver` in development and `PostgresSaver` in production (shares the existing PostgreSQL instance). This gives state checkpointing with no additional infrastructure.

---

### 7.1 DigestGraph

```python
# app/graphs/digest_graph.py

class DigestState(TypedDict):
    user_id: str
    period_start: date
    period_end: date
    user_context: UserContext           # domains, role, experience, feedback_summary
    raw_articles: list[Article]
    deduped_articles: list[Article]
    scored_articles: list[ScoredArticle]
    score_retry_count: int
    summaries: dict[str, Summaries]    # article_id → {technical, narrative, bullet, socratic}
    challenges: dict[str, str]         # article_id → question
    edge_report: str | None
    digest_markdown: str
    digest_html: str
    errors: list[str]

# Node definitions (async functions):
# fetch_articles(state) → {raw_articles}
# deduplicate(state) → {deduped_articles}
# score_articles(state) → {scored_articles}          # claude-sonnet-4-6, batch 30
# check_score_quality(state) → routing decision      # conditional edge
# generate_summaries(state) → {summaries}            # claude-haiku, fan-out
# generate_challenges(state) → {challenges}          # claude-sonnet-4-6, fan-out
# generate_edge_report(state) → {edge_report}        # claude-sonnet-4-6
# render_digest(state) → {digest_markdown, digest_html}
# persist(state) → writes DB + export path
# notify(state) → email + Slack + WebSocket push

# Conditional routing:
def route_after_scoring(state: DigestState) -> str:
    read_now_count = sum(1 for a in state["scored_articles"] if a.tier == "read_now")
    if read_now_count < 3 and state["score_retry_count"] < 2:
        return "score_articles"          # retry with broader batch
    elif read_now_count == 0:
        return "render_digest"           # degrade: render archive-only digest
    return "generate_summaries"          # happy path

# Graph wiring:
graph = StateGraph(DigestState)
graph.add_node("fetch_articles", fetch_articles)
graph.add_node("deduplicate", deduplicate)
graph.add_node("score_articles", score_articles)
graph.add_node("generate_summaries", generate_summaries)
graph.add_node("generate_challenges", generate_challenges)
graph.add_node("generate_edge_report", generate_edge_report)
graph.add_node("render_digest", render_digest)
graph.add_node("persist", persist)
graph.add_node("notify", notify)
graph.add_edge(START, "fetch_articles")
graph.add_edge("fetch_articles", "deduplicate")
graph.add_edge("deduplicate", "score_articles")
graph.add_conditional_edges("score_articles", route_after_scoring)
graph.add_edge("generate_summaries", "generate_challenges")
graph.add_edge("generate_challenges", "generate_edge_report")
graph.add_edge("generate_edge_report", "render_digest")
graph.add_edge("render_digest", "persist")
graph.add_edge("persist", "notify")
graph.add_edge("notify", END)
graph.set_entry_point("fetch_articles")
```

**Scoring node prompt** (externalized to `app/prompts/scoring.md`):
```
Role: Senior technical editor — distributed systems, AI architecture, cross-domain synthesis.

User context:
- Domains: {user_domains_with_weights}
- Role: {user_role}, {experience_years} years experience
- Learning goal: {learning_goal}
- Recent feedback: {feedback_summary}

Score each article 1–10 on:
- Architectural impact (40%): Does this change how systems are designed?
- Durability (40%): Will this matter in 5 years?
- Cross-domain leverage (20%): Does it illuminate multiple domains?

Signal score = (impact × 0.4) + (durability × 0.4) + (cross_domain × 0.2)

Tier assignment:
- signal ≥ 8.0, estimated_minutes < 30: read_now
- signal ≥ 7.0, estimated_minutes ≥ 30: deep_dive
- highest cross_domain in batch: spark (override)
- signal 5.0–6.9: archive
- signal < 5.0: filtered

Hard filter (score 0): tool releases with no architectural novelty,
benchmark leaderboards, marketing content, content irrelevant in 12 months.

Output: strict JSON array. Schema: {article_id, signal_score, durability_score,
architectural_impact, cross_domain_score, digest_tier, estimated_minutes,
domains_confirmed, why_it_matters, filter_reason}
```

**Summary node** generates all four styles in parallel (Haiku). Four prompts externalized:
- `app/prompts/summary_technical.md` — precise terminology, mechanisms, trade-offs, 5 sentences max
- `app/prompts/summary_narrative.md` — story, context first, adjacent-expertise reader, 5 sentences max
- `app/prompts/summary_bullet.md` — 3 key points, 2 implications, 1 prerequisite, one sentence each
- `app/prompts/summary_socratic.md` — 2 questions + answers, forces active thinking before reveal

---

### 7.2 ChallengeGraph

Runs in-process on WebSocket message receipt. Streams evaluation back per section using LangGraph's streaming support.

```python
class ChallengeState(TypedDict):
    challenge_id: str
    user_id: str
    user_answer: str
    challenge: Challenge               # question, article_id, domain, difficulty
    article: Article
    edge_profile: EdgeProfile
    evaluation: str                    # what user got right
    gaps: list[str]                    # specific misconceptions surfaced
    synthesis: str                     # fills the gap with citations
    follow_up: str                     # one next concept or article
    graph_delta: GraphDelta            # nodes + edges to add
    progression_delta: float
    difficulty_outcome: str            # correct | partial | incorrect

# Nodes:
# load_context(state)       → fetch challenge + article + edge profile
# evaluate_answer(state)    → claude-sonnet-4-6 streaming; emits ws chunks
# extract_graph_delta(state) → claude-haiku; concept extraction from synthesis
# update_graph(state)       → write graph_nodes + graph_edges
# update_progression(state) → write progression_events, recalculate edge score,
#                              update SM-2 schedule for related concept nodes
# complete(state)           → mark challenge complete, update user_articles if relevant

# Routing: update_progression → update_sm2_schedule → complete → END
# (SM-2 schedule updates happen after progression, before completion)
```

**Challenge generation prompt** (externalized to `app/prompts/challenge_generate.md`):
```
Design a Socratic challenge for a senior technical professional.
The challenge must:
- Require genuine reasoning, not recall
- Surface a non-obvious implication of the article's core insight
- Be answerable in 2–3 paragraphs by someone who read the article
- Reveal the gap between surface and deep understanding
- Be specific enough that a wrong answer reveals a specific misconception

Domain: {domain}
User role: {role}
Difficulty: {difficulty}   # intermediate | advanced | expert
Article summary: {summary}

Output a single question. No preamble.
```

**Challenge evaluation prompt** (externalized to `app/prompts/challenge_evaluate.md`):
```
You are an expert technical mentor. Evaluate the student's answer.
1. Acknowledge what they understood correctly — specific, not generic
2. Identify the specific gap or misconception
3. Provide synthesis filling the gap — cite sources
4. Suggest one follow-up concept or article

Tone: Direct, collegial. Push back if wrong. Agree if right.
Domain: {domain} | Edge profile: {edge_profile_summary}
Article: {article_title} ({article_url})
Question: {question}
```

---

### 7.3 EdgeReportGraph

Runs as a Celery task after DigestGraph completes. Reads scored articles and summaries from DB.

```python
class EdgeReportState(TypedDict):
    user_id: str
    digest_id: str
    digest_articles: list[ScoredArticle]
    edge_profile: EdgeProfile
    prior_edge_report: str | None       # previous week's report for continuity
    ai_capability_items: list[ScoredArticle]  # filtered: AI capability advances
    edge_report: str
    skill_deltas: list[SkillDelta]      # extracted skill durability changes

# Nodes:
# load_context(state)             → fetch digest + edge profile + prior report
# filter_ai_capability(state)     → extract AI advance items from digest
# generate_report(state)          → claude-sonnet-4-6; structured edge report
# extract_skill_deltas(state)     → claude-haiku; parse report for skill changes
# persist_report(state)           → write edge_reports + update skill_durability
```

**Edge report prompt** (externalized to `app/prompts/edge_report.md`):
```
Role: Personalized AI capability analyst for a senior technical professional.

STRICT RULES:
- Every capability claim must cite a specific article from the digest (by title)
- Name specific skills (e.g. "distributed consensus protocol design"),
  never categories (e.g. "systems skills")
- "One thing to do" must be an actionable reading or practice — not "learn more about X"
- FORBIDDEN PHRASES: "AI is advancing rapidly", "stay ahead of the curve",
  "landscape is evolving", "exciting developments", "unprecedented"
- If insufficient domain-specific content exists, say so explicitly — do not generate generic content

User domain: {domains}
Role: {role}, {experience_years} years
Edge profile: {edge_profile_summary}
Prior report summary: {prior_report_summary}
This week's digest (scored articles): {digest_articles}

Output format (strict markdown):
## What Changed This Week in AI — Your Domains Only
## Skill Durability Update
## Your Edge This Week
## One Thing to Do
```

---

### 7.4 ReviewGraph

Triggered when a concept node is due for spaced review. Can run via WebSocket (real-time) or Celery (batch pre-generation).

```python
class ReviewState(TypedDict):
    user_id: str
    node_id: str
    concept: GraphNode                  # label, domain, familiarity, review_count
    related_articles: list[Article]     # source articles for this concept
    question: str
    user_answer: str | None
    outcome: str | None                 # correct | incorrect
    sm2_update: SM2Update               # new interval, ease, due_at

# Nodes:
# load_concept(state)          → fetch node + related articles
# generate_question(state)     → claude-haiku; generates review question
# evaluate_answer(state)       → claude-haiku streaming; evaluates + streams
# compute_sm2(state)           → pure function; SM-2 interval/ease recalculation
# update_node(state)           → write graph_nodes SM-2 fields
# update_progression(state)    → write progression_events (review_survived or review_failed)
```

**SM-2 implementation note:** `compute_sm2` is a pure function with no LLM call. Standard algorithm: `new_interval = max(1, old_interval × ease)` if correct; `interval = 1` if incorrect. Ease factor adjusts ±0.1 based on outcome, bounded [1.3, 2.5]. Implementation should follow the canonical SuperMemo SM-2 spec, not be improvised.

---

### 7.5 ExploreGraph

Triggered by HTTP request to `/explore/search` or `/explore/deep-research`. Standard search is synchronous (~2 sec). Deep research is async Celery job (~30–60 sec).

```python
class ExploreState(TypedDict):
    user_id: str
    query: str
    mode: str                           # standard | deep_research
    edge_profile: EdgeProfile
    corpus_results: list[ScoredArticle] # pgvector similarity search results
    web_results: list[WebResult]        # fallback if corpus insufficient
    synthesis: str
    citations: list[Citation]
    follow_up_queries: list[str]        # deep research only: sub-questions explored

# Standard mode routing:
# load_context → search_corpus → check_corpus_coverage
#   → sufficient: synthesize_from_corpus → format_response → END
#   → insufficient: search_web → synthesize_combined → format_response → END

# Deep research mode routing (additional nodes):
# generate_sub_queries → [parallel search per sub-query] → synthesize_all
#   → extract_gaps → suggest_learning_path → format_report → END
```

---

### 7.6 Prompt Management

All prompts externalized to `app/prompts/*.md`. Loaded at graph initialization, not hard-coded in nodes. This allows prompt iteration without code deployment.

```
app/prompts/
├── scoring.md
├── summary_technical.md
├── summary_narrative.md
├── summary_bullet.md
├── summary_socratic.md
├── challenge_generate.md
├── challenge_evaluate.md
├── edge_report.md
├── graph_extract.md
├── review_generate.md
└── explore_synthesize.md
```

Prompt loading pattern:
```python
# app/prompts/__init__.py
from pathlib import Path

def load_prompt(name: str) -> str:
    return (Path(__file__).parent / f"{name}.md").read_text()
```

---

### 7.7 Cost Optimization Strategy

| Operation | Graph | Model | Frequency | Tokens est. | Cost/user/week |
|---|---|---|---|---|---|
| Article scoring | DigestGraph | claude-sonnet-4-6 | Weekly | 15K in / 4K out | ~$0.06 |
| Summaries (8 × 4 styles) | DigestGraph | claude-haiku | Weekly | 12K in / 8K out | ~$0.01 |
| Challenge generation (8) | DigestGraph | claude-sonnet-4-6 | Weekly | 8K in / 2K out | ~$0.03 |
| Edge report | EdgeReportGraph | claude-sonnet-4-6 | Weekly | 5K in / 2K out | ~$0.02 |
| Challenge evaluation (avg 3) | ChallengeGraph | claude-sonnet-4-6 | Per interaction | 3K in / 1K out | ~$0.02 |
| Review challenge (avg 4) | ReviewGraph | claude-haiku | Per review | 1.5K in / 0.5K out | ~$0.004 |
| Graph extraction (3) | ChallengeGraph | claude-haiku | Per completion | 2K in / 1K out | ~$0.002 |
| **Total per Pro user/week** | | | | | **~$0.15** |

**Key levers:**
- Platform-level scoring cache in `DigestGraph`: score articles once per platform, reuse for users with ≥70% domain overlap. Cache in Redis keyed by `article_id + domain_set_hash`.
- Haiku for all bulk/non-real-time nodes; Sonnet only where reasoning quality is product-critical
- LangGraph state checkpointing: failed digest resumes from last successful node — no duplicate Claude API calls on retry
- Batch API for `generate_summaries` fan-out when available

---

## 8. API Specification

### 8.1 REST Endpoints

```
Base URL: /api/v1
Auth: Clerk JWT via Authorization: Bearer {token} header

-- DIGESTS --
GET    /digests                         # List user's digests (paginated)
GET    /digests/latest                  # Get most recent digest
GET    /digests/{id}                    # Get digest detail
GET    /digests/{id}/markdown           # Get markdown export (Pro)
POST   /digests/{id}/regenerate         # Trigger regeneration (rate limited)

-- ARTICLES --
GET    /articles/{id}                   # Get article detail with scores
POST   /articles/{id}/feedback          # Submit feedback signal (-1, 0, 1)

-- ARTICLE LIFECYCLE (This Week / Queue / Library are views over status) --
POST   /articles/{id}/status            # Transition status: queued|in_progress|completed|dismissed
GET    /queue                           # Working set: queued + in_progress, sorted by signal+age
GET    /library                         # Completed items, reverse chronological
GET    /library?domain={d}&since={date} # Filtered library view

-- CHALLENGES --
GET    /challenges                      # List user's challenges
GET    /challenges/pending              # Get unanswered challenges
GET    /challenges/{id}                 # Get challenge detail
POST   /challenges/{id}/respond         # Submit answer (triggers evaluation)

-- PROGRESSION & REVIEW (game layer) --
GET    /progression                     # Edge score, rhythm, mastery counts
GET    /progression/events              # Recent progression events (activity feed)
GET    /review/due                      # Concepts due for spaced review
POST   /review/{node_id}/respond        # Answer a review challenge (updates SM-2 schedule)

-- EXPLORE --
POST   /explore/search                  # Search curated corpus
POST   /explore/deep-research           # Trigger deep research job (async)
GET    /explore/research/{job_id}       # Poll deep research status

-- KNOWLEDGE GRAPH --
GET    /graph                           # Get user's full graph
GET    /graph/nodes/{id}                # Get node detail with connected articles
POST   /graph/nodes                     # Manually add node
POST   /graph/edges                     # Manually add edge
GET    /graph/export                    # Export as markdown or JSON
GET    /graph/gaps                      # Get suggested gap areas

-- EDGE INTELLIGENCE --
GET    /edge/report/latest              # Get latest edge report
GET    /edge/reports                    # List all edge reports
GET    /edge/skills                     # Get skill durability map
GET    /edge/score                      # Get current edge score

-- LEARNING PATHS --
GET    /paths                           # List user's learning paths
POST   /paths                           # Create new path
GET    /paths/{id}                      # Get path detail
PATCH  /paths/{id}/items/{item_id}      # Mark item complete/incomplete
POST   /paths/generate                  # AI-generate path from goal

-- SOURCES --
GET    /sources                         # Browse source library
GET    /sources?domain={domain}         # Filter by domain
POST   /sources/custom                  # Add custom source (Pro)
DELETE /sources/custom/{id}             # Remove custom source

-- PREFERENCES --
GET    /preferences                     # Get user preferences
PATCH  /preferences                     # Update preferences
GET    /edge-profile                    # Get edge profile
PATCH  /edge-profile                    # Update edge profile

-- WEBHOOKS --
POST   /webhooks/clerk                  # Clerk lifecycle events
```

### 8.2 WebSocket Events

```
Connection: wss://api.signal.app/ws?token={jwt}

-- Server → Client --
digest.ready          {digest_id, summary_stats}
challenge.evaluation  {challenge_id, chunk, is_final}
graph.updated         {nodes_added, edges_added}
edge.score_changed    {delta, new_score, reason}
review.due            {node_id, concept, count_due}
progression.event     {event_type, delta, new_edge_score}
digest.generating     {step, total_steps, message}

-- Client → Server --
challenge.respond     {challenge_id, answer}
review.respond        {node_id, answer}
ping                  {}
```

### 8.3 Error Response Format

```json
{
  "error": {
    "code": "DIGEST_GENERATION_FAILED",
    "message": "Digest generation failed after 3 retries",
    "detail": "Claude API returned 529 on final attempt",
    "request_id": "req_abc123",
    "retry_after": 3600
  }
}
```

---

## 9. Frontend Architecture

### 9.1 Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Framework | Next.js 14 (App Router) | SSR for SEO on public pages; RSC for digest rendering; static export for landing |
| Language | TypeScript (strict mode) | Required for agent-readable codebase |
| Styling | Tailwind CSS + CSS variables | Design system tokens as CSS vars; Tailwind for utility classes |
| State | Zustand (client) + React Query (server) | Zustand for UI state (panel collapse, graph viewport); React Query for all API data |
| Graph viz | D3.js (force-directed) | Knowledge graph rendering; full control over layout and animation |
| Rich text | React Markdown + rehype-highlight | Digest and edge report rendering with code highlighting |
| WebSocket | native WebSocket + reconnect | Challenge evaluation streaming |
| Auth | @clerk/nextjs | Client-side Clerk integration |
| Email | React Email + Resend | Digest emails built as React components |
| Testing | Vitest + Playwright | Unit + E2E |

### 9.2 Route Structure

```
app/
├── (public)/
│   ├── page.tsx                    # Landing page
│   ├── pricing/page.tsx
│   └── about/page.tsx
│
├── (auth)/
│   ├── sign-in/page.tsx
│   └── sign-up/page.tsx
│
└── (app)/                          # Protected routes
    ├── layout.tsx                  # Three-panel shell
    ├── dashboard/page.tsx          # This Week (current digest intake)
    ├── digest/
    │   ├── page.tsx                # Latest digest
    │   └── [id]/page.tsx           # Specific digest
    ├── queue/page.tsx              # Working set (queued + in_progress)
    ├── library/page.tsx           # Completed record (feeds graph + review)
    ├── explore/page.tsx            # Search + deep research
    ├── graph/page.tsx              # Knowledge graph canvas
    ├── paths/
    │   ├── page.tsx                # Learning paths list
    │   └── [id]/page.tsx           # Path detail
    ├── edge/page.tsx               # Edge intelligence full view
    ├── archive/page.tsx            # All past digests (read-only history)
    └── settings/
        ├── page.tsx                # General settings
        ├── domains/page.tsx
        ├── sources/page.tsx
        └── profile/page.tsx
```

### 9.3 Key Component Architecture

```
components/
├── layout/
│   ├── AppShell.tsx               # Three-panel layout manager
│   ├── NavPanel.tsx               # Left navigation
│   └── EdgePanel.tsx              # Right edge intelligence panel
│
├── digest/
│   ├── DigestDocument.tsx         # Full digest renderer
│   ├── DigestTier.tsx             # Tier section (🔴 🟡 🔵 🗄️)
│   ├── ArticleCard.tsx            # Article with expand/collapse + lifecycle actions
│   ├── ArticleSummary.tsx         # Cliff-notes in chosen style
│   └── FeedbackControls.tsx       # Thumbs up/skip/down
│
├── lifecycle/
│   ├── QueueView.tsx              # Working set (queued + in_progress)
│   ├── LibraryView.tsx           # Completed record
│   └── StatusActions.tsx         # Save / Mark read / Dismiss
│
├── challenge/
│   ├── ChallengeModal.tsx         # Full challenge flow
│   ├── ChallengeInput.tsx         # Answer text area
│   └── EvaluationStream.tsx       # Streaming evaluation renderer
│
├── graph/
│   ├── GraphCanvas.tsx            # D3 force-directed graph
│   ├── NodeDetail.tsx             # Click node popover
│   └── EdgeFrontier.tsx           # AI encroachment frontier line
│
├── progression/
│   ├── EdgeScore.tsx              # Central edge score indicator
│   ├── RhythmTracker.tsx          # Weekly consistency (forgiving streak)
│   ├── DueForReview.tsx           # Spaced-repetition queue
│   └── ReviewChallenge.tsx        # Review challenge UI
│
├── edge/
│   ├── EdgeReport.tsx             # Weekly edge report renderer
│   └── SkillMap.tsx               # Skill durability visualization
│
├── explore/
│   ├── SearchBar.tsx              # Cited search input
│   ├── SearchResults.tsx          # Results with Signal scores
│   └── DeepResearchPanel.tsx      # Deep research job status
│
└── ui/                            # Design system primitives
    ├── Button.tsx
    ├── Card.tsx
    ├── Badge.tsx                  # Domain tags, tier indicators
    ├── Score.tsx                  # Signal/durability score display
    └── StreamingText.tsx          # Progressive text renderer
```

### 9.4 Design Token Implementation

```css
/* globals.css — CSS custom properties */
:root {
  --bg-base:        #0D0F12;
  --bg-surface:     #141720;
  --bg-elevated:    #1C2030;
  --border:         #2A2F3D;
  --text-primary:   #E8EAF0;
  --text-secondary: #8B92A8;
  --text-muted:     #4A5068;
  --accent:         #5B8DEF;
  --tier-red:       #E05252;
  --tier-amber:     #D4922A;
  --tier-blue:      #4A9EBD;
  --tier-gray:      #4A5068;
  --success:        #4CAF82;
  --error:          #E05252;

  --font-display:   'Inter', system-ui, sans-serif;
  --font-body:      'Lora', Georgia, serif;
  --font-mono:      'JetBrains Mono', 'Fira Code', monospace;
  --font-ui:        'Inter', system-ui, sans-serif;

  --radius-sm:      4px;
  --radius-md:      6px;
  --radius-lg:      10px;

  --panel-nav:      240px;
  --panel-edge:     280px;
}
```

---

## 10. Infrastructure & DevOps

### 10.1 Initial Deployment (Railway)

**Services:**
```toml
# railway.toml
[build]
builder = "dockerfile"

[[services]]
name = "api"
source = "."
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
healthcheckPath = "/health"

[[services]]
name = "worker"
source = "."
startCommand = "celery -A app.worker worker --concurrency 4 --loglevel info"

[[services]]
name = "scheduler"
source = "."
startCommand = "celery -A app.worker beat --loglevel info"
replicas = 1  # must be exactly 1

[[services]]
name = "web"
source = "./frontend"
startCommand = "npm run start"
```

**Managed services (Railway):**
- PostgreSQL with pgvector extension enabled
- Redis 7

### 10.2 Environment Configuration

```bash
# Core
ANTHROPIC_API_KEY=
DATABASE_URL=
REDIS_URL=
SECRET_KEY=                         # JWT signing

# Auth
CLERK_SECRET_KEY=
CLERK_PUBLISHABLE_KEY=
CLERK_WEBHOOK_SECRET=

# Email
RESEND_API_KEY=
EMAIL_FROM=digest@signal.app

# AI Model config
CLAUDE_SCORING_MODEL=claude-sonnet-4-6
CLAUDE_SUMMARY_MODEL=claude-haiku-4-5-20251001
CLAUDE_EDGE_MODEL=claude-sonnet-4-6
CLAUDE_CHALLENGE_MODEL=claude-sonnet-4-6
CLAUDE_REVIEW_MODEL=claude-haiku-4-5-20251001

# LangGraph config
LANGGRAPH_CHECKPOINT_DB=postgresql+psycopg://...  # same as DATABASE_URL
LANGGRAPH_MAX_CONCURRENCY=4                       # parallel graph executions per worker

# Limits
MAX_ARTICLES_PER_DIGEST=100
MAX_SUMMARIES_PER_DIGEST=8
CHALLENGE_DAILY_LIMIT=10
EXPLORE_DEEP_RESEARCH_LIMIT=3       # per day, Pro

# Observability
SENTRY_DSN=
LOG_LEVEL=INFO

# Feature flags
FEATURE_KNOWLEDGE_GRAPH=true
FEATURE_DEEP_RESEARCH=false         # Phase 2
```

### 10.3 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml
      - run: ruff check .
      - run: mypy app/

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci && npm run test && npm run build

  deploy:
    needs: [test, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: railway up --service api
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      - run: railway up --service worker
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      - run: railway up --service web
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### 10.4 Python Project Structure

```
signal-backend/
├── app/
│   ├── main.py                     # FastAPI app init
│   ├── config.py                   # Settings (pydantic-settings)
│   ├── database.py                 # SQLAlchemy async engine
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── router.py
│   │   │   ├── digests.py
│   │   │   ├── articles.py
│   │   │   ├── challenges.py
│   │   │   ├── explore.py
│   │   │   ├── graph.py
│   │   │   ├── edge.py
│   │   │   ├── paths.py
│   │   │   ├── sources.py
│   │   │   ├── preferences.py
│   │   │   └── webhooks.py
│   │   └── websocket.py
│   │
│   ├── models/                     # SQLAlchemy models (mirror schema above)
│   ├── schemas/                    # Pydantic request/response models
│   │
│   ├── services/
│   │   ├── lifecycle_service.py    # Article status transitions (queue/library)
│   │   ├── progression_service.py  # Edge score, rhythm, progression events
│   │   ├── review_service.py       # Spaced repetition (SM-2 scheduling)
│   │   ├── ingestion_service.py    # Feed fetching + extraction
│   │   └── notification_service.py # Email + Slack delivery
│   │
│   ├── graphs/                     # LangGraph StateGraph definitions
│   │   ├── __init__.py
│   │   ├── digest_graph.py         # DigestGraph (main weekly pipeline)
│   │   ├── challenge_graph.py      # ChallengeGraph (real-time evaluation)
│   │   ├── edge_report_graph.py    # EdgeReportGraph (post-digest)
│   │   ├── review_graph.py         # ReviewGraph (spaced repetition)
│   │   ├── explore_graph.py        # ExploreGraph (search + deep research)
│   │   └── state_types.py          # TypedDict state schemas for all graphs
│   │
│   ├── worker/
│   │   ├── celery_app.py
│   │   ├── digest_tasks.py         # thin wrapper: invoke DigestGraph
│   │   ├── edge_report_tasks.py    # thin wrapper: invoke EdgeReportGraph
│   │   ├── ingestion_tasks.py      # feed fetch + embed (no LangGraph needed)
│   │   ├── review_tasks.py         # nightly decay job + invoke ReviewGraph
│   │   └── notification_tasks.py   # email + Slack (no LangGraph needed)
│   │
│   ├── prompts/                    # Prompt templates (externalized)
│   │   ├── scoring.md
│   │   ├── summary_technical.md
│   │   ├── summary_narrative.md
│   │   ├── summary_bullet.md
│   │   ├── summary_socratic.md
│   │   ├── challenge_generate.md
│   │   ├── challenge_evaluate.md
│   │   ├── review_challenge.md     # Spaced-repetition review question
│   │   ├── edge_report.md
│   │   └── graph_extract.md
│   │
│   └── middleware/
│       ├── auth.py                 # Clerk JWT validation
│       ├── rate_limit.py
│       └── cost_tracking.py        # Token usage logging
│
├── alembic/                        # Database migrations
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── docker-compose.yml              # Local development
```

### 10.5 Local Development

```yaml
# docker-compose.yml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: signal
      POSTGRES_PASSWORD: signal
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    env_file: .env.local
    depends_on: [postgres, redis]
    ports:
      - "8000:8000"

  worker:
    build: .
    command: celery -A app.worker worker --loglevel debug
    volumes:
      - .:/app
    env_file: .env.local
    depends_on: [postgres, redis]

  scheduler:
    build: .
    command: celery -A app.worker beat --loglevel debug
    volumes:
      - .:/app
    env_file: .env.local
    depends_on: [postgres, redis]
```

---

## 11. Cost Model

### 11.1 Per-User Economics

| Tier | Claude API/month | Infra/user/month | Total COGS | Revenue | Margin |
|---|---|---|---|---|---|
| Free (1 digest/week) | ~$0.24 | ~$0.10 | ~$0.34 | $0 | negative |
| Pro (weekly digest + challenges) | ~$0.56 | ~$0.25 | ~$0.81 | $18 | ~95% |
| Team (daily + team features) | ~$2.40 | ~$0.50 | ~$2.90 | $79 | ~96% |

Free tier is a loss leader — acceptable if conversion to Pro is ≥5%.

### 11.2 Infrastructure Scaling

| User count | Railway config | Monthly infra cost |
|---|---|---|
| 0–500 | Starter plan, shared Postgres | ~$50 |
| 500–2,000 | Pro plan, dedicated Postgres | ~$200 |
| 2,000–10,000 | Scale plan, Postgres + read replica | ~$800 |
| 10,000+ | Migrate to Kubernetes (EKS/GKE) | Variable |

---

## 12. Security & Privacy

### 12.1 Auth & Authorization

- All protected routes require valid Clerk JWT
- JWT validated on every request via middleware (no session store)
- User can only access their own data — all queries parameterized by `user_id` from JWT
- Clerk webhook events signed with `CLERK_WEBHOOK_SECRET` — verified before processing

### 12.2 Data Privacy

- Article content cached at platform level (no PII)
- User knowledge graph, edge profile, challenge answers: user-owned, deletable
- User deletion: Clerk webhook triggers cascade delete across all user tables
- No user data sold or shared with third parties
- Claude API calls: per Anthropic's data handling policy — no training on API data

### 12.3 Secret Management

- All secrets in environment variables, never in code or git
- Railway environment variables encrypted at rest
- `ANTHROPIC_API_KEY` never exposed to frontend
- GitHub Actions secrets for CI/CD

### 12.4 Rate Limiting

```python
# Per user per hour
RATE_LIMITS = {
    "api_requests": 200,
    "challenge_responses": 10,
    "explore_searches": 20,
    "deep_research_jobs": 3,     # Pro only
    "digest_regeneration": 1,
}
```

---

## 13. Build Sequence & Agent Task Breakdown

### Phase 0 — Personal MVP (Week 1–3)
*Goal: Working personal tool. Validates curation + scoring pipeline.*

**Agent Task 0.1: Repository Setup**
- Create GitHub repository `signal`
- Initialize Python project with `pyproject.toml`, `ruff`, `mypy`, `pytest`
- Initialize Next.js project in `frontend/`
- Set up `docker-compose.yml` for local development
- Configure GitHub Actions with test workflow
- Deliverable: Green CI on empty project

**Agent Task 0.2: Database Layer**
- Install pgvector on Postgres
- Implement SQLAlchemy async models for: users, sources, articles, article_scores, digests
- Write Alembic migrations
- Write model tests
- Deliverable: `alembic upgrade head` creates all tables; tests pass

**Agent Task 0.3: Ingestion Pipeline**
- Implement `ingestion_service.py`: feedparser + Readability extraction
- Implement `sources.yaml` loader
- Implement URL normalization + deduplication
- Write unit tests with mock feeds
- Deliverable: Given `sources.yaml`, fetches articles, stores to DB, deduplicates

**Agent Task 0.4: DigestGraph — Scoring Node**
- Install `langgraph`, `langgraph-checkpoint-postgres`, `anthropic`
- Define `DigestState` TypedDict in `app/graphs/state_types.py`
- Implement `score_articles` node function in `app/graphs/digest_graph.py`
- Externalize scoring prompt to `app/prompts/scoring.md`
- Implement `check_score_quality` conditional routing function
- Write tests with mock Claude responses using `langgraph` test utilities
- Deliverable: `score_articles` node scores a batch of articles and routes correctly

**Agent Task 0.5: DigestGraph — Summary + Challenge Nodes**
- Implement `generate_summaries` node (fan-out, Haiku, four styles)
- Implement `generate_challenges` node (Sonnet, one per tier-1/2 article)
- Externalize four summary prompts + challenge prompt to `app/prompts/`
- Write tests
- Deliverable: Given scored articles, returns summaries in all four styles + challenge questions

**Agent Task 0.6: DigestGraph — Full Graph + Render**
- Implement remaining nodes: `fetch_articles`, `deduplicate`, `render_digest`, `persist`, `notify`
- Wire full `DigestGraph` with all edges and conditional routing
- Implement Jinja2 markdown + HTML render templates
- Configure `SqliteSaver` for development checkpointing
- Implement MkDocs config + GitHub Pages deploy action
- Deliverable: `DigestGraph.invoke(state)` generates a complete markdown digest end-to-end

**Agent Task 0.7: GitHub Action**
- Weekly cron action invoking `DigestGraph` directly (no Celery in Phase 0)
- Commit generated markdown to repo
- Deploy to GitHub Pages via `peaceiris/actions-gh-pages`
- Deliverable: Sunday cron generates and publishes digest automatically

---

### Phase 1 — Multi-User Alpha (Week 4–10)
*Goal: 5 beta users receiving personalized digests via web UI.*

**Agent Task 1.1: FastAPI Foundation**
- Implement `app/main.py` with lifespan, CORS, error handlers
- Implement Clerk JWT middleware
- Implement `/health` endpoint
- Implement user creation via Clerk webhook
- Deliverable: API running on Railway, auth working end-to-end

**Agent Task 1.2: Celery Job Infrastructure**
- Set up Celery + Redis on Railway
- Implement `digest_tasks.py` wrapping digest service
- Implement `ingestion_tasks.py` for scheduled feed fetching
- Implement Celery Beat schedule (feed fetch: 6h, digest: per-user schedule)
- Deliverable: Jobs running on schedule, observable via Celery Flower

**Agent Task 1.3: Core API Endpoints**
- Implement: `/digests`, `/digests/{id}`, `/articles/{id}/feedback`, `/preferences`, `/sources`
- Write integration tests for each endpoint
- Deliverable: All endpoints tested and returning correct responses

**Agent Task 1.4: Next.js Shell**
- Implement three-panel `AppShell.tsx` with collapse behavior
- Implement `NavPanel.tsx` and `EdgePanel.tsx` (static initially)
- Implement Clerk auth flow (sign-in/sign-up pages)
- Apply design tokens from §9.4
- Deliverable: Authenticated shell renders with correct visual design

**Agent Task 1.5: Digest UI**
- Implement `DigestDocument.tsx`, `DigestTier.tsx`, `ArticleCard.tsx`
- Implement summary style toggle
- Implement `FeedbackControls.tsx` with optimistic updates
- Connect to API via React Query
- Deliverable: Full digest renders in browser with correct visual hierarchy

**Agent Task 1.6: Article Lifecycle (Queue & Library)**
- Implement `user_articles` table + migration
- Implement `lifecycle_service.py`: status transitions with timestamps
- Implement `/articles/{id}/status`, `/queue`, `/library` endpoints
- Implement Queue and Library views in frontend (lenses over status)
- Wire save/mark-read/dismiss actions on `ArticleCard.tsx`
- Deliverable: An article moves surfaced → queued → in_progress → completed; This Week / Queue / Library each show the correct subset with no duplication

**Agent Task 1.7: Email Delivery**
- Build digest email template using React Email
- Implement `notification_service.py` with Resend
- Add email delivery to digest generation pipeline
- Deliverable: Digest emailed to user after generation

**Agent Task 1.8: User Preferences UI**
- Implement domain selection with taxonomy tree
- Implement digest preferences form
- Connect to `/preferences` API
- Deliverable: User can configure domains, cadence, style, delivery

---

### Phase 2 — Edge Intelligence + Challenge Layer (Week 11–20)
*Goal: Full edge intelligence layer live. Challenge interaction working.*

**Agent Task 2.1: EdgeReportGraph**
- Implement `app/graphs/edge_report_graph.py` with `EdgeReportState` TypedDict
- Implement nodes: `load_context`, `filter_ai_capability`, `generate_report`, `extract_skill_deltas`, `persist_report`
- Externalize edge report prompt to `app/prompts/edge_report.md` with forbidden-phrases enforcement
- Implement `edge_report_tasks.py` Celery task as thin wrapper invoking `EdgeReportGraph`
- Implement `skill_durability` table population from `extract_skill_deltas` node output
- Migrate `PostgresSaver` from `SqliteSaver` for production checkpointing
- Deliverable: Edge report generated, stored, and `skill_durability` updated after each digest

**Agent Task 2.2: WebSocket Infrastructure**
- Implement WebSocket endpoint in FastAPI
- Implement client-side WebSocket hook with reconnect logic
- Implement `StreamingText.tsx` for progressive rendering
- Deliverable: WebSocket connection stable, streaming text renders correctly

**Agent Task 2.3: ChallengeGraph**
- Implement `app/graphs/challenge_graph.py` with `ChallengeState` TypedDict
- Implement nodes: `load_context`, `evaluate_answer` (streaming), `extract_graph_delta`, `update_graph`, `update_progression`, `complete`
- Externalize challenge evaluation prompt to `app/prompts/challenge_evaluate.md`
- Wire `evaluate_answer` to stream chunks via WebSocket using LangGraph streaming
- Implement challenge storage and history API endpoints
- Deliverable: User can answer a challenge and receive streamed evaluation; graph updates on completion

**Agent Task 2.4: Challenge UI**
- Implement `ChallengeModal.tsx` with text input
- Implement `EvaluationStream.tsx` with citation rendering
- Implement challenge history view
- Deliverable: Full challenge flow functional in browser

**Agent Task 2.5: Knowledge Graph — Backend**
- `extract_graph_delta` and `update_graph` nodes already implemented in `ChallengeGraph` (Task 2.3)
- Implement `graph_nodes` + `graph_edges` CRUD API endpoints
- Implement graph export endpoint (markdown + JSON)
- Implement gap analysis: query sparse subgraphs and return suggested fill concepts
- Deliverable: Graph builds incrementally from challenge completions; export works

**Agent Task 2.6: Knowledge Graph — Frontend**
- Implement `GraphCanvas.tsx` with D3 force-directed layout
- Implement node detail popover
- Implement frontier line animation (the signature element)
- Implement gap suggestion UI
- Deliverable: Knowledge graph renders and updates in real-time

**Agent Task 2.7: Edge Panel**
- Implement `EdgePanel.tsx` with: edge score, skill map summary, this week's challenge, path progress
- Implement `SkillMap.tsx` visualization
- Implement `EdgeReport.tsx` renderer
- Deliverable: Right panel populated with live edge intelligence data

**Agent Task 2.8: ExploreGraph**
- Implement `app/graphs/explore_graph.py` with `ExploreState` TypedDict
- Implement standard mode: `load_context → search_corpus → check_coverage → synthesize → format`
- Implement deep research mode: adds `generate_sub_queries → parallel_search → synthesize_all → suggest_path`
- Implement `/explore/search` (sync) and `/explore/deep-research` (async Celery) endpoints
- Implement `SearchBar.tsx` and `SearchResults.tsx` with Signal scores
- Deliverable: Explore mode functional with cited results and deep research option

**Agent Task 2.9: Learning Paths**
- Implement `learning_paths` API endpoints
- Implement path generation via Claude API
- Implement path progress tracking
- Implement `PathDetail.tsx` UI
- Deliverable: User can generate, view, and track learning paths

**Agent Task 2.10: Markdown Export**
- Implement `/digests/{id}/markdown` endpoint (Pro gate)
- Generate Obsidian-compatible YAML frontmatter
- Deliverable: Pro user can download digest as Obsidian-ready markdown

**Agent Task 2.11: Progression & Edge Score**
- Implement `user_progression` + `progression_events` tables
- Implement `progression_service.py`: event logging, edge score updates, weekly rhythm
- Wire progression events to: reading completion, challenge evaluation, review outcomes
- Emit `progression.event` and `edge.score_changed` over WebSocket
- Implement Edge Score + rhythm display in `EdgePanel.tsx`
- Deliverable: Edge score moves on real events; rhythm tracks engaged weeks; activity feed populated

**Agent Task 2.12: ReviewGraph + Spaced Repetition**
- Implement `app/graphs/review_graph.py` with `ReviewState` TypedDict
- Implement nodes: `load_concept`, `generate_question` (Haiku), `evaluate_answer` (Haiku streaming), `compute_sm2` (pure function — use canonical SM-2 spec, do not improvise), `update_node`, `update_progression`
- Externalize review prompt to `app/prompts/review_generate.md`
- Implement `review_tasks.py`: nightly Celery Beat job for familiarity decay + `review_due_at` recomputation
- Implement `/review/due` and `/review/{node_id}/respond` API endpoints
- Implement "Due for Review" section in `EdgePanel.tsx` and `ReviewChallenge.tsx` UI
- Deliverable: Concepts decay, resurface when due, correct review extends interval, difficulty adapts to mastery

---

### Phase 3 — Monetization & Growth (Week 21–32)

**Agent Task 3.1: Billing**
- Integrate Stripe via `stripe-python`
- Implement subscription creation, upgrade, downgrade, cancellation
- Implement tier enforcement middleware (feature gates)
- Implement billing UI (Stripe Customer Portal redirect)

**Agent Task 3.2: Onboarding Flow**
- Implement multi-step onboarding UI (§3.1)
- Implement edge profile questionnaire with conversational UI
- Implement first digest generation loading state
- Implement "first visit" welcome experience

**Agent Task 3.3: Team Tier**
- Implement team/organization data model
- Implement seat management
- Implement shared digest and team edge mapping
- Implement Slack integration (shared digest posting)

**Agent Task 3.4: Observability**
- Integrate Sentry (error tracking, performance)
- Implement cost tracking middleware (log Claude token usage per request)
- Implement digest funnel analytics (generated → opened → article clicked → challenge completed)
- Build internal ops dashboard

**Agent Task 3.5: Public Landing Page**
- Implement marketing site on `signal.app`
- Implement pricing page
- Implement SEO fundamentals

---

## 14. Architecture Decision Records

### ADR-001: FastAPI over Django REST Framework

**Status:** Accepted

**Context:** Python backend needed. Team experience with both.

**Decision:** FastAPI.

**Rationale:** Async-native aligns with Celery job model. Pydantic validation matches response schemas. Auto-generated OpenAPI docs useful for agent-readable API. Django's ORM advantages irrelevant given SQLAlchemy choice for pgvector support.

**Consequences:** No Django admin (acceptable — use internal dashboard). No built-in auth (acceptable — Clerk handles this).

---

### ADR-002: PostgreSQL + pgvector over Dedicated Vector DB

**Status:** Accepted

**Context:** Need vector similarity search for article deduplication and explore search. Options: pgvector extension on Postgres vs. dedicated Pinecone/Weaviate/Qdrant.

**Decision:** pgvector on PostgreSQL.

**Rationale:** At <10M articles, pgvector with IVFFlat index has acceptable query performance (<50ms p99 for 1536-dim vectors). Eliminates a second database system, operational overhead, and cost. Transactional consistency with article metadata in same DB. Revisit at scale.

**Consequences:** Will need to migrate to dedicated vector DB if article corpus exceeds ~50M rows or query latency degrades. That migration is well-understood.

---

### ADR-003: claude-haiku for Summaries, claude-sonnet for Edge + Challenges

**Status:** Accepted

**Context:** Claude API costs must be managed. Not all operations require maximum capability.

**Decision:** Tiered model usage.

**Rationale:** Summaries are structured, well-defined tasks where Haiku performs comparably to Sonnet at 10% of the cost. Edge reports and challenge evaluations require nuanced domain reasoning where Sonnet quality is material to product value. Scoring is a middle case — Sonnet used because mis-scoring affects all downstream UX.

**Consequences:** Need to monitor Haiku summary quality vs. Sonnet baseline. If quality diverges on specific domains, can add domain-specific model overrides.

---

### ADR-004: Celery + Redis over Cloud-Native Job Queue (SQS/Cloud Tasks)

**Status:** Accepted

**Context:** Need reliable scheduled and async job execution. Options: Celery+Redis, AWS SQS+Lambda, GCP Cloud Tasks, Railway Cron.

**Decision:** Celery + Redis.

**Rationale:** Railway managed Redis eliminates ops burden. Celery provides rich task primitives (retries, rate limiting, chaining, result backend). Same codebase as API — no Lambda cold start concerns. Team familiarity. Revisit if job volume requires fan-out at scale.

**Consequences:** Redis is a single point of failure for job queue. Mitigated by Railway's managed Redis HA. Will need to add dead letter queue pattern for failed jobs.

---

### ADR-005: D3.js for Knowledge Graph over React Flow / Vis.js

**Status:** Accepted

**Context:** Knowledge graph is the signature product element. Needs custom frontier line animation, precise layout control, and performance with 500+ nodes.

**Decision:** D3.js force-directed layout.

**Rationale:** D3 gives full control over physics, visual encoding, and custom SVG elements (frontier line). React Flow is too opinionated for the custom aesthetic. Vis.js has worse performance at scale. D3 is the right tool despite higher implementation complexity.

**Consequences:** Higher frontend development effort (~2x vs. React Flow). D3 + React integration requires careful effect management. Justified by product differentiation.

---

### ADR-006: Single Article Lifecycle over Separate Reading List and Digest Stores

**Status:** Accepted

**Context:** Early design treated "Digests" and "Reading List" as parallel nav destinations. This created a split-brain: an article surfaced in a digest and saved to a reading list existed conceptually in two places, with ambiguous status ownership ("if I read it from the list, does the digest update?").

**Decision:** A single per-user article lifecycle (`user_articles` table) with one status field (`surfaced → queued → in_progress → completed → dismissed`). This Week, Queue, and Library are read-only views over status, not separate stores.

**Rationale:** An article has exactly one status per user. The digest fills the queue; completion feeds the graph. Eliminates duplication and ambiguity. Makes the `completed` transition a single, unambiguous event — which the progression and spaced-repetition systems depend on.

**Consequences:** Digest becomes a generated view bounded by `surfaced_at`, not a container of articles. Archive view of old digests reconstructs from `source_digest_id`. Slightly more complex queries (status-filtered) traded for a vastly cleaner mental model and a clean event source for the game layer.

---

### ADR-007: Spaced Repetition + Edge Score over Full Gamification Suite

**Status:** Accepted

**Context:** Considered adopting Duolingo/Brilliant-style gamification to drive retention. The full suite (streaks, hearts, leagues, leaderboards, badges) risks reading as infantilizing to the target user (senior professionals) and can create compulsion loops detached from real learning.

**Decision:** Adopt only mechanics tied to genuine intellectual progress: spaced repetition (concept familiarity decay + SM-2 review scheduling), adaptive challenge difficulty, a forgiving weekly-rhythm consistency mechanic, and the Edge Score as the single central progression signal. Explicitly exclude leaderboards, leagues, hearts/lives, and cosmetic badges.

**Rationale:** Spaced repetition has strong learning-science backing and turns the knowledge graph from a passive record into an active retention tool. Every retained mechanic maps to a real signal (mastery, recall, edge growth). Competitive/social and loss-aversion mechanics carry perverse incentives for an audience whose value proposition is *their own* edge, not ranking against others.

**Consequences:** Requires a nightly decay/scheduling job and SM-2 implementation. The game layer is fully driven by the article lifecycle (ADR-006) and challenge completions — no separate event infrastructure. Forgoes the engagement spikes that aggressive streak mechanics produce, accepting steadier, less manipulative retention.

---

### ADR-008: LangGraph for All AI Workflows over Flat Service Functions

**Status:** Accepted

**Context:** The AI processing pipelines (digest generation, challenge evaluation, edge report, review, explore) are multi-step workflows with branching logic, retry behavior, partial failure modes, and shared state across steps. The original design implemented these as flat sequences of service function calls coordinated by Celery tasks.

**Options considered:**
- **Flat service functions** (original) — simple, low dependency count, familiar
- **LangGraph StateGraph** — explicit state schema, conditional routing, built-in checkpointing, streaming support
- **Prefect / Airflow** — full DAG orchestration, heavyweight for this use case

**Decision:** LangGraph for all AI workflows.

**Rationale:**

*State explicitness:* Each graph owns a TypedDict state schema. At any node boundary, the full state is inspectable. Debugging a failed digest means reading the state snapshot at the failed node — not re-running the entire pipeline or adding logging scaffolding.

*Conditional routing first-class:* The `check_score_quality` routing node (retry scoring if too few high-signal articles; degrade gracefully to archive-only digest) is trivial in LangGraph and awkward in flat service code. Challenge difficulty adaptation (route to harder or easier question generation based on recent performance) is similarly clean.

*Checkpointing = free retry resilience:* LangGraph's `PostgresSaver` checkpoints state after each node. A failed digest at the `generate_edge_report` node resumes there — no re-scoring, no re-summarizing, no duplicate Claude API calls. This is particularly valuable for the digest pipeline which involves 5–7 sequential LLM calls.

*Streaming:* `ChallengeGraph` streams evaluation chunks back to the WebSocket client per-node. LangGraph's streaming support handles this natively; flat functions would require manual chunk management.

*Team familiarity:* The team already uses LangGraph for enterprise AI agent work. No new learning curve.

**Consequences:** Adds `langgraph` and `langgraph-checkpoint-postgres` as dependencies. Celery tasks become thin wrappers (`graph.invoke(state)`) rather than orchestrators. Service functions become LangGraph node functions (plain async Python — no framework lock-in at the node level). The `PostgresSaver` shares the existing PostgreSQL instance — no additional infrastructure. Slightly more upfront graph wiring code justified by significantly better observability and resilience.

---

## 15. Open Questions & Risks

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| RSS feeds unreliable / paywalled | High | Medium | Readability fallback; source quality monitoring; consider newsletter parser (Mailgun inbound) for email newsletters |
| Claude API latency spikes during digest generation | Medium | Medium | Async generation (user not waiting); retry with backoff; status page communication |
| pgvector performance degrades at scale | Low | Medium | IVFFlat index tuned from day one; migration path to Pinecone documented in ADR-002 |
| Edge report quality too generic | High | Critical | Extensive prompt iteration before launch; human review of first 100 edge reports; explicit quality gate before monetization |
| Challenge evaluation quality too generic | Medium | High | Same approach as edge report; A/B test against user satisfaction signal |

### Product Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Perplexity ships edge intelligence before launch | Medium | High | Speed to market on Phase 0-1; ensure edge intelligence quality is materially better than generic "AI is changing your field" |
| Users open digest but don't complete challenges | High | Medium | Challenge completion is the core loop; track the surfaced→queued→completed funnel (now a clean status pipeline); spaced-repetition resurfacing and the forgiving weekly rhythm pull users back without dark patterns; A/B test challenge question quality |
| Free tier costs exceed acceptable burn | Medium | Medium | Free tier capped at 3 domains, weekly only, no challenges (challenges require evaluation = cost) |
| Knowledge graph too complex to build incrementally | Low | Medium | Phase 2 deliverable; can ship as "coming soon" without blocking Phase 1 launch |

### Open Decisions

- **Voice input for challenges** — Mobile use case suggests voice answer input. Adds Whisper API cost. Defer to Phase 3.
- **Podcast/transcript ingestion** — Latent Space, Dwarkesh, etc. publish transcripts. High-value source type but adds ingestion complexity. Phase 3.
- **Open-source curator core** — Open-sourcing `curator.py` and source library could drive community contributions and trust. Decision needed before GA.
- **Community signal** — Should aggregate upvote data (trending articles in a domain) be visible to users? Privacy/value tradeoff. Defer decision.
- **Mobile app** — Web-first. Responsive mobile web for Phase 1–2. Native app evaluation in Phase 3.
- **Obsidian plugin** — Direct vault sync via Obsidian plugin API would eliminate friction for the target user. Evaluate after Pro launch.