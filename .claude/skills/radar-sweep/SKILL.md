---
name: radar-sweep
description: The market-radar's sensing pass — sweep recent public signal (HN + Reddit, free, recency-windowed) on a company or theme and bucket every hit against the contract's watch signals (distress, ownership, momentum, valuation, AI-pressure). Use to scout a candidate or refresh the pipeline.
---

**Thesis-driven**: the hunt (band, regions, sectors, signals, weights, dedup sources) lives in a
thesis file — `theses/bending-spoons.yaml` is the default and mirrors Bending Spoons' contract.
**To scout for another acquirer: copy that file OUTSIDE this repo, tune every field (band, regions,
sector hints, signal keywords, weights, event queries, dedup csvs), and add `--thesis <your file>`
to every command.** The engine is fully generic; the thesis is the strategy — keep yours private. Start any session with
`python3 ${CLAUDE_SKILL_DIR}/scripts/radar_sweep.py --preflight` (thesis + sources status).

Run the deterministic sensing pass, then judge — never the reverse. The hunt is COHERENT WITH THE
SUBJECT: it buys formerly-public companies, carve-outs from listed parents, and private digital
brands — so the radar works in three tiers, structured-first:

**Tier 1 — STRUCTURED (EDGAR, free):** the mechanical gates and ownership events for anything
US-listed (including EU companies listed in the US, which file 20-F/IFRS — read natively):
- `--universe CY2024` — the mechanical top of the funnel (US): every US filer's annual revenue that
  year (union of 3 XBRL revenue concepts, deduped by CIK, owned/pipeline names removed), filtered
  to the $50M–$5B band. ~2,500 names in-band for CY2024 — Bending Spoons' own funnel scale (~L2617);
  narrow it with `--gates` (sector + region) per candidate
- `--universe-eu CY2024 [--countries IT,DE,FR]` — the same net over the EU-listed universe, from the
  ESEF repository (filings.xbrl.org, free, keyless): enumerates every EU-regulated-market filing for
  the period + countries, fetches IFRS revenue per filing (capped by `--limit`, default 60 — raise it
  or narrow `--countries` to go deeper; enumeration is always complete), band-filters in native
  currency (indicative — mostly EUR, not USD-converted), removes owned/pipeline. Deep-dive any name
  with `--company`. This closes the EU half of the funnel the US frames endpoint can't see.
- `--events --days 30` — recent 8-Ks with sale/divestiture language, digital-SIC filtered
- `--gates "TKR1, TKR2"` — per candidate: revenue band · HQ EU/NA · digital SIC → PASS/FAIL [derived]

**Tier 2 — CHATTER (HN + Reddit, free):** brand/theme sweeps bucketed on the watch signals,
`--rank` for maturity scores. Corroboration and early smoke — never the primary evidence.

