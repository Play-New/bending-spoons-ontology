---
id: capability-market-radar
type: action
title: Market radar — continuous target discovery
status: confirmed
purpose: the always-on sourcing agent; discovering buyable targets is the recurring value, upstream of any single deal
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: agent          # a judgment loop, not a fixed procedure
mcp: activatable-agent  # how the MCP would expose it
relations:
  - { type: feeds, target: capability-screen-target, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — market radar (agent)

The upstream engine. It does not wait for a target to be handed over; it watches a defined universe continuously and surfaces businesses as they become *buyable now*. In the MCP this is an **activatable agent**, not a one-shot tool: you turn it on against a thesis and it runs.

```
action: source                      # the ontology verb (../../ontology.md §2); this agent backs it
parameters:
  - thesis            # the boundary, human-set: famous-but-fallen digital brands, loyal/sticky base,
                      # bloated costs, distracted or motivated owner [to-validate — press only]
  - watch-universe    # the sized market it patrols: >1,000 identified businesses, ~$400B aggregate
                      # estimated 2025 revenue (bsp-f1 ~L177,~L318)
logic: judgment loop (agent)        # what to look at next depends on what it finds, and "buyable now"
                                    # is a judgment, not a fixed rule — it scores each candidate against
                                    # the thesis and emits when one crosses the maturity threshold.
                                    # It watches these signals of maturation:
  - loyal base but declining momentum
  - layoffs / financial distress / defensive cost-cutting
  - ownership change, distracted founder, a parent wanting to liquidate
  - compressed public valuation
  - AI pressure on the core business
  # The filing itself names three of these as tailwinds: owners' willingness to sell rising, lower valuation
  # levels, and companies "not well equipped to leverage AI" (bsp-f1 ~L312). The "near 1-3x revenue" band and
  # the "famous-but-fallen" framing are founders'/press characterizations, [to-validate — press only].
transaction — what it commits (write-back: targets.csv):
  create: Target      # a new candidate, its nine gate properties estimated from public observation:
                      # revenue_scale · hq · product_offering · revenue_model · room_for_improvement ·
                      # predictable_earnings · owner_willingness_to_sell · valuation_level · ai_pressure
  modify: Target      # re-score the maturation signals as they move — owner_willingness_to_sell,
                      # valuation_level, ai_pressure (the three the filing names as tailwinds, bsp-f1 ~L312)
  link: (none)        # Target declares no links; the Deal links to it later (Deal —of→ Target, at close)
submission criteria:
  - a Target is created only inside the thesis boundary
  - public signals only at this stage (filings, press, app-store and traffic proxies); a press-derived
    property value enters marked [to-validate — press only]
governance:
  - free to observe; admitting a target into the pipeline is HUMAN (it does not auto-screen) [decision]
  - moving the perimeter itself is proposed to the human, never done [decision]
side-effects:
  - emit the matured candidate to the screen queue WITH the reason it is buyable now (feeds screen-target)
  - flag when the perimeter itself should move (a proposal to the human, not a write)
backing:
  - dataset: ../../world-model/customer/targets.csv — the Target backing, 1:1 with the gates
  - runtime: agent (continuous judgment loop) — exposed by the MCP as an activatable agent
```

The target market's *properties* — the criteria, the revenue band, the sizing — are the `Target` object (`../../world-model/customer/market-of-targets.md`); the *gates* that apply them are `screen-target`. This node is only the always-on scouting **action** over that market.

Why an agent and not a skill: the sequence of what to look at next depends on what it finds, and "buyable now" is a judgment, not a fixed rule. It reads the same observation surfaces (public filings, press, app-store and traffic proxies) that a human analyst would, continuously. Discovery — not the execution of any single deal — is the recurring value.

## References
- `bsp-f1` — the acquisition strategy and target profile (Business section); the AI-driven sourcing tailwinds — rising willingness to sell, lower valuations, AI-unequipped incumbents (~L312); the sized universe the radar draws on: >1,000 identified businesses, ~$400B aggregate 2025 revenue (~L177,~L318). The self-regenerating-pipeline thesis and the "famous-but-fallen / 1-3x revenue" framing are founders'/press views, `[to-validate — press only]`.
