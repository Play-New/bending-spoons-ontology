"""The action-execution engine — the contracts, runnable.

Two-phase, per the contract discipline (foundations/ontology.md §5-§6):
  propose(action, params) -> validates parameters + submission criteria, computes the
                             TRANSACTION as a concrete diff, returns a proposal. Writes nothing.
  apply(proposal_id, approved_by) -> enforces the governance gate (human-gated actions refuse
                             to run without an approver), performs the write-back, runs the
                             audit, and commits only if green; rolls back if red.

The engine executes only what a contract declares. Judgment (an agent's logic tier) stays
outside: an agent DECIDES what to propose; the commit is always the declared transaction,
behind its gate. Proposals are working state in mcp/proposals/ (not part of the model).
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROPOSALS = Path(__file__).resolve().parent / "proposals"

TARGETS = "world-model/customer/targets.csv"
BUSINESSES = "world-model/company/businesses.csv"
INTERFACES = "interfaces/interfaces.csv"
DEALS = "world-model/company/deals.csv"
FACILITIES = "world-model/company/facilities.csv"

TODAY = time.strftime("%Y-%m-%d")


# ----------------------------- csv helpers -----------------------------
def _read_csv(rel: str) -> tuple[list[str], list[dict], list[str]]:
    """Return (header, rows-as-dicts, comment-lines) preserving order."""
    header, rows, comments = [], [], []
    for line in (ROOT / rel).read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            comments.append(line)
            continue
        r = next(csv.reader(io.StringIO(line)))
        if not header:
            header = r
        else:
            rows.append(dict(zip(header, r)))
    return header, rows, comments


def _fmt_row(header: list[str], row: dict) -> str:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="").writerow([row.get(c, "") for c in header])
    return buf.getvalue()


# ----------------------------- diff primitives -----------------------------
# A diff is a list of edits the apply phase executes verbatim:
#   {op: append_csv_row, file, row: {...}}
#   {op: set_csv_field,  file, key_col, key, field, value}
#   {op: set_frontmatter_prop, file, prop, value}
#   {op: create_file, file, content}

def _apply_edit(e: dict) -> None:
    p = ROOT / e["file"]
    if e["op"] == "create_file":
        if p.exists():
            raise ValueError(f"refusing to overwrite existing file: {e['file']}")
        p.write_text(e["content"], encoding="utf-8")
        return
    if e["op"] == "append_csv_row":
        header, _, _ = _read_csv(e["file"])
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        # insert before any trailing comment lines
        tail = len(lines)
        while tail > 0 and lines[tail - 1].startswith("#"):
            tail -= 1
        lines.insert(tail, _fmt_row(header, e["row"]))
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    if e["op"] == "set_csv_field":
        header, rows, _ = _read_csv(e["file"])
        text = p.read_text(encoding="utf-8")
        out = []
        hit = False
        seen_header = False
        for line in text.splitlines():
            if line.startswith("#") or not seen_header:
                if not line.startswith("#"):
                    seen_header = True
                out.append(line)
                continue
            r = dict(zip(header, next(csv.reader(io.StringIO(line)))))
            if r.get(e["key_col"]) == e["key"]:
                r[e["field"]] = e["value"]
                out.append(_fmt_row(header, r))
                hit = True
            else:
                out.append(line)
        if not hit:
            raise ValueError(f"row not found: {e['key']} in {e['file']}")
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
        return
    if e["op"] == "set_frontmatter_prop":
        text = p.read_text(encoding="utf-8")
        pat = re.compile(rf"^(  {re.escape(e['prop'])}: ).*$", re.M)
        if not pat.search(text):
            raise ValueError(f"property {e['prop']} not found in {e['file']}")
        v = e["value"]
        if any(c in str(v) for c in ':#{}[],&*?|>%@`"\''):
            v = f'"{v}"'
        p.write_text(pat.sub(rf"\g<1>{v}", text, count=1), encoding="utf-8")
        return
    raise ValueError(f"unknown edit op: {e['op']}")


# ----------------------------- node stubs (for close) -----------------------------
BUSINESS_STUB = """---
id: {id}
type: business
title: {title}
status: confirmed
purpose: acquired business — created at close; dossier to be written from the next filing
provenance: official-filing
as_of: {today}        # period of the underlying data
last_synced: {today}  # last verified against sources/
sources: [{source}]
properties:
{props}relations:
visibility: shared
---
# {title}

