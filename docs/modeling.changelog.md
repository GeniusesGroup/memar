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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: core principles; domain decomposition; abstraction justification; the attribute-or-edge test; acquired vs. discovered data; event-aware state modeling; document-spec restructuring; loop-edge classification; edge taxonomy; practice-document extraction; terminology corrections; the unified modeling/review practice; the pluggable-module principle.
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 Pro, extended thinking) — drafted, argued: initial draft, argumentation.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued, reviewed: initial draft; argumentation; independence-signal review; event-framing review.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote: structural revision, template compliance, content enrichment.
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed: critical review, content enrichment.

#### Summary
First structured revision of this document. Added `ID` (495220, derived from the original Start Date). Migrated `Contributor(s)` from the deprecated `contribution`/`task` format to the `Tasks`-based format. Fixed `Citations` `Reason` value for Terminology from the non-standard "Foundation Alignment" to "Depends_on." Wrote the previously empty Abstract and Guide-level explanation sections. Added Discussion bundles (Drawbacks, Rationale and alternatives, Prior art, and where appropriate Unresolved questions and Future possibilities) to every Reference-level topic. Added the missing document-level Discussion and Change Rationale sections. Converted plain-text internal references to hyperlinks. Added additional examples (e-commerce Order/Payment relationship) and expanded existing discussion points with deeper analysis and more alternatives.

---

### Vocabulary separation revision
- Time: 2026-07-02T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### Summary
Replaced implementation-level vocabulary in the modeling phase with Discovery Vocabulary terms (abstraction, concern, conceptual boundary, responsibility). Clarified that modeling outputs conceptual knowledge rather than implementation structures. Added "Modeling Produces Abstractions and Supporting Documents" to establish this vocabulary boundary. Rewrote "Concept Existence vs. Model Existence" and "Domain Decomposition" to consistently use abstraction-level terminology throughout.

---

### Discovery and behavior emphasis
- Time: 2026-07-04T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### Summary
Added a paragraph to "Graphs Are Not Documentation Artifacts" clarifying that graphs serve as a discovery environment where questions, assumptions, and modeling decisions evolve alongside structure, not merely as visualization tools. Added "Modeling Focuses on Behavior Before Structure" to establish that a system's real complexity resides in what it does, not what it stores, and that modeling should prioritize behavioral understanding before structural decisions. Added an explicit definition of "aggregator" in "Domain Decomposition over Aggregate-Root Modeling" to prevent ambiguous interpretation across modeling, architecture, and composition contexts.

---

### Phase relationships and systemic thinking
- Time: 2026-07-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.

#### Summary
Added "Modeling, Protocol, and Architecture" to clarify that these are not sequential pipeline phases but complementary aspects of a single architectural process — modeling discovers domain understanding, protocol captures it as knowledge contracts, and both are architectural in nature. Added a paragraph on systemic thinking to the guide-level explanation, emphasizing that modeling must examine how concerns interact across boundaries rather than partitioning the domain along organizational lines.

---

### Attribute-or-edge test, naming precision, concurrent discovery, and event-aware state modeling
- Time: 2026-07-10T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued.

#### Summary
Added "The Attribute-or-Edge Test" under "Concept Existence vs. Model Existence," operationalizing the independent-responsibility criterion as a mechanical check ("is this data owned here, or is it a named edge to an already-independent concern?"), using a `Product`/`Text` example covering storage, validation, versioning, internationalization, and search as responsibilities properly owned by a shared `Text` abstraction rather than duplicated per node. Replaced the `Order`/`Payment` example in "Modeling Requires Explicit Relationship Analysis" with `Invoice`/`Financial Transaction`, with an explicit note that word choice at the modeling stage is not cosmetic — `Order` and `Payment` were rejected because they smuggle in incorrect assumptions about workflow outcome and implementation layer. Renamed "Modeling Focuses on Behavior Before Structure" to "Behavior and Structure Are Discovered Together," clarifying that behavior and structure are discovered concurrently rather than in strict sequence, while retaining the discipline of interrogating every proposed node or edge for its behavioral consequences immediately. Added "Acquired Data vs. Discovered Data" as a complementary lens to the existing Fundamental/Derived distinction, with a position/velocity example illustrating why a discovered value should not be stored as if it were an acquired one. Added "Modeling State Change as Events, Not Destructive Updates," establishing that state changes are architecturally significant events to be modeled deliberately, without prescribing any specific storage engine or persistence strategy.

