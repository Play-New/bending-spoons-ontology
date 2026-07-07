# Try it — questions to ask Bending Spoons

Once the MCP server is connected (see the README), just talk to Claude in plain language. You don't
call tools by name — you ask, and Claude picks the tool. Below is a tested bank of questions grouped by
intent, with the tool each one exercises noted in `code`. Copy any of them.

**Legend** · ✓ = verified against the live tools · ⚡ = needs internet **and `RADAR_CONTACT` set on the server** (scouts SEC EDGAR, which 403s without a declared contact — see the README) · ✍️ = writes to the
model, so it asks for your approval before anything changes.

---

## 1 · Understand the company
- ✓ *"What is Bending Spoons and what is this repo?"* → `overview`
- ✓ *"Show me the whole portfolio."* → `list_nodes(business)` (17 businesses)
- ✓ *"Tell me about Evernote — retention, tenure, where it is in its lifecycle."* → `get_node`
- ✓ *"What did they pay for each acquisition?"* → `get_node(deals.csv)` (Evernote $199.7M, WeTransfer $476.3M, Vimeo $1.36B, AOL $1.45B…)
- ✓ *"What's the net revenue retention across the businesses?"* → `search('NRR')` (AOL 95%, Evernote 99%, Remini 87%, StreamYard 91%)
- ✓ *"What does Bending Spoons refuse to do?"* → `will`
- ✓ *"Search the model for 'margin of safety'."* → `search` (finds the will's downside-floor refusal)
- ✓ *"Which apps (interfaces) does WeTransfer ship, and to which business do they belong?"* → `get_node(interfaces/…)`
- ✓ *"What does the analysis argue is the next layer — the cross-product customer graph?"* → `get_node(cross-product-graph)` · `analysis` (a level of analysis, not a gap in the model)

## 2 · The capabilities — how the machine actually works
The capabilities are the differentiated part: the machine's own moves, each a written contract you can read.
- ✓ *"What can this machine actually do? List its capabilities."* → `list_capabilities` (the kinetic contracts: 8 actions + 4 functions)
- ✓ *"How does Bending Spoons find acquisition targets?"* → `get_capability('market-radar')`
- ✓ *"What are the gates a target must pass to be screened in?"* → `get_capability('screen-target')`
- ✓ *"How do they underwrite a deal? What's the hurdle and how is the walk-away price built?"* → `get_capability('deal-value')` (65% levered / 25% unlevered IRR; debt capped at the lower of 85% of EV and what the cash flows repay)
- ✓ *"How do they verify the assumptions before closing?"* → `get_capability('deal-diligence')`
- ✓ *"What's the transformation playbook they apply after buying?"* → `get_capability('deal-optimize')`
- ✓ *"How does the Platform act on its people (the Spooners)?"* → `get_capability('talent')`
- ✓ *"What happens when a product is wound down — do they sell it?"* → `get_capability('retire')` (retire ≠ sell)
- ✓ *"How is the whole thing financed? What's the leverage covenant?"* → `get_capability('finance')` (raise/refinance; ≤4.00 leverage covenant)
- ✓ *"Explain the capital flywheel — where do the economics actually resolve?"* → `get_capability('capital-allocation')`
- ✓ *"Why does the model treat the portfolio as impermanent?"* → `get_capability('portfolio-impermanence')`
- ✓ *"Who are the paying, committed users — how is that base defined?"* → `get_capability('product-users')`
- ✓ *"Turn on the portfolio-monitor loop and watch the held businesses against their underwriting."* → `activate_agent('deal-monitor')`

## 3 · Scout like they do (live)
**The two-step demo — run these in order:**
1. ⚡ *"Find US acquisition targets and screen them — which fit Bending Spoons?"* → `radar_discover` — **runs the search and the screened names come out** (pulls the in-band universe, auto-applies band · US HQ · digital-sector gates, returns the in-thesis survivors — no tickers to supply). Italy variant: *"…in Italy, $50–300M"* → `radar_universe(eu, IT)` (listed-only, small set).
2. ⚡ *"Take [name from the shortlist] and give me the full read — brand, distress, ownership."* → `radar_gates` + `radar_loyalty` + `radar_signals`/`radar_scout` against the `screen-target` gates / `market-radar` signals (gates are pass/fail; "buyable now" is a judgment, not a weighted score)

**Private targets** — the ones EDGAR/ESEF can't see (listed-only), which is where many real deals originate:
- ⚡ *"Show me the private-target watchlist."* → `radar_watchlist` (a human-curated seed list of famous-but-fallen **private** brands — `[to-validate]`; you edit it, the machine scores it)
- ⚡ *"Score the watchlist: run brand strength and distress on each — which are famous, loyal, and in decline?"* → `radar_watchlist` → `radar_loyalty` + `radar_scout` (these signals don't need SEC filings)

**Discovery is name-free** — to *find* candidates you name a place + a band, not a company. `radar_universe`
is the top of the funnel; `radar_scout` only sweeps chatter on a name you *already have*.
- ⚡ *"Find listed companies in Italy with $50M–$5B revenue I could acquire."* → `radar_universe(region='eu', countries='IT')` — returns real in-band names (Eurotech, CY4Gate, Class Editori, B&C Speakers, Alkemy, Toscana Aeroporti…)
- ⚡ *"Find in-band US-listed targets."* → `radar_universe(region='us')`
- ⚡ *"Check the acquisition gates for Sonos and Pinterest."* → `radar_gates`
- ⚡ *"Is Ubisoft inside the thesis?"* → `radar_company` (one specific EU / unlisted name you already have)
- ⚡ *"How strong is Evernote's brand right now?"* → `radar_loyalty`
- ⚡ *"Any ownership-change signals in the last month?"* → `radar_signals`
- ⚡ *"What's the recent chatter on Bandcamp?"* → `radar_scout` (needs a name; HN/Reddit only — blind to non-English & financial press, so silence ≠ all-clear)

## 4 · Hire like they do
- ✓ *"Assess this candidate against Bending Spoons' published hiring gates: [paste a CV / profile]."* → `hire`
  (Decision-support only. Candidate scoring is high-risk under the EU AI Act — the tool recommends and
  stops at the committee; a human decides. It never picks.)
- ✓ *"Draft the problem-solving and behavioral tasks Bending Spoons would use for this role."* → `hire`

## 5 · Run the deal machine (writes — it asks before it changes anything)
Every write is two-phase: the tool **proposes** (validates the gates, computes the diff, writes nothing),
then you **approve** and it applies — one git commit per action, and the audit must stay green or it rolls back.
- ✍️ *"Source this target: [name, revenue scale, HQ, revenue model]."* → `propose_action('source')`
- ✍️ *"Screen [target] against the gates."* → `propose_action('screen')`
- ✍️ *"Underwrite [target] to the 65/25 hurdle and give me the walk-away price."* → `propose_action('underwrite')`
- ✍️ *"Close the deal on [target] and create the business."* → `propose_action('close')` → `apply_action`
- ✓ *"What proposals are pending?"* → `list_proposals`
- ✓ *"Reject this proposal — it's not in thesis."* → `reject_action`

Refusals you can trigger on purpose (the guardrails):
- ✓ *"Screen a company we never sourced."* → refused: *unknown target* — `screen` **mutates** a sourced Target, so it must exist; to just **check** the gates (read-only, no sourcing) use `radar_gates` / `radar_company`, or `source` it first to admit it to the pipeline.
- ✓ *"Underwrite something that only returns 40% levered / 20% unlevered."* → refused: *below the hurdle (default ≥65 / ≥25)* — the bar is a **will parameter, not dogma**: the filing says it's "plausible we'll have to lower them" with scale, so a human may lower it deliberately (`hurdle_levered_pct` / `hurdle_unlevered_pct`).

## 6 · Check the model itself
- ✓ *"Is the model internally consistent? Run the audit."* → `run_audit`
- ✓ *"Where does every fact come from? Show me the sources."* → `list_sources` (the two SEC filings + Bending Spoons' own hiring docs)
- ✓ *"Show me the official hiring selection document."* → `get_source('bsp-selection-process')`
- ✓ *"What does the thesis say about where the company could go?"* → `analysis`
- ✓ *"What are the modeling foundations this rests on?"* → `foundations`

---

*This bank is kept honest by the server test-suite (every capability must be retrievable and listed) and by
the full-response acceptance capture. ⚡ questions need the machine you run it on to have internet; ✓ questions
are verified offline.*
