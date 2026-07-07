---
id: capability-finance
type: action
title: Finance — raise and refinance the fuel
status: confirmed
purpose: the raise/refinance verb — financing structures are one of the four core CEO decisions; this is where that decision writes the model
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-05  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
runtime: skill
mcp: invocable-tool
relations:
  - { type: feeds, target: capability-deal-diligence, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — finance (raise / refinance)

The flywheel does not spin on organic cash (`../functions/capital-allocation.md`): the closes are funded by debt raised and re-raised deal by deal — the AOL/Eventbrite/Vimeo stack was signed within weeks of the closings (`bsp-f1` ~L3114-3116). The filing ranks "determination of financing structures" among the four key strategic decisions of the CEO (~L4577); this contract is that decision as a transaction.

```
action: raise / refinance           # the ontology verb (../../ontology.md §2); this skill backs it
parameters:
  - need              # the capital requirement: a close to fund, a facility to amend or repay
  - structure         # instrument + terms: TLA / TLB / RCF / bilateral, currency, size
logic: financing judgment (CEO)     # one of the four core decisions (~L4577); the stated preferences:
                                    # debt over equity (equity is expensive: ~6.1%/yr financing dilution,
                                    # ~L1749-1758), term-loan market first (TLA since 2017, first TLB
                                    # 2025, no bonds ever)
transaction — what it commits (write-back: ../../world-model/company/facilities.csv):
  create: Facility    # sign a new facility: name · type · currency · size · signed
  modify: Facility    # draw · amend (e.g. the TLB add-ons) · repay (status: active / drawn / partially drawn / repaid)
  link:   (none)      # which facility funds which deal is disclosed only in aggregate — a note, not a link
submission criteria:
  - the post-transaction leverage ratio stays ≤ 4.00 net debt / adjusted EBITDA (the covenant that
    binds every raise, bsp-f1 ~L4541-4546; held at 2.24 FY2025 / 2.19 Q1 2026, ~L1751-1753)
  - the negative covenants hold: no restricted disposals, distributions, or additional debt outside
    the agreed exceptions (~L4547-4549)
  - an equity raise may not cause a change of control (Nasdaq 5635(b) ceiling on the board's
    delegated authority, ~L3481-3488)
governance:
  - will constraints (../../will.md, External covenants + capital discipline): the covenant gates,
    no-dividends/reinvest-all, and the founder-control ceiling on dilution
  - approval: HUMAN — the CEO's decision (~L4577); the model computes headroom, it never signs [decision]
side-effects:
  - a signed facility funds the next `close` (feeds capability-deal-diligence — flywheel ① in
    ../../ontology.md §3)
  - interest expense flows into the headline reading (net income ≈ 0 under $142.6M of 2025 interest expense, ~L523/~L1893 —
    ../functions/capital-allocation.md)
backing:
  - dataset: ../../world-model/company/facilities.csv — the Facility backing, 1:1
  - runtime: skill — exposed by the MCP as an invocable tool
```

## References
- `bsp-f1` — financing as a core CEO decision (~L4577); the AOL/Eventbrite/Vimeo funding stack (~L3114-3116); capital-structure history + equity-cost stance (~L1749-1758); leverage covenant and negative covenants (~L4541-4549); change-of-control ceiling (~L3481-3488).
- `bsp-424b4` — post-period raises: UniCredit €150M, Intesa €100M, €260M RCF draw (~L1543-1549).
