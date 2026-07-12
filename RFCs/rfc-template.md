---
Title: "RFC Template Specification"
Status: Proposed
Start Date: 2026-06-30
RFC Number: 495000
Applied to: ["*"]
Related RFCs: []
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Contribution: "Defined the template structure, reviewed and revised each field specification"
    Tasks: []
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    Tasks: []
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Contribution: "Restructured the document to follow the template's own section layout, consolidated shared field definitions into a Common concepts subsection, cleaned the template block, and applied the pre-Final merging and contributor-preservation rules."
    Tasks: []
---

# RFC Template Specification

A [Request for Comments (RFC)](https://en.wikipedia.org/wiki/Request_for_Comments) is a publication in a series from the principal technical development and standards-setting bodies. This document specifies the canonical template every RFC in the `memar` project must follow, and defines the meaning of every field in that template. The template itself appears in the Reference-level explanation below, and can be copied verbatim from there to start a new RFC.

## Summary
The RFC Template is the canonical starting point for any new RFC in the `memar` project. It consists of a YAML front-matter block — capturing identity (`Title`, `RFC Number`, `Start Date`), classification (`Status`, `Applied to`), cross-references (`Related RFCs`), and attribution (`Contributor(s)`) — followed by a body with a fixed set of prose sections (`Summary`, `Motivation`, `Guide-level explanation`, `Reference-level explanation`, `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities`, and an optional `Change Rationale`). This specification document defines the meaning of every front-matter field, the rules for filling it in, and the intended purpose of each body section, so that any contributor (human or AI) can produce a well-formed RFC by copying the template from the Reference-level explanation and following the guidance here without needing to consult any other file.

## Motivation
Three concerns motivate maintaining a single, consolidated specification of the template:

First, feeding multiple files into every chat session that produced or reviewed an RFC imposed a loading cost, and maintaining the template separately from its field specifications created a risk of drift between the template and its specs as either evolved. Consolidating the template and its field specifications into one document removes both problems.

Second, the template's front-matter fields have non-obvious rules that a contributor cannot infer from the template alone. `RFC Number` requires a specific generation procedure; `Status` carries specific dependency-worthiness obligations; `Contributor(s)` has a specific structure that distinguishes human from AI entries without a `type` field. Leaving these rules implicit invited inconsistent contributions across a project intended to span multiple generations and contributors.

Third, recording who was involved in producing an RFC, and specifically what each of them did, matters because AI assistance is already part of how RFCs are produced here, at every level from a small suggestion to drafting an entire document; and a listed human "author" is not automatically a guarantee that the content was independently reviewed — what matters is the actual description of involvement, not a category label. The `Contributor(s)` field is designed around this observation, and the `URI` identity mechanism is consistent with how this project already handles a related problem: RFC 000014, "Dependency Resolution via File URI and Companion Manifest," already resolves dependencies through URIs rather than a bespoke identifier scheme.

## Guide-level explanation
When starting a new RFC:

1. Copy the template from the **Reference-level explanation → The Template** subsection below into a new file named `<short-descriptive-slug>.md`. The filename contains no number and no domain prefix — only a short, hyphenated, human-readable slug derived from the Title (e.g. `sRPC-connection-identity.md`, not `001500-sRPC-connection-identity.md`).
2. Generate the `RFC Number` at the time the file is first drafted, using the current UTC time truncated to the hour (see the RFC Number subsection for the exact command). Whoever creates the file generates the number; there is no requirement that it be generated specifically at commit time. Once set, this number never changes again for the lifetime of the RFC — even if the RFC is later rejected, superseded, or the title/slug is revised.
3. Fill in every front-matter field per the rules in the **Reference-level explanation → Front-matter fields** subsections.
4. Replace every placeholder body section with the new RFC's content, following the purpose statement given for each section in the **Reference-level explanation → Body sections** subsection.
5. When reading an RFC, its `Status` field tells you what you may safely do with it. The full semantics of each status value — including which values are safe to depend on — appear in the Status subsection below; the Guide-level rule of thumb is that `Draft` and `Proposed` are not yet safe to depend on, while `Final` is.

## Reference-level explanation

### The Template

Copy everything inside the fenced block below — starting from the `---` front-matter delimiter through the end of the `## Change Rationale` section — into a new file to start a new RFC. Replace every placeholder value and section body with that RFC's content. Refer to the field-specific subsections that follow for detailed guidance on each front-matter field.

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
Contributor(s):
  - Name: ""
    URI: ""
    Contribution: ""
    Tasks: 
      - Titles: []
        URI: ""
        Explanation: ""
---

# RFC Title

## Summary

## Motivation

## Guide-level explanation

## Reference-level explanation

### Suggested Naming Conventions

## Drawbacks

## Rationale and alternatives

## Prior art

## Unresolved questions

## Future possibilities

## Change Rationale
```

### Common concepts

Several front-matter fields share concepts that are defined once here and referenced from each field-specific subsection below. A field-specific subsection only restates a concept when it adds a field-specific constraint on top of the common definition.

**URI**. A URI is a string identifier as defined by RFC 3986. Two forms are used in this template:
- **Absolute URI**: carries a scheme, e.g. `mailto:omid@geniuses.group`, `https://claude.ai`. Used when the URI must resolve independently of this repository.
- **Relative reference**: a scheme-less reference resolved against a base URI (RFC 3986, Section 5), e.g. `./chat-logs/x.md`. Used for resources local to this repository. RFC 3986 explicitly defines relative references as a first-class, standards-compliant form.

The `file:` scheme (RFC 8089) specifically requires an absolute path, which breaks portability across different clones of the same repository; a scheme-less relative reference is therefore used for local paths instead of `file:`. This is a standards-compliant choice, not a workaround. Whether a given field accepts absolute URIs only, relative references only, or both, is stated in that field's subsection.

**Field naming convention**. All front-matter field names use PascalCase (e.g. `Name`, `URI`, `Contribution`, `Tasks`, `Model`, `Effort`, `Title`, `Status`, `Reason`). This applies uniformly across all front-matter fields and is not restated in each field's subsection.

**Cross-reference vocabulary**. The `Related RFCs` field's `Reason` value uses a controlled vocabulary: `Reference`, `Depends_on`, `Depends_for`, `Extends`, `Extends_by`, `Conflicts`, `Superseded`, `Superseded_by`. The same vocabulary is used in prose throughout this document when describing how RFCs relate to each other; the meaning of each value is defined once in the Related RFCs subsection and not restated elsewhere.

### Front-matter fields

#### Title

The `Title` field is a short, unique, human-readable name for the RFC, enclosed in double quotes (e.g. `"RFC Numbering Scheme"`). It is the source of the filename slug and the primary identifier humans use when referring to the RFC in prose. A title change that alters the concept is treated as a new RFC with its own new `RFC Number`; a title change that merely rephrases the same concept is treated as a minor revision of the same RFC.

#### Status

The `Status` field tells a reader not just "where the RFC is in the process" but specifically what they may safely do with it. The README's Status table is intentionally compact for quick scanning, but deciding whether to set `Depends_on` or `Extends` on another RFC, or whether to treat its content as settled enough to build on, needs a sharper answer than a single line can give — for example, exactly what a Proposed RFC's Status implies about the chance it still changes before Final, or what obligation (if any) attaches once an RFC reaches Final. Leaving those obligations implicit invites different contributors, over a multi-generational timeline, to infer them inconsistently.

The five allowed values, with their full meaning:

| Status         | Meaning                                                                                                                                           | Applied to                       | Safe to depend on?                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------- |
| **Draft**      | Direction is not yet settled; real, unresolved questions remain. Each Draft RFC's own "Unresolved questions" section states exactly what is open. | Empty                            | No                                                 |
| **Proposed**   | Design discussion reached consensus; ready for final review before being reflected in canonical documentation.                                    | Empty                            | Not yet — may still be revised during final review |
| **Final**      | Reflected in canonical documentation.                                                                                                             | Lists exactly where              | Yes                                                |
| **Superseded** | Replaced by a newer RFC. See `Superseded by`.                                                                                                     | Unchanged from when it was Final | No — depend on the superseding RFC instead         |
| **Rejected**   | Considered and explicitly not adopted. Kept for the historical record.                                                                            | Empty                            | No                                                 |

Additional rules that apply regardless of which value is set:

- `RFC Number` is never reused, regardless of status, including Rejected.
- Moving a Final RFC's substance requires a new, superseding RFC — not an in-place edit of the Final RFC's design. What counts as a substance-level change versus a minor correction (e.g. a typo, or a genuinely ambiguous sentence) that can be fixed in place is not defined by this specification (see Unresolved questions).
- If circumstances change enough that a Rejected idea deserves reconsideration, that is a new RFC with its own number, referencing the rejected one via `Related RFCs`, rather than reviving the old one in place.

**Status-specific drawbacks and alternatives.** Maintaining a second document describing Status semantics alongside the compact table in `README.md` means the two must stay consistent as either evolves, which is an ongoing (if currently small) maintenance obligation, not a one-time cost. This specification also elaborates obligations (e.g. "Final is safe to depend on") that were previously left implicit; if a Final RFC needs a genuine correction that falls short of a new design direction, this specification does not define the exact procedure for that — it only distinguishes "correction" from "supersession" in principle, not in a way precise enough to remove judgment calls. The alternative of leaving only the one-line table and letting detailed obligations be inferred informally was rejected because informal inference tends to drift inconsistently across a project expected to span multiple generations and contributors. The alternative of folding this level of detail directly into `README.md` was rejected because it would keep the README from staying a fast, scannable index, which was the stated reason for extracting this content out in the first place.

**Status-specific prior art.** Several long-running spec processes separate a short status marker from a fuller definition of what that marker commits readers and implementers to — for instance, the distinction between an RFC's short status line and the fuller governing document that defines what each status level actually means for implementers is a pattern that recurs across standards-track processes, not something unique to this project.

**Status-specific unresolved questions.**
1. What precisely distinguishes a "minor correction" that can be applied in place to a Final RFC from a change substantial enough to require a superseding RFC?
2. Should there be a formal mechanism to keep this document and the README's compact table synchronized as both evolve, or is manual vigilance sufficient at the current scale?

**Status-specific future possibilities.** If a future RFC introduces an additional status value (for example, something between Proposed and Final for "accepted in principle, pending a specific dependency"), this document is where that value's semantics should be added.

#### Start Date

The `Start Date` field is the calendar date (in `YYYY-MM-DD` form, UTC) on which the RFC file was first drafted. It is set once at file creation and never changed afterward, even if the RFC is later revised, rejected, or superseded. Together with `RFC Number`, it provides a secondary chronological signal: `RFC Number` carries hour-level precision, while `Start Date` carries human-readable date-level precision that is more convenient for prose references ("the RFC started on 2026-07-04"). For pre-existing RFCs retroactively renumbered under the scheme described in the RFC Number subsection, `Start Date` is also the fallback signal used to derive a reasonable hour-value when no hour-level creation time was originally recorded.

#### RFC Number

`RFC Number` is a UTC unix-time-derived integer, generated once when the RFC file is first drafted, and never reused or reassigned afterward. It carries no meaning about domain, subsystem, or importance — only relative creation order. Generating the number does not imply the RFC is approved, ready, or stable; that is the job of the `Status` field, entirely independent of the number. Filenames do not contain the number; they contain only a short, human-readable, hyphenated slug derived from the Title. The number lives solely in the `RFC Number` front-matter field and is looked up via full-text search or the README index, not via the filename or directory position.

**Value.** UTC unix time truncated to the hour — i.e. `(unix seconds) / 3600`, taken as an integer — written as a plain decimal integer (e.g. `495317`). UTC is mandatory to avoid ambiguity across contributors in different time zones. This keeps the number roughly six digits for the foreseeable future (it does not reach seven digits until roughly the year 3110), close in length to the numbers already in use in the RFCs folder today.

**Generation.** Any command that yields this value is acceptable; this specification does not mandate a specific tool, only that the method be simple and available without special setup. Known-working examples per platform:
- **Linux / macOS (bash or zsh)**: `echo $(( $(date -u +%s) / 3600 ))` — works as-is on both, since macOS's built-in `date` also supports `%s`.
- **Windows (PowerShell)**: `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`
- **Any platform with Python installed** (a convenient fallback if the above are inconvenient): `python3 -c "import time; print(int(time.time()//3600))"`

**Uniqueness and collisions.** Because the unit is an hour rather than a second, it is expected and normal — not a rare edge case — for two or more RFCs drafted in the same working session to land in the same hour (this has already happened in practice: the four Chapar RFCs were produced in a single session). When this happens, resolve it manually and simply: keep the first RFC's number as generated, and give the next one the following hour's value (or any other free value), regardless of whether that hour has actually passed yet. No sub-hour precision or automated tie-breaking is defined.

**Filename.** `<slug>.md`, where slug is a short, hyphenated, lowercase-or-natural-case rendering of the Title, with no number and no domain prefix. The slug is expected to remain stable once the RFC reaches Final status, consistent with the existing rule that a meaningful rename constitutes a new RFC.

**Retroactive numbering for pre-existing RFCs.** RFCs written before this scheme was adopted may be assigned an hour-value derived from their recorded `Start Date` (e.g. midnight UTC of that date) if and when they are retroactively renumbered. Where multiple pre-existing RFCs share the same `Start Date`, order them by reasonable, manual judgment (e.g. their current legacy number) — no strict formal rule is imposed for this.

**Merging before Final.** When two or more RFCs in `Draft` or `Proposed` status are merged into a single RFC without changing the overall content and details — typically to reduce cognitive load by consolidating related material — the merged document reuses one of the existing RFC numbers (Usually the one others merged into it); no new number is generated, and the other numbers are abandoned (they never reached `Final`, so they need not remain in the historical record). The merged document does not add `Related RFCs` entries pointing to the now-merged RFCs: since none of them reached `Final`, there is no need to reference the old structure, and doing so would only add noise. This rule applies only to merges that happen before any of the involved RFCs reaches `Final`; once an RFC is `Final`, merging its substance into another RFC requires a new, superseding RFC with its own new number, per the rules in the Status subsection.

**Storage representation.** Out of scope for this specification. How this number is represented in code (integer width, signedness, etc.) is an implementation detail for whichever system needs to store or process it, not a constraint imposed here.

**Lookup.** Because the number is not in the filename, discovery relies on (a) full-text search for the `RFC Number:` field, and (b) the README index table, which lists Number, Title, and Status.

**Numbering-specific motivation.** Three separate problems, discovered across earlier attempts at this project, motivate this numbering scheme:
1. **Domain-encoded ranges create coupling.** An earlier informal scheme reserved number ranges per domain (e.g. 1–999 for Khayyam). This tied a supposedly permanent identifier to a classification that can itself change over time (e.g. deciding the standard library should be its own domain, separate from Khayyam). Any such reclassification would force renumbering, and renumbering breaks every existing cross-reference (`Depends_on`, `Extends`, `Supersedes`) across the whole RFC graph.
2. **A single incrementing counter needs a coordinator.** A project intended to span multiple generations and, potentially, multiple contributors working without constant synchronization cannot safely rely on a single "next number" counter without some registration authority.
3. **Encoding domain or filename content into the number is redundant with, and weaker than, other fields.** `Start Date` already records chronology explicitly; a domain field (if one exists) already records classification explicitly. The number does not need to duplicate either.

**Numbering-specific drawbacks.** The number is no longer purely arbitrary — it now encodes creation order, which is a form of meaning. This is a deliberate exception to the earlier "the number should carry no meaning" principle, justified because creation time is an immutable historical fact and cannot later be "reclassified" the way a domain label can. Collisions at hour granularity are expected to occur regularly during multi-RFC working sessions, not just in rare theoretical cases, and must be resolved by a human each time rather than automatically, or can be resolved by an automated script run in the related PR (Pull Request). Retroactive backfilling for pre-existing RFCs sharing the same `Start Date` has no principled ordering signal (only date-level, not hour-level, precision is actually recorded for them), so their relative order among each other will be a manual judgment call rather than a historically exact reconstruction.

**Numbering-specific rationale and alternatives.**
- **Domain-encoded ranges (rejected)**: couples the identifier to a classification that can change, forcing renumbering and broken cross-references when it does.
- **Single incrementing counter, assigned at creation (rejected)**: requires a central coordinator to avoid collisions in any scenario with more than one simultaneous contributor.
- **Single incrementing counter, assigned only at "Final" / merge time (a leading alternative, not chosen here)**: this is the approach used by the Rust RFC process (see Prior art) — files carry a `0000-` placeholder until a natural, already-unique event (the pull request number) is available, and are renamed only then. This avoids the coordination problem without needing timestamps, and never assigns a number to unstable Draft content. It was not chosen here because a number that exists from the moment an RFC is first drafted was preferred, including so that very old, already-existing ideas could in principle be assigned identifiers retroactively based on when they were actually conceived.
- **Second-level unix timestamp (considered, not chosen)**: minimizes collisions almost entirely but produces a ten-digit number, noticeably longer than the numbers currently in use, for a benefit (near-zero collision risk) that this project's actual RFC-writing pace does not need.
- **Hash of the filename/slug (rejected)**: does not provide content-integrity guarantees (the underlying content can still change after the hash is fixed, since the hash is computed from the name, not the content), produces a long, non-memorable identifier, and does not solve any problem that an hour-based counter does not already solve more simply.

**Numbering-specific prior art.** The Rust RFC process assigns no number when an RFC is first drafted; the file is created with a `0000-` placeholder, and the RFC's number is set only once a pull request exists, using that pull request's own number, at which point the file is renamed. Rust's own internal design discussion around this scheme explicitly considered and rejected using something other than a small, continuous-feeling number, on the grounds that continuous small numbers are more attractive to work with than sparse or arbitrary ones, even though using the PR number leaves gaps. IETF RFCs are also strictly sequential and assigned by a central RFC Editor, with no domain-based range reservation; the number denotes only publication order, not subject matter.

**Numbering-specific unresolved questions.** None remaining. The one open question from the earlier draft — whether to use hour- or minute-level granularity — was resolved during discussion: hour-level granularity is adopted.

**Numbering-specific future possibilities.**
- A small helper script or shell alias that prints the current hour-value and optionally checks the RFCs folder for an existing collision before a new file is created, once the number of contributors or RFCs justifies the tooling investment.
- If the pace of RFC production, or the number of concurrent contributors, grows enough that hour-level collisions become frequent and burdensome — rather than the occasional same-session overlap seen so far — minute-level granularity should be reconsidered. This is not expected in the near term but is worth revisiting if the project's contributor base grows, since manual, in-person resolution of a collision assumes the colliding authors become aware of each other at the point of merging, which holds less reliably once more than one person is producing RFCs independently and asynchronously. As said earlier, it can also be resolved by an automated script run in the related PR (Pull Request).

#### Applied to

The `Applied to` field is an array of file URIs (or the single string `"*"`) indicating where the RFC's design has been reflected in canonical documentation. The value `"*"` means the RFC applies to every RFC in `memar` (typically used by meta-RFCs like this one). A more specific entry is a file URI with an optional fragment, e.g. `["Khayyam.md#control-flow"]`. The field is left empty (`[]`) for RFCs in `Draft` or `Proposed` status — their design has not yet been reflected anywhere — and is populated only when the RFC reaches `Final`. For `Superseded` RFCs, the value is left unchanged from when the RFC was Final (it still records where the now-superseded design used to live). For `Rejected` RFCs, the value is empty (`[]`), since the design was never adopted.

#### Related RFCs

The `Related RFCs` field is an array of objects, each describing a relationship between this RFC and another RFC. Each entry has four fields:

- **Title**: the `Title` of the referenced RFC, in double quotes.
- **URI**: the URI of the referenced RFC. For RFCs in this repository, this is typically a relative reference to the RFC file (e.g. `./rfc-template.md`) or empty `""` until the URI scheme for RFCs is settled. See **Common concepts** for the URI format rules.
- **Reason**: one of the controlled-vocabulary values defined in **Common concepts** under "Cross-reference vocabulary". The meaning of each value:
  - `Reference` — cites the other RFC for context, with no structural dependency.
  - `Depends_on` — this RFC cannot be implemented or understood without the referenced RFC.
  - `Depends_for` — the inverse of `Depends_on`; the referenced RFC depends on this one.
  - `Extends` — this RFC builds on top of the referenced RFC.
  - `Extends_by` — the inverse of `Extends`; the referenced RFC extends this one.
  - `Conflicts` — left non-empty only if a real, still-unresolved tension exists between the two RFCs.
  - `Superseded` — this RFC makes the referenced RFC obsolete.
  - `Superseded_by` — this RFC is made obsolete by the referenced RFC.
- **Explanation**: a free-text description of why the relationship holds.

Entries are not ordered by importance; list order carries no meaning. When an RFC is superseded by a newer one, the older RFC's `Status` becomes `Superseded` and a `Related RFCs` entry with `Reason: Superseded_by` is added pointing to the newer RFC; correspondingly, the newer RFC adds an entry with `Reason: Superseded` pointing back to the older one.

#### Contributor(s)

The `Contributor(s)` field is a single array that lists every contributor — human or AI — as one entry. There is no separate `Author(s)` or `AI(s)` array, and no `type` field distinguishing person from AI; an entry with `Model`/`Effort` fields present is an AI system, and an entry without them is a person (or, in the future, an organization). Each entry has a `URI` identifying the contributor (see **Common concepts** for the URI format rules; this field must be an absolute URI, since it identifies the contributor independently of this repository), a free-text `Contribution` describing what they actually did or how they were involved (including simple presence in a discussion, not only discrete work product), and an optional `Tasks` list of task entries (each with a `Titles` array, a `URI`, and an `Explanation`).

**Contributor preservation rule.** Every human or AI that modifies this file MUST add a new entry to the `Contributor(s)` array describing their own involvement in that revision, and MUST NOT delete or modify any existing contributor entry. This rule ensures the attribution record accumulates over the RFC's lifetime and is never rewritten by later revisions.

**Note on scope and history.** This is the third revision of this idea within the same discussion. The first draft proposed `Author(s)` and `AI(s)` as separate arrays; the second merged them with an explicit `type` field (`person`/`ai`/`organization`) to preserve the human/AI accountability distinction. This version removes `type` again, since it turned out to guarantee nothing real — a listed human contributor may not have actually reviewed the content any more carefully than an AI system did, so the distinction that mattered was never "what kind of entity is this" but "what did this specific entry actually do," which `Contribution` already exists to capture. Presence of `Model`/`Effort` fields is sufficient signal that an entry is an AI system, without a separate field to say so.

**Reference example.**

```yaml
Contributor(s):
  - Name: "My Name"
    URI: "mailto:me@example.org"
    Contribution: "Free-text description of involvement, e.g. 'Design direction, critical review, and final wording decisions' or simply 'Present for the design discussion'"
    Tasks: []                            # optional: task entries — see below

  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"            # present only for AI entries — the officially documented model identifier at time of writing, not an informal shorthand
    Effort: "extended thinking enabled" # optional, free text — providers' effort/reasoning-level scales differ and may change; not an enforced vocabulary
    Contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    Tasks:
      - Titles: ["Model financial account"]  # e.g. task titles
        URI: "./chat-logs/2026-07-04-example.md"  # Task URI such as a chat share URL, issue URL, or local file reference
        Explanation: "Archived conversation showing the initial drafting and revision of the financial account model"
```

**Field notes.**
- **URI**: required, and must be an absolute URI (see **Common concepts**) — this field identifies the contributor, not a work artifact, so it should always resolve independently of this repository.
- **Model** / **Effort**: present only for AI entries. `Model` should be the officially documented identifier valid at the time of writing; `Effort` is free text. Providers' effort/reasoning-level scales differ and may change; `Effort` is not an enforced vocabulary.
- **Contribution**: required, free text, not a controlled vocabulary at this scale. Covers any level and kind of involvement — origination, drafting, critique, review, translation, or simple presence — at whatever detail is useful.
- **Tasks**: optional array of task entries. Each entry is an object with three fields:
  - **Titles**: an array of short task title strings (e.g. `Model financial account`).
  - **URI**: a URI identifying the task or its supporting material. See **Common concepts** for the URI format rules; both absolute and relative-reference forms are allowed here.
  - **Explanation**: free-text description of the task and how it relates to this contributor's involvement.
  - Where these archives should actually be stored (this repository, or elsewhere, given the concern that chat-log archives could make this repository unnecessarily large) is a separate, unresolved infrastructure question — not something this field definition needs to settle.
  - The `Tasks` concept referenced here is expected to eventually connect to a fuller, dedicated model of "Task" as a general work-item primitive.
- Entries are not ordered by importance or seniority; list order carries no meaning.

**Contributor-specific drawbacks.**
- `Contribution` as free text (rather than a fixed vocabulary) means no automated tooling can reliably query "who did what kind of work" across many RFCs without also parsing inconsistent natural-language phrasing, at least until there is enough real data to justify a fixed vocabulary.
- Without an explicit `type` field, identifying an AI entry depends on the presence of `Model`/`Effort`, which is only a reliable signal as long as no future contributor type appears that isn't a person and doesn't have a model/effort concept either (e.g. some future automated tool that isn't itself an "AI model" in this sense) — if that happens, this may need revisiting.
- A `Model` identifier recorded in an old RFC may later be deprecated or renamed by its provider, leaving a reference that no longer resolves to anything currently documented.
- The `Tasks` field's ultimate meaning is not fully settled here, since it is expected to connect to a separate, not-yet-designed Task concept; this field's definition of `Tasks` may need to change once that concept is finalized.

**Contributor-specific rationale and alternatives.**
- **Keep `Author(s)` and `AI(s)` as two separate arrays (an earlier draft; not chosen)**: gives the human/AI distinction for free from the array itself, but duplicates nearly every field and needs a new parallel array for every future contributor category.
- **Merge into one array with an explicit `type` field (an earlier draft; not chosen)**: turned out to encode a distinction (accountability by category) that isn't actually guaranteed by category membership — a human `type: person` entry offers no real guarantee of independent review, so the field added structure without adding real information; `Contribution` already does the only job that mattered.
- **Call the descriptive field `participation` instead of `Contribution` (considered, not chosen)**: `Contribution` matches how comparable structured-attribution systems (e.g. the CRediT taxonomy used in academic publishing) already frame this idea; its scope here is defined broadly enough to also cover simple presence, so a separate `participation` field is not needed.
- **Represent local references strictly as `file://` URIs (rejected)**: see **Common concepts** for why `file:` is not used for local paths in this template.

**Contributor-specific prior art.** The use of `URI` for contributor identity follows the established internal pattern already described in the Motivation section (RFC 000014's use of File URIs for dependency resolution). The CRediT (Contributor Roles Taxonomy) system, used by many academic journals to attribute specific roles to each author of a paper, is an existing example of structured contributor attribution outside this project — though CRediT uses a fixed, controlled set of role categories, which this specification deliberately does not adopt, since a contributor's actual involvement can be broader or more specific than any fixed category list would allow.

**Contributor-specific unresolved questions.**
1. Should `Contribution` eventually move to a fixed, controlled set of categories, or stay free text indefinitely? Revisit if inconsistent phrasing starts to hinder search once there are many more RFCs and contributors.
2. Where should archived material referenced by `Tasks` actually be stored, given that keeping it inside this repository was explicitly ruled out as adding unwanted size and clutter? Not addressed here.

**Contributor-specific future possibilities.** If tooling is ever built to help produce or check RFCs, it could prompt for `Contributor(s)` entries at file-creation time, validate that `URI` values are well-formed, and eventually help identify which older, AI-assisted RFCs are worth re-verification as the AI systems that helped write them improve.

### Body sections

The body of an RFC follows the front-matter and consists of a fixed set of prose sections, in this order. Each section has a specific purpose; an RFC that omits a section without good reason is incomplete.

#### Summary
One paragraph explanation of the decision/feature. The Summary is the only section many readers will read in full; it should be self-contained and answer "what does this RFC decide, and why does it matter" without requiring the reader to scroll.

#### Motivation
What problem in software development is this RFC solving? Concrete pain points and use cases. The Motivation section should make the problem vivid enough that a reader who has never felt it can still understand why someone would. Avoid generic statements like "X is important"; instead, name the specific failure mode or friction that motivated this RFC.

#### Guide-level explanation
Explain as if teaching a new developer: introduce the concept, show examples, explain how it changes the way they think and write code. The Guide-level explanation is intentionally less precise than the Reference-level explanation; its job is to give a reader the right mental model before they encounter the formal detail. Code examples here are illustrative, not normative.

#### Reference-level explanation
The technical detail: exact syntax, interaction with other language features, edge cases. This is the normative section — anything stated here is what an implementer or downstream RFC author is expected to follow. If the Reference-level explanation is ambiguous, the RFC is not yet ready for `Proposed` status.

##### Suggested Naming Conventions
If this RFC introduces a new family of types, methods, or files whose naming is not already fixed by another RFC, state the suggested naming convention here (e.g. a required prefix, a suffix pattern, or a file/slug convention). Note explicitly that it is a non-binding convention: enforcement, if any, is a per-organization Linter configuration choice, not a language-level requirement. This subsection is optional; delete it if not applicable.

#### Drawbacks
Honest accounting of the costs of this decision — what gets harder, not just what gets better. The Drawbacks section is what distinguishes an RFC from a marketing document; an RFC with no honest drawbacks section has not been thought through.

#### Rationale and alternatives
- Why is this the best design among alternatives considered?
- What alternatives were rejected, and why?
- What is the impact of *not* doing this?

The Rationale and alternatives section records the design space that was explored, so that a future contributor wondering "why wasn't X done instead" can find the answer here rather than re-deriving it. Alternatives that were considered and rejected are at least as important to record as the chosen design.

#### Prior art
What do other languages/ecosystems do here? What worked, what didn't? The Prior art section grounds the RFC in existing practice and helps a reader calibrate whether the proposed approach is conventional, novel, or contrarian.

#### Unresolved questions
What is still open and intentionally deferred to a future RFC or to tooling? The Unresolved questions section is a contract with the future: anything listed here is explicitly allowed to remain open, and anything not listed here is implicitly claimed to be settled by the rest of the RFC.

#### Future possibilities
Natural extensions or related ideas, out of scope here but worth recording. The Future possibilities section captures the "while we're here, we noticed..." thoughts that would otherwise be lost, so they can seed future RFCs.

#### Change Rationale
Explanation of the fundamental reasons this RFC changed in each revision. The Change Rationale section is most useful for RFCs that went through substantive revisions between drafts; for RFCs that went straight from first draft to Final with no substantive change, this section may be left empty or omitted entirely.

## Drawbacks
- Consolidating the template and its field specifications into a single document means the field specifications can no longer be loaded or referenced independently; a reader who needs only one field's rules must still load the entire document. This is a trade-off between modularity and loading cost.
- The single file is longer than any of its predecessors, and there is no way to load only part of it into context.
- The `Change Rationale` body section's necessity is an open question (see Unresolved questions); whether it duplicates version-control functionality has not been resolved.

## Rationale and alternatives
- **Keep the template and its field specifications as separate files (rejected)**: required loading multiple files into every chat session that produced or reviewed an RFC, and created an ongoing sync obligation between the template and its specs.
- **Keep the template file separate, consolidate only the field specifications into one spec file (considered, not chosen)**: would have preserved the convenience of a small, copy-paste-ready template file, but at the cost of still having two files to load and still risking drift between template and spec. The chosen approach — embedding the template inside the spec — removes that drift risk entirely; the cost (having to copy the template out of a fenced code block inside a longer document) is small and paid once per new RFC.
- **Embed the template inline as prose rather than as a fenced code block (rejected)**: would make the template harder to copy verbatim and harder to visually distinguish from the surrounding specification prose.

## Prior art
The Rust RFC process maintains a single `0000-template.md` file and a separate `README.md` describing the process; it does not consolidate the template with per-field specifications. The approach taken here — embedding the template inside its own specification document — is a project-specific choice driven by the `memar` project's practice of feeding the template plus its companion specs into chat-based AI assistance at every RFC-writing session, which makes the loading cost of multiple files more salient than it would be in a typical human-only workflow.

## Unresolved questions
1. Is the `Change Rationale` body section in the template still needed, or does version control (e.g. Git) make it redundant?
2. Should this consolidated spec itself be split again once the project has enough RFCs that the loading cost of a single long document starts to matter, or is the single-file approach sustainable indefinitely?

## Future possibilities
- If tooling is ever built to help produce or check RFCs, it could read this single spec file and prompt a contributor through each front-matter field and body section in order, validating values (e.g. `RFC Number` is a valid hour-value, `Status` is one of the five allowed values, `URI` fields are well-formed) as the contributor fills them in.
- If a future RFC introduces an additional `Status` value, an additional `Related RFCs` `Reason` value, or an additional contributor-entry field, this specification is where that addition should be documented.
- If the `Change Rationale` section is eventually judged redundant with version control, a future RFC could remove it from the template.

## Change Rationale
This document consolidates the RFC template and its field specifications into a single specification. The consolidation was motivated by the loading cost of feeding multiple files into every chat session that produced or reviewed an RFC, and by the drift risk between the template and its field specifications. The field specifications are presented as subsections of the Reference-level explanation. Field naming and structure use the template's PascalCase convention, and the `Tasks` field is an array of objects with `Titles`, `URI`, and `Explanation` fields. A **Common concepts** subsection centralizes the URI, field-naming, and cross-reference-vocabulary definitions. A pre-Final merging rule allows related Draft or Proposed RFCs to be consolidated without generating a new RFC number or referencing the old structure. A contributor preservation rule requires every human or AI that modifies this file to add their own entry and forbids modifying existing entries.
