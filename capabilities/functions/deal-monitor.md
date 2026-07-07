---
id: capability-deal-monitor
type: function
title: Monitor — watch the held businesses against their underwriting
status: confirmed
purpose: the downstream continuous loop; verify that transformed businesses deliver the returns they were underwritten to
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: agent
mcp: activatable-agent
relations:
visibility: shared
---
# Capability — monitor (agent)

The always-on downstream loop over the held portfolio (one of the two loops that are the recurring value; `market-radar` is the other). It watches each business against the return it was underwritten to.

```
function: monitor                   # the drift reading (../../ontology.md §2); read-only
input:
  - scope             # a held Business or the whole portfolio
  - period
computation:          # logic: judgment loop (agent) — the agent decides what to READ next, never writes
  - snapshot the operating properties (businesses.csv: nrr_pct, arpu, paying_customers_m,
    adj_op_margin_pct) and cash generation for the period
  - compare realized vs underwritten: the case behind the Deal's irr and the Target's
    walk-away price (deals.csv, targets.csv)
  - DISTINGUISH growth from new users vs growth from price extraction on a slowly declining base
    (the F-1's own per-business notes repeatedly show revenue up on higher revenue-per-subscriber while the
     subscriber count FALLS — Evernote bsp-f1 ~L1865, Splice ~L1868, Issuu/StreamYard ~L1872 — flag which is which;
     NRR itself "can fluctuate significantly... often as a result of monetization initiatives", ~L409)
output: a drift report per business — holding vs drifting, and which kind of growth [derived] —
  escalated to the human. It never self-corrects: a corrective move is deal-optimize's
  transaction, behind that action's own gate.
```

Its blind spot is itself a finding: it monitors **per-product** because that is all the model holds. It cannot watch a *customer* across products, because there is no cross-product customer graph (`../../world-model/customer/cross-product-graph.md`). The thing it cannot monitor is the roadmap.

## References
- `bsp-f1` — per-business revenue-per-subscriber vs subscriber-count dynamics (~L1865-1876); portfolio NRR 93%/91%/95%/94% for 2023/2024/2025/Q1 2026 (~L407) and by business (AOL 95%, Evernote 99%, Remini 87%, StreamYard 91%, ~L408); revenue-weighted average subscriber tenure 8.0 years (~L411); average revenue per MAU 2.5x higher 2025 vs 2022 at Evernote (~L2756) and 64% higher 2025 vs 2023 at StreamYard (~L2810); portfolio 500M+ MAU / 9M+ paying customers in March 2026 (~L361).
