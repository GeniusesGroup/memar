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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - rewrote, moved

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
