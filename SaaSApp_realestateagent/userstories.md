# Real Estate Intelligence Agent — User Stories

Derived from [businessproblemdefinition.md](businessproblemdefinition.md).

This document translates the business problem into user stories with acceptance criteria, written from the
end user's perspective. It closes with a validation report scoring the set against three success metrics:
**Coverage**, **Clarity and Specificity**, and **Relevance**.

**25 story cards** — 23 in the main body (Epics 0-4), 2 enabling (Appendix A), 1 deferred (Appendix B).

## How to read a story card

Every card names exactly one persona, one epic, a MoSCoW priority, and its dependencies.

- **Acceptance criteria (AC)** carry *behaviour* — what the agent does given a precondition. Written
  GIVEN / WHEN / THEN so each is independently testable.
- **Definition of done (DoD)** carries *non-behavioural* completion — compliance with the cross-cutting
  criteria, thresholds recorded, inputs named. It does not restate the AC.
- **Priority** uses one rule: *Must* = a target outcome fails without it; *Should* = a target outcome is
  materially weakened; *Could* = neither.

Target outcomes from the source document are referenced as **TO1** (evaluate properties efficiently),
**TO2** (analyse rental information effectively), **TO3** (manage tenant information and activities),
**TO4** (efficiency **and quality** of decision-making **across** all three).

---

## 1. Personas

| ID | Persona | Primary goal | Epics |
|---|---|---|---|
| P1 | Real Estate Agent | Advise clients quickly and defensibly | PE, RA, TM |
| P2 | Property Owner / Landlord | Maximise return, keep tenancies sound | PE, RA, TM, XD |
| P3 | Property Manager | Run day-to-day tenancy operations | DF, RA, TM |
| P4 | Tenant | Self-serve on their own tenancy | TM (+ both Appendix A stories) |
| P5 | Investor / Buyer | Evaluate and compare acquisition targets | PE, RA |

**Intentional exclusions**, recorded so they do not read as coverage misses: P3 has no Property Evaluation
story and P4 has no Property Evaluation or Rental Analysis story. Neither role evaluates acquisitions or
sets rents.

---

## 2. Cross-cutting acceptance criteria

Stated once, inherited by every AI-backed story and referenced by ID rather than repeated in full.
`US-TM-05` and `US-EN-01` are excluded from X1/X2 — they are data entry and access control, not analysis.

| ID | Criterion |
|---|---|
| **X1** | **Grounding** — every figure or claim cites the records it was derived from. No uncited numbers. |
| **X2** | **Insufficient data** — below the evidence threshold for that story, the agent states the shortfall, names what is missing, and returns no figure. It does not estimate, and it does not answer from general knowledge. |
| **X3** | **Advisory only** — the agent never performs an outward action (sending a notice, changing a rent, contacting a tenant, assigning work) without explicit human confirmation. |
| **X4** | **Responsiveness** — within the time budget for that interaction class. |

---

## 3. Defined terms and thresholds

Every threshold an acceptance criterion depends on is pinned here. A criterion resting on an undefined
term is not testable, so nothing below may be left as a bare adjective.

| Term | Value | Used by |
|---|---|---|
| Evidence threshold | ≥3 comparable records, transacted within 12 months, in the same locality | X2, PE-01, PE-05, RA-01, RA-03, RA-04 |
| Confidence level | **High** ≥6 comparables ≤6 months · **Medium** 3-5 comparables ≤12 months · **Low** 3 comparables 12-24 months · below this → X2 refusal | PE-01, PE-05, RA-01 |
| Time budget | Single-record lookup ≤3s · multi-record analysis ≤10s · portfolio-wide scan ≤30s | X4 (all stories) |
| Record staleness window | 90 days since last update; beyond it an answer using the record flags it as stale | DF-01, all cited records |
| Max comparison set | 8 properties per side-by-side comparison | PE-04, RA-05 |
| Renewal horizon | Tenancies expiring within 90 days appear in the pipeline | TM-02 |
| Arrears prioritisation | Ordered by amount outstanding × days overdue, descending | TM-03 |
| Urgency bands | **Emergency** (habitability or safety) · **Urgent** (loss of an amenity) · **Routine** (all else) | TM-04 |
| Tenant summary components | Arrears status, open maintenance issues, lease-expiry proximity — these three, no others | TM-07 |
| Portfolio | The set of properties the signed-in user holds access rights to: owned (P2) or managed (P3) | RA-04, TM-07, XD-02 |

