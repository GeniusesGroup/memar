---
Title: "Documentation"
Status: Proposed
Start Date: 2026-07-25
ID: 495820
---

# Documentation
This document defines what a Facet is, names the five facets currently in use, explains how the facet system extends, and carries the cross-cutting conventions that span facets (file naming, documentation language, results routing, citations, URI). It does not itself specify the structure of any facet — that is each facet's own document's job.

## Abstract
Documentation in this project is organized into **Facets** — distinct kinds of documentation content, each with its own governing structure and its own specification document. A facet is defined by the reader's relationship to the content: what the reader is expected to do with it. This project currently defines five facets — **Explanation** (content meant to be studied to understand something), **Practice** (content meant to be followed to accomplish something), **Changelog** (content meant to be consulted to audit how an artifact changed over time), **Handoff** (content meant to be read to resume a paused discussion across a session boundary), and **Research** (content meant to be examined to evaluate a deliberate inquiry). See [Facets currently defined](#facets-currently-defined) for the definitions and [Extensibility](#extensibility) for how new facets may be added. Cross-cutting conventions that apply regardless of facet — how a document's name encodes its category, concept, and facet; the language the written record is kept in; where a result of each type is recorded; citation practice; URI form — are defined here as well.

## Introduction

### Motivation
A single documentation structure cannot serve two categorically different reader needs without compromising both. Content meant to be *studied* (specifications, analyses, definitions) demands rich front matter, structured argumentation, citation trails, and contributor attribution. Content meant to be *followed* step by step (procedures, agent instructions, Skill files) demands brevity, imperativeness, and minimal context overhead — every field that is not the procedure itself is pure cost to the agent reading it mid-task. Forcing both kinds of content into one shared schema means either overburdening the procedural content with apparatus it does not need, or under-equipping the analytical content with structure it does. The Facet concept resolves this by acknowledging, upfront, that "documentation" is not one thing — it is a family of related but structurally distinct kinds of content, each deserving its own specification.

A third need surfaced once the first two facets were in active use: recording why an artifact changed over time. A reader consulting such a record is neither studying the artifact's current design (Explanation) nor following a procedure against it (Practice) — they are auditing history. Rather than leaving this as ad-hoc per-document convention, the Changelog facet was added to give it the same named, extensible treatment as the other two.

### Methodology
The decision to adopt a facet-based architecture was not made in the abstract. It arose from observing a real problem: the earlier version of this specification (then a single `documentation.md`) attempted to govern both analytical specifications *and* procedural Skill files with the same schema. That produced a concrete tension — the same document's thirteenth revision explicitly moved procedural walkthrough content into a separate Skill file, on the principle that procedural and analytical content are categorically different. The facet concept crystallized that instinct into a named, extensible architectural decision. The Practice facet's schema was not invented — it was adopted from the independently-converged convention of three real AI ecosystems (Anthropic's, OpenAI's, and Microsoft's own skill-creator Skill files), each designed without coordination with the others, providing stronger evidence than a from-scratch design would have. The Changelog facet was added later, after the same `<base>.changelog.md` pattern was being applied across multiple artifacts and naming it as a Facet proved a smaller conceptual cost than leaving it as implicit convention. The Handoff facet followed the same path a second time: the state-capture pattern (`<base>.handoff.md`) repeated informally across the project's working sessions and practice drafts before being named, and registering it as the fourth facet formalized a practiced convention rather than predicting a need.

## Explanation

### Content Rule: No Fabricated or Redundant Provenance
Documentation content must be current truth, not archaeology. Three rules apply to every Explanation- and Practice-facet document:

- **No fabricated information.** Never invent facts, history, usage evidence, or attribution — including plausible-looking reconstruction of things nobody recorded. If something is unknown, it is stated as unknown or omitted, never glossed over with a confident-sounding filler. This project is under active development; presenting a guess as an established fact poisons every downstream decision built on it.
- **Historical notes live in exactly one place.** How a document, a convention, or the documentation method itself came to be — including what an older approach looked like and when it was replaced — belongs in the paired changelog, once. Base documents state current rules and their reasons, without narrating what used to be written where, which revision introduced which sentence, or how a migration was executed. A reader needing that history consults the one home it has; a reader who does not is never taxed by it.
- **No redundant restatement.** When content exists in its authoritative home, other documents link to it instead of repeating it — repetition is where documents go to drift apart.


### Facet
A **Facet** is a named category of documentation content, defined by the reader's relationship to it: what the reader is expected to *do* with the content. Each facet has its own governing specification — a separate document that defines what structure, fields, and conventions documents of that facet must follow. The facet itself is the meta-layer: it names the category, states what makes it distinct, and points to its specification.

The core observation is that documentation content is not homogeneous: a reader studying a specification to understand a design, a reader following a procedure to accomplish a task, a reader consulting a history to audit changes, a reader reading a record to resume a paused discussion, and a reader examining an inquiry to evaluate it are doing five categorically different things, and the structure that serves each best is not the same. Forcing all five into one shared schema means either overburdening the simpler kinds with apparatus they don't need, or under-equipping the richer kinds with structure they do. The Facet concept resolves this by naming each kind upfront and giving it its own governing specification.


### Facets currently defined
Five facets are defined as of this document's current revision. Each is specified in its own document, following the Explanation facet's own structure — meaning that the specifications of all five facets are themselves Explanation-facet documents.

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

The Changelog facet absorbs what used to live in base documents' front matter as `Citations`, `Contributors`, and `Applied to`, and what used to live in their body as `## Change Rationale`. A reader of a base artifact needs its current state, not its provenance; provenance belongs in history, and history belongs here. **Exception**: a Changelog-facet file does not itself get a companion changelog — a deliberate stop to the recursion, justified in [documentation-changelog.md → Abstract](./documentation-changelog.md#abstract). (This exception applies to Changelog-facet files — the `.changelog.md` companions — not to the Changelog facet's own governing specification, which is an Explanation-facet document and does have a companion changelog: [documentation-changelog.changelog.md](./documentation-changelog.changelog.md).)

#### Handoff
Content meant to be *read to resume a paused discussion*: a companion record (`<base>.handoff.md`) carrying a discussion's current state across a session boundary — decisions with their confidence, resolved ambiguities, open questions, assumptions, and proposed next steps — so the next session (an AI system, a returning human, a colleague joining mid-stream) can continue from recovered state instead of re-derivation.

**Governing specification:** [documentation-handoff.md](./documentation-handoff.md)

The Handoff facet is defined by the same companion-file convention as the Changelog facet, but its reader relationship differs from all three older facets: a changelog is consulted to audit the past, while a handoff is read to continue unfinished work. Its central discipline — the record is an *analysis* of the discussion, not a transcript, with the risks of distillation named and structurally controlled — and its agent-general scope (a fully human session is covered by the same artifact) are defined in the governing specification. Unlike a changelog, a handoff is mutable working state, revised as the discussion moves and retired when nothing open remains.

#### Research
Content meant to be *examined to evaluate a deliberate inquiry*: a numbered companion record (`<base>.research.<NNN>.md`) carrying one bounded inquiry into a stated question — the question and goals with their explicit standing, the participants and their roles, the methodology, the findings, and the conclusion — including negative and inconclusive outcomes.

**Governing specification:** [documentation-research.md](./documentation-research.md)

The Research facet follows the same companion-file convention as the Changelog and Handoff facets — with a per-base numeric ordinal, since a base artifact may carry several researches — but its reader relationship differs from all four older facets: a changelog is consulted to audit what changed, a handoff to resume unfinished work, while a research is examined to evaluate how a question was pursued and how firm its outcome stands. It records inquiries that may or may not produce a change — a negative result ("investigated; no change warranted") has no other home in this system. Its lifecycle — mutable while Active, frozen once Complete or Withdrawn, corrected by supersession — is defined in the governing specification.

### Which facet does a document belong to?
The decision is made by the document's author, guided by the document's *primary purpose*: if a reader is expected to study it to understand something, it is Explanation; if a reader is expected to follow it to accomplish something, it is Practice; if a reader is expected to consult it to audit how a paired artifact changed over time, it is Changelog; if a reader is expected to read it to resume a paused discussion across a session boundary, it is Handoff; if a reader is expected to examine it to evaluate a deliberate inquiry into a stated question, it is Research. Most documents are unambiguous. When the boundary is unclear — for example, a document that contains both analytical content and a step-by-step procedure — the author should ask which purpose dominates: if the procedure is the document's reason for existing and the analysis exists only to support it, the document is Practice (with the analytical portion treated as context-setting within the procedure). If the analysis is the document's reason for existing and a brief procedure is included only as an illustrative example, the document is Explanation.


### Extensibility
The facet system is designed to be extensible without structural upheaval. New facets may be added by writing a new governing specification document (itself an Explanation-facet document) and registering it here. The current five-facet model covers the reader relationships observed in this project so far: studying to understand, following to accomplish, consulting to audit history, reading to resume a paused discussion, and examining to evaluate a deliberate inquiry. If a future document type demonstrates a need that fits none of these five, a sixth facet could be added following the same pattern, with no change to the facet concept itself or to the existing facet specifications.


### Relationship between this document and its facet specifications
This document (`documentation.md`) is the entry point and meta-layer. It defines what facets are, names them, and explains extensibility. It does not itself specify the structure of any facet — that is each facet's own governing document's job. The six files form a hierarchy:

| Document | Role | Facet it follows |
| --- | --- | --- |
| `documentation.md` (this document) | Meta-layer: defines Facets, names current facets, explains extensibility | Explanation |
| `documentation-explanation.md` | Governs the Explanation facet: specifies structure, fields, body sections, and conventions | Explanation |
| `documentation-practice.md` | Governs the Practice facet: specifies Skill-file schema, progressive disclosure, writing style | Explanation |
| `documentation-changelog.md` | Governs the Changelog facet: specifies entry structure, CONTRIBUTORS.md, propagation tracking | Explanation |
| `documentation-handoff.md` | Governs the Handoff facet: specifies the `<base>.handoff.md` state-capture artifact, the analysis-not-transcription discipline, and its relationship to the other facets | Explanation |
| `documentation-research.md` | Governs the Research facet: specifies the `<base>.research.<NNN>.md` inquiry-record artifact, its mandatory core, lifecycle, and relationship to the other facets | Explanation |

