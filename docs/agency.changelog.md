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
- The three plain-text "Knowledge Management" mentions in the Agency and Knowledge Management topic are now hyperlinks to [Knowledge](../modules/knowledge/knowledge.md), which was renamed from knowledge-management.md and re-scoped to the concept in the same pass.
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
  - [Qwen](../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../CONTRIBUTORS.md#opencode)) - moved

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
- **Speech act theory and philosophy of action**, which has its own long-standing treatment of intentionality — directly relevant to the open question on intentionality recorded at migration time in `agency.handoff.md`, and now carried in the body at [What Is Agency?](./agency.md#what-is-agency).
- None of these were cited in the body at migration time because none had been verified against this specific model closely enough to cite responsibly; listing them as prior art to investigate, rather than silently omitting them, is intended to make the gap visible rather than to imply it does not exist.

---

### Four handoff questions closed by answers already in the body
- Time: 2026-10-04T18:20:54Z
- Type: Fixed
- Propagates to:
  - agency.handoff.md: Done — the intrinsic-vs-relational, Agent-as-role, Agency-without-goals, and role/knowledge-boundary questions left the handoff, each already answered in the body (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- Four entries left [agency.handoff.md](./agency.handoff.md)'s Open Questions; each answer was already carried by this document's body, so no body edit was made.
- *Is Agency intrinsic, relational, or both?* — answered by [What Is Agency?](./agency.md#what-is-agency): both intrinsic and relational manifestations are represented without one replacing the other.
- *Is Agent fundamentally a role?*, with its sub-question on a System exhibiting intrinsic Agency and no Principal — answered by [Terminology → Agent](./agency.md#terminology): "A system that exhibits Agency, especially a system occupying the agent position in an agentive relationship" — the relational position is the case marked "especially", so a System acting on its own behalf is an Agent before any relationship exists.
- *Can a System have Agency without goals?* — answered by [Terminology → Goal / Purpose](./agency.md#terminology): a goal "may originate with a Principal (as a delegated objective) or be self-generated (as an intrinsic objective)", over an Agency whose own definition rests on acting toward objectives.
- *Does a role imply a bounded knowledge space? (Specialization ≠ narrow knowledge)* — answered by [Agency and Organizational Boundaries](./agency.md#agency-and-organizational-boundaries): a role classification "becomes harmful when it prevents communication or implies that knowledge outside the classification is irrelevant".

#### Considered and not done
- **Adding the multipotentialite refinement of the role/knowledge claim to this document's body** — that a role constrains *primary focus*, never the knowledge space an agent must draw on, breadth coming from setting aside upstream abstractions and exercising critical/adaptive/systems thinking rather than from accumulated volume: the removed handoff entry carried this refinement and the body does not state it. Not added here, because the body's existing statement already answers the question the handoff asked, and the refinement's own home is the Role document the handoff's Anticipated Work already schedules — restating it a third time in Agency would duplicate both.

---

### Execution Agent settled as descriptive terminology; responsibility-change cases named
- Time: 2026-10-04T20:11:40Z
- Type: Changed
- Propagates to:
  - agency.handoff.md: Done — both the Execution Agent question and the responsibility-change representation question left Open Questions, each answered in this document's body.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Execution Agent](./agency.md#execution-agent) now states that the term remains descriptive terminology defined in this document rather than a Concept Process defines of its own, since naming an Execution Agent presupposes Agency and Process alike; the subsection carries a cross-link to [Process → Agency and Execution Responsibility](../modules/process/process.md#agency-and-execution-responsibility).
- A new subsection, [Transfer, Reassignment, Takeover, and Replication](./agency.md#transfer-reassignment-takeover-and-replication), added under Agency in Process Execution names the four movements of execution responsibility and states what stays fixed across them — who holds the responsibility changes; the domain entity and the mechanism realizing it do not — cross-linked to [Treating Execution Ownership as Domain Ownership](./agency.md#treating-execution-ownership-as-domain-ownership).
- The two questions left [agency.handoff.md](./agency.handoff.md)'s Open Questions.

#### Considered and not done
- **Promoting Execution Agent to a formal Concept in Process (rejected)**: it can be named only once Agency and Process are already defined, so it fails the same independence test that kept Delegation a topic here rather than a document of its own; the volume of its use is not the criterion.
- **Giving responsibility change a relation name of its own (rejected)**: the cases differ in who holds execution responsibility and in what bounds it, not in the kind of relationship that holds — a new edge name would add vocabulary without changing what is modeled.
- **Modeling concurrent responsibility as an accountability question here (deferred)**: replication leaves more than one Agent responsible for the same state, which raises who is answerable for the outcome; that question remains open in [agency.handoff.md](./agency.handoff.md#how-does-accountability-propagate-through-delegated-agency) and its resolution may still require splitting accountability.

---

### Agency and Type categories placed outside the taxonomy
- Time: 2026-10-04T20:11:24Z
- Type: Fixed
- Propagates to:
  - agency.handoff.md: Done — the "How does Agent/System/Principal relate to Khayyam's Type categories?" open question was removed; [Agency and Type Categories](./agency.md#agency-and-type-categories) is its home, and the Anticipated Work bullet for the worked example now points there instead of at the deleted entry.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- Added `#### Agency and Type Categories` at the end of [Relation to Memar](./agency.md#relation-to-memar), the first link this document makes to `type.md`: the four Type categories classify Types by the semantic role each fulfills, and none of them classifies a System, whose core identity is fixed in [System → System](./system.md#system) rather than by a Type category.
- Stated that Agent and Principal are the endpoint positions of `agent_for` rather than entities carrying an explicit identity and a defined contract, so neither qualifies as a Type.
- Recorded the consequence and its limit together: Agency cuts across the Type categories rather than belonging to one, while which category, if any, realizes a given agentive System is left unanswered and routed to the worked example the handoff already schedules.
- Removed the corresponding Open Questions entry from [agency.handoff.md](./agency.handoff.md); the worked-example bullet that linked to it now links to the new sub-section, keeping the bullet's future work unchanged.

#### Considered and not done
- **Deleting the worked-example bullet along with the question (rejected)**: the document-level Future possibility — a worked example connecting this document to `type.md` — is unmet by this entry and survives it. Only its inline anchor to the removed question changed. The bullet's wording was also left otherwise intact rather than rewritten around the new sub-section, since the work it schedules is unchanged and re-describing it here would pre-empt the example itself.

---

### Agency settled as both an intrinsic capability and a relational condition
- Time: 2026-10-05T07:30:00Z
- Type: Changed
- Propagates to:
  - agency.handoff.md: Done — two questions left Open Questions (property/capability/condition, and Agency versus mere behavior) and the self-directed-action question was narrowed to where the boundary of "external" falls (handoff: no entry of its own).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [What Is Agency?](./agency.md#what-is-agency) now states that both halves of the definition hold and neither replaces the other — the intrinsic capability belongs to the System itself (see [Agency as a Property of Systems](./agency.md#agency-as-a-property-of-systems)), the relational condition is what the agentive relation establishes (see [Agency as a Relationship-Enabled Property](./agency.md#agency-as-a-relationship-enabled-property)) — and carries the consequence that a System which has both is an Agent.
- Added [What Distinguishes Agency from Mere Behavior](./agency.md#what-distinguishes-agency-from-mere-behavior) under that topic, stating the boundary as the intrinsic capability: behavior produced under instruction, on request, or through a fixed transformation remains behavior however elaborate it is, and a thing told to perform a task is not thereby an Agent, because the capability is not in its nature (Omid Hekayati — decided).
- The [Abstract](./agency.md#abstract) no longer lists the property/capability/condition question among the questions deliberately left unresolved; it states the settled claim instead, and the Agent-is-a-role question stays listed as open.
- [agency.handoff.md](./agency.handoff.md) lost the *Is Agency a property, capability, or condition?* and *What distinguishes Agency from mere behavior?* entries; its self-directed-action entry was narrowed to the residue, keeping the internal-delegation redescription available but recording that it cannot dissolve the distinction; and the intentionality entry's pointer at the removed entry now names the new body section.

#### Considered and not done
- **Adopting the internal-delegation redescription as the working account for self-directed action (rejected)**: it describes the act faithfully, but it cannot dissolve the intrinsic/relational distinction, because the criterion is whether the thing itself has the capability (Omid Hekayati — decided).
- **Adding a Working Principles item for the ruling (rejected)**: that list is the fallback for questions still open in the handoff, and this ruling is stated as the definition and its Agent consequence in [What Is Agency?](./agency.md#what-is-agency) rather than as a fallback principle.

#### Deliberation
- The ruling was that Agency is at once an intrinsic capability and a relational condition, that a thing possessing both is what makes an Agent, and that a thing asked or directed to act does not become an Agent when the capability is absent from its nature — offered with the case of a rock told to perform a task, which does not (Omid Hekayati — decided).
- The redescription of a self-directed act as delegation to one of the System's own internal Systems was argued to remain available and admissible under that definition, with the ruling bearing only on whether the redescription dissolves the distinction between intrinsic and relational agency (Space Bunny Alpha — argued) (Omid Hekayati — decided).
- The owner took the three handoff questions as read: the property/capability/condition question answered by "both", the Agency-versus-behavior question answered by the rock test, and the self-directed-action question settled as to the distinction's survival but not as to the boundary of "external" (Space Bunny Alpha — argued).

---

### Intentionality, the boundary of "external", and Agent's document boundary settled from definitions already held

- Time: 2026-10-05T10:12:46Z
- Type: Changed
- Propagates to:
  - agency.handoff.md: Done - three entries left Open Questions: what exactly constitutes intentionality, where the boundary of "external" falls for self-directed action, and whether Agent becomes its own document.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- [What Is Agency?](./agency.md#what-is-agency) now defines the term its own definition had rested on without definition. Intentionality is the System's own holding of an objective and determining of the means toward it, and the chain from a desired outcome through an interpreted objective, intermediate goals, and a plan to action is Agency's structure rather than its criterion.
- [Agency as a Property of Systems](./agency.md#agency-as-a-property-of-systems) now states that whether a Principal is external to a System that acts is relative to where that System's boundary is drawn for the analysis in hand, so a Principal that is one of the System's own internal Systems is not external to it and the internal-delegation redescription states where the boundary was drawn rather than dissolving the intrinsic/relational distinction; where both descriptions fit the same act, the model works with both.
- [Methodology](./agency.md#methodology) now records that Agent does not pass the independence test this document already applies to Delegation and to Execution Agent, because an Agent is the thing that has both halves of Agency and so cannot be defined before Agency is.

#### Considered and not done
- **Leaving the sufficiency half of intentionality open (rejected)**: the body already holds that behavior a System produces under instruction, on request, or through a fixed transformation remains behavior however elaborate it is, and that the criterion is whether the capability is in the System's nature. Together these force the answer - a System describable as running the chain without the capability in its nature is exhibiting behavior, not intentionality - so the chain cannot be what establishes it.
- **Reading the internal-delegation redescription as settling which of the two descriptions the model works with (rejected)**: it fixes where the boundary was drawn, not that one description displaces the other. The body already holds that intrinsic and delegated Agency are not mutually exclusive kinds and can coexist, so both remain available where both fit.
- **Deferring Agent's document boundary until Role, Permission, and Contract are written (rejected)**: the test this document applies is whether a Concept can be defined without first defining another, which is a property of Agent's own definition and not of how many later documents reference it. Waiting for the reference count to grow would leave a question whose answer cannot change with it.

---

### False taxonomies moved to Modeling; the professional-category instance stays
- Time: 2026-10-12T07:45:14Z
- Type: Changed
- Propagates to:
  - modeling.md: Done — [False Taxonomies Hide Shared Structure](./modeling.md#false-taxonomies-hide-shared-structure) holds the concept and the general examples.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, applied

#### What changed
- *False Taxonomies* became [Professional Categories as False Taxonomies](./agency.md#professional-categories-as-false-taxonomies): the Frontend/Backend instance and its consequence for agency stay; the general definition and the SOA/Microservices, Relation/Aggregate Root, and Content/Semantic examples moved to Modeling, which owns classification.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:44:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to [agency.md](./agency.md), [agency.handoff.md](./agency.handoff.md), and this changelog (the False Taxonomies move is out of scope and was not judged). The settled answers hold against the definitions they cite ([System → Key Properties](./system.md#key-properties) boundary as an analytical choice, [Type → Categories of Type](./type.md#categories-of-type)), each sits in the document that owns its subject, each carries its reason, and each has a changelog entry above; no changelog entry was removed, and the one edited line (the speech-act bullet) only repoints a link whose target was removed. `memar content check` reports no problem.
- [agency.md](./agency.md) Abstract: it still named "whether Agent is fundamentally a role rather than a type" as the central open question, although that question left the handoff and is answered by the body; it now names accountability propagation, which the handoff still holds.
- [agency.md](./agency.md) Terminology → Agent: it defined Agent as a System that "exhibits Agency, especially" one in an agentive relationship, which contradicts [What Is Agency?](./agency.md#what-is-agency), where an Agent has both the intrinsic capability and the relational condition; it now states the two halves and links there.
- [agency.handoff.md](./agency.handoff.md): removed *Does self-directed action ever fully escape delegation…*. The entry above dated 2026-10-05T10:12:46Z records it settled and moved to the body ([Agency as a Property of Systems](./agency.md#agency-as-a-property-of-systems)) but the entry had only been narrowed and still called the boundary of "external" open; its content is carried by that body section and by the two changelog entries of 2026-10-05.

#### Considered and not done
- **Adding the multipotentialite role/knowledge refinement to the body**: left as the earlier entry decided; its home is the Role document scheduled in Anticipated Work.
