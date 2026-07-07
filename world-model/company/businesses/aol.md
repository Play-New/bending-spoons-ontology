---
id: aol
type: business
title: AOL
status: confirmed
purpose: A mature consumer internet franchise (email, news portal, search) that Bending Spoons acquired to run its transformation machine on cash-generative, committed users.
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-aol]
properties:
  revenue_usd_m: n.d.
  mau_m: n.d.
  paying_customers_m: n.d.
  nrr_pct: 95
  tenure_yrs: n.d.
  arpu: n.d.
  revenue_mix: advertising + subscription
  organic_channel_pct: n.d.
  conversion_pct: n.d.
  adj_op_margin_pct: n.d.
  status: main
  lifecycle: transforming
relations:
visibility: shared
---
# AOL

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
AOL operates an email service, a news portal, and a search engine catering to a consumer audience (bsp-f1 ~L378; bsp-424b4 ~L358). In Q1 2026 it was one of the ten main businesses — in alphabetical order, AOL, Brightcove, Eventbrite, Evernote, Harvest, komoot, Remini, StreamYard, Vimeo, and WeTransfer — that in aggregate accounted for more than 80% of revenue for the period (bsp-f1 ~L375–376). On a full-year 2025 carve-out basis (before Bending Spoons owned it), AOL's revenue was $633.4 million (bsp-f1 ~L3218; bsp-424b4 ~L3160). Its own site frames it as a consumer bundle of free products (AOL Mail, the AOL App) and paid add-ons — Ad-Free Mail, Desktop Gold, tech support (AOL Live Support Plus), and security/identity products such as Tech Fortress, System Mechanic, ID Protection, Data Secure, and Complete by AOL (site-aol, https://www.aol.com/products/). Advertising is a material part of its economics: in Q1 2026 advertising represented 12% of revenue, driven primarily by AOL, Remini, and WeTransfer (bsp-f1 ~L1686; bsp-424b4 ~L1676).

## The deal
On January 2, 2026, Bending Spoons acquired 100% of the issued and outstanding equity securities of AOL Holdco I LLC, a Delaware limited liability company, for a total cash consideration of $1.45 billion (bsp-f1 ~L4388; bsp-424b4 ~L4491). AOL Holdco I LLC is the owner of AOL (bsp-f1 ~L378). The preliminary purchase-price allocation as of the acquisition date shows total consideration of $1,454,432 thousand allocated to: goodwill $847,949K, customer base $398,720K, intellectual properties $56,044K, other intangible assets $141,740K, plus cash $18,154K and trade receivables/other current assets $20,218K, against $28,393K of liabilities assumed (total assets acquired $1,482,825K) (bsp-f1 ~L3225; bsp-424b4 ~L3229). The acquisition is one of only two in the period — the other being Vimeo — that Bending Spoons treats as "significant" for purposes of Rule 3-05 of Regulation S-X: the filings state that all 2025/2026 acquisitions other than AOL Holdco I LLC and Vimeo are not significant and therefore need no separate historical financials (bsp-f1 ~L232–234; bsp-424b4 ~L211). Accordingly, AOL's audited combined financials for the years ended December 31, 2024 and 2025 are presented on a carve-out basis under the name AOL Holdco II LLC, a business of College Parent, L.P. (bsp-f1 ~L217–218, ~L4257; bsp-424b4 ~L195–196). Bending Spoons funded the AOL, Eventbrite, and Vimeo purchase prices ($1,454M, $505M, and $1,359M, respectively) together from a combination of term-loan facilities — a EUR TLB (€300M / $339M) dated January 30, 2026, a USD TLB ($950M) dated January 2, 2026, a USD TLA ($660M) dated January 2, 2026, and EUR TLA facilities (€476M / $538M) (bsp-f1 ~L3114–3116). (AOL's own legacy debt — the "AOL Term Loan A" / "AOL Debt Agreement," which stood at $775M at December 31, 2025 — was the target's pre-existing borrowing and was repaid in full when the business was sold to Bending Spoons on January 2, 2026 (bsp-f1 ~L5755, ~L5812).) Because AOL is a U.S. consumer-communications business acquired by a foreign (Italian) parent, Bending Spoons submitted a voluntary notice to the Committee on Foreign Investment in the United States (CFIUS) in March 2026; that filing is on file with CFIUS and is currently undergoing the review process, which the company expects could take several months (bsp-f1 ~L950–952; bsp-424b4 ~L931–933).

