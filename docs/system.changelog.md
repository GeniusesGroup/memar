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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, claimed: initiated the need for this document; core definition of Technology as applied knowledge; the inseparability of System and Architecture; the lived-experience critique connecting technology and lifestyle; war/discourse/governance as technologies; the ISA example as a test case for Architecture-as-System; "reality is the best guess one System can make of another" as the grounding intuition for structural abstraction; the Framework vs. Sub-Framework distinction; the working test for Architecture legitimacy; the original proposal to reintroduce open/closed/isolated systems classification, later expanded into System Openness.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — claimed, argued: initial draft; candidate definitions for System, Architecture, Technology, Protocol, Abstraction; bidirectional phrasing for the "shaped by" edge; the Conceptual vs. Graph Centrality distinction; identified Edge Types as an emerging topic; argued against premature dedicated documents for Edge Types and Abstraction; pressed for an explicit statement of the ISA-legitimacy departure from industry usage; connected this document to the Terminology document's mental-models principle.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, high effort) — rewrote: initial draft; critical review and refinement; synthesized contributor inputs into a coherent document; added the Knowledge, Model, Framework, and Implementation sections; composed Relationships Between Concepts and Discussion.
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed: critical review; structural critique; identified the Abstraction/Model front-matter contradiction; the Framework-as-System vs. Framework-as-Aspect distinction; reformulated the Meta-Principle; Structural vs. Purposive Abstraction, grounded in Maturana and Varela; expanded Omid's open/closed/isolated proposal into the full System Openness subsection; reconciliation pass with the Framework document (removed the residual "Framework is a System" claim); corrected contributor-attribution errors.

#### Summary
Introduced foundational definitions for System, Structure, Architecture, Technology, Knowledge, Science, Model, Abstraction, Protocol (by reference), Framework (by reference), and Implementation. Established the conceptual graph relating these concepts, and positioned this document as a prerequisite for all subsequent conceptual documents in the Memar ecosystem.

#### Rationale and alternatives
- **Defining only System and Architecture, leaving the other concepts to their own documents (rejected).** These concepts form a coherent conceptual graph; defining System and Architecture alone would produce a document that is internally incomplete and forces every subsequent document to independently establish its own conceptual context.
- **Using existing standard definitions without adaptation (rejected).** No single existing standard provides a complete, mutually consistent set of definitions for everything Memar needs.

---

### Refinement round — Meta-Principle, Openness, Edge Types, and terminology bridge
- Time: 2026-07-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: corrected an internal contradiction where Abstraction was stated to be deferred to the Modeling document but was, in fact, already fully defined here; refined the Meta-Principle from an unconditional claim ("Architecture and Framework are Systems") to a qualified one ("...*may themselves be modeled as* Systems when they exhibit the requisite properties"); distinguished Conceptual Centrality from Graph Centrality; updated the "shaped by" edge definition to state its bidirectional character at the point of definition rather than only in the change history; added the bridge to the Terminology document's "terminology shapes mental models" principle; added a lightweight Edge Taxonomy note.
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued: raised the Conceptual vs. Graph Centrality distinction and identified Edge Types as an emerging topic (see attribution correction below — this was originally misattributed to Claude and later corrected).

#### Summary
Defined Framework and Architecture as co-equal aspects of System (Constraint Space vs. Decision Space); clarified that "shapes" in "Architecture shapes a System" is bidirectional and iterative, not one-way control, using classical-architecture and ISA examples; identified Edge Types as an emerging topic that may eventually need its own dedicated document.

---

### Framework-as-System regression fix
- Time: 2026-07-18T00:00:00Z
- Type: Fixed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: corrected a regression where an earlier revision treated "Framework as System" as one of two equally valid senses of the word Framework, contradicting the Framework document's atomic definition ("a framework is a description of a system"). Framework as Aspect now remains the account of how a framework's constraints appear within a built System's Structure; Framework Considered as a System is now presented explicitly as optional and instance-specific, not a co-equal sense of the word. Softened the "shaped by" edge type definition correspondingly, from an unconditional "Architecture is itself a System" to a hedged reading.

#### Summary
Fixed a conceptual regression in how Framework's relationship to System was stated, restoring consistency with the general principle (also applied to Technology and to Architecture in the Meta-Principle) that System is never baked into a concept's core definition — it is, at most, a secondary lens a sufficiently rich instance of a concept may be examined through.

---

### Attribution corrections, Description definition, and Systems Thinking note
- Time: 2026-07-20T00:00:00Z
- Type: Fixed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: corrected a contributor-attribution error (the ISA example was introduced by Omid Hekayati, not Claude); corrected a second attribution error (the Conceptual Centrality vs. Graph Centrality distinction and the identification of Edge Types as an emerging topic were raised by ChatGPT in a later review round, not by Claude); added a short definition of Description ("a statement that represents something in words, or more broadly in any symbolic form") at the point where Framework's definition first depends on it; added "A Note on Systems Thinking" to address a recurring source of confusion between explanatory-level looseness ("almost anything can be called a System") and the definitional discipline the Meta-Principle enforces.
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed: flagged both attribution errors for correction.

#### Summary
Corrected two contributor-attribution errors in the change history, added a missing definition for "Description" that Framework's own definition depended on without ever stating, and added reader guidance distinguishing casual systems-thinking language from this document's formal definitional discipline.

