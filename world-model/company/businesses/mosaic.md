---
id: mosaic
type: business
title: Mosaic
status: confirmed
purpose: A portfolio of mobile app assets carved out of IAC and folded into the Bending Spoons machine — the one case in the 2024 cohort acquired as an asset deal rather than an entity.
provenance: official-site
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4, site-mosaic]
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
# Mosaic

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
Mosaic is a set of mobile app assets Bending Spoons acquired from IAC Inc. in 2024 (bsp-f1 ~L1863; bsp-424b4 ~L1853). In the revenue discussion, Bending Spoons lists the 2024 cohort as "Issuu, Meetup, Mosaic (which was an asset deal), StreamYard, and WeTransfer" — Mosaic is the only member of that year's cohort the filings flag explicitly as an asset deal rather than an acquisition of a company entity (bsp-f1 ~L1863; bsp-424b4 ~L1853). In the pro-forma / combined-financials discussion of 2024 acquisitions, the same event is described as "certain assets from IAC Inc." — listed alongside the entity acquisitions of Issuu, Community Matters Holdings (Meetup), StreamYard Top Corp, and The Creative Productivity Group (WeTransfer), which is where the structural distinction is visible: peers were named parent-entity acquisitions, Mosaic was assets (bsp-f1 ~L227; bsp-424b4 ~L205). Two of the constituent apps, iTranslate and RoboKiller, now run under Bending Spoons: their official sites each carry the footer "© Bending Spoons Operations S.p.A." (site-mosaic). The filings do not name iTranslate, RoboKiller, or any individual Mosaic app — the specific product roster is confirmed only from the products' own sites (site-mosaic), and the "Mosaic Group" name and 40+ app count are press-only [to-validate — press only].

## The deal
The filings record the transaction as a 2024 acquisition of "certain assets from IAC Inc.," and name it as "Mosaic (which was an asset deal)" (bsp-f1 ~L227, ~L1863; bsp-424b4 ~L205, ~L1853). This is the filings' own emphasis: within the 2024 cohort it is the asset deal, structurally distinct from buying a parent entity (as with StreamYard Top Corp or The Creative Productivity Group / WeTransfer) (bsp-f1 ~L225-227; bsp-424b4 ~L203-205). The accounting basis matches: transactions that do not meet the definition of a business are treated as asset acquisitions, with cost allocated to the assets acquired on the basis of relative fair values and contingent consideration recognized only once the related uncertainty is resolved or becomes probable and estimable — no goodwill is recorded, unlike a business combination (bsp-f1 ~L4796, ~L4803). Neither filing discloses a price, consideration, or goodwill/PPA figure for Mosaic (verified: the only Mosaic mentions are the 2024-cohort revenue and cash-flow lines; no dollar amount is attached — bsp-f1 ~L1863, ~L2032; bsp-424b4 ~L1853, ~L2022). NOTE: the "$5 million expense in association with an asset acquisition" (2023) and the follow-on "$1 million expense related to the same acquisition" (2024) refer to a single asset acquisition first recorded in 2023 — Mosaic was acquired in 2024, so these figures are NOT attributable to Mosaic and must not be read as its cost (bsp-f1 ~L1952, ~L1974; bsp-424b4 ~L1942, ~L1964). Any figure for the transaction value (e.g. a "$100 million+" valuation) appears only in press coverage and is not stated in the filings [to-validate — press only]. The count of employees who did not transfer is likewise press-only [to-validate — press only].

## The playbook applied (where the OFFICIAL record shows it)
The asset-deal structure is itself the first visible playbook move: the filings show Bending Spoons took the assets but not the corporate entity — "certain assets from IAC Inc." (bsp-f1 ~L227; bsp-424b4 ~L205). A telling OFFICIAL negative: the 2024 reorganization-related expense is attributed to separation packages for the reorganizations of "Issuu, Meetup, StreamYard, and WeTransfer" — Mosaic is NOT named in that reorganization list (bsp-f1 ~L1950; bsp-424b4 ~L1940). Consistent with an asset deal where few or no team members transferred, there is no separation-package reorganization credited to Mosaic in the filings; the layoff / employees-not-transferred figures are press-only [to-validate — press only]. Post-acquisition, the surviving apps have been migrated onto the Bending Spoons operating entity — iTranslate and RoboKiller both now publish under "Bending Spoons Operations S.p.A." (site-mosaic), the same operating shell the company routes its portfolio through, consistent with the filings' Italian-parent structure — Bending Spoons S.p.A., an Italian joint-stock company headquartered at Via Nino Bonnet 10, Milan (bsp-f1 ~L196, ~L464-468). Notably, the current Bending Spoons products page does not list Mosaic, iTranslate, RoboKiller, or Clime among its headline products (site-mosaic), while the individual app sites remain live under the Bending Spoons entity — suggesting a portfolio that is operated but not marketed as a flagship, i.e. optimized/harvested rather than showcased. Pricing tiers and plan limits were not quoted on the app landing pages fetched (site-mosaic).

