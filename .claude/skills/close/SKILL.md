---
name: close
description: Close an acquisition: create the Deal + Business + Interface(s) (GATE 2: go/no-go is the user's).
disable-model-invocation: true
---

Execute the `close` verb of the Bending Spoons world model, per its contract.

1. Read the contract: `capabilities/actions/deal-diligence.md` — parameters, submission criteria, gate. Follow it exactly.
2. Gather the parameters from the user/context (ask only for what the contract requires and you cannot read
   from the model itself).
   Before proposing, prefer running the deal-diligence agent (it ranks and verifies the assumptions
   behind the approved walk-away price and drafts the exact close params).
3. Propose (phase 1 — writes nothing):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('close', PARAMS), indent=2))"`
   If the engine REFUSES, report the refusal verbatim — it is a submission criterion firing (a will
   constraint or an invariant), not an error to work around.
4. Show the user: the checks, the gate, and the exact diff. GATE 2: the go/no-go is the user's; consider running the deal-diligence agent first.
5. Only on the user's explicit yes, apply (phase 2):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; print(engine.apply('PROPOSAL_ID', 'USER_NAME'))"`
   The engine runs the audit and commits if green; report the outcome. Never edit the csvs directly.
