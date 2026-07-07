---
id: janus-orion
type: tool
title: Janus / Orion — experimentation toolkit
status: confirmed
purpose: run rigorous, high-concurrency experiments so every product and pricing decision is decided by evidence, portfolio-wide
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: platform-primitive
mcp: invocable-tool
relations:
  - { type: part-of, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: deployed-across, target: business, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
  - { type: reads, target: pico-lumen-abacus, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Janus / Orion

**Properties** (per `../../../ontology.md` §1 `Tool`): function — experimentation toolkit (concurrent A/B, audience targeting) · built 2017 · usage — >3,000 experiments in 2025 · AI-based — (targeting) · deployed-across-portfolio — yes.
**Links:** `part-of`→Platform · `deployed-across`→Business · `reads`→pico-lumen-abacus.

The experimentation toolkit. Janus and Orion together enable rapid and rigorous product iteration: advanced audience targeting and the concurrent execution of hundreds of experiments with minimal operational overhead (`bsp-f1` ~L2550-2551). It is how the machine decides — a claim becomes a change only after an experiment says so.

```
primitive: janus-orion
does:
  - run concurrent A/B experiments with advanced audience targeting, low operational overhead
  - turn product/pricing hypotheses into measured decisions
scale: more than 3,000 experiments run in 2025
began: 2017 (increasing sophistication over time)
```

How the intelligence layer composes it: it is the decision procedure the transform/monetize verbs run through. A pricing move proposed off `minerva`'s LTV signal is validated in Janus/Orion before it ships through `juno`; the results write back through `pico-lumen-abacus`. Deployed on every acquired business, it is why transformations are evidence-driven and repeatable rather than bespoke.

## References
- `bsp-f1` — Janus and Orion constitute the experimentation toolkit enabling rapid, rigorous product iteration; support advanced audience targeting and concurrent execution of hundreds of experiments with minimal overhead; more than 3,000 experiments run in 2025; began developing in 2017 (~L2550-2552).
