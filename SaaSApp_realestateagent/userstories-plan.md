# Plan — User Stories for the Real Estate Intelligence Agent

## Context

[businessproblemdefinition.md](SaaSApp_realestateagent/businessproblemdefinition.md) defines a Real Estate
Intelligence Agent with three functional areas — property evaluation, rental analysis, tenant management —
but stops at that level. It names no user roles ("real estate stakeholders"), no data sources, and no
measurable outcomes. Nothing can be built or estimated from it as written.

This task closes that gap by translating the business problem into user stories with acceptance criteria,
written from the end user's perspective, then validating them against three success metrics: **Coverage**,
**Clarity and Specificity**, and **Relevance**.

The repo is greenfield — a single markdown file and a `.gitignore`, one commit. There is no code, no schema,
and no existing story format to conform to. This is a pure documentation deliverable.

**Confirmed with the user:**
- Cover the **full stakeholder set (5 roles)**.
- Enabling functionality goes in a **separate flagged appendix**, since the business problem explicitly says
  "No additional functionality is included within the defined scope."
- Acceptance criteria use **both** Given/When/Then scenarios **and** a definition-of-done checklist per story.
- **Data ingestion is in scope** — promoted out of the appendix into Epic 0. The Project Purpose's
  "based on the information available to them" is read as requiring the agent to own those records, not
  assume another system provides them. The three epics are unbuildable otherwise.
- **The audit trail is in scope** — promoted into Epic 4, which unblocks `US-XD-02` and keeps target
  outcome 4's *quality* half genuinely covered rather than gap-flagged.

Both promotions widen the scope the source document stated. That is a deliberate, recorded decision:
the scope statement understated the build, and the validation section says so plainly.

## Deliverable

Two new files, both under `SaaSApp_realestateagent/`. No existing files are modified.

| File | Contents |
|---|---|
| `userstories.md` | The story set — personas, cross-cutting criteria, defined terms, Epics 0-4, appendices, validation report. The primary deliverable. |
| `userstories-plan.md` | This plan, committed alongside it so the reasoning, the two validation passes, and the recorded scope decisions travel with the repo rather than living only in a session. |

### Document structure

1. **Header** — purpose, source doc reference, how to read a story card.
2. **Personas** — the 5 roles, each with a one-line goal and the epics they touch.
3. **Cross-cutting acceptance criteria** — stated once, inherited by every AI-backed story (see below).
4. **Defined terms and thresholds** — the values every acceptance criterion is measured against.
5. **Epic 0 — Data foundation** (`US-DF-nn`)
6. **Epic 1 — Property Evaluation** (`US-PE-nn`)
7. **Epic 2 — Rental Analysis** (`US-RA-nn`)
8. **Epic 3 — Tenant Management** (`US-TM-nn`)
9. **Epic 4 — Cross-domain decision support** (`US-XD-nn`)
10. **Appendix A — Enabling stories** (`US-EN-nn`), flagged *outside the stated scope, required to build*.
11. **Appendix B — Deferred stories** and the reason each was held back.
12. **Validation report** — scored against the three success metrics, carrying the findings tables below.

### Personas

| ID | Persona | Primary goal | Epics |
|---|---|---|---|
| P1 | Real Estate Agent | Advise clients quickly and defensibly | PE, RA, TM |
| P2 | Property Owner / Landlord | Maximise return, keep tenancies healthy | PE, RA, TM, XD |
| P3 | Property Manager | Run day-to-day tenancy operations | DF, RA, TM |
| P4 | Tenant | Self-serve on their own tenancy | TM *(+ both Appendix A stories)* |
| P5 | Investor / Buyer | Evaluate and compare acquisition targets | PE, RA |

Every story card names exactly one persona, including those in Appendix A — the task is to describe
functionality *from the end user's perspective*, so a story with no user is not a user story.

### Story card format

```
### US-PE-01 — Compare a property against recent comparable sales
**Persona:** P1 Real Estate Agent   **Epic:** Property Evaluation
**Priority:** Must   **Depends on:** —

As a Real Estate Agent, I want <capability> so that <outcome>.

**Acceptance criteria**
AC1  GIVEN <precondition> WHEN <action> THEN <observable result>
AC2  GIVEN <edge case>    WHEN <action> THEN <observable result>
AC3  GIVEN <failure mode> WHEN <action> THEN <observable result>

**Definition of done**
- [ ] <non-behavioural completion condition>
```

