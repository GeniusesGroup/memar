# Timeline Handoff

## Topic & Purpose
Timeline as Content's attach surface and the open question whether Timeline is primitive or a projection/composition.

## Status
Active — Content↔Timeline attachment decided; whether Timeline is an independent entity remains open.

## Decisions

### From Organization ideas backlog — Content & Timeline (timeline-related)

- Content is the org's holding domain: any piece of content is an independent unit attachable to one or more Timelines — the Twitter model (a tweet in its author's timeline, and in others' via retweet); the org equivalent: an RFC/chat in its author's timeline *and* in a project's. *(decided)*
- A repository (e.g. Memar itself) is just another Content, living in a Timeline where only designated members may add; the creation of a project is an entry-point node that thousands of other contents (tasks, RFCs) link to. *(decided)*

### Decisions taken by the memory-port design (2026-10-23)
Taken by task 20261023-T074641Z-5420 so that the first storage of timelines and placements (the task verbs and the migration) guesses nothing; each is **Tentative**, open to the owner's ruling, and says what changing it costs. The evidence is the table in that task's `docs/storage-forced-questions.md`, kept on the records branch. Questions are those numbered under Research 001 below.
- **Question 1 and the contradictions about the timeline's id and owner.** The owner's ruling that a Task, its timeline and its group share one id stands: a task's timeline is the part `timeline` of the Task's node, which holds the pointer to the current content of each name (below), and the research's default, a timeline with an id of its own and the group as its audience, is not taken for tasks. A placement names its timeline in a field holding an id, which for a task is the Task's id, so a later timeline with another id gives new placements another value and rewrites none. The domain key `timeline` is issued by this module; `task.md` says the Task's timeline is owned by content, and the key settles only where the part is stored, not who owns the meaning.
- **The group of a task and a conversation.** The change plan gives the Task and its group one id and also migrates a task's `Conversation` as its group, which many tasks share. Both hold when the Task has its own audience, the part `group`, absent at birth and written when someone joins, and the conversation is a node of its own that the Task's part names by a field. A migrated conversation takes an id derived from the old one.
- **Question 2 (identity of a placement).** A placement is a node with its own id. Its part is `placement` (question 18), holding the timeline's id, the thing placed (a content's id), the placer, the reason, the instants `placed_at` and `occurred_at`; its labels are the label of placements and the timeline's id, so `scan` by the timeline's id finds its placements. A plain edge would have to be given ids afterwards for every past placement.
- **The current plan and the current report.** The owner's "latest of its label" is held as a stored pointer and not computed, and it is kept for each content name so that any document can be revised, not only a plan or a report: the part `timeline` of the Task's node holds a map from the name of a content to the id of its current content, a new version is placed and the pointer is moved in one batch with an expectation on the token read, and the move is a change of state recorded by a Request. A projection by instant would let two agents who read the same plan each place an edited one and both win, with the earlier silently lost; the pointer makes the second fail and read again, and the rounds of a plan are its Request chain.
- **Question 3 (order).** The order of a timeline is `placed_at`, then the id. No position is stored; the timeline domain may add a decided position to new placements later and read the old by instant. `placed_at` is stamped by the composing service, not by the port.
- **Question 4 (ending, erasure).** Nothing is ended or erased in this design. An end, when wanted, is a change of a separate part `placement-end` of the placement's node, recorded by a Request like any change of state, so the part `placement` stays as written. Erasure waits for the owner's rule in [Memory Handoff](../../computer/memory/memory.handoff.md#what-is-the-retention-and-erasure-rule-for-preserved-history-and-where-do-a-records-versions-live).
- **Question 15 (closing).** Not stored. A Complete task's timeline stays open, because another round of the same Task places more contents there.
- **Question 17 (system notices).** A change of state is recorded by a Request and is not also placed in the timeline; the timeline is for discussion.
- **Question 25 (sensitivity).** The memory contract has no access notion; what a viewer may see is the authorization above it and is not stored with the node.
- **The reply order (contradiction 13).** Replies are not stored by this design; placement order is the only order.
- **Not blocking storage, left open as they stand:** questions 5 to 10, 12 to 14, 16 and 19 to 24. A node can be stored with them open; answering them adds a relation or a field beside the record.

## Open Questions
### Does the timeline domain keep its storage shape, the keys `timeline`, `placement` and `placement-end`, in the kernel module?
- State: `timeline.md` names nothing of `record`. The Tentative decisions of 2026-10-23 above, in this handoff, state a task's timeline as the part `timeline` of the Task's node and a placement as a node with the parts `placement` and `placement-end`; a part under a domain key is only `record`'s, a pluggable capsule, and the owner ruled on 2026-10-24 that a kernel module's link to `record` is only the reference to an address ([Memory Address](../../computer/memory/address/address.md)). The decisions are not load-bearing in `timeline.md`, so nothing was edited there; the sentence that the store has no access notion now names the memory contract.
- Options: (1) Recommended: the decisions stay here as the choices of the composition that binds timelines to `record`, each stated so, and `timeline.md` states a placement and a timeline's identifier as addresses by reference when its storage is written. (2) The part keys are the timeline domain's own subject and move into `timeline.md`, which would make it name `record`'s model; this contradicts the ruling unless the ruling is revised.
- Anchor: the section "Decisions taken by the memory-port design (2026-10-23)" of this handoff.
- Blocks: the first storage of timelines and placements. Assumption meanwhile: option 1.
- Asked: 2026-10-24, Claude (task `20261024-T160312Z-25344`), for Omid Hekayati.

- Whether Timeline is an independent entity at all — Task (and possibly Timeline) may be projections/compositions of more primitive concepts. *(open)*
- Canonical definitions of Content, Task, Timeline, Group and their minimal decomposition (is Timeline primitive? does Task decompose into Group + Content + Relation + State + Permission?). *(consolidated open-questions backlog #1 — Timeline half)*

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [timeline.research.001.md](timeline.research.001.md) (thirteen scenarios, a five-element kernel, six rival models, a mapping of every edge folder, eleven missing pieces, twenty-four test scenarios, fourteen contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. The settled facts above (content is an independent unit attachable to one or more Timelines; a repository is a Content in a Timeline where only designated members add) are not re-argued. [timeline.md](timeline.md) is not edited.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](timeline.research.001.md#open-questions). Ordered by what they change.

1. **Is a timeline a thing of its own, a group classified as a timeline, or only a view?** Default: a thing of its own; the group is its audience; feeds are views. Blocks: the alias-UUID conversion of `dt-uuid.kh`, `edges-loop/timeline`, `chat`, `user`, the case premise, the task's "one timeline", the group research's Q13, open question 1 above.
2. **Does a placement have an identity of its own?** Default: yes. Blocks: the shape of `event_is`, forward provenance, pin, the read anchor, correction.
3. **Who decides the order: a single changer per timeline, or the clock?** Default: a single changer; placed and occurred instants kept as facts. Blocks: content's group index and lock TODO, offline creation.
4. **Does ending a placement, a capacity, a window or an erasure delete anything?** Default: an end never deletes; a window is a read rule; erasure detaches actor and thing. Blocks: `limit_max_event`, the right to clear.
5. **Is the ordered append-only sequence one relation defined once with the account ledger?** Default: separate domains, shared correction rule only. Blocks: the ledger and placement filing.
6. **Is a pin a curation by an authority, a viewer's preference, or both?** Default: both, two relations. Blocks: `pin`, content's `widgets/pin`.
7. **Is mute a timeline relation, a notification preference or a viewer preference; may a rule override it for mandatory notices?** Default: a viewer preference; overridable by rule for a class of notice. Blocks: `mute`, `signal_preference`, the bulletin case.
8. **Who owns the read position: the timeline, or one receipts pluggable shared with content?** Default: one receipts pluggable; cursor acquired, counts discovered. Blocks: `read_until`, the modules.handoff bucket.
9. **Is the home timeline derived, and are the friendship-cycle and recommendation reasons derived or analytics?** Default: derived; recommendation is analytics. Blocks: `dt-reason.kh`, `user`.
10. **Are Private, Public, Life and Notification kinds, or consequences of audience, placer and assembly?** Default: consequences. Blocks: `user`.
11. **How is the audience attached, and who owns it?** Default: authorization owns group-scoped access; the timeline exposes `condition_is` and events. Blocks: `chat`, `edges-loop/timeline`.
12. **May an authority place on a timeline against its owner's will?** Default: yes, recorded as the system acting by a delegation citing the ruling. Blocks: the case's compelled apology.
13. **Can a placement exist and be invisible until a condition holds?** Default: yes, by a rule at read time. Blocks: the case's Decided visibility until all judges have voted.
14. **What does a newcomer to an audience see?** Default: set by rule; with none, from joining. Blocks: the family chat case.
15. **Can a timeline be closed, and is that different from ending?** Default: yes; readable, no new placements. Blocks: task completion, final ruling.
16. **Does a timeline survive the end of its group, task, case or owner?** Default: yes. Blocks: the group research's Q16.
17. **Is a system notice or log activity a placement without a content?** Default: yes. Blocks: content's `log-activity`.
18. **Is the stored record named a placement, with "event" reserved for Memar's runtime occurrence?** Default: yes. Blocks: the names of `event` and its protocol files.
19. **Is forward timeline's placement with provenance, with a shared restriction rule?** Default: yes. Blocks: content's `forward` folders.
20. **Are the timeline's two limits and content's interaction limits one capability?** Default: yes. Blocks: nine folders.
21. **Are calendar entries and placements one thing or two?** Default: two. Blocks: management.md "Event lifecycle vs timeline".
22. **Is a collection a timeline whose only placer is the curator?** Default: undecided, Explored. Blocks: content's `collection`.
23. **How does a placement reach a follower in another organization?** Default: through `follow`. Blocks: follow's delivery question.
24. **Is `blocked-text` a rule on placement?** Default: yes, through `condition_is`. Blocks: `blocked-text`.
25. **Does sensitivity reach a timeline's existence, a placement and a cursor?** Default: yes. Blocks: authorization, receipts.

### Next Steps
1. Owner answers Q1 to Q3 first; they change what the domain is.
2. Hold the alias-UUID conversion of `protocol/dt-uuid.kh` until Q1; do not convert `dt-reason.kh`, `service-set_event.kh` or `read_until/protocol/data_model.kh` before Q2, Q8 and Q18 (their `org/` import prefix and the absent `knowledge/comment` path are stale in any case).
3. After Q1 to Q3, give the domain document a Model and Policies section (kernel K1 to K5) and one Placement and Open questions section per bare edge folder, using the mapping in the research's finding 5.
4. Settle with the content owner the shared items: group index, pin, forward, receipts, interaction limits (content Q3, Q4, Q15), so no relation stays defined twice.
5. Ask the task and case owners to restate "one timeline owned by content" and the case premise in the light of Q1.
6. Add a timeline.changelog.md entry for each decision taken.

## Related Artifacts
- [`README.md`](README.md)
- [`../../knowledge/content/content.handoff.md`](../../knowledge/content/content.handoff.md)
- [`../task/task.handoff.md`](../task/task.handoff.md)
- [`timeline.research.001.md`](timeline.research.001.md) — Research 001 (2026-10-18); questions and Next Steps above
- [`timeline.changelog.md`](timeline.changelog.md)

## Notes
- Provenance: Organization ideas backlog → Knowledge / Content / Task → Content & Timeline (2026-09-16 migration).
- Repository-as-Content / Timeline entry-point arguments expanded in [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Modeling method, entry points, and documentation facets).
