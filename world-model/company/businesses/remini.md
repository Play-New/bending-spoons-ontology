---
id: remini
type: business
title: Remini
status: confirmed
purpose: A consumer AI image/video enhancement app that Bending Spoons acquired early and turned into a word-of-mouth, ads-plus-subscription monetization machine — the clearest case of the transformation playbook creating organic growth.
provenance: official-filing
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1, bsp-424b4]
properties:
  revenue_usd_m: n.d.
  mau_m: n.d.
  paying_customers_m: n.d.
  nrr_pct: 87
  tenure_yrs: n.d.
  arpu: n.d.
  revenue_mix: "subscription ~85% since 2023 (~L2689) + advertising"
  organic_channel_pct: n.d.
  conversion_pct: n.d.
  adj_op_margin_pct: n.d.
  status: main
  lifecycle: optimized
relations:
visibility: shared
---
# Remini

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects). No business↔business or business↔customer link exists — that absence is the gap (`../../customer/cross-product-graph.md`).


## What it is
Remini is a consumer-focused image and video enhancement and generation application (bsp-f1 ~L390; bsp-424b4 ~L370). At the time of acquisition it was a mobile application offering AI-based photo editing functionality, primarily focused on enhancing blurry or low-resolution images (bsp-424b4 ~L2649). Bending Spoons then completely redesigned the app around the photo-enhancement features that already accounted for nearly all user engagement, eliminating non-core functionality such as coloring black-and-white photos or removing scratches and blemishes (bsp-424b4 ~L2677–2679). The current feature set, per the filing, includes an AI feature (launched 2023) that lets users upload a few photos of themselves and generates photorealistic images of them, plus text-based image editing, virtual outfit try-on, and video generation (bsp-424b4 ~L2680, ~L2685). It was one of Bending Spoons' main businesses in Q1 2026, listed alphabetically alongside AOL, Brightcove, Eventbrite, Evernote, Harvest, komoot, StreamYard, Vimeo, and WeTransfer; these main businesses in aggregate accounted for more than 80% of revenue for the period (bsp-f1 ~L375, ~L1694). A specific "100 million monthly active users" claim and the marketing-page capability list (unblur/denoise/restoration/enlargement/color-fix, etc.) appear only on the company's public site, not in either filing: [to-validate — press only].

## The deal
Both filings state that Remini was acquired in June 2021 (bsp-f1 ~L390; bsp-424b4 ~L2648). The acquisition was structured as an asset transaction, and no team transferred with the business (bsp-424b4 ~L2660). Neither filing discloses a price, consideration, goodwill, or purchase-price allocation specific to Remini (verified: no Remini-line consideration/goodwill figure in either file). The stated rationale at the time: Remini had already experienced strong growth but analysis suggested room to improve marketing and monetization efficiency; the company saw the trajectory as sufficiently predictable given robust subscriber retention and customer acquisition occurring almost entirely through organic channels; and it expected Remini to add significantly to overall revenue, making the transformation an attractive use of resources (bsp-424b4 ~L2651–2653).

## The playbook applied (where the OFFICIAL record shows it)
Remini is the lead case study in both filings — the first of three worked examples of the Platform-powered acquire/transform/optimize cycle (bsp-424b4 ~L2648; bsp-f1 ~L129). Both filings summarize it as: "At Remini, we rewrote the codebase in full, developed dedicated tooling, redesigned user experience and monetization, and delivered powerful new features" (bsp-f1 ~L129; bsp-424b4 ~L106). Remini is also listed among the businesses Bending Spoons "continue[s] to optimize" that have been in the portfolio for years (bsp-f1 ~L134; bsp-424b4 ~L111). The headline outcome: since acquisition the product was rebuilt from the ground up, and in 2025 Remini served on average more than five times as many monthly active users and generated more than nine times as much revenue relative to pre-acquisition levels (bsp-424b4 ~L2655). (A revenue-vs-2021 index graph is referenced but the underlying data is not derived from audited financial statements (bsp-424b4 ~L2657).)

Organization. The team was allocated after the asset deal (no team came with it): ~30 FTE Spooners initially, scaled to a peak of 64 average FTEs in 2024, then reduced to ~20 FTEs at end-2025 as opportunities showed diminishing returns and resources were redeployed elsewhere — the filing presents this up-and-down staffing as a demonstration of decisive talent reallocation, not distress (bsp-424b4 ~L2661, ~L2664–2665, ~L2673). (This is the only Remini-specific headcount detail in the filings; any Remini-specific "layoff" framing tied to a general reorganization is [to-validate — press only].)

Technology. Within months of acquisition Bending Spoons integrated its proprietary technologies, fully rewrote Remini's codebase, and rearchitected its IT infrastructure (bsp-f1 ~L2677; bsp-424b4 ~L2669). It built new proprietary tooling for productizing and testing AI-based features, later made available across the portfolio (bsp-f1 ~L2678; bsp-424b4 ~L2670). Viral spikes created scale challenges: during a 2023 spike the rate of images generated per day rose from fewer than 100,000 to ~7 million in under a month, addressed via UX/infra optimizations including dynamically adjusting the free/paid balance and pricing at peak and real-time selection of the lowest-cost sufficient GPU set (bsp-f1 ~L2681–2683; bsp-424b4 ~L2673–2675).

