# Documentation — Explanation Practice Changelog
This document records why and how `documentation-explanation.practice.md` changed over time. See [Documentation — Changelog](./documentation-changelog.md) for what this file's structure means.

## Changelog

### Initial specification
- Time: 2026-07-25T00:00:00Z (approximate — historical import)
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: this Skill file is the procedure for producing an Explanation-facet document; the structure it produces is defined by that specification, not repeated here.
  - [Documentation](./documentation.md) — Reference: the meta-layer that defines what a Facet is and why Practice-facet files exist alongside Explanation-facet specifications.
- Contributors:
  - See the project-wide [CONTRIBUTORS.md](../CONTRIBUTORS.md) registry.

#### Summary
Created as the Practice-facet companion to `documentation-explanation.md`, following the Practice facet's schema (name/description-only frontmatter, imperative body, under ~500 lines). Walks a contributor through producing a new Explanation-facet document: copying the template, generating the `ID`, filling in front matter, writing the body, and progressive migration of older documents.

### Aligned with the post-Changelog-facet specification
- Time: 2026-08-11T00:00:00Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: the base specification's body skeleton dropped `Change Rationale` and the `Applied to`/`Citations`/`Contributors` front-matter fields as part of the Changelog-facet migration; this Skill file was updated to match.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: step 6 of the procedure now creates a paired Changelog-facet file, whose structure is defined by this specification.
  - [Documentation](./documentation.md) — Reference: added to the Reference files list because the cross-cutting Citations and URI conventions now live there, and a contributor following this procedure may need to consult them.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: pointed out that this Skill file had been missed during the earlier round of changes that moved provenance out of Explanation-facet base documents into the Changelog facet; the procedure was still telling a contributor to fill in `Applied to`, `Citations`, and `Contributors` in the front matter and to keep a `## Change Rationale` body section, all of which the base specification no longer permits.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: removed `Applied to`, `Citations`, `Contributors` from step 3's front-matter instructions and from the Template code block; removed `## Change Rationale` from the Template code block; removed step 4's mention of the obsolete "Guide" topic convention (an internal topic optionally linked from Abstract, now replaced by the Practice facet's companion-file convention); added a new step 6 instructing the contributor to create the paired `<base>.changelog.md` file and, when revising an older document, to migrate its former provenance fields into Changelog entries; added `documentation-changelog.md` to the Reference files list.

#### Summary
This Skill file was missed when the Changelog-facet migration was applied to the rest of the documentation set in the previous round of changes. The procedure was still instructing a contributor to fill in `Applied to`, `Citations`, and `Contributors` in the base document's front matter and to keep a `## Change Rationale` body section — all of which the base specification (`documentation-explanation.md`) no longer permits, since provenance now lives in the paired Changelog-facet file. The file was brought in line with the current specification: the front-matter instructions now cover only `Title`, `Status`, `Start Date`, `ID`; the Template code block drops `Applied to`, `Citations`, `Contributors`, and `## Change Rationale`; the obsolete "Guide" topic convention (an internal topic optionally linked from Abstract) was removed from step 4, since procedural content now belongs in this Practice-facet companion file rather than an internal topic; a new step 6 was added instructing the contributor to create the paired `<base>.changelog.md` file (and, when revising an older document, to migrate its former provenance fields into Changelog entries); and the Reference files list now includes `documentation-changelog.md` and `documentation.md`.

#### Rationale and alternatives
- **Keep the "Guide" topic convention in step 4 (rejected)**: the base specification's `documentation-explanation.changelog.md` records that the Guide/optional-topic mechanism was removed in favor of the Practice facet's companion-file convention (`<base>.practice.md`), since every document that needs how-to content now gets one automatically via the Practice facet, with no per-document naming decision required. A Skill file is itself the Practice-facet companion — instructing the contributor to also create an internal "Guide" topic in the base document would re-introduce the obsolete convention this very file replaces.
- **Inline the full Changelog entry structure in step 6 (considered, not chosen)**: would have duplicated the entry structure (Time, Type, Cited, Propagates to, Tasks, Contributors, Summary, Rationale and alternatives) from `documentation-changelog.md`, creating a sync obligation every time that structure changes. Step 6 instead points to `documentation-changelog.md` for the structure, keeping this Skill file focused on what is specific to producing an Explanation-facet document.
- **Add the URI rule inline in the Template (rejected)**: the URI format (absolute vs. relative reference, the `file:` scheme prohibition) is now a cross-cutting convention defined in `documentation.md → URI`. Adding it here would duplicate the rule; a contributor who needs it can follow the Reference files link to `documentation.md`.