**Tier 3 — PRESS (WebSearch, use it seriously):** for private companies and EU-listed names EDGAR
cannot see (most of Bending Spoons' >1,000-target universe is private — this tier IS the "manual
analysis" Bending Spoons itself performs). Recipes — run 2+ and triangulate, date every claim:
- ownership: `"<company>" ("explores sale" OR "strategic alternatives" OR "in talks to sell")`
- parent divestiture: `"<parent>" (divest OR carve-out OR "non-core") <asset>`
- distress: `site:layoffs.fyi <company>` · `"<company>" (layoffs OR restructuring)`
- momentum: `"<company>" (subscribers OR MAU OR users) (decline OR churn OR fell)`
- valuation: `"<company>" (valuation OR "down round" OR writedown)`
- EU targets, local press: `"<company>" (vendita OR cession OR Übernahme OR "te koop")`
Everything from tiers 2-3 is `[to-validate — press only]`; tier 1 values are `[derived]` from EDGAR.

**Tier 1 extensions (live):** `--company "Legal Name"` — the EU-listed + unlisted chain: GLEIF
(identity, LEI, HQ country — free, keyless) → ESEF/filings.xbrl.org (structured IFRS revenue via xBRL-JSON — free, keyless;
NOTE: repository coverage varies by country — FR/IT/NL/Nordics are good, DE is partial — so "no
filing found" never means "not listed") → honest n.d. for private companies
(no LEI/no ESEF: that slice is chatter + press + judgment; UK privates via Companies House once
CH_API_KEY is set). `--loyalty "Brand"` — the brand-strength card: committed base (App Store rating
volume/avg) · brand interest (Wikipedia trend %) · community (subreddit size where reachable) —
proxies, monitorable by snapshot+diff; retention/NRR proper is non-public and enters at diligence.
 `--forms --days 5` — ownership-change filings from the EDGAR daily
index (SC 13D activist stakes · SC 13E-3 going-private · 25/15 delisting), sector-filtered per thesis.
**Tier 2 extensions (live):** `--interest "Brand"` — Wikipedia-pageviews momentum (window vs previous
window, % delta); `--appstore "App"` — rating volume/average as a committed-base proxy (iTunes, keyless).

**Source roadmap** (researched and endpoint-verified; not yet integrated — in value order):
| source | gives | access | effort |
|---|---|---|---|
| filings.xbrl.org (ESEF) | structured IFRS revenue for ALL EU-listed cos (~25k filings, 28 countries) | free, no key, `filings.xbrl.org/api` | M (XBRL parsing) |
| UK Companies House | private-UK accounts (turnover where filed) + PSC ownership | free key, 600 req/5min | M |
| GLEIF LEI | HQ/legal form + parent-child ownership graph; the cross-source join key | free, no key, `api.gleif.org/api/v1` | S |
| WARN Firehose | 50-state layoff notices, daily, bulk CSV/JSON | free (check ToS) — or self-host biglocalnews/warn-scraper | M |
| GitHub API | repo-activity decline for dev-tool targets | free, 5k req/h with token | M |
| Tranco (+ CrUX/Cloudflare Radar) | domain-rank trend for web-SaaS targets | free (Tranco keyless; CrUX/Radar free keys) | S-M |
| npm / PyPI stats | dev-adoption momentum | free, no key | S |
| Pappers (FR) / BRREG (NO) / PRH (FI) | private-company data per country | free tiers vary | S-M |
| growth rankings (FT1000, Deloitte Fast 500 EMEA, Inc 5000, Sifted leaderboards) | annual PRIVATE-company universe lists with revenue/growth indications; the signal is the DELTA — names that stop appearing = growth over, maturation begins | public annual lists (download/scrape once a year; Sifted partly paywalled) | S (annual diff) |
Skip (verified weak): layoffs.fyi (fragile scrape + attribution), Polymarket (thin M&A coverage),
Google Play / Google Trends (no reliable free automation), SimilarWeb/data.ai/Sensor Tower (paid only).

Setup (once per shell, required by SEC EDGAR): `export RADAR_CONTACT="Name email@domain"` —
the structured tier (--gates/--events/--universe) returns 403 without a real contact.

1. Run the sweep (from the repo root):
   `python3 ${CLAUDE_SKILL_DIR}/scripts/radar_sweep.py "<company or theme>" --days 30`
   Several candidates at once → `--rank "A, B, C"`: one maturity score per candidate
   (formula declared in the script header, [decision]), owned/pipeline names excluded
   automatically. Widen with `--days 90` for slow-moving targets.
2. Read the brief: hits are bucketed by the market-radar contract's WATCH SIGNALS
   (`capabilities/actions/market-radar.md`) and ranked by engagement. Everything in it is
   press/social → `[to-validate — press only]`; never present a hit as a fact.
3. JUDGE (or spawn the `market-radar` agent with the brief in its prompt — it has no execution
   tools, so give it the brief; it drafts the propose-params): does the signal say *buyable now*?
   Which of the nine Target gates does the candidate plausibly pass?
4. If yes: propose via the engine —
   `python3 -c "import sys; sys.path.insert(0,'mcp'); import engine, json; print(json.dumps(engine.propose('source', PARAMS), indent=2))"`
   and STOP: admission into the pipeline is the human gate (`engine.apply` with the user's name).

WebSearch remains a complementary source for press the sweep can't reach — same
`[to-validate — press only]` rule.
