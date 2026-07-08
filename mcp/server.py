"""MCP server for the Bending Spoons world model.

Serves the markdown + git world model (the model at the repo root, the declared
analysis, the shared `will.md`, `foundations/`, and `sources/`) over the
Model Context Protocol. The markdown is the truth; this server only *serves* it.
Composition and execution of the skills stays LLM-side and human-gated — the
server exposes the contracts and the data, it does not act on the world by itself.

Run:  python server.py           (stdio transport, for an MCP client)
Deps: pip install -r requirements.txt   (mcp, pyyaml, pydantic)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

import yaml
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel

# The repo root is the parent of this mcp/ folder.
ROOT = Path(__file__).resolve().parent.parent
MODELS = {"observed": ROOT}  # flattened: the model lives at the repo root
SOURCES = ROOT / "sources"

mcp = FastMCP("bending-spoons-world-model")

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


# ----------------------------- helpers -----------------------------
def _parse_md(path: Path) -> tuple[dict, str]:
    """Split a node file into (yaml frontmatter dict, prose body)."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), m.group(2)


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _resolve(path: str) -> Path:
    """Resolve a repo-relative path safely (no escaping the repo)."""
    p = (ROOT / path).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError(f"path escapes the repo: {path}")
    return p


def _iter_nodes(model: str):
    """Yield every .md node under a model folder ('observed')."""
    base = MODELS.get(model)
    if not base or not base.exists():
        return
    for sub in ("world-model", "capabilities", "interfaces"):
        d = base / sub
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.md")):
            if f.name.lower() == "index.md":
                continue
            yield f


def _which_models(model: str) -> list[str]:
    return list(MODELS) if model in ("both", "all", "") else [model]


def _top_docs():
    """The top-level model documents `search` must also cover. They are NOT object-nodes,
    so `_iter_nodes`/`list_nodes` deliberately exclude them — but they are first-class,
    queryable model content (the will's refusals, the ontology spine, the analysis thesis,
    the two contracts). Omitting them from search is a silent blind spot (e.g. 'margin of
    safety' lives only in will.md)."""
    for n in ("will.md", "ontology.md", "bending-spoons-as-an-intelligence.md", "AGENTS.md",
              "foundations/ontology.md", "foundations/org-as-an-intelligence.md"):
        f = ROOT / n
        if f.exists():
            yield f


