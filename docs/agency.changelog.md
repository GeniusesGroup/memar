# Agency Changelog

## Changelog

### Initial draft produced through multi-AI discussion
- Time: 2026-08-04T10:15:00Z
- Type: Created
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, reviewed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued, rewrote

#### What changed
- Produced the first complete draft of this document's conceptual content: the Agency/Agent/Principal/`agent_for` model, the Delegation/Responsibility/Authority/Capability cluster, the Human/Organizational/Software/AI/Hybrid Agency taxonomy, the False Taxonomies and Historical Continuity arguments, the Common Modeling Errors catalog, the Terminological Principles glossary, the Open Questions list, and the Working Principles list. Produced as a single flat sequence of 65 numbered sections, without front matter, ahead of this project's Explanation-facet specification — the full first draft in prose form at the end of the conversation (ChatGPT).
- The working definitions, examples, and counter-examples — the contractor, the writing-ambiguity example, the Hamid Reza Mazandarani exchange — were supplied (Omid Hekayati).

#### Deliberation
- The modeling question (Agency vs. Agent vs. AI Agent) was originated (Omid Hekayati).
- The model was co-developed through iterative critique across a long conversation (ChatGPT).
- Several structural drafts were proposed and then reversed: an `agent.md`-centered outline, then an `agency.md`-centered one, then a `delegation.md` split that was itself later rejected (ChatGPT).
- The final naming and structural calls were made: `agency.md` over `agent.md`; `agent_for` as a relationship, not a node; Delegation folded into Agency rather than split into `delegation.md` (Omid Hekayati).

