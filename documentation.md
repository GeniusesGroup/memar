---
Title: "Documentation"
Status: Proposed
Start Date: 2026-06-21
ID: 495000
Applied to: []
Citations:
    - Title: "Modeling"
      URI: "./modeling.md"
      Relation: Depends_on
      Reason: "Documentation is the result of correct modeling. The concept of Documentation cannot be understood or defined independently from the modeling process"
    - Title: "Dependency Resolution via File URI and Companion Manifest"
      URI: "./khayyam-dependency_resolution.md"
      Relation: "Reference"
      Reason: "This specification's use of URI for contributor identity follows the same File URI approach already established for dependency resolution."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Directed every revision", "Resolved merge-numbering and collision-resolution rules", "Resolved the Contribution-to-Task decision", "Caught multiple front-matter inconsistencies", "Directed the Abstract/Introduction/Explanation restructuring", "Proposed removing the fixed Guide-level/Reference-level headings in favor of an author-named, Abstract-linked Guide topic", "Directed the generalization from RFC-specific to document-generic scope"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Drafted and revised the specification across multiple rounds", "Proposed the topic-first Reference-level structure and Discussion section", "Migrated Contributors to Task-based tracking", "Implemented the Abstract/Introduction/Explanation restructuring", "Implemented the author-named Guide-topic convention", "Fixed regressions and naming collisions in the supplied file's own restructuring", "Renamed and generalized the specification to document-generic wording"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Works: ["Critical review"]
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Works: ["Restructured an earlier revision's section layout", "Applied the pre-Final merging and contributor-preservation rules"]
        URI: ""
---

# Documentation
This document specifies the canonical documentation structure every formal document produced under Geniuses Group must follow.

## Abstract
This specification defines the structure every formal document in Geniuses Group's projects must follow: a YAML front-matter block for identity, classification, citations, and attribution, followed by a body organized as `Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`, and `Change Rationale`. See [Guide](#how-to-make-a-new-document) for how to write a new document using this specification.

## Introduction
*This section's subsections (`Motivation`, `Methodology`) are a suggested partitioning, not the only one — an author may add another subsection here with a stated reason the existing ones don't cover what's needed. The `Introduction` heading itself carries no direct content.*

### Motivation
The real motivation for this specification is not specific to any one project or document purpose — it is to give every document produced across Geniuses Group's projects a single, predictable structure, so a reader or an AI assistant who has read one document already knows where to find anything in another, regardless of which project or document type it belongs to.

### Methodology
This specification's structure was not designed in the abstract in a single pass. It was arrived at through: research into precedent from other documentation and standards processes (including IETF); sustained critical review across multiple working sessions, with each proposed change argued for and against rather than accepted on first suggestion; direct testing of proposed structural changes against a real document already written under an earlier version of this specification ([protocol.md](https://github.com/GeniusesGroup/memar/blob/2cb39b5eeb3a0eddd5bc1bfe132193068dea768b/RFCs/protocol.md)), which is what surfaced a concrete scattering problem later fixed by the topic-first structure below, rather than that problem being reasoned out abstractly beforehand; and a review of documentation conventions across disciplines (research papers, standards documents, architecture records), which found the same recurring building blocks — identity, a compact claim, motivating context, detailed content, open questions, rationale — differing mainly in emphasis rather than fundamental shape.

## Explanation
*Reading every topic below in full is not required — read only what's relevant to your question. If a single topic can answer this document's central, most likely question on its own, without needing the rest, the author should link to it from the Abstract labeled "Guide" (as this document does). Not every document has such a topic; this is optional, not mandatory. When one exists, it is conventionally listed first, so a reader who skips the Abstract and comes straight here still finds it without needing to search. There is no fixed heading name reserved for it — name it for what it actually does (e.g. "How to make a new document" below), not generically.*

### How to make a new document
1. Copy the template from [The Template](#the-template) below into a new file named `<short-descriptive-slug>.md` — no number, no domain prefix, just a short, hyphenated, human-readable slug derived from the Title.
2. Set `ID` to the current UTC hour-count, and never change it again. On Linux/macOS: `echo $(( $(date -u +%s) / 3600 ))`. On Windows PowerShell: `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`. On any platform with Python: `python3 -c "import time; print(int(time.time()//3600))"`.
3. Fill in the rest of the front matter:
   - `Title`: short, quoted, unique.
   - `Status`: start at `Draft`.
   - `Start Date`: today's date (UTC), matching the moment `ID` was generated.
   - `Applied to`: leave `[]` until the document reaches `Final`.
   - `Citations`: leave `[]` if none apply; otherwise one entry per cited source, with `Relation` one of `Reference`, `Depends_on`, `Depends_for`, `Extends`, `Extends_by`, `Conflicts`, `Superseded`, `Superseded_by`, and `Reason` explaining why.
   - `Contributors`: one entry per contributor, each with at least one `Tasks` item (`Works` — an array of very short, headline-style strings describing what was done — plus optional `URI`). AI contributors also add `Model` and `Effort`.
4. Write the body.
   - `Abstract`, `Introduction` (`Motivation`, `Methodology`) stay unified, document-wide prose.
   - Under `Explanation`, split the content into topic subsections; give each topic its own `#### Discussion` (`Drawbacks` / `Rationale and alternatives` / `Prior art` / `Unresolved questions` / `Future possibilities`) only where the topic genuinely has something to say, never as an empty header. For a topic needing finer sub-sections, nest `#### {Sub section title}` under it. A topic may also propose its own `Conventions` — see [Optional Sections](#optional-sections) for this and other optional building blocks; placement is flexible beyond the fixed top-level sections.
   - If a single topic can answer the document's central question on its own, name it for what it does, list it first, and link it from the Abstract labeled "Guide." Anything that applies to the whole document rather than one topic goes in the document-wide `Discussion` section, not into any topic's own bundle.
   - Leave `Results` empty unless there is real, observed outcome to report — it is retrospective, not a prediction made while writing the document.

### The Template
This is illustrative, not normative — it shows the shape every document starts from, not a rigid enforcement of exactly what must be present. Copy everything below into a new file and replace every placeholder.

```
---
Title: ""
Status: Draft
Start Date: ""
ID: ""
Applied to: []
Citations:
    - Title: ""
      URI: ""
      Relation: ""
      Reason: ""
Contributors:
  - Name: ""
    URI: ""
    Tasks:
      - Works: []
        URI: ""
---

# Document Title

## Abstract

## Introduction

### Motivation

### Methodology

## Explanation

### {A freely-named, illustrative topic answering the document's central question on its own — optional; list it first and link it from Abstract labeled "Guide" if it exists}

### {Section title}
{Description text}

#### {Sub section title}
{Description text}

#### Discussion

##### Drawbacks

##### Rationale and alternatives

##### Prior art

##### Unresolved questions

##### Future possibilities

## Results

## Discussion

### Drawbacks

### Rationale and alternatives

### Prior art

### Unresolved questions

### Future possibilities

## Change Rationale
```

### File
- `<slug>.md` — short, hyphenated, no number, no domain prefix. Stable once Final.
- Filenames never contain [ID](#id)

### Title
A short, unique, human-readable name for the document, in double quotes. It is the source of the filename slug. A title change that alters the concept is a new document with a new `ID`; a title change that merely rephrases the same concept is a minor revision of the same document.

### Status

| Status | Meaning | Applied to | Safe to depend on? |
| --- | --- | --- | --- |
| **Draft** | Direction is not yet settled; real, unresolved questions remain, named in that document's own Unresolved questions. | Empty | No |
| **Proposed** | Design discussion reached consensus; ready for final review before being reflected in canonical documentation. | Empty | Not yet — may still be revised during final review |
| **Final** | Reflected in canonical documentation. | Lists exactly where | Yes |
| **Superseded** | Replaced by a newer document. See `Superseded by`. | Unchanged from when it was Final | No — depend on the superseding document instead |
| **Rejected** | Considered and explicitly not adopted. Kept for the historical record. | Empty | No |

Additional rules:
- `ID` is never reused, regardless of status, including Rejected.
- Move `Status` to `Proposed` once discussion converges.
- Move to `Final` once it's reflected in canonical documentation.
- Nothing before `Final` should be treated as settled by anyone depending on the document.
- Moving a Final document's substance requires a new, superseding document, not an in-place edit.
- A reconsidered Rejected idea becomes a new document with its own number, referencing the rejected one via `Citations`.
- `Applied to` reflects canonical-documentation status only, never informal or practical usage. A document can be in active, wide practical use while still `Proposed`; that does not change what `Applied to` should contain. (This document is itself an example: in active use as the working specification while `Proposed`, with `Applied to` correctly empty.)

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

### Applied to
An array of file URIs, or the single string `"*"` meaning the document applies without limitation — to any project that chooses to use this specification, not to one project specifically. A more specific entry is a file URI with an optional fragment, e.g. `["Khayyam.md#control-flow"]`. Empty (`[]`) for `Draft`/`Proposed`/`Rejected`; populated only at `Final`; unchanged from its Final value for `Superseded`.

### Citations
An array of records citing another document or an external source, each with:
- **Title**: the cited work's title, quoted.
- **URI**: the cited work's URI — a relative reference for a document in this repository (e.g. `./dependency-resolution.md`), an absolute URI for anything external. See [URI](#uri).
- **Relation**: one of `Reference` (cites for context, no structural dependency), `Depends_on` (cannot be implemented/understood without the cited work), `Depends_for` (inverse of `Depends_on`), `Extends` (builds on top of), `Extends_by` (inverse of `Extends`), `Conflicts` (a real, unresolved tension), `Superseded` (this document obsoletes the cited document), `Superseded_by` (the inverse).
- **Reason**: free text on why the relationship holds.

List order carries no meaning. When a document is superseded, both sides update: the older document's `Status` becomes `Superseded` with a `Superseded_by` entry pointing forward; the newer document adds a `Superseded` entry pointing back.

**Citing external sources.** A citation should only be added when the relationship is substantive, not decorative — not a passing or general-sounding mention. When judging whether an external source is worth citing, prefer:
- Peer-reviewed or standards-body sources (published research, IETF/W3C/ISO-style documents) over a vendor's own product documentation, where both are available.
- Structure as a quality signal: a source that shows its reasoning or evidence rather than only asserting a conclusion is more trustworthy than one that reads well but argues nothing — polished prose is not itself evidence of rigor.
- A clear distinction between two different kinds of claims from the same source: a claim about *observable, testable behavior* (e.g. "this software does X under condition Y") is generally reliable regardless of the source's other qualities; a claim about that same source's *own design philosophy or motives* is a self-assessment and should be treated with more skepticism, since the source is not a neutral party about itself.

#### Discussion
##### Rationale and alternatives
An earlier version of this field lacked inverse pairs for `Depends_on`/`Extends`, while `Superseded`/`Superseded_by` already had both directions — an unexplained asymmetry. `Depends_for` and `Extends_by` were added specifically to remove it, so every relationship type is expressible from either side. The field was originally named `Related RFCs` with `Reason` holding the relationship type and `Explanation` holding the free-text justification — backwards from their plain-English meanings (`Reason` reads as "why," not "which category"). Renamed to `Citations` (also broadening scope beyond RFCs in this repository to any external source), with `Relation` now holding the category and `Reason` holding the justification.

##### Unresolved questions
1. The boundary between `Reference` and `Depends_on` is not precisely defined. The current wording above already conflates two things that may not always agree — whether the cited work is needed to *understand* this document's text, and whether it's needed to *implement* this document correctly — under one definition ("cannot be implemented/understood without..."). A real case can satisfy one without the other: this document's own `Reference` entry for RFC 000014 is understandable and implementable without RFC 000014 at all, since this document's `URI` topic defines its own rules independently — but a different document could be fully readable on its own while still being impossible to correctly implement without another document's mechanism already existing. A proposed starting criterion for the *understandability* axis — if this document's own definitions are unintelligible without reading the cited work, use `Depends_on`; if it's merely a pointer to further information and this document stands alone without it, use `Reference` — is a reasonable basis, but does not by itself resolve whether an *implementability* axis needs to be tracked separately, or how to classify cases where the two axes disagree. Deferred to a dedicated session rather than resolved here.

### URI
A URI is a string identifier as defined by RFC 3986. Two forms are used throughout this specification:
- **Absolute URI**: carries a scheme, e.g. `mailto:omid@geniuses.group`, `https://claude.ai`. Used when the URI must resolve independently of this repository.
- **Relative reference**: a scheme-less reference resolved against a base URI (RFC 3986, Section 5), e.g. `./chat-logs/x.md`. Used for resources local to this repository. This is a first-class, standards-compliant form, not a workaround.

The `file:` scheme (RFC 8089) specifically requires an absolute path, which breaks portability across different clones of the same repository; a scheme-less relative reference is used for local paths instead of `file:` for that reason.

### Contributors
A single array listing every contributor — human, AI, or organization — as one entry. There is no `type` field: an entry with `Model`/`Effort` present is an AI system; one without them is a person or organization. There is no `Contribution` field — every contributor's involvement is recorded as one or more `Tasks` entries instead.

**Required.** Every contributor entry must have at least one `Tasks` entry, and every `Tasks` entry must have at least one item in `Works`. A `Tasks` entry's `URI` is optional — include it when a supporting artifact genuinely exists and is reachable; when it doesn't, `Works` alone (e.g. `["Present for the design discussion"]`) is sufficient.

**Preservation rule.** This applies to every document in the project, not only this one. While a document's `Status` is not yet `Final`, a contributor may update or extend their own entry across revisions, but must never add to or rewrite another contributor's entry. The one exception: if another contributor's entry describes work that has since been removed or reverted from the document itself, so that entry now describes something no longer present, any contributor may remove that specific stale portion — this is pruning an inaccurate claim, not an editorial rewrite, and still does not permit adding new claims or altering what remains of that entry. Once a document reaches `Final`, every contributor entry is frozen and immutable, including from this pruning exception. Whether pruned material should be preserved in `Change Rationale` or is adequately covered by version-control history alone is not settled — see the Unresolved questions under [Discussion](#discussion-6).

**Reference example.**
```yaml
Contributors:
  - Name: "My Name"
    URI: "mailto:me@example.org"
    Tasks:
      - Works: ["Present for the design discussion", "Did not directly edit the text"]
        URI: ""

  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "extended thinking enabled"
    Tasks:
      - Works: ["Drafted initial text", "Incorporated revisions"]
        URI: "./chat-logs/2026-07-04-example.md"
```

**Field notes.**
- **URI** (contributor-level): required, absolute (see [URI](#uri)) — identifies the contributor, not a work artifact.
- **Model / Effort**: present only for AI entries. `Model` is the officially documented identifier at time of writing; `Effort` is free text, not an enforced vocabulary.
- **Tasks**: array; each entry has `Works` (array of short strings, required, at least one item) and `URI` (optional, absolute or relative reference).
- **Works length.** Each item must be short and headline-like — a few words, not a sentence or a paragraph. If real detail is needed beyond a short phrase, put it behind a `URI` (a document, an archived conversation) rather than writing a long entry.
- Entries are not ordered by importance; list order carries no meaning.

#### Discussion
##### Drawbacks
`Works` as free text means no automated tooling can reliably query "who did what" across many documents without parsing inconsistent phrasing, at least until there's enough data to justify a fixed vocabulary. Without an explicit `type` field, identifying an AI entry depends on `Model`/`Effort` presence, reliable only as long as no future contributor type exists without a model/effort concept either. A `Model` identifier may later be deprecated or renamed by its provider, leaving an unresolvable historical reference. Where `Tasks` archives should actually be stored is not settled by this field's definition (see Unresolved questions).

##### Rationale and alternatives
- **Keep `Author(s)`/`AI(s)` as two separate arrays (an earlier draft; not chosen)**: duplicates nearly every field and needs a new parallel array for every future contributor category.
- **A single array with an explicit `type` field (an earlier draft; not chosen)**: encoded a distinction that isn't actually guaranteed by category membership — a human entry offers no real guarantee of independent review, so `type` added structure without adding real information.
- **A dedicated `Contribution` field (an earlier draft; not chosen)**: once `Tasks` gained real structure, a separate free-text field became redundant — anything expressible in `Contribution` is expressible as a `Tasks` entry's `Works`, including simple presence with no artifact, since `URI` there is optional.
- **Separate `Titles` and `Explanation` fields within each `Tasks` entry (an earlier draft; not chosen)**: `Titles`' name was too easily confused with the document's own top-level `Title` field — in practice, contributors (including an AI contributor) copied the document's `Title` verbatim into `Titles` rather than describing the specific work done, defeating the field's purpose. Merging into a single `Works` array of short strings, with a name unrelated to `Title`, removes that specific confusion.
- **`file://` URIs for local references (rejected)**: requires an absolute path per RFC 8089, breaking portability across repository clones; a relative reference achieves the same purpose while remaining standards-compliant.

##### Prior art
This field's use of `URI` for identity follows RFC 000014's use of File URIs for dependency resolution. The CRediT (Contributor Roles Taxonomy) system used by academic journals is a comparable example of structured contributor attribution outside this project — though CRediT uses a fixed, controlled set of role categories, which this specification deliberately does not adopt for `Works`, since a contributor's actual involvement can be broader or more specific than any fixed list allows.

##### Unresolved questions
1. Should `Works` eventually move to a fixed, controlled set of categories, or stay free text indefinitely?
2. Where should archived material referenced by `Tasks` actually be stored, given that keeping it inside this repository was explicitly ruled out as adding unwanted size and clutter?

### Body sections
The body follows the front-matter, as a fixed set of top-level (`##`) sections in order: `Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`, `Change Rationale`. No document may introduce a new top-level section beside these without a change to this specification itself. Beyond that one hard boundary, exact placement and heading depth of anything nested under a fixed top-level section are the author's choice — see [Optional Sections](#optional-sections) for a non-exhaustive catalog of building blocks commonly used that way.

- **Abstract**: one self-contained paragraph stating this document's actual claim or decision — not a preview of what the reader is about to read, and not usage instructions. If a single topic under Explanation can answer the document's central question on its own, link to it here labeled "Guide."
- **Introduction**: document-wide context needed before the technical content. Carries no direct content itself.
- **Explanation**: the document's actual content, as topic subsections in the order the author judges most useful — see [Conventions](#conventions) for this specification's own mandatory naming and cross-referencing rules, and [The Discussion pattern](#the-discussion-pattern) for how each topic's rationale-type content is structured.
- **Results**: what was actually observed after real use of this document's decision — retrospective, not a prediction made while writing the document. Left empty until there is real data to report; not required to ever be filled in.
- **Discussion**: see [The Discussion pattern](#the-discussion-pattern).
- **Change Rationale**: why the document changed across revisions — kept separate from Discussion, since it is about the document's own history, not a justification of the current design, and accumulates append-only much like `Contributors`.

### The Discussion pattern
`Discussion` appears in two places, following the same rule in both: the document-wide `## Discussion` (for anything that applies to the whole document rather than one topic) and each topic's own `#### Discussion` (or deeper, if the topic itself has sub-sections). In both places, `Discussion` wraps whichever of `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities` actually have content — never as a fully empty wrapper, and never with an individual empty sub-header either. This is the one consistent rule at every level; there is no separate, looser rule for topics without sub-sections. A topic-level `Conventions` item, if used, is not part of this wrapper — see [Optional Sections](#optional-sections).

### Conventions
This specification's own mandatory naming and cross-referencing rules — every document following it follows these, not just an option to consider.

#### Field Naming Convention
All front-matter field names use PascalCase (`Name`, `URI`, `Tasks`, `Model`, `Effort`, `Title`, `Status`, `Relation`, etc.), applied uniformly across every field in every document.

#### Internal Cross-References
Any reference within a document to another section of the same file must be a real hyperlink (e.g. `[URI](#uri)`), never plain text (e.g. `see URI` or a malformed pseudo-link like `see ###URI`). A broken anchor is easy to spot; a stale plain-text reference is not.

### Optional Sections
A non-exhaustive catalog of building blocks a document's author may use — nowhere is any of these mandatory, and this list may grow. Where exactly one goes, and at what heading depth, is the author's choice; the only hard rule is the one already stated under [Body sections](#body-sections) — no new top-level (`##`) section beside the fixed six. In practice, these are typically nested under `Introduction`, `Explanation`, or `Discussion`, wherever fits that document's actual content.

This catalog — rather than a separate template per document purpose ([`RFC - Request for Comments`](https://en.wikipedia.org/wiki/Request_for_Comments), `[ADR - Architecture decision record](https://en.wikipedia.org/wiki/Architectural_decision)`, `SRD - Specify technical requirements for development`, `PRD - Product Requirement Document`, `MRD - Marketing requirement document`, `BRD - Business requirement document`, and similar labels) — is how this specification accommodates different kinds of documents. The structure itself does not change: documents across many disciplines (research papers, standards, architecture records) converge on the same underlying building blocks (identity, a compact claim, motivating context, detailed content, open questions, rationale), differing mainly in which blocks they emphasize, not in fundamental shape. A separate independent template per document purpose tends to produce definitional drift over time instead — the same concept, such as "Abstract" or "Motivation," ends up defined slightly differently in each one. Authors pick whichever items below fit the document they're writing.

#### Conventions
A topic may propose its own non-binding convention — naming, structural, or otherwise — typically as a sibling of that topic's `Discussion`. Broader than naming alone: use it for any convention the topic introduces, explicitly non-binding — enforcement, if any, is a per-organization Linter configuration choice.

#### Motivation
The specific problem or friction a document solves — not a generic statement of importance, but the concrete failure mode that motivated writing it. Commonly placed under `Introduction`.

#### Methodology
How a document's content was actually arrived at (research into precedent, the critique process it went through, testing against real examples) — worth including only when that process itself is worth recording; most documents can omit it. Commonly placed under `Introduction`, alongside but independent of `Motivation` — the two are unrelated in content and either can be used without the other.

#### Problem
The problem this document addresses, stated from the reader's, user's, or business's perspective — distinct from `Motivation`, which explains why the document itself was worth writing. For most documents the two coincide and only `Motivation` is needed; use `Problem` separately when the document's subject is a problem someone else is experiencing, not the document's own reason for existing.

#### Model
A description of the domain or data model the document concerns — entities, relationships, structure. Useful when the document's subject is itself a model rather than a decision, a proposal, or a narrative explanation.

#### Risks
Known threats or uncertainties to whatever this document proposes succeeding — distinct from `Drawbacks` (known costs of the current design, regardless of outcome) and `Unresolved questions` (open design questions this document hasn't settled). `Risks` is about what could go wrong externally, not what the design itself costs or hasn't decided yet.

### Progressive migration
A document written under an earlier version of this specification is not required to be updated immediately when this specification changes. Instead, it is brought in line with the current structure the next time that file is naturally edited for any reason — not as a dedicated, separate migration pass. This applies to structural changes (section names, nesting) as much as to front-matter field changes.

#### Discussion
##### Rationale and alternatives
**A dedicated, one-time migration pass across all existing documents (considered, not chosen)**: front-loads the entire cost at once and risks becoming its own large, disruptive undertaking as the number of existing documents grows; deferring each file's migration to its next natural edit spreads the cost out and avoids ever needing a dedicated migration project.

## Results
Insufficient time has passed since this specification's structure was adopted to report real, observed outcomes from its use across multiple documents. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Consolidating the specification and its field specifications into one document means they can no longer be loaded independently — a reader needing only one field's rules must load the whole document. The document is longer than any of its predecessors, and there is no way to load only part of it into context (mitigated by the Abstract-linked "Guide" topic being self-contained for the ordinary case — see Rationale and alternatives). Adding a `Document Profiles` topic that honestly defines only one profile in full is itself a form of incompleteness — a reader looking for how to write a PRD or ADR today will not find one, only an acknowledgment that it doesn't exist yet.

### Rationale and alternatives
- **Keep the specification and its field specifications as separate files (rejected)**: required loading multiple files into every document-writing session and created an ongoing sync obligation between them.
- **Keep a small, separate copy-paste-ready template file, consolidate only the specs (considered, not chosen)**: still two files to load, still a drift risk. The chosen approach keeps drift risk at zero while keeping the everyday reading burden close to what a small separate template file would have offered.
- **Organize the body by content-type rather than by topic — this document's own earlier structure (superseded)**: reviewing a real document produced under that structure (`protocol.md`) showed that content about a single topic ends up scattered across as many as six different top-level sections. The topic-first structure replaces it.
- **A fixed `Guide-level explanation` / `Reference-level explanation` heading pair (an earlier draft; not chosen)**: forced every document's practical walkthrough into a name that didn't always fit its actual content — this document's own such content is not "explaining" anything, it's usage instructions — and implied a two-tier importance ranking (Guide "more important" than Reference-level) that isn't true for every document. Replaced with an optional, freely-named, Abstract-linked "Guide" topic: the convention that matters (a fixed word, "Guide," always findable from the Abstract) survives, while the section's actual name and its position relative to other topics are left to the author.
- **Embed the template inline as prose rather than a fenced code block (rejected)**: harder to copy verbatim, harder to visually distinguish from surrounding prose.
- **Model the body sections directly on the standard seven-part research paper structure (Title, Abstract, Introduction, Literature Review, Methodology, Results, Discussion and Conclusion) (considered, partially adopted)**: `Abstract`, `Introduction`, `Methodology`, `Results`, and `Discussion` map reasonably well and were adopted; a `Literature Review`-equivalent (`Prior art`) was considered for promotion to a standalone, early top-level section, but rejected — see Prior art below. A `Conclusion`-equivalent was considered and folded into `Discussion` rather than kept separate, since a design document under active revision doesn't reach a "conclusion" the way a completed study does, and a separate section for it would overlap with `Discussion`'s own role.
- **Fully define PRD, ADR, and other profiles now, rather than deferring them (rejected)**: would repeat the exact mistake this specification's own Methodology is built to avoid — designing structure in the abstract instead of testing it against a real document of that kind.

### Prior art
The Rust RFC process maintains a single `0000-template.md` and a separate `README.md` describing the process, rather than consolidating the template with per-field specifications — a project-specific choice here, driven by this project's practice of feeding the specification plus its specs into AI-assisted chat sessions at every document-writing occasion, which makes the loading cost of multiple files more salient than in a typical human-only workflow.

Moving `Prior art` to an early, standalone section (mirroring a Literature Review's position, right after the Introduction) was considered and rejected: in this project, prior art is inherently comparative and backward-looking — it explains why a design does or doesn't resemble what other projects do, which only makes sense after the reader already knows what this project's own design is. A Literature Review in a research paper instead builds context the reader needs before the paper's own contribution is presented, which is a different function. Every actual Prior art entry in this specification (e.g. comparing to Rust's or IETF's numbering process) illustrates this: it is only meaningful once the reader already knows what this specification decided.

### Unresolved questions
1. Should this consolidated spec itself be split again once the project has enough documents that the loading cost of a single long document starts to matter?
2. Is `Change Rationale` needed at all, given that version control already records exactly what changed and when? Kept for now at the top level rather than removed, pending a decision. This is reinforced by a related question raised while refining the `Contributors` preservation rule: whether material pruned from a stale contributor entry should be preserved in `Change Rationale` — if version control already covers that case adequately, it is one more reason `Change Rationale` may be redundant.
3. The boundary between `Reference` and `Depends_on` in `Citations` is not precisely defined — see the Unresolved questions under [Citations](#citations).
4. See [Document Profiles → Unresolved questions](#document-profiles) for open questions about how additional profiles beyond RFC should be defined and composed with this base structure.

### Future possibilities
If tooling is ever built to help produce or check documents, it could read this single spec file and walk a contributor through each front-matter field and body section in order, validating values as they're filled in. If a future document introduces an additional `Status` value, `Citations` `Relation` value, or `Contributors` field, this specification is where that addition should be documented.

## Change Rationale
- **Initial consolidation.** Consolidated the RFC template and its field specifications into a single specification, motivated by the loading cost of feeding multiple files into every chat session and the drift risk between the template and its specs. A pre-Final merging rule allows related Draft/Proposed RFCs to be consolidated without generating a new RFC number. A contributor preservation rule requires every contributor to add their own entry and forbids modifying others'.
- **Second revision.** Fixed front-matter self-inconsistencies: `Applied to` contained `["*"]` while `Status` was `Proposed`, contradicting the Status table (emptied, with a clarifying rule); `Start Date` had drifted from the date implied by `RFC Number` (corrected). Clarified the Contributor preservation rule governs every RFC, not only this document. Corrected an inaccurate claim in the `Related RFCs` `URI` field description. Replaced vague merge-numbering guidance with an explicit tie-break rule. Generalized collision-resolution guidance away from a specific PR-based mechanism.
- **Third revision.** Replaced the flat content-type-first organization of Reference-level explanation with a topic-first structure after confirming, against a real RFC (`protocol.md`), that content was genuinely scattered across up to six top-level sections. Introduced the RFC-wide `Discussion` section, kept separate from `Change Rationale`. Moved `The Template` into Guide-level explanation. Removed `Contribution` in favor of Task-based tracking, requiring at least one `Tasks` entry per contributor. Shortened and refocused Motivation on a shared structure across Geniuses Group's projects rather than a Memar-specific concern.
- **Fourth revision.** Fixed a malformed internal reference and added an explicit rule that all internal section references must be real hyperlinks. Removed `Common concepts`, promoting `URI` to its own Reference-level topic. Relocated `Field Naming Convention` from `Discussion` to `Reference-level explanation`. Documented the recursive sub-section/Discussion nesting pattern. Rewrote Guide-level explanation to be self-contained for the ordinary case. Added an explicit rule that `Tasks` entries should be short and headline-style. Refined the Contributors preservation rule to allow pruning stale claims.
- **Fifth revision.** Merged `Tasks`' `Titles` and `Explanation` fields into a single `Works` field after this document's own Contributors list showed the predicted failure mode in practice. Logged an Unresolved question under `Related RFCs` about the `Depends_on`/`Reference` boundary, deferred to a dedicated future session.
- **Sixth revision.** Renamed `Summary` to `Abstract` and rewrote its content to state this document's actual claim rather than give navigational instructions. Introduced `Introduction` (`Motivation`, `Methodology`) and `Explanation` (`Guide-level explanation`, `Reference-level explanation`) as wrapper sections. Added `Results`, defined as strictly retrospective. Renamed `Related RFCs` to `Citations`, broadening its scope to non-RFC sources, and corrected an inverted field pairing (`Relation` now holds the relationship category, `Reason` the free-text justification). Added source-credibility criteria for external citations. Considered and rejected relocating `Prior art` to an early, standalone section. Added a progressive migration rule. Generalized the "custom subsection with a stated reason" allowance to `Introduction` and `Explanation`'s own subsections. Noted, as a newly surfaced constraint, that the deepest defined nesting level reached the maximum heading depth Markdown/HTML supports.
- **Seventh revision.** Removed the fixed `Guide-level explanation` / `Reference-level explanation` heading pair, after recognizing that forcing every RFC's practical walkthrough under a literal "explanation"-suffixed name was itself inconsistent with the observation that such content, in this document's own case, does not explain anything — it documents usage. Topics now sit directly under `Explanation` in author-chosen order and names. An RFC may optionally designate one topic as an illustrative walkthrough answering its central question; when it does, that topic is named for what it actually does (here, "How to make a new RFC"), conventionally listed first, and linked from the Abstract labeled "Guide" — preserving a fixed, findable convention (the word "Guide" in the Abstract) without hardcoding the target topic's own name or implying a fixed importance ranking among topics. This also removed one level of heading nesting throughout, resolving the previously noted concern about reaching Markdown's maximum heading depth.
- **Eighth revision.** Fixed four issues found by comparing against the file actually supplied for this round, which had been worked from an earlier self-authored draft instead: unified the Discussion pattern so every topic with rationale-type content wraps it in a `Discussion` header consistently — previously a topic without sub-sections put its bundles directly under itself while a topic with sub-sections wrapped them in `Discussion`, an inconsistency between two decision rules where the RFC-wide level effectively had only one; `Suggested Naming Conventions` now consistently sits as a sibling of `Discussion` rather than inconsistently being inside it in one variant and outside it in the other, and was inconsistently named `Naming Conventions` in the nested variant. Moved `File` to be the first real topic, per its position in the supplied file. Removed a duplicate sentence about AI `Model`/`Effort` fields at the end of The Template section that repeated what step 3 of the walkthrough already covers. Removed `Filenames never contain it` from `RFC Number`'s own text, since that rule belongs to and now lives solely under `File`.
- **Ninth revision.** Worked from the file actually supplied, incorporating its own restructuring (grouping conventions, pulling the Discussion pattern out of Body sections) while fixing issues found in its execution: removed migration guidance from "How to make a new RFC," since upgrading an existing RFC is unrelated to making a new one; merged two redundant sentences within `Progressive migration` into one; consolidated a broken, duplicated `Optional Sections`/`Conventions` structure into a single `Conventions` topic; fixed a reversion where `Suggested Naming Conventions` had been folded back inside the `Discussion` wrapper and where topic-level Discussion had been described as optional again, both contradicting the eighth revision's unification; added dedicated `Motivation and Methodology` and `The Discussion pattern` topics, with `Body sections` now linking to them instead of inlining their definitions; named the new `Motivation and Methodology` and `About Suggested Naming Conventions` topics specifically to avoid colliding with this document's own real `Introduction` prose and with the many literal `Suggested Naming Conventions` bundle instances elsewhere in the template.
- **Tenth revision.** Fixed a heading-level mismatch between prose and example (describing a topic-level convention item as a sibling of `#### Discussion` while showing it at `###` in a code block). Corrected a misunderstanding of the ninth revision's own `Conventions` heading appearing twice: one instance is this template's own mandatory rules (kept, unchanged in meaning), the other is a catalog entry within `Optional Sections` for a topic's own proposed convention — these are different things that happened to share a name, not a duplicate to merge. Removed the `Motivation and Methodology` topic created in the ninth revision, since Motivation and Methodology are unrelated in content and neither belongs bundled with the other, and since limiting `Optional Sections` to only these two implied it was an exhaustive list rather than an open, growing catalog. Broadened the topic-level naming-only convention item into a general `Conventions` item covering any non-binding convention a topic proposes, not naming alone. `Optional Sections` no longer prescribes a specific heading depth for any of its entries — placement is the author's choice, bounded only by the existing rule against new top-level sections.
- **Eleventh revision.** Renamed this specification from `rfc-template.md` (`RFC Template Specification`) to `documentation.md` (`Documentation Framework Specification`), following an extended discussion on knowledge management concluding that `RFC`, `PRD`, `ADR`, and similar labels are better treated as profiles applied to one shared documentation structure than as independent document types requiring separate templates. `RFC Number` was renamed to `ID` throughout, since the identifier mechanism itself was never RFC-specific. Added a `Document Profiles` topic stating this principle and honestly marking that only the RFC profile is fully defined and tested today; other profiles (`PRD`, `ADR`, `Concept Definition`) are deliberately left undefined until each can be developed and tested against a real document of that kind, consistent with this specification's own Methodology. Removed a front-matter `Citations` entry that had cited `rfc-template.md` as a separate document this one "Extends" — inapplicable, since this is a rename of that document, not an extension of it. Generalized RFC-specific wording throughout the rest of the specification to be document-generic, without otherwise changing any established rule, structure, or convention — this revision is a rename and generalization pass, not a redesign.
