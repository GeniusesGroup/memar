# Agency Changelog

## Changelog

### Initial draft produced through multi-AI discussion
- Time: 2026-08-04T10:15:00Z
- Type: Created
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, reviewed: originated the modeling question (Agency vs. Agent vs. AI Agent), supplied the working definitions, examples, and counter-examples (the contractor, the writing-ambiguity example, the Hamid Reza Mazandarani exchange), and made the final naming and structural calls (`agency.md` over `agent.md`; `agent_for` as a relationship, not a node; Delegation folded into Agency rather than split into `delegation.md`).
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued, rewrote: co-developed the model through iterative critique across a long conversation, proposed and then reversed several structural drafts (an `agent.md`-centered outline, then an `agency.md`-centered one, then a `delegation.md` split that was itself later rejected), and produced the full first draft of this document's content in prose form at the end of that conversation.

#### Summary
Produced the first complete draft of this document's conceptual content: the Agency/Agent/Principal/`agent_for` model, the Delegation/Responsibility/Authority/Capability cluster, the Human/Organizational/Software/AI/Hybrid Agency taxonomy, the False Taxonomies and Historical Continuity arguments, the Common Modeling Errors catalog, the Terminological Principles glossary, the Open Questions list, and the Working Principles list. Produced as a single flat sequence of 65 numbered sections, without front matter, ahead of this project's Explanation-facet specification.

