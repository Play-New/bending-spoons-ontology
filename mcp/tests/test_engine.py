"""E2E: the full deal lifecycle through the engine, in a sandbox copy of the repo.

Run via run_all.py (which provides the sandbox); direct: python3 test_engine.py <sandbox_root>.
Covers every verb (happy path) and every contractual refusal path, then asserts the
world model's integrity: rows written, node stubs created, node<->csv 1:1, git commits
with the approver recorded, audit green at the end.
"""
import csv
import io
import json
import subprocess
import sys
from pathlib import Path

SBX = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SBX / "mcp"))
import engine  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def case(name, fn, expect_refusal=None):
    try:
        out = fn()
        if expect_refusal:
            R["fail"] += 1
            R["cases"].append(("FAIL", name, f"expected refusal '{expect_refusal}' but succeeded"))
        else:
            R["pass"] += 1
            R["cases"].append(("PASS", name, ""))
        return out
    except Exception as e:
        if expect_refusal and expect_refusal.lower() in str(e).lower():
            R["pass"] += 1
            R["cases"].append(("PASS", name, f"refused as contracted: {str(e)[:80]}"))
        else:
            R["fail"] += 1
            R["cases"].append(("FAIL", name, str(e)[:160]))
        return None


def rows(rel, key):
    out = {}
    header = None
    for line in (SBX / rel).read_text().splitlines():
        if line.startswith("#"):
            continue
        r = next(csv.reader(io.StringIO(line)))
        if header is None:
            header = r
        else:
            out[dict(zip(header, r))[key]] = dict(zip(header, r))
    return out


# ---- lifecycle ----
p = case("source: propose NewCo", lambda: engine.propose("source", {
    "target": "NewCo", "revenue_scale": "in band [inferred]", "hq": "Europe",
    "product_offering": "digital (consumer)", "revenue_model": "self-serve subscriptions",
    "source": "[to-validate — press only]"}))
case("source: params missing → refuse", lambda: engine.propose("source", {"target": "X"}),
     expect_refusal="missing parameters")
case("source: apply w/o approver → refuse", lambda: engine.apply(p["id"]),
     expect_refusal="human-gated")
case("source: apply approved", lambda: engine.apply(p["id"], "test-human"))
case("source: duplicate → refuse", lambda: engine.propose("source", {
    "target": "NewCo", "revenue_scale": "x", "hq": "Europe",
    "product_offering": "d", "revenue_model": "s"}), expect_refusal="already exists")

p = case("screen: propose", lambda: engine.propose("screen", {"target": "NewCo"}))
assert p and p["gate"] == "auto", "screen must be auto-gated"
case("screen: apply auto", lambda: engine.apply(p["id"]))
assert rows("world-model/customer/targets.csv", "target")["NewCo"]["status"] == "screened-in", "screen wrote status"
R["cases"].append(("PASS", "screen: status written screened-in", "")); R["pass"] += 1

case("underwrite: below hurdle → refuse", lambda: engine.propose("underwrite", {
    "target": "NewCo", "irr_levered_pct": 50, "irr_unlevered_pct": 30, "walk_away_price": "$1"}),
     expect_refusal="hurdles")
p = case("underwrite: above hurdle", lambda: engine.propose("underwrite", {
    "target": "NewCo", "irr_levered_pct": 70, "irr_unlevered_pct": 28, "walk_away_price": "$100M"}))
case("underwrite: apply GATE 1", lambda: engine.apply(p["id"], "test-human"))

p = case("close: propose", lambda: engine.propose("close", {
    "target": "NewCo", "business": "NewCo", "date": "2026-07", "cohort": "2026",
    "deal_type": "acquisition", "consideration_usd_m": 100, "category": "testing", "source": "bsp-f1"}))
case("close: apply GATE 2", lambda: engine.apply(p["id"], "test-human"))
assert (SBX / "world-model/company/businesses/newco.md").exists(), "business node stub created"
assert (SBX / "interfaces/newco.md").exists(), "interface node stub created"
assert "newco" in rows("world-model/company/deals.csv", "produces_business"), "deal row written"
R["cases"].append(("PASS", "close: deal+business+interface rows + node stubs", "")); R["pass"] += 1
case("close: unknown target → refuse", lambda: engine.propose("close", {
    "target": "Ghost", "business": "Ghost", "date": "2026", "cohort": "2026", "deal_type": "acquisition"}),
     expect_refusal="unknown target")

p = case("transform: propose", lambda: engine.propose("transform", {
    "business": "newco", "business_changes": {"lifecycle": "transforming"},
    "interface_changes": {"newco": {"ai_features": "AI-assisted"}}}))
case("transform: apply", lambda: engine.apply(p["id"], "test-human"))
assert rows("world-model/company/businesses.csv", "business")["newco"]["lifecycle"] == "transforming"
assert "ai_features: AI-assisted" in (SBX / "interfaces/newco.md").read_text(), "node frontmatter synced"
R["cases"].append(("PASS", "transform: csv+node written 1:1", "")); R["pass"] += 1
case("transform: undeclared property → refuse", lambda: engine.propose("transform", {
    "business": "newco", "business_changes": {"secret": "x"}}), expect_refusal="not a writable")

