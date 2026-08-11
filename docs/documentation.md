---
Title: "Documentation"
Status: Proposed
Start Date: 2026-07-25
ID: 495820
---

# Documentation
This document defines what a Facet is, names the three facets currently in use, and explains how the facet system extends. It does not itself specify the structure of any facet — that is each facet's own document's job.

## Abstract
Documentation in this project is organized into **Facets** — distinct kinds of documentation content, each with its own governing structure and its own specification document. A facet is defined by the reader's relationship to the content: what the reader is expected to do with it. This project currently defines three facets — **Explanation** (content meant to be studied to understand something), **Practice** (content meant to be followed to accomplish something), and **Changelog** (content meant to be consulted to audit how an artifact changed over time). See [Facets](#facets) for the definitions and [Extensibility](#extensibility) for how new facets may be added.

## Introduction

### Motivation
A single documentation structure cannot serve two categorically different reader needs without compromising both. Content meant to be *studied* (specifications, analyses, definitions) demands rich front matter, structured argumentation, citation trails, and contributor attribution. Content meant to be *followed* step by step (procedures, agent instructions, Skill files) demands brevity, imperativeness, and minimal context overhead — every field that is not the procedure itself is pure cost to the agent reading it mid-task. Forcing both kinds of content into one shared schema means either overburdening the procedural content with apparatus it does not need, or under-equipping the analytical content with structure it does. The Facet concept resolves this by acknowledging, upfront, that "documentation" is not one thing — it is a family of related but structurally distinct kinds of content, each deserving its own specification.

A third need surfaced once the first two facets were in active use: recording why an artifact changed over time. A reader consulting such a record is neither studying the artifact's current design (Explanation) nor following a procedure against it (Practice) — they are auditing history. Rather than leaving this as ad-hoc per-document convention, the Changelog facet was added to give it the same named, extensible treatment as the other two.

