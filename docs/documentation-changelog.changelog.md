# Documentation — Changelog Changelog
This document records why and how `documentation-changelog.md` changed over time. See [Documentation — Changelog](./documentation-changelog.md) for what this file's structure means.

## Changelog

### Initial specification
- Time: 2026-07-25T00:00:00Z (approximate — historical import)
- Cited:
  - [Diátaxis](https://diataxis.fr/) — Reference: studied early in this project's documentation design as a model for separating documentation content by reader purpose. Its four-way split (Tutorials, How-to guides, Reference, Explanation) was adopted as the starting axis for this project's own Facet concept, but proved insufficient once a real need emerged that none of those four forms covers: recording the history of an artifact rather than telling the reader how to act on it or how to understand it. The Changelog facet was added as a third facet precisely to cover this case. Diátaxis is cited here as the prior art that motivated the Facet concept and as the framework this project extended beyond; it is not mentioned in the base specification itself, per the rule that argumentative citations live only in the changelog.
  - [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — Reference: examined as existing vocabulary for change types (`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`), offered in the base specification's Type section as a starting point, not a requirement.
  - [Conventional Commits](https://www.conventionalcommits.org/) — Reference: examined as a second existing vocabulary for change types (`feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`/`revert`), offered alongside Keep a Changelog in the Type section.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Created as the governing specification for the Changelog facet, defining: the `<base>.changelog.md` companion-file convention; the entry structure (short descriptive title, metadata bullets for `Time`/`Type`/`Cited`/`Propagates to`/`Tasks`/`Contributors`, followed by `Summary` and optional `Rationale and alternatives` as prose headings); the project-wide `CONTRIBUTORS.md` registry; and propagation tracking (Claude — drafted; Super Z — refined across multiple rounds).
- Base documents' former `Citations`, `Contributors`, and `Applied to` front-matter fields (and `## Change Rationale` body section) were absorbed into this facet (Omid Hekayati — directed; Claude — drafted).
- The `Evidence` relation was added to the Cited vocabulary (Super Z).
- The exception that Changelog-facet files do not themselves get companion changelogs was clarified (Super Z).

#### Deliberation
- The need to move provenance out of base documents into companion history files was identified (Omid Hekayati).
- Adopting the Facet pattern for the Changelog, rather than leaving it as ad-hoc convention, was directed (Omid Hekayati).

#### Considered and not done
- **Giving a Changelog-facet file its own companion changelog (rejected)**: would recurse indefinitely with no natural stopping point. Version control already records what changed in a changelog file itself, which is sufficient — the whole reason a Changelog facet exists for other artifacts is that version control alone doesn't capture *why*, but a changelog entry's own reason for existing is already "recording why," so the same gap doesn't recur one level up.
- **Treating Changelog as an ad-hoc per-document convention rather than a named Facet (rejected)**: once the same `<base>.changelog.md` pattern was being applied across multiple artifacts, naming it as a Facet — with its own governing specification and the same extension mechanism the existing two facets use — was the smaller conceptual cost than leaving it as implicit convention.
- **Reusing Diátaxis's four-form framework for the Changelog facet (rejected)**: Diátaxis's four forms (Tutorials, How-to guides, Reference, Explanation) all describe content the reader studies or follows; a changelog is consulted to audit history, which is a different reader relationship entirely. Forcing it into one of Diátaxis's four categories would obscure what makes a changelog structurally distinct. The Changelog facet is this project's own extension beyond Diátaxis's framework.

### Trimmed Cited section to reference the meta-layer's cross-cutting Citations definition
- Time: 2026-08-11T00:00:00Z
- Type: Changed
- Cited:
  - [Documentation](./documentation.md) — Depends_for: the source-selection criteria and full Relation vocabulary (including `Evidence`) are now defined there as cross-cutting concerns, applying wherever citations appear in any facet.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- The `### Cited` section previously defined the full Relation vocabulary inline and gave per-relation guidance (notably for the new `Evidence` relation); that content was duplicated from where it now lives authoritatively — `documentation.md → Citations`, added as a cross-cutting concern in the same round of changes.
- The section was trimmed from two paragraphs to one, removing the inline Relation vocabulary enumeration and the per-relation guidance for `Evidence` and replacing them with a reference to `documentation.md → Citations`.
- Kept only what is specific to a Changelog entry's `Cited` field: the "replaces former Citations field" framing; the "cite here is sufficient provenance" rule (no need to repeat it in the base artifact's body); and the inline-hyperlink exception for sources the base artifact's own body genuinely needs at the point of reading — link it inline as a normal hyperlink, never as an unlinked "see X" pointer.

#### Deliberation
- The `### Cited` section in this specification was carrying two different kinds of content — Changelog-specific format rules, and the general citation vocabulary and source-selection criteria that any facet needing citations would also need (Omid Hekayati — argued).
- The latter does not belong here; it belongs in the meta-layer so a future facet inherits it without redefinition (Omid Hekayati — argued).

#### Considered and not done
- **Keep the full Relation vocabulary inline in this specification (rejected)**: would have required keeping two definitions in sync — the one here and the one in `documentation.md → Citations` — every time the vocabulary changed. With `Evidence` just added and the `Reference`/`Depends_on` boundary still an open Unresolved question, the vocabulary is not yet stable enough to risk duplication drift.
- **Move the Relation vocabulary here and have `documentation.md` reference this file (considered, not chosen)**: would have made the Changelog spec the canonical home for a concern that is not Changelog-specific. The vocabulary applies wherever citations appear — currently Changelog, potentially a future Research facet — so its canonical home is the meta-layer, not any one facet's spec.

### Scoped the changelog to the base artifact; practice companions share it
- Time: 2026-09-01T14:34:32Z
- Type: Changed
- Cited:
  - [Documentation — Explanation Changelog](./documentation-explanation.changelog.md) — Evidence: the worked case for the change — the retired `documentation-explanation.practice.changelog.md` recorded its practice file's changes as alignments forced by base-document changes, demonstrating that base and companion changes are one narrative rather than two.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- The Changelog-scope rule was added to the specification: a changelog is paired to a base artifact, and the base artifact's `<base>.practice.md` companion records its changes in that same changelog — a practice file never receives a changelog of its own (Omid Hekayati — decided one changelog per topic, not one per file: fewer documents, and the changes to a base document and its practice companion are too closely related to justify two ledgers; Super Z — rewrote).
- This supersedes the earlier four-file structure (`<base>.md`, `<base>.practice.md`, `<base>.changelog.md`, `<base>.practice.changelog.md`) (Omid Hekayati — decided).
- Existing `.practice.changelog.md` files merge into their base artifact's changelog as a propagation of this change (Omid Hekayati — decided).

#### Deliberation
- The earlier four-file structure had been a decision the owner themselves specified during the Chapar documentation migration (recorded in `chapar.practice.changelog.md`), and the owner now supersedes it by their own direction (Omid Hekayati).
- The `thinking` topic had already been handled with one changelog per topic in practice, noted approvingly (Omid Hekayati).

#### Propagates to
- `documentation-explanation.practice.changelog.md`: Done — merged into `documentation-explanation.changelog.md` and deleted.
- `type.practice.changelog.md`: Done — merged into `type.changelog.md` and deleted.
- `giti.practice.changelog.md`: Done — merged into `giti.changelog.md` and deleted.
- `chapar.practice.changelog.md`: Done — merged into `chapar.changelog.md` and deleted.
- `networking.changelog.md`: Done — its reference to the retired `giti.practice.changelog.md` repointed to `giti.changelog.md`.

#### Considered and not done
- **Keep the uniform per-file rule (rejected by the owner)**: mechanically simpler to state, but the coupling evidence ran the other way — companion changelogs were recording alignments forced by base changes — and the file-count cost is one this documentation system already names in its Drawbacks. The scope rule is barely more complex than the naming rule it sits beside.
- **Extend the sharing rule to Handoff companions now (rejected for now)**: the Handoff facet's own open question about handoff-changelog history stays open; this change does not preempt it.

---

### CONTRIBUTORS.md model lists given an explicit chronological, append-only order
- Time: 2026-09-05T14:30:00Z
- Type: Changed
- Propagates to:
  - CONTRIBUTORS.md: Done — every Models list reordered oldest-first (Super Z and Qwen were descending) and official per-model links added where the vendor page was verified by direct fetch.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — argued, rewrote

#### What changed
- The CONTRIBUTORS.md section now states that an AI contributor's Models list is chronological, oldest first, with new models appended at the end — the same append-only convention as changelog entries, so adding a model never forces a re-sort.
- It now also states that a model may carry a link to its official documentation page where one exists and has been verified.
- Applied in CONTRIBUTORS.md: GLM and Qwen lists reversed to ascending; OpenAI, Anthropic, Google DeepMind, Z.ai, and Qwen-collection model pages linked, each linked URL verified by fetching.
- GLM-5.0 and Qwen3.8-Flash carry no dedicated link because no verifiable per-model page was found, and the previous GLM-5.3-Flash link was removed: it pointed at oxalpha.io, an unrelated third-party model page, not Z.ai.

#### Deliberation
- Whether the Models lists should run ascending or descending was asked, with a request to audit the file's model ordering and add official website links per model where possible (Omid Hekayati — requested).
- Ascending (append-only) was recommended, to match the facet's own entry convention (Qwen — argued).

---

### Abstract extended; discussion content relocated; entry structure restructured per the finalized method
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Propagates to:
  - documentation-changelog.handoff.md: Created - this specification's open questions moved there.
  - documentation-explanation.md: Done - the method this migration follows was finalized there in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - rewrote, moved

#### What changed
- The Session consolidation topic added: one working session touching one base artifact produces one entry, not one per edit; a new entry only when the kind of work changes (Omid Hekayati - the rule, after observing the session itself produce five redundant entries in one changelog; Super Z - written).
- The Abstract gained a second paragraph naming decision-shaping context and comparative prior-art surveys as this facet's content classes (Omid Hekayati - decided; Super Z - written).
- The entry template is restructured: `Summary` becomes `What changed`; `Considered and not done`, `Related work`, and `Decision` are added as optional entry sections (Omid Hekayati - demanded structured sections instead of prose Summary after seeing migrated content flattened into narrative; Super Z - written).
- The Contributors bullet is shortened to presence plus role tags; every substantive claim in an entry carries its attribution inline in parentheses (Omid Hekayati - the role prose had grown and scattered attribution; Super Z - wrote the rule).
- The Structure topic is aligned with the Explanation facet's Optional Sections model: entry content sections are open-catalog building blocks, not mandatory templates (Omid Hekayati - decided; Super Z - applied).
- A final audit found several `Rationale and alternatives` and `Unresolved questions` blocks that the earlier passes missed; all are recorded below and in the paired handoff (Super Z - audit and migration).

#### Considered and not done
- A separate changelog per practice file (rejected): the coupling between a base specification and its procedure runs one way - so per-file changelogs either duplicate the same change as two entries or split one narrative across two ledgers referencing each other, and they multiply files for no reader benefit.
- Extend the sharing rule to Handoff companions now (rejected for now): a handoff is mutable working state rather than a procedure, and whether its churn is worth changelog history at all is an open question in the Handoff facet; deciding it here would preempt that question without new evidence.
- A single `Applied to` field on the base artifact, as before (rejected): could only express "where the current design already landed," not "what changes are still owed elsewhere," and couldn't distinguish which specific change a propagation obligation came from.
- `Pending`/`Done` only, no `Rejected` (considered, not chosen): a propagation that's considered and deliberately declined would have no way to stop appearing as outstanding work in a future search.
- Timestamp as the entry's own `###` heading (an earlier draft; not chosen): put a machine-format string where a human-scannable title should be. Time is a fact about the entry, not its identity, so it moved into a `Time` bullet.
- A `####` heading for every field, including the short metadata ones (an earlier draft; not chosen): for fields that are genuinely metadata rather than content, a heading is more structural weight than the field needs.
- Giving a Changelog-facet file its own companion changelog (rejected): would recurse indefinitely with no natural stopping point; version control already records what changed in a changelog file itself.
- Treating Changelog as an ad-hoc per-document convention rather than a named Facet (rejected): once the same pattern was being applied across multiple artifacts, naming it as a Facet was the smaller conceptual cost than leaving it as implicit convention.

#### Decision
Open questions (dot-boundary criterion, entry-title uniqueness, historical-entry timestamps) moved to the paired handoff.

### Added the Deliberation section; narrowed What changed to outcomes; replaced the verbatim-relocation constraint
- Time: 2026-09-07T20:56:16Z
- Type: Changed
- Propagates to:
  - documentation-changelog.handoff.md: Done - the "Where multi-participant deliberation narrative lives in an entry" question removed; its resolution graduated into the specification and is recorded in this entry.
  - Pre-finalization changelog entries carrying verbatim-migrated narrative: Done - campaign executed 2026-09-07, one sub-agent per file under the procedure recorded in documentation-changelog.handoff.md → Anticipated Work; 45 files remediated plus the two pilot files given a second pass; `content.changelog.md` excluded as unrecoverable from its own text and left for owner-assisted repair.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) - argued, wrote

#### What changed
- The Optional Sections catalog gained `Deliberation`: the chronology of positions in a multi-participant session, as claim-shaped sentences each carrying its own inline attribution, ordered by the exchange rather than by person; distinct from `Considered and not done` (rejected alternatives as outcomes) and `Decision` (the final ruling); never needed for single-contributor changes, and never reconstructed from evidence the entry does not carry.
- `What changed` was narrowed by an explicit writing rule: it states the outcome of the change, not the process that produced it.
- The verbatim-relocation constraint was replaced by an information-loss prohibition: migrated narrative may be rewritten claim-shaped, since what the constraint guards is content, not shape; the rewrite of the affected pre-finalization entries is tracked as the Pending propagation above.
- Per-claim attribution in `What changed` was narrowed to the varying-authorship case: uniform attribution stays in the `Contributors` tags rather than repeating on every bullet, and decision and position claims live only in `Deliberation` - one fact, one home.
- The remediation campaign was executed the same day across the changelog set: 46 `Deliberation` sections now exist; the only surviving violation is `content.changelog.md`, whose chronology cannot be restructured from its own text (owner-assisted repair tracked in the paired handoff).

#### Deliberation
- The oddity was flagged from a separate session: deliberation chronology and migrated verbatim narrative squeezed into `What changed` read as transplant rather than record - one `(Name)` tag per narrative paragraph instead of per claim (Omid Hekayati - the failure report).
- The owner proposed fixed person/topic-centric entry titles ("what was the problem and who raised it", "who raised critiques") (Omid Hekayati - the proposal).
- Counter-arguments were recorded in the same discussion: fixed titles re-import the per-purpose-template model both facets rejected, tax small single-contributor changes with empty structure, and contradict the open-catalog principle adopted in the 2026-09-06 finalization (Qwen - argued).
- The root was then diagnosed one level up: the Abstract already promises decision-shaping context a home in the changelog, but the catalog held only outcome-shaped sections - the defect was a missing catalog section, not the `What changed` section itself (Qwen - the diagnosis; Omid Hekayati - accepted).
- What tipped the balance: the root diagnosis made a named process section both necessary and sufficient, so the catalog extension was chosen over the alternatives recorded below (Qwen - argued; Omid Hekayati - decided).
- In the same session the owner asked whether `Deliberation` should be mandatory even for single-participant changes, to close every duplication route; the variant was argued against - a forced section for an exchange that never happened gets padded with re-narrated outcomes, the same per-purpose-template failure that killed the fixed-entry-titles proposal above, while the varying-authorship rule already leaves solo entries with zero names in `What changed` - and the owner directed proceeding with the narrower rule (Omid Hekayati - the question, decided; Qwen - argued).

#### Considered and not done
- Fixed person/topic-centric entry titles ("what was the problem and who raised it", "who raised critiques") (rejected): re-imports the per-purpose-template model both facets rejected, taxes small single-contributor changes with empty structure, and contradicts the open-catalog principle adopted in the 2026-09-06 method finalization. (Omid Hekayati - the proposal; Qwen - the counter-arguments; Omid Hekayati - decided)
- Absorbing the chronology into `Decision` (rejected): `Decision` must stay short and quotable as the ruling; merging process into ruling destroys its citation value. (Qwen - argued; Omid Hekayati - accepted)
- Keeping `What changed` as the home with a writing rule only, no new section (rejected): claim-shaped sentences under a title meaning "the change itself" still mislabel deliberation as outcome - the form fix alone leaves the identity crisis that produced the oddity. (Qwen - argued; Omid Hekayati - accepted)

---

### Added the Trivial changes rule: changes with nothing to audit receive no entry; commit economy added alongside
- Time: 2026-09-09T06:02:23Z
- Type: Added
- Cited:
  - [SDK](./protocols/sdk.changelog.md) — Evidence: the triggering case — a link-repair entry in gui.changelog.md whose whole content restated a one-line diff — was flagged in the SDK protocol's own changelog while its propagation record was being written.
- Propagates to:
  - gui.changelog.md: Done — the "SDK link corrected" entry removed under the new rule; the fix itself had already landed and remains in version control.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via ZCode) — recorded

