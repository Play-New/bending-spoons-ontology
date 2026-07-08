#!/usr/bin/env python3
"""radar-sweep — a thesis-driven M&A scouting radar. Generic engine, pluggable hunt.

The STRATEGY lives in a thesis file (theses/*.yaml): band, regions, sector hints, watch
signals, ranking weights, noise lists, dedup sources, event queries. The default thesis is
the repo subject's (theses/bending-spoons.yaml, mirroring its market-radar contract); pass
--thesis <file> to hunt for a different acquirer (copy the default thesis and tune it).

Three tiers, structured-first:
  --universe CY2024      every US-reported annual revenue that year, filtered to the band (EDGAR frames)
  --events   --days 30   recent 8-Ks with sale/divestiture language, sector-filtered (EDGAR full-text)
  --gates    "T1, T2"    per-candidate mechanical gates: revenue band · HQ region · sector (EDGAR
                         companyfacts + submissions; reads IFRS/20-F, so EU companies US-listed too)
  <brand|theme>          chatter sweep (HN + Reddit, free), recency-windowed, signal-bucketed
  --rank "A, B, C"       maturity scores across candidates (declared formula below)
  --preflight            show the loaded thesis, dedup counts, and source reachability; run nothing

Everything from chatter/press is [to-validate — press only]; EDGAR values are [derived].
SEC requires a contact User-Agent: export RADAR_CONTACT="Name email@domain".
"""
from __future__ import annotations

import argparse
import json
import math
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:  # macOS framework Python often lacks local certs; prefer certifi when present
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # public read-only APIs; degraded verification, said out loud
    _CTX = ssl._create_unverified_context()
    print("<!-- certifi not installed: TLS verification degraded -->", file=sys.stderr)

_UA = {"User-Agent": f"radar-sweep research ({os.environ.get('RADAR_CONTACT', 'contact-not-set@example.com')})"}
_SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_THESIS = _SCRIPT_DIR.parent / "theses" / "bending-spoons.yaml"

US_STATES = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE"
                " NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
EU_HINTS = ["germany", "france", "italy", "spain", "netherlands", "sweden", "denmark", "norway",
            "finland", "ireland", "united kingdom", "poland", "austria", "belgium", "portugal",
            "switzerland", "luxembourg", "czech", "greece", "romania", "hungary", "estonia"]
REV_CONCEPTS = {"us-gaap": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
                "ifrs-full": ["Revenue", "RevenueFromContractsWithCustomers"]}
FORMS = {"us-gaap": ("10-K",), "ifrs-full": ("20-F",)}


# ----------------------------- thesis loading -----------------------------
def _repo_root() -> Path | None:
    for up in _SCRIPT_DIR.parents:
        if (up / ".git").exists() or (up / "world-model").exists():
            return up
    return None


def load_thesis(path: str | Path = DEFAULT_THESIS) -> dict:
    import yaml
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    cfg["_path"] = str(path)
    cfg["_owned"], cfg["_pipeline"] = set(), {}
    root = _repo_root()
    if root:
        import csv as _csv
        import io as _io

        def rows(rel):
            out, header = [], None
            f = root / rel
            if not f.exists():
                return out
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("#"):
                    continue
                r = next(_csv.reader(_io.StringIO(line)))
                if header is None:
                    header = r
                else:
                    out.append(dict(zip(header, r)))
            return out

        for d in (cfg.get("dedup") or {}).get("owned", []) or []:
            for r in rows(d["csv"]):
                cfg["_owned"].add(r[d["column"]].lower())
        for d in (cfg.get("dedup") or {}).get("pipeline", []) or []:
            for r in rows(d["csv"]):
                cfg["_pipeline"][r[d["column"]].lower()] = r.get(d.get("status_column", ""), "?")
    return cfg


# ----------------------------- fetch -----------------------------
def _get(url: str):
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=20, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8"))


# US filers report revenue under several XBRL concepts; sweeping one misses thousands.
# The union (deduped by CIK, max value per filer) is the real mechanical net — the top of
# the funnel, matching how the subject casts wide before narrowing (bsp-f1 ~L2617).
_REVENUE_CONCEPTS = ["Revenues",
                     "RevenueFromContractWithCustomerExcludingAssessedTax",
                     "RevenueFromContractWithCustomerIncludingAssessedTax"]


