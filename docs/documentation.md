---
Title: "Documentation"
Status: Proposed
Start Date: 2026-07-25
ID: 495826
Applied to: []
Citations:
    - Title: "Diátaxis"
      URI: "https://diataxis.fr/"
      Relation: "Extends"
      Reason: "The Facet concept borrows Diátaxis's core insight — that documentation content is categorically different depending on whether the reader is meant to study it or to follow it — and adapts it to this project's own scope and naming. Diátaxis itself identifies four forms (Tutorials, How-to guides, Reference, Explanation); this project currently distinguishes two facets (Practice, Explanation), with the same underlying two-axis principle." 
    - Title: "Modeling"
      URI: "./modeling.md"
      Relation: Depends_on
      Reason: "Documentation is the result of correct modeling. The concept of Documentation cannot be understood or defined independently from the modeling process."
    - Title: "Anthropic Claude skill-creator"
      URI: "https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md"
      Relation: "Reference"
      Reason: "One of three independently-designed real Skill-file conventions examined as evidence for the Practice facet's governing schema."
    - Title: "OpenAI Codex skill-creator"
      URI: "https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md"
      Relation: "Reference"
      Reason: "Second independently-converged real Skill-file convention, explicitly listing inclusion of auxiliary documentation inside a skill as an anti-pattern."
    - Title: "Microsoft skill-creator"
      URI: "https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md"
      Relation: "Reference"
      Reason: "Third independently-converged real Skill-file convention, sharing the same core schema despite layering additional SDK-specific structure on top."
    - Title: "Dependency Resolution via File URI and Companion Manifest"
      URI: "./khayyam-dependency_resolution.md"
      Relation: "Reference"
      Reason: "The Explanation facet's use of URI for contributor identity and citations follows the same File URI approach already established for dependency resolution."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Identified that one documentation structure cannot serve both 'studying' and 'following' use cases", "Directed the three-facet decomposition (documentation.md, documentation-explanation.md, documentation-practice.md)", "Proposed the Facet naming convention borrowed from Diátaxis"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Fetched and compared three independent real Skill-file conventions (Anthropic, OpenAI, Microsoft)", "Proposed the Facet meta-layer as the correct architectural response to the schema divergence problem"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Works: ["Wrote the initial documentation.md meta-layer", "Improved documentation-practice.md with additional conventions"]
        URI: ""
---

# Documentation
This document defines what a Facet is, names the two facets currently in use, and explains how the facet system extends. It does not itself specify the structure of either facet — that is each facet's own document's job.