> ⚠️ **These values are proposed defaults, not agreed ones.** The source document states no thresholds, so
> every figure above needs sign-off from the product owner before build. The retention period in `US-EN-05`
> is left explicitly as `TBC` because it cannot be defaulted responsibly — see that story.

---

## 4. Epic 0 — Data foundation

*Promoted into scope by decision (see §10). Every other epic reads what this story writes.*

### US-DF-01 — Load and maintain the records the agent reads
**Persona:** P3 Property Manager  **Epic:** Data foundation
**Priority:** Must  **Depends on:** —

As a Property Manager, I want to load and keep current the property, rental and tenant records the agent
reads, so that its answers reflect reality rather than a stale snapshot.

**Acceptance criteria**
- **AC1** GIVEN a record with every required field for its type WHEN I submit it THEN it is stored, and the agent's next answer about that subject reflects it.
- **AC2** GIVEN a record missing a required field WHEN I submit it THEN it is rejected, the missing field is named, and no partial record is stored.
- **AC3** GIVEN a record I have updated WHEN the agent next cites it THEN the citation shows the current value and its last-updated date.
- **AC4** GIVEN a record older than the staleness window WHEN it is used in any answer THEN that answer marks the record stale and shows its age.

**Definition of done**
- [ ] Required fields enumerated per record type (property, rental, tenancy, payment, maintenance)
- [ ] Staleness window set per §3
- [ ] Every citation surface carries a last-updated date, satisfying X1 downstream

---

## 5. Epic 1 — Property Evaluation  → TO1

### US-PE-01 — Value a property against comparable sales
**Persona:** P1 Real Estate Agent  **Epic:** Property Evaluation
**Priority:** Must  **Depends on:** US-DF-01

As a Real Estate Agent, I want a valuation estimate built from comparable recent sales, so that I can advise
a client from evidence rather than instinct.

**Acceptance criteria**
- **AC1** GIVEN comparables meeting the evidence threshold WHEN I request a valuation THEN the agent returns a price **range**, every comparable used, and a confidence level.
- **AC2** GIVEN comparables below the evidence threshold WHEN I request a valuation THEN the agent states the shortfall, names what is missing, and returns no price figure (X2).
- **AC3** GIVEN a returned valuation WHEN I inspect any figure THEN it traces to the records it came from (X1).
- **AC4** GIVEN comparables that reach only the Low band WHEN the valuation returns THEN the band is shown together with the reason it is Low.

**Definition of done**
- [ ] Evidence threshold and confidence bands per §3
- [ ] Multi-record analysis time budget met (X4)
- [ ] A single-point figure is never returned in place of a range

### US-PE-02 — Summarise a property's condition and features
**Persona:** P1 Real Estate Agent  **Epic:** Property Evaluation
**Priority:** Should  **Depends on:** US-DF-01

As a Real Estate Agent, I want a summary of a property's condition and features drawn from its stored
records, so that I can brief a client without reading every document.

**Acceptance criteria**
- **AC1** GIVEN a property with at least one condition-bearing record WHEN I request a summary THEN the agent returns it and names every record type it read.
- **AC2** GIVEN a property with no condition-bearing records WHEN I request a summary THEN the agent states none are on file and returns no summary (X2).
- **AC3** GIVEN two records that disagree on a feature WHEN the summary is produced THEN both values appear with their record dates, and neither is silently chosen.

**Definition of done**
- [ ] Input record types enumerated in the story, never assumed
- [ ] X1 citation on every stated feature

### US-PE-03 — Screen a property against investment criteria
**Persona:** P5 Investor / Buyer  **Epic:** Property Evaluation
**Priority:** Should  **Depends on:** US-DF-01

As an Investor, I want a property screened against criteria I have set, so that I can rule it in or out
without working through it by hand.

