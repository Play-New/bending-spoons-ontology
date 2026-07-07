---
id: pico-lumen-abacus
type: tool
title: Pico / Lumen / Abacus — the data infrastructure
status: confirmed
purpose: the standardized data spine every acquired business is migrated onto; ingest → transform → serve metrics, one contract across the whole portfolio
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: platform-primitive
mcp: invocable-tool
relations:
  - { type: part-of, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: deployed-across, target: business, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Pico / Lumen / Abacus

**Properties** (per `../../../ontology.md` §1 `Tool`): function — data infrastructure (ingest → transform → serve metrics) · built 2017 · usage — >3.8B data points/day (Q1 2026) · AI-based — yes (schema harmonization, field-purpose inference) · deployed-across-portfolio — yes.
**Links:** `part-of`→Platform · `deployed-across`→Business.

The data spine of the Platform. Three tightly-integrated services that, taken together, give every business in the group one consistent way to move and read its data (`bsp-f1` ~L2532). It is the substrate the other primitives compose on: nothing downstream (LTV, experiments, monetization) works without a standardized data layer underneath it.

```
primitive: pico-lumen-abacus
  pico    — high-throughput data INGESTION
  lumen   — data TRANSFORMATION
  abacus  — computes and SERVES standardized metrics at scale
does:
  - ingest, harmonize, and serve one standardized metric set across all businesses
  - process >3.8 billion data points per day on average (Q1 2026)
  - use AI to harmonize schemas, tag events, infer the purpose of data fields (incl. privacy/compliance)
deployed: migrated onto every acquired business — the first thing the group lays down so a
          new business can be measured against portfolio benchmarks from day one
began: 2017 — a key area of investment ever since
```

How the intelligence layer composes it: it is the read/write surface the whole loop runs against. A newly acquired business is put on Pico/Lumen/Abacus so its metrics become comparable to the rest of the portfolio; `minerva` consumes its output to predict user value; `janus-orion` reads and writes experiment metrics through it. It is the reason a target can run "pricing, prediction, and monetization it could not before" the day the deal closes (`../platform.md`).

## References
- `bsp-f1` — Pico/Lumen/Abacus form the data infrastructure; supports consistent analysis across all businesses; processed more than 3.8 billion data points per day on average in Q1 2026; Pico ingests, Lumen transforms, Abacus computes and serves standardized metrics; AI harmonizes schemas / tags events / infers field purpose; began developing in 2017 (~L2532-2534, ~L2535-2537).
