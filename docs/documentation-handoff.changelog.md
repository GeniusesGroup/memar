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

#### Summary
Created `documentation-handoff.md` (ID 496741) as the governing specification for the Handoff facet: a `<base>.handoff.md` companion capturing the distilled state of a discussion so a later session — AI, human, or organizational — can resume it. The specification defines the concept (state transfer across a session boundary, borrowing the established cross-domain term), its central discipline (analysis, not transcription — three named risks with structural controls: fixed skeleton against selection asymmetry, mandatory confidence vocabulary against analysis-record confusion, required rationale capture against invisible premises), its relationship to the existing facets (no design claims — conclusions graduate into Explanation-facet documents; mutable state, not append-only history), the fixed section skeleton, and the file format. Created the paired practice file with the producing, consuming, and placement procedures. Absorbed and deleted the three practice documents; the surviving references to them are these provenance records.

#### Rationale and alternatives
- **Keep the three practice files separate (rejected by the owner)**: they were overlapping drafts of the same artifact, each informal, none authoritative, and together they suggested workflows (review checklists, proposal templates) whose home is not handoff at all — consolidation replaces three sources of drift with one specification.
- **Fold the handoff content into the Practice facet as a larger practice document (rejected)**: a handoff's primary reader is a session reconstructing discussion state, not an agent executing steps — the reader relationship that defines the Practice facet. The procedural content went to the paired practice file; the state-capture artifact needed its own governing specification.

### Removed the resolved registration question from the base document
- Time: 2026-09-01T14:34:32Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: a question whose answer is settled must not remain in the base document at all — the base document carries current state, and its changelog carries the history; the question's existence and resolution are recorded here.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The base document's Unresolved questions had carried the facet-registration question struck through as resolved, after the owner directed registration. Per the owner's rule — an answered question leaves the base document entirely; the changelog is where "a question was here, and is now settled" is recorded — the question was removed, the remaining questions renumbered, and the Future possibilities bullet anticipating registration was dropped since registration has occurred. The resolution event itself is recorded in the "Registered the Handoff facet as the fourth facet" entry of [documentation.changelog.md](./documentation.changelog.md); this entry preserves the fact that the question existed in this document and where its answer came from.
- **Fold the handoff content into the Changelog facet as a second file kind (rejected)**: a changelog is append-only history consulted to audit the past; a handoff is mutable state consulted to resume work. Append-only state-capture buries the current state under the discussion's own evolution — the exact cost the artifact exists to avoid. The two facets cross-reference instead.
