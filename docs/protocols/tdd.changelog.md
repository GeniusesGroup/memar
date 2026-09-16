# TDD Realization Changelog

## Changelog

### Initial draft — TDD as written input/output expectations before enactment
- Time: 2026-09-16T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, reviewed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- The initial draft states TDD as a domain-independent discipline derived from [Process](../process.md): before a process is enacted, the expectations for its input and output are written. TDD is the instance where the process is software development and the written expectation takes a machine-checkable form.
- The definition is grounded in the process concept rather than in software testing, so that canopy concepts such as the user story resolve to the same artifact: a process's written input and output expectations — not a documentation genre beside the code.
- The scope section states where the discipline binds, where it does not, and why: exploratory processes (expectations written for the inquiry itself), already-enacted processes (verification work, not the discipline), and non-repeatable processes (the first benefit stands; the check is unavailable, not voided).

#### Considered and not done
- **Teaching the discipline through worked examples (rejected)**: a demonstration is a surface pattern an executing agent can imitate without its reason, and imitation of a case's surface is what misleads when the next case differs. The document gives reasons and relationships; the absence of examples is an explicit decision of this draft, not an omission. (Omid Hekayati)
- **Defining TDD by the red-green-refactor cycle or by test code (rejected)**: the cycle, frameworks, and file layouts are enactment mechanisms of one possible realization. Defining the discipline by its most common mechanism would repeat the mechanism-first error process.md names. (Omid Hekayati)

#### Deliberation
- Omid's stated motivation, carried into the document's own Motivation: before anyone knows how a process must be carried out, they already hold its input and output expectations tacitly, in temporary memory — so the discipline is simply making that holding explicit and shared *first*, rather than leaving it private and exempt from checking.
- The root of the discipline in the word *process* — which has its own document — was claimed as the reason the definition stays domain-independent, and is what grounds the user-story reading.

---

