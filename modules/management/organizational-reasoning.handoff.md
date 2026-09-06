# Management Organizational Reasoning Handoff

## Topic & Purpose
Consolidating the positioning claim that emerged from the Task Management discussions (2026-08-04/05): the organization project is a **system for modeling and reasoning about an organization**, not primarily a system for executing organizational processes — and working out what follows for HR, rules, and capacity analysis.

## Status
Active — the positioning is endorsed in discussion but nothing is implemented or formally ratified against it yet.

## Decisions
- **Positioning claim** — confidence: Tentative (Omid and the assistant converged; not yet recorded anywhere governing). Reasoning: task execution is one output; the core value is reasoning over the model of the organization itself (roles, staff, tasks, capacity, structure); workflow engines/ERP/BPM start from process execution, which is the differentiator to avoid.
- **HR is a consumer, not a domain** (Tentative): leave request, hiring, performance review, promotion must not be assumed as independent entities/modules — a leave request is a Task; hiring is a possible decision output; reviews/promotions are analyses over Task/Role/Staff relations. Whether any needs dedicated structure is a conclusion of modeling, not a starting assumption. Rejected alternative: HR as a sibling domain (repeats the start-from-industry-vocabulary failure).
- **Decisions come from diagnosis, not rules** (Tentative): the naive "role count ↑ ⇒ recommend hiring" was rejected as the 1980s expert-system failure mode (static if-then cause-effect). Pipeline: Reality → Observation (model state: assignments vs capacity, slipped due dates, backlog growth) → Diagnosis (reasoning) → Decision → Action (hire, outsource, re-scope, reprioritize, train, rest, automate, remove responsibility...). Hiring is one possible Action, never a direct rule output. The capacity-carrying relation is **Staff↔Task**. Rule-side echo recorded in [`../computer/rule/README.md`](../computer/rule/README.md).

## Ambiguities Resolved
- "Smart HR" framing — resolved: the one-person-organization warning (solo owner holding dozens of roles; system suggests a hiring Task + delegation) is organizational reasoning over the model; no HR domain involved.
- Assistant's linear approval example — resolved: see the estate-side correction (approval ≠ certification); same pattern here: diagnosis replaces permission machinery.

## Open Questions
1. Where do observations live — pluggable analytics over Task/Staff relations, or first-class recorded facts? (Connects to analytics-is-always-pluggable in `modules/economics/core-vs-pluggable.md`.) **Blocks** pipeline design.
2. How is a diagnosis represented — an artifact with cited observations? Who/what may produce one? **Blocks**.
3. What authorizes an Action (e.g. posting a hiring Task) — delegation/rights, or new consent machinery? **Blocks**.
4. Is the pipeline general infrastructure (finance, governance) or management-module private? — does not block the first worked example.

## Assumptions
- **The reasoning trace must be auditable** (a suggestion links to the observations and diagnosis path that produced it) — stability: Strong (both sides aligned; untested in design).
- **The one-person organization is the right first worked example** — stability: Weak; exercises roles, tasks, capacity, delegation, hiring with no stakeholder ambiguity, but may prove too degenerate to generalize from.

## Key Definitions Established
- Organizational Reasoning (working): drawing conclusions (diagnoses, suggestions) from the model of the organization, as distinct from executing processes or firing pre-coded rules.

## Proposed Next Steps
1. Resolve open #1 (observation storage) with the analytics placement criteria.
2. Sketch the diagnosis-artifact shape (open #2) using the reasoning-trace assumption.
3. Work the one-person-organization scenario end-to-end as the first test.

## Related Artifacts
- [`README.md`](README.md) — module home (Update if the positioning gets ratified)
- [`../computer/rule/README.md`](../computer/rule/README.md) — Rule side of the diagnosis-not-rules decision (None)
- [`task/edges/task-concept.md`](task/edges/task-concept.md) — Task side; unresolved #12 (capacity analysis) (None)
- [`../economics/core-vs-pluggable.md`](../economics/core-vs-pluggable.md) — analytics placement criteria (None)

## Notes
- Source conversation retired; all durable content is here and in the artifacts above.
