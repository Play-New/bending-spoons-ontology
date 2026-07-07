---
id: capability-deal-diligence
type: action
title: Diligence — verify the underwriting assumptions
status: confirmed
purpose: stress-test the load-bearing assumptions behind the walk-away price before the deal is committed
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
runtime: agent
mcp: activatable-agent
relations:
  - { type: verifies, target: capability-deal-value, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — diligence (agent)

A judgment loop, not a fixed checklist: it starts from the assumptions the walk-away price rests on, decides which to verify first (the most load-bearing), interrogates the data room and public record, and returns confirmations or red flags that re-feed `deal-value`.

```
action: close acquisition           # the ontology verb (../../ontology.md §2); this agent backs it —
                                    # the loop verifies, the CLOSE is the transaction it clears
parameters:
  - target            # the candidate under negotiation (Target.status = screened-in, underwritten)
  - underwriting      # the assumptions + walk-away price committed by deal-value
  - data-room access
logic: judgment loop (agent)        # what to check next depends on what the last check turned up;
                                    # it runs BEFORE anything is committed:
  - rank the assumptions by how much the walk-away price moves if they are wrong; verify the top ones first
  - confirm the real FCF trajectory, margins, and per-cohort churn (the numbers that were estimates pre-diligence)
  - hunt for price-distorting facts the seller may not volunteer — e.g. equity instruments held by the
    acquired team that accelerate on change of control (the F-1 records this cost: $5M at Issuu and
    WeTransfer in 2024, bsp-f1 ~L1946; $36M at Brightcove and Vimeo in 2025, ~L1947) — and deferred
    consideration (Tractive: $781M at closing plus $119M payable one year after closing, ~L4599)
  - return: assumptions confirmed/corrected + red flags, re-feeding deal-value
transaction — the CLOSE it clears (write-back: deals.csv + the new business + interface nodes):
  create: Deal        # the event, one row in deals.csv: date · cohort · deal_type · consideration ·
                      # enterprise value · irr · ppa {goodwill, customer_base, ip, trademark}
  link:   Deal —of→ Target · Deal —produces→ Business   # both declared once, on the Deal
  create: Business    # the operating asset the deal produces — its node under ../../world-model/company/
                      # businesses/ + a businesses.csv row (the operating baseline at close) — plus its
                      # Interface node(s) under ../../interfaces/ + interfaces.csv rows (Interface —of→ Business)
submission criteria:
  - abort if a red flag breaches a will constraint (e.g. the return no longer clears the IRR hurdle)
  - a corrected assumption re-feeds deal-value: the walk-away price is re-committed through GATE 1,
    never silently adjusted here
  - Deal ⊥ Business: consideration, deal-type, date, PPA are booked on the Deal only; revenue, users,
    retention live on the Business only; brand/category/capabilities on the Interface
governance:
  - none to investigate; GATE 2 — the go/no-go remains human (it never kills or commits a deal
    on its own) [decision]
side-effects:
  - red flags surfaced to the human gate as they are found (not only at the end)
  - on close: hand the new Business to deal-optimize (transformation, typically completed within the
    first year following closing, bsp-f1 ~L2646); the platform assembles the task-force onto it
    (the link Spooners —deployed-on→ Business is the talent action's, not this one's)
backing:
  - datasets: ../../world-model/company/deals.csv (the Deal created) ·
              ../../world-model/company/businesses.csv + businesses/<name>.md (the Business created) ·
              ../../interfaces/interfaces.csv + interfaces/<name>.md (the Interface(s) created)
  - runtime: agent (what to check next depends on what the last check turned up) — MCP: activatable agent
```

Why an agent: what to check next depends on what the last check turned up, and "material enough to move the price" is a judgment. It is the step that turns the pre-diligence estimate (structurally uncertain — real margins and churn are not public) into an underwriting the machine can commit to.

## References
- `bsp-f1` — the equity-acceleration cost lines (Issuu/WeTransfer ~L1946, Brightcove/Vimeo ~L1947, Eventbrite ~L1961) and the Tractive deferred-consideration structure (~L4599) the diligence must catch. The filing also names the target-valuation judgments that diligence tests — "future revenue, retention, engagement, pricing power, costs, margins, and growth trajectory" (`bsp-424b4` ~L689).