# ----------------------------- tools -----------------------------
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def overview() -> str:
    """Entry point — READ THIS FIRST: what this world model is and how it is laid out.

    This IS Bending Spoons as a queryable model, grounded in its filings — NOT just an acquisition
    radar. It holds the company's HELD PORTFOLIO (17 businesses: Evernote, WeTransfer, Vimeo, AOL,
    Eventbrite, Brightcove, komoot, Meetup…), the deals, the capabilities, the will, and the
    interfaces. For the portfolio call list_nodes('business'). The facts live HERE — answer from
    these tools, not the web. Returns the repo README (the model + the declared analysis).
    """
    parts = []
    for name in ("README.md",):
        f = ROOT / name
        if f.exists():
            parts.append(f"===== {name} =====\n{f.read_text(encoding='utf-8')}")
    return "\n\n".join(parts) if parts else "No overview files found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_nodes(model: str = "both", type: Optional[str] = None,
               status: Optional[str] = None) -> str:
    """List the nodes of the world model. list_nodes(type='business') is THE PORTFOLIO — the companies
    Bending Spoons actually owns (Evernote, WeTransfer, Vimeo, AOL, Eventbrite, Brightcove, komoot,
    Meetup, Remini, StreamYard, Splice, Issuu…), 17 in all. This is the authoritative,
    filing-grounded source for the portfolio — use it, not the web.

    Args:
      model: 'observed' (the only model; kept for interface stability).
      type:  optional filter on the node's `type` — business = the held portfolio; also interface, tool,
             spooners, founders, deal, facility, target, action, function, gap.
      status: optional filter on `status` (confirmed / proposed).
    Returns one line per node: model/path — type/status — title.
    """
    rows = []
    for mdl in _which_models(model):
        for f in _iter_nodes(mdl):
            meta, _ = _parse_md(f)
            if type and str(meta.get("type", "")).lower() != type.lower():
                continue
            if status and str(meta.get("status", "")).lower() != status.lower():
                continue
            rows.append(f"{_rel(f)}  —  {meta.get('type','?')}/{meta.get('status','?')}  —  "
                        f"{meta.get('title', f.stem)}")
    return "\n".join(rows) if rows else "No matching nodes."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_node(path: str) -> str:
    """Return the full content of one node by its repo-relative path.

    Example path: 'world-model/company/platform.md'. Use list_nodes or
    search to discover paths.
    """
    f = _resolve(path)
    if not f.exists():
        return f"Not found: {path}"
    return f.read_text(encoding="utf-8")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(text: str, model: str = "both") -> str:
    """Full-text search across the whole model.

    Covers the world-model nodes, the capabilities and interfaces, AND the top-level model
    documents (the will, the ontology spine, the analysis thesis, the two foundations
    contracts). Returns matching files with the lines that matched. Case-insensitive.
    """
    q = text.lower()
    out, seen = [], set()

    def scan(f: Path):
        if f in seen or not f.exists():
            return
        seen.add(f)
        body = f.read_text(encoding="utf-8")
        hits = [ln.strip() for ln in body.splitlines() if q in ln.lower()]
        if hits:
            out.append(f"### {_rel(f)}\n" + "\n".join(f"  · {h}" for h in hits[:5]))

    for mdl in _which_models(model):
        for f in _iter_nodes(mdl):
            scan(f)
    for f in _top_docs():
        scan(f)
    return "\n\n".join(out) if out else f"No matches for '{text}'."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_capability(name: str, model: str = "observed") -> str:
    """Return a capability / skill contract by name.

    In `observed`, capabilities live under capabilities/actions/ (market-radar,
    screen-target, deal-value, deal-diligence, deal-optimize, talent, retire, finance) and
    capabilities/functions/ (deal-monitor, capital-allocation,
    portfolio-impermanence, product-users). The model's audit is a service
    tool (mcp/audit-contract.md), not a subject capability.
    (The Platform tools — Minerva, Juno, Janus/Orion, Pico/Lumen/Abacus, Role
    Model — are OBJECTS, under world-model/company/tools/, not capabilities.)
    The contract is returned for the LLM/human to compose; the server does not run it.
    """
    base = MODELS.get(model, MODELS["observed"])
    for f in (base / "capabilities").rglob("*.md"):
        if f.stem == name or f.stem == name.replace(" ", "-").lower():
            return f.read_text(encoding="utf-8")
    return (f"Capability '{name}' not found under {model}/capabilities/. "
            f"Try list_capabilities.")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_capabilities(model: str = "observed") -> str:
    """List the model's kinetic contracts, grouped by folder: the ACTIONS (write objects)
    and FUNCTIONS (read them) of ontology.md §2. NOTE: these are the ontology's kinetic
    layer, which *realize* the org's composable capabilities — not the same as a "capability"
    in the composable-competency sense (the invocable competency); see foundations/org-as-an-intelligence.md §3."""
    base = MODELS.get(model, MODELS["observed"]) / "capabilities"
    if not base.exists():
        return f"No capabilities/ under {model}."
    rows = []
    for f in sorted(base.rglob("*.md")):
        rows.append(f"{f.relative_to(base)}  —  {_parse_md(f)[0].get('title', f.stem)}")
    return "\n".join(rows) if rows else "None."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def will() -> str:
    """Return the will (problem → mission → intent → constraints).

    Shared by the model and the analysis: the volition does not change; the
    structure would. The will guides the intelligence layer.
    """
    f = ROOT / "will.md"
    return f.read_text(encoding="utf-8") if f.exists() else "will.md not found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ontology(model: str = "observed") -> str:
    """Return the typed spine (objects, links, kinetic actions, flywheel) for a model."""
    f = MODELS.get(model, MODELS["observed"]) / "ontology.md"
    return f.read_text(encoding="utf-8") if f.exists() else f"{model}/ontology.md not found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def analysis() -> str:
    """Return the repo's one declared thesis.

    The model (at the repo root) states only confirmed facts; this returns the
    analysis of how the subject would reorganize as an intelligence —
    deliberately an essay, never a second model — plus the generic org
    contract it instantiates.
    """
    parts = []
    for rel in ("bending-spoons-as-an-intelligence.md", "foundations/org-as-an-intelligence.md"):
        f = ROOT / rel
        if f.exists():
            parts.append(f"===== {rel} =====\n{f.read_text(encoding='utf-8')}")
    return "\n\n".join(parts) if parts else "analysis sources not found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def foundations() -> str:
    """Return the two contracts the model rests on: the ontology contract (how it
    is structured) and the org-as-an-intelligence contract (how it is organized)."""
    parts = []
    for rel in ("foundations/ontology.md", "foundations/org-as-an-intelligence.md"):
        f = ROOT / rel
        if f.exists():
            parts.append(f"===== {rel} =====\n{f.read_text(encoding='utf-8')}")
    return "\n\n".join(parts) if parts else "foundations/ not found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_sources() -> str:
    """List the captured sources every fact is anchored to (the two official SEC
    filings plus any press/theory captures). Facts cite bsp-f1 or bsp-424b4."""
    if not SOURCES.exists():
        return "No sources/."
    rows = []
    for f in sorted(SOURCES.rglob("*.md")):  # recursive — includes sources/hiring/ (tier-2 official BS docs)
        meta, _ = _parse_md(f)
        sid = meta.get("id") or f.stem  # tier-2 hiring docs cite by stem (e.g. bsp-selection-process), no frontmatter
        rows.append(f"{f.relative_to(SOURCES)}  —  id: {sid}  —  {meta.get('title', f.stem)}")
    return "\n".join(rows)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_source(name: str) -> str:
    """Return a captured source by filename or id (e.g. 'bsp-f1', 'bsp-424b4').

    Note: the large *-fulltext.txt captures are not returned in full; use search
    to find a fact and its ~L line reference, then read the filing directly.
    """
    if not SOURCES.exists():
        return "No sources/."
    for f in sorted(SOURCES.rglob("*.md")):  # recursive — resolves tier-2 docs like 'bsp-selection-process'
        meta, _ = _parse_md(f)
        if f.stem == name or f.name == name or meta.get("id") == name:
            return f.read_text(encoding="utf-8")
    return f"Source '{name}' not found."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def activate_agent(name: str) -> str:
    """Return the contract of an activatable agent loop.

    The continuous loops are `market-radar` (upstream discovery) and
    `deal-monitor` (downstream, watches the held portfolio). This returns the
    agent's contract so a client can run the loop; the server does not run it,
    and any action that changes the model or acts outward is human-gated.
    """
    for mdl in ("observed",):
        base = MODELS[mdl] / "capabilities"
        if not base.exists():
            continue
        for f in base.rglob("*.md"):
            if f.stem == name:
                return f.read_text(encoding="utf-8")
    return (f"Agent '{name}' not found. The activatable agents are 'market-radar' "
            f"and 'deal-monitor'.")