**Priority** uses MoSCoW against one rule: *Must* = a target outcome (TO1-TO4) fails without it;
*Should* = a target outcome is materially weakened; *Could* = neither. Without a stated rule, 26
priorities get invented ad hoc.

**Depends on** lists story IDs that must land first. Added because several stories have real
dependencies that were previously invisible — notably `US-XD-02` on `US-EN-04`, which crosses the
scope boundary into Appendix A.

**Acceptance criteria vs Definition of done** — these must not restate each other, or the doubled
format is noise. AC carry *behaviour*: what the agent does given a precondition. DoD carries
*non-behavioural* completion: X1-X4 compliance verified, thresholds from the Defined terms table
recorded, inputs named, dependency landed.

### Cross-cutting acceptance criteria (applied to every AI-backed story)

Stated once in section 3, referenced by ID from each story rather than repeated in full:

- **X1 Grounding** — every figure or claim cites the records it was derived from; no uncited numbers.
- **X2 Insufficient data** — below the evidence threshold defined for that story, the agent says so
  explicitly and returns no figure, rather than estimating.
- **X3 Advisory only** — the agent never executes an outward action (sending a notice, changing a rent,
  contacting a tenant) without explicit human confirmation.
- **X4 Responsiveness** — within the time budget defined for that interaction class.

### Defined terms and thresholds

Added during validation. X2 and X4 above, and several stories, referenced thresholds that were never
defined — making their acceptance criteria unfalsifiable. Every term below is pinned here and referenced
by name from the stories; none may be left as a bare adjective.

| Term | Definition to pin | Used by |
|---|---|---|
| Evidence threshold | Minimum count and maximum age of comparable records before a figure may be returned | X2, PE-01, RA-01 |
| Confidence level | A named band (High / Medium / Low) with stated comparable-count and recency ranges per band | PE-01, PE-05, RA-01 |
| Time budget | A value per interaction class: single-record lookup, multi-record analysis, portfolio-wide scan | X4 (all stories) |
| Tenant health | The component set it rolls up — arrears status, open maintenance issues, lease-expiry proximity | TM-07 |
| Portfolio | Whether it means one owner's properties or one manager's managed set | RA-04, TM-07, XD-02 |

If a value cannot be agreed at authoring time it is written as `TBC — <owner>`, never as a vague adjective.

### Story inventory (25 story cards — 23 main body, 2 enabling)

Revised across two validation passes; every change is marked inline and the reasoning recorded in the
findings tables and Appendix B. Count went 26 → 25 when `US-EN-03` was removed as circular; the
main-body/appendix split then moved 21/4 → 23/2 when `US-EN-02` and `US-EN-04` were promoted into scope.

Per epic: DF 1, PE 6, RA 5, TM 8, XD 3 = 23 main body; EN 2 in Appendix A; RA-06 deferred in Appendix B.

**Epic 0 — Data foundation** *(promoted from Appendix A by user decision — every other epic depends on it)*
- `US-DF-01` **P3** — load and maintain the property, rental and tenant records the agent reads, so its
  answers reflect current reality *(was `US-EN-02`)*
  **Priority:** Must — TO1, TO2 and TO3 all fail without it

**Epic 1 — Property Evaluation**
- `US-PE-01` P1 — comparable-sales valuation with range, comparables used, and confidence level
- `US-PE-02` P1 — condition and feature summary, stating which record types it reads *(revised: original
  asserted inspection notes the source doc never mentions; the story must name its inputs, not assume them)*
- `US-PE-03` P5 — screen a property against stated investment criteria (budget, location, type, yield floor)
- `US-PE-04` P5 — side-by-side comparison of shortlisted properties on a consistent metric set
- `US-PE-05` P2 — explain what is driving (and depressing) their property's valuation
- `US-PE-06` P1 — free-form Q&A about a property, answered only from the property's own records

**Epic 2 — Rental Analysis**
- `US-RA-01` P1 — recommend an achievable rent range from comparable rentals
- `US-RA-02` P2 — gross and net rental yield, with the inputs used shown
- `US-RA-03` P2 — compare a proposed rent against current rent and comparables, showing the resulting
  position and the vacancy risk indicators available *(revised: "model a rent change" left the output undefined)*
