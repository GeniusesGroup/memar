---
RFC Number: 495003
Title: "Unified Contributor Attribution: Contributor(s)"
Status: Draft
Start Date: 2026-07-04
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: ""
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    task: []
---

## Summary
Replaces the separate `Author(s)` field (and the earlier, not-yet-committed proposal for a parallel `AI(s)` field) with a single `Contributor(s)` array. Each entry has a `uri` identifying the contributor, a free-text `contribution` describing what they actually did or how they were involved (including simple presence in a discussion, not only discrete work product), and an optional `task` list of references to supporting material.

Note on scope: this is the third revision of this idea within the same discussion. The first draft proposed `Author(s)` and `AI(s)` as separate arrays; the second merged them with an explicit `type` field (`person`/`ai`/`organization`) to preserve the human/AI accountability distinction. This version removes `type` again, since it turned out to guarantee nothing real — a listed human contributor may not have actually reviewed the content any more carefully than an AI system did, so the distinction that mattered was never "what kind of entity is this" but "what did this specific entry actually do," which `contribution` already exists to capture. Presence of `model`/`effort` fields is sufficient signal that an entry is an AI system, without a separate field to say so.

## Motivation
Recording who was involved in producing an RFC, and specifically what each of them did, matters for the same reasons already established: AI assistance is already part of how RFCs are produced here, at every level from a small suggestion to drafting an entire document; and a listed human "author" is not automatically a guarantee that the content was independently reviewed — what matters is the actual description of involvement, not a category label.

`uri` as the identity mechanism is consistent with how this project already handles a related problem: RFC 000014, "Dependency Resolution via File URI and Companion Manifest," already resolves dependencies through URIs rather than a bespoke identifier scheme.

## Guide-level explanation

List every contributor — human or AI — as one entry in `Contributor(s)`, describing in `contribution` what that entry actually did, however small or passive that involvement was (including simply being present for a discussion without directly editing the text). There is no separate category field; an entry with `model`/`effort` fields present is an AI system, and an entry without them is a person (or, in the future, an organization).

## Reference-level explanation
```yaml
Contributor(s):
  - name: "My Name"
    uri: "mailto:me@example.org"
    contribution: "Free-text description of involvement, e.g. 'Design direction, critical review, and final wording decisions' or simply 'Present for the design discussion'"
    task: []                            # optional: references to supporting material — see below

  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"            # present only for AI entries — the officially documented model identifier at time of writing, not an informal shorthand
    effort: "extended thinking enabled" # optional, free text — providers' effort/reasoning-level scales differ and may change; not an enforced vocabulary
    contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    task:
      - "./chat-logs/2026-07-04-example.md"
```

Field notes:
- **uri**: required, and must be a genuine absolute URI (`mailto:`, `https://`, etc.) — this field identifies the contributor, not a work artifact, so it should always resolve independently of this repository.
- **model** / **effort**: present only for AI entries. `model` should be the officially documented identifier valid at the time of writing; `effort` is free text.
- **contribution**: required, free text, not a controlled vocabulary at this scale. Covers any level and kind of involvement — origination, drafting, critique, review, translation, or simple presence — at whatever detail is useful.
- **task**: optional array of references to supporting material for this contributor's involvement (an archived conversation, a discussion thread, a document). This can be:
  - an absolute URI for an external resource (`https://...`), or
  - a plain relative reference with no scheme (e.g. `./chat-logs/x.md`) for something local to this repository. This is not a workaround — RFC 3986 explicitly defines relative references as a first-class, standards-compliant form, resolved against a base URI (Section 5). The `file:` scheme specifically (per RFC 8089) requires an absolute path; that is a constraint of that one scheme, not of URIs generally, which is why a scheme-less relative reference is used here instead of `file:` for local paths.
  - Where these archives should actually be stored (this repository, or elsewhere, given the concern that chat-log archives could make this repository unnecessarily large) is a separate, unresolved infrastructure question — not something this RFC's field definition needs to settle.
  - The `task` concept referenced here is expected to eventually connect to a fuller, dedicated model of "Task" as a general work-item primitive, currently being developed separately (see the seed notes in `rfc-task-concept.md`). Until that is settled, `task` here is a lightweight, self-contained reference list and nothing more.
- Entries are not ordered by importance or seniority; list order carries no meaning.

## Drawbacks
- `contribution` as free text (rather than a fixed vocabulary) means no automated tooling can reliably query "who did what kind of work" across many RFCs without also parsing inconsistent natural-language phrasing, at least until there is enough real data to justify a fixed vocabulary.
- Without an explicit `type` field, identifying an AI entry depends on the presence of `model`/`effort`, which is only a reliable signal as long as no future contributor type appears that isn't a person and doesn't have a model/effort concept either (e.g. some future automated tool that isn't itself an "AI model" in this sense) — if that happens, this may need revisiting.
- A `model` identifier recorded in an old RFC may later be deprecated or renamed by its provider, leaving a reference that no longer resolves to anything currently documented.
- The `task` field's ultimate meaning is not fully settled here, since it is expected to connect to a separate, not-yet-designed Task concept; this RFC's definition of `task` may need to change once that concept is finalized.

## Rationale and alternatives
- **Keep `Author(s)` and `AI(s)` as two separate arrays (an earlier draft; not chosen)**: gives the human/AI distinction for free from the array itself, but duplicates nearly every field and needs a new parallel array for every future contributor category.
- **Merge into one array with an explicit `type` field (an earlier draft; not chosen)**: turned out to encode a distinction (accountability by category) that isn't actually guaranteed by category membership — a human `type: person` entry offers no real guarantee of independent review, so the field added structure without adding real information; `contribution` already does the only job that mattered.
- **Call the descriptive field `participation` instead of `contribution` (considered, not chosen)**: `contribution` matches how comparable structured-attribution systems (e.g. the CRediT taxonomy used in academic publishing) already frame this idea; its scope here is defined broadly enough to also cover simple presence, so a separate `participation` field is not needed.
- **Represent local references strictly as `file://` URIs (rejected)**: `file:` specifically requires an absolute path per RFC 8089, which breaks portability across different clones of the same repository; a plain relative reference achieves the same purpose while remaining fully standards-compliant.

## Prior art
RFC 000014 in this same repository already uses File URIs, rather than a bespoke identifier format, to resolve dependencies — this RFC's use of `uri` for contributor identity follows that same established internal pattern.

The CRediT (Contributor Roles Taxonomy) system, used by many academic journals to attribute specific roles to each author of a paper, is an existing example of structured contributor attribution outside this project — though CRediT uses a fixed, controlled set of role categories, which this RFC deliberately does not adopt, since a contributor's actual involvement can be broader or more specific than any fixed category list would allow.

## Unresolved questions
1. Should `contribution` eventually move to a fixed, controlled set of categories, or stay free text indefinitely? Revisit if inconsistent phrasing starts to hinder search once there are many more RFCs and contributors.
2. The `task` field's final semantics depend on the separate Task concept currently being developed (see `rfc-task-concept.md`); this RFC should not be considered fully settled until that dependency is resolved.
3. Where should archived material referenced by `task` actually be stored, given that keeping it inside this repository was explicitly ruled out as adding unwanted size and clutter? Not addressed here.

## Future possibilities
If tooling is ever built to help produce or check RFCs, it could prompt for `Contributor(s)` entries at file-creation time, validate that `uri` values are well-formed, and eventually help identify which older, AI-assisted RFCs are worth re-verification as the AI systems that helped write them improve.