#### Rationale and alternatives
Renaming "Modeling Focuses on Behavior Before Structure" to "Behavior and Structure Are Discovered Together" also resolved an internal tension with the adjacent "Behavior Often Reveals the Quality of the Model" section, which already described behavior as co-discovered rather than sequentially deferred — the rename brought the two sections into agreement rather than leaving one implicitly contradicting the other.

---

### Independence signal, event framing, and discovery entry point
- Time: 2026-07-13T00:00:00Z
- Type: Added
- Contributors:
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued.

#### Summary
Added "Reuse Across Contexts as an Additional Signal" beneath the Attribute-or-Edge Test, framing cross-context reuse as a corroborating but non-required signal for independent-abstraction status, with `Text` (reused) and `Invoice` (not reused, still independent) as contrasting examples. Established the `Product`/`Title`/`Text` example as a recurring reference example, cross-referenced from the `Invoice`/`Financial Transaction` example so the structural (attribute-vs-node) and behavioral (invariant-ownership) lessons remain distinct but mutually discoverable. Added an explicit "a discovered concept should not automatically become a stored concept" principle to "Acquired Data vs. Discovered Data." Reordered "Modeling State Change as Events, Not Destructive Updates" to lead with "the model should preserve reality before it preserves projections" and an explicit disclaimer that Event Sourcing, CQRS, and append-only storage are not thereby mandated. Added "Initial Discovery Questions," a short checklist distinguishing how to begin discovering abstractions from the rest of the document's treatment of what a good abstraction looks like, explicitly scoped as an entry point rather than a gate. (This checklist was itself removed in a later revision — see "Specification realignment" below.)

#### Rationale and alternatives
Framing reuse as a corroborating but non-required signal, rather than a primary criterion, was a deliberate choice: independent responsibility and lifecycle remain the actual test, and overstating reuse's importance would have let a genuinely independent but rarely-reused concept (like `Invoice`) look wrongly disqualified.

---

### Specification realignment; practice moved to a skill; loop-edge classification; edge-type vocabulary
- Time: 2026-07-20T00:00:00Z
- Type: refactor
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote: structural revision, template compliance.
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: loop-edge classification, edge taxonomy, practice-document extraction.

#### Summary
Migrated the front matter to the then-current specification (`Contributor(s)` renamed to `Contributors`; `Works` entries shortened to headline style). Moved Motivation under Introduction and added Methodology. Moved the former top-level Guide section under Explanation as its first topic, linked from the Abstract. Removed every checklist and step-by-step procedure that had accumulated in this document — the modeling workflow, Initial Discovery Questions, Challenging a Proposed Concept, Testing an Assumption, Early Indicators of Modeling Progress, and Expected Output of a Modeling Session — replacing them with short principle statements cross-referenced to a new companion `domain-modeling` skill that then held the concrete procedures. Generalized the TODO-marked "Content Before Classification" section into "Classification Emerges From Rules and Relations, Not From Intrinsic Labels," formalizing a loop-edge-to-node promotion mechanism — provisional classifications are represented as self-referencing (loop) edges, promoted to independent nodes only when the classification itself passes the same independent-responsibility test already established in "Concept Existence vs. Model Existence." Added "Edge Types and Their Traditional Counterparts," naming reference, composition/ownership, label, and shortcut/index edges alongside their relational-database counterparts, with an explicit caution that shortcut edges must never become a source of truth.

#### Rationale and alternatives
An intermediate draft of this change mistakenly cited a separate `modeling-practice.md` document via `Citations`; this was corrected, since Skills are not governed by the Document process and are referenced as ordinary links, not `Citations` entries. This intermediate approach (practice content as a Skill) was itself superseded by the next revision below.

---

### Practice moved to a sibling document instead of a Skill; "domain-" prefix dropped; Guide removed; edge taxonomy simplified
- Time: 2026-07-28T00:00:00Z
- Type: refactor
- Propagates to:
  - modeling.practice.md: Done — practice/procedural content now lives there instead of in a Skill.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved: per a project decision made in a parallel conversation, moved practice content out of a Skill entirely and into a sibling document.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### Summary
