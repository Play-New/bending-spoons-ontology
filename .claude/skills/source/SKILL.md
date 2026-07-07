---
name: source
description: Create a new Target in the pipeline (the source verb). Human-gated: admission needs the user's approval.
disable-model-invocation: true
---

Execute the `source` verb of the Bending Spoons world model, per its contract.

1. Read the contract: `capabilities/actions/market-radar.md` — parameters, submission criteria, gate. Follow it exactly.
2. Gather the parameters from the user/context (ask only for what the contract requires and you cannot read
   from the model itself).
3. Propose (phase 1 — writes nothing):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('source', PARAMS), indent=2))"`
   If the engine REFUSES, report the refusal verbatim — it is a submission criterion firing (a will
   constraint or an invariant), not an error to work around.
4. Show the user: the checks, the gate, and the exact diff. Admission into the pipeline is the human gate.
5. Only on the user's explicit yes, apply (phase 2):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; print(engine.apply('PROPOSAL_ID', 'USER_NAME'))"`
   The engine runs the audit and commits if green; report the outcome. Never edit the csvs directly.
