"""One-time builder: fetch SIC + HQ-state for every in-band US filer and cache it, so discover() can
screen the WHOLE universe instantly instead of a slice. SIC/state are stable per company, so this is a
point-in-time [derived from EDGAR] snapshot. Run:  RADAR_CONTACT="you@x" python3 build_sic_cache.py
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import radar_sweep as R  # noqa: E402

if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    print(__doc__ or "usage: build_sic_cache.py [cooldown_seconds]")
    sys.exit(0)
cooldown = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
if cooldown:
    print(f"cooldown {cooldown}s (let any EDGAR 429 block clear)…", flush=True)
    time.sleep(cooldown)

cfg = R.load_thesis()
u = R.universe("CY2024", cfg)
band = u["in_band"]  # (cik, name, m)
print(f"in-band universe: {len(band)} filers to index", flush=True)
if not band:
    print("universe empty — EDGAR is likely still rate-limiting. Aborting WITHOUT writing (keep any good cache).", flush=True)
    sys.exit(1)

cache: dict = {}


def fetch(item):
    cik, _name, _m = item
    for attempt in range(5):
        try:
            time.sleep(0.25)  # in-request throttle; with 2 workers stays ~4 req/s, well under SEC's ~10/s
            subs = R._get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json")
            loc = ((subs.get("addresses", {}).get("business", {}) or {}).get("stateOrCountryDescription") or "")
            sic = subs.get("sicDescription") or ""
            return str(int(cik)), [sic, loc]
        except Exception:
            time.sleep(2 ** attempt)  # exponential backoff on 429/5xx (EDGAR blocks bursts hard)
    return None


def _pass(items, workers):
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, r in enumerate(ex.map(fetch, items), 1):
            if r:
                cache[r[0]] = r[1]
            if i % 250 == 0:
                print(f"  {i}/{len(items)} ({len(cache)} cached)", flush=True)


_pass(band, 2)
for rnd in range(4):  # retry the misses a few times — EDGAR throttling is transient
    misses = [it for it in band if str(int(it[0])) not in cache]
    if not misses:
        break
    print(f"retry round {rnd + 1}: {len(misses)} misses…", flush=True)
    time.sleep(15)
    _pass(misses, 1)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "edgar_sic_hq.json")
os.makedirs(os.path.dirname(out), exist_ok=True)

# coverage guard (defect-to-test): a partial build — EDGAR throttled the per-CIK /submissions/ fetches
# through all retries — must never clobber a more complete cache, or discover() silently under-screens
# afterward. Refuse to shrink the index; keep the larger existing one and re-run when EDGAR isn't throttling.
new_n = len(cache)
existing_n = 0
if os.path.exists(out):
    try:
        existing_n = len(json.load(open(out, encoding="utf-8")).get("sic_hq", {}))
    except Exception:
        existing_n = 0
coverage = new_n / len(band) if band else 0
if new_n < existing_n:
    print(f"REFUSING to overwrite: this build indexed {new_n} filers but the existing cache holds "
          f"{existing_n} — keeping the larger index (EDGAR was likely throttling). Re-run later.", flush=True)
    sys.exit(1)
json.dump({"as_of": "CY2024", "band_usd_m": cfg["band_usd_m"], "sic_hq": cache}, open(out, "w"))
print(f"WROTE {os.path.relpath(out)} — {new_n} of {len(band)} in-band filers indexed ({coverage:.0%})", flush=True)
