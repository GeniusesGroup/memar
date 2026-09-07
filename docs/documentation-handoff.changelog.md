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
  - [thinking.md](./thinking.md): Done — the boundary note that pointed to the retired `documentation-review.practice.md` now points to [Documentation](./documentation.md) as the documentation system's entry point.
  - `documentation-critique.practice.md`: Done — its "Relation to Other Practices" rows referencing the two retired practices updated to the merged practice.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: directed the consolidation of the handoff-related practice documents into one base document named `documentation-handoff.md` (dropping the `conversation` qualifier — the `documentation-` prefix already scopes it, and "handoff" is the established cross-domain term); required that the artifact be defined agent-generally (a fully human session is covered by the same artifact, not only AI chat sessions); required that the artifact's self-awareness risks — selection asymmetry, analysis-versus-record confusion, invisible premises — be named and structurally controlled rather than left as caveats; proposed the `.handoff.md` companion suffix following the `.changelog.md` precedent.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: drafted the specification and the paired practice, structured the three risks and their controls, and executed the consolidation.

#### What changed
Created `documentation-handoff.md` (ID 496741) as the governing specification for the Handoff facet: a `<base>.handoff.md` companion capturing the distilled state of a discussion so a later session — AI, human, or organizational — can resume it. The specification defines the concept (state transfer across a session boundary, borrowing the established cross-domain term), its central discipline (analysis, not transcription — three named risks with structural controls: fixed skeleton against selection asymmetry, mandatory confidence vocabulary against analysis-record confusion, required rationale capture against invisible premises), its relationship to the existing facets (no design claims — conclusions graduate into Explanation-facet documents; mutable state, not append-only history), the fixed section skeleton, and the file format. Created the paired practice file with the producing, consuming, and placement procedures. Absorbed and deleted the three practice documents; the surviving references to them are these provenance records.

#### Considered and not done
- **Keep the three practice files separate (rejected by the owner)**: they were overlapping drafts of the same artifact, each informal, none authoritative, and together they suggested workflows (review checklists, proposal templates) whose home is not handoff at all — consolidation replaces three sources of drift with one specification.
- **Fold the handoff content into the Practice facet as a larger practice document (rejected)**: a handoff's primary reader is a session reconstructing discussion state, not an agent executing steps — the reader relationship that defines the Practice facet. The procedural content went to the paired practice file; the state-capture artifact needed its own governing specification.

### Removed the resolved registration question from the base document
- Time: 2026-09-01T14:34:32Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: a question whose answer is settled must not remain in the base document at all — the base document carries current state, and its changelog carries the history; the question's existence and resolution are recorded here.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
The base document's Unresolved questions had carried the facet-registration question struck through as resolved, after the owner directed registration. Per the owner's rule — an answered question leaves the base document entirely; the changelog is where "a question was here, and is now settled" is recorded — the question was removed, the remaining questions renumbered, and the Future possibilities bullet anticipating registration was dropped since registration has occurred. The resolution event itself is recorded in the "Registered the Handoff facet as the fourth facet" entry of [documentation.changelog.md](./documentation.changelog.md); this entry preserves the fact that the question existed in this document and where its answer came from.
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
- The skeleton's `Open Questions` section gained a sibling, `Anticipated Work`, receiving extensions and growth paths a discussion anticipates but no one has committed to - and the anticipated work a base document records for its future, per the Explanation facet's Relevance discipline (Omid Hekayati - the routing decision; Super Z - applied).
- The specification's own body reformed under the finalized method: topic-level `#### Drawbacks` and document-level `## Drawbacks` replaced by open-catalog sections; rejected-alternative and open-question content moved out (Super Z).
- The `Structure` topic now describes the skeleton as an open catalog of state sections, explicitly aligned with the Explanation facet's Optional Sections model; the former word "fixed" is replaced by "open" (Omid Hekayati - decided; Super Z - applied).
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
- Telecommunications handover: transfer of an in-progress session between channels or cells without loss - the source of the term and of the requirement that the transfer preserve the session rather than restart it. (Super Z - migrated)
- Change-of-shift report in healthcare: structured transfer of patient state between shifts, with its own documented failure literature when done poorly. (Super Z - migrated)
- Follow-the-sun development: the same transfer across time zones in software work. (Super Z - migrated)
- Meeting minutes and decision logs: the long-established human practice of distilling a discussion into its outcomes - a handoff is their disciplined descendant, with structure added for the risks minutes historically ignore (confidence, assumptions, invisible premises). (Super Z - migrated)
- Within AI-assisted development, handoff/context-summary conventions have begun appearing in ecosystem tooling - evidence of the need, though typically free-form and unstructured in exactly the ways the analysis-not-transcription discipline warns against. (Super Z - migrated)

#### Considered and not done (from the removed Drawbacks section)
- The facet adds a fourth artifact kind to the documentation system - one more thing a contributor must understand and choose among. It also institutionalizes a writing obligation at session boundaries, where motivation to produce it is lowest; the quality controls make the obligation heavier than the ad-hoc habit it replaces, by design. And the boundary between "handoff" and "early draft of the real document" is a real risk: a discussion that has effectively concluded should graduate into Explanation- and Changelog-facet documents, not persist as a handoff indefinitely - enforcing it requires judgment every time. (Super Z - migrated from the removed section)

#### Decision
The wrapper titles are gone from this specification's body; open questions and anticipated work live in the paired handoff. (Omid Hekayati - approved)
