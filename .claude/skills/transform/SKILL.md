---
name: transform
description: Apply transformation levers to a Business and its Interfaces (the transform verb; human-gated — it changes a live business).
disable-model-invocation: true
---

Execute the `transform` verb of the Bending Spoons world model, per its contract.

1. Read the contract: `capabilities/actions/deal-optimize.md` — parameters, submission criteria, gate. Follow it exactly.
2. Gather the parameters from the user/context (ask only for what the contract requires and you cannot read
   from the model itself).
   The five levers write BOTH types: reorganize/re-tech/monetize → Business; redesign-UI/AI-features
   (and sunsets) → Interface. Check the boundary rule: ARPU up on falling subscribers is price
   extraction — deal-monitor will surface it.
3. Propose (phase 1 — writes nothing):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('transform', PARAMS), indent=2))"`
   If the engine REFUSES, report the refusal verbatim — it is a submission criterion firing (a will
   constraint or an invariant), not an error to work around.
4. Show the user: the checks, the gate, and the exact diff. Human-gated: it changes a live business; check the boundary rule (no price extraction dressed as value).
5. Only on the user's explicit yes, apply (phase 2):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; print(engine.apply('PROPOSAL_ID', 'USER_NAME'))"`
   The engine runs the audit and commits if green; report the outcome. Never edit the csvs directly.
