---
id: deal
type: deal
title: Deal — the acquisition event
status: confirmed
purpose: the transaction that turns a Target into a Business and books the purchase-price allocation
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
relations:
  - { type: of, target: target, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: produces, target: business, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Deal — the acquisition event

The atomic **event** of the machine: one acquisition. It takes a `Target`, pays a consideration, and produces a `Business` — booking the purchase-price allocation (PPA). **The deal's data is kept separate from the business's operating data** (Deal ⊥ Business ⊥ Interface): consideration, deal-type, date and PPA belong to the `Deal`; revenue, users and retention belong to the `Business` it produces; the app the user touches is the `Interface`. Its instances are the roster in `deals.csv`.

Bending Spoons has completed **more than 50** acquisitions since 2013 (`bsp-f1` ~L326), at a pace of 1 (2023), 5 (2024), 6 (2025), 2 (Q1 2026) (`bsp-f1` ~L328). Aggregate enterprise value scaled ~10×: $194M → $876M → $1.92B → $2.01B (Q1 2026 alone) (`bsp-f1` ~L333; the filing states the same series endpoints as "capital deployed in acquisitions", ~L111 — two phrasings, one series). Each is underwritten to the IRR hurdle (65% levered / 25% unlevered) on five years of free cash flow plus a terminal value, **assuming the business is never sold** (`bsp-f1` ~L334-340).

- properties (per `../../ontology.md §1 Deal`, 1:1 with `deals.csv`): consideration · enterprise value · deal-type (acquisition / asset-deal / carve-out) · IRR · cohort year · date · PPA {goodwill, customer base, IP, trademark}
- links: `of`→Target (FK `deals.csv.of_target`; `n.d.` for acquisitions predating the pipeline snapshot) · `produces`→Business (FK `deals.csv.produces_business`)
- backed by: `deals.csv` (one row per acquisition: date · type · consideration · PPA · the two link FKs)

## References
- `bsp-f1` — more than 50 acquisitions (~L326); cadence per year (~L328); aggregate enterprise value per year (~L333); IRR hurdles + the underwrite-assuming-no-sale method (~L334-340).
