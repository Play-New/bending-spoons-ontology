#!/usr/bin/env python3
"""deal-audit, runnable — the mechanical subset of the §5 invariants
(foundations/ontology.md §5-§6; the full contract lives in
mcp/audit-contract.md). Run from the repo root:
    python3 mcp/audit.py
Exit code 0 = green. Every defect once found by hand becomes a check here."""
import csv, glob, os, re, sys

defects = []

# csv rows parse with uniform column counts (inv. 2 backing / the unquoted-comma defect)
for c in glob.glob('world-model/**/*.csv', recursive=True):
    rows = [r for r in csv.reader(open(c)) if r and not r[0].startswith('#')]
    if not all(len(r) == len(rows[0]) for r in rows):
        defects.append(f"csv shape: {c}")

# no framework vocabulary, author or framework-company names in model files (rule 9; the paraphrase leak)
banned = re.compile(r'palantir|dorsey|botha|foundry|honest signal|signal that does not lie|the honest read|mini-agi|cash app|sequoia|block\.xyz'
                    r'|user decision|this session|review of \d{4}-\d{2}-\d{2}', re.I)  # incl. session-process chatter — files are the artifact, git is the process
banned_proper = re.compile(r'\bBlock\b|\bTIDAL\b|\bSquare\b')  # case-sensitive proper nouns
allowed = {'README.md', 'foundations/ontology.md', 'foundations/org-as-an-intelligence.md', 'CLAUDE.md'}
# scan .md AND .csv — the backing datasets carry prose in note fields, and a removed concept
# ("honest signal") once leaked into financials.csv precisely because this loop was .md-only (defect-to-test)
for f in glob.glob('**/*.md', recursive=True) + glob.glob('**/*.csv', recursive=True):
    if f in allowed or f.startswith(('sources/', 'mcp/')):
        continue
    t = open(f, encoding='utf-8').read()
    if banned.search(t) or banned_proper.search(t):
        defects.append(f"banned vocab: {f}")

# node frontmatter properties == backing csv row, value for value (inv. 2, static 1:1)
try:
    import yaml
except ImportError:
    yaml = None
    # fail CLOSED: this is the only check that compares stored values node↔csv; if it cannot run,
    # the audit must go red (a commit-gating safety net must never degrade to green).
    defects.append("pyyaml not installed — node↔csv reconciliation could not run (audit fails closed)")
if yaml is not None:
    RECON = [  # (csv path, key column, node path template, id suffix)
        ('world-model/company/businesses.csv', 'business', 'world-model/company/businesses/{}.md', ''),
        ('interfaces/interfaces.csv', 'interface', 'interfaces/{}.md', '-interface'),
    ]
    for cpath, key, tpl, suffix in RECON:
        csv_rows = {r[key]: r for r in
                    csv.DictReader(l for l in open(cpath) if not l.startswith('#'))}
        prop_cols = [c for c in next(iter(csv_rows.values())) if c not in (key, 'source', 'note')]
        for name, row in csv_rows.items():
            node_path = tpl.format(name)
            if not os.path.exists(node_path):  # clean defect, not an uncaught FileNotFoundError
                defects.append(f"csv row without node file: {cpath} '{name}' -> missing {node_path}")
                continue
            t = open(node_path, encoding='utf-8').read()
            fm = yaml.safe_load(t.split('---')[1])
            node_props = {k: str(v) for k, v in (fm.get('properties') or {}).items()}
            for c in prop_cols:
                if node_props.get(c) != row[c]:
                    defects.append(f"node↔csv drift: {name}.{c}: node={node_props.get(c)!r} csv={row[c]!r}")
            if fm.get('id') != name + suffix:
                defects.append(f"node id != csv key: {name}")

# freshness: every node carries as_of (data period) + last_synced (last verified against sources/)
for f in glob.glob('world-model/**/*.md', recursive=True) + glob.glob('capabilities/**/*.md', recursive=True) + glob.glob('interfaces/*.md') + ['ontology.md'] + ['will.md', 'bending-spoons-as-an-intelligence.md']:
    t = open(f, encoding='utf-8').read()
    if not t.startswith('---'):
        continue
    fm = t.split('---')[1]
    if 'last_synced:' not in fm or 'as_of:' not in fm:
        defects.append(f"no freshness stamp (as_of/last_synced): {f}")

