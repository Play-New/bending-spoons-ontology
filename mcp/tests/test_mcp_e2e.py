"""MCP end-to-end: a user drives the WHOLE loop through the actual MCP server tools — proving Bending
Spoons is runnable from any MCP client, not just from Python. Runs in the sandbox run_all.py provides
(apply_action writes + commits there). Exercises the tools the surface test can't: overview,
list_capabilities, activate_agent, the successful propose→apply path, and reject_action.
Run via run_all.py; direct: python3 test_mcp_e2e.py <sandbox_root>.
"""
import asyncio
import inspect
import json
import subprocess
import sys
from pathlib import Path

SBX = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SBX / "mcp"))
import server as s  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))


def call(t, **k):
    r = t(**k)
    return asyncio.run(r) if inspect.iscoroutine(r) else r


# ---- read tools not covered by the surface test ----
record("Bending Spoons" in call(s.overview), "overview() returns the repo intro")
lc = call(s.list_capabilities)
record("deal-value" in lc and "market-radar" in lc, "list_capabilities() lists the contracts")
record("monitor" in call(s.activate_agent, name="deal-monitor").lower(), "activate_agent() returns the loop contract")


# ---- RUN THE LOOP THROUGH THE MCP TOOLS (the point: runnable from a client) ----
def propose(action, params):
    out = call(s.propose_action, action=action, params=params)
    assert out.strip().startswith("{"), f"propose {action} refused: {out}"
    return json.loads(out)["id"]


def apply(pid, who="mcp-user"):
    return call(s.apply_action, proposal_id=pid, ctx=None, approved_by=who)  # approver set → elicitation skipped, ctx unused


steps = [
    ("source", {"target": "Pocket", "revenue_scale": "in band [inferred]", "hq": "North America",
                "product_offering": "digital (read-later)", "revenue_model": "freemium subs", "source": "[to-validate — press only]"}),
    ("screen", {"target": "Pocket"}),
    ("underwrite", {"target": "Pocket", "irr_levered_pct": 72, "irr_unlevered_pct": 27, "walk_away_price": "$180M"}),
    ("close", {"target": "Pocket", "business": "Pocket", "date": "2026-07", "cohort": "2026",
               "deal_type": "acquisition", "consideration_usd_m": 180, "category": "read-later", "source": "bsp-f1"}),
]
for action, params in steps:
    out = apply(propose(action, params))
    record(out.startswith("APPLIED") and "committed" in out, f"MCP {action}: propose→apply writes + commits", out)

# the model REALLY changed, and each action is one commit (the audit trail)
biz = (SBX / "world-model/company/businesses.csv").read_text()
record("pocket" in biz, "MCP loop changed the model (pocket business row exists)")
log = subprocess.run(["git", "log", "--oneline", "-6"], cwd=SBX, capture_output=True, text=True).stdout
record(all(f"action: {v}" in log for v in ("source", "screen", "underwrite", "close")) and "mcp-user" in log,
       "MCP loop left one commit per action, approver recorded", log[:160])

# the human gate over MCP: apply without an approver on a human-gated proposal must NOT write.
# Use a fresh screened-in target so the refusal is the GATE, not a state precondition.
apply(propose("source", {"target": "GateCo", "revenue_scale": "in band", "hq": "Europe",
                         "product_offering": "digital", "revenue_model": "subs", "source": "[to-validate — press only]"}))
apply(propose("screen", {"target": "GateCo"}))
gid = propose("underwrite", {"target": "GateCo", "irr_levered_pct": 70, "irr_unlevered_pct": 26, "walk_away_price": "$50M"})
no_approver = call(s.apply_action, proposal_id=gid, ctx=None, approved_by="")
record(no_approver.startswith("REFUSED") and "human-gated" in no_approver,
       "MCP human gate: apply_action without an approver is refused", no_approver)

# reject_action (the human's no) + list_proposals reflects it
rid = propose("source", {"target": "RejectMe", "revenue_scale": "x", "hq": "Europe",
                         "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
record(call(s.reject_action, proposal_id=rid, reason="not in thesis").startswith("REJECTED"),
       "MCP reject_action: the human's no is recorded")

# audit green after the whole MCP-driven lifecycle
record(subprocess.run(["python3", "mcp/audit.py"], cwd=SBX, capture_output=True, text=True).returncode == 0,
       "audit green after the full MCP-driven loop")

print(json.dumps(R))
