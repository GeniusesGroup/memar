# Documentation Changelog
This document records why and how `documentation.md` changed over time. See [Documentation — Changelog](./documentation-changelog.md) for what this file's structure means.

## Changelog

### Initial split into three facets
- Time: unknown (historical import — this document's own creation, before this changelog existed)
- Cited:
  - [Diátaxis](https://diataxis.fr/) — Extends: the Facet concept borrows Diátaxis's core insight — that documentation content is categorically different depending on whether the reader is meant to study it or to follow it — and adapts it to this project's own scope and naming. Diátaxis itself identifies four forms (Tutorials, How-to guides, Reference, Explanation); this project initially distinguished two facets (Practice, Explanation), then added Changelog as a third, with the same underlying two-axis principle.
  - [Modeling](./modeling.md) — Depends_on: Documentation is the result of correct modeling. The concept of Documentation cannot be understood or defined independently from the modeling process.
  - [Anthropic Claude skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — Reference: one of three independently-designed real Skill-file conventions examined as evidence for the Practice facet's governing schema.
  - [OpenAI Codex skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) — Reference: second independently-converged real Skill-file convention, explicitly listing inclusion of auxiliary documentation inside a skill as an anti-pattern.
  - [Microsoft skill-creator](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) — Reference: third independently-converged real Skill-file convention, sharing the same core schema despite layering additional SDK-specific structure on top.
  - [Dependency Resolution via File URI and Companion Manifest](./khayyam-dependency_resolution.md) — Reference: the Explanation facet's use of URI for contributor identity and citations follows the same File URI approach already established for dependency resolution.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, directed, proposed
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote
  - [Claude](../CONTRIBUTORS.md#claude) — argued, proposed

#### What changed
- Split the former single `documentation.md` (`RFC Template Specification`, before that the original `rfc-template.md`) into three files: this document, defining what a documentation "Facet" is and listing the Facets currently specified; `documentation-explanation.md`, governing the Explanation facet (the substantive successor of the former single file, keeping its original identity); and `documentation-practice.md`, governing the Practice facet.
- Created as the meta-layer of the three-file documentation architecture, defining the Facet concept (borrowed from Diátaxis), naming the two current facets (Explanation, Practice), and describing how the system extends along Diátaxis's own two-axis model toward Diátaxis's full four-quadrant split (Super Z — wrote the initial `documentation.md` meta-layer).
- Adopted the Practice facet's schema from the independently-converged convention of three real AI ecosystems (Anthropic, OpenAI, Microsoft) rather than inventing a project-specific one.
- Split from the former single `documentation.md` (now `documentation-explanation.md`) after the thirteenth revision of that document showed that procedural and analytical content could no longer share a single governing schema without compromising both.
- `documentation-practice.md` was improved with additional conventions (Super Z).

#### Deliberation
- `RFC`, `PRD`, `ADR`, and similar labels should be profiles applied to one shared documentation structure, not independent document types — following an extended discussion on knowledge management (Omid Hekayati — argued).
- One documentation structure cannot serve both 'studying' and 'following' use cases (Omid Hekayati — identified).
- The three-facet decomposition (documentation.md, documentation-explanation.md, documentation-practice.md) was directed (Omid Hekayati — directed).
- The Facet naming convention borrowed from Diátaxis was proposed (Omid Hekayati — proposed).
- The schema for Practice-facet files should be adopted from real, independently-converged ecosystem convention (Anthropic/OpenAI/Microsoft skill-creator files) rather than invented; three independent real Skill-file conventions (Anthropic, OpenAI, Microsoft) were fetched and compared as evidence (Claude — argued).
- The Facet meta-layer is the correct architectural response to the schema divergence problem (Claude — proposed).

#### Considered and not done
- **One shared schema for both Explanation and Practice content (the previous approach; not chosen)**: research into three independently-designed real Skill-file conventions found they converge on a schema deliberately lighter than Explanation-facet documents need. Forcing one shared schema onto both facets would mean either bloating Practice-facet files with apparatus they're specifically supposed to avoid, or stripping Explanation-facet documents of provenance machinery they genuinely need.
- **"Why" and "How" as the facet names (considered, not chosen)**: rejected on the same grounds `Abstract` replaced `Summary` for — "why" reads as a synonym for `Motivation` specifically, not as a description of an entire facet's purpose.

### Migrated Citations, Contributors into this changelog file; added Changelog as a third Facet
- Time: 2026-08-05T08:51:08Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote, flagged

#### What changed
- This changelog file was extracted from `documentation.md`'s front matter.
- Per the decision to move provenance out of base documents into their paired Changelog-facet file, `documentation.md`'s own front-matter `Citations` and `Contributors` are superseded by this file.
- Separately, `Changelog` was confirmed as a third Facet (not a separate concept), following the same extension mechanism `documentation.md` was already written to support — a new bullet under Facet, with its own governing file `documentation-changelog.md`.
- An explicit rule was also agreed: a document needing procedural content gets a companion `<base>.practice.md` file — this replaces the older, now-obsolete per-document "Guide" convention (an internal topic optionally linked from Abstract), since every document that needs how-to content now gets one automatically via the Practice facet, with no per-document naming decision required.
- The pending base-document cleanup was flagged; it is recorded in the `Propagates to` section below.

#### Propagates to
- `documentation.md`: Done — removed front-matter `Citations`/`Contributors`; added `Changelog` to the Facet list with the "no self-changelog" exception noted; added the explicit `<base>.practice.md` rule; removed the Diátaxis citation from the main body text where it functioned as argumentative evidence (kept only where the definition of Facet itself genuinely needs it for a first-time reader).
- `documentation-explanation.md`: Done — removed the obsolete Guide/optional-topic mechanism (Abstract's Guide link, Explanation's intro note, Body sections' Abstract bullet).

### Removed Diátaxis references from the base document; added cross-cutting Citations and URI sections; trimmed per-facet structural summaries
- Time: 2026-08-11T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Every remaining mention of Diátaxis was removed from `documentation.md` — Abstract, Methodology, the Facet topic's etymology and four-axis explanation, Discussion, Prior art, Extensibility.
- The per-facet "Key structural characteristics" blocks were removed from all three facet entries (Explanation, Practice, Changelog), leaving only the definition and a pointer to the governing specification.
- Two cross-cutting sections were added: `### Citations` (the source-selection criteria and full Relation vocabulary with per-relation guidance — including the new `Evidence` relation and the `Reference`/`Depends_on` boundary Unresolved question — that previously lived in `documentation-explanation.md`'s `### Citations` topic before it was removed during the Changelog migration) and `### URI` (the RFC 3986 form definitions and `file:` scheme prohibition that previously lived in `documentation-explanation.md`'s `### URI` topic) — both explicitly scoped as applying wherever citations or URIs appear in any document of any facet, so a future facet that needs citation tracking (e.g. a Research facet) inherits the same rules without redefinition, and so a reader of any changelog entry can follow the same Relation vocabulary without each facet redefining it.

#### Deliberation
- Diátaxis is an argumentative citation — an external framework cited as the inspiration for the Facet concept is argumentative provenance, not content the reader needs at the point of reading — and its mention in `documentation.md` was a violation of the project's own rule that argumentative citations live only in the changelog, where it is already preserved as a `Cited` entry (Omid Hekayati — argued).
- The per-facet "Key structural characteristics" blocks duplicated structural detail already specified authoritatively in each facet's own governing specification, creating a real sync obligation every time a facet's structure changed, with no compensating benefit to a reader — who can follow the governing-specification link for the full structure (Omid Hekayati — argued).

#### Considered and not done
- **Keep Diátaxis in `documentation.md` for first-time readers (rejected)**: the argument for keeping it was that a reader new to the Facet concept benefits from knowing the external framework it derives from. The counter-argument, accepted here, is that the Facet concept is self-contained — it can be defined directly as "a named category of documentation content defined by the reader's relationship to it" — without borrowing vocabulary from Diátaxis. A reader who wants the historical context can find it in this changelog's `Cited` entries; the base document's text should not carry argumentative provenance.
- **Keep "Key structural characteristics" as a navigational summary (rejected)**: would have required keeping the meta-layer in sync with every structural change in every facet's own specification. The leaner alternative — definition plus pointer to the governing spec — costs the reader one extra click but eliminates the sync risk entirely, which is the better trade for a meta-layer whose whole purpose is to be stable across facet changes.
- **Define Citations and URI inside each facet that needs them (rejected)**: would have required duplicating the source-selection criteria and Relation vocabulary across the Changelog spec, the Explanation spec, and any future facet that needs citations. Centralizing them in the meta-layer means a single authoritative definition, no drift, and a future Research facet (or similar) inherits the rules for free.
- **Define Citations and URI inside the Changelog spec only (considered, not chosen)**: would have been correct if only the Changelog facet ever used citations. But the source-selection criteria and Relation vocabulary are not Changelog-specific — they are about *how to cite a source*, which is a cross-cutting documentation concern. The Changelog spec now references the meta-layer's definition and only adds what is specific to a Changelog entry's `Cited` field (the "cite here is sufficient provenance" rule and the inline-hyperlink exception).

#### Propagates to
- `documentation-changelog.md`: Done — `### Cited` section trimmed from two paragraphs to one; Relation vocabulary and per-relation guidance removed, replaced with a reference to `documentation.md → Citations`; only Changelog-specific content kept.
- `documentation-explanation.md`: Done — `#### URI` subsection under `### Conventions` trimmed to a one-line reference to `documentation.md → URI`; the Internal Cross-References example was updated from `[URI](#uri)` (which would have become a broken anchor after the URI subsection moved) to `[Conventions](#conventions)`.

### Registered the Handoff facet as the fourth facet; added the no-fabricated-provenance content rule
- Time: 2026-09-01T14:15:37Z
- Type: Added
- Cited:
  - [Documentation — Handoff](./documentation-handoff.md) — Depends_on: the newly registered facet's governing specification; the meta-layer's entry is a pointer to it, not a restatement of it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided, directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- Registered the Handoff facet in the meta-layer as the fourth facet: the Abstract now names four facets (adding "read to resume a paused discussion"), the core observation paragraph's three-reader enumeration became four readers, the Facets list gained a Handoff entry (definition plus pointer to [documentation-handoff.md](./documentation-handoff.md), following the lean definition-plus-pointer pattern established for the other facets), the facet-selection guidance, Extensibility, hierarchy table (now five files), Drawbacks, and Future possibilities were updated to the four-facet model, and the Methodology records that the Handoff pattern repeated informally across working sessions before being named — the same adoption path as the Changelog facet.
- The Facet topic's Unresolved question about future reader relationships was updated to reflect that the discussion-resumption relationship was observed in real records before it was named.
- Separately, a new cross-cutting content rule — "No Fabricated or Redundant Provenance" — was added under Explanation: no invented facts, and historical/migration narration lives once (in the paired changelog), never repeated across documents.

#### Deliberation
- The Handoff facet was to be registered in the meta-layer rather than left as an unregistered specification, resolving the registration question that specification's own Unresolved questions had deferred (Omid Hekayati — decided).
- Base documents must not carry fabricated information or scattered migration narration — a rule the meta-layer was the right home for, since it applies to every Explanation- and Practice-facet document (Omid Hekayati — directed).

#### Considered and not done
- **Leave the Handoff facet unregistered pending more usage evidence (rejected by the owner)**: the facet already has a governing specification, a paired practice, and a real adopted convention (`<base>.handoff.md`); an unregistered specification outside the meta-layer is exactly the implicit-convention state the facet system exists to eliminate, and the Changelog facet registered with no more evidence of repetition than this.

---

### Body structure finalized; discussion content relocated per the finalized method
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Propagates to:
  - documentation.handoff.md: Created - this document's open questions and anticipated work moved there.
  - documentation-explanation.md: Done - the method this migration follows was finalized there in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - rewrote, moved

#### What changed
- The body's fixed top-level sections are reduced to `Abstract`, `Introduction`, `Explanation`, `Results` (Omid Hekayati - the `Discussion` section with sub-titles added avoidable ambiguity to the skeleton; Super Z - applied).
- `Drawbacks` becomes an Optional Sections catalog entry (Omid Hekayati - directed; Super Z - written, placed after `Examples`), taken by an author where the content calls for it - document-wide after `Results`, or topic-level.
- The routing of former discussion content (evidence inline; considered-and-not-done to the changelog; open questions and anticipated work to the handoff) moved into the Relevance discipline convention, which is the criterion the routing follows (Super Z).
- All `Rationale and alternatives`, `Prior art`, `Unresolved questions`, and `Future possibilities` blocks removed from this document's body; their content is preserved below and in the paired handoff (Super Z - audit and migration).

#### Considered and not done
- Keeping a `Discussion` wrapper that holds only `Drawbacks` (rejected): a wrapper for a single optional section is structural weight with no routing content left inside; the section enters the catalog directly. (Omid Hekayati)
- Keeping `Rationale and alternatives` as a body wrapper so the design's rejected alternatives stay near their decision (rejected): the AI-loading hazard - negated positions read as affirmed ones - outweighs locality; the changelog's `Considered and not done` carries them. (Omid Hekayati - the hazard; Super Z - recorded)
- Treating the no-fabricated-provenance rule as a style preference rather than a content rule (rejected): redundant and fabricated provenance are not stylistic blemishes - fabricated history misleads reasoning, and scattered migration notes multiply the places a future reader must check before trusting any one statement. Both directly undermine the single-source-of-truth structure the facet system exists to provide. (Omid Hekayati - the rule; Super Z - migrated)
- Keeping a single, shared documentation structure for all content (rejected): this was the status quo, and it produced the concrete tension described in Methodology - procedural and analytical content ended up competing for the same schema's attention. The Facet decomposition resolved that by giving each kind of content a structure optimized for its own use case. (Omid Hekayati)
- Using the names "Why" and "How" for the two facets (rejected): "Why" does not describe what the Explanation facet contains - it contains specifications, definitions, analyses, and design decisions, not only reasons or motivations. "How" is closer but still too narrow - Practice encompasses any content meant to be followed, not only step-by-step procedures. (Omid Hekayati)
- Naming the facets "Specification" and "Skill" instead of "Explanation" and "Practice" (rejected): "Specification" describes a specific kind of Explanation-facet document, not the facet itself. "Skill" describes the file format and folder convention of the Practice facet's most common instantiation, not the facet itself. The facet names should describe the reader's relationship to the content. (Omid Hekayati)
- Making the facet names language-agnostic (considered, not chosen): English facet names are already used throughout this project's technical content and tooling. Introducing a second set of names in another language without a concrete need would add a translation obligation with no clear benefit. (Omid Hekayati)
- Treating Changelog as a sub-convention of Explanation or Practice rather than its own facet (rejected): a changelog is neither studied to understand a subject nor followed to accomplish a task - it is consulted to audit history. Bundling it under either of the other two facets would force a structural mismatch. (Omid Hekayati)
- Defining additional facets now, before a real need for them exists (rejected): would produce empty or near-empty specifications - exactly the mistake this project's own Methodology warns against. The Changelog facet itself was added only after the same `<base>.changelog.md` pattern was already being applied across multiple artifacts. (Omid Hekayati)

#### Related work
- The Tyree-Akerman architecture-decision-record template (cited in documentation-explanation.md) is independent, narrower evidence for the same underlying principle: that different documentation purposes converge on the same structural concerns even when designed without knowledge of each other. (Super Z - migrated)
- The three independently-converged Skill-file conventions (Anthropic, OpenAI, Microsoft - see documentation-practice.md) are evidence from the Practice side specifically: all three arrived at the same minimal schema without coordination, demonstrating that the structural requirements of Practice-facet content are not this project's invention but a genuinely load-bearing constraint that emerges wherever this kind of content is produced. (Super Z - migrated)

#### Decision
Fixed skeleton: four sections. Everything else optional, catalogued. Open questions (mixed-facet documents, facet registry, further reader relationships) and anticipated work (facet growth) live in the paired handoff. (Omid Hekayati - approved)
