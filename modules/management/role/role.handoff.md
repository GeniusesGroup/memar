# Role Handoff

## Topic & Purpose
Agency-based staffing model for human/AI roles; role ≠ tool knowledge; Telegram-derived hiring and role-design bullets (architect hiring, design vs engineering, cross-disciplinary literacy, service segmentation, tool ≠ architecture, mentor/coach/consultant). Migrated from the Organization ideas backlog second/third/fourth passes (2026-09-16/17).

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

## Related Artifacts
- [`README.md`](README.md)
- [`../staff/staff.handoff.md`](../staff/staff.handoff.md)
- Memar `agency.md`

## Notes
- Provenance: Organization ideas backlog → Agency + third-pass role≠tool + fourth-pass Telegram bullets (2026-09-16/17 migration).