---

### Process extracted to its own standalone document
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - process.md: Done — process.md now holds the full definition, guide-level reasoning, and reference-level treatment this document's `### Process` section previously held in full.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved: confirmed Process should exist as a standalone document given how far its scope had grown beyond what an inline subsection here could hold.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: shortened the `### Process` subsection to a pointer plus only the System-specific half of the Process↔System relationship (a system without processes is a heap, not a system; a system is defined by its processes as much as by its elements); moved the process-nesting examples, the full definition, and the process-before-mechanism reasoning to process.md in full rather than duplicating them; recorded the reversal of this document's own prior Rationale and alternatives entry rejecting a standalone Process document explicitly, rather than leaving it silently outdated.

#### Summary
Reversed a previously-recorded decision (item 1 of the old Change Rationale: "Defining System before other concepts... to avoid circular dependencies") specifically for Process, once its scope outgrew what an inline subsection could hold without either truncating the analysis or making this document disproportionately large. The dependency between System and Process is now asymmetric rather than symmetric: this document keeps System's own definition and its half of the Process↔System relationship; process.md keeps Process's own definition and its half of that same relationship.

#### Rationale and alternatives
Considered leaving the original rejection in place and merging the growing Process content back into this document instead. Rejected once the content had reached a size and depth (failure/rollback, concurrency/locking, retry, cancellation, asynchrony, each analyzed against real distributed-systems discussions) that would have made this document disproportionately large relative to its other topics.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - protocol.md: Pending — not yet migrated to the current Explanation-facet template.
  - terminology.md: Pending — not yet migrated to the current Explanation-facet template.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that every old-style document touched going forward be migrated to the current structure, with a paired changelog file, one document at a time.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: restructured this document from `Summary/Motivation/Guide-level Explanation/Reference-level Explanation/Discussion/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); moved front-matter `Citations` and `Contributor(s)`/`Tasks` into this changelog's entries; migrated the 26-item `## Change Rationale` list into the changelog entries above, grouped by inferred revision round rather than one entry per numbered item, since the original list had no per-item timestamps; normalized Discussion sub-heading casing throughout (`Rationale and Alternatives` → `Rationale and alternatives`, `Prior Art` → `Prior art`, `Unresolved Questions` → `Unresolved questions`) to match the template.

#### Summary
This document is now structured per `documentation-explanation.md`. Its Citations, Contributor roster, and full change history — previously living in front matter and a document-level `## Change Rationale` — now live entirely in this file.

#### Rationale and alternatives
The original `## Change Rationale` list had no per-entry timestamps, only relative order, and several items span review rounds rather than single sessions. Rather than inventing precise timestamps for 26 individual items, entries above are grouped by inferred round and dated approximately; correct the dates above if more precise ones are known. This is the same open question `documentation-changelog.md`'s own Unresolved Questions section names for migrated historical entries.

---

### Responsibility added as a Key Property, closing a gap shared with process.md and modularity.md
- Time: 2026-08-16T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — Observation topic and Relationship to Other Concepts updated to reference this section.
  - modularity.md: Done — Module Identity and Responsibility, and the Module Among Related Concepts table, updated to reference this section instead of using "responsibility" informally.
  - modeling.md: Done — the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling now cites this section.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved: identified, while reviewing modularity.md against process.md and modeling.md, that "responsibility" was load-bearing in all three documents without a formal home anywhere; approved adding it here specifically because this is the project's mother document for these concepts, not because of any status difference between the documents involved; supplied the correction that modeling and observation form a cycle rather than two strictly separated phases (a part may first be modeled naively, then revised once observation shows its boundary does not hold), and that the falsifiable/unfalsifiable distinction between "this boundary was drawn for this concern, for this observer" and "this module has high cohesion" originates from a LinkedIn discussion Omid took part in as a commenter, not as the original post's author.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: added Responsibility as a new Key Property (System's Purpose expressed relative to a containing System) and a "When Is a Responsibility Coherent?" subsection giving the operational test — independent behavioral boundary and lifecycle, checked against a stated concern rather than declared — grounded in the operational criterion already present in `modeling.md`'s Domain Decomposition topic ("independent responsibility, behavioral boundary, or lifecycle") and cross-referenced to `process.md`'s Observation topic for the observer-relativity argument; added a corresponding Unresolved question flagging that `modularity.md`, `process.md`, and `modeling.md` all used the word informally before this definition existed and should be checked against it.

#### Summary
Added Responsibility as a new Key Property of System: a part's Purpose expressed relative to the larger System containing it, not a separate primitive. Added a companion subsection stating what actually makes a Responsibility coherent — an independent behavioral boundary and lifecycle, evaluated against a stated concern — since asserting coherence without naming that concern makes an unfalsifiable claim. This closes a gap that had `modularity.md`, `process.md`, and `modeling.md` each leaning on the word "responsibility" without any of the four documents defining it.

#### Rationale and alternatives
Considered leaving Responsibility informal, on the grounds that `modeling.md`'s existing "independent responsibility, behavioral boundary, or lifecycle" phrasing was already operational enough in context. Rejected because three documents were each free to drift the term in a different direction without a shared definition to check against, which is exactly the coordination risk this round of review was meant to close.