def universe(year: str, cfg: dict) -> dict:
    """The in-band US universe: union of revenue concepts, deduped by CIK, minus owned/pipeline."""
    lo, hi = cfg["band_usd_m"]
    by_cik, reporting, errors = {}, set(), []
    for concept in _REVENUE_CONCEPTS:
        try:
            frame = _get(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{concept}/USD/{year}.json")
        except Exception as e:  # a missing concept for a year is not fatal — record and go on
            errors.append(f"{concept}: {e}")
            continue
        for d in frame.get("data", []):
            reporting.add(d["cik"])
            m = d["val"] / 1e6
            # keep the largest reported figure per filer (concepts can disagree on scope)
            if d["cik"] not in by_cik or m > by_cik[d["cik"]][1]:
                by_cik[d["cik"]] = (d["entityName"], m)
    in_band, dropped = [], 0
    for cik, (name, m) in by_cik.items():
        if not (lo <= m <= hi):
            continue
        if name.lower() in cfg["_owned"] or name.lower() in cfg["_pipeline"]:
            dropped += 1
            continue
        in_band.append((cik, name, m))          # keep the CIK so discover() can gate by CIK
    in_band.sort(key=lambda r: r[2])
    return {"reporting": len(reporting), "in_band": in_band,
            "dropped_owned_pipeline": dropped, "errors": errors}


_SIC_HQ_CACHE = None


def _load_sic_cache() -> dict:
    """The prebuilt SIC+HQ index (data/edgar_sic_hq.json) — lets discover() screen the WHOLE in-band
    universe instantly instead of a live slice. Empty dict if the cache is absent."""
    global _SIC_HQ_CACHE
    if _SIC_HQ_CACHE is None:
        try:
            path = os.path.join(_SCRIPT_DIR, "..", "data", "edgar_sic_hq.json")
            _SIC_HQ_CACHE = json.load(open(path, encoding="utf-8")).get("sic_hq", {})
        except Exception:
            _SIC_HQ_CACHE = {}
    return _SIC_HQ_CACHE


def _region_ok(loc: str, cfg: dict) -> bool:
    """North-America = a US state code, Canada, or Puerto Rico; Europe = an EU HQ hint. (Defect-to-test:
    the gate matched only US 2-letter state codes, silently dropping Canadian- and PR-HQ filers that are
    in the north-america thesis region.)"""
    lu = (loc or "").upper()
    na = lu in US_STATES or lu == "PR" or "CANADA" in lu or "PUERTO RICO" in lu
    eu = any(h in (loc or "").lower() for h in EU_HINTS)
    return ("north-america" in cfg["regions"] and na) or ("europe" in cfg["regions"] and eu)


def _gate_row(name, m, loc, sic, cfg) -> dict:
    """Apply the mechanical gates (region · sector) to one company's SIC + HQ."""
    region_ok = _region_ok(loc, cfg)
    sector = "PASS" if any(h in sic.lower() for h in cfg["sector_hints"]) else "JUDGE"
    return {"name": name, "revenue_m": round(m), "hq": loc or "n.d.", "sic": sic,
            "region": "PASS" if region_ok else "FAIL", "sector": sector}


def discover(year: str, cfg: dict, limit: int = 150) -> dict:
    """Run the US universe AND auto-apply the mechanical gates, returning the in-thesis survivors
    (region PASS · sector PASS/JUDGE) BY NAME — discovery that outputs a screened shortlist, no tickers.
    With the prebuilt SIC/HQ cache it screens the WHOLE in-band universe instantly; without it, it falls
    back to a bounded live slice. The SIC sector call is coarse (PASS = mechanical flag, not thesis-fit)."""
    u = universe(year, cfg)
    band = u["in_band"]                          # (cik, name, m)
    cache = _load_sic_cache()

    if cache:                                    # full-universe screen from the cached index — every filer
        rows, uncached = [], 0
        for cik, name, m in band:
            hit = cache.get(str(int(cik)))
            if not hit:
                uncached += 1
                continue
            rows.append(_gate_row(name, m, hit[1], hit[0], cfg))
        survivors = [r for r in rows if r["region"] == "PASS" and r["sector"] in ("PASS", "JUDGE")]
        survivors.sort(key=lambda r: (r["sector"] != "PASS", r["revenue_m"]))
        return {"total_in_band": len(band), "screened": len(rows), "errored": uncached,
                "survivors": survivors, "source": "cache (full universe)", "universe_errors": u["errors"]}

    # fallback: no cache → gate a bounded live slice, concurrently
    step = max(1, len(band) // limit)
    subset = band[::step][:limit]

    def _g(item):
        cik, name, m = item
        try:
            subs = _get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json")
        except Exception:
            return None
        loc = ((subs.get("addresses", {}).get("business", {}) or {}).get("stateOrCountryDescription") or "")
        return _gate_row(name, m, loc, subs.get("sicDescription") or "", cfg)

    with ThreadPoolExecutor(max_workers=5) as ex:   # keep under SEC's ~10 req/s fair-access ceiling
        raw = list(ex.map(_g, subset))
    rows = [r for r in raw if r]
    survivors = [r for r in rows if r["region"] == "PASS" and r["sector"] in ("PASS", "JUDGE")]
    survivors.sort(key=lambda r: (r["sector"] != "PASS", r["revenue_m"]))
    return {"total_in_band": len(band), "screened": len(subset), "errored": len(raw) - len(rows),
            "survivors": survivors, "source": "live slice", "universe_errors": u["errors"]}


def hn(query: str, days: int, limit: int) -> list[dict]:
    since = int(time.time()) - days * 86400
    q = urllib.parse.quote(query)
    url = (f"https://hn.algolia.com/api/v1/search?query=%22{q}%22"  # quoted = exact phrase
           f"&numericFilters=created_at_i>{since}&hitsPerPage={limit}")
    out = []
    for h in _get(url).get("hits", []):
        out.append({"src": "hn", "title": h.get("title") or h.get("story_title") or "",
                    "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "score": int(h.get("points") or 0), "comments": int(h.get("num_comments") or 0),
                    "date": (h.get("created_at") or "")[:10]})
    return out


def reddit(query: str, days: int, limit: int) -> list[dict]:
    t = "week" if days <= 7 else "month" if days <= 31 else "year"
    url = f"https://www.reddit.com/search.json?q={urllib.parse.quote(query)}&sort=new&t={t}&limit={limit}"
    out = []
    try:
        data = _get(url)
    except Exception as e:
        print(f"<!-- reddit unavailable: {e} -->", file=sys.stderr)
        return out
    for c in data.get("data", {}).get("children", []):
        d = c.get("data", {})
        out.append({"src": f"r/{d.get('subreddit','?')}", "title": d.get("title", ""),
                    "url": "https://reddit.com" + d.get("permalink", ""),
                    "score": int(d.get("score") or 0), "comments": int(d.get("num_comments") or 0),
                    "date": time.strftime("%Y-%m-%d", time.gmtime(d.get("created_utc") or 0))})
    return out


# ----------------------------- chatter tier -----------------------------
def bucket(items: list[dict], cfg: dict) -> dict[str, list[dict]]:
    signals = cfg["signals"]
    buckets: dict[str, list[dict]] = {k: [] for k in signals}
    buckets.update({"unclassified": [], "out-of-band": [], "already-owned": [], "already-in-pipeline": []})
    for it in items:
        text = it["title"].lower()
        if any(f" {o} " in f" {text} " or o in text.split() for o in cfg["_owned"]):
            buckets["already-owned"].append(it)
            continue
        if any(p in text for p in cfg["_pipeline"]):
            buckets["already-in-pipeline"].append(it)
            continue
        if any(g in text for g in cfg.get("out_of_band", [])):
            buckets["out-of-band"].append(it)
            continue
        hit = [sig for sig, kws in signals.items() if any(k in text for k in kws)]
        for sig in (hit or ["unclassified"]):
            buckets[sig].append(it)
    for sig in buckets:
        buckets[sig].sort(key=lambda x: -(x["score"] + x["comments"]))
    return buckets


def sweep(query: str, days: int, limit: int, cfg: dict) -> dict:
    items = hn(query, days, limit) + reddit(query, days, limit)
    ql = query.lower()
    items = [it for it in items if ql in it["title"].lower()]  # anti-fuzz relevance
    seen, deduped = set(), []
    for it in items:
        k = it["title"].strip().lower()
        if k and k not in seen:
            seen.add(k)
            deduped.append(it)
    return bucket(deduped, cfg)


# maturity = Σ_signal weight · Σ_hits log2(1+points+comments) · recency, then × quality multipliers
# [decision: our formula — weights and multipliers live in the thesis file]
def maturity(buckets: dict, days: int, cfg: dict) -> tuple[float, list[str]]:
    today = time.time()
    score = 0.0
    for sig, w in cfg["weights"].items():
        for it in buckets.get(sig, []):
            try:
                age = max(0.0, (today - time.mktime(time.strptime(it["date"], "%Y-%m-%d"))) / 86400)
            except Exception:
                age = days / 2
            score += w * math.log2(1 + it["score"] + it["comments"]) * max(0.3, 1 - age / max(days, 1))
    fired = [s for s in cfg["weights"] if buckets.get(s)]
    for sig, mult in (cfg.get("quality_multipliers") or {}).items():
        if buckets.get(sig):
            score *= mult
            fired.append(f"{sig}(×{mult})")
    return round(score, 1), fired


# ----------------------------- structured tier (EDGAR) -----------------------------
def _tickers() -> dict:
    return {v["ticker"].upper(): v for v in _get("https://www.sec.gov/files/company_tickers.json").values()}


def _is_annual(u) -> bool:
    return (int(u["end"][:4]) - int(u["start"][:4])) == 1 or (
        int(u["end"][:4]) == int(u["start"][:4]) and u["start"][5:7] == "01" and u["end"][5:7] == "12")


def _annual_revenue(cik: str):
    facts = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")
    for taxo, concepts in REV_CONCEPTS.items():
        gaap = facts.get("facts", {}).get(taxo, {})
        best = None
        for concept in concepts:
            for cur, units in gaap.get(concept, {}).get("units", {}).items():
                for u in units:
                    if u.get("form") in FORMS[taxo] and u.get("fp") == "FY" and u.get("start") and u.get("end"):
                        if _is_annual(u) and (best is None or u["end"] > best[1]):
                            best = (u["val"], u["end"], concept, cur)
        if best:
            return best
    return None


def gates(ticker: str, cfg: dict) -> dict:
    """The mechanical screening gates from EDGAR (band · region · sector). [derived]"""
    tk = _tickers().get(ticker.upper().replace(".", "-"))
    if not tk:
        return {"ticker": ticker, "error": "unknown ticker on EDGAR"}
    cik = f"{tk['cik_str']:010d}"
    lo, hi = cfg["band_usd_m"]
    out = {"ticker": ticker.upper(), "company": tk["title"], "cik": cik}
    rev = _annual_revenue(cik)
    if rev:
        val_m, cur = rev[0] / 1e6, rev[3]
        out["revenue_m"] = f"{round(val_m)} {cur}"
        out["revenue_asof"] = rev[1]
        in_band = lo <= val_m <= (hi * (1.1 if cur != "USD" else 1.0))
        out["gate_band"] = ("PASS" if in_band else "FAIL") + ("" if cur == "USD" else f" (indicative, {cur})")
    else:
        out["gate_band"] = "n.d. (no annual XBRL revenue)"
    subs = _get(f"https://data.sec.gov/submissions/CIK{cik}.json")
    loc = ((subs.get("addresses", {}).get("business", {}) or {}).get("stateOrCountryDescription") or "")
    ok = _region_ok(loc, cfg)
    out["hq"] = loc or "n.d."
    out["gate_region"] = "PASS" if ok else ("n.d. (check manually)" if not loc else "FAIL")
    sic = (subs.get("sicDescription") or "")
    out["sic"] = sic
    out["gate_sector"] = "PASS" if any(h in sic.lower() for h in cfg["sector_hints"]) else "JUDGE (SIC not clearly in-thesis)"
    return out


_SIC_CACHE: dict = {}


def _sector_ok(cik10: str, cfg: dict) -> tuple[bool, str]:
    """Returns (in_sector, sic). sic == "?unreachable" means the SIC lookup FAILED (not a genuine
    non-match) — the caller must not silently drop an ownership signal on a transient outage; that
    sentinel is NOT cached, so a later hit can retry."""
    if cik10 not in _SIC_CACHE:
        try:
            _SIC_CACHE[cik10] = _get(f"https://data.sec.gov/submissions/CIK{cik10}.json").get("sicDescription") or ""
        except Exception:
            return False, "?unreachable"   # do not poison the cache; distinguishable from a real no-match
    sic = _SIC_CACHE[cik10]
    return any(h in sic.lower() for h in cfg["sector_hints"]), sic


def form_watch(days: int, cfg: dict) -> dict:  # {"hits": [...], "reached": int, "errored": int}
    """Ownership-change filings from the EDGAR daily index (form-type poll):
    SC 13D (activist stake) · SC 13E3 (going-private) · 25/15 (delisting/going dark).
    Free, no key; the forms list is thesis-configurable (event_forms)."""
    forms = tuple(cfg.get("event_forms", ["SC 13D", "SC 13E3", "25", "15-12B"]))
    out, checked, reached, errored = [], 0, 0, 0
    day = time.time()
    while checked < days and len(out) < 60:
        d = time.gmtime(day)
        day -= 86400
        if d.tm_wday >= 5:  # weekend: no index
            continue
        checked += 1
        qtr = (d.tm_mon - 1) // 3 + 1
        url = (f"https://www.sec.gov/Archives/edgar/daily-index/{d.tm_year}/QTR{qtr}/"
               f"form.{time.strftime('%Y%m%d', d)}.idx")
        try:
            req = urllib.request.Request(url, headers=_UA)
            with urllib.request.urlopen(req, timeout=20, context=_CTX) as r:
                text = r.read().decode("latin-1")
            reached += 1
        except Exception:
            errored += 1
            continue  # holiday / not yet published / EDGAR unreachable (403 without RADAR_CONTACT)
        for line in text.splitlines():
            parts = [p for p in line.split("  ") if p.strip()]
            if len(parts) < 4:
                continue
            form = parts[0].strip()
            if form not in forms:
                continue
            company = parts[1].strip()
            cik = parts[2].strip() if parts[2].strip().isdigit() else ""
            ok, sic = _sector_ok(cik.zfill(10), cfg) if cik else (False, "?nocik")
            if ok or sic in ("?unreachable", "?nocik"):  # don't silently drop an ownership signal on a SIC-lookup failure OR an unparseable CIK
                out.append({"form": form, "company": company, "sic": sic,
                            "date": time.strftime("%Y-%m-%d", d)})
    # reached==0 with errors means EVERY fetch failed — an all-clear here would be a false negative,
    # so the caller must distinguish it from a genuine no-hits sweep (parity with edgar_events/universe).
    return {"hits": out, "reached": reached, "errored": errored}


def edgar_events(days: int, cfg: dict, limit: int = 8) -> list[dict]:
    start = time.strftime("%Y-%m-%d", time.gmtime(time.time() - days * 86400))
    end = time.strftime("%Y-%m-%d")
    out = []
    for q in cfg["event_queries"]:
        url = ("https://efts.sec.gov/LATEST/search-index?q=" + urllib.parse.quote(q)
               + f"&forms=8-K&startdt={start}&enddt={end}")
        try:
            for h in _get(url).get("hits", {}).get("hits", [])[:limit]:
                s = h.get("_source", {})
                cik10 = ((s.get("ciks") or [""])[0]).zfill(10)
                ok, sic = _sector_ok(cik10, cfg) if cik10.strip("0") else (False, "?nocik")
                if ok or sic in ("?unreachable", "?nocik"):  # surface an event whose SIC lookup failed / CIK is unparseable, don't silently drop it
                    out.append({"query": q, "company": "; ".join(s.get("display_names", [])),
                                "sic": sic, "date": s.get("file_date", "")})
        except Exception as e:
            out.append({"query": q, "error": str(e)[:80]})
    return out


# ------------------- EU-listed + unlisted tier (GLEIF -> ESEF -> optional CH) -------------------
EU_CC = set("DE FR IT ES NL SE DK NO FI IE GB PL AT BE PT CH LU CZ GR RO HU EE LV LT SI SK HR BG CY MT IS".split())
NA_CC = {"US", "CA"}


def gleif(name: str) -> dict | None:
    """Entity identity from GLEIF (free, keyless): legal name, LEI, HQ country, status.
    Returns None only when the API RESPONDED with no match (genuine absence); raises
    ConnectionError when it was never reached, so a network outage is not mistaken for
    'no LEI / private company' (parity with form_watch / edgar_events)."""
    reached = False
    for flt in ("entity.legalName", "fulltext"):
        try:
            g = _get("https://api.gleif.org/api/v1/lei-records?filter%5B" + flt + "%5D="
                     + urllib.parse.quote(name) + "&page%5Bsize%5D=3")
            reached = True
        except Exception:
            continue
        for d in g.get("data", []):
            e = d["attributes"]["entity"]
            return {"lei": d["id"], "legal_name": e["legalName"]["name"],
                    "country": e["legalAddress"]["country"], "status": e["status"]}
    if not reached:
        raise ConnectionError("GLEIF was unreachable (every request failed)")
    return None  # the API responded but had no matching record — genuine absence


def _revenue_from_json(json_url: str):
    """Pull (value, period-label, currency, entity-name) from one ESEF xBRL-JSON report."""
    doc = _get("https://filings.xbrl.org" + json_url)
    facts = doc.get("facts", {})
    revs, name = [], None
    for fact in facts.values():
        dims = fact.get("dimensions", {})
        concept = dims.get("concept")
        if concept in ("ifrs-full:Revenue", "ifrs-full:RevenueFromContractsWithCustomers") \
                and len(dims) <= 4 and fact.get("value"):
            revs.append((dims.get("period", ""), float(fact["value"]), (dims.get("unit") or "").split(":")[-1]))
        elif concept in ("ifrs-full:NameOfReportingEntityOrOtherMeansOfIdentification",) and fact.get("value"):
            name = str(fact["value"]).strip()
    if not revs:
        return None
    period, val, cur = sorted(revs)[-1]
    return val, period[:10] + "→" + period.split("/")[-1][:10], cur, name


def esef_revenue(lei: str):
    """Latest annual IFRS revenue from the ESEF repository (free, keyless), via xBRL-JSON."""
    f = _get(f"https://filings.xbrl.org/api/filings?filter%5Bentity.identifier%5D={lei}"
             f"&sort=-period_end&page%5Bsize%5D=1")
    data = f.get("data", [])
    if not data or not data[0]["attributes"].get("json_url"):
        return None
    r = _revenue_from_json(data[0]["attributes"]["json_url"])
    return r[:3] if r else None


# EU-regulated markets whose issuers file in the ESEF repository (ISO-3166 alpha-2).
_EU_ESEF_COUNTRIES = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
                      "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK",
                      "SI", "ES", "SE", "NO", "IS"]


def eu_universe(year: str, cfg: dict, countries=None, limit: int = 60) -> dict:
    """The in-band EU-listed universe from the ESEF repository (filings.xbrl.org, free, keyless).
    Enumerates every ESEF filing for the target countries + period, then fetches revenue per
    filing (capped by `limit`) and band-filters. Honest about what the cap left unfetched."""
    period_end = year.replace("CY", "") + "-12-31" if year.upper().startswith("CY") else year
    countries = countries or _EU_ESEF_COUNTRIES
    lo, hi = cfg["band_usd_m"]
    filings, per_country = [], {}
    for cc in countries:
        try:
            r = _get("https://filings.xbrl.org/api/filings?"
                     + urllib.parse.urlencode({
                         "filter": json.dumps([{"name": "country", "op": "eq", "val": cc},
                                               {"name": "period_end", "op": "eq", "val": period_end}]),
                         "page[size]": 500}))
        except Exception:
            per_country[cc] = "error"
            continue
        rows = [d["attributes"]["json_url"] for d in r.get("data", []) if d["attributes"].get("json_url")]
        per_country[cc] = len(rows)
        filings += [(cc, u) for u in rows]
    enumerated = len(filings)
    to_fetch = filings[:limit]
    fetched = len(to_fetch)

    # the ESEF endpoint is slow; fetch revenue CONCURRENTLY so a country sweep is seconds, not minutes
    # (was sequential — up to `limit` round-trips one at a time, which cost the demo ~5 minutes).
    def _rev(item):
        cc, url = item
        try:
            return cc, url, _revenue_from_json(url)
        except Exception:
            return cc, url, None

    with ThreadPoolExecutor(max_workers=5) as ex:   # polite to the ESEF endpoint; still seconds, not minutes
        results = list(ex.map(_rev, to_fetch))

    in_band, seen = [], set()
    for cc, url, r in results:
        if not r:
            continue
        val, _, cur, name = r
        m = val / 1e6
        name = name or url.split("/")[1]
        key = name.lower()
        if key in seen or key in cfg["_owned"] or key in cfg["_pipeline"]:
            continue
        seen.add(key)
        if lo <= m <= hi:          # native currency (mostly EUR) — indicative vs the USD band
            in_band.append((name, m, cur, cc))
    in_band.sort(key=lambda r: r[1])
    return {"enumerated": enumerated, "fetched": fetched, "in_band": in_band,
            "per_country": per_country, "capped": enumerated > fetched}


def company(name: str, cfg: dict) -> dict:
    """The gate-check chain for EU-listed and unlisted companies:
    GLEIF (identity/HQ) -> ESEF (revenue if EU-listed) -> honest n.d. for the rest."""
    out = {"query": name}
    try:
        g = gleif(name)
    except ConnectionError as e:
        out["identity"] = f"UNAVAILABLE: GLEIF unreachable ({e}) — this is NOT 'no LEI / private'; retry"
        out["next"] = "the identity tier could not run; do not conclude private — re-run when the network is up"
        return out
    if not g:
        out["identity"] = "no LEI found (typical for private app companies — LEIs cover financial-market entities)"
        out["next"] = "use the chatter/press tiers; for UK private companies set CH_API_KEY (Companies House)"
        return out
    out.update(g)
    cc = g["country"]
    ok = ("europe" in cfg["regions"] and cc in EU_CC) or ("north-america" in cfg["regions"] and cc in NA_CC)
    out["gate_region"] = "PASS" if ok else "FAIL"
    rev = None
    try:
        rev = esef_revenue(g["lei"])
    except Exception:
        pass
    if rev:
        val_m, cur = rev[0] / 1e6, rev[2]
        lo, hi = cfg["band_usd_m"]
        out["revenue_m"] = f"{round(val_m)} {cur}"
        out["revenue_period"] = rev[1]
        out["gate_band"] = ("PASS" if lo <= val_m <= hi * 1.1 else "FAIL") + f" (indicative, {cur})"
        out["listed"] = "EU-listed (ESEF filer)"
    else:
        out["gate_band"] = ("n.d. — no filing in the filings.xbrl.org repository; the company may still be "
                            "EU-listed (repository coverage varies by country — e.g. DE is partial); "
                            "structured revenue unavailable, fall back to press")
        out["listed"] = "no ESEF filing found (absence of evidence, not evidence of absence)"
    return out


# ----------------------------- consumer tier (free, keyless) -----------------------------
def wiki_interest(article: str, days: int) -> dict:
    """Brand-interest momentum: Wikipedia pageviews, this window vs the previous one."""
    end = time.strftime("%Y%m%d", time.gmtime(time.time() - 86400))
    start = time.strftime("%Y%m%d", time.gmtime(time.time() - 2 * days * 86400))
    art = urllib.parse.quote(article.replace(" ", "_"), safe="")
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/"
           f"all-access/user/{art}/daily/{start}/{end}")
    items = _get(url).get("items", [])
    views = [(it["timestamp"][:8], it["views"]) for it in items]
    half = len(views) // 2
    prev = sum(v for _, v in views[:half]) or 1
    cur = sum(v for _, v in views[half:])
    return {"article": article, "days": days, "current": cur, "previous": prev,
            "delta_pct": round(100 * (cur - prev) / prev, 1)}


