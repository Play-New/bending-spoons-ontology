---
id: capital-allocation
type: function
title: Capital allocation — the flywheel
status: confirmed
purpose: where the machine's economics actually resolve, and where its risk lives
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
runtime: skill
mcp: invocable-tool
relations:
  - { type: funds, target: deal, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capital allocation — the flywheel

The economics of Bending Spoons resolve here, not on the income statement. The flywheel is a three-step Playbook the founders state as "acquire, transform and optimize, then reinvest," essentially unchanged since 2013: acquired businesses throw off earnings, the earnings (plus "prudent levels of incremental debt") are reinvested into more acquisitions, underwritten to a hard return hurdle, and the cycle compounds (`bsp-f1`, ~L105, ~L264, ~L278). They model it on serial-acquirer compounders — naming Henry Singleton at Teledyne and Tom Murphy at Capital Cities as inspirations, and Broadcom, Danaher, and TransDigm as more recent studies (`bsp-f1`, ~L103-104) — and expect to "allocate almost all available capital to acquisitions for many years to come," paying no dividends (`bsp-f1`, ~L114, ~L1412).

```
function: headline reading          # ../../ontology.md §2; the reading where the machine's economics resolve
input:
  - financials.csv    # the scoreboard: revenue · operating/net income · cash flows · debt, per period
  - deals.csv         # capital deployed per cohort
  - the will's hurdles (../../will.md: 65% levered / 25% unlevered)
computation:
  - the three diverging lines: revenue vs GAAP net income vs adjusted operating income (~L523, ~L349-350)
  - capital deployed per year vs the hurdles held constant (~L110-111)
  - the growth split: total revenue growth minus organic (95% − 13% in 2025 → ~82 points bought) (~L1864, ~L1871)
  - net debt (total debt − cash, ~L1562/~L4503) vs net operating cash flow (~L523) — who funds the flywheel
  - the leverage ratio (net debt / adjusted EBITDA) vs the ≤4.00 covenant: 2.24 FY2025 · 2.19 Q1 2026 (~L1751-1753)
output: the headline reading [derived] — revenue compounds while GAAP net income ≈ 0 and net debt
  climbs; a compounding engine financed with debt, judged on adjusted earnings and return on
  deployed capital, not on the income statement. Read-only; the reinvest loop it describes is
  governed by the will (§3 of ontology.md), not committed here.
```

## The discipline that is the moat behaving
They hold IRR hurdles of 65% levered and 25% unlevered (applied to acquisitions closed 2023 through Q1 2026), and held them even as capital deployed scaled roughly tenfold, from $194M in all of FY2023 to $2.01B in Q1 2026 alone (`bsp-f1`, ~L110-111). The unlevered IRR is computed on estimated free cash flow attributable to the acquired business over the five years after close plus a terminal value; the levered IRR adds hypothetical acquisition financing (`bsp-f1`, ~L117, ~L121). Holding a return bar constant while deploying ten times the capital is the machine working, not the revenue line.

## Why the headline numbers mislead
A reader who mirrors the headline misreads the company in one of two opposite ways. Revenue grew 132% year over year in Q1 2026 and reached $1.31B for FY2025 (`bsp-f1`, ~L1907, ~L1860), which reads as a boom. GAAP net income over the same period went $160.6M, then $89.0M, then about $(0.2)M in 2025 (`bsp-f1`, ~L523), which reads as a collapse. Both readings are wrong. The 2023 figure was inflated by a $103.1M income-tax *benefit* line (a $65M + $22M + $16M stack of one-off items, not core earnings), and 2025 was near breakeven under $142.6M of interest expense plus acquisition, amortization, and reorganization charges (`bsp-f1`, ~L523, ~L1904).

The signals that tell the truth are the productivity and retention of the machine: adjusted operating income was $137M / $299M / $613M / $308M (Q1 2026) with adjusted operating margin rising 36% to 51%, net revenue retention held in the low-to-mid 90s (93/91/95/94% across the periods), revenue-weighted average subscriber tenure is 8.0 years, and revenue per FTE Spooner rose from $1.12M to $2.57M (FY basis; $0.97M in the single quarter Q1 2026) (`bsp-f1`, ~L349-350, ~L407, ~L411, ~L307). The company is best understood as a compounding engine financed with debt, judged on adjusted earnings and return on deployed capital, not as an income statement.

## The financing (where the risk lives)
The flywheel does not spin on organic cash. Net cash from operating activities was $290.6M in FY2025 (and just $75.7M in Q1 2026) (`bsp-f1`, ~L523), against ~$1.65B of cash used for acquisitions (net cash from investing activities of $(1,647,942) thousand; acquisitions of businesses net of cash acquired were $(1,644,718) thousand) in Q1 2026 alone (the F-1's broader "capital deployed" for that quarter was ~$2.01B; the two figures measure different things, cash-on-deals vs total capital deployed) (`bsp-f1`, ~L4275, ~L111); the same quarter drew $1,967,570 thousand of new debt proceeds (`bsp-f1`, ~L4275), so the gap is filled by **debt and equity**, not by the businesses (`bsp-f1`). At March 31, 2026 total debt including current portion was $4,356,067 thousand (~$4.36B, up from $2,670,882 thousand at Dec 2025) and cash and cash equivalents were $740,823 thousand (~$741M), implying net debt of ~$3.6B (net debt is a defined term in the F-1 — financial debt and capitalized lease obligations less available cash — and here is derived from those two line items) (`bsp-f1`, ~L1562, ~L4503, ~L1765). The July 2026 IPO priced at $29.00/share and, of the $1,681,159,435 total offering, delivered **net proceeds of $933M to the company** (proceeds before expenses to the company were $953.9M; $653.7M went to selling shareholders), intended for general corporate purposes and new acquisitions (`bsp-424b4`, ~L7, ~L19, ~L473, ~L475). This is the model's real risk: it runs on borrowed money against cash cows that lose users slowly. It works while the machine keeps landing deals and the cows keep producing.

## The deepest tell (read the growth, not the revenue)
FY2025 revenue grew 95%, but organic revenue growth was only 13% in 2025 (and 7% in 2024); the remaining ~82 points were bought (the split is derived: 95% total less 13% organic) (`bsp-f1`, 95% at ~L1868, 13% at ~L1871, 2024's 7% at ~L1864). And "organic" is generous: the F-1 defines it as this year's revenue over the same businesses' prior year *including estimated pre-acquisition revenue where applicable*, and much of the 13% traces to higher average revenue per subscriber on a declining subscriber base (e.g. Issuu and StreamYard), i.e. price increases on a slowly-declining user base, not new customers (`bsp-f1`, the definition ~L1878, the Issuu/StreamYard driver ~L1872). So the growth story depends on continuing to buy larger targets. The open strategic question the model surfaces: are they compounding a durable machine, or running to stand still on inorganic growth? Both readings fit the same F-1; that tension sits at the center of the company.

## References
- `bsp-f1` — Bending Spoons Form F-1, 8 Jun 2026 (MD&A, financial summary): https://www.sec.gov/Archives/edgar/data/2004711/000110465926071170/tm2613674-7_f1.htm
- `bsp-424b4` — final prospectus (424B4), 30 Jun 2026 — IPO price $29.00, proceeds and use of proceeds (~L7, L19, L473).
