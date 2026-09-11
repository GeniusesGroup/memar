# Content Changelog

## Changelog

### Initial revision
- Time: 2026-07-27T00:00:00Z
- Type: Added
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: this document follows the Explanation facet structure (Abstract, Introduction, Explanation, Results, Discussion).
  - [Modeling](./modeling.md) — Depends_on: builds on foundational principles — Behavior Before Structure, Code vs Rule, graph-based conceptual modeling, Discovery Before Design.
  - [Terminology](./terminology.md) — Depends_on: definitions in this document must not contradict established project terminology conventions.
  - [HTML5 Specification](https://html.spec.whatwg.org/) — Reference: observational corpus for discovery — one of several existing languages studied, not an architectural authority.
  - [ARIA Specification](https://www.w3.org/TR/wai-aria/) — Reference: observational corpus — demonstrates gaps HTML alone does not cover, particularly around state and role semantics.
  - [Related Work Survey (AI-generated research)](../researchs/semantic_primitive_discovery-related_work-z.ai.md) — Reference: background survey of prior art (RDF, RDFa, JSON-LD, Topic Maps, XForms, etc.). Treat as exploratory research, not architectural authority — see [researchs/README.md](../researchs/README.md) for status caveats.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, reviewed: original concept formulation; 10+ years of iterative idea development; Design Languages project (prior art/prototype); critical review and direction-setting across all discovery sessions.
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5) — argued, rewrote: process critique; Concept/Implementation boundary analysis; Composition vs Aggregate distinction; Addressability and Reference-as-edge critique; document synthesis.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — claimed, argued: early Semantic Interface Architecture framing; Reference-as-edge discovery; Lexical Token vs Sense proposal; Authoring Model vs Syntax distinction.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.0V) — drafted: Related Work Survey and HTML/ARIA element analysis (research, not authoritative).

#### Summary
First revision of this document: a single layered Explanation-facet document defining Content as a conceptual model, covering the concerns discovered across a decade of iterative development and multiple discovery sessions — Semantic (definition and scope), Reference-as-relation, Lexical Token vs. Sense, Addressability, Composition (Aggregate vs. Presentation), Layout, Theme, Event, Type Reference, multi-instance/runtime identity, the Authoring Syntax vs. Semantic Graph split, "Khayyam-manner" language criteria, and the open case of structural notation within an Authoring Syntax itself.

The document's scope and framing changed substantially across the discovery process that produced it; that evolution is recorded here so a future reader is not confused by any apparent contradiction between earlier working assumptions (visible in prior chat logs and interim drafts) and the final structure:

1. **From a CSS-avoidance idea to a full Content model.** The originating idea (write semantic HTML, let a Design Language render it) was narrow and GUI-centric. Discovery broadened it first to include non-GUI modalities (VUI, CLI, Braille), then to question whether HTML itself was an appropriate foundation at all, and ultimately to a model independent of any specific markup language.
2. **From "extend HTML" to "HTML as corpus, not authority."** Early research (retained in [researchs/](../researchs/) for its evidentiary value) catalogued HTML/ARIA elements looking for gaps to patch. This was explicitly abandoned as a *starting point* — though the research itself remains valuable as observational evidence — once it became clear that cataloguing existing tags anchors thinking to HTML's own historical accidents.
3. **From a two-file structure (`semantic.md` + `semantic-catalog.md`) to a single layered document (`content.md`).** An interim proposal to keep principles and a raw discovery catalog in two separate files was reconsidered and reversed: the catalog belongs entirely in [researchs/](../researchs/) (as exploratory, non-authoritative material), while this document itself was widened — not narrowed — into a single document covering Content's full set of discovered concerns at a layered level of abstraction, rather than being split across multiple interdependent architecture files.
4. **A scope-narrowing decision was made, then explicitly reversed.** At one point during discovery, the working conclusion was that this document's scope should be limited strictly to unstructured-content semantics (Reference, Token/Sense, Addressability), with Composition, Layout, Theme, and Event entirely out of scope — on the grounds that those concerns belonged to Khayyam. This narrowing was later explicitly rejected: silence about a real, related concern is not architecturally neutral, and a future reader encountering these concerns with no guidance here would default to unexamined ecosystem assumptions. The final structure instead defines *what each concern means* here, while consistently delegating *how it is mechanically implemented* to host languages and consumer projects — the "Concept vs. Implementation Mechanism" split formalized in Foundational Principles and applied throughout.
5. **From "Domain Aggregate" language to concern-agnostic terminology.** The word "Domain," borrowed early from DDD-adjacent thinking, was deliberately avoided in favor of more precise, non-imported terminology, consistent with the project's general stance (documented in [framework.md](./framework.md)) against treating industry terminology as authoritative without independent redefinition.
6. **From treating Composition as a single concept to distinguishing Aggregate Composition from Presentation Composition.** This distinction emerged specifically from testing an early, overly broad claim ("Composition is just Aggregate, formed at higher layers") against a concrete legacy example, where it clearly failed — presentation-only nodes (action buttons in an invoice row) have no domain counterpart at all.
7. **The Authoring→Graph→Renderer diagram was corrected after review.** An early draft described the Graph→Output relationship as "compiles to," implying a single deterministic output. This was corrected to a two-relationship model: Authoring compiles *to* the Graph (single target), while the Graph is independently *reached by* multiple, simultaneous Renderers (fan-out) — a distinction that directly explains why the Theme/Layout/multi-modal layer exists at all, rather than leaving it implicit. The same conflation had briefly appeared in the document's own drafting and was removed as part of this correction.
8. **The Theme/Layout boundary and the possibility of user-authored Composition were added as an explicit open question ("Where Theme's Authority Ends"), not resolved.** Earlier drafts treated Layout and Theme as adjacent but did not record the deeper uncertainty about where one's authority ends and the other's begins, nor the more radical possibility (raised via the Android Launcher analogy) that user-facing customization freedom might extend beyond styling into Composition itself.
9. **The structural-notation-within-Authoring-Syntax topic was added as a newly surfaced, high-priority open question**, arising only after the rest of the document had substantially settled, from noticing that this project's own Markdown+YAML-front-matter documentation convention exhibits the same "two competing places for the same information" pattern the document argues against elsewhere (the RDFa-vs-JSON-LD case) — this time inside the very format used to write this document.

