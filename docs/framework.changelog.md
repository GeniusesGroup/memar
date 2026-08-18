# Framework Changelog

## Changelog

### Initial draft
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Depends_on: this document builds directly on the terminology philosophy, classification layers, and concept-first thinking established there; its definitions must stay consistent with those principles.
  - [System](./system.md) — Depends_on: this document depends on the foundational definitions of System, Structure, Framework, and Architecture established there — particularly the co-equal relationship between Framework (design space) and Architecture (concrete realization), and the distinction between domain-level and system-level constraints.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: core architectural stance; the document authority principle; the terminology governance concept; the word-weight rebalancing vision; the Framework/Sub-Framework distinction and the degree-of-silence criterion; the Terminology Caveat; rejected "Framework is a System" as the core definition and established Description as Framework's core identity instead; Framework vs. Development Framework as a specialization; frameworks may be implicit as well as explicit; goal-orientation (Purpose Space) as a first-class dimension alongside Constraint Space.
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted: initial draft; argued for and against alternatives; incorporated revisions.
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort, extended thinking) — reviewed: critical review; identified the Framework-as-Aspect ambiguity; pressed for the framework/sub-framework distinction and the degree-of-silence criterion; challenged whether ISA-scale is the threshold for Architecture-as-System; identified Edge Types as needing independent formal treatment; reconciliation pass with System removing the residual "Framework is a System" claim; replaced the "level of abstraction" Framework/Model test with the particular-instance-vs-space-of-instances test; added the upstream-process example to Purpose Space; added the Description definition.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued: argumentation for and against alternatives; incorporated revisions.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote: Document Authority and Terminology Governance topic; restructuring to broader scope; Framework/Sub-Framework formalization; Word-Weight Rebalancing concept for AI model integration.

#### Summary
Established Framework's atomic definition ("a framework is a description of a system"), its co-equal relationship with Architecture (Constraint Space vs. Decision Space), the Framework/Model distinction, explicit vs. implicit frameworks, Framework vs. Development Framework, goal-oriented frameworks and Purpose Space, Framework vs. Library vs. Toolkit, the Framework/Sub-Framework distinction (the degree-of-silence criterion), Memar's own design-space-over-implementation-layers stance, and Document Authority and Terminology Governance including the Word-Weight Rebalancing concept for AI models.

---

