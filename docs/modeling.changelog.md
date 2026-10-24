# Modeling Changelog

## Changelog

### Initial revision
- Time: 2026-06-30T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Depends_on: terminology governs how concepts are understood across all modeling discussions.
  - [Protocol](./protocol.md) — Depends_on: defines Protocol as a pure declarative specification; modeling produces the domain structures that protocols then constrain.
  - [System](./system.md) — Depends_on: defines Model and Abstraction at the conceptual level; this document builds on those definitions to specify how Memar performs modeling as an architectural activity.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 Pro, extended thinking) — drafted, argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued, reviewed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed

#### What changed
- First structured revision of this document.
- Added `ID` (495220, derived from the original Start Date).
- Migrated `Contributor(s)` from the deprecated `contribution`/`task` format to the `Tasks`-based format.
- Fixed `Citations` `Reason` value for Terminology from the non-standard "Foundation Alignment" to "Depends_on."
- Wrote the previously empty Abstract and Guide-level explanation sections.
- Added Discussion bundles (Drawbacks, Rationale and alternatives, Prior art, and where appropriate Unresolved questions and Future possibilities) to every Reference-level topic.
- Added the missing document-level Discussion and Change Rationale sections.
- Converted plain-text internal references to hyperlinks.
- Added additional examples (e-commerce Order/Payment relationship) and expanded existing discussion points with deeper analysis and more alternatives.
- The core principles; domain decomposition; abstraction justification; the attribute-or-edge test; acquired vs. discovered data; event-aware state modeling; document-spec restructuring; loop-edge classification; edge taxonomy; practice-document extraction; terminology corrections; the unified modeling/review practice; and the pluggable-module principle were claimed (Omid Hekayati).
- The independence-signal review and the event-framing review were contributed (ChatGPT).
- The structural revision, template compliance, and content enrichment were done (Super Z).
- The critical review and content enrichment were done (Claude).

---

### Vocabulary separation revision
- Time: 2026-07-02T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### What changed
- Implementation-level vocabulary in the modeling phase was replaced with Discovery Vocabulary terms (abstraction, concern, conceptual boundary, responsibility).
- It was clarified that modeling outputs conceptual knowledge rather than implementation structures.
- "Modeling Produces Abstractions and Supporting Documents" was added to establish this vocabulary boundary.
- "Concept Existence vs. Model Existence" and "Domain Decomposition" were rewritten to consistently use abstraction-level terminology throughout.

---

### Discovery and behavior emphasis
- Time: 2026-07-04T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### What changed
- A paragraph was added to "Graphs Are Not Documentation Artifacts" clarifying that graphs serve as a discovery environment where questions, assumptions, and modeling decisions evolve alongside structure, not merely as visualization tools.
- "Modeling Focuses on Behavior Before Structure" was added to establish that a system's real complexity resides in what it does, not what it stores, and that modeling should prioritize behavioral understanding before structural decisions.
- An explicit definition of "aggregator" was added in "Domain Decomposition over Aggregate-Root Modeling" to prevent ambiguous interpretation across modeling, architecture, and composition contexts.

---

### Phase relationships and systemic thinking
- Time: 2026-07-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### What changed
- "Modeling, Protocol, and Architecture" was added to clarify that these are not sequential pipeline phases but complementary aspects of a single architectural process — modeling discovers domain understanding, protocol captures it as knowledge contracts, and both are architectural in nature.
- A paragraph on systemic thinking was added to the guide-level explanation, emphasizing that modeling must examine how concerns interact across boundaries rather than partitioning the domain along organizational lines.

---

### Attribute-or-edge test, naming precision, concurrent discovery, and event-aware state modeling
- Time: 2026-07-10T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued.

#### What changed
- "The Attribute-or-Edge Test" was added under "Concept Existence vs. Model Existence," operationalizing the independent-responsibility criterion as a mechanical check ("is this data owned here, or is it a named edge to an already-independent concern?"), using a `Product`/`Text` example covering storage, validation, versioning, internationalization, and search as responsibilities properly owned by a shared `Text` abstraction rather than duplicated per node.
- The `Order`/`Payment` example in "Modeling Requires Explicit Relationship Analysis" was replaced with `Invoice`/`Financial Transaction`, with an explicit note that word choice at the modeling stage is not cosmetic — `Order` and `Payment` were rejected because they smuggle in incorrect assumptions about workflow outcome and implementation layer.
- "Modeling Focuses on Behavior Before Structure" was renamed to "Behavior and Structure Are Discovered Together," clarifying that behavior and structure are discovered concurrently rather than in strict sequence, while retaining the discipline of interrogating every proposed node or edge for its behavioral consequences immediately.
- "Acquired Data vs. Discovered Data" was added as a complementary lens to the existing Fundamental/Derived distinction, with a position/velocity example illustrating why a discovered value should not be stored as if it were an acquired one.
- "Modeling State Change as Events, Not Destructive Updates" was added, establishing that state changes are architecturally significant events to be modeled deliberately, without prescribing any specific storage engine or persistence strategy.

#### Considered and not done
Renaming "Modeling Focuses on Behavior Before Structure" to "Behavior and Structure Are Discovered Together" also resolved an internal tension with the adjacent "Behavior Often Reveals the Quality of the Model" section, which already described behavior as co-discovered rather than sequentially deferred — the rename brought the two sections into agreement rather than leaving one implicitly contradicting the other.

---

### Independence signal, event framing, and discovery entry point
- Time: 2026-07-13T00:00:00Z
- Type: Added
- Contributors:
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued.

#### What changed
- "Reuse Across Contexts as an Additional Signal" was added beneath the Attribute-or-Edge Test, framing cross-context reuse as a corroborating but non-required signal for independent-abstraction status, with `Text` (reused) and `Invoice` (not reused, still independent) as contrasting examples.
- The `Product`/`Title`/`Text` example was established as a recurring reference example, cross-referenced from the `Invoice`/`Financial Transaction` example so the structural (attribute-vs-node) and behavioral (invariant-ownership) lessons remain distinct but mutually discoverable.
- An explicit "a discovered concept should not automatically become a stored concept" principle was added to "Acquired Data vs. Discovered Data."
- "Modeling State Change as Events, Not Destructive Updates" was reordered to lead with "the model should preserve reality before it preserves projections" and an explicit disclaimer that Event Sourcing, CQRS, and append-only storage are not thereby mandated.
- "Initial Discovery Questions" was added — a short checklist distinguishing how to begin discovering abstractions from the rest of the document's treatment of what a good abstraction looks like, explicitly scoped as an entry point rather than a gate. (This checklist was itself removed in a later revision — see "Specification realignment" below.)

#### Considered and not done
Framing reuse as a corroborating but non-required signal, rather than a primary criterion, was a deliberate choice: independent responsibility and lifecycle remain the actual test, and overstating reuse's importance would have let a genuinely independent but rarely-reused concept (like `Invoice`) look wrongly disqualified.

---

### Specification realignment; practice moved to a skill; loop-edge classification; edge-type vocabulary
- Time: 2026-07-20T00:00:00Z
- Type: refactor
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed

#### What changed
- The front matter was migrated to the then-current specification (`Contributor(s)` renamed to `Contributors`; `Works` entries shortened to headline style), Motivation was moved under Introduction with Methodology added, and the former top-level Guide section was moved under Explanation as its first topic, linked from the Abstract — the structural revision and template compliance (Super Z).
- Every checklist and step-by-step procedure that had accumulated in this document — the modeling workflow, Initial Discovery Questions, Challenging a Proposed Concept, Testing an Assumption, Early Indicators of Modeling Progress, and Expected Output of a Modeling Chat — was removed, replaced with short principle statements cross-referenced to a new companion `domain-modeling` skill that then held the concrete procedures (Omid Hekayati — practice-document extraction).
- The TODO-marked "Content Before Classification" section was generalized into "Classification Emerges From Rules and Relations, Not From Intrinsic Labels," formalizing a loop-edge-to-node promotion mechanism — provisional classifications are represented as self-referencing (loop) edges, promoted to independent nodes only when the classification itself passes the same independent-responsibility test already established in "Concept Existence vs. Model Existence" (Omid Hekayati — loop-edge classification).
- "Edge Types and Their Traditional Counterparts" was added, naming reference, composition/ownership, label, and shortcut/index edges alongside their relational-database counterparts, with an explicit caution that shortcut edges must never become a source of truth (Omid Hekayati — edge taxonomy).

#### Considered and not done
An intermediate draft of this change mistakenly cited a separate `modeling-practice.md` document via `Citations`; this was corrected, since Skills are not governed by the Document process and are referenced as ordinary links, not `Citations` entries. This intermediate approach (practice content as a Skill) was itself superseded by the next revision below.

---

### Practice moved to a sibling document instead of a Skill; "domain-" prefix dropped; Guide removed; edge taxonomy simplified
- Time: 2026-07-28T00:00:00Z
- Type: refactor
- Propagates to:
  - modeling.practice.md: Done — practice/procedural content now lives there instead of in a Skill.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### What changed
- Practice/procedural content was moved out of a Skill entirely and into a sibling document, `modeling.practice.md`, living alongside this document; the remaining forward pointers this document had toward that companion content were removed, since the reference relationship runs the other way (the practice document points back here, and even that is kept minimal).
- The Guide topic was removed entirely: everything it covered was about how this document is operationalized in a session, which became `modeling.practice.md`'s responsibility.
- The "domain-" prefix was dropped from "domain modeling" in the Abstract and from every "domain-modeling" skill/practice reference throughout — "modeling" alone is Memar's term for this activity.
- "Edge Types and Their Traditional Counterparts" was simplified from four enumerated, seemingly-exhaustive edge types down to a single architecturally meaningful distinction (an edge is either a shortcut edge or it is not), with reference, ownership, and label demoted to non-exhaustive, illustrative examples of ordinary edges rather than a closed taxonomy.
- A misuse of "RFC" in this document's own change history was corrected — Memar's terminology reserves "RFC" for external standards-track documents (e.g. IETF RFCs), not for Memar's own document type; "document" is the correct term throughout.

#### Deliberation
- The move of practice content out of a Skill entirely and into a sibling document came from a project decision made in a parallel conversation (Omid Hekayati).

---

### Three-way edge distinction; unified modeling/review practice; pluggable-module principle
- Time: 2026-08-05T00:00:00Z
- Type: Changed
- Propagates to:
  - modeling.practice.md: Done — rewritten to merge model discovery and model review into a single unified procedure.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote.

