# Documentation — Research Changelog

## Changelog

### Created the Research facet specification from the owner's requirements
- Time: 2026-09-08T07:51:36Z
- Type: Added
- Cited:
  - [Documentation](../documentation.md) — Depends_on: defines the Facet system this specification extends; registration of the Research facet as the fifth facet there is pending the specification's confirmation.
  - [Documentation — Changelog](../changelog/changelog.md) — Reference: the companion-file pairing and naming rules, the inline-attribution norm, and the open-catalog section pattern this specification follows.
  - [Documentation — Handoff](../handoff/handoff.md) — Reference: the analysis-not-transcription discipline and the controlled-vocabulary approach this specification reuses; the boundary between the two facets is defined in the new specification.
- Propagates to:
  - documentation.md: Done — the Research facet registered as the fifth facet; see the "Registered the Research facet as the fifth facet" entry of [documentation.changelog.md](../documentation.changelog.md).
  - documentation.handoff.md: Done — the Facet growth anticipated-work entry updated to the sixth-facet case.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, proposed, applied

#### What changed
- The Findings section explicitly distinguishes numeric estimates from measured results: an inspectable method and supporting evidence are required before a numeric claim may be cited as measured data, regardless of its author's identity.
- The obsolete README in the research directory was removed after preserving its numeric-evidence safeguard and updating all three inbound links. Existing research files remained unchanged at that time; they were deleted 2026-09-23 after their final transfer audit.

#### Considered and not done
- Duplicating the old attribution and adoption rules was unnecessary: Participants and the graduation path into the governing document already cover them. The old permission to abandon research without a formal deprecation process was not transferred because the current lifecycle preserves Complete and Withdrawn records and corrects them by supersession (Super Z — proposed; Omid Hekayati — approved).

---

### Separate a question's origin from a citation
- Time: 2026-10-04T13:27:43Z
- Propagates to:
  - documentation.md: Reference - the rule this section defers to was added in the same chat
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - claimed, argued

#### What changed
- `### Methodology` now states that a question's origin is recorded without being cited: attributing where a question came from gives that source no standing and lets it carry no conclusion, and a finding the consulted sources do not support is stated as the inquiry's own reasoning rather than as something those sources establish.
- The section already required the sources consulted to be named and already deferred to the citation rule; what it did not say is what happens when the source that raised the question is one the citation rule would not accept.

#### Considered and not done
- The clause was not placed in `### Participants` (Space Bunny Alpha — argued). That section records the thinking systems who raised questions, not the sources they read, so the question and the source are different items and only the question belongs there.
- No `Evidence` relation was added for an origin, and no requirement was added that a research name the material it read but did not rely on (Space Bunny Alpha — argued). The Methodology already requires the sources consulted to be stated, and a source of no standing is named there by class rather than by name.

#### Deliberation
The new `Source standing` rule in `documentation.md` sends a question's origin to this facet's `Participants` and leaves the consequence unstated here, which left the two documents able to disagree about whether an origin supports a finding (Space Bunny Alpha — argued). The gap was closed on the owner's authorization to complete the propagation the same chat rather than leave it open (Omid Hekayati — decided).

---

