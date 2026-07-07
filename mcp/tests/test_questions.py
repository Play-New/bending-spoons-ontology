"""Acceptance: run the documented try-it.md questions against the LIVE tools and assert each
returns a sane, on-topic answer — so the question bank can never quietly start lying (a client
following docs/try-it.md must get what the doc promises). Read-only; runs on the real repo.

python3 test_questions.py <repo_root>.

Offline tiers only (query · capability · agent · hire · audit). The radar_* tier is network-bound
and is exercised live by test_funnel / test_radar; here we only assert its docstrings route intent
(mirrored in test_server). Defect-to-test: born from a Desktop session where a client hit a wrong
tool and an over-strict gate that no acceptance test had caught.
"""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "mcp"))
import server  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def ask(label, thunk, must_contain):
    """Run one documented question; PASS iff it returns text containing every expected marker."""
    try:
        out = thunk() or ""
    except Exception as e:  # a question in the bank must never crash the tool
        R["fail"] += 1
        R["cases"].append(("FAIL", f"Q: {label}", f"raised {type(e).__name__}: {e}"[:160]))
        return
    missing = [m for m in must_contain if m.lower() not in out.lower()]
    ok = bool(out.strip()) and not missing
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", f"Q: {label}",
                       "" if ok else (f"missing {missing}" if out.strip() else "EMPTY")))


# ---- §1 understand the company (query tier) ----
ask("What is Bending Spoons / this repo?", server.overview, ["Bending Spoons", "portfolio"])
ask("Show me the whole portfolio", lambda: server.list_nodes(type="business"),
    ["evernote", "wetransfer", "vimeo", "aol"])
ask("What does it refuse to do?", server.will, ["never sell", "margin of safety"])
ask("Search 'margin of safety'", lambda: server.search("margin of safety"), ["will.md"])
ask("What's the NRR across businesses?", lambda: server.search("NRR"), ["AOL"])
ask("The modeling foundations", server.foundations, ["semantic"])
ask("The value-migration thesis", server.analysis, ["cross-product"])
ask("The ontology index", server.ontology, ["object"])

# ---- §2 the capabilities (the differentiated tier) — every one must resolve AND be listed ----
CAPS = {
    "market-radar": ["continuous", "discovery"],
    "screen-target": ["gate"],
    "deal-value": ["IRR", "walk-away"],
    "deal-diligence": ["assumption"],
    "deal-optimize": ["transform"],
    "talent": ["Spooner"],
    "retire": ["never-sell", "wind"],
    "finance": ["refinance", "covenant"],
    "capital-allocation": ["flywheel"],
    "deal-monitor": ["underwrit"],
    "portfolio-impermanence": ["impermanent"],
    "product-users": ["paying"],
}
listed = server.list_capabilities()
ask("List its capabilities", server.list_capabilities, ["actions/", "functions/"])
for name, markers in CAPS.items():
    ask(f"get_capability('{name}')", (lambda n=name: server.get_capability(n)), ["title:"] + markers)
    ok = f"{name}.md" in listed
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", f"capability listed: {name}", "" if ok else "not in list_capabilities"))

# ---- agentic skills ----
ask("Turn on the portfolio-monitor loop", lambda: server.activate_agent("deal-monitor"),
    ["monitor", "agent"])
ask("Assess this candidate (hire)", lambda: server.hire("Jane Doe — ex-Stripe eng, led payments reliability"),
    ["problem-solving", "committee"])
ask("hire refuses to be the decider", lambda: server.hire("pick the best for me"),
    ["AI ACT", "DECLINE the decision"])

# ---- §6 check the model ----
ask("Run the audit", server.run_audit, ["AUDIT GREEN"])
ask("Where does every fact come from?", server.list_sources, ["bsp-f1", "bsp-selection-process"])
ask("Show the hiring selection doc", lambda: server.get_source("bsp-selection-process"), ["# Source"])

# ---- discovery routing (the Desktop failures), asserted offline via docstrings ----
uni = (server.radar_universe.__doc__ or "").lower()
ask("'find in-band listed companies in Italy' routes to radar_universe (name-free discovery)",
    lambda: uni, ["find", "region='eu'"])
disc = (server.radar_discover.__doc__ or "").lower()
ask("'find US targets, screen them' routes to radar_discover (run the search → screened names out)",
    lambda: disc, ["run the search", "names out"])

print(json.dumps(R))