# ----------------------------- action engine (two-phase execution) -----------------------------
import engine as _engine


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False, openWorldHint=False))
def propose_action(action: str, params: dict) -> str:
    """Propose an action against the world model — phase 1 of 2 (writes NOTHING).

    Validates parameters and the contract's submission criteria, computes the
    transaction as a concrete diff, and stores a pending proposal. Actions:
    source, screen, underwrite, close, transform, retire, finance (talent is
    advisory in v1). Human-gated actions can only be applied with an approver.
    """
    try:
        prop = _engine.propose(action, params)
    except Exception as e:
        return f"REFUSED: {e}"
    return json.dumps(prop, indent=2, ensure_ascii=False)


class _Approval(BaseModel):
    approved_by: str


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=False, openWorldHint=False))
async def apply_action(proposal_id: str, ctx: Context, approved_by: str = "") -> str:
    """Apply a pending proposal — phase 2 of 2 (the write-back).

    Enforces the governance gate: a human-gated proposal without an approver
    triggers an ELICITATION (accept/decline) asking the human for their name;
    if the client does not support elicitation, it refuses. Then: write-back,
    audit, commit only if green — full rollback if red.
    """
    if not approved_by:
        pend = {p["id"]: p for p in _engine.pending()}
        prop = pend.get(proposal_id)
        if prop and prop.get("gate") == "human":
            try:
                r = await ctx.elicit(
                    message=f"Proposal {proposal_id} ({prop['action']}) is human-gated by its contract. "
                            f"Approve the write-back? Enter your name to approve.",
                    schema=_Approval)
                if r.action == "accept" and r.data:
                    approved_by = r.data.approved_by
                else:
                    return f"DECLINED: {proposal_id} not applied (elicitation: {r.action})."
            except Exception:
                pass  # client without elicitation support → engine will refuse below
    try:
        prop = _engine.apply(proposal_id, approved_by or None)
    except Exception as e:
        return f"REFUSED: {e}"
    return f"APPLIED {prop['id']} (approved by {prop['approved_by']}); audit green, committed."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_proposals() -> str:
    """List pending/applied/rejected action proposals (the engine's working state)."""
    rows = [f"{p['id']}  {p['status']}  gate={p['gate']}  files={sorted({e['file'] for e in p['diff']})}"
            for p in _engine.pending()]
    return "\n".join(rows) or "No proposals."


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False, openWorldHint=False))
def reject_action(proposal_id: str, reason: str = "") -> str:
    """Reject a pending proposal (the human gate saying no)."""
    try:
        p = _engine.reject(proposal_id, reason)
    except Exception as e:
        return f"REFUSED: {e}"
    return f"REJECTED {p['id']}: {reason or 'no reason given'}"