## Abstract
Documentation in this project is organized into **Facets** — distinct kinds of documentation content, each with its own governing structure and its own specification document. The word "Facet" is borrowed from Diátaxis, a systematic approach to technical documentation that identifies four distinct forms (Tutorials, How-to guides, Reference, Explanation) based on the reader's need: to learn, to accomplish, to refer, or to understand. This project currently defines two facets — **Explanation** and **Practice** — mapping onto the same two-axis principle Diátaxis describes, but scoped and named for this project's own context. See [Facets](#facets) for the definitions and [Extensibility](#extensibility) for how new facets may be added.

## Introduction

### Motivation
A single documentation structure cannot serve two categorically different reader needs without compromising both. Content meant to be *studied* (specifications, analyses, definitions) demands rich front matter, structured argumentation, citation trails, and contributor attribution. Content meant to be *followed* step by step (procedures, agent instructions, Skill files) demands brevity, imperativeness, and minimal context overhead — every field that is not the procedure itself is pure cost to the agent reading it mid-task. Forcing both kinds of content into one shared schema means either overburdening the procedural content with apparatus it does not need, or under-equipping the analytical content with structure it does. The Facet concept resolves this by acknowledging, upfront, that "documentation" is not one thing — it is a family of related but structurally distinct kinds of content, each deserving its own specification.

### Methodology
The decision to adopt a facet-based architecture was not made in the abstract. It arose from observing a real problem: the earlier version of this specification (then a single `documentation.md`) attempted to govern both analytical specifications *and* procedural Skill files with the same schema. That produced a concrete tension — the same document's thirteenth revision explicitly moved procedural walkthrough content into a separate Skill file, citing Diátaxis as the justification for treating the two as categorically different. The facet concept crystallized that instinct into a named, extensible architectural decision. The Practice facet's schema was not invented — it was adopted from the independently-converged convention of three real AI ecosystems (Anthropic's, OpenAI's, and Microsoft's own skill-creator Skill files), each designed without coordination with the others, providing stronger evidence than a from-scratch design would have.

## Explanation

### Facet
A **Facet** is a named category of documentation content, defined by the reader's relationship to it: what the reader is expected to *do* with the content. Each facet has its own governing specification — a separate document that defines what structure, fields, and conventions documents of that facet must follow. The facet itself is the meta-layer: it names the category, states what makes it distinct, and points to its specification.

The concept is borrowed from Diátaxis (δῐᾰ́τᾰξῐς: dia, "across" + taxis, "arrangement"), a documentation framework by Daniele Procida that identifies four distinct forms of documentation along two axes. The first axis distinguishes content the reader follows *in order to act* (practical) from content the reader studies *in order to understand* (theoretical). The second axis distinguishes content oriented toward *learning a new subject* (directed, guided) from content oriented toward *accomplishing a specific goal or looking up a specific fact* (undirected, self-serve). The intersection of these two axes produces Diátaxis's four quadrants: Tutorials (practical + learning), How-to guides (practical + goal-directed), Reference (theoretical + fact-directed), and Explanation (theoretical + understanding-directed). This project's Facet concept adopts the first axis — the practical/theoretical distinction — as the primary differentiator between its own facets, because that is the axis along which the structural requirements of the content diverge most sharply in this project's context.

#### Discussion

##### Rationale and alternatives
- **Keep a single, shared documentation structure for all content (rejected)**: this was the status quo, and it produced the concrete tension described in Methodology — procedural and analytical content ended up competing for the same schema's attention. The Facet decomposition resolved that by giving each kind of content a structure optimized for its own use case.
- **Use the names "Why" and "How" for the two facets (rejected)**: "Why" does not describe what the Explanation facet contains — it contains specifications, definitions, analyses, and design decisions, not only reasons or motivations. "How" is closer but still too narrow — Practice encompasses any content meant to be followed, not only step-by-step procedures. "Facet" and the specific facet names (Explanation, Practice) carry less misleading connotation and align with an established external framework.
- **Adopt all four Diátaxis quadrants from the start (considered, not chosen)**: Diátaxis's four-way split (Tutorials, How-to guides, Reference, Explanation) is well-motivated for large-scale user-facing documentation sites. This project's current documentation needs do not yet require that granularity — the practical/theoretical axis alone produces the structural divergence that matters here. Starting with two facets and leaving room for more (see [Extensibility](#extensibility)) follows this project's own methodology: adopt what is needed now, not what might be needed later, and extend when a real need arises.

##### Prior art
Diátaxis itself is the primary prior art. Its four-quadrant model has been adopted by documentation projects at Vonage, Gatsby, and Cloudflare, among others — cited on Diátaxis's own site as case studies. The Tyree-Akerman architecture-decision-record template (cited in [documentation-explanation.md](./documentation-explanation.md)) is independent, narrower evidence for the same underlying principle: that different documentation purposes converge on the same structural concerns even when designed without knowledge of each other.

The three independently-converged Skill-file conventions (Anthropic, OpenAI, Microsoft — see Citations) are evidence from the Practice side specifically: all three arrived at the same minimal schema (name/description-only frontmatter, progressive disclosure, no auxiliary documentation inside the skill folder) without coordination, demonstrating that the structural requirements of Practice-facet content are not this project's invention but a genuinely load-bearing constraint that emerges wherever this kind of content is produced.

##### Unresolved questions
1. Whether the second Diátaxis axis (learning/accomplishing) will ever become relevant within this project's scope — if it does, the current two-facet model splits cleanly along that axis without structural upheaval.
2. Whether a facet should carry any metadata of its own (a canonical name, a one-line definition, a reference to its governing specification) in a centralized registry, or whether the current loose convention (each facet is simply documented in its own specification file, cross-referenced from here) is sufficient.

### Facets currently defined
Two facets are defined as of this document's current revision. Each is specified in its own document, following the Explanation facet's own structure — meaning that the specifications of both facets are themselves Explanation-facet documents.

#### Explanation
Content meant to be *studied* to understand something: specifications, analyses, design decisions, concept definitions, and any document whose primary purpose is for a reader to comprehend a subject rather than to execute a procedure.

**Governing specification:** [documentation-explanation.md](./documentation-explanation.md)

**Key structural characteristics:** rich YAML front matter (identity fields, status lifecycle, citations with typed relations, contributor attribution with task tracking), a fixed body skeleton (`Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`, `Change Rationale`), and a consistent Discussion pattern for rationale, drawbacks, prior art, and open questions at every level of the document.

The Explanation facet's structure draws on conventions found across research papers, IETF standards documents, and architecture decision records, unified into a single shared structure that applies regardless of the document's subject — whether it is a protocol specification, a product requirement, or a concept definition.

#### Practice
Content meant to be *followed* to accomplish something: step-by-step procedures, agent instructions, and Skill files — any document whose primary purpose is for a reader (human or AI agent) to execute a sequence of actions and produce a result.

**Governing specification:** [documentation-practice.md](./documentation-practice.md)

**Key structural characteristics:** minimal front matter (exactly `name` and `description`, no other fields), a body that stays under roughly 500 lines, three-level progressive disclosure (metadata, body, bundled resources), and an explicit prohibition against including auxiliary documentation (README, CHANGELOG) inside the skill folder.

The Practice facet's schema is not this project's invention — it is adopted from the independently-converged convention of three real AI ecosystems (Anthropic, OpenAI, Microsoft). See [documentation-practice.md](./documentation-practice.md) for the full specification and the evidence for this adoption.

#### Discussion

##### Rationale and alternatives
- **Name the facets "Specification" and "Skill" instead of "Explanation" and "Practice" (rejected)**: "Specification" describes a specific *kind* of Explanation-facet document, not the facet itself. A concept definition, an analysis, or an architecture decision are all Explanation-facet documents but none of them is a "specification." Similarly, "Skill" describes the file format and folder convention of the Practice facet's most common instantiation, not the facet itself. The facet names should describe the *reader's relationship* to the content, not one specific format it might take.
- **Make the facet names language-agnostic (considered, not chosen)**: English facet names are already used throughout this project's technical content and tooling. Introducing a second set of names in another language without a concrete need would add a translation obligation with no clear benefit. If a future need arises for non-English facet names, the facet system is abstract enough to accommodate it.

### Which facet does a document belong to?
The decision is made by the document's author, guided by the document's *primary purpose*: if a reader is expected to study it to understand something, it is Explanation; if a reader is expected to follow it to accomplish something, it is Practice. Most documents are unambiguous. When the boundary is unclear — for example, a document that contains both analytical content and a step-by-step procedure — the author should ask which purpose dominates: if the procedure is the document's reason for existing and the analysis exists only to support it, the document is Practice (with the analytical portion treated as context-setting within the procedure). If the analysis is the document's reason for existing and a brief procedure is included only as an illustrative example, the document is Explanation.

#### Discussion

##### Unresolved questions
Whether a single document should ever be allowed to carry both facets' structures simultaneously (for example, an Explanation-facet body with a Practice-facet appendix) is not settled. The current position — one facet per document, choose the dominant purpose — is simpler and avoids the ambiguity of mixed-facet documents, but may prove too rigid if a real need for mixed content arises.

### Extensibility
The facet system is designed to be extensible without structural upheaval. New facets may be added by writing a new governing specification document (itself an Explanation-facet document) and registering it here. The current two-facet model maps onto the first Diátaxis axis (practical/theoretical). If a future need arises, the second axis (learning/accomplishing) provides a natural splitting point:

- **Explanation** could split into **Reference** (fact-directed: APIs, field definitions, configuration catalogs — content a reader looks up, not reads end-to-end) and **Explanation** (understanding-directed: design rationale, concept definitions, analyses — content a reader studies to build mental models).
- **Practice** could split into **Tutorial** (learning-directed: guided walkthroughs meant to teach a newcomer a subject from scratch, where the reader's learning journey is the point, not the end result) and **How-to** (goal-directed: step-by-step procedures for accomplishing a specific task, where the reader already knows the basics and just needs the steps).

These four-way names (Reference, Explanation, Tutorial, How-to) are not adopted here — they are Diátaxis's own names, and this project has no current need for that granularity. But the facet system's design means that if and when the need arises, the extension is a matter of writing new specification documents and updating this section, not a fundamental redesign.

#### Discussion

##### Rationale and alternatives
- **Define all four facets now, even though only two are needed (rejected)**: would produce two empty or near-empty specifications — exactly the mistake this project's own Methodology warns against (designing structure in the abstract instead of testing it against a real document). Defining a facet's structure before there is a real document of that kind to test it against risks producing a specification that looks complete but does not actually serve the use case it was designed for.
- **Use a formal facet registry file instead of this prose section (considered, not chosen)**: a machine-readable registry (YAML or JSON) would make facet discovery automatable. At the current scale of two facets, the overhead of maintaining a separate registry file alongside the prose explanation is not justified. The prose here is authoritative; a registry can be extracted from it mechanically if tooling ever needs one.

##### Prior art
Diátaxis's own four-quadrant model is the existence proof that this two-axis decomposition is stable under extension. Projects that adopted Diátaxis (Vonage, Gatsby, Cloudflare) did not start with all four quadrants fully populated — they grew into them as their documentation matured, exactly the pattern this section describes.

##### Future possibilities
- If tooling is built that consumes facet metadata, a formal facet registry could be extracted from this section without changing the underlying model.
- If a future document type demonstrates a need that fits neither Explanation nor Practice cleanly (for example, a document that is primarily a worked example or a decision log with no analytical argument), a third facet could be added — the system does not require the number of facets to remain at two.

### Relationship between this document and its facet specifications
This document (`documentation.md`) is the entry point and meta-layer. It defines what facets are, names them, and explains extensibility. It does not itself specify the structure of any facet — that is each facet's own governing document's job. The three files form a hierarchy:

| Document | Role | Facet it follows |
| --- | --- | --- |
| `documentation.md` (this document) | Meta-layer: defines Facets, names current facets, explains extensibility | Explanation |
| `documentation-explanation.md` | Governs the Explanation facet: specifies structure, fields, body sections, and conventions | Explanation |
| `documentation-practice.md` | Governs the Practice facet: specifies Skill-file schema, progressive disclosure, writing style | Explanation |

All three are Explanation-facet documents — they are specifications to be studied, not procedures to be followed. The documents *produced with the help of* `documentation-practice.md` (such as a `write-a-document/SKILL.md`) are Practice-facet documents. The governing specifications and the documents they govern belong to different facets by design: the Explanation facet's specification tells you how to write an Explanation-facet document, while the Practice facet's specification tells you how to write a Practice-facet document.

#### Discussion

##### Prior art
This pattern — a meta-specification that defines categories and points to per-category specifications — is common in modular standards. IETF RFCs, for example, are organized by category (Standards Track, Best Current Practice, Informational, Experimental) with separate documents defining what each category means, while the overall RFC process document defines what the categories are and how they relate. The same principle applies here at a smaller scale.

## Results
Insufficient time has passed since this facet-based architecture was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Adding a meta-layer document means a reader who wants to understand the full documentation system must now consult three files instead of one. This is a deliberate trade-off: the three-file structure eliminates the structural compromise of the earlier single-file approach, at the cost of one additional file to read. The mitigating factor is that a reader who only needs to *write* a document of one facet (by far the most common case) only needs that facet's governing specification and the companion Skill file — the meta-layer is needed only when understanding the system as a whole.

### Rationale and alternatives
- **Keep a single `documentation.md` that governs both facets inline (rejected)**: this was the pre-facet approach, and it produced the concrete tension described in Methodology — the Practice facet's schema (adopted from three real ecosystems) fundamentally conflicts with the Explanation facet's rich front matter. A single document can describe both, but it cannot *govern* both with a single consistent set of rules.
- **Give each facet an entirely independent name, unconnected to any external framework (considered, not chosen)**: borrowing from Diátaxis gives the facet concept an established theoretical grounding and a clear, externally-referencable definition. An entirely independent naming scheme would require this document to do more definitional work for less benefit.

### Prior art
The earlier single-document approach (then `documentation.md`, now `documentation-explanation.md`) went through thirteen revisions, several of which directly addressed the tension between procedural and analytical content. The sixth revision introduced the `Optional Sections` catalog as a mechanism for accommodating different document purposes within one structure. The thirteenth revision moved procedural content into a separate Skill file, citing Diátaxis. The facet concept is the architectural crystallization of that thirteenth-revision instinct — not just moving the procedural content elsewhere, but explicitly naming *why* it belongs elsewhere.

### Unresolved questions
1. Should the meta-layer (`documentation.md`) eventually contain a machine-readable facet registry (for example, a YAML block listing each facet's name, governing specification, and one-line definition) in addition to the current prose description?
2. Whether the three-file structure itself should be reconsidered if the number of facets grows beyond three or four — at that point, the meta-layer's prose may become long enough that a tabular or registry-based approach is more maintainable.

### Future possibilities
If a third or fourth facet is ever added, the meta-layer's [Facets currently defined](#facets-currently-defined) section grows by one entry per facet, and each new facet's governing specification follows the same pattern: an Explanation-facet document that specifies the new facet's structure, cross-referenced from here. No change to the facet concept itself or to the existing facet specifications is required — the system is additive by design.

## Change Rationale
- **Initial specification.** Created as the meta-layer of the three-file documentation architecture, defining the Facet concept (borrowed from Diátaxis), naming the two current facets (Explanation, Practice), and describing how the system extends along Diátaxis's own two-axis model. Adopted the Practice facet's schema from the independently-converged convention of three real AI ecosystems (Anthropic, OpenAI, Microsoft) rather than inventing a project-specific one. Split from the former single `documentation.md` (now `documentation-explanation.md`) after the thirteenth revision of that document showed that procedural and analytical content could no longer share a single governing schema without compromising both.
