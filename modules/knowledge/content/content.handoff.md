# Content Handoff

## Topic & Purpose
Content as the org's holding domain: Timeline attachment, relations & edge vocabulary, versioning/identity across edits, Code as Content, GUI projection requirements that mention content, modeling interrogation method, and offline concurrency / merge-conflict semantics. Migrated from the Organization ideas backlog (2026-09-16) and second-pass notes where content-shaped.

## Status
Active — most Content & Timeline / relations / Code-as-Content decisions decided; Content definition, Timeline primitivity, content-identity mechanism detail, and concurrency semantics remain open.

## Decisions

### Content & Timeline

- Content is the org's holding domain: any piece of content is an independent unit attachable to one or more Timelines — the Twitter model (a tweet in its author's timeline, and in others' via retweet); the org equivalent: an RFC/chat in its author's timeline *and* in a project's. *(decided)*
- A repository (e.g. Memar itself) is just another Content, living in a Timeline where only designated members may add; the creation of a project is an entry-point node that thousands of other contents (tasks, RFCs) link to. *(decided)*
- "Entry point" should be Content, not Concept: every token (word, phrase, question…) takes its identity from the Text domain and may then be described through the Content domain. *(decided)*
- Search-entry model: a term opens a hub that *describes* it and links onward — not a single file/page carrying every specialized view; related tasks are reached by navigating to their own screens. *(decided; navigation/selection method for each view — open)*
- A folder/directory's entry document must actually define and explain the word that names the directory; GitHub's fallback of a bare file listing is explicitly rejected. *(decided)*
- Wiki-as-is is rejected as the org's knowledge model: it still assumes Concept → one Document; the relation is Concept → knowledge graph → many documents. *(decided)*
- Whether Timeline is an independent entity at all — Task (and possibly Timeline) may be projections/compositions of more primitive concepts. *(open)*
- Formal definition of Content itself — the chat repeatedly used the word without fixing boundaries; the org owes the canonical definition (memar's later `content.md` covers a different, interface-semantics Content). *(open)*

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

## Open Questions

From Content & Timeline and Versioning passages above (status tags preserved on the Decision bullets). Consolidated list items that belong to content:

1. Canonical definitions of Content, Task, Timeline, Group and their minimal decomposition (is Timeline primitive? does Task decompose into Group + Content + Relation + State + Permission?).
3. Content-identity-across-edit mechanism (stable UUID + events vs. new-content-per-revision).
4. Logical-snapshot tooling, and whether any real need for global-state entities survives.
7. Search-entry UX contract: how a term resolves to a hub and how specialized views are reached.
8. Whether Repository-shaped grouping re-emerges as an emergent property or stays a plain context node.

Also: Offline/multi-actor concurrency semantics (store-inventory class problem) — decided direction 2026-10-05, owner: serialize through per-entity lock (unique changer, consistent-hash routing), not timestamp reconciliation; mechanism detail open. *(prefer this handoff for the merge-conflict/semantic-unit home)*

## Related Artifacts
- [`README.md`](README.md)
- [`../text/text.handoff.md`](../text/text.handoff.md)
- [`../../management/timeline/timeline.handoff.md`](../../management/timeline/timeline.handoff.md)
- [`../../management/task/task.handoff.md`](../../management/task/task.handoff.md)
- [`../../gui/gui.handoff.md`](../../gui/gui.handoff.md)
- [`../../../modules-plugable/knowledge/channel-comms/README.md`](../../../modules-plugable/knowledge/channel-comms/README.md) — temporary editorial/channel framework

## Notes
- Provenance: Organization ideas backlog → Knowledge / Content / Task domain (2026-09-16 migration). Document-model and knowledge-capture bullets live in this handoff (below); editorial channel framework lives in `modules-plugable/knowledge/channel-comms/README.md`.
- The Modeling interrogation method is recorded under Relations & edge vocabulary above *(decided method)*.
- Further brainstorm dialectic (Git/filesystem, Change Rationale, documentation facets, Repository-as-domain-concept open question) lives in the KM handoff Discussion sections — cross-link, do not treat chat as home: [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md).

### Knowledge vs Document / Representation *(appended from KM brainstorm — status unsettled as Content-domain wording)*

- An RFC (or any filed content) is **not knowledge itself** — it is a **representation / articulation** of knowledge. The filesystem critique asked whether knowledge can even be "containerized"; the Content domain must keep this distinction when defining boundaries of Content vs Document vs Knowledge. *(from brainstorm — status unsettled; full dialectic in KM handoff Discussion — Git, filesystem, and organizational knowledge)*
- Related open: Is Repository itself a domain concept, or merely a filesystem-era projection / emergent grouping of Content linked to a common context? *(open — Timeline/Content decisions treat repository-shaped nodes as Content + Timeline; the deeper "domain concept?" question remains)*

## Decisions — org document model & knowledge capture (migrated; was parked in ephemeral KM seed)

### The org's own document model

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