**Acceptance criteria**
- **AC1** GIVEN saved criteria and a property with data for each WHEN I screen it THEN every criterion shows met / not met with the value that decided it.
- **AC2** GIVEN a criterion with no data on file WHEN I screen THEN it reads **cannot assess** — never *not met* — and the overall result is marked incomplete.
- **AC3** GIVEN every criterion met WHEN the screen completes THEN the result is presented as a screen outcome, not as advice to buy (X3).

**Definition of done**
- [ ] "Cannot assess" and "not met" are visually distinct and never conflated
- [ ] X1 on each deciding value

### US-PE-04 — Compare shortlisted properties side by side
**Persona:** P5 Investor / Buyer  **Epic:** Property Evaluation
**Priority:** Should  **Depends on:** US-DF-01

As an Investor, I want shortlisted properties set against one metric set, so that I can rank them on
like-for-like terms.

**Acceptance criteria**
- **AC1** GIVEN 2 to 8 shortlisted properties WHEN I compare them THEN each appears against the same metric set, with absent metrics marked absent rather than shown as blank or zero.
- **AC2** GIVEN one property missing a metric the others carry WHEN the comparison renders THEN it is excluded from ranking on that metric only, and the exclusion is stated.
- **AC3** GIVEN more than 8 properties WHEN I compare THEN the agent states the limit and does not truncate silently.

**Definition of done**
- [ ] Max comparison set per §3
- [ ] Absent is never rendered as zero

### US-PE-05 — Explain what drives a property's valuation
**Persona:** P2 Property Owner  **Epic:** Property Evaluation
**Priority:** Could  **Depends on:** US-PE-01

As a Property Owner, I want to see which attributes raise and lower my property's valuation, so that I can
decide where to spend before a sale.

**Acceptance criteria**
- **AC1** GIVEN a valuation meeting the evidence threshold WHEN I request drivers THEN attributes are listed as positive or negative, each with the comparables evidencing it.
- **AC2** GIVEN an attribute with no comparable evidence WHEN drivers are listed THEN it does not appear (X1).
- **AC3** GIVEN a driver list WHEN it is presented THEN no monetary uplift is attached to any improvement unless comparables evidence that figure.

**Definition of done**
- [ ] X1, X2 satisfied
- [ ] Confidence band from the underlying valuation carried through

### US-PE-06 — Ask free-form questions about a property
**Persona:** P1 Real Estate Agent  **Epic:** Property Evaluation
**Priority:** Should  **Depends on:** US-DF-01, US-EN-01

As a Real Estate Agent, I want to ask about a property in my own words, so that I need not know where each
fact is stored.

**Acceptance criteria**
- **AC1** GIVEN a question answerable from that property's records WHEN I ask THEN the answer cites every record used (X1).
- **AC2** GIVEN a question not answerable from records on file WHEN I ask THEN the agent states it does not hold the information and names what would be needed. **It does not answer from general knowledge** (X2).
- **AC3** GIVEN a property I hold no access rights to WHEN I ask about it THEN access is refused.

**Definition of done**
- [ ] General-knowledge fallback disabled — verified with a question whose answer is public but absent from records
- [ ] Single-record lookup time budget met (X4)

---

## 6. Epic 2 — Rental Analysis  → TO2

### US-RA-01 — Recommend an achievable rent range
**Persona:** P1 Real Estate Agent  **Epic:** Rental Analysis
**Priority:** Must  **Depends on:** US-DF-01

As a Real Estate Agent, I want a rent range built from comparable rentals, so that I can price a listing
with evidence behind it.

**Acceptance criteria**
- **AC1** GIVEN comparable rentals meeting the evidence threshold WHEN I request a recommendation THEN a rent range, the comparables used, and a confidence band are returned.
- **AC2** GIVEN comparables below the threshold WHEN I request one THEN the shortfall is stated and no figure is returned (X2).
- **AC3** GIVEN every comparable older than 12 months WHEN a range is returned THEN the band is Low and the recency is stated.

**Definition of done**
- [ ] Evidence threshold and bands per §3
- [ ] Range, never a single point

### US-RA-02 — Calculate rental yield
**Persona:** P2 Property Owner  **Epic:** Rental Analysis
**Priority:** Must  **Depends on:** US-DF-01

As a Property Owner, I want gross and net yield for my property, so that I can judge the return it is
actually producing.