def appstore(name: str, country: str = "us") -> list[dict]:
    """Loyal-base proxy: App Store rating volume + average (iTunes Search, free, keyless)."""
    url = (f"https://itunes.apple.com/search?term={urllib.parse.quote(name)}"
           f"&entity=software&country={country}&limit=3")
    out = []
    for r in _get(url).get("results", []):
        out.append({"app": r.get("trackName"), "rating": r.get("averageUserRating"),
                    "ratings_count": r.get("userRatingCount"), "genre": r.get("primaryGenreName"),
                    "seller": r.get("sellerName")})
    return out


def loyalty_card(brand: str, days: int) -> list[str]:
    """The brand-strength card: the loyalty proxies that are free and monitorable.
    (Loyalty proper = retention/NRR is non-public for private companies — these are proxies.)"""
    lines = []
    try:
        apps = appstore(brand)
        if apps:
            a = apps[0]
            lines.append(f"committed base (App Store): **{a['ratings_count']:,} ratings, avg {a['rating']:.2f}** — {a['app']}")
        else:
            lines.append("committed base (App Store): no app found")
    except Exception as e:
        lines.append(f"committed base (App Store): unavailable ({str(e)[:50]})")
    try:
        w = wiki_interest(brand, days)
        lines.append(f"brand interest (Wikipedia): {w['current']:,} views/{days}d, **{w['delta_pct']:+}%** vs previous window")
    except Exception:
        lines.append("brand interest (Wikipedia): no article found (use the exact title)")
    try:
        r = _get(f"https://www.reddit.com/r/{urllib.parse.quote(brand)}/about.json").get("data", {})
        if r.get("subscribers"):
            lines.append(f"community (r/{brand}): **{r['subscribers']:,} members**, {r.get('active_user_count', '?')} active now")
    except Exception:
        lines.append(f"community (r/{brand}): unavailable on this network — check reddit.com/r/{brand} manually")
    return lines


