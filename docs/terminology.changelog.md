# Terminology Changelog

## Changelog

### Initial version
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — drafted
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5) — reviewed, expanded

#### What changed
- Created, introducing Memar's terminology philosophy, terminology layers, terminology debt, concept-first reasoning, tool-first anti-patterns, scientific-methodology rationale, terminology-governance principles, and AI-interpretation guidance; establishing terminology as a first-class architectural concern within the Memar ecosystem; and defining the relationship between terminology quality, mental-model quality, and architectural quality (Omid Hekayati — claimed the core concepts, terminology philosophy, architectural rationale, and the three-tier classification; ChatGPT — initial drafting, critique, synthesis; Claude — critical review, clarification, grounding citations, expansion).
- The worked examples (heat pump, container/docker, cloud) were defined (Omid Hekayati — claimed).
- A critique of AI-drafted material was included (Omid Hekayati — claimed).
- The position that independent AI review serves as interim external scrutiny was recorded (Omid Hekayati — claimed).

---

### Review cycle with ChatGPT
- Time: 2026-06-23T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — reviewed, argued.

#### What changed
- Strengthened the Graph example to explicitly cite Graph Theory and Graph Rewriting rather than naming only the anti-pattern.
- Strengthened the Business Terms definition to describe business terminology as optimized for adoption and communication efficiency rather than precision, avoiding an unprovable claim about intent.
- Added Cloud and Container/Docker as worked examples.
- Established the dependency direction that other Memar documents should depend on this document, and not the reverse.

#### Considered and not done
- **Listing the Protocol document in this document's Citations (rejected — explicit decision)**: Protocol is a specific application of the principles established here, not a peer or a prerequisite; the decision was part of establishing the dependency direction above.

---

### Critical review cycle with Claude
- Time: 2026-06-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- A substantial critical-review pass was applied; the internal inconsistency in the Scientific-terms tier was corrected.
- Explicit, criterion-based definitions were added for the Scientific and Technology layers, supplying tier-assignment criteria.
- The open question of whether Protocol belongs in the Scientific layer was resolved by clarifying that the layer is defined by methodology rather than prior academic membership.
- An explicit note was added on what "independent verification" currently means for Memar in practice.
- A deep "Protocol vs. API Specification" section that had begun restating Protocol's own ontology was removed, consistent with the decision that this document should not depend on or import content from other documents.
- The concept-vs-representation pattern was grounded in two citable frameworks instead of an informal "terms migrate" intuition: the "conceptual leakage" pattern was named, grounded in genericized trademark theory and prototype theory.
- The AI Implications section's core claim was marked as an explicit working hypothesis rather than a stated fact.
- The document was expanded throughout from an outline into full explanatory prose.

#### Deliberation
- The Scientific-terms layer, as originally written, was flagged as silently conflating mathematical/formal, empirical/scientific, and philosophical/foundational concepts under a single label (Claude).

#### Considered and not done
- **Describing conceptual leakage as a term "migrating" or "evolving" toward its representation (raised, then rejected).** Reframed as conceptual leakage instead — the underlying concept does not change; usage collapses it with a popular representation of it. This replaces any notion that the concept itself changes over time.

---

### Definition vs Explanation expansion
- Time: 2026-07-05T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### What changed
Precisely defined Comprehensive and Exclusive as the two directions of necessary and sufficient conditions, rather than leaving them as intuitive labels. Clarified that a definition composed of several necessary properties (as in the Protocol document) remains a Definition, not an Explanation, and gave a practical test for telling the two apart. Introduced the regress problem and primitive notions to explain why some Memar concepts are necessarily left without a complete independent definition at a given point in the framework's development, and why this is expected rather than a defect. Added an explicit requirement that a Memar Definition state, rather than leave implicit, when it diverges from a term's common ecosystem usage.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - system.md: Reference only — no change needed there; this entry only corrects terminology.md's own stale description of System.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document is now structured per `documentation-explanation.md`: restructured from `Summary/Motivation/Guide-Level Explanation/Reference-Level Explanation/Drawbacks/Rationale and Alternatives/Prior Art/Unresolved Questions/Future Possibilities/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`).
- The front-matter `Contributor(s)` roster and the prior `## Change Rationale` narrative moved into this changelog's entries (Citations was already empty; the narrative migrated into the changelog entries above); the document's Contributor roster and full change history now live entirely in this file rather than in front matter and a document-level `## Change Rationale`.
- Discussion sub-heading casing was normalized to match the template.
- A nesting inconsistency was corrected: Business Terms sat as a sibling of "Terminology Layers" instead of nested under it, unlike its two sibling layers (Scientific Terms, Technology Terms).
- A stale claim in "The Regress Problem and Primitive Notions" was corrected: System was said to lack a complete formal definition — System now has one, in system.md, so the passage was reframed as a historical illustration of the general pattern rather than a claim about System's current status.

#### Deliberation
- The migration of this document to the current structure with a paired changelog file was requested, along with a check that any Process-related content be examined for migration to process.md, following the same treatment already applied to protocol.md (Omid Hekayati — requested).

