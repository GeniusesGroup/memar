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

### Preserved the numeric-evidence safeguard when retiring the research-directory README
- Type: Changed
- Propagates to:
  - content.md: Done — the numeric-claims reference now points to this specification's Findings section.
  - content.changelog.md: Done — both research-status references now point to the distinction between research findings and adopted understanding.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, proposed, applied

#### What changed
- The Findings section explicitly distinguishes numeric estimates from measured results: an inspectable method and supporting evidence are required before a numeric claim may be cited as measured data, regardless of its author's identity.
- The obsolete README in the research directory was removed after preserving its numeric-evidence safeguard and updating all three inbound links. Existing research files remained unchanged at that time; they were deleted 2026-09-23 after their final transfer audit.

#### Considered and not done
- Duplicating the old attribution and adoption rules was unnecessary: Participants and the graduation path into the governing document already cover them. The old permission to abandon research without a formal deprecation process was not transferred because the current lifecycle preserves Complete and Withdrawn records and corrects them by supersession (Super Z — proposed; Omid Hekayati — approved).

---

### Separate a question's origin from a citation
- Time: 2026-10-04T13:27:43Z
- Propagates to:
  - documentation.md: Reference - the rule this section defers to was added in the same session
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed, argued

#### What changed
- `### Methodology` now states that a question's origin is recorded without being cited: attributing where a question came from gives that source no standing and lets it carry no conclusion, and a finding the consulted sources do not support is stated as the inquiry's own reasoning rather than as something those sources establish.
- The section already required the sources consulted to be named and already deferred to the citation rule; what it did not say is what happens when the source that raised the question is one the citation rule would not accept.

#### Considered and not done
- The clause was not placed in `### Participants` (Space Bunny Alpha — argued). That section records the thinking systems who raised questions, not the sources they read, so the question and the source are different items and only the question belongs there.
- No `Evidence` relation was added for an origin, and no requirement was added that a research name the material it read but did not rely on (Space Bunny Alpha — argued). The Methodology already requires the sources consulted to be stated, and a source of no standing is named there by class rather than by name.

#### Deliberation
The new `Source standing` rule in `documentation.md` sends a question's origin to this facet's `Participants` and leaves the consequence unstated here, which left the two documents able to disagree about whether an origin supports a finding (Space Bunny Alpha — argued). The gap was closed on the owner's authorization to complete the propagation the same session rather than leave it open (Omid Hekayati — decided).

---

