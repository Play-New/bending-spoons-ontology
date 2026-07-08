---
id: mileiq
type: business
title: MileIQ
status: confirmed
purpose: A mileage-tracking app acquired in mid-2025 and folded into the Bending Spoons portfolio — a case of the acquire-reorganize-operate machine at work.
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-mileiq]
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
  lifecycle: transforming
relations:
visibility: shared
---
# MileIQ

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
MileIQ is an automatic mileage-tracking application; the F-1 states plainly that "MileIQ provides a mileage tracking application" (bsp-f1 ~L4966, bsp-424b4 ~L5070). The app automatically detects and classifies drives as business or personal and generates tax-compliant reports for deductions or expense reimbursements (site-mileiq). It serves two audiences: individual drivers who need mileage records for taxes or reimbursement, and team managers who oversee multiple drivers from small groups to large fleets (site-mileiq). Industry-specific solutions are offered for construction, real estate, small business, rideshare/delivery, food & beverage, and nonprofits (site-mileiq).

## The deal
_Consideration, enterprise value, and the PPA breakdown are held once in `../deals.csv` — the single source of truth for the `Deal`; the account below is the grounded elaboration, and the CSV prevails on any divergence._

On June 30, 2025, Bending Spoons completed the acquisition of 100% of the issued and outstanding equity securities of MileIQ Inc., a Delaware corporation and the owner of MileIQ, and accounted for it as a business combination (bsp-f1 ~L4965, bsp-424b4 ~L5069). The F-1 describes MileIQ as a company that "provides a mileage tracking application" (bsp-f1 ~L4966). The F-1 does not disclose a standalone price for MileIQ; instead it reports that "the total consideration paid for the Loomly, komoot, MileIQ, and Harvest acquisitions was $701 million" as a group (bsp-f1 ~L4973, bsp-424b4 ~L5077). For that same group of four acquisitions, the fair value of net assets acquired was $701.253 million, of which $469.086 million was goodwill, $222.886 million was customer base, $30.678 million was intellectual properties, and $32.785 million was other intangible assets (mainly trademarks) (bsp-f1 ~L4974). The estimated useful life is 5 years for intellectual properties, 7 to 14 years for the customer base, and 5 to 10 years for other intangible assets (bsp-f1 ~L4975). No portion of this consideration, goodwill, or intangible value is broken out for MileIQ alone; every figure is a four-company group total. Transaction costs (professional fees) recognized in general and administrative expense in connection with the MileIQ acquisition amounted to $1 million (bsp-f1 ~L4968).

## The playbook applied (where the OFFICIAL record shows it)
The F-1 shows the standard post-acquisition reorganization pattern applied to MileIQ. Across research and development, sales and marketing, and general and administrative expense lines for 2025, the F-1 repeatedly lists "separation packages offered to team members in connection with the reorganizations of Brightcove, Harvest, komoot, Loomly, MileIQ, and WeTransfer" as a driver of increased cost (bsp-f1 ~L1883, ~L1887, ~L1891; bsp-424b4 ~L1873, ~L1877, ~L1881). The reorganization-related expense note confirms that in 2025 this expense "was driven by separation packages offered to team members in connection with the reorganizations of Brightcove, Harvest, komoot, Loomly, MileIQ, and WeTransfer" (bsp-f1 ~L1951, bsp-424b4 ~L1941). The specific size of any MileIQ headcount reduction is [to-validate — press only]; the F-1 states only that separation packages were offered, not a percentage or number.

On the product's own record, MileIQ has been rebranded under Bending Spoons ownership: the mileiq.com footer reads "© 2026 Bending Spoons US Inc." (site-mileiq). The live site presents a two-track offering — Individuals and Teams — with a self-serve Free tier and a paid Unlimited tier, plus a separate business-pricing track for teams (site-mileiq).

## What holds the customer
The load-bearing signal is willingness-to-pay by the committed user. MileIQ's pricing page enforces a hard usage gate — a Free plan capped at 40 tracked drives per month, versus an Unlimited plan at $11.66/month billed annually (equivalently $13.99/month billed monthly) that removes the cap (site-mileiq). This gate converts the habitual, high-mileage driver — the one for whom mileage is real tax money — into a paying subscriber, while casual drivers stay free. The site claims drivers save on average $8,400 per year in tax deductions and quotes 1M+ active users and 80,000+ five-star reviews (site-mileiq); these are self-reported marketing figures, so treat the specific numbers as [to-validate — press only]. The F-1 does not break out MileIQ-specific MAU, paying customers, net revenue retention, ARPU, or churn — those metrics are reported only at the portfolio level (over 500 million monthly active users and more than 9 million monthly paying customers in March 2026, bsp-f1 ~L172) — so any MileIQ-specific retention or unit read is [to-validate — press only] against non-public data.

## Where it sits in the machine
MileIQ is in the transforming stage: acquired June 30, 2025, run through a reorganization with separation packages during 2025 (bsp-f1 ~L1951), and now operating under the Bending Spoons US Inc. brand with a live freemium-to-subscription funnel (site-mileiq). In portfolio terms it sits in the 2025 cohort of acquisitions ("In 2025, we acquired Brightcove, Harvest, komoot, Loomly, MileIQ, and Vimeo," bsp-f1 ~L2034), and is one of the businesses "acquired after the end of Q1 2025 and before the end of Q1 2026" alongside AOL, Eventbrite, Harvest, and Vimeo (bsp-f1 ~L1910). For accounting purposes it is grouped in the F-1 with Loomly, komoot, and Harvest under a single $701 million consideration line (bsp-f1 ~L4973). That same four-company group contributed revenue of $119 million and income before tax of $27 million to the 2025 consolidated income statement, from the respective acquisition dates (bsp-f1 ~L4977) — MileIQ's own share of that stub is not disclosed. MileIQ is also included in the supplemental pro forma combined results (with komoot, Loomly, Harvest, Brightcove, and Vimeo) as if acquired on January 1, 2024 (bsp-f1 ~L5008). The F-1 does not assert a thematic cluster for MileIQ (unlike the video pairing of Vimeo and Brightcove), so any "expense/productivity" clustering beyond the shared accounting group would be inference and is not claimed here.

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt).
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt); MileIQ acquisition and reorganization language match the F-1.
- `site-mileiq` — MileIQ official site: https://mileiq.com/ and https://mileiq.com/pricing.
