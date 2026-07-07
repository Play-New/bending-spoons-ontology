"""MCP server surface: tools registered, annotations set, apply is elicitation-capable.
python3 test_server.py <repo_root>. Read-only.
"""
import asyncio
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "mcp"))
import server  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))


async def main():
    tools = {t.name: t for t in await server.mcp.list_tools()}
    expected = {"overview", "list_nodes", "get_node", "search", "get_capability", "list_capabilities",
                "will", "ontology", "analysis", "foundations", "list_sources", "get_source",
                "activate_agent", "propose_action", "apply_action", "list_proposals", "reject_action",
                # the scouting/hiring/audit tier, MCP-native so the whole loop runs from any MCP client:
                "radar_universe", "radar_discover", "radar_watchlist", "radar_gates", "radar_company",
                "radar_loyalty", "radar_signals", "radar_scout", "hire", "run_audit"}
    record(expected == set(tools), f"exactly {len(expected)} tools registered (none missing, none unexpected)",
           {"missing": sorted(expected - set(tools)), "unexpected": sorted(set(tools) - expected)})

    readers = expected - {"propose_action", "apply_action", "reject_action"}
    for name in sorted(readers):
        ann = getattr(tools.get(name), "annotations", None)
        record(bool(ann and ann.readOnlyHint), f"annotation readOnlyHint on {name}")
    ann = getattr(tools.get("apply_action"), "annotations", None)
    record(bool(ann and ann.destructiveHint), "annotation destructiveHint on apply_action")
    ann = getattr(tools.get("propose_action"), "annotations", None)
    record(bool(ann and ann.destructiveHint is False), "propose_action marked non-destructive")

    fn = server.apply_action
    record(asyncio.iscoroutinefunction(fn), "apply_action is async (elicitation-capable)")
    record("ctx" in inspect.signature(fn).parameters, "apply_action takes Context (elicitation wiring)")
    record("elicit" in inspect.getsource(fn), "apply_action elicits approval when approver missing")

    # tool descriptions must not lie about the layout
    for name in tools:
        d = (tools[name].description or "")
        record("observed/" not in d and "projected/" not in d, f"description current (no stale folders): {name}")

    # ---- elicitation BEHAVIOR (mock Context + engine; no real model mutation) ----
    class _Res:
        def __init__(self, action, name=None):
            self.action = action
            self.data = type("D", (), {"approved_by": name})() if name else None

    class _Ctx:
        def __init__(self, res): self._res = res
        async def elicit(self, message, schema): return self._res

    _orig_pending, _orig_apply = server._engine.pending, server._engine.apply
    server._engine.pending = lambda: [{"id": "p-x", "gate": "human", "action": "source"}]
    _applied = {}
    server._engine.apply = lambda pid, approver=None: _applied.update(approver=approver) or {"id": pid, "approved_by": approver}
    try:
        out_accept = await server.apply_action("p-x", _Ctx(_Res("accept", "Alice")))
        record("APPLIED" in out_accept and _applied.get("approver") == "Alice",
               "elicitation accept → applies with the elicited approver", out_accept)
        out_decline = await server.apply_action("p-x", _Ctx(_Res("decline")))
        record("DECLINED" in out_decline and _applied.get("approver") == "Alice",  # apply NOT called again on decline
               "elicitation decline → DECLINED, not applied", out_decline)
    finally:
        server._engine.pending, server._engine.apply = _orig_pending, _orig_apply

    # REFUSED wrapping: reject_action on an unknown id returns a clean REFUSED (not a crash)
    record(server.reject_action("does-not-exist-xyz").startswith("REFUSED"),
           "reject_action wraps an engine refusal as REFUSED")

    # the newly MCP-native tier (offline-safe behavior): hire returns the gates + the candidate, read-only;
    # run_audit returns the real audit result. (The radar_* tools are network-bound — exercised live in test_funnel.)
    h = server.hire("Jane Doe — ex-Stripe engineer, led payments reliability, GPA 3.9")
    record("problem-solving" in h and "committee" in h and "Jane Doe" in h,
           "hire tool returns the selection gates + the candidate (advisory, read-only)")
    record("engine.propose('hire'" not in h and "engine.apply" not in h,
           "hire tool writes nothing (no engine call in its output)")
    a = server.run_audit()
    record("AUDIT GREEN" in a, "run_audit tool returns the live audit result", a[:80])
    # tier-2 official BS docs must be listable AND resolvable via the sources tools (they live in sources/hiring/)
    ls = server.list_sources()
    record("bsp-selection-process" in ls and "bsp-talent-formula" in ls, "list_sources includes the tier-2 hiring docs (recursive)")
    record(server.get_source("bsp-selection-process").startswith("# Source"), "get_source resolves a tier-2 doc by id")
    # hire must be EU-AI-Act-aware: high-risk framing + refuse to be the decider
    hc = server.hire("pick the best for me")
    record("AI ACT" in hc.upper() and "high-risk" in hc.lower(), "hire tool carries the EU AI Act high-risk caveat")
    record("DECLINE the decision" in hc or "never picks" in hc, "hire tool refuses to be the decider (decision-support only)")
    for name in ("radar_universe", "radar_gates", "radar_company", "radar_loyalty", "radar_signals", "radar_scout", "hire", "run_audit"):
        ann = getattr(tools.get(name), "annotations", None)
        record(bool(ann and ann.readOnlyHint), f"annotation readOnlyHint on {name} (never writes the model)")

    # ---- search must cover the WHOLE model, not just object-nodes (defect-to-test) ----
    # 'margin of safety' is a will refusal that lives ONLY in will.md; search once returned
    # "No matches" because it scanned world-model/capabilities/interfaces nodes but never the
    # top-level docs (will, ontology, analysis, foundations). It must find them now.
    record("will.md" in server.search("margin of safety"),
           "search covers the will (the margin-of-safety refusal is findable)")
    record("bending-spoons-as-an-intelligence.md" in server.search("knowledge-flywheel"),
           "search covers the analysis thesis")
    record("foundations/ontology.md" in server.search("semantic"),
           "search covers the foundations contracts")
    # regression guard: it STILL scans the object-nodes it always did
    record(any("businesses/" in ln for ln in server.search("semantic").splitlines()),
           "search still finds world-model node content")
    record("No matches" in server.search("zzz-not-a-real-token-zzz"),
           "search returns a clean no-match for an absent token")

    # ---- every capability must be retrievable AND listed (keeps docs/try-it.md honest) ----
    CAPS = ["market-radar", "screen-target", "deal-value", "deal-diligence", "deal-optimize",
            "talent", "retire", "finance", "capital-allocation", "deal-monitor",
            "portfolio-impermanence", "product-users"]
    listed = server.list_capabilities()
    for c in CAPS:
        contract = server.get_capability(c)
        record(contract.startswith("---") and "title:" in contract, f"capability retrievable: {c}", contract[:60])
        record(f"{c}.md" in listed, f"capability listed by list_capabilities: {c}")

    # ---- the capability≠kinetic distinction must stay documented (defect-to-test) ----
    cap_readme = ROOT / "capabilities" / "README.md"
    record(cap_readme.exists() and "kinetic" in cap_readme.read_text(encoding="utf-8").lower(),
           "capabilities/README documents the kinetic layer (a capability is not an action)")
    foundc = (ROOT / "foundations" / "org-as-an-intelligence.md").read_text(encoding="utf-8").lower()
    record("do not conflate" in foundc,
           "foundations §3 carries the scope note: a capability is not an action")
    ls_doc = (server.list_capabilities.__doc__ or "").lower()
    record("kinetic" in ls_doc,
           "list_capabilities docstring names its output the kinetic contracts")

    # ---- README install command must be zsh/macOS-robust (defect-to-test) ----
    # a beginner on macOS zsh hit `zsh: command not found: pip` following a bare `pip install`.
    # the README must use `python3 -m pip` (bare `pip` is not guaranteed on PATH).
    import re as _re
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    record("python3 -m pip install -r mcp/requirements.txt" in readme,
           "README install step uses `python3 -m pip` (not bare pip)")
    record(not _re.search(r'(?m)(^|[^m] )pip install', readme),
           "README has no bare `pip install` (would break on macOS zsh)")

    # ---- radar tools must route by user intent (defect-to-test) ----
    # a Desktop client asked "find EU-listed companies in Italy $50M–$5B" and mis-picked radar_scout
    # (HN/Reddit chatter, needs a name) over radar_universe (name-free discovery), then answered from
    # outside the model with a company it named itself.
    uni_doc = (server.radar_universe.__doc__ or "").lower()
    scout_doc = (server.radar_scout.__doc__ or "").lower()
    record("find" in uni_doc and ("region='eu'" in uni_doc or "italy" in uni_doc),
           "radar_universe docstring routes 'find companies by geography + band' here")
    record("radar_universe" in scout_doc and "not" in scout_doc,
           "radar_scout docstring says it is not discovery and redirects to radar_universe")

    # ---- the connection guide must tell users about RADAR_CONTACT (defect-to-test) ----
    # a Desktop user connected the server and hit EDGAR 403 on the US radar because the
    # setup guide never mentioned the RADAR_CONTACT env var that SEC EDGAR requires.
    record("RADAR_CONTACT" in readme,
           "README connection guide documents RADAR_CONTACT (the live-radar env var)")

    # ---- the live tools ship an acceptable-use / data-sources policy (defect-to-test) ----
    policy = ROOT / "mcp" / "POLICY.md"
    ptext = policy.read_text(encoding="utf-8").lower() if policy.exists() else ""
    record(policy.exists() and all(s in ptext for s in ("edgar", "radar_contact", "reddit", "≤10 req")),
           "mcp/POLICY.md documents the live data sources + RADAR_CONTACT + rate limits")

    # ---- 'show me the portfolio' must route to the model, not the web (defect-to-test) ----
    # a Desktop client asked for the portfolio, saw only the radar tier, wrongly concluded the
    # connector was 'just an acquisition radar', and offered to pull the portfolio from the web.
    ov = (server.overview.__doc__ or "").lower()
    ln = (server.list_nodes.__doc__ or "").lower()
    record("portfolio" in ov and "not the web" in ov,
           "overview surfaces the held portfolio and names the model as the source (not the web)")
    record("portfolio" in ln and "business" in ln and "not the web" in ln,
           "list_nodes routes 'the portfolio' to type='business' (authoritative, not the web)")

    # ---- 'how strong is a brand right now' must route to radar_loyalty, not a raw web search ----
    # a Desktop client asked about Evernote's brand; radar_loyalty said "for a candidate", so the model
    # thought it didn't apply to a HELD business and web-searched instead (defect-to-test).
    ly = (server.radar_loyalty.__doc__ or "").lower()
    record("brand" in ly and "held" in ly and "[to-validate" in ly,
           "radar_loyalty routes brand-strength for a held brand too (not just an acquisition candidate)")

    # ---- 'run the search, names come out screened' must route to radar_discover (defect-to-test) ----
    # a user wanted discovery to OUTPUT a screened shortlist automatically (no tickers to supply);
    # radar_universe alone only dumps the raw 2,563. radar_discover chains universe→auto-gate→survivors.
    dv = (server.radar_discover.__doc__ or "").lower()
    record("run the search" in dv and "names out" in dv,
           "radar_discover routes 'run the search / find targets → screened names out, no tickers'")

    # ---- the SIC/HQ index must ship so discover screens the WHOLE universe, not a live slice ----
    _cache_f = ROOT / ".claude" / "skills" / "radar-sweep" / "data" / "edgar_sic_hq.json"
    _n_idx = len(json.loads(_cache_f.read_text(encoding="utf-8")).get("sic_hq", {})) if _cache_f.exists() else 0
    record(_n_idx > 2000, f"edgar_sic_hq index shipped ({_n_idx} filers) — discover evaluates the full universe")

    # ---- the PRIVATE-target watchlist ships (listed EDGAR/ESEF is not the only source) ----
    _wl = ROOT / ".claude" / "skills" / "radar-sweep" / "data" / "watchlist.csv"
    _wl_rows = ([l for l in _wl.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")][1:] if _wl.exists() else [])
    record(_wl.exists() and "radar_watchlist" in tools and len(_wl_rows) > 90,
           f"private-target watchlist ships ({len(_wl_rows)} brands) + radar_watchlist exposes it")

    # ---- no framework/author name shipped in a live .py tool description (rule 9; audit lints only .md/.csv) ----
    # "Dorsey" once shipped in a live docstring because audit.py's banned scan skips .py — guard the code too.
    for _pyf in ("server.py", "engine.py"):
        _src = (ROOT / "mcp" / _pyf).read_text(encoding="utf-8")
        _bad = _re.findall(r"(?i)palantir|dorsey|botha|foundry|sequoia", _src)
        record(not _bad, f"mcp/{_pyf} ships no framework/author name (rule 9)", _bad[:3])

    # ---- radar_discover formats the screened shortlist right (defect-to-test: it had no behavioral test) ----
    _orig_radar = server._radar_mod
    try:
        server._radar_mod = lambda: (type("R", (), {"discover": lambda self, y, c: {
            "total_in_band": 2000, "screened": 150, "errored": 0, "survivors": [
                {"name": "Acme SaaS", "revenue_m": 120, "hq": "CA", "sic": "Services-Prepackaged Software",
                 "region": "PASS", "sector": "PASS"},
                {"name": "RealtyCo Trust", "revenue_m": 90, "hq": "NY", "sic": "Real Estate Investment Trusts",
                 "region": "PASS", "sector": "JUDGE"}]}})(), {})
        out_d = server.radar_discover("us")
        record("Acme SaaS" in out_d and "1 more" in out_d and "RealtyCo" not in out_d,
               "radar_discover: PASS names are the shortlist, JUDGE counted (not named)", out_d[:120])
        server._radar_mod = lambda: (type("R", (), {"discover": lambda self, y, c: {
            "total_in_band": 2000, "screened": 150, "errored": 150, "survivors": []}})(), {})
        out_e = server.radar_discover("us")
        record("unreachable" in out_e and "rate-limit" in out_e,
               "radar_discover: a rate-limited run is not a false 'found nothing'", out_e[:120])
        record("currently auto-screens" in server.radar_discover("eu"),
               "radar_discover(eu) redirects to radar_universe (US-only auto-screen)")
    finally:
        server._radar_mod = _orig_radar

asyncio.run(main())
print(json.dumps(R))
