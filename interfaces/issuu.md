---
id: issuu-interface
type: interface
title: Issuu
status: confirmed
purpose: the Issuu delivery interface — where the machine meets its users, and the capabilities bundled in it today
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
properties:
  business: issuu
  category: digital publishing
  capabilities_delivered: digital publishing · flipbook distribution
  ai_features: n.d.
  status: live
relations:
  - { type: of, target: issuu, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Issuu — interface

**Properties** → structured in the frontmatter above, 1:1 with `interfaces.csv` (per `../ontology.md §1 Interface`).
**Link:** `Interface —of→ Business` (declared here, once) → `../world-model/company/businesses/issuu.md` — the asset behind this interface; its operating data (revenue, retention, margin) lives there and in `../world-model/company/businesses.csv`.

The Issuu interface delivers, bundled inside itself, the capabilities the model maps in `README.md` (per `bsp-f1` ~L4932): digital publishing · flipbook distribution. Today a capability serves only the users of the interface it ships in — that bundling is the confirmed state of Bending Spoons today; what unbundling would mean is the analysis (`../bending-spoons-as-an-intelligence.md §3`).