#### What changed
- "Edge Types and Their Traditional Counterparts" was corrected a second time: an edge is not simply "shortcut or not" — a loop-edge (a node connected to itself) is a third, structurally distinct kind of edge in its own right, now named as a peer of ordinary edges and shortcut edges rather than folded in as one example of an ordinary edge.
- The `Invoice`-total shortcut-edge example was replaced with a clearer one (whether an `Invoice` was paid in cash, without traversing every `Financial Transaction` to check each one's account label).
- `modeling.practice.md` was rewritten to merge model discovery and model review into a single unified procedure rather than two documents, incorporating Model Reading, Node/Relationship audits, a Single Responsibility Check, an Implementation Contamination Check, a Completeness Check, a Common Anti-Patterns table, and Severity Levels from a separately-authored review practice (Omid Hekayati — the unified modeling/review practice).
- "Extensible Behavior Belongs to Pluggable Modules" was added, establishing — via a discount-mechanism example on `Invoice` — that a concept's model should expose attachment points for independently-modeled, pluggable Rule modules rather than growing new fields or branches to absorb every variation a plugin might need (Omid Hekayati — the pluggable-module principle).

#### Considered and not done
Deliberately avoided the title "Code vs. Rule" for the pluggable-module section, since discussion showed that framing itself invites the same conceptual narrowing this document's own terminology guidance warns against. The deeper treatment, including its relationship to Khayyam's own modularity model, was left for a future, dedicated, shared document rather than restated here.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document is now structured per `documentation-explanation.md`, with the same template as system.md, protocol.md, terminology.md, and process.md. Its Citations, Contributor roster, and full change history now live entirely in this file.
- This document had already been substantially migrated in earlier revisions (Abstract/Introduction/Explanation/document-level Discussion, with correct lowercase Discussion sub-heading casing throughout, were already in place).
- The remaining gaps were a missing `## Results` section, front matter still carrying `Citations` and `Contributors` directly rather than in a changelog, and the `## Change Rationale` section itself, which is migrated into the changelog entries above (Claude).
- This document was checked for Process-specific content that should migrate to process.md, following the review already applied to protocol.md and terminology.md — none was found, since every use of "process" here is either the ordinary-English sense ("modeling process," "business process") or a reference to the Document process (this document's own review/status pathway), not Memar's formal Process concept (Claude).

#### Deliberation
- The migration of this document to the current structure with a paired changelog file was requested, matching the treatment already applied to system.md, protocol.md, and terminology.md (Omid Hekayati).

---

### Explicit cross-reference to the formal Process concept
- Time: 2026-08-15T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- Previously, this document used "process" only in its ordinary English sense throughout, with no signal to the reader that Memar has a separate, formal Process concept at all — someone modeling from this document alone had no reason to go look for one.
- A direct cross-reference was added in "Modeling, Protocol, and Architecture" — the section that already discusses the System→Process→Protocol chain conceptually without naming Process as a defined term — as a paragraph stating directly that this document's informal uses of "process" are ordinary English, not the formal Process concept, and that Protocol actually governs the formal one, with a link to process.md added alongside the existing Protocol and Terminology links (Claude).
- A second, lighter cross-reference was added in "Behavior and Structure Are Discovered Together" — the section where the behavioral vocabulary discussed (failure, retry, concurrency) overlaps directly with process.md's own vocabulary — connecting that vocabulary (failure, retry, concurrency, recovery) directly to process.md's formal treatment of the same vocabulary (Claude).

#### Deliberation
- It was pointed out that a reader who models something using only this document, without knowledge of process.md, could reasonably assume "process" carries its ordinary ecosystem-default meaning here rather than Memar's formal definition — this document should not let that ambiguity stand (Omid Hekayati).

### Modeling review and vocabulary cleanup
- Time: 2026-08-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed

#### What changed
- Procedural workflow content was removed from the reference document so that execution guidance remains in `modeling.practice.md`.
- It was clarified that modeling produces abstractions, relationships, constraints, and supporting documents rather than implementation-level structures.
- The `Product`/`Title`/`Text` attribute-or-edge example, acquired-versus-discovered data distinction, event-aware state modeling, concurrent behavior-and-structure discovery, explicit aggregation emergence, and pluggable-module principle were preserved.
- An explicit statement was added to the practice document that requirement terminology is evidence to investigate rather than an authoritative model boundary.
- Implementation-level vocabulary was removed from the modeling document and its historical change descriptions to keep the modeling vocabulary consistent.
- The final vocabulary and modeling-boundary corrections were Omid Hekayati's.
- The final consistency pass and cleanup was Claude's.

---

### Coordination pass with system.md, process.md, and modularity.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Propagates to:
  - system.md: Done — the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling now cites system.md's Responsibility section.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document had been carrying the full architectural reasoning for pluggable Modules in its own words, with a note already flagging that the material belonged in a shared document once one existed.
- Now that `modularity.md` exists, "Extensible Behavior Belongs to Pluggable Modules" was shortened to state only the modeling-level consequence and the `Invoice` illustration, pointing at `modularity.md`'s now-existing "Pluggable Behavior" topic for the architectural treatment this section used to carry in full — resolving the forward-reference this section had explicitly left for "a dedicated, shared document" before that document existed (Claude).
- The independent-responsibility criterion this document had already worked out informally was tied back to `system.md`'s formal Responsibility definition, with `system.md`'s new Responsibility section cited from the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling (Claude).
- Unresolved question 1 under the pluggable-modules Discussion was resolved, since `system.md` now states the general test explicitly (Claude).

#### Deliberation
- A coordinated pass across `system.md`, `process.md`, `modularity.md`, and `modeling.md` together was requested, so shared concepts have one authoritative home each (Omid Hekayati).

---

### Lens plurality, constraint ownership, and edge-direction open questions
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
- Propagates to:
  - modularity.md: Done in this same pass — see modularity.changelog.md; the hosting question added here cross-references it.
  - protocol.md, agency.md: Done in this same pass — observer-facing consequences of Protocol and Agency roles.

#### What changed
- "One Reality, Multiple Abstraction Lenses" was added: a single reality may be modeled through co-equal abstraction modes (structural, behavioral/process, normative, systemic) that are neither hierarchy levels nor entities inside the produced model, with the warning that parallel structures differing only by lens usually indicate one concern counted several times.
- "Constraints Belong to the Constraining Concern" was added: a constraint originating outside a resource is modeled as a relationship owned by the constraining concern, carrying its own target/satisfied/remaining state and observing the affected resources, never duplicated onto each of them; with the corollary that two related-looking quantities on one node may be independent projections evaluated against different active rules rather than primary-plus-cache.
- Edge Types Unresolved Questions was extended with two items deferred to storage-semantics design: whether a bidirectional relationship is one Type observed from two directions or two distinct Types (and where relationship identity resides), and which Module hosts a relationship whose endpoints belong to different Modules (Super Z).

#### Deliberation
- Both principles originated during accounting-domain development discussions — a resource quantity that looked cache-like turning out to evaluate external constraints, and several abstraction views repeatedly confused with separate entities (Omid Hekayati).
- Both principles were co-developed across two discovery sessions, including the first formulation of constraint copying onto resources and its later correction (ChatGPT).
- Both findings were generalized into principle-level topics without domain examples (Super Z).
- An earlier proposed shortcut-edge ownership clause was withdrawn after review showed it conflated two different abstraction lenses (Super Z).
- The final scope and wording were approved (Omid Hekayati).

#### Considered and not done
- **Writing current working positions into the document itself (rejected)**: tentative positions stay out of base documents per project convention. Recorded here instead so they are not re-derived later. Working positions at the time of this change: (1) the working preference for a bidirectional pair is two distinct relationship Types, since the human-facing descriptions of the two directions differ regardless of representation; (2) a proposed clause assigning shortcut-edge ownership to the deriving concern was examined and withdrawn — shortcut edges are judged within their own abstraction lens, while acquired/discovered data is a separate lens, and the output of discovered data may itself be an ordinary edge.

---

### Classification gray zones: incidental metadata and temporal graduation
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - type.md: Done — the type-layer counterpart landed in the same pass (stateless concepts remain Types; family resemblance is not qualification); see type.changelog.md.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted.

#### What changed
- Explicit treatment of two recurring gray zones was added to the loop-edge classification discussion: incidental metadata (a field merely recording when or in what scope a label applies does not make it a data-carrying concern in its own right — the test remains independent responsibility, not field presence) and temporal graduation (something classified today may evolve until its rules justify independence tomorrow; such label-to-node promotion is legitimate but must be decided explicitly at each evolution point under the same test, never assumed silently in either direction).
- This inherits the classification thread of the dissolved *Static Concepts Must Be Types* document (495421): its "static concept vs data carrier" determination was this document's node-vs-loop-edge question seen from the implementation side.
- The formalization follow-up remains covered by the already-open criteria question under Concept Existence vs. Model Existence, so no new unresolved-question entry was needed.

#### Deliberation
- The dissolution of the source document and the distribution of its classification content here was approved during the type-documentation correction pass (Omid Hekayati).

---

### Concept-vs-data definition pair absorbed from a dissolved type-series stub
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - type.md: Done — the companion stub `type-rules_and_invariants.md` was absorbed there and `type-relations.md` dissolved as redundant in the same pass; see type.changelog.md.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### What changed
- The crisp definitional pair from the dissolved 20-line stub `type-concepts_vs_data.md` was absorbed into "Concept Existence vs. Model Existence": a concept has semantic identity (participates in the model, may own behavior and rules) while data represents information without necessarily having independent identity of its own, anchored by the canonical `Person`/birth-date and `Contract`/description-field example pairs.
- The stub's "Modeling Question" and common-mistake warning (data structures first, concepts later) were already carried by this section's opening framing and the acquired-versus-discovered lens respectively.
- The stub had sat in the type- series despite declaring its own key question a modeling question; dissolution resolves that layer misplacement.

#### Deliberation
- Review and merge of the small type-series companions into the strong documents was directed (Omid Hekayati).

---

### Code/Rule separation absorbed from the organization repository
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — drafted, applied.
- Propagates to:
  - modularity.md: Done in this same pass — reciprocal cross-reference added to "Rules as a Provisional Term"; see modularity.changelog.md.

#### What changed
- "Separating Structure (Code) from Policy (Rule)" was added: every domain is modeled in two layers — Code (the fixed structural shape: node types, edge types, and their mandatory relationships) and Rule (conditional, context-dependent policy logic) — with Rule modeled as a first-class graph node connected by an edge to the Code element it governs, execution delegated to a separate rule-engine component, and the statute/bylaw analogy retained.
- The content was absorbed from the organization repository's RFC "Separation of Code (Structure) and Rule (Policy) in Graph Domain Modeling" (495340, Proposed) together with its companion topic note "Code vs. Rule Boundary Criteria"; the RFC's project-specific implementation aspects remain in that repository's `modules/computer/rule`.
- Edge Types Unresolved Questions was extended with the static-typing-versus-loop-edge type-upgrade criterion question surfaced during the same absorption.

#### Deliberation
- The source RFC's content was judged a general modeling principle rather than Organization-domain material, and its absorption into this document was ordered (Omid Hekayati).

#### Considered and not done
- **Writing the boundary-test hypothesis into the document (rejected)**: the candidate test from the source note ("a condition that varies by organization, jurisdiction, or time without changing the underlying node/edge type needed is a Rule; a condition that determines whether a type can exist at all is Code") is an untested working position, recorded here so it is not re-derived later; it must be run against real edge cases (NOT-NULL-style constraints, cardinality constraints) before being trusted.
- **Resolving the tension with "Rules as a Provisional Term" (rejected as premature)**: the source RFC asserts Rule as a first-class graph node, while this framework's module framing treats *Rule* as a provisional term for a Module's optional relationship to another Module. Both framings are kept, cross-linked, and their reconciliation is recorded as an open question rather than decided unilaterally.

---

### One Data Store section renamed and reframed; tool names purged
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Propagates to:
  - protocols/memory/memory.md: Done — the definitional vocabulary this section now leans on (memory as one class, volatility categories, the dichotomy rejection, the cache-as-derived-copy reading) added there in the same pass; see memory.changelog.md.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The rule's force is unchanged — one concern's authoritative data has one location, and a derived copy is never a second authority — but its vocabulary now comes from the Memory document's definitions instead of the ecosystem's storage split, and no product or technology name appears in the section.
- The section was renamed to "One Authoritative Location per Concern's Data"; all product and technology names were purged; both failure faces were re-stated in memory terms (locations and retention tiers, not store products); the explicit note that the shadow-tier pattern is a product of the memory/storage dichotomy was added and the dichotomy rejection in memory.md cross-linked; the modeling-level rule itself (one authoritative location per concern's data) was kept unchanged in force (Super Z).

#### Deliberation
- The "One Data Store Serves One Concern's Ownership" section was judged misplaced in vocabulary and framing: naming products in an abstract modeling document misleads from the ground up — the product name was corrected to a generic cache term in a first pass, then the whole section was sent back for abstraction (Omid Hekayati).
- The section's reliance on the memory/storage split inherited exactly the dichotomy the framework rejects (Omid Hekayati).
- The reframe in retention-property terms was directed, with definitions deferred to the new Memory document (Omid Hekayati).

---

### Direction of reference reversed: modeling states the rule, protocols work it out
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The reference now runs one way: memory.md (protocol layer) cites modeling.md (concept layer) for the rule; modeling.md no longer cites any protocol document. The section is shorter, tool-free, and self-contained at the modeling level.
- The section was shrunk to the rule, the derived-copy reading, the two recurring violations stated without links, and the general modeling-time guidance (the question surfaces during modeling; either Memar's libraries and protocol documents carry the answer, or the organization builds its own library against them); the shadow-tier working-out, the dichotomy link, and the volatility vocabulary were moved into memory.md, which now holds the full treatment; the one direction that remains was kept (memory.md citing this section as the modeling-level statement of the rule) (Super Z).

#### Deliberation
- It was identified that the section's direct links into `protocols/memory/memory.md` created a bidirectional reference between a root concept document and a protocol document, which is unstable — memory's document is developed *on* modeling's method, so the dependency runs one way only (Omid Hekayati).
- Two options were directed — move the memory document to root, or state the rule abstractly here with the working-out owned by the protocol documents — and the second was chosen: modeling keeps the rule and names the boundary; the protocol documents keep the definitions and the worked-out failures (Omid Hekayati).

---

### Documentation-method migration completed: Discussion wrappers, Rationale, Prior art, Unresolved questions, Future possibilities dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - modeling.handoff.md: Created - open questions and future possibilities moved there.
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only (Super Z - applied the finalized documentation method).
- The document-level Drawbacks and Rationale and alternatives content preserved below; Unresolved questions and Future possibilities moved to the paired handoff (Super Z).
- The aggregator Naming Conventions note folded inline into the Domain-Decomposition topic (Super Z).

Dissolved every Discussion wrapper and the document-level Discussion; drawback statements and premise evidence folded inline into their topics; rejected alternatives, comparative prior art, document-level Drawbacks, open questions, and future possibilities relocated without loss. (Super Z)

#### Considered and not done
- **Treat models as approximations of reality (considered, not chosen as primary definition; migrated from the Models-Are-Not-Reality topic's retired Rationale and alternatives)**: while true, this framing can imply that models should be judged by their fidelity to reality, which is only one dimension of model quality. A model may serve its purpose well even if it departs significantly from reality in aspects that are irrelevant to that purpose.
- **A single canonical decomposition per domain (rejected; migrated from the Abstraction-Lenses topic's retired Rationale and alternatives)**: assuming every aspect of reality has exactly one correct structural breakdown forces behavioral and governance observations to be squeezed into structural artifacts where they fit poorly.
- **Formal multi-view frameworks (considered, not chosen; migrated from the Abstraction-Lenses topic's retired Rationale and alternatives)**: architecture frameworks that prescribe fixed view sets provide useful checklists but conflict with Memar's discovery-driven approach; which lenses matter is discovered from the concern at hand, not fixed up front.
- **No initial checklist (rejected; migrated from the Initial-Discovery-Questions topic's retired Rationale and alternatives)**: leaving modelers to begin entirely from first principles each time is consistent with treating modeling as pure judgment, but in practice produces inconsistent starting points across sessions and modelers, and gives no guidance for the common case of an unstructured, lengthy requirement.
- **Implementation-driven modeling (rejected; migrated from the Model-as-Primary-Artifact topic's retired Rationale and alternatives)**: starting from code and extracting the model afterward is common in agile practices, but consistently produces models that reflect incidental implementation decisions rather than domain structure. The cost of correcting such models grows with every additional feature built on top of them.
- **Parallel modeling and implementation (considered, not chosen; migrated from the same topic)**: developing the model and implementation concurrently reduces time-to-first-prototype but makes it harder to distinguish model concepts from implementation artifacts during review. Memar permits rapid prototyping for learning purposes but does not treat prototypes as committed implementation.
- **Direct implementation coupling (rejected; migrated from the Models-Must-Survive topic's retired Rationale and alternatives)**: allowing implementations to depend directly on each other's internals is simpler in the short term but makes any change to a single concern ripple unpredictably across the system. This is the dominant source of rigidity in most software architectures.
- **Shared-database integration without protocol boundaries (rejected; migrated from the same topic)**: this is the de facto pattern in many systems, where different services or modules share a database schema and therefore share each other's structural decisions. It eliminates the indirection but makes any schema change a coordinated, high-risk event.
- **Technology-first architecture (rejected; migrated from the Adaptability topic's retired Rationale and alternatives)**: selecting the technology stack and then fitting the domain into it is the dominant industry practice. It produces systems whose structure reflects framework conventions (controllers, repositories, entities) rather than domain boundaries, making the system adaptable to framework changes but not to domain evolution.
- **Full technology agnosticism (considered, not chosen; migrated from the same topic)**: deferring all technology decisions until after modeling is complete is the ideal but may be impractical when the team's expertise or the deployment environment constrains the feasible implementation options. A pragmatic middle ground acknowledges known constraints without allowing them to dictate the model's conceptual structure.
- **Entity-first modeling (rejected; migrated from the Relationship-Analysis topic's retired Rationale and alternatives)**: starting by defining entities and their attributes, then adding relationships as an afterthought, produces models where the relationships are shaped by storage convenience rather than domain semantics. This is the dominant approach in ORM-driven development.
- **Relationship-only modeling (rejected; migrated from the same topic)**: focusing exclusively on relationships without grounding them in identifiable concerns produces an abstract graph that is difficult to map to concrete system boundaries. Memar requires both nodes and edges, not one at the expense of the other.
- **Schema-first modeling (rejected; migrated from the Graphs-as-a-Tool topic's retired Rationale and alternatives)**: starting from database schemas or API definitions anchors the model to implementation decisions too early. The resulting model reflects storage and transport concerns rather than domain structure.
- **Text-first modeling (rejected; migrated from the same topic)**: describing the domain in prose and extracting entities from the text is a common UML-driven practice, but prose descriptions tend to linearize relationships that are inherently graph-structured, causing many cross-cutting concerns to be missed.
- **Formal ontology languages (considered, not chosen; migrated from the same topic)**: using OWL or similar formalisms would provide precise semantics but introduces a tooling and expertise barrier that is disproportionate for most software modeling contexts. Memar uses informal graphs but structures the modeling process around them systematically.
- **Graphs as living documentation (considered, not chosen; migrated from the Graphs-Are-Not-Documentation topic's retired Rationale and alternatives)**: maintaining the graph as a continuously updated document alongside the codebase keeps the modeling history accessible but introduces an ongoing maintenance obligation. The graph must be updated every time the model evolves, or it becomes misleading. For teams that already struggle with documentation maintenance, this obligation may be unrealistic.
- **Versioned graph artifacts (considered, not chosen; migrated from the same topic)**: committing graph snapshots to version control at each modeling milestone preserves history without requiring continuous maintenance. This approach is promising but has no established convention for graph file formats or commit granularity.
- **Structure-first modeling (rejected; migrated from the Behavior-and-Structure topic's retired Rationale and alternatives)**: defining entities, their attributes, and their relationships before examining behavior is the dominant industry approach, driven by ORM tools, database-first design, and API-specification workflows. It produces models that accurately describe what the system contains but often fail to capture what the system does — leading to behavioral gaps that surface only during implementation or, worse, in production.
- **Strict behavior-before-structure sequencing (rejected; migrated from the same topic)**: requiring behavior to be fully understood before any structural decision is made is appealing in principle but unworkable in practice — stakeholders cannot describe behavior in a vacuum, without reference to the concepts that behavior acts upon. It also implies a rigidity of phases that Memar's modeling process does not otherwise impose.
- **Unstructured parallel discovery (rejected; migrated from the same topic)**: discovering behavior and structure simultaneously without discipline is appealing but in practice tends to produce models where structural assumptions unconsciously constrain behavioral exploration. For example, once an Order entity has been defined with a status field, the team may stop asking whether status is even the right behavioral model for order lifecycle. Memar's approach differs from unstructured parallelism by requiring that every proposed node or edge be immediately interrogated for its behavioral consequences, rather than accepted and revisited later.
- **Behavior-driven modeling (rejected in its conventional form; migrated from the Behavior-Reveals-Quality topic's retired Rationale and alternatives)**: starting from user stories or behavior specifications and deriving the model from them tends to produce models that reflect usage patterns rather than domain structure. The resulting model may be optimized for current workflows but resistant to unanticipated changes.
- **Separate behavioral and structural modeling (rejected; migrated from the same topic)**: this is the dominant industry practice — model the structure first, then define behavior as methods, handlers, or services. Memar does not treat behavior as a separate phase because behavioral expectations are often the clearest indicator of whether structural boundaries have been drawn correctly.
- **Artifact-count metrics (rejected; migrated from the Graph-Stability topic's retired Rationale and alternatives)**: measuring maturity by the number of concerns, services, or tests produced is tempting because it is easy to automate. However, these metrics conflate modeling quality with implementation effort. A system can have hundreds of well-tested services built on a poorly structured model.
- **External review as the primary maturity signal (considered, not chosen; migrated from the same topic)**: relying on peer review or expert assessment to determine model maturity is valuable but subjective and difficult to scale. Graph stability provides an internal, reproducible signal that complements external review.
- **Spike-driven modeling (considered, not chosen; migrated from the Modeling-Before-Implementation topic's retired Rationale and alternatives)**: building a thin vertical slice through the system to validate model assumptions, then discarding the spike and modeling properly before real implementation. This preserves the learning benefit of early implementation without committing to the model that the spike reveals to be wrong. The risk is that teams rarely discard spikes — they tend to evolve into production code, carrying their modeling assumptions with them.
- **Time-boxed modeling (considered, not chosen; migrated from the same topic)**: setting a fixed duration for modeling (e.g., one sprint) and beginning implementation regardless of maturity. This is pragmatic but explicitly accepts the cost of model changes during implementation.
- **Name-driven decomposition (rejected; migrated from the Concept-Existence topic's retired Rationale and alternatives)**: every named concept gets its own abstraction. This maximizes modularity but produces artificial fragmentation — the "artificial decomposition" failure described in that topic.
- **Data-driven decomposition (rejected; migrated from the same topic)**: every distinct data structure gets its own abstraction. This inherits the assumptions of database normalization and conflates storage concerns with domain boundaries.
- **Responsibility-driven decomposition (chosen; migrated from the same topic as the recorded decision)**: only concepts that carry an independent responsibility, behavioral boundary, or lifecycle receive their own abstraction. This requires more judgment but produces boundaries that reflect the domain's actual architecture.
- **Direct type tagging (rejected; migrated from the Classification topic's retired Rationale and alternatives)**: attaching a type or label field directly to a node, as in most property-graph databases, is simpler to implement but treats classification as an intrinsic, static property rather than something that emerges from — and can be re-evaluated against — the node's actual relationships and satisfied rules.
- **Class hierarchies with inheritance (rejected; migrated from the same topic)**: defining Instruction, Memory, and Procedure as subclasses of Content in a conventional inheritance hierarchy commits to the classification at definition time and makes it difficult for a node to satisfy more than one classification, or to have its classification re-evaluated as the rules it satisfies change.
- **Treating all stored data uniformly (rejected; migrated from the Acquired-vs-Discovered topic's retired Rationale and alternatives)**: not distinguishing acquired from discovered data is the default in most schema-first designs, where every field is stored as though it were an equally primary fact. This makes it impossible to later tell which fields are recomputable and which represent irreplaceable source-of-truth information.
- **Destructive update as the default (rejected; migrated from the Events-Not-Updates topic's retired Rationale and alternatives)**: treating in-place overwrite as the default and history preservation as an opt-in special case is the dominant industry practice, inherited directly from relational UPDATE semantics. It silently discards architecturally significant information unless a team happens to think of history preservation in advance.
- **Mandatory event sourcing for all concerns (rejected; migrated from the same topic)**: requiring every concern to be modeled as an append-only event log is appealing for consistency but conflates a modeling-level concern with an implementation-level commitment. Memar treats the preservability of state history as a modeling question and leaves how it is achieved to implementation.
- **Constraint state duplicated onto each affected resource (rejected; migrated from the Constraining-Concern topic's retired Rationale and alternatives)**: simple to store and fast to read locally, but it destroys the aggregate meaning of the constraint, scatters one responsibility across many models, and makes the set of active limitations invisible as a whole.
- **A single global registry of all constraints (rejected; migrated from the same topic)**: recentralizes what should be independently modeled concerns and recreates aggregation-by-theme at the constraint level; each constraining concern owns its own state and relationships.
- **UI-driven modeling (rejected; migrated from the Presentation topic's retired Rationale and alternatives)**: deriving the model from pages, screens, and API endpoints is the de facto industry practice, driven by the prevalence of UI-first design tools and API-first development workflows. It produces models that are tightly coupled to a specific product's user experience and resistant to changes in that experience.
- **Event-driven modeling (considered, not chosen; migrated from the same topic)**: starting from domain events (e.g., "OrderPlaced", "PaymentReceived") rather than UI structures. This is a stronger starting point for domain discovery but requires familiarity with event-storming techniques and does not naturally capture state-based concepts.
- **Language-driven modeling (considered, not chosen; migrated from the same topic)**: analyzing the domain's ubiquitous language — the terms, phrases, and patterns that domain experts use — to identify concepts. This is aligned with DDD's strategic design phase but requires sustained access to domain experts, which is not always available.
- **Classical DDD aggregate-root pattern (rejected; migrated from the Domain-Decomposition topic's retired Rationale and alternatives)**: a single, owning entity directly containing related sub-concerns. In practice, it tends to pull unrelated validation and identity logic into one type, and breaks down whenever a concept (like "the current user") genuinely has more than one valid shape depending on context (local form vs. OAuth-resolved identity).
- **Trait/mixin-based decomposition (considered, not chosen; migrated from the same topic)**: defining concerns as mixins that are composed into a single entity at compile time. This addresses the code-organization concern but does not solve the architectural problem: the composed entity still has a single identity and lifecycle, which forces all contexts to share one shape.
- **Composition-root pattern from functional programming (considered, not chosen; migrated from the same topic)**: assembling dependencies at a single composition root, as in pure dependency injection. Memar's approach is similar but applies at the concept level (abstractions) rather than the service level, and allows multiple composition roots for different contexts rather than a single application-wide root.
- **Per-data-shape system selection as a default (rejected; migrated from the One-Authoritative-Location topic's inline considered-and-rejected paragraph)**: the data-shape argument ("relational for structured, document for flexible") attributes the shape to the data, but shape is a property of the concern's responsibilities — a concern modeled correctly has one shape, and the split pattern usually means the modeling was never finished and two half-modeled fragments are being kept separately.
- **Invalidation discipline as the mitigating practice (rejected; migrated from the same paragraph)**: some ecosystems treat cache invalidation as a hard problem worth engineering well. The harder truth is that invalidation is hard precisely because two owners were introduced for one concern; removing the second owner removes the problem class rather than solving its instances.
- **Anticipatory hard-coding (rejected; migrated from the Pluggable-Modules topic's retired Rationale and alternatives)**: building a single, maximally configurable discount mechanism directly into Invoice that tries to anticipate every variation a team can imagine. This inevitably fails to anticipate the variation that actually arrives, and every failure to anticipate becomes a change to Invoice itself rather than the addition of an independent module.
- **Inheritance-based variation (rejected; migrated from the same topic)**: modeling TieredDiscountInvoice, LocationRestrictedInvoice, and similar as subtypes of Invoice. This multiplies Invoice itself rather than keeping it stable, and runs into the same combinatorial-explosion problem inheritance-based variation always does once more than one axis of variation exists at once (e.g. tiered and location-restricted).
- **Hardcoded conditionals in application code (rejected; migrated from the Code/Rule topic's retired Rationale and alternatives)**: duplicates logic per organization/jurisdiction, makes cross-organization variation a code-deployment event instead of a data event, and leaves the graph an incomplete source of truth.
- **External, non-graph policy store (not chosen as primary; migrated from the same topic)**: a rules table in a separate relational system, or a policy-as-code file outside the graph, breaks the single-source-of-truth goal — "which entities are affected by Rule X" would require a join outside the model. This remains a legitimate execution-layer detail (the rule-engine itself may be an external process); what stays in-graph is the Rule's existence and relationships.
- **Ad-hoc modeling without a defined process (rejected; migrated from the document-level retired Rationale and alternatives)**: this is the default in most organizations. It produces inconsistent models whose quality depends entirely on the individual architect's skill and experience, without any mechanism for systematic improvement.
- **Heavyweight formal modeling (rejected; migrated from the document-level retired Rationale and alternatives)**: approaches like full UPDM or SysML modeling provide rigor but introduce tooling and expertise barriers that make them impractical for most software teams. Memar seeks a middle ground: systematic enough to be teachable and repeatable, lightweight enough to be applied without specialized tools.

#### Considered and not done (topic-level drawbacks relocated per owner ruling)
- **The model/reality gap can produce epistemic paralysis** — if no model is complete, how can any model be trusted? The answer is that models do not need to be complete to be useful; they need to be honest about what they include and what they exclude, and the consequences of each omission should be understood and documented. A model that is explicitly incomplete but whose incompleteness is well-characterized is more useful than a model that claims completeness but silently omits important aspects of its target. (Migrated from the Models-Are-Not-Reality topic)
- **Treating lenses as informal vocabulary means no mechanical rule says when a second observation names a new lens versus a new concern.** The principle can also be misused in both directions: multiplying entities by treating every observation angle as its own sub-model, or suppressing legitimate distinctions by declaring everything "just another lens on the same thing." (Migrated from the Abstraction-Lenses topic)
- **A checklist risks being treated as a mechanical procedure whose completion signals that modeling is "done,"** which contradicts the iterative, non-linear nature of the rest of the document. It is intended only as an entry point for the first pass over a new requirement, not as a gate or a substitute for the deeper discovery process. (Migrated from the Initial-Discovery-Questions topic)
- **Treating the model as primary requires upfront investment before any visible implementation progress,** which can create political friction in velocity-measured environments; and the claim that "a model can be validated without implementation" is itself limited — some categories of correctness (performance characteristics, storage feasibility, integration compatibility) can only be fully evaluated once an implementation exists. (Migrated from the Model-as-Primary-Artifact topic)
- **Protocol boundaries introduce indirection,** increasing the cognitive overhead of understanding the system, particularly for developers accustomed to directly accessing object internals; and there is a risk of over-abstracting early, creating protocol boundaries around concerns simple enough that the indirection is not justified by any real need for implementation independence. (Migrated from the Models-Must-Survive topic)
- **The adaptability principle can be misread as license to defer all technology decisions indefinitely,** while some technology constraints (regulatory requirements, existing infrastructure, team expertise) may legitimately constrain the model or the shape of its realizations; a team that exclusively models without considering technological feasibility risks producing a model that cannot be practically implemented in its target environment. (Migrated from the Adaptability topic)
- **Treating every relationship as first-class increases the complexity of the modeling process itself.** Not all relationships carry architectural significance — many are purely structural or incidental — and the effort can become bogged down in cataloging relationships that have no impact on boundaries or responsibilities; distinguishing architecturally significant relationships from incidental ones requires judgment that is difficult to codify. (Migrated from the Relationship-Analysis topic)
- **Graph exploration has no natural stopping criterion,** which conflicts with the practical need to begin implementation; and there is no widely adopted standard for what a "modeling graph" should look like, so graphs from different teams or sessions may be difficult to compare or consolidate. (Migrated from the Graphs-as-a-Tool topic)
- **Even a three-way edge distinction can tempt teams into premature notation standardization** — creating a formal taxonomy before the domain's actual relationships are understood, precisely the schema-first anti-pattern this document elsewhere rejects. The named roles are descriptive vocabulary for edges that already exist for good reasons, not a checklist every model must populate. (Migrated from the Edge-Types topic)
- **Treating graphs as disposable working tools may leave no durable record of the modeling process** once implementation begins — the original graph, with its intermediate states, abandoned alternatives, and rejected structures, may no longer exist, making it difficult to understand why certain boundaries were chosen, especially when the original modelers are no longer available. (Migrated from the Graphs-Are-Not-Documentation topic)
- **Co-discovery of structure and behavior can make modeling chats feel unfocused,** since node-field discussions are repeatedly interrupted by behavioral questions and vice versa; stakeholders expecting a clean sequential process may find this uncomfortable, behavior-poor or data-centric domains may need extra facilitation, and there is a risk of over-analyzing edge-case behavior before core structural patterns have stabilized. (Migrated from the Behavior-and-Structure topic)
- **The behavioral-complexity-as-signal claim can be overapplied.** Some domains are genuinely complex — regulatory compliance, multi-currency financial settlement, real-time collaborative editing — and no amount of modeling will eliminate their inherent behavioral complexity; applying the principle indiscriminately risks a culture where legitimate domain complexity is dismissed as a modeling failure, producing oversimplified models that cannot handle real-world edge cases. (Migrated from the Behavior-Reveals-Quality topic)
- **Graph stability is a retrospective indicator** — it can only be measured after multiple modeling chats, so it cannot guide early modeling decisions; and apparent stability may reflect insufficient challenge rather than genuine convergence — a model untested against new requirements or critical review may appear stable simply because it has not been stressed. (Migrated from the Graph-Stability topic)
- **The model-before-implement discipline can conflict with lean, experiment-driven product development.** If the team discovers after implementing a prototype that its model assumptions were wrong, the pre-prototype modeling effort may be partially wasted; and the principle does not account for domains that are poorly understood at the outset and can only be clarified through iterative implementation — insisting on modeling maturity there may delay the very learning that would improve the model. (Migrated from the Modeling-Before-Implementation topic)
- **The fundamental/derived distinction is itself subjective and context-dependent.** A `DiscountedPrice` that in one context is a calculated view may in another carry its own business rules (minimum thresholds, regulatory restrictions, temporal validity windows) that justify an independent abstraction; misclassification in either direction produces real architectural damage. (Migrated from the Concept-Existence topic)
- **Representing every candidate classification as a loop-edge adds graph machinery** a direct-labeling approach would avoid; and for teams unfamiliar with graph-native modeling, distinguishing a never-promoted loop-edge (like `Status`) from a genuine promotion candidate may not be obvious without practice, risking graphs cluttered with loop-edges no one intends to promote. (Migrated from the Classification topic)
- **Preserving every state change as an event, taken to an extreme, retains trivial or inconsequential changes indefinitely,** creating storage and query-performance concerns unrelated to domain modeling; not every state change carries architectural significance, and modeling should distinguish changes worth preserving from incidental ones rather than preserving everything by default. (Migrated from the Events-Not-Updates topic)
- **Modeling constraints as observing concerns moves work from write time to evaluation time:** answering "what remains usable here?" requires consulting active relationships instead of reading one stored number; systems with many simultaneous constraints need an explicit composition story, and deferring it risks inconsistent answers from ad hoc queries. (Migrated from the Constraining-Concern topic)
- **Many projects begin with a UI design or API specifications and have no alternative starting point for modeling.** Dismissing the UI as an unreliable source is theoretically sound but practically frustrating when the UI is the most concrete artifact the team possesses; and in some domains — particularly consumer-facing products — the user experience is the domain, making the presentation/domain distinction difficult to maintain. (Migrated from the Presentation topic)
- **Without a single canonical owning entity, assembling "the whole picture" requires composition-layer indirection** and discipline to avoid quietly re-inventing a de facto aggregate root inside a frequently reused widget; the approach also increases the number of abstractions, making the architecture harder to navigate for newcomers expecting a `User` object containing all user-related data and behavior. (Migrated from the Domain-Decomposition topic)
- **Pushing variation into pluggable modules trades one kind of complexity for another:** the team now maintains `Invoice` plus an open-ended set of independently evolving Rule modules, with discipline required about what belongs in the core versus a plugin; for a genuinely small, stable set of variations, a full Rule/module boundary can cost more than hard-coding the variation. (Migrated from the Pluggable-Modules topic)
- **The Code/Rule separation adds indirection for every conditional behavior:** even simple, rarely-varying conditions require traversing to a Rule node and invoking the engine instead of a direct code check — a real runtime and cognitive cost, not just a modeling nicety. Rule-sprawl risk: once "make it a Rule" becomes the default answer to any conditional, genuinely universal constraints may be over-modeled as Rule nodes "just in case," inflating the graph without benefit. And making Rule evaluation graph-traversal-dependent may carry real performance implications at scale, especially where one instance is subject to many applicable Rules that must all be resolved to determine validity. (Migrated from the Code/Rule topic)
- **Naming-history narration relocated:** `Order` and `Payment` were initially considered and rejected as the relationship-analysis example — an order is a command that may never be fulfilled (e.g. an order to buy 1,000 shares of a stock, or 50 beams of steel, that never executes), so it has no inherent connection to financial settlement; and a `Payment` is typically itself a composition-layer construct (a checkout widget or page) rather than a base concern. `Invoice` and `Financial Transaction` were chosen instead because they name the actual base concerns without smuggling in assumptions about workflow outcome or implementation layer; the care in naming matters because an imprecise name at the modeling stage silently encodes an incorrect assumption into the abstraction's identity, and that assumption then propagates into every place the abstraction is used. (Migrated from the Relationship-Analysis topic)

#### Considered and not done (from the removed document-level Drawbacks section)
- **The modeling approach described in this document demands significant upfront investment before any implementation progress is visible.** For small or well-understood domains, the full graph-discovery process may be disproportionate to the complexity being managed. The approach also assumes that a team has access to domain expertise — if the domain experts are unavailable or the domain is poorly understood, graph exploration may produce a model that reflects the team's assumptions rather than the domain's actual structure.

#### Related work
- This document does not introduce new naming conventions for implementation artifacts. The conceptual terms used here (abstraction, concern, aggregator, composition layer, graph) are established elsewhere in the Memar specification and are not redefined here. (Migrated from the document-level retired Naming Conventions note)
- The overall approach draws from multiple traditions: DDD (Eric Evans) for the emphasis on domain language and bounded contexts, Event Storming (Alberto Brandolini) for the practice of discovering domain structure through collaborative exploration, and graph theory for the analytical framework used to evaluate model structure. Memar's distinctive contribution is the integration of these traditions into a single, coherent modeling discipline that is tightly coupled with the abstraction and protocol constructs defined in other documents. (Migrated from the document-level retired Prior art)

---

### Decomposition-signal citation re-anchored to the base layer
- Time: 2026-09-10T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) — applied

#### What changed
- The aggregation topic's decomposition guidance now cites [Module Identity and Responsibility](../modules/knowledge/modularity/modularity.md#module-identity-and-responsibility) — the base-layer statement of the same test — instead of Composition Depth as a Decomposition Signal (`docs/khayyam/method.md#composition-depth-as-a-decomposition-signal-no-expression-chaining`) in the Khayyam method document, which itself derives the principle from System and Modularity and only enforces it syntactically at the language layer.
- Reason: a base document never cites the language layer as the authority for its own principles; the language document's own text already names System and Modularity as the conceptual sources, so the base citation is the correct direction. The language layer's syntactic enforcement is named in prose, without a link, as ownership.
- Same-session context: the formerly cited document moved from `docs/khayyam-method.md` to `docs/khayyam/method.md` when the Khayyam layer received its own folder; the re-anchoring makes the citation direction correct regardless of that placement.

### A shared relation is defined once
- Time: 2026-09-23T06:20:00Z
- Type: Added
- Cited:
  - [Modeling → One Authoritative Location per Concern's Data](./modeling.md#one-authoritative-location-per-concerns-data) - Relation: Depends_on: one concern has one authoritative home; a relation copied per domain is that failure
  - [Modeling Practice → Placing a relation](./modeling.practice.md#placing-a-relation) - Relation: Depends_on: the steps a doer follows
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — required the test, and that the doer read it in the practice
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../CONTRIBUTORS.md#cursor)) — wrote

#### What changed
- [Modeling](./modeling.md) states that a relation several domains need is defined once, in the domain that already covers those records. A shared status marker such as draft stays with the shared statuses. A record taking another's place is defined once on thing. A relation only one domain needs stays in that domain. Each domain keeps the rule for when its own records may take the shared relation.
- [modeling.practice.md](./modeling.practice.md) carries the steps for placing a relation. The doer follows those steps and opens the explanation only to check that the statement still matches.

#### Deliberation
Owner: when an edge is about to be created, ask whether other domains need it, as with draft. If they do, place it generally — for a relation between records, under thing — so it is not copied into each domain. The check of modeling.md found the one-location rule for a concern's data, and no statement of this test for a relation. Content's current direction, one identity with change events rather than a new node per edit, is a domain that does not thereby need the successor edge.

Owner: the steps belong in the practice. An agent doing the work reads the practice, not the explanation, unless a step names a section to check.

---

### The decomposition worked outside software
- Time: 2026-10-02T00:00:00Z
- Type: Added
- Propagates to:
  - docs/system.md: Rejected — no change. The worked case leans on *Responsibility*, *When Is a Responsibility Coherent?*, and *Boundary* as this document already states them; it adds no claim about those definitions and no fourth one for a system to satisfy.
  - docs/framework.md: Done — nothing to change in its own text, and its pointer to this document's governing topics is unaffected; the worked case is what its claim that Memar's concepts are language-independent now rests on in this document rather than on assertion.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
- A `The Same Decomposition Outside Software` subsection was added under *Domain Decomposition over Aggregate-Root Modeling*, working the argument's own terms — concern, Responsibility, behavioral boundary, lifecycle, use case — on a monumental tower rather than on a software model. It is the only place in this document where the decomposition is demonstrated outside a codebase, and it is placed inside the section it qualifies rather than in a section of its own, because it is that section's argument carried across a boundary and not a new rule.
- The worked case states why the argument transfers: the definitions it rests on are `System → Responsibility`, which states a Responsibility as a Purpose viewed from a containing System, and `System → When Is a Responsibility Coherent?`, which states what about a Responsibility can be checked. Neither mentions an implementation, so nothing in the decomposition requires one.
- Six concerns are worked, each identified by the test the section gives rather than by being named as a component: ground treatment, structural shell, vertical circulation, masonry supply and provenance, environmental behaviour as a measured performance property, and egress capacity under an authority with its own revision schedule. The subsection states that none of them is a part of a tower in the sense a brick is, because each has a lifecycle that would have been discoverable had the tower never been proposed.
- The case then shows the section's central claim arriving unprompted: no canonical aggregator exists, and three compositions — construction-phase, operations, and public-visit — each assemble overlapping concerns and are named for the use case they serve. A reader looking for the tower is told that its absence is the method working.
- The distinction between a concern and its output is carried across and identified as the translation's hardest test: a structural check returns a load figure, the figure is not the concern, and the concern is the verification of the load path — what is claimed, against what evidence, at what interval, and who may revise the claim. The subsection notes that a model filing the figure as the concern has decomposed the tower into measurements, exactly as filing `ActiveUserID` as the concern decomposes an interface into a return value.
- The subsection closes on what the construction case does not settle: the composition layer is identifiable in software by convention, and for a tower its counterpart is the set of activities and parties through which the concerns are delivered, which nothing in this document's method names. It records that these are identifiable at all, and that the identification is as contestable as any other boundary decision, as belonging to the observer who places it.

#### Considered and not done
- A second worked case, on an organization rather than a physical artifact — rejected: one case establishes that the argument is not about code, and a second would add length without adding reach. Where the remaining gap lies is recorded below rather than papered over with another example.
- Naming the composition layer for non-software systems — rejected: that is the same undecided concept `system.md` records as an open question in *Structure*, and this document does not settle by drafting what another document left open by decision.
- Writing the transfer as a principle ("the decomposition applies to any system") — rejected: a principle this general would restate the argument rather than test it, and the subsection's own contribution is that it worked the argument rather than asserting its scope. The claim being supported is better served by one case that holds than by a sentence that cannot fail.

---

### A model's document is named after the concept it models; the rule was first stated here, then moved to Documentation, and the rename was carried out
- Time: 2026-10-03T00:00:00Z
- Type: Changed
- Cited:
  - [Documentation → File Naming](../modules-plugable/knowledge/documentation/documentation.md#file-naming) - Depends_on: the rule this chat adopted, its purpose as an addressing safeguard, the two boundaries that fix it - that nothing in the name carries the kind of document, and that the front-matter `Title` stays free to read as the model *of* the concept - and the measurements stated with it
  - [Documentation Practice → Folder READMEs](../modules-plugable/knowledge/documentation/documentation.practice.md#folder-readmes) - Depends_on: a folder's main document is the target of that folder's `README.md`, which is a path a reader types and a tool resolves
  - Khayyam Rules Catalog (`bundles/khayyam/rules/README.md`) - Evidence: the one kind of artifact in the repository that already kept this rule - "Each rule has its own folder, holding a main document named after the rule" - which is the precedent the rule was drawn from
- Propagates to:
  - docs/documentation.md: Done - the rule, its evidence, and its boundaries are stated in that document's `File Naming` topic.
  - docs/modeling.md: Done - the deleted topic is replaced by one claim under `Expected Output of a Modeling Chat`, and the Abstract carries the same reduction.
  - docs/modeling.practice.md: Done - its closing pointer now goes to `Documentation` rather than to a topic of this document.
  - modules/computer/binding/ and modules/process/construction/: Pending - each holds a main document and so takes a `README.md` that is a symbolic link to it, and neither link exists. A link is recorded by `git update-index --add --cacheinfo 120000,<hash>,<readme>`, a git operation, so the two links are owed and are recorded here rather than created.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - required, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - drafted, applied
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - merged this chat's two records into this one

#### What changed
- [Documentation → File Naming](../modules-plugable/knowledge/documentation/documentation.md#file-naming) states that a document which is a model is named after the concept the model is about; a folder holding that document is named for the responsibility whose model it is, and the document takes that same name beside it — `modules/computer/binding/binding.md`, `modules/process/construction/construction.md`, `modules/process/control-flow/control-flow.md` — and every companion record takes the same base name (`binding.handoff.md`).
- The rule is mandatory rather than a preference, and its purpose is stated with it: the smallest mistake in addressing a model — the wrong folder segment, or a path rebuilt from memory — should reach nothing rather than reach a real document about a different concept. A fixed name removes that safeguard, because one file name shared by every model folder leaves a wrong folder segment resolving to a real document, two paths differing only in the segment a mistake gets wrong. A subject name carries the mirror risk instead, that a path mistake lands in a neighbouring folder, and in this repository's naming density that is the cheaper cost.
- Six files were renamed: three model documents and their three handoff companions — `modules/computer/binding/model.md` to `binding.md`, `modules/process/construction/model.md` to `construction.md`, `modules/process/control-flow/model.md` to `control-flow.md`, each `model.handoff.md` onto the same base. No folder holds a `model.md`.
- Eleven files' links into the renamed documents were repaired, each re-pointed at the document that now holds the claim rather than at a path that merely exists.
- **Where the rule was first put.** The rule was first stated as a topic of this document, *A Model's Document Is Named After the Concept It Models*, on the owner's ruling that it be mandatory rather than a preference. The ground was addressing: a fixed file name across every model folder means the smallest mistake in building a path reaches a real document about a different concept, which is the failure a reader cannot see.
- **The placement was then corrected, and the rule now lives in `Documentation`.** On the owner's later ruling that a documentation rule — what a name is — has nothing to say in a modeling document and belongs where a file name's meaning is settled, the topic was removed from this document and the rule stated in [Documentation → File Naming](../modules-plugable/knowledge/documentation/documentation.md#file-naming), inside the topic whose own subject is what a file name carries and what a document's kind is. The rule was moved rather than duplicated: a rule stated in two documents is stated twice, and the two copies have no owner to settle the drift between them.
- **What this document says in its place.** One claim, under *Expected Output of a Modeling Chat*: understanding that has not been written down has not been delivered, so a session that reached it ends by writing the documents its understanding produced — the abstractions, concerns, relationships, constraints, boundaries, and supporting documents its output consists of — one document per model, each placed and named under the rule `Documentation` owns. The Abstract carries the same reduction, and the practice companion's closing line points at `Documentation` rather than at a topic of this document. An empty topic titled for the rule was not left behind as a pointer: a topic named for a rule this document no longer owns asserts an ownership the owner has withdrawn.
- **The measurements were re-measured and moved with the rule.** The figures that came with it — 41 of the repository's 115 base documents carrying their own folder's name, and every folder under `modules/khayyam/rules/` (`bundles/khayyam/rules/README.md`) doing so because that catalog states the rule for its own case — were re-measured against the tree as it stands after these renames and are stated where the rule now lives. They are measurements of this repository at this moment, not properties of the rule, and re-measuring them is owed whenever either number is cited.

#### What it does not claim
- It does not claim the rule reaches every base document in the repository. It reaches a document that is a folder's main model; it does not reach a model a session leaves beside the documents it read rather than in a folder of its own, and it does not bind the front-matter `Title`.
- It does not claim the three renamed documents changed. Only their names and the links into them changed; no claim inside any of the three was touched by this chat.
- It does not claim the measurements are evidence for the rule. They record what this repository looks like when measured, and the rule holds whichever number they give.

#### Considered and not done
- **Renaming only the base documents and leaving the folders' own `README.md` files as real files.** A folder with a main document takes its `README.md` as a symbolic link to that document, and a README that is a text file naming its target is a text file that points at a sibling, not a link, whatever it says inside. Two of the three folders have no `README.md` at all and one already carries a link, so what is owed is two links; a link is recorded by `git update-index --add --cacheinfo 120000,…`, which is a git operation and was not performed. The two are recorded as owed above rather than created, and the owner confirmed on the same day that they are owed rather than waived: a folder whose main document is now concept-named and which has no README is a folder a reader cannot enter by the path the rule establishes.
- **Keeping `model.md` beside the concept-named document as a second entry point.** The rule refuses it: the facet system has one separator for the facet key and one home for the subject, and a general word standing where the subject belongs is the one misplacement that system exists to prevent.
- **Extending the rule to every base document in the repository.** Two pairs of base documents share a base name with another across folders, and a wrong subject path there resolves to no file rather than to a neighbour; they were recorded rather than renamed.

---

### Ask what a requirement is a piece of before modeling it
- Time: 2026-10-04T13:27:43Z
- Cited:
  - [Process Research 002](../modules/process/process.changelog.md) - Evidence: the coverage survey behind the change and the review of this document's own scoping decision
- Propagates to:
  - modeling.md: Reference - its decision to keep entry-point questions in Practice was reviewed and upheld; no change
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- A new section, *Stepping Back From the Requirement*, precedes *Starting a New Requirement*: stepping back from what reached the modeler is a step earlier than decomposing it.
- It states what reaches a modeler as the last link of a chain someone else reasoned through, and adds the three questions that reach the links above it: what becomes better if this is done and for whom, what larger question this piece was part of, and whose problem it is.
- It states that the answers may leave the requirement exactly as stated, in which case they cost one exchange, and that they may instead show the proposed mechanism answers a problem nobody has stated yet, that the person living with the outcome is not the requester, or that what is asked to improve is a symptom whose cause lies upstream.
- It states the two-layer answer for the case where the requester cannot be asked: the first layer gives exactly what was asked for, the second states the reading of the underlying problem that answer assumes.
- The section anchors the existing claim that a requirement's wording is evidence to investigate by giving it the same standing for a proposed mechanism.

#### Considered and not done
- The step-back questions were not added to `modeling.md` (Omid Hekayati — decided). That document twice declines to carry entry-point questions as execution practice rather than architectural definition; the survey reviewed the decision and found it sound, and a conduct question added beside it would contradict the scoping the document states about itself.
- They were not added to `process.md` either, which is where they were first proposed (Space Bunny Alpha — argued; Omid Hekayati — upheld the boundary): a document that states what a process is does not say how a modeling chat is opened.
- Naming the origin of these questions in this file was not done (Space Bunny Alpha — argued). Per [Documentation → Citations → Source standing](../modules-plugable/knowledge/documentation/documentation.md#citations), the questions were raised from material of no standing; it is recorded as the inquiry's origin in [Process Changelog - the four disciplines surveyed against Process, Modeling, and their practices](../modules/process/process.changelog.md#four-disciplines-surveyed-against-process-modeling-and-their-practices) instead.

#### Deliberation
The questions were proposed for the concept document first, on the reasoning that a document about modeling should state what a modeler must establish before the work (Space Bunny Alpha — argued). The owner corrected the direction on the boundary between what a document defines and what a procedure follows, and the questions moved to this companion (Omid Hekayati — decided). A second proposal would have added the causal decomposition and the finish-line rule to `process.md` in the same change; it was rejected on the same boundary and its two questions are open in the handoffs instead (Omid Hekayati — decided).

---

### Sufficient maturity is a gate, not a judgment call
- Time: 2026-10-04T00:00:00Z
- Type: Changed
- Cited:
  - [System → What Architecture Is Not](./system.md#what-architecture-is-not) - Considered: the gate was checked against this claim, which holds that architecture is not a phase, and was bounded so that it does not contradict it
  - [Rule → Which Module a Rule Belongs To](../modules/process/rule/rule.md#which-module-a-rule-belongs-to) - Evidence: the subject test that decides a module's home, which the gate's first consequence applies to a folder rather than to a document
- Propagates to:
  - modeling.handoff.md: Done - *The Model as the Primary Artifact* item 1 is recorded as settled and points here; item 2 is narrowed to what the gate leaves open
  - ../.agents/skills/memar/SKILL.md: Done - one working rule added that sends an agent to this gate before code is written, and names the bootstrap exception
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- `modeling.practice.md` gains an eighth step in *The Modeling Workflow*: before code is written for a requirement, state the module it belongs to and that module's contract, and record the questions that stating it raised. The step carries the independence test with it, since a module's home follows its subject and the subject is not known until the requirement has been decomposed far enough to answer whether it is one requirement or several.
- The section gains a paragraph giving the gate three consequences: the bootstrap exception, named and bounded to the code the language itself needs to compile and run; the gate's own width, which asks which module's contract must exist before code is committed to that module and does not hold that architecture is finished before implementation begins; and a module's contents as a standing report on whether the gate was taken, which is a reason to stop and decompose rather than a licence to add to a folder.
- `modeling.handoff.md` records the threshold question as settled by this gate, and states why `modeling.md`'s own wording stays at "should" and "majority": that document states an architectural position, and this companion states the procedure this repository follows.
- The memar skill gains one working rule, beside its existing ones for Cognition and Test, that sends an agent to this gate before code is written and reports an unstated module back rather than proceeding.

#### Considered and not done
- The gate was not added to `modeling.md` (Omid Hekayati - decided). That document twice declines to carry execution practice as architectural definition, and a gate that a session can be refused by is a procedure rather than a position; the same boundary the step-back questions were moved across for the same reason.
- The rule was not stated in the memar skill as its own text (Omid Hekayati - decided). The skill holds agent-specific content only, and a second statement of one principle in a third place is the overlap this repository already has to audit elsewhere.
- `modeling.md`'s "Modeling Before Implementation" was not reworded from "should" to a gate (Space Bunny Alpha - argued). Doing so would make the concept document state this repository's procedure, which is what the companion is for.

---

### The exception is claimed, not self-certified
- Time: 2026-10-04T00:00:00Z
- Type: Changed
- Cited:
  - [Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance) - Considered: whether a practice companion may give a word a bounded sense of its own, which is what naming the exception as a category would have done
- Propagates to:
  - modeling.handoff.md: Done - the settled entry restated so that it no longer names a category
  - ../.agents/skills/memar/SKILL.md: Done - the working rule now names the documents rather than the exception, in the form the other intake rules take
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- The eighth step's exception is no longer a named category. `modeling.practice.md` previously called the code that exists only so a language can be compiled and run "bootstrap code" and told a session to label it as such where it stands; the paragraph now states the bound without the label and states that the exception is not a category an implementation may place itself in — a session claims it, and the claim is the owner's to accept or refuse.
- The paragraph now says what keeps the exception from becoming a general licence: work whose subject is anything other than a language's own ability to run is a mechanism that has not been modeled yet, and the gate reports it back rather than exempting it.
- The skill's working rule names [Modeling](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md) and [Modeling Practice](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.practice.md) the way the intake rules name [Cognition](https://github.com/GeniusesGroup/memar/blob/main/docs/cognition.md), rather than pointing at one section anchor and repeating the exception's wording. The gate is now reached through the documents that state it, and the skill line carries no part of it.

#### Considered and not done
- The word "bootstrap" was not redefined, narrowed further, or replaced (Omid Hekayati - decided). The repository already uses it for a plan phase that carries no definition, for a compiler probe folder, for the state in which a language's first library capsules have no primitive to build on, and for a network's first path; a practice companion that bound it to one narrow meaning would collide with all four, and the audit that found them is recorded in the task's report rather than as a Terminology entry, because no document claims the word as a Memar definition to revise.
- The exception was not widened to "any code written before its module's contract is stated" (Space Bunny Alpha - argued). That reading is wider than the bound it replaced rather than narrower, and it would exempt exactly the case the gate exists to report: code whose subject is a mechanism nobody has modeled yet.

---

### Three handoff entries removed; their answers were already in the governing documents
- Time: 2026-10-04T18:17:58Z
- Type: Fixed
- Propagates to:
  - modeling.handoff.md: Done — the derived-concept-that-grows question, the settled-gate entry, and the pluggable-Rule-coherence question left the open list; each answer already lived in modeling.md, modeling.practice.md, or this changelog (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `Concept Existence vs. Model Existence` no longer carries the question of what happens to a concept that starts as derived and later evolves to carry independent responsibilities. [Modeling → Classification Emerges From Rules and Relations, Not From Intrinsic Labels](./modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) answers it in its second gray zone: such a graduation from label to node is legitimate, but it is a modeling decision to be made explicitly at each evolution point under the same test, never assumed silently in either direction. That test is the independent-responsibility test the same section had already applied to promotion, so the question is answered by the document, not by a second one.
- `The Model as the Primary Artifact` no longer carries the entry marking "sufficient" settled as a gate rather than a judgment call. The gate and its three consequences are in [Modeling Practice → The Modeling Workflow](./modeling.practice.md#the-modeling-workflow) — "The eighth step is a gate rather than a preference, and three things follow from it" — and this changelog's *Sufficient maturity is a gate, not a judgment call* entry already records that this handoff's item was settled and narrowed. The item sat in the open list only because the handoff was a living state capture that no later pass updated; the remaining item in that section is the part the gate leaves open.
- `Extensible Behavior Belongs to Pluggable Modules` no longer asks whether `system.md`'s coherence test is sufficient for deciding when variations must become pluggable Rule modules. This changelog's *Coordination pass with system.md, process.md, and modularity.md* records that the question was resolved there, since `system.md` now states the general test explicitly. The surviving item in that section — how a concept declares its attachment points without an anticipatory contract — is untouched and stays open.
- Nothing in `modeling.md` or `modeling.practice.md` changed. All three answers were already where their governing documents hold them; this chat only removed the handoff's duplicate of settled state, per [Handoff → Open Questions](../modules-plugable/knowledge/documentation/handoff/handoff.md#open-questions), where an entry leaves the artifact once its rule has landed in the governing document and the changelog records the decision.
- The remaining items in the three sections keep their text; where deletion left a single numbered item, its ordinal was corrected from `2.` to `1.`.

#### Considered and not done
- **Marking the three entries as answered in place rather than deleting them.** A handoff is mutable current state, and its settled design lives in the governing document and the changelog; an "Answered" marker would keep a copy of that design in the artifact that most needs to stay short, and the copy would drift.
- **Rewording the surviving sibling items to absorb the removed context.** The gate entry and the coherence entry carried qualifications the neighbouring open items lean on; the neighbours already point at the documents that hold those qualifications, so rewriting them would restate a governing document inside the handoff.

---

### One handoff question closed; five left standing
- Time: 2026-10-04T18:30:13Z
- Type: Fixed
- Propagates to:
  - modeling.handoff.md: Done — the caching-an-expensive-discovered-value question left the open list; the shortcut-edge discipline already answers it (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `Acquired Data vs. Discovered Data` no longer carries the question of when a discovered value that is expensive to recompute may also be persisted as a cached, non-authoritative copy. [Modeling → Edge Types and Their Traditional Counterparts](./modeling.md#edge-types-and-their-traditional-counterparts) answers both halves of it in its shortcut-edge bullet: a shortcut edge "exists purely to make an already-derivable traversal cheaper to compute" — the point at which persisting it is legitimate — and it "is only ever a cache of a fact derivable from other edges already in the graph", to be "modeled and named in a way that makes clear it is not itself authoritative", being "discovered, not acquired, and ... always remain re-derivable from the edges that produced it". That bullet already names [Acquired vs. Discovered data](./modeling.md#acquired-data-vs-discovered-data) as the discipline it carries over, so the answer was written into the same document whose section raised the question.
- Nothing in `modeling.md` or `modeling.practice.md` changed. The section heading went with its only item, since the open list is current state and an emptied section carries none.

#### Considered and not done
- **The criteria separating a history-worthy state change from a safely destructive one (`Modeling State Change as Events, Not Destructive Updates`) was left open.** [Modeling → Modeling State Change as Events, Not Destructive Updates](./modeling.md#modeling-state-change-as-events-not-destructive-updates) answers a weaker question than the entry asks: it places the inherently time-series case and the overwritten-value case under one concern, and states that overwriting "is a decision with real, often unintended, architectural consequences, and that decision should be made deliberately during modeling". That is a requirement to decide consciously, not a criterion telling a modeler which changes may safely be overwritten; the missing sentence would have to say what makes a change's history architecturally significant rather than safely discardable.
- **Caching an evaluated constraint result (`Constraints Belongs to the Constraining Concern`, second item) was left open.** The shortcut-edge bullet never mentions constraint evaluation; treating the cache of a computed result as simply one more shortcut edge restates the passage in other words rather than saying what would have to hold of a constraint result for that cache to qualify — the missing sentence would have to state the conditions under which an evaluated result of external constraints may be persisted and still re-derivable.
- **Where the rule-engine lives and how it queries the graph (`Separating Structure (Code) from Policy (Rule)`, sixth item) was left open.** The section settles the first half — execution "belongs to a separate rule-engine component that reads Rule nodes from the graph", and traversal of the model, not reading code, must answer "which entities are subject to Rule X" — but says nothing about efficient querying at the scale this framework targets, which is the other half of the entry; the missing sentence would have to say how the engine finds the applicable Rules and instances at that scale.
- **Whether an ordinary edge carries its own addressable identity (`Edge identity and reification`) was left open.** [Type → Type and Relations](./type.md#type-and-relations) says only that graph-based domain models are those "where both Nodes and Edges may carry independent meaning", and that a relation "may itself need to become a Type once it has properties like start/end dates or status" — the promotion path the entry already accounts for, not the addressing of an edge where it stands; the missing sentence would have to say whether an unpromoted edge can be named and used as the endpoint of another edge.
- **Approach for a team inheriting a legacy system with no model (`Document-level`, third item) was left open.** [Modeling Practice](./modeling.practice.md)'s opening says discovering, refining, and reviewing "are not separate activities" sharing one procedure, which places an undocumented system among the starting points without saying whether to model from scratch and migrate or to extract the model incrementally from the codebase; the missing sentence would have to state that recommended approach. The entry's own Anticipated Work already carries the legacy transition path as future work, which is the same gap seen from the other side.
- **Marking the closed entry as answered in place rather than deleting it.** A handoff is current state, and its settled design belongs to the governing document and this changelog; an "Answered" marker would keep a second copy of that design in the artifact that most needs to stay short, and the copy would drift. Per [Handoff → What a Handoff Is](../modules-plugable/knowledge/documentation/handoff/handoff.md#what-a-handoff-is), the entry graduates out and this entry carries the record.

---

### Three handoff questions closed: behaviorless concepts, formalism, and the lens signal
- Time: 2026-10-04T20:14:25Z
- Type: Changed
- Cited:
  - [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) — Evidence: the narrowed checkable test the lens signal is taken from.
- Propagates to:
  - modeling.handoff.md: Done — the "A concept that requires no behavior" entry was deleted in full, item 1 under *Models Are Not Reality* and item 2 under *One Reality, Multiple Abstraction Lenses* were deleted, and the surviving items in those two sections were renumbered to `1.`.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Concept Existence vs. Model Existence](./modeling.md#concept-existence-vs-model-existence) now states that behavior is one criterion among several and its absence settles nothing; that a concept whose own rules, lifecycle, validation requirements, or architectural responsibilities are independent is a finished model even where it prescribes no behavior; and that a concept with none of these is a derived representation or contextual view rather than an unfinished model. The sentences sit inside the paragraph that states the criterion, between that criterion and the name test the paragraph already carried. The `A concept that requires no behavior` entry left `modeling.handoff.md`; the Khayyam question it pointed at — whether `tp Name ab` is a legal form — is the language's, and stays open in Abstraction in Khayyam Handoff (`docs/khayyam/abstraction.handoff.md#does-khayyam-allow-an-abstraction-with-no-methods`).
- [What a Model Is](./modeling.md#what-a-model-is) now closes its claim about the medium: the agnosticism is a position rather than a silence, no notation and no method is prescribed, and the reason is that the obligations a model must meet — a stated purpose, selection by that purpose, and an explicit account of what it omits — are stated independently of the medium. Item 1 under `Models Are Not Reality` in the handoff is deleted and item 2 renumbered to `1.`; the notation question under `Graphs as a Modeling Tool` and the methodology question under `Modeling Before Implementation` each name a specific formalism this sentence deliberately leaves unchosen, and both stay open.
- [One Reality, Multiple Abstraction Lenses](./modeling.md#one-reality-multiple-abstraction-lenses) gains the observable signal its "usually" lacked: the distinction turns on independent changeability, not on the lens, and two structures observed through one lens are two concerns when each can be changed, replaced, extended, or reasoned about without the other changing for reasons unconnected to its own purpose. Where that test fails, the two differ only by lens and are one concern counted twice. Item 2 under that heading is deleted and item 1 renumbered to `1.`, leaving open whether the lenses are ever named formally.

#### Considered and not done
- **Restating the abstraction criterion as a numbered list of independent tests (rejected):** the paragraph already carries the disjunction, and a list would imply each term is separately sufficient, which is not what "only when it represents an autonomous concern with its own rules, behavior, lifecycle, validation requirements, or architectural responsibilities" claims.
- **Deciding whether Khayyam's method-less `tp Name ab` form is legal (rejected):** that is the language's question and it stays open in the Khayyam handoff; a modeling position does not settle a grammar.
- **Closing the notation and methodology sibling questions with the same sentence (rejected):** a position that no formalism is prescribed does not settle whether one should ever be, which is what each of those entries asks.
- **Naming the lens signal "the lens test" (rejected):** the section states that the lenses are not entities inside the produced model, and a coined name would give them standing the section denies.

---

### Six open questions answered in place; one answered elsewhere
- Time: 2026-10-04T20:35:35Z
- Type: Changed
- Cited:
  - [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) — Evidence: the coherence test and its stated concern, which decide where a boundary may move
  - [Modularity → Capability Completeness](../modules/knowledge/modularity/modularity.md#capability-completeness) — Evidence: the Module that introduces a relationship owns what makes it meaningful, and the answer this document's handoff entry now defers to
  - Encapsulation in Khayyam → Sovereign Encapsulation (`docs/khayyam/encapsulation.md#sovereign-encapsulation`) — Evidence: the rule that already denies a consumer any route into a capsule's fields
  - [Content → Authoring Syntax vs. Semantic Graph](../modules/knowledge/content/content.md#authoring-syntax-vs-semantic-graph) — Considered: many independent Renderers reaching one graph, which is what makes notation a rendering choice
- Propagates to:
  - modeling.handoff.md: Done — six entries removed across five sections, one section removed entirely, and the endpoint-hosting entry removed as answered elsewhere
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `modeling.md` → *Graphs Are Not Documentation Artifacts* states what a graph asserts — which concerns are nodes, which relationships are edges, and what each edge claims — as unchanged whether the graph is sketched, tabulated, or written out, and that Memar therefore prescribes no notation: one may be offered as a rendering among several, never as the condition a graph must meet to be read. `modeling.handoff.md` *Graphs as a Modeling Tool* no longer asks whether a notation should be prescribed; the merging question remains.
- *Graph Stability as an Indicator of Model Maturity* now separates the two kinds of change: expected refinement changes a boundary's realization, fundamental restructuring moves a boundary, and a move is judged by the coherence test in [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) against a stated concern — what is expected to vary, for whom, under which future change. The handoff entry that asked for the distinction is gone.
- *Classification Emerges From Rules and Relations, Not From Intrinsic Labels* now states what a modeler counts before the independent-responsibility test can be run: repetition carrying its own consistent rules, together with a relation that opens wherever the label applies. `Status` repeats widely and carries neither, which is why frequency alone decides nothing. The handoff entry asking for that pre-test signal is gone.
- *Domain Decomposition over Aggregate-Root Modeling* now states where a validation that differs between two aggregators of the same concerns belongs: either the concern itself — meaning the model conflated two concerns — or a Rule that attaches, never an aggregator's body. The handoff entry asking whether the abstractions or the aggregators handle it is gone.
- [Type → Explicit Behavior Ownership](./type.md#explicit-behavior-ownership) → *The Ownership Graph* states that an aggregator grants no abstraction access to another's internal state: the two are reached only by explicit delegation. Encapsulation in Khayyam → Sovereign Encapsulation (`docs/khayyam/encapsulation.md#sovereign-encapsulation`) already denies the route, so what remains for a linter is a governance diagnostic rather than a new check on reachability. The handoff entry asking for a convention or lint rule is gone, and with it the *Domain Decomposition over Aggregate-Root Modeling* heading, whose two entries both left.
- *Extensible Behavior Belongs to Pluggable Modules* now states the declaration's form — a reference edge named after the concern it acts on, saying where behavior may attach and never what shape it takes — and settles what an attaching Rule must provide on the Module that introduced the capability, per [Modularity → Capability Completeness](../modules/knowledge/modularity/modularity.md#capability-completeness). The handoff's *Extensible Behavior Belongs to Pluggable Modules* section is removed, that entry having been its only content.
- `modeling.handoff.md` *Edge Types and Their Traditional Counterparts* no longer asks which Module hosts a relationship whose endpoints belong to different Modules. That document has answered it; the answer lives in [Modularity → Capability Completeness](../modules/knowledge/modularity/modularity.md#capability-completeness), and neither `modularity.md` nor `modularity.handoff.md` was touched here.

#### Considered and not done
- The *Anticipated Work* bullet proposing a lightweight graph notation was kept. An offered notation is what that bullet describes, and deleting it would close work this decision leaves open.
- No threshold count of label recurrences was introduced. A number would settle by tally what the classification section settles by rules, and would freeze the case of a label that appears twice and still opens a relation.
- The aggregator was not given a context-aware validation seam. That would make each aggregator a second owner of the same check, which [Modularity → Capability Completeness](../modules/knowledge/modularity/modularity.md#capability-completeness) forbids.
- No lint rule was named. Encapsulation in Khayyam → Sovereign Encapsulation (`docs/khayyam/encapsulation.md#sovereign-encapsulation`) leaves enforcement policy to the compiler and linter layer, and a concept document states no diagnostic it has not established itself.
- No abstract attachment interface or required annotation was introduced for a host to declare. That is the anticipatory contract the section exists to avoid; how several Rules attaching to one point are resolved stays open under *Separating Structure (Code) from Policy (Rule)*.
- No pass condition or threshold was added alongside the refinement/restructuring distinction. [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) already holds that two observers may reasonably disagree once the concern is stated, and a sharper rule would contradict it.

---

### The Code/Rule section joins its graph lens to the module lens
- Time: 2026-10-05T08:59:05Z
- Propagates to:
  - modeling.handoff.md: Done - the item asking whether the two framings are one concept removed and the remaining items renumbered; the internal representation of a Rule's condition, conflict resolution among Rules, Rule temporal validity, the Code/Rule boundary test and the rule engine's architecture left open
  - rule.md: Done - the settled two-lens statement lives there, and this section keeps only what the graph lens owes a model
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `### Separating Structure (Code) from Policy (Rule)` keeps its graph-level requirement — a Rule is a first-class node, connected by an edge to the Code element it governs, so that "which entities are subject to Rule X" is answerable by traversal — and now states that the same Rule is a Module developed on its own in the architectural sense ([Modularity → Rules as a Provisional Term](../modules/knowledge/modularity/modularity.md#rules-as-a-provisional-term)), that both statements are of one concept ([Rule → One Concept, Two Lenses](../modules/process/rule/rule.md#one-concept-two-lenses)), that neither lens is primary, and what each lens owes.
- `### Extensible Behavior Belongs to Pluggable Modules` no longer describes Rule as a provisional term; it names the concept as carried both as a node in the model and as a Module developed on its own.
- `modeling.handoff.md` no longer carries the item that set the two framings against each other, and the item asking whether a Rule is itself content the model must represent is left open on its own terms.

#### Considered and not done
- **Replacing the graph-node requirement with the module framing**: rejected. A Rule a model can traverse to and from and a Rule with a boundary of its own are different requirements, and either one alone leaves work the other lens cannot do — which is why the ruling settles both rather than choosing between them (Space Bunny Alpha — argued).
- **Adding a fourth edge kind for Rule nodes**: not done. The edge taxonomy is open in the handoff over what an ordinary edge is addressable in its own right, and adding a kind here would answer that question by naming rather than by ruling.
- **Restating the two lenses in full in this document**: rejected. The graph lens's consequence is what this section states; the module lens's belongs to Modularity.

#### Deliberation
This document had been carrying the graph framing at full strength while explicitly declining to reconcile it with Modularity's, which left the Code/Rule topic resting on a description its sibling document was hedging (Space Bunny Alpha — argued). Joining the two lenses here — each owning its own obligation, neither primary — lets the topic stand on a settled concept and leaves its genuinely open questions, the representation of a Rule's condition, conflict resolution, temporal validity and the Code/Rule boundary test, as questions about a thing now defined rather than about a framing still in dispute (Omid Hekayati — decided).

---

### Six open questions closed by the definitions this document already holds
- Time: 2026-10-05T09:36:18Z
- Type: Changed
- Cited:
  - [Modeling → What a Model Is](./modeling.md#what-a-model-is) — Evidence: "Memar prescribes no formalism — neither notation nor method — because the obligations a model must meet are stated independently of its medium", which is what leaves the discovery technique open
  - [Modeling → Challenging Proposed Concepts](./modeling.md#challenging-proposed-concepts) — Evidence: the challenge every candidate meets whatever surfaced it, on which the technique-agnostic position rests
  - [Modeling → Classification Emerges From Rules and Relations, Not From Intrinsic Labels](./modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) — Evidence: promotion as a decision "made explicitly at each evolution point under the same test, never assumed silently", and the statement that a classification is not an intrinsic property of a node
  - [Modeling → Acquired Data vs. Discovered Data](./modeling.md#acquired-data-vs-discovered-data) — Evidence: acquired data "cannot be recomputed from anything else already in the model", which is what distinguishes the state change worth keeping from the one that may overwrite
  - [Modeling → Modeling State Change as Events, Not Destructive Updates](./modeling.md#modeling-state-change-as-events-not-destructive-updates) — Evidence: a correction is "a new fact that references the effect it corrects, never a deletion or rewriting of the history", which is what carries to a Rule's amendment and repeal
  - [Modeling → Modeling Produces Conceptual Abstractions, Not Implementation Structures](./modeling.md#modeling-produces-conceptual-abstractions-not-implementation-structures) — Evidence: realizations belong to later architectural and implementation work, which is what makes a mechanism choice a non-question at modeling time
- Propagates to:
  - modeling.handoff.md: Done — six entries removed across five sections and the survivors renumbered; the remaining twenty-seven entries are carried to the owner as open
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `modeling.md` → *Modeling Before Implementation* states that Memar fixes the criteria a candidate concept must survive, not the technique that surfaces it, and that event storming, domain storytelling, and a team's own habit are equally acceptable discovery routes. Two handoff entries asked this — the *Modeling Before Implementation* item and the *Document-level* item about prescribed workshops — and both are gone.
- *Classification Emerges From Rules and Relations, Not From Intrinsic Labels* now states what a label's promotion does to the relationships the label carried: promotion moves the label, not what the label carried, so a loop-edge is re-examined at the promotion point and becomes an edge to the new node only by passing the same independent-responsibility test the label had to pass. The handoff entry asking whether those relationships migrate automatically is gone.
- *Modeling State Change as Events, Not Destructive Updates* now states the deciding question for a change worth preserving as history: whether overwriting discards an acquired fact, since a value the model can derive again is discovered and replacing it costs nothing, while a previous value nothing can recompute is acquired and the change that destroys it is an event the model keeps. The handoff entry asking for those criteria is gone.
- *Separating Structure (Code) from Policy (Rule)* now states that a Rule's amendment and repeal are state changes to a concern, recorded as a new fact referencing what it corrects, and that an edge created while a Rule was in force is read against the Rule that created it. The handoff entry asking how temporal validity is tracked and how it meets historical edges is gone; the dedicated Rule sub-model stays under *Anticipated Work*.
- *Edge Types and Their Traditional Counterparts* now states that there is no mechanism to choose at modeling time: the classification is a claim about the domain, stated once as a loop-edge, and whether a realization enforces it statically at compile time or dynamically at runtime is an implementation decision. The handoff entry carrying the unvalidated static-versus-dynamic hypothesis is gone.
- `modeling.handoff.md` no longer asks whether Memar prescribes a modeling methodology, in either of the two places it asked it.

#### Considered and not done
- A rule stating *which* techniques qualify was not written. Any such list would be an enumeration of the criteria's implementations, and would fix the design space of how a session works before the practice companion has been examined against real sessions.
- The unvalidated working hypothesis was not adopted as a rule with softened wording. "Static when the type is always and definitionally the parent" asserts an intrinsic type relationship, which the classification section denies; the resolution keeps the claim in the model and leaves the enforcement mechanism to the realization.
- No threshold, count, or scoring instrument was added anywhere. The session count in *Graph Stability as an Indicator of Model Maturity*, the measurability of the abstraction criterion, and the observability of the early indicators all remain open precisely because a number would settle by tally what this document settles by responsibility.
- An opt-in capability interface for state history was not introduced. The record now states the criterion that decides the question, and whether the concern is exposed as a capability belongs to the protocol layer rather than to this document.
- Nothing was written about sqlc or ent. Both are registered instances whose examination is still owed, and answering them from the definitions above would apply a rule to an unexamined case and report the examination as done.

---

### A model states Types, and the no-formalism position keeps its subject
- Time: 2026-10-05T17:15:06Z
- Type: Changed
- Cited:
  - [Type → Abstract](./type.md#abstract) — Evidence: "every semantic entity is a Type: a semantic entity that has no Type is not an entity this framework can state", and that mathematics — type theory — is the language a system's semantics are stated in
  - [Type → Type Beyond Programming Languages](./type.md#type-beyond-programming-languages) — Evidence: "Where a system's semantics are described in a human language instead, that description is a report of the system's Types, not a substitute for stating them"
  - [Type → Type vs Implementation Type](./type.md#type-vs-implementation-type) — Evidence: "A counterpart across that boundary is either modeled as Types or is not modeled at all", which is what the authoritative-location rule now scopes itself against
- Propagates to:
  - modeling.handoff.md: Done — the *Concept Existence vs. Model Existence* entry is narrowed to the independence half it still asks about
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- *What a Model Is* now says that a model states a system's semantics and that every system is modelable in mathematics, which in this framework is type theory, then keeps the medium-plurality position with its subject intact: Memar prescribes no notation and no method **for how a model is constructed or read**, so the three obligations the paragraph protected — a stated purpose, selection by that purpose, and an explicit account of what it omits — stand unchanged. What the paragraph no longer says is that a natural-language description of a business process is a model; it says such a description reports that system's Types rather than substituting for stating them, while the equation, the diagram, and the prose account all remain carriers of a model.
- *Concept Existence vs. Model Existence* now states that a concept has semantic identity and so is a Type, and that the separate question is whether it earns a model element of its own or is stated as an attribute, derived representation, or contextual view of another Type. The section still supplies what `type.md`'s admission criterion cites it for — the independent-responsibility test that decides whether a concept is an element in its own right.
- *One Authoritative Location per Concern's Data* now scopes its own rule: one location per concern **within one model**, and another organization's model of the same concept is authoritative at its own level rather than being a derived copy of this one, because it is a counterpart whose Types are declared in its own right and what crosses the boundary is that counterpart's model, not a replica of this model's data.
- `modeling.handoff.md`'s *Concept Existence vs. Model Existence* entry is narrowed: the existence half is recorded as settled, and the entry now asks only for the criteria beyond independent responsibility and lifecycle, plus their measurability.

#### Considered and not done
- The technique-agnostic position in *Modeling Before Implementation* was left exactly as it is. Event storming, domain storytelling, and a team's own habit surface candidates; what a candidate must become is now stated as a Type, and neither half of the ruling says how a session gets there.
- The unresolved line asking for formal criteria determining when a concept becomes an independent abstraction was not rewritten. It asks about independence, which is untouched here; narrowing it belongs with whoever rules on the independence criteria the handoff still asks for.
- Nothing was written about a graph's notation. *What a Model Is* now separates the language a model's semantics are stated in from the medium a model is read in, and `modeling.handoff.md` still asks how graphs from different sessions are merged or compared; that question is unaffected and stays open.

#### Deliberation
The report that produced these findings read *What a Model Is* as offering a natural-language description as itself a model, and read that as incompatible with a document declaring mathematics the layer in which semantics are stated. The owner's ruling required the obligations to survive untouched, and they do: only the example that carried the tension changed shape, from an assertion that prose is a model to the statement that prose reports Types. The two readings of *Concept Existence vs. Model Existence* were settled the same way — the section keeps its role as the source of the independence criterion, and the sentence that let a concept exist with no Type is replaced by one that names what is actually separate (Omid Hekayati — decided). The authoritative-location rule reached the same chat from the other direction: read maximally it makes every other organization's state of the same concept a derived copy, which a boundary whose counterpart is modeled as Types in its own right does not support, so the rule was scoped to one model rather than withdrawn (Space Bunny Alpha — argued, drafted, applied).

---

### The maturity gate is written before implementation, not encouraged at it
- Time: 2026-10-05T17:39:20Z
- Type: Changed
- Cited:
  - Test → The Expectation Is Written Before the Work (`docs/modules/process/test.md#the-expectation-is-written-before-the-work`) — Premise: the protocol-layer statement of the same ordering — the written form of a named Process's expectations is produced before the enactment judged against it, its ground is reach, and no development is one for which stating the expectation first is optional
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- *Modeling Before Implementation* no longer opens with "Modeling should reach a sufficient level of maturity before implementation begins" and closes with "For this reason, Memar encourages extensive exploration at the modeling stage before committing to implementation decisions". Both are replaced by a statement of the bar as something written first and of what the bar consists in: "The bar a model must clear before implementation begins is stated before implementation begins, and what it consists in is written down with it: the criteria a proposed model must survive ([Challenging Proposed Concepts](./modeling.md#challenging-proposed-concepts)) and how much unresolved disagreement it may still carry." The paragraph now requires the exploration that reaches that bar and leaves the route that produces it unprescribed, which is the position the section's own closing paragraph already held and which the encouragement never carried. The cost rationale sentence between the two remains as it was.
- The three obligations this section already states are untouched: a proposed model is continuously challenged against the same criteria used throughout modeling, a proposed model is examined against existing concepts before implementation begins, and the majority of conceptual consolidation happens before implementation rather than after it.
- This discharges the `Pending` propagation recorded in `docs/modules/process/test.changelog.md` at line 127, under the entry titled *The floor carries what an expectation must reach, and a green run reports what the party establishes* — "its maturity gate carries the parallel clause the floor sentence just shed; the exact wording is reported to that file's owner rather than edited here". The maturity gate is this document's, it is named there, and it now states the ordering the protocol states; no wording was added to that file and its `Pending` line is left standing, it being outside this change's ownership.

#### Considered and not done
- **Naming a threshold, a count, or a scoring instrument (not done)**: the bar is said to consist in the criteria and in how much unresolved disagreement a proposed model may still carry, and a number would settle by tally what this document settles by responsibility. The same ground is recorded in this file's entry of 2026-10-05T09:36:18Z, and nothing here contradicts it.
- **Requiring that a proposed model carry no unresolved disagreement (not done)**: what the bar names is the amount of unresolved disagreement it may still carry, so this clause is what admits such a model and bounds the amount rather than what forbids it. What that amount is for a given domain belongs to whoever sets the bar, not to this paragraph.
- **Stating the bar as a formality of stages (rejected)**: the reason a bar must be written before implementation is the cost that follows implementation, not a sequence of approvals, and a stage formality would let the writing happen without the bar's content being settled.

---

### False taxonomies given their home beside classification
- Time: 2026-10-12T07:45:14Z
- Type: Added
- Propagates to:
  - agency.md: Done — the general section there narrowed to agency's own instance, [Professional Categories as False Taxonomies](./agency.md#professional-categories-as-false-taxonomies), linking here.
  - cognition.md: Done — the named kinds of thinking are read as a false taxonomy and link here.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- [False Taxonomies Hide Shared Structure](./modeling.md#false-taxonomies-hide-shared-structure) follows *Classification Emerges From Rules and Relations*: a false taxonomy is a classification useful for a local purpose that is mistaken for the structure of what it divides — false, not wrong. The section adds what the agency text did not state: the characteristic form is shared components credited to single classes, recurrence of the same components across treatments of each class is its signal, and the remedy is to model the components and keep the class names as handles for compositions.
- The general examples moved here from agency.md (SOA and Microservices, Relation and Aggregate Root, Content and Semantic), and kinds of thinking joined them.

#### Considered and not done
- **Leaving the concept in agency.md (rejected; owner's decision)**: the claim is about classification in general, and agency was one instance of it; cognition would otherwise have had to cite agency for a modeling concept.
- **A new term, *false classification* (rejected; owner's decision)**: the existing term carried the same sense.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:44:59Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted changes to `modeling.md`, `modeling.practice.md`, `modeling.handoff.md` and this file, other than the *False Taxonomies Hide Shared Structure* work of 2026-10-12T07:45:14Z, which was out of scope. The handoff removals (the behaviorless-concept, formalism, lens-signal, maturity-threshold, notation, methodology, loop-edge promotion, state-change, temporal-validity, aggregator, pluggable-behavior and Rule-framing questions) each match an answer now in `modeling.md` or `modeling.practice.md` and an entry already in this file (2026-10-04T18:17:58Z to 2026-10-05T17:39:20Z); the answers carry their reason and cite governing documents. The two link repairs in this file (`bundles/khayyam/rules`, `modules/process/test.md`) resolve; `memar content check` reports no problem in the four files.
- One fix in `modeling.handoff.md`: *Graphs as a Modeling Tool* item 2 called ent "the sharpest available test" of the document's position; nothing in the project supports ranking it against other instances, so it now reads "a test".
- Left as found, and reported: the handoff gained four open entries that no entry in this file records (*What a Model Is*, *Early Indicators of Modeling Progress*, and the sqlc and ent items). They are open questions and assert nothing about the domain; the *What a Model Is* quotation was checked against `organization/bundles/supply-chain/supply-chain.changelog.md` (Deliberation), but the "retired session file" provenance of the other three could not be checked. Also, the 2026-10-04T20:35:35Z entry closes the *Extensible Behavior* section's first question (whether the coherence test suffices) without naming it; [Modularity → Pluggable Behavior](../modules/knowledge/modularity/modularity.md#pluggable-behavior) answers it in effect, by tying attachment to behavior outside a Module's essential responsibility.

---

### Practice description states a boundary
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- `modeling.practice.md`'s `description` now states what it is not for: mapping an accepted concept onto a type, and critique of material that is not a model, which Documentation — Practice → Description quality criteria requires.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.