Moved practice/procedural content out of a Skill entirely and into a sibling document, `modeling.practice.md`, living alongside this document; removed the remaining forward pointers this document had toward that companion content, since the reference relationship runs the other way (the practice document points back here, and even that is kept minimal). Removed the Guide topic entirely: everything it covered was about how this document is operationalized in a session, which became `modeling.practice.md`'s responsibility. Dropped the "domain-" prefix from "domain modeling" in the Abstract and from every "domain-modeling" skill/practice reference throughout — "modeling" alone is Memar's term for this activity. Simplified "Edge Types and Their Traditional Counterparts" from four enumerated, seemingly-exhaustive edge types down to a single architecturally meaningful distinction (an edge is either a shortcut edge or it is not), with reference, ownership, and label demoted to non-exhaustive, illustrative examples of ordinary edges rather than a closed taxonomy. Corrected a misuse of "RFC" in this document's own change history — Memar's terminology reserves "RFC" for external standards-track documents (e.g. IETF RFCs), not for Memar's own document type; "document" is the correct term throughout.

---

### Three-way edge distinction; unified modeling/review practice; pluggable-module principle
- Time: 2026-08-05T00:00:00Z
- Type: Changed
- Propagates to:
  - modeling.practice.md: Done — rewritten to merge model discovery and model review into a single unified procedure.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: the unified modeling/review practice, the pluggable-module principle.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote.

