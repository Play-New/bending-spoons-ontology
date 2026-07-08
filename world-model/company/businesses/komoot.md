---
id: komoot
type: business
title: komoot
status: confirmed
purpose: A route-planning and outdoor-navigation business Bending Spoons acquired, reorganized, and is now growing on subscription revenue — a case of the machine at work.
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-komoot]
properties:
  revenue_usd_m: n.d.
  mau_m: n.d.
  paying_customers_m: n.d.
  nrr_pct: n.d.
  tenure_yrs: n.d.
  arpu: n.d.
  revenue_mix: subscription + one-time purchases (~L1689)
  organic_channel_pct: n.d.
  conversion_pct: n.d.
  adj_op_margin_pct: n.d.
  status: main
  lifecycle: optimized
relations:
visibility: shared
---
# komoot

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
komoot provides route planning and navigation tools supported by community-generated content for outdoor activities (bsp-f1 ~L388; bsp-424b4 ~L368). Both filings describe it more specifically as a route-planning and navigation product for hikers and cyclists (bsp-f1 ~L2007; bsp-424b4 ~L1997). Its own site describes it as an outdoor-adventure platform to find, plan, and share routes for hiking, cycling, mountain biking, road cycling, and running, with turn-by-turn voice navigation and offline maps (site-komoot, komoot.com). The filings list komoot among Bending Spoons' main businesses in Q1 2026 (AOL, Brightcove, Eventbrite, Evernote, Harvest, komoot, Remini, StreamYard, Vimeo, WeTransfer), which in aggregate accounted for more than 80% of revenue for the period (bsp-f1 ~L375-376; bsp-424b4 ~L355). The corporate entity acquired is komoot GmbH, a limited liability company incorporated under the laws of Germany and the owner of komoot (bsp-f1 ~L228, ~L4961; bsp-424b4 ~L206, ~L5065).

## The deal
_Consideration, enterprise value, and the PPA breakdown are held once in `../deals.csv` — the single source of truth for the `Deal`; the account below is the grounded elaboration, and the CSV prevails on any divergence._

On March 20, 2025, Bending Spoons completed the acquisition of 100% of the share capital of komoot GmbH and accounted for it as a business combination (bsp-f1 ~L4961; bsp-424b4 ~L5065, ~L5067). Transaction costs (professional fees) of $1 million were recognized in general-and-administrative expense (bsp-424b4 ~L5068). No komoot-only price is disclosed: the filings report a single blended total consideration of $701 million for the Loomly, komoot, MileIQ, and Harvest acquisitions (bsp-f1 ~L4973; bsp-424b4 ~L5077), and the corresponding fair-value net assets acquired total $701.253 million (bsp-424b4 ~L5078). Purchase-price allocation for that four-deal group: goodwill of $469 million ($469.086M), intellectual properties $30.678M, customer base $222.886M, and other intangible assets (mainly trademarks) $32.785M — komoot's share of each is not broken out (bsp-f1 ~L5073; bsp-424b4 ~L5078, ~L5177). Estimated useful lives: 5 years for intellectual properties, 7–14 years for the customer base, and 5–10 years for other intangibles/trademarks (bsp-424b4 ~L5080). komoot's intangible assets were transferred to Italy, triggering exit taxes payable in Germany (bsp-f1 ~L5350; bsp-424b4 ~L5454). Bending Spoons holds registered and pending trademarks for the komoot mark across the U.S., E.U., and other jurisdictions (bsp-f1 ~L1183; bsp-424b4 ~L1166).

## What the stub period contributed
The consolidated income statement for 2025 includes revenue from the Loomly, komoot, MileIQ, and Harvest group of $119 million and income before tax of $27 million for the periods from their respective acquisition dates — a blended figure, not komoot-only (bsp-f1 ~L4977; bsp-424b4 ~L5081). Unaudited supplemental pro-forma combined revenue (as if Bending Spoons, komoot, Loomly, MileIQ, Harvest, Brightcove, and Vimeo had all been acquired on Jan 1, 2024) was $1,445.650M for 2024 and $1,761.916M for 2025, with pro-forma net income moving from a $(32.555)M loss in 2024 to $9.143M in 2025 (bsp-f1 ~L5008, ~L5014; bsp-424b4 ~L5112, ~L5118); komoot is one of seven businesses in that aggregate and is not separated.

