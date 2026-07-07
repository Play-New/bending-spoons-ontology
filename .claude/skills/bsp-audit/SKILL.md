---
name: bsp-audit
description: Run the model's audit (the model's audit service, mechanical subset) and summarize — green/red, defects with the invariant each violates. Run after any batch of edits.
---

1. From the repo root run: `python3 mcp/audit.py`
2. If GREEN: say so, one line.
3. If RED: list each defect, name the §5 invariant it violates (read
   `mcp/audit-contract.md` for the mapping), and propose the minimal fix — but per
   defect-to-test, also ask: should this defect class become a new standing check in `mcp/audit.py`?
