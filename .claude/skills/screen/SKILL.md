---
name: screen
description: Screen a Target against the hard gates (the screen verb). Applies auto — the write IS the screen.
disable-model-invocation: true
---

Execute the `screen` verb of the Bending Spoons world model, per its contract.

1. Read the contract: `capabilities/actions/screen-target.md` — parameters, submission criteria, gate. Follow it exactly.
2. ESTIMATE THE GATES with the radar's structured tiers before asking the user anything:
   - US-listed candidate → `python3 .claude/skills/radar-sweep/scripts/radar_sweep.py "TKR" --gates`
     (revenue band · HQ · sector, [derived] from EDGAR)
   - EU-listed / unknown → `... "Legal Name" --company` (GLEIF → ESEF chain; honest n.d. for privates)
   - private → the press recipes in the radar-sweep skill (triangulate ≥2 sources; everything
     [to-validate — press only]) + `--loyalty "Brand"` as the predictable-earnings proxy
     (rating base · interest trend · community)
   Fill the nine gate values from these, marked by provenance; ask the user only for what remains.
3. Propose (phase 1 — writes nothing):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('screen', PARAMS), indent=2))"`
   If the engine REFUSES, report the refusal verbatim — it is a submission criterion firing (a will
   constraint or an invariant), not an error to work around.
4. Show the user: the checks, the gate, and the exact diff. screen applies auto (no approver needed): the write is the screen itself; admission to underwriting stays human.
5. Only on the user's explicit yes, apply (phase 2):
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; print(engine.apply('PROPOSAL_ID', 'USER_NAME'))"`
   The engine runs the audit and commits if green; report the outcome. Never edit the csvs directly.
