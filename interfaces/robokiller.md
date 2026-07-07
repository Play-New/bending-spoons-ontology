---
id: robokiller-interface
type: interface
title: RoboKiller
status: confirmed
purpose: the RoboKiller delivery interface — where the machine meets its users, and the capabilities bundled in it today
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [site-mosaic]
properties:
  business: mosaic
  category: call-blocking
  capabilities_delivered: call blocking
  ai_features: n.d.
  status: live
relations:
  - { type: of, target: mosaic, cardinality: N:1, confidence: high, source: site-mosaic, status: confirmed }
visibility: shared
---
# RoboKiller — interface

**Properties** → structured in the frontmatter above, 1:1 with `interfaces.csv` (per `../ontology.md §1 Interface`).
**Link:** `Interface —of→ Business` (declared here, once) → `../world-model/company/businesses/mosaic.md` — the asset behind this interface; its operating data (revenue, retention, margin) lives there and in `../world-model/company/businesses.csv`.

The RoboKiller interface delivers, bundled inside itself, the capabilities the model maps in `README.md` (per `site-mosaic` — the brands are named on the official Mosaic site, not in the filings): call blocking. Today a capability serves only the users of the interface it ships in — that bundling is the confirmed state of Bending Spoons today; what unbundling would mean is the analysis (`../bending-spoons-as-an-intelligence.md §3`).
