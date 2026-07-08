"""The full funnel, end to end: radar senses -> human-shaped params -> engine proposes ->
gate -> apply -> screen. Needs network + a sandbox; run via run_all.py with --live.
python3 test_funnel.py <sandbox_root> [--live]
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

SBX = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SBX / "mcp"))
import engine  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))


if "--live" not in sys.argv:
    record(True, "funnel e2e skipped (offline)")
    print(json.dumps(R))
    sys.exit(0)

spec = importlib.util.spec_from_file_location(
    "radar_sweep", SBX / ".claude/skills/radar-sweep/scripts/radar_sweep.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)
cfg = radar.load_thesis(SBX / ".claude/skills/radar-sweep/theses/bending-spoons.yaml")

# 1. SENSE: chatter sweep on a real brand
buckets = radar.sweep("Bandcamp", 60, 25, cfg)
sc, fired = radar.maturity(buckets, 60, cfg)
record(isinstance(sc, float), f"radar: sweep+maturity ran (score {sc}, fired {fired})")

# 2. graceful CLI guards (the round-2 regressions)
run = lambda *args: subprocess.run(
    [sys.executable, str(SBX / ".claude/skills/radar-sweep/scripts/radar_sweep.py"), *args],
    capture_output=True, text=True)
r = run("Xyzzy Nonexistent App", "--interest")
record("no Wikipedia article" in r.stdout, "regression: interest 404 graceful")
r = run("x", "--thesis", "/tmp/definitely-missing.yaml")
record(r.returncode == 2 and "not found" in r.stdout, "regression: missing thesis graceful exit 2")
r = run("Xyzzy Nonexistent", "--appstore")
record("no apps found" in r.stdout, "regression: empty appstore message")
if os.environ.get("RADAR_CONTACT"):  # EDGAR 403s without a contact; guard exactly as the radar suite does
    try:
        g = radar.gates("BRK.B", cfg)
        record("error" not in g, "regression: dotted ticker normalized (BRK.B -> BRK-B)")
    except Exception as e:
        record(False, "regression: dotted ticker", e)
else:
    record(True, "regression: dotted ticker skipped (RADAR_CONTACT not set)")

# 3. HANDOFF: radar output becomes a source proposal in the engine (human-shaped params)
prop = engine.propose("source", {
    "target": "FunnelCo", "revenue_scale": "in band [inferred]", "hq": "North America",
    "product_offering": "digital (consumer)", "revenue_model": "self-serve subscriptions",
    "source": "[to-validate — press only]",
    "note": f"radar maturity {sc}; signals: {', '.join(fired) or 'none'}"})
record(prop["gate"] == "human", "engine: source proposal is human-gated")
engine.apply(prop["id"], "funnel-test-human")
p2 = engine.propose("screen", {"target": "FunnelCo"})
engine.apply(p2["id"])
audit = subprocess.run([sys.executable, "mcp/audit.py"], cwd=SBX, capture_output=True, text=True)
record(audit.returncode == 0, "funnel: audit green after radar→source→screen")

# 4. MCP-NATIVE: the scouting/hire/audit tier is drivable as MCP tools (the whole loop from any client)
try:
    import server as _srv  # noqa: E402  (SBX/mcp is on sys.path)
    co = _srv.radar_company("Ubisoft Entertainment")  # GLEIF→ESEF, keyless, real network result
    record("lei" in co.lower() and ("FR" in co or "country" in co.lower()),
           f"MCP radar_company returns real data (Ubisoft): {co[:70]}")
    hk = _srv.hire("Test candidate, strong CV")
    record("problem-solving" in hk and "committee" in hk, "MCP hire tool returns the selection gates (read-only)")
    record("AUDIT GREEN" in _srv.run_audit(), "MCP run_audit tool returns the live audit result")
except Exception as e:
    record(False, "MCP-native radar/hire/audit tier", str(e)[:160])

print(json.dumps(R))