- `US-RA-04` P3 — flag under- and over-performing units across a managed portfolio
- `US-RA-05` P5 — compare rental performance **across their own properties** *(revised: "or markets"
  removed — external market data is not established as available)*

**Epic 3 — Tenant Management**
- `US-TM-01` P3 — consolidated tenant profile: lease terms, contact, payment history, open issues
- `US-TM-02` P3 — lease expiry and renewal pipeline with a recommended action per tenancy
- `US-TM-03` P3 — arrears detection with prioritised follow-up list
- `US-TM-04` P3 — triage and route maintenance requests by urgency
- `US-TM-05` P4 — submit a maintenance request and track its status
  ⚠️ *Consistency flag: this is data entry, not AI assistance — it creates the records `US-TM-04` triages.
  That makes it ingestion, the same category as `US-EN-02`, which sits in Appendix A. Either both are
  main-body or both are enabling. Recommend keeping it here (a tenant raising a request is genuinely a
  "tenant activity" per TO3) and noting the inconsistency rather than hiding it.*
- `US-TM-06` P4 — self-serve answers about own lease (dates, rent, obligations, notice periods)
- `US-TM-07` P2 — portfolio tenant summary rolling up arrears, open issues and lease-expiry proximity
  *(revised: "health" was undefined and therefore untestable; the components are now named)*
- `US-TM-08` P1 — draft tenant communications (renewal, arrears reminder) for human review before sending

**Epic 4 — Cross-domain decision support** *(added during validation — closes the TO4 coverage gap)*

Target outcome 4 asks to improve the efficiency **and quality** of decision-making **across** all three
areas. The original inventory addressed neither half: every story sat inside a single epic, and nothing
let a user judge whether the agent's advice was sound. Two stories close it.

- `US-XD-01` **P2** — one briefing for a property combining its valuation, rental position and tenancy
  status, so a decision spanning the three areas does not require three separate sessions
  *(revised: was P1/P2. The card format holds one persona, and under `US-EN-01` role-based access an agent
  and an owner would not see the same records. Assigned to the owner, who makes the hold/re-let/sell call;
  if the agent needs the same briefing it is a separate card, not a shared one.)*
  **Depends on:** PE-01, RA-02, TM-07
- `US-XD-02` P2 — review recommendations the agent previously made against what actually happened, so
  decision quality is observable rather than assumed
  **Depends on:** `US-XD-03`
  *Availability resolved: the outcome data (achieved sale price, actual let rent, renewal taken) sits in the
  property and tenancy records the other epics already read; the stored recommendations come from `US-XD-03`,
  now in scope. Pass 2 caught this dependency crossing the scope boundary and it has been closed.*
- `US-XD-03` **P2** — see what the agent recommended and what was decided, so advice is reviewable after
  the fact *(was `US-EN-04`; promoted from Appendix A by user decision to unblock `US-XD-02`)*
  **Priority:** Must — TO4's *quality* half fails without it

**Appendix A — Enabling stories** *(outside the stated scope; the three epics cannot function without them)*

Both now carry a persona — pass 1 left these written as system capabilities, which fails the task's
own requirement that functionality be described from the end user's perspective. Two of the original
five were promoted into scope and one was removed, leaving these two genuinely enabling stories.

- `US-EN-01` **P4 Tenant** — sign in and see only my own tenancy, not other tenants' records
  *(role-based access stated from the persona with the most to lose from getting it wrong)*
- `US-EN-05` **P4 Tenant** — have my personal data retained only as long as a named jurisdiction requires
  *(revised: with no jurisdiction stated a retention period cannot be verified; if none is supplied it is
  written `TBC — owner`)*

**Moved out of this appendix:**
- `US-EN-02` → **`US-DF-01`**, Epic 0. Promoted into scope by user decision; every epic depends on it.
- `US-EN-04` → **`US-XD-03`**, Epic 4. Promoted into scope by user decision; unblocks `US-XD-02`.
- `US-EN-03` **removed** — it read "grounding and citation guardrail enforcing X1/X2 system-wide", which is
  circular: X1 and X2 are already declared as acceptance criteria on every story. A story whose whole content
  is "enforce the criteria we said apply everywhere" adds nothing, and it had no user. The guardrail is
  architecture, not a user story; X1/X2 remain the acceptance surface, verified per story via the DoD.

