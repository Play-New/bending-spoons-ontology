"""Guards: the safety rails under adversarial use — rollback on red audit, gate bypass
attempts, double-apply, tampered proposals. Run via run_all.py: python3 test_guards.py <sandbox_root>.
"""
import json
import subprocess
import sys
from pathlib import Path

SBX = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SBX / "mcp"))
import engine  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, detail[:160]))


# ---- 1. DIFF TAMPER IS IGNORED: apply re-derives the diff from the contract, not from stored state ----
prop = engine.propose("source", {"target": "RollbackCo", "revenue_scale": "x", "hq": "Europe",
                                 "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
f = engine.PROPOSALS / f"{prop['id']}.json"
tampered = json.loads(f.read_text())
# inject a business row with no node file — if the STORED diff were applied, the audit would go red
tampered["diff"].append({"op": "append_csv_row", "file": "world-model/company/businesses.csv",
                         "row": {"business": "ghostco", "status": "main", "lifecycle": "acquired",
                                 "source": "bsp-f1", "note": "injected — must be ignored"}})
f.write_text(json.dumps(tampered))
before_biz = (SBX / "world-model/company/businesses.csv").read_text()
engine.apply(prop["id"], "test-human")  # succeeds: the re-derived source diff is clean; the tamper is ignored
record("ghostco" not in (SBX / "world-model/company/businesses.csv").read_text()
       and (SBX / "world-model/company/businesses.csv").read_text() == before_biz,
       "diff tamper ignored: injected row never lands (diff re-derived from the contract)")
record("RollbackCo" in (SBX / "world-model/customer/targets.csv").read_text(),
       "diff tamper ignored: the legitimate re-derived transaction still applied")

# ---- 1b. ROLLBACK on a RED audit: model reverts byte-identical, proposal returns to pending ----
p1b = engine.propose("source", {"target": "RedAuditCo", "revenue_scale": "x", "hq": "Europe",
                                "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
before_t = (SBX / "world-model/customer/targets.csv").read_text()
_orig = engine.subprocess.run
def _fail_audit(cmd, *a, **k):
    if list(cmd[:2]) == ["python3", "mcp/audit.py"]:
        class R:  # simulate a red audit
            returncode = 1; stdout = "DEFECTS:\n - simulated"
        return R()
    return _orig(cmd, *a, **k)
engine.subprocess.run = _fail_audit
try:
    engine.apply(p1b["id"], "test-human")
    record(False, "rollback: a red audit must raise")
except Exception as e:
    record("audit RED" in str(e), "rollback: apply raised on red audit", str(e))
finally:
    engine.subprocess.run = _orig
record((SBX / "world-model/customer/targets.csv").read_text() == before_t,
       "rollback: targets.csv byte-identical after a red-audit apply")
p1b_state = json.loads((engine.PROPOSALS / f"{p1b['id']}.json").read_text())
record(p1b_state["status"] == "pending" and "approved_by" not in p1b_state,
       "rollback: red-audit apply leaves the proposal pending, not applied", p1b_state.get("status", "?"))

# ---- 2. GATE: human-gated apply without approver, and after-the-fact double apply ----
p2 = engine.propose("source", {"target": "GateCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
try:
    engine.apply(p2["id"])
    record(False, "gate: apply without approver must refuse")
except ValueError as e:
    record("human-gated" in str(e), "gate: apply without approver refused", str(e))
engine.apply(p2["id"], "test-human")
try:
    engine.apply(p2["id"], "test-human")
    record(False, "double-apply must refuse")
except ValueError as e:
    record("not pending" in str(e), "double-apply refused (proposal consumed)", str(e))

# ---- 3. UNKNOWN proposal id ----
try:
    engine.apply("nope-123", "x")
    record(False, "unknown proposal must refuse")
except ValueError as e:
    record("unknown proposal" in str(e), "unknown proposal refused", str(e))

# ---- 4. REJECT flow ----
p3 = engine.propose("source", {"target": "RejectCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
engine.reject(p3["id"], "not in thesis")
try:
    engine.apply(p3["id"], "test-human")
    record(False, "apply after reject must refuse")
except ValueError as e:
    record("not pending" in str(e), "apply after reject refused", str(e))

# ---- 5. file-overwrite guard (tested directly on _apply_edit — since apply now re-derives the diff,
#         a create_file-over-existing can only originate inside a builder, so guard the primitive itself) ----
_before_will = (SBX / "will.md").read_text()
try:
    engine._apply_edit({"op": "create_file", "file": "will.md", "content": "overwrite attempt"})
    record(False, "create_file over existing file must refuse")
except Exception as e:
    record("refusing to overwrite" in str(e), "_apply_edit refuses to overwrite an existing file", str(e))
record((SBX / "will.md").read_text() == _before_will, "will.md untouched after overwrite attempt")

# ---- 6. GIT PREFLIGHT: the engine must refuse to mutate the model outside a git work tree ----
p5 = engine.propose("source", {"target": "NoGitCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
before_targets_5 = (SBX / "world-model/customer/targets.csv").read_text()
git_dir = SBX / ".git"
moved = git_dir.with_name(".git-hidden")
git_dir.rename(moved)                       # simulate "not a git repo"
try:
    engine.apply(p5["id"], "test-human")
    record(False, "git preflight: apply outside a git work tree must refuse")
except Exception as e:
    record("not a git work tree" in str(e), "git preflight: apply refused outside git repo", str(e))
finally:
    moved.rename(git_dir)                    # restore
record((SBX / "world-model/customer/targets.csv").read_text() == before_targets_5,
       "git preflight: model untouched when git is unavailable (failed before any edit)")

# ---- 7. GATE RE-DERIVATION: tampering the stored gate must not downgrade a human gate ----
p6 = engine.propose("source", {"target": "GateTamperCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
f6 = engine.PROPOSALS / f"{p6['id']}.json"
t6 = json.loads(f6.read_text()); t6["gate"] = "auto"; f6.write_text(json.dumps(t6))
try:
    engine.apply(p6["id"])  # no approver; stored gate says auto, but the contract gate is human
    record(False, "gate re-derivation: tampered gate must not bypass the human gate")
except ValueError as e:
    record("human-gated" in str(e), "gate re-derivation: gate re-derived from contract, tamper defeated", str(e))

# ---- 8. SCOPED COMMIT: an unrelated PRE-STAGED file must NOT be swept into the action commit ----
# (the real leak: `git add` is scoped but a pathspec-less `git commit` would commit the whole index)
(SBX / "will.md").write_text((SBX / "will.md").read_text() + "\n<!-- unrelated dirty edit -->\n")
subprocess.run(["git", "add", "--", "will.md"], cwd=SBX, capture_output=True)  # pre-stage the unrelated file
p7 = engine.propose("source", {"target": "ScopedCommitCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
engine.apply(p7["id"], "test-human")
committed = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
                           cwd=SBX, capture_output=True, text=True).stdout
record("targets.csv" in committed and "will.md" not in committed,
       "scoped commit: pre-staged will.md NOT swept into the action commit (pathspec commit)", committed.replace("\n", " "))
# and the pre-staged unrelated change must survive (still staged), not be lost
still_staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=SBX, capture_output=True, text=True).stdout
record("will.md" in still_staged, "scoped commit: the pre-staged unrelated change survives, uncommitted")
subprocess.run(["git", "reset", "-q", "--", "will.md"], cwd=SBX, capture_output=True)
subprocess.run(["git", "checkout", "--", "will.md"], cwd=SBX, capture_output=True)

# ---- 9. REJECT guards: unknown id and non-pending must refuse cleanly (no crash / no corruption) ----
try:
    engine.reject("does-not-exist-999", "x")
    record(False, "reject: unknown id must refuse")
except ValueError as e:
    record("unknown proposal" in str(e), "reject: unknown id refused (no FileNotFoundError)", str(e))
p8 = engine.propose("source", {"target": "RejectAppliedCo", "revenue_scale": "x", "hq": "Europe",
                               "product_offering": "d", "revenue_model": "s", "source": "bsp-f1"})
engine.apply(p8["id"], "test-human")
try:
    engine.reject(p8["id"], "too late")
    record(False, "reject: an already-applied proposal must refuse")
except ValueError as e:
    record("not pending" in str(e), "reject: cannot overwrite an applied proposal", str(e))

# ---- 10. AUDIT FAILS CLOSED without pyyaml (a commit-gating safety net must never degrade to green) ----
r = subprocess.run(["python3", "-c",
                    "import sys; sys.modules['yaml']=None; exec(compile(open('mcp/audit.py').read(), 'audit.py', 'exec'))"],
                   cwd=SBX, capture_output=True, text=True)
record(r.returncode != 0 and "fails closed" in r.stdout,
       "audit fails closed when pyyaml is unavailable (no false green)", (r.stdout or r.stderr)[-160:])

# ---- 11. AUDIT emits a clean defect (not a traceback) for a csv row with no node file ----
biz_csv = SBX / "world-model/company/businesses.csv"
_orig_biz = biz_csv.read_text()
biz_csv.write_text(_orig_biz.rstrip() + "\nghostco,n.d.,n.d.,n.d.,n.d.,n.d.,n.d.,n.d.,n.d.,n.d.,n.d.,main,acquired,bsp-f1,no node\n")
r = subprocess.run(["python3", "mcp/audit.py"], cwd=SBX, capture_output=True, text=True)
record(r.returncode != 0 and "csv row without node file" in r.stdout and "Traceback" not in r.stderr,
       "audit: missing node file → clean defect, not an uncaught FileNotFoundError", (r.stdout + r.stderr)[-160:])
biz_csv.write_text(_orig_biz)

# ---- 12. AUDIT guards the disclosed-price-tagged-press-only regression (Tractive) ----
deals_csv = SBX / "world-model/company/deals.csv"
_orig_deals = deals_csv.read_text()
deals_csv.write_text(_orig_deals.rstrip() + "\nghostdeal,n.d.,2026,2026,acquisition,999,,,,bsp-f1,\"$1 [to-validate — press only]\"\n")
r = subprocess.run(["python3", "mcp/audit.py"], cwd=SBX, capture_output=True, text=True)
record(r.returncode != 0 and "press-only" in r.stdout,
       "audit: filing-sourced deal tagged press-only → defect (Tractive regression guard)", r.stdout[-160:])
deals_csv.write_text(_orig_deals)

print(json.dumps(R))
