---
id: spooners
type: spooners
title: Spooners — the durable core team
status: confirmed
purpose: the reallocatable core workforce that operates the machine, distinct from the transient acquired staff
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
relations:
  - { type: operates, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: deployed-on, target: business, cardinality: N:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Spooners — the durable core team

**Properties** (per `../../ontology.md` §1 `Spooners`): headcount — 621 FTE (Q1 2026) · share of total FTE — 27% · talent-team size — 55 (~9% of Spooners) · redeployability — moved across the portfolio on short notice · attrition — 16.2% in 2025, of which wanted 15.6% (only 0.6% of intended-retains left, `bsp-f1` ~L2463-2464). *(Revenue-per-Spooner is a `function` over `financials.csv`, not a property.)*
**Links:** `operates`→Platform · `deployed-on`→Business.

The reallocatable core workforce — the people who run the operating machine, as opposed to the staff of the businesses being acquired. At Q1 2026 there were **621 FTE Spooners = 27% of total FTE** team members (`bsp-f1` ~L2425); the talent team itself was 55 Spooners, ~9% of Spooners (`bsp-f1` ~L2457). The vast majority of headcount growth came from acquired teams, **most of which are transitioned out** after a deal (`bsp-f1` ~L2413) — so the Spooner core is durable while the acquired staff is transient.

Spooners are **redeployed across the portfolio on short notice** (`bsp-f1` ~L151): a task-force stands up on a fresh acquisition, then reallocates when the opportunity shifts. That mobility is what makes the `platform` an operating *machine* rather than a holding company — it is the human side of the moat.

The productivity signal is **revenue per FTE Spooner**, rising $1.12M → $1.64M → $2.57M (FY 2023–2025) and $0.97M in the single quarter Q1 2026 (`bsp-f1` ~L307) — the machine doing more with the same core, AI a catalyst. (This is a `function`/reading over `financials.csv`, not a property of the node.)

Links: `operates`→`platform`; `deployed-on`→`product` (the reallocation, many products over time — the transient assignment written by the *assemble task-force* / *reallocate talent* actions).

## References
- `bsp-f1` — 621 Spooners = 27% of FTE, talent team 55 / 9% (~L2425, ~L2457); acquired teams mostly transitioned out (~L2413); redeployment on short notice (~L151); revenue per FTE Spooner (~L307).