case("retire: no drift evidence → refuse", lambda: engine.propose("retire", {"business": "newco"}),
     expect_refusal="drift")
p = case("retire: propose with evidence", lambda: engine.propose("retire", {
    "business": "newco", "to": "tail", "drift_evidence": "test drift finding"}))
case("retire: apply", lambda: engine.apply(p["id"], "test-human"))
case("retire: backwards transition → refuse", lambda: engine.propose("retire", {
    "business": "newco", "to": "main", "drift_evidence": "x"}), expect_refusal="illegal transition")

case("finance: covenant breach → refuse", lambda: engine.propose("finance", {
    "facility": "t1", "type": "term loan A", "currency": "EUR", "size_m": 1,
    "signed": "2026", "post_transaction_leverage": 4.5}), expect_refusal="covenant")
p = case("finance: within covenant", lambda: engine.propose("finance", {
    "facility": "test-loan", "type": "term loan A", "currency": "EUR", "size_m": 500,
    "signed": "2026-07", "post_transaction_leverage": 2.8, "source": "bsp-f1"}))
case("finance: apply", lambda: engine.apply(p["id"], "test-human"))

case("talent: advisory → refuse", lambda: engine.propose("talent", {}), expect_refusal="advisory")
case("unknown verb → refuse", lambda: engine.propose("nonsense", {}), expect_refusal="unknown action")

# ---- uncovered branches (defect-to-test, from the adversarial audit) ----
case("close: business already exists → refuse", lambda: engine.propose("close", {
    "target": "NewCo", "business": "NewCo", "date": "2026", "cohort": "2026", "deal_type": "acquisition"}),
     expect_refusal="already exists")
case("underwrite: target not screened-in → refuse", lambda: engine.propose("underwrite", {
    "target": "AOL", "irr_levered_pct": 70, "irr_unlevered_pct": 28, "walk_away_price": "$1"}),
     expect_refusal="screened-in")
case("transform: interface not of the business → refuse", lambda: engine.propose("transform", {
    "business": "newco", "interface_changes": {"vimeo": {"ai_features": "x"}}}),
     expect_refusal="is not of business")
case("finance: modify unknown facility → refuse", lambda: engine.propose("finance", {
    "post_transaction_leverage": 2.0, "modify": "ghost-facility"}), expect_refusal="unknown facility")
# finance modify-success: change an existing facility's status (the happy modify branch + write-back + commit)
pm = case("finance: modify existing facility (happy path)", lambda: engine.propose("finance", {
    "modify": "test-loan", "status": "drawn", "post_transaction_leverage": 2.0}))
case("finance: modify applied", lambda: engine.apply(pm["id"], "test-human"))
assert rows("world-model/company/facilities.csv", "facility")["test-loan"]["status"] == "drawn", "modify wrote status"
R["cases"].append(("PASS", "finance: modify write-back set facility status=drawn", "")); R["pass"] += 1

# rollback when git commit fails AFTER a green audit: model reverts, proposal returns to pending
pcf = engine.propose("source", {"target": "CommitFailCo", "revenue_scale": "x", "hq": "Europe",
                                "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
before_cf = (SBX / "world-model/customer/targets.csv").read_text()
_orig_run = engine.subprocess.run
def _fail_commit(cmd, *a, **k):
    if list(cmd[:2]) == ["git", "commit"]:
        raise subprocess.CalledProcessError(1, cmd)
    return _orig_run(cmd, *a, **k)
engine.subprocess.run = _fail_commit
try:
    engine.apply(pcf["id"], "test-human")
    R["cases"].append(("FAIL", "commit-failure rollback: apply must raise", "")); R["fail"] += 1
except Exception:
    R["cases"].append(("PASS", "commit-failure: apply raised when git commit fails", "")); R["pass"] += 1
finally:
    engine.subprocess.run = _orig_run
_pcf_state = json.loads((engine.PROPOSALS / f"{pcf['id']}.json").read_text())["status"]
if (SBX / "world-model/customer/targets.csv").read_text() == before_cf and _pcf_state == "pending":
    R["cases"].append(("PASS", "commit-failure rollback: model reverted + proposal back to pending", "")); R["pass"] += 1
else:
    R["cases"].append(("FAIL", "commit-failure rollback", f"reverted={(SBX / 'world-model/customer/targets.csv').read_text()==before_cf} state={_pcf_state}")); R["fail"] += 1
# and the index must be CLEAN after a failed commit — nothing left staged to leak into the next action's commit
_staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=SBX, capture_output=True, text=True).stdout.strip()
(R["cases"].append(("PASS", "commit-failure rollback: git index left clean (no staged leak)", "")), R.__setitem__("pass", R["pass"] + 1)) \
    if _staged == "" else \
    (R["cases"].append(("FAIL", "commit-failure rollback: index not clean", _staged[:160])), R.__setitem__("fail", R["fail"] + 1))

# created-file rollback (the close path): a close whose commit fails must UNLINK the created node files,
# revert the csvs, and leave the index clean (the append-only source tests never exercise create_file rollback)
pcl = engine.propose("close", {"target": "AOL", "business": "RollbackBiz", "date": "2026", "cohort": "2026",
                               "deal_type": "acquisition", "source": "bsp-f1"})
_biz_node = SBX / "world-model/company/businesses/rollbackbiz.md"
_if_node = SBX / "interfaces/rollbackbiz.md"
engine.subprocess.run = _fail_commit  # reuse the commit-failer defined above
try:
    engine.apply(pcl["id"], "test-human")
    R["cases"].append(("FAIL", "close commit-failure: apply must raise", "")); R["fail"] += 1
except Exception:
    R["cases"].append(("PASS", "close commit-failure: apply raised", "")); R["pass"] += 1
finally:
    engine.subprocess.run = _orig_run
_clean = (not _biz_node.exists() and not _if_node.exists()
          and "rollbackbiz" not in (SBX / "world-model/company/businesses.csv").read_text()
          and subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=SBX, capture_output=True, text=True).stdout.strip() == "")