**Acceptance criteria**
- **AC1** GIVEN a property with rent and cost records WHEN I request yield THEN gross and net yield return with every input value shown.
- **AC2** GIVEN cost records missing WHEN I request yield THEN gross returns, net is withheld, and the missing cost categories are named (X2).
- **AC3** GIVEN any yield figure WHEN it is shown THEN the calculation method is stated alongside it.

**Definition of done**
- [ ] Both formulae documented in the story
- [ ] X1 on every input

### US-RA-03 — Position a proposed rent against evidence
**Persona:** P2 Property Owner  **Epic:** Rental Analysis
**Priority:** Should  **Depends on:** US-RA-01

As a Property Owner, I want a proposed rent set against the current rent and the comparable range, so that
I can see where my proposal sits before I commit to it.

**Acceptance criteria**
- **AC1** GIVEN a proposed rent and comparables meeting the threshold WHEN I submit it THEN the agent shows its position against both the current rent and the comparable range, plus any vacancy indicators on file.
- **AC2** GIVEN no vacancy indicators on file WHEN the position returns THEN their absence is stated and **no risk score is invented** (X2).
- **AC3** GIVEN a proposed rent outside the comparable range WHEN the position returns THEN the distance beyond the range is quantified.
- **AC4** GIVEN any output WHEN it is produced THEN no rent is altered on any record (X3).

**Definition of done**
- [ ] Output defined as a position against evidence, not a prediction
- [ ] X1, X2, X3 satisfied

### US-RA-04 — Flag under- and over-performing units
**Persona:** P3 Property Manager  **Epic:** Rental Analysis
**Priority:** Should  **Depends on:** US-RA-01

As a Property Manager, I want units across a portfolio flagged against their comparable ranges, so that I
can see which rents are out of line without checking each one.

**Acceptance criteria**
- **AC1** GIVEN a portfolio with rent records WHEN I run the scan THEN each unit is placed against its comparable range, with those below and above flagged and the range shown.
- **AC2** GIVEN a unit without comparables meeting the threshold WHEN the scan runs THEN it is listed as **not assessable** — never as performing in line (X2).
- **AC3** GIVEN a portfolio scan WHEN it runs THEN it completes within the portfolio-scan time budget (X4).

**Definition of done**
- [ ] "Not assessable" reported as its own count, never folded into a pass
- [ ] Portfolio defined per §3

### US-RA-05 — Compare rental performance across my properties
**Persona:** P5 Investor / Buyer  **Epic:** Rental Analysis
**Priority:** Could  **Depends on:** US-RA-02

As an Investor, I want rental performance compared across the properties I hold, so that I can see which
are carrying the portfolio and which are dragging on it.

**Acceptance criteria**
- **AC1** GIVEN 2 or more properties with rent records WHEN I compare THEN each appears on one metric set.
- **AC2** GIVEN a property with no rent records WHEN the comparison renders THEN it is excluded and the exclusion is stated.
- **AC3** GIVEN any comparison WHEN it is produced THEN it draws only on the user's own properties, and **claims no external market position**.

**Definition of done**
- [ ] Scope limited to the user's own records — no external data source implied anywhere in the output

---

## 7. Epic 3 — Tenant Management  → TO3

### US-TM-01 — See a consolidated tenant profile
**Persona:** P3 Property Manager  **Epic:** Tenant Management
**Priority:** Must  **Depends on:** US-DF-01

As a Property Manager, I want one view of a tenant's lease, contact details, payment history and open
issues, so that I need not assemble it from four places before a conversation.

**Acceptance criteria**
- **AC1** GIVEN a tenant in my managed set WHEN I open the profile THEN lease terms, contact details, payment history and open issues appear together, each with its source and last-updated date (X1).
- **AC2** GIVEN a section with no records WHEN the profile renders THEN it reads "none on file" rather than rendering empty.
- **AC3** GIVEN a tenant outside my managed set WHEN I attempt to open it THEN access is refused.

**Definition of done**
- [ ] Four sections present in every profile, populated or explicitly empty
- [ ] Staleness marking per §3