# ----------------------------- radar (scouting), hire, audit — the rest of the loop, MCP-native -----------------------------
# The market-radar sensing tier and the hiring assistant were CLI/skill-only; these tools expose them so
# the whole funnel (scout → screen → underwrite → close → transform → hire) is drivable from any MCP client.
import importlib.util as _ilu

_RADAR_PATH = ROOT / ".claude/skills/radar-sweep/scripts/radar_sweep.py"
_radar = None
_thesis = None


def _radar_mod():
    """Load the radar module + the default thesis once (lazy — the thesis reads the model's own csvs).
    Raises FileNotFoundError with a clear message if the radar script is absent; the tools below turn any
    load failure into an honest 'radar unavailable' string rather than a raw traceback. Cache is keyed on
    _thesis so a failed load never leaves a half-initialized module cached."""
    global _radar, _thesis
    if _thesis is None:
        if not _RADAR_PATH.exists():
            raise FileNotFoundError(f"radar script not found at {_RADAR_PATH}")
        spec = _ilu.spec_from_file_location("radar_sweep", _RADAR_PATH)
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _thesis = mod.load_thesis()   # assign the module LAST, and only after the thesis loads
        _radar = mod
    return _radar, _thesis


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_universe(year: str = "CY2024", region: str = "us", countries: str = "") -> str:
    """FIND / LIST acquisition candidates by geography + revenue band — START HERE for requests like
    "find companies in Italy / Europe / the US with $50M–$5B revenue I could acquire". This is the
    mechanical TOP of the funnel: every listed company with in-band revenue, owned/pipeline names removed.
    region='eu' (ESEF; set countries='IT' for Italy, or 'IT,DE,FR') or region='us' (SEC frames).
    Do NOT use radar_scout to discover companies — that is chatter on a name you already have.
    Values are [derived]; the US tier needs RADAR_CONTACT set for SEC EDGAR."""
    r, cfg = _radar_mod()
    if region.lower() == "eu":
        cc = [c.strip().upper() for c in countries.split(",") if c.strip()] or None
        u = r.eu_universe(year, cfg, cc, 150)
        rows = "\n".join(f"- {n} ({c}) — {m:,.0f}M {cur}" for n, m, cur, c in u["in_band"][:40])
        cap = " [revenue-fetch capped; narrow --countries or ask for more]" if u["capped"] else ""
        return (f"EU universe {year}: {u['enumerated']} ESEF filings enumerated, {len(u['in_band'])} in-band "
                f"(of {u['fetched']} fetched){cap}.\n{rows or '(none in band)'}")
    yr = year if year.upper().startswith("CY") else "CY" + year
    u = r.universe(yr, cfg)
    if not u["in_band"] and u["errors"]:
        return "US universe unavailable: " + "; ".join(u["errors"]) + "  (is RADAR_CONTACT set for SEC EDGAR?)"
    rows = u["in_band"]                          # (cik, name, m)
    sample = rows[::max(1, len(rows) // 25)][:25]
    return (f"US universe {yr}: {len(rows)} companies in band (of {u['reporting']} unique filers; "
            f"{u['dropped_owned_pipeline']} owned/pipeline removed). Evenly-sampled slice — raw, "
            f"no sector screen (use radar_discover to get the screened in-thesis names):\n"
            + "\n".join(f"- {n} — ${m:,.0f}M" for c, n, m in sample))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_discover(region: str = "us", countries: str = "") -> str:
    """RUN THE SEARCH and get screened candidate NAMES OUT automatically — no tickers to supply. This is
    the tool for "find targets" / "who could Bending Spoons buy": it pulls the in-band listed universe and
    auto-applies the mechanical gates (revenue band · HQ · digital sector) across the WHOLE in-band universe
    (via a prebuilt SIC/HQ index — every filer, not a sample), returning ONLY the in-thesis survivors
    (digital PASS + JUDGE) by name — so you get a real shortlist, not a raw multi-thousand-name dump.
    region='us' (SEC EDGAR; needs RADAR_CONTACT). Honest limits: the SIC sector call is coarse (PASS is a
    mechanical flag, not thesis-fit; JUDGE = human check), and it sees LISTED filers only (private targets —
    where many real deals originate — never surface here). [derived from EDGAR; point-in-time index]."""
    r, cfg = _radar_mod()
    if region.lower() != "us":
        return ("radar_discover currently auto-screens region='us' (SEC). For Europe, radar_universe(region='eu', "
                "countries='IT,…') returns the in-band listed set directly; ESEF carries no sector code, so screen those by judgment.")
    d = r.discover("CY2024", cfg)
    passes = [s for s in d["survivors"] if s["sector"] == "PASS"]
    judge = [s for s in d["survivors"] if s["sector"] == "JUDGE"]
    if not passes and not judge:
        uni_err = d.get("universe_errors") or []
        if uni_err and d.get("total_in_band", 0) == 0:   # the revenue-frame fetch failed — NOT an empty universe
            return ("US universe UNAVAILABLE — the revenue-frame fetch failed: " + "; ".join(uni_err) +
                    "  (likely SEC rate-limiting; retry). This is NOT a genuine empty result — the universe "
                    "could not be read. Is RADAR_CONTACT set for SEC EDGAR?")
        er = d.get("errored", 0)
        hint = (f" — but {er} of {d['screened']} fetches were unreachable (likely SEC rate-limiting; retry)"
                if er else ". Is RADAR_CONTACT set for SEC EDGAR?")
        return f"US universe: {d['total_in_band']} in-band; screened {d['screened']}, found no in-thesis survivors{hint}"
    passes.sort(key=lambda s: -s["revenue_m"])   # biggest/most-recognizable first
    lines = [f"US in-thesis shortlist — auto-screened ALL {d['screened']} of {d['total_in_band']} in-band filers; "
             f"{len(passes)} cleared band · US HQ · digital sector (showing top 25 by revenue) "
             f"[derived from EDGAR; SIC coarse — PASS is a mechanical flag, not thesis-fit]:"]
    for s in passes[:25]:
        lines.append(f"- {s['name']} — ${s['revenue_m']:,}M · {s['hq']} · {s['sic']}")
    if judge:
        lines.append(f"\n+ {len(judge)} more cleared band + US HQ but the SIC didn't read as digital "
                     f"(JUDGE — a human call; SIC codes lag the real business).")
    return "\n".join(lines)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def radar_watchlist() -> str:
    """The PRIVATE-target watchlist — candidate brands that are NOT SEC/ESEF filers, so the listed radar
    (radar_universe / radar_discover) can NEVER surface them. This is the human perimeter: [to-validate —
    press only] hypotheses (famous consumer/prosumer brands past their peak), not model facts. Discovery of
    private targets can't come from filings — a human seeds this list; the machine SCORES it. To score any
    name, run radar_loyalty (brand strength) and radar_scout (distress / ownership) — those signals don't
    need SEC filings. Curate the list at .claude/skills/radar-sweep/data/watchlist.csv."""
    path = ROOT / ".claude" / "skills" / "radar-sweep" / "data" / "watchlist.csv"
    if not path.exists():
        return "No watchlist.csv found — seed private candidates there."
    import csv as _csv
    rows = list(_csv.DictReader(ln for ln in path.read_text(encoding="utf-8").splitlines()
                                if ln.strip() and not ln.startswith("#")))
    out = [f"Private-target watchlist — {len(rows)} human-curated candidates [to-validate — press only]; "
           f"score any with radar_loyalty + radar_scout (no SEC filing needed):"]
    for r in rows:
        out.append(f"- {r.get('brand','?')} ({r.get('category','')}) — {r.get('why','')}")
    return "\n".join(out)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_gates(tickers: str) -> str:
    """Per-candidate mechanical gates (revenue band · HQ region · digital sector) for US-listed tickers
    (comma-separated, e.g. 'SONO, PINS'). [derived from EDGAR]. Needs RADAR_CONTACT. For EU/unlisted names use radar_company."""
    r, cfg = _radar_mod()
    out = []
    for tk in [t.strip() for t in tickers.split(",") if t.strip()]:
        g = r.gates(tk, cfg)
        if "error" in g:
            out.append(f"- {tk}: {g['error']}")
            continue
        out.append(f"- {tk}: revenue {g.get('revenue_m', 'n.d.')} → band {g.get('gate_band', '?')} · "
                   f"HQ {g.get('hq', '?')} → {g.get('gate_region', '?')} · {g.get('sic', '?')} → {g.get('gate_sector', '?')}")
    return "\n".join(out) or "no tickers given"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_company(name: str) -> str:
    """Look up ONE specific EU-listed or unlisted candidate you already have, by legal name (not discovery —
    to FIND candidates by country + revenue band use radar_universe): GLEIF identity/HQ → ESEF revenue,
    honest n.d. for private companies (and a distinct 'UNAVAILABLE' if GLEIF is unreachable). [derived]."""
    r, cfg = _radar_mod()
    c = r.company(name, cfg)
    return "\n".join(f"- {k}: {v}" for k, v in c.items())


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_loyalty(brand: str, days: int = 30) -> str:
    """HOW STRONG IS A BRAND RIGHT NOW — the live brand-strength card for ANY brand: a HELD portfolio
    business (e.g. Evernote, WeTransfer) OR an acquisition candidate. USE THIS for brand-strength /
    current-sentiment questions instead of an ad-hoc web search. Pulls public signals: committed base
    (App Store rating volume/avg) · brand-interest trend (Wikipedia) · community (subreddit). Needs no
    RADAR_CONTACT (App Store / Wikipedia / Reddit, not EDGAR). All [to-validate — press only], never a
    fact; NRR proper enters at diligence. It does NOT cover review-site (Trustpilot) or press sentiment,
    so supplement with the web only if needed — and mark that too [to-validate — press only]."""
    r, _cfg = _radar_mod()
    return "\n".join(r.loyalty_card(brand, days))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_signals(days: int = 30) -> str:
    """Ownership signals: recent 8-Ks with sale/divestiture language + ownership-change filings
    (SC 13D · SC 13E-3 · 25/15), sector-filtered per the thesis. Each is a 'buyable-soon' signal. Needs RADAR_CONTACT."""
    r, cfg = _radar_mod()
    lines = [f"8-K sale/divestiture language (last {days}d):"]
    for e in r.edgar_events(days, cfg):
        lines.append(f"- {e['query']}: unavailable ({e['error']})" if "error" in e
                     else f"- [{e.get('date', '')}] {e.get('company', '')} · {e.get('sic', '')}")
    fw = r.form_watch(min(days, 5), cfg)
    lines.append(f"ownership-change filings (last {min(days, 5)}d, {fw['reached']} index-days reached):")
    if not fw["hits"] and fw["reached"] == 0:
        lines.append("- UNAVAILABLE: no EDGAR daily index reachable — NOT an all-clear (set RADAR_CONTACT?)")
    for h in fw["hits"]:
        lines.append(f"- [{h['date']}] {h['form']}: {h['company']} · {h['sic']}")
    if len(lines) == 2:
        lines.append("- (none in the window)")
    return "\n".join(lines)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def radar_scout(query: str, days: int = 30) -> str:
    """Chatter sweep (Hacker News + Reddit) on a brand or theme you ALREADY have a name for. This is
    NOT a way to discover companies — to FIND candidates by country + revenue band use radar_universe.
    Blind to non-English and financial press, so silence here is source-blindness, not an all-clear.
    Buckets the hits on the watch signals (distress · ownership · momentum · valuation · ai-pressure ·
    loyal-base). Corroboration only — everything here is [to-validate — press only], never a fact.
    Owned/pipeline names are flagged."""
    r, cfg = _radar_mod()
    buckets = r.sweep(query, days, 25, cfg)
    hit = False
    lines = [f"chatter for '{query}' (last {days}d) — [to-validate — press only]:"]
    for sig, items in buckets.items():
        if not items:
            continue
        hit = True
        lines.append(f"{sig}:")
        for it in sorted(items, key=lambda x: x.get("score", 0) + x.get("comments", 0), reverse=True)[:4]:
            lines.append(f"  - [{it.get('src', '?')}] {it.get('title', '')[:110]} ({it.get('score', 0)}pts)")
    if not hit:
        lines.append("  (no bucketed chatter — try --days 90 or the press recipes in the radar-sweep skill)")
    return "\n".join(lines)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def hire(candidate_profile: str) -> str:
    """The hiring assistant (read-only, ADVISORY decision-support — it does NOT decide). Returns Bending
    Spoons' published selection funnel + gates and scores the candidate against them, for a human to weigh.
    Grounded in sources/hiring/ + the F-1 funnel. NOTE: scoring candidates is a high-risk use under the EU AI
    Act (Annex III §4) — a human must make the call, the candidate must be informed an AI assisted, and the
    gates must be applied without discrimination; this tool is built to support that, not to replace it."""
    return (
        "⚠️ EU AI ACT — HIGH-RISK USE (Annex III §4, recruitment/candidate evaluation). This is decision-SUPPORT,\n"
        "not a decision. If asked to 'decide' or 'pick' — DECLINE the decision: a human must make the call\n"
        "(Art. 14 human oversight), the candidate must be informed an AI system assisted, the gates must be\n"
        "applied without discrimination, and a deployer using this on real candidates carries the Act's duties\n"
        "(oversight · transparency · logging). This tool assembles the case and STOPS; it never picks.\n\n"
        "HIRING ASSISTANT — score the candidate below against Bending Spoons' selection gates, then STOP at the\n"
        "committee (the human gate). Advisory and read-only: recommend, never assert a hire; write nothing.\n\n"
        "FUNNEL (sources/hiring/bsp-selection-process): screening (CV) → tasks (problem-solving · role-specific · "
        "behavioral) → interviews → references → committee (decision, independent of the direct lead — "
        "sources/hiring/bsp-talent-formula). Scale: ~800k applications → 286 hired, <0.04% (bsp-f1 ~L284).\n\n"
        "GATES (score each pass / judge / fail, mark provenance):\n"
        "  1. problem-solving — makes sense of unfamiliar problems\n"
        "  2. role-specific — expertise AND potential ('how fast you grow, not where you start')\n"
        "  3. behavioral — ownership · commitment · ambition · drive for exceptional results as a team\n"
        "  4. talent-over-experience — long-term potential outweighs current expertise\n"
        "  5. honesty — no offer if accomplishments are misrepresented (hard disqualifier)\n\n"
        "Use only the materials provided (CV / submitted work / links the candidate shared) — no autonomous "
        "scraping. Generate tasks/interview questions if useful, but you cannot fabricate the candidate's "
        "performance. Output: a per-gate verdict + a funnel position + a recommendation for the committee — never a decision.\n\n"
        f"CANDIDATE / REQUEST:\n{candidate_profile}"
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def run_audit() -> str:
    """Run the model's integrity audit (the mechanically-enforceable subset of the §5 invariants + the
    standing defect-to-test checks; see mcp/audit-contract.md for which invariants are mechanical vs
    review-verified) and return the result — green, or the exact defects. Read-only; runs under the
    server's own interpreter. Run it after any batch of edits."""
    import subprocess
    r = subprocess.run([sys.executable, "mcp/audit.py"], cwd=ROOT, capture_output=True, text=True)
    return (r.stdout or r.stderr).strip() or ("AUDIT GREEN" if r.returncode == 0 else "AUDIT RED (no output)")


if __name__ == "__main__":
    mcp.run()
