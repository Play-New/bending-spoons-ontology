---
id: capability-talent
type: action
title: Talent — the Platform's transactions on Spooners
status: confirmed
purpose: the three people-verbs — hire, assemble task-force, reallocate — that grow and move the durable core across the portfolio
provenance: reflection
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: advisory-in-v1
relations:
  - { type: uses, target: role-model, cardinality: 1:1, confidence: high, source: bsp-f1, status: confirmed }
visibility: shared
---
# Capability — talent (the people-verbs)

**Advisory in v1 (no engine write-back).** The contract below specifies the people-verbs, but the engine
does **not** commit them: the filings disclose only *aggregate* `Spooners` data (headcount, share of FTE),
no per-person facts — so writing a per-person `Spooners` record would manufacture ungrounded data (rule 4). The
transaction block is therefore the *specified* write-back, executed by hand against the aggregate node;
`../../mcp/engine.py` `_talent` refuses to commit. The runnable, grounded slice — a candidate scored against the
disclosed selection gates (`../../sources/hiring/`) — is the hiring assistant, human-gated, read-only.

The Platform's own transactions: the machine's durable input is the reallocatable Spooner core (`../../world-model/company/spooners.md`), grown by an extreme hiring funnel and moved across the portfolio on short notice. One contract backs the three §2 people-verbs — they share parameters, backing, and gate.

```
action: hire                        # + `assemble task-force` + `reallocate talent` (../../ontology.md §2)
parameters:
  - role / need       # what the portfolio needs: a new Spooner, or a task-force on a Business
  - candidate | spooner | business  # per verb: who is hired, who is moved, onto what
logic: the talent machine (skill)   # the funnel is codified — Role Model, the recruiting technology
                                    # that supports the Talent team end to end, backs assessment
                                    # (bsp-f1 ~L2556); the talent team
                                    # (55 Spooners, ~9%, ~L2457) runs it; placement is human judgment
transaction — what it commits (write-back: the Spooners node's properties; no per-person dataset —
                                the filing discloses aggregates only):
  create: Spooners     # `hire` — grow the durable core: ~800,000 applications in 2025, 286 hired,
                      # <0.04% acceptance (bsp-f1 ~L284); updates Spooners.headcount / share-of-FTE
  link:   Spooners —deployed-on→ Business   # `assemble task-force` — onto a fresh acquisition
                      # (declared once, on Spooner, §1; e.g. ~30 FTE initially allocated to Remini, ~L2669)
  modify: that link   # `reallocate talent` — move Spooners across the portfolio as returns shift
                      # ("transferred between businesses on short notice", ~L293; Remini 30 → 64 → ~20
                      #  FTE as returns diminished, ~L2669-2673)
submission criteria:
  - hire only into the Spooner core (high-potential, major responsibility early, ~L159); the acquired
    staff is NOT hired this way — it is transitioned out by `reorganize` (deal-optimize)
  - keep the org flat: no more than three managerial layers CEO → IC (a will constraint, ../../will.md)
governance:
  - approval: HUMAN — hiring and placement decisions stay with the talent team and DRIs [decision]
side-effects:
  - a task-force assembled on a new Business hands the transformation to deal-optimize
  - reallocation frees capacity that market-radar's next close will consume (the flywheel's people-side)
backing:
  - node: ../../world-model/company/spooners.md (headcount · share-of-FTE · talent-team size · redeployability)
  - tool: Role Model (../../world-model/company/tools/role-model.md) — produces→Spooners
  - runtime: skill — advisory in v1 (the engine does not commit this; see the note above)
```

## References
- `bsp-f1` — the hiring funnel (~800k applications, 286 hired, <0.04%, ~L284); the talent team (55, ~L2457); redeployability on short notice (~L293); the Remini allocation curve 30→64→~20 FTE (~L2669-2673); hire-young doctrine (~L159); flat-org constraint (~L2519).