(R["cases"].append(("PASS", "close commit-failure rollback: created node files unlinked + csvs reverted + index clean", "")), R.__setitem__("pass", R["pass"] + 1)) \
    if _clean else \
    (R["cases"].append(("FAIL", "close commit-failure rollback", f"biz_node={_biz_node.exists()} if_node={_if_node.exists()}")), R.__setitem__("fail", R["fail"] + 1))

# ---- integrity after the full run ----
audit = subprocess.run(["python3", "mcp/audit.py"], cwd=SBX, capture_output=True, text=True)
(R["cases"].append(("PASS", "audit green after full lifecycle", "")), R.__setitem__("pass", R["pass"] + 1)) \
    if audit.returncode == 0 else (R["cases"].append(("FAIL", "audit green after full lifecycle", audit.stdout[:200])),
                                   R.__setitem__("fail", R["fail"] + 1))
log = subprocess.run(["git", "log", "--oneline", "-8"], cwd=SBX, capture_output=True, text=True).stdout
ok = all(v in log for v in ("action: source", "action: screen", "action: underwrite", "action: close",
                            "action: transform", "action: retire", "action: finance")) and "test-human" in log
(R["cases"].append(("PASS", "git: one commit per applied action, approver recorded", "")),
 R.__setitem__("pass", R["pass"] + 1)) if ok else \
    (R["cases"].append(("FAIL", "git commit trail", log[:200])), R.__setitem__("fail", R["fail"] + 1))


# ---- HQ gate accepts a European / North-American HQ however it is written (defect-to-test) ----
# a client's target with hq="Italy" was screened out because the gate literally matched the word
# "Europe"; a real in-region HQ must pass whether given as continent, country name, or ISO code.
def _rec(ok, name, detail=""):
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))
    R["pass" if ok else "fail"] += 1


for _hq in ("Italy", "Milan, Italy", "Germany", "IT", "Milan, IT", "Europe",
            "United States", "San Francisco, CA, US", "Canada"):
    _rec(engine._hq_in_region(_hq), f"HQ gate accepts in-region HQ: '{_hq}'")
for _hq in ("Tokyo, Japan", "Sydney, Australia", "Singapore", "n.d.", ""):
    _rec(not engine._hq_in_region(_hq), f"HQ gate rejects out-of-region HQ: '{_hq}'")


# ---- the 65/25 hurdle is a will PARAMETER, not a hard-coded law (defect-to-test) ----
# the fixed refusal read as rigid; will.md says the bar "moves with scale, not dogma".
try:
    engine._underwrite({"target": "HurdleProbe", "irr_levered_pct": 40,
                        "irr_unlevered_pct": 20, "walk_away_price": 1})
    _rec(False, "underwrite: default bar refuses 40/20", "no error raised")
except ValueError as e:
    m = str(e)
    _rec("clear the hurdles" in m and "hurdle_levered_pct" in m and "will.md" in m,
         "underwrite: default 65/25 refuses 40/20 AND cites the movable will bar", m[:140])
try:
    # a deliberately-lowered bar lets a sub-65/25 case CLEAR the hurdle; it then fails later on the missing
    # row (unknown target), which proves the hurdle gate passed — the rigidity is gone.
    engine._underwrite({"target": "HurdleProbe", "irr_levered_pct": 55, "irr_unlevered_pct": 22,
                        "walk_away_price": 1, "hurdle_levered_pct": 55, "hurdle_unlevered_pct": 22})
    _rec(False, "underwrite: lowered bar clears hurdle then hits unknown target", "no error raised")
except ValueError as e:
    _rec("clear the hurdles" not in str(e),
         "underwrite: a deliberately-lowered bar (55/22) clears the hurdle gate", str(e)[:140])

# ---- screen refusal must redirect, not dead-end (defect-to-test) ----
try:
    engine._screen({"target": "NopeCo-never-sourced"})
    _rec(False, "screen: unknown target should raise", "no error raised")
except ValueError as e:
    m = str(e)
    _rec("unknown target" in m and "radar_gates" in m and "source" in m,
         "screen: unknown-target refusal redirects to radar_gates / source (not a dead end)", m[:140])

print(json.dumps(R))