#### Rationale and alternatives
See the entry below for the alternatives considered and rejected during this drafting process (`agent.md` as the document's name, `delegation.md` as a separate document, `agent_for` as a node) — they are recorded as `Rationale and alternatives` inside the base document itself, under the topics they each concern, rather than only here, since each is tied to a specific, still-referenceable claim in the body and not only to the history of how that claim was reached.

### Migrated into the Explanation-facet structure and reviewed for completeness
- Time: 2026-08-15T14:15:00Z
- Type: Restructured
- Propagates to:
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed: requested the migration to the current documentation format, requested that gaps between the 2026-08-04 discussion and the drafted document be identified and closed, and requested that the reviewing AI's own critiques be added to the document rather than left in chat.
  - [Claude](../CONTRIBUTORS.md#claude) - `Model: claude-sonnet-5` - reviewed, rewrote: reviewed the full 2026-08-04 discussion transcript against the drafted document; reorganized the document from a flat 65-section sequence into the Explanation-facet template (`Abstract` / `Introduction` / `Explanation` topics with per-topic `Discussion` / `Results` / document-level `Discussion`); distributed the former `Open Questions` and `Common Modeling Errors` sections into the specific topics they concern; completed the `Terminology` glossary (added Goal/Purpose, Execution, Decision-Making, Trust, Contract, Accountability, Communication, previously defined in the body but missing from the glossary); expanded `False Taxonomies` with three additional examples raised in the original discussion but not carried into the draft (SOA/Microservices, Relation/Aggregate Root, Content/Semantic); added an explicit `Rationale and alternatives` entry under `Delegation` and under `The agent_for Relationship` documenting the rejected `delegation.md`-as-separate-document and `agent_for`-as-node alternatives, using the reasoning already present in the discussion but not previously written into the document as a rejected alternative; added a new Unresolved Question about this document's relationship to `type.md`'s Type categories; added a new Unresolved Question, under Intrinsic and Delegated Agency, about whether self-directed action is ever fully free of an internal Principal; and added a full document-level `Discussion` section (Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, Future possibilities) containing Claude's own review — not only a report of gaps between the discussion and the draft, but Claude's independent assessment of the model's remaining weak points.

#### Summary
Restructured the document to follow `documentation-explanation.md`'s current template (front matter, `Abstract`, `Introduction` with `Motivation`/`Methodology`, topic-organized `Explanation`, `Results`, document-level `Discussion`). Closed several gaps between the 2026-08-04 discussion and the drafted document: an incomplete `Terminology` glossary, thin `False Taxonomies` examples, and several structural decisions (rejecting `agent.md`, rejecting `delegation.md`, rejecting `agent_for`-as-node) that were reasoned through in discussion but never written into the document as explicit rejected alternatives. Added new content that did not exist in either the discussion or the prior draft: a `Rationale and alternatives` entry for the document's own flat-vs-topic-structure choice, a `Prior art` section naming three literatures this document has not yet been checked against (principal-agent theory, agent-oriented programming / multi-agent systems, speech-act theory), and several new `Unresolved questions` (the `type.md` relationship; whether self-directed action fully escapes an internal Principal; whether this document's own multi-AI production process is itself an instance of the Hybrid Agency it describes).

#### Rationale and alternatives
- **Silently fixing gaps without flagging them as edits (rejected)**: an earlier approach to this edit considered folding the added content into the existing prose so it would read as though it had always been there. Rejected because it would misrepresent provenance — this document's own stated principle, carried over from the 2026-08-04 discussion, is that definitions and design decisions should be traceable to why they were made; silently blending newly-added reasoning into inherited prose would undermine that principle inside the very document that states it. Every addition of substance is instead attributable to this changelog entry.
- **Leaving the reviewer's own critique only in the chat, not in the document (rejected, per explicit request)**: the default in past reviews of this kind had been to report gaps and critique conversationally rather than to write them into the artifact. Rejected here at the person's explicit request; the critique now lives in the document's own `## Discussion` section (`Drawbacks`, `Prior art`, `Unresolved questions`, `Future possibilities`) so it survives independently of this specific conversation.

### Agency and Process execution responsibility model
- Time: 2026-08-17
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified that an execution Agent may be responsible for a bounded portion of a Process without implying a permanent domain-ownership boundary or an `agent_for` relationship; emphasized that a system may have many processing Agents and that responsibility may be dynamically reassigned.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — integrated the resulting model into `agency.md`.

#### Summary
Added an explicit treatment of Agency in Process execution. The document now distinguishes `agent_for` (acting on behalf of a Principal) from execution responsibility, defines Execution Agent as a descriptive use of Agency rather than a new entity type, distinguishes execution responsibility from domain ownership, and records Worker and Actor as possible implementation representations rather than conceptual primitives. Dynamic assignment, partitioning, migration, rebalancing, and Consistent Hashing are documented as execution concerns that follow from responsibility modeling rather than defining Agency.

#### Rationale and alternatives
- **Treating Worker as the primitive execution concept (rejected):** Worker is implementation vocabulary and varies by runtime.
- **Treating Actor as the primitive execution concept (rejected):** Actor Model is a particular execution model and is narrower than Agency.
- **Using `agent_for` for execution responsibility (rejected):** acting on behalf of a Principal and being responsible for advancing a process are distinct relationships.

### Cross-referenced process.md, closing the Worker/Agency gap
- Time: 2026-08-17T00:00:00Z
- Type: Changed
- Propagates to:
  - process.md: Done — reciprocal links added there in the same pass; see process.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: noticed, after today's ChatGPT session added "Agency in Process Execution," that this document and process.md's Concurrency topic cover closely related ground (Worker, execution responsibility, responsibility-before-synchronization) without referencing each other, and asked for a deliberate integration pass rather than leaving the two to develop independently.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: reviewed today's "Agency and Process execution responsibility model" changelog entry and the corresponding body content (Agency in Process Execution, Execution Agent, Agency and Ownership of Process State, Dynamic Assignment, Agency Before Synchronization) against process.md's own, independently-written Concurrency topic; found them consistent in substance (both treat Worker as a non-primitive representation of a more general responsibility concept, both reach a similar escalating decision chain before reaching for synchronization) with no contradiction requiring resolution; added a link from "Agency in Process Execution"'s opening paragraph and from the Worker mention under Execution Agent to process.md's Concurrency topic; added Process to the "Relation to Memar" diagram, which listed System, Module, and Organization but had omitted Process despite this document's own Process-execution content.

#### Summary
Found this document's new Process-execution content substantively consistent with process.md's independently-developed Concurrency topic — both arrived at treating Worker as a representation of a more general responsibility concept, and both reach a similar responsibility-before-synchronization ordering. No content was rewritten to resolve a conflict, since none was found; the two documents were cross-linked instead of left to duplicate each other going forward, and Process was added to this document's own "Relation to Memar" summary diagram, which had omitted it.

#### Rationale and alternatives
Considered merging the "Agency Before Synchronization" chain and process.md's Concurrency decision chain into a single, shared chain cited by both documents, since they overlap substantially. Deferred: the two chains are pitched at different levels of generality (Agency's version is domain-general; Process's version has Concurrency-specific steps — shared mutable state, invariants, scheduling — that don't belong in Agency's more general statement of the same principle), and collapsing them into one shared version is a larger structural change than a same-day integration pass should attempt without dedicated review.
