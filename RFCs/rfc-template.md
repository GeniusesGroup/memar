---
Title: "RFC Template Specification"
Status: Proposed
Start Date: 2026-06-21
RFC Number: 495000
Applied to: []
Related RFCs:
    - Title: "Dependency Resolution via File URI and Companion Manifest"
      URI: "./khayyam-dependency_resolution.md"
      Reason: "Reference"
      Explanation: "This specification's use of URI for contributor identity follows the same File URI approach RFC already established for dependency resolution."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Directed every revision", "Resolved merge-numbering and collision-resolution rules", "Resolved the Contribution-to-Task decision", "Caught multiple front-matter inconsistencies"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Drafted and revised the specification across multiple rounds", "Proposed the topic-first Reference-level structure and Discussion section", "Migrated Contributors to Task-based tracking"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Works: ["Restructured an earlier revision's section layout", "Applied the pre-Final merging and contributor-preservation rules"]
        URI: ""
---

# RFC Template Specification
A [Request for Comments (RFC)](https://en.wikipedia.org/wiki/Request_for_Comments) is a publication in a series from the principal technical development. This document specifies the canonical template every RFC produced under Geniuses Group must follow.

## Summary
To write a new RFC: copy the template, fill in the front matter, and write the body in the order below — [Guide-level explanation](#guide-level-explanation) walks through exactly how, and is all that's needed for an ordinary RFC. [Reference-level explanation](#reference-level-explanation) is the full, authoritative definition of every field and section, organized by topic; consult it for edge cases or when revisiting why a rule exists, not as a requirement for writing a typical RFC. [Discussion](#discussion-4) holds the reasoning behind this specification's own design and is never required reading to write an RFC.

## Motivation
The real motivation for this specification is not specific to any one project — it is to give every RFC produced across Geniuses Group's projects a single, predictable structure, so a reader or an AI assistant who has read one RFC already knows where to find anything in another, regardless of which project it belongs to.

A secondary, practical motivation is that reviewing a real RFC written under an earlier version of this template, [protocol.md](https://github.com/GeniusesGroup/memar/blob/2cb39b5eeb3a0eddd5bc1bfe132193068dea768b/RFCs/protocol.md), showed a concrete cost of not having that structure: content about a single sub-topic was scattered across as many as six different top-level sections, making it hard to find or revise everything relevant to it. The topic-first [Reference-level explanation](#reference-level-explanation) structure exists to fix that.

## Guide-level explanation
When starting a new RFC:

1. Copy the template from [The Template](#the-template) below into a new file named `<short-descriptive-slug>.md` — no number, no domain prefix, just a short, hyphenated, human-readable slug derived from the Title.
2. Set `RFC Number` to the current UTC hour-count, and never change it again. On Linux/macOS: `echo $(( $(date -u +%s) / 3600 ))`. On Windows PowerShell: `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`. On any platform with Python: `python3 -c "import time; print(int(time.time()//3600))"`.
3. Fill in the rest of the front matter:
   - `Title`: short, quoted, unique.
   - `Status`: start at `Draft`.
   - `Start Date`: today's date (UTC), matching the moment `RFC Number` was generated.
   - `Applied to`: leave `[]` until the RFC reaches `Final`.
   - `Related RFCs`: leave `[]` if none apply; otherwise one entry per related RFC, with `Reason` one of `Reference`, `Depends_on`, `Depends_for`, `Extends`, `Extends_by`, `Conflicts`, `Superseded`, `Superseded_by`.
   - `Contributors`: one entry per contributor, each with at least one `Tasks` item (`Works` — an array of very short, headline-style strings describing what was done, e.g. `["Initial draft", "Design review"]` — plus optional `URI`). AI contributors also add `Model` and `Effort`.
4. Write the body. `Summary`, `Motivation`, and `Guide-level explanation` stay unified, RFC-wide prose. Under `Reference-level explanation`, split the content into topic subsections (`### {Section title}`); give each topic its own `#### Discussion` that collecting `##### Drawbacks` / `##### Rationale and alternatives` / `##### Prior art` / `##### Unresolved questions` / `##### Future possibilities` / `##### Suggested Naming Conventions` only where that topic genuinely has something to say for it — never as an empty header. If a topic needs finer sub-sections, nest `#### {Sub section title}` under it, with the sibling by `#### Discussion`. Anything that applies to the whole RFC rather than one topic goes in the RFC-wide `## Discussion` section, not into any topic's own bundle.
5. Move `Status` to `Proposed` once discussion converges, and to `Final` once it's reflected in canonical documentation. Nothing before `Final` should be treated as settled by anyone depending on the RFC.

### The Template
This is illustrative, not normative — it shows the shape every RFC starts from, not a rigid enforcement of exactly what must be present. Copy everything below into a new file and replace every placeholder.

```
---
Title: ""
Status: Draft
Start Date: ""
RFC Number: ""
Applied to: []
Related RFCs:
    - Title: ""
      URI: ""
      Reason: ""
      Explanation: ""
Contributors:
  - Name: ""
    URI: ""
    Tasks:
      - Works: []
        URI: ""
---

# RFC Title

## Summary

## Motivation

## Guide-level explanation

## Reference-level explanation

### {Section title}
{Description text}

#### {Sub section title}
{Description text}

#### Discussion

##### Naming Conventions

##### Drawbacks

##### Rationale and alternatives

##### Prior art

##### Unresolved questions

##### Future possibilities

## Discussion

### Naming Conventions

### Drawbacks

### Rationale and alternatives

### Prior art

### Unresolved questions

### Future possibilities

## Change Rationale
```

## Reference-level explanation
*Each subsection below is a topic. A topic's `####` subsections are included only when that topic actually has content for them — an RFC should never contain an empty header. Content that does not belong to any single topic belongs in [Discussion](#discussion-4) instead.*

### File
-  Filenames never contain [RFC Number](#rfc-number).
- **Filename.** `<slug>.md` — short, hyphenated, no number, no domain prefix. Stable once Final.

### Title
A short, unique, human-readable name for the RFC, in double quotes. It is the source of the filename slug. A title change that alters the concept is a new RFC with a new `RFC Number`; a title change that merely rephrases the same concept is a minor revision of the same RFC.

### Status

| Status | Meaning | Applied to | Safe to depend on? |
| --- | --- | --- | --- |
| **Draft** | Direction is not yet settled; real, unresolved questions remain, named in that RFC's own Unresolved questions. | Empty | No |
| **Proposed** | Design discussion reached consensus; ready for final review before being reflected in canonical documentation. | Empty | Not yet — may still be revised during final review |
| **Final** | Reflected in canonical documentation. | Lists exactly where | Yes |
| **Superseded** | Replaced by a newer RFC. See `Superseded by`. | Unchanged from when it was Final | No — depend on the superseding RFC instead |
| **Rejected** | Considered and explicitly not adopted. Kept for the historical record. | Empty | No |

Additional rules:
- `RFC Number` is never reused, regardless of status, including Rejected.
- Moving a Final RFC's substance requires a new, superseding RFC, not an in-place edit.
- A reconsidered Rejected idea becomes a new RFC with its own number, referencing the rejected one via `Related RFCs`.
- `Applied to` reflects canonical-documentation status only, never informal or practical usage. An RFC can be in active, wide practical use while still `Proposed`; that does not change what `Applied to` should contain. (This document is itself an example: in active use as the working template while `Proposed`, with `Applied to` correctly empty.)

#### Discussion

##### Drawbacks
Maintaining this detailed semantics alongside the compact Status table in `README.md` means the two must stay consistent as either evolves. This specification also elaborates obligations (e.g. "Final is safe to depend on") without precisely defining what counts as a correction small enough to apply in place versus a change substantial enough to require a superseding RFC.

##### Rationale and alternatives
- **Leave only the one-line README table, infer detailed obligations informally (rejected)**: informal inference drifts inconsistently across a multi-generational project.
- **Fold this level of detail directly into `README.md` (rejected)**: would keep the README from staying a fast, scannable index, which is the reason this detail was extracted out in the first place.

##### Prior art
Several long-running spec processes separate a short status marker from a fuller definition of what that marker commits readers and implementers to — a pattern that recurs across standards-track processes generally, not something unique here.

##### Unresolved questions
1. What precisely distinguishes a "minor correction" applicable in place to a Final RFC from a change substantial enough to require a superseding RFC?
2. Should there be a formal mechanism keeping this document and the README's compact table synchronized, or is manual vigilance sufficient at the current scale?

### Start Date
The calendar date (`YYYY-MM-DD`, UTC) the RFC file was first drafted. Set once, never changed. Should agree with the date implied by `RFC Number`, since both are meant to be captured at the same moment.

### RFC Number
A UTC unix-time-derived integer, generated once when the file is first drafted, never reused or reassigned. It carries no meaning beyond relative creation order — generating it does not imply approval; that is `Status`'s job.

**Value.** UTC unix time truncated to the hour — `(unix seconds) / 3600` — as a plain decimal integer (e.g. `495317`).

**Generation.** See [Guide-level explanation](#guide-level-explanation) for the per-platform commands.

**Uniqueness and collisions.** Two or more RFCs drafted in the same working session landing in the same hour is expected and normal. Resolve manually today: keep the first RFC's number, give the next one the following hour's value or any other free value. Manual resolution is a stopgap, not the preferred end state (see [Future possibilities](#future-possibilities) below in this topic).

**Retroactive numbering.** Pre-existing RFCs may be assigned an hour-value derived from their recorded `Start Date` if retroactively renumbered. Where several share a `Start Date`, order by reasonable manual judgment — no strict rule imposed.

**Merging before Final.** Two or more `Draft`/`Proposed` RFCs merged into one, without changing overall content, reuse one existing number; no new number is generated, and no `Related RFCs` entries are added pointing to the abandoned ones (they never reached Final). Which number is kept:
- If the merged document keeps one original title unchanged, it uses that RFC's original number.
- If an entirely new title is chosen, the merged document uses the smallest (earliest) of the numbers being merged.

This rule applies only pre-Final; once Final, merging requires a new, superseding RFC per the Status rules.

**Storage representation.** Out of scope here — an implementation detail.

**Lookup.** Full-text search for `RFC Number:`, or the README index (Number, Title, Status).

#### Discussion

##### Drawbacks
The number is no longer purely arbitrary — it now encodes creation order, a deliberate exception to "the number should carry no meaning," justified because creation time is an immutable fact that can't later be "reclassified" the way a domain label can. Collisions at hour granularity are expected regularly during multi-RFC sessions and must currently be resolved manually — a stopgap only, since no tooling exists yet. Retroactive backfilling for RFCs sharing a `Start Date` has no principled ordering signal.

##### Rationale and alternatives
- **Domain-encoded ranges (rejected)**: couples the identifier to a classification that can change, forcing renumbering and broken cross-references.
- **Single incrementing counter at creation (rejected)**: needs a central coordinator to avoid collisions with more than one simultaneous contributor.
- **Single incrementing counter at Final/merge time, à la Rust (considered, not chosen)**: avoids ever numbering unstable content, but doesn't allow assigning identifiers to old, already-existing ideas retroactively the way an hour-derived value does.
- **Second-level unix timestamp (considered, not chosen)**: near-zero collision risk, but a ten-digit number — longer than this project's actual RFC-writing pace needs.
- **Hash of the filename/slug (rejected)**: no content-integrity guarantee, long and non-memorable, solves nothing an hour-based counter doesn't already solve more simply.

##### Prior art
Rust's RFC process assigns no number at drafting; a `0000-` placeholder is used until a pull request exists, at which point the PR's own number becomes the RFC number. Rust's internal design discussion explicitly preferred small, continuous-feeling numbers over sparse or arbitrary ones. IETF RFCs are strictly sequential, centrally assigned, with no domain-based reservation.

##### Unresolved questions
None remaining. The earlier open question (hour- vs. minute-level granularity) was resolved in favor of hour-level.

##### Future possibilities
- A small helper script or shell alias that prints the current hour-value and checks for an existing collision, once the number of contributors or RFCs justifies the tooling investment.
- Replacing manual collision resolution with an algorithmic mechanism is preferable long-term to ad hoc human judgment, regardless of granularity; the specific tooling and workflow for that is not decided here.

### Applied to
An array of file URIs, or the single string `"*"` meaning the RFC applies without limitation — to any project that chooses to use this template, not to one project specifically. A more specific entry is a file URI with an optional fragment, e.g. `["Khayyam.md#control-flow"]`. Empty (`[]`) for `Draft`/`Proposed`/`Rejected`; populated only at `Final`; unchanged from its Final value for `Superseded`.

### Related RFCs
An array of relationship records, each with:
- **Title**: the referenced RFC's `Title`, quoted.
- **URI**: the referenced RFC's URI — typically a relative reference to the file within this repository (e.g. `./dependency-resolution.md`). See [URI](#uri).
- **Reason**: one of `Reference` (cites for context, no structural dependency), `Depends_on` (cannot be implemented/understood without the referenced RFC), `Depends_for` (inverse of `Depends_on`), `Extends` (builds on top of), `Extends_by` (inverse of `Extends`), `Conflicts` (a real, unresolved tension), `Superseded` (this RFC obsoletes the referenced one), `Superseded_by` (the inverse).
- **Explanation**: free text on why the relationship holds.

List order carries no meaning. When an RFC is superseded, both sides update: the older RFC's `Status` becomes `Superseded` with a `Superseded_by` entry pointing forward; the newer RFC adds a `Superseded` entry pointing back.

#### Discussion
##### Rationale and alternatives
An earlier version of this field lacked inverse pairs for `Depends_on`/`Extends`, while `Superseded`/`Superseded_by` already had both directions — an unexplained asymmetry. `Depends_for` and `Extends_by` were added specifically to remove it, so every relationship type is expressible from either side.

##### Unresolved questions
1. The boundary between `Reference` and `Depends_on` is not precisely defined. The current wording above already conflates two things that may not always agree — whether the referenced RFC is needed to *understand* this RFC's text, and whether it's needed to *implement* this RFC correctly — under one definition ("cannot be implemented/understood without..."). A real case can satisfy one without the other: this document's own `Reference` entry for RFC 000014 is understandable and implementable without RFC 000014 at all, since this document's `URI` topic defines its own rules independently — but a different RFC could be fully readable on its own while still being impossible to correctly implement without another RFC's mechanism already existing. A proposed starting criterion for the *understandability* axis — if this RFC's own definitions are unintelligible without reading the target RFC, use `Depends_on`; if the target is merely a pointer to further information and this RFC stands alone without it, use `Reference` — is a reasonable basis, but does not by itself resolve whether an *implementability* axis needs to be tracked separately, or how to classify cases where the two axes disagree. Deferred to a dedicated session rather than resolved here.

### URI
A URI is a string identifier as defined by RFC 3986. Two forms are used throughout this template:
- **Absolute URI**: carries a scheme, e.g. `mailto:omid@geniuses.group`, `https://claude.ai`. Used when the URI must resolve independently of this repository.
- **Relative reference**: a scheme-less reference resolved against a base URI (RFC 3986, Section 5), e.g. `./chat-logs/x.md`. Used for resources local to this repository. This is a first-class, standards-compliant form, not a workaround.

The `file:` scheme (RFC 8089) specifically requires an absolute path, which breaks portability across different clones of the same repository; a scheme-less relative reference is used for local paths instead of `file:` for that reason.

### Field Naming Convention
All front-matter field names use PascalCase (`Name`, `URI`, `Tasks`, `Model`, `Effort`, `Title`, `Status`, `Reason`, etc.), applied uniformly across every field in every RFC. This is distinct from [Suggested Naming Conventions](#body-sections), which is about naming conventions a specific RFC proposes for the types, methods, or files it introduces — not about this template's own field names.

### Internal Cross-References
Any reference within an RFC to another section of the same file must be a real hyperlink (e.g. `[URI](#uri)`), never plain text (e.g. `see URI` or a malformed pseudo-link like `see ###URI`). A broken anchor is easy to spot; a stale plain-text reference is not.

### Contributors
A single array listing every contributor — human, AI, or organization — as one entry. There is no `type` field: an entry with `Model`/`Effort` present is an AI system; one without them is a person or organization. There is no `Contribution` field — every contributor's involvement is recorded as one or more `Tasks` entries instead.

**Required.** Every contributor entry must have at least one `Tasks` entry, and every `Tasks` entry must have at least one item in `Works`. A `Tasks` entry's `URI` is optional — include it when a supporting artifact genuinely exists and is reachable; when it doesn't, `Works` alone (e.g. `["Present for the design discussion"]`) is sufficient.

**Preservation rule.** This applies to every RFC in the project, not only this document. While an RFC's `Status` is not yet `Final`, a contributor may update or extend their own entry across revisions, but must never add to or rewrite another contributor's entry. The one exception: if another contributor's entry describes work that has since been removed or reverted from the document itself, so that entry now describes something no longer present, any contributor may remove that specific stale portion — this is pruning an inaccurate claim, not an editorial rewrite, and still does not permit adding new claims or altering what remains of that entry. Once an RFC reaches `Final`, every contributor entry is frozen and immutable, including from this pruning exception. Whether pruned material should be preserved in `Change Rationale` or is adequately covered by version-control history alone is not settled — see the Unresolved questions under [Discussion](#discussion-4).

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
- **Works length.** Each item must be short and headline-like — a few words, not a sentence or a paragraph. This single field replaces an earlier two-field design (`Titles` plus a separate `Explanation`); that split caused contributors to copy the RFC's own `Title` verbatim into `Titles` instead of describing the specific work done, which the merged, explicitly-short `Works` field is meant to make harder to do by mistake. If real detail is needed beyond a short phrase, put it behind a `URI` (a document, an archived conversation) rather than writing a long entry.
- Entries are not ordered by importance; list order carries no meaning.

#### Discussion
##### Drawbacks
`Works` as free text means no automated tooling can reliably query "who did what" across many RFCs without parsing inconsistent phrasing, at least until there's enough data to justify a fixed vocabulary. Without an explicit `type` field, identifying an AI entry depends on `Model`/`Effort` presence, reliable only as long as no future contributor type exists without a model/effort concept either. A `Model` identifier may later be deprecated or renamed by its provider, leaving an unresolvable historical reference. Where `Tasks` archives should actually be stored is not settled by this field's definition (see Unresolved questions).

##### Rationale and alternatives
- **Keep `Author(s)`/`AI(s)` as two separate arrays (an earlier draft; not chosen)**: duplicates nearly every field and needs a new parallel array for every future contributor category.
- **A single array with an explicit `type` field (an earlier draft; not chosen)**: encoded a distinction that isn't actually guaranteed by category membership — a human entry offers no real guarantee of independent review, so `type` added structure without adding real information.
- **A dedicated `Contribution` field (an earlier draft; not chosen)**: once `Tasks` gained real structure, a separate free-text field became redundant — anything expressible in `Contribution` is expressible as a `Tasks` entry's `Works`, including simple presence with no artifact, since `URI` there is optional.
- **Separate `Titles` and `Explanation` fields within each `Tasks` entry (an earlier draft; not chosen)**: `Titles`' name was too easily confused with the RFC's own top-level `Title` field — in practice, contributors (including an AI contributor) copied the RFC's `Title` verbatim into `Titles` rather than describing the specific work done, defeating the field's purpose. Merging into a single `Works` array of short strings, with a name unrelated to `Title`, removes that specific confusion.
- **`file://` URIs for local references (rejected)**: requires an absolute path per RFC 8089, breaking portability across repository clones; a relative reference achieves the same purpose while remaining standards-compliant.

##### Prior art
This field's use of `URI` for identity follows RFC 000014's use of File URIs for dependency resolution. The CRediT (Contributor Roles Taxonomy) system used by academic journals is a comparable example of structured contributor attribution outside this project — though CRediT uses a fixed, controlled set of role categories, which this specification deliberately does not adopt for `Works`, since a contributor's actual involvement can be broader or more specific than any fixed list allows.

##### Unresolved questions
1. Should `Works` eventually move to a fixed, controlled set of categories, or stay free text indefinitely?
2. Where should archived material referenced by `Tasks` actually be stored, given that keeping it inside this repository was explicitly ruled out as adding unwanted size and clutter?

### Body sections
The body follows the front-matter, as a fixed set of sections in order:

- **Summary**: one self-contained paragraph.
- **Motivation**: the specific problem or friction being solved, RFC-wide — not per-topic.
- **Guide-level explanation**: teach a newcomer; illustrative, not normative; self-contained enough that the reader never has to consult Reference-level explanation for the ordinary case.
- **Reference-level explanation**: the normative section, organized as topic subsections (`### {Section title}`). A topic needing finer sub-sections nests `#### {Sub section title}` under it, with optionally a sibling `#### Discussion` (and `#####` bundles) for anything about the topic as a whole — the same topic/Discussion split repeated one level down, but included only where that topic actually has content for them.
  - **Suggested Naming Conventions**: if a topic introduces a new family of types, methods, or files whose naming isn't already fixed elsewhere, state the suggested convention here, explicitly non-binding — enforcement, if any, is a per-organization Linter configuration choice.
- **Discussion**: the RFC-wide counterpart to the same content, for anything that applies to the whole RFC rather than one topic. Structured as `### Naming Conventions`, `### Drawbacks`, `### Rationale and alternatives`, `### Prior art`, `### Unresolved questions`, `### Future possibilities`.
- **Change Rationale**: why the RFC changed across revisions — kept separate from Discussion, since it is about the document's own history, not a justification of the current design, and accumulates append-only much like `Contributors`.

## Discussion

### Naming Conventions
Not applicable at the RFC-wide level for this document — see [Field Naming Convention](#field-naming-convention) under Reference-level explanation, which is normative rather than a discussion point.

### Drawbacks
Consolidating the template and its field specifications into one document means they can no longer be loaded independently — a reader needing only one field's rules must load the whole document. The document is longer than any of its predecessors, and there is no way to load only part of it into context (mitigated by Guide-level explanation being self-contained for the ordinary case — see Rationale and alternatives).

### Rationale and alternatives
- **Keep the template and field specifications as separate files (rejected)**: required loading multiple files into every RFC-writing session and created an ongoing sync obligation between them.
- **Keep a small, separate copy-paste-ready template file, consolidate only the specs (considered, not chosen)**: still two files to load, still a drift risk. The chosen approach keeps drift risk at zero while keeping the everyday reading burden close to what a small separate template file would have offered.
- **Organize Reference-level explanation by content-type rather than by topic — this document's own earlier structure (superseded)**: reviewing a real RFC produced under that structure (`protocol.md`) showed that content about a single topic ends up scattered across as many as six different top-level sections. The topic-first structure replaces it.
- **Embed the template inline as prose rather than a fenced code block (rejected)**: harder to copy verbatim, harder to visually distinguish from surrounding prose.

### Prior art
The Rust RFC process maintains a single `0000-template.md` and a separate `README.md` describing the process, rather than consolidating the template with per-field specifications — a project-specific choice here, driven by this project's practice of feeding the template plus its specs into AI-assisted chat sessions at every RFC-writing occasion, which makes the loading cost of multiple files more salient than in a typical human-only workflow.

### Unresolved questions
1. Should this consolidated spec itself be split again once the project has enough RFCs that the loading cost of a single long document starts to matter?
2. Is `Change Rationale` needed at all, given that version control already records exactly what changed and when? Kept for now at the top level rather than removed, pending a decision. This is reinforced by a related question raised while refining the `Contributors` preservation rule: whether material pruned from a stale contributor entry should be preserved in `Change Rationale` — if version control already covers that case adequately, it is one more reason `Change Rationale` may be redundant.

### Future possibilities
If tooling is ever built to help produce or check RFCs, it could read this single spec file and walk a contributor through each front-matter field and body section in order, validating values as they're filled in. If a future RFC introduces an additional `Status` value, `Related RFCs` `Reason` value, or `Contributors` field, this specification is where that addition should be documented.

## Change Rationale
- **Initial consolidation.** Consolidated the RFC template and its field specifications into a single specification, motivated by the loading cost of feeding multiple files into every chat session and the drift risk between the template and its specs. A pre-Final merging rule allows related Draft/Proposed RFCs to be consolidated without generating a new RFC number. A contributor preservation rule requires every contributor to add their own entry and forbids modifying others'.
- **Second revision.** Fixed front-matter self-inconsistencies: `Applied to` contained `["*"]` while `Status` was `Proposed`, contradicting the Status table (emptied, with a clarifying rule); `Start Date` had drifted from the date implied by `RFC Number` (corrected). Clarified the Contributor preservation rule governs every RFC, not only this document. Corrected an inaccurate claim in the `Related RFCs` `URI` field description. Replaced vague merge-numbering guidance with an explicit tie-break rule. Generalized collision-resolution guidance away from a specific PR-based mechanism.
- **Third revision.** Replaced the flat content-type-first organization of Reference-level explanation with a topic-first structure after confirming, against a real RFC (`protocol.md`), that content was genuinely scattered across up to six top-level sections. Introduced the RFC-wide `Discussion` section, kept separate from `Change Rationale`. Moved `The Template` into Guide-level explanation. Removed `Contribution` in favor of Task-based tracking, requiring at least one `Tasks` entry per contributor. Shortened and refocused Motivation on a shared structure across Geniuses Group's projects rather than a Memar-specific concern.
- **Fourth revision.** Fixed a malformed internal reference (a plain-text pseudo-link) and added an explicit rule that all internal section references must be real hyperlinks. Removed `Common concepts`, promoting `URI` to its own Reference-level topic. Relocated `Field Naming Convention` from `Discussion` to `Reference-level explanation`, renamed to avoid confusion with the unrelated, topic-specific `Suggested Naming Conventions`, since it is a normative rule rather than a discussion point. Documented the recursive `#### {Sub section title}` / `#### Discussion` pattern for topics needing finer nesting. Rewrote Summary to be action-oriented rather than a field-by-field catalog. Rewrote Guide-level explanation to be self-contained for the ordinary case — inlining the RFC Number generation commands and a front-matter cheat sheet — without forward references to Reference-level explanation. Added an explicit rule that `Tasks` `Explanation` entries should be short and headline-style, not paragraphs, since this document's own earlier `Contributors` entries had grown too long. Refined the `Contributors` preservation rule to allow pruning a stale claim from another contributor's entry (describing work no longer present in the document) while still forbidding edits or additions on their behalf. Shortened this document's own `Contributors` entries accordingly.
- **Fifth revision.** Merged `Tasks`' `Titles` and `Explanation` fields into a single `Works` field — an array of short, headline-style strings — after this document's own `Contributors` list showed the predicted failure mode in practice: every entry had copied the RFC's own `Title` verbatim into `Titles` instead of describing specific work done. Logged an Unresolved question under `Related RFCs` about precisely distinguishing `Depends_on` from `Reference`, including a proposed understandability-based criterion and a noted, unresolved second axis (implementability), deferred to a dedicated future session rather than resolved here.