### The Findings-confidence entry leaves the research handoff; the catalog states where tentativeness lives
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation-research.handoff.md: Done - the entry asking whether Findings need their own confidence vocabulary was removed; Optional Sections -> Findings states that a finding's tentativeness is carried by its own statement (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- The entry asking whether Findings need their own confidence vocabulary, distinct from the Handoff facet's decision confidences, left `## Open Questions`: [documentation-research.md -> Optional Sections -> Findings](./documentation-research.md#findings) places the standing where it is already written - "A finding that is genuinely tentative says so in its own statement - that is content; question-level standing is carried by the question statuses."
- The handoff's *Proposed Next Steps* line naming this decision was left in place (Space Bunny Alpha - argued): its content is not solely this question, since the same line also schedules whether enough accumulated practice exists to begin this facet's paired Practice document.

#### Considered and not done
- A findings-level confidence vocabulary was not added to the body (Space Bunny Alpha - argued). The catalog states where a finding's standing is expressed, and the entry's own trigger - accumulated real researches showing whether wording suffices - had not been reached.

---

### The membership criterion now requires material from outside this project, and three near-misses are named
- Time: 2026-10-07T05:10:00Z
- Type: Changed
- Cited:
  - [Comparison: Memar and Hindsight](./comparisons/hindsight.001.md) - Evidence: two threads it opened that were investigated against this project's own documents only, with no source from outside them.
  - [Comparison: Memar and Tensorus](./comparisons/tensorus.001.md) - Evidence: the sibling thread, merged with the above rather than tracked twice.
- Propagates to:
  - knowledge.handoff.md: Done - the three live threads from the removed record now live there, with what the investigation established recorded so it is not repeated.
  - comparisons/hindsight.001.md: Done - both threads now state their disposition inline.
  - comparisons/tensorus.001.md: Done - its thread states the shared disposition and points at the handoff.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- The Abstract definition of a research gains its third qualifier - conducted with material from outside this project - and the topic [What Qualifies as an Inquiry Worth This Facet](./documentation-research.md#what-qualifies-as-an-inquiry-worth-this-facet) states the criterion as the check a session performs before opening a research file, with the test: if every source consulted is a document of this project, the work is an audit of this project's own record.
- Three near-misses are named with where each belongs instead: an open question written up belongs in the base artifact's handoff; an inventory of what this project's documents already say is an audit whose claims belong in a changelog entry or a handoff; a written record of the reasoning behind a decision already made is decision-shaping context and belongs in that decision's changelog entry.
- Two records written earlier the same day under the looser reading were removed rather than kept: a supersession-inquiry record and a required-fields audit, both conducted entirely against this project's own documents. What the first had established is preserved in [knowledge.handoff.md](./knowledge.handoff.md), where its open threads now live; what the second found - that no required field among the six facet specifications' and CONTRIBUTORS.md's forces an invented value - is recorded as the disposition inside [the Hindsight comparison](./comparisons/hindsight.001.md) where the question was raised.

#### Considered and not done
- **Re-judging the seven research records that predate this criterion** (not taken): documentation-handoff.research.001.md, knowledge.research.001.md and process.research.001.md cite material from outside this project and meet it; documentation-research.md's own record, ramework.research.001.md, knowledge.audit.002.md, process.audit.002.md and 
ule.research.001.md cite none, and would not meet the criterion as now stated. Whether they are re-opened, re-titled, or left as the record of a practice that has since tightened is the owner's ruling, and it is recorded as an open question in [documentation-research.handoff.md](./documentation-research.handoff.md) rather than decided here.
- **A lighter artifact for internal audits** (not taken): an audit has a real home in principle - the changelog entry of the change it produces - and an audit that produces no change has none. Creating a facet for it would add a sixth reader relationship for a category that has appeared twice and produced no change; the criterion above is the cheaper correction.
- **Keeping the two removed records as historical files** (rejected): a file under this name claims an inquiry happened; these two did not, and the diff plus this entry are the record.

---

### Three internal audits re-filed under their own name, and the audit form given a rule
- Time: 2026-10-07T05:45:00Z
- Type: Changed
- Cited:
  - [documentation-research.handoff.md](./documentation-research.handoff.md) - Premise: the open question this entry closes, and the error it corrects.
- Propagates to:
  - framework.audit.001.md: Done - renamed from framework.research.001.md; retitled, with one paragraph stating what the file is.
  - knowledge.audit.002.md: Done - renamed from knowledge.research.002.md on its own Methodology's statement that no external prior art was consulted.
  - process.audit.002.md: Done - renamed from process.research.002.md; its sources were external, its method a survey of this repository.
  - rule.research.001.md: None needed - it meets the criterion and is untouched.
  - framework.changelog.md: Done - three propagation targets and one citation retargeted.
  - knowledge.changelog.md, process.changelog.md, modeling.changelog.md, process.handoff.md, documentation-research.changelog.md, documentation-research.handoff.md, comparisons/spec-kit.001.md, comparisons/tensorus.001.md: Done - inbound links retargeted.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- Three records that consulted only this repository's own documents, or whose method was a survey of them, were renamed from <base>.research.<NNN>.md to <base>.audit.<NNN>.md, retitled, and given one paragraph after the heading stating what the file is, why the facet does not govern it, and why it is kept. Nothing was deleted: each one's findings are cited by the changelog entries that carried them, and deleting a cited record to satisfy a naming rule would trade a false label for a broken reference.
- [What Qualifies as an Inquiry Worth This Facet](./documentation-research.md#what-qualifies-as-an-inquiry-worth-this-facet) gained the audit form as a named case: a file named <base>.audit.<NNN>.md, stating in one paragraph what was checked and against what, carrying no status lifecycle, and owing no companion changelog because the changes it produced are recorded where they landed. Its questions live in the base artifact's handoff, as a research's do.
- An error was corrected rather than inherited. The earlier note in documentation-research.handoff.md named rule.research.001.md as failing the criterion, on the strength of a count of URLs in each record; its sources are the SBVR and Business Rules Group vocabularies and the production-rule literature, cited by name, so it meets the criterion and was left alone. The renames were made only after re-reading each record's own Methodology section - which is the check the criterion asks a session to perform before opening a file, applied to files that already existed.

#### Considered and not done
- **Deleting the three records instead** (rejected): each is cited by changelog entries that carried its findings, and the same rule that forbids a research claiming an inquiry that did not happen would leave a broken reference if the answer were erasure.
- **Re-opening the three as real inquiries with an external source named** (not taken): that is new work rather than a repair, and an inquiry written to satisfy a criterion is the failure mode the criterion exists to catch.
- **Giving the audit form a full specification, as a sixth facet** (rejected): an audit's reader relationship is the reader of a coverage survey, which no facet describes, and the three records were produced once each with no shared procedure to specify. The one-paragraph rule is the whole requirement the evidence supports; whether audits recur is held open in the handoff.