### Methodology
The decision to adopt a facet-based architecture was not made in the abstract. It arose from observing a real problem: the earlier version of this specification (then a single `documentation.md`) attempted to govern both analytical specifications *and* procedural Skill files with the same schema. That produced a concrete tension — the same document's thirteenth revision explicitly moved procedural walkthrough content into a separate Skill file, on the principle that procedural and analytical content are categorically different. The facet concept crystallized that instinct into a named, extensible architectural decision. The Practice facet's schema was not invented — it was adopted from the independently-converged convention of three real AI ecosystems (Anthropic's, OpenAI's, and Microsoft's own skill-creator Skill files), each designed without coordination with the others, providing stronger evidence than a from-scratch design would have. The Changelog facet was added later, after the same `<base>.changelog.md` pattern was being applied across multiple artifacts and naming it as a Facet proved a smaller conceptual cost than leaving it as implicit convention.

## Explanation

### Facet
A **Facet** is a named category of documentation content, defined by the reader's relationship to it: what the reader is expected to *do* with the content. Each facet has its own governing specification — a separate document that defines what structure, fields, and conventions documents of that facet must follow. The facet itself is the meta-layer: it names the category, states what makes it distinct, and points to its specification.

The core observation is that documentation content is not homogeneous: a reader studying a specification to understand a design, a reader following a procedure to accomplish a task, and a reader consulting a history to audit changes are doing three categorically different things, and the structure that serves each best is not the same. Forcing all three into one shared schema means either overburdening the simpler kinds with apparatus they don't need, or under-equipping the richer kinds with structure they do. The Facet concept resolves this by naming each kind upfront and giving it its own governing specification.

#### Discussion

##### Rationale and alternatives
- **Keep a single, shared documentation structure for all content (rejected)**: this was the status quo, and it produced the concrete tension described in Methodology — procedural and analytical content ended up competing for the same schema's attention. The Facet decomposition resolved that by giving each kind of content a structure optimized for its own use case.
- **Use the names "Why" and "How" for the two facets (rejected)**: "Why" does not describe what the Explanation facet contains — it contains specifications, definitions, analyses, and design decisions, not only reasons or motivations. "How" is closer but still too narrow — Practice encompasses any content meant to be followed, not only step-by-step procedures. "Facet" and the specific facet names (Explanation, Practice) carry less misleading connotation and describe the reader's relationship to the content directly.

##### Prior art
The Tyree-Akerman architecture-decision-record template (cited in [documentation-explanation.md](./documentation-explanation.md)) is independent, narrower evidence for the same underlying principle: that different documentation purposes converge on the same structural concerns even when designed without knowledge of each other.

The three independently-converged Skill-file conventions (Anthropic, OpenAI, Microsoft — see [documentation-practice.md](./documentation-practice.md)) are evidence from the Practice side specifically: all three arrived at the same minimal schema (name/description-only frontmatter, progressive disclosure, no auxiliary documentation inside the skill folder) without coordination, demonstrating that the structural requirements of Practice-facet content are not this project's invention but a genuinely load-bearing constraint that emerges wherever this kind of content is produced.

##### Unresolved questions
1. Whether additional reader relationships will emerge within this project's scope that don't fit any of the three current facets — if they do, the system extends by adding a new facet following the same pattern.
2. Whether a facet should carry any metadata of its own (a canonical name, a one-line definition, a reference to its governing specification) in a centralized registry, or whether the current loose convention (each facet is simply documented in its own specification file, cross-referenced from here) is sufficient.

### Facets currently defined
Three facets are defined as of this document's current revision. Each is specified in its own document, following the Explanation facet's own structure — meaning that the specifications of all three facets are themselves Explanation-facet documents.

#### Explanation
Content meant to be *studied* to understand something: specifications, analyses, design decisions, concept definitions, and any document whose primary purpose is for a reader to comprehend a subject rather than to execute a procedure.

**Governing specification:** [documentation-explanation.md](./documentation-explanation.md)

The Explanation facet's structure draws on conventions found across research papers, IETF standards documents, and architecture decision records, unified into a single shared structure that applies regardless of the document's subject — whether it is a protocol specification, a product requirement, or a concept definition. Provenance — citations, contributor attribution, cross-document propagation tracking, and revision history — lives in the paired Changelog-facet file, not in the base document itself. See the governing specification for the full structure, fields, and conventions.

#### Practice
Content meant to be *followed* to accomplish something: step-by-step procedures, agent instructions, and Skill files — any document whose primary purpose is for a reader (human or AI agent) to execute a sequence of actions and produce a result.

**Governing specification:** [documentation-practice.md](./documentation-practice.md)

The Practice facet's schema is not this project's invention — it is adopted from the independently-converged convention of three real AI ecosystems (Anthropic, OpenAI, Microsoft). See the governing specification for the full schema, progressive-disclosure model, and writing-style guidance.

#### Changelog
Content meant to be *consulted* to audit history: an append-only, chronologically-ordered record of changes to one paired artifact — what changed, why, on what evidence, who did what, and what else it should affect.

**Governing specification:** [documentation-changelog.md](./documentation-changelog.md)

The Changelog facet absorbs what used to live in base documents' front matter as `Citations`, `Contributors`, and `Applied to`, and what used to live in their body as `## Change Rationale`. A reader of a base artifact needs its current state, not its provenance; provenance belongs in history, and history belongs here. **Exception**: a Changelog-facet file does not itself get a companion changelog — a deliberate stop to the recursion, justified in [documentation-changelog.md → Discussion](./documentation-changelog.md#rationale-and-alternatives). (This exception applies to Changelog-facet files — the `.changelog.md` companions — not to the Changelog facet's own governing specification, which is an Explanation-facet document and does have a companion changelog: [documentation-changelog.changelog.md](./documentation-changelog.changelog.md).)

#### Discussion

