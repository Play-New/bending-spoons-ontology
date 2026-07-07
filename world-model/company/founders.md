---
id: founders
type: founders
title: The founders — the controlling group
status: confirmed
purpose: the actors the founder-control constraint hooks onto — who they are, what they hold, and the mechanics that make control personal
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-05  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
relations:
visibility: shared
---
# The founders — the controlling group

**Properties** (per `../../ontology.md` §1 `Founders`): members & roles — Luca Ferrari (co-founder · chair & CEO since June 2013) · Francesco Patarnello (co-founder · vice-chair · **head of Business Acquisitions** — the human at the deal gates) · Matteo Danieli (co-founder · director · product) · Luca Querella and Tomasz Greber (co-founders, the two "Evertale standouts") · class-A holders: **Danieli, Ferrari, Patarnello, Querella** (four of the five; not Greber) · votes per class A share: **5** (vs 1 per ordinary) · post-IPO voting power: **82.71%** · super-voting floor: **37,500,000 class A shares** per holder · control-transfer rule: personal and non-transferable · board slates: only the board or ≥5% holders · employment agreements: **none** for Ferrari or Patarnello.
**Links:** none declared — this object is hooked by a **will constraint** (founder control, `../../will.md`), which is what earns it a node (`../../foundations/ontology.md §4.0`).

## Who they are
The origin is the founding story itself: Patarnello, Danieli, and Ferrari, exhausted from a post-graduation backpacking trip, resolve to build a company (`bsp-f1` ~L58); after Evertale fails, they liquidate it and start again "alongside Luca Querella and Tomasz Greber, two Evertale standouts" (~L69). Ferrari has been chief executive officer and a director since June 2013, previously a McKinsey associate and Evertale co-founder (~L2917-2919); the "Chair" and "Vice chair" titles are in the management table (~L2912); Patarnello runs Business Acquisitions (~L2928) — the role that makes him the person behind the `underwrite`/`close` gates in `../../capabilities/actions/`.

## What they hold, and why it is load-bearing
Four of the five hold every class A share; post-IPO they exercise **82.71% of total voting power** (82.48% if the over-allotment is exercised) (`bsp-424b4` ~L13). Each class A share carries **5 votes** (`bsp-f1` ~L1389; bylaws ~L3510). The control is engineered to be **personal**: class A converts to ordinary 1-for-1 on transfer outside the class-A circle, on death, or when a holder's stake falls below **37,500,000 class A shares** (~L3511-3519, ~L3514) — it cannot be sold, inherited, or diluted away without dissolving itself. Board slates may be submitted only by the board or by ≥5%-voting shareholders (~L3554-3569), which with 5:1 votes makes the class-A holders the operative electors of the board.

## The exposure the filing itself flags
There are **no employment agreements** with Ferrari or Patarnello — "they may terminate their relationship with us at any time" (~L635-638). The same structure that concentrates control concentrates key-person risk: the will's whole buy-and-hold posture is only as durable as the people the constraint hooks onto.

## References
- `bsp-f1` — founding story (~L58, ~L69); roles (~L2912, ~L2917-2940); 5 votes per class A (~L1389, ~L3510); conversion events + floor (~L3511-3519, ~L3514); slate mechanism (~L3554-3569); no employment agreements (~L635-638).
- `bsp-424b4` — post-IPO voting power 82.71% / 82.48% (~L13).