---

### Migrated to the current documentation structure
- Time: 2026-09-05T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: conversion to the current facet-based documentation structure.
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote: front-matter slimming, provenance migration, heading and cross-reference normalization, Discussion-pattern restructuring.

#### Summary
Brought `content.md` in line with the current Explanation-facet specification:

- Front matter reduced to identity fields (`Title`, `Status`, `Start Date`, `ID`); the former `Citations`, `Contributors`, and `Applied to` fields moved into the Initial revision entry above (`Applied to` was empty — nothing to propagate).
- The `## Change Rationale` top-level section removed from the base document; its Evolution Summary is preserved in the Initial revision entry above. Its Known Limitations and Planned Revisions subsections were dropped rather than migrated, as every item in them restated content already present in the base document's Drawbacks, per-topic Unresolved questions, and Future possibilities.
- Numbered section headings (`### 1. …` … `### 15. …`) replaced with descriptive, unnumbered topic headings; `### 9.1` and `#### 15.1` became unnumbered subsections of their parent topics.
- All plain-text internal cross-references ("Section 4", "Section 13", the malformed "(Section, Introduction)") converted to real hyperlinks per the Internal Cross-References convention.
- Inline bold "Open Question" paragraphs restructured into topic-level `#### Discussion` → `##### Unresolved questions` bundles; the document-wide Unresolved questions list was distributed to the owning topics, keeping only the cross-cutting media-addressing question document-wide.
- Stale `/research/` paths corrected to the actual [researchs/](../researchs/) directory, as relative references.

---

### Second migration wave: Discussion retired; open work moved to the new paired handoff
- Time: 2026-09-11T08:11:30Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the three-section skeleton and the Relevance-discipline routing this migration applies are defined by the Explanation facet's governing specification.
  - [Documentation — Handoff](./documentation-handoff.md) — Depends_on: the Open Questions / Anticipated Work record created by this migration follows the Handoff facet's specification.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.3) - applied

#### What changed
- All ten topic-level `#### Discussion` / `##### Unresolved questions` wrappers were dissolved; their questions (ten topic-level, plus the document-wide cross-cutting media question) moved to the newly created [content.handoff.md](./content.handoff.md) as Open Questions, per the Relevance-discipline routing — open questions are working state, not current design.
- The document-level `## Discussion` section was retired: its Drawbacks record and Prior-art surveys are preserved in this entry below; its Rationale-and-alternatives items are recorded under Considered and not done; its Future possibilities became the handoff's Anticipated Work. The `---` separator preceding the section went with it.
- This was the last remaining second-wave document besides polymorphism, abstraction-implements, giti, and lexer (see [documentation-explanation.handoff.md](./documentation-explanation.handoff.md)); the earlier hesitation about appending to this file is resolved by the owner's direction to run this migration in the same round — the remediation item for the Initial revision entry above (see [documentation-changelog.handoff.md](./documentation-changelog.handoff.md)) remains open and this entry does not touch that entry.

