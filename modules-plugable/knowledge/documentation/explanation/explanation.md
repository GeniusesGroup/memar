---
Title: "Documentation — Explanation"
Status: Proposed
Start Date: 2026-06-21
ID: 495000
---

# Documentation — Explanation
This document specifies the canonical documentation structure every formal explanation document must follow.

## Abstract
This specification defines the structure every formal document in any projects must follow: a YAML front-matter block for identity and classification, followed by a body organized as `Abstract`, `Introduction`, and `Explanation`. Provenance — citations, contributor attribution, cross-document propagation tracking, and revision history — does not live in this document's front matter or body; it lives in the changelog contents of the tasks that changed the document ([Changelog](../changelog/changelog.md)), since a reader of the base artifact needs its current state, not its provenance. The same reader-relationship governs more than field-level provenance: any body content that serves the audit reader rather than the current-state reader is excluded by the same criterion — see [Relevance discipline](#relevance-discipline).

See [Documentation](../documentation.md) for what a template is and how this specification fits into the wider documentation system.

## Introduction
*This section's subsections (`Motivation`, `Methodology`) are a suggested partitioning, not the only one — an author may add another subsection here with a stated reason the existing ones don't cover what's needed. The `Introduction` heading itself carries no direct content.*

### Motivation
The real motivation for this specification is not specific to any one project or document purpose — it is to give every document projects a single, predictable structure, so a reader or an AI assistant who has read one document already knows where to find anything in another, regardless of which project or document type it belongs to.

### Methodology
This specification's structure was not designed in the abstract in a single pass. It was arrived at through: research into precedent from other documentation and standards processes (including IETF); sustained critical review across multiple working chats, with each proposed change argued for and against rather than accepted on first suggestion; direct testing of proposed structural changes against a real document already written under an earlier version of this specification ([protocol.md](https://github.com/GeniusesGroup/memar/blob/2cb39b5eeb3a0eddd5bc1bfe132193068dea768b/RFCs/protocol.md)), which is what surfaced a concrete scattering problem later fixed by the topic-first structure below, rather than that problem being reasoned out abstractly beforehand; and a review of documentation conventions across disciplines (research papers, standards documents, architecture records), which found the same recurring building blocks — identity, a compact claim, motivating context, detailed content, open questions, rationale — differing mainly in emphasis rather than fundamental shape.

## Explanation
*Reading every topic below in full is not required — read only what's relevant to your question. Procedural, "do this, then this" content for producing a document under this specification lives in the rules of this module; this specification describes structure, not procedure.*

