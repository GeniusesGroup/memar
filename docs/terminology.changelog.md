# Terminology Changelog

## Changelog

### Initial version
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: core concepts; terminology philosophy; architectural rationale; the three-tier classification; critique of AI-drafted material; the worked examples (heat pump, container/docker, cloud); the position on independent AI review as interim external scrutiny.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — drafted: initial drafting, critique, synthesis.
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5) — reviewed, expanded: critical review, clarification, grounding citations, expansion.

#### Summary
Introduced Memar's terminology philosophy, terminology layers, terminology debt, concept-first reasoning, tool-first anti-patterns, scientific-methodology rationale, terminology-governance principles, and AI-interpretation guidance. Established terminology as a first-class architectural concern within the Memar ecosystem, and defined the relationship between terminology quality, mental-model quality, and architectural quality.

---

### Review cycle with ChatGPT
- Time: 2026-06-23T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — reviewed, argued.

#### Summary
Strengthened the Graph example to explicitly cite Graph Theory and Graph Rewriting rather than naming only the anti-pattern. Strengthened the Business Terms definition to describe business terminology as optimized for adoption and communication efficiency rather than precision, avoiding an unprovable claim about intent. Added Cloud and Container/Docker as worked examples.

#### Rationale and alternatives
Established the dependency direction that other Memar documents should depend on this document, and not the reverse — including the explicit decision that the Protocol document should not be listed in this document's Citations, since Protocol is a specific application of the principles established here, not a peer or a prerequisite.

---

### Critical review cycle with Claude
- Time: 2026-06-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: flagged that the Scientific-terms layer, as originally written, silently conflated mathematical/formal, empirical/scientific, and philosophical/foundational concepts under a single label; added explicit, criterion-based definitions for the Scientific and Technology layers; resolved an open question about whether Protocol belongs in the Scientific layer by clarifying that the layer is defined by methodology rather than prior academic membership; added an explicit note on what "independent verification" currently means for Memar in practice; removed a deep "Protocol vs. API Specification" section that had begun restating Protocol's own ontology, consistent with the decision that this document should not depend on or import content from other documents; named the "conceptual leakage" pattern, grounding it in genericized trademark theory and prototype theory; marked the AI Implications section's core claim as an explicit working hypothesis rather than a stated fact; expanded the document throughout from an outline into full explanatory prose.

#### Summary
A substantial critical-review pass correcting an internal inconsistency in the Scientific-terms tier, adding explicit tier-assignment criteria, removing content that had begun duplicating Protocol's own ontology, and grounding the concept-vs-representation pattern in two citable frameworks instead of an informal "terms migrate" intuition.

#### Rationale and alternatives
- **Describing conceptual leakage as a term "migrating" or "evolving" toward its representation (raised, then rejected).** Reframed as conceptual leakage instead — the underlying concept does not change; usage collapses it with a popular representation of it. This replaces any notion that the concept itself changes over time.

---

### Definition vs Explanation expansion
- Time: 2026-07-05T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### Summary
Precisely defined Comprehensive and Exclusive as the two directions of necessary and sufficient conditions, rather than leaving them as intuitive labels. Clarified that a definition composed of several necessary properties (as in the Protocol document) remains a Definition, not an Explanation, and gave a practical test for telling the two apart. Introduced the regress problem and primitive notions to explain why some Memar concepts are necessarily left without a complete independent definition at a given point in the framework's development, and why this is expected rather than a defect. Added an explicit requirement that a Memar Definition state, rather than leave implicit, when it diverges from a term's common ecosystem usage.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - system.md: Reference only — no change needed there; this entry only corrects terminology.md's own stale description of System.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that this document be migrated to the current structure with a paired changelog file, and that any Process-related content be checked for migration to process.md, following the same treatment already applied to protocol.md.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: restructured this document from `Summary/Motivation/Guide-Level Explanation/Reference-Level Explanation/Drawbacks/Rationale and Alternatives/Prior Art/Unresolved Questions/Future Possibilities/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); moved front-matter `Contributor(s)` into this changelog's entries (Citations was already empty); migrated the prior `## Change Rationale` narrative into the changelog entries above; normalized Discussion sub-heading casing to match the template; corrected a nesting inconsistency where Business Terms sat as a sibling of "Terminology Layers" instead of nested under it, unlike its two sibling layers (Scientific Terms, Technology Terms); corrected a stale claim in "The Regress Problem and Primitive Notions" that System lacked a complete formal definition — System now has one, in system.md, so the passage was reframed as a historical illustration of the general pattern rather than a claim about System's current status.

#### Summary
This document is now structured per `documentation-explanation.md`. Its Contributor roster and full change history now live entirely in this file rather than in front matter and a document-level `## Change Rationale`.

#### Rationale and alternatives
Checked this document for Process-specific content that should migrate to process.md, following the same review applied to protocol.md. Found none: this document's only uses of the word "process" are either the ordinary-English sense ("evaluation process," "review process") or the informal, non-Memar sense of an OS process ("Container before Process Isolation," "a process is not defined by an operating system") — neither is Memar's formal Process concept, so no content was moved.

---

### Terminology Authority and Governance, and Word-Weight Rebalancing, absorbed from framework.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Cited:
  - [Framework](./framework.md) — Depends_on: the content absorbed into this entry's additions originated in framework.md's "Document Authority and Terminology Governance" topic; this also resolves the "Migration to the Explanation-facet document template" entry's own open question about eventually citing a stable Framework document, since framework.md now exists with a settled ID (495003) rather than only as informal working material.
- Propagates to:
  - framework.md: Done — its "Document Authority and Terminology Governance" topic was shrunk to a short pointer to the sections added here in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved: agreed a shared concept should live in exactly one place; asked that this document be extended rather than rewritten, since it already existed in the current template with its own changelog.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: added "Terminology Authority and Governance" as a new subsection under Definition vs Explanation, right after Diverging From Ecosystem Definitions, covering how a Definition's authority is established (the four elements Comprehensive and Exclusive and Diverging From Ecosystem Definitions already imply, made explicit) and maintained (subsequent documents follow it; revision is possible but costly and recorded in that document's own changelog; popularity does not override precision), without repeating what Diverging From Ecosystem Definitions already states; added "Word-Weight Rebalancing" as a new subsection under AI Implications, carrying over framework.md's mechanism sketch but rewritten to match this document's own epistemic register — presented as one proposed way to act on AI Implications' working hypothesis, not as a settled mechanism, since framework.md's original phrasing ("an AI model... would: 1. Load... 2. Resolve...") stated it far more confidently than this document's own AI Implications section states the hypothesis it would be acting on.

#### Summary
`framework.md`'s "Document Authority and Terminology Governance" topic substantially duplicated this document's own "Diverging From Ecosystem Definitions" and "AI Implications" sections, and in the AI case stated the same claim with a different, more confident level of certainty than this document uses for it. Absorbed the non-duplicate content here — how a Definition's authority is established and maintained, and the Word-Weight Rebalancing mechanism sketch, re-hedged to this document's tone — and left `framework.md` with a pointer instead of a parallel restatement.

#### Rationale and alternatives
Considered keeping Word-Weight Rebalancing at framework.md's original, more confident phrasing on the grounds that it was already written and reviewed. Rejected: this document's AI Implications section is explicit that the underlying claim is an unvalidated working hypothesis, and a mechanism built to act on a hypothesis should not be stated with more certainty than the hypothesis itself carries — doing so would let the more confident copy quietly become the ecosystem's working understanding of AI Implications by virtue of being the more citable-sounding of the two versions.
