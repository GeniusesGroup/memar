# System Changelog

## Changelog

### Initial synthesis
- Time: 2026-07-14T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Depends_on: this document builds directly on the terminology philosophy, classification layers, and concept-first thinking established there; its definitions must stay consistent with those principles.
  - [Protocol](./protocol.md) — Reference: this document includes a brief pointer to Protocol's definition; the Protocol document is the authoritative source.
  - [Modeling](./modeling.md) — Extends: this document defines Model and Abstraction at the conceptual level; Modeling builds on those definitions to specify how Memar performs modeling as an architectural activity.
  - [Framework](./framework.md) — Depends_on: full treatment of Framework's relationship to Architecture and System lives there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — claimed, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, high effort) — rewrote
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed

#### What changed
- Introduced foundational definitions for System, Structure, Architecture, Technology, Knowledge, Science, Model, Abstraction, Protocol (by reference), Framework (by reference), and Implementation; established the conceptual graph relating these concepts; positioned this document as a prerequisite for all subsequent conceptual documents in the Memar ecosystem.
- Technology was defined at its core as applied knowledge (Omid Hekayati).
- The initial draft was produced (ChatGPT, Super Z).
- Contributor inputs were synthesized into a coherent document; the Knowledge, Model, Framework, and Implementation sections were added; Relationships Between Concepts and Discussion were composed, with critical review and refinement (Super Z).
- The "shaped by" edge was phrased bidirectionally, and the document was connected to the Terminology document's mental-models principle (ChatGPT).
- The Meta-Principle was reformulated; Structural vs. Purposive Abstraction was introduced, grounded in Maturana and Varela; Omid's open/closed/isolated proposal was expanded into the full System Openness subsection; a reconciliation pass with the Framework document removed the residual "Framework is a System" claim; contributor-attribution errors were corrected (Claude).

#### Deliberation
- The need for this document was initiated (Omid Hekayati).
- The inseparability of System and Architecture was claimed (Omid Hekayati).
- A lived-experience critique connecting technology and lifestyle was argued (Omid Hekayati).
- War, discourse, and governance were claimed as technologies (Omid Hekayati).
- The ISA example was offered as a test case for Architecture-as-System (Omid Hekayati).
- "Reality is the best guess one System can make of another" was claimed as the grounding intuition for structural abstraction (Omid Hekayati).
- The Framework vs. Sub-Framework distinction and a working test for Architecture legitimacy were claimed (Omid Hekayati).
- The reintroduction of the open/closed/isolated systems classification was originally proposed, later expanded into System Openness (Omid Hekayati).
- Candidate definitions for System, Architecture, Technology, Protocol, and Abstraction were claimed (ChatGPT).
- The Conceptual vs. Graph Centrality distinction was raised (ChatGPT).
- Edge Types were identified as an emerging topic (ChatGPT).
- Premature dedicated documents for Edge Types and Abstraction were argued against (ChatGPT).
- An explicit statement of the ISA-legitimacy departure from industry usage was pressed for (ChatGPT).
- A critical, structural review of the draft was given (Claude).
- The Abstraction/Model front-matter contradiction was identified (Claude).
- The Framework-as-System vs. Framework-as-Aspect distinction was identified (Claude).

#### Considered and not done
- **Defining only System and Architecture, leaving the other concepts to their own documents (rejected).** These concepts form a coherent conceptual graph; defining System and Architecture alone would produce a document that is internally incomplete and forces every subsequent document to independently establish its own conceptual context.
- **Using existing standard definitions without adaptation (rejected).** No single existing standard provides a complete, mutually consistent set of definitions for everything Memar needs.

---

### Refinement round — Meta-Principle, Openness, Edge Types, and terminology bridge
- Time: 2026-07-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued

#### What changed
- Framework and Architecture were defined as co-equal aspects of System (Constraint Space vs. Decision Space).
- The "shapes" in "Architecture shapes a System" was clarified as bidirectional and iterative, not one-way control, using classical-architecture and ISA examples.
- An internal contradiction was corrected: Abstraction had been stated as deferred to the Modeling document but was, in fact, already fully defined here.
- The Meta-Principle was refined from an unconditional claim ("Architecture and Framework are Systems") to a qualified one ("...*may themselves be modeled as* Systems when they exhibit the requisite properties").
- The "shaped by" edge definition was updated to state its bidirectional character at the point of definition rather than only in the change history.
- The bridge to the Terminology document's "terminology shapes mental models" principle was added.
- A lightweight Edge Taxonomy note was added.

#### Deliberation
- The Conceptual vs. Graph Centrality distinction was raised and Edge Types were identified as an emerging topic that may eventually need its own dedicated document (ChatGPT — see attribution correction below: this was originally misattributed to Claude and later corrected).

---

### Framework-as-System regression fix
- Time: 2026-07-18T00:00:00Z
- Type: Fixed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- Fixed a conceptual regression in how Framework's relationship to System was stated, restoring consistency with the general principle (also applied to Technology and to Architecture in the Meta-Principle) that System is never baked into a concept's core definition — it is, at most, a secondary lens a sufficiently rich instance of a concept may be examined through.
- An earlier revision had treated "Framework as System" as one of two equally valid senses of the word Framework, contradicting the Framework document's atomic definition ("a framework is a description of a system"); this was corrected.
- Framework as Aspect remains the account of how a framework's constraints appear within a built System's Structure; Framework Considered as a System is now presented explicitly as optional and instance-specific, not a co-equal sense of the word.
- The "shaped by" edge type definition was softened correspondingly, from an unconditional "Architecture is itself a System" to a hedged reading.

---

### Attribution corrections, Description definition, and Systems Thinking note
- Time: 2026-07-20T00:00:00Z
- Type: Fixed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed

#### What changed
- Two contributor-attribution errors in the change history were corrected: the ISA example was introduced by Omid Hekayati, not Claude; and the Conceptual Centrality vs. Graph Centrality distinction and the identification of Edge Types as an emerging topic were raised by ChatGPT in a later review round, not by Claude.
- A missing definition for "Description" — "a statement that represents something in words, or more broadly in any symbolic form" — was added at the point where Framework's definition first depends on it.
- "A Note on Systems Thinking" was added as reader guidance to address a recurring source of confusion, distinguishing casual systems-thinking language — the explanatory-level looseness of "almost anything can be called a System" — from this document's formal definitional discipline, the one the Meta-Principle enforces.

#### Deliberation
- Both attribution errors were flagged for correction (Omid Hekayati).

---

### Process extracted to its own standalone document
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - process.md: Done — process.md now holds the full definition, guide-level reasoning, and reference-level treatment this document's `### Process` section previously held in full.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The previously-recorded decision (item 1 of the old Change Rationale: "Defining System before other concepts... to avoid circular dependencies") was reversed specifically for Process, once its scope outgrew what an inline subsection could hold without either truncating the analysis or making this document disproportionately large.
- The `### Process` subsection was shortened to a pointer plus only the System-specific half of the Process↔System relationship (a system without processes is a heap, not a system; a system is defined by its processes as much as by its elements).
- The process-nesting examples, the full definition, and the process-before-mechanism reasoning were moved to process.md in full rather than duplicated.
- The reversal of this document's own prior Rationale and alternatives entry rejecting a standalone Process document was recorded explicitly, rather than left silently outdated.
- The dependency between System and Process is now asymmetric rather than symmetric: this document keeps System's own definition and its half of the Process↔System relationship; process.md keeps Process's own definition and its half of that same relationship.

#### Deliberation
- Process was confirmed to warrant a standalone document, given how far its scope had grown beyond what an inline subsection here could hold (Omid Hekayati).

#### Considered and not done
- **Leave the original rejection in place and merge the growing Process content back into this document (rejected)**: considered, then rejected once the content had reached a size and depth (failure/rollback, concurrency/locking, retry, cancellation, asynchrony, each analyzed against real distributed-systems discussions) that would have made this document disproportionately large relative to its other topics.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - protocol.md: Pending — not yet migrated to the current Explanation-facet template.
  - terminology.md: Pending — not yet migrated to the current Explanation-facet template.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document is now structured per `documentation-explanation.md`: restructured from `Summary/Motivation/Guide-level Explanation/Reference-level Explanation/Discussion/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`).