### Reader relationship
Content meant to be *studied* to understand something: specifications, analyses, design decisions, concept definitions, and any document whose primary purpose is for a reader to comprehend a subject rather than to execute a procedure. The structure below serves that reader, and it is one structure whatever the subject is — a protocol specification, a product requirement, or a concept definition — as [Optional Sections](#optional-sections) sets out. A document whose reader relationship is another's belongs to that facet, which states it in its own specification ([Practice](../practice/practice.md#reader-relationship) is the one most often mistaken for this); what serves a reader who audits history rather than one who reads the current state is settled in this specification's [Abstract](#abstract).

### Title
A short, unique, human-readable name for the document, in double quotes. A title change that alters the concept is a new document with a new `ID`; a title change that merely rephrases the same concept is a minor revision of the same document.

### Status
An Explanation-facet document carries its Status in the front-matter `Status` field. The values it may take, their meanings, and whether each is safe to depend on are the type `Status` ([documentation.md → Status](../documentation.md#status)), asked with `Status.for_kind`. A `Superseded` document names its successor through [`Superseded by`](../documentation.md#citations).

Rules specific to this facet:
- `ID` is never reused, regardless of status, including Rejected.
- Move `Status` to `Proposed` once discussion converges.
- Move to `Final` once it's reflected in canonical documentation.
- Whether discussion has converged, and whether a document is reflected in canonical documentation, are decided by a reader against the governing documents, not by a command: `memar content check` does not read `Status`. A reader who disagrees records the disagreement rather than moving the field.
- Nothing before `Final` should be treated as settled by anyone depending on the document.
- Moving a Final document's substance requires a new, superseding document, not an in-place edit.
- A reconsidered Rejected idea becomes a new document with its own number, referencing the rejected one via a `Superseded` entry in the `Cited` field of the changelog content that records it (see [changelog.md → Cited](../changelog/changelog.md#cited)).
- `Status` reflects canonical-documentation status only, never informal or practical usage. A document can be in active, wide practical use while still `Proposed`; that does not change its `Status`. (This document is itself an example: in active use as the working specification while `Proposed`.)

### Start Date
The calendar date (`YYYY-MM-DD`, UTC) the document file was first drafted. Set once, never changed. Should agree with the date implied by `ID`, since both are meant to be captured at the same moment.

### ID
A UTC unix-time-derived integer, generated once when the file is first drafted, never reused or reassigned. It carries no meaning beyond relative creation order — generating it does not imply approval; that is `Status`'s job.

**Value and generation.** The value is UTC unix time truncated to the hour, as a plain decimal integer; `memar content hour-id` prints it ([`content_hour_id.py`](../services/content_hour_id.py)), and nothing else defines it.

**Uniqueness and collisions.** Two or more documents drafted in the same working chat landing in the same hour is expected and normal. Resolve manually today: keep the first document's number, give the next one the following hour's value or any other free value. Manual resolution is a stopgap, not the preferred end state (an `anticipated-work` content of the task that records it).

**Retroactive numbering.** Pre-existing documents may be assigned an hour-value derived from their recorded `Start Date` if retroactively renumbered. Where several share a `Start Date`, order by reasonable manual judgment — no strict rule imposed.

**Merging before Final.** Two or more `Draft`/`Proposed` documents merged into one, without changing overall content, reuse one existing number; no new number is generated, and no `Citations` entries are added pointing to the abandoned ones (they never reached Final). Which number is kept:
- If the merged document keeps one original title unchanged, it uses that document's original number.
- If an entirely new title is chosen, the merged document uses the smallest (earliest) of the numbers being merged.

This rule applies only pre-Final; once Final, merging requires a new, superseding document per the Status rules.

**Storage representation.** Out of scope here — an implementation detail.

**Lookup.** Full-text search for `ID:`.

### Body sections
The body follows the front-matter, as a fixed set of top-level (`##`) sections in the order the types of [`./primitive/`](./primitive/) carrying the label `body-section` give. No document may introduce a new top-level section beside these without a change to this specification itself. Everything else a document needs is an optional building block from [Optional Sections](#optional-sections) - placed by the author wherever fits, at whatever heading depth the location calls for. The fixed three are the skeleton; the catalog is the flesh.

Each fixed section is declared, with what it is for, where it goes and how it differs from its neighbours, by the types of [`./primitive/`](./primitive/) carrying the label `body-section`; `Explanation` follows the naming and cross-referencing rules of [Conventions](#conventions) and the body-versus-contents split of [Relevance discipline](#relevance-discipline).

### Conventions
This specification's own mandatory naming and cross-referencing rules — every document following it follows these, not just an option to consider.

#### Field Naming Convention
A front-matter field is written as the key type of its facet declares it ([`explanation_key.py`](./primitive/explanation_key.py) for this facet's); no case rule is imposed on all keys, since `_`, `-` and a space each have uses (`Start Date`, `Depends_on`, and a practice's lowercase `name` and `description`, which an agent app reads).

#### Internal Cross-References
Any reference within a document to another section of the same file must be a real hyperlink (e.g. `[Conventions](#conventions)`), never plain text (e.g. `see Conventions` or a malformed pseudo-link like `see ###Conventions`). A broken anchor is easy to spot; a stale plain-text reference is not.

#### Relevance discipline
A body statement earns its place by serving the reader of the document's **current state**: reading it must change that reader's understanding of the design as it stands — its claims, definitions, arguments, or open questions. Content whose value is to a reader auditing *how* that state came to be does not belong in the body, however true or interesting it is: where and with whom positions were formed, in what order decisions arrived, the narrative of the debate that shaped them, anecdotes, and participant detail are decision-shaping context and belong to the changelog contents of the tasks that changed the document ([Changelog](../changelog/changelog.md)). The test is not usefulness — decision-shaping context is usually useful — but which reader it serves.

This applies inside sections that legitimately exist: a `Motivation` states the failure mode that motivates the document (current-state relevant), and a `Methodology` states the method and its verification discipline (current-state relevant); neither carries the social history of the positions they describe. The rule generalizes the provenance statement in this specification's [Abstract](#abstract) from a field list to a criterion: whatever a changelog reader needs and a current-state reader does not, is changelog content.

**Recurring misroute — filling Abstract, Motivation, or Methodology with audit material.** Agents repeatedly put into these three openings what belongs only in the changelog: session dates, who argued or reviewed, which drafting pass relocated what, "see the paired changelog for the alternatives rejected," and other sentences that teach nothing about the *subject* and everything about the *document's production*. The test for each opening is the same Relevance criterion, applied narrowly:

- **Abstract** — does this sentence state the document's claim? If it narrates how the claim was reached, drop it or move it to the changelog.
- **Motivation** — does this sentence name the failure mode that makes the document necessary? If it narrates who noticed the failure, when, or how the writing session unfolded, drop it or move it.
- **Methodology** — does this sentence state a method the reader must hold to understand or verify the content (what layer is consumed, what is excluded and why as a standing rule, what verification discipline the claims rest on)? If it only records that a review happened, who participated, or which prior draft looked different, it fails — that material never helps a later reader understand the subject better; it only helps an auditor reconstruct the writing. Omit Methodology entirely when nothing methodologically distinctive remains after that filter.

The changelog contents are the correct home for production history; pointing at them from Motivation or Methodology does not license restating that history in the body.

The full routing of former discussion-section content follows from this criterion:

- **Evidence** - the premise facts a design's argument depends on (an external system's behavior, a measured result, a literature position) stay in the body, cited inline at the claim they support; an unsupported premise weakens the claim. Comparative surveys - how other projects organize the same problem and how this project differed - are not premise evidence; they are audit content, kept as a `research` content ([Research](../research/research.md)).
- **Considered and not done** - alternatives examined and rejected, with their reasons, are decision-shaping context: they serve the audit reader, and an AI-assisted reader cannot reliably tell a negated position from an affirmed one when loading a document into context. They live in the `Options` field of the `decision` content that made the decision ([Handoff](../handoff/handoff.md#the-kinds)).
- **Open questions** - working state, not current design; they may be answered, may be moot. They live as `question` contents of a task ([Handoff](../handoff/handoff.md#the-kinds)). One boundary keeps this from over-applying: where a *specific claim* is genuinely tentative, the claim itself says so in its own statement - that is content; the question and its resolution work live in its `question` content. `Status` carries document-level maturity; the body does not restate it question by question.
- **Anticipated work** - extensions and growth paths the design anticipates are not current design either; they live as `anticipated-work` contents.
- **Observed results** - what real use of the document's decision actually produced is not body content; a result's home is determined by its type, per the cross-cutting routing map in [documentation.md → Results routing](../documentation.md#results-routing).

#### URI
URI format (absolute vs. relative reference, the `file:` scheme prohibition) is defined in [documentation.md → URI](../documentation.md#uri) as a cross-cutting convention, applying wherever a URI appears in any document of any facet.

### Optional Sections
A non-exhaustive catalog of building blocks a document's author may use — nowhere is any of these mandatory, and this list may grow. Where exactly one goes, and at what heading depth, is the author's choice; the only hard rule is the one already stated under [Body sections](#body-sections) — no new top-level (`##`) section beside the fixed three. In practice, these are typically nested under `Introduction` or `Explanation`, wherever fits that document's actual content.

This catalog — rather than a separate template per document purpose ([`RFC - Request for Comments`](https://en.wikipedia.org/wiki/Request_for_Comments), [`ADR - Architecture decision record`](https://en.wikipedia.org/wiki/Architectural_decision), `SRD - Specify technical requirements for development`, `PRD - Product Requirement Document`, `MRD - Marketing requirement document`, `BRD - Business requirement document`, and similar labels) — is how this specification accommodates different kinds of documents. `RFC` is not a document type of its own; it is a review phase applied to a document. `PRD` is not a document type of its own; it is a product-oriented documentation guide. The structure itself does not change between them. Every scientific discipline — computer science, physics, biology, mathematics — writes papers with the same skeleton (Title, Abstract, Introduction, Method, Results, Discussion, References); no field skips the Abstract, and the differences between fields show up in emphasis and content, never in whether that skeleton applies. This specification treats every documented concept the same way: `Customer`, `Repository`, `Task`, and `Protocol` all enter documentation as equal, undifferentiated subjects — nothing about the structure should presume one kind of subject is inherently more important, or inherently different in kind, than another; what a given document actually needs to say about its subject is what determines which of the items below get used, not the subject's category. A separate independent template per document purpose tends to produce definitional drift over time instead — the same concept, such as "Abstract" or "Motivation," ends up defined slightly differently in each one. Authors pick whichever items below fit the document they're writing; unused items are simply omitted, not left as empty headers.

Each building block is declared, with what it is for, where it goes and how it differs from the others, one type each in [`./primitive/`](./primitive/), carrying the label `optional-section`.

### Making a document
The steps that produce a document under this specification, in order. What each field and section means is stated above; the section types are the types of [`./primitive/`](./primitive/).
1. Start from the skeleton: the front matter fields `Title`, `Status`, `Start Date` and `ID`, then one top heading and the fixed body sections.
   ```
   ---
   Title: ""
   Status: Draft
   Start Date: ""
   ID: ""
   ---

   # Document Title

   ## Abstract

   ## Introduction

   ### Motivation

   ### Methodology

   ## Explanation

   ### {Topic}

   #### {Sub topic}
   ```
2. Set `ID` once to the current UTC hour-count that `memar content hour-id` prints, and never change it.
3. Fill the rest of the front matter: a short, unique `Title` in quotes, `Status` starting at `Draft`, and `Start Date` as today's UTC date, matching the moment `ID` was generated.
4. Write the body. `Abstract` and `Introduction` stay unified, document-wide prose; `Explanation` is split into topics, with a sub topic where finer structure helps. Premise evidence for a claim is cited inline at the claim. Document-wide optional sections sit directly under the body's top level, not inside a topic.
5. Filter the Abstract, the Motivation and the Methodology before leaving them ([Framing Sections State the Subject, Not the Writing](./rules/framing-sections-state-the-subject-not-the-writing/framing-sections-state-the-subject-not-the-writing.md)), and keep alternatives, open questions and anticipated work out of the body ([The Body Holds No Alternatives, Questions or Plans](./rules/the-body-holds-no-alternatives-questions-or-plans/the-body-holds-no-alternatives-questions-or-plans.md)).
6. Hold the draft to the [standards of cognitive material](../../../../docs/cognition.md#standards-of-cognitive-material) while writing, clarity first, and examine each claim as it is drafted and not in a later phase.
7. Place a `changelog` content on the task that made the document ([Changelog](../changelog/changelog.md)); the document keeps no provenance of its own. For a revision of a document written under an earlier version, bring it in line at this edit ([Progressive migration](#progressive-migration)) and carry any `Citations`, `Contributors` or `Applied to` fields and any `Change Rationale` body content of the old version into changelog contents.

### Progressive migration
A document written under an earlier version of this specification is not required to be updated immediately when this specification changes. Instead, it is brought in line with the current structure the next time that file is naturally edited for any reason - not as a dedicated, separate migration pass. This applies to structural changes (section names, nesting) as much as to front-matter field changes.