#### Considered and not done
- **Migrating Process-related content to process.md (examined, none found)**: this document was checked for Process-specific content, following the same review applied to protocol.md. Found none: this document's only uses of the word "process" are either the ordinary-English sense ("evaluation process," "review process") or the informal, non-Memar sense of an OS process ("Container before Process Isolation," "a process is not defined by an operating system") — neither is Memar's formal Process concept, so no content was moved.

---

### Terminology Authority and Governance, and Word-Weight Rebalancing, absorbed from framework.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Cited:
  - [Framework](./framework.md) — Depends_on: the content absorbed into this entry's additions originated in framework.md's "Document Authority and Terminology Governance" topic; this also resolves the "Migration to the Explanation-facet document template" entry's own open question about eventually citing a stable Framework document, since framework.md now exists with a settled ID (495003) rather than only as informal working material.
- Propagates to:
  - framework.md: Done — its "Document Authority and Terminology Governance" topic was shrunk to a short pointer to the sections added here in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- `framework.md`'s "Document Authority and Terminology Governance" topic substantially duplicated this document's own "Diverging From Ecosystem Definitions" and "AI Implications" sections, and in the AI case stated the same claim with a different, more confident level of certainty than this document uses for it; the non-duplicate content was absorbed here and `framework.md` was left with a pointer instead of a parallel restatement.
- "Terminology Authority and Governance" was added as a new subsection under Definition vs Explanation, right after Diverging From Ecosystem Definitions, covering how a Definition's authority is established (the four elements Comprehensive and Exclusive and Diverging From Ecosystem Definitions already imply, made explicit) and maintained (subsequent documents follow it; revision is possible but costly and recorded in that document's own changelog; popularity does not override precision), without repeating what Diverging From Ecosystem Definitions already states.
- "Word-Weight Rebalancing" was added as a new subsection under AI Implications, carrying over framework.md's mechanism sketch but rewritten to match this document's own epistemic register — presented as one proposed way to act on AI Implications' working hypothesis, not as a settled mechanism.

#### Deliberation
- The principle that a shared concept should live in exactly one place was agreed (Omid Hekayati — approved).
- The extension of this document rather than a rewrite was requested, since it already existed in the current template with its own changelog (Omid Hekayati — requested).

#### Considered and not done
- **Keeping Word-Weight Rebalancing at framework.md's original, more confident phrasing (rejected)**: considered on the grounds that it was already written and reviewed; rejected because this document's AI Implications section is explicit that the underlying claim is an unvalidated working hypothesis, and a mechanism built to act on a hypothesis should not be stated with more certainty than the hypothesis itself carries — doing so would let the more confident copy quietly become the ecosystem's working understanding of AI Implications by virtue of being the more citable-sounding of the two versions. framework.md's original phrasing ("an AI model... would: 1. Load... 2. Resolve...") stated the mechanism far more confidently than this document's own AI Implications section states the hypothesis it would be acting on.

---

### The Default Meaning of an Unreferenced Term added; Vocabulary document retired
- Time: 2026-09-03T00:00:00Z
- Type: Added
- Cited:
  - `docs/vocabulary.md` (deleted) — Evidence: the retired document's own state motivated the rule; it held only two external links (connection-oriented/connectionless, consumed by chapar.md's Ethernet-comparison discussion) and no membership criterion, no front matter, and no changelog of its own, so it had begun functioning as an unmanaged catch-all — the exact failure mode an ungoverned vocabulary list invites.
