---
id: world-model-index
type: index
title: World model — node map
status: confirmed
purpose: file-tree navigation for human readers — the object nodes in the world model, one line each (the MCP skips index files by design)
provenance: reflection
sources: []          # navigation only — no facts of its own
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
visibility: shared
---
# World model — node map

Navigation only (no new content). Two world models — the **company** (what Bending Spoons *is*) and the **customer** (what it *serves*). Every node here is an **object** (an instance of a type in `../ontology.md`); the actions & functions live in `../capabilities/`; the identity and will in `../will.md`.

## Company (`company/`) — objects
- `founders` (`company/founders.md`) — the controlling group: roles, class-A mechanics, 82.71% voting power.
- `facility` (`company/facility.md`) — the debt instruments (backed by `company/facilities.csv`): what `raise / refinance` writes.
- `platform` (`company/platform.md`) — the operating machine (proprietary data + the codified method); the asset "treated as our most important product".
- `company/tools/` — the proprietary technologies as objects: `minerva`, `juno`, `janus-orion`, `pico-lumen-abacus`, `role-model`.
- `spooners` (`company/spooners.md`) — the durable, reallocatable core team (621 FTE / 27% at Q1 2026), distinct from the transient acquired staff.
- `company/businesses/` — the 17 `Business` objects: aol, brightcove, eventbrite, evernote, harvest, issuu, komoot, loomly, meetup, mileiq, mosaic, remini, splice, streamyard, tractive, vimeo, wetransfer. Their delivery apps are the 18 `Interface` objects in `../interfaces/`.
- `deal` (`company/deal.md`) — the `Deal` object: the acquisition event (`of`→Target · `produces`→Business).
- `company/businesses.csv` / `company/deals.csv` / `company/financials.csv` — **backing datasets** (not object nodes; columns = the object's properties, 1:1): Business operating data · the Deal roster · the economic scoreboard the functions read.

## Customer (`customer/`) — objects
- `market-of-targets` (`customer/market-of-targets.md`) — the `Target` object: the >1,000-business acquisition market (for this machine, the "customer" is also the owner who sells).
- `targets.csv` — **backing dataset** for `Target` (columns = its properties, 1:1): filled examples of screened targets.
- `cross-product-graph` (`customer/cross-product-graph.md`) — the `gap`: no de-duplicated cross-product identity today; the single largest un-modeled asset; `../bending-spoons-as-an-intelligence.md` argues how it would be built and centered.

The **readings** over these objects — capital-allocation, portfolio-impermanence, product-users — are **functions**, in `../capabilities/functions/`, not world-model objects.
