---
id: platform
type: platform
title: The Platform — the operating machine
status: confirmed
purpose: the moat — the machine that makes every acquired business worth more inside the group than outside it
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
relations:
  - { type: operates, target: business, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# The Platform

**Properties** (per `../../ontology.md` §1): proprietary data (>3.8B data points/day, `bsp-f1` ~L2533) · shared infrastructure (billing, hosting, engineering) · the codified method. *(A property is stored ON this object. Revenue-per-Spooner ($1.12M→$2.57M, ~L307) and AI-authored-code share (<10%→>90%, ~L306) are computed ratios → `functions`; company-level financials are Bending Spoons' results, not Platform attributes. Per-object financials like `Business.revenue` are properties of the Business, not of the Platform.)*
**Links:** `operates`→Business. Inverses declared on the other side: `Tool —part-of→ Platform`, `Spooners —operates→ Platform`.

Bending Spoons names its competitive advantage the Platform: People plus proprietary technologies plus proprietary data (`bsp-f1`). It is the real product. The company says so directly: "we decided to treat the operating machine itself as our most important product, and to direct our greatest efforts toward building it" (`bsp-f1`, ~L87). Any single app (WeTransfer, Evernote) is something the Platform operates on, not the thing itself.

## The three parts
- **People (Spooners).** A durable, high-density core team, flexibly redeployable across every business — Spooners "are allocated flexibly across the organization and may be transferred between businesses on short notice" (`bsp-f1`, ~L293). 621 FTE Spooners at Q1 2026, 27% of total FTE team members (`bsp-f1`, ~L2425). The hiring funnel is extreme: around 800,000 applications to become a Spooner in 2025, 286 hired, less than 0.04% (`bsp-f1`, ~L284). The doctrine is to hire high-potential students and new graduates and place them in major responsibility early (`bsp-f1`, ~L159), keep the organization "lean, flat, and dynamically staffed" with "limited hierarchy" — "as flat as possible" to cut bureaucracy (`bsp-f1`, ~L2410, ~L2517-2518) — and run on a culture of "truth-seeking and extreme ownership" (`bsp-f1`, ~L283, ~L2439). Talent is treated as a movable resource: Remini was an asset deal with no team transferred; Bending Spoons initially allocated approximately 30 FTE Spooners to it, scaled to a peak of 64 average FTE in 2024, then redeployed resources elsewhere as returns diminished, declining to approximately 20 FTE Spooners by the end of 2025 (`bsp-f1`, ~L2669, ~L2672, ~L2673).
- **Proprietary technologies.** Built once, deployed across every acquired business, so the day an acquisition closes it can run pricing, prediction, and monetization it could not before. The F-1 names them (~L2532-2560): the **Pico / Lumen / Abacus** data infrastructure (Pico handles high-throughput ingestion, Lumen performs transformation, Abacus computes and serves standardized metrics; more than 3.8 billion data points/day on average in Q1 2026) (`bsp-f1`, ~L2532-2534); **Minerva**, an AI system estimating user lifetime value (in development since 2019, now supporting multi-year predictions and carrying insights across products) (`bsp-f1`, ~L2539-2541); **Juno**, the payments system built in 2023 that takes over an acquired product's subscription responsibilities "with minimal friction" (`bsp-f1`, ~L2543-2547); the **Janus / Orion** experimentation toolkit (more than 3,000 experiments run in 2025) (`bsp-f1`, ~L2550-2552); and **Role Model**, the recruiting technology behind the Spooner funnel (investment started 2017; handles tens of thousands of applications per talent manager per year) (`bsp-f1`, ~L2556-2560). (The "Spoon Engine / 50+ services" framing common in third-party write-ups is *not* in the F-1 — `[to-validate — press only]`.)
- **Proprietary data.** Accumulated across more than 50 acquisitions and served to over 500M monthly active users in March 2026, feeding the predictors and the experimentation (`bsp-f1`, ~L298, ~L361).

## Why it is the moat
The portfolio can be bought; the financials are an output; the Platform is the part that does not transfer with any deal. It is what lets them apply the same transformation to the next business and underwrite the next acquisition with confidence. The clearest evidence it is compounding: revenue per FTE Spooner rose from $1.12M to $1.64M to $2.57M across FY2023-2025 (`bsp-f1`, ~L307), and the share of pull requests authored or co-authored by AI went from less than 10% in Q1 2025 to more than 90% by the end of Q1 2026, with around 70% authored by AI alone (`bsp-f1`, ~L306), so the machine is increasingly automating its own construction.

## References
- `bsp-f1` — Bending Spoons Form F-1, 8 Jun 2026 (Business, founders' letter, MD&A): https://www.sec.gov/Archives/edgar/data/2004711/000110465926071170/tm2613674-7_f1.htm — "most important product" (~L87); Spooner headcount / hiring funnel (~L2425, L284); flat hierarchy (~L2517-2518); Remini redeployment (~L2668-2673); the named technologies Pico/Lumen/Abacus/Minerva/Juno/Janus/Orion/Role Model (~L2532-2560); revenue per Spooner (~L307); AI-authored PRs (~L306); 50+ acquisitions / 500M+ MAU (~L298, L361).
