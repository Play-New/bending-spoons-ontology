---
id: capability-deal-value
type: action
title: Value — underwrite to IRR and produce the walk-away price
status: confirmed
purpose: the heart of the machine — turn a screened target into the maximum price justified by OUR cash flows
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: invocable-tool
relations:
  - { type: feeds, target: capability-deal-diligence, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — value (the underwriting model)

The most transferable part of the whole machine: a walk-away price built on *your own* projected cash flows, which lets you win the right deals at the top of what is justifiable rather than haggle to the minimum.

```
action: underwrite                  # the ontology verb (../../ontology.md §2) — the one FUNCTION-BACKED
                                    # action: the IRR model computes, the action commits its output
parameters:
  - target            # a screened candidate (Target.status = screened-in)
  - assumptions       # human-supplied: 5-yr FCF trajectory, terminal growth (yrs 6-10), WACC, financing mix
  - hurdle_levered_pct / hurdle_unlevered_pct   # the bar; default 65/25. A human may lower it DELIBERATELY
                                                # (will.md: "plausible we'll have to lower them" with scale) — a parameter, not a hard law
logic — function-backed (the computation whose output the action commits):
  - unlevered IRR = IRR on estimated free cash flow directly attributable to the business over the five
    years following the expected closing date, plus a terminal value at the end of that period (bsp-f1 ~L117)
  - levered IRR   = same basis, plus the impact of hypothetical acquisition financing (bsp-f1 ~L121);
    the assumed debt equals the LOWER of 85% of the acquisition's enterprise value and the maximum
    repayable from the projected 5-yr FCF (~L2286)
  - terminal value = years 6-10 growth assumptions + WACC (current method); earlier deals used an
    EV/EBITDA multiple at year 5 (~L1655-1662)
  - computed on FREE CASH FLOW, not net income (net income carries the acquisition's amortization,
    interest, and one-offs). The filing's own operating lens is ADJUSTED EBITDA — EBITDA adjusted to exclude
    transaction- and reorganization-related expense and equity compensation, on a pro-forma full-period basis,
    reflecting achieved and capped expected reorganization cost savings (bsp-f1 ~L1766-1767) — and it uses an
    EBITDA-multiple market approach only as a cross-check to the income (DCF) approach (bsp-f1 ~L2146,~L2149).
    Guiding question: "if we stopped acquiring tomorrow, how much cash would this asset throw off?"
  - the WALK-AWAY PRICE: the most the model justifies on OUR cash flows
transaction — what it commits (write-back onto the target):
  modify: Target      # set Target.irr {levered, unlevered} and Target.walk_away_price — the underwriting
                      # record, written on the candidate; at close the achieved figure is booked as the
                      # Deal's own irr property (deals.csv)
  create: (none)      # the Deal does not exist until close (deal-diligence clears it)
  link:   (none)
submission criteria:
  - abort if the case cannot clear the hurdle bar — default 65% levered / 25% unlevered (bsp-f1 ~L110-111): a
    will constraint enforced here as the gate. The bar is a PARAMETER, not dogma — the filing says it is
    "plausible we'll have to lower them" as scale grows (~L112-113), so a human may move it deliberately
    (hurdle_levered_pct / hurdle_unlevered_pct), logged and human-gated at apply
  - pre-diligence inputs are ESTIMATES: real FCF, margins, and cohort churn come from the data room,
    not public sources — the model is only as good as the assumptions (deal-diligence verifies them)
governance:
  - will constraints that bind the model (../../will.md): the hurdles, and the never-sell refusal —
    underwrite to a LONG HOLD (5-yr FCF + terminal value, assuming the business is never sold),
    never to an exit multiple
  - approval: HUMAN — GATE 1: approve the walk-away price before diligence. Negotiation and closing
    stay human. [decision]
side-effects:
  - hand the approved case (assumptions + walk-away price) to deal-diligence (feeds capability-deal-diligence)
backing:
  - function: the IRR model over the human-supplied assumptions (this node)
  - constraint source: ../../will.md — the hurdles, held as capital deployed scaled ~10× (bsp-f1 ~L111)
  - runtime: skill — exposed by the MCP as an invocable tool
```

Why this shape. Because they hold rather than sell (`../../will.md`), they underwrite to a long hold (five-year cash flows + terminal value), not to an exit multiple. The walk-away price is the mechanism behind the "win by paying more" posture: the operating machine extracts more cash from the same asset, so the maximum they can justify is higher than a rival's — they reportedly offered ~50% above the second bid for Evernote and say they have never lost a deal to a higher offer (`[to-validate — press only]` — founders' account, not in bsp-f1/bsp-424b4). The filing's own evidence for the posture is that they held the same 65%/25% hurdles even as capital deployed rose from $194M in all of 2023 to $2.01B in Q1 2026 (`bsp-f1` ~L111) — paying far more without lowering the bar.

## References
- `bsp-f1` — the IRR hurdles (65% levered / 25% unlevered, ~L110-111); IRR on 5-yr FCF + terminal value (~L117), levered adds financing (~L121); adjusted-EBITDA definition (~L1766) and the EBITDA-multiple market cross-check to the income approach (~L2146,~L2149); capital deployed $194M (2023) → $2.01B (Q1 2026) with the hurdle held (~L111).