- Propagates to:
  - `docs/vocabulary.md`: Done — deleted. Its two links moved into [networking.md](./protocols/networking.md)'s Layer presence topic (the classification question is a cross-layer networking concern, not a layer-2 protocol's); the RFC-process paragraph it carried was RFC-era boilerplate rather than governed content, so it died with the file without loss — the substance of that paragraph (a consistent, reviewed path for changes to enter the project's documentation, with statuses that say what may be depended on) is specified authoritatively in [documentation-explanation.md](./documentation-explanation.md)'s Status section, and its remaining wording was generic GitHub pull-request boilerplate.
  - thinking.md: Done — the Discourse Norms' definitions-outrank-terminology entry previously pointed to vocabulary.md as a lookup home; it now points to this document's new section instead.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- **The Default Meaning of an Unreferenced Term** was added as a new section directly after Terminology Authority and Governance, completing that section's boundary statement: governance covers the terms Memar has defined; this section covers all the others (Super Z — drafted). The rule: an unreferenced word carries exactly its general (dictionary or established scientific) meaning — ecosystem redefinitions, industry mythology, and framework narratives do not attach to it. Referencing a Memar Definition is the explicit act that switches a word to its specialized sense.
- The rule replaces the retired `vocabulary.md`, whose role had been to hold pointers to general meanings but which had no membership criterion and had become an unmanaged catch-all.
- The vocabulary links were relocated and the inbound references repointed (Super Z).
- The monolithic example was supplied (Omid Hekayati).

#### Deliberation
- vocabulary.md was judged unsalvageable as a registry: without a hard membership criterion it would only accumulate entries nobody governs — "a place where anything can be dumped" (Omid Hekayati — decided).
- The default-meaning rule was directed to live in this document as an independent section, stated as a general principle rather than tied to the retired file (Omid Hekayati — directed).
- The general-meaning default was further directed to exclude ecosystem definitions and narratives entirely, not merely business-layer ones — a word without a Memar reference means its dictionary/general sense, nothing more (Omid Hekayati — directed).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - terminology.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The `terminology.md` body now carries only the fixed four top-level sections (Abstract, Introduction, Explanation, Results); the `## Discussion` heading and its subsections — `Drawbacks`, `Rationale and alternatives` (with its five `Why…` entries), `Prior art`, `Unresolved questions`, `Future possibilities` — no longer exist in the document.
- The document-level Drawbacks accounting and the four surviving rejected-alternative rationales moved to this entry's `Considered and not done`; the comparative survey of engineering disciplines' reasoning order moved to this entry's `Related work`.
- The nine open questions and eleven future-possibility items moved to the newly created paired handoff (`terminology.handoff.md`) as `Open Questions` and `Anticipated Work`.
- Two `Rationale and alternatives` entries were dropped as already graduated rather than copied: "Why prefer scientific terminology?" is carried by the body's Scientific Terms and Science as Methodology sections, and "Why Three Layers, and Not More" is carried by the Abstract and the Scientific Terms simplification note.
- Body pointers to retired sections were repointed: the Abstract and Scientific Terms references to "Why Three Layers, and Not More" were replaced by the graduated body text and a link to the handoff's `Open Questions`, and the Word-Weight Rebalancing pointer to "Future possibilities" now links to the handoff's `Anticipated Work`.

#### Considered and not done
- **The terminology-first method's costs were recorded, not treated as disqualifying (migrated from the removed document-level `Drawbacks` section)**: the approach increases documentation, learning, review, terminology-analysis, and concept-clarification effort; discussions may initially become slower, because participants are encouraged to clarify concepts before proposing technologies rather than jumping straight to a familiar tool; and some widely accepted industry terminology may require decomposition into more fundamental concepts before it can be used safely within Memar, which itself takes time and can feel, to a newcomer, like unnecessary ceremony around a word everyone already understands well enough for ordinary purposes. Some participants may view the process as unnecessary complexity, particularly under deadline pressure, when a familiar but imprecise term would let a conversation move faster in the short term. Memar considers these costs significantly lower than the long-term costs of reasoning from distorted mental models, which tend to surface much later, much more expensively, and in a form far harder to trace back to their terminological origin; the objective of the method is quality of understanding, not speed of discussion.
- **Using popular terminology as-is (rejected; migrated from the retired "Why not simply use popular terminology?")**: popularity does not imply precision — many popular terms accumulate conflicting meanings over time precisely because their popularity is driven by broad appeal rather than by narrow, precise applicability — so popularity is insufficient on its own as a foundation for architectural reasoning, even though it remains useful for other purposes (discoverability, communication with newcomers, marketing).
- **Eliminating technology terminology (rejected; migrated from the retired "Why not eliminate technology terminology?")**: technology terminology remains necessary, because implementation eventually requires technologies and no system can be built entirely out of scientific principles without ever naming an actual technique or tool; only technology terminology redefining foundational concepts is rejected — technology is a consumer of concepts and should not become the source of concepts.
- **Eliminating business terminology (rejected; migrated from the retired "Why not eliminate business terminology?")**: business terminology often carries valuable historical, organizational, operational, and commercial knowledge — Agile and DevOps, whatever their definitional instability, both encode real, hard-won lessons about how software gets built by actual teams under actual constraints — so the problem is not its existence but its misuse as a conceptual foundation, and it can remain useful provided it does not replace more fundamental concepts in architectural reasoning.
- **Classifying terminology not at all (rejected; migrated from the retired "Why classify terminology at all?")**: terminology influences mental models, mental models influence architecture, and architecture influences system outcomes, so terminology is an architectural concern, not merely a stylistic one; classification provides a mechanism for evaluating terminology quality before it affects architectural decisions, rather than discovering the problem only after the architecture built on top of it has already calcified.

#### Related work
- Most mature engineering disciplines naturally move from Scientific Principles, to Engineering Models, to Technologies, to Tools, before making implementation decisions — structural engineering does not begin with CAD software selection, aeronautical engineering does not begin with simulation tool selection, thermal engineering does not begin with product selection — while software development frequently reverses this order and begins with tools, arguably because software's tooling is cheap and immediate to acquire in a way that a wind tunnel or a structural test rig is not, which removes much of the friction that would otherwise force earlier disciplines back toward first principles. This document's attempt is to restore, within Memar, that direction of reasoning commonly found in mature engineering disciplines, while acknowledging that software's low barrier to tool acquisition makes the discipline harder to sustain than it is in fields where reaching for a tool prematurely is simply not an option. (Migrated from the removed document-level `Prior art` section)