**Properties** → structured in the frontmatter above, 1:1 with `../businesses.csv` (per `../../../ontology.md` §1 `Business`; name = the title/PK). Operating data only — price, date, deal-type and PPA are the `Deal`'s (`../deals.csv`); the app the user touches is the `Interface` (`../../../interfaces/`).
**Links:** none declared on `Business` (`Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects).

Created by the `close acquisition` action; the grounded dossier is written when the next filing discloses the business.
"""

INTERFACE_STUB = """---
id: {id}-interface
type: interface
title: {title}
status: confirmed
purpose: the {title} delivery interface — where the machine meets its users
provenance: official-filing
as_of: {today}        # period of the underlying data
last_synced: {today}  # last verified against sources/
sources: [{source}]
properties:
{props}relations:
  - {{ type: of, target: {business}, cardinality: N:1, confidence: high, source: {source}, status: confirmed }}
visibility: shared
---
# {title} — interface

**Properties** → structured in the frontmatter above, 1:1 with `interfaces.csv` (per `../ontology.md §1 Interface`).
**Link:** `Interface —of→ Business` (declared here, once) → `../world-model/company/businesses/{business}.md`.

Created by the `close acquisition` action; capabilities-delivered to be grounded from the next filing.
"""


def _props_block(d: dict) -> str:
    out = []
    for k, v in d.items():
        v = str(v)
        if any(c in v for c in ':#{}[],&*?|>%@`"\''):
            v = f'"{v}"'
        out.append(f"  {k}: {v}")
    return "\n".join(out) + "\n"


# ----------------------------- the 8 actions -----------------------------
# Each builder: (params) -> (checks, gate, diff)  — checks are the contract's
# submission criteria, evaluated where mechanical; gate is 'auto' or 'human'.

def _source(p):
    """create/update Target (contract: capabilities/actions/market-radar.md)."""
    req = ["target", "revenue_scale", "hq", "product_offering", "revenue_model"]
    missing = [k for k in req if not p.get(k)]
    if missing:
        raise ValueError(f"missing parameters: {missing}")
    header, rows, _ = _read_csv(TARGETS)
    if any(r["target"] == p["target"] for r in rows):
        raise ValueError(f"target already exists: {p['target']} (use screen/underwrite to advance it)")
    checks = ["thesis boundary + public-signals-only: attested by the proposer (agent logic, not mechanical)"]
    row = {c: p.get(c, "[inferred]") for c in header}
    row.update({"target": p["target"], "status": "candidate", "irr": "n.d.", "walk_away_price": "n.d.",
                "source": p.get("source", "[to-validate — press only]"),
                "note": p.get("note", f"sourced {TODAY} by market-radar")})
    return checks, "human", [{"op": "append_csv_row", "file": TARGETS, "row": row}]


# HQ-gate geography — a European or North-American HQ counts however it is written: the continent,
# a country name, or an ISO code. (Defect-to-test: "Italy" was rejected because the gate literally
# substring-matched the word "Europe"; a real European HQ must pass regardless of phrasing.)
_EU_NAMES = ("europe", "germany", "france", "italy", "spain", "netherlands", "sweden", "denmark",
             "norway", "finland", "ireland", "united kingdom", "britain", "england", "scotland",
             "poland", "austria", "belgium", "portugal", "switzerland", "luxembourg", "czech",
             "greece", "romania", "hungary", "estonia", "latvia", "lithuania", "slovenia",
             "slovakia", "croatia", "bulgaria", "cyprus", "malta", "iceland")
_NA_NAMES = ("north america", "united states", "u.s.", "usa", "america", "canada")
_EU_CC = set("DE FR IT ES NL SE DK NO FI IE GB UK PL AT BE PT CH LU CZ GR RO HU EE LV LT SI SK HR BG CY MT IS".split())
_NA_CC = {"US", "CA"}


def _hq_in_region(hq: str) -> bool:
    """True if the HQ string names Europe or North America — by continent, country, or ISO code."""
    s = (hq or "").lower()
    if any(n in s for n in _EU_NAMES + _NA_NAMES):
        return True
    toks = {t.strip(".,;()[]").upper() for t in (hq or "").split()}
    return bool(toks & (_EU_CC | _NA_CC))


def _screen(p):
    """set Target.status (contract: capabilities/actions/screen-target.md) — the hard gates, mechanical."""
    header, rows, _ = _read_csv(TARGETS)
    row = next((r for r in rows if r["target"] == p.get("target")), None)
    if row is None:
        raise ValueError(
            f"unknown target: '{p.get('target')}' — screen mutates a sourced Target's status, so the target "
            f"must exist first. To just CHECK the gates on a company (read-only, no sourcing) use radar_gates "
            f"(US ticker) / radar_company (EU name); to admit it into the pipeline, source it first.")
    checks, fails = [], []
    hq_ok = _hq_in_region(row["hq"])
    (checks if hq_ok else fails).append(f"hq gate: '{row['hq']}' {'OK' if hq_ok else 'FAIL (HQ not in Europe / North America)'}")
    it_heavy = "IT service" in row["revenue_model"]
    (fails if it_heavy else checks).append(f"revenue-model gate: '{row['revenue_model']}' {'FAIL (IT-services-heavy)' if it_heavy else 'OK'}")
    rs = row["revenue_scale"]
    rs_ok = bool(rs) and rs != "n.d."
    (checks if rs_ok else fails).append(f"revenue-scale gate ($50M–$5B): '{rs or 'EMPTY'}' {'attested' if rs_ok else 'FAIL (no value)'}")
    status = "screened-in" if not fails else "screened-out"
    return checks + fails, "auto", [{"op": "set_csv_field", "file": TARGETS, "key_col": "target",
                                     "key": p["target"], "field": "status", "value": status}]


def _underwrite(p):
    """set Target.irr + walk_away_price (contract: capabilities/actions/deal-value.md) — hurdle enforced.
    The bar defaults to 65/25 but is a will PARAMETER, not a hard-coded law: the filing says it is
    'plausible we'll have to lower them' as scale grows (will.md), so a human may pass hurdle_levered_pct /
    hurdle_unlevered_pct to move the bar deliberately (logged + human-gated at apply)."""
    for k in ("target", "irr_levered_pct", "irr_unlevered_pct", "walk_away_price"):
        if p.get(k) in (None, ""):
            raise ValueError(f"missing parameter: {k}")
    lev, unlev = float(p["irr_levered_pct"]), float(p["irr_unlevered_pct"])
    _hl, _hu = p.get("hurdle_levered_pct"), p.get("hurdle_unlevered_pct")   # explicit: a deliberate 0 must stick
    hl = float(_hl) if _hl not in (None, "") else 65.0
    hu = float(_hu) if _hu not in (None, "") else 25.0
    lowered = " [deliberately lowered — will.md: the bar moves with scale]" if (hl < 65 or hu < 25) else ""
    if lev < hl or unlev < hu:
        raise ValueError(f"ABORT (submission criteria): case does not clear the hurdles — "
                         f"levered {lev}% (needs ≥{hl:g}) / unlevered {unlev}% (needs ≥{hu:g}); "
                         f"the {hl:g}/{hu:g} bar is a will constraint (will.md), not dogma — a human may lower it "
                         f"deliberately via hurdle_levered_pct / hurdle_unlevered_pct if scale warrants")
    header, rows, _ = _read_csv(TARGETS)
    row = next((r for r in rows if r["target"] == p["target"]), None)
    if row is None:
        raise ValueError(f"unknown target: {p['target']}")
    if row.get("status") != "screened-in":
        raise ValueError(f"target status is '{row.get('status')}' — only screened-in targets may be underwritten")
    checks = [f"hurdles: levered {lev}% ≥ {hl:g} OK · unlevered {unlev}% ≥ {hu:g} OK{lowered}",
              "pre-diligence inputs are ESTIMATES (deal-diligence verifies them)"]
    return checks, "human", [  # GATE 1 — the walk-away price needs human approval
        {"op": "set_csv_field", "file": TARGETS, "key_col": "target", "key": p["target"],
         "field": "irr", "value": f"levered {lev}% / unlevered {unlev}% [decision]"},
        {"op": "set_csv_field", "file": TARGETS, "key_col": "target", "key": p["target"],
         "field": "walk_away_price", "value": str(p["walk_away_price"])},
    ]


def _close(p):
    """create Deal + Business + Interface(s) (contract: capabilities/actions/deal-diligence.md)."""
    for k in ("target", "business", "date", "cohort", "deal_type"):
        if not p.get(k):
            raise ValueError(f"missing parameter: {k}")
    biz = p["business"].lower()
    theader, trows, _ = _read_csv(TARGETS)
    # match case-insensitively but store the CANONICAL target key, so the of_target FK resolves in the audit
    of_target = next((r["target"] for r in trows if r["target"].lower() == p["target"].lower()), None)
    if of_target is None:
        raise ValueError(f"unknown target: {p['target']} (Deal —of→ Target must resolve)")
    _, brows, _ = _read_csv(BUSINESSES)
    if any(r["business"] == biz for r in brows):
        raise ValueError(f"business already exists: {biz}")
    src = p.get("source", "bsp-f1")
    dheader, _, _ = _read_csv(DEALS)
    deal_row = {c: "" for c in dheader}
    deal_row.update({"produces_business": biz, "of_target": of_target, "date": p["date"], "cohort": p["cohort"],
                     "deal_type": p["deal_type"], "consideration_usd_m": str(p.get("consideration_usd_m", "")),
                     "ppa": p.get("ppa", ""), "source": src, "note": p.get("note", f"closed via engine {TODAY}")})
    bheader, _, _ = _read_csv(BUSINESSES)
    biz_row = {c: "n.d." for c in bheader}
    biz_row.update({"business": biz, "status": "main", "lifecycle": "acquired", "source": src,
                    "note": p.get("note", f"created at close {TODAY}")})
    iface = p.get("interface", biz)
    iheader, _, _ = _read_csv(INTERFACES)
    if_row = {c: "n.d." for c in iheader}
    if_row.update({"interface": iface, "business": biz, "category": p.get("category", "n.d."),
                   "capabilities_delivered": p.get("capabilities_delivered", "n.d."),
                   "status": "live", "source": src, "note": "created at close"})
    biz_props = {k: biz_row[k] for k in bheader if k not in ("business", "source", "note")}
    if_props = {"business": biz, **{k: if_row[k] for k in iheader if k not in ("interface", "business", "source", "note")}}
    checks = ["Deal ⊥ Business ⊥ Interface: price/PPA on the Deal, operating data on the Business, app on the Interface",
              "red flags re-feed deal-value through GATE 1 (attested by the diligence loop)"]
    return checks, "human", [  # GATE 2 — go/no-go is human
        {"op": "append_csv_row", "file": DEALS, "row": deal_row},
        {"op": "append_csv_row", "file": BUSINESSES, "row": biz_row},
        {"op": "append_csv_row", "file": INTERFACES, "row": if_row},
        {"op": "create_file", "file": f"world-model/company/businesses/{biz}.md",
         "content": BUSINESS_STUB.format(id=biz, title=p["business"], today=TODAY, source=src, props=_props_block(biz_props))},
        {"op": "create_file", "file": f"interfaces/{iface}.md",
         "content": INTERFACE_STUB.format(id=iface, title=p.get("interface_title", p["business"]), today=TODAY,
                                          source=src, business=biz, props=_props_block(if_props))},
    ]


_BIZ_WRITABLE = {"revenue_usd_m", "mau_m", "paying_customers_m", "nrr_pct", "tenure_yrs", "arpu",
                 "revenue_mix", "organic_channel_pct", "conversion_pct", "adj_op_margin_pct",
                 "status", "lifecycle"}
_IF_WRITABLE = {"category", "capabilities_delivered", "ai_features", "status"}


def _transform(p):
    """modify Business and/or Interface properties (contract: capabilities/actions/deal-optimize.md)."""
    biz = p.get("business")
    _, brows, _ = _read_csv(BUSINESSES)
    if not any(r["business"] == biz for r in brows):
        raise ValueError(f"unknown business: {biz}")
    diff, checks = [], []
    for prop, val in (p.get("business_changes") or {}).items():
        if prop not in _BIZ_WRITABLE:
            raise ValueError(f"'{prop}' is not a writable Business property (inv. 2: only declared §1 properties)")
        diff.append({"op": "set_csv_field", "file": BUSINESSES, "key_col": "business", "key": biz, "field": prop, "value": str(val)})
        diff.append({"op": "set_frontmatter_prop", "file": f"world-model/company/businesses/{biz}.md", "prop": prop, "value": val})
        checks.append(f"Business.{prop} → {val}")
    for iface, changes in (p.get("interface_changes") or {}).items():
        _, irows, _ = _read_csv(INTERFACES)
        irow = next((r for r in irows if r["interface"] == iface), None)
        if irow is None or irow["business"] != biz:
            raise ValueError(f"interface '{iface}' does not exist or is not of business '{biz}'")
        for prop, val in changes.items():
            if prop not in _IF_WRITABLE:
                raise ValueError(f"'{prop}' is not a writable Interface property")
            diff.append({"op": "set_csv_field", "file": INTERFACES, "key_col": "interface", "key": iface, "field": prop, "value": str(val)})
            diff.append({"op": "set_frontmatter_prop", "file": f"interfaces/{iface}.md", "prop": prop, "value": val})
            checks.append(f"Interface[{iface}].{prop} → {val}")
    if not diff:
        raise ValueError("no changes given (business_changes / interface_changes)")
    checks.append("boundary rule: monetization must not be price extraction dressed as value (attested; deal-monitor keeps it visible)")
    return checks, "human", diff


def _retire(p):
    """modify Business.status main → tail → retired (contract: capabilities/actions/retire.md)."""
    biz = p.get("business")
    _, brows, _ = _read_csv(BUSINESSES)
    row = next((r for r in brows if r["business"] == biz), None)
    if row is None:
        raise ValueError(f"unknown business: {biz}")
    order = ["main", "tail", "retired"]
    cur = row["status"] if row["status"] in order else "tail"
    nxt = p.get("to") or order[min(order.index(cur) + 1, 2)]
    if nxt not in order or order.index(nxt) <= order.index(cur):
        raise ValueError(f"illegal transition {cur} → {nxt} (main → tail → retired; the row is never deleted)")
    if not p.get("drift_evidence"):
        raise ValueError("submission criteria: a sustained drift finding from deal-monitor is required (drift_evidence)")
    checks = [f"transition {cur} → {nxt}; the row is never deleted (never-sell ≠ never-die)",
              f"drift evidence: {p['drift_evidence']}"]
    return checks, "human", [
        {"op": "set_csv_field", "file": BUSINESSES, "key_col": "business", "key": biz, "field": "status", "value": nxt},
        {"op": "set_frontmatter_prop", "file": f"world-model/company/businesses/{biz}.md", "prop": "status", "value": nxt},
    ]


def _finance(p):
    """create/modify Facility (contract: capabilities/actions/finance.md) — covenant enforced."""
    lev = p.get("post_transaction_leverage")
    if lev is None:
        raise ValueError("submission criteria: post_transaction_leverage (net debt / adj EBITDA) is required")
    if float(lev) > 4.0:
        raise ValueError(f"ABORT: post-transaction leverage {lev} breaches the ≤4.00 covenant (bsp-f1 ~L4541-4546)")
    checks = [f"leverage covenant: {lev} ≤ 4.00 OK", "negative covenants + CoC ceiling: attested by the proposer"]
    header, rows, _ = _read_csv(FACILITIES)
    if p.get("modify"):
        fac = p["modify"]
        if not any(r["facility"] == fac for r in rows):
            raise ValueError(f"unknown facility: {fac}")
        return checks, "human", [{"op": "set_csv_field", "file": FACILITIES, "key_col": "facility",
                                  "key": fac, "field": "status", "value": p.get("status", "drawn")}]
    for k in ("facility", "type", "currency", "size_m", "signed"):
        if not p.get(k):
            raise ValueError(f"missing parameter: {k}")
    row = {c: "" for c in header}
    row.update({k: str(p[k]) for k in ("facility", "type", "currency", "size_m", "signed")})
    row.update({"status": p.get("status", "available"), "source": p.get("source", "[to-validate — press only]"),
                "note": p.get("note", f"raised via engine {TODAY}")})
    return checks, "human", [{"op": "append_csv_row", "file": FACILITIES, "row": row}]


def _talent(p):
    """advisory in v1: the Spooners backing is the aggregate node (no per-person dataset), so the
    engine cannot write it structurally — it returns the transaction as a documented manual edit."""
    raise ValueError("talent is advisory in v1: the Spooners backing is aggregate prose (the filing discloses no "
                     "per-person data). Propose the change via the contract (capabilities/actions/talent.md) and "
                     "edit spooners.md's Properties line manually — the audit will hold the 1:1.")


ACTIONS = {
    "source": _source, "screen": _screen, "underwrite": _underwrite, "close": _close,
    "transform": _transform, "retire": _retire, "finance": _finance, "talent": _talent,
}


# ----------------------------- propose / apply -----------------------------
def propose(action: str, params: dict) -> dict:
    if action not in ACTIONS:
        raise ValueError(f"unknown action: {action} (have: {', '.join(ACTIONS)})")
    checks, gate, diff = ACTIONS[action](params or {})
    prop = {"id": f"{action}-{uuid.uuid4().hex[:8]}", "action": action, "params": params,
            "created": TODAY, "checks": checks, "gate": gate, "diff": diff, "status": "pending"}
    PROPOSALS.mkdir(exist_ok=True)
    (PROPOSALS / f"{prop['id']}.json").write_text(json.dumps(prop, indent=2, ensure_ascii=False), encoding="utf-8")
    return prop


def apply(proposal_id: str, approved_by: str | None = None) -> dict:
    f = PROPOSALS / f"{proposal_id}.json"
    if not f.exists():
        raise ValueError(f"unknown proposal: {proposal_id}")
    prop = json.loads(f.read_text(encoding="utf-8"))
    if prop["status"] != "pending":
        raise ValueError(f"proposal is {prop['status']}, not pending")
    if prop["action"] not in ACTIONS:
        raise ValueError(f"unknown action in proposal: {prop['action']}")
    # re-derive the gate from the contract at apply-time — NEVER trust the stored gate field.
    # (a tampered proposals/*.json must not be able to downgrade a human gate to auto or inject a diff;
    # re-invoking the builder also re-validates the submission criteria against CURRENT state — so a state
    # change between propose and apply is caught, not silently committed from a stale stored diff.)
    _checks, gate, diff = ACTIONS[prop["action"]](prop.get("params") or {})
    if gate == "human" and not approved_by:
        raise ValueError("this action is human-gated by its contract: apply requires approved_by=<the human>")
    # the commit IS the audit trail — refuse to mutate the model outside a git work tree (fail before any edit)
    if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                      cwd=ROOT, capture_output=True, text=True).returncode != 0:
        raise RuntimeError(f"the engine writes one git commit per action, but {ROOT} is not a git work tree; "
                           "run inside the model's repo (git init if you are experimenting on a copy)")
    # commit the RE-DERIVED diff, not the stored one — the stored prop["diff"] is only a propose-time preview.
    # snapshot for rollback — covers the edits, the audit, AND the commit
    touched = sorted({e["file"] for e in diff})
    backup = {t: (ROOT / t).read_text(encoding="utf-8") for t in touched if (ROOT / t).exists()}
    created = [t for t in touched if not (ROOT / t).exists()]

    def _rollback():
        for t, content in backup.items():
            (ROOT / t).write_text(content, encoding="utf-8")
        for t in created:
            (ROOT / t).unlink(missing_ok=True)
        if touched:  # unstage the transaction so a failed apply leaves nothing staged for the next commit
            subprocess.run(["git", "reset", "-q", "--", *touched], cwd=ROOT, capture_output=True)

    try:
        for e in diff:
            _apply_edit(e)
        audit = subprocess.run(["python3", "mcp/audit.py"], cwd=ROOT, capture_output=True, text=True)
        if audit.returncode != 0:
            raise RuntimeError(f"audit RED after write:\n{audit.stdout}")
        # mark applied, then commit; if the commit fails, the except rolls the status back to pending (below),
        # so a failed commit never leaves an "applied" record without a matching commit
        prop.update({"status": "applied", "approved_by": approved_by or "auto", "applied": TODAY})
        f.write_text(json.dumps(prop, indent=2, ensure_ascii=False), encoding="utf-8")
        # commit ONLY the declared transaction, by PATHSPEC — `git add -A` would sweep a dirty tree in, and a
        # pathspec-less `git commit` would sweep the whole pre-existing index in; both break the audit-trail
        # guarantee. `git commit -- <touched>` commits exactly those paths regardless of index state. The
        # ephemeral proposal record (proposals/) is gitignored and deliberately not committed.
        if touched:
            subprocess.run(["git", "add", "--", *touched], cwd=ROOT, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-q",
                            "-m", f"action: {prop['action']} ({proposal_id}) — approved by {approved_by or 'auto'}\n\n"
                                  f"Committed by the Bending Spoons action engine; the commit contains only the "
                                  f"declared transaction, and the audit was green at write-back.",
                            "--", *touched],
                           cwd=ROOT, check=True, capture_output=True)
    except Exception:
        _rollback()
        prop.update({"status": "pending"})          # never leave a half-applied proposal marked applied
        prop.pop("approved_by", None); prop.pop("applied", None)
        f.write_text(json.dumps(prop, indent=2, ensure_ascii=False), encoding="utf-8")
        raise
    return prop


def reject(proposal_id: str, reason: str = "") -> dict:
    f = PROPOSALS / f"{proposal_id}.json"
    if not f.exists():
        raise ValueError(f"unknown proposal: {proposal_id}")
    prop = json.loads(f.read_text(encoding="utf-8"))
    if prop["status"] != "pending":
        raise ValueError(f"proposal is {prop['status']}, not pending")  # can't reject an applied/rejected one
    prop.update({"status": "rejected", "reason": reason})
    f.write_text(json.dumps(prop, indent=2, ensure_ascii=False), encoding="utf-8")
    return prop


def pending() -> list[dict]:
    PROPOSALS.mkdir(exist_ok=True)
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PROPOSALS.glob("*.json"))]
