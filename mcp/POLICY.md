# Data sources & acceptable use

This covers the **live** tools — the `radar_*` scouting tier and `hire`. The model tools (query,
`get_capability`, the two-phase engine, `run_audit`) touch **no external service** and are unaffected.

## You are the requester
The live radar tools make requests to third-party services **from the machine you run the server on,
under your identity**. `RADAR_CONTACT` (the env var in the README setup) is *your* declared contact — SEC
EDGAR and others see it on every request. So the duty to comply with each source's terms and rate limits
is **yours, the operator's**, not the repo's. Set `RADAR_CONTACT` to a real contact, and keep usage modest.

The code identifies itself (a contact `User-Agent`) but does **not** hard-throttle. If you batch calls, add
delays and honor each source's limits — e.g. SEC EDGAR asks for **≤10 requests/second** and a declared
contact, and returns **403** otherwise.

## The live sources, and their terms
| Source | Hosts | Used by | Terms to honor |
|---|---|---|---|
| SEC EDGAR | `data.sec.gov` · `www.sec.gov` · `efts.sec.gov` | `radar_universe(us)` · `radar_gates` · `radar_signals` | Fair-access: declared contact `User-Agent` (`RADAR_CONTACT`) + ≤10 req/s |
| GLEIF | `api.gleif.org` | `radar_company` | Open LEI API |
| XBRL / ESEF | `filings.xbrl.org` | `radar_universe(eu)` · `radar_company` | Open filings index |
| Hacker News | `hn.algolia.com` · `news.ycombinator.com` | `radar_scout` | Public API |
| Reddit | `reddit.com` | `radar_scout` · `radar_loyalty` | Public JSON, subject to Reddit's Terms — heavy/commercial use needs their API terms |
| Wikipedia | `wikimedia.org` | `radar_loyalty` | Open; content is CC BY-SA (attribution) |
| Apple App Store | `itunes.apple.com` | `radar_loyalty` | Public lookup |

## Output discipline
Everything the live tier returns is **`[to-validate — press only]`** — corroboration, never a fact written
into the model. Third-party press is never a fact source (`../CLAUDE.md` rule 8). Model facts come only from
the official filings and Bending Spoons' own documents (see `../NOTICE`).

## `hire`
Decision-**support** only. Scoring candidates is **high-risk under the EU AI Act** (Annex III §4): the tool
assembles the case, carries the caveat, and **stops at the committee** — a human decides. It never picks,
and writes nothing.

## Affiliation
This repository is a point-in-time demonstrative exercise by Play New, built from public disclosures. It is
**not affiliated with, authored by, or endorsed by Bending Spoons** (see `../NOTICE`).
