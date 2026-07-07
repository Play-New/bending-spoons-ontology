---
id: streamyard
type: business
title: StreamYard
status: confirmed
purpose: A creator-facing live-streaming and recording SaaS that Bending Spoons acquired, reorganized to a leaner team, and re-monetized — a textbook case of the acquire-and-transform machine at work.
provenance: filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
properties:
  revenue_usd_m: n.d.
  mau_m: n.d.
  paying_customers_m: n.d.
  nrr_pct: 91
  tenure_yrs: n.d.
  arpu: n.d.
  revenue_mix: n.d.
  organic_channel_pct: n.d.
  conversion_pct: n.d.
  adj_op_margin_pct: n.d.
  status: main
  lifecycle: optimized
relations:
visibility: shared
---
# StreamYard

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
StreamYard "provides video recording and multi-destination live-streaming tools for creators and businesses" (bsp-424b4 ~L372, ~L2328). It sits among Bending Spoons' main businesses, which in Q1 2026 were, in alphabetical order, AOL, Brightcove, Eventbrite, Evernote, Harvest, komoot, Remini, StreamYard, Vimeo, and WeTransfer (bsp-424b4 ~L355). At acquisition StreamYard "benefited from high levels of organic customer acquisition, driven largely by word of mouth and reflecting a well-established brand within the live-streaming niche," with strong subscriber retention and limited dependence on paid advertising that "supported reliable earnings forecasts" (bsp-424b4 ~L2751). The filing also notes the product had "already compelling" offering with identified opportunities to increase revenue and lower costs (bsp-424b4 ~L2786). Trademark rights in the StreamYard word mark and logo are held across the U.S., E.U., and other jurisdictions (bsp-424b4 ~L1166).

## The deal
On April 23, 2024, Bending Spoons "completed the acquisition of 100% of the issued and outstanding equity securities of StreamYard Top Corp., a Delaware corporation and the owner of StreamYard (among other digital products)" (bsp-424b4 ~L5031). In the reorganization narrative the entity is described as "StreamYard Top Corp Inc. (then ultimate parent company of StreamYard, Inc.)" (bsp-424b4 ~L203-204). It was one of five businesses Bending Spoons acquired in 2024, alongside Issuu, Meetup, Mosaic (an asset deal), and WeTransfer (bsp-424b4 ~L1853, ~L2022).

**Consideration and purchase accounting.** No StreamYard-only price is disclosed; the filing reports a combined figure: "The total consideration paid for the Meetup, StreamYard, and Issuu acquisitions was $280.7 million" (bsp-424b4 ~L5039). The combined fair-value allocation for those three deals was goodwill $211,559K, intellectual properties $11,436K, customer base $77,966K, other intangible assets $21,905K, deferred tax assets $3,312K, other non-current assets $1,619K, cash and equivalents $60,637K, and trade receivables/other current assets $12,969K — total assets acquired $401,403K; liabilities assumed $120,658K; fair value of net assets acquired $280,745K (bsp-424b4 ~L5040). Goodwill acquired in 2024 of $212 million was attributable to the Meetup, StreamYard, and Issuu acquisitions (bsp-424b4 ~L5176).

**Stub-period contribution.** "Our consolidated income statement for 2024 includes revenue from Meetup, StreamYard, and Issuu of $92.4 million and income before tax of $21.7 million for the periods from the respective acquisition dates" (bsp-424b4 ~L5046) — a combined figure, not StreamYard-only.

## The playbook applied (where the OFFICIAL record shows it)
The filing states the transformation plainly: "At StreamYard, we transitioned to a leaner organization, upgraded audio and video quality, introduced advanced functionality, and enhanced marketing and monetization" (bsp-424b4 ~L108). "Since the acquisition, we have streamlined the organization, enhanced the technology and product, and optimized monetization and marketing... These initiatives have accelerated growth and improved profitability" (bsp-424b4 ~L2751).

**Organization (the leaner team, now quantified).** "We reorganized the business, reducing the number of full-time equivalent team members dedicated to StreamYard from 154 at the time of acquisition to 44 (most of whom were Spooners) at the end of 2024, less than one year later, a reduction of 71%" (bsp-424b4 ~L2763). Nearly all G&A activities were absorbed into existing Bending Spoons teams, shifting to "fewer, more talent-dense teams" (bsp-424b4 ~L2763). This shows up in the financials: separation packages for the reorganizations of Issuu, Meetup, StreamYard, and WeTransfer drove increased R&D, sales-and-marketing, and G&A expense from 2023 to 2024 (bsp-424b4 ~L1872, ~L1876, ~L1880), and were a 2024 reorganization-expense driver (bsp-424b4 ~L1940); the StreamYard reorganization also appears among the Q1 2025 separation-package drivers (bsp-424b4 ~L1953). After the reorganization, the reduced ongoing personnel cost of Issuu, Meetup, StreamYard, and WeTransfer partly offset 2024→2025 expense growth (bsp-424b4 ~L1873, ~L1877, ~L1881).

