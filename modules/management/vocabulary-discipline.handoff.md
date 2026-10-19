# Management Vocabulary Discipline Handoff

## Topic & Purpose
Proposing a standing methodological rule for the project — **no common management term (Task, Project, Department, Team, Employee, Manager, Process, ...) is accepted as a fundamental concept of the model until its conceptual definition has been extracted** — and consolidating the reduction hypotheses it has produced so far. From the Task Management discussions (2026-08-04/05).

## Status
Active — the rule is practiced but not yet ratified anywhere; the fundamental-concept evaluation has not started.

## Decisions
- **The rule itself** — confidence: Tentative (Omid endorsed the reasoning; no ratification home decided). Reasoning: management/social vocabulary carries decades of semantic, cultural, and commercial baggage — more than software concepts — so the seduction risk is higher than it was in Memar; a named, checkable gate is needed, not reviewer vigilance. Rejected alternatives: reviewer vigilance alone (failure invisible at capture time); banning industry words outright (target is epistemic, not lexical — the word may be the right label *after* extraction); applying only to "big" terms (reminder/sprint-class terms are exactly where bias enters unnoticed).
- **Application procedure** (Tentative): (1) ask "independent concept, or configuration of a more fundamental one?"; (2) extract the conceptual definition before sketching any entity graph; (3) check the dictionary — ecosystem bias inserts qualifiers the word does not carry (e.g. "small" in Task); (4) fix the term with a weak rename guard; (5) record the reduction hypothesis even when keeping the term.

## Ambiguities Resolved
- Task's "small" qualifier — resolved: dictionary ("any piece of work that is undertaken or attempted") carries no size qualifier; the instinct came from PM tooling, not the concept. Consequence recorded in [`task/edges/task-concept.md`](task/edges/task-concept.md).
- Whether DDD's Ubiquitous Language conflicts — resolved: opposite emphasis, not contradiction; DDD adopts business language, this rule demands extraction first because management vocabulary carries vendor branding DDD's stakeholders do not impose.

## Open Questions
1. Where is the rule ratified — `Contribution.md` (a pointer exists there already), a future `docs/` modeling-method note, or this module? Should be findable before a new contributor's first schema proposal. **Does not block practicing the rule.**
2. Does the rule need an enforcement artifact (PR checklist for new concepts) or is documentation enough?
3. Retrospective audit: which existing module names would fail the rule today (candidates: `meeting`, `shift`)? Is an audit wanted at all?

## Assumptions
- **Candidate fundamental concepts** (from the discussion; stability: Unexamined): Goal, Responsibility, Commitment, Capability, Capacity, Constraint, Resource, Role, Decision, Relationship. Hypothesis: Task, Reminder, Meeting, Sprint, Ticket (and likely Project, Department, Employee) each reduce to configurations of these — differences live in rules, relations, and policies, not entity essence. If it falls: the industry vocabulary survives as primitives, and the rule's payoff shrinks to naming hygiene.
- **The software-side bias list generalizes to management** (Database-first, Aggregate Root, language-coupled modules, control-flow/error-handling as language features) — stability: Strong (documented in Memar discussions).

## Key Definitions Established
None yet — the rule demands definitions per term; the applied examples so far: Task (working name kept, definition open — [`task/edges/task-concept.md`](task/edges/task-concept.md)), Department (settled structurally as Group — [`group/README.md`](group/README.md)), Leadership (colloquial umbrella — [`../../bundles/leadership/README.md`](../../bundles/leadership/README.md)).

## Proposed Next Steps
1. Decide the ratification home (open #1) and extend the rule text into `Contribution.md`.
2. Evaluate the candidate concept list one by one under the rule, starting with the terms the modules already use (`role`, `group`, `task`).
3. If the audit (open #3) is wanted, schedule it after the candidates are evaluated.

## Related Artifacts
- [`README.md`](README.md) — module home (Update when the rule is ratified)
- [`task/edges/task-concept.md`](task/edges/task-concept.md) — applied example + the reduction pattern (Prior art section) (None)
- [`group/README.md`](group/README.md) — applied example (None)
- [`../../bundles/leadership/README.md`](../../bundles/leadership/README.md) — sibling caution (None)
- Memar `docs/terminology.md` — the discipline's origin (None)

## Notes
- Worked examples are the rule's acceptance risk: without them it reads as pedantry to contributors used to industry vocabulary (Drawback recorded).
- Per-module "vocabulary audit" notes (definition, reduction hypothesis, rename-guard status per name) remain a Future possibility, not started.
