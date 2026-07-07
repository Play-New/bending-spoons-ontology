export const meta = {
  name: 'bsp-control-pass',
  description: 'Full control pass over the bending-spoons-ontology repo: 5 area reviewers, adversarial verification of findings',
  phases: [
    { title: 'Review', detail: 'five area reviewers in parallel' },
    { title: 'Verify', detail: 'adversarially confirm each HIGH/MED finding' },
  ],
}

const ROOT = '/Users/matteo/Github/bending-spoons-ontology'

const CONTEXT = `Repo: ${ROOT} (read-only for you; do NOT edit files).
CURRENT STRUCTURE (just refactored — check against THIS, not any older shape):
- The model lives at the repo ROOT: ontology.md (index: §1 objects · §2 actions & functions · §3 flywheel), world-model/ (company/ + customer/), capabilities/ (actions/ ×8: market-radar, screen-target, deal-value, deal-diligence, deal-optimize, talent, retire, finance · functions/ ×5), interfaces/ (18 Interface nodes + interfaces.csv + README index).
- Object types (§1, 10 total): Business ×17 (world-model/company/businesses/ + businesses.csv) · Interface ×18 (a Business may ship several; Mosaic ships iTranslate+RoboKiller; link Interface—of→Business) · Platform · Tool ×5 (world-model/company/tools/) · Spooner (aggregate type node) · Founders (collective type node) · Deal (deal.md + deals.csv, FK produces_business) · Facility (facility.md + facilities.csv) · Target (+targets.csv) · cross-product-graph (the gap, an anti-object).
- NO observed/ or projected/ folders exist (historical only, in git history and one historical mention in the essay). The thesis is ONE root essay: bending-spoons-as-an-intelligence.md (§1-§7).
- foundations/ontology.md has §1-§6 (incl. §4.0 decision test, §4.7 naming rule singular=type-node/plural=instance-folder, §4.8 two clocks, §5 contract shape + 11 invariants, §6 security). foundations/org-as-an-intelligence.md: named headings, five-things list cited as §1-§5. will.md: constraints in 5 groups (deal/org/capital discipline, founder control, external covenants).
- Naming: type "Interface" (NOT "Surface" — that word may appear only as the definitional gloss "delivery surface"); "Business" (NOT "Product" as a current type; product-users.md is a function name and cross-product-graph.md a node name — both fine).
- Publication tone: files are the artifact — no session-process chatter (no "user decision", "this session", dated review mentions).
RULES to check against: every backtick path resolves from its file's location (root-relative allowed only in root files); every §-reference lands on a real heading; counts must be true (17 businesses, 18 interfaces, 5 tools, 8 actions, 5 functions, 11 invariants, 10 object types); csv↔node 1:1; no stale Product/Surface/observed//projected//tool/ references outside legitimate uses.
Return ONLY real, verifiable defects — no style opinions.`

const AREAS = [
  { key: 'entry-docs', scope: 'README.md, CLAUDE.md, AGENTS.md, bending-spoons-as-an-intelligence.md — every claim, tree, count, path, and cross-reference vs the actual repo state' },
  { key: 'company', scope: 'ontology.md + world-model/company/** (businesses/ ×17 + businesses.csv, tools/ ×5, spooners.md, founders.md, deal.md + deals.csv, facility.md + facilities.csv, platform.md, financials.csv) + world-model/index.md — §1 declarations vs nodes vs csvs (1:1), §2 table vs contracts, internal consistency of figures and ~L citations across files' },
  { key: 'interfaces-customer', scope: 'interfaces/** (README + 18 nodes + interfaces.csv) + world-model/customer/** (market-of-targets.md + targets.csv, cross-product-graph.md) — node↔csv 1:1, of→Business links resolve, README table matches nodes, no stale Surface/product wording' },
  { key: 'capabilities', scope: 'capabilities/actions/*.md (8) + capabilities/functions/*.md (5) — each action has the seven contract fields with verb matching ontology.md §2 exactly (both directions); functions have function/input/computation/output; deal-audit mirrors foundations §5 invariants 1:1; every path and §ref resolves; transaction property names exist in §1/csv headers' },
  { key: 'foundations-mcp', scope: 'foundations/*.md + will.md + mcp/server.py + mcp/audit.py + mcp/README.md — internal §-pointers, will constraint ~L refs coherent with how contracts cite the same facts, server docstrings true of the flattened layout, audit globs/EXPECT headers match real files, mcp/README tool list = actual @mcp.tool() functions' },
]

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['HIGH', 'MED', 'LOW'] },
          file: { type: 'string' },
          line: { type: 'number' },
          defect: { type: 'string' },
          evidence: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'file', 'defect', 'evidence', 'fix'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    confirmed: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['confirmed', 'reason'],
}

phase('Review')
const results = await pipeline(
  AREAS,
  a => agent(
    `${CONTEXT}\n\nYOUR AREA: ${a.scope}\n\nRead every file in your area fully. Hunt for real defects: broken/wrong-depth paths, stale §refs, wrong counts, csv↔node drift, contract fields missing or diverging from ontology.md §2 / foundations §5, stale terminology (Surface as a type name, Product as a current type, observed//projected/ or tool/ as paths), contradictions between files, unsourced figures, session-process chatter. Max 15 findings, most severe first. Cap LOW findings at 5.`,
    { label: `review:${a.key}`, phase: 'Review', schema: FINDINGS }
  ),
  (review, a) => parallel(
    (review?.findings || [])
      .filter(f => f.severity !== 'LOW')
      .map(f => () =>
        agent(
          `${CONTEXT}\n\nYou are a skeptic. A reviewer claims this defect in ${ROOT}:\nfile: ${f.file}${f.line ? ' line ~' + f.line : ''}\ndefect: ${f.defect}\nevidence: ${f.evidence}\nproposed fix: ${f.fix}\n\nRead the actual file(s) involved and try to REFUTE the claim (maybe the reviewer misread, the reference actually resolves, the count is right, or the "defect" is legitimate content). confirmed=true ONLY if you verified the defect is real as stated. Default to confirmed=false when uncertain.`,
          { label: `verify:${a.key}`, phase: 'Verify', schema: VERDICT }
        ).then(v => ({ ...f, area: a.key, confirmed: v?.confirmed ?? false, verify_reason: v?.reason ?? 'no verdict' }))
      )
  ).then(verified => ({
    area: a.key,
    confirmed: verified.filter(Boolean).filter(f => f.confirmed),
    refuted: verified.filter(Boolean).filter(f => !f.confirmed).map(f => ({ file: f.file, defect: f.defect, why: f.verify_reason })),
    low: (review?.findings || []).filter(f => f.severity === 'LOW'),
  }))
)

const all = results.filter(Boolean)
log(`confirmed: ${all.reduce((n, r) => n + r.confirmed.length, 0)} · refuted: ${all.reduce((n, r) => n + r.refuted.length, 0)} · low (unverified): ${all.reduce((n, r) => n + r.low.length, 0)}`)
return all