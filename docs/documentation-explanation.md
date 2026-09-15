---
Title: "Documentation — Explanation"
Status: Proposed
Start Date: 2026-06-21
ID: 495000
---

# Documentation — Explanation
This document specifies the canonical documentation structure every formal explanation document must follow.

## Abstract
This specification defines the structure every formal document in any projects must follow: a YAML front-matter block for identity and classification, followed by a body organized as `Abstract`, `Introduction`, and `Explanation`. Provenance — citations, contributor attribution, cross-document propagation tracking, and revision history — does not live in this document's front matter or body; it lives in the paired [Changelog](./documentation-changelog.md), since a reader of the base artifact needs its current state, not its provenance. The same reader-relationship governs more than field-level provenance: any body content that serves the audit reader rather than the current-state reader is excluded by the same criterion — see [Relevance discipline](#relevance-discipline).

See [Documentation](./documentation.md) for what a Facet is and how this specification fits into the wider documentation system.

## Introduction
*This section's subsections (`Motivation`, `Methodology`) are a suggested partitioning, not the only one — an author may add another subsection here with a stated reason the existing ones don't cover what's needed. The `Introduction` heading itself carries no direct content.*

### Motivation
The real motivation for this specification is not specific to any one project or document purpose — it is to give every document projects a single, predictable structure, so a reader or an AI assistant who has read one document already knows where to find anything in another, regardless of which project or document type it belongs to.

### Methodology
This specification's structure was not designed in the abstract in a single pass. It was arrived at through: research into precedent from other documentation and standards processes (including IETF); sustained critical review across multiple working sessions, with each proposed change argued for and against rather than accepted on first suggestion; direct testing of proposed structural changes against a real document already written under an earlier version of this specification ([protocol.md](https://github.com/GeniusesGroup/memar/blob/2cb39b5eeb3a0eddd5bc1bfe132193068dea768b/RFCs/protocol.md)), which is what surfaced a concrete scattering problem later fixed by the topic-first structure below, rather than that problem being reasoned out abstractly beforehand; and a review of documentation conventions across disciplines (research papers, standards documents, architecture records), which found the same recurring building blocks — identity, a compact claim, motivating context, detailed content, open questions, rationale — differing mainly in emphasis rather than fundamental shape.

## Explanation
*Reading every topic below in full is not required — read only what's relevant to your question. Procedural, "do this, then this" content for producing a document under this specification lives in the paired Practice-facet file `documentation-explanation.practice.md` (named per the rule in [documentation.md](./documentation.md)); this specification describes structure, not procedure.*