**Appendix B — Deferred, recorded rather than silently dropped**

| Story | Reason |
|---|---|
| `US-RA-06` rental demand and seasonality signals | Needs external market data. The source doc scopes the agent to *"the information available to them"*, and no such feed is established. Reinstate if a market-data source is confirmed. |

### Validation report (the "Validate" role)

A second pass written into the same file, not a separate document:

- **Coverage** — traceability matrix mapping each of the 3 required functionalities and each of the 4 target
  outcomes in the source doc to the story IDs that satisfy it. Any row without a story is called out as a gap,
  not quietly dropped.
- **Clarity and Specificity** — each story checked for: vague verbs ("manage", "handle", "support") replaced
  with observable behaviour; every AC independently testable; thresholds quantified rather than "fast" or
  "accurate". Stories revised during this pass are listed with before/after.
- **Relevance** — each story traced back to a target outcome. Anything that does not trace is moved to
  Appendix A (enabling), Appendix B (deferred), or deleted, with the decision recorded in every case.
- **Gaps in the source document** — an honest list of what the business problem definition does not specify
  and therefore what these stories had to assume: no named data sources, no named user roles, no success
  KPIs, no non-functional requirements (volume, latency, availability), no compliance/jurisdiction context.
  Each assumption made is stated explicitly so it can be confirmed or corrected.

**Findings already applied (first validation pass, before authoring):**

| Metric | Finding | Action taken |
|---|---|---|
| Coverage | TO4 unmet — nothing addressed *quality* of decisions, and every story sat inside one epic despite TO4 saying *across* all three | Added Epic 4: `US-XD-01`, `US-XD-02` |
| Clarity | X2 evidence threshold, X4 time budget, PE-01 confidence level and TM-07 "health" were referenced but never defined — untestable | Added the Defined terms and thresholds table |
| Clarity | `US-RA-03` "model a rent change" — no defined output | Rewritten to state the comparison and its output |
| Clarity | `US-TM-07` "tenant health" — undefined roll-up | Components named explicitly |
| Clarity | `US-PE-02` assumed inspection notes the source doc never mentions | Story must name its input record types |
| Clarity | `US-EN-05` retention period unverifiable with no jurisdiction | Jurisdiction named, or `TBC — owner` |
| Relevance | `US-RA-05` "or markets" needs external data not established as available | Narrowed to the user's own properties |
| Relevance | `US-RA-06` depends entirely on unavailable market data | Deferred, with reason recorded |

**Findings applied (second validation pass):**

Pass 1 revised the inventory but left the scaffolding around it describing the old one. Most of what
follows is self-inflicted drift, which is exactly what a re-validation is for.

| Metric | Finding | Action taken |
|---|---|---|
| Coverage | Document structure list still showed 8 sections — no Epic 4, no Defined terms, no Deferred appendix. The contents page contradicted the inventory. | Rewritten to 11 sections |
| Coverage | Personas table Epics column never updated after Epic 4 was added; P2 was missing XD | P2 → `PE, RA, TM, XD` |
| Clarity | `Priority: Must` sat in the card format with no scheme defined and no priority assigned to any story — 26 ad-hoc judgements waiting to happen | MoSCoW pinned with an explicit rule tied to TO1-TO4 |
| Clarity | Nothing said how Definition of done differs from the AC, so the doubled format would produce restatement | AC = behavioural; DoD = non-behavioural completion. Rule stated |
| Clarity | `US-XD-01` carried two personas (P1/P2); the card format holds one, and RBAC means they see different records | Assigned to P2, with the reasoning recorded |
| Relevance | Appendix A stories had **no persona at all** — written as system capabilities, failing the task's "from the end user's perspective" requirement | All four given a persona |
| Relevance | `US-EN-03` was circular — "enforce X1/X2", which are already universal AC, and it had no user | Removed; X1/X2 verified per story via DoD |
| Availability | `US-XD-02` depends on `US-EN-04`, an out-of-scope appendix story — the gate that deferred `US-RA-06` was not applied to the story added in the same pass | Dependency declared; conditional entry added to Appendix B; decision escalated |
| Consistency | No dependency field existed despite real cross-story dependencies (XD-01→PE/RA/TM, XD-02→EN-04, TM-03→TM-01) | `Depends on` added to the card format |
| Consistency | `US-TM-05` is data entry feeding TM-04 — the same ingestion category as `US-EN-02`, which is in the appendix. Two categories, two treatments | Flagged inline; recommend keeping in main body under TO3 |

