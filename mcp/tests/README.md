# Tests — how to run

From the repo root:

    python3 mcp/tests/run_all.py            # full suite (offline)
    python3 mcp/tests/run_all.py --live     # + live radar-sweep smoke (network)

Suites (write-suites run in a disposable sandbox copy — the working tree is never touched):
- **engine e2e** — the full deal lifecycle (source→screen→underwrite→close→transform→retire→finance)
  plus every contractual refusal path; asserts rows, node stubs, node↔csv 1:1, one git commit per
  applied action with the approver recorded, audit green at the end.
- **guards** — adversarial: rollback on red audit (byte-identical files after a failed apply),
  gate bypass, double-apply, tampered proposals, file-overwrite attempts.
- **skills + agents + workflow** — every skill: frontmatter, explicit-only flags on the verb skills,
  referenced paths exist, verb exists in the engine, stated gate matches the engine gate, bundled
  scripts run; every agent: structurally read-only tool set; the workflow: meta + phases.
- **radar-sweep** — the bucketing brain offline (signal classification, ranking, multi-signal);
  `--live` adds HN reachability + exact-phrase relevance.
- **mcp server surface** — 27 tools registered (query · engine · radar · hire · audit), readOnly/destructive annotations, apply_action
  async + Context + elicitation wiring, no stale folder names in tool descriptions.
- **model audit** — the 11 invariants + standing checks (mcp/audit.py).

Per defect-to-test (the repo's discipline): any defect found by hand becomes a new case here.
