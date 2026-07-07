---
id: capability-retire
type: action
title: Retire — wind a product down without selling it
status: confirmed
purpose: represent the death of a product as a transaction — never-sell ≠ never-die; the portfolio churns by status, not by deletion
provenance: reflection
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, site-mosaic]
runtime: skill
mcp: invocable-tool
relations:
  - { type: triggered-by, target: capability-deal-monitor, cardinality: 1:1, confidence: medium, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — retire

The transaction the impermanence reading (`../functions/portfolio-impermanence.md`) implies but the model previously could not represent: businesses decline and die inside the machine — they are **never sold** (`../../will.md`) but they do fade (Meetup and Issuu, acquired 2024, already off the "main businesses" list by Q1 2026, `bsp-f1` ~L375; Mosaic's surviving utility apps are managed for cash while the rest was sunset, site-mosaic). Without a retire verb, a dead business either lingers inflating the portfolio or vanishes with no action trail — both are corruption.

```
action: retire                      # the ontology verb (../../ontology.md §2)
parameters:
  - business          # a held Business whose returns no longer justify Spooner capacity
logic: threshold + judgment (skill)  # deal-monitor's drift reading is the trigger; whether a decline
                                     # is terminal (retire) or workable (re-transform) is human judgment
transaction — what it commits (write-back: businesses.csv):
  modify: Business    # status: main → tail → retired. THE ROW IS NEVER DELETED — impermanence is a
                      # status change with an action trail, not a disappearance (never-sell ≠ never-die)
  link: (none)        # existing links stay; the Spooner task-force is unwound by `reallocate talent`
submission criteria:
  - only on a sustained drift finding from deal-monitor (returns vs underwriting), not on a single period
  - never as a disguised sale — divesting a material business breaches the will (../../will.md)
governance:
  - approval: HUMAN — retiring a live business affects real users [decision]
side-effects:
  - `reallocate talent` unwinds the task-force (the Remini curve: 30 → 64 → ~20 FTE as returns
    diminished, bsp-f1 ~L2669-2673 — the observed shape of a wind-down's people-side)
  - the freed capacity and any residual cash feed the flywheel (§3)
backing:
  - dataset: ../../world-model/company/businesses.csv (the status column; rows are never deleted)
  - sensor: ../functions/deal-monitor.md (drift) · ../functions/portfolio-impermanence.md (the reading)
  - runtime: skill — exposed by the MCP as an invocable tool
```

`[decision]` This verb is modeled, not disclosed: the filings never describe a formal retirement process — the evidence is the observed churn (100% → 24% revenue concentration in two years, `bsp-f1` ~L401) and per-product fade-outs. Everything cited is real; the verb that organizes it is ours.

## References
- `bsp-f1` — the concentration collapse (~L401); Meetup/Issuu off the main list (~L375); the Remini wind-down curve (~L2669-2673).
