---
id: juno
type: tool
title: Juno — payments and subscription system
status: confirmed
purpose: take over an acquired business's billing and subscription responsibilities with minimal friction, unlocking monetization control from day one
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: platform-primitive
mcp: invocable-tool
relations:
  - { type: part-of, target: platform, cardinality: N:1, confidence: high, source: bsp-f1, status: confirmed }
  - { type: deployed-across, target: business, cardinality: 1:N, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Juno

**Properties** (per `../../../ontology.md` §1 `Tool`): function — payments & subscription system · built 2023 · usage — checkout, subscriptions, pricing, invoicing, experimentation · AI-based — (data integration) · deployed-across-portfolio — yes.
**Links:** `part-of`→Platform · `deployed-across`→Business.

The monetization rails. Juno is the system for managing payments: checkout flows, subscriptions, price changes, promotional codes, billing retries, invoicing, and experimentation — enabling more efficient monetization at lower cost (`bsp-f1` ~L2543-2544). It is the primitive that turns a transformation lever (repricing, tier changes, one-time→subscription) into something that actually bills.

```
primitive: juno
does:
  - run checkout, subscriptions, price changes, promo codes, billing retries, invoicing, experimentation
  - on acquiring a business, TAKE OVER its subscription responsibilities — other than core
    payment processing — from third-party providers "with minimal friction"
  - integrate payment data from the Apple App Store and Google Play Store
migration: enhanced migration functionality is what makes the takeover low-friction; the payoff
           is cost optimization AND greater control over the customer experience
built: 2023 (initial focus web-based electronic payments; expanded since)
```

How the intelligence layer composes it: when a deal closes, Juno is deployed to assume the target's billing so the machine can immediately run pricing and packaging experiments through `janus-orion`, priced against the value `minerva` predicts. It is the concrete mechanism behind "the day an acquisition closes it can run monetization it could not before" (`../platform.md`).

## References
- `bsp-f1` — Juno is a system for managing payments (checkout, subscriptions, price changes, promo codes, billing retries, invoicing, experimentation); built in 2023 with initial focus on web-based electronic payments; expanded to integrate App Store / Play Store payment data; enhanced migration lets Bending Spoons transition key subscription responsibilities (other than core payment processing) from third-party providers to Juno with minimal friction, enabling cost optimization and greater control over the customer experience (~L2543-2547).
