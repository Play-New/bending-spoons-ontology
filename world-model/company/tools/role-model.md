---
id: role-model
type: tool
title: Role Model — recruiting technology
status: confirmed
purpose: run the extreme Spooner hiring funnel — the primitive that produces the talent the whole machine redeploys
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: platform-primitive
mcp: invocable-tool
relations:
  - { type: part-of, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: produces, target: spooners, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Role Model

**Properties** (per `../../../ontology.md` §1 `Tool`): function — recruiting technology (the Spooner funnel) · built 2017 · usage — tens of thousands of applications per talent manager/yr · AI-based — yes (assessments + models) · deployed-across-portfolio — no (talent intake).
**Links:** `part-of`→Platform · `produces`→Spooners.

The talent primitive. Role Model is a recruiting technology that supports the Talent team end to end; it draws on first-party assessments and AI models to improve the quality of hiring decisions, and lets each talent manager handle tens of thousands of job applications per year (`bsp-f1` ~L2556-2558). If the other primitives make an acquired business worth more, Role Model makes the People half of the Platform — the reallocatable core team — possible at all.

```
primitive: role-model
does:
  - run the Spooner funnel end to end (candidate assessment through hire decision)
  - draw on first-party assessments + AI models to improve hiring quality
  - let each talent manager process TENS OF THOUSANDS of applications per year
evolved: from streamlining recruiting ops into an automated advisor trained on historical
         outcomes, including extensive post-hire performance data
began: investment started 2017
```

How the intelligence layer composes it: it is the intake for the People layer that everything else depends on. The funnel it runs (around 800,000 applications, 286 hired in 2025 — under 0.04%, `../platform.md`) produces the high-density, flexibly-redeployable Spooners the machine moves across the portfolio to execute transformations. It is included as a first-class primitive because talent is treated as movable infrastructure, the same way data and payments are.

## References
- `bsp-f1` — Role Model is recruiting technology supporting the Talent team end to end; draws on first-party assessments and AI models to improve hiring decisions; helps each talent manager handle tens of thousands of applications per year; investment started 2017, evolving into an automated advisor trained on historical outcomes including post-hire performance data (~L2556-2560).