##### Rationale and alternatives
- **Name the facets "Specification" and "Skill" instead of "Explanation" and "Practice" (rejected)**: "Specification" describes a specific *kind* of Explanation-facet document, not the facet itself. A concept definition, an analysis, or an architecture decision are all Explanation-facet documents but none of them is a "specification." Similarly, "Skill" describes the file format and folder convention of the Practice facet's most common instantiation, not the facet itself. The facet names should describe the *reader's relationship* to the content, not one specific format it might take.
- **Make the facet names language-agnostic (considered, not chosen)**: English facet names are already used throughout this project's technical content and tooling. Introducing a second set of names in another language without a concrete need would add a translation obligation with no clear benefit. If a future need arises for non-English facet names, the facet system is abstract enough to accommodate it.
- **Treat Changelog as a sub-convention of Explanation or Practice rather than its own facet (rejected)**: a changelog is neither studied to understand a subject nor followed to accomplish a task — it is consulted to audit history. Bundling it under either of the other two facets would force a structural mismatch (a changelog has no YAML front matter, no fixed body skeleton, no progressive disclosure) and would obscure the fact that the same `<base>.changelog.md` pattern is applied uniformly across artifacts of every facet, not only Explanation-facet ones.

### Which facet does a document belong to?
The decision is made by the document's author, guided by the document's *primary purpose*: if a reader is expected to study it to understand something, it is Explanation; if a reader is expected to follow it to accomplish something, it is Practice; if a reader is expected to consult it to audit how a paired artifact changed over time, it is Changelog. Most documents are unambiguous. When the boundary is unclear — for example, a document that contains both analytical content and a step-by-step procedure — the author should ask which purpose dominates: if the procedure is the document's reason for existing and the analysis exists only to support it, the document is Practice (with the analytical portion treated as context-setting within the procedure). If the analysis is the document's reason for existing and a brief procedure is included only as an illustrative example, the document is Explanation.

#### Discussion

##### Unresolved questions
Whether a single document should ever be allowed to carry both facets' structures simultaneously (for example, an Explanation-facet body with a Practice-facet appendix) is not settled. The current position — one facet per document, choose the dominant purpose — is simpler and avoids the ambiguity of mixed-facet documents, but may prove too rigid if a real need for mixed content arises.

### Extensibility
The facet system is designed to be extensible without structural upheaval. New facets may be added by writing a new governing specification document (itself an Explanation-facet document) and registering it here. The current three-facet model covers the reader relationships observed in this project so far: studying to understand, following to accomplish, and consulting to audit history. If a future document type demonstrates a need that fits none of these three — for example, a document that is primarily a worked example, or a decision log with no analytical argument — a fourth facet could be added following the same pattern, with no change to the facet concept itself or to the existing facet specifications.

#### Discussion

##### Rationale and alternatives
- **Define additional facets now, before a real need for them exists (rejected)**: would produce empty or near-empty specifications — exactly the mistake this project's own Methodology warns against (designing structure in the abstract instead of testing it against a real document). Defining a facet's structure before there is a real document of that kind to test it against risks producing a specification that looks complete but does not actually serve the use case it was designed for. The Changelog facet itself was added only after the same `<base>.changelog.md` pattern was already being applied across multiple artifacts, not predicted in advance.
- **Use a formal facet registry file instead of this prose section (considered, not chosen)**: a machine-readable registry (YAML or JSON) would make facet discovery automatable. At the current scale of three facets, the overhead of maintaining a separate registry file alongside the prose explanation is not justified. The prose here is authoritative; a registry can be extracted from it mechanically if tooling ever needs one.

##### Future possibilities
- If tooling is built that consumes facet metadata, a formal facet registry could be extracted from this section without changing the underlying model.
- If a fourth or fifth facet is ever added, the meta-layer's [Facets currently defined](#facets-currently-defined) section grows by one entry per facet, and each new facet's governing specification follows the same pattern: an Explanation-facet document that specifies the new facet's structure, cross-referenced from here. No change to the facet concept itself or to the existing facet specifications is required — the system is additive by design.

