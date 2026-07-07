---
id: minerva
type: tool
title: Minerva — real-time user-LTV predictor
status: confirmed
purpose: estimate every user's lifetime value in real time and feed it into marketing and monetization decisions across the whole portfolio
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: platform-primitive
mcp: invocable-tool
relations:
  - { type: part-of, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: consumes, target: pico-lumen-abacus, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: deployed-across, target: business, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Minerva

**Properties** (per `../../../ontology.md` §1 `Tool`): function — real-time user-LTV prediction · built 2019 · usage — multi-year predictions, scaled by orders of magnitude · AI-based — yes · deployed-across-portfolio — yes.
**Links:** `part-of`→Platform · `consumes`→pico-lumen-abacus · `deployed-across`→Business.

The predictor. Minerva uses AI to estimate user lifetime value, updates its predictions in real time, and feeds those predictions as inputs into other internal systems — improving the quality of marketing and monetization decisions (`bsp-f1` ~L2539-2540). It is where the standardized data becomes a per-user judgment the machine can act on.

```
primitive: minerva
does:
  - estimate user lifetime value, updated in REAL TIME
  - provide critical inputs to other internal systems (pricing, marketing spend, monetization)
  - carry insights ACROSS products — leverage data from other products to generate insights
    for a newly acquired business, so a fresh acquisition inherits the group's priors
supports: multi-year LTV predictions; scaled to loads greater by orders of magnitude
began: 2019
```

How the intelligence layer composes it: Minerva sits on top of `pico-lumen-abacus` output and turns it into a value signal the loop steers on — which cohorts to acquire, where to spend, what to charge. Its cross-product reach (using one product's data to bootstrap predictions for a newly acquired one) is the closest present-day approximation of a shared customer signal, and the seed the analysis reads as the start of the customer graph (`../../../bending-spoons-as-an-intelligence.md §3`).

## References
- `bsp-f1` — Minerva leverages AI to estimate user lifetime value; updates predictions in real time; provides critical inputs to other internal systems; improves marketing and monetization decisions; began developing in 2019 and enhanced since to support multi-year predictions, leverage data from other products for newly acquired businesses, and scale by orders of magnitude (~L2539-2541).