#### Summary
Corrected "Edge Types and Their Traditional Counterparts" a second time: an edge is not simply "shortcut or not" — a loop-edge (a node connected to itself) is a third, structurally distinct kind of edge in its own right, now named as a peer of ordinary edges and shortcut edges rather than folded in as one example of an ordinary edge. Replaced the `Invoice`-total shortcut-edge example with a clearer one (whether an `Invoice` was paid in cash, without traversing every `Financial Transaction` to check each one's account label). Rewrote `modeling.practice.md` to merge model discovery and model review into a single unified procedure rather than two documents, incorporating Model Reading, Node/Relationship audits, a Single Responsibility Check, an Implementation Contamination Check, a Completeness Check, a Common Anti-Patterns table, and Severity Levels from a separately-authored review practice. Added "Extensible Behavior Belongs to Pluggable Modules," establishing — via a discount-mechanism example on `Invoice` — that a concept's model should expose attachment points for independently-modeled, pluggable Rule modules rather than growing new fields or branches to absorb every variation a plugin might need.

#### Rationale and alternatives
Deliberately avoided the title "Code vs. Rule" for the pluggable-module section, since discussion showed that framing itself invites the same conceptual narrowing this document's own terminology guidance warns against. The deeper treatment, including its relationship to Khayyam's own modularity model, was left for a future, dedicated, shared document rather than restated here.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that this document be migrated to the current structure with a paired changelog file, matching the treatment already applied to system.md, protocol.md, and terminology.md.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: this document had already been substantially migrated in earlier revisions (Abstract/Introduction/Explanation/document-level Discussion, with correct lowercase Discussion sub-heading casing throughout, were already in place); the remaining gaps were a missing `## Results` section, front matter still carrying `Citations` and `Contributors` directly rather than in a changelog, and the `## Change Rationale` section itself, which is migrated into the changelog entries above; checked this document for Process-specific content that should migrate to process.md, following the review already applied to protocol.md and terminology.md — found none, since every use of "process" here is either the ordinary-English sense ("modeling process," "business process") or a reference to the Document process (this document's own review/status pathway), not Memar's formal Process concept.

#### Summary
This document is now structured per `documentation-explanation.md`, with the same template as system.md, protocol.md, terminology.md, and process.md. Its Citations, Contributor roster, and full change history now live entirely in this file.

---

### Explicit cross-reference to the formal Process concept
- Time: 2026-08-15T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: pointed out that a reader who models something using only this document, without knowledge of process.md, could reasonably assume "process" carries its ordinary ecosystem-default meaning here rather than Memar's formal definition — this document should not let that ambiguity stand.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: added a paragraph to "Modeling, Protocol, and Architecture" stating directly that this document's informal uses of "process" are ordinary English, not the formal Process concept, and that Protocol actually governs the formal one; added a link to process.md alongside the existing Protocol and Terminology links. Added a second, lighter cross-reference in "Behavior and Structure Are Discovered Together," connecting that section's behavioral vocabulary (failure, retry, concurrency, recovery) directly to process.md's formal treatment of the same vocabulary.

#### Summary
Previously, this document used "process" only in its ordinary English sense throughout, with no signal to the reader that Memar has a separate, formal Process concept at all — someone modeling from this document alone had no reason to go look for one. Two cross-references were added: a direct one in "Modeling, Protocol, and Architecture," the section that already discusses the System→Process→Protocol chain conceptually without naming Process as a defined term, and a lighter one in "Behavior and Structure Are Discovered Together," where the behavioral vocabulary discussed (failure, retry, concurrency) overlaps directly with process.md's own vocabulary.


### Modeling review and vocabulary cleanup
- Time: 2026-08-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: final vocabulary and modeling-boundary corrections.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed: final consistency pass and cleanup.

#### Summary
Removed procedural workflow content from the reference document so that execution guidance remains in `modeling.practice.md`. Clarified that modeling produces abstractions, relationships, constraints, and supporting documents rather than implementation-level structures. Preserved the `Product`/`Title`/`Text` attribute-or-edge example, acquired-versus-discovered data distinction, event-aware state modeling, concurrent behavior-and-structure discovery, explicit aggregation emergence, and pluggable-module principle. Added an explicit statement to the practice document that requirement terminology is evidence to investigate rather than an authoritative model boundary. Removed implementation-level vocabulary from the modeling document and its historical change descriptions to keep the modeling vocabulary consistent.

---

### Coordination pass with system.md, process.md, and modularity.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Propagates to:
  - system.md: Done — the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling now cites system.md's Responsibility section.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a coordinated pass across `system.md`, `process.md`, `modularity.md`, and `modeling.md` together, so shared concepts have one authoritative home each.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: shortened "Extensible Behavior Belongs to Pluggable Modules" to state only the modeling-level consequence and the `Invoice` illustration, pointing at `modularity.md`'s now-existing "Pluggable Behavior" topic for the architectural treatment this section used to carry in full — resolving the forward-reference this section had explicitly left for "a dedicated, shared document" before that document existed; cited `system.md`'s new Responsibility section from the independent-responsibility justification in Domain Decomposition over Aggregate-Root Modeling; resolved Unresolved question 1 under the pluggable-modules Discussion, since `system.md` now states the general test explicitly.

#### Summary
This document had been carrying the full architectural reasoning for pluggable Modules in its own words, with a note already flagging that the material belonged in a shared document once one existed. Now that `modularity.md` exists, that section is reduced to the modeling-level consequence and its illustrating example, referencing `modularity.md` for the rest. The independent-responsibility criterion this document had already worked out informally is now also tied back to `system.md`'s formal Responsibility definition.

---

### Lens plurality, constraint ownership, and edge-direction open questions
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: originated both principles during accounting-domain development discussions (a resource quantity that looked cache-like turning out to evaluate external constraints; several abstraction views repeatedly confused with separate entities); approved final scope and wording.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued: co-developed both principles across two discovery sessions, including the first formulation of constraint copying onto resources and its later correction.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — drafted, reviewed, applied: generalized both findings into principle-level topics without domain examples; added edge bidirectionality and hosting unresolved questions; withdrew an earlier proposed shortcut-edge ownership clause after review showed it conflated two different abstraction lenses.
- Propagates to:
  - modularity.md: Done in this same pass — see modularity.changelog.md; the hosting question added here cross-references it.
  - protocol.md, agency.md: Done in this same pass — observer-facing consequences of Protocol and Agency roles.

#### Summary
Added "One Reality, Multiple Abstraction Lenses": a single reality may be modeled through co-equal abstraction modes (structural, behavioral/process, normative, systemic) that are neither hierarchy levels nor entities inside the produced model, with the warning that parallel structures differing only by lens usually indicate one concern counted several times. Added "Constraints Belong to the Constraining Concern": a constraint originating outside a resource is modeled as a relationship owned by the constraining concern, carrying its own target/satisfied/remaining state and observing the affected resources, never duplicated onto each of them; with the corollary that two related-looking quantities on one node may be independent projections evaluated against different active rules rather than primary-plus-cache. Extended Edge Types Unresolved Questions with two items deferred to storage-semantics design: whether a bidirectional relationship is one Type observed from two directions or two distinct Types (and where relationship identity resides), and which Module hosts a relationship whose endpoints belong to different Modules.

#### Rationale and alternatives
- **Writing current working positions into the document itself (rejected)**: tentative positions stay out of base documents per project convention. Recorded here instead so they are not re-derived later. Working positions at the time of this change: (1) the working preference for a bidirectional pair is two distinct relationship Types, since the human-facing descriptions of the two directions differ regardless of representation; (2) a proposed clause assigning shortcut-edge ownership to the deriving concern was examined and withdrawn — shortcut edges are judged within their own abstraction lens, while acquired/discovered data is a separate lens, and the output of discovered data may itself be an ordinary edge.
