---
name: underwrite
description: Underwrite a screened Target to the IRR hurdles and set the walk-away price (GATE 1: the user approves the number).
disable-model-invocation: true
---

Execute the `underwrite` verb of the Bending Spoons world model, per its contract.

1. Read the contract: `capabilities/actions/deal-value.md` — parameters, submission criteria, gate. Follow it exactly.
2. Build the ASSUMPTIONS with the user before any number (the contract's anti-bias rule:
   assumptions are frozen BEFORE the model runs — will.md, deal discipline):
   - 5-yr FCF trajectory attributable to the business (pre-diligence = estimates, say so)
   - terminal value: years 6-10 growth + WACC (current method) or EV/EBITDA at year 5 (legacy)
   - levered case: assumed debt = LOWER of 85% of EV and what 5-yr FCF can repay
   - margin of safety: does the case hold "even under severely unfavorable scenarios"?
   Then compute levered/unlevered IRR and the walk-away price; the engine enforces 65/25.
3. Propose (phase 1 — writes nothing):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('underwrite', PARAMS), indent=2))"`
   If the engine REFUSES, report the refusal verbatim — it is a submission criterion firing (a will
   constraint or an invariant), not an error to work around.
4. Show the user: the checks, the gate, and the exact diff. GATE 1: the walk-away price needs the user's explicit approval by name.
5. Only on the user's explicit yes, apply (phase 2):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; print(engine.apply('PROPOSAL_ID', 'USER_NAME'))"`
   The engine runs the audit and commits if green; report the outcome. Never edit the csvs directly.