### File
What a filename encodes — which separator marks the category, which the conceptual term, which the facet companion — is defined in [documentation.md → File Naming](./documentation.md#file-naming) as a cross-cutting convention applying to every facet. Two rules concern this specification's front matter specifically:
- The slug derives from the document's [`Title`](#title), and a filename never contains its [ID](#id).
- The name is stable once the document's `Status` is `Final`.

### Title
A short, unique, human-readable name for the document, in double quotes. It is the source of the filename slug. A title change that alters the concept is a new document with a new `ID`; a title change that merely rephrases the same concept is a minor revision of the same document.

### Status

| Status | Meaning | Safe to depend on? |
| --- | --- | --- |
| **Draft** | Direction is not yet settled; real, unresolved questions remain, recorded in the document's paired handoff. | No |
| **Proposed** | Design discussion reached consensus; ready for final review before being reflected in canonical documentation. | Not yet — may still be revised during final review |
| **Final** | Reflected in canonical documentation. | Yes |
| **Superseded** | Replaced by a newer document. See [`Superseded by`](./documentation.md#citations). | No — depend on the superseding document instead |
| **Rejected** | Considered and explicitly not adopted. Kept for the historical record. | No |

Additional rules:
- `ID` is never reused, regardless of status, including Rejected.
- Move `Status` to `Proposed` once discussion converges.
- Move to `Final` once it's reflected in canonical documentation.
- Nothing before `Final` should be treated as settled by anyone depending on the document.
- Moving a Final document's substance requires a new, superseding document, not an in-place edit.
- A reconsidered Rejected idea becomes a new document with its own number, referencing the rejected one via a `Superseded` entry in the paired Changelog's `Cited` field (see [documentation-changelog.md → Cited](./documentation-changelog.md#cited)).
- `Status` reflects canonical-documentation status only, never informal or practical usage. A document can be in active, wide practical use while still `Proposed`; that does not change its `Status`. (This document is itself an example: in active use as the working specification while `Proposed`.)


### Start Date
The calendar date (`YYYY-MM-DD`, UTC) the document file was first drafted. Set once, never changed. Should agree with the date implied by `ID`, since both are meant to be captured at the same moment.

### ID
A UTC unix-time-derived integer, generated once when the file is first drafted, never reused or reassigned. It carries no meaning beyond relative creation order — generating it does not imply approval; that is `Status`'s job.

**Value.** UTC unix time truncated to the hour — `(unix seconds) / 3600` — as a plain decimal integer (e.g. `495317`).

**Generation.** See [How to make a new document](./documentation-explanation.practice.md) for the per-platform commands.

**Uniqueness and collisions.** Two or more documents drafted in the same working session landing in the same hour is expected and normal. Resolve manually today: keep the first document's number, give the next one the following hour's value or any other free value. Manual resolution is a stopgap, not the preferred end state (see the paired handoff's anticipated work).

**Retroactive numbering.** Pre-existing documents may be assigned an hour-value derived from their recorded `Start Date` if retroactively renumbered. Where several share a `Start Date`, order by reasonable manual judgment — no strict rule imposed.

**Merging before Final.** Two or more `Draft`/`Proposed` documents merged into one, without changing overall content, reuse one existing number; no new number is generated, and no `Citations` entries are added pointing to the abandoned ones (they never reached Final). Which number is kept:
- If the merged document keeps one original title unchanged, it uses that document's original number.
- If an entirely new title is chosen, the merged document uses the smallest (earliest) of the numbers being merged.

This rule applies only pre-Final; once Final, merging requires a new, superseding document per the Status rules.

**Storage representation.** Out of scope here — an implementation detail.

**Lookup.** Full-text search for `ID:`, or the README index (Number, Title, Status).


### Body sections
The body follows the front-matter, as a fixed set of top-level (`##`) sections in order: `Abstract`, `Introduction`, `Explanation`. No document may introduce a new top-level section beside these without a change to this specification itself. Everything else a document needs is an optional building block from [Optional Sections](#optional-sections) - placed by the author wherever fits, at whatever heading depth the location calls for. The fixed three are the skeleton; the catalog is the flesh.

- **Abstract**: one self-contained paragraph stating this document's actual claim or decision - not a preview of what the reader is about to read, and not usage instructions.
- **Introduction**: document-wide context needed before the technical content. Carries no direct content itself.
- **Explanation**: the document's actual content, as topic subsections in the order the author judges most useful - see [Conventions](#conventions) for this specification's own mandatory naming and cross-referencing rules, and [Relevance discipline](#relevance-discipline) for what belongs in the body versus the companion facets.

### Conventions
This specification's own mandatory naming and cross-referencing rules — every document following it follows these, not just an option to consider.

#### Field Naming Convention
All front-matter field names use PascalCase (`Name`, `URI`, `Tasks`, `Model`, `Effort`, `Title`, `Status`, etc.), applied uniformly across every field in every document.

#### Internal Cross-References
Any reference within a document to another section of the same file must be a real hyperlink (e.g. `[Conventions](#conventions)`), never plain text (e.g. `see Conventions` or a malformed pseudo-link like `see ###Conventions`). A broken anchor is easy to spot; a stale plain-text reference is not.

#### Relevance discipline
A body statement earns its place by serving the reader of the document's **current state**: reading it must change that reader's understanding of the design as it stands — its claims, definitions, arguments, or open questions. Content whose value is to a reader auditing *how* that state came to be does not belong in the body, however true or interesting it is: where and with whom positions were formed, in what order decisions arrived, the narrative of the debate that shaped them, anecdotes, and participant detail are decision-shaping context and belong to the paired [Changelog](./documentation-changelog.md). The test is not usefulness — decision-shaping context is usually useful — but which reader it serves.

This applies inside sections that legitimately exist: a `Motivation` states the failure mode that motivates the document (current-state relevant), and a `Methodology` states the method and its verification discipline (current-state relevant); neither carries the social history of the positions they describe. The rule generalizes the provenance statement in this specification's [Abstract](#abstract) from a field list to a criterion: whatever a changelog reader needs and a current-state reader does not, is changelog content.

The full routing of former discussion-section content follows from this criterion:

- **Evidence** - the premise facts a design's argument depends on (an external system's behavior, a measured result, a literature position) stay in the body, cited inline at the claim they support; an unsupported premise weakens the claim. Comparative surveys - how other projects organize the same problem and how this project differed - are not premise evidence; they are audit content, living in the changelog entry's `Related work` section.
- **Considered and not done** - alternatives examined and rejected, with their reasons, are decision-shaping context: they serve the audit reader, and an AI-assisted reader cannot reliably tell a negated position from an affirmed one when loading a document into context. They live in the changelog entry that made the decision, under the entry's own `Considered and not done` section.
- **Open questions** - working state, not current design; they may be answered, may be moot. They live in the paired [Handoff](./documentation-handoff.md) as `Open Questions`. One boundary keeps this from over-applying: where a *specific claim* is genuinely tentative, the claim itself says so in its own statement - that is content; the question and its resolution work live in the handoff. `Status` carries document-level maturity; the body does not restate it question by question.
- **Anticipated work** - extensions and growth paths the design anticipates are not current design either; they live in the paired handoff as `Anticipated Work`.
- **Observed results** - what real use of the document's decision actually produced is not body content; a result's home is determined by its type, per the cross-cutting routing map in [documentation.md → Results routing](./documentation.md#results-routing).

#### URI
URI format (absolute vs. relative reference, the `file:` scheme prohibition) is defined in [documentation.md → URI](./documentation.md#uri) as a cross-cutting convention, applying wherever a URI appears in any document of any facet.

### Optional Sections
A non-exhaustive catalog of building blocks a document's author may use — nowhere is any of these mandatory, and this list may grow. Where exactly one goes, and at what heading depth, is the author's choice; the only hard rule is the one already stated under [Body sections](#body-sections) — no new top-level (`##`) section beside the fixed three. In practice, these are typically nested under `Introduction` or `Explanation`, wherever fits that document's actual content.

This catalog — rather than a separate template per document purpose ([`RFC - Request for Comments`](https://en.wikipedia.org/wiki/Request_for_Comments), [`ADR - Architecture decision record`](https://en.wikipedia.org/wiki/Architectural_decision), `SRD - Specify technical requirements for development`, `PRD - Product Requirement Document`, `MRD - Marketing requirement document`, `BRD - Business requirement document`, and similar labels) — is how this specification accommodates different kinds of documents. `RFC` is not a document type of its own; it is a review phase applied to a document. `PRD` is not a document type of its own; it is a product-oriented documentation guide. The structure itself does not change between them. Every scientific discipline — computer science, physics, biology, mathematics — writes papers with the same skeleton (Title, Abstract, Introduction, Method, Results, Discussion, References); no field skips the Abstract, and the differences between fields show up in emphasis and content, never in whether that skeleton applies. This specification treats every documented concept the same way: `Customer`, `Repository`, `Task`, and `Protocol` all enter documentation as equal, undifferentiated subjects — nothing about the structure should presume one kind of subject is inherently more important, or inherently different in kind, than another; what a given document actually needs to say about its subject is what determines which of the items below get used, not the subject's category. A separate independent template per document purpose tends to produce definitional drift over time instead — the same concept, such as "Abstract" or "Motivation," ends up defined slightly differently in each one. Authors pick whichever items below fit the document they're writing; unused items are simply omitted, not left as empty headers. Whether further optional sections deserve catalog entries is tracked in this specification's [handoff](./documentation-explanation.handoff.md).

#### Definition
A formal definition of the concept or term this document is about — distinct from `Abstract`, which states a claim about a document's own content, not a definition of a subject. Use `Definition` when the document's central purpose is describing what something *is* (a concept, a term, a domain entity), rather than proposing or explaining a decision.

#### Conventions
A topic may propose its own non-binding convention — naming, structural, or otherwise — typically as a sibling of that topic's other subsections. Broader than naming alone: use it for any convention the topic introduces, explicitly non-binding — enforcement, if any, is a per-organization Linter configuration choice.

#### Motivation
The specific problem or friction a document solves — not a generic statement of importance, but the concrete failure mode that motivated writing it. Commonly placed under `Introduction`.

#### Methodology
How a document's content was actually arrived at (research into precedent, the critique process it went through, testing against real examples) — worth including only when that process itself is worth recording; most documents can omit it. Commonly placed under `Introduction`, alongside but independent of `Motivation` — the two are unrelated in content and either can be used without the other.

#### Problem
The problem this document addresses, stated from the reader's, user's, or business's perspective — distinct from `Motivation`, which explains why the document itself was worth writing. For most documents the two coincide and only `Motivation` is needed; use `Problem` separately when the document's subject is a problem someone else is experiencing, not the document's own reason for existing.

#### Assumptions and Constraints
The underlying assumptions a decision or design relies on (cost, schedule, available technology, and similar), and any additional constraints the environment imposes on it. Distinct from the paired handoff's `Open Questions`: an assumption or constraint is something taken as given for this document's purposes, not an open question this document is still trying to settle.

#### Model
A description of the domain or data model the document concerns — entities, relationships, structure. Useful when the document's subject is itself a model rather than a decision, a proposal, or a narrative explanation.

#### Risks
Known threats or uncertainties to whatever this document proposes succeeding. `Risks` is about what could go wrong externally, not what the design itself costs. Open questions (recorded in the paired handoff) are about what the design hasn't decided yet.

#### Implications
What a decision or design requires beyond itself - new decisions it forces, new or modified requirements it creates, scope or schedule renegotiation it demands. Distinct from the paired handoff's `Anticipated Work` (optional extensions): `Implications` are consequences that follow from adopting this document's decision, whether or not anyone wants them to.

#### Examples
Concrete instances of the concept, rule, or pattern this document defines — showing what following (or violating) it actually looks like in practice. Distinct from `Explanation`'s own illustrative content: `Examples` is for a document whose primary content is a definition or a rule, where worked instances are the clearest way to convey what that rule permits or forbids.

### Progressive migration
A document written under an earlier version of this specification is not required to be updated immediately when this specification changes. Instead, it is brought in line with the current structure the next time that file is naturally edited for any reason - not as a dedicated, separate migration pass. This applies to structural changes (section names, nesting) as much as to front-matter field changes.