## What holds the customer
The load-bearing signal for Mosaic is the paid-conversion and retention of committed users of the surviving utility apps (iTranslate translation, RoboKiller call-blocking) — subscription apps whose value is recurring, not one-time. The apps still run a free-to-premium funnel ("Try it free," a plans page) under the Bending Spoons entity (site-mosaic), which is the tell that they are managed for subscription willingness-to-pay rather than sunset. Two OFFICIAL negatives sharpen the read: (1) the 2024 organic-revenue narrative — organic growth was 7% in 2024 — credits Evernote, Remini, and StreamYard by name for the largest contributions and does not credit Mosaic (bsp-f1 ~L1864; bsp-424b4 ~L1854); (2) the company's per-business net revenue retention disclosure breaks out only AOL (95%), Evernote (99%), Remini (87%), and StreamYard (91%) averaged Q1 2023–Q1 2026 — Mosaic is not among the businesses given an NRR figure (bsp-f1 ~L407-408; bsp-424b4 ~L388, ~L1693). Both silences are consistent with a small, cash-optimized tail asset rather than a growth or headline-retention engine. Exact price points and Mosaic-specific retention/churn numbers are not disclosed, so the strength of that willingness-to-pay is inferred, not measured.

## Where it sits in the machine
Lifecycle: transforming toward optimized — the assets have been absorbed onto the Bending Spoons operating entity and are run quietly, off the headline products page (site-mosaic). Portfolio role: a low-profile utility/mobile-subscription tail, distinct from the marquee clusters. Unlike the enterprise-video cluster (Vimeo and Brightcove, both acquired in 2025 per the filings — bsp-f1 ~L228, ~L2034), Mosaic is a bundle of consumer mobile utilities with no obvious cluster peer named in the filings; treating it as a coherent "group" beyond the individually confirmed apps is press-only [to-validate — press only]. Corroborating its tail status: Mosaic is not named among the businesses whose transformation drove operating cash-flow improvement (2024: Evernote plus 2024 acquisitions generically; 2025: Issuu, Meetup, StreamYard, WeTransfer) (bsp-f1 ~L2029-2030; bsp-424b4 ~L2020).

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt): names "Mosaic (which was an asset deal)" and "certain assets from IAC Inc." in the 2024 acquisition cohort (~L227, ~L1863, ~L2032); discloses no price, consideration, or goodwill for Mosaic; asset-acquisition accounting policy (~L4796, ~L4803); 2024 organic-growth credits exclude Mosaic (~L1864); 2024 reorganization list excludes Mosaic (~L1950); per-business NRR excludes Mosaic (~L407-408); 2023 $5M / 2024 $1M asset-acquisition expense is a single 2023-originated acquisition, not Mosaic (~L1952, ~L1974).
- `bsp-424b4` — Bending Spoons final prospectus (424B4, captured at sources/2026-07-bsp-424b4-fulltext.txt): same Mosaic facts (~L205, ~L1853, ~L2022); organic-growth (~L1854); reorganization list (~L1940); NRR (~L388, ~L1693); asset-acquisition expense note (~L1942, ~L1964).
- `site-mosaic` — official app sites of the acquired Mosaic assets and the Bending Spoons products page: https://www.itranslate.com (footer "© Bending Spoons Operations S.p.A."), https://www.robokiller.com (footer "© Bending Spoons Operations S.p.A."), https://bendingspoons.com (products page; does not list Mosaic/iTranslate/RoboKiller/Clime).