### Relocation — concept core moved to process.md; document rewritten as the software adoption
- Time: 2026-09-16T00:00:00Z
- Type: Changed
- Propagates to:
  - process.md: Done — new topics *Expectations and Checks* and *Development as a Process*; entry in its changelog.
  - process.changelog.md: Done — the addition entry recorded there.
  - process.handoff.md: Done — open questions and the Development graduation criterion recorded there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- The concept-level core of the initial draft — expectations written before enactment, the check as the comparison of an instance against stated expectations, why tacit holding fails, the post-hoc and inquiry boundaries — moved to [Process → Expectations and Checks](../process.md#expectations-and-checks), where Omid located it: without the process model, testing has no subject, so the concept is Process's property, not TDD's. This document was rewritten to consume that topic and keep only what is Memar's own: the adoption of the name, the mechanism separation, the user-story reading, and the scope (Super Z — applied).
- New first topic *What Memar Adopts* states the adoption and the name's role: the ecosystem's word is kept to reach the developers who carry it, while definitions stay anchored to the concept layer (Super Z — drafted; Omid — approved).
- Scope restated to cover Memar's non-software system categories and Memar's own documentation production.
- A *Development as a Process* topic was added to `process.md` in the same pass, defining Development per its established general meaning — a process of stage-by-degree advancement — so this protocol's governing relationship to development runs through the concept layer instead of resting on an undefined word (Omid — argued; Super Z — drafted).

#### Considered and not done
- **Keeping the concept core in this protocol document (rejected)**: the concept is domain-independent and definitional; keeping it here would force base documents to cite a protocol layer for a general meaning, which the layering's citation rule forbids, and would entangle the concept with TDD's name — the conflation the discipline exists to prevent. (Omid Hekayati)
- **A Development document at docs/ root or under protocols/ (rejected for now)**: the concept's warranted content fits a topic in `process.md` without residue, and Development is the process under governance rather than a rule set, so it fails the protocols folder's membership criterion. Graduation criterion recorded in `process.handoff.md` (Omid Hekayati).

---

### Scope generalized from software to systems, per Omid's review
- Time: 2026-09-16T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed, argued, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- The document's stated scope was generalized from "the development of software" to "the development of systems" — Development taken in the full generality [Process → Development as a Process](../process.md#development-as-a-process) defines. The Abstract, *What Memar Adopts*, and *Scope* were rewritten accordingly (Super Z — applied).
- The name's role was made explicit: TDD is the word software's ecosystem gave the discipline, and its home territory remains software — the place where the check most often takes a machine-applicable form. Memar keeps the name to reach the developers who carry it while the discipline itself binds every domain: a checkout counter being designed for a store and a mobile phone being brought to production are under the same ordering as a function, their expectations written before the work and checked after (Omid Hekayati — argued; Super Z — drafted).
- The *Scope* topic now states what varies across domains: the form the check can take, never whether the ordering binds.

#### Deliberation
- Omid's review of the relocation pass objected to scoping the adoption to software: though the draft's wording had addressed development generally without noticing, a physical product (a mobile phone) or a piece of store equipment being designed (a checkout counter) needs its expectations stated just as much — and whenever anything is to be developed, its input and output expectations exist implicitly in the development's path even unwritten, so the discipline's demand is only that they not be left implicit: "don't fool ourselves; write them from the start" — since no system can be developed without knowing what is wanted from it. Limiting the word to anything narrower than System would repeat the narrowing this project has repeatedly pushed back against (Omid Hekayati).
- The objection was accepted in full; the earlier draft's software-leaning phrasing was an artifact of the name's origin, not a considered position, and the rewrite keeps the name while removing the boundary it appeared to draw (Super Z — recorded; Omid Hekayati — the decision).

---

### Practice companion created; Abstract pointer and Boundary retarget added
- Time: 2026-09-16T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — the *Defect Resolution as an Inquiry* topic the Boundary retarget links is added there; entry recorded in [process.changelog.md](../process.changelog.md).
  - process.handoff.md: Done — the topic's open questions and graduation criterion recorded there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- Created `tdd.practice.md` as the paired Practice facet, per the owner's direction that the protocol must not stay reasons-only: the procedure a development step follows — naming the process and intent, writing the expectations in checkable form before enactment, choosing the check's form by domain (executed test where possible, observation procedure where not), enacting the smallest increment, and running the check with recorded disposition — plus where the expectation lives (the another-agent-could-run-the-check test), a failure-modes table, the inquiry and post-hoc-verification boundary routing carried from [Process → Expectations and Checks](../process.md#expectations-and-checks), and per-scale guidance (function, feature, system). Steps carry links to the base document's topics and are not re-argued there.
- The base document's Abstract gained one sentence pointing at the practice, following the pattern [filesystem.md](./filesystem.md) set with its companion practice.
- The practice's Boundary section names the reported defect as the inquiry case's recurring instance and links [Process → Defect Resolution as an Inquiry](../process.md#defect-resolution-as-an-inquiry), so a defect investigation routes through that topic and only the concluding fix runs this practice's cycle.
- Per the changelog scope rule, the practice companion shares this ledger and receives no changelog of its own.

#### Considered and not done
- **Importing worked examples into the practice (rejected)**: the base document's exclusion of examples is an explicit decision, and the practice's steps are the followable form of the reasons, not a second place for demonstrations. (Omid Hekayati)

#### Deliberation
- The owner's direction: the base document deliberately excludes worked examples — a demonstration is a surface pattern to imitate — but the discipline must still be followable; the practice carries the followable procedure without importing examples, so the exclusion stands while the agent-level question "what do I actually do at the start of a development step?" has a home (Omid Hekayati).
- The defect-routing addition follows the owner's approved plan for the Defect Resolution topic: the practice names the situation's home rather than carrying its own debugging guidance (Omid Hekayati — decided; Super Z — applied).

---