**Technology (cost and reliability).** Unnecessary vendor contracts were terminated or consolidated at Bending Spoons scale; engineering deleted "multiple petabytes of unused recording files" and built real-time cloud-resource automation. Together these actions lowered IT infrastructure expense as a percentage of revenue by 65% in 2025 versus 2023 (the last full pre-acquisition year) (bsp-424b4 ~L2770). The incident rate was approximately 75% lower in 2025 than in 2023, aided by AI agents that analyze logs and codebases (bsp-424b4 ~L2774). Redesigned rollback tools and stronger monitoring shortened pre-release cycles "from weeks prior to the acquisition to hours at the end of 2025" (bsp-424b4 ~L2776).

**Product (>50 improvements, two AI/format bets with adoption data).** Multi-aspect-ratio streaming was added (auto-generating a portrait version alongside landscape); "In Q1 2026, 13% of subscribers leveraged this capability" (bsp-424b4 ~L2786). An AI highlight/clip feature that analyzes video and transcripts to auto-generate short vertical segments was used by "31% of subscribers" in Q1 2026 (bsp-424b4 ~L2792). Audio/video quality was reengineered to support higher bitrates (bsp-424b4 ~L2789-2791). "Beyond these initiatives, we shipped more than 50 additional product improvements in 2024 and 2025, including cross-platform chat overlays, expanded streaming destinations, studio workflow enhancements, and multiple usability refinements" (bsp-424b4 ~L2793). StreamYard is one of the businesses where AI-based features have been introduced (bsp-424b4 ~L2813).

**Marketing and monetization (the re-monetization, quantified).** Paid advertising was paused and the acquisition pipeline rebuilt: "in 2025 compared to 2023... paid advertising generated 142% more new registered users, despite advertising spend being 11% lower" (bsp-424b4 ~L2796). More than 140 tests were launched in 2024-25 "across onboarding flows, paywall design, subscription periodicity, pricing, and checkout optimization," lifting the organic-registered-user-to-subscriber conversion rate by 66% in 2025 vs 2023 (bsp-424b4 ~L2798-2800). An automated system detects business-like usage to move enterprise customers onto appropriate plans, reducing individual-plan cannibalization of enterprise revenue (bsp-424b4 ~L2801). The net monetization result: "average revenue per monthly active user being 64% higher in 2025 than in 2023" (bsp-424b4 ~L2802).

**Revenue outcome.** StreamYard was among the businesses making the largest contributions to organic revenue growth in both 2024 (organic growth 7%, with Evernote, Remini, and StreamYard) and 2025 (organic growth 13%, with Issuu, Meetup, Remini, StreamYard, and WeTransfer) (bsp-424b4 ~L1854, ~L1861). The 2024 revenue increase was "due to an increase in subscription revenue driven by growth in both average revenue per subscriber and the number of subscribers" (bsp-424b4 ~L1857); the 2025 increase came from "higher subscription revenue resulting from an increase in average revenue per subscriber, partly offset by a decrease in the number of subscribers" (bsp-424b4 ~L1862) — i.e., the 2025 lift came from charging existing users more, not from adding users. The filing presents (unaudited) StreamYard revenue indexed to its 2021 revenue in a graph, but no absolute figures (bsp-424b4 ~L2756). Improved cash generation at StreamYard (with Issuu, Meetup, and WeTransfer) "following our transformations of these businesses" helped drive operating cash flow up 42% from 2024 to 2025 (bsp-424b4 ~L2020); StreamYard is also named among the transformed businesses lifting operating cash flow 254% from Q1 2025 to Q1 2026 (bsp-424b4 ~L2032).

## What holds the customer
The load-bearing signal is willingness-to-pay per retained user. The filing reports StreamYard net revenue retention of 91%, averaged across Q1 2023 through Q1 2026 (bsp-424b4 ~L388, ~L2344) — below AOL (95%) and Evernote (99%) but above Remini (87%) in the same table. The 91% is corroborated by the growth composition: in 2025, revenue rose from higher average revenue per subscriber even as the number of subscribers fell (bsp-424b4 ~L1862), and average revenue per monthly active user was 64% higher in 2025 than 2023 (bsp-424b4 ~L2802). Sub-100% NRR means expansion from remaining customers does not fully offset churn, so the committed professional cohort is being monetized hard rather than the base being grown. The moat framing is the filing's own: the risk of replacement by general-purpose AI chatbots is seen as limited "for use cases that require sophisticated and relatively niche solutions (such as StreamYard's and Vimeo's video management and streaming offerings)" (bsp-424b4 ~L2843). The per-cohort split is [to-validate — press only]; the filing gives no StreamYard-only subscriber count, ARPU level, or revenue in dollars.

## Where it sits in the machine
Lifecycle: optimized. The filing explicitly groups StreamYard with the businesses it "continue[s] to optimize" — "Remini, Evernote, StreamYard, and the other businesses that have been part of our portfolio for years" — as distinct from the more recently acquired businesses still being transformed (bsp-424b4 ~L111). Portfolio role: creator-facing live video, a cash-generative subscription business already through its reorganization. It anchors the creator/SMB end of a video-adjacent cluster — Vimeo and Brightcove are also video businesses, with Brightcove described as focused on large enterprises (~15,000 monthly active users and ~1,700 monthly paying customers) (bsp-424b4 ~L354), while StreamYard's stated audience is creators and businesses (bsp-424b4 ~L2328).

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt). Contains the same StreamYard facts as the 424B4 at slightly different line numbers (e.g. acquisition ~L4927, consideration ~L4935, stub revenue ~L4942, case study ~L2757-2821).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt).