# ----------------------------- CLI -----------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?", default="", help="brand/theme; tickers with --gates; CYyyyy with --universe")
    ap.add_argument("--thesis", default=str(DEFAULT_THESIS), help="thesis yaml (the acquirer's hunt)")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--rank", action="store_true", help="rank comma-separated candidates by maturity")
    ap.add_argument("--gates", action="store_true", help="EDGAR gate-check for comma-separated tickers")
    ap.add_argument("--events", action="store_true", help="EDGAR 8-K sale/divestiture sweep, sector-filtered")
    ap.add_argument("--universe", action="store_true", help="EDGAR frames: US annual revenues in band (query=CY2024)")
    ap.add_argument("--universe-eu", dest="universe_eu", action="store_true",
                    help="ESEF repository: EU-listed annual revenues in band (query=CY2024)")
    ap.add_argument("--countries", default="", help="ISO-2 codes for --universe-eu (e.g. IT,DE,FR); default = all EU ESEF")
    ap.add_argument("--forms", action="store_true",
                    help="EDGAR daily-index form watch: 13D (activist), 13E-3 (going-private), 25/15 (delisting)")
    ap.add_argument("--interest", action="store_true", help="Wikipedia pageviews momentum for a brand (query=article)")
    ap.add_argument("--appstore", action="store_true", help="App Store rating volume/average for an app (query=name)")
    ap.add_argument("--company", action="store_true",
                    help="EU-listed/unlisted gate chain: GLEIF identity -> ESEF revenue (query=legal name)")
    ap.add_argument("--loyalty", action="store_true", help="brand-strength card: ratings + interest + community (query=brand)")
    ap.add_argument("--preflight", action="store_true", help="show thesis + sources status; run nothing")
    a = ap.parse_args()
    try:
        cfg = load_thesis(a.thesis)
    except FileNotFoundError:
        print(f"# thesis file not found: {a.thesis} — copy theses/bending-spoons.yaml and tune it.")
        sys.exit(2)
    except Exception as e:
        print(f"# thesis file invalid ({a.thesis}): {str(e)[:120]}")
        sys.exit(2)
    hdr = f"[thesis: {cfg['name']} · band ${cfg['band_usd_m'][0]}M–${cfg['band_usd_m'][1]}M · {'/'.join(cfg['regions'])}]"

    if a.preflight:
        print(f"# radar preflight {hdr}")
        print(f"- thesis file: {cfg['_path']}")
        print(f"- signals: {', '.join(cfg['signals'])} · weights: {cfg['weights']}")
        print(f"- sector hints: {', '.join(cfg['sector_hints'])}")
        print(f"- dedup: {len(cfg['_owned'])} owned · {len(cfg['_pipeline'])} in pipeline")
        print(f"- SEC contact UA: {'SET' if os.environ.get('RADAR_CONTACT') else 'NOT SET (export RADAR_CONTACT=…; EDGAR will 403)'}")
        for label, probe in [("HN (chatter)", lambda: hn("test", 7, 1)),
                             ("EDGAR tickers (structured)", _tickers)]:
            try:
                probe()
                print(f"- {label}: reachable")
            except Exception as e:
                print(f"- {label}: UNREACHABLE ({str(e)[:60]})")
        print("No sweeps executed (preflight).")
        return

    if a.gates:
        print(f"# radar-gates {hdr} — mechanical gates from EDGAR [derived]")
        for tkr in [x.strip() for x in a.query.split(",") if x.strip()]:
            g = gates(tkr, cfg)
            if "error" in g:
                print(f"- {tkr}: {g['error']}")
            else:
                print(f"- **{g['company']}** ({g['ticker']}): revenue {g.get('revenue_m','?')}M "
                      f"(FY to {g.get('revenue_asof','?')}) → {g['gate_band']} · HQ {g['hq']} → "
                      f"{g['gate_region']} · {g['sic']} → {g['gate_sector']}")
        print("\n_Checkable gates: band, region, sector. The judgment gates stay with the screen step._")
        return

    if a.company:
        print(f"# radar-company {hdr} — GLEIF → ESEF chain (EU-listed + unlisted) [derived]")
        c = company(a.query, cfg)
        for k in ("legal_name", "lei", "country", "status", "listed", "revenue_m", "revenue_period",
                  "gate_band", "gate_region", "identity", "next"):
            if c.get(k):
                print(f"- {k.replace('_', ' ')}: {c[k]}")
        print("\n_GLEIF covers entities with an LEI; ESEF covers EU-regulated-market filers. Private"
              " app companies have neither — that slice is chatter + press + judgment (the manual analysis)._")
        return

    if a.loyalty:
        print(f"# radar-loyalty {hdr} — brand-strength proxies for '{a.query}'")
        for line in loyalty_card(a.query, a.days):
            print(f"- {line}")
        print("\n_Proxies, monitorable over time (snapshot + diff). Loyalty proper (retention/NRR) is"
              " non-public for private companies — it enters at diligence. [derived where API, else n.d.]_")
        return

    if a.forms:
        print(f"# radar-forms {hdr} — ownership-change filings, last {a.days} business days (EDGAR daily index)")
        fw = form_watch(a.days, cfg)
        hits = fw["hits"]
        for e in hits:
            label = {"SC 13D": "ACTIVIST STAKE", "SC 13E3": "GOING-PRIVATE", "25": "DELISTING",
                     "15-12B": "DEREGISTRATION"}.get(e["form"], e["form"])
            print(f"- [{e['date']}] {label}: {e['company']} · {e['sic']}")
        if not hits and fw["reached"] == 0:
            print(f"- UNAVAILABLE: no EDGAR daily index was reachable ({fw['errored']} fetch(es) failed) — "
                  f"this is NOT an all-clear; check RADAR_CONTACT / network and re-run")
        elif not hits:
            print(f"- no in-thesis filings in the window ({fw['reached']} day(s) checked)")
        print("\n_Sector-filtered per thesis. 13D = a sale precursor; 13E-3/25/15 = going dark. "
              "Run --gates on the name next. [derived from EDGAR]_")
        return

    if a.interest:
        try:
            w = wiki_interest(a.query, a.days)
        except Exception as e:
            print(f"# radar-interest: no Wikipedia article found for '{a.query}' "
                  f"({'404' if '404' in str(e) else str(e)[:60]}). Use the exact article title "
                  f"(e.g. 'Evernote', 'WeTransfer').")
            return
        arrow = "↓ DECLINING" if w["delta_pct"] < -10 else ("↑ growing" if w["delta_pct"] > 10 else "→ flat")
        print(f"# radar-interest {hdr} — Wikipedia pageviews momentum")
        print(f"- **{w['article']}**: {w['current']:,} views last {a.days}d vs {w['previous']:,} the {a.days}d before "
              f"→ **{w['delta_pct']:+}%** {arrow}")
        print("\n_Brand-interest proxy (free, keyless). Sustained decline feeds the momentum signal. [derived]_")
        return

    if a.appstore:
        print(f"# radar-appstore {hdr} — rating base (iTunes Search, free)")
        results = appstore(a.query)
        if not results:
            print(f"- no apps found for '{a.query}'")
        for r in results:
            rc = r["ratings_count"] or 0                 # iTunes returns null for a ratingless app
            avg = f"{r['rating']:.2f}" if r["rating"] is not None else "n.d."
            print(f"- **{r['app']}** ({r['seller']}, {r['genre']}): {rc:,} ratings, avg {avg}")
        print("\n_Rating volume ≈ committed-base size; track the count over time for momentum. [derived]_")
        return

    if a.events:
        print(f"# radar-events {hdr} — sale/divestiture language in 8-Ks, last {a.days} days")
        for e in edgar_events(a.days, cfg):
            if "error" in e:
                print(f"- {e['query']}: unavailable ({e['error']})")
            else:
                print(f"- [{e['date']}] {e['company']} · {e.get('sic','')} — matched {e['query']}")
        print("\n_Sector-filtered per thesis. Each hit is an OWNERSHIP signal: run --gates on the ticker next._")
        return

    if a.universe:
        yr = a.query if a.query.upper().startswith("CY") else "CY" + (a.query or str(time.gmtime().tm_year - 1))
        lo, hi = cfg["band_usd_m"]
        print(f"# radar-universe {hdr} — US-reported annual revenue {yr}, in band (EDGAR frames, "
              f"{len(_REVENUE_CONCEPTS)} revenue concepts unioned)")
        u = universe(yr, cfg)
        if not u["in_band"] and u["errors"]:
            for e in u["errors"]:
                print(f"- concept unavailable: {e}")
            return
        rows = u["in_band"]
        print(f"**{len(rows)} companies in band** (of {u['reporting']} unique filers reporting; "
              f"{u['dropped_owned_pipeline']} owned/pipeline names removed). Evenly-sampled slice:")
        for _c, name, m in rows[::max(1, len(rows) // 20)][:20]:
            print(f"- {name} — ${m:,.0f}M")
        for e in u["errors"]:
            print(f"\n_partial: {e}_")
        print("\n_The raw band, all sectors, US-listed only. Sector + region are judged per candidate"
              " (--gates); the EU-listed slice comes from --universe-eu / --company; private companies"
              " are chatter + press + judgment. This is the mechanical top of the funnel — narrow it with the gates._")
        return

    if a.universe_eu:
        yr = a.query if a.query.upper().startswith("CY") else "CY" + (a.query or str(time.gmtime().tm_year - 1))
        countries = [c.strip().upper() for c in a.countries.split(",") if c.strip()] or None
        cap = max(a.limit, 60)
        print(f"# radar-universe-eu {hdr} — EU-listed annual revenue {yr}, in band (ESEF repository, "
              f"filings.xbrl.org, native currency)")
        u = eu_universe(yr, cfg, countries, cap)
        cov = ", ".join(f"{cc}:{n}" for cc, n in sorted(u["per_country"].items()) if n)
        print(f"**{u['enumerated']} ESEF filings enumerated** for {yr} ({cov}).")
        if u["capped"]:
            print(f"_Revenue fetched for the first {u['fetched']} (raise --limit or narrow --countries "
                  f"to fetch more; enumeration is complete, revenue extraction is capped)._")
        print(f"\n**{len(u['in_band'])} in band** (of {u['fetched']} fetched; owned/pipeline removed):")
        for name, m, cur, cc in u["in_band"]:
            print(f"- {name} ({cc}) — {m:,.0f}M {cur}")
        print("\n_Band is indicative: revenue is in native currency (mostly EUR), not converted to USD."
              " ESEF covers EU-regulated-market issuers; coverage varies by country. Deep-dive any name"
              " with --company. [derived from ESEF]_")
        return

    if a.rank:
        rows = []
        for cand in [c.strip() for c in a.query.split(",") if c.strip()]:
            cl = cand.lower()
            if cl in cfg["_owned"]:
                rows.append((cand, None, ["ALREADY OWNED"]))
            elif cl in cfg["_pipeline"]:
                rows.append((cand, None, [f"IN PIPELINE ({cfg['_pipeline'][cl]})"]))
            else:
                s, fired = maturity(sweep(cand, a.days, a.limit, cfg), a.days, cfg)
                rows.append((cand, s, fired))
        rows.sort(key=lambda r: -(r[1] or -1))
        print(f"# radar-rank {hdr} — {a.days}-day maturity [decision: formula in this script]")
        print("| candidate | maturity | signals fired |\n|---|---|---|")
        for cand, s, fired in rows:
            print(f"| {cand} | {'—' if s is None else s} | {', '.join(fired) or 'none'} |")
        print("\n_Maturity ranks the press signal only; the gates are judged at screen. [to-validate — press only]_")
        return

    # single brand/theme sweep
    ql0 = a.query.lower()
    if ql0 in cfg["_owned"]:
        print(f"# '{a.query}' is ALREADY OWNED — not a target. Use the monitor loop for held assets.")
        return
    if ql0 in cfg["_pipeline"]:
        print(f"# '{a.query}' is ALREADY IN THE PIPELINE (status: {cfg['_pipeline'][ql0]}) — advance it, don't re-source it.")
        return
    buckets = sweep(a.query, a.days, a.limit, cfg)
    n = sum(len(v) for v in buckets.values())
    print(f"# radar-sweep: {a.query} {hdr} — last {a.days} days ({n} items, HN + Reddit)")
    print("_Press/social signal → [to-validate — press only]._\n")
    labels = {"unclassified": "unclassified (judge manually)",
              "out-of-band": "out-of-band (outside the thesis band — world signal, not targets)",
              "already-owned": "already OWNED — not a target",
              "already-in-pipeline": "already in the PIPELINE — advance it, don't re-source it"}
    for sig in list(cfg["signals"]) + ["unclassified", "out-of-band", "already-owned", "already-in-pipeline"]:
        rows = buckets.get(sig, [])
        if not rows:
            continue
        print(f"## {labels.get(sig, sig.upper())} — {len(rows)} hit(s)")
        for it in rows[:8]:
            print(f"- [{it['score']}▲ {it['comments']}💬 {it['date']} {it['src']}] {it['title']}\n  {it['url']}")
        print()
    s, fired = maturity(buckets, a.days, cfg)
    print(f"**Signals fired:** {', '.join(fired) or 'none'} · **maturity: {s}** — the judgment is the human's/agent's.")


if __name__ == "__main__":
    main()