- Its Citations, Contributor roster, and full change history — previously living in front matter and a document-level `## Change Rationale` — now live entirely in this file: front-matter `Citations` and `Contributor(s)`/`Tasks` were moved into this changelog's entries.
- The 26-item `## Change Rationale` list was migrated into the changelog entries above, grouped by inferred revision round rather than one entry per numbered item, since the original list had no per-item timestamps.
- Discussion sub-heading casing was normalized throughout (`Rationale and Alternatives` → `Rationale and alternatives`, `Prior Art` → `Prior art`, `Unresolved Questions` → `Unresolved questions`) to match the template.

#### Deliberation
- The migration of every old-style document touched going forward to the current structure, with a paired changelog file, one document at a time, was requested (Omid Hekayati).

#### Considered and not done
- **Inventing precise timestamps for the 26 migrated items (rejected)**: the original `## Change Rationale` list had no per-entry timestamps, only relative order, and several items span review rounds rather than single sessions; entries above are grouped by inferred round and dated approximately instead — correct the dates above if more precise ones are known. This is the same open question `documentation-changelog.md`'s own Unresolved Questions section names for migrated historical entries.

---

### Responsibility added as a Key Property, closing a gap shared with process.md and modularity.md
- Time: 2026-08-16T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — Observation topic and Relationship to Other Concepts updated to reference this section.
  - modularity.md: Done — Module Identity and Responsibility, and the Module Among Related Concepts table, updated to reference this section instead of using "responsibility" informally.
  - modeling.md: Done — the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling now cites this section.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- Responsibility was added as a new Key Property of System: a part's Purpose expressed relative to the larger System containing it, not a separate primitive.
- A "When Is a Responsibility Coherent?" subsection was added stating what actually makes a Responsibility coherent — an independent behavioral boundary and lifecycle, evaluated against a stated concern rather than declared — since asserting coherence without naming that concern makes an unfalsifiable claim; grounded in the operational criterion already present in `modeling.md`'s Domain Decomposition topic ("independent responsibility, behavioral boundary, or lifecycle") and cross-referenced to `process.md`'s Observation topic for the observer-relativity argument.
- This closes a gap that had `modularity.md`, `process.md`, and `modeling.md` each leaning on the word "responsibility" without any of the four documents defining it.
- A corresponding Unresolved question was added flagging that `modularity.md`, `process.md`, and `modeling.md` all used the word informally before this definition existed and should be checked against it.

#### Deliberation
- While reviewing modularity.md against process.md and modeling.md, it was identified that "responsibility" was load-bearing in all three documents without a formal home anywhere (Omid Hekayati).
- Adding it here was approved specifically because this is the project's mother document for these concepts, not because of any status difference between the documents involved (Omid Hekayati).
- The correction that modeling and observation form a cycle rather than two strictly separated phases was supplied — a part may first be modeled naively, then revised once observation shows its boundary does not hold (Omid Hekayati).
- The provenance of the falsifiable/unfalsifiable distinction between "this boundary was drawn for this concern, for this observer" and "this module has high cohesion" was supplied: it originates from a LinkedIn discussion Omid took part in as a commenter, not as the original post's author (Omid Hekayati).

#### Considered and not done
- **Leave Responsibility informal (rejected)**: considered on the grounds that `modeling.md`'s existing "independent responsibility, behavioral boundary, or lifecycle" phrasing was already operational enough in context; rejected because three documents were each free to drift the term in a different direction without a shared definition to check against, which is exactly the coordination risk this round of review was meant to close.

---

### Knowledge definition now defers to the Knowledge document for its detailed treatment
- Time: 2026-09-05T11:30:00Z
- Type: Changed
- Propagates to:
  - knowledge.md: Done — created as the detailed home of the concept in the same pass (see its changelog).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- The Knowledge definition in the Knowledge and Science topic now points to [Knowledge](./knowledge.md) for the detailed treatment of the concept — the same deferral pattern this document already uses for Protocol ("defined in detail in its Protocol document").
