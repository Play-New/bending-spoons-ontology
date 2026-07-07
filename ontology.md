# Ontology — Bending Spoons (the model, today)

The index of the model: the object **types**, their **links**, the **actions**, and the **functions**. The data and the source citations live in the nodes (`world-model/`, `capabilities/`, the csvs); this file is the map. Bending Spoons is the **machine** that acquires, transforms, and compounds digital businesses — who it is and what it wants are in `will.md`; the objects below are its parts.

**Will** → `will.md` — what it wants and refuses (shared with the analysis, `bending-spoons-as-an-intelligence.md`).

---

## 1. Objects — the semantic layer

The entities that exist, and their links (object↔object only). Definitions, data, and F-1 grounding live in the linked nodes.

Central chain: a **`Deal`** is `of` a **`Target`** and `produces` a **`Business`**, which ships one or more **`Interface`s** — `Target → Deal → Business → Interface`.

- **`Business`** — ×17, the acquired company-as-asset (its *operating* data only; the acquisition price & PPA are the `Deal`'s; the app the user touches is the `Interface`). → `world-model/company/businesses/`
  - properties: name (= the title/primary key, the `business` column) · revenue · MAU · monthly-paying-customers · NRR · subscriber-tenure · ARPU · revenue mix (subscription / advertising / transaction / one-time) · acquisition channels (organic vs paid) · conversion rate · adj-operating margin · status (main / tail / excluded / retired) · lifecycle (acquired → transforming → optimized; the transform action's write-target)
  - links: *(none declared here — `Deal —produces→`, `Platform —operates→`, `Spooners —deployed-on→`, `Tool —deployed-across→`, `Interface —of→` are declared on those objects; the absence of any cross-business/customer link is the gap; `bending-spoons-as-an-intelligence.md` argues what would fill it)*
- **`Interface`** — ×18, the delivery surface: the app/site the user touches; a Business may ship several (Mosaic ships iTranslate and RoboKiller). → `interfaces/` (one node each + `interfaces.csv`)
  - properties: brand (= the title/PK, the `interface` column) · category · capabilities-delivered (bundled inside the interface today) · AI features shipped · status (live / sunset — an interface can die while its business lives; written by `transform`) *(the frontmatter `business:` field is the of-link FK, §4.5)*
  - links: `of`→Business (N:1, declared here once)
- **`Platform`** — the operating machine, "our most important product". → `world-model/company/platform.md`
  - properties: proprietary data (scale: >3.8B data points/day) · shared infrastructure (billing, hosting, engineering) · the codified method  *(a property is a value stored ON this object. Revenue-per-Spooner is a computed cross-object ratio → a `function`; company-level financials are Bending Spoons' consolidated results, attributes of no single object → the scoreboard, read by functions. Per-object financials — `Business.revenue`, `Deal.consideration` — ARE properties, of those objects.)*
  - link: `operates`→Business (the machine runs the businesses; `Tool`s declare `part-of`→Platform, `Spooners` declare `operates`→Platform)
- **`Tool`** — the proprietary technologies: Minerva · Juno · Janus/Orion · Pico/Lumen/Abacus · Role Model. → `world-model/company/tools/`
  - properties: name · function (what it does) · built / since · usage scale (data points/day, experiments/yr) · AI-based? · deployed-across-portfolio?
  - links: `part-of`→Platform · `deployed-across`→Business · inter-tool `consumes`/`reads`→Tool · Role Model `produces`→Spooners
- **`Spooners`** — the durable, reallocatable core team (vs the transient acquired staff). → `world-model/company/spooners.md`
  - properties: headcount · share of total FTE · talent-team size · redeployability (moved on short notice) · (revenue-per-Spooner is a `function` over `financials.csv`, not a stored property)
  - links: `deployed-on`→Business (reallocated across the portfolio) · `operates`→Platform
- **`Founders`** — the controlling group: the five who started it; the four class-A holders who hold control. → `world-model/company/founders.md`
  - properties: members & roles (Ferrari CEO · Patarnello head of Business Acquisitions · Danieli · Querella · Greber) · class-A holders (4 of 5) · votes per class A (5) · post-IPO voting power (82.71%) · super-voting floor (37.5M) · control-transfer rule (personal, non-transferable) · slate mechanism · employment agreements (none for CEO/vice-chair)
  - links: *(none — the will's founder-control constraint hooks here; that is what earns the node, §4.0)*
- **`Deal`** (Acquisition) — the acquisition event; its data is separate from the business it produces. → `world-model/company/deal.md` (backed by `deals.csv`)
  - properties: consideration · enterprise value · deal-type · IRR 65/25 · cohort · date · PPA {goodwill, customer base, IP, trademark}
  - links: `of`→Target · `produces`→Business
- **`Facility`** — a debt facility: the instrument the raise/refinance verb writes; the flywheel's fuel is borrowed here. → `world-model/company/facility.md` (backed by `facilities.csv`)
  - properties: name · type (term loan A / term loan B / RCF / bilateral) · currency · size · signed · status (active / drawn / partially drawn / repaid)
  - links: *(none — `capital-allocation` reads the stack; the leverage covenant hooks it)*
- **`Target`** — a company in the acquirable market (>1,000 businesses, ~$400B revenue). → `world-model/customer/market-of-targets.md`
  - properties *(= the `screen-target` gates, `bsp-f1`)*: revenue scale ($50M–$5B) · HQ (Europe / N. America) · product offering (digital: consumer or enterprise) · revenue model (self-serve / sales-led subs / advertising; not IT-services) · room-for-improvement · predictable earnings (retention) · owner willingness-to-sell · valuation level · AI-pressure on core
  - pipeline-state properties *(not gates — written by the §2 actions, per-target values undisclosed in the filings)*: status (shared property; set by `screen`) · irr {levered, unlevered} · walk-away price (set by `underwrite`)

Object **sets** (views, not types): **Portfolio** = the set of `Business` · **Market** = the set of `Target`.

---

## 2. Actions & functions — the kinetic layer

The shape: an **action** is a single transaction that **creates / modifies / deletes** objects, sets **properties**, or writes **links** — often function-backed, with a write-back record. A **function** only *computes a reading* (no write-back). Both live in `capabilities/`; grounded detail is in the node.

### Actions — write to the ontology
| action | transaction it commits | backed by |
|---|---|---|
| source | create / update `Target` | agent `market-radar` |
| screen | set `Target.status` (worth underwriting?) | `screen-target` |
| underwrite | set `Target.irr`, `Target.walk_away_price` (5-yr FCF vs 65/25 hurdle) | `deal-value` *(function-backed)* |
| close acquisition | create `Deal` (with consideration + `ppa {goodwill, customer_base, ip, trademark}`); link `Deal —of→ Target`; create `Business` + its `Interface`(s); link `Deal —produces→ Business` | `deal-diligence` |
| transform | modify `Business` {re-tech · reorganize · monetize (free↔paid, tiers, subscription)} and `Interface` {redesign UI · AI features · sunset} | `deal-optimize` |
| run experiment | modify `Business`/`Interface` (pricing & UX variants chosen; A/B at scale) | `deal-optimize` (Janus/Orion) |
| hire | create `Spooners` (grow the durable core) | `talent` (Role Model) |
| assemble task-force | create link `Spooners —deployed-on→ Business` (onto the acquisition) | `talent` |
| reorganize | modify `Business` org (acquired staff transitioned out) | `deal-optimize` |
| reallocate talent | modify link `Spooners —deployed-on→ Business` across the portfolio | `talent` |
| retire | modify `Business.status` (main → tail → retired; the row is never deleted) | `retire` |
| raise / refinance | create / modify `Facility` (sign · draw · amend · repay) | `finance` |

Capital **reinvest** is not an object transaction — it is the flywheel's fuel loop (§3), governed by `will.md`. The **raise** side *is* one: financing structures are one of the four core CEO decisions (`bsp-f1` ~L4577), and `raise / refinance` writes the `Facility`.

Every verb above has a contract in `capabilities/actions/`: source · screen · underwrite · close acquisition · transform (also covering run-experiment and reorganize) · **talent** (the people-verbs: hire · assemble task-force · reallocate) · **retire** (`[decision]` — modeled from the observed churn, not a disclosed process) · **finance** (raise / refinance).

### Functions — read only (computed, no write-back; contract = input · computation · output)
- **monitor** — read held `Business`es vs their underwriting → flag drift. `deal-monitor`
- **headline reading** — derive net-income≈0 / organic-% over the financial data (§3). `capital-allocation`
- **impermanence** — derive the 100%→24% portfolio churn (§3). `portfolio-impermanence`
- **committed-base reading** — derive willingness-to-pay & retention per business; scale carries the non-dedup caveat. `product-users`

---

## 3. The flywheel — the self-reinforcing loop
Not an object: the loop the §2 actions form. It is a true flywheel because **two loops share the spine** — the capital that fuels it, and the Platform edge that makes each turn *bigger*, not just repeated.

```
        ┌────────── ① reinvest (cash + debt) ◄──────────────┐
        ▼                                                    │
 source → screen → underwrite → close → transform → monetize → cash
                      ▲
                      └── ② edge widens ◄── Platform/Tools improve ◄── scale + data
                          (every turn; Spooner output per head ↑)
```

**① Capital compounding (fuel):** cash + raised debt is reinvested into the next `close` — capital feeds on itself. But on its own it only *scales* the same edge, it does not *widen* it.
**② Capability compounding (the real flywheel):** each turn adds scale and proprietary data → `Platform` and `Tool`s improve → `Spooners` output per head rises → the underwriting `edge` widens → the next `close` is bigger. The machine gets better every turn. The **mechanism** of this loop is the model's **feedback layer** (`[decision]`): each turn's realized outcomes feed back to recalibrate the capability that produced them — a target→deal→business outcome recalibrates sourcing/underwriting, a business that grows refines the transform playbook, a hire who succeeds sharpens the selection gates. An *outcome reading* (function: realized-vs-expected) into a *calibrate step* (adjusting the capability's own parameters) is what would turn this loop from a diagram into a running mechanism — the "press-play" agentic org. This is the **direction the repo builds toward**, marked `[decision]`, not a built engine verb: `calibrate` is not a §2 object-transaction (it tunes a capability's parameters, not an object), and a genuinely data-driven calibration needs *longitudinal* outcome data (realized-vs-underwritten over time) that a single-snapshot filing does not disclose — so the mechanism is specified here and becomes executable as that data accrues. Today the loop's outcome-reading side is real (`monitor` reads held businesses vs their underwriting; `retire` already consumes its drift finding); the calibrate-back-to-sourcing side is the specified next turn. (See `README.md` → *Where this is going*; the customer-signal version is the analysis's knowledge-flywheel.)

Two forces act on it. **Leverage** amplifies ① (more debt → bigger deals) but fragilizes it (interest drives GAAP net income to ≈0; net debt climbs). And the loop **leaks at the customer**: usage/retention should feed `source`/`monetize`, but the unified `Customer` is UNBUILT, so that signal never compounds.

**The reading** (a function over `world-model/company/financials.csv`): revenue compounds while net income ≈ 0 and net debt climbs — the machine runs on borrowed money against slowly-declining cash cows. The analysis (`bending-spoons-as-an-intelligence.md §5`) argues a different loop on the same spine — the **knowledge-flywheel**.