### US-TM-02 — Work a lease renewal pipeline
**Persona:** P3 Property Manager  **Epic:** Tenant Management
**Priority:** Must  **Depends on:** US-TM-01

As a Property Manager, I want tenancies approaching expiry listed with a recommended action, so that no
renewal is missed by default.

**Acceptance criteria**
- **AC1** GIVEN tenancies with expiry dates WHEN I open the pipeline THEN those inside the renewal horizon are listed by expiry, each with a recommended action and the reason for it.
- **AC2** GIVEN a tenancy with no expiry date on file WHEN the pipeline renders THEN it is listed separately as **expiry unknown**, not omitted.
- **AC3** GIVEN a recommended action WHEN it is shown THEN nothing is sent and no record is altered without my confirmation (X3).

**Definition of done**
- [ ] Renewal horizon per §3
- [ ] Every recommendation carries its reason (X1)

### US-TM-03 — Identify and prioritise arrears
**Persona:** P3 Property Manager  **Epic:** Tenant Management
**Priority:** Must  **Depends on:** US-TM-01

As a Property Manager, I want tenants in arrears listed in priority order, so that I chase the largest
exposure first rather than the most recent.

**Acceptance criteria**
- **AC1** GIVEN payment records WHEN I open arrears THEN tenants in arrears appear with amount outstanding and days overdue, ordered by the arrears prioritisation rule.
- **AC2** GIVEN a tenant with incomplete payment records WHEN the list renders THEN they are flagged **cannot assess** — never *no arrears* (X2).
- **AC3** GIVEN the list WHEN it is shown THEN no tenant is contacted without my confirmation (X3).

**Definition of done**
- [ ] Prioritisation rule per §3, stated in the interface
- [ ] "Cannot assess" counted separately from "in arrears" and "clear"

### US-TM-04 — Triage maintenance requests by urgency
**Persona:** P3 Property Manager  **Epic:** Tenant Management
**Priority:** Should  **Depends on:** US-TM-05

As a Property Manager, I want open maintenance requests banded by urgency, so that an emergency is not
sitting behind a routine job in the queue.

**Acceptance criteria**
- **AC1** GIVEN open requests WHEN I open triage THEN each carries an urgency band with the reason, ordered most urgent first.
- **AC2** GIVEN a request whose description carries too little detail to band WHEN triage runs THEN it goes to **needs clarification** rather than receiving a guessed band (X2).
- **AC3** GIVEN a routing decision WHEN I make it THEN work is assigned only on my confirmation (X3).

**Definition of done**
- [ ] Urgency bands per §3
- [ ] Banding reason shown on every request (X1)

### US-TM-05 — Submit a maintenance request and track it
**Persona:** P4 Tenant  **Epic:** Tenant Management
**Priority:** Must  **Depends on:** US-EN-01

As a Tenant, I want to raise a maintenance request and follow its progress, so that I know it has been
received and where it stands.

**Acceptance criteria**
- **AC1** GIVEN I am signed in WHEN I submit a request with a description THEN it is stored against my tenancy and given a reference I can quote.
- **AC2** GIVEN I omit a required field WHEN I submit THEN submission is refused and the missing field is named.
- **AC3** GIVEN a request I have submitted WHEN I return later THEN I see its current status and the date it last changed.

**Definition of done**
- [ ] Required fields enumerated
- [ ] X1/X2 do not apply — this is data entry, not analysis. It is the input `US-TM-04` triages.

### US-TM-06 — Get answers about my own tenancy
**Persona:** P4 Tenant  **Epic:** Tenant Management
**Priority:** Should  **Depends on:** US-DF-01, US-EN-01

As a Tenant, I want to ask about my own lease in plain language, so that I need not read the whole
agreement to find one date or obligation.

**Acceptance criteria**
- **AC1** GIVEN a question answerable from my tenancy records WHEN I ask THEN the answer cites the clause or record it came from (X1).
- **AC2** GIVEN a question not answerable from those records WHEN I ask THEN the agent states it does not hold the information, and does not answer from general knowledge (X2).
- **AC3** GIVEN a question about another tenancy WHEN I ask THEN access is refused.
- **AC4** GIVEN a question calling for legal interpretation WHEN answered THEN the reply states it reports what the lease says and is not legal advice.

