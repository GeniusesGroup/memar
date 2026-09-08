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
- Every checklist and step-by-step procedure that had accumulated in this document — the modeling workflow, Initial Discovery Questions, Challenging a Proposed Concept, Testing an Assumption, Early Indicators of Modeling Progress, and Expected Output of a Modeling Session — was removed, replaced with short principle statements cross-referenced to a new companion `domain-modeling` skill that then held the concrete procedures (Omid Hekayati — practice-document extraction).
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
  - protocols/memory.md: Done — the definitional vocabulary this section now leans on (memory as one class, volatility categories, the dichotomy rejection, the cache-as-derived-copy reading) added there in the same pass; see memory.changelog.md.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

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
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The reference now runs one way: memory.md (protocol layer) cites modeling.md (concept layer) for the rule; modeling.md no longer cites any protocol document. The section is shorter, tool-free, and self-contained at the modeling level.
- The section was shrunk to the rule, the derived-copy reading, the two recurring violations stated without links, and the general modeling-time guidance (the question surfaces during modeling; either Memar's libraries and protocol documents carry the answer, or the organization builds its own library against them); the shadow-tier working-out, the dichotomy link, and the volatility vocabulary were moved into memory.md, which now holds the full treatment; the one direction that remains was kept (memory.md citing this section as the modeling-level statement of the rule) (Super Z).

#### Deliberation
- It was identified that the section's direct links into `protocols/memory.md` created a bidirectional reference between a root concept document and a protocol document, which is unstable — memory's document is developed *on* modeling's method, so the dependency runs one way only (Omid Hekayati).
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
- **Co-discovery of structure and behavior can make modeling sessions feel unfocused,** since node-field discussions are repeatedly interrupted by behavioral questions and vice versa; stakeholders expecting a clean sequential process may find this uncomfortable, behavior-poor or data-centric domains may need extra facilitation, and there is a risk of over-analyzing edge-case behavior before core structural patterns have stabilized. (Migrated from the Behavior-and-Structure topic)
- **The behavioral-complexity-as-signal claim can be overapplied.** Some domains are genuinely complex — regulatory compliance, multi-currency financial settlement, real-time collaborative editing — and no amount of modeling will eliminate their inherent behavioral complexity; applying the principle indiscriminately risks a culture where legitimate domain complexity is dismissed as a modeling failure, producing oversimplified models that cannot handle real-world edge cases. (Migrated from the Behavior-Reveals-Quality topic)
- **Graph stability is a retrospective indicator** — it can only be measured after multiple modeling sessions, so it cannot guide early modeling decisions; and apparent stability may reflect insufficient challenge rather than genuine convergence — a model untested against new requirements or critical review may appear stable simply because it has not been stressed. (Migrated from the Graph-Stability topic)
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
