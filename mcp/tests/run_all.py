#!/usr/bin/env python3
"""Run every test suite and print the report. From the repo root:
    python3 mcp/tests/run_all.py [--live]

Write-suites (engine, guards) run in a disposable sandbox copy of the repo; read-suites
(skills/agents, radar, server, audit) run against the working tree. Exit 0 = all green.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = Path(__file__).resolve().parent
LIVE = "--live" in sys.argv

suites = []


def run(name, script, target, extra=()):
    r = subprocess.run([sys.executable, str(TESTS / script), str(target), *extra],
                       capture_output=True, text=True)
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        data = {"pass": 0, "fail": 1, "cases": [("FAIL", f"{name}: suite crashed", (r.stderr or r.stdout)[-300:])]}
    suites.append((name, data))


# sandbox for write-suites (fresh copy per suite so failures don't cascade)
for name, script in [("engine e2e", "test_engine.py"), ("guards", "test_guards.py"),
                     ("mcp e2e (server tools drive the loop)", "test_mcp_e2e.py")]:
    sbx = Path(tempfile.mkdtemp(prefix="bsp-test-")) / "repo"
    shutil.copytree(ROOT, sbx, ignore=shutil.ignore_patterns("proposals"))
    run(name, script, sbx)
    shutil.rmtree(sbx.parent, ignore_errors=True)

if LIVE:
    sbx = Path(tempfile.mkdtemp(prefix="bsp-test-")) / "repo"
    shutil.copytree(ROOT, sbx, ignore=shutil.ignore_patterns("proposals"))
    run("funnel e2e (radar → engine, live)", "test_funnel.py", sbx, ("--live",))
    shutil.rmtree(sbx.parent, ignore_errors=True)

run("skills + agents + workflow", "test_skills_agents.py", ROOT)
run("radar-sweep", "test_radar.py", ROOT, ("--live",) if LIVE else ())
run("mcp server surface", "test_server.py", ROOT)
run("acceptance: try-it.md questions", "test_questions.py", ROOT)

audit = subprocess.run([sys.executable, "mcp/audit.py"], cwd=ROOT, capture_output=True, text=True)
suites.append(("model audit (11 invariants + standing checks)",
               {"pass": 1, "fail": 0, "cases": [("PASS", "audit green", "")]} if audit.returncode == 0
               else {"pass": 0, "fail": 1, "cases": [("FAIL", "audit red", audit.stdout[:300])]}))

# ---- report ----
total_p = sum(s["pass"] for _, s in suites)
total_f = sum(s["fail"] for _, s in suites)
print("=" * 72)
print("TEST REPORT — bending-spoons-ontology")
print("=" * 72)
for name, s in suites:
    flag = "GREEN" if s["fail"] == 0 else "RED"
    print(f"\n[{flag}] {name}: {s['pass']} passed, {s['fail']} failed")
    for status, case, detail in s["cases"]:
        if status == "FAIL":
            print(f"    ✗ {case}  — {detail}")
    if s["fail"] == 0:
        for status, case, detail in s["cases"]:
            print(f"    ✓ {case}")
print("\n" + "=" * 72)
print(f"TOTAL: {total_p} passed, {total_f} failed → {'ALL GREEN' if total_f == 0 else 'FAILURES PRESENT'}")
print("=" * 72)
sys.exit(1 if total_f else 0)
