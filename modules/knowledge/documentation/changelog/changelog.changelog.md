# Documentation — Changelog Changelog
This document records why and how `documentation-changelog.md` changed over time. See [Documentation — Changelog](./changelog.md) for what this file's structure means.

## Changelog

### Initial specification
- Time: 2026-07-25T00:00:00Z (approximate — historical import)
- Cited:
  - [Diátaxis](https://diataxis.fr/) — Reference: studied early in this project's documentation design as a model for separating documentation content by reader purpose. Its four-way split (Tutorials, How-to guides, Reference, Explanation) was adopted as the starting axis for this project's own Facet concept, but proved insufficient once a real need emerged that none of those four forms covers: recording the history of an artifact rather than telling the reader how to act on it or how to understand it. The Changelog facet was added as a third facet precisely to cover this case. Diátaxis is cited here as the prior art that motivated the Facet concept and as the framework this project extended beyond; it is not mentioned in the base specification itself, per the rule that argumentative citations live only in the changelog.
  - [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — Reference: examined as existing vocabulary for change types (`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`), offered in the base specification's Type section as a starting point, not a requirement.
  - [Conventional Commits](https://www.conventionalcommits.org/) — Reference: examined as a second existing vocabulary for change types (`feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`/`revert`), offered alongside Keep a Changelog in the Type section.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../../../../CONTRIBUTORS.md#claude) — rewrote
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Documentation](../documentation.md) — Depends_for: the source-selection criteria and full Relation vocabulary (including `Evidence`) are now defined there as cross-cutting concerns, applying wherever citations appear in any facet.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Documentation — Explanation Changelog](../explanation/explanation.changelog.md) — Evidence: the worked case for the change — the retired `documentation-explanation.practice.changelog.md` recorded its practice file's changes as alignments forced by base-document changes, demonstrating that base and companion changes are one narrative rather than two.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../../../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — argued, rewrote

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) - rewrote, moved

#### What changed
- The Session consolidation topic added: one working chat touching one base artifact produces one entry, not one per edit; a new entry only when the kind of work changes (Omid Hekayati - the rule, after observing the session itself produce five redundant entries in one changelog; Super Z - written).
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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Qwen](../../../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) - argued, wrote

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
- In the same chat the owner asked whether `Deliberation` should be mandatory even for single-participant changes, to close every duplication route; the variant was argued against - a forced section for an exchange that never happened gets padded with re-narrated outcomes, the same per-purpose-template failure that killed the fixed-entry-titles proposal above, while the varying-authorship rule already leaves solo entries with zero names in `What changed` - and the owner directed proceeding with the narrower rule (Omid Hekayati - the question, decided; Qwen - argued).

#### Considered and not done
- Fixed person/topic-centric entry titles ("what was the problem and who raised it", "who raised critiques") (rejected): re-imports the per-purpose-template model both facets rejected, taxes small single-contributor changes with empty structure, and contradicts the open-catalog principle adopted in the 2026-09-06 method finalization. (Omid Hekayati - the proposal; Qwen - the counter-arguments; Omid Hekayati - decided)
- Absorbing the chronology into `Decision` (rejected): `Decision` must stay short and quotable as the ruling; merging process into ruling destroys its citation value. (Qwen - argued; Omid Hekayati - accepted)
- Keeping `What changed` as the home with a writing rule only, no new section (rejected): claim-shaped sentences under a title meaning "the change itself" still mislabel deliberation as outcome - the form fix alone leaves the identity crisis that produced the oddity. (Qwen - argued; Omid Hekayati - accepted)

---

### Added the Trivial changes rule: changes with nothing to audit receive no entry; commit economy added alongside
- Time: 2026-09-09T06:02:23Z
- Type: Added
- Cited:
  - SDK (`docs/modules/process/service-sdk.changelog.md`) — Evidence: the triggering case — a link-repair entry in gui.changelog.md whose whole content restated a one-line diff — was flagged in the SDK protocol's own changelog while its propagation record was being written.