#### What changed
- The specification gained `Trivial changes`: a change with nothing to audit — broken-link repair, typo fix, cosmetic correction — receives no entry; the diff is the whole record. Two boundaries accompany it: a change that starts disclosing something worth auditing is no longer trivial and earns an entry; and a trivial fix made alongside a substantive change rides inside that session's consolidated entry instead of earning its own.
- The specification also gained `Commit economy`, immediately after: the same rule one level up — a trivial change does not earn its own commit and waits to ride with the repository's next substantive commit — with the boundary that batching is a delay in recording, not a substitute: at session end the working state is committed; uncommitted working state is not a storage medium.

#### Deliberation
- The noise was flagged with the concrete example: a whole changelog entry for a link correction "is really pointless" and clutters the ledger for no audit value (Omid Hekayati — claimed).
- The exception's discretionary nature was acknowledged in the request itself — an agent could read it otherwise — so the rule was made structural: the test is the facet's own audit reader, with the two boundaries stated in the specification rather than left to each writer's judgment (Super Z — recorded; Omid Hekayati — decided).
- The same discussion then extended the economy to commits: fast-committing small changes costs a permanent history entry, review weight, and attention that a trivial change cannot justify (Omid Hekayati — claimed).
- One accumulation risk was raised and answered inside the rule rather than as a separate section: batching could become hoarding if trivial changes never catch a ride, so the rule states the session-end boundary explicitly — batching is a delay in recording, not a substitute for recording (Super Z — recorded; Omid Hekayati — accepted).
- The two rules were added in one consolidated entry the same session, per the Session consolidation rule (Super Z — recorded).