#### Considered and not done (migrated from the retired document-level Rationale and alternatives)
- **Extending RDFa/Microdata in place (rejected)**: embedding structured metadata as attributes inside content tags reproduces, by construction, the exact dual-source/scattered-metadata problem the Type Reference and Authoring Syntax vs. Semantic Graph topics were built to eliminate — regardless of how syntactically convenient any single attribute looks in isolation.
- **Adopting JSON-LD (a single separate metadata block) as the standard target format (rejected)**: a separate block is still a second, independently-maintained source of truth alongside the content itself, and the industry's own migration toward JSON-LD was driven by tooling convenience rather than resolving that duality — it merely relocated where the duplication lives. The Compiler-mediated model treats *any* such target (inline attributes, a separate JSON-LD block, or something else) purely as a generated output, never a hand-maintained source.
- **Adopting schema.org (or any other external vocabulary) as the default Type vocabulary (rejected)**: doing so would import that vocabulary's own modeling choices — which may not agree with this project's own modeling discipline (the `Password`-as-connection-token example) — directly into the architecture's foundation, and external vocabularies are demonstrably subject to unilateral change or deprecation on a timeline outside this project's control (the 2026 schema.org/FAQ-richresult case study). Only the reference *mechanism* is standardized; vocabularies remain external and optional.
- **Simply extending HTML's element/attribute vocabulary (rejected; the original approach of the early research)**: HTML's ~30 years of gradual, historically-motivated accretion means many of its elements are compositions of more fundamental concepts rather than fundamental concepts themselves (e.g., `h1`–`h6` as `Text` + an `Importance` level, rather than six independent concepts) — extending such a vocabulary risks perpetuating its historical accidents rather than correcting them.

#### Related work (from the retired Prior art)
- A detailed survey of prior art (HTML, ARIA, RDF, RDFa, JSON-LD, Topic Maps, Semantic Web stack, Hypermedia/REST, Microformats, Microdata, OWL, SKOS, XForms, UML, HCI pattern languages, Web Components, Design Tokens, VUI grammars, Accessibility Tree) exists in [semantic_primitive_discovery-related_work-z.ai.md](../researchs/semantic_primitive_discovery-related_work-z.ai.md). That survey is AI-generated exploratory research and **carries no architectural authority** — see [researchs/README.md](../researchs/README.md) for the project's general policy on research-directory content; one entry in that survey (CKML) could not be independently verified and should be treated as unconfirmed pending primary-source review, not as an established finding.
- **XForms'** model/view separation via `<xforms:bind>` is the closest existing precedent to the Authoring Model / Semantic Graph split, though XForms never achieved broad adoption and offers no general-purpose (non-form) interface vocabulary.
- **Hypermedia/REST's** link-relation model (`rel="edit"`, `rel="cancel"`) is the closest existing precedent for expressing behavioral/action intent through typed relations rather than dedicated element types — directly relevant to the Reference-as-relation position.

#### Drawbacks (from the retired body Discussion)
- **Analytical cost.** Correctly separating Semantic, Composition, Layout, Theme, and Event — rather than reaching for a familiar mixed-syntax shortcut — requires deliberate, sustained analytical effort per concern. Teams without the discovery process behind this document may find the separations arbitrary or over-engineered until they encounter the specific failure modes (dual-source metadata, singleton widgets, scattered aggregate math) that motivated each one.
- **No implementation yet exists to validate these concepts against real, large-scale use.** Every concept above is discovery-stage; none has been stress-tested against a production system built specifically to this model.
- **Authoring tooling does not yet exist.** No editor support, validation, or auto-completion currently exists for any Authoring Model described in [Authoring Syntax vs. Semantic Graph](./content.md#authoring-syntax-vs-semantic-graph) — such tooling must be built, not assumed.
- **Risk of scope creep is structurally real, not hypothetical.** This document's own scope expanded substantially over the course of discovery (from a narrow CSS-avoidance idea, to a "Semantic Interface Architecture," to the full Content model covering Composition/Layout/Theme/Event). Each concern's "Implementation note" boundary exists specifically to contain this tendency going forward, but the boundary requires active maintenance — future contributors must resist re-absorbing implementation mechanics into this document once they exist elsewhere.
- **This document's own authoring format has not yet been checked against its own principles.** [Structural Notation Within an Authoring Syntax Itself](./content.md#structural-notation-within-an-authoring-syntax-itself) identifies that the document's own Markdown+front-matter convention may itself violate the inline-vs-external distinction this document argues for elsewhere — a self-consistency gap that is acknowledged, not fixed, here.
