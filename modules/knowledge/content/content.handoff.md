# Content Handoff

## Topic & Purpose
Open questions, decisions not yet recorded in a governing document, and anticipated work for two readings of Content that share this module. The first is the Content model document ([content.md](content.md)), which models how meaning, reference, composition, arrangement and interaction relate when describing any piece of content, relocated here when the documentation method removed unresolved-question lists and the Discussion wrapper from base documents' bodies. The second is the organization's content domain: Content as the holding domain — Timeline attachment, relations and edge vocabulary, versioning and identity across edits, Code as Content, GUI projection requirements that mention content, the modeling interrogation method, and offline concurrency and merge-conflict semantics — migrated from the Organization ideas backlog (2026-09-16), with second-pass notes where content-shaped, and carried here from the organization repository's handoff when the two repositories were merged (2026-10-19). Whether the two readings are one concept is itself open ([below](#do-the-interface-semantics-content-and-the-organizations-content-domain-share-one-document)).

## Status
Active — for the Content model document, the open work below; for the content domain, most Content and Timeline, relations and Code-as-Content decisions are decided, while the Content definition, Timeline primitivity, the content-identity mechanism and concurrency semantics remain open.

Open work for `content.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Decisions
The entries below were carried from the organization repository's handoff as they stood on 2026-10-19; none has landed in a governing document, so each stays here ([Decisions](../../../modules-plugable/knowledge/documentation/handoff/handoff.md#decisions)). The tag at the end of an entry is the confidence the source gave it; the source did not record each entry's rejected alternatives, and none is invented here. An entry tagged `open`, `problem` or `observation` is not a decision and is kept where the source put it.

### Content & Timeline

- Content is the org's holding domain: any piece of content is an independent unit attachable to one or more Timelines — the Twitter model (a tweet in its author's timeline, and in others' via retweet); the org equivalent: an RFC/chat in its author's timeline *and* in a project's. *(decided)*
- A repository (e.g. Memar itself) is just another Content, living in a Timeline where only designated members may add; the creation of a project is an entry-point node that thousands of other contents (tasks, RFCs) link to. *(decided)*
- "Entry point" should be Content, not Concept: every token (word, phrase, question…) takes its identity from the Text domain and may then be described through the Content domain. *(decided)*
- Search-entry model: a term opens a hub that *describes* it and links onward — not a single file/page carrying every specialized view; related tasks are reached by navigating to their own screens. *(decided; navigation/selection method for each view — open)*
- A folder/directory's entry document must actually define and explain the word that names the directory; GitHub's fallback of a bare file listing is explicitly rejected. *(decided)*
- Wiki-as-is is rejected as the org's knowledge model: it still assumes Concept → one Document; the relation is Concept → knowledge graph → many documents. *(decided)*
- Whether Timeline is an independent entity at all — Task (and possibly Timeline) may be projections/compositions of more primitive concepts. *(open)*
- Formal definition of Content itself — the chat repeatedly used the word without fixing boundaries; the org owes the canonical definition ([content.md](content.md) covers a different, interface-semantics Content; see [the open question on the two readings](#do-the-interface-semantics-content-and-the-organizations-content-domain-share-one-document)). *(open)*

### Relations & edge vocabulary (content-relevant)

- Comment is not an independent entity — Content + a `reply_to` relation; what looks like a type is often a label or a loop-edge detectable in other ways. *(decided)*
- Folder and Tag alike reduce to Node + Relation. *(decided)*
- Working edge verbs: `belongs_to` (tree containment), `reply_to`, `produces` (Task→Decision), `changes` (Decision→Content Version), `supports` (Discussion→Decision), `code_module_of`, `depends_on`, `implements`. Full Task-domain edge taxonomy explicitly deferred to the Task domain's own session. *(direction; taxonomy — open)*
- Modeling interrogation method for every word: independent node or dependent? which edge (simple/loop/shortcut)? — e.g. `Customer` as a shortcut edge for Users linked to purchases; then refine ("must the purchase be *successful*?") — each refinement discovers a Rule to document. Words are never gated as "good/bad for the model"; only *where* they belong, so the model is allowed to grow. *(decided method)*

### Versioning (content identity)

- Versioning is not a per-domain concern: the model always treats the **current value as authoritative**; any domain needing a change path uses one shared, cross-domain mechanism — per-record edit retrieval implemented once for all domains (username change included), and "for every record: who requested the change, who approved it" must exist. *(decided)*
- Storing raw old versions alone has no value — the value is the request/authority/reason chain. *(decided)*
- Time-series data (every reading stands on its own; none "replaces" a previous) must not be conflated with the version concept. *(decided)*
- Content identity across edits: a persistent ContentUUID surviving edits with change-events attached, vs. new-content-per-revision — direction leans to the former; mechanism is the org's to settle (it determines versioning, history, review, knowledge evolution, task tracking). *(decided direction, open detail)*

### Code as Content

- Code is Content; file/folder is not its identity — stable identity is ContentUUID with `code_module_of`, `depends_on`, `implements` edges linking code to modules/projects/tasks; a project name is itself a defined content with dependencies. *(decided)*
- High-level source code is not an executable artifact — it is declarative (a compiler/interpreter artifact) and, in AI-era development, a source of truth for domain knowledge via its tokens; treat code first as knowledge representation. *(decided)*
- Expect the hardest mental resistance exactly here (abandoning file/folder for code); org GUIs may keep a file/folder view for legacy users while the model stays content-based — precedent: chatbots show file GUIs yet feed models plain text and store k/v internally, because the model needs content, not paths. *(observation)*

### GUI projection requirements that mention content

- Multiple simultaneous GUIs (GitHub-, Reddit-, Twitter-, Jira-like, forum, wiki, graph, timeline, kanban, file-explorer for legacy users) must be buildable over the same data; if they can't, the team is modeling UI, not domain. *(decided)*
- Repository-wide physical snapshots are replaced by logical snapshots: "show me all content states related to Task-42". *(decided)*

### Concurrency (offline multi-actor) — merge-conflict / semantic unit

- Concurrent modification survives removal of files/Git — chain-store problem: offline and online branches selling the same last item within the checkout window, with the branch network dropping offline so stock counts are unverifiable; the org must model "two actors modified reality on different observations — now what?" as its own requirement. *(decided direction 2026-10-05, owner)* One clear path: ordered change requires lock. Designate a unique changer per entity (single writer) and route every change for that entity to its changer; scale by consistent hashing of entity identity over changer nodes (worked precedent: per-account lock with accounts mapped to nodes, record traveling as event). Time/version-stamp acceptance is not impossible but high-cost, and rejected as the default. Mechanism, not model: the lock/queue never becomes the responsibility model itself.
- "Merge conflict" is a same-file artifact, not a behavior problem: the org's unit of conflict should be the semantic unit, not the byte container. *(decided)*
- Monorepo-vs-multi-repo arguments are wasted energy. *(decided)*

### The org's own document model

Migrated from the organization's ephemeral KM seed, where it was parked.

- Universal knowledge-concept document blocks: Identity, Motivation, Definition, Explanation, Relationships, **Modeling Notes** (node? edge? property? projection? rule?), **Common Misconceptions**, Open Questions, References — plus a **Modeling Journey / Discovery Process** block (initial assumption → why questioned → alternative interpretations → current understanding), because much of the knowledge's value is in the *path*, so a future human or AI doesn't re-walk it. *(accepted; the two named blocks are also recorded as catalog candidates in `documentation-explanation.handoff.md`)*
- Define reusable building blocks once (Definition, Explanation, Relationship, Rule, Decision, Reference, Question, Example…), then let templates *compose* them — never the same section reworded across templates; multiple independent templates (PRD/MRD/BRD-style) are a transitional allowance, superseded by one shared structure + profiles. *(decided method)*
- Documentation = structure + context + phase: RFC is a *review phase* a content can be in, not a document kind — while in that phase the system runs automatic behaviors (e.g. notifying designated people to comment when new related content appears). *(decided)*
- Process rule: domains like Content/Task get formally declared only after at least one approval besides Omid, before their documentation structure is discussed. *(decided)*
- An org concept document (e.g. "Cash Transaction") with Title, Abstract, Definition, Motivation, Domain Model, Rules, Examples, Related Concepts, Open Questions is a sound shape. *(accepted example)*
- The smallest reusable knowledge unit is any token (word, phrase, question…) — human knowledge has no existential nature without human-language tokens; don't impose document-sized atomicity. *(decided)*
- A concept is not always a node; the question is its correct place, not the word's acceptability ("accept all concepts; then discover their place in the model"). *(decided)*

### Knowledge capture, channels & migration

- Diagnosis: organizations produce vast data but cannot retrieve knowledge ("why did we decide X?" after two years — nobody answers, or everyone answers differently); the deeper failure is that Decision, Discussion, Task, Document, and Code are not components of **one** system, each siloed in Email/Slack/Telegram/WhatsApp/Jira/GitHub/Google Docs/Notion. *(decided)*
- Communication ≠ Knowledge: a conversation produces knowledge but is not knowledge; knowledge must be discoverable, relatable, reusable, challengeable, evolvable. *(decided)*
- Do not ban external channels — build org software good enough that people won't want to leave, and provide a way to import the data from channels they did use. *(decided; import mechanism — open)*
- Sectors' critique/suggestion channels currently leak to social networks and messengers — capturing feedback as first-class knowledge is an org requirement. *(problem)*
- Before designing the KM domain, spend sessions on the *validity of the questions themselves* — otherwise months go into rebuilding what was never the organization's real problem. *(decided method)*
- Extinction of legacy ideas (filesystem-centrism, OS-as-everything, IDE-centric work moving into chat environments) is what permits root-level re-modeling; adoption/change management should expect tool-migration as the norm. *(decided)*

## Open Questions

### Does the content domain need nodes, parts and labels, or only addresses?
- State: "When a check runs" in `content.md` speaks of a text node, a `blob` node and the label `legacy-unchecked`, which are `record`'s terms (a node, its parts under domain keys, its labels), and "How a Task is stored" in `task.md` makes a content a node with the part `content`. The owner ruled on 2026-10-24 that a kernel module's link to `record` is only the reference to an address ([Memory Address](../../computer/memory/address/address.md)). That a store holds bytes and is blind to their encoding is the memory contract's own and is repointed to it; the `labels` part and `scan` by label are only `record`'s (the concept of a label is [Label](../label/label.md)'s), and the node vocabulary and `legacy-unchecked` beside them are load-bearing for the check's attachment to texts, and were not edited.
- Options: (1) Recommended: `content.md` states a text and a content by the address that holds them and says the check is attached by whatever classification the composition keeps, and the label `legacy-unchecked` and the node vocabulary are the composition's use of `record`; cost: a rewrite of the paragraph. (2) The paragraph stays, stated as the composition's use of `record`. (3) The content domain needs labels as its own subject.
- Anchor: the bullet "When a check runs" of [content.md](content.md).
- Blocks: the move of the `record` capsule. Assumption meanwhile: option 2.
- Asked: 2026-10-24, Claude (task `20261024-T160312Z-25344`), for Omid Hekayati.

### Primary media versus a text transcription of the same content
- State: a content may carry audio (or other media) while an agent or a human also types that utterance into text stored under text. On a Task timeline it must be clear which content is the *primary* capture and which edge is the textual rendering. Owner named this on 2026-10-20; design task `20261020-T131911Z-22300` (depends on sitting 4).
- Options: (1) one content node with a medium object plus a `transcript_of` (or similar) edge to a text-bearing content; (2) one content with two attachments, primacy a label or edge attribute; (3) other — session proposes.
- Anchor: this handoff; task `20261020-T131911Z-22300`.
- Blocks: timeline display of multimodal Task discussion; any rule that collapses transcript into a second unrelated content.
- Asked: 2026-10-20, by task `20261020-T131818Z-22300`.

### Do the interface-semantics Content and the organization's content domain share one document?
- State: since the merge of 2026-10-19 both live in this module. [content.md](content.md) is the interface-semantics model (Semantic, Addressability, Composition, Layout, Theme, Event) and names no Timeline, identity or revision concern; the organization's content domain (Decisions above, [content.research.001.md](content.research.001.md)) is a different thing, as the research's [first finding](content.research.001.md) already says. The domain's canonical definition is owed and has no home: writing it into `content.md` would put two models in one document, and a second document needs a name that does not collide.
- Options: (1) keep `content.md` as the interface-semantics model and give the domain its own document beside it under a name the owner picks (recommended: the two concepts answer different questions, and neither document's text has to bend); (2) one document with two parts; (3) rename one of the two terms. Whichever is chosen, the definition the research's questions 1 to 3 wait on is written there.
- Anchor: this module's folder; the research's [Open Questions](content.research.001.md#open-questions); the owner's rulings of 2026-10-17 that content as a domain is the organization's and that file-system thinking is put aside there.
- Blocks: the content-domain definition and every Next Step of [Research 001](#research-001-questions-and-next-steps-2026-10-15) that writes into a document. Assumption meanwhile (Tentative): `content.md` stays the interface-semantics model and nothing of the domain is written into it.
- Asked: 2026-10-19, by the session that carried the organization's text.
- Ruled 2026-10-24 (owner, task 20261023-T164153Z-4608): the two readings are one concept; the organization's unit is the records of Content. The canonical definition of those records still has no home and is not written; see [Text Handoff](../text/text.handoff.md#owners-rulings-on-the-premises-of-text-content-and-representation-2026-10-24).

### How do overlapping or nesting compound tokens behave?
- State: moved 2026-09-11 from the same wrapper. Token composition (the polysemy mechanism) has not been tested against real multi-word phrases that overlap or nest.
- Next: run real corpus cases through the composition rule.

### Does the project need a minimal, rendering-agnostic arrangement primitive?
- State: moved 2026-09-11 from the Layout topic's retired Discussion wrapper. Whether even a minimal abstraction (ordering, grouping, priority — algorithms entirely left to renderers) is warranted, versus zero shared vocabulary, is unresolved; the body defers this to a dedicated document once sufficient concrete cases exist.
- Next: see the dedicated Layout/Theme document under Anticipated Work.

### Where does Theme's authority end, and does user-authored composition freedom extend beyond styling?
- State: moved 2026-09-11 from the Theme topic's retired Discussion wrapper. The Theme/Layout/Launcher-like-boundary relationship is unresolved, as is the more radical possibility that end users may compose their own Widget/Page arrangements (the Android Launcher analogy, recorded in the body's Where Theme's Authority Ends).
- Next: decided together with the arrangement question in the dedicated Layout/Theme document.

### What addressing mechanism supports deep recursive addressability?
- State: moved 2026-09-11 from the Multi-Instance topic's retired Discussion wrapper. Current URL structure does not naturally accommodate arbitrarily deep addressability into a Composition graph; the question's recurrence across unstructured content and Composition is itself evidence that Addressability is one shared primitive, but the concrete mechanism is unresolved here.
- Next: design the deep-addressing mechanism; coordinate with the Platform layer (PersiaOS) where cross-runtime synchronization is concerned.

### Must the Authoring Model be a new syntax, or a disciplined HTML/Markdown subset?
- State: moved 2026-09-11 from the Authoring Syntax topic's retired Discussion wrapper. Both remain live candidates — a new compact syntax, or a subset of HTML/Markdown compiled through an intermediate tool that strips scattered metadata (`title`, `property`, `content` attributes and similar) in favor of short `refers-to-type` edges resolved from a Type Definition. Neither is chosen.
- Next: prototype both against real legacy templates (the invoice examples).

### What is the testable criterion for "Khayyam-manner"?
- State: moved 2026-09-11 from the Khayyam-manner topic's retired Discussion wrapper. The two properties (no unwrapped primitives; absolute encapsulation) are stated informally; without a pass/fail test the label risks being claimed by any language.
- Next: derive the criterion from concrete cases — see the anticipated short document below.

### Where is the boundary between structural delimitation and embedded semantic tagging?
- State: moved 2026-09-11 from the Structural Notation topic's retired Discussion wrapper. Flagged high-priority: the Position A/B question (pure delimiter vs. implicit semantic tagging, e.g. Markdown's `#`) is directly testable against this project's own YAML-front-matter-plus-inline-Markdown convention, and the document's own ASCII tree/graph diagrams already demonstrably exhibit Position-B behavior (recorded in the body).
- Next: see the self-audit under Anticipated Work.