**Definition of done**
- [ ] Access boundary verified against another tenant's records
- [ ] Legal-interpretation disclaimer present on clause answers

### US-TM-07 — See a portfolio tenant summary
**Persona:** P2 Property Owner  **Epic:** Tenant Management
**Priority:** Should  **Depends on:** US-TM-01, US-TM-03

As a Property Owner, I want arrears, open issues and lease-expiry proximity rolled up across my portfolio,
so that I can see where attention is needed without opening every tenancy.

**Acceptance criteria**
- **AC1** GIVEN my portfolio WHEN I open the summary THEN it rolls up exactly the three components named in §3 — arrears status, open maintenance issues, lease-expiry proximity.
- **AC2** GIVEN a tenancy missing data for a component WHEN the summary renders THEN it is counted in a **not assessable** figure shown alongside, and never folded into a sound count.
- **AC3** GIVEN any figure in the summary WHEN I select it THEN it drills through to the tenancies behind it (X1).

**Definition of done**
- [ ] Exactly three components, per §3 — no undefined composite score
- [ ] "Not assessable" always visible next to the totals

### US-TM-08 — Draft tenant communications for review
**Persona:** P1 Real Estate Agent  **Epic:** Tenant Management
**Priority:** Could  **Depends on:** US-TM-01

As a Real Estate Agent, I want draft renewal and arrears letters populated from tenancy records, so that I
start from a filled draft instead of a blank page.

**Acceptance criteria**
- **AC1** GIVEN a tenant and a communication type WHEN I request a draft THEN it is produced from tenancy records with every inserted value cited (X1).
- **AC2** GIVEN a produced draft WHEN it is presented THEN **it is not sent**; sending requires my explicit confirmation (X3).
- **AC3** GIVEN data missing for a merge field WHEN the draft is produced THEN that field is marked incomplete rather than filled with a guess (X2).
- **AC4** GIVEN a notice carrying legal effect WHEN it is drafted THEN it carries a review-before-sending warning.

**Definition of done**
- [ ] No send path exists that bypasses confirmation
- [ ] Every merge field either cited or marked incomplete

---

## 8. Epic 4 — Cross-domain decision support  → TO4

Target outcome 4 asks for efficiency **and quality** of decisions **across** all three areas. Stories
confined to a single epic satisfy neither half: `US-XD-01` covers *across*, `US-XD-02` and `US-XD-03`
cover *quality*.

### US-XD-01 — Get one briefing spanning all three areas
**Persona:** P2 Property Owner  **Epic:** Cross-domain
**Priority:** Must  **Depends on:** US-PE-01, US-RA-02, US-TM-07

As a Property Owner, I want valuation, rental position and tenancy status for a property in one briefing,
so that a decision spanning all three does not take three separate sessions.

**Acceptance criteria**
- **AC1** GIVEN a property I own WHEN I request a briefing THEN valuation position, rental position and tenancy status appear together, each citing its sources (X1).
- **AC2** GIVEN one of the three areas lacking data WHEN the briefing renders THEN that section states what is missing and the other two still render (X2).
- **AC3** GIVEN a complete briefing WHEN it is presented THEN it shows positions and does not recommend selling, holding or re-letting (X3).

**Definition of done**
- [ ] All three sections present, populated or explicitly incomplete
- [ ] Multi-record analysis time budget met (X4)

### US-XD-02 — Review past recommendations against outcomes
**Persona:** P2 Property Owner  **Epic:** Cross-domain
**Priority:** Must  **Depends on:** US-XD-03

As a Property Owner, I want to see what the agent recommended against what actually happened, so that its
reliability is something I can observe rather than assume.

**Acceptance criteria**
- **AC1** GIVEN recommendations recorded by `US-XD-03` with a recorded outcome WHEN I open the review THEN each shows what was recommended, what was decided, and what followed.
- **AC2** GIVEN a recommendation with no outcome yet WHEN the review renders THEN it is listed as **outcome pending** and excluded from any accuracy figure.
- **AC3** GIVEN any accuracy figure WHEN it is shown THEN the number of cases behind it is shown with it.

**Definition of done**
- [ ] Pending cases never counted as agreements
- [ ] Sample size displayed beside every rate