#### Rationale and alternatives
See the entry below for the alternatives considered and rejected during this drafting process (`agent.md` as the document's name, `delegation.md` as a separate document, `agent_for` as a node) — they are recorded as `Rationale and alternatives` inside the base document itself, under the topics they each concern, rather than only here, since each is tied to a specific, still-referenceable claim in the body and not only to the history of how that claim was reached.

### Migrated into the Explanation-facet structure and reviewed for completeness
- Time: 2026-08-15T14:15:00Z
- Type: Restructured
- Propagates to:
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed
  - [Claude](../CONTRIBUTORS.md#claude) - `Model: claude-sonnet-5` - reviewed, rewrote

#### What changed
- Reviewed the full 2026-08-04 discussion transcript against the drafted document.
- Reorganized the document from a flat 65-section sequence into `documentation-explanation.md`'s current template (front matter, `Abstract`, `Introduction` with `Motivation`/`Methodology`, topic-organized `Explanation` with per-topic `Discussion` / `Results`, `Results`, document-level `Discussion`).
- Distributed the former `Open Questions` and `Common Modeling Errors` sections into the specific topics they concern.
- Completed the `Terminology` glossary, closing a gap with the 2026-08-04 discussion: added Goal/Purpose, Execution, Decision-Making, Trust, Contract, Accountability, Communication, previously defined in the body but missing from the glossary.
- Expanded the thin `False Taxonomies` examples with three additional examples raised in the original discussion but not carried into the draft (SOA/Microservices, Relation/Aggregate Root, Content/Semantic).
- Documented as explicit rejected alternatives the structural decisions (rejecting `agent.md`, rejecting `delegation.md`, rejecting `agent_for`-as-node) that were reasoned through in the 2026-08-04 discussion but never written into the document: an explicit `Rationale and alternatives` entry added under `Delegation` and under `The agent_for Relationship` documenting the rejected `delegation.md`-as-separate-document and `agent_for`-as-node alternatives, using the reasoning already present in the discussion but not previously written into the document as a rejected alternative.
- Added new content that did not exist in either the discussion or the prior draft: a `Rationale and alternatives` entry for the document's own flat-vs-topic-structure choice; a `Prior art` section naming three literatures this document has not yet been checked against (principal-agent theory, agent-oriented programming / multi-agent systems, speech-act theory); and several new `Unresolved questions` — this document's relationship to `type.md`'s Type categories; whether self-directed action is ever fully free of an internal Principal (under Intrinsic and Delegated Agency); and whether this document's own multi-AI production process is itself an instance of the Hybrid Agency it describes.
- Added a full document-level `Discussion` section (Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, Future possibilities) containing Claude's own review — not only a report of gaps between the discussion and the draft, but Claude's independent assessment of the model's remaining weak points.

#### Deliberation
- The migration to the current documentation format was requested (Omid Hekayati — requested).
- The identification and closing of gaps between the 2026-08-04 discussion and the drafted document was requested (Omid Hekayati — requested).
- It was requested that the reviewing AI's own critiques be added to the document rather than left in chat (Omid Hekayati — requested).

#### Considered and not done
- **Silently fixing gaps without flagging them as edits (rejected)**: an earlier approach to this edit considered folding the added content into the existing prose so it would read as though it had always been there. Rejected because it would misrepresent provenance — this document's own stated principle, carried over from the 2026-08-04 discussion, is that definitions and design decisions should be traceable to why they were made; silently blending newly-added reasoning into inherited prose would undermine that principle inside the very document that states it. Every addition of substance is instead attributable to this changelog entry.
- **Leaving the reviewer's own critique only in the chat, not in the document (rejected, per explicit request)**: the default in past reviews of this kind had been to report gaps and critique conversationally rather than to write them into the artifact. Rejected here at the person's explicit request; the critique now lives in the document's own `## Discussion` section (`Drawbacks`, `Prior art`, `Unresolved questions`, `Future possibilities`) so it survives independently of this specific conversation.

### Agency and Process execution responsibility model
- Time: 2026-08-17
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified, emphasized
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — integrated

#### What changed
- Added an explicit treatment of Agency in Process execution. The document now distinguishes `agent_for` (acting on behalf of a Principal) from execution responsibility, defines Execution Agent as a descriptive use of Agency rather than a new entity type, distinguishes execution responsibility from domain ownership, and records Worker and Actor as possible implementation representations rather than conceptual primitives. Dynamic assignment, partitioning, migration, rebalancing, and Consistent Hashing are documented as execution concerns that follow from responsibility modeling rather than defining Agency.
- The resulting model was integrated into `agency.md` (ChatGPT).

#### Deliberation
- It was clarified that an execution Agent may be responsible for a bounded portion of a Process without implying a permanent domain-ownership boundary or an `agent_for` relationship (Omid Hekayati — clarified).
- It was emphasized that a system may have many processing Agents and that responsibility may be dynamically reassigned (Omid Hekayati — emphasized).

#### Considered and not done
- **Treating Worker as the primitive execution concept (rejected):** Worker is implementation vocabulary and varies by runtime.
- **Treating Actor as the primitive execution concept (rejected):** Actor Model is a particular execution model and is narrower than Agency.
- **Using `agent_for` for execution responsibility (rejected):** acting on behalf of a Principal and being responsible for advancing a process are distinct relationships.

### Cross-referenced process.md, closing the Worker/Agency gap
- Time: 2026-08-17T00:00:00Z
- Type: Changed
- Propagates to:
  - process.md: Done — reciprocal links added there in the same pass; see process.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- Reviewed today's "Agency and Process execution responsibility model" changelog entry and the corresponding body content (Agency in Process Execution, Execution Agent, Agency and Ownership of Process State, Dynamic Assignment, Agency Before Synchronization) against process.md's own, independently-written Concurrency topic; found them substantively consistent — both treat Worker as a non-primitive representation of a more general responsibility concept, and both reach a similar escalating decision chain before reaching for synchronization, a similar responsibility-before-synchronization ordering — with no contradiction requiring resolution. No content was rewritten to resolve a conflict, since none was found.
- Added a link from "Agency in Process Execution"'s opening paragraph and from the Worker mention under Execution Agent to process.md's Concurrency topic; the two documents were cross-linked instead of left to duplicate each other going forward.
- Added Process to the "Relation to Memar" summary diagram, which listed System, Module, and Organization but had omitted Process despite this document's own Process-execution content.

#### Deliberation
- After today's ChatGPT session added "Agency in Process Execution," it was noticed that this document and process.md's Concurrency topic cover closely related ground (Worker, execution responsibility, responsibility-before-synchronization) without referencing each other, and a deliberate integration pass was asked for rather than leaving the two to develop independently (Omid Hekayati — requested).

#### Considered and not done
Considered merging the "Agency Before Synchronization" chain and process.md's Concurrency decision chain into a single, shared chain cited by both documents, since they overlap substantially. Deferred: the two chains are pitched at different levels of generality (Agency's version is domain-general; Process's version has Concurrency-specific steps — shared mutable state, invariants, scheduling — that don't belong in Agency's more general statement of the same principle), and collapsing them into one shared version is a larger structural change than a same-day integration pass should attempt without dedicated review.

---

### Observer-to-agent role transition made explicit
- Time: 2026-08-25T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - drafted, applied
- Propagates to:
  - protocol.md: Done in this same pass - its "Protocols and External Observers" topic cross-links back to this subsection.

#### What changed
- Added "From Observer to Agent" under Agent as a Relational Concept, with the cross-link to protocol.md's new observer-facing topic (Super Z - drafted, applied). The point made explicit: observer and agent are relationship-relative positions, not intrinsic types; coming to understand a System's protocols ordinarily precedes acting on that System, and the same System may shift roles repeatedly as relationships form. The hospital complaint-procedure sequence is kept as the illustrative example because it shows observation performed specifically in preparation for action, not merely for comprehension.
- The observation-enables-action insight and the complaint-procedure example were supplied during accounting-domain discovery discussions (Omid Hekayati).

#### Considered and not done
- **Placing the transition under Execution instead (rejected)**: execution concerns how an Agent acts once agency is already in play; the new subsection concerns how a System comes to occupy the Agent position at all, which belongs with the relational-role reasoning of Agent as a Relational Concept rather than with the execution pipeline.

---

### Knowledge Management references hyperlinked; glossary Knowledge defers to its concept home
- Time: 2026-09-05T11:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- The three plain-text "Knowledge Management" mentions in the Agency and Knowledge Management topic are now hyperlinks to [Knowledge](./knowledge.md), which was renamed from knowledge-management.md and re-scoped to the concept in the same pass.
- The glossary's Knowledge entry no longer states a competing standalone definition: it now defers to knowledge.md, building on the foundational definition in [System](./system.md#knowledge-and-science).
- The Relation to Memar concept list already named Knowledge; that reference now resolves to a real document.

#### Deliberation
- It was directed that knowledge, thinking, and agency be linked so the concepts do not stand apart (see knowledge.changelog.md) (Omid Hekayati — decided).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - agency.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only: the document-level `## Discussion` (Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, Future possibilities) and all eight topic-level `#### Discussion` wrappers are retired; no Discussion content remains in the body.
- All fifteen open questions — from What Is Agency?, Agent as a Relational Concept, The `agent_for` Relationship, Agency in Process Execution, Goals and Purpose, Accountability, Relation to Memar, and the document level — now live in the paired handoff's Open Questions; the three document-level Future possibilities items now live there as Anticipated Work.
- The eight rejected alternatives (two under The `agent_for` Relationship, three under Agency in Process Execution, one under Delegation, two document-level) and the three document-level Drawbacks are preserved below under Considered and not done; the document-level Prior art survey is preserved below under Related work. No block carried premise evidence for a body claim, so no inline folds into the body were required.
- The Abstract's closing sentence, the Working Principles preface, and the Results note now point to the paired handoff where the open questions they reference live, replacing references to sections no longer in the body.

#### Considered and not done
- **Modeling `agent_for` as a node, with Agent and Principal as its endpoints (an earlier draft; not chosen; migrated from The `agent_for` Relationship topic's retired Rationale and alternatives)**: an earlier pass at this model treated Agent and Principal as intrinsic entity types connected by the relationship, and separately treated the relationship as something that might need to be modeled as its own entity because it carries qualifiers (a status, a scope, a time bound). Both moves were reconsidered. If `A ── agent_for ──► B` can be represented directly as a graph edge, there is no reason to create an intermediate `AgentFor` node merely because the relationship has a name — the same reasoning that keeps other named relationships in Memar as edges rather than nodes. And once `agent_for` is an edge rather than a node, Agent and Principal stop being types a System belongs to and become the labels for the two endpoints of that edge — which is what forced the reconsideration described in [Agent as a Relational Concept](./agency.md#agent-as-a-relational-concept) and in [The Central Distinction](./agency.md#the-central-distinction).
- **Treating Agent as the primitive concept of this document (rejected; migrated from the same)**: once `agent_for` is understood as an edge between two Systems, Agent is no longer a natural candidate for the document's primitive concept, since it names a position on an edge rather than a node. The candidates for primitive status become Agency, System, and Relation instead — which is the reasoning that produced this document's own title (see also [Methodology](./agency.md#methodology)).
- **Treating Worker as the primitive execution concept (rejected; migrated from the Agency in Process Execution topic's retired Rationale and alternatives)**: Worker is useful implementation vocabulary, but its meaning varies across runtimes and frameworks. The underlying question is whether an acting system has a bounded execution responsibility. Worker is therefore treated as a possible representation of an Execution Agent rather than the conceptual primitive.
- **Treating Actor as the primitive execution concept (rejected; migrated from the same)**: Actor Model provides valuable accumulated knowledge about isolated state, communication, and independent execution, but `Actor` carries a particular model of execution. Agency is intentionally broader: an Agent may be human, organizational, software, AI, hybrid, or another acting system, and an execution Agent need not be implemented using the Actor Model.
- **Treating `agent_for` as the relationship for every execution responsibility (rejected; migrated from the same)**: `agent_for` describes acting on behalf of another System. An Execution Agent may instead be responsible for advancing a process or managing a partition of state without representing another System in that sense. The process model therefore needs a distinct responsibility relationship rather than stretching `agent_for` beyond its meaning.
- **A separate `delegation.md` document (considered, then rejected; migrated from the Delegation topic's retired Rationale and alternatives)**: an earlier draft of this work proposed splitting Delegation out into its own document, on the reasoning that Delegation was substantial enough in volume to justify a dedicated file. That reasoning was reconsidered and rejected: volume is not the criterion Memar uses for whether something is an independent Concept. The relevant question is whether Delegation can be defined without first defining Agency — and it cannot. Asking "what is Delegation?" already presupposes a System capable of Agency assigning some of it to another System; the definition is not self-standing. Delegation is therefore modeled as a chapter of Agency rather than as an independent document, at least until some future need demonstrates otherwise.
- **Organizing this document as a flat sequence of independently-numbered sections, in an earlier draft (rejected at the facet migration; migrated from the removed document-level Rationale and alternatives)**: the version of this document produced before it was brought into the Explanation-facet structure used 65 sequentially numbered top-level sections with no grouping. That structure made it difficult to see which concepts were sub-parts of which — for example, that Verification and Validation exist to qualify Trust, or that the nine items under Common Modeling Errors are a single coherent unit rather than nine independent topics. Migrating to the current facet's topic/sub-topic structure, with each topic carrying its own `#### Discussion` where it has open questions or rejected alternatives specific to it, was chosen over keeping the flat structure and only reformatting the front matter, because the flat structure was itself judged to be part of what made prior open questions and rejected alternatives hard to keep attached to the specific claim they concern.
- **Keeping this document's original social-media motivation (a short public post plus follow-up comments, aimed at a general technical audience) merged into this document, rather than as a separate artifact (rejected; migrated from the removed document-level Rationale and alternatives)**: the discussion that produced this document's content began as planning for a public post about AI Agents. That framing — persuading a general audience, in a small number of short comments — was deliberately not carried into this document. An document answers to different requirements (completeness, precision, exposed open questions) than a public post does (brevity, a single strong claim, a call to action), and conflating the two would have forced this document to either under-explain its concepts for the sake of readability or over-explain them for the sake of a general audience. The public-facing material remains a separate artifact outside Memar's documentation set.

#### Considered and not done (from the removed document-level Drawbacks section)
- **Intentionality is load-bearing but only partially grounded.** The core definition of Agency in [What Is Agency?](./agency.md#what-is-agency) depends on the word "intentionally," and while [Goals and Purpose](./agency.md#goals-and-purpose) offers a partial, working account (a Principal-objective → Agent-interpretation → goals → plan → action chain as a necessary condition), that account is not verified as sufficient, and the document proceeds to use the term throughout as though it were settled. A reader applying this model closely will hit this gap directly.
- **The number of concepts introduced without a closed set of relationships between them is large.** Delegation, Responsibility, Authority, Capability, Context, Knowledge, Trust, Contract, and Accountability are each modeled as distinct, but this document only states pairwise non-equivalences (Capability ≠ Authority ≠ Responsibility, Authority ≠ Responsibility, Autonomy ≠ Agency) rather than a positive account of how the full set composes. A reader cannot currently derive, from this document alone, what combination of these concepts is sufficient for a coherent delegation — only a list of ways delegation can fail when one is missing (see [Failure of Agency](./agency.md#failure-of-agency)).
- **Every example of Agency in this document is drawn from human or organizational contexts, translated to software and AI by analogy.** The contractor, the customer, the engineer, the company — these carry intuitions about intention, understanding, and trust that may not transfer cleanly to a software or AI Agent, and this document does not test where the analogy breaks, only asserts that the underlying structure is shared. This is consistent with the document's stated purpose (model Agency before AI Agent), but it does mean the AI-specific claims here are less load-tested than the human and organizational ones.

#### Related work
- This document has not yet been checked against, or explicitly positioned relative to, several existing bodies of work that plausibly overlap with it and are worth investigating before this document is considered stable. (Migrated from the removed document-level Prior art section)
- **Principal-agent theory**, from economics, which has a long-standing formal treatment of delegation, information asymmetry, and misaligned incentives between a Principal and an Agent — much of it directly relevant to the [Delegation](./agency.md#delegation), [Trust](./agency.md#trust), and [Accountability](./agency.md#accountability) topics in the body, and not yet cross-referenced there.
- **Agent-oriented programming and multi-agent systems research**, a decades-old field in computer science and AI concerned with formalizing exactly the kind of Agent/Principal/Delegation structure this document models informally. This document's claim that "Agent is older than AI" would be considerably stronger with direct engagement with this literature rather than only the general historical argument made in [Historical Continuity](./agency.md#historical-continuity).
- **Speech act theory and philosophy of action**, which has its own long-standing treatment of intentionality — directly relevant to the open question on intentionality now recorded in [agency.handoff.md](./agency.handoff.md#what-exactly-constitutes-intentionality).
- None of these were cited in the body at migration time because none had been verified against this specific model closely enough to cite responsibly; listing them as prior art to investigate, rather than silently omitting them, is intended to make the gap visible rather than to imply it does not exist.