---

### Append without loading; forbid newest-first insertion
- Time: 2026-09-18T13:05:00Z
- Type: Changed
- Cited:
  - Owner session — Evidence: agents repeatedly prepended changelog entries, forcing a full-file read; the Structure rule already said oldest-first but lacked an agent-facing append path.
- Propagates to:
  - .agents/skills/memar/scripts/memar-doc.py: Done — changelog-append subcommand.
  - .agents/commands/: Done — paste catalog removed; executable helpers under commands/ (same session correction).
  - .agents/skills/memar/SKILL.md: Done — navigation step 5.
  - CONTRIBUTORS.md: Done — Composer identity added; Cursor remains under Tools.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../CONTRIBUTORS.md#composer) (Composer via Cursor) — drafted

#### What changed
- Strengthened [Structure](./documentation-changelog.md#structure): oldest-first is mandatory; newest-first is forbidden; agents must not load a changelog into context solely to append.
- Documented `memar-doc.py changelog-append` as the mechanical append path (see that script's `--help`; peeks only the file tail).
- Clarified AI contributor recording: model Name in CONTRIBUTORS.md, host tool under Tools, entry field shape `{ModelName} via {ToolName}`.

#### Deliberation
- Prepending was identified as a recurring agent failure with real cost on large changelogs (Omid Hekayati — claimed). The fix is structural (append command + explicit forbid) rather than hoping writers re-read Structure (Composer — recorded; Omid Hekayati — decided).

---

### Same-session undone mistakes earn no entry
- Time: 2026-09-18T14:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../CONTRIBUTORS.md#composer) (Composer via Cursor) — drafted

#### What changed
- Extended [Trivial changes](./documentation-changelog.md#trivial-changes): a same-session wrong change that was reverted or relocated before any durable snapshot of the wrong state has nothing to audit — delete the entry; Session consolidation does not invent provenance for corrected keystroke history.
- Documented `memar-doc.py changelog-append` as the mechanical append path without embedding a pasteable recipe catalog in Structure.
