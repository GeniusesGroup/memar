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

## Khayyam conversion (2026-10-03)

### Status
Protocol layer converted. [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) is the only source in the domain that carried declarations, and it **accepts** against the Khayyam frontend (verified against a root where both `org/…` and `memar/…` resolve).

### Decisions

- **A task's identity is the thing domain's identity.** *(Decided.)* The Go source wrote `type UUID group_p.UUID`, a named-type re-declaration two links from the owner. Khayyam has no alias form, so the file includes `ThingUUID` and `Array_ThingUUID` from `org/modules/identity/thing/protocol/dt-uuid.kh` and declares no `TaskUUID`. Sixth domain to reach this conclusion (`user`, `time`, `uri`, `calendar`, `group`, now `task`); `department`, `staff` and `shift` reach it in the same wave. The Go comment — "It is base on group to support some group rules e.g. invite, …" — is the reason this domain must *not* mint its own identity, and it now reads as an argument for the opposite of what it was attached to.
- **`Field_TaskID` + `TaskID`, `Field_TasksID` + `TasksIDs`.** *(Decided.)* The Go already used the `_ID` spelling, so the sweep's `Field_X`+`X` rename does not apply here; the plural accessor's `TasksIDs` is the corpus spelling (`EdgesIDs`, `EstateIDs`, `LabelsIDs`). Result parameters `t` and `a` follow `Field_EdgeID` / `Field_EstateID`.
- **`edges-loop/status/task-status.kh` was left unconverted.** *(Decided.)* It holds four `iota` label constants and no type, function, or interface — vocabulary, which is data. Same disposition as the other label-only edge files in this tree.
- **`_import/task/{init-gui,init-server,module}.kh` were left unconverted.** *(Decided.)* `_import/` is the legacy `package org` / `libgo/protocol` shim tree; its declarations re-state identities `protocol/dt-uuid.kh` owns, and no `_import` file has been converted in any wave.
- **No `TaskModel` was written.** *(Decided.)* There is no Go `Model` interface in the domain and no requirement beyond identity to compose one. [`task.md`](task.md) and this handoff both say "Task is not primitive: modeled as an additive entity over Group" and "Task itself is also a Content" — two different requirements, one of which points at a domain (content) that has not declared a model this file could compose. Writing `TaskModel` over identity alone would be the empty extension point rule 6 names; writing it over `GroupModel` + `TextModel` would ratify an unratified decision. See Open Questions.

### Open Questions raised by the conversion

- **`TaskModel`'s two candidate requirements are both unratified, and they point at two different domains.** "Additive over Group" says `GroupModel`; "also a Content" says a content model. `modules/knowledge/content/` has no `protocol/model.kh` in the tree, so the second requirement has nothing to name. Deciding `TaskModel` is blocked on a decision this domain has not made, not on a missing declaration.
- **`edges-loop/status/task-status.kh` is a status set in the right folder already, but the mechanism is open.** `Status_ReadyForDevelopment / Status_InProgress / Status_Close / Status_Success` sits under `edges-loop/`, which the migration map's Phase 0 review lists as the correct home for statuses, so unlike several `knowledge/question` edges this one is *not* misfiled. What is open is whether these are statuses at all: [`../group/group.md`](../group/group.md) unresolved #1 (static embedding vs runtime type upgrade) and [`edges-loop/task-labels/task-labels.md`](edges-loop/task-labels/task-labels.md) ("Scrum/XP/rejection states: recorded as *labels*, not core statuses") both bear on it. If they are labels, the file belongs with the other label vocabulary and not as a status set.
- **`edges-loop/table/table.md` and `edges-loop/task-labels/task-labels.md` document something the folder cannot hold.** Both record, from their own sources, that a board is "a visual aid … in GUI" and a *projection* (projection ⊘ domain model). `table.md`'s own Model line says "Not a domain edge … no candidate edge". An `edges-loop/` folder for a non-edge is the folder-kind error the Phase 0 review is about; the fix is a move, which is not this conversion's to make.
- **The `Minimum`/`Expected`/`Maximum` triple is now claimed twice in the corpus.** [`../group/edges/membership-term-member_limit/protocol/data_model.kh`](../group/edges/membership-term-member_limit/protocol/data_model.kh) was converted this wave to `Observer_GroupMemberLimit_Minimum` / `_Expected` / `_Maximum`, because `modules/knowledge/knowledge_unit/edges/duration/protocol/data_model.kh` declares the identical three method names over `duration.Second` and the bare names are therefore ambiguous. Whoever converts knowledge_unit must take the qualified spellings or recognise the two records as one abstraction.
- **`Field_TaskID` unblocks two other domains, and both are outside this one.** `modules/identity/thing/edges/criterion/protocol/{data_model,storage}.kh` both import `task_p.Field_TaskID` / `task_p.UUID` and are the reason this file was in the blocker list; they now have the name to import. `modules/knowledge/text/widgets/text/protocol/gui-widget.kh` needs `comment_p.Field_CommentID`, which is not this domain's to provide.

### Related Artifacts added
- [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) — the identity surface; includes the thing domain's declaration.
- [`../group/group.handoff.md`](../group/group.handoff.md) — the same identity conclusion reached one domain up, and the record of why `rights/contract` and `rights/case` no longer reach the group through an alias.

## Related Artifacts
- [`README.md`](README.md)
- [`edges/task-concept.md`](edges/task-concept.md)
- [`../group/README.md`](../group/README.md) — Task-is-additive-over-Group also recorded there
- [`../vocabulary-discipline.handoff.md`](../vocabulary-discipline.handoff.md)
- [`../../knowledge/content/content.handoff.md`](../../knowledge/content/content.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Task + Change Set; third pass Documentation/Practice/Agent Configuration items (2026-09-16/17 migration). Session direction accepted task as home for the org-process third-pass bullets listed above.
- Long brainstorm arguments for Task History > Commit Message, Decision-as-label, Change Set under Task, and global-snapshot open question are preserved in full in [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Git, filesystem, and organizational knowledge); structured outcomes remain in this handoff. Documentation facet / Explanation vs Practice naming dialectic (Memar-side) is in the same handoff (Discussion — Modeling method, entry points, and documentation facets) with org implications already under third-pass bullets above.
