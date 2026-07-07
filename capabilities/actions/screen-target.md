---
id: capability-screen-target
type: action
title: Screen a target
status: confirmed
purpose: gate a candidate against the four criteria before the expensive underwriting
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: invocable-tool
relations:
  - { type: feeds, target: capability-deal-value, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — screen a target

The cheap gate before the expensive model. It takes a candidate from `market-radar` and decides whether it is worth underwriting at all, then hands the survivors to `deal-value`.

```
action: screen                      # the ontology verb (../../ontology.md §2); this skill backs it
parameters:
  - target            # a Target sourced by market-radar, its nine gate properties populated
logic: fixed business rule (skill)  # the four analysis factors scored against the gates — no judgment
                                    # loop: cheap, disqualifying, runs first and wide
transaction — what it commits (write-back: targets.csv):
  modify: Target      # set Target.status (the shared property): screened-in (worth underwriting) or
                      # screened-out — decided by scoring the four analysis factors the F-1 names for
                      # its manual analysis (bsp-f1 ~L448) against the gate properties:
                      # revenue_scale · hq · product_offering · revenue_model
  create: (none)      # nothing new exists yet — the Deal is created only at close
  link:   (none)
submission criteria:
  - hard gates — fail any one and the target is OUT (bsp-f1 ~L449-456):
      * revenue_scale: estimated annual revenue $50M–$5B (currently prioritized range; expect to
        pursue >$5B over time)
      * hq: Europe or North America
      * product_offering / revenue_model: digital, and one the Platform suits today — self-serve
        subscriptions, sales-led subscriptions, or advertising; exclude businesses heavy in IT services
  - screening is disqualifying only: it never sets a price (the money question — what the target
    is worth to US — is deal-value's)
governance:
  - none to screen; admitting a survivor to underwriting is a human call [decision]
side-effects:
  - hand survivors to deal-value for underwriting (feeds capability-deal-value)
backing:
  - dataset: ../../world-model/customer/targets.csv — the gates 1:1; the screen writes the status
  - runtime: skill (fixed gates, no judgment loop) — exposed by the MCP as an invocable tool
```

Screening is deliberately separate from underwriting: it is cheap and disqualifying, so it runs first and wide. The money question — what the target is worth to *us* — lives in `deal-value.md`.

## References
- `bsp-f1` — the four analysis factors applied by manual analysis (~L448); the three hard criteria every identified business satisfies (~L449-456); the sizing of the universe — >1,000 businesses, ~$400B aggregate 2025 revenue (~L177,~L450), of which 347 at $50-100M, 476 at $100-500M, 114 at $500M-1B, 94 at $1-5B (~L450).
