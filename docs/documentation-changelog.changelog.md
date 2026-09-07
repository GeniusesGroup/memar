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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: identified the need to move provenance out of base documents into companion history files; directed adopting the Facet pattern for the Changelog rather than leaving it as ad-hoc convention.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: drafted the initial Changelog facet specification, including the entry structure, CONTRIBUTORS.md mechanism, and propagation tracking.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: refined the specification across multiple rounds; added the `Evidence` relation to the Cited vocabulary; clarified the exception that Changelog-facet files do not themselves get companion changelogs.

#### What changed
Created as the governing specification for the Changelog facet, defining: the `<base>.changelog.md` companion-file convention; the entry structure (short descriptive title, metadata bullets for `Time`/`Type`/`Cited`/`Propagates to`/`Tasks`/`Contributors`, followed by `Summary` and optional `Rationale and alternatives` as prose headings); the project-wide `CONTRIBUTORS.md` registry; and the absorption of base documents' former `Citations`, `Contributors`, and `Applied to` front-matter fields (and `## Change Rationale` body section) into this facet.

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: the `### Cited` section in this specification was carrying two different kinds of content — Changelog-specific format rules, and the general citation vocabulary and source-selection criteria that any facet needing citations would also need. The latter does not belong here; it belongs in the meta-layer so a future facet inherits it without redefinition.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: trimmed `### Cited` from two paragraphs to one, removing the inline Relation vocabulary enumeration and the per-relation guidance for `Evidence`; replaced them with a reference to `documentation.md → Citations`. Kept only what is specific to a Changelog entry's `Cited` field: the "replaces former Citations field" framing, the "cite here is sufficient provenance" rule, and the inline-hyperlink exception for sources the base artifact's own body genuinely needs at the point of reading.

#### What changed
The `### Cited` section previously defined the full Relation vocabulary inline and gave per-relation guidance (notably for the new `Evidence` relation). That content was duplicated from where it now lives authoritatively — `documentation.md → Citations`, added as a cross-cutting concern in the same round of changes. The section was trimmed to keep only the Changelog-specific rules: that a `Cited` entry replaces the base artifact's former `Citations` field; that citing a source here is sufficient provenance (no need to repeat it in the base artifact's body); and the one exception — if the base artifact's own body genuinely needs a source at the point a reader is reading it, link it inline as a normal hyperlink, never as an unlinked "see X" pointer.

#### Considered and not done
- **Keep the full Relation vocabulary inline in this specification (rejected)**: would have required keeping two definitions in sync — the one here and the one in `documentation.md → Citations` — every time the vocabulary changed. With `Evidence` just added and the `Reference`/`Depends_on` boundary still an open Unresolved question, the vocabulary is not yet stable enough to risk duplication drift.
- **Move the Relation vocabulary here and have `documentation.md` reference this file (considered, not chosen)**: would have made the Changelog spec the canonical home for a concern that is not Changelog-specific. The vocabulary applies wherever citations appear — currently Changelog, potentially a future Research facet — so its canonical home is the meta-layer, not any one facet's spec.

### Scoped the changelog to the base artifact; practice companions share it
- Time: 2026-09-01T14:34:32Z
- Type: Changed
- Cited:
  - [Documentation — Explanation Changelog](./documentation-explanation.changelog.md) — Evidence: the worked case for the change — the retired `documentation-explanation.practice.changelog.md` recorded its practice file's changes as alignments forced by base-document changes, demonstrating that base and companion changes are one narrative rather than two.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: one changelog per topic, not one per file — fewer documents, and the changes to a base document and its practice companion are too closely related to justify two ledgers; noted approvingly that the `thinking` topic had already been handled this way in practice.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
Added the Changelog-scope rule to the specification: a changelog is paired to a base artifact, and the base artifact's `<base>.practice.md` companion records its changes in that same changelog — a practice file never receives a changelog of its own. This supersedes the earlier four-file structure (`<base>.md`, `<base>.practice.md`, `<base>.changelog.md`, `<base>.practice.changelog.md`) — a decision the owner had themselves specified during the Chapar documentation migration (recorded in `chapar.practice.changelog.md`) and now supersedes by their own direction. Existing `.practice.changelog.md` files merge into their base artifact's changelog as a propagation of this change.

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked whether the Models lists should run ascending or descending, and to audit the file's model ordering and add official website links per model where possible.
  - [OpenCode](../CONTRIBUTORS.md#opencode) (Qwen3.8-Flash) — argued, rewrote: recommended ascending (append-only) to match the facet's own entry convention; verified each linked URL by fetching it.

#### What changed
The CONTRIBUTORS.md section now states that an AI contributor's Models list is chronological, oldest first, with new models appended at the end — the same append-only convention as changelog entries, so adding a model never forces a re-sort — and that a model may carry a link to its official documentation page where one exists and has been verified. Applied in CONTRIBUTORS.md: GLM and Qwen lists reversed to ascending; OpenAI, Anthropic, Google DeepMind, Z.ai, and Qwen-collection model pages linked. GLM-5.0 and Qwen3.8-Flash carry no dedicated link because no verifiable per-model page was found, and the previous GLM-5.3-Flash link was removed: it pointed at oxalpha.io, an unrelated third-party model page, not Z.ai.

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
- A separate changelog per practice file (rejected): the coupling between a base specification and its procedure runs one way - so per-file changelogs either duplicate the same change as two entries or split one narrative across two ledgers referencing each other, and they multiply files for no reader benefit. (Omid Hekayati)
- Extend the sharing rule to Handoff companions now (rejected for now): a handoff is mutable working state rather than a procedure, and whether its churn is worth changelog history at all is an open question in the Handoff facet; deciding it here would preempt that question without new evidence. (Omid Hekayati)
- A single `Applied to` field on the base artifact, as before (rejected): could only express "where the current design already landed," not "what changes are still owed elsewhere," and couldn't distinguish which specific change a propagation obligation came from. (Omid Hekayati)
- `Pending`/`Done` only, no `Rejected` (considered, not chosen): a propagation that's considered and deliberately declined would have no way to stop appearing as outstanding work in a future search. (Omid Hekayati)
- Timestamp as the entry's own `###` heading (an earlier draft; not chosen): put a machine-format string where a human-scannable title should be. Time is a fact about the entry, not its identity, so it moved into a `Time` bullet. (Omid Hekayati)
- A `####` heading for every field, including the short metadata ones (an earlier draft; not chosen): for fields that are genuinely metadata rather than content, a heading is more structural weight than the field needs. (Omid Hekayati)
- Giving a Changelog-facet file its own companion changelog (rejected): would recurse indefinitely with no natural stopping point; version control already records what changed in a changelog file itself. (Omid Hekayati)
- Treating Changelog as an ad-hoc per-document convention rather than a named Facet (rejected): once the same pattern was being applied across multiple artifacts, naming it as a Facet was the smaller conceptual cost than leaving it as implicit convention. (Omid Hekayati)

#### Decision
Open questions (dot-boundary criterion, entry-title uniqueness, historical-entry timestamps) moved to the paired handoff. (Omid Hekayati - approved)