### Relationship between this document and its facet specifications
This document (`documentation.md`) is the entry point and meta-layer. It defines what facets are, names them, and explains extensibility. It does not itself specify the structure of any facet — that is each facet's own governing document's job. The four files form a hierarchy:

| Document | Role | Facet it follows |
| --- | --- | --- |
| `documentation.md` (this document) | Meta-layer: defines Facets, names current facets, explains extensibility | Explanation |
| `documentation-explanation.md` | Governs the Explanation facet: specifies structure, fields, body sections, and conventions | Explanation |
| `documentation-practice.md` | Governs the Practice facet: specifies Skill-file schema, progressive disclosure, writing style | Explanation |
| `documentation-changelog.md` | Governs the Changelog facet: specifies entry structure, CONTRIBUTORS.md, propagation tracking | Explanation |

All four are Explanation-facet documents — they are specifications to be studied, not procedures to be followed. The documents *produced with the help of* `documentation-practice.md` (such as a `write-a-document/SKILL.md`) are Practice-facet documents; the documents *produced with the help of* `documentation-changelog.md` (such as `documentation-explanation.changelog.md`) are Changelog-facet documents. The governing specifications and the documents they govern belong to different facets by design.

#### Discussion

##### Prior art
This pattern — a meta-specification that defines categories and points to per-category specifications — is common in modular standards. IETF RFCs, for example, are organized by category (Standards Track, Best Current Practice, Informational, Experimental) with separate documents defining what each category means, while the overall RFC process document defines what the categories are and how they relate. The same principle applies here at a smaller scale.

### Citations
A citation is a structured reference to another document or external source, recording the relationship between this document and the cited work. Citations are currently used in [Changelog-facet](./documentation-changelog.md) entries (in the `Cited` bullet field); they may also appear in other facets that need provenance tracking in the future. The rules below apply wherever a citation appears, regardless of which facet the citing document belongs to.

**Source-selection criteria.** A citation should only be added when the relationship is substantive, not decorative — not a passing or general-sounding mention. When judging whether an external source is worth citing, prefer:
- Peer-reviewed or standards-body sources (published research, IETF/W3C/ISO-style documents) over a vendor's own product documentation, where both are available.
- Structure as a quality signal: a source that shows its reasoning or evidence rather than only asserting a conclusion is more trustworthy than one that reads well but argues nothing — polished prose is not itself evidence of rigor.
- A clear distinction between two different kinds of claims from the same source: a claim about *observable, testable behavior* (e.g. "this software does X under condition Y") is generally reliable regardless of the source's other qualities; a claim about that same source's *own design philosophy or motives* is a self-assessment and should be treated with more skepticism, since the source is not a neutral party about itself.

**Relation vocabulary.** Each citation specifies a `Relation` describing how the cited work relates to the citing document:
- `Reference`: cites for context, no structural dependency.
- `Depends_on`: cannot be implemented or understood without the cited work.
- `Depends_for`: inverse of `Depends_on` — the cited work depends on this document.
- `Extends`: builds on top of the cited work.
- `Extends_by`: inverse of `Extends` — the cited work extends this document.
- `Conflicts`: a real, unresolved tension between this document and the cited work.
- `Superseded`: this document obsoletes the cited work. When a document is superseded, both sides update: the older document's `Status` becomes `Superseded` with a `Superseded_by` entry pointing forward; the newer document adds a `Superseded` entry pointing back.
- `Superseded_by`: the inverse — this document is obsoleted by the cited work.
- `Evidence`: the cited work is what supports a proposition made in this document. Distinct from `Reference` (cited for context only) and `Depends_on` (a structural dependency). Use `Evidence` when the source is the empirical or argumentative basis for a claim, but the claim does not structurally depend on the source existing.

#### Discussion