### US-XD-03 — Keep a record of advice given and decisions taken
**Persona:** P2 Property Owner  **Epic:** Cross-domain
**Priority:** Must  **Depends on:** US-DF-01

As a Property Owner, I want what the agent recommended and what was decided kept on record, so that advice
can be reviewed after the fact rather than disappearing with the session.

**Acceptance criteria**
- **AC1** GIVEN the agent returns a recommendation WHEN it is presented THEN it is recorded with a timestamp, the inputs cited, and the user it was shown to.
- **AC2** GIVEN I act on a recommendation WHEN I confirm the action THEN the decision is recorded against that recommendation.
- **AC3** GIVEN a recorded entry WHEN a correction is needed THEN it is appended — entries are not editable after the fact.

**Definition of done**
- [ ] Append-only storage verified
- [ ] Every X3 confirmation writes a decision record

---

## 9. Appendix A — Enabling stories

*Outside the scope stated in the source document, but the epics above cannot function without them.*
Each names a persona: a story with no user is not a user story.

### US-EN-01 — Sign in and see only my own records
**Persona:** P4 Tenant  **Epic:** Enabling
**Priority:** Must  **Depends on:** —

As a Tenant, I want to sign in and see only my own tenancy, so that my records are not visible to other
tenants and theirs are not visible to me.

**Acceptance criteria**
- **AC1** GIVEN valid credentials WHEN I sign in THEN I see records for my own tenancy only.
- **AC2** GIVEN a request for a record outside my tenancy WHEN it is made THEN it is refused and the attempt is recorded.
- **AC3** GIVEN any of the five personas WHEN signed in THEN the visible record set matches that role's defined scope.

**Definition of done**
- [ ] Access boundary tested per persona, not only for the tenant
- [ ] Refusals written to the record in `US-XD-03`

### US-EN-05 — Have my personal data kept only as long as required
**Persona:** P4 Tenant  **Epic:** Enabling
**Priority:** Should  **Depends on:** US-EN-01

As a Tenant, I want my personal data retained only for the period the governing jurisdiction requires, so
that it is not held indefinitely by default.

**Acceptance criteria**
- **AC1** GIVEN the retention period for the configured jurisdiction elapses WHEN the retention job runs THEN my data is deleted or anonymised per the stated rule.
- **AC2** GIVEN I ask what is held about me WHEN I request it THEN a complete list is returned.
- **AC3** GIVEN no jurisdiction is configured WHEN the system starts THEN it flags the gap rather than applying an unstated default.

**Definition of done**
- [ ] Jurisdiction: **`TBC — product owner`**. The source document names none, and a retention period cannot be defaulted responsibly.
- [ ] Retention rule documented before any tenant data is stored

---

## 10. Appendix B — Deferred

| Story | Reason held back |
|---|---|
| `US-RA-06` — summarise rental demand and seasonality | Requires external market data. The Project Purpose scopes the agent to *"the information available to them"*, and no such feed is established anywhere in the source document. Reinstate if a market-data source is confirmed. |

---

## 11. Validation report

Two validation passes were run against the three success metrics. The findings below were applied to this
document, not merely noted.

### 11.1 Coverage — traceability matrix

| Source requirement | Satisfied by | Status |
|---|---|---|
| Required functionality: Property Evaluation | US-PE-01 … 06 | ✅ |
| Required functionality: Rental Analysis | US-RA-01 … 05 | ✅ |
| Required functionality: Tenant Management | US-TM-01 … 08 | ✅ |
| TO1 — evaluate properties efficiently | US-PE-01 … 06, US-DF-01 | ✅ |
| TO2 — analyse rental information effectively | US-RA-01 … 05, US-DF-01 | ✅ |
| TO3 — manage tenant information and activities | US-TM-01 … 08, US-DF-01 | ✅ |
| TO4 — efficiency of decisions **across** all three | US-XD-01 | ✅ |
| TO4 — **quality** of decisions | US-XD-02, US-XD-03 | ✅ |

All five personas are the subject of at least one main-body story: P1 (PE-01, PE-02, PE-06, RA-01, TM-08),
P2 (PE-05, RA-02, RA-03, TM-07, XD-01, XD-02, XD-03), P3 (DF-01, RA-04, TM-01…04), P4 (TM-05, TM-06),
P5 (PE-03, PE-04, RA-05).