### Revision: Framework as Description
- Time: 2026-07-01T00:00:00Z (approximate — this document had no per-revision timestamps prior to this changelog; correct if a more precise date is known)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved.
  - [Claude](../CONTRIBUTORS.md#claude) — argued, rewrote: applied the Definition vs. Explanation principle (proposed for Terminology) to replace a piled-on definition with an atomic one.

#### Summary
Replaced the previous definition — "a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined problem domain" — with the atomic definition: "a framework is a description of a system." All additional properties (hypothetical nature, goal-orientation, relationship to Model, implicit vs. explicit, development framework as specialization) became explanatory content rather than definitional content. *Hypothetical* was retained but explicitly disambiguated from its colloquial meaning ("assumed before realization," not "imaginary or unrealizable"). Framework and Model were distinguished by purpose and level rather than treated as interchangeable — a model describes what a system *is*, a framework describes what systems *may be* within a space; all frameworks employ models, but not all models constitute frameworks. Explicit and implicit frameworks were distinguished as a difference of accessibility, not of kind (Linux's "everything is a file" principle as the example of an implicit framework element). Framework and Development Framework were separated, with "development framework" as the specialization colloquial usage almost always actually means. Goal-oriented frameworks and Purpose Space were introduced: frameworks are purpose spaces as well as constraint spaces, with a consistency requirement that a development framework's own goals must be achievable by its own development process, not only by the systems built within it. Explanatory sections were also cleaned of word-layer conflicts — "constraints" and "capabilities" as components of Structure were no longer used ambiguously where Framework's relationship to Structure was discussed.

#### Rationale and alternatives
The atomic-definition approach was chosen over continuing to pile qualifying adjectives into the definition itself, on the grounds that discriminative power should come from the explanatory structure surrounding a definition, not from the definition trying to do all the work alone — the same principle later applied consistently across Memar's other foundational documents.

---

### Revision: Reconciling Framework-as-Aspect with the Atomic Definition
- Time: 2026-07-18T00:00:00Z (approximate, aligned with the corresponding System changelog entry — "Framework-as-System regression fix" — since the two were resolved together)
- Type: Fixed
- Propagates to:
  - system.md: Done — the corresponding section there was retitled and rewritten in the same pass; see system.changelog.md's "Framework-as-System regression fix" entry.
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: identified that this document's own Future Possibilities section still asserted "the framework itself is an independent System (Framework-as-System)" as settled, and that System's own Framework treatment still presented "Framework is a System" as one of two co-equal, definitional senses of the word — both left over from before the atomic definition above was adopted, and both in direct tension with it. Resolved the tension in both documents in the same pass.

#### Summary
The Explicit and Implicit Frameworks topic now states the Linux "everything is a file" example without asserting that Linux, as a framework, is a System — the Framework-as-Aspect relationship (a framework's influence becoming part of a built system's Structure) holds regardless of whether the framework, considered on its own, independently qualifies as a System. The now-resolved Future Possibilities item asserting Framework-as-System was removed. System's corresponding section was retitled and rewritten in the same pass so that "Framework Considered as a System" is presented explicitly as an optional, instance-specific lens (available to sufficiently rich, evolving frameworks such as Khayyam) rather than a co-equal sense of what "Framework" means — consistent with the general principle, applied elsewhere to Technology and to Architecture, that System is never baked into a concept's core definition.

---

### Revision: Framework/Model Test, Purpose Space Example, Description Definition
- Time: 2026-07-20T00:00:00Z (approximate, aligned with the corresponding System changelog entry — "Attribution corrections, Description definition, and Systems Thinking note")
- Type: Changed
- Propagates to:
  - system.md: Done — the Description definition was added there, at the point where Framework's definition first depends on it, in the same pass.
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: corrected the Framework/Model distinction; added a second Purpose Space example; added the Description definition to system.md.

#### Summary
Three corrections raised in review. First, the Framework/Model distinction was corrected: the previous test ("level and purpose of abstraction") was misleading, since a model can describe something arbitrarily large (a cosmological model still describes one universe) and a framework can describe something arbitrarily small (a framework with two admissible configurations is still a framework). The corrected test is particular instance vs. space of instances — a model describes a *this*, however large; a framework describes a *kind*, however small its space of members. Second, Purpose Space gained a second, distinct example: beyond a framework's stated goals shaping the design space directly, a framework constraint (e.g., "nothing may be assumed by default") can force a *prior* clarifying process into existence — illustrated by the 100-unit residential example, where a detailed description of residents' intended lifestyle must happen before the private-kitchen question can be evaluated, because a habitual answer would itself be an unexamined default. Third, since Framework's definition depends on the word "description," which was previously undefined anywhere in Memar's documents, a short definition — "a statement that represents something in words, or more broadly in any symbolic form" — was added in system.md at the point where Framework's definition first depends on it, using the term's ordinary dictionary sense rather than introducing a new specialized concept.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-16T00:00:00Z
- Type: refactor
- Propagates to:
  - modularity.md, process.md, modeling.md, system.md: Reference — this document's cross-references to system.md's Structure and Responsibility topics were checked against their current content as part of this pass, since those documents were revised earlier in the same review effort.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for this document to be migrated to the current structure, for "RFC" to be replaced with "Document" throughout (per the project-wide convention that RFC names a change-status pathway, not the artifact itself), for a changelog file to be created since none existed, and for a critical review now that more of the surrounding documents have been worked through.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: restructured the document from `Summary/Motivation/Guide-level explanation/Reference-level explanation/Discussion/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); merged the Guide-level building analogy into Explanation as its own topic rather than keeping a separate Guide/Reference split; moved front-matter `Citations` and `Contributor(s)` into this changelog's entries; migrated the three-round `## Change Rationale` history into the changelog entries above, with approximate dates aligned to the corresponding system.changelog.md entries where the two documents were revised together, flagged as approximate; replaced "RFC" with "document" or "Document" throughout the body, including in cross-references to other documents (`[System RFC]` → `[System](./system.md)`, etc.); replaced "capabilities and limitations" with "capabilities and constraints" in Explicit and Implicit Frameworks, matching the term system.md uses; removed the specific identifier "(RFC 495465)" from the Protocol cross-reference under Document Authority, since a document's numeric identifier is not a stable citation form and the relative link already does that job; folded the Purpose Space topic's own nested Unresolved questions and Future possibilities into Framework as Description's single topic-level Discussion, rather than leaving a separately-nested Discussion one level deeper than every other subsection; added a new Unresolved question connecting Purpose Space's goal-orientation to system.md's newly-added Responsibility property; added two Unresolved questions raised by this review — whether Document Authority and Terminology Governance belongs in this document or in terminology.md, and the dangling, unlinked citation to "memar-go generics elimination RFC" under Memar's Framework.

#### Summary
This document is now structured per `documentation-explanation.md`, with "RFC" replaced by "Document" throughout its body and cross-references, front-matter Citations and Contributors migrated to this changelog, and its three-round change history preserved as changelog entries with approximate, flagged dates. No definitional content was changed in this pass beyond the terminology and structural migration and the capability/constraint wording fix; substantive findings from this review are recorded as new Unresolved questions rather than resolved unilaterally.

#### Rationale and alternatives
Considered moving Document Authority and Terminology Governance out of this document into `terminology.md` directly, since its content is general to every Memar document rather than specific to Framework. Deferred instead: `terminology.md` has not been reviewed in this pass, and moving a substantial topic across documents without first checking the destination document's own scope and content risks creating the same kind of duplication or contradiction this whole review effort has been trying to remove. Logged as an Unresolved question instead of decided unilaterally.

---

### Document Authority and Terminology Governance moved to terminology.md
- Time: 2026-08-16T00:00:00Z
- Type: refactor
- Propagates to:
  - terminology.md: Done — "Terminology Authority and Governance" and "Word-Weight Rebalancing" added there in the same pass; see terminology.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved: agreed the section should move once the duplication with terminology.md was confirmed by reading terminology.md directly, and asked that terminology.md itself be extended rather than rewritten.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: confirmed, after reading terminology.md in full, that "Document Authority and Terminology Governance" substantially duplicated terminology.md's "Diverging From Ecosystem Definitions" and "AI Implications" sections, and that the AI-facing half (Word-Weight Rebalancing) stated the same underlying claim with more confidence than terminology.md's own AI Implications section states the working hypothesis it depends on. Shrank the section to a short paragraph pointing at terminology.md's now-expanded sections, removed the topic's own nested Discussion (its Unresolved question about placement is now resolved), and removed the corresponding item from this document's top-level Unresolved questions.

#### Summary
"Document Authority and Terminology Governance" is no longer duplicated in this document. Its content now lives in `terminology.md`, extended in place rather than rewritten, and this document keeps only a short pointer plus the one piece that is Framework-specific: the Protocol document as a worked example of a Definition built to that standard.

---

### Fixed: Memar's Framework overclaimed "the entire software stack" as Memar's scope
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Cited:
  - [README.md](../README.md) — Reference: the project's own README already states Memar's domain-agnostic identity ("developing... technology, software, hardware, apps, gadgets, buildings, organizations/society, and more") and already names "Computer" as the specific software-implementation category under System Categories; this fix aligns the document with that existing scope rather than introducing a new one.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: identified that the Abstract's claim — "Memar's framework defines the design space for the entire software stack" — reads as a claim about Memar as a whole, contradicting Memar's own domain-agnostic identity (also stated in his skill definition for Memar: "developing... any system such as technology, software, hardware, apps, gadgets, buildings, organizations/society, and more"); asked whether Memar's project-level identity should be consolidated in the project README or in a new, dedicated `memar.md`, deferring to the reviewer's recommendation.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: recommended keeping Memar's project-level identity in the existing README rather than creating `memar.md`, since the README already states that identity correctly and at the right scope (domain-agnostic, with "Computer" already named as the software-specific category) — a new document would duplicate rather than consolidate. Rewrote the Abstract and the *Memar's Framework* topic's opening to state explicitly that this document, and that topic specifically, describe Memar's Computer (software) system category, cross-referencing the README for Memar's broader identity, rather than letting the software-stack claim read as a claim about Memar as a whole. Added a corresponding Unresolved question about whether Memar's other system categories need a comparable design-space treatment somewhere.

#### Summary
"Memar's framework defines the design space for the entire software stack" is only true of Memar's software instantiation, not of Memar as a project — the project README already establishes Memar as domain-agnostic (software, hardware, buildings, organizations, and more) and already calls the software-specific instantiation "Computer." This document's Abstract and its *Memar's Framework* topic now say so explicitly and point to the README, instead of implicitly equating Memar with its software instantiation. No content was moved into a new `memar.md`; the existing README already serves as Memar's single, correctly-scoped identity statement.

#### Rationale and alternatives
Considered creating a dedicated `memar.md` to hold Memar's project-level identity, migrated out of the README into the Explanation-facet template. Rejected: the README already states this identity, at the correct domain-agnostic scope, and a README is read by a different audience (first-time visitors to the repository) than an Explanation-facet document is — forcing it into that template would not consolidate anything, it would create a second "what is Memar" document that the README and `memar.md` would then need to be kept consistent with each other, which is the exact duplication risk this whole review effort has been working against.