- The foundational one-line definition itself is unchanged and remains here, because other documents depend on this document's concept web.

#### Deliberation
- The Knowledge Management document was directed to be renamed and re-scoped to Knowledge, making this document's one-line definition the foundational layer and knowledge.md the detailed treatment (Omid Hekayati).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - system.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only; every Discussion wrapper was dissolved — the document-level `## Discussion` and nine topic-level wrappers (System, Structure, Process, Architecture, Technology, Knowledge and Science, Abstraction, Implementation, Relationships Between Concepts) — with each block's content either folded inline at the claim it supports or relocated below and to the paired handoff, nothing dropped.
- The document-level Terminology Layer Placement content is now a body topic ([system.md → Terminology Layer Placement](./system.md#terminology-layer-placement)): it states each concept's current terminology-layer classification, which serves the current-state reader, not the audit reader.
- The Architecture topic's Drawbacks content is now the body subsection [Architecture → Architectural Weight as a Spectrum](./system.md#architectural-weight-as-a-spectrum) — a current-state mitigation claim that the working test and the architecture open questions depend on; the Implementation topic's Drawbacks claim (the architecture/implementation distinction is between kinds of decisions, not kinds of people, and the architects/developers separation is not endorsed) is now inline at the end of Implementation Is Not Architecture for the same reason.
- The Architecture topic's Prior-art ISA worked example is now the body subsection [Architecture → The Instruction Set Architecture Example](./system.md#the-instruction-set-architecture-example), because "A Working Test" calibrates on it; the block's ISO/IEC 42010 comparison went to Related work below.
- Rejected alternatives, considered-and-answered objections, and accepted cost trade-offs from the retired wrappers are preserved below under Considered and not done; prior-art and comparative surveys and the retired document-level Naming Conventions note are preserved below under Related work.
- Twenty-five open questions (twenty-two from the topic-level wrappers, three document-level) and eight anticipated-work items (the document-level Future possibilities list) moved to [system.handoff.md](./system.handoff.md), grouped by their source topic with per-topic numbering preserved.
- The document-level `Rationale and alternatives` items were not duplicated here: both rejected alternatives are already recorded in this file's Initial synthesis entry, and the synthesis rationale itself stands in the body's Methodology.
- The Process topic's Unresolved-questions wrapper held only a migration pointer and was dropped after verification that its targets — the process-composition and Process–State questions and the Process↔System circularity question — are now tracked in [process.handoff.md](./process.handoff.md).
- Body pointers that named the retired sections were repointed: Methodology's synthesis rationale to this file's Initial synthesis entry; the Structure arrangement-of-parts note, the Architecture working-test note, and the Edge-Types formalization note to the paired handoff; the Framework-as-Aspect open-question pointer to [framework.handoff.md](./framework.handoff.md); the "How to Read" guide now describes the changelog/handoff split in place of per-topic Discussion wrappers.

#### Considered and not done
- **The objection that System's generality drains the term's discriminative power (considered and answered; migrated from the System topic's Drawbacks)**: the term's usefulness comes not from narrowing the set of things it applies to, but from providing a common analytical lens — relationships, boundaries, emergence, purpose — through which very different entities can be compared, reasoned about, and designed; a definition that excluded, say, social systems would force Memar to treat software architecture and organizational architecture as fundamentally different activities, when in practice they share deep structural similarities that the general definition makes visible.
- **Restrict "system" to computational or software entities (rejected; migrated from the System topic's Rationale and alternatives)**: consistent with much industry usage, but it would sever the conceptual connection between software architecture and other forms of system design (organizational, infrastructure, process) that Memar explicitly recognizes as architecturally relevant, and it would contradict the Terminology document's principle that concepts should outlive technologies.
- **Restrict "system" to entities with clearly defined boundaries (rejected; migrated from the System topic's Rationale and alternatives)**: many real-world systems (ecosystems, markets, organizational cultures) have fuzzy, contested, or observer-dependent boundaries; excluding them would impoverish Memar's conceptual vocabulary for describing the environments in which software systems operate.
- **Adopt a purely mathematical definition from dynamical systems theory (rejected; migrated from the System topic's Rationale and alternatives)**: while mathematically precise, it would exclude many systems that are architecturally relevant but do not have easily formalizable state spaces — organizational systems, governance systems, and social mechanisms being primary examples.
- **Define Process as a standalone document (originally rejected; reversed 2026-08-15 by the "Process extracted to its own standalone document" entry; migrated from the Process topic's Rationale and alternatives)**: the original rejection argued "Process cannot be defined without reference to System. A standalone Process document would either duplicate System's definition or silently depend on it, creating the same circular dependency problem this document exists to prevent." That argument correctly rules out a *symmetric* duplication; the 2026-08-15 reversal made the dependency asymmetric instead — this document keeps System's own definition and the System-specific half of the Process↔System relationship, `process.md` keeps Process's own definition and the Process-specific half, and neither re-derives the other's core definition. Whether this asymmetry fully eliminates the circularity, or only relocates it, is not yet settled — tracked in [process.handoff.md](./process.handoff.md)'s Process and System open questions.
- **Define Process as a sub-concept under Protocol (rejected; migrated from the Process topic's Rationale and alternatives)**: Protocol governs processes, but Process is not a sub-concept of Protocol. Processes exist whether or not they are governed by protocols; many processes in natural, social, and organizational systems operate without any formal protocol governing them. Process is a foundational concept that Protocol depends on, not the reverse.
- **Restrict architecture to "high-level design" (rejected; migrated from the Architecture topic's Rationale and alternatives)**: the most common industry definition, but it creates a false distinction between "architectural" decisions and "implementation" decisions that does not hold under scrutiny — many decisions made during implementation have architectural consequences, and excluding them from the architectural domain means those consequences go unexamined.
- **Define architecture as "the structure of a system" (rejected; migrated from the Architecture topic's Rationale and alternatives)**: this confuses a system's structure with the process and decisions that produced it. A system's structure is a snapshot; architecture is the reasoning, constraints, and trade-offs that the snapshot embodies.
- **Define architecture as "the decisions that are expensive to change" (rejected; migrated from the Architecture topic's Rationale and alternatives)**: pragmatically useful as a heuristic, but a consequence-based definition that can only be applied retrospectively — a decision is not known to be expensive to change until after it has been made and the attempt to change it has been evaluated, while architecture as a discipline needs a definition that can be applied prospectively.
- **The objection that "technology" becomes nearly synonymous with "applied knowledge" (accepted trade-off; migrated from the Technology topic's Drawbacks)**: Memar accepts this deliberately; the alternative — restricting "technology" to physical or computational artifacts — creates a conceptual blind spot, making it impossible to reason precisely about the technological character of governance, discourse, lifestyle, and other non-artifact systems, even though these systems are developed, maintained, and evolved through the same kind of applied knowledge that produces physical artifacts. The cost of missing this connection is higher than the cost of using a broad definition.
- **Restrict technology to physical artifacts and software (rejected; migrated from the Technology topic's Rationale and alternatives)**: the most common usage, but it excludes methods, processes, organizational practices, and social mechanisms that are clearly developed through applied knowledge and directed at specific goals — the defining features of technology.
- **Define technology as "tools and their application" (rejected; migrated from the Technology topic's Rationale and alternatives)**: this conflates the tool (artifact) with the knowledge that produced it, perpetuating the Tool-First Thinking pattern the Terminology document identifies as a primary source of architectural error.
- **Define technology as "the application of science" (rejected; migrated from the Technology topic's Rationale and alternatives)**: while historically suggestive, it implies that technology requires prior scientific understanding, which is not always the case — many technologies predate the scientific understanding of why they work, and craft knowledge, trial-and-error engineering, and empirical refinement can produce effective technologies without a fully developed scientific theory.
- **The contributor learning burden of science-grounded architectural reasoning (acknowledged cost; migrated from the Knowledge and Science topic's Drawbacks)**: increasing the learning burden is a real cost that Memar acknowledges — not every contributor needs to become a domain scientist, but every contributor needs enough scientific literacy to distinguish a concept from its implementation and to evaluate whether a technology's claims about a concept are grounded in the underlying science or are marketing-level simplifications.
- **Base architectural reasoning on practical experience alone (rejected; migrated from the Knowledge and Science topic's Rationale and alternatives)**: practical experience is valuable but is subject to cognitive biases, survivorship bias, and the difficulty of distinguishing correlation from causation in complex systems; science provides mechanisms for correcting these biases that practical experience alone does not.
- **Treat all knowledge sources as equally valid (rejected; migrated from the Knowledge and Science topic's Rationale and alternatives)**: this would eliminate the ability to evaluate the quality of evidence behind a claim; the Terminology document's distinction between Scientific, Technology, and Business terminology exists precisely because different knowledge sources have different validation mechanisms and different levels of reliability.
- **The conceptual overhead of teaching abstraction as a first-class concern (acknowledged cost; migrated from the Abstraction topic's Drawbacks)**: contributors must learn not only how to use abstractions but how to evaluate their boundaries, their leakage patterns, and their suitability for specific purposes — a real cost, particularly for newcomers accustomed to treating abstractions as opaque, leak-proof boundaries provided by a framework or language runtime.
- **Treat abstraction as an implementation detail (rejected; migrated from the Abstraction topic's Rationale and alternatives)**: the default in many software frameworks, where abstractions are provided by the framework and treated as opaque by the user; this works until the abstraction leaks, at which point the user is unable to reason about the failure because they were never expected to understand what the abstraction hides — unacceptable for a framework whose stated goal is to improve reasoning quality.
- **Treat implementation as part of architecture (rejected; migrated from the Implementation topic's Rationale and alternatives)**: while every implementation decision has some architectural dimension, treating all implementation as architecture would eliminate the useful distinction between decisions that affect the system's properties and decisions that do not; the distinction is not about importance — an implementation bug can be as consequential as an architectural flaw — but about the kind of reasoning required to evaluate and make each type of decision.
- **The communication cost of a graph model over a linear chain (accepted trade-off; migrated from the Relationships Between Concepts topic's Drawbacks)**: a graph is inherently harder for readers expecting a simple ordering to internalize, but the simplicity of a linear chain is deceptive — it creates false confidence in a hierarchy that does not exist, and that false confidence propagates into architectural reasoning as an unconscious assumption that some concepts are "above" others.
- **Present the concepts as a linear dependency chain (rejected; migrated from the Relationships Between Concepts topic's Rationale and alternatives)**: a linear chain implies concepts can be ordered from "most fundamental" to "most derived" with each depending on exactly one predecessor — false: Architecture depends on System but also on Knowledge, Technology, and Process, and Modeling on Architecture but also on Abstraction and System; presenting them as a chain forces a tree-shaped mental model the rest of the document contradicts.
- **Present the concepts as a flat list with cross-references (rejected; migrated from the Relationships Between Concepts topic's Rationale and alternatives)**: a flat list does not convey the relationship structure at all, leaving readers to infer it, which produces exactly the kind of hierarchical misunderstanding the section exists to prevent.
- **Present the concepts as a taxonomy (rejected; migrated from the Relationships Between Concepts topic's Rationale and alternatives)**: a taxonomy implies mutually exclusive categories, but these concepts overlap — Modeling and Architecture, Protocol and Framework, Technology and Implementation — and a graph accommodates overlap naturally through multiple edge types.
- **Separate System and Architecture into independent documents (considered and rejected; migrated from the document-level Discussion subsection "Why a Single Document for These Concepts?")**: every statement about architecture is implicitly a statement about the system being architected, and every statement about how to understand a system is implicitly an architectural statement; attempting to define System without reference to Architecture produces a definition that is inert — it describes what a system is but not why the distinction matters or how the concept is used — while defining Architecture without a prior definition of System forces Architecture to define its own object, which either duplicates System's definition or silently assumes it; a single document defining both concepts and their relationship is therefore more coherent than two documents each pretending the other does not exist.
- **Splitting the remaining concepts into their own documents, with diminishing force (considered and rejected; migrated from the same document-level subsection)**: Technology could plausibly be separated, but its definition is so closely tied to System (technology develops systems) and to Knowledge/Science (technology is applied knowledge) that separating it would create circular dependencies; Model and Abstraction are included because they are the primary mechanisms through which architectural reasoning operates and because the Modeling document depends on both being defined; Protocol is included only as a brief pointer to its own document, to complete the conceptual map; Framework is included with a brief definition and a link to its dedicated document, which carries the full Framework-Architecture co-equal treatment; Implementation is included because distinguishing it from Architecture is a frequent source of confusion and it plays a central role in the conceptual relationship structure.
- **Defining many concepts in one document, with the risk that some receive less scrutiny than a dedicated document would give them (accepted risk; migrated from the document-level Drawbacks)**: accepted because the alternative — defining each concept in isolation — creates the circular-dependency problem recorded in the entry above, and because this document's primary purpose is to establish a shared vocabulary, not the final, exhaustive treatment of each concept; concepts requiring deeper treatment already have or are expected to receive dedicated documents ([Protocol](./protocol.md), [Framework](./framework.md), and [Modeling](./modeling.md)).

#### Related work
- **System definition (migrated from the System topic's Prior art)**: consistent with general systems theory as articulated by von Bertalanffy ("General System Theory," 1968), Boulding ("The World as a Total System," 1985), and Checkland ("Systems Thinking, Systems Practice," 1981), and with the IEEE standard definition of a system as "a collection of components organized to accomplish a specific function or set of functions" (IEEE Std 610.12), though this document's definition is broader in that it does not restrict the function to be specified in advance and does not require the components to be physical.
- **Architecture definition (migrated from the Architecture topic's Prior art)**: ISO/IEC 42010:2022 defines architecture as "the fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution"; this document's definition is consistent with that standard but emphasizes the process dimension more explicitly — architecture is not only what the system is, but how it came to be that way and how it will continue to change. (The same block's ISA worked example, a premise the body's working test depends on, was folded inline into the body instead.)
- **Technology definition (migrated from the Technology topic's Prior art)**: consistent with the philosophy of technology as articulated by Ellul, Mumford, Heidegger ("The Question Concerning Technology," 1954), and the UNESCO definition of technology as "the know-how and creative process that may assist people to exploit tools, resources and systems to solve problems and to enhance their control over the natural and made environment in an endeavor to improve the human condition"; also consistent with the Terminology document's definition of Technology Terms.
- **Science–knowledge–technology relationship (migrated from the Knowledge and Science topic's Prior art)**: explored extensively in the philosophy of science (Popper, "The Logic of Scientific Discovery," 1959; Kuhn, "The Structure of Scientific Revolutions," 1962; Lakatos, "The Methodology of Scientific Research Programmes," 1978) and the philosophy of technology (as cited in the Technology entry above).
- **Abstraction theory (migrated from the Abstraction topic's Prior art)**: developed in the literature on abstract data types, information hiding (Parnas, "On the Criteria to Be Used in Decomposing Systems into Modules," 1972), and abstraction barriers; the philosophical treatment of abstraction as a cognitive process is developed in the cognitive science literature (e.g., Hofstadter, "Gödel, Escher, Bach," 1979); the structural-versus-purposive distinction is consistent with Maturana and Varela's concept of structural coupling ("Autopoiesis and Cognition," 1980; "The Tree of Knowledge," 1987), in which an observing system's own structure determines which perturbations from another system it is even capable of registering, independent of any purpose the observer might later apply to what it registers.
- **Architecture/implementation distinction (migrated from the Implementation topic's Prior art)**: discussed in the software architecture literature (Bass, Clements, and Kazman, "Software Architecture in Practice," various editions) and implicit in the ISO/IEC 42010 standard.
- **Document-level approach (migrated from the document-level Prior art)**: establishing a shared vocabulary before proceeding to domain-specific specifications is common in standards-setting bodies; the ISO/IEC 42010 standard for architecture description provides definitions of "system" and "architecture" broadly consistent with this document, though this document's definitions are broader in several respects (particularly the inclusion of non-computational systems and the lifecycle-spanning definition of architecture), while the IEEE standard glossary of software engineering terminology is narrower, being restricted to software — this document draws on both traditions but is not bound by either.
- **Naming conventions (migrated from the document-level Naming Conventions note)**: this document proposes no naming conventions for code-level identifiers; the concepts defined there are foundational and their names (System, Architecture, Technology, Model, Abstraction, Protocol, Framework, Implementation) are treated as common English words whose meaning within Memar is defined by the document, not by any naming convention.

---

### Established the Ecosystem definition
- Time: 2026-09-10T11:32:04Z
- Type: Added
- Cited:
  - [Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance) — Evidence: the four-element authority requirement (boundary, distinctions, colloquial acknowledgment, rationale) the new topic follows.
  - [Terminology → Business Terms](./terminology.md#business-terms) — Reference: already lists ecosystem movements among its examples, which the topic's colloquial-usage note leans on.
- Propagates to:
  - software.md: Done — "software ecosystem" read through the definition; the founding interim ban superseded (software.changelog.md).
  - software.handoff.md: Done — the ecosystem terminology-decision item removed as graduated.
  - terminology.md: Done — one informational pointer at the governance section's Memar-ecosystem use.
  - framework.md, protocols/networking.md, khayyam-runtime.md: Done — claim-bearing Memar-ecosystem uses anchored.
  - modularity.md: Done — the one semantic divergence the audit found reworded.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, rewrote

#### What changed
- New concept topic: **Ecosystem** — a System whose constituents are themselves Systems interacting through relationships within a shared environment the ecosystem comprises, the whole's Structure (its capabilities and constraints) fixed by no design, single or collective, and emergent from those interactions. Key properties: constituents are Systems (designed artifacts qualify — what is excluded is a whole whose Structure a definition fixes); the environment sits inside the boundary; a center of gravity is not a designer. Distinctions from Framework, community, platform, and market; the industry's marketing sense acknowledged as a Business Term and excluded.
- Structure conformity verified and stated in the topic: Structure carries its defined sense — the capabilities and constraints a System exposes and enforces — and the definition's claim is about the *origin* of whole-level Structure (emergent rather than laid down by a definition), not a second meaning of the word (Omid Hekayati required the check).
- Concepts at a Glance gained the ecosystem bullet; Terminology Layer Placement classifies ecosystem as a Scientific Term (ecology origin, extended along the same structural lines rather than a coined sense); the biological-ecosystem example under System's Purpose property now links to the topic.
- The Motivation's bare "the most fundamental terms in the ecosystem" was reworded to name its referent ("Memar's conceptual foundation") — one of two semantic divergences the framework-wide audit of the word found (the other is modularity.md's, propagated above).
- The definition was reached by candidate testing per the Protocol document's method: the minimal system-of-systems form was rejected (admits products — modules are Systems), the self-governed-constituents form was rejected (expels designed artifacts, which are legitimate constituents), and the center-of-gravity form was rejected (widens the boundary instead of fixing it).

#### Deliberation
- Defining the word here, rather than leaving it ordinary-language or banning it, was decided after the audit showed the corpus's ~120 body uses conforming to the structural sense; software.md's founding session had recorded the word as undefined pending a decision, and this entry is that decision (Omid Hekayati — decided).
- The placement here rather than in terminology.md was directed with the layering constraint: terminology is the more foundational document and must not depend on this document's definitions; its reference to the ecosystem concept is informational only (Omid Hekayati — directed).
- Anchoring was limited to where a cold reader could misread (the Memar-ecosystem uses that carry claims) rather than applied to every occurrence; the external-industry uses stay ordinary-language per the Default Meaning rule (Omid Hekayati — directed).
- An initial draft of this round gave the word-level fixes (the anchors, the terminology pointer, the two rewordings) one changelog row each in their own artifacts; the owner flagged the rows as Trivial-changes violations — a fix with nothing of its own to audit takes no entry and no standalone commit, so the fixes ride this entry, which states their outcomes, and their changelogs carry no rows (Omid Hekayati — corrected).

