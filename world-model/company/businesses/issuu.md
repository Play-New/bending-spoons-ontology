---
id: issuu
type: business
title: Issuu
status: confirmed
purpose: A digital-publishing SaaS Bending Spoons acquired, reorganized, and now runs for cash — a case of the acquire-and-transform machine at work on a subscription creator tool.
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-issuu]
properties:
  revenue_usd_m: n.d.
  mau_m: n.d.
  paying_customers_m: n.d.
  nrr_pct: n.d.
  tenure_yrs: n.d.
  arpu: n.d.
  revenue_mix: n.d.
  organic_channel_pct: n.d.
  conversion_pct: n.d.
  adj_op_margin_pct: n.d.
  status: tail
  lifecycle: optimized
relations:
visibility: shared
---
# Issuu

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
Issuu is a digital publishing platform that "enables creators and publishers to distribute, monetize, and analyze the performance of digital publications" (bsp-f1). Its own site describes it as "the industry-leading digital publishing platform" and a "self-service platform that equips anyone, from individuals to global brands, to easily convert static documents into a dynamic digital experience" (site-issuu, https://issuu.com/about). The core job is converting PDFs and other document formats into interactive page-turning flipbooks that can be distributed, embedded, and turned into social posts, videos, and articles, with reader analytics and digital-sales/monetization tooling (site-issuu, https://issuu.com/about). Its audience spans content marketers, designers, publishers, salespeople, and social-media managers, plus teams in education, real estate, retail, nonprofits, and publishing (site-issuu, https://issuu.com/about).

## The deal
On July 18, 2024, Bending Spoons completed the acquisition of 100% of the issued and outstanding equity securities of Issuu Inc., a Delaware corporation and the owner of Issuu, accounting for it as a business combination (bsp-f1 ~L4931; bsp-424b4 ~L5035). The F-1 describes Issuu's business as one that "enables creators and publishers to distribute, monetize, and analyze the performance of digital publications" (bsp-f1 ~L4932; bsp-424b4 ~L5036). Issuu was one of the businesses acquired in 2024 alongside Meetup, Mosaic (an asset deal), StreamYard, and WeTransfer (bsp-f1 ~L1863; bsp-424b4 ~L1853).

The F-1 does not disclose a standalone price for Issuu: it reports only that "the total consideration paid for the Meetup, StreamYard, and Issuu acquisitions was $280.7 million" as a combined figure (bsp-f1 ~L4935; bsp-424b4 ~L5039). Transaction costs (professional fees) for the Issuu acquisition specifically amounted to $2.1 million, recognized in general and administrative expense (bsp-f1 ~L4934; bsp-424b4 ~L5038 — the $2.1M line immediately follows the Issuu acquisition sentence, distinguishing it from StreamYard's $1.4M and Meetup's $1.5M). Post-close, Issuu, Inc. is listed as one of the subsidiaries that granted all-asset security interests in favor of the finance parties under Bending Spoons' main facilities agreements as of December 31, 2024 (bsp-f1 ~L4902; bsp-424b4 ~L5006).

Purchase accounting is disclosed only for the combined Meetup + StreamYard + Issuu pool (fair value of net assets acquired $280,745 thousand), not for Issuu alone (bsp-f1 ~L4936; bsp-424b4 ~L5040). That pool's allocation: goodwill $211,559K, intellectual properties $11,436K, customer base $77,966K, other intangibles (mainly trademarks) $21,905K, deferred tax assets $3,312K, other non-current assets $1,619K, cash $60,637K, and trade receivables/other current assets $12,969K, against total liabilities assumed of $120,658K (bsp-f1 ~L4936; bsp-424b4 ~L5040). Goodwill acquired in 2024 of $212 million was attributable to the Meetup, StreamYard, and Issuu acquisitions combined (bsp-f1 ~L5072; bsp-424b4 ~L5176). The intangibles carry estimated useful lives of 5 years (IP), 6 or 7 years (customer base), and 7 or 10 years (trademarks/other) (bsp-f1 ~L4940; bsp-424b4 ~L5041). On the equity side, in connection with the acquisition certain unvested Issuu equity awards accelerated on the change of control; the $1 million portion of their fair value attributable to post-combination vesting was treated as a separate transaction and recognized as compensation cost across cost of revenue, R&D, S&M, and G&A in 2024 (bsp-f1 ~L4939–4941; bsp-424b4 ~L5043–5045). Issuu also appears among the acquired teams (with WeTransfer) whose equity-instrument acceleration drove $5 million of transaction-related costs in 2024 (bsp-f1 ~L1946; bsp-424b4 ~L1936).

Stub-period contribution: Bending Spoons' 2024 consolidated income statement includes revenue of $92.4 million and income before tax of $21.7 million from Meetup, StreamYard, and Issuu combined, for the periods from their respective acquisition dates — not broken out for Issuu alone (bsp-f1 ~L4942; bsp-424b4 ~L5046).

## The playbook applied (where the OFFICIAL record shows it)
The F-1 documents the standard transform sequence on Issuu. First, a reorganization with headcount reduction: separation packages were "offered to team members in connection with the reorganizations of Issuu, Meetup, StreamYard, and WeTransfer" in 2024, contributing to reorganization-related expense across R&D, sales and marketing, and G&A that year (bsp-f1 ~L1882, L1886, L1890, L1950; bsp-424b4 ~L1872, L1876, L1880, L1940). Issuu is also named in the Q1 2025 reorganization-expense driver, alongside Brightcove, Evernote, komoot, Loomly, Meetup, StreamYard, and WeTransfer (bsp-f1 ~L1963; bsp-424b4 ~L1953). Second, the run-rate then drops: 2025 R&D, S&M, and G&A each reflect "a reduction in the personnel costs associated with the ongoing operations of Issuu, Meetup, StreamYard, and WeTransfer after their reorganizations in 2024" (bsp-f1 ~L1883, L1887, L1891; bsp-424b4 ~L1873, L1877, L1881). Third, cash generation improves: net cash from operating activities in 2025 (up $86M, or 42%) was driven partly "by improved cash generation at Issuu, Meetup, StreamYard, and WeTransfer following our transformations of these businesses" (bsp-f1 ~L2030; bsp-424b4 ~L2020), and the theme repeats for Q1 2026 (net cash from operating activities up $54M, or 254%), where Issuu is again named among the transformed businesses driving the improvement (bsp-f1 ~L2039; bsp-424b4 ~L2032). The specific layoff percentage or headcount cut for Issuu is not stated in either filing — [to-validate — press only]; do not assert a number. On the product side, the site shows continued feature breadth (flipbooks, articles, social-post creation, video, QR codes, digital sales, and integrations with Canva, Adobe Express, and Adobe InDesign), but the official pricing page renders its tiers client-side and did not expose specific plan names or dollar figures on fetch — [to-validate] price tiers (site-issuu, https://issuu.com/about; https://issuu.com/pricing).

## What holds the customer
The load-bearing signal for a subscription creator tool is the committed user's willingness to pay, and the filings give an unusually clear read. For 2024→2025, the increase in Issuu (and StreamYard) revenue "was driven by higher subscription revenue resulting from an increase in average revenue per subscriber, partly offset by a decrease in the number of subscribers" (bsp-f1 ~L1872; bsp-424b4 ~L1862). That is the machine's core bet made visible: prune the low-value tail and raise price/mix on the committed base, so ARPU rises even as subscriber count falls. (The filings state this ARPU-up/subscribers-down driver only for the annual 2024→2025 comparison; they do not restate it for Q1 2025→Q1 2026.) Issuu is also named among the businesses making the largest contributions to organic revenue growth in 2025 (which was 13%), alongside Meetup, Remini, StreamYard, and WeTransfer (bsp-f1 ~L1871; bsp-424b4 ~L1861). The filings attribute a portion of the acquired customer relationships to a "customer base" intangible (part of the $77,966 thousand customer-base fair value across the Meetup/StreamYard/Issuu pool, amortized over 6 or 7 years), consistent with betting on retained willingness-to-pay (bsp-f1 ~L4936, L4940; bsp-424b4 ~L5040, L5041). Neither the MAU/paying-subscriber counts, the NRR, nor the exact churn and ARPU figures for Issuu alone are broken out in either filing — [to-validate — press only].

## Where it sits in the machine
Issuu is at the optimized stage of the lifecycle: acquired July 2024, reorganized in 2024, and by 2025–Q1 2026 the filings already report reduced ongoing personnel costs (bsp-f1 ~L1883, L1887, L1891) and improved cash generation "following our transformations of these businesses" (bsp-f1 ~L2030, L2039; bsp-424b4 ~L2020, L2032). Its portfolio role is a cash-generative creator/publisher SaaS in the same 2024 cohort as Meetup, StreamYard, and WeTransfer (bsp-f1 ~L1863; bsp-424b4 ~L1853), and it is financially disclosed jointly with Meetup and StreamYard in the purchase-accounting table (bsp-f1 ~L4936; bsp-424b4 ~L5040). The filings do not group Issuu into an "enterprise video" cluster; Issuu sits in the digital-publishing / creator-tools part of the portfolio (bsp-f1 ~L4932; bsp-424b4 ~L5036).

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt). Every Issuu figure in the F-1 is restated identically in the 424B4.
- `site-issuu` — Issuu official site: https://issuu.com/about, https://issuu.com (homepage), https://issuu.com/pricing (pricing page fetched; tiers/prices did not render). Not a Bending Spoons fact source; retained only for product-description color.
