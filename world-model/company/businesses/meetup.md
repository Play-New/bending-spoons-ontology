---
id: meetup
type: business
title: Meetup
status: confirmed
purpose: A community-and-events platform Bending Spoons acquired, reorganized, and turned to organic subscription growth — a clean case of the acquire-transform-optimize machine at work.
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-meetup]
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
# Meetup

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
Meetup facilitates the organization of events and connects individuals through interest-based communities (bsp-424b4 ~L5028, bsp-f1 ~L4924). Its own site frames it as "the people platform, where interests become friendships," running local groups and events across interests from hiking and reading to networking and skill-sharing, with membership free to join (site-meetup, https://www.meetup.com/). Its revenue model is subscription-based: organizers pay for tiers, and the filings attribute Meetup's revenue growth to increases in both average revenue per subscriber and the number of subscribers (bsp-424b4 ~L1863, bsp-f1 ~L1873).

## The deal
On January 23, 2024, Bending Spoons completed the acquisition of 100% of the issued and outstanding equity securities of Community Matters Holdings Inc., a Delaware corporation and the owner of Meetup, accounted for as a business combination (bsp-424b4 ~L5027, bsp-f1 ~L4923). The acquired entity was the then ultimate parent company of Meetup LLC (bsp-424b4 ~L203, bsp-f1 ~L225). The filings do not disclose a standalone price for Meetup: they report that the total consideration paid for the Meetup, StreamYard, and Issuu acquisitions combined was $280.7 million (bsp-424b4 ~L5039, bsp-f1 ~L4935), and that goodwill of $212 million was attributable to those three acquisitions together (bsp-424b4 ~L5176, bsp-f1 ~L5072). The purchase-price allocation for the Meetup/StreamYard/Issuu combined business combination records goodwill of $211,559K, customer base of $77,966K, intellectual properties of $11,436K, other intangible assets of $21,905K, cash and cash equivalents of $60,637K, total assets acquired of $401,403K against total liabilities assumed of $120,658K, for a fair value of net assets acquired of $280,745K (bsp-424b4 ~L5040, bsp-f1 ~L4936). The three acquired businesses (Meetup, StreamYard, Issuu) contributed combined 2024 revenue of $92.4 million and income before tax of $21.7 million from their respective acquisition dates (bsp-424b4 ~L5046, bsp-f1 ~L4942).

## The playbook applied (where the OFFICIAL record shows it)
The filings show the standard reorganization pattern: separation packages were offered to team members in connection with the reorganizations of Issuu, Meetup, StreamYard, and WeTransfer in 2024, recognized across R&D, sales-and-marketing, and G&A expense (bsp-424b4 ~L1872, ~L1876, ~L1880; bsp-f1 ~L1882, ~L1886, ~L1890). Meetup reorganization-related expense was also called out in the 2024 reorganization-cost driver line and again among the Q1 2025 reorganization drivers (bsp-424b4 ~L1940, ~L1953; bsp-f1 ~L1950, ~L1963). By the following year the filing records the payoff: 2024-to-2025 operating-cash-flow growth ($86 million, or 42%) was "primarily driven by improved cash generation at Issuu, Meetup, StreamYard, and WeTransfer following our transformations of these businesses," and the personnel-cost reductions confirm the reorganizations were completed "in 2024" (bsp-424b4 ~L2020, ~L1873; bsp-f1 ~L2030, ~L1883). The exact layoff percentage is [to-validate — press only]; the filings state the reorganization occurred but give no Meetup headcount figure.

Meetup's own site evidences continued product investment post-acquisition: a redesigned modern web interface (2025) and a new mobile design finalized in December 2025 (site-meetup, https://www.meetup.com/blog/2026-meetup-roadmap/). A three-tier organizer structure is now published — Meetup Starter (free: 1 group, up to 2 in-person events/month, up to 10 attendees/event), Meetup Standard (paid: up to 3 groups, unlimited events/attendees, ticket sales, member dues, email promotions), and Meetup Pro (multi-group/network management, custom branding, analytics) (site-meetup, https://www.meetup.com/blog/introducing-meetup-starter/; https://www.meetup.com/lp/meetup-pro/). The 2026 roadmap names a unified organizer+member app, QR-code check-ins, richer member profiles, and a Super Organizer badge (site-meetup, https://www.meetup.com/blog/2026-meetup-roadmap/). Gap: exact dollar prices for Standard and Pro are not exposed on the public pages fetched (the help-center pricing article is gated); no AI features are named in the official posts reviewed.

## What holds the customer
For Meetup the load-bearing signal is the paying organizer's willingness-to-pay and retention, and the official record is unusually clean on this. Meetup was among the largest contributors to the company's 13% organic revenue growth in 2025, and the filings state the increase in Meetup revenue "was due to an increase in subscription revenue, driven by an increase in both average revenue per subscriber and the number of subscribers" — i.e. both price and count rising together, the opposite of the milk-then-decline pattern the same filings record for some other assets where subscriber counts fell (bsp-424b4 ~L1861, ~L1863; bsp-f1 ~L1871, ~L1873). In Q1 2026 Meetup was again among the largest contributors to the company's 6% organic revenue growth, with the increase "driven by higher subscription revenue resulting from an increase in the number of subscribers" (bsp-424b4 ~L1901, ~L1902; bsp-f1 ~L1911, ~L1912). The paid-tier structure itself (site-meetup) is the willingness-to-pay instrument: a free Starter tier deliberately capped (1 group, 2 events/month, 10 attendees) funnels committed organizers into Standard/Pro. Rising subscribers alongside rising ARPU is the retained-committed-user signal; grounding it to per-cohort churn would require data the filings do not break out [to-validate — press only].

## Where it sits in the machine
Meetup is at the optimized stage: acquired January 2024, reorganized within 2024, and by 2025-Q1 2026 a repeat top contributor to organic growth on both price and volume (bsp-424b4 ~L1861, ~L1901; bsp-f1 ~L1871, ~L1911). Its portfolio role is a durable subscription community-and-events asset held under the Bending Spoons brand estate — Meetup is among the material word marks and logos the company holds trademark registrations/applications for (bsp-424b4 ~L1166, bsp-f1 ~L1183). It clusters loosely with the events/communications assets Bending Spoons acquired in the same window (StreamYard, and later Eventbrite), but the filings do not assert a formal "events" product cluster, so that grouping is an observation rather than a filing-stated relation.

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt).
- `site-meetup` — Meetup official site/blog: https://www.meetup.com/ ; https://www.meetup.com/blog/2026-meetup-roadmap/ ; https://www.meetup.com/blog/introducing-meetup-starter/ ; https://www.meetup.com/lp/meetup-pro/ .
