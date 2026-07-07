---
name: hire
description: The hiring assistant — run a candidate through Bending Spoons' selection funnel and score them against the disclosed gates. Read-only, advisory: it drafts a recommendation; the committee decides. The people-side twin of screen-target.
disable-model-invocation: true
---

Run a candidate through Bending Spoons' **selection funnel**, scored against the disclosed gates. This is
the people-side twin of `screen`: `screen` runs a *company* through the nine Target gates; `hire` runs a
*person* through the selection funnel. It is **read-only and advisory** — it produces a scored
recommendation for the human committee; it does **not** write the model (the filings disclose only
aggregate `Spooners` data, so there is no per-person node to write — `capabilities/actions/talent.md`).

**Grounding — the funnel and the gates come only from Bending Spoons' own documents:**
- the funnel stages and criteria: `sources/hiring/bsp-selection-process.md` (screening → tasks →
  interviews → references → committee) and `sources/hiring/bsp-talent-formula.md` (the committee,
  independent of the direct lead; the three assessment dimensions);
- the scale and selection values: `bsp-f1` ~L284 (≈800k applications → 286 hired, <0.04%), ~L138/~L158/~L283
  (talent density · technical excellence · truth-seeking · extreme ownership · talent-over-experience).

**Parameterizable** (the point — anyone can run their own version): the gates below are Bending Spoons'.
To hire for another company, change the gates and the funnel to theirs; the procedure is generic.

## The gates (score each; cite the source)
1. **problem-solving** — can they make sense of unfamiliar problems? (`bsp-selection-process`, tasks)
2. **role-specific** — expertise *and* potential; "how fast you grow, not where you start"
3. **behavioral** — ownership · commitment · ambition · drive for exceptional results as a team
4. **talent-over-experience** — long-term potential outweighs current expertise
5. **honesty** — no offer if accomplishments are misrepresented (a hard disqualifier)

## Procedure
1. Take the candidate's materials **that the user provides** (CV, submitted work, and only the public
   links they share — no autonomous scraping of a private individual).
2. Run the funnel, mapping each stage to the gates:
   - **screening** (CV) → talent-over-experience, role-specific signal, quantitative achievements;
   - **tasks** → problem-solving + behavioral (generate BS-style tasks; the candidate does them; you
     *score submitted work*, you do not fabricate performance);
   - **interviews** → behavioral + role-specific (draft the guide; score responses if supplied);
   - **references** → corroboration (out of scope to contact; note what to ask).
3. Produce a **per-gate verdict** (pass / judge / fail + one-line rationale) and a funnel position, each
   marked by provenance (`[derived]` from the gate docs; `[to-validate]` for anything you infer).
4. **STOP at the committee.** The decision is the committee's (independent of any single lead) — the human
   gate. Present the recommendation; never assert a hire. Nothing is written to the model.

Everything you produce is a draft for the committee. If asked to "hire" someone, you score and recommend;
you do not, and cannot, commit a Spooners — that boundary is the same human gate every action in this model
carries.
