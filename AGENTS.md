# AGENTS.md — the intelligence layer

This is the runtime of Bending Spoons modeled as an intelligence. It is not a folder of data; it is the only active part — the layer that reads the model and the will and **composes capabilities into action**. The intelligence lives here, in the system; the people are at the edge.

It composes over **the model at the root** (`ontology.md` · `world-model/` · `capabilities/` · `interfaces/`) — Bending Spoons as it is today. The analysis (`bending-spoons-as-an-intelligence.md`) argues how the *same* composition logic would run on a re-aimed capability set and a different central object — the loop changing from capital to knowledge (the generic move: `foundations/org-as-an-intelligence.md`). This file describes the logic of the present machine.

## What it composes on
- **`will.md`** (shared) — the *volere*: problem → mission → intent → constraints. The constraints are enabling: they let action happen at the edge without a hierarchy, not a list of prohibitions. Read the will first; it sets direction and the hard lines.
- **`ontology.md`** — the *sapere*, typed: objects, typed links, the kinetic action table, governance, and §3 the flywheel. The map of what exists and how it connects.
- **`world-model/company/`** and **`world-model/customer/`** — the two world models the will orients: what Bending Spoons *is* (the machine + the products-as-assets) and what it *serves* (product users + the market of targets). Grounded, cited to `sources/`.

## What it composes
- **`capabilities/`** — the kinetic primitives, made runnable, split into **`actions/`** (the verbs that write the model, each under a seven-field contract: source→`market-radar`, screen→`screen-target`, underwrite→`deal-value`, close→`deal-diligence`, transform→`deal-optimize`, the people-verbs→`talent` (advisory in v1 — no engine write-back), retire→`retire`, raise/refinance→`finance`) and **`functions/`** (read-only readings under the three-field contract input·computation·output: `deal-monitor` and the economic/customer readings `capital-allocation` / `portfolio-impermanence` / `product-users`). The model's own validator is NOT here — auditing this repo is a service of the model, not a capability of Bending Spoons; its contract lives at `mcp/audit-contract.md`, runnable as `mcp/audit.py`. The Platform tools (Minerva, Juno, Janus/Orion, Pico/Lumen/Abacus, Role Model) are **objects**, in `world-model/company/tools/`. The atomic building blocks the intelligence layer combines; they have no UI of their own.
- **Read-only projections** — the runtime can generate inspection surfaces over the model (e.g. a portfolio monitor) on demand; they are not authored as files. Interpretation — what the headline hides — is not a projection; it lives in the model (`capabilities/functions/capital-allocation.md`).

## How it acts (the composition rule)
Recognize a moment in the model, compose the capabilities that meet it, act — under the will's constraints. Two examples, grounded in the machine as modeled:
- A target crosses `market-radar`'s maturity threshold → compose `screen-target` then `deal-value` (underwrite to the IRR hurdle) → produce a walk-away price. **Stop at the gate.**
- A held business's retention drifts in `deal-monitor` → compose the Playbook levers (`deal-optimize`) and surface the move.

## The gates (non-negotiable)
The intelligence layer proposes; it does not decide the calls that are the edge's to make.
1. **Walk-away price** — after `deal-value`, a human approves the number before diligence.
2. **Negotiation and closing stay human** — the deliberate Bending Spoons discipline: the machine computes the maximum justifiable, the person holds the line at the table.
3. **Anything that changes the model or acts outward is `approval: human`**; only read-only projections run `auto`. The will's constraints (never sell, hold the hurdle, ≤3 layers, returns over growth) are checked on every composition.

## The loop it runs
```
market-radar ──▶ screen-target ──▶ deal-value ──[GATE: walk-away price]──▶ deal-diligence ──[GATE: negotiate/close, human]──▶ acquire ──▶ deal-optimize (transform)
     ▲                                                                                                                                          │
     │                                                          talent reallocated across ┐                                                    ▼
     └──── the customer signal (product-users, market-of-targets) feeds discovery ◀───── deal-monitor ◀──── transform (Platform) ────────────────┘
```
This is the **capital-flywheel** of the model. When the intelligence tries to compose a solution and a capability is missing, that failure is the roadmap — the clearest instance is `world-model/customer/cross-product-graph.md`, the moat it cannot yet compose because no unified customer graph exists. Building it is exactly what would turn the capital-flywheel into the knowledge-flywheel — the argument of `bending-spoons-as-an-intelligence.md`.

The loop is meant to **learn, not just repeat**: the return edges above (deal-monitor, product-users) are the model's **feedback layer** — realized outcomes recalibrating the capability that produced them (deal→business into sourcing/underwriting, growth into the transform playbook, a successful hire into the selection gates). An *outcome reading* into a *calibrate action* is what makes the org self-improving and runnable end to end (`ontology.md §3` loop ②; `README.md` → *Where this is going*).

## What earns a runnable (skill / agent / workflow)
The kinetic layer is modeled in full (`ontology.md §2`), but **not every verb becomes a skill, agent, or workflow** — only a **reproducible, parameterizable capability** does, so that anyone can do what Bending Spoons does, their way, by changing parameters. What is built:
- the **deal engine** — built end to end: the scouting → evaluation verbs (`source · screen · underwrite · close · transform`) each have an invocable skill, `deal-desk` orchestrates them, and `radar-sweep` scouts — parameterized by the thesis file (`.claude/skills/radar-sweep/theses/bending-spoons.yaml`), so another acquirer runs it their way.
- the **hiring assistant** — built as the read-only `/hire` skill: it runs a candidate through Bending Spoons' selection funnel and scores them against the disclosed gates (`sources/hiring/`), human-gated at the committee — the people-side twin of `screen`. **Advisory by design**: it drafts a recommendation and writes nothing, because the filings disclose only aggregate `Spooners` data (no per-person facts to write). Parameterizable — change the gates to hire for another company.
- the two internal transactions no one invokes to compose value — `raise / refinance` (treasury, fuel-side) and `retire` (a reactive wind-down triggered by `deal-monitor`) — stay **engine-only actions** (proposed through `engine.propose`), not verb skills.

## The MCP surface (what this exposes)
Exposed as an MCP server — **27 tools**, everything as tools (no `@mcp.resource`; the nodes are served read-only through query tools, which is what an LLM client consumes):
- **Node reads (read-only query tools)** = the model as queryable content: `overview`, `list_nodes`, `get_node`, `search`, `ontology`, `will`, `analysis`, `foundations`, `list_sources`, `get_source`, `list_capabilities`, `get_capability`.
- **The whole funnel (MCP-native, no terminal)** = scouting + hiring + audit as read-only tools: `radar_universe`, `radar_discover` (runs the universe + auto-applies the mechanical gates → in-thesis survivors by name), `radar_watchlist` (the human-curated PRIVATE-target seed list — listed radar can't see private brands), `radar_gates`, `radar_company`, `radar_loyalty`, `radar_signals`, `radar_scout` (parameterized by the thesis), `hire` (advisory selection scoring), `run_audit`.
- **Action tools** = the deal verbs behind the two-phase engine: `propose_action` · `apply_action` · `list_proposals` · `reject_action`. `raise`/`retire` go through `propose_action` (no verb skill); `hire`/`talent` is advisory in v1. The Platform primitives are objects, not tools; the model service tools (`mcp/audit.py`, the `bsp-audit` skill, the `bsp-control-pass` workflow) maintain the model itself.
- **Agents** = the continuous loops (`market-radar` upstream, `deal-monitor` downstream) — activatable via `activate_agent`.
- **Execution** = two-phase and human-gated (`propose_action` → `apply_action`): the engine (`mcp/engine.py`) validates the contract's submission criteria mechanically (hurdles, covenant, transitions, §1 writability), writes back csv+node 1:1, and commits only on a green audit — rollback otherwise. The gates in the contracts are enforced in code: a human-gated proposal cannot be applied without a named approver.
The world model (markdown + git) is the truth; the MCP is the layer that serves it. A derived structured view (yaml/db) can be projected from the ontology for querying, but the markdown stays authoritative.
