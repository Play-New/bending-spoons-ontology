"""radar-sweep unit tests (offline: the bucketing brain) + optional live smoke.
python3 test_radar.py <repo_root> [--live]
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "radar_sweep", ROOT / ".claude/skills/radar-sweep/scripts/radar_sweep.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)
CFG = radar.load_thesis()                    # the default (subject) thesis
import tempfile, yaml as _yaml
_t2 = {"name": "declination-test", "band_usd_m": [5, 300], "regions": ["europe"],
       "sector_hints": ["recruiting"], "signals": {"distress": ["layoff", "laid off"],
       "market-shift": ["ai recruiting"], "loyal-base": ["loyal"]},
       "weights": {"distress": 2.5, "market-shift": 2.0},
       "quality_multipliers": {"loyal-base": 1.3}, "event_queries": [], "out_of_band": [],
       "dedup": {"owned": [], "pipeline": []}, "press_languages": ["en"]}
_tmp = Path(tempfile.mkdtemp()) / "declination.yaml"
_tmp.write_text(_yaml.safe_dump(_t2))
CFG2 = radar.load_thesis(_tmp)

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))


mk = lambda title, score=1: {"src": "hn", "title": title, "url": "u", "score": score, "comments": 0, "date": "2026-07-05"}
b = radar.bucket([
    mk("Acme announces layoffs of 20% of staff", 50),
    mk("Acme explores sale to private equity", 40),
    mk("Acme users report declining quality and churn", 30),
    mk("Acme valuation cut in down round", 20),
    mk("Can ChatGPT replace Acme entirely?", 10),
    mk("Acme releases a new logo", 5),
], CFG)
record(any("layoffs" in i["title"] for i in b["distress"]), "bucket: layoffs → distress")
b2 = radar.bucket([mk("Bandcamp has laid off most of their engineers", 43)], CFG)
record(bool(b2["distress"]), "bucket: 'laid off' variant → distress (the Bandcamp miss)")
record(any("sale" in i["title"] for i in b["ownership"]), "bucket: explores sale → ownership")
record(any("churn" in i["title"] for i in b["momentum"]), "bucket: churn → momentum")
record(any("down round" in i["title"] for i in b["valuation"]), "bucket: down round → valuation")
record(any("ChatGPT" in i["title"] for i in b["ai-pressure"]), "bucket: ChatGPT → ai-pressure")
record(any("logo" in i["title"] for i in b["unclassified"]), "bucket: neutral → unclassified")
record(b["distress"][0]["score"] == 50, "ranking: engagement-sorted within bucket")
multi = radar.bucket([mk("Acme layoffs amid declining users")], CFG)
record(multi["distress"] and multi["momentum"], "multi-signal title lands in both buckets")
oob = radar.bucket([mk("Meta announces massive layoffs", 500), mk("Microsoft acquisition rumors", 300)], CFG)
record(not oob["distress"] and not oob["ownership"] and len(oob["out-of-band"]) == 2,
       "mega-caps binned out-of-band, never counted as target signal")

# maturity ranking [decision-formula regression]
b_hot = radar.bucket([mk("Acme explores sale to private equity", 100), mk("Acme layoffs", 50)], CFG)
b_cold = radar.bucket([mk("Acme ships new feature", 500)], CFG)
s_hot, fired_hot = radar.maturity(b_hot, 30, CFG)
s_cold, _ = radar.maturity(b_cold, 30, CFG)
record(s_hot > s_cold and s_cold == 0.0, f"maturity: ownership+distress ({s_hot}) outranks neutral buzz ({s_cold})")
b_loyal = radar.bucket([mk("Acme layoffs", 50), mk("I still use Acme every day", 10)], CFG)
s_loyal, fired_loyal = radar.maturity(b_loyal, 30, CFG)
b_plain = radar.bucket([mk("Acme layoffs", 50)], CFG)
s_plain, _ = radar.maturity(b_plain, 30, CFG)
record(s_loyal > s_plain and any("loyal" in f for f in fired_loyal),
       "maturity: loyal-base multiplies quality (distressed WITH base > without)")
own = radar.bucket([mk("evernote still beloved", 10)], CFG)
record(bool(own["already-owned"]), "dedup: owned brand binned already-owned")

# EDGAR helpers, offline
record(radar._is_annual({"start": "2025-01-01", "end": "2025-12-31"}), "annual: calendar FY detected")
record(radar._is_annual({"start": "2024-07-01", "end": "2025-06-30"}), "annual: fiscal-year span detected")
record(not radar._is_annual({"start": "2025-01-01", "end": "2025-03-31"}), "annual: quarter rejected")
# thesis declination: same engine, different hunt
record(CFG["name"] == "bending-spoons" and CFG["band_usd_m"] == [50, 5000], "default thesis = the subject's contract")
record(len(CFG["_owned"]) >= 19 and "evernote" in CFG["_owned"] and "itranslate" in CFG["_owned"], f"default thesis dedup reads the model ({len(CFG['_owned'])} owned)")
record(CFG2["name"] == "declination-test" and CFG2["regions"] == ["europe"]
       and "market-shift" in CFG2["signals"] and CFG2["band_usd_m"] == [5, 300],
       "declined thesis loads: EU, recruiting, own signals and band")
b_alt = radar.bucket([mk("Acme announces layoffs of staff", 10), mk("AI recruiting platforms rise", 10)], CFG2)
record(bool(b_alt["distress"]) and bool(b_alt["market-shift"]), "declined thesis buckets with ITS OWN signals")
own2 = radar.bucket([mk("evernote still beloved", 10)], CFG2)
record(not own2["already-owned"], "declined thesis has its own dedup (evernote NOT owned there)")
record("--gates" in open(ROOT / ".claude/skills/radar-sweep/scripts/radar_sweep.py").read()
       and "ifrs-full" in open(ROOT / ".claude/skills/radar-sweep/scripts/radar_sweep.py").read(),
       "structured tier present: gates + IFRS/20-F support")

# offline: a GLEIF network outage must NOT be reported as "no LEI / private" (silent-false-negative guard)
_real_get = radar._get
radar._get = lambda url: (_ for _ in ()).throw(OSError("simulated network outage"))
try:
    try:
        radar.gleif("Whatever GmbH")
        record(False, "gleif: total outage must raise, not return None")
    except ConnectionError:
        record(True, "gleif: total outage raises ConnectionError (not confused with absence)")
    except Exception as e:
        record(False, "gleif: outage should raise ConnectionError", str(e))
    c = radar.company("Whatever GmbH", CFG)
    record("UNAVAILABLE" in c.get("identity", "") and "unreachable" in c.get("identity", ""),
           "company: GLEIF outage reported as UNAVAILABLE, not 'no LEI / private'", c.get("identity", ""))
finally:
    radar._get = _real_get

if "--live" in sys.argv:
    try:
        hits = radar.hn("Evernote", 60, 10)
        record(isinstance(hits, list), f"live: HN reachable ({len(hits)} hits)")
        record(all("everyone" not in h["title"].lower() or "evernote" in h["title"].lower() for h in hits),
               "live: exact-phrase query (no everyone-for-Evernote fuzz)")
    except Exception as e:
        record(False, "live: HN reachable", e)
    import os
    if os.environ.get("RADAR_CONTACT"):
        try:
            g = radar.gates("DBX", CFG)
            record(g.get("gate_band") == "PASS" and g.get("gate_region") == "PASS",
                   f"live: EDGAR gates on DBX ({g.get('revenue_m')})")
        except Exception as e:
            record(False, "live: EDGAR gates on DBX", e)
        try:
            w = radar.wiki_interest("Evernote", 14)
            record("delta_pct" in w and w["current"] > 0, f"live: wiki interest ({w.get('delta_pct')}%)")
        except Exception as e:
            record(False, "live: wiki interest", e)
        try:
            apps = radar.appstore("Evernote")
            record(any("Evernote" in (r.get("app") or "") for r in apps), "live: appstore lookup")
        except Exception as e:
            record(False, "live: appstore lookup", e)
        try:
            c = radar.company("Ubisoft Entertainment", CFG)
            record(c.get("gate_band", "").startswith("PASS") and c.get("country") == "FR",
                   f"live: GLEIF→ESEF chain (Ubisoft {c.get('revenue_m')})")
            c2 = radar.company("komoot GmbH", CFG)
            record("identity" in c2 and "no LEI" in c2["identity"], "live: private-company honest fallback")
            # TeamViewer SE: valid LEI but absent from filings.xbrl.org (DE coverage is partial).
            # The card must NOT claim "not a filer" — absence of evidence, not evidence of absence.
            c3 = radar.company("TeamViewer SE", CFG)
            record("absence of evidence" in c3.get("listed", "") and c3.get("gate_region") == "PASS",
                   "live: repository-gap honesty (TeamViewer, DE)")
            card = radar.loyalty_card("Evernote", 14)
            record(len(card) == 3 and any("ratings" in l for l in card), "live: loyalty card (3 proxies)")
        except Exception as e:
            record(False, "live: company/loyalty tier", e)
        try:
            fw = radar.form_watch(2, CFG)
            record(isinstance(fw, dict) and "hits" in fw and "reached" in fw and "errored" in fw,
                   f"live: EDGAR form-watch (reached={fw.get('reached')}, {len(fw.get('hits', []))} in-thesis hits)")
        except Exception as e:
            record(False, "live: EDGAR form-watch", e)
        try:
            # the union of revenue concepts must beat any single concept — the funnel-top fix.
            # Single 'Revenues' gave ~1,000 in-band; the union must clear a real funnel scale.
            u = radar.universe("CY2024", CFG)
            record(len(u["in_band"]) > 1500 and u["reporting"] > 3000,
                   f"live: universe union (in-band {len(u['in_band'])} of {u['reporting']} filers)")
            names = {n.lower() for _c, n, _m in u["in_band"]}   # in_band is (cik, name, m)
            record(not (names & CFG["_owned"]), "live: universe excludes owned assets")
            record(all(isinstance(t, tuple) and len(t) == 3 for t in u["in_band"][:5]),
                   "live: universe in_band is (cik, name, m) 3-tuples (discover gates by CIK)")
        except Exception as e:
            record(False, "live: universe union", e)
        try:
            # EU universe: Italy 2024 must enumerate a real filing count and return in-band names.
            eu = radar.eu_universe("CY2024", CFG, ["IT"], 12)
            record(eu["enumerated"] > 100 and eu["fetched"] <= 12,
                   f"live: EU universe enumerate+cap (IT {eu['enumerated']} filings, {eu['fetched']} fetched)")
            eu_names = {n.lower() for n, *_ in eu["in_band"]}
            record(not (eu_names & CFG["_owned"]) and not (eu_names & set(CFG["_pipeline"])),
                   "live: EU universe excludes owned/pipeline")
        except Exception as e:
            record(False, "live: EU universe", e)
    else:
        record(True, "live: EDGAR gates skipped (RADAR_CONTACT not set)")

print(json.dumps(R))
