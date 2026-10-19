# Timeline Handoff

## Topic & Purpose
Timeline as Content's attach surface and the open question whether Timeline is primitive or a projection/composition.

## Status
Active — Content↔Timeline attachment decided; whether Timeline is an independent entity remains open.

## Decisions

### From Organization ideas backlog — Content & Timeline (timeline-related)

- Content is the org's holding domain: any piece of content is an independent unit attachable to one or more Timelines — the Twitter model (a tweet in its author's timeline, and in others' via retweet); the org equivalent: an RFC/chat in its author's timeline *and* in a project's. *(decided)*
- A repository (e.g. Memar itself) is just another Content, living in a Timeline where only designated members may add; the creation of a project is an entry-point node that thousands of other contents (tasks, RFCs) link to. *(decided)*

## Open Questions
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