## The playbook applied (where the OFFICIAL record shows it)
The filings evidence the standard post-acquisition reorganization: separation packages were offered to team members in connection with the reorganizations of Brightcove, Harvest, komoot, Loomly, MileIQ, and WeTransfer in 2025, contributing to increases in R&D, sales-and-marketing, and general-and-administrative expense that year (bsp-f1 ~L1883, ~L1887, ~L1891, ~L1951; bsp-424b4 ~L1873, ~L1877, ~L1881, ~L1941). komoot's reorganization began early: it already appears in the Q1 2025 reorganization-related expense driver list alongside Brightcove, Evernote, Issuu, Loomly, Meetup, StreamYard, and WeTransfer (bsp-f1 ~L1963; bsp-424b4 ~L1953). By Q1 2026 the filings describe a reduction in personnel costs associated with the ongoing operations of Brightcove, komoot, and WeTransfer "after their reorganizations" — i.e., the reorg was largely complete and its cost base had come down (bsp-f1 ~L1917, ~L1919, ~L1922; bsp-424b4 ~L1907, ~L1909, ~L1912). The reorganization also improved cash flow: net cash from operating activities grew 254% ($21.350M → $75.654M) from Q1 2025 to Q1 2026, driven in part by "improved cash generation at Brightcove, Issuu, komoot, Loomly, StreamYard, and WeTransfer following our transformations of these businesses" (bsp-f1 ~L2039; bsp-424b4 ~L2032). Any specific headcount or layoff percentage is [to-validate — press only] and is not stated in the filings. On the product side, komoot's own Premium page shows the current paid feature set — multi-day route planning, personal collections, live tracking, weather-on-route, sport-specific maps, worldwide offline maps and navigation, 3D maps, and a komoot map on Garmin (site-komoot, komoot.com/premium). Exact price tiers are not exposed on the public pages fetched (they sit behind a purchase/login flow), so plan prices are a gap here.

## What holds the customer
The load-bearing signal is willingness-to-pay and retention of the committed user. The filings give a direct read: in Q1 2026, organic revenue growth was 6%, with komoot, Meetup, and WeTransfer making the largest contributions, and the increase in komoot (and WeTransfer) revenue "was due to an increase in subscription revenue driven by an increase in both average revenue per subscriber and the number of subscribers" (bsp-f1 ~L1911, ~L1913; bsp-424b4 ~L1901, ~L1903). That is the strongest possible official signal — more paying subscribers AND higher revenue per subscriber (ARPU up) simultaneously, post-reorg. The filings also note komoot has "one-time purchases" as a revenue source within its "Other" revenue category, indicating a mixed monetization model beyond subscriptions (bsp-f1 ~L1689; bsp-424b4 ~L1679). Bending Spoons also frames komoot as AI-resistant: it cites komoot's "user-generated, hyper-local content" as an example of information neither broadly accessible nor reproducible, limiting the risk of replacement by general-purpose AI chatbots (bsp-f1 ~L2851; bsp-424b4 ~L2843). komoot's site claims 45 million users and a 4.8/5 app rating from 300k+ reviewers, but those are marketing figures, not audited retention metrics, and should be treated as such (site-komoot, komoot.com); the filings disclose no MAU, paying-subscriber count, or NRR for komoot.

## Where it sits in the machine
Lifecycle stage: optimized — acquired March 20, 2025, reorganized during 2025 (reorg already underway by Q1 2025), and by Q1 2026 a lower ongoing cost base, improved cash generation, and growing subscription revenue are all documented (bsp-f1 ~L1917, ~L2039; bsp-424b4 ~L1907, ~L2032). Portfolio role: a consumer-subscription business in the outdoor/activity vertical, with seasonality — komoot "typically sees higher usage and revenue during the warm-weather months in Europe, where most of its customers are located" (bsp-f1 ~L2007; bsp-424b4 ~L1997). The filings do not cluster komoot with any other named product into a formal segment; it is grouped only alphabetically among the main businesses (AOL, Brightcove, Eventbrite, Evernote, Harvest, komoot, Remini, StreamYard, Vimeo, WeTransfer) (bsp-f1 ~L375; bsp-424b4 ~L355). A thematic adjacency to tractive (acquired 2026, pet/outdoor tracking) is not asserted by the filings and would be [to-validate — press only].

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt).
- `site-komoot` — komoot official site: https://www.komoot.com/ and https://www.komoot.com/premium.
