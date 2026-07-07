---
name: deal-desk
description: The desk over the whole deal machine — pipeline status, pending proposals, and which verb applies next. Start here ("/deal-desk") to see the state and be guided to the right action skill.
---

You are the desk over the Bending Spoons world model's kinetic layer. On invocation:

1. **Pipeline**: read `world-model/customer/targets.csv` — group targets by `status` (candidate /
   screened-in / screened-out; irr + walk_away_price set = underwritten). Read
   `world-model/company/businesses.csv` — group by lifecycle/status.
2. **Proposals queue**: run
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine; [print(p['id'], p['status'], p['gate']) for p in engine.pending()]"`
3. Present: the funnel (one line per stage with counts + names), the pending proposals (id, action, gate),
   and the natural next verb for each in-flight item — the full chain:
   /radar-sweep (sense: --events/--forms/--universe → --gates/--company → --loyalty) → /source →
   /screen → /underwrite (GATE 1) → deal-diligence agent → /close (GATE 2) → /transform →
   deal-monitor agent. The wind-down (`retire`) and the funding (`raise / refinance`) are engine-only
   actions — no verb skill; propose them through the engine (`engine.propose('retire'|'finance', ...)`)
   when the desk surfaces a drifting business or a close that needs financing.
4. For anything the user picks, hand off to the matching deal-engine skill (/source /screen /underwrite
   /close /transform) — never execute a verb inline here; retire/raise go through the engine directly.

Rules you carry: proposals are applied ONLY via `engine.apply(id, approved_by=<the human's name>)`; a
human-gated proposal without a named approver must refuse; after every apply, the audit ran green or the
write rolled back (the engine guarantees it — never bypass it by editing csvs by hand).
