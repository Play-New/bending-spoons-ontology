---
id: service-audit
type: service-tool
title: Audit — the cross-cutting validator
status: confirmed
purpose: enforce the model's integrity; a service tool of the model, not a capability of Bending Spoons
provenance: reflection
as_of: 2026-03-31        # period of the underlying data (Q1 2026; later events cited in prose)
last_synced: 2026-07-04  # last verified against sources/
sources: [bsp-f1]
runtime: skill
mcp: invocable-tool
relations:
visibility: shared
---
# Service tool — audit (the model's validator)

A deterministic cross-cutting check on THIS REPO. It is not one of Bending Spoons' capabilities (Bending Spoons audits deals, not this model) — it lives with the MCP because it guards the model the MCP serves. `audit.py` (this directory) is its runnable form; the `bsp-audit` skill and the `bsp-control-pass` workflow invoke it.

```
function: audit                     # the enforcer of the contract (../foundations/ontology.md §5-§6)
input:
  - scope             # a node, a contract, a backing dataset, or the whole model
computation — the §5 invariants, checked 1:1 (a §5 invariant with no check here is itself a defect):
   1. every contract verb ↔ ontology.md §2, declared once, same transaction, checked BOTH ways;
      a §2 row marked "contract pending" commits nothing
   2. every property a transaction writes is declared in §1 and is a backing-dataset column (1:1);
      statically, a node's properties are exactly §1's for its type
   3. every link a transaction writes is declared once in §1, object↔object, declared direction
   4. only an action carries a transaction; a function that writes is a defect
   5. no edit hides in side-effects — a side-effect naming a state change names its committing action
   6. every gate, rule, and figure cites its source (~L into sources/, will.md, or [decision])
   7. the runtime (skill/agent) changes only the logic — never the transaction or its gates
   8. provenance travels with every fact, markers with every inference; weakest marker wins
      in any reading (press-only is never laundered into an unmarked derived figure)
   9. provenance of edit: every csv row / node value is attributable to a declared action's
      transaction — a hand-added row with a resolving citation is still corruption
  10. a type:function node carries exactly input·computation·output and no write verb
  11. freshness — every node carries the two clocks (as_of + last_synced); an edit that changes
      facts must update last_synced; as_of advances only with a newer source period
  plus the standing checks born from real defects (defect-to-test — each was first found by hand):
  - no figure the source does not support; no disclosed fact negated (the two original defects, below)
  - prose numbers reconcile with the csvs; period labels agree with the source
  - official-source policy: no news/third-party analysis presented as filing fact
  - no framework vocabulary or author names in model files — including paraphrases
    (a leak this model already hit: a framework concept rephrased into the nodes;
     epistemic status is expressed by markers, never by rhetoric)
  - every relation target resolves; every relative path resolves at its depth
  - csv rows parse: no unquoted commas shifting columns
output: a defect list with severity + minimal fix (read-only, auto to run); per defect-to-test,
  a recurring manual finding becomes a new standing check in this list
```

This is where the real defects this model already hit become permanent guards. The two originals: (1) a disclosed deal price negated as "not disclosed" (WeTransfer $476.3M, `bsp-f1` ~L4943; Tractive $781M at closing plus $119M deferred consideration payable one year after closing, `bsp-f1` ~L4599), and (2) numbers invented and attributed to the F-1 (the AOL enterprise/MAU figures — the filing gives no such AOL-specific figures; it discloses only portfolio-level MAU/paying-customer counts, `bsp-f1` ~L361-362). Later reviews added four more, now standing: framework vocabulary leaked in paraphrase; a relative path that resolved at the wrong depth; an unquoted comma shifting a targets.csv row; properties written by actions but undeclared in §1/backing. The audit exists so none recurs.

## References
- `bsp-f1` — the standard every claim in this model is checked against.
