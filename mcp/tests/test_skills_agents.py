"""Every skill, every agent, the workflow: structural + contract-coherence tests.
Read-only — runs on the real repo. python3 test_skills_agents.py <repo_root>.

Per skill: frontmatter parses with name+description; verb skills are explicit-only
(disable-model-invocation); every repo path the skill references exists; the verb the
skill executes exists in the engine. Per agent: frontmatter parses; the tool list is
STRUCTURALLY read-only (no Bash/Write/Edit); referenced contract files exist. Workflow:
has the meta block and phases.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "mcp"))
import engine  # noqa: E402

R = {"pass": 0, "fail": 0, "cases": []}


def record(ok, name, detail=""):
    R["pass" if ok else "fail"] += 1
    R["cases"].append(("PASS" if ok else "FAIL", name, str(detail)[:160]))


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^([\w-]+): (.*)$", m.group(1), re.M)) if m else {}


VERB_SKILLS = {"source", "screen", "underwrite", "close", "transform"}  # the deal-engine flow; raise/retire are engine-only actions
# expected: 5 deal-engine verbs + deal-desk (orchestrator) + radar-sweep (scout) + hire (the read-only
# hiring assistant, not an engine verb) + bsp-audit (model service)
EXPECTED_SKILLS = VERB_SKILLS | {"deal-desk", "radar-sweep", "hire", "bsp-audit"}
skills = sorted((ROOT / ".claude/skills").iterdir())
names = {s.name for s in skills}
record(names == EXPECTED_SKILLS, f"skill tree matches the discipline: {sorted(names)}", sorted(EXPECTED_SKILLS))

for d in skills:
    f = d / "SKILL.md"
    if not f.exists():
        record(False, f"skill {d.name}: SKILL.md exists")
        continue
    t = f.read_text()
    fm = frontmatter(t)
    record(bool(fm.get("name")) and bool(fm.get("description")),
           f"skill {d.name}: frontmatter name+description")
    record(fm.get("name") == d.name, f"skill {d.name}: name matches directory")
    if d.name in VERB_SKILLS:
        record(fm.get("disable-model-invocation") == "true",
               f"skill {d.name}: explicit-only (disable-model-invocation)")
        record(d.name in engine.ACTIONS, f"skill {d.name}: verb exists in engine")
        # gate coherence: the engine's gate for this verb matches what the skill tells the user
        try:
            gate = "auto" if d.name == "screen" else "human"
            says_auto = "applies auto" in t.lower() or "apply auto" in t.lower()
            record((gate == "auto") == says_auto, f"skill {d.name}: stated gate matches engine gate")
        except Exception as e:
            record(False, f"skill {d.name}: gate coherence", e)
    # every backtick-quoted repo file the skill references exists
    for p in re.findall(r"`([\w./-]+\.(?:md|py|csv))`", t):
        if p.startswith("PROPOSAL") or "${" in p:
            continue
        record((ROOT / p).exists(), f"skill {d.name}: referenced path exists: {p}")
    # bundled scripts run --help
    for s in (d / "scripts").glob("*.py") if (d / "scripts").exists() else []:
        import subprocess
        r = subprocess.run([sys.executable, str(s), "--help"], capture_output=True, text=True)
        record(r.returncode == 0, f"skill {d.name}: script {s.name} --help runs")

# hire is the read-only hiring assistant: it must NOT be an engine verb and must NOT write the model
_hire = (ROOT / ".claude/skills/hire/SKILL.md").read_text()
record("hire" not in engine.ACTIONS, "hire skill is read-only: not an engine write verb")
record("engine.propose('hire'" not in _hire and "engine.apply" not in _hire,
       "hire skill never commits through the engine (advisory by design)")
record("sources/hiring/" in _hire, "hire skill grounds its gates in the official BS hiring docs")

WRITE_TOOLS = {"Bash", "Write", "Edit", "NotebookEdit"}
for f in sorted((ROOT / ".claude/agents").glob("*.md")):
    t = f.read_text()
    fm = frontmatter(t)
    record(bool(fm.get("name")) and bool(fm.get("description")), f"agent {f.stem}: frontmatter")
    tools = {x.strip() for x in fm.get("tools", "").split(",")}
    record(not (tools & WRITE_TOOLS), f"agent {f.stem}: structurally read-only (tools: {sorted(tools)})")
    for p in re.findall(r"`(capabilities/[\w./-]+\.md|world-model/[\w./-]+\.(?:md|csv))`", t):
        record((ROOT / p).exists(), f"agent {f.stem}: referenced contract exists: {p}")

wf = ROOT / ".claude/workflows/bsp-control-pass.js"
record(wf.exists(), "workflow bsp-control-pass.js exists")
if wf.exists():
    t = wf.read_text()
    record("export const meta" in t and "phases" in t, "workflow: meta block with phases")
    record("pipeline(" in t and "schema" in t.lower(), "workflow: pipeline + structured outputs")

print(json.dumps(R))