# every world-model node declares its properties (the 1:1 anchor; the gap node declares 'none')
for f in glob.glob('world-model/**/*.md', recursive=True):
    if f.endswith('index.md') or f.endswith('README.md'):
        continue
    t = open(f, encoding='utf-8').read()
    if not re.search(r'\*\*Properties\b|- properties', t):
        defects.append(f"no properties declaration: {f}")

# every Business has its producing Deal, and vice versa (inv. 3, the produces FK);
# every Interface points at a real Business (the of FK)
bizs = {r[0].lower() for r in csv.reader(open('world-model/company/businesses.csv'))
        if r and not r[0].startswith('#') and r[0] != 'business'}
deals = {r[0].lower() for r in csv.reader(open('world-model/company/deals.csv'))
         if r and not r[0].startswith('#') and r[0] != 'produces_business'}
if bizs - deals: defects.append(f"businesses without a Deal: {bizs - deals}")
if deals - bizs: defects.append(f"Deals without a business: {deals - bizs}")
surf_biz = {r[1].lower() for r in csv.reader(open('interfaces/interfaces.csv'))
            if r and not r[0].startswith('#') and r[0] != 'interface'}
if surf_biz - bizs: defects.append(f"interfaces pointing at unknown business: {surf_biz - bizs}")

# the Deal —of→ Target FK: every non-n.d. of_target must resolve to a targets.csv key (materializes inv. 3
# for the of-link, which used to be declared but unbacked). n.d. = an acquisition predating the pipeline snapshot.
targets = {r['target'] for r in csv.DictReader(l for l in open('world-model/customer/targets.csv') if not l.startswith('#'))}
for row in csv.DictReader(l for l in open('world-model/company/deals.csv') if not l.startswith('#')):
    ot = (row.get('of_target') or '').strip()
    if ot and ot != 'n.d.' and ot not in targets:
        defects.append(f"Deal of_target does not resolve to a Target: {row['produces_business']} -> {ot!r}")

# a filing-sourced deal must not tag its disclosed price press-only (the Tractive/WeTransfer regression
# guard — audit-contract.md: "a disclosed deal price negated as 'not disclosed'" must never recur)
for row in csv.DictReader(l for l in open('world-model/company/deals.csv') if not l.startswith('#')):
    if row.get('source', '').strip() in ('bsp-f1', 'bsp-424b4') and 'to-validate — press only' in (row.get('note') or ''):
        defects.append(f"filing-sourced deal tagged press-only: {row['produces_business']} "
                       f"(a disclosed price cannot be [to-validate — press only])")

# business/interface nodes: structured properties in frontmatter; no Deal-data or undeclared top-level fields (inv. 2, Deal ⊥ Business)
for f in glob.glob('world-model/company/businesses/*.md') + [p for p in glob.glob('interfaces/*.md') if not p.endswith('README.md')]:
    t = open(f, encoding='utf-8').read()
    fm = t.split('---')[1]
    if '\nproperties:' not in fm:
        defects.append(f"no frontmatter properties: {f}")
    if re.search(r'^(deal|lifecycle):', fm, re.M) or 'operated-by' in fm:
        defects.append(f"illegal frontmatter: {f}")

# functions: three fields, no write verbs (inv. 4, 10)
for f in glob.glob('capabilities/functions/*.md'):
    t = open(f, encoding='utf-8').read()
    if not re.search(r'^function:', t, re.M):
        defects.append(f"no function: header: {f}")
    if re.search(r'^(action|agent|does):', t, re.M):
        defects.append(f"write-verb in function: {f}")

# actions: the seven-field contract (inv. 1 / §5)
for f in glob.glob('capabilities/actions/*.md'):
    t = open(f, encoding='utf-8').read()
    for field in ('action:', 'parameters:', 'logic', 'transaction',
                  'submission criteria:', 'governance:', 'side-effects:', 'backing:'):
        if field not in t:
            defects.append(f"missing '{field}': {f}")

# every backtick-quoted repo path in a model file resolves (the wrong-depth defect, generalized)
import os
PATHLIKE = re.compile(r'`(\.{0,2}/?[\w./-]+\.(?:md|csv|py|txt))(?: §[\w.-]+)?`')  # allow `path.md §N` refs
ALL_BASENAMES = {os.path.basename(p) for p in glob.glob('**/*.*', recursive=True)}
for f in glob.glob('**/*.md', recursive=True):
    if f.startswith(('sources/',)):
        continue
    t = open(f, encoding='utf-8').read()
    for p in PATHLIKE.findall(t):
        if '/' not in p:  # bare filename = a name-reference, not a path: must exist somewhere
            if p not in ALL_BASENAMES:
                defects.append(f"unknown file name: {f} -> {p}")
            continue
        rel_to_file = os.path.normpath(os.path.join(os.path.dirname(f), p))
        root_ok = os.path.exists(p) and '/' not in f  # root-relative style allowed only in root files
        if not (os.path.exists(rel_to_file) or root_ok):
            defects.append(f"unresolved path: {f} -> {p}")

# frontmatter completeness: required keys on every node (§4.7-8)
# (the two */ontology.md files are the SCHEMA indexes, not nodes — exempt)
REQUIRED = ('id:', 'type:', 'title:', 'status:', 'purpose:', 'provenance:', 'sources:', 'visibility:')
for f in glob.glob('world-model/**/*.md', recursive=True) + glob.glob('capabilities/**/*.md', recursive=True) + glob.glob('interfaces/*.md') + ['ontology.md'] + ['will.md', 'bending-spoons-as-an-intelligence.md']:
    if f.endswith('ontology.md'):
        continue
    t = open(f, encoding='utf-8').read()
    if not t.startswith('---'):
        defects.append(f"no frontmatter: {f}")
        continue
    fm = t.split('---')[1]
    for k in REQUIRED:
        if f'\n{k}' not in fm:
            defects.append(f"frontmatter missing {k[:-1]}: {f}")

# relation targets resolve to a declared node id or a §1 type name
ids = set()
for f in glob.glob('**/*.md', recursive=True):
    m = re.search(r'^id: (\S+)', open(f, encoding='utf-8').read(), re.M)
    if m:
        ids.add(m.group(1))
TYPES = {'business', 'interface', 'founders', 'facility', 'platform', 'tool', 'spooners', 'deal', 'target'}
for f in glob.glob('world-model/**/*.md', recursive=True) + glob.glob('capabilities/**/*.md', recursive=True) + glob.glob('interfaces/*.md') + ['ontology.md']:
    for tgt in re.findall(r'\{ type: [\w-]+, target: ([\w-]+)', open(f, encoding='utf-8').read()):
        if tgt not in ids and tgt not in TYPES:
            defects.append(f"unresolved relation target: {f} -> {tgt}")

# backing csv columns == §1 property sets for Target and Deal (1:1, + provenance/FK per §4.5)
EXPECT = {
 'world-model/customer/targets.csv':
   ['target','revenue_scale','hq','product_offering','revenue_model','room_for_improvement',
    'predictable_earnings','owner_willingness_to_sell','valuation_level','ai_pressure',
    'status','irr','walk_away_price','source','note'],
 'world-model/company/deals.csv':
   ['produces_business','of_target','date','cohort','deal_type','consideration_usd_m','enterprise_value_usd_m',
    'irr','ppa','source','note'],
 'interfaces/interfaces.csv':
   ['interface','business','category','capabilities_delivered','ai_features','status','source','note'],
 'world-model/company/facilities.csv':
   ['facility','type','currency','size_m','signed','status','source','note'],
}
for path, cols in EXPECT.items():
    header = next(csv.reader(open(path)))
    if header != cols:
        defects.append(f"csv header != §1 declaration: {path}")

if defects:
    print("DEFECTS:")
    for d in defects:
        print(" -", d)
    sys.exit(1)
print("AUDIT GREEN — all mechanical checks pass")
