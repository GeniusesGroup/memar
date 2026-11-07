<!--
  NOTE: this is a seed document, not a finished RFC. It captures only the framing
  and motivation discussed so far, across two conversations: one primarily about
  a different topic (Contributor attribution, 2026-07-04), and the dedicated
  Task Management discussion with ChatGPT (2026-08-04/05, transferred here so
  that chat could be deleted). Omid asked for this to be kept outside of git
  (not committed) as a placeholder, to be picked up and actually designed —
  Reference-level explanation onward — in a dedicated future session.
-->

---
RFC Number: 000000  # PLACEHOLDER — not yet meaningful; this document is not ready for numbering.
Title: "Task: A Unified Work-Item Primitive"
Status: Draft
Start Date: 2026-07-04
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Task is proposed as a single, deliberately general primitive representing any unit of work that can be planned, discussed, decomposed into subordinate units, and tracked toward completion — intended to replace the need for separate, incompatible models for things commonly (and, in Omid's view, ambiguously) branded across the software industry as project management, production/manufacturing tracking, issue tracking, and customer support ticketing. This document captures only the framing and motivating examples discussed so far. The actual data model, state semantics, and dependency mechanics are explicitly out of scope here and deferred to a dedicated design chat.

Two definitional stances from the 2026-08-04/05 discussion constrain the design:

- **The word "small" is ecosystem bias, not the concept.** The dictionary definitions of task — "any piece of work that is undertaken or attempted"; "a specific piece of work required to be done as a duty or for a specific fee" — contain no size qualifier. The instinct to define a Task as a *small executable unit* came from project-management tools, not from the concept. Consequence: a project is not a degenerate or overloaded use of Task; the industry hierarchy `Project → Epic → Story → Task/Bug` may invert to a flat Task model where "Project", "Epic", and "Story" are conventional names for some Tasks, distinguished by attributes, relations, and rules rather than by separate entity types.
- **Task management is needed even by a one-person organization.** What the industry sells as a standalone "reminder" feature is task management in disguise: one defines a work item and specifies when it must be done. The software should reason over it (see the organizational-reasoning handoff): e.g. warn a solo owner who has accumulated dozens of roles that they are overcommitting and should post a hiring Task and delegate.

## Motivation
Terms like ERP and BPMS carry vendor-specific branding and inconsistent, ambiguous meaning across the industry, even though the underlying problems they address — decomposing a unit of work into subordinate units, tracking each independently, and knowing when a larger unit is done because its parts are done — are the same problem being solved repeatedly, differently, in unrelated tools (a project tracker, a manufacturing system, an issue tracker, a helpdesk). A single, well-defined primitive avoids re-solving this problem separately for every domain that happens to need it.

## Guide-level explanation
A Task is general enough to represent, among other things:

- **A project** is itself a Task — e.g. constructing the company's headquarters is a Task that someone (not necessarily a human) is responsible for pursuing and delegating its sub-Tasks to, and that can remain active for the life of the project while splitting into thousands of finer Tasks.
- **A production run** is a Task that can automatically spawn many finer-grained subordinate Tasks. For example, manufacturing a piece of furniture from a submitted order can generate a whole tree of subordinate Tasks (framing, painting, and so on) derived from a separate Task that defines the manufacturing process itself, each independently trackable.
- **An issue** is a Task.
- **A support ticket** is a Task that may depend on several internal Tasks related to a user's request, without needing to expose that internal complexity to the user — only the final outcome needs to reach the user-facing ticket, for example automatically once its subordinate Tasks reach a completed state.
- **A leave request** is a Task — not an independent "HR domain" entity. HR is a *consumer* of the organization model, not a sibling domain (see the organizational-reasoning handoff): hiring, performance review, and promotion are likewise expected to be expressible with the base model rather than assumed as primitives.

Things commonly modeled as standalone concepts are expected to reduce to **behaviors, policies, or rules attached to a Task** rather than sibling entities:

- Deadline, reminder, escalation, delegation — responsibilities of managing one Task, not five features. ("Reminder" = a Task plus a policy about notifying; the industry's standalone reminder products are the concept re-derived badly.) Priority_Rank is Thing's, not Task's.
- "Sprint"-like time constraints — plausibly a time-bound rule/constraint on a set of Tasks, not a Task subtype.

## Reference-level explanation
Deliberately not addressed in this seed document. This is where the real design work belongs: the actual fields of a Task, how subordinate/dependency relationships between Tasks are represented, and the precise mechanics of status and completion propagation from subordinate Tasks to a parent.

## Drawbacks
Not fully explored yet; concerns worth carrying into the dedicated chat:

- A primitive general enough to cover a project, a production run, an issue, and a ticket risks becoming too undifferentiated to do useful classification or validation work, unless it is later paired with enough structure to distinguish meaningfully different uses without reintroducing the same category-proliferation problem this RFC is trying to avoid.
- Automatic completion propagation from subordinate Tasks to a parent needs real semantics: partial completion, a failed or rejected subordinate, optional versus required subordinates, and parallel versus sequential dependency structures. This is comparable in depth to long-studied workflow-modeling problems and should not be treated as an incidental detail.
- The flat-Task stance cuts against two decades of user training (Project/Epic/Story/Task tooling); even if technically right, onboarding and UI projections will need to reconstruct familiar hierarchies as projections, not as the model.
- "Task" is itself under suspicion of being a familiar industry word rather than a fundamental entity; committing the primitive name early may produce renaming churn later — accepted for now, with no better word currently identified (Omid explicitly keeps a weak guard: if a better word emerges, the rename is allowed).

## Rationale and alternatives
- Deferred in general to the dedicated chat. Two stances already taken:
- **Flat Task over the industry hierarchy**: `Project → Epic → Story → Task/Bug` presumes scale-graded entity types. Under the dictionary definition, all of these are "pieces of work undertaken"; what differs (duration, subtask count, number of responsible parties, resource breadth, dependency depth) are attributes and relations. Rejected alternative: separate Project/Epic entity types — reintroduces the ERP-style category proliferation this RFC exists to avoid.
- **Word choice deferred, not decided**: "Task" is kept as the working name for lack of a better word and for lexical fit (same argument style as `user`), while the question "is Task the fundamental entity, or another industry label on something deeper?" stays open.

## Prior art
Not addressed yet, beyond points worth carrying forward:

- Rejecting vendor-branded terms like ERP or BPMS does not necessarily mean rejecting the underlying technical and academic literature on workflow modeling (task decomposition, dependency graphs, exception handling in process models), which exists independently of any specific commercial product and predates most of the branded tools built on top of it. That literature may be worth reviewing in the dedicated chat, independent of any vendor terminology.
- The recurring reduction pattern observed across this project (and Memar before it): Service → maybe Capability; Repository → maybe Storage Policy; Aggregate → maybe Boundary; Event → maybe Observation; and here: Project → maybe Task; Department → maybe Group (see [`group/README.md`](../../group/README.md)); Reminder → maybe Rule; Sprint → maybe Time Constraint. The working question in every case: *is this an independent concept, or a configuration of a more fundamental one?*

## Future possibilities
Deferred to the dedicated chat.