### Can one Content participate in multiple Timelines, and is Timeline a distinct concern?
- State: narrowed 2026-10-04. The knowledge-management session modeled organizational history as Content units attached to one or more Timelines — the pattern where a post lives in its author's timeline and reaches others' timelines through re-entry, without duplicating the unit, and where one Task's outcome appears in several participants' views while remaining one Content. That part follows from relations the body already states: neither Composition membership nor arrangement is a property of a node, so one Content may appear in as many Timelines as there are consumers arranging it; the organization's decision that any content is attachable to one or more Timelines is under [Content & Timeline](#content--timeline). What remains open is the cross-Composition case — whether a Timeline spanning separate Compositions (a post reaching another's timeline by re-entry) is an arrangement at all — and whether Timeline is an independent entity or a projection of more primitive concepts (the organization's open entry under the same heading), together with the body's own deferral of any shared arrangement vocabulary to the dedicated Layout/Theme document. content.md names no Timeline concern, and none is claimed here; `knowledge.md` formerly pointed its scope boundary at a "Timeline" domain model here, which did not exist — that dangling reference was removed.
- Next: decide whether Timeline is a distinct concern, or a consumer-side projection under Arrangement/Composition, when the first multi-timeline case is worked in a consumer project such as `organization`.

### What are the canonical definitions of Content, Task, Timeline and Group, and their minimal decomposition?
- State: carried from the organization's handoff (its open item 1). Is Timeline primitive? Does Task decompose into Group + Content + Relation + State + Permission? The definition of Content for the domain is the one [the first entry above](#do-the-interface-semantics-content-and-the-organizations-content-domain-share-one-document) leaves without a home.
- Next: answered by the owner after the research's questions 1 to 3 ([Research 001](#research-001-questions-and-next-steps-2026-10-15)).

### What is the content-identity-across-edit mechanism?
- State: carried from the organization's handoff (its open item 3). A stable UUID with change events versus a new content per revision; the direction leans to the former ([Versioning](#versioning-content-identity)), the mechanism is open. Research question 1 refines it.
- Next: settled with research question 1.

### What logical-snapshot tooling is needed, and does any real need for global-state entities survive?
- State: carried from the organization's handoff (its open item 4). Repository-wide physical snapshots are replaced by logical snapshots ([GUI projection requirements](#gui-projection-requirements-that-mention-content)); the tooling is not designed.
- Next: design when a first logical-snapshot case is worked.

### What is the search-entry contract: how does a term resolve to a hub, and how are specialized views reached?
- State: carried from the organization's handoff (its open item 7). The model is decided ([Content & Timeline](#content--timeline)); the user-facing contract is not.
- Next: write the contract with the first consumer GUI.

### Does Repository-shaped grouping re-emerge as an emergent property, or stay a plain context node?
- State: carried from the organization's handoff (its open item 8). The Timeline and Content decisions treat repository-shaped nodes as Content plus Timeline; the deeper question of whether Repository is a domain concept or a file-system-era projection of Content linked to a common context stays open.
- Next: see the Repository question in the knowledge-management handoff linked under Notes.

### What is the concurrency mechanism's detail?
- State: carried from the organization's handoff. The direction is decided (2026-10-05, owner): serialize through a per-entity lock, with a unique changer and consistent-hash routing, not timestamp reconciliation ([Concurrency](#concurrency-offline-multi-actor--merge-conflict--semantic-unit)). The mechanism's detail is open; this handoff is the home for the merge-conflict and semantic-unit question.
- Next: design with the first offline multi-actor case.

## Research 001 questions and next steps (2026-10-15)

### Standing of the research's proposals
Proposals only, from [content.research.001.md](content.research.001.md) (thirteen scenarios, a four-element kernel, five rival models, a mapping of every edge, loop and widget folder, thirty test scenarios, eighteen contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above are not re-argued.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](content.research.001.md#open-questions). Ordered by what they change.

1. **Is the content the work-level identity with immutable revisions below it, and how do the persistent id and the content-derived identity of the text handoff meet?** Default: persistent identity for the thing discussed; each revision an immutable value with a content-derived address. Blocks: the definition of the content domain (its home is [an open question above](#do-the-interface-semantics-content-and-the-organizations-content-domain-share-one-document)), the Task proposal's `changes` target, any `ContentModel`.
2. **Does a content share the text's UUID (the [Idea backlog](#idea-backlog)) or hold the text by a relation?** Default: a relation. Blocks: the backlog item, the text-ownership convergence in [text.handoff.md](../text/text.handoff.md).
3. **Is placing a content in a group's ordered list the timeline's `event_is`, and is forward a placement with provenance?** Default: yes to both. Blocks: Timeline primitivity (the Timeline entry under Open Questions above), the forward and pin folders, the group index lock question.
4. **Who orders a group's contents: a single changer per group, or time?** Default: a single changer (the Decided concurrency direction); time is a presentation. Blocks: the group data model's TODO, offline creation.
5. **Who is the author: requester, speaking identity, credited parties, or the home timeline's owner?** Default: the kernel keeps the request chain; the speaking identity is the home placement's owner; credits are attribution. Blocks: `ChangeSenderUser`, ownership's participant file.
6. **Is one body in two languages one content with two texts, or two contents related by translation?** Default: one content, one text per language. Blocks: translation handling.
7. **What does delete mean, and what survives?** Default: the `deleted` status plus a rule closing the body, with a tombstone; erasure of the body a separate authority-gated event; "delete for me" a viewer preference. Blocks: the `deleted` loop's methods, retention duty.
8. **Do read, seen and delivered merge into one ladder, and what separates seen from read?** Default: one capability, `delivered < seen < read`; delivered stays client-held. Blocks: three edge folders, `user_status`.
9. **Do the genre loops stay, and which?** Default: none promoted now; medium derived from objects; album, serial and episode to collection; editorial forms wait for rules; `game`, `sport_game`, `concert` leave as not-content; `confidential` becomes visibility. Blocks: the 18 folders and their Placement sections.
10. **Does collection live in label's `list` with a position, or as a content module?** Default: extend `list`. Blocks: album, serial, serial-episode, course.
11. **Is a derived view (redaction) a revision or a separate content with a derived-from link?** Default: a separate view with a link. Blocks: sealed and redacted filings.
12. **Does a reply or credit target a part of a content, and is the part an entity or a field?** Default: Explored; addressed by revision and locator. Blocks: the commentary use case.
13. **Is an imported email a raw acquired object with discovered fields?** Default: yes. Blocks: the email data model, Bcc.
14. **Does `bio` leave the content domain for thing?** Default: yes if it survives the placing test. Blocks: the bio folder.
15. **Should interaction-limits attach to any relation and be set by the owner first, the group as default?** Default: yes. Blocks: the merge of seven folders, timeline's two limit edges, the backlog's group-level forms.
16. **Is a machine-written text or a system notice content?** Default: a notice is a timeline event; a summary is discovered data. Blocks: `log-activity`, derived summaries.
17. **Who owns reporting and appeal of a content?** Default: the justice side. Blocks: the `Report()` service, the `hidden` vocabulary.
18. **Should the review phase be a pluggable module, and how does it relate to the documentation Status?** Default: yes later; decide the relation first. Blocks: RFC automatic behaviours.
19. **Does a paid-partnership disclosure live in attribution with a rule?** Default: yes. Blocks: the `group-user` note.
20. **Where does the misfiled `NotificationTemplate` in `protocol/data_model.kh` go?** Default: the notification domain. Blocks: nothing; hygiene.

### Next Steps
1. Owner reviews research findings 1 and 2 and answers questions 1 to 3 first; they change what the domain is.
2. If question 1 is accepted, a session writes the definition paragraph and the four-element kernel into the document that owns the content domain (not done: the research added no Model or Policies, and [the home of that document](#do-the-interface-semantics-content-and-the-organizations-content-domain-share-one-document) is open).
3. A session fills Placement and Open questions on the 18 edge folders that have none, using the research's mapping as a reading list; no folder moves before the owner answers questions 3, 8, 9 and 15 and catalogue R2.
4. Draft the candidate documents for `revision`, `interaction-limits`, `receipts` and `attribution` once questions 1, 7, 8 and 15 are answered; do not write a `ContentModel` before question 1.
5. Resolve with the timeline domain whether the group's ordered list is its `event` edge (question 3), and with the text domain whether mention and hashtag tokens stay text's while content owns the resolved relation.
6. Reconcile the contradictions listed in the research in the documents that own each side, notably the reply group rule, the three edit models, the forward model, and the `to_label` edges that point at a user.
7. Ask the Task research's owner session to align K5 (`changes`) with this research's revision, and its question 15 with question 1 here.
8. Read what the research did not: the text domain's `mention`, `hashtag` and `anchor_text`, the notification, uri and object domains, the detection and justice pluggables, and the literature on collaborative editing; record anything that changes a Tentative item.

## Anticipated Work

### A concrete Authoring Syntax prototype
- State: from the retired document-level Future possibilities. Compile an Authoring Model to Khayyam graph calls and test against real legacy templates (the invoice examples referenced throughout the document) to validate the concept/implementation split claimed across the concern topics.
- Next: after the Authoring-Model syntax question above narrows the candidate space.

### A dedicated Layout/Theme document
- State: from the retired Future possibilities. Once enough real Composition examples exist across at least GUI and one non-visual modality (VUI or Braille) to test candidate rendering-agnostic arrangement vocabularies and the Theme/Layout/Launcher boundary.
- Next: collect the cases; carry the two related Open Questions above.

### A testable "Khayyam-manner" criterion
- State: from the retired Future possibilities. Likely its own short document, derived from concrete cases of languages that do and do not qualify.
- Next: draft once implementation experience accumulates.

### A self-audit of this project's own Markdown+front-matter convention
- State: from the retired Future possibilities. Test the Position A/B question against the documentation format this very document is written in — directly testable against material already in daily use, unlike most other open questions.
- Next: run when documentation-method work next touches the authoring format.

### Cross-modal rendering experiments
- State: from the retired Future possibilities. Take a single Semantic Graph instance through both a GUI renderer and a VUI renderer, to empirically test whether the Semantic/Interaction/Rendering separation claimed throughout actually holds under real multi-modal pressure. A design-system-level variant was also proposed during research — one design system's tokens taken through multiple renderers — recorded in [content.changelog.md](./content.changelog.md)'s research-deletion entry.
- Next: depends on the first renderer implementations.

### Idea backlog
Carried from the organization's `content.md`, where it stood as a section of the document; review discipline per [vocabulary-discipline.handoff.md](../../management/vocabulary-discipline.handoff.md). Nothing below is ratified. Each idea is anticipated work, and each review question is an open question for the owner.

- **Idea**: GUI widget limit forms `[comment, ---, forward_off] >>` and `[group, ---, forward_off] >>` — all comments in that group can't forward; policy text recorded: "No `comment` can made a relation to this `comment` with `forward` label."
- **Review questions**: widget = GUI-side surface, not a core edge — who enforces `forward_off`: a rule on the existing [forward](edges/forward/forward.md) edge (core never knows rule; the group list is a parameter ⇒ one rules module + configuration) with the widget only surfacing it in the pluggable GUI, or is all of this presentation configuration with nothing to model?
- **Idea**: GUI widget limit forms `[comment, ---, quote_off] >>` and `[group, ---, quote_off] >>` — all comments in that group can't quote; policy text recorded: "No `comment` can made a relation to this `comment` with `quote` label."
- **Review questions**: widget = GUI-side surface, not a core edge — does `quote_off` ride as a rule on the existing [quote](edges/quote/quote.md) edge (core never knows rule; group lists are parameters), surfaced by the GUI widget? Any semantics beyond presentation?
- **Idea**: GUI widget limit forms `[comment, reply_off, ---] >>` and `[group, reply_off, ---] >>` — all comments in that group can't get reply. The `Policy (rule):::` statement was left empty in the source — the `reply_off` policy text still needs authoring (forward and quote have theirs).
- **Review questions**: same placement question as forward/quote — a rule on the existing [reply](edges/reply/reply.md) edge, not a core widget edge; what should the `reply_off` policy say once authored — mirror the forward/quote wording, or does reply's standalone-thread rule demand something different?
- **Idea**: if a comment wants `text`, it MUST use the same UUID for the `text` domain (shared identity, not a copy); if a comment's text contains only emojis, show them larger than normal text.
- **Review questions**: same-UUID requirement = the comment node taking the text identity simultaneously (content multi-typing / reference-not-embed — the precedent recorded in [product.md](../../economics/product/product.md): a node can take Product and Content identities at once) vs a stored edge to a text node — which is it, and does it converge with the text-only ownership decision in [text.handoff.md](../text/text.handoff.md)? Emoji sizing is presentation → pluggable GUI only — confirm nothing to model?
- **Idea**: three reads of content — by type, by time, and by user plus type — returning content ids with offset and limit.
- **Review questions**: these reads are content's own lookup, not a GUI page. Does each read earn a module (analytics is always pluggable; a query with its own storage is a module), or are they one content read with parameters?

### The check dispatcher
- State: `memar content check` becomes a dispatcher over the domains a node belongs to, as [Checking text](content.md#checking-text) states; the code that builds it asks each owning domain for its rules (text, documentation, an authoring syntax). Which module holds the Markdown conventions is open: the Authoring Syntax topic of the content document names none.
- Next: build it in the task that re-bases the task verbs on the record contract; until then the verb stays as it is.
- State (2026-10-24): the code was split before the dispatcher: the bytes half is `text/services/text_check.py`, and `content_check.py` in the documentation module composes it with the Markdown and documentation rules. The dispatcher proper (asking each domain a node belongs to by its label) is still owed.

### The services left, and the names they keep
- State (2026-10-24): the Python services of this module were placed by subject (see the changelog record of that date). What stays is the reference and the two verbs that resolve it. Every verb kept its word under `memar content`, because a file named `content_<verb>.py` outside the domain's folder is the domain's verb by the router's rule.
- Next, a task of its own: drop the category word from the verbs so that each service has a complete name of its own (owner, 2026-10-24). It renames every MCP tool (`content_search` and the rest), `AGENTS.md`, the skill and the installed launcher (`content path`), and needs the router to accept a service that belongs to no group. The four verbs that exist under two names (`meta`/`get-meta`, `section`/`get-section`, `path`/`resolve-path`, `obligations`/`list-undischarged-propagations`) are another chat's rename in progress and end with it.
- Open: `write` and `edit` are in the filesystem module and the services that read the checkout (`reference`, `corpus`, `task_records`) still reach files and git through `plugable_load`; they are the seam the memory port programme (task 20261022-T185903Z-15504) replaces, and its plans name the old paths.

## Related Artifacts
- [`content.md`](content.md) — the interface-semantics Content model this handoff's first reading serves
- [`content.research.001.md`](content.research.001.md) — the conceptual research: scenarios, kernel, models, mapping, tests, owner questions
- [`content.changelog.md`](content.changelog.md)
- [`README.md`](README.md)
- [`../text/text.handoff.md`](../text/text.handoff.md)
- [`../../management/timeline/timeline.handoff.md`](../../management/timeline/timeline.handoff.md)
- [`../../management/task/task.handoff.md`](../../management/task/task.handoff.md)
- [`../../../modules-plugable/gui/gui.handoff.md`](../../../modules-plugable/gui/gui.handoff.md)
- [`../../../modules-plugable/knowledge/channel-comms/README.md`](../../../modules-plugable/knowledge/channel-comms/README.md) — temporary editorial/channel framework

## Notes
- Provenance: Organization ideas backlog → Knowledge / Content / Task domain (2026-09-16 migration). Document-model and knowledge-capture bullets live in this handoff (under Decisions); editorial channel framework lives in `modules-plugable/knowledge/channel-comms/README.md`.
- The Modeling interrogation method is recorded under Relations & edge vocabulary above *(decided method)*.
- Further brainstorm dialectic (Git/filesystem, Change Rationale, documentation facets, Repository-as-domain-concept open question) lives in the KM handoff Discussion sections — cross-link, do not treat chat as home: [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md).

### Knowledge vs Document / Representation *(appended from KM brainstorm — status unsettled as Content-domain wording)*

- An RFC (or any filed content) is **not knowledge itself** — it is a **representation / articulation** of knowledge. The filesystem critique asked whether knowledge can even be "containerized"; the Content domain must keep this distinction when defining boundaries of Content vs Document vs Knowledge. *(from brainstorm — status unsettled; full dialectic in KM handoff Discussion — Git, filesystem, and organizational knowledge)*
- Related open: Is Repository itself a domain concept, or merely a filesystem-era projection / emergent grouping of Content linked to a common context? *(open — Timeline/Content decisions treat repository-shaped nodes as Content + Timeline; the deeper "domain concept?" question remains)*