##### Unresolved questions
The boundary between `Reference` and `Depends_on` is not precisely defined. The current wording conflates two things that may not always agree — whether the cited work is needed to *understand* this document's text, and whether it's needed to *implement* this document correctly — under one definition ("cannot be implemented/understood without..."). A real case can satisfy one without the other: a document may be fully readable on its own while still being impossible to correctly implement without another document's mechanism already existing. A proposed starting criterion for the *understandability* axis — if this document's own definitions are unintelligible without reading the cited work, use `Depends_on`; if it's merely a pointer to further information and this document stands alone without it, use `Reference` — is a reasonable basis, but does not by itself resolve whether an *implementability* axis needs to be tracked separately. Deferred to a dedicated session rather than resolved here.

### URI
A URI is a string identifier as defined by RFC 3986. Two forms are used throughout this project's documentation:
- **Absolute URI**: carries a scheme, e.g. `mailto:omid@geniuses.group`, `https://claude.ai`. Used when the URI must resolve independently of this repository.
- **Relative reference**: a scheme-less reference resolved against a base URI (RFC 3986, Section 5), e.g. `./chat-logs/x.md`. Used for resources local to this repository. This is a first-class, standards-compliant form, not a workaround.

The `file:` scheme (RFC 8089) specifically requires an absolute path, which breaks portability across different clones of the same repository; a scheme-less relative reference is used for local paths instead of `file:` for that reason. This rule applies wherever a URI appears — internal hyperlinks, citation entries, contributor identity, examples, and any other reference to a local resource, in any facet.

## Results
Insufficient time has passed since this facet-based architecture was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Adding a meta-layer document means a reader who wants to understand the full documentation system must now consult four files instead of one. This is a deliberate trade-off: the four-file structure eliminates the structural compromise of the earlier single-file approach, at the cost of one additional file to read. The mitigating factor is that a reader who only needs to *write* a document of one facet (by far the most common case) only needs that facet's governing specification and the companion Skill file — the meta-layer is needed only when understanding the system as a whole.

### Rationale and alternatives
- **Keep a single `documentation.md` that governs all facets inline (rejected)**: this was the pre-facet approach, and it produced the concrete tension described in Methodology — the Practice facet's schema (adopted from three real ecosystems) fundamentally conflicts with the Explanation facet's rich front matter. A single document can describe all facets, but it cannot *govern* all of them with a single consistent set of rules.
- **Give each facet an entirely independent name, unconnected to any external framework (considered, not chosen)**: the facet names (Explanation, Practice, Changelog) are this project's own, chosen to describe the reader's relationship to the content directly. An entirely independent naming scheme was not needed because the names already state what they mean.

### Prior art
The earlier single-document approach (then `documentation.md`, now `documentation-explanation.md`) went through thirteen revisions, several of which directly addressed the tension between procedural and analytical content. The sixth revision introduced the `Optional Sections` catalog as a mechanism for accommodating different document purposes within one structure. The thirteenth revision moved procedural content into a separate Skill file, on the principle that procedural and analytical content are categorically different. The facet concept is the architectural crystallization of that thirteenth-revision instinct — not just moving the procedural content elsewhere, but explicitly naming *why* it belongs elsewhere. The Changelog facet was added after the same `<base>.changelog.md` pattern emerged across multiple artifacts and proved to be a real, repeated structural need rather than an ad-hoc convention.

### Unresolved questions
1. Should the meta-layer (`documentation.md`) eventually contain a machine-readable facet registry (for example, a YAML block listing each facet's name, governing specification, and one-line definition) in addition to the current prose description?
2. Whether the four-file structure itself should be reconsidered if the number of facets grows beyond four or five — at that point, the meta-layer's prose may become long enough that a tabular or registry-based approach is more maintainable.

### Future possibilities
If a fourth or fifth facet is ever added, the meta-layer's [Facets currently defined](#facets-currently-defined) section grows by one entry per facet, and each new facet's governing specification follows the same pattern: an Explanation-facet document that specifies the new facet's structure, cross-referenced from here. No change to the facet concept itself or to the existing facet specifications is required — the system is additive by design.