- Propagates to:
  - gui.changelog.md: Done — the "SDK link corrected" entry removed under the new rule; the fix itself had already landed and remains in version control.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [ZCode](../../../../CONTRIBUTORS.md#zcode)) — recorded

#### What changed
- The specification gained `Trivial changes`: a change with nothing to audit — broken-link repair, typo fix, cosmetic correction — receives no entry; the diff is the whole record. Two boundaries accompany it: a change that starts disclosing something worth auditing is no longer trivial and earns an entry; and a trivial fix made alongside a substantive change rides inside that chat's consolidated entry instead of earning its own.
- The specification also gained `Commit economy`, immediately after: the same rule one level up — a trivial change does not earn its own commit and waits to ride with the repository's next substantive commit — with the boundary that batching is a delay in recording, not a substitute: at session end the working state is committed; uncommitted working state is not a storage medium.

#### Deliberation
- The noise was flagged with the concrete example: a whole changelog entry for a link correction "is really pointless" and clutters the ledger for no audit value (Omid Hekayati — claimed).
- The exception's discretionary nature was acknowledged in the request itself — an agent could read it otherwise — so the rule was made structural: the test is the facet's own audit reader, with the two boundaries stated in the specification rather than left to each writer's judgment (Super Z — recorded; Omid Hekayati — decided).
- The same discussion then extended the economy to commits: fast-committing small changes costs a permanent history entry, review weight, and attention that a trivial change cannot justify (Omid Hekayati — claimed).
- One accumulation risk was raised and answered inside the rule rather than as a separate section: batching could become hoarding if trivial changes never catch a ride, so the rule states the session-end boundary explicitly — batching is a delay in recording, not a substitute for recording (Super Z — recorded; Omid Hekayati — accepted).
- The two rules were added in one consolidated entry the same chat, per the Session consolidation rule (Super Z — recorded).

---

### Append without loading; forbid newest-first insertion
- Time: 2026-09-18T13:05:00Z
- Type: Changed
- Cited:
  - Owner session — Evidence: agents repeatedly prepended changelog entries, forcing a full-file read; the Structure rule already said oldest-first but lacked an agent-facing append path.
- Propagates to:
  - .agents/skills/memar/scripts/memar-doc.py: Done — changelog-append subcommand.
  - .agents/commands/: Done — paste catalog removed; executable helpers under commands/ (same chat correction).
  - .agents/skills/memar/SKILL.md: Done — navigation step 5.
  - CONTRIBUTORS.md: Done — Composer identity added; Cursor remains under Tools.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../../../../CONTRIBUTORS.md#composer) (Composer via [Cursor](../../../../CONTRIBUTORS.md#cursor)) — drafted

#### What changed
- Strengthened [Structure](./changelog.md#structure): oldest-first is mandatory; newest-first is forbidden; agents must not load a changelog into context solely to append.
- Documented `memar-doc.py changelog-append` as the mechanical append path (see that script's `--help`; peeks only the file tail).
- Clarified AI contributor recording: model Name in CONTRIBUTORS.md, host tool under Tools, entry field shape `{ModelName} via {ToolName}`.

#### Deliberation
- Prepending was identified as a recurring agent failure with real cost on large changelogs (Omid Hekayati — claimed). The fix is structural (append command + explicit forbid) rather than hoping writers re-read Structure (Composer — recorded; Omid Hekayati — decided).

---

### Same-session undone mistakes earn no entry
- Time: 2026-09-18T14:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../../../../CONTRIBUTORS.md#composer) (Composer via [Cursor](../../../../CONTRIBUTORS.md#cursor)) — drafted

#### What changed
- Extended [Trivial changes](./changelog.md#trivial-changes): a same-session wrong change that was reverted or relocated before any durable snapshot of the wrong state has nothing to audit — delete the entry; Session consolidation does not invent provenance for corrected keystroke history.
- Documented `memar-doc.py changelog-append` as the mechanical append path without embedding a pasteable recipe catalog in Structure.

---

### CONTRIBUTORS.md contact and Co-authored-by records; spec example replaced with a live-file pointer
- Time: 2026-09-23T08:09:51Z
- Type: Added
- Cited:
  - Owner session — Evidence: correspondence emails and Co-authored-by trailers verified against official vendor contact pages, official tool repositories, and real attributed commits.
- Propagates to:
  - CONTRIBUTORS.md: Done — model entries gained correspondence `[eMail]` records, Tools entries gained `Co-authored-by:` trailer records, the Template gained the field shape, and the For AI agents section was removed as relocated into this specification.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Mimo](../../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — researched, drafted

#### What changed
- CONTRIBUTORS.md: every model entry now carries its organization's public correspondence address; every Tools entry carries the exact `Co-authored-by:` trailer its agent appends to commits, only where one is officially published (Gemini, Grok and Buffy publish none, so no record was invented); the Template gained the `Co-authored-by: Name <email>` field shape.
- This specification's CONTRIBUTORS.md section: the inline example block was replaced by a pointer to the repository's own CONTRIBUTORS.md so no duplicated, cached copy of the data exists to drift, and a new commit-time paragraph fixes the conventions — `[eMail]` as correspondence address, trailers in exact `Name <email>` form under Tools entries only, model attribution recorded only in changelog `Contributors` bullets as `{ModelName} via {ToolName}`, and never inventing a missing trailer.

#### Deliberation
- Trailers were first recorded under model entries, then moved once a trailer was recognized as the host agent's identity — matching this specification's own rule that the host tool is recorded under Tools, not under the model Name (Omid Hekayati — claimed, decided).
- Keeping the guidance inside CONTRIBUTORS.md would have duplicated convention beside data; it now lives in this section, and the example points at the live file instead of caching its shape (Omid Hekayati — decided; Mimo — agreed, applied).

---

### CONTRIBUTORS.md restructured to person headings; brands and tools subordinated
- Time: 2026-09-23T12:57:22Z
- Type: Changed
- Cited:
  - Owner session — Evidence: legal entity names, contacts, and trailers of the fourteen entities verified against official terms, privacy, and contact pages; the Super Z brand has no official public source and is recorded as a project-local name.
- Propagates to:
  - CONTRIBUTORS.md: Done — restructured to person `##` headings with brands and tools as owning-entity `###` sections; `# Tools` removed.
  - docs/documentation-changelog.md: Done — § CONTRIBUTORS.md, the host-tool and commit-time sentences, and the entry field's `via` updated to the person rule.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — researched, drafted

#### What changed
- CONTRIBUTORS.md: every `##` heading is now a person — natural or legal — carrying a short recognizable name with a `Full Legal Name` bullet, and an `Alias Legal Name` bullet only where more than one entity could claim the contribution (OpenAI, Zhipu, Xiaomi); former brand headings (ChatGPT, Claude, Gemini, Super Z, Qwen, Grok, Composer, Mimo, Meta AI) and every former Tools heading (VS Code, Codex, ZCode, OpenCode, Cursor, Hermes, Buffy) became `###` sections under their owning person with all historical slugs preserved, Copilot's trailer moved from under VS Code to its own `###` under GitHub, correspondence emails deduplicated to their single most specific owner, and the `# Tools` section removed; every `###` section gained a one-line `Bio` stating what it is, and the Template was rebuilt to the real two-level shape — person bullets at `##`, a `### {Brand}` shape carrying Models, and a `### {Tool}` shape carrying the `Co-authored-by:` trailer where it actually lives.
- This specification's CONTRIBUTORS.md section: the heading rule now describes persons with `Full Legal Name`/`Alias Legal Name` and `###` subordination of brands and tools; "recorded in Tools below" became "its own `###` section under the owning entity"; commit-time trailers are recorded "in the owning tool's `###` section only"; the entry field's `via` keeps the tool's own name as its label, linked to that tool's `###` section inside the owning entity's entry (template line included); each `###` section now opens with a one-line `Bio` stating what the section is.
- Existing `Contributors` bullets across the repository were migrated to the linked shape — 65 tool names linked as `via [{ToolName}](../../../../docs/…#{tool})` across 31 files — and seven `CONTRIBUTORS.md` links carrying a wrong `../../` prefix were corrected to resolve to the file; forms with no recorded section (`via the OpenCode agent`, six occurrences) and inline-code spans were left untouched, by a dry-run-first, idempotent migration script.

#### Deliberation
- The three propositions — every `##` a person with brands as `###` sub-sections, `# Tools` dropped, and `via` retargeted to the owning entity — were taken to consultation and adopted after a counter-opinion on answering-brand linking was weighed (Omid Hekayati — claimed, argued, decided).
- Heading form (short name with a `Full Legal Name` bullet, `Alias Legal Name` only under doubt) and `via` label = tool name were fixed by a question round rather than guessed (Omid Hekayati — decided).
- Review feedback: `###` sections like ZCode were opaque about what they are, and the Template misplaced `Co-authored-by:` at person level — a one-line `Bio` was added to every `###` section and the Template rebuilt to the real person/brand/tool structure (Omid Hekayati — requested, decided; Mimo — applied).

---

### Stealth models recorded in CONTRIBUTORS.md; attribution shape and character encoding repaired
- Time: 2026-09-30T06:12:02Z
- Type: Changed
- Cited:
  - [Stealth Models](https://stealthmodels.com/) - Evidence: the field guide that publishes models under a codename before their developer is disclosed, the entity under which this project records the codenames it ran under.
  - [Space Bunny Alpha](https://spacebunnyalpha.com/) - Evidence: the codename's own guide, its OpenCode connection, and the unconfirmed state of the developer behind it.
  - [Ox Alpha](https://stealthmodels.com/ox-alpha/) - Evidence: the codename's own guide and the reveal that ties the codename to the model recorded under `Super Z`.
- Propagates to:
  - CONTRIBUTORS.md: Done — `## Stealth Models` gained its `Bio` and two `###` sections, `Ox Alpha` carrying only a `Revealed as` field pointing at the section its contributions are recorded under, and `Space Bunny Alpha` carrying the identifier this project runs the model under.
  - docs/type.changelog.md, docs/content.changelog.md, docs/khayyam/khayyam.changelog.md, docs/khayyam/modularity.changelog.md, docs/protocols/computer/compiler.changelog.md, docs/protocols/token.changelog.md, modules/khayyam/display/display.research.001.md, modules/khayyam/targets/js/target.changelog.md: Done — every bullet that named the host tool where the model belonged now names the model and links to its `###` section.
  - modules/khayyam/display/display.research.002.md: Done — its Researcher line named the host tool and no model; the owner confirmed which model wrote the record, so the line names it.
  - docs/khayyam/abstraction.changelog.md, docs/khayyam/agency.changelog.md, docs/khayyam/encapsulation.changelog.md, docs/khayyam/inheritance.changelog.md, docs/khayyam/method.changelog.md, docs/khayyam/variable.changelog.md: Done — `[OpenCode] (qwen3.8-flash)` became `[Qwen] (qwen3.8-flash via [OpenCode])`.
  - modules/khayyam/execution.research.001.md: Done — the Researcher line naming the host tool with `mimo-v2.6-flash` now names Mimo.
  - docs/protocols/computer/os.changelog.md: Done — a `[Qwen] (qwen3.8-flash)` bullet with no host tool gained the `via` field every other bullet of that model carries.
  - docs/documentation.changelog.md, docs/type.changelog.md, docs/khayyam/agency.changelog.md, docs/khayyam/encapsulation.changelog.md, docs/khayyam/khayyam.changelog.md, docs/khayyam/method.changelog.md, docs/khayyam/polymorphism.changelog.md, docs/protocols/process/control-flow.changelog.md: Done — 24 bullets whose `via` field named the host tool as plain text now link it to that tool's `###` section.
  - docs/protocols/computer/lexer.changelog.md, docs/protocols/computer/compiler.changelog.md: Done — the stray comma inside `(GLM-5.3-Flash, via OpenCode)` removed, so the entry field reads as the shape this specification states.
  - docs/protocols/token.changelog.md: Done — its `Pending` propagation for a missing contributor entry is now `Done`.
  - docs/protocols/token.md, modules/khayyam/lsp/lsp.handoff.md, bundles/khayyam/lsp/tests/definition-across-inclusion.test.ts, bundles/khayyam/lsp/tests/definition-fixture.ts, modules/khayyam/rules/lifecycle-method-names/lifecycle-method-names.md, modules/khayyam/rules/lifecycle-method-names/lifecycle-method-names.handoff.md: Done — text written through a byte-level decode that mangled every non-ASCII character; the em dashes, arrows, and quotation marks across the six files restored to the characters they stand for.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
- CONTRIBUTORS.md: `## Stealth Models` now states what the field guide is, and the two codenames this project ran under sit under it as `###` sections. `Ox Alpha` carries a `Revealed as` field pointing at `Super Z` and no `Models` list, because a codename is not a model: the contributions made while it stood for a model are recorded in this repository under the name it was revealed as, and a reader arriving at either name needs the other. `Space Bunny Alpha` carries the one identifier this project runs the model under. The label a bullet carries is the codename or brand, so `#space-bunny-alpha` and `#ox-alpha` are the anchors its bullets resolve to.
- Nine attribution bullets across eight files named the host tool or the legal person where the model belonged, and one of them named a section that does not exist. Each now names the model and links to its `###` section, with the host tool kept in the `via` field: `[OpenCode] (opencode/space-bunny)`, `[OpenCode] (space-bunny via OpenCode)`, `[Space Bunny Free](#space-bunny)`, `[Anomaly Innovations](../../../../docs/…#anomaly-innovations) (space-bunny via OpenCode)`, and `Space Bunny Alpha (space-bunny via OpenCode)` all became `[Space Bunny Alpha](../../../../docs/…#space-bunny-alpha) ({ModelName} via [OpenCode](../../../../docs/…#opencode))`. The three prose attributions that named the host tool inline — `opencode/space-bunny` — now name the model, which is the form this specification's inline-attribution paragraph uses.
- Seven bullets in the Khayyam folder carried `[OpenCode] (qwen3.8-flash)`, one research record's Researcher line carried `[OpenCode]` with `mimo-v2.6-flash`, and a second research record's Researcher line named the host tool with no model at all; each now names its model.
- Twenty-four bullets across eleven files left the host tool in the `via` field as plain text where this specification states the label stays the tool's own name linked to its `###` section; each now carries that link, and one `[Qwen]` bullet that recorded no host at all gained the field.
- Six files carried every em dash, arrow, and curly quotation mark as the two- and three-character sequence a byte-level decode produces. Each was restored from that sequence back to the character it stands for, and the repository now holds no sequence of that shape outside build output.
- docs/protocols/token.changelog.md's propagation for the contributor entry this chat's work needed was `Pending`; it is `Done`.

#### Considered and not done
- A `Full Legal Name` bullet for Stealth Models — rejected: the site describes itself as an independent field guide from the team behind Demodokos and names no person or company, so any entry would be invented.
- Putting the codename back into the entries that ran under it, and linking the `(ox-alpha)` prose attributions in `type.changelog.md` to the new section — not taken: the owner keeps the revealed name in the entries and the codename in this file, so each side points at the other once.
- Repairing the character encoding inside `modules/khayyam/targets/js/build/` — not taken: that is generated output, not a source file, and the next build rewrites it.
- Linking the host tool inside the prose of `superpowers.md`, `sdk.changelog.md`, and `chapar.md` — not taken: those sentences are narrative rather than `Contributors` bullets, so the entry field's shape does not govern them.
- Linking the `space-bunny` identifier to a documentation page — rejected: OpenCode's model documentation names no page for it, and the field guide's own page is already the section's `Website`.

---

### Approval requires a reviewer who did not do the work
- Time: 2026-10-04T00:00:00Z
- Type: Added
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](../../../../docs/comparisons/spec-kit.001.md) - **Reference**: whose Adapt filter produced the item. Spec Kit's `/converge` states "completion claims are not evidence" for its progress markers, which Memar had as a principle for expectations and not as a rule about who may judge a change.
- Propagates to:
  - [documentation-changelog.practice.md](./changelog.practice.md): Done - the procedure that carries out the rule, kept beside the facet rather than in any agent skill, because the conditions bind whoever writes the entry and a rule that lives in the tooling disappears with the tooling.
  - [.agents/skills/memar/SKILL.md](../../../../.agents/skills/memar/SKILL.md): Done - one clause naming which reviewer this runtime supplies, and nothing else. The first draft of this work put the whole rule there, which was wrong in a way worth recording: it made a facet's obligation depend on a skill that a future server or MCP transport would not have. That file carries no changelog of its own.
  - [terminology.md](../../../../docs/terminology.md): None needed - [On Independent Verification, Today](../../../../docs/terminology.md#on-independent-verification-today) already says what an internal audit is worth against an outside institution, and this entry cites that limit rather than restating it.
  - [documentation-explanation.md](../explanation/explanation.md): None needed - no document-structure rule changes.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided the two-role arrangement
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - drafted

#### What changed
- [Contributors (entry field)](./changelog.md#contributors-entry-field) gains [Approval Requires a Reviewer Who Did Not Do the Work](./changelog.md#approval-requires-a-reviewer-who-did-not-do-the-work). `approved` is separated from the rest of the open role vocabulary because it is the one tag that judges the entry's own correctness rather than describing a contribution, and three conditions now hold it: the reviewer did not do the work, the reviewer returns a verdict naming what it ran and what the run returned, and no verdict means no `approved` - a withheld verdict goes into the entry with its reason, and an unapproved entry is the correct state for unchecked work rather than a gap to tidy.
- An approved entry therefore names two roles where an unapproved one names only the first: the party that did the work and the party that said it holds. The section states why that separation is the whole content of the tag, since without it `approved` records that someone was satisfied, which the word "satisfied" already says.
- The section states what the tag is not. An audit by a party that did not do the work, using evidence it ran itself, is the strongest scrutiny available inside one collaboration, and this is not a certificate: the tag records that a second party checked, not that the work is correct in general.
- [Documentation Changelog Practice → Recording an approval](./changelog.practice.md#recording-an-approval) states how the rule is satisfied: which changes are worth reviewing at all, the four things a review request carries (the claim quoted from `What changed`, the evidence as a command to be run, the boundaries, and the verdict asked for), the three outcomes and what each does to the entry, and why a changed claim goes to a different reviewer rather than back to the same one. It also states who reviews: independence from the work is the requirement, not a roster, so where a runtime offers no second cognitive system the honest outcome is no `approved`.

#### Considered and not done
- **Letting the session's own agent approve from its task report (rejected by the owner):** the task report is written by the party the approval would judge, so it is the unverified claim wearing a verified one's name. This is the point Spec Kit's `/converge` makes about its own checkboxes, applied to the party rather than to the marker.
- **Adding a third role - an owner who issues the certificate after the internal audit (not added):** the two-role form the owner described is what is implemented. Whether an outside signature is wanted on top of it is a separate question and would be a change to [Terminology " + chr(0x2192) + " On Independent Verification, Today](../../../../docs/terminology.md#on-independent-verification-today), not to this field.
- **A closed role taxonomy for the vocabulary (rejected for now, unchanged):** the section still says the vocabulary is open. Fixing it is a separate decision, and the approval rule does not depend on it.
- **Requiring the reviewer to be a different *kind* of participant (a human, or a specific model) (rejected):** what the rule needs is independence from the work, not a roster. Naming a roster would make the tag unavailable whenever the roster is unavailable, which is most of the time.

---

### The dot-boundary entry leaves the changelog handoff; Changelog scope states the criterion
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation-changelog.handoff.md: Done - the companion-naming dot-boundary entry was removed; Changelog scope states the criterion and names the counter-example (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- *The dot-boundary criterion for companion naming* left `## Open Questions`: [documentation-changelog.md -> Changelog scope](./changelog.md#changelog-scope) gives the criterion and its counter-example - "the companion rule keys on the **dot** ... and does not reach hyphenated standalone documents that merely end in 'practice' or similar", with `documentation-practice.md` named as the standing counter-example.

#### Considered and not done
- A derivability test for a hypothetical name falling between the two patterns was not added to the section (Space Bunny Alpha - argued). The section already states the discriminator and the exclusion, so a name is classified by a stated rule rather than by case-by-case judgment; no real case exists from which a further criterion could be derived.

---

### A verdict is the reviewer's comparison; a command is its strongest evidence, not the only admissible one
- Time: 2026-10-05T17:20:58Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Approval Requires a Reviewer Who Did Not Do the Work](./changelog.md#approval-requires-a-reviewer-who-did-not-do-the-work), condition 2, defines a verdict as the reviewer's own comparison of what now holds against what the entry claims, naming what it examined and what it found, and naming a command and its output where one can show the claim false. A verdict may rest on reading alone where reading decides the claim; what still disqualifies an opinion is that it names nothing examined.
- That condition now says in terms what keeps the tag from becoming self-certification: the first condition, the reviewer's independence from the work, not the presence of a command. The tag is narrowed only in what a verdict may rest on.
- The closing paragraph's "using evidence it ran itself" becomes "over evidence it gathered and weighed itself", so the document no longer describes every audit as command-backed when condition 2 no longer requires one.
- [documentation-changelog.practice.md → Recording an approval](./changelog.practice.md#recording-an-approval) follows: step 1 no longer rules a reading-decided change out of review, only out of the second party's usual cost; step 2's evidence bullet asks for the command where one exists and the passages to read where reading decides, and a brief naming neither now produces the bare opinion that establishes nothing; and the *Permitted* outcome asks the entry to record what the verdict examined and found, so a later reader weighs the same evidence and reaches the verdict in its own mind rather than re-running in place of judging.
- [documentation-changelog.practice.md → What this is not](./changelog.practice.md#what-this-is-not) carries the same correction to its first sentence.

#### Considered and not done
- Weakening condition 1, or making a reviewer of a reading-decided change cheaper to skip: the load-bearing half of the tag is that the party that did the work may not judge it, and nothing here touches that. An opinion remains worthless when it names nothing examined, so the tag records a comparison rather than a feeling.
- Dropping the requirement that an approved entry record what was examined: without it the later reader inherits the verdict instead of the evidence, which is the substitution this change was made to stop.

---

### A placement audit of every changelog in the repository, and the four routing gaps it exposed
- Time: 2026-10-10T05:17:06Z
- Type: Added
- Propagates to:
  - [documentation-changelog.handoff.md](./changelog.handoff.md): Done — carries the four new open questions and the two new anticipated-work items the audit produced.
  - `bundles/khayyam/rules/import-address/import-address.changelog.md`: Done — an entry recording a change to `docs/khayyam/modularity.md` left this rule's ledger.
  - `docs/khayyam/modularity.changelog.md`: Done — holds that entry.
  - `docs/khayyam/khayyam.changelog.md`: Done — holds an entry recording a change to `khayyam.practice.md`, misplaced from `encapsulation.changelog.md`.
  - `docs/modules/net/networking.changelog.md`: Done — holds an entry recording a change to `networking.md`, misplaced from `giti.changelog.md`.
  - [modularity.changelog.md](../../modularity/modularity.changelog.md): Done — no longer holds the entry recording a rename inside the `modules/` tree, which moved to that tree's own ledger.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — asked for the audit, reported misplaced records in `cognition.changelog.md`
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — delegated, audited, applied
- Related work:
  - [Documentation Practice](../documentation.practice.md) → *Results and companions* — the routing rule the audit judged every entry against
  - [Documentation — Changelog](./changelog.md) → *Changelog scope*, *Changelog membership*, *Trivial changes*, *Session consolidation* — the four rules that decide scope, admission, deletion, and how many entries one session writes
  - [Content](../../content/content.md), [Modeling](../../../../docs/modeling.md), [Process](../../../process/process.md), [System](../../../../docs/system.md), [Knowledge](../../knowledge.md), [Cognition](../../../../docs/cognition.md), [Framework](../../../../docs/framework.md) — the base artifacts whose ledgers were audited

#### What changed
- Every changelog in `docs/` and in the Khayyam bundle was audited entry by entry against the routing rule: roughly 560 entries across 77 files, each judged once. Three entries were found misplaced with an unambiguous destination and moved, each keeping its text and gaining one clause recording the file it was first written on: an entry recording a change to `docs/khayyam/modularity.md` from `import-address.changelog.md`; an entry recording where the `Field_UserUUID` procedure lives from `encapsulation.changelog.md` to `khayyam.changelog.md`; and *Added Edge computing as a Networking-level architectural principle* from `giti.changelog.md` to `networking.changelog.md`. An entry recording a rename inside the `modules/` tree left `modularity.changelog.md` for the tree's own README ledger.
- Five entries were deleted as trivial under *Trivial changes*: a link repair that the entry itself calls mechanical with no change to any claim; an anchor repair inside a frozen audit record whose `Action` reads `None`; a correction of three statements the specification's own rule already required; a verbatim duplicate sentence; and a same-session migration that was undone the same chat, leaving its document byte-identical to before.
- Four entries whose subject is genuinely more than one artifact were left where they stand and are now open questions rather than silent judgement calls: they are listed by title in the handoff.
- The owner's report that `cognition.changelog.md` had recently received records about other artifacts was checked and not supported: no entry in that file records a change to another artifact, and the file is byte-identical to HEAD.

#### Deliberation
- A propagation an entry names under `Propagates to` does not make the entry misplaced: what decides is what the change changed. Several entries across the audit write into a protocol document under `docs/modules/` or a rule under `bundles/khayyam/` while remaining correctly placed on their base artifact's ledger, and each was kept on that ground (Space Bunny Alpha — ruled for the audit).
- A companion document gets no changelog of its own under *Changelog scope*, so an entry recording only a `.practice.md`, `.handoff.md`, or `.research.NNN.md` change belongs on the base artifact's ledger. This is why `documentation-handoff.changelog.md` correctly holds three entries about `documentation-handoff.practice.md`, a shape a prior report had flagged as suspect (Space Bunny Alpha — checked against the rule).
- *Stale propagation paths are not misplacement.* The moves of `docs/protocols/` to `docs/modules/` and `modules/khayyam/` to `bundles/khayyam/` left 27 dead paths in the `docs/modules/computer/` ledgers alone; every audit left them for a repair pass and counted them instead (Space Bunny Alpha — ruled for the audit).

#### Considered and not done
- **Moving an entry with no single destination (not done)**: four such entries were reported instead, because a move needs a destination and the rule does not supply a tie-breaker for a change with no single subject (Space Bunny Alpha — reported).
- **Collapsing the moved Edge-computing entry into the one already at its destination (not done)**: the two carry the same timestamp and the same topic, and merging would have edited an entry outside the audit's remit; the question is now recorded (Space Bunny Alpha — reported).
- **Repairing the f-string fragments inside two entries (not done)**: `" + chr(0x2192) + "` in this topic's ledger and `" + chr(0x2014) + "` in `../process.changelog.md` are link-text defects inside entries that are correctly placed and not trivial, which no current rule reaches; the rule question is now recorded (Space Bunny Alpha — reported).
- **Repairing the dead propagation paths (not done)**: a separate pass over ledgers, not an audit of entries (Space Bunny Alpha — noted).

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:48:00Z
- Type: Changed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - reviewed, revised

#### What changed
- Reviewed the uncommitted change to `documentation-changelog.md`, `documentation-changelog.practice.md`, `documentation-changelog.handoff.md` and this ledger against HEAD. The link retarget in `documentation-changelog.md` (`protocols/process/test.md` to `modules/process/test.md`) resolves and needed no change. The `Recording an approval` rewording in the practice document is the change recorded by the entry that precedes the placement-audit entry, and it holds with what that entry says; it was not altered. The handoff's removed *dot-boundary* question was already recorded as answered by *The dot-boundary entry leaves the changelog handoff; Changelog scope states the criterion*, and the criterion is in `documentation-changelog.md` under Changelog scope, so that removal loses nothing.
- Fixed in the placement-audit entry in this file: the `Related work` line's seven links were written `[Content(./content.md)` and did not render as links, and now read `[Content](../../content/content.md)`; the blank line before `#### What changed`, `#### Deliberation` and `#### Considered and not done` was missing, unlike every other entry; one `Propagates to` link text began `../../bundles/` while its target (correctly) began `../bundles/`, and three others carried `../` text over `./` targets, and their texts now match their targets.
- Fixed in `documentation-changelog.handoff.md`: the Anticipated Work item *Pending queue triage, blocking rule, and traceability surface* said nothing triages the Pending queue (61 at last report) and that answering "which documents depend on this one" needed full-text search. [Spec Kit comparison](../../../../docs/comparisons/spec-kit.001.md), section 12, records the queue triaged (18 discharged, 5 re-pointed, 37 kept open), `check` now reports 52 undischarged, and the `backlinks` and `obligations` verbs exist. The item is rewritten as *Pending queue: blocking ruling, enforcement, and traceability surface*, keeping what is still undecided.
- Not checked: the audit entry's counts (about 560 entries, 77 files), the byte-identity of `cognition.changelog.md` to HEAD at the time of the audit (the file now differs through another session's work), and the two open questions' line citations beyond `documentation-changelog.changelog.md:336`.

---

### Dead links in recorded entries are repaired; a question recorded only to be remembered needs no entry
- Time: 2026-10-12T10:57:14Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- New section [Links in recorded entries](./changelog.md#links-in-recorded-entries): an entry's prose is history, its links are not. A dead link is repointed where its target moved, and turned into plain text where the target no longer exists, so no reader or check asks about it again.
- [Trivial changes](./changelog.md#trivial-changes) gains *A question recorded so it is not forgotten*: adding a stated, unevaluated question to a handoff receives no changelog entry, unless the addition carries a decision (alternatives weighed, a question narrowed, merged, or replaced). Removing a question is never covered.
- Applied the first rule: links to the retired `.agents/scripts/memar-content.py`, `tests/memar-content.py` and `tests/memar-install.py` in cognition, documentation and test changelogs now point at their successors under `.agents/scripts/services/`; the two links to cognition.md's removed *Grouping Notes* heading are now plain text.

#### Considered and not done
- **Teaching `memar content check` to skip dead links inside changelogs (rejected)**: whether a target moved or vanished is a judgment the check cannot make; repairing the link once removes the question for everyone.

---

### Practice description states a boundary
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- `documentation-changelog.practice.md`'s `description` now states what it is not: the field shapes, state vocabulary, and approval rule, and where an unfinished withheld verdict goes, which [Documentation — Practice → Description quality criteria](../practice/practice.md#description-quality-criteria) requires.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.

---

### The Changelog facet's definition moves here from documentation.md
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - modules/content/documentation/documentation.md: Done (task `20261016-T150928Z-4276`) - the passage this entry moved here no longer stands there.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Reader relationship](./changelog.md#reader-relationship): the definition `documentation.md` held for this facet moved here — the content consulted to audit history, an append-only record of one paired artifact. The note that the facet absorbs what base documents' front matter and `Change Rationale` once held, and the exception that a Changelog-facet file gets no companion of its own while this specification does, were already stated in this specification and were merged, not repeated.
- The sentence that named the Handoff and Research relationships now points at their own sections.
- Made in task 20261016-T150928Z-4276, finishing answer 6 of the owner's rulings of 2026-10-16: a new facet edits only its own module.

#### Considered and not done
- **Restating the other facets' reader relationships here to contrast this one with them**: each facet's own specification states its relationship, and a restatement is a second place to edit when one changes; this specification points at the other's section instead.

---

### The facet's closed lists leave the specification for their types
- Time: 2026-10-17T12:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The three relations of a task reference are no longer listed in [Tasks](./changelog.md#tasks) (`TaskRelation`). The propagation states (`PropagationState`), the entry sections (`EntrySection`) and the role tags code reads (`ContributorRole`, an open vocabulary) are typed; their prose is unchanged.
- Why: the owner ruled on 2026-10-16 that every field a facet declares is a type, and that once typed the prose restating it leaves the document, keeping the reason ([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)); the types are in this facet's `primitive/`.
- Made in task 20261016-T194831Z-4504.
