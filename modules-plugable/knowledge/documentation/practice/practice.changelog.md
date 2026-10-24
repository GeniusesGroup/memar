# Documentation — Practice Changelog
This document records why and how `documentation-practice.md` changed over time. See [Documentation — Changelog](../changelog/changelog.md) for what this file's structure means.

## Changelog

### Initial specification
- Time: unknown (historical import — this document's own creation, before this changelog existed)
- Cited:
  - [Documentation](../documentation.md) — Depends_on: this document specifies one facet defined by documentation.md; its own concept of what a facet is, and why Practice is governed separately from Explanation, is defined there, not repeated here.
  - [Documentation — Explanation](../explanation/explanation.md) — Reference: the sister facet specification; cited to make explicit that the two facets share the same meta-layer (documentation.md) but differ in governing structure.
  - [Anthropic Claude skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — Reference: one of three independently-designed real Skill-file conventions this specification's schema is adopted from rather than invented; source for the name/description-only frontmatter rule and the progressive-disclosure loading model.
  - [OpenAI Codex skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) — Reference: independently converges on the same name/description-only frontmatter and progressive-disclosure model as Anthropic's; explicitly lists including a README.md or other auxiliary documentation inside a skill as an anti-pattern, a rule adopted directly in this specification.
  - [Microsoft skill-creator](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) — Reference: a third, independent convergence on the same core schema (name/description, progressive disclosure, scripts/references/assets), despite layering substantial SDK-specific structure on top for its own narrower use case — cited as evidence the core schema, not the SDK-specific layer, is what's actually load-bearing across ecosystems.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../../../../CONTRIBUTORS.md#claude) — rewrote
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
Created as part of splitting the former `documentation.md` into three files. Adopts, rather than invents, the schema independently converged on by Anthropic's, OpenAI's, and Microsoft's own skill-creator Skill files: `name`/`description`-only frontmatter, three-level progressive disclosure, `scripts`/`references`/`assets` bundled resources, and an explicit rule against including auxiliary documentation inside a Skill folder.
- Three independent real Skill-file conventions were fetched and compared; this specification was drafted (Claude).
- Description quality criteria; When to split vs. extend guidance; Reference file naming convention; Body structure guidance were added (Super Z).

#### Deliberation
- The need for a governing specification for Practice-facet files was identified (Omid Hekayati).
- Adopting the real ecosystem convention rather than inventing a new one was directed (Omid Hekayati).

### Migrated Citations, Contributors, and Applied to into this changelog file
- Time: 2026-08-05T08:51:08Z
- Type: Changed
- Contributors:
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
Per the decision to move all provenance (citations, contributor attribution, cross-document propagation tracking) out of base documents and into their paired Changelog-facet file, this document was created. `documentation-practice.md`'s own front-matter `Citations`, `Contributors`, and `Applied to` fields, and its `## Change Rationale` section, were extracted into this file; they are superseded by it and should be removed from the base document (tracked separately — see Propagates to).

#### Propagates to
- `documentation-practice.md`: Done — removed front-matter `Citations`, `Contributors`, `Applied to`; removed `## Change Rationale` section; updated the inline reference to `Citations` in the Discussion's Rationale and alternatives (no longer an active front-matter field of Explanation-facet documents).

---

### Body restructured; discussion content relocated; practice companion expanded per the finalized method
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Propagates to:
  - documentation-practice.handoff.md: Created - this specification's open question and anticipated catalog work moved there.
  - documentation-explanation.md: Done - the method this migration follows was finalized there in the same pass.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) - rewrote, moved

#### What changed
- The document's own body reformed under the finalized Explanation-facet pattern: `## Drawbacks` replaces the former `## Discussion` wrapper, then is itself removed when the method dissolves Drawbacks entirely (Super Z - applied; Omid Hekayati - directed).
- A final audit found the Microsoft prior-art block and the Skills-topic Unresolved question that the earlier passes missed; both recorded below (Super Z - audit and migration).
- The practice companion (`documentation-practice.practice.md`) was expanded from a naming-only stub to a six-step procedure with an edge-cases section, drawn from this specification's Frontmatter, Description quality criteria, Writing style, and Body structure topics; the naming convention for domain-specific practice families was intentionally not retained in the rewritten file, as it covers a different concern (organizing multiple skills within one domain) that belongs in the project's broader Skill-file conventions (Super Z - rewrote; Omid Hekayati - directed the expansion and approved the scope narrowing).

#### Considered and not done
- Design a new, project-specific schema for Skill files (rejected): would produce a fourth, incompatible convention where three independently-converged ones already exist and already work with real tooling - including the AI systems this project relies on to author and use these files. (Super Z - migrated from the body)
- Require Skill files to cite an Explanation-facet document via a `Citations` field when one exists (considered, not chosen): `Citations` is provenance machinery that now lives in the paired Changelog-facet file; requiring it inside a Skill file would reintroduce exactly the apparatus this facet is supposed to avoid. A Skill file's body may still mention a related Explanation-facet document by name in plain prose. Provenance for the Skill file itself, if needed, lives in the Skill's paired Changelog-facet file, not inside the Skill folder. (Super Z - migrated from the body)
- The Skill-file conventions bind this project to a two-field front-matter contract that a future ecosystem revision could change; the convention sources are external and evolve on their own schedule, and this project would have to track that evolution. (Super Z - migrated from the removed Drawbacks section)

#### Related work
- Microsoft's own skill-creator convention layers substantial additional structure on top of the shared core (a fixed section order, mandatory callout blocks, a categorization/symlink system) - but explicitly scopes that additional structure to one narrow sub-case (Azure SDK skills specifically), noting elsewhere that "for domain skills, use your judgment to organize logically." The two-field frontmatter rule itself, unlike the rest of Microsoft's structure, is not qualified this way - it applies universally in all three conventions examined. (Super Z - migrated from the body)

#### Decision
Open work (Skill-file conventions beyond the cited examples; optional-section catalog candidates) moved to the paired handoff. (Omid Hekayati - approved)

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:49:00Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - reviewed

#### What changed
- Reviewed; no change needed. The uncommitted change to this file is the removal of the entry *Rejected positions given a deletion procedure*, which was first written on this file by mistake. It is present, with its text intact and one added clause recording the move, in `documentation.changelog.md` (the ledger of `documentation.practice.md`, the document it changes), so no information is lost. This is the move the placement audit recorded in `documentation-changelog.changelog.md`.

---

### A Practice's name is its file's base name
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- [Frontmatter](./practice.md#frontmatter) now states that `name` is the name of the file it heads: a Practice companion's base name, the part before `.practice.md`, and for a `SKILL.md` the name of its folder. Before, it said only "lowercase with hyphens", and five Practices carried a name that did not follow their file. No Memar document stated the rule; `memar content search` for "base name", "agentskills", and the five names found none.
- `documentation-practice.practice.md`'s front-matter `name` was `document-practice-creator`; it is now `documentation-practice`, the file's base name, as [Documentation — Practice → Frontmatter](./practice.md#frontmatter) now states. No other document referred to the old name. Its description's pointer to `document-explanation-creator` now reads `documentation-explanation`.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.

#### Considered and not done
- Citing agentskills.io as the source of the rule: not done. The plan of this task reports that the format it was adopted from ties a skill's name to its folder, but the specification could not be fetched in this chat (the connection was refused), so the rule is stated on its own reason rather than on a claim not read.

---

### The Practice facet's definition moves here from documentation.md
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - modules/content/documentation/documentation.md: Done (task `20261016-T150928Z-4276`) - the passage this entry moved here no longer stands there.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Reader relationship](./practice.md#reader-relationship): the definition `documentation.md` held for this facet moved here — the content followed to accomplish something, and why its front matter is two fields and its body a procedure. The note that the schema was adopted from three AI ecosystems was already in [Abstract](./practice.md#abstract), so it was merged, not repeated.
- The clause that restated Explanation's relationship now points at Explanation's own section.
- Made in task 20261016-T150928Z-4276, finishing answer 6 of the owner's rulings of 2026-10-16: a new facet edits only its own module.

#### Considered and not done
- **Restating the other facets' reader relationships here to contrast this one with them**: each facet's own specification states its relationship, and a restatement is a second place to edit when one changes; this specification points at the other's section instead.

---

### A practice's front matter stated once
- Time: 2026-10-17T16:00:00Z
- Type: Corrected
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- Step 1 no longer says a practice has no front matter; it has the two fields of the Practice facet and none of the Explanation facet's.
- Why: task 20261016-T095101Z-22960 found the text contradicted the documents and types in use; the owner approved the correction on 2026-10-17.
