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

#### Summary
Created as the governing specification for the Changelog facet, defining: the `<base>.changelog.md` companion-file convention; the entry structure (short descriptive title, metadata bullets for `Time`/`Type`/`Cited`/`Propagates to`/`Tasks`/`Contributors`, followed by `Summary` and optional `Rationale and alternatives` as prose headings); the project-wide `CONTRIBUTORS.md` registry; and the absorption of base documents' former `Citations`, `Contributors`, and `Applied to` front-matter fields (and `## Change Rationale` body section) into this facet.

#### Rationale and alternatives
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

#### Summary
The `### Cited` section previously defined the full Relation vocabulary inline and gave per-relation guidance (notably for the new `Evidence` relation). That content was duplicated from where it now lives authoritatively — `documentation.md → Citations`, added as a cross-cutting concern in the same round of changes. The section was trimmed to keep only the Changelog-specific rules: that a `Cited` entry replaces the base artifact's former `Citations` field; that citing a source here is sufficient provenance (no need to repeat it in the base artifact's body); and the one exception — if the base artifact's own body genuinely needs a source at the point a reader is reading it, link it inline as a normal hyperlink, never as an unlinked "see X" pointer.

#### Rationale and alternatives
- **Keep the full Relation vocabulary inline in this specification (rejected)**: would have required keeping two definitions in sync — the one here and the one in `documentation.md → Citations` — every time the vocabulary changed. With `Evidence` just added and the `Reference`/`Depends_on` boundary still an open Unresolved question, the vocabulary is not yet stable enough to risk duplication drift.
- **Move the Relation vocabulary here and have `documentation.md` reference this file (considered, not chosen)**: would have made the Changelog spec the canonical home for a concern that is not Changelog-specific. The vocabulary applies wherever citations appear — currently Changelog, potentially a future Research facet — so its canonical home is the meta-layer, not any one facet's spec.