Product. The app was completely redesigned around its core photo-enhancement engagement, with non-core features cut; the filing quantifies the result: 60-day-from-install user retention up 36% and photos processed/saved per user over the same window up 46% (bsp-f1 ~L2688; bsp-424b4 ~L2680). The 2023 AI-selfie feature (upload a few photos, generate photorealistic images) triggered a viral spike that took Remini to #1 by free downloads on the U.S. Apple App Store and in many other countries (bsp-f1 ~L2689–2691; bsp-424b4 ~L2681–2683). AI features introduced at Remini are cited as evidence of the capabilities advantage expected to compound as AI advances (bsp-f1 ~L1794; bsp-424b4 ~L1784).

Marketing & monetization. After the 2023 spike the company built tooling (market screening, user-sentiment analysis, a dedicated experimentation framework) to engineer spikes deliberately, and has since triggered six additional viral spikes (bsp-f1 ~L2694–2695; bsp-424b4 ~L2686–2687). Shortly after closing it refocused Remini from one-time/consumable purchases to subscriptions: subscriptions were 43% of Remini revenue in 2021, rose to 85% in 2023, and have stayed ~that level since (bsp-424b4 ~L2689). More than 1,000 monetization experiments have been run at Remini, primarily to optimize subscription revenue while also lifting advertising revenue (bsp-f1 ~L2698; bsp-424b4 ~L2690). Average revenue per monthly active user was 50% higher in 2025 than in 2021 — even as MAU rose more than fivefold over the same period, so ARPU and the user base grew together (bsp-424b4 ~L2691). At the group level Remini contributes to two revenue lines: it was among the largest contributors to organic revenue growth in both 2024 (which was 7%, with Evernote, Remini, StreamYard) and 2025 (13%, with Issuu, Meetup, Remini, StreamYard, WeTransfer), and it is named with AOL and WeTransfer as a primary driver of advertising revenue, which was 12% of total revenue in Q1 2026 (bsp-f1 ~L1864, ~L1871, ~L1686; bsp-424b4 ~L1854, ~L1861, ~L1676). Exact consumer tier pricing/plan limits are not in either filing — [to-validate — press only].

## What holds the customer
For Remini the load-bearing signal is a mixed one, and the official record is unusually candid about it. On willingness-to-pay retention, both filings give Remini's net revenue retention averaged across Q1 2023–Q1 2026 as 87% — the lowest of the four businesses broken out (AOL 95%, Evernote 99%, StreamYard 91%) (bsp-f1 ~L408, ~L1703; bsp-424b4 ~L388, ~L1693). This is consistent with a consumer app where committed spend is thinner than in productivity or workplace tools. The offsetting signal is acquisition efficiency: Remini "relies predominantly on word of mouth" for customer acquisition — contrasted explicitly with Brightcove's sales-driven acquisition — which is the hardest-to-fake evidence of genuine user value: growth that is pulled, not bought (bsp-f1 ~L431, ~L1724; bsp-424b4 ~L411, ~L1714). The filing reinforces this with the redesign metrics — 60-day retention +36% and photos saved per user +46% — as direct evidence the reworked core deepened engagement (bsp-424b4 ~L2680). The tension surfaces in the most recent period: both filings attribute a decrease in Remini revenue to a decline in monthly active users, which cut both advertising revenue and subscriber counts (bsp-f1 ~L1914; bsp-424b4 ~L1904). So the net reading: real organic pull and strong AI-driven feature velocity, with subscription now the dominant revenue mode (~85% since 2023) and ARPU up 50% (2025 vs 2021), but sub-portfolio subscription stickiness and MAU-sensitive economics — the committed user pays and refers, but the base itself can swing (bsp-424b4 ~L2689, ~L2691).

## Where it sits in the machine
Remini sits in the "optimized" lifecycle stage — both filings explicitly group it with Evernote and StreamYard as businesses Bending Spoons continues to optimize after years of ownership, as opposed to the transforming cohort of more recently acquired AOL, Eventbrite, and Vimeo (bsp-f1 ~L134–135, ~L151; bsp-424b4 ~L111, ~L151). Its portfolio role is the consumer-AI, dual-monetization (subscription-led + advertising) node, and the flagship proof of the AI-capabilities thesis: it is the recurring first case study the company reaches for when demonstrating that its Platform can rewrite the codebase, re-monetize, and infuse AI into an acquired product (bsp-424b4 ~L2648; bsp-f1 ~L129). Remini is squarely on the mass-consumer, word-of-mouth side of the portfolio, contrasted in the filings with sales-driven, larger-enterprise businesses such as Brightcove (bsp-f1 ~L431; bsp-424b4 ~L411). It is also a source of reusable capability for the rest of the portfolio: the AI-feature productization/testing tooling built for Remini was subsequently made available across other businesses (bsp-424b4 ~L2670).

## References
- `bsp-f1` — Bending Spoons Form F-1 (captured at sources/2026-06-bsp-f1-fulltext.txt). Remini case study at ~L2656–2698; portfolio/NRR/advertising/organic-growth mentions at ~L375, ~L408, ~L431, ~L1686, ~L1794, ~L1864, ~L1871, ~L1914.
- `bsp-424b4` — Bending Spoons 424B4 final prospectus (captured at sources/2026-07-bsp-424b4-fulltext.txt). Remini case study at ~L2648–2691; portfolio/NRR/advertising/organic-growth mentions at ~L355, ~L388, ~L411, ~L1676, ~L1784, ~L1854, ~L1861, ~L1904.
- Site-only claims not in either filing (100M MAU, marketing-page capability list, "100+ AI models", consumer tier pricing) are marked [to-validate — press only] in the body; `site-remini` is not one of the two official fact sources and has been removed from the node's `sources`.