### The Findings-confidence entry leaves the research handoff; the catalog states where tentativeness lives
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation-research.handoff.md: Done - the entry asking whether Findings need their own confidence vocabulary was removed; Optional Sections -> Findings states that a finding's tentativeness is carried by its own statement (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- The entry asking whether Findings need their own confidence vocabulary, distinct from the Handoff facet's decision confidences, left `## Open Questions`: [documentation-research.md -> Optional Sections -> Findings](./research.md#findings) places the standing where it is already written - "A finding that is genuinely tentative says so in its own statement - that is content; question-level standing is carried by the question statuses."
- The handoff's *Proposed Next Steps* line naming this decision was left in place (Space Bunny Alpha - argued): its content is not solely this question, since the same line also schedules whether enough accumulated practice exists to begin this facet's paired Practice document.

#### Considered and not done
- A findings-level confidence vocabulary was not added to the body (Space Bunny Alpha - argued). The catalog states where a finding's standing is expressed, and the entry's own trigger - accumulated real researches showing whether wording suffices - had not been reached.

---

### The membership criterion now requires material from outside this project, and three near-misses are named
- Time: 2026-10-07T05:10:00Z
- Type: Changed
- Cited:
  - [Comparison: Memar and Hindsight](../../../../docs/comparisons/hindsight.001.md) - Evidence: two threads it opened that were investigated against this project's own documents only, with no source from outside them.
  - [Comparison: Memar and Tensorus](../../../../docs/comparisons/tensorus.001.md) - Evidence: the sibling thread, merged with the above rather than tracked twice.
- Propagates to:
  - knowledge.handoff.md: Done - the three live threads from the removed record now live there, with what the investigation established recorded so it is not repeated.
  - comparisons/hindsight.001.md: Done - both threads now state their disposition inline.
  - comparisons/tensorus.001.md: Done - its thread states the shared disposition and points at the handoff.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- The Abstract definition of a research gains its third qualifier - conducted with material from outside this project - and the topic [What Qualifies as an Inquiry Worth This Facet](./research.md#what-qualifies-as-an-inquiry-worth-this-facet) states the criterion as the check a session performs before opening a research file, with the test: if every source consulted is a document of this project, the work is an audit of this project's own record.
- Three near-misses are named with where each belongs instead: an open question written up belongs in the base artifact's handoff; an inventory of what this project's documents already say is an audit whose claims belong in a changelog entry or a handoff; a written record of the reasoning behind a decision already made is decision-shaping context and belongs in that decision's changelog entry.
- Two records written earlier the same day under the looser reading were removed rather than kept: a supersession-inquiry record and a required-fields audit, both conducted entirely against this project's own documents. What the first had established is preserved in [knowledge.handoff.md](../../../../modules/knowledge/knowledge.handoff.md), where its open threads now live; what the second found - that no required field among the six facet specifications' and CONTRIBUTORS.md's forces an invented value - is recorded as the disposition inside [the Hindsight comparison](../../../../docs/comparisons/hindsight.001.md) where the question was raised.

#### Considered and not done
- **Re-judging the seven research records that predate this criterion** (not taken): documentation-handoff.research.001.md, knowledge.research.001.md and process.research.001.md cite material from outside this project and meet it; documentation-research.md's own record, ramework.research.001.md, knowledge.changelog.md, process.changelog.md and 
ule.research.001.md cite none, and would not meet the criterion as now stated. Whether they are re-opened, re-titled, or left as the record of a practice that has since tightened is the owner's ruling, and it is recorded as an open question in [documentation-research.handoff.md](./research.handoff.md) rather than decided here.
- **A lighter artifact for internal audits** (not taken): an audit has a real home in principle - the changelog entry of the change it produces - and an audit that produces no change has none. Creating a facet for it would add a sixth reader relationship for a category that has appeared twice and produced no change; the criterion above is the cheaper correction.
- **Keeping the two removed records as historical files** (rejected): a file under this name claims an inquiry happened; these two did not, and the diff plus this entry are the record.

---

### Three internal audits re-filed under their own name, and the audit form given a rule
- Time: 2026-10-07T05:45:00Z
- Type: Changed
- Cited:
  - [documentation-research.handoff.md](./research.handoff.md) - Premise: the open question this entry closes, and the error it corrects.
- Propagates to:
  - framework.audit.001.md: Done - renamed from framework.changelog.md; retitled, with one paragraph stating what the file is.
  - knowledge.changelog.md: Done - renamed from knowledge.changelog.md on its own Methodology's statement that no external prior art was consulted.
  - process.changelog.md: Done - renamed from process.changelog.md; its sources were external, its method a survey of this repository.
  - rule.research.001.md: None needed - it meets the criterion and is untouched.
  - framework.changelog.md: Done - three propagation targets and one citation retargeted.
  - knowledge.changelog.md, process.changelog.md, modeling.changelog.md, process.handoff.md, documentation-research.changelog.md, documentation-research.handoff.md, comparisons/spec-kit.001.md, comparisons/tensorus.001.md: Done - inbound links retargeted.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- Three records that consulted only this repository's own documents, or whose method was a survey of them, were renamed from <base>.research.<NNN>.md to <base>.audit.<NNN>.md, retitled, and given one paragraph after the heading stating what the file is, why the facet does not govern it, and why it is kept. Nothing was deleted: each one's findings are cited by the changelog entries that carried them, and deleting a cited record to satisfy a naming rule would trade a false label for a broken reference.
- [What Qualifies as an Inquiry Worth This Facet](./research.md#what-qualifies-as-an-inquiry-worth-this-facet) gained the audit form as a named case: a file named <base>.audit.<NNN>.md, stating in one paragraph what was checked and against what, carrying no status lifecycle, and owing no companion changelog because the changes it produced are recorded where they landed. Its questions live in the base artifact's handoff, as a research's do.
- An error was corrected rather than inherited. The earlier note in documentation-research.handoff.md named rule.research.001.md as failing the criterion, on the strength of a count of URLs in each record; its sources are the SBVR and Business Rules Group vocabularies and the production-rule literature, cited by name, so it meets the criterion and was left alone. The renames were made only after re-reading each record's own Methodology section - which is the check the criterion asks a session to perform before opening a file, applied to files that already existed.

#### Considered and not done
- **Deleting the three records instead** (rejected): each is cited by changelog entries that carried its findings, and the same rule that forbids a research claiming an inquiry that did not happen would leave a broken reference if the answer were erasure.
- **Re-opening the three as real inquiries with an external source named** (not taken): that is new work rather than a repair, and an inquiry written to satisfy a criterion is the failure mode the criterion exists to catch.
- **Giving the audit form a full specification, as a sixth facet** (rejected): an audit's reader relationship is the reader of a coverage survey, which no facet describes, and the three records were produced once each with no shared procedure to specify. The one-paragraph rule is the whole requirement the evidence supports; whether audits recur is held open in the handoff.

---

### The audit form withdrawn; a survey and a rejected claim are recorded in the changelog instead
- Time: 2026-10-07T06:40:00Z
- Type: Fixed
- Cited:
  - [Documentation — Changelog](../changelog/changelog.md) - Depends_on: the facet that already owns comparative prior-art surveys, and whose membership this entry widens.
- Propagates to:
  - framework.changelog.md: Done - the Go-group claim survey's residue recorded, with Surveyed and Examined and not adopted.
  - knowledge.changelog.md: Done - the placement survey's result recorded; its five open questions moved to knowledge.handoff.md.
  - process.changelog.md: Done - the four-discipline survey's result recorded; its uncarried threads moved to process.handoff.md.
  - documentation-research.handoff.md: Done - the open question narrowed to the one the reversal actually leaves.
  - framework.audit.001.md, knowledge.audit.002.md, process.audit.002.md: Done - removed, their substance carried by the three entries above.
  - documentation-research.md: Done - the audit-form paragraph removed; where such a survey belongs is now stated in the criterion topic as the changelog.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- The audit form is withdrawn. The previous entry introduced <base>.audit.<NNN>.md and this one reverses it, because the facet the form duplicated already existed: [Documentation — Changelog](../changelog/changelog.md) declares comparative prior-art surveys and decision-shaping context to be its own content classes, and every one of the three records had its reasoning in the very entries that carried their findings.
- What was genuinely missing is now stated in the specification that owns it. A new topic, [Changelog membership](../changelog/changelog.md#changelog-membership-what-may-be-recorded-here), holds that an entry records an event bearing on the artifact's state and that the event need not be a change to its text - among them a survey whose negative result is the finding, which is the case no other facet admitted. The boundary is the test each case passes: still to be done is a handoff entry; settled, settled-against, or already held is recorded here. A survey that produced open questions records the survey in the ledger and the questions in the handoffs that own them.
- Two catalog sections were added for it: [Surveyed](../changelog/changelog.md#surveyed), what was checked against what and what the check found, stated so a later chat does not repeat it; and [Examined and not adopted](../changelog/changelog.md#examined-and-not-adopted), material examined and deliberately not carried with its reason - a case that had no home at all, because a rejected claim produces no change to hang from.
- The three records are removed and their residue carried by three entries. The Go-group audit's residue was the largest: twenty-six claim clusters checked against the documents, twelve already carried, eleven becoming open questions in ten handoffs, five categories of claim examined and not adopted, and the deletion condition that let the raw exports be removed. Two artifacts gained handoff files in that chat and the questions remain live there.
- Where such material belongs is now said once, in the criterion topic: an internal survey is recorded in the changelog of the artifact it examines.

#### Considered and not done
- **Renaming the Changelog facet to Audit** (rejected, and the question is the owner's if it returns): "audit" already names the reader relationship this facet serves - a reader auditing how the current state came to be - and would now also name one of its own sections, so the facet would point at its contents rather than at its subject. What the practice actually lacked was membership, not a name; if a rename is ever wanted, History is the accurate generalization, because the facet's subject is how the state came to be whether or not this chat changed it.
- **Registering the audit form in documentation.md instead** (not taken): it would register a second non-facet artifact kind on the strength of three instances whose residue the changelog already had a home for, which is the implicit-convention state the facet system exists to eliminate.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:50:00Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - reviewed

#### What changed
- Reviewed; no change needed. The uncommitted changes to `documentation-research.md` and `documentation-research.handoff.md` are link retargets after the folder moves (`modules/khayyam/` to `bundles/khayyam/`, `protocols/computer/lexer.md` to `modules/computer/lexer.md`). Checked that `bundles/khayyam/khayyam.research.001.md` and `docs/modules/computer/lexer.md` exist, that the example path `docs/modules/computer/lexer.research.001.md` matches the link, and that `memar content check` reports no problem in either file.

---

### The Status values are defined in Documentation
- Time: 2026-10-13T10:43:00Z
- Type: Changed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- The [Status](./research.md#status-mandatory) section now links to [documentation.md → Status](../documentation.md#status) for the four values `Active`, `Paused`, `Complete`, `Withdrawn` and their meanings, and keeps what is specific to a research: Status is a section because a research has no front matter, `Complete` requires every question to carry a final status, `Withdrawn` records its reason, and a superseded research names its successor beneath.
- Why: one Status vocabulary for every document kind, defined once; see [documentation.changelog.md](../documentation.changelog.md).

---

### The Research facet's definition moves here from documentation.md
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - modules/content/documentation/documentation.md: Done (task `20261016-T150928Z-4276`) - the passage this entry moved here no longer stands there.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Reader relationship](./research.md#reader-relationship): the definition `documentation.md` held for this facet moved here — the content examined to evaluate a deliberate inquiry. That a negative result has no other home, the per-base ordinal and the lifecycle (mutable while Active, frozen once Complete or Withdrawn) were already in this specification and were merged, not repeated.
- The sentence that restated the Explanation, Changelog and Handoff relationships now points at their own sections, and says that a relationship none of them answers enters by its own specification.
- Made in task 20261016-T150928Z-4276, finishing answer 6 of the owner's rulings of 2026-10-16: a new facet edits only its own module.

#### Considered and not done
- **Restating the other facets' reader relationships here to contrast this one with them**: each facet's own specification states its relationship, and a restatement is a second place to edit when one changes; this specification points at the other's section instead.

---

### The Status values leave this specification for the type
- Time: 2026-10-17T08:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [./research.md#status-mandatory]: the sentence no longer lists the Status values this kind may take; it names the type `Status` and the way a script asks it (`Status.for_kind`), and keeps its rules.
- Why: the closed set is code in `.agents/scripts/services/status.py`, and a prose list of a closed set is a copy ([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)); [documentation.md → Status](../documentation.md#status) had already dropped its table under the same ruling.
- Made in task 20261016-T194830Z-21416.

---

### The facet's closed lists leave the specification for their types
- Time: 2026-10-17T12:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The question statuses and goal statuses are no longer listed in [Question and Goals](./research.md#question-and-goals-mandatory) (`QuestionStatus`, `GoalStatus`). The sections are typed (`ResearchSection`, with the mandatory core marked); their prose is unchanged.
- Why: the owner ruled on 2026-10-16 that every field a facet declares is a type, and that once typed the prose restating it leaves the document, keeping the reason ([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)); the types are in this facet's `primitive/`.
- Made in task 20261016-T194831Z-4504.
