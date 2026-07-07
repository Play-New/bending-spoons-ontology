---
id: cross-product-graph
type: gap
title: The cross-product customer graph — the unbuilt moat
status: proposed
purpose: name the single biggest thing the customer world model does NOT capture — and the largest opportunity
provenance: reflection
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
relations:
visibility: shared
---
# The cross-product customer graph — the unbuilt moat

**Properties: none — deliberately.** This is the model's one **anti-object** (the declared exception, `../../CLAUDE.md` rule 1): it types an *absence*, so it carries no property values — its entire content is the **evidence of absence** below, each item cited. The object it is the absence *of* is the `CustomerGraph` of the analysis (`../../bending-spoons-as-an-intelligence.md §3`), where the properties (coverage · resolution quality · cross-product LTV & retention) become declarable.
**Links:** none — a gap links to nothing; when something links to it, it has stopped being a gap.

`[decision]` This is a first-class **gap object**: the most important thing the customer world model could hold and today does not. Modeled here because, in this architecture, the gap the intelligence layer cannot yet compose *is* the roadmap.

## The evidence that it is unbuilt
Bending Spoons serves over 500M monthly active users (March 2026, `bsp-f1` ~L172), but it does not have a single **Person** it can recognize across products:
- **No de-duplication.** MAU and paying-customer figures are explicit non-deduplicated sums across products; the F-1 states it does "not have a reliable method of de-duplication" and that "the aggregated monthly active user figure may count the same user more than once" (`bsp-f1` ~L186). The same limit is repeated for tenure — a customer transacting across products has "a separate customer identifier" per product, so the relationship length "may in some cases underestimate" the truth (`bsp-f1` ~L422). A user of Evernote and WeTransfer is two rows, not one person.
- **No single sign-on / unified account.** Searched the filing: no single sign-on, no unified account, no shared identity across products (terms absent from the F-1).
- **Network effects are intra-product only.** The F-1 locates network effects *inside* a product — "Eventbrite's organizer-attendee and WeTransfer's sender-recipient dynamics" (`bsp-f1` ~L2851) — never *between* products. The one cross-product tie the filing names as an *asset* is a data mechanism, not an identity one: Minerva, the AI lifetime-value predictor, was "enhanced… to leverage data from other products to generate insights for newly acquired businesses" (`bsp-f1` ~L1775/~L2541). That moves signal between products for underwriting and monetization, but it is not a per-person graph — it does not reconcile the same human across products. The other cross-product tie is a *risk*, not an asset: reputational spillover — "harm to the reputation of one product can adversely affect the perception and performance of our other products," because products share the Bending Spoons brand (`bsp-f1` ~L660-661).

## Why it is the unbuilt moat
The org contract (`../../foundations/org-as-an-intelligence.md` §2) describes exactly this moat, built by companies that see both sides of their transactions: a per-customer understanding that compounds — one graph, one customer, richer every transaction. Bending Spoons instead holds **silos**: it knows the committed archive-keeper of Evernote and the professional sender of WeTransfer in depth, but cannot see that they may be the same person and cannot cross-sell on identified behavior. It moves *aggregate* signal across products for underwriting (Minerva, above), but not *per-person* signal — there is no reconciled customer. Its glue is the Platform + capital + fungible talent, **not** a unified customer graph.

A cross-product customer graph would convert 500M **product** users into one **Bending Spoons** customer world model — the compounding, per-person financial-and-behavioral understanding that is the durable data moat. It would also change the model's economics: cross-product retention and lifetime, not just per-product NRR.

## Status and caveat
`status: proposed` — this is a modeled opportunity/gap, not a stated Bending Spoons initiative. The F-1 shows no such graph and names no plan to build one. The closest existing mechanism, AOL's Membership Services, does personalize — "the scaled user base coupled with personalization efforts creates a powerful opportunity for the Membership Services to contextually introduce the best offer to the right user at the right time" (`bsp-f1` ~L5493) — but this is internal to the AOL business (its GSS platform powers subscription management for AOL and its parent's products only, `bsp-f1` ~L5496), not a portfolio-wide mechanism. Whether Bending intends to build a portfolio-wide graph is unknown from the filing.

## References
- `bsp-f1` — the non-deduplication caveat (~L186/~L422), the intra-product network-effect language (~L2851), the reputational-spillover risk (~L660-661), the Minerva cross-product data mechanism (~L1775/~L2541), and AOL's Membership Services personalization (~L5493/~L5496).
