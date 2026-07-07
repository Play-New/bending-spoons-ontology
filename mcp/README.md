# mcp/ — the model's service tools

This directory is **not part of the model** — the model lives at the repo root (`ontology.md` · `world-model/` · `capabilities/` · `interfaces/`). What lives here is the machinery that **serves and guards** that model: the MCP server, the execution engine, and the audit. These are *model service tools* (Bending Spoons' own capabilities are the verbs in `capabilities/` — Bending Spoons audits deals, not this repo).

| file | role |
|---|---|
| `server.py` | the MCP server — exposes the model over the Model Context Protocol (read + two-phase propose/apply) |
| `engine.py` | the execution engine — propose/apply, human gates in code, audit-green-or-rollback, one git commit per action |
| `audit.py` | the runnable invariants — the mechanical subset of the §5 contract |
| `audit-contract.md` | the audit's contract (`type: service-tool`) — the full invariant list `audit.py` enforces |
| `tests/` | the full suite (engine · guards · skills/agents · radar · server · audit) |

The service layer has a **second half that cannot live here**: Claude Code discovers skills and workflows only under `.claude/`, so the `bsp-audit` skill and the `bsp-control-pass` workflow (which invoke `audit.py`) live there by runtime convention. Together they are the tools that maintain the model — distinct from both Bending Spoons' capabilities and the Platform objects.

---

## MCP server — the world model as a live connector

This exposes the Bending Spoons world model over the Model Context Protocol. The markdown + git model is the truth; this server *serves* it. Composition and execution of the skills stays LLM-side and human-gated — the server returns contracts and data, it never acts on the world by itself.

## What it exposes
**Tools (read + compose):**
- `overview()` — start here: the README (the model + the analysis, and how they relate).
- `list_nodes(type, status)` — enumerate the model's nodes; filter by `type`, `status`.
- `get_node(path)` — full content of one node by repo-relative path.
- `search(text, model)` — full-text search across nodes.
- `will()` — the will (problem → mission → intent → constraints), shared by the model and the analysis.
- `ontology(model)` — the typed spine + flywheel of the model.
- `analysis()` — the declared thesis: `bending-spoons-as-an-intelligence.md` + the generic org contract it instantiates.
- `foundations()` — the two contracts the model rests on (structure + organization), with the enforced §5 contract shape and the §6 security model.
- `list_capabilities(model)` / `get_capability(name, model)` — the runnable contracts. At the root: `capabilities/actions/` (market-radar, screen-target, deal-value, deal-diligence, deal-optimize, talent, retire, finance) and `capabilities/functions/` (deal-monitor, capital-allocation, portfolio-impermanence, product-users). The proprietary technologies (Minerva, Juno, Janus-Orion, Pico-Lumen-Abacus, Role Model) are **objects**, in `world-model/company/tools/`.
- `list_sources()` / `get_source(id)` — the captured sources (facts anchor to `bsp-f1` or `bsp-424b4`).
- `activate_agent(name)` — the contract for the continuous loops `market-radar` (upstream) and `deal-monitor` (downstream). The loop runs client-side; actions are human-gated.

**What it serves:** the model at the repo root (`ontology.md` · `world-model/` · `capabilities/` · `interfaces/`) — every node `status: confirmed` except the declared gap — plus the analysis (`status: proposed`). Reading `status` is how a client tells fact from thesis.

**Executing the actions (two-phase, human-gated):**
- `propose_action(action, params)` — phase 1: validates parameters and the contract's **submission criteria** (the underwriting hurdles, the ≤4.00 leverage covenant, the retire transition rules, property writability per §1), computes the **transaction as a concrete diff**, stores a pending proposal. Writes nothing.
- `apply_action(proposal_id, approved_by)` — phase 2: enforces the **governance gate** (a human-gated action refuses to run without an approver — GATE 1 for the walk-away price, GATE 2 for the close), performs the write-back (csv + node frontmatter, kept 1:1), **runs the audit, and commits only if green** — full rollback if red. Every applied action is a git commit that records the verb and the approver.
- `list_proposals()` / `reject_action(id, reason)` — the queue and the human's no.
`screen` applies auto (its write *is* the screen); `talent` is advisory in v1 (the Spooners backing is aggregate prose). The judgment tier stays LLM-side: an agent decides *what to propose*; the engine commits only the declared transaction, behind its gate.

**Scouting, hiring, audit (read-only — the rest of the loop, MCP-native so no terminal is needed):**
- `radar_universe(year, region, countries)` — the mechanical top of the funnel: in-band listed companies (US SEC frames, or EU ESEF). `radar_discover(region, countries)` — runs the universe AND auto-applies the mechanical gates (band · HQ · digital sector) across a slice, returning the in-thesis survivors by name (discovery that outputs a screened shortlist, no tickers). `radar_watchlist()` — the human-curated PRIVATE-target seed list (brands EDGAR/ESEF can't see; score them with radar_loyalty + radar_scout). `radar_gates(tickers)` — per-candidate gates (band · region · sector) for US tickers. `radar_company(name)` — the GLEIF→ESEF chain for EU/unlisted names. `radar_loyalty(brand)` — the brand-strength card. `radar_signals(days)` — ownership signals (8-K sale language + 13D/13E-3/25/15 filings). `radar_scout(query, days)` — HN/Reddit chatter, bucketed (`[to-validate — press only]`). The structured tiers need `RADAR_CONTACT` set for SEC EDGAR. See [POLICY.md](POLICY.md) for the live data sources and their acceptable-use terms (you are the requester; honor each source's rate limits).
- `hire(candidate_profile)` — the hiring assistant: returns the selection funnel + disclosed gates and scores the candidate; advisory, read-only, stops at the committee.
- `run_audit()` — the model's integrity audit (green / the exact defects).

With these, **the whole loop runs from any MCP client** — scout → screen → underwrite → close → transform → hire → audit — in natural language, with the human gate delivered as an elicitation, and no terminal.

## Run
```bash
cd mcp
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python server.py          # stdio transport
```

## Connect (Claude Desktop / any MCP client)
Add to the client's MCP config (adjust the absolute paths):
```json
{
  "mcpServers": {
    "bending-spoons-ontology": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/bending-spoons-ontology/mcp/server.py"]
    }
  }
}
```
Then, in the client: call `overview()` first, then `list_nodes` / `get_node` to explore, `get_capability` to pull a skill contract to run, and `analysis` to read the declared thesis.

## Customising the skills
The skills are contracts with explicit parameters (scouting criteria, valuation objective). A client customises a run by supplying those parameters when it composes the capability — e.g. `market-radar` can scout for undervalued mature businesses (the model's reading) or for user-bases + missing capabilities (the analysis's reading). Same skill, different parameters.
