---
Title: "Documentation — Explanation"
Status: Proposed
Start Date: 2026-06-21
ID: 495000
---

# Documentation — Explanation
This document specifies the canonical documentation structure every formal explanation document must follow.

## Abstract
This specification defines the structure every formal document in any projects must follow: a YAML front-matter block for identity and classification, followed by a body organized as `Abstract`, `Introduction`, `Explanation`, `Results`, and `Discussion`. Provenance — citations, contributor attribution, cross-document propagation tracking, and revision history — does not live in this document's front matter or body; it lives in the paired [Changelog](./documentation-changelog.md), since a reader of the base artifact needs its current state, not its provenance.

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
- `<slug>.md` — short, hyphenated, no number, no domain prefix. Stable once Final.
- Filenames never contain [ID](#id)

### Title
A short, unique, human-readable name for the document, in double quotes. It is the source of the filename slug. A title change that alters the concept is a new document with a new `ID`; a title change that merely rephrases the same concept is a minor revision of the same document.

### Status

| Status | Meaning | Safe to depend on? |
| --- | --- | --- |
| **Draft** | Direction is not yet settled; real, unresolved questions remain, named in that document's own Unresolved questions. | No |
| **Proposed** | Design discussion reached consensus; ready for final review before being reflected in canonical documentation. | Not yet — may still be revised during final review |
| **Final** | Reflected in canonical documentation. | Yes |
| **Superseded** | Replaced by a newer document. See [`Superseded by`](#relation). | No — depend on the superseding document instead |
| **Rejected** | Considered and explicitly not adopted. Kept for the historical record. | No |

Additional rules:
- `ID` is never reused, regardless of status, including Rejected.
- Move `Status` to `Proposed` once discussion converges.
- Move to `Final` once it's reflected in canonical documentation.
- Nothing before `Final` should be treated as settled by anyone depending on the document.
- Moving a Final document's substance requires a new, superseding document, not an in-place edit.
- A reconsidered Rejected idea becomes a new document with its own number, referencing the rejected one via a `Superseded` entry in the paired Changelog's `Cited` field (see [documentation-changelog.md → Cited](./documentation-changelog.md#cited)).
- `Status` reflects canonical-documentation status only, never informal or practical usage. A document can be in active, wide practical use while still `Proposed`; that does not change its `Status`. (This document is itself an example: in active use as the working specification while `Proposed`.)

#### Discussion
##### Drawbacks
Maintaining this detailed semantics alongside the compact Status table in `README.md` means the two must stay consistent as either evolves. This specification also elaborates obligations (e.g. "Final is safe to depend on") without precisely defining what counts as a correction small enough to apply in place versus a change substantial enough to require a superseding document.

##### Rationale and alternatives
- **Leave only the one-line README table, infer detailed obligations informally (rejected)**: informal inference drifts inconsistently across a multi-generational project.
- **Fold this level of detail directly into `README.md` (rejected)**: would keep the README from staying a fast, scannable index, which is the reason this detail was extracted out in the first place.

##### Prior art
Several long-running spec processes separate a short status marker from a fuller definition of what that marker commits readers and implementers to — a pattern that recurs across standards-track processes generally, not something unique here.

##### Unresolved questions
1. What precisely distinguishes a "minor correction" applicable in place to a Final document from a change substantial enough to require a superseding document?
2. Should there be a formal mechanism keeping this document and the README's compact table synchronized, or is manual vigilance sufficient at the current scale?

### Start Date
The calendar date (`YYYY-MM-DD`, UTC) the document file was first drafted. Set once, never changed. Should agree with the date implied by `ID`, since both are meant to be captured at the same moment.

### ID
A UTC unix-time-derived integer, generated once when the file is first drafted, never reused or reassigned. It carries no meaning beyond relative creation order — generating it does not imply approval; that is `Status`'s job.

**Value.** UTC unix time truncated to the hour — `(unix seconds) / 3600` — as a plain decimal integer (e.g. `495317`).

**Generation.** See [How to make a new document](#how-to-make-a-new-document) for the per-platform commands.

**Uniqueness and collisions.** Two or more documents drafted in the same working session landing in the same hour is expected and normal. Resolve manually today: keep the first document's number, give the next one the following hour's value or any other free value. Manual resolution is a stopgap, not the preferred end state (see Future possibilities below).

**Retroactive numbering.** Pre-existing documents may be assigned an hour-value derived from their recorded `Start Date` if retroactively renumbered. Where several share a `Start Date`, order by reasonable manual judgment — no strict rule imposed.

**Merging before Final.** Two or more `Draft`/`Proposed` documents merged into one, without changing overall content, reuse one existing number; no new number is generated, and no `Citations` entries are added pointing to the abandoned ones (they never reached Final). Which number is kept:
- If the merged document keeps one original title unchanged, it uses that document's original number.
- If an entirely new title is chosen, the merged document uses the smallest (earliest) of the numbers being merged.

This rule applies only pre-Final; once Final, merging requires a new, superseding document per the Status rules.

**Storage representation.** Out of scope here — an implementation detail.

**Lookup.** Full-text search for `ID:`, or the README index (Number, Title, Status).

#### Discussion
##### Drawbacks
The number is no longer purely arbitrary — it now encodes creation order, a deliberate exception to "the number should carry no meaning," justified because creation time is an immutable fact that can't later be "reclassified" the way a domain label can. Collisions at hour granularity are expected regularly during multi-document sessions and must currently be resolved manually — a stopgap only, since no tooling exists yet. Retroactive backfilling for documents sharing a `Start Date` has no principled ordering signal.

##### Rationale and alternatives
- **Domain-encoded ranges (rejected)**: couples the identifier to a classification that can change, forcing renumbering and broken cross-references.
- **Single incrementing counter at creation (rejected)**: needs a central coordinator to avoid collisions with more than one simultaneous contributor.
- **Single incrementing counter at Final/merge time, à la Rust (considered, not chosen)**: avoids ever numbering unstable content, but doesn't allow assigning identifiers to old, already-existing ideas retroactively the way an hour-derived value does.
- **Second-level unix timestamp (considered, not chosen)**: near-zero collision risk, but a ten-digit number — longer than this project's actual document-writing pace needs.
- **Hash of the filename/slug (rejected)**: no content-integrity guarantee, long and non-memorable, solves nothing an hour-based counter doesn't already solve more simply.

##### Prior art
Rust's RFC process assigns no number at drafting; a `0000-` placeholder is used until a pull request exists, at which point the PR's own number becomes the RFC number. Rust's internal design discussion explicitly preferred small, continuous-feeling numbers over sparse or arbitrary ones. IETF RFCs are strictly sequential, centrally assigned, with no domain-based reservation.

##### Unresolved questions
None remaining. The earlier open question (hour- vs. minute-level granularity) was resolved in favor of hour-level.

##### Future possibilities
- A small helper script or shell alias that prints the current hour-value and checks for an existing collision, once the number of contributors or documents justifies the tooling investment.
- Replacing manual collision resolution with an algorithmic mechanism is preferable long-term to ad hoc human judgment, regardless of granularity; the specific tooling and workflow for that is not decided here.

### Body sections
The body follows the front-matter, as a fixed set of top-level (`##`) sections in order: `Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`. No document may introduce a new top-level section beside these without a change to this specification itself. Beyond that one hard boundary, exact placement and heading depth of anything nested under a fixed top-level section are the author's choice — see [Optional Sections](#optional-sections) for a non-exhaustive catalog of building blocks commonly used that way.

- **Abstract**: one self-contained paragraph stating this document's actual claim or decision — not a preview of what the reader is about to read, and not usage instructions.
- **Introduction**: document-wide context needed before the technical content. Carries no direct content itself.
- **Explanation**: the document's actual content, as topic subsections in the order the author judges most useful — see [Conventions](#conventions) for this specification's own mandatory naming and cross-referencing rules, and [The Discussion pattern](#the-discussion-pattern) for how each topic's rationale-type content is structured.
- **Results**: what was actually observed after real use of this document's decision — retrospective, not a prediction made while writing the document. Left empty until there is real data to report; not required to ever be filled in.
- **Discussion**: see [The Discussion pattern](#the-discussion-pattern).

### The Discussion pattern
`Discussion` appears in two places, following the same rule in both: the document-wide `## Discussion` (for anything that applies to the whole document rather than one topic) and each topic's own `#### Discussion` (or deeper, if the topic itself has sub-sections). In both places, `Discussion` wraps whichever of `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities` actually have content — never as a fully empty wrapper, and never with an individual empty sub-header either. This is the one consistent rule at every level; there is no separate, looser rule for topics without sub-sections. A topic-level `Conventions` item, if used, is not part of this wrapper — see [Optional Sections](#optional-sections).

### Conventions
This specification's own mandatory naming and cross-referencing rules — every document following it follows these, not just an option to consider.

#### Field Naming Convention
All front-matter field names use PascalCase (`Name`, `URI`, `Tasks`, `Model`, `Effort`, `Title`, `Status`, etc.), applied uniformly across every field in every document.

#### Internal Cross-References
Any reference within a document to another section of the same file must be a real hyperlink (e.g. `[Conventions](#conventions)`), never plain text (e.g. `see Conventions` or a malformed pseudo-link like `see ###Conventions`). A broken anchor is easy to spot; a stale plain-text reference is not.

#### URI
URI format (absolute vs. relative reference, the `file:` scheme prohibition) is defined in [documentation.md → URI](./documentation.md#uri) as a cross-cutting convention, applying wherever a URI appears in any document of any facet.

### Optional Sections
A non-exhaustive catalog of building blocks a document's author may use — nowhere is any of these mandatory, and this list may grow. Where exactly one goes, and at what heading depth, is the author's choice; the only hard rule is the one already stated under [Body sections](#body-sections) — no new top-level (`##`) section beside the fixed five. In practice, these are typically nested under `Introduction`, `Explanation`, or `Discussion`, wherever fits that document's actual content.

This catalog — rather than a separate template per document purpose ([`RFC - Request for Comments`](https://en.wikipedia.org/wiki/Request_for_Comments), `[ADR - Architecture decision record](https://en.wikipedia.org/wiki/Architectural_decision)`, `SRD - Specify technical requirements for development`, `PRD - Product Requirement Document`, `MRD - Marketing requirement document`, `BRD - Business requirement document`, and similar labels) — is how this specification accommodates different kinds of documents. `RFC` is not a document type of its own; it is a review phase applied to a document. `PRD` is not a document type of its own; it is a product-oriented documentation guide. The structure itself does not change between them. Every scientific discipline — computer science, physics, biology, mathematics — writes papers with the same skeleton (Title, Abstract, Introduction, Method, Results, Discussion, References); no field skips the Abstract, and the differences between fields show up in emphasis and content, never in whether that skeleton applies. This specification treats every documented concept the same way: `Customer`, `Repository`, `Task`, and `Protocol` all enter documentation as equal, undifferentiated subjects — nothing about the structure should presume one kind of subject is inherently more important, or inherently different in kind, than another; what a given document actually needs to say about its subject is what determines which of the items below get used, not the subject's category. A separate independent template per document purpose tends to produce definitional drift over time instead — the same concept, such as "Abstract" or "Motivation," ends up defined slightly differently in each one. Authors pick whichever items below fit the document they're writing; unused items are simply omitted, not left as empty headers.

We need to check other like: Evidence Against (the Idea), Design Principles, Consequences, Open Questions, ... too.

#### Definition
A formal definition of the concept or term this document is about — distinct from `Abstract`, which states a claim about a document's own content, not a definition of a subject. Use `Definition` when the document's central purpose is describing what something *is* (a concept, a term, a domain entity), rather than proposing or explaining a decision.

#### Conventions
A topic may propose its own non-binding convention — naming, structural, or otherwise — typically as a sibling of that topic's `Discussion`. Broader than naming alone: use it for any convention the topic introduces, explicitly non-binding — enforcement, if any, is a per-organization Linter configuration choice.

#### Motivation
The specific problem or friction a document solves — not a generic statement of importance, but the concrete failure mode that motivated writing it. Commonly placed under `Introduction`.

#### Methodology
How a document's content was actually arrived at (research into precedent, the critique process it went through, testing against real examples) — worth including only when that process itself is worth recording; most documents can omit it. Commonly placed under `Introduction`, alongside but independent of `Motivation` — the two are unrelated in content and either can be used without the other.

#### Problem
The problem this document addresses, stated from the reader's, user's, or business's perspective — distinct from `Motivation`, which explains why the document itself was worth writing. For most documents the two coincide and only `Motivation` is needed; use `Problem` separately when the document's subject is a problem someone else is experiencing, not the document's own reason for existing.

#### Assumptions and Constraints
The underlying assumptions a decision or design relies on (cost, schedule, available technology, and similar), and any additional constraints the environment imposes on it. Distinct from `Unresolved questions`: an assumption or constraint is something taken as given for this document's purposes, not an open question this document is still trying to settle.

#### Model
A description of the domain or data model the document concerns — entities, relationships, structure. Useful when the document's subject is itself a model rather than a decision, a proposal, or a narrative explanation.

#### Risks
Known threats or uncertainties to whatever this document proposes succeeding — distinct from `Drawbacks` (known costs of the current design, regardless of outcome) and `Unresolved questions` (open design questions this document hasn't settled). `Risks` is about what could go wrong externally, not what the design itself costs or hasn't decided yet.

#### Implications
What a decision or design requires beyond itself — new decisions it forces, new or modified requirements it creates, scope or schedule renegotiation it demands. Distinct from `Drawbacks` (costs inherent to the design) and `Future possibilities` (optional extensions): `Implications` are consequences that follow from adopting this document's decision, whether or not anyone wants them to.

#### Examples
Concrete instances of the concept, rule, or pattern this document defines — showing what following (or violating) it actually looks like in practice. Distinct from `Explanation`'s own illustrative content: `Examples` is for a document whose primary content is a definition or a rule, where worked instances are the clearest way to convey what that rule permits or forbids.

### Progressive migration
A document written under an earlier version of this specification is not required to be updated immediately when this specification changes. Instead, it is brought in line with the current structure the next time that file is naturally edited for any reason — not as a dedicated, separate migration pass. This applies to structural changes (section names, nesting) as much as to front-matter field changes.

#### Discussion
##### Rationale and alternatives
**A dedicated, one-time migration pass across all existing documents (considered, not chosen)**: front-loads the entire cost at once and risks becoming its own large, disruptive undertaking as the number of existing documents grows; deferring each file's migration to its next natural edit spreads the cost out and avoids ever needing a dedicated migration project.

## Results
Insufficient time has passed since this specification's structure was adopted to report real, observed outcomes from its use across multiple documents. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Consolidating the specification and its field specifications into one document means they can no longer be loaded independently — a reader needing only one field's rules must load the whole document. The document is longer than any of its predecessors, and there is no way to load only part of it into context (mitigated by the Abstract being self-contained for the ordinary case — see Rationale and alternatives).

### Rationale and alternatives
- **Keep the specification and its field specifications as separate files (rejected)**: required loading multiple files into every document-writing session and created an ongoing sync obligation between them.
- **Keep a small, separate copy-paste-ready template file, consolidate only the specs (considered, not chosen)**: still two files to load, still a drift risk. The chosen approach keeps drift risk at zero while keeping the everyday reading burden close to what a small separate template file would have offered.
- **Organize the body by content-type rather than by topic — this document's own earlier structure (superseded)**: reviewing a real document produced under that structure (`protocol.md`) showed that content about a single topic ends up scattered across as many as six different top-level sections. The topic-first structure replaces it.
- **A fixed `Guide-level explanation` / `Reference-level explanation` heading pair (an earlier draft; not chosen)**: forced every document's practical walkthrough into a name that didn't always fit its actual content — this document's own such content is not "explaining" anything, it's usage instructions — and implied a two-tier importance ranking (Guide "more important" than Reference-level) that isn't true for every document. Replaced with the Practice facet's companion-file convention: a document needing procedural content gets a paired `<base>.practice.md` file, named per the rule in [documentation.md](./documentation.md), with no per-document naming decision required.
- **Embed the template inline as prose rather than a fenced code block (rejected)**: harder to copy verbatim, harder to visually distinguish from surrounding prose.
- **Model the body sections directly on the standard seven-part research paper structure (Title, Abstract, Introduction, Literature Review, Methodology, Results, Discussion and Conclusion) (considered, partially adopted)**: `Abstract`, `Introduction`, `Methodology`, `Results`, and `Discussion` map reasonably well and were adopted; a `Literature Review`-equivalent (`Prior art`) was considered for promotion to a standalone, early top-level section, but rejected — see Prior art below. A `Conclusion`-equivalent was considered and folded into `Discussion` rather than kept separate, since a design document under active revision doesn't reach a "conclusion" the way a completed study does, and a separate section for it would overlap with `Discussion`'s own role.
- **A `Change Rationale` top-level section, recording why the document changed across revisions (rejected, removed)**: kept separate from `Discussion` on the grounds that it was about the document's own history rather than a justification of the current design, and accumulated append-only much like `Contributors`. Both `Change Rationale` and `Contributors` have since been moved out of the base document and into the paired [Changelog](./documentation-changelog.md) facet, where append-only historical content belongs; a reader of the base artifact needs its current state, not its provenance.

### Prior art
The Rust RFC process maintains a single `0000-template.md` and a separate `README.md` describing the process, rather than consolidating the template with per-field specifications — a project-specific choice here, driven by this project's practice of feeding the specification plus its specs into AI-assisted chat sessions at every document-writing occasion, which makes the loading cost of multiple files more salient than in a typical human-only workflow.

Moving `Prior art` to an early, standalone section (mirroring a Literature Review's position, right after the Introduction) was considered and rejected: in this project, prior art is inherently comparative and backward-looking — it explains why a design does or doesn't resemble what other projects do, which only makes sense after the reader already knows what this project's own design is. A Literature Review in a research paper instead builds context the reader needs before the paper's own contribution is presented, which is a different function. Every actual Prior art entry in this specification (e.g. comparing to Rust's or IETF's numbering process) illustrates this: it is only meaningful once the reader already knows what this specification decided.

An independent architecture-decision-record template by Jeff Tyree and Art Akerman is evidence for treating document purposes as a shared structure with per-purpose emphasis rather than as independent templates: its fields (`Issue`, `Decision`, `Positions`, `Argument`, `Implications`, `Related decisions`/`requirements`/`artifacts`/`principles`) map closely onto concerns this specification already names differently (`Abstract`, `Rationale and alternatives`) or has now added to `Optional Sections` (`Implications`), despite being designed independently and for a narrower purpose (architecture decisions specifically, not documentation generally). Most of its fields were not adopted as-is, since they duplicated an existing concept under a different name; `Implications` was the one genuinely distinct addition it contributed.

### Unresolved questions
1. Should this consolidated spec itself be split again once the project has enough documents that the loading cost of a single long document starts to matter?

### Future possibilities
If tooling is ever built to help produce or check documents, it could read this single spec file and walk a contributor through each front-matter field and body section in order, validating values as they're filled in. If a future document introduces an additional `Status` value, this specification is where that addition should be documented; new `Citations` `Relation` values, `Contributors` field changes, and `Applied to`-style propagation tracking are now documented in [documentation-changelog.md](./documentation-changelog.md) instead, since those fields now live there.
