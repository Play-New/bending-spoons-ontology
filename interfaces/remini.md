---
id: remini-interface
type: interface
title: Remini
status: confirmed
purpose: the Remini delivery interface — where the machine meets its users, and the capabilities bundled in it today
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
properties:
  business: remini
  category: consumer AI photo/video
  capabilities_delivered: image/video enhancement · generative restoration
  ai_features: AI-native
  status: live
relations:
  - { type: of, target: remini, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Remini — interface

**Properties** → structured in the frontmatter above, 1:1 with `interfaces.csv` (per `../ontology.md §1 Interface`).
**Link:** `Interface —of→ Business` (declared here, once) → `../world-model/company/businesses/remini.md` — the asset behind this interface; its operating data (revenue, retention, margin) lives there and in `../world-model/company/businesses.csv`.

The Remini interface delivers, bundled inside itself, the capabilities the model maps in `README.md` (per `bsp-f1` ~L377-397): image/video enhancement · generative restoration. Today a capability serves only the users of the interface it ships in — that bundling is the confirmed state of Bending Spoons today; what unbundling would mean is the analysis (`../bending-spoons-as-an-intelligence.md §3`).
