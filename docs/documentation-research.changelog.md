# Documentation — Research Changelog

## Changelog

### Created the Research facet specification from the owner's requirements
- Time: 2026-09-08T07:51:36Z
- Type: Added
- Cited:
  - [Documentation](./documentation.md) — Depends_on: defines the Facet system this specification extends; registration of the Research facet as the fifth facet there is pending the specification's confirmation.
  - [Documentation — Changelog](./documentation-changelog.md) — Reference: the companion-file pairing and naming rules, the inline-attribution norm, and the open-catalog section pattern this specification follows.
  - [Documentation — Handoff](./documentation-handoff.md) — Reference: the analysis-not-transcription discipline and the controlled-vocabulary approach this specification reuses; the boundary between the two facets is defined in the new specification.
- Propagates to:
  - documentation.md: Done — the Research facet registered as the fifth facet; see the "Registered the Research facet as the fifth facet" entry of [documentation.changelog.md](./documentation.changelog.md).
  - documentation.handoff.md: Done — the Facet growth anticipated-work entry updated to the sixth-facet case.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Created `documentation-research.md` (ID 496903) as the governing specification for the Research facet: a numbered companion artifact (`<base>.research.<NNN>.md`) recording a deliberate inquiry — its questions and goals with explicit standing, its participants and roles, its method and findings, and its conclusion, including negative and inconclusive outcomes (Omid Hekayati — requested, decided the requirement set; Super Z — drafted).
- The specification defines the concept (a deliberate, bounded inquiry examined to be evaluated), its boundaries against the three existing facets, the dot-keyed companion naming with a per-base numeric ordinal, the mandatory core (Table of Contents, Status, Question and Goals, Participants) with controlled status vocabularies, the open catalog of optional sections (Method, Findings, Open Questions, Conclusion, Related Artifacts, Notes), and the lifecycle (mutable while Active, frozen once Complete or Withdrawn, corrected by supersession, no companion changelog or handoff) (Super Z — drafted).
- Created this changelog and the paired handoff carrying the open decisions (Super Z — drafted).
- The owner's first review confirmed the draft overall and directed one change: the optional `Method` section moved into the mandatory core as `Methodology`, named after the Explanation facet's section of the same name — same kind of content (how the work was actually arrived at), but never omissible, because findings without a stated method cannot be audited (Omid Hekayati — decided; Super Z — applied).

#### Deliberation
- The owner stated the requirement set: the question and goals at the file's opening with their standing recorded rather than assumed — including the scope the research covers; the participants and roles — questioner, goal-setter, researcher, and a reviewer who approves or does not approve the writing and may add questions; a table of contents, because research files are expected to grow long (Omid Hekayati — required).
- The owner posed the multiple-research naming question — description in the name or a numeric discriminator — and the numeric ordinal was drafted as the answer, with the description carried by the title and question instead (Omid Hekayati — the question; Super Z — the recommendation, pending the owner's ruling).
- The requirements were mapped onto the existing facet machinery rather than a new identity system: statuses as controlled vocabularies on the Handoff facet's pattern, participants via CONTRIBUTORS.md links and role tags, claim attribution via the changelog's inline-attribution norm (Super Z — designed).
- The facet's necessity was argued from the system's own gaps: a negative result has no changelog entry to live in, an open question retires with its handoff, and the Explanation body excludes process narrative — so an inquiry's record had no home (Super Z — argued).

#### Considered and not done
- **A descriptive slug in the filename** (`lexer.research.tokenization.md`) (rejected in draft, pending the owner's ruling): the description is already carried by the H1 and the question statement; a slug goes stale exactly when an inquiry's scope shifts — the situation the record is built to survive — and renaming to fix it breaks the relative references other documents hold.
- **Parenthesized numbering** (`lexer.research.(001).md`) (rejected in draft): the parentheses carry no meaning the bare ordinal lacks, are hostile to shell quoting, and have no precedent among the project's separators (`.`, `-`, `_`).
- **A bare first file** (`lexer.research.md`) (rejected): it forces the first research's renaming when a second appears, and renaming breaks inbound references; `001` from the start keeps every file's name permanent.
- **Research as an Explanation-facet document** (rejected): an Explanation body excludes open questions and process narrative by the relevance discipline, and its provenance lives in a paired changelog — a research violates both by design, because examining the inquiry's process and standing is its reader relationship.
- **Research as Changelog entries** (rejected): a changelog records what changed in an artifact; an inquiry that concludes "no change warranted" — the negative result this facet exists to preserve — would leave no trace at all.
- **Research as a Handoff variant** (rejected): a handoff is mutable state that retires when the discussion ends; a research is a durable record that persists after completion and can be cited as evidence by later changelog entries.
- **A companion changelog for each research file** (rejected): the file's own statuses and participant record are its live state, and supersession is its correction mechanism — the same recursion stop the other companion facets apply.
- **A paired practice document now** (deferred): unlike the Handoff facet, which consolidated three field-tested practice drafts, no research procedure has accumulated yet; the practice is anticipated work until real researches show the procedure.