**Scope decisions taken (both were open questions raised by validation, settled by the user):**

| Question | Decision | Consequence |
|---|---|---|
| The Project Purpose says the agent works *"based on the information available to them"* (records exist), while Defined Scope admits nothing beyond the three areas. Is ingestion in scope? | **In scope.** `US-EN-02` → `US-DF-01`, Epic 0 | The story set is now buildable; it also resolves the `US-TM-05` inconsistency, since ingestion is no longer split across a main body and an appendix |
| `US-XD-02` covers TO4's *quality* half but depended on out-of-scope `US-EN-04` | **Audit trail in scope.** `US-EN-04` → `US-XD-03`, Epic 4 | TO4 is genuinely covered rather than gap-flagged, and no main-body story now depends on an appendix story |

Both widen the scope the source document stated. The deliverable records this explicitly: the Defined Scope
section of `businessproblemdefinition.md` understates what the three functional areas actually require, and
that finding belongs in front of whoever owns that document.

**Intentional persona exclusions** (recorded so they do not read as coverage misses): P3 Property Manager
has no Property Evaluation story and P4 Tenant has no Property Evaluation or Rental Analysis story —
neither role evaluates acquisitions or sets rents.

## Verification

This is a document, so verification is a review pass, not a test run:

1. **Coverage gate** — the traceability matrix must show every one of the 3 required functionalities and all
   4 target outcomes mapped to at least one story. Any unmapped row is a fail. TO4 specifically requires a
   story for the *quality* half and one spanning all three areas, not just efficiency stories.
2. **Clarity gate** — read every AC and confirm it states an observable, checkable result. Grep the finished
   file for the banned vague verbs (`manage`, `handle`, `support`, `improve`, `optimise`) outside of quoted
   source text; each hit must be justified or rewritten.
3. **Undefined-term gate** — every term in the Defined terms table resolves to a value or an explicit
   `TBC — <owner>`. No acceptance criterion may depend on a threshold that is never stated; this was the
   most common defect in the first validation pass.
4. **Relevance gate** — every story in the main body traces to a target outcome; anything that does not is in
   Appendix A or the Deferred table with its reason.
5. **Availability gate** — no story depends on a data source the source doc does not establish as available.
   This is what deferred `US-RA-06` and narrowed `US-RA-05`.
6. **Scope gate** — confirm no main-body story introduces functionality beyond property evaluation, rental
   analysis, tenant management, the TO4-mandated cross-domain view, or the data foundation and audit trail
   the user explicitly promoted into scope. Anything else is a fail, and the two promotions must appear in
   the deliverable's validation report as recorded widenings rather than silent additions.
7. **Persona gate** — all 5 personas appear as the subject of at least one main-body story, the intentional
   exclusions (P3/P4) are recorded rather than left looking accidental, and **every card names exactly one
   persona — including Appendix A**. Zero personas or two both fail.
8. **Internal-consistency gate** — the contents list, the Personas table's Epics column, and the story count
   must all match the inventory. Pass 2 found all three had drifted after pass 1 edited stories without
   updating the scaffolding; re-run this gate after *any* story is added, removed, or reassigned.
9. **Dependency gate** — every `Depends on` target exists, and any main-body story depending on an Appendix A
   story is escalated as a scope decision rather than left implicit.
10. **Non-duplication gate** — no story's content reduces to restating a cross-cutting criterion (the defect
   that removed `US-EN-03`), and no DoD item restates its own AC.
11. Render the file and confirm the tables and story cards are readable in the IDE preview.

## Out of scope for this task

- No implementation, schema, or code.
- No estimation, sprint assignment, or backlog tooling — story cards only.
- The source `businessproblemdefinition.md` is not edited; gaps in it are reported in the validation section
  rather than fixed in place.
