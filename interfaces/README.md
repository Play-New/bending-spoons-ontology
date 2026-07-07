---
id: interfaces-index
type: index
title: Interfaces — the delivery surfaces (layer index)
status: confirmed
purpose: navigation for the interfaces layer — one node per Interface, backed by interfaces.csv
provenance: reflection
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: []          # navigation only — grounding lives in the Interface nodes
visibility: shared
---
# Interfaces — the delivery surfaces

The layer where the machine meets its users. An **`Interface`** is the app/site the user touches — a *delivery surface* in the org contract's words — distinct from the **`Business`** behind it (the asset: revenue, retention, margin — `../world-model/company/businesses/`), linked once: `Interface —of→ Business`. A business may ship several interfaces (Mosaic ships iTranslate and RoboKiller), and an interface can be sunset while its business lives. Each interface delivers a set of **capabilities bundled inside it** — real today, but trapped: a capability serves only the users of the interface it ships in.

**The 18 interfaces** (one node each; backing = `interfaces.csv`, 1:1):

| interface | delivers (bundled) | of business |
|---|---|---|
| [aol](aol.md) | email · news feed · search · consumer security/identity add-ons | aol |
| [brightcove](brightcove.md) | enterprise video delivery · streaming infrastructure | brightcove |
| [eventbrite](eventbrite.md) | ticketing · event discovery · payment rails | eventbrite |
| [evernote](evernote.md) | capture · notes/OCR · personal archive · search-over-your-stuff | evernote |
| [harvest](harvest.md) | time-tracking · invoicing | harvest |
| [issuu](issuu.md) | digital publishing · flipbook distribution | issuu |
| [itranslate](itranslate.md) | translation | mosaic |
| [komoot](komoot.md) | route planning · outdoor navigation · GPS activity log | komoot |
| [loomly](loomly.md) | social scheduling | loomly |
| [meetup](meetup.md) | group formation · local community/RSVP | meetup |
| [mileiq](mileiq.md) | mileage/location logging | mileiq |
| [remini](remini.md) | image/video enhancement · generative restoration | remini |
| [robokiller](robokiller.md) | call blocking | mosaic |
| [splice](splice.md) | mobile video editing | splice |
| [streamyard](streamyard.md) | live-streaming · multi-cast production | streamyard |
| [tractive](tractive.md) | pet GPS tracking · activity/health monitoring (hardware + app) | tractive |
| [vimeo](vimeo.md) | video hosting/distribution | vimeo |
| [wetransfer](wetransfer.md) | large-file transfer · ephemeral delivery | wetransfer |

Because the portfolio is impermanent (businesses generating 100% of revenue in Q1 2024 fell to 24% by Q1 2026, `bsp-f1` ~L401), the set of interfaces is a snapshot, never the identity — see `../capabilities/functions/portfolio-impermanence.md`.

Other places Bending Spoons meets a counterpart — the M&A table (sellers), the filings and the Nasdaq listing (capital), the hiring funnel (talent), the corporate site (public) — are **not modeled as interfaces**: no modeled decision writes them as objects (`../foundations/ontology.md §4.0`, the decision test). They live where the decisions live: the gates of the deal actions, `../sources/`, and the `talent` contract.

**The analysis** (`../bending-spoons-as-an-intelligence.md §3`) argues what this table implies: unbundle the middle column from the left one — the capabilities become orchestratable primitives, the interfaces become interchangeable, and a meta-interface composes across them. Here in the model they remain bundled: that is the confirmed state of Bending Spoons today.
