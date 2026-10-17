# Documentation — Handoff Changelog

## Changelog

### Created the Handoff facet specification; consolidated the three practice documents
- Time: 2026-09-01T13:13:52Z
- Type: Added
- Cited:
  - [Handover](https://en.wikipedia.org/wiki/Handover) — Evidence: the term's established cross-domain usage — telecommunications defines handover/handoff as transferring an ongoing call or session between channels without loss, and its See-also links change-of-shift reporting in healthcare and follow-the-sun development — supporting both the name choice and the claim that the concept is agent-generic rather than AI-specific.
- Propagates to:
  - `documentation-conversation_handoff.practice.md`: Done — absorbed (the practice's trigger lists, confidence vocabulary, decision-with-rationale requirements, nuance-preservation rules, both-sides usage guidance, and metadata conventions) and the file deleted. Superseded by this document and its paired practice.
  - `documentation-conversation_continuity_notes.practice.md`: Done — absorbed (the stub's task list: handoff files between conversations, decision recording, open-question recording, assumption recording — all four now mandated structure) and the file deleted.
  - `documentation-review.practice.md`: Done — absorbed into the paired practice file's graduation step (propose-don't-modify-without-approval; exact-section + replacement-ready English text; the resolve-an-ambiguity test; the five improvement types; the text-quality requirements) and the file deleted. Its per-type markdown proposal templates, output-format wrapper, and detailed review checklists were dropped as over-specified scaffolding — recorded here so the judgment is revisitable rather than silent.
  - [thinking.md](./cognition.md): Done — the boundary note that pointed to the retired `documentation-review.practice.md` now points to [Documentation](./documentation.md) as the documentation system's entry point.
  - `documentation-critique.practice.md`: Done — its "Relation to Other Practices" rows referencing the two retired practices updated to the merged practice.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- Created `documentation-handoff.md` (ID 496741) as the governing specification for the Handoff facet: a `<base>.handoff.md` companion capturing the distilled state of a discussion so a later session — AI, human, or organizational — can resume it (Omid Hekayati — decided; Super Z — drafted).
- The specification defines the concept (state transfer across a session boundary, borrowing the established cross-domain term), its central discipline (analysis, not transcription — three named risks with structural controls: fixed skeleton against selection asymmetry, mandatory confidence vocabulary against analysis-record confusion, required rationale capture against invisible premises), its relationship to the existing facets (no design claims — conclusions graduate into Explanation-facet documents; mutable state, not append-only history), the fixed section skeleton, and the file format (Super Z — drafted).
- Created the paired practice file with the producing, consuming, and placement procedures (Super Z — drafted).
- Absorbed and deleted the three practice documents; the surviving references to them are these provenance records (Omid Hekayati — directed; Super Z — executed).

#### Deliberation
- The consolidation was directed into one base document named `documentation-handoff.md`, dropping the `conversation` qualifier — the `documentation-` prefix already scopes it, and "handoff" is the established cross-domain term (Omid Hekayati — decided).
- The artifact was required to be defined agent-generally — a fully human session is covered by the same artifact, not only AI chat sessions (Omid Hekayati — required).
- The artifact's self-awareness risks — selection asymmetry, analysis-versus-record confusion, invisible premises — were required to be named and structurally controlled rather than left as caveats (Omid Hekayati — required).
- The `.handoff.md` companion suffix was proposed following the `.changelog.md` precedent (Omid Hekayati — proposed).
- The specification and paired practice were drafted, the three risks and their controls structured, and the consolidation executed (Super Z — rewrote).

#### Considered and not done
- **Keep the three practice files separate (rejected by the owner)**: they were overlapping drafts of the same artifact, each informal, none authoritative, and together they suggested workflows (review checklists, proposal templates) whose home is not handoff at all — consolidation replaces three sources of drift with one specification.
- **Fold the handoff content into the Practice facet as a larger practice document (rejected)**: a handoff's primary reader is a session reconstructing discussion state, not an agent executing steps — the reader relationship that defines the Practice facet. The procedural content went to the paired practice file; the state-capture artifact needed its own governing specification.

### Removed the resolved registration question from the base document
- Time: 2026-09-01T14:34:32Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The base document's Unresolved questions had carried the facet-registration question struck through as resolved, after the owner directed registration; the question was removed, the remaining questions renumbered, and the Future possibilities bullet anticipating registration was dropped since registration has occurred (Omid Hekayati — decided; Super Z — rewrote).
- The governing rule: a question whose answer is settled must not remain in the base document at all — the base document carries current state, and its changelog carries the history; the changelog is where "a question was here, and is now settled" is recorded, so the question's existence and resolution are recorded here (Omid Hekayati — decided).
- The resolution event itself is recorded in the "Registered the Handoff facet as the fourth facet" entry of [documentation.changelog.md](./documentation.changelog.md); this entry preserves the fact that the question existed in this document and where its answer came from (Omid Hekayati — the rule; Super Z — recorded).

#### Considered and not done
- **Fold the handoff content into the Changelog facet as a second file kind (rejected)**: a changelog is append-only history consulted to audit the past; a handoff is mutable state consulted to resume work. Append-only state-capture buries the current state under the discussion's own evolution — the exact cost the artifact exists to avoid. The two facets cross-reference instead.

### Body restructured; discussion content relocated per the finalized method
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - documentation-handoff.handoff.md: Created - this specification's open questions and anticipated work moved there.
  - documentation-explanation.md: Done - the method this migration follows was finalized there in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - rewrote, moved

#### What changed
- The handoff facet now explicitly covers the parked-open-question case: the `not the conclusion made permanent` bullet was extended with the survived-question rule and its two exits - graduate through the changelog, or drop through the changelog - keeping base documents' bodies doubt-free while preserving open work (Omid Hekayati - decided; Super Z - written).
- The skeleton's `Open Questions` section gained a sibling, `Anticipated Work`, receiving extensions and growth paths a discussion anticipates but no one has committed to - and the anticipated work a base document records for its future, per the Explanation facet's Relevance discipline (Super Z - applied).
- The specification's own body reformed under the finalized method: topic-level `#### Drawbacks` and document-level `## Drawbacks` replaced by open-catalog sections; rejected-alternative and open-question content moved out (Super Z).
- The `Structure` topic now describes the skeleton as an open catalog of state sections, explicitly aligned with the Explanation facet's Optional Sections model; the former word "fixed" is replaced by "open" (Super Z - applied).

#### Deliberation
- The owner made the routing decision that open questions and anticipated work leave the base document's body for the paired handoff; Super Z applied it (Omid Hekayati - the routing decision; Super Z - applied).
- The owner decided the `Structure` shift from "fixed" to "open", aligning the skeleton with the Explanation facet's Optional Sections model; Super Z applied it (Omid Hekayati - decided; Super Z - applied).
- A final audit found several `Rationale and alternatives`, `Prior art`, and `Unresolved questions` blocks that the earlier passes missed; all are recorded below and in the paired handoff (Super Z - audit and migration).

#### Considered and not done
- Naming the artifact "continuity note" (rejected): describes a hope (that the topic continues) rather than the artifact's function (transferring state across a boundary); "Handoff" names the function with an established, cross-domain word, consistent with the project's preference for established terminology over invented labels. (Omid Hekayati - the naming argument)
- Naming the artifact "conversation note" (rejected): scopes the artifact to AI chat sessions; the need is agent-generic - a fully human working session (a design review, a pair-modeling session, a shift handover) requires exactly the same state transfer. (Omid Hekayati)
- Leaving the handoff as convention without a governing specification (rejected): the pattern was already repeating across real artifacts; leaving it unnamed would reproduce the drift the documentation meta-layer exists to prevent. (Omid Hekayati)
- Free-form structure (rejected): the fixed skeleton is the selection-asymmetry control; a free-form handoff cannot be audited for what it omitted. (Omid Hekayati)
- A machine-readable format (YAML/JSON) instead of Markdown (considered, not chosen): would make handoffs queryable, but the artifact's primary reader is a session that reads prose, and a structured format raises the writing cost at exactly the point (session end) where the writer has least capacity for it. A structured extraction can be added later as tooling. (Super Z)
- Timestamped entries like a changelog (rejected): a handoff's entries are the current state of a discussion, not a history of changes to it - the state is rewritten as the discussion moves, not appended to. (Omid Hekayati)
- Specify a transcript-based handoff (rejected): preserves fidelity but fails the purpose - the next session must re-analyze the full exchange, paying again the cost the handoff existed to avoid, and transcript volume discourages writing the artifact at all. (Super Z)
- Specify only a free-form summary (rejected): minimal effort, but leaves all three distillation risks uncontrolled. (Super Z)
- Use meeting-minutes format as-is (considered, not chosen): minutes capture outcomes and action items but conventionally omit confidence levels, assumption tracking, and rejected-alternative rationale - the three controls this specification makes mandatory; the handoff structure is minutes extended with those controls. (Super Z)
- Extend the Practice facet instead, with a bigger practice document and no new facet (rejected): a practice is followed to accomplish something; a handoff is consulted to resume state - different reader relationships. (Super Z)
- Extend the Changelog facet instead (rejected): append-only history would force every refinement into a new entry, burying current state under the evolution. (Super Z)
- Give each facet an entirely independent naming scheme unconnected to external frameworks (considered, not chosen): the names already state what they mean. (Super Z)

#### Related work
- Telecommunications handover: transfer of an in-progress session between channels or cells without loss - the source of the term and of the requirement that the transfer preserve the session rather than restart it.
- Change-of-shift report in healthcare: structured transfer of patient state between shifts, with its own documented failure literature when done poorly.
- Follow-the-sun development: the same transfer across time zones in software work.
- Meeting minutes and decision logs: the long-established human practice of distilling a discussion into its outcomes - a handoff is their disciplined descendant, with structure added for the risks minutes historically ignore (confidence, assumptions, invisible premises).
- Within AI-assisted development, handoff/context-summary conventions have begun appearing in ecosystem tooling - evidence of the need, though typically free-form and unstructured in exactly the ways the analysis-not-transcription discipline warns against.

#### Considered and not done (from the removed Drawbacks section)
- The facet adds a fourth artifact kind to the documentation system - one more thing a contributor must understand and choose among. It also institutionalizes a writing obligation at session boundaries, where motivation to produce it is lowest; the quality controls make the obligation heavier than the ad-hoc habit it replaces, by design. And the boundary between "handoff" and "early draft of the real document" is a real risk: a discussion that has effectively concluded should graduate into Explanation- and Changelog-facet documents, not persist as a handoff indefinitely - enforcing it requires judgment every time.

#### Decision
The wrapper titles are gone from this specification's body; open questions and anticipated work live in the paired handoff.

### Added the mid-session tangent trigger; qualified the resolved-question move with graduation
- Time: 2026-09-07T21:05:00Z
- Type: Changed
- Propagates to:
  - `.agents/skills/memar/SKILL.md`: Done - the skill carries only the tangent intake trigger (a Working rules bullet pointing to this practice) and, in its *Separation of knowledge* section, the general rule to discover the governing facet from `documentation.md` instead of inventing ad-hoc note formats; the procedure itself stays here, so no information is duplicated across the layers.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) - argued, wrote

#### What changed
- The practice gained a `Mid-Session Tangents` section: a tangent (a request opening a development thread whose context the current session will not otherwise need) is now a mid-session handoff trigger, with the procedure - propose a separate session once, the person's choice final; record the tangent's state into the appropriate handoff immediately; state in one line what was recorded and where; load no more context than recording requires. Clarifying questions and small related edits are explicitly excluded from the definition, so the trigger cannot degrade into nagging.
- The skill carries only the intake trigger and a pointer to this practice, not the procedure.
- Consuming step 4 was qualified: a resolved question stays in Ambiguities Resolved only until its resolution graduates; a graduated item is removed from the handoff, because the specification carries the answer and the changelog carries the record.

#### Deliberation
- The tangent rule was motivated by an observed failure: a documentation-change request raised inside an unrelated session polluted that session's context and the work could not be completed there (Omid Hekayati - the failure report).
- The first draft carried the full tangent procedure in the skill; the owner redirected to a minimal trigger there with the procedure in this practice, so no information is duplicated across the layers (Omid Hekayati - the redirect; Qwen - applied).
- The first version of this entry kept the resolution's explanation in the handoff's Ambiguities Resolved and left the position chronology inside `What changed`; the owner flagged both as violations of the method the same session had just written - graduated content leaves the handoff, and a new writing rule binds the entry that introduces it (Omid Hekayati - the critique; Qwen - accepted and restructured).
- The critique exposed the step 4 ambiguity: "resolved questions move to Ambiguities Resolved" read as permanent retention; the owner directed closing it with the graduation qualifier (Omid Hekayati - decided; Qwen - drafted).

### Graduation rule made explicit for handoff decisions
- Time: 2026-09-08T12:20:10Z
- Type: Changed
- Cited:
  - [Documentation — Research](./documentation-research.md) - Evidence: the real instance that exposed the gap - its handoff's Decisions section held only decisions already graduated into the governing specification and its changelog.
- Propagates to:
  - documentation-handoff.practice.md: Done - the consuming procedure's graduation step now removes the graduated decision from the handoff, and the quality checklist gained the no-graduated-decisions check.
  - documentation-research.handoff.md: Done - its Decisions section removed entirely; every decision in it had graduated into [documentation-research.md](./documentation-research.md) and its changelog.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, critiqued, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - analyzed, rewrote

#### What changed
- The specification's Decisions section now states the graduation boundary directly: a decision lives in the handoff only while it is not yet durably recorded elsewhere; when its rule has landed in the governing document and its changelog records the decision, the entry leaves the handoff - the base document carries the rule and the changelog carries the record (Omid Hekayati - the critique; Super Z - the rule drafted).

#### Deliberation
- The owner read a real handoff's Decisions section, found settled content there, and posed the alternative reading: the handoff is the place for material a future session can still answer or improve, not for decisions taken and finished (Omid Hekayati - critiqued).
- The root check confirmed the reader was not misreading: the specification carried a graduation rule for the handoff as a whole and, since the previous session, an explicit one for resolved questions in the practice's consuming procedure - but the Decisions section itself carried none, so a writer following the skeleton could fill it with graduated decisions while violating no stated section-level rule (Super Z - the analysis; the specification was the defect, not the reading).
- The boundary drawn is graduation, not confidence level: a Decided-but-not-yet-graduated decision is genuine resumable state - the next session must not re-argue it, and it may not yet be written anywhere else - while a graduated one already has its two authoritative homes (Super Z - the extension; the critique itself did not argue this far, so it is recorded as the receiver's extension and stands by the evidence standard).

#### Considered and not done
- Keeping graduated decisions in the handoff as a summary of where the design stands (rejected): the base document carries the rule and the changelog carries the record; a summary copy is guaranteed to drift, and the handoff's Topic & Purpose is the one narrative home for how the discussion stands.
- Fixing only the instance handoff and leaving the specification as it was (rejected): the error was reproducible by the specification as written - any writer following the skeleton could refill Decisions with graduated content; the rule belongs in the specification, the procedure step in the practice, and the instance cleanup follows from both.

---

### Three entries leave the Handoff facet's own handoff; the practice and the companion rule already carry them
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation-handoff.handoff.md: Done - the multi-topic, file-placement, and own-changelog entries were removed; the practice's Placement section and the Research facet's companion rule carry each answer (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- *Multi-topic handoffs* left `## Open Questions`: [documentation-handoff.practice.md -> Producing a Handoff -> Placement](./documentation-handoff.practice.md#placement) requires one handoff per topic - "a multi-topic discussion is split into one handoff per topic so each can resume, conclude, and retire independently".
- *Handoff file placement* left `## Open Questions`: the same Placement section states that handoffs paired with a governed base document live beside it, as `<base>.handoff.md` next to `<base>.md`.
- *Own changelog for long-lived handoffs* left `## Open Questions`: [documentation-research.md -> Lifecycle and Integrity](./documentation-research.md#lifecycle-and-integrity) states the recursion stop the companion facets apply - a research file receives no companion changelog and no companion handoff, "the same recursion stop the other companion facets apply".

#### Considered and not done
- The placement rule was not extended to base artifacts outside `docs/` (Space Bunny Alpha - argued). The Placement section owns that rule, and the entry's own trigger - the first non-`docs` base artifact needing a handoff - has not arrived; revising the section is the work that trigger calls for.
- The no-companion-changelog rule was not restated in this facet's own specification (Space Bunny Alpha - argued). The Research facet states it and names itself the recursion stop the other companion facets apply, so the handoff follows from that statement; a second, facet-specific rule would be the same bound under two homes.

---

### Placement follows File Naming; the conversation-records folder is retired
- Time: 2026-10-05T05:22:56Z
- Type: Fixed
- Propagates to:
  - documentation-handoff.practice.md: Done — the Placement section now defers to [Documentation → File Naming](./documentation.md#file-naming) for both cases and names no folder.
- Cited:
  - [Documentation — Handoff → File Format](./documentation-handoff.md#file-format) - Depends_on: the rule this corrects, stating that a handoff is `<base-filename>.handoff.md` and that its base artifact "is not necessarily a document".
  - [Documentation → File Naming](./documentation.md#file-naming) - Depends_on: the rule this defers to, stating that a model a session leaves beside the documents it read "is working state and takes `<base>.handoff.md` as a Handoff".
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- The Placement section no longer names a location. Both its cases — a handoff paired with a governed base document, and a handoff for a discussion not yet tied to one — now resolve through the single rule that already governs where a base artifact goes, and a handoff whose subject has no folder yet is stated to open that folder rather than to be diverted elsewhere.
- The one-topic-per-file rule is kept, and is now stated as a property of the handoff rather than of a folder.
- The previous entry in this file named the trigger for this work and said it had not arrived. It has now arrived three times: `modules/computer/binding/binding.handoff.md`, `modules/process/construction/construction.handoff.md`, and `modules/process/control-flow/control-flow.handoff.md` are handoffs for base artifacts outside `docs/`, and `modules/khayyam/rules/` had accumulated twenty-one tracked files citing a file inside the conversation-records folder as the `Evidence` for a rule's origin — links into a directory no reader can follow and no commit can carry.

#### Considered and not done
- **Keeping `chats-context/` as the sanctioned location and only repairing the links that pointed into it** (rejected): the links were the symptom. A location outside the tree cannot be cited under [Documentation → Citations](./documentation.md#citations), cannot be committed, and is lost on any clone that does not have the folder — so every artifact that needs to name its own origin ends up either unbacked or broken. The rule invited that outcome rather than being violated by it.
- **Naming a durable replacement folder inside the repository** (rejected): any such folder is a second naming rule, and a file's name already carries its subject. A folder of handoffs would have to invent names for subjects that have no home yet, which is the question [File Naming](./documentation.md#file-naming) answers by saying the subject's own folder is where the file goes.
- **Extending the section to say what a handoff about a subject with no documents at all should do** (not done): File Naming's clause covers a session that read documents, and this repository's sessions always do. The case of a discussion with nothing read and nothing to name has no instance, and a rule written for it now would be a prediction rather than a repair.

---

### Session completion is declared by its starter
- Time: 2026-10-07T02:57:26-04:00
- Type: Clarified
- Contributors:
  - opencode/exo-free via [OpenCode](../CONTRIBUTORS.md#opencode) — drafted, applied
- Propagates to:
  - .agents/skills/memar/SKILL.md: Done — the agent workflow points here for the session boundary while keeping only the tool-dependent folder instructions.
  - .agents/scripts/memar-session.py: Done — the close help and implementation honor this boundary and use recoverable trash.

#### What changed
`documentation-handoff.practice.md` now places session end only at the point the person who started it declares the work finished. Handoff production is evaluated at that boundary, not after an agent's first answer or a single completed task.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:50:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to this family (practice, handoff, this changelog) against HEAD.
- Three handoff questions were removed and their answers are in the practice's Placement section and the Research facet's companion rule (quotations verified); the new changelog entry records each. Left as is.
- The Placement rewrite is recorded and justified by the entry *Placement follows File Naming*; its three instance files exist. That entry said the trigger "has now arrived twice" and then named three files; corrected to "three times".
- The practice also gained a sentence in *Mid-Session Tangents* (bounded work a session needs integrated is delegation, not a tangent, per "the skill's runtime rules"); the entry *Session completion is declared by its starter* records only the session-end hunk. This entry records the omission. Its `Propagates to` names `.agents/scripts/memar-session.py`, which no longer exists; it records what was true when written.
- Left unchanged: that entry's time is written with an offset (`-04:00`), which the format allows.

---

### A conversation ends when its person says so; a session may correct another's finished work
- Time: 2026-10-12T10:57:14Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- [When This Practice Applies](./documentation-handoff.practice.md#when-this-practice-applies) said a *session* ends only when the person who started it declares the work finished. That was a leftover from before a session meant one task: it is the *conversation* that ends on the person's word, while a session ends when its task's check passes or the task stops.
- A new section, [Correcting Another Session's Work](./documentation-handoff.practice.md#correcting-another-sessions-work): a session may correct another session's work once that session has finished and the problem still stands, and reports each correction in the changed document's record, in its own report, and to the person.

#### Considered and not done
- **Forbidding corrections across sessions (rejected; owner's decision)**: work does not belong to the session that wrote it; what must be avoided is interfering with a session still running.

---

### Queued sessions, the short hand-back, and the owner's digest
- Time: 2026-10-12T16:02:36Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- A new section, [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back), documents the work engine `memar session` now provides: a conversation queues further tasks as sessions and never works them in its own context; a priority from 1 to 10 (5 when absent, the higher sooner) that anyone may change, saying why; `claims N` hands the N first in line to a coordinator, which gives each brief to one fresh sub-agent; a hand-back of the Stop line, the report's path, and at most ten lines of `Decisions needed`; and `digest`, the one list of decisive questions the owner reads instead of every report.
- Observed: one conversation carrying six tasks, with full reports handed back into it, reached about 500K tokens; the coordinator's context and the owner's attention were the two bottlenecks the engine answers.
- The [handoff](./documentation-handoff.handoff.md) gained the open question of where a project's sessions live (owner observation, for queued session `20261012-T155915Z-12312`) and the anticipated work of running queued sessions unattended, which belongs to the `organization` project.

#### Considered and not done
- **A runner that launches each queued session itself (`memar session run` with a launch template)**: Memar starts no agent; the coordinator starts each sub-agent the way its runtime does, and scheduled execution is left to the `organization` project.

---

### Queued work: the help holds the numbers, the digest holds failed hand-backs
- Time: 2026-10-12T16:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back) now points to `memar session --help` for the commands and the limits they enforce — the priority's range and default, the lines a hand-back may hold, how long a claim holds — and keeps what is its own: why the work runs so, and that whoever changes a priority says why in the plan.
- The digest is run for the coordinator's own conversation, holds every failed hand-back whether or not it carries decisions, and leaves out done sessions; the practice and the help say the same.
- Prompted by a review that had not seen the work (session `20261012-T160457Z-8656`), which found the practice restating the help's numbers and the two disagreeing about the digest.

---

### Queued work: claims names its project
- Time: 2026-10-12T16:35:29Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back) now says `memar session claims` takes only from the one project the coordinator names, with no default and no way to take from all, and that a coordinator that does not know the project asks the owner; `claims` refuses without `--project`, and its help and `memar session --help` say the same.
- Why: one run serves one project, and a guessed or spanning scope hides which project the work lands in.
- The owner's ruling, applied in session `20261012-T163251Z-25244`.

---

### Sizing a task and recording follow-ups: the rule placed for every project
- Time: 2026-10-13T06:25:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- A new section, [Sizing a Task and Recording Follow-Ups](./documentation-handoff.practice.md#sizing-a-task-and-recording-follow-ups), states that a task's size is set by weighing a session's load against its work and by the files and governing reading its tasks share: split at an owner decision, at a change testable alone with different files and reading, and at a parallel unit; merge sequential tasks on the same files and reading; hand related tasks queued under one topic to one agent; cut the load per step before merging. It also says to record worth-doing follow-ups as queued sessions opened with `--parent`, erring toward one too many.
- The skill's Delegation bullet now points here and keeps only the working marks it applies.
- Why: the owner ruled (2026-10-13) that this is a general concept Memar solves once for every project, so it does not live in a project's preferences.md. The conclusions come from sessions `20261013-T054743Z-12960` and `20261013-T054829Z-23016`, applied in session `20261013-T060529Z-24608`.

#### Considered and not done
- **A numeric break-even (a multiple of the session load)**: not derived from measurement, so withdrawn by the reviewer; the rule is provisional until a real session is measured.

---

### Queued work: one sub-agent per batch of one topic
- Time: 2026-10-13T06:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back), under Taking queued work, now says that `memar session claims` takes the first task's topic batch next, in line order, and says what it passed over; and that the coordinator hands a batch of one topic to one fresh sub-agent, each session keeping its own plan and report, never sessions of different topics to one sub-agent. It replaces the rule of one sub-agent per session, never two sessions to one sub-agent.
- `memar session --help` now lists `topic`, `topics`, `new --topic` and `claims --topic --fill`, shows the `topic:` front-matter line, tells the queuer to give each queued task a topic and to run `topics` first, and carries the same batch rule in the coordinator steps.
- Why: the owner ruled that related tasks on the same files and reading cost less in one context; the behaviour was implemented in session `20261013-T060530Z-28452` and the text applied in session `20261013-T060530Z-19088`.

---

### The digest becomes a per-day review, and list, gc, and digest flag finished-but-open sessions
- Time: 2026-10-13T08:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back), under The digest, now says that `memar session digest --day` is the owner's review of a day's sessions, closed one by one with `memar session close` on the owner's word, that a done session with decisions is in the digest, and that the digest, `list`, and `gc` flag a session not done that looks finished or abandoned. `memar session --help` carries the same recipe.
- `memar session list`, `gc`, and `digest` now raise a `concerns:` line for a session whose steps are all checked while it is open, whose Request is empty and quiet for a day, or that has no status. They only flag: nothing is moved or closed by it.
- Why: the owner audited about thirty finished-but-never-closed folders by hand and ruled that digest should be a review run with an agent; done in sessions `20261013-T041036Z-24948` and `20261012-T163252Z-11472`.

---

### The Open Questions entry written during a task stands alone
- Time: 2026-10-13T10:50:00Z
- Type: Added
- Propagates to:
  - [Cognition Practice](./cognition.practice.md#norm-application-points): Done - the escalation checkpoint points at the practice section below.
  - `memar content questions` and the lint of entries: Pending - later sessions of topic `question-handoff`.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided the direction
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- [Open Questions](./documentation-handoff.md#open-questions) now lists the six fields of an entry written during a task (heading as the question, State, Options with the recommended first, Anchor, Blocks with the Tentative assumption, Asked), the standalone test, and that an entry is open by being present and leaves by graduation or recorded drop.
- [Questions Found During a Task](./documentation-handoff.practice.md#questions-found-during-a-task) is new: the entry or a queued session by whether an agent could make the question smaller; the finding session writes it, or the coordinator for a sub-agent that may not write; the raising session is done at once, with one pointer line per entry; the answer graduates and the entry is removed, its heading named in the changelog; an uncommitted entry lives on one machine only.
- Why: questions left in the conversation or in a report are lost when the session is swept; the owner ruled (2026-10-13) that they last in the handoff. Design from session `20261013-T085819Z-21616`; applied in sessions `20261013-T103109Z-22272` and `20261013-T103110Z-17584`. The wording awaits the owner's approval, recorded in [documentation-handoff.handoff.md](./documentation-handoff.handoff.md).

#### Considered and not done
- **An explicit `Answer: Pending` field**: presence under the heading already means open, as the practice removes answered entries.

---

### The Status values are defined in Documentation
- Time: 2026-10-13T10:42:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- The [Status](./documentation-handoff.md#status) section now links to [documentation.md → Status](./documentation.md#status) for the four values `Active`, `Paused`, `Blocked`, `Complete` and their meanings, and states what is specific to a handoff: Status is a section because a handoff has no front matter, and `Complete` is the handoff with nothing left open.
- Why: one Status vocabulary for every document kind, defined once; see [documentation.changelog.md](./documentation.changelog.md).

---

### Handoff Practice speaks the Status words, and names the project rule
- Time: 2026-10-13T11:40:00Z
- Type: Changed
- Propagates to:
  - [documentation.md → Status](./documentation.md#status): Done - the Pending propagation of its entry "One Status vocabulary, defined once" for this document and the Memar skill is resolved.
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- [Documentation Handoff Practice](./documentation-handoff.practice.md): a finished session is read by its plan's Status (Complete or Blocked, not Active or Queued), a queued plan becomes Active when claimed, the hand-back carries the report's Status rather than a Stop line, and the digest prints it. A project told by a word is resolved by `memar project find WORD`, never by reasoning about the name.
- [Where a project's sessions live](./documentation-handoff.handoff.md): the entry now says no session verb has a default project or reads the calling folder, names are resolved through `temp/projects.log`, and a missing sessions folder is created.
- Why: the scripts moved to Queued, Active, Blocked, Complete (sessions `20261013-T103111Z-27036`, `20261013-T103108Z-15196`); the prose agents read first must speak the same words.

#### Considered and not done
- **Rewriting the earlier changelog entries that say `Stop` or `open`**: they are history.

---

### The project registry and Khayyam's dependency management are recorded as one open question
- Time: 2026-10-13T14:40:00Z
- Type: addition
- Cited:
  - [Documentation Handoff → Open Questions](./documentation-handoff.md#open-questions) - Depends_on: the six fields of an entry written during a task
- Propagates to:
  - [documentation-handoff.handoff.md](./documentation-handoff.handoff.md): Done - one Open Question with Blocks set
  - `bundles/khayyam/khayyam.handoff.md`: Done - the twin entry and a Tentative decision
  - [.agents/scripts/README.md](../.agents/scripts/README.md): Done - the constraint stated beside "A script is told its project"
- Contributors:
  - [Claude Code](../CONTRIBUTORS.md#claude) - drafted, applied

#### What changed
- The owner's ruling of 2026-10-13 is written down: the project registry (`memar project`, `temp/projects.log`) and Khayyam's dependency management are developed only together, and nothing is added to either until they are one. The reason is recorded with it: no magic in code.

---

### Queued Work points at each verb's own help, and the command module's help protocol is an open question
- Time: 2026-10-14T18:20:00Z
- Type: Changed
- Propagates to:
  - `.agents/scripts/services/session.py` and the session verbs' services: Done (session `20261014-T175052Z-9344`) - `memar session --help` states only the domain's own work; each verb's own help states its part.
  - `modules/lib/lib.handoff.md`: Done - the entry *What protocol a command's help follows once `process/command/` is complete*
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Opus 5.5) - drafted, applied

#### What changed
- [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back) now says the commands and their limits are declared by the `--help` of `memar session` and of each of its verbs, each stating its own, and names the verb whose help gives each limit: the priority's range and default (`memar session priority --help`), how long a claim holds (`memar session claim --help`), the lines a hand-back may hold (`memar session new --help`).
- Why: the owner ruled (2026-10-14) that each command's help states only its own work, not its sub-commands'; `memar session --help` had grown to about 19 KB by repeating every verb's command lines and recipes, and the pointers here named it for limits it no longer states.
- The owner's question of which protocol command help follows once the command module (`modules/lib/process/command/`) is complete is written as an open entry in `modules/lib/lib.handoff.md`, with options; nothing is built on that module.

#### Considered and not done
- **Rewriting the earlier entries that say `memar session --help` carries the recipe**: they are history.
