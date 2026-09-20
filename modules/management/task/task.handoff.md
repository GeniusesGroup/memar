# Task Handoff

## Topic & Purpose
Task as the primary organizational unit (replacement for commit messages), Decision-as-label, Change Set association via linked content revisions, and org process items that fit task/knowledge work (Documentation/Practice/Agent Configuration, AI-agent guidance as practices, definition-first classification, curated definitions). Migrated from the Organization ideas backlog (2026-09-16) and third-pass (2026-09-17).

## Status
Active — Task / Change Set decisions decided; canonical decomposition and full Task edge taxonomy still open.

## Decisions

### From Organization ideas backlog — Task

- Task is the primary organizational unit and the replacement for the commit message: a Task hosts discussions, questions, objections, alternatives, evidence, decisions, outcomes, and the content revisions it produced — hundreds-times richer than any commit message, nothing lost. *(decided)*
- Task is the root node; Decision is a label/state on a Task (or sub-task) indicating the kind of want it carries — Decision is an outcome of Task, not a root concept. *(decided)*
- The chat records of this kind of session are themselves Tasks (the org's task-management data store); discussion data belongs *next to* the content it changed, as links. *(decided)*
- Task is not primitive: modeled as an additive entity over **Group** — participant/member management belongs to Group, not Task; Task itself is also a Content (needs human text, images, audio). *(decided — Group is the org repo's own concept; no Memar-side owner)*
- "Change Set": where simultaneous changes must stay associated (Decision-42 touched RFC-A/B/C together), the association lives as the Task's linked content revisions — Commit Message and central Snapshot removed, the co-change link preserved. (The literal name never entered any doc; the org can keep or rename it.) *(decided)*
- A GitHub-Issues-style GUI for tasks is optional and must not influence the model. *(decided)*
- "Task History > Commit Message" in essentially all cases; diffs, not snapshots, are what humans and AIs actually query. *(decided)*
- Whether the org truly needs a global "state of the knowledge graph at time T" entity, or it is always reconstructable by linking involved contents to the Task (making the Task *the* commit message); in a non-file model even the validity of asking is doubted. *(open)*

### Third-pass items (org process — task/knowledge work home)

- **Apply the three-way separation to every org knowledge artifact: Documentation / Practice /
  Agent Configuration.** Org truth lives in docs; org how-to lives in practices; per-agent/platform
  wiring lives in agent configuration — never mixed. Acceptance test from the session: if a practice
  would still be worth keeping when no AI agent exists, it is documentation; if it exists only to
  satisfy one agent's limitations, it is agent configuration and must not enter the docs. *(decided
  direction; recorded in memar as an open item — the org should adopt it as standing policy for its
  internal playbooks and its AI fleet configuration)*
- **Model the org's AI-agent guidance estate as practices, not "instructions".** The org runs many
  agents across many platforms; platform categories (instructions/skills/memory) will re-appear and
  re-fragment. Name org guidance as practices with explicit scope (global vs domain-specific), keep
  the global set minimal, and extract focused practices instead of growing a monolith — the
  instructions-bloat failure (5k→12k words) is the anti-pattern to design against from day one.
  *(decided direction in the sessions; candidate org infra rule)*
- **Definition-first classification for org record-keeping.** When the org creates artifact
  categories (document types, templates, record classes), each category is justified by a definition
  before it exists as a label, and every existing classification is treated as a hypothesis
  requiring justification — the taxonomy-first habit of industry tooling is exactly what memar's
  classification principles reject, and the org's document management will face it immediately.
  *(direction; operationalizes modeling.md for org records)*
- **Curated definitions over volume for everything the org feeds its AIs.** The org's AI-facing
  knowledge base should be definition-anchored and curated, not accumulated: precise, agreed
  definitions given precedence over training-data defaults (the mechanism sketched in memar's
  terminology document), because volume of text correlates with marketing distortion, not accuracy —
  the practical residue of the channel's AGI/ambiguity discussion. *(direction; candidate org
  knowledge-base design rule)*

## Open Questions

From the Task section *(open)* bullet above, plus consolidated list items about Task:

1. Canonical definitions of Content, Task, Timeline, Group and their minimal decomposition (is Timeline primitive? does Task decompose into Group + Content + Relation + State + Permission?).
2. Full Task edge/label taxonomy including Decision-as-label semantics.
4. Logical-snapshot tooling, and whether any real need for global-state entities survives.

## Related Artifacts
- [`README.md`](README.md)
- [`edges/task-concept.md`](edges/task-concept.md)
- [`../group/README.md`](../group/README.md) — Task-is-additive-over-Group also recorded there
- [`../vocabulary-discipline.handoff.md`](../vocabulary-discipline.handoff.md)
- [`../../knowledge/content/content.handoff.md`](../../knowledge/content/content.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Task + Change Set; third pass Documentation/Practice/Agent Configuration items (2026-09-16/17 migration). Session direction accepted task as home for the org-process third-pass bullets listed above.
- Long brainstorm arguments for Task History > Commit Message, Decision-as-label, Change Set under Task, and global-snapshot open question are preserved in full in [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Git, filesystem, and organizational knowledge); structured outcomes remain in this handoff. Documentation facet / Explanation vs Practice naming dialectic (Memar-side) is in the same handoff (Discussion — Modeling method, entry points, and documentation facets) with org implications already under third-pass bullets above.
