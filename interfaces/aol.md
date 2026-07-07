---
id: aol-interface
type: interface
title: AOL
status: confirmed
purpose: the AOL delivery interface — where the machine meets its users, and the capabilities bundled in it today
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
properties:
  business: aol
  category: email/news/search
  capabilities_delivered: email · news feed · search · consumer security/identity add-ons
  ai_features: n.d.
  status: live
relations:
  - { type: of, target: aol, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# AOL — interface

**Properties** → structured in the frontmatter above, 1:1 with `interfaces.csv` (per `../ontology.md §1 Interface`).
**Link:** `Interface —of→ Business` (declared here, once) → `../world-model/company/businesses/aol.md` — the asset behind this interface; its operating data (revenue, retention, margin) lives there and in `../world-model/company/businesses.csv`.

The AOL interface delivers, bundled inside itself, the capabilities the model maps in `README.md` (per `bsp-f1` ~L377-397): email · news feed · search · consumer security/identity add-ons. Today a capability serves only the users of the interface it ships in — that bundling is the confirmed state of Bending Spoons today; what unbundling would mean is the analysis (`../bending-spoons-as-an-intelligence.md §3`).
