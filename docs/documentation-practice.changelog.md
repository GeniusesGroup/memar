# Documentation — Practice Changelog
This document records why and how `documentation-practice.md` changed over time. See [Documentation — Changelog](./documentation-changelog.md) for what this file's structure means.

## Changelog

### Initial specification
- Time: unknown (historical import — this document's own creation, before this changelog existed)
- Cited:
  - [Documentation](./documentation.md) — Depends_on: this document specifies one facet defined by documentation.md; its own concept of what a facet is, and why Practice is governed separately from Explanation, is defined there, not repeated here.
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: the sister facet specification; cited to make explicit that the two facets share the same meta-layer (documentation.md) but differ in governing structure.
  - [Anthropic Claude skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — Reference: one of three independently-designed real Skill-file conventions this specification's schema is adopted from rather than invented; source for the name/description-only frontmatter rule and the progressive-disclosure loading model.
  - [OpenAI Codex skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) — Reference: independently converges on the same name/description-only frontmatter and progressive-disclosure model as Anthropic's; explicitly lists including a README.md or other auxiliary documentation inside a skill as an anti-pattern, a rule adopted directly in this specification.
  - [Microsoft skill-creator](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) — Reference: a third, independent convergence on the same core schema (name/description, progressive disclosure, scripts/references/assets), despite layering substantial SDK-specific structure on top for its own narrower use case — cited as evidence the core schema, not the SDK-specific layer, is what's actually load-bearing across ecosystems.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: identified the need for a governing specification for Practice-facet files; directed adopting the real ecosystem convention rather than inventing a new one.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: fetched and compared three independent real Skill-file conventions; drafted this specification.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: added Description quality criteria; added When to split vs. extend guidance; added Reference file naming convention; added Body structure guidance.

#### Summary
Created as part of splitting the former `documentation.md` into three files. Adopts, rather than invents, the schema independently converged on by Anthropic's, OpenAI's, and Microsoft's own skill-creator Skill files: `name`/`description`-only frontmatter, three-level progressive disclosure, `scripts`/`references`/`assets` bundled resources, and an explicit rule against including auxiliary documentation inside a Skill folder.

### Migrated Citations, Contributors, and Applied to into this changelog file
- Time: 2026-08-05T08:51:08Z
- Type: Changed
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: extracted this changelog file from `documentation-practice.md`'s front-matter `Citations`/`Contributors`/`Applied to` and body `## Change Rationale`; flagged the pending base-document cleanup below.

#### Summary
Per the decision to move all provenance (citations, contributor attribution, cross-document propagation tracking) out of base documents and into their paired Changelog-facet file, this document was created. `documentation-practice.md`'s own front-matter `Citations`, `Contributors`, and `Applied to` fields, and its `## Change Rationale` section, are superseded by this file and should be removed from the base document (tracked separately — see Propagates to).

#### Propagates to
- `documentation-practice.md`: Done — removed front-matter `Citations`, `Contributors`, `Applied to`; removed `## Change Rationale` section; updated the inline reference to `Citations` in the Discussion's Rationale and alternatives (no longer an active front-matter field of Explanation-facet documents).
