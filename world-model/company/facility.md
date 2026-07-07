---
id: facility
type: facility
title: Facility — the debt instruments that fuel the flywheel
status: confirmed
purpose: the object the raise/refinance verb writes — the machine's acquisitions are debt-funded, and the facilities are where that decision lands
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-05  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
relations:
visibility: shared
---
# Facility — the debt instruments

The filing names "determination of financing structures" as one of the four key strategic decisions of the CEO, alongside acquisitions, integration, and resource allocation (`bsp-f1` ~L4577) — which is what earns this object its node (`../../foundations/ontology.md §4.0`): a recurring modeled decision (`raise / refinance`, `../../capabilities/actions/finance.md`) writes it, the leverage covenant (`../../will.md`, external covenants) hooks onto it, and the headline reading prices its cost. Its instances are the roster in `facilities.csv`.

The shape of the discipline: term-loan-A market since 2017, first term loan B only in 2025, **no bonds ever issued**; equity is treated as expensive (~$549M primary equity raised, 99% since 2023; average dilution ~6.1%/yr from financing + ~1.5%/yr from equity comp) (`bsp-f1` ~L1749-1758). The AOL, Eventbrite, and Vimeo purchase prices ($1,454M · $505M · $1,359M) were funded by a stack of facilities signed within weeks of the closings, together with cash on hand (~L3114-3116) — the raise and the close move together.

- properties (per `../../ontology.md §1 Facility`, 1:1 with `facilities.csv`): name · type (term loan A / term loan B / RCF / bilateral) · currency · size · signed · status (active / drawn / partially drawn / repaid)
- links: none declared — `capital-allocation` reads the stack (net debt, leverage vs ≤4.00); which facility funded which deal is disclosed only in aggregate (~L3114-3116), so it is a note, not a link
- backed by: `facilities.csv`

## References
- `bsp-f1` — financing as a core CEO decision (~L4577); the funding stack for AOL/Eventbrite/Vimeo (~L3114-3116); capital-structure history and equity discipline (~L1749-1758); facility agreements named (~L4124-4137); leverage covenant (~L4541-4549).
- `bsp-424b4` — post-period financings: UniCredit €150M and Intesa €100M term loans signed and drawn, €260M drawn on the RCF, after March 31, 2026 (~L1543-1549).