All six are Explanation-facet documents — they are specifications to be studied, not procedures to be followed. The documents *produced with the help of* `documentation-practice.md` (such as a `write-a-document/SKILL.md`) are Practice-facet documents; the documents *produced with the help of* `documentation-changelog.md` (such as `documentation-explanation.changelog.md`) are Changelog-facet documents; the documents *produced with the help of* `documentation-handoff.md` (such as a `<base>.handoff.md` companion) are Handoff-facet documents; the documents *produced with the help of* `documentation-research.md` (such as a `<base>.research.<NNN>.md` companion) are Research-facet documents. The governing specifications and the documents they govern belong to different facets by design.

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


### URI
A URI is a string identifier as defined by [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986). Two forms are used throughout this project's documentation:
- **Absolute URI**: carries a scheme, e.g. `mailto:omid@geniuses.group`, `https://claude.ai`. Used when the URI must resolve independently of this repository.
- **Relative reference**: a scheme-less reference resolved against a base URI ([RFC 3986, Section 5](https://datatracker.ietf.org/doc/html/rfc3986#section-5)), e.g. `./chat-logs/x.md`. Used for resources local to this repository. This is a first-class, standards-compliant form, not a workaround.

The `file:` scheme ([RFC 8089](https://datatracker.ietf.org/doc/html/rfc8089)) specifically requires an absolute path, which breaks portability across different clones of the same repository; a scheme-less relative reference is used for local paths instead of `file:` for that reason. This rule applies wherever a URI appears — internal hyperlinks, citation entries, contributor identity, examples, and any other reference to a local resource, in any facet.

### File Naming
A file name carries structure, not only an identifier: it states which category a document belongs to, which concept it addresses, and — for a companion record — which facet it follows. Three separators divide that labor, and each carries exactly one kind of boundary; a name is legible when no separator is asked to carry two.

- **Folder, or hyphen (`-`)** — the structural boundary between category and topic. The folder carries it where a category has enough documents to own a directory (`protocols/media-type.md`, `khayyam/variable.md`); the hyphen carries it where documents sit beside one another in one directory (`abstraction-implements.md`, `networking-osi_1-Asb.md`). The left side names the namespace, the right side the subject.
- **Underscore (`_`)** — joins the words of a single conceptual term so the term reads as one unit rather than as separate parts (`immutable_infrastructure.md`, `osi_1`).
- **Dot (`.`)** — separates a companion record's facet key from its base name (`<base>.changelog.md`, `<base>.handoff.md`, `<base>.practice.md`, `<base>.research.<NNN>.md`), which is how the companion pairing is stated instead of inferred.

The distinction is load-bearing: `type-explicit_behavior_ownership.md` says *category* `type`, *term* `Explicit Behavior Ownership`, while a name whose parts all wear the same separator states no boundary at all and leaves the reader to guess where the category stops and the topic starts.

A name is chosen by the criteria that govern the term it encodes — it communicates meaning, preserves conceptual boundaries, avoids implementation-specific vocabulary, and stays stable over time, since a rename changes how the concept is addressed rather than how it is written. The human-readable form of a document's name is its front-matter `Title`, which is the slug's source; see [documentation-explanation.md → Title](./documentation-explanation.md#title).

### Documentation Language
The project's written record is kept in English. The reason is the record's audience rather than a preference about which language reads better: documentation is read by agents of every kind — human, IDE, CLI, AI — across sessions, shifts, and projects, and one language is what lets all of them read the same text instead of a version of it. A proposal to change documentation states its replacement text in English, ready to substitute, so accepting a proposal never requires a translation pass. Conversation is outside this rule: it follows whoever is speaking, and the language a discussion happened in is no reason to write the record in it.

### Results routing
Documentation work constantly produces results, and the type of the result — not the writer's preference — determines where it is recorded. This routing is cross-cutting: its homes span several facets, while each home's structure is defined by that facet's own governing specification, not repeated here.

- **Anticipated results** — what a decision is expected to achieve, stated while writing: the document's own claim, in its [Abstract](./documentation-explanation.md#abstract).
- **Derived results** — consequences that adopting the decision forces, whether or not anyone wants them: the [Implications](./documentation-explanation.md#implications) entry of the Explanation facet's Optional Sections.
- **Observed results** — what real use actually produced: an observation that changed the design belongs to the [Changelog](./documentation-changelog.md) entry that made the change; one that supports a specific claim is cited inline at that claim, as Evidence ([Relevance discipline](./documentation-explanation.md#relevance-discipline)); one that warrants deliberate study is a [Research](./documentation-research.md) record; one awaiting action is working state in the paired [handoff](./documentation-handoff.md).

An Explanation-facet document carries no `Results` section; the boundary is defined in [documentation-explanation.md → Body sections](./documentation-explanation.md#body-sections).

