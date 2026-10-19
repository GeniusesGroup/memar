# Role Handoff

## Topic & Purpose
Agency-based staffing model for human/AI roles; role ≠ tool knowledge; Telegram-derived hiring and role-design bullets (architect hiring, design vs engineering, cross-disciplinary literacy, service segmentation, tool ≠ architecture, mentor/coach/consultant).

## Status
Active — directions decided; several items remain candidate org rules pending ratification.

## Decisions

### From Organization ideas backlog — Agency (`Agency - chatgpt.md`)

- **Model the org's human/AI staffing on the agency cluster, not on "employees with tools".** The
  concepts the org's role/permission/contract machinery needs are already separated in memar's
  `agency.md`: Delegation ≠ Responsibility ≠ Authority ≠ Capability; Agent is a *position* in a
  relationship (`agent_for`), not an entity type; accountability does not automatically transfer with
  delegation. When the org models "who may do what", start from these distinctions instead of
  importing an HR-shaped taxonomy — the open questions it still carries (accountability split?
  intrinsic vs delegated agency boundary?) are the org's open questions too. *(direction; the org is
  the first real consumer that can settle several of them)*

### Third-pass — role ≠ tool

- **Role definitions — human staffing and agent briefs alike — must not reduce a role to a named
  tool's knowledge.** Role = primary focus area, never a knowledge boundary: `React Developer` does
  not mean the knowledge required is React (same for "Database Agent"). The boundary case any org
  role template must survive: the multipotentialite thinker whose breadth comes from abstraction and
  thinking modes, not accumulated volume. *(decided direction; ties to the agency-modeling item
  above — the org's role/permission docs should inherit it as an explicit failure mode)*

### Fourth pass — Telegram-group exports (Omid Hekayati's messages)

- **Hire and grow architects who reason in "approaches within architecture", not "architecture
  vs. architecture".** The owner's recurring teaching line: the sum of all decisions is the
  architecture; "clean", "microservice", "modular", "DDD" are approaches *inside* it, complementary
  more often than competing. Org tech-lead/architect hiring and its architecture-review practice
  should test for exactly this move — a candidate who argues approach-against-approach instead of
  composing approaches against requirements is the anti-pattern. *(decided direction; candidate org
  engineering-hiring and review criterion)*
- **Separate design roles from engineering roles in the org's role model.** The recurring position:
  design creates or reshapes requirements; engineering implements existing ones — and software
  engineers drifting into service design is a named industry failure. The org's staffing model
  (and its agent-fleet briefs) should keep the modes distinct, with architecture on the design side
  of the line. *(decided direction; ties to the role-≠-knowledge item in the third pass)*
- **Cross-disciplinary literacy is a hiring/promotion signal for architecture-track roles.** The
  owner's maxim — "what stays a question for years in one science was answered long ago in another"
  — plus the building/medicine/industrial-engineering examples. The org's knowledge workflows should
  schedule cross-domain study, and its architecture-track evaluation should value demonstrated
  cross-domain reading. *(direction; ties to the multipotentialite boundary case in the third pass)*
- **Service segmentation decisions are simultaneously team-segmentation decisions.** From the
  microservice critique: adopting a distributed approach reshaped industry department boundaries,
  often without a domain reason. When the org partitions its services, it is also partitioning its
  teams — decide segmentation from the domain model and ownership boundaries, never from tooling
  fashion, and expect every partition to add a real integration cost. *(direction; candidate org
  org-design rule — the org is the first consumer of memar's modularity distinction between Module
  and deployment/service units)*
- **Keep tool adoption separate from architecture decisions in org evaluation.** The recurring
  teaching line: k8s/grpc/protobuf-style tooling is not an architecture — evaluating a platform
  proposal must first name the architectural decision, then check whether the tool serves it; tools
  chosen for their own sake accumulate hidden requirements. *(direction; operationalizes the
  framework/protocol-first rule recorded in memar's framework handoff)*
- **Mentor / coach / consultant are distinct roles — keep them distinct in the org's people and
  AI-role definitions.** Owner's distinctions: a mentor never gives direction, only helps the person
  ask better questions; a coach helps answer the big questions but not the small navigational ones;
  a consultant is a commercial hybrid carrying contractual obligations. The org's human-development
  ladder and its AI-fleet role briefs should use these as three different relation types, not one
  "helper" bucket. *(decided direction from the owner; ties to the agency relation modeling above)*

## Open Questions
- Agency open questions the org inherits: accountability split? intrinsic vs delegated agency boundary? *(direction; the org is the first real consumer that can settle several of them)*

## Research 001 questions and next steps (2026-10-18)

### Status
[role.research.001.md](role.research.001.md) is added (Active; nothing in it is Decided). It proposes that the domain's concept is the position and its occupancy, separate from the capacity in one relation, the authority bundle, the job description and the title, and it analyses staff, department, shift and calendar as one cluster. The Model and Policies of [role.md](role.md) are not edited; the Decided directions above are not re-argued.

### Open Questions raised by the research
Each has a default; what each blocks is in the research's Open Questions. The numbers here are this list's own (the research numbers its twenty-four differently, and merges none of these); the three that change the most are first.

1. **Is the concept the position and its occupancy, with capacities, authority bundles, job descriptions and titles separate?** Default: yes, with the test "can be full or vacant". Blocks: the domain statement, `edges-loop/role`, GR.8, TA.7, every `RoleID`.
2. **Are employment (staff) and occupancy (role) two relations, and does the Decided staff identity cover each employment?** Default: two relations; the user's identity stays the person's, and each employment gets its own identity. Blocks: staff-status per employment, person-position, hiring pipeline, attendance.
3. **Does authority and assignment bind to the position (late-bound, occupant resolved at a stated instant) or to the person?** Default: to the position, through delegate; acts carry "occupant acting as position". Explored: delegate has no research. Blocks: the delegate record (role, rule or bundle), `GetRoleAccess`, `PrivateInRole`, task assign rules, X3.
4. Folder and accessor name `role` or `position`? Default: keep `role`, call the concept "position", avoid `seat`.
5. Is a position its own thing that can take members, or a group classified as one? Default: its own identity that also takes members (group Q2).
6. Is an occupancy the group's membership record or its own? Default: the membership, kind `occupant`, `acting` or `exerciser for`.
7. One context at a time, any thing as context? Default: yes, changed by an event with history.
8. Are reporting and unit containment two relations? Default: yes; reporting has many parents and no effective occupancy upward.
9. May an occupant be an organization, a group or a software agent, with an exerciser separate? Default: yes.
10. Are count, eligibility, term, incompatibility and succession order rules at named points? Default: yes; identity invariants stay Code.
11. Are the organization's required hours and a person's preference two records? Default: yes, different asserters.
12. Is `shift` demoted to the pattern of a coverage pluggable, instances as tasks, assignments as occupancies? Default: yes (survey default P12).
13. Does a leave suspend an occupancy? Default: a leave is a task kind; suspension is a rule of the organization.
14. Is the design/engineering distinction a rule over a position's focus and never a barrier to reasoning? Default: yes (the false-taxonomy guard).
15. Are mentor, coach and consultant relations between persons, not positions? Default: yes.
16. Is the hiring pipeline an annotation on a hiring task whose subject is a vacant position? Default: yes.
17. Is a job description a template (thing's `template`, `derived_from`) with changes offered? Default: yes.
18. Does the calendar supply a named calendar system, a working calendar and work periods as a reading? Default: yes; depends on the time domain.
19. Does a public-office history survive an occupant's erasure request? Default: the fact stays, the identity link detaches only on an authority's order (X1).
20. Standing judge post and per-case seat as two positions in two contexts? Default: yes; whether a standing office exists with no case stays the judicial-office Q1.
21. Does a capacity (plaintiff, assigner, buyer) stay a relation unless it passes the graduation test? Default: yes.
22. Is compensation a rule on the position (pay band) or the person? Default: ask; no cost.

### Contradictions reported, not resolved
Role as group versus position; the Decided staff identity versus per-employment lifecycle; what delegate delegates (role, rule or bundle); the decided design/engineering separation versus the false-taxonomy caution; the legacy contract losing context and interval; other domains crediting this one with processing it lacks; "shift" as pattern, instance and assignment; attendance vocabulary stated three times; `recruit` naming two facts; the synthesis's omission of the organization research. Full list: the research's Contradictions found.

### Next Steps
1. The owner answers questions 1 to 3 in sitting 3 of the synthesis's decision graph, after GR.1 to GR.3, before GR.8 and TA.7.
2. After the answers, write the domain statement into [role.md](role.md) (Model, Policies) and replace the two stale Open questions of [edges/group](edges/group/group.md) with the position's context.
3. Convert [protocol/dt-uuid.kh](protocol/dt-uuid.kh) to the thing's identity once the accessor name (question 4) is ruled; harvest `ParentID` and `departmentID` from the legacy records, then retire the `internal/` and `services/` residue.
4. Ask for a delegate research session: three domains' defaults (X3) lean on it and the role's authority row is Explored until it exists.
5. Ask for case and judicial-office owners to read question 20 before judicial-office is copied as a standing office.

## Related Artifacts
- [`role.research.001.md`](role.research.001.md) — Research 001: what the domain is for, kernel and pluggable, rival models, edge mapping, tests and owner questions.
- [`role.changelog.md`](role.changelog.md)
- [`README.md`](README.md)
- [`../staff/staff.handoff.md`](../staff/staff.handoff.md)
- Per-edge doc: [`edges/group/group.md`](edges/group/group.md) — role↔group label edge; overlap with the group parent edge flagged there.
- Memar `agency.md`

## Notes
- Provenance: Organization ideas backlog → Agency + third-pass role≠tool + fourth-pass Telegram bullets (2026-09-16/17 migration).
