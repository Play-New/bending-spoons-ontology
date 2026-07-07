---
id: capability-deal-optimize
type: action
title: Optimize — apply the transformation playbook
status: confirmed
purpose: turn an acquired business into an optimized one by applying the Playbook's transformation levers
provenance: upload
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: invocable-tool
relations:
  - { type: uses, target: platform, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — optimize (the transformation playbook, runnable)

Step 2 of the Playbook made into a plan. The F-1 states the transformation as **five actions, verbatim**: "reorganizing teams, overhauling technology, redesigning user interfaces, accelerating product development, and enhancing marketing and monetization" (`bsp-f1` ~L273), "typically completed within the first year following closing" (~L2646).

```
action: transform                   # the ontology verb (../../ontology.md §2); this skill also backs
                                    # `run experiment` and `reorganize` — they modify the Business and its Interfaces
parameters:
  - business          # an acquired Business (created at close) and its Interface(s)
  - baseline          # its financials + user metrics at close (the businesses.csv row)
logic: the Playbook (skill)         # the five levers are fixed (the F-1 states them verbatim); what is
                                    # planned per lever, per product, is human judgment — the logic
                                    # produces a transformation plan with an owner (DRI) and expected
                                    # impact per lever, then the transaction applies it
transaction — what it commits (write-back: businesses.csv + interfaces.csv + their nodes), the five levers:
  modify: Business    # 1. reorganize teams — the acquired staff transitioned out, management layers
                      #    flattened (e.g. Evernote FTEs 341 -> 60, an 82% cut, and 4 -> 2 management
                      #    layers, bsp-f1 ~L2715-2716); the `reorganize` verb of §2
                      # 2. overhaul technology — migrate onto the Platform: people + proprietary
                      #    technologies + data (bsp-f1 ~L266,~L280); Juno for payments (bsp-f1 ~L2543)
                      # 3. redesign user interfaces
                      # 4. accelerate product development (AI-authored PRs <10% in
                      #    Q1 2025 -> >90% by end of Q1 2026, ~70% by AI alone, bsp-f1 ~L141); the ai_features
                      #    WRITE lands on the Interface (below), not here
                      # 5. enhance marketing and monetization — sets arpu · conversion rate ·
                      #    organic_channel_pct · adj_op_margin_pct · status (main / tail):
                      #    Minerva LTV-driven pricing (bsp-f1 ~L2539), tier/plan changes (free↔paid)
  modify: Interface   # levers 3-4 write the INTERFACE: redesigned UI · ai_features shipped · status
                      # (live → sunset — an interface can be wound down while its business lives, e.g.
                      #  Mosaic's surviving utility apps vs its sunset ones)
  modify: Business/Interface # `run experiment` — pricing & UX variants chosen, A/B at scale via Janus/Orion
                      # (bsp-f1 ~L2550) — e.g. >200 experiments 2023-25 (~L2750)
  modify: Business    # completion moves Business.lifecycle: acquired → transforming → optimized
                      # (typically within the first year following closing, ~L2646)
  link: (none here)   # the task-force onto the business — Spooners —deployed-on→ Business — is written
                      # by the platform's assemble/reallocate actions, not by this one (declared once)
submission criteria:
  - abort a monetization move that is price extraction dressed as value — the pattern the F-1's own
    per-business notes make visible: revenue up on higher revenue-per-subscriber against a falling
    subscriber count (Evernote bsp-f1 ~L1865; Issuu ~L1872) [decision: the boundary rule is ours,
    derived from that disclosed pattern]
  - the transformation is typically completed within the first year following closing (bsp-f1 ~L2646)
governance:
  - approval: HUMAN — it changes a live business and acts on real users [decision]
side-effects:
  - separation packages + retention bonuses booked as recurring cost lines (bsp-f1 ~L1882,~L1883,~L1917,~L1846)
  - each experiment's outcome is emitted as signal; the resulting improvement of Platform/Tools is the
    flywheel-② READING of ../../ontology.md §3 — a dynamic the model observes, committed by no edit here
  - deal-monitor (../functions/deal-monitor.md) reads the transformed business against its underwriting
backing:
  - datasets: ../../world-model/company/businesses.csv · ../../interfaces/interfaces.csv (+ their nodes)
  - tools: Juno (payments, ~L2543) · Minerva (LTV pricing, ~L2539) · Janus/Orion (experiments, ~L2550)
  - runtime: skill — exposed by the MCP as an invocable tool
```

The caution belongs inside this capability: lever 5 can lift short-term revenue by pruning the tail and raising ARPU on the committed base, which is real, but some of the resulting "organic" growth is price extraction, not new demand — the F-1's own per-business notes show revenue rising on higher revenue-per-subscriber against a *falling* subscriber count (Evernote, `bsp-f1` ~L1865; Issuu, ~L1872) — `deal-monitor` and `../functions/product-users.md` keep that visible. Target after transformation: the consolidated adjusted operating income margin the machine is known for (36% in 2023 → 51% in Q1 2026, `bsp-f1` ~L529). Cost discipline shows up too: at StreamYard, IT infrastructure expense as a percentage of revenue fell 65% in 2025 vs 2023, its last full pre-acquisition year (`bsp-f1` ~L2778 — a per-business showcase, not a company-wide figure).

Reorganization (lever 1) is a recurring F-1 cost line — separation packages for the reorganizations of Issuu, Meetup, StreamYard, WeTransfer (2024); Brightcove, Harvest, komoot, Loomly, MileIQ, WeTransfer (2025); AOL, Eventbrite, Vimeo (Q1 2026), with retention bonuses for the team members kept through the transition (`bsp-f1` ~L1882, ~L1883, ~L1917, ~L1846).

## References
- `bsp-f1` — the five-lever transformation sentence (~L273), the within-a-year completion (~L2646), the AI-authored-PR figure (~L141), the adjusted operating income margin trajectory (~L529), the Evernote org rebuild (~L2714-2716), Juno/Minerva/Janus/Orion (~L2539,~L2543,~L2550), IT-infra cost cut (~L2778).
