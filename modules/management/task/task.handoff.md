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

### Does the Task need more of `record` than the reference to an address?
- State: "How a Task is stored" in `task.md` says a Task is a node of the record contract and then states the Task's node as parts under domain keys (`task`, `timeline`, `group`, `request-head`), `labels` that classify nodes, the encoding of a part, and the revision of a content by moving a `timeline` entry in one batch under an expectation. The owner ruled on 2026-10-24 that the link of Task, timeline and Request to `record` is only the reference to an address that the memory module offers ([Memory Address](../../computer/memory/address/address.md)), since `record` is a pluggable capsule and a kernel module depends on nothing of it ([Kernel Neutrality → The rule](../../knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). A part under a domain key, a label and `scan` by label are only `record`'s, so this section states more than a reference, and it is load-bearing for the task verbs; it was therefore not edited, and its link to `record.md` stays.
- Options: (1) Recommended: the section's stored shape (parts, keys, labels, encoding) moves to the pluggable `modules-plugable/management/task/`, which already holds the optional task records, and `task.md` keeps what a Task is, naming its identifier as an address by reference; cost: a rewrite of the section and of what links to its anchor. (2) The section stays and is retitled as how a project that binds work records to `record` stores a Task, stated as the composition's use of that capsule; cost: a kernel document still names a pluggable capsule. (3) The Task needs nodes, parts and labels as its own subject; then the node model is kernel and the ruling on `record` is revised.
- Anchor: [How a Task is stored](task.md#how-a-task-is-stored); the answer lands there and in the `record` capsule's documents.
- Blocks: the move of the `record` capsule to `modules-plugable/computer/memory/store/record/` and the verbs re-based on it. Assumption meanwhile: option 2, the section is read as the composition's use of the capsule and not as the Task's definition.
- Asked: 2026-10-24, Claude (task `20261024-T160312Z-25344`), for Omid Hekayati.

From the Task section *(open)* bullet above, plus consolidated list items about Task:

1. Canonical definitions of Content, Task, Timeline, Group and their minimal decomposition (is Timeline primitive? does Task decompose into Group + Content + Relation + State + Permission?).
2. Full Task edge/label taxonomy including Decision-as-label semantics.
4. Logical-snapshot tooling, and whether any real need for global-state entities survives.

### The twelve Task rules, and what of `process/session` belongs here
- State: the twelve rule folders stand under `modules-plugable/management/task/rules/` — a second placement for this module's name, with no main document and no manifest — while this handoff and `task.changelog.md` record them as Task's rules. Owner 2026-10-20: after full migration of services, `modules/process/session` is **deleted**; the word *session* in modules is only the OSI Session layer (`modules/net/protocol/osi_5-session.kh`); `memar task` verbs go too. Migration task `20261020-T131909Z-22300` carries the inventory and destination table (opened when Decision 4 of `20261019-T133400Z-4624` had assumed a session that did not exist).
- Options: (1) move the twelve rule folders into `modules/management/task/rules/`, the role folder of this module — the reading the owner's words favour, since the rules state what a Task is; (2) make them a pluggable capability with its own name, main document and manifest.
- Anchor: `modules-plugable/management/task/rules/`; deletion of `modules/process/session` after migration.
- Blocks: implement `20261020-T163035Z-14292` (table + task-id); then naming/git-shelf `20261020-T180133Z-19180`; then scripts `20261020-T163034Z-14292`.
- Asked: 2026-10-19, by task 20261019-T133400Z-4624; deletion end-state ruled 2026-10-20 in coordinator `20261020-T131818Z-22300`.

## Khayyam conversion (2026-10-03)

### Status
Protocol layer converted. [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) is the only source in the domain that carried declarations, and it **accepts** against the Khayyam frontend (verified against a root where both `org/…` and `memar/…` resolve).

### Decisions

- **A task's identity is the thing domain's identity.** *(Decided.)* The Go source wrote `type UUID group_p.UUID`, a named-type re-declaration two links from the owner. Khayyam has no alias form, so the file includes `ThingUUID` and `Array_ThingUUID` from `modules/identity/thing/protocol/dt-uuid.kh` and declares no `TaskUUID`. Sixth domain to reach this conclusion (`user`, `time`, `uri`, `calendar`, `group`, now `task`); `department`, `staff` and `shift` reach it in the same wave. The Go comment — "It is base on group to support some group rules e.g. invite, …" — is the reason this domain must *not* mint its own identity, and it now reads as an argument for the opposite of what it was attached to.
- **`Field_TaskID` + `TaskID`, `Field_TasksID` + `TasksIDs`.** *(Decided.)* The Go already used the `_ID` spelling, so the sweep's `Field_X`+`X` rename does not apply here; the plural accessor's `TasksIDs` is the corpus spelling (`EdgesIDs`, `EstateIDs`, `LabelsIDs`). Result parameters `t` and `a` follow `Field_EdgeID` / `Field_EstateID`.
- **`edges-loop/status/task-status.kh` was left unconverted.** *(Decided.)* It holds four `iota` label constants and no type, function, or interface — vocabulary, which is data. Same disposition as the other label-only edge files in this tree.
- **`_import/task/{init-gui,init-server,module}.kh` were left unconverted.** *(Decided.)* `_import/` is the legacy `package org` / `libgo/protocol` shim tree; its declarations re-state identities `protocol/dt-uuid.kh` owns, and no `_import` file has been converted in any wave.
- **No `TaskModel` was written.** *(Decided.)* There is no Go `Model` interface in the domain and no requirement beyond identity to compose one. [`task.md`](task.md) and this handoff both say "Task is not primitive: modeled as an additive entity over Group" and "Task itself is also a Content" — two different requirements, one of which points at a domain (content) that has not declared a model this file could compose. Writing `TaskModel` over identity alone would be the empty extension point rule 6 names; writing it over `GroupModel` + `TextModel` would ratify an unratified decision. See Open Questions.

### Open Questions raised by the conversion

- **`TaskModel`'s two candidate requirements are both unratified, and they point at two different domains.** "Additive over Group" says `GroupModel`; "also a Content" says a content model. `modules/knowledge/content/` has no `protocol/model.kh` in the tree, so the second requirement has nothing to name. Deciding `TaskModel` is blocked on a decision this domain has not made, not on a missing declaration.
- **`edges-loop/status/task-status.kh` is a status set in the right folder already, but the mechanism is open.** `Status_ReadyForDevelopment / Status_InProgress / Status_Close / Status_Success` sits under `edges-loop/`, which the migration map's Phase 0 review lists as the correct home for statuses, so unlike several `knowledge/question` edges this one is *not* misfiled. What is open is whether these are statuses at all: [`../group/group.md`](../group/group.md) unresolved #1 (static embedding vs runtime type upgrade) and [`edges-loop/task-labels/task-labels.md`](edges-loop/task-labels/task-labels.md) ("Scrum/XP/rejection states: recorded as *labels*, not core statuses") both bear on it. If they are labels, the file belongs with the other label vocabulary and not as a status set.
- **`edges-loop/table/table.md` and `edges-loop/task-labels/task-labels.md` document something the folder cannot hold.** Both record, from their own sources, that a board is "a visual aid … in GUI" and a *projection* (projection ⊘ domain model). `table.md`'s own Model line says "Not a domain edge … no candidate edge". An `edges-loop/` folder for a non-edge is the folder-kind error the Phase 0 review is about; the fix is a move, which is not this conversion's to make.
- **The `Minimum`/`Expected`/`Maximum` triple is now claimed twice in the corpus.** [`../group/edges/membership-term-member_limit/protocol/data_model.kh`](../group/edges/membership-term-member_limit/protocol/data_model.kh) was converted this wave to `Observer_GroupMemberLimit_Minimum` / `_Expected` / `_Maximum`, because `modules/knowledge/knowledge_unit/edges/duration/protocol/data_model.kh` declares the identical three method names over `duration.Second` and the bare names are therefore ambiguous. Whoever converts knowledge_unit must take the qualified spellings or recognise the two records as one abstraction.
- **`Field_TaskID` unblocks two other domains, and both are outside this one.** `modules/identity/thing/edges/criterion/protocol/{data_model,storage}.kh` both import `task_p.Field_TaskID` / `task_p.UUID` and are the reason this file was in the blocker list; they now have the name to import. `modules/knowledge/text/ui/text/protocol/gui-widget.kh` needs `comment_p.Field_CommentID`, which is not this domain's to provide.

### Related Artifacts added
- [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) — the identity surface; includes the thing domain's declaration.
- [`../group/group.handoff.md`](../group/group.handoff.md) — the same identity conclusion reached one domain up, and the record of why `rights/contract` and `rights/case` no longer reach the group through an alias.

## Research 001 questions and next steps (2026-10-15)

### Status
Proposals only, from [task.research.001.md](task.research.001.md) (eleven scenarios, a five-element kernel, four rival models, a mapping of every edge folder, twenty test scenarios, twelve contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above are not re-argued.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](task.research.001.md#open-questions). Ordered by what they change.

1. **What is the node: the declared intent of a unit of work, or a unit of work required of someone?** Default: the declared intent; duty and assignment are relations. Blocks: the definition in [task.md](task.md), M4, any `TaskModel`.
2. **Does a task have a team from birth, or acquire one when people join?** Default: acquired. Blocks: [group.md unresolved 1](../group/group.md#unresolved-questions), `TaskModel` over `GroupModel`, the case premise.
3. **Is completion propagation kernel or pluggable; may a parent end with open children?** Default: pluggable; only with an explicit outcome per open child. Blocks: the completion module, the seed's automatic-close example.
4. **Several parents allowed, and is `blocks` separate from containment?** Default: several parents, acyclic, two relations. Blocks: the edges/task split, `Move`, the cycle guard.
5. **Is a reopen a state change or a new task that supersedes the first?** Default: a new task that supersedes. Blocks: the lifecycle, the ticket model.
6. **Must an assignee accept; does silence mean accept?** Default: accept required; silence is not acceptance; delegate owns it. Blocks: the assignment model.
7. **Do participant labels dissolve into Group, Role and delegation, with the assigner as the creator of the membership edge?** Default: yes. Blocks: retiring the four ownership task-relation files.
8. **What is the outcome vocabulary?** Default: completed, partial, rejected, cancelled, abandoned, separate from lifecycle position. Blocks: `Success`/`Close`, partial completion.
9. **Where do task statuses live (catalogue R4)?** Default: `status/<name>/` for lifecycle, `edges-loop/` for classification. Blocks: the folder of task-status.kh and the Scrum/XP vocabulary.
10. **Is a delegate that is a thing (software agent, machine) first-class, with accountability staying with the principal?** Default: yes. Blocks: skill-matching for non-humans.
11. **Who may see which task?** Default: participants see their tasks; outsiders see relayed outcomes. Blocks: the ticket model, the authorization versus access-control overlap.
12. **Where does the merged campaign capability live; does `settlement-reference` yield to budget?** Default: `modules-plugable/management/campaign`; budget keeps the one relation. Blocks: moves and deletions of four edge folders.
13. **Does `Progress` leave criterion?** Default: yes, as discovered data. Blocks: criterion conversion.
14. **Do `project`, `shift` and the stage vocabularies become classifications or pluggable vocabularies of a task?** Default: yes. Blocks: the project and shift folders.
15. **Is the decision a label on the task or a node the task produces?** Default: a label, with `changes` read directly; a node only if a decision needs its own lifecycle. Blocks: the shape of the Change Set edge.
16. **May a task be created in another organization's space?** Default: no; cross-organization work is participation. Blocks: ticket and exchange models.

### Next Steps
1. Owner reviews research findings 1 and 2 and answers questions 1 to 3 first; they change what the domain is.
2. Done on the defaults, still Tentative (2026-10-18): [task.md](task.md) now defines the node as the declared intent, states what Task owns against content, text, timeline, group, delegate, rule, label and status, and maps every Memar session term to its Task term. If the owner answers questions 1 to 3 otherwise, the definition and the Assign task rules are revised.
   - New open item: where the queue and claim capability lives (no pluggable holds it yet).
   - New open item: whether Blocked is stored or derived.
3. A session fills [Placement](../../modules.md#edge-folder) and Open questions on the six edge folders that have none (advertisement, campaign, marketing, settlement-reference, and the loop stubs), using the research's mapping as a reading list; no folder moves before the owner answers questions 12, 14 and catalogue R2/R4.
4. Draft the three kernel edge documents (`part_of`, `blocks`, `changes`) as candidates once questions 4 and 15 are answered; do not write a `TaskModel` before question 2.
5. Resolve with the group domain whether roles-in-a-task are Group membership with a Role (questions 2 and 7), and with the delegate domain who owns acceptance (question 6).
6. Reconcile the contradictions listed in the research (notably the `Blocking`/`block` collision, the marketing edge directions, and the duplicate budget relation) in the documents that own each side.
7. Review the project-management and workflow-modeling literature the seed RFC names as possibly worth reviewing; the research did not consult it.

## Research 002 questions (2026-10-18)

### Status
Proposals only, from [task.research.002.md](task.research.002.md): what outside work on source control, context engineering and multi-agent coordination says, set against this domain. Every item is **Tentative**; nothing is Decided and [task.md](task.md) is unchanged. The source-control article does not discuss tasks or bounded context; it supports only the properties (online, immutable addressed changes, derived views).

### Open Questions raised by the research
Numbering continues Research 001's; the full text and defaults are in the research's [Open Questions](task.research.002.md#open-questions).

17. Is a reader's context a derived view of the Task graph, assembled by a pluggable capability? Default: yes, home undecided.
18. Is a summary a content that `summarizes` a kept span, never the record? Default: yes.
19. What does a child inherit from its ancestors by walk? Default: decisions, checks, constraints, references; not text.
20. Does a content have one write holder at a time? Default: yes.
21. Do events and revisions have a canonical addressed append-only order? Default: yes.
22. Does `changes` point at content revisions or paths? Default: revisions.
23. Concurrent change to one content: lock or optimistic with a conflict child Task? Default: optimistic.
24. Is review attached to the intent, and are approval rules conditioned on the kind of change? Default: yes.
25. Does a parent read a child's trace or only its hand-back? Default: hand-back.
26. Where does how-agents-run live, and what does the Task give it? Default: its own concept; the Task gives the view.

### Revised after an independent review (2026-10-18)
The addendum in [task.research.002.md](task.research.002.md#addendum--independent-review-by-a-stronger-model-2026-10-18) changes the defaults of 17, 18, 19, 20, 21, 23 and 24 and adds 27 to 34. The two corrections that matter: 23's default (optimistic) contradicted the owner's decided single-changer direction and is replaced by it; 18 (a summary) belongs to content and conflicts with content's question 16. New: 27 a `#123` in text is content's mention, backlinks derived; 28 following a reference gives a card; 29 a Task whose binding set exceeds a reader's bound is decomposed, never ranked down; 30 a hand-back lists the decisions taken; 31 an optional WIP limit on the claim; 32 subscription is the notification domain's and the inbox is derived; 33 an agent's chat is a run on a Task; 34 a view cites items at a revision within a run. Suggested order for the owner: 33, 17, 27, 20, 23, 29, 22, 21, 19, 30, 28, 25, 24, 31, 32, 34, 18, 26.

### Owner's answers to the review (2026-10-18)
Recorded as the owner stated them; the owner said several remain unclear to him, and those stay open.

- **Q33 (a chat is a run on a Task): not accepted as framed.** The chat is a timeline that holds contents; its relation to a Task is not the concept of a run. *(owner)* The relation between a chat's timeline and a Task is therefore open again.
- **Q27 (a reference in text is content's mention): agreed.** *(owner)* Beyond a mention, two Tasks may be related by an edge, and the reason can be other than a dependency: for example, the two Tasks ask for the same thing.
- **Q18 (is a summary acquired content): no.** A summary is discovered by nature, from related content. *(owner)* This matches content's question 16 and withdraws the addendum's "acquired when someone made it".
- **Q29 (decompose, never rank out): agreed in part**, not yet clear to the owner.
- **Q17, Q23, Q30 and Q19, Q26: no position yet**; unclear to the owner. Q23 stays under the decided single-changer direction of 2026-10-05 until he says otherwise.
- **Thinking text of a participant: stored, on a different edge from the discussion, and no other participant is obliged to read it.** *(owner's direction, to be confirmed against the independent opinions)*

New open question raised by the owner: **when a user is added to a Task to ask their opinion, is that a new Task, or may several participants, human or AI, work on one Task, each mention changing that participant's own cognitive path?** The owner's leaning is the second, with thinking kept on its own edge.

### Second opinion (2026-10-18)
See [task.research.002.md](task.research.002.md#second-opinion--a-fresh-agent-positions-formed-before-reading-the-addendum-2026-10-18). Proposals, all Tentative: a new person on a Task is a participant unless the ask has its own check, its own holder by delegation, its own view, or its own writes (then a child Task); a mention changes the mentioned participant's path and never the Task's; thinking text goes in the thinker's own timeline, related to the reply it produced, with the rule that nothing binds unless it is recorded as a decision, question, change or reply; a chat is a timeline and a Task relates to contents, not to a timeline (question 33 replaced by: is the relation of a Task to a timeline derived from the contents related to it?); a summary is discovered and cached with its inputs; `same_ask` is a candidate fifth Task relation; siblings' decisions reach a child through the parent; the claim rule warns and does not refuse; a decision must be an addressable item (Research 001 question 15). Open for the owner: those six, and the plain-language Q17, 19, 23, 29, 30.

### Owner's rulings, the second round (2026-10-18)
Recorded as the owner stated them. They supersede the parts of the research named after each.

- **One timeline per Task, used by every participant.** A participant may add any number of texts to a content in that timeline, related by edges of different kinds and for different reasons, some of which only the author knows and uses on its way to the Task's output. Thinking text is such a text; no other participant is obliged to read it. *(owner)* Supersedes the second opinion's section C (thinking text in the thinker's own timeline) and D (one timeline serving several Tasks, a Task having parts in several chats), and the addendum's Finding 12 and Proposal 18. The owner added that he does not want the Task concept fitted to today's AI chat tools, whose per-agent chat shape he criticises.
- **Nothing binds unless recorded as a decision, question, change or reply.** Agreed. *(owner; it is also what Memar's Cognition already says: externalize session state into shared artifacts.)*
- **`same_ask` is accepted as a Task relation.** *(owner)*
- **Question 19 (what a child inherits): no structured inheritance.** Each Task is independent and no field or structure is added that forces decisions and checks to be written for children. One important process of doing a Task is to search for leads with retrieval methods such as BM25 across all content the worker can reach, not only the Tasks related by an edge. *(owner)* Supersedes the addendum's rings and Proposals 11, 12 and 14, and the second opinion's answer to Q19.
- **A Task that will change a content is first related to it by an edge**, so everyone knows which Tasks intend to change or have changed it; at its end the edge is removed or becomes another edge. The owner calls this like a commit but more complete, and better than the source-control article's idea, which the article only hints at without describing. *(owner; the name, and whether it also serializes writers, are open. This is a candidate answer to question 23, not yet that answer.)*
- **Question 17 and the context: the only thing always in a worker's context is the first content of the Task's timeline, or a chosen list, which is something like a plan and says the path of the work. The worker loads anything else by searching, through a service like `memar content`.** *(owner)* So the derived view is a plan plus search, not a walked graph.
- **Cache: do not lock the model to today's AI models.** The way of caching is to be changed in whole. *(owner)* Findings 4 and 13 of Research 002 and Proposal 5 describe prefix reuse for today's models and are not requirements of the Task model.
- **Task is wide.** A user's complaint against the organization and an inner partition wall on the second floor are Tasks as much as a code change, and the model must cover all such needs without being limited to AI workers. *(owner)* [task.md](task.md) now says so.
- **Question 23, answered: no write ordering is forced by the edge.** When more than one Task intends to change one thing, their changes may be coordinated by a service like a database transaction, but nothing requires the writes to be coordinated at the same moment; the coordination may be conceptual, the two Tasks being related and done together. So the intent-to-change edge announces, and a separate edge relates two Tasks conceptually. *(owner)* This replaces the single-changer default for Task-level coordination in Research 002; content's own decision of 2026-10-05 on one changer per entity stays content's. The conceptual relation between two Tasks is `same_ask` when they ask the same thing; whether a wider "done together" relation is a second edge or the same one is open.
- No position on the remaining questions; he will do whatever is needed.

### Owner's answers to the six questions (2026-10-18)
- **Search belongs to text.** Task and content understand nothing of text, so finding a word or phrase is text's. The service that loads what was found into a worker's context has no domain yet; the domain is created first, and the question is left until then. *(owner)*
- **New Task or participant:** agreed for now, with the three questions (own done-or-not-done state, own acceptor, own check). Rules must stay easy to create, amend and remove; this one may be amended. The Task rules from this work are kept under [modules-plugable/management/task/rules](../../../modules-plugable/management/task/rules/README.md). *(owner)*
- **Duplicates and more relations:** two or more further Task-to-Task edges are certain: a Task that does more than the Task it closes, and a Task closed because a new decision conflicts with an earlier one. Names open. *(owner)*
- **A decision is recorded either way:** a documentation requirement is used as a text template, and a content may also be joined to its text by an edge directly. *(owner)* The question whether a decision is a marked text or an item of its own is therefore answered as "both ways are right".
- **A Task too big for a worker is split.** Certain. Tasks may last as long as the organization (the vision of the organization may have hundreds of Tasks over its life). *(owner)*
- **Name of the intent-to-change edge:** no idea; the owner will leave a todo in the code if one comes. *(owner)*

### Owner intake — Session versus Task span (2026-10-20)
Recorded from the coordinating chat of task `20261020-T131818Z-22300`. Sitting 8 (`20261018-T203922Z-11220`) took a thin batch yes on 2026-10-20; see the next section for what became Decided and what stayed open.

- **No work-item *session* outside OSI.** Owner 2026-10-20: Memar's process "session" was Task misnamed; the word *session* in modules remains only for the network Session layer (`modules/net/protocol/osi_5-session.kh`). `modules/process/session` is deleted after service migration; `memar task` verbs go too. Until that migration finishes, the tooling is a temporary adapter — not a second concept.
- **One Task holds its whole process.** Designing the plan, evaluating it, and changing the plan are steps of the same Task — not separate Tasks/sessions. Mixing the status of a document the Task changes with the Task's own status produced many sessions for one ask; that is a defect to correct in practice and in the conversion of task records after terms settle.
- **Independent asks stay separate and linked.** Work that must stand alone is its own Task, and those Tasks must be connected (`part_of`, `blocks`, or further relations the owner accepts). Several independent asks must not be stuffed into one Task.
- **Task records not yet pushed.** Live and archived task folders may be rewritten by a script once terms settle (new commit or history rewrite — owner chooses later).
- Follow-ups queued from that chat: migration `20261020-T131909Z-22300`; filesystem/edge storage `20261020-T131910Z-22300`; content primary vs transcription `20261020-T131911Z-22300`.
### Owner accepted sitting-8 defaults (2026-10-20)
*(coordinator chat; thin consent first, then four clarifying answers the same day after a conflict check.)*

**Decided** (batch yes, no conflict with prior owner text): TA.1, TA.2, TA.3, TA.4, TA.5, TA.6, TA.7, TA.8, TA.9, TA.10, TA.11, TA.12, TA.13, TA.14, TA.16; TA2.21, TA2.22, TA2.24, TA2.25, TA2.26, TA2.27, TA2.28, TA2.31, TA2.32. Defaults as in the sitting-8 brief.

**Clarified and decided (owner answers after conflict check, same day):**

1. **"Both ways" for text (2026-10-18 clarified) plus TA.15 (same day).** Text may be plain or templated. **Decision is a label on Content**, reachable by a shortcut edge from a Task; text accompanies the decision. Not a label on the Task node itself.
   - **Decision (TA.15):** label on **Content**, shortcut edge from a Task; text (plain or templated) accompanies it. Bare event_is of an invoice on a timeline is not the decision path (	imeline/edges/event/event.md Reason classifies appearance, not Task intent).
2. **TA2.17 — out of Task.** What sits in a worker's model context is the AI / how-agents-run domain's, not Task's. A limited window or cheap cache may vanish someday; then the question changes again. Irrelevant detail must move to its owning domain so Task's path stays uncluttered. *(owner)* Sitting-8 graph-view default is dropped for Task.
3. **Concurrent work on one content — Task should not own it.** Knowing that two Tasks aim at similar work (GitHub-style `#12345` references) matters, but whether that is Task–Task or a content record on a timeline with an edge is undecided. Owner leaning: Task must not be entangled with the content domain, so Task preferably knows nothing of concurrent content writers; content/timeline own that. *(owner; Tentative on the edge shape)* TA2.20/23 as Task kernel questions are withdrawn from Task.
4. **No *session* concept outside the network Session layer.** Topics hung on Memar's process session are misplaced and must move. The owner agrees the `memar task` command surface should go too. The only rightful use of the word session in modules is the OSI Session layer (`modules/net/protocol/osi_5-session.kh`). After its services are fully migrated, `modules/process/session` is deleted. Two independent concepts sharing the word "session" is rejected. *(owner)*

**Already standing (unchanged):** TA2.18 summary discovered; TA2.19 no structured inheritance; TA2.33 chat is not a run on a Task.

**Still Tentative:** TA2.29, TA2.30, TA2.34. TA.15 Decided (Decision label on Content + Task shortcut + text).

## Critique as a content on the timeline (2026-10-30, Tentative)
Task 20261026-T200844Z-21460. The owner's observation of 2026-10-26: many Tasks exist only to critique the output of one part of another Task. Tentative until the owner reads the digest; the rules are in [the Task rules](../../../modules-plugable/management/task/rules/README.md) (`critique-is-a-content-on-the-timeline`, `a-reply-names-what-to-read`, `an-ask-is-addressed-and-answered`, `a-reply-chain-ends`, `a-call-lists-what-the-callee-reads`, `a-record-is-a-message-on-a-task`) and what the task asks of the domains that keep texts, and the migration, are in [the pluggable task module's document](../../../modules-plugable/management/task/task.md).
- **The model.** A critique of a Task's output is a content on that Task's timeline, called for by a content that lists what the critic reads; the critic answers with a content that replies to the one it examined; an ask to act again is a reply addressed to the role that made it; a reply names the numbers of the contents it asks to be read, each with a reason. A critique that has its own acceptor or check, or that judges material no Task made, stays a Task.
- **What is strong in the owner's model.** It leaves no Task that carries nothing (the three questions already say so); the critique, the answer and the rework stay on the one timeline where their subject is, so no second record has to be joined to the first; the reply edge is a provenance a chat cannot give; naming numbers with reasons keeps a late or fresh agent's reading small; it applies the rule that nothing binds unless recorded.
- **What was missing, and what the rules add.** (1) Who may reply and who is bound: anyone on the Task may reply, only the addressee's own act answers an ask, silence is not acceptance. (2) How a reply addresses a content: by the `reply_to` edge, never by the words; a number is only for the reader, and it must be stable, so it is assigned at placement and never reused. (3) How an agent is called: by an ask to a role, with the contents and documents it reads and the three facts of the model rule; the original agent may be gone, so the ask is to the role and not to a living agent. (4) How a chain ends: by a reply that asks nothing, by the owner, or, after the limit without new ground, by a question to the owner. (5) The critic's independence: the call lists what it reads, and where visibility is not yet held by the system, a critique that must not see another is a Task of its own. (6) What a critique changes: no Status; the same request and check make another round, added work a child Task.
- **Not settled by the rules.** The numbering of placements is the timeline's: it is a position the timeline domain may add to placements ([Timeline Handoff](../timeline/timeline.handoff.md)); the edge that names an ask's addressee, and whether it is the content domain's or the task module's, is open; the limit of rounds is a parameter whose value is a proposal.
- **Owner's corrections of 2026-10-30.** (1) A design for the Task domain is made with no file or directory in mind; a requirement about where a text is kept or how it is joined is asked of text, content and timeline, and the folder shape first proposed was wrong and is withdrawn. (2) The migration is done by creating tasks: each old handoff, alone or with related ones, becomes tasks that take queue statuses, and its text becomes content on their timelines. (3) It waits until the series of task 20261023-T074642Z-5420 has settled where tasks and texts are kept, so that no domain is rewritten against files. (4) Handoffs are no longer written as documents: the rule is that a task is created quickly (task 20261030-T073507Z-6324 first), the existing handoffs are removed sooner, and the way of making a handoff becomes a template of a descriptive message on a task. The handoff was an example: every facet of the documentation module becomes a template for writing a text and nothing more, mostly used on task timelines. (5) Tasks in progress finish as they are, so their chats meet no sudden change; nothing is stopped, and only queued tasks not yet started are held or reshaped.

## Tentative: several humans and several agents at once (2026-10-24)
Task 20261024-T052152Z-22628. Tentative until the owner reads the digest; the memory-port programme (task 20261022-T185903Z-15504 and its queue) re-bases this module's files, so each item below that touches code waits on the programme task it names, and none edits what the programme is changing now.
- **Collisions.** A plan declares the files it writes in a key `Writes` (path globs); `claims` and `claim` refuse a task whose `Writes` overlap a task that is Active or claimed; a task with no `Writes` is treated as writing everywhere and runs alone. Worktree per task and a merge protocol are a design task, queued after the key exists. Two races are closed by small implement tasks: a lock in `changelog-append`, and `content write --expect-hash` (refuse when the file is not the one read).
- **Participants.** An agent session is `agent:<model>/<task-id>`; the claim records it in place of host and pid. Roles wait on the Request and identity work.
- **Dispatch.** Memar starts no agent. The delegating agent runs sub-agents one at a time; two at once only for tasks whose `Writes` are disjoint, and with the owner's standing permission, given 2026-10-25: sub-agents may run in parallel when the tasks' Writes are disjoint (read-only panel agents need no Writes).
- **Review.** A newly started critique agent per task; the decisions digest is the owner's one reading.
- **Where work runs and what stops for the owner (owner's ruling, 2026-10-24).** Default: a sub-agent on the strongest usable model, its questions answered by the delegating agent from the documents and a second opinion, recorded Tentative; a new chat only for work that needs the owner during the work. A task whose work is one of the four kinds that always reach the owner (a definition other documents consume, a removal of stated meaning, a change beyond the instance, a premise the model rests on) carries the label `change-class=held`: it ends Blocked at a proposal (content and file list) in its docs/ and applies nothing; the digest lists held proposals first. Every other change is applied and listed in the digest with how to undo it.
- **Measurement.** `tasks.log` gains claim and finish events with times; a report gains a Model line and a usage line; benchmark: the same N tasks with disjoint `Writes`, run one at a time and then in parallel, compared by wall time, collisions and rework.
- **Human channel (open).** An owner's comment in the GUI (task 20261022-T193636Z-9280) must reach the agent's chat; until it exists the owner's attention is spent through the decisions digest and the questions of the handoffs. Owner attention is the bottleneck: a question is brought only after the questions-answer agent leaves it.
- **Dispatch and review, still open.** The usage limits of the agents' plans and the order of priority (the delegating agent keeps `priority` and `claims` order and stops when a runtime refuses a model), the adapter an agent runtime other than Claude Code needs (the MCP server maps verbs to tools only), and what a human approval costs the human (no measure exists; the benchmark task measures review wait).
- **Where `Writes` lives (open).** Declared file ownership is a choice a second organization could make otherwise, so its home (a pluggable coordination module, or a field of the Task node after the port) is decided by the first step of task 20261024-T161434Z-18560 before any key is added. Parallel work through `Writes` waits on the programme's P3 task; what can start now is the lock and `--expect-hash` task, the triage of the working tree, and the held mechanism.
- **Discovering and answering questions without the owner (owner's ruling, 2026-10-25; Tentative).** In a development path no question goes to a chat. A decision runs a panel: (1) three agents, started one after another, each lists the questions the decision raises from the governing documents without seeing the others' lists; (2) the deciding agent merges the lists and removes duplicates; (3) two different agents answer each merged question from the documents, each without the other's answer, giving reasons and the passage read; (4) a question both answer alike is decided Tentative with the reasons; (5) a disagreement that stays, or a question of the four always-asked kinds, is written as an entry in the handoff of the document it concerns and reaches the owner through the digest, not a chat. Cost: five to eight short agent starts per decision, run serially; worth it for a decision other documents or tasks consume, not for a choice one edit carries. A sub-agent starts no agents, so one that meets a decision ends Blocked with the decision stated, and its delegating task runs the panel. The one-at-a-time rule is kept: the panel's agents are read-only and short, so their parallel run, which the owner's pending standing permission would allow, is safe from half-made edits and costs only usage. The task-graph view and orchestrator prompt (task 20261025-T140528Z-16944) takes from here: declared writes (the `Writes` task, after its placement decision), parallel runs (one at a time until the owner's permission; read-only panels first), and this panel.
- **Open for the owner.** How the 271 paths changed in the working tree without an owner decision are to be triaged (queued as a task).

## Questions Found During a Task
- **2026-10-20 — migration `20261020-T163035Z-14292` shelf-only (answered same day).** Owner: (1) identity terminology must finish in that chat — flags/types/helpers now `--task-id` / `TaskId`; remaining help prose “session” → follow-up; (2) deep critique+rename of all Memar CLI verbs/services → `20261020-T180133Z-19180` (new chat); (3) `computer/records`→`git` and (4) `task_kind`→label → same `180133`. Scripts task `20261020-T163034Z-14292` Depends_on `163035` and `180133`.

## Related Artifacts
- [`task.research.002.md`](task.research.002.md) — outside work on source control, context and many participants set against the domain
- [`task.research.001.md`](task.research.001.md) — the conceptual research: scenarios, kernel, models, mapping, tests, owner questions
- [`task.changelog.md`](task.changelog.md)
- [`README.md`](README.md)
- [`edges/task-concept.md`](edges/task-concept.md)
- [`../group/README.md`](../group/README.md) — Task-is-additive-over-Group also recorded there
- [`../vocabulary-discipline.handoff.md`](../vocabulary-discipline.handoff.md)
- [`../../knowledge/content/content.handoff.md`](../../knowledge/content/content.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Task + Change Set; third pass Documentation/Practice/Agent Configuration items (2026-09-16/17 migration). Session direction accepted task as home for the org-process third-pass bullets listed above.
- Long brainstorm arguments for Task History > Commit Message, Decision-as-label, Change Set under Task, and global-snapshot open question are preserved in full in [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Git, filesystem, and organizational knowledge); structured outcomes remain in this handoff. Documentation facet / Explanation vs Practice naming dialectic (Memar-side) is in the same handoff (Discussion — Modeling method, entry points, and documentation facets) with org implications already under third-pass bullets above.