## The playbook applied (where the OFFICIAL record shows it)
The filings list AOL among the recently acquired businesses that are the current focus of transformation, alongside Eventbrite and Vimeo ("much of our current focus is on transforming those more recently acquired, including AOL, Eventbrite, and Vimeo") (bsp-f1 ~L135; bsp-424b4 ~L112). The reorganization is visible in the cost lines: Q1 2026 research-and-development, sales-and-marketing, and general-and-administrative expense each grew in part because of "separation packages offered to team members in connection with the reorganizations of AOL, Eventbrite, and Vimeo" (bsp-f1 ~L1917, ~L1919, ~L1922; bsp-424b4 ~L1907). The specific size of any AOL workforce reduction (a headcount or layoff percentage) is not stated in either filing — [to-validate — press only]; do not state a number. On the product side, AOL's own site shows the monetization surface the playbook operates on: a free core (AOL Mail, AOL App) funnelling into paid tiers (Ad-Free Mail, Desktop Gold, Live Support Plus, and security/identity bundles) (site-aol, https://www.aol.com/products/). The official help and product pages reference these paid plans but do not publish specific prices or storage limits — exact price tiers are a gap in the official record captured here (site-aol, https://help.aol.com/products/aol-mail).

## What holds the customer
For AOL the load-bearing signal is retention of the committed, paying consumer. The filings disclose that, averaged across Q1 2023 through Q1 2026, net revenue retention for AOL was 95% (Evernote 99%, Remini 87%, StreamYard 91% for the businesses broken out) (bsp-f1 ~L408, ~L1703; bsp-424b4 ~L388). Net revenue retention is defined as subscription revenue in a quarter from customers acquired before the end of the same quarter a year earlier, divided by the prior-year subscription revenue from those customers (bsp-f1 ~L413). A 95% NRR on a decades-old consumer email/portal base indicates a sticky, willing-to-pay cohort whose subscriptions persist year over year — the exact profile Bending Spoons buys and optimizes. Note that this NRR figure spans a period largely before Bending Spoons owned AOL (acquired January 2026), so it reflects the asset's inherent stickiness rather than post-acquisition monetization; post-deal retention is not separately disclosed and is [to-validate — press only].

## Where it sits in the machine
AOL is in the transforming stage of the lifecycle: acquired in January 2026 and explicitly named among the businesses currently being transformed, alongside Eventbrite and Vimeo (bsp-f1 ~L135, ~L378; bsp-424b4 ~L112, ~L358). Its portfolio role is a large, cash-generative consumer franchise (full-year 2025 carve-out revenue $633.4M) with strong retention (95% NRR) and a meaningful advertising revenue stream (bsp-f1 ~L3218, ~L408, ~L1686). AOL is a standalone consumer internet property; the filings do not group it into a product cluster, so no clustering is asserted here. It is held within the Bending Spoons holding structure via AOL Holdco I LLC and operated on the shared platform (bsp-f1 ~L4388).

## The seller-dependency the underwriting must price
A structural fact of the carve-out: roughly 40% of AOL's revenue flows THROUGH a contractual agreement with the former Parent — FY2025 display advertising ($240.1M) and search advertising ($11.3M) are earned via the Parent's arrangements, out of $633.4M total revenue (`bsp-f1` ~L5697-5707). The continuity of that contract is therefore a load-bearing underwriting assumption, not a detail; `deal-monitor` watches it. The Business also arrived leveraged: the AOL Term Loan A ($775.0M, SOFR+4.5%) was repaid in full at the January 2, 2026 closing (~L5755-5760) — capital deployed beyond the equity consideration, which `capital-allocation` counts.

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt).
- `site-aol` — AOL official site/product pages actually used: https://www.aol.com/products/ and https://help.aol.com/products/aol-mail.