### 11.2 Findings — first pass

| Metric | Finding | Action |
|---|---|---|
| Coverage | TO4 unmet — nothing addressed decision *quality*, and every story sat inside one epic despite TO4 saying *across* all three | Epic 4 added |
| Clarity | Evidence threshold, time budget, confidence level and "tenant health" were referenced but never defined — the criteria resting on them were untestable | §3 Defined terms added |
| Clarity | "Model a rent change" left the output undefined | Rewritten as `US-RA-03`, output stated |
| Clarity | "Tenant health" was an undefined roll-up | Three components named (§3, TM-07) |
| Clarity | Condition summary assumed inspection notes the source document never mentions | `US-PE-02` must name its inputs |
| Clarity | Retention period unverifiable with no jurisdiction stated | `TBC — product owner`, recorded not defaulted |
| Relevance | Comparing "across markets" needs external data not established as available | `US-RA-05` narrowed to the user's own properties |
| Relevance | Demand and seasonality depends entirely on unavailable market data | `US-RA-06` deferred (Appendix B) |

### 11.3 Findings — second pass

The first pass revised stories but left the surrounding structure describing the old set. Most of what
follows is self-inflicted drift, which is what a re-validation exists to catch.

| Metric | Finding | Action |
|---|---|---|
| Coverage | Contents structure still described the pre-Epic-4 document | Rewritten |
| Coverage | Personas table was never updated after Epic 4 was added | P2 given XD |
| Clarity | A priority field existed with no scheme defined and no story prioritised | MoSCoW pinned to a TO-failure rule |
| Clarity | Nothing distinguished DoD from AC, so the doubled format would restate itself | AC behavioural, DoD non-behavioural |
| Clarity | `US-XD-01` carried two personas; under role-based access they would not see the same records | Assigned to P2 |
| Relevance | Enabling stories had **no persona at all** — system capabilities, failing the "end user's perspective" requirement | All given personas |
| Relevance | One enabling story was circular: "enforce X1/X2", already universal criteria, with no user | Removed (26 → 25 cards) |
| Availability | `US-XD-02` depended on an out-of-scope appendix story — the gate that deferred `US-RA-06` had not been applied to it | Escalated, then resolved by the scope decision below |
| Consistency | No dependency field existed despite real cross-story dependencies | `Depends on` added to every card |
| Consistency | Maintenance-request submission is ingestion sitting in the main body while data loading sat in the appendix | Resolved by the scope decision below |

### 11.4 Scope decisions taken

Both questions arose from validation and were settled by the project owner. Both **widen the scope the
source document stated**, and are recorded here rather than applied silently.

| Question | Decision | Consequence |
|---|---|---|
| The Project Purpose says the agent works *"based on the information available to them"*, implying records exist — while Defined Scope admits nothing beyond the three areas. Is data ingestion in scope? | **In scope** — Epic 0, `US-DF-01` | The set is now buildable, and the `US-TM-05` inconsistency dissolves: ingestion is no longer split across the scope boundary |
| `US-XD-02` covers TO4's quality half but depended on an out-of-scope audit trail | **In scope** — `US-XD-03` | TO4 is genuinely covered, and no main-body story depends on an appendix story |

### 11.5 Gaps in the source document

Assumptions this document had to make, each stated so it can be confirmed or corrected:

1. **No data sources named.** Every story assumes records are held by the agent (now `US-DF-01`). If they live in an external system, every epic gains an integration dependency.
2. **No user roles named.** "Real estate stakeholders" was resolved into the five personas in §1.
3. **No thresholds or KPIs.** Every value in §3 is a proposed default awaiting sign-off.
4. **No non-functional requirements.** Volume, availability and concurrency are unstated; only response-time budgets are proposed here.
5. **No jurisdiction or compliance context.** Retention in `US-EN-05` is left `TBC` rather than guessed.
6. **The Defined Scope section understates the build.** Two functions the three named areas cannot operate without — data loading and an audit trail — were excluded by it. This finding belongs in front of whoever owns that document.
