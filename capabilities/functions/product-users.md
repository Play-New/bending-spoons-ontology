---
id: product-users
type: function
title: Product users — the paying committed base
status: confirmed
purpose: the customer world model of the people the products serve; where the customer signal lives
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: invocable-tool
relations:
  - { type: fragmented-by, target: cross-product-graph, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Product users — the paying committed base

```
function: committed-base reading    # ontology.md §2; who keeps paying while the price rises
input:
  - businesses.csv    # per-business operating properties: nrr_pct · arpu · organic_channel_pct · conversion_pct
  - the portfolio-level user disclosures (~L172, ~L362, ~L407-425, ~L434)
computation:
  - scale, with the caveat that defines it: MAU and paying sums are NON-DEDUPLICATED across
    products (~L186-187) — a sum of bases, not a count of people
  - willingness-to-pay: portfolio NRR per period + per-business NRR where broken out (~L407-408)
  - the per-business growth signature: ARPU up on falling subscribers (pruning) vs ARPU and
    subscribers up together (pull) (~L1865, ~L1872-1873, ~L1913)
  - tenure structure (~L410-411) and channel mix (~L431, ~L434)
  - contracted-forward commitment: remaining performance obligations $597.2M at 2025 YE (vs $155M / $57.9M prior, ~L4734)
output: the committed-base reading [derived] — per business and portfolio-wide. A per-PERSON reading
  is impossible by construction: there is no cross-product customer graph (the gap,
  ../../world-model/customer/cross-product-graph.md).
```

The *sapere* about who the products serve. Bending Spoons touches a very large base — monthly active users of 111M (Dec 2023) → 290M (Dec 2024) → 389M (Dec 2025) → over 500M (March 2026), and monthly paying customers of 3M → 5M → 8M → more than 9M over the same points (`bsp-f1` ~L362; ~L172 for the "over 500M / more than 9M" March 2026 figures). **These are non-deduplicated sums across products** (`bsp-f1` ~L186): the filing states it has "no reliable method of de-duplication," so the same user may be counted more than once — a person on Evernote and WeTransfer is counted twice — and the number is "an indication of the scale of our portfolio rather than a precise count of distinct users" (`bsp-f1` ~L187). So this is not "500M people"; it is the sum of per-product bases (see `../../world-model/customer/cross-product-graph.md`).

## What holds the customer: willingness-to-pay
The load-bearing signal here is not the size of the base or the app-store rating; it is whether the committed, high-switching-cost user keeps paying while the price rises. The F-1 gives it two ways:
- **Portfolio net revenue retention:** 93% (2023), 91% (2024), 95% (2025), 94% (Q1 2026) (`bsp-f1` ~L407). NRR is defined as subscription revenue in a quarter from customers acquired before the end of the same quarter a year earlier, over the prior-year quarter's revenue — so it isolates growth from the *existing* base, excluding new acquisition (`bsp-f1` ~L413-418).
- **Net revenue retention, per broken-out business (averaged Q1 2023–Q1 2026):** Evernote 99%, AOL 95%, StreamYard 91%, Remini 87% (`bsp-f1` ~L408; NRR is disclosed for only these 4 of the 10 main businesses — see the gap below). Evernote's 99% is the tell: the loyal archive-keeper absorbs steep price increases while marginal users churn. The filing notes a business's NRR "can fluctuate significantly over time, often as a result of monetization initiatives" (`bsp-f1` ~L409).
- **The optimization signature — ARPU up while subscriber count sometimes falls.** Across several businesses the F-1 attributes growth to higher average revenue per subscriber, at times *partly offset by a decrease in the number of subscribers*: Evernote in 2024 (`bsp-f1` ~L1865), Issuu and StreamYard in 2025 (`bsp-f1` ~L1872). That is the machine pruning the low-value tail and monetizing the committed base harder. On other businesses ARPU *and* subscribers rise together — Meetup in 2025 (`bsp-f1` ~L1873), komoot and WeTransfer in Q1 2026 (`bsp-f1` ~L1913) — the stronger read.
- **Tenure compounds retention:** "subscribers with longer tenure generally exhibit higher retention rates than newer subscribers, and longer-standing businesses tend to accumulate longer-tenured subscriber bases" (`bsp-f1` ~L425/~L1720). Time in the base is itself the moat. The tenure is deep and heavily weighted to the long-standing base: in Q1 2026, 48% of subscription revenue came from customers with tenure of at least five years, including 28% from customers of at least ten years, and revenue-weighted average subscriber tenure was 8.0 years (`bsp-f1` ~L410-411). (Because of the same de-dup limit, the filing warns tenure "may in some cases underestimate" the true relationship length — `bsp-f1` ~L422.)

## How they arrive (channels)
Customers acquired through **organic channels** (word of mouth, non-paid search) accounted for 79% of revenue from new customers in 2023, 76% in 2024, 79% in 2025, and 83% in Q1 2026 (`bsp-f1` ~L434) — the rest from paid advertising or direct sales and other go-to-market. The channel mix varies sharply by business: Remini relies predominantly on word of mouth, whereas Brightcove's acquisition is driven primarily by sales efforts (`bsp-f1` ~L431). Note: "organic channels" (how they arrive) is *not* "organic growth" (13% in 2025); conflating the two is a trap (see `../../world-model/customer/cross-product-graph.md` and the ontology's named gaps).

## What monetization intensity the filing does disclose
Not a static portfolio ARPU line, but a directional one — and disclosed per business, not portfolio-wide: at **Remini**, average revenue per monthly active user was 50% higher in 2025 than in 2021 even as its MAU grew more than fivefold (`bsp-f1` ~L2699) — the sharpest disclosed instance of monetization per user rising while the base multiplied. And the machine tunes conversion directly — the disclosed worked example is **StreamYard**: more than 140 tests across onboarding, paywall, periodicity, pricing, and checkout in 2024–2025 lifted its conversion rate from organic registered users to subscribers by 66% in 2025 vs 2023 (`bsp-f1` ~L2806-2807).

## What is NOT here (and why it matters)
No single static portfolio-wide ARPU figure, no disclosed churn rate (churn appears only as a risk factor — e.g. price increases and mandated cancellation flows "could increase churn," `bsp-f1` ~L767/~L772/~L864), no free-to-paid conversion %, and no CAC or LTV published *as a customer metric*. Note the filing does describe an internal LTV *capability* — Minerva, the AI user-lifetime-value predictor developed from 2019 (`bsp-f1` ~L2539, ~L2541) — but no LTV number is disclosed. The richest customer object of all — a single cross-product **Person** — does not exist. That absence is modeled as its own node because it is the biggest unbuilt moat: `../../world-model/customer/cross-product-graph.md`.

## References
- `bsp-f1` — Bending Spoons Form F-1 (line refs into `../../sources/2026-06-bsp-f1-fulltext.txt`): MAU/paying figures (~L172/~L362) and non-dedup caveat (~L186-187); portfolio NRR (~L407) and per-business NRR (~L408); NRR definition (~L413-418); tenure metrics (~L410-411/~L422/~L425); ARPU-vs-subscriber signature (~L1865/~L1872/~L1873/~L1913); channel mix (~L431/~L434); ARPU-per-MAU +50% (~L2699); conversion tests and +66% (~L2806-2807); churn as risk (~L767/~L772/~L864); Minerva LTV predictor (~L2539).
