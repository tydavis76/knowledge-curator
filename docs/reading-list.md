---
tags: [reading-list, backlog]
---

# Reading List

Manually curated backlog — items worth reading that aren't part of the weekly digest cycle.
Organized by time commitment and domain.

---

## This Week (< 2 hours total)

### [Local-First Software](https://www.inkandswitch.com/local-first/) — Kleppmann et al., 2019
**Domain:** Distributed Systems / Knowledge Management | **~45 min**

The foundational essay for offline-capable, user-owned data systems. Direct relevance to
agent memory design: the seven ideals (no spinners, your data survives the cloud, works
offline, collaboration without servers) map cleanly onto constraints for autonomous agent
tooling. Read before designing any agent persistence layer.

### The Book of Why — Pearl, Chapters 1–3
**Domain:** Causal Inference / AI Foundations | **~60 min**

Establishes the ladder of causation (association → intervention → counterfactuals).
Changes how you reason about what LLMs can and cannot do — they're stuck on the first
rung. Pairs with Pearl's 2018 paper below for the technical argument.

---

## This Month (30–45 min/week)

### Designing Data-Intensive Applications — Kleppmann
**Domain:** Distributed Systems | **Ongoing**

Focus: chapters on replication, consistency models, and CRDTs. Read through the lens of
LangGraph agent state — where does eventual consistency cause problems in multi-agent
workflows? Where are linearizability guarantees actually required?

### Antifragile — Taleb
**Domain:** Systems Thinking / Risk | **Ongoing**

Cross-domain: systems that gain from disorder. Maps directly to resilience architecture —
what's the difference between robust (survives shocks) and antifragile (improves from
them)? Applies to both software systems and investment portfolios. Chainlink oracle design
as a case study.

### Chainlink Whitepaper + Oracle Security Threat Model
**Domain:** Distributed Systems / Crypto | **~2 hours total**

- [Chainlink 2.0 Whitepaper](https://research.chain.link/whitepaper-v2.pdf)
- [Oracle Manipulation: How it works](https://blog.chain.link/flash-loans-and-the-importance-of-tamper-proof-oracles/)

Feeds the investment thesis with systems-level intuition on cascade risk. Key question:
under what failure modes does oracle consensus break, and how does the incentive design
handle adversarial nodes?

---

## Reference Tier

### [Symbol Grounding Problem](https://plato.stanford.edu/entries/chinese-room/) — SEP
**Domain:** Philosophy of Mind / AI | **~20 min**

Settles the debate framing on LLM intentionality. The Chinese Room argument and its
rebuttals. Useful when distinguishing "understands" from "models the distribution of
tokens that follow from understanding."

### [Evolutionary Architecture and Fitness Functions](https://martinfowler.com/articles/evodb.html) — Fowler
**Domain:** Software Architecture | **~30 min**

The bliki series on treating architectural properties as testable constraints. Fitness
functions as architectural unit tests — maps to how agent evaluation should be
structured.

### [Theoretical Impediments to Machine Learning with Seven Sparks from the Causal Revolution](https://arxiv.org/abs/1801.04016) — Pearl, 2018
**Domain:** AI / Causal Inference | **~30 min**

The academic core of the causality argument. Seven things ML cannot do without causal
structure. Pairs with The Book of Why chapters 1–3.

---

## Completed

<!-- Move items here after reading with a brief note on what you took away -->
