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
  - [Dependency Resolution via File URI and Companion Manifest](./khayyam/modularity.md) — Reference: the Explanation facet's use of URI for contributor identity and citations follows the same File URI approach already established for dependency resolution, in the document that absorbed that one.
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

### Registered the Research facet as the fifth facet
- Time: 2026-09-08T11:46:19Z
- Type: Added
- Cited:
  - [Documentation — Research](./documentation-research.md) — Depends_on: the newly registered facet's governing specification; the meta-layer's entry is a pointer to it, not a restatement of it.
- Propagates to:
  - documentation.handoff.md: Done - the Facet growth anticipated-work entry updated from the fifth-facet case to the sixth-facet case, now that the fifth facet exists.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Registered the Research facet in the meta-layer as the fifth facet: the Abstract now names five facets (adding "examined to evaluate a deliberate inquiry"), the core observation paragraph's reader enumeration became five readers, the Facets list gained a Research entry (definition plus pointer to [documentation-research.md](./documentation-research.md), following the lean definition-plus-pointer pattern established for the other facets), the facet-selection guidance gained the research branch, Extensibility was updated to the five-facet model, and the hierarchy table grew to six files (Omid Hekayati — confirmed the registration and the draft; Super Z — applied).
- The registered reader relationship is *examining to evaluate a deliberate inquiry* — categorically different from auditing history (Changelog) and resuming a paused discussion (Handoff): a research records how a question was pursued and how firm its outcome stands, and carries the negative results ("investigated; no change warranted") that produce no changelog entry and would otherwise leave no trace.

#### Deliberation
- The Research facet's specification was drafted from the owner's requirements before any informal accumulation — a different adoption path than the Changelog and Handoff facets, which each consolidated a practiced convention; the owner accepted this inversion, ruling that the requirement set (explicit question/goal standing, participant roles with review outcome, mandatory table of contents, stick-to-base naming) is itself the evidence of the recurring need (Omid Hekayati — decided; Super Z — recorded).
- The facet's entry names the reader relationship "examined to evaluate" rather than "studied" or "consulted" — a research's reader is judging an inquiry's course and outcome, not learning a subject or auditing an artifact (Super Z — drafted; owner confirmed).

#### Considered and not done
- **Deferring registration until a first real research exists (rejected by the owner)**: the facet system's own earlier position — define additional facets only when a real need exists — was weighed; the counter accepted here is that the specification was drafted against a concrete, stated requirement set, the companion pattern is already field-tested by two facets, and the naming decision gates every research filename, so registering before the first file exists prevents a renaming after references form (Omid Hekayati — decided).
- **Naming the facet "Investigation" (considered, not chosen)**: "Research" matches the established cross-domain word for a deliberate bounded inquiry and keeps the file suffix (`research`) and facet name identical, as Changelog and Handoff do (Super Z).

---

### Results routing established as a cross-cutting convention; own Results section removed
- Time: 2026-09-10T16:57:44Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the three-section skeleton this change self-applies, and the Results-routing exclusion it implements, are defined by the Explanation facet's governing specification; the removal decision and its evidence base are recorded in that document's paired changelog (2026-09-10T16:57:44Z entry).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - argued, directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.3) - researched, wrote

#### What changed
- `Results routing` was added as a cross-cutting convention, after `URI` and on the same precedent: a concern whose homes span several facets is defined at the meta layer, at pointer level, with each home's structure left to that facet's own specification. The routing keys on the type of the result — anticipated (the document's Abstract claim), derived (the `Implications` catalog entry), observed (the changelog entry that made the change, inline Evidence at a claim, a Research record, or handoff working state) — so an agent holding a result looks up its home by type without needing to know which facet's structure applies first (Omid Hekayati - argued the placement and the lookup path; Super Z - written).
- The document's own `## Results` section - an unpopulated placeholder - was removed under the three-section skeleton (`Abstract`, `Introduction`, `Explanation`); an Explanation-facet document carries no Results section.

---

### File Naming and Documentation Language registered as cross-cutting conventions
- Time: 2026-09-14T17:47:53Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) - Reference: the two rules specific to that specification's front matter (the slug derives from `Title`; the name is stable once `Final`) stay stated there, while the separator structure moved here.
  - [Filesystem](./modules/lib/memory/filesystem.md) - Reference: the rejected alternative home, cited because its own thesis is the reason for the rejection.
- Propagates to:
  - documentation-explanation.md: Done - its `File` topic's superseded filename wording ("hyphenated, no number, no domain prefix") replaced by a pointer to [File Naming](./documentation.md#file-naming); that wording contradicted the practice the convention now describes, since directories carry the category and digits appear inside conceptual terms (`osi_1`) and in Research ordinals by design.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - argued, directed
  - [ZCode](../CONTRIBUTORS.md#zcode) - researched, wrote

#### What changed
- `File Naming` joined `Citations`, `URI`, and `Results routing` as a convention defined at the meta layer. It assigns exactly one boundary to each of three separators: folder or hyphen for the category/topic edge (the folder where a category owns a directory, the hyphen where documents sit beside one another), underscore for the words of one conceptual term, and dot for a companion record's facet key. The last of the three had been stated per-facet inside each governing specification (`<base>.changelog.md`, `<base>.research.<NNN>.md`) but never as one rule, so a new facet had to infer the pattern from existing files rather than read it somewhere (Omid Hekayati - directed the home; ZCode - wrote, deriving the rule from the separators the set already uses).
- `Documentation Language` was registered with it: the written record is English and a proposal carries replacement-ready English, while conversation is explicitly outside the rule. The justification given is the record's audience - agents of every kind, human, IDE, CLI, and AI, across sessions and shifts - rather than a preference among languages, so the rule states what it is for and what it does not govern.
- Both conventions arrived by dissolving a stray untracked draft that held them, not by drafting them fresh: which is why the naming entry covers companions and folders, neither of which that draft contemplated (Omid Hekayati - directed the dissolution).

#### Deliberation
- Whether a document's name is a documentation concern or a filesystem concern was decided by the substance: a name is how a record is addressed in whatever medium currently holds it, and Memar's position is that a record's identity is its addressability rather than the name of the file carrying it. Registering the convention here states it where every facet's files are governed; registering it in the Filesystem protocol would have subordinated a documentation-method rule to the medium that document exists to argue against.
- The medium-bound character of both conventions was recorded as open work instead of being smoothed over: once the project's own organization exists and records are addressed rather than pathed, the naming convention and the dot-companion mechanism have to be re-derived, and the naming of non-document content (a film, a recording) is deliberately not generalized from file habits now, since a name can hold far less than such content is. (Omid Hekayati - argued that generalizing from the file side is unwinnable; ZCode - recorded.)

#### Considered and not done
- **A standing `Conventions` document (rejected)**: the draft was dissolved rather than registered. A container whose only membership criterion is "shared agreements" has no boundary on what enters it - the draft had accumulated a documentation naming rule, a citation-direction rule the folder READMEs already own, and three empty section headings of exactly the kind the Results-section round found to attract misrouted content over time - reproducing the shape already rejected on record for a generic `coding-style.md`.
- **Placing the naming convention in `protocols/memory/filesystem.md` (rejected)**: its thesis is that path-shaped names are not content's structure; the convention would have been read as that document endorsing the filesystem view it argues against.

---

### Written surface and Content Rule extensions
- Time: 2026-09-18T14:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../CONTRIBUTORS.md#composer) (Composer via [Cursor](../CONTRIBUTORS.md#cursor)) — drafted

#### What changed
- Registered cross-cutting [Written surface](./documentation.md#written-surface): no blank line between a section title and its body; no double blank runs; load-bearing logic stays linear; present-state writing when the reader has no prior durable snapshot to compare against. Rules are writing rules, not markup-protocol rules.
- Extended [Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) with **No derivative inventories** — do not cache directory/script/comparison membership lists in READMEs; point at the live collection.
- Placed followable steps in [documentation.practice.md](./documentation.practice.md) (not in documentation-practice.md, which governs the Practice facet schema).

#### Deliberation
- Blank line after a section title rejected (Omid Hekayati). Surface rules must not be Markdown-tied (Omid Hekayati). Membership indexes in pointer files rejected as invalidating caches (Omid Hekayati). Narrating "revised" against invisible prior text rejected (Omid Hekayati).

---

### The doer follows the practice
- Time: 2026-09-23T06:30:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — required the reading rule
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../CONTRIBUTORS.md#cursor)) — wrote

#### What changed
- [documentation.practice.md](./documentation.practice.md) states that work a practice already covers is done by reading that practice. The paired explanation is opened when a step names a section to check, or when the task is to change the explanation.
- The changelog step states session consolidation: one session produces one entry on a base artifact. A later edit in that session extends the entry.

#### Deliberation
Owner: an executing agent does not need to read the explanatory document to carry out a rule that the practice can state. The practice files already existed for that split, and they did not say so as a reading rule. The modeling session wrote a relation rule into the explanation and did not add the steps to the practice.

---

### The body affirms what holds; removed formulations stay in the changelog
- Time: 2026-09-23T09:05:00Z
- Type: Fixed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: Relevance discipline already sends a negated alternative to the changelog because a reader loading the body treats a negation as a live claim.
- Propagates to:
  - documentation.practice.md: Done — the written-surface step states the same rule, including when a prior snapshot exists.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- Written surface gains a bullet: a body sentence states the current rule. The replaced wording, the dropped label, and the rejected alternative are changelog content. A sentence whose job is to warn the reader off a previous formulation does not stay in the body, whether or not a prior snapshot of that formulation exists.
- The practice's written-surface step carries the same instruction.

#### Deliberation
- The present-state bullet covered only the case where the reader cannot open a prior snapshot. That left a reading on which, once a snapshot exists, the body may narrate "X is retired" and "Y is not the rule." A Khayyam edit did exactly that with two signature labels after replacing them. The relevance discipline already forbids a negated alternative in the body; the written-surface rule did not say so in the step an editor follows (Omid Hekayati — requested; Grok — applied).

---

### A model's document is named after the concept it models
- Time: 2026-10-03T00:00:00Z
- Type: Added
- Cited:
  - [Modeling → Expected Output of a Modeling Session](./modeling.md#expected-output-of-a-modeling-session) - Depends_on: the document that now carries the reduced claim and points here for the rule
  - [Khayyam Rules Catalog](../bundles/khayyam/rules/README.md) - Evidence: "Each rule has its own folder, holding a main document named after the rule" - the one kind of artifact in this repository that already kept the rule, and the precedent it is drawn from
  - [Documentation Practice → Folder READMEs](./documentation.practice.md#folder-readmes) - Depends_on: the folder-README rule that makes a folder's main document addressable by a path a reader types
- Propagates to:
  - docs/modeling.md: Done - the rule it stated is now a pointer here, and its Abstract and *Expected Output of a Modeling Session* carry the reduced claim.
  - docs/modeling.practice.md: Done - its closing pointer goes here.
  - docs/modeling.changelog.md: Done - the entry recording the rename now cites the rule's home.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - required
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - drafted, applied

#### What changed
- [File Naming](./documentation.md#file-naming) gains the rule: a document that states a model is named after the concept the model is about; the folder holding it is named for the responsibility whose model it is and the document takes that same name beside it - `modules/computer/binding/binding.md`, `modules/process/construction/construction.md`, `modules/process/control-flow/control-flow.md` - and every companion record takes the same base name. Nothing in such a name carries the kind of document, since the dot already carries the facet key and the base name already carries the subject, which is the one misplacement this document's own separator system exists to prevent.
- The topic states the rule's purpose, which is addressing rather than tidiness: the smallest mistake in addressing a model - the wrong folder segment, or a path rebuilt from memory - should reach nothing rather than reach a real document about a different concept. The evidence is the repository's own: 41 of its 115 base documents already carry their own folder's name, all 26 folders under `modules/khayyam/rules/` do because that catalog states the rule for its own case, and two pairs of base documents share a base name across folders, so a wrong subject path resolves to no file rather than to a neighbour - which is what makes the subject name the cheaper of the two costs.
- Two boundaries are stated with it: the rule reaches a document that is a folder's main model and not working state left beside the documents a session read, which takes `<base>.handoff.md`; and it does not bind the front-matter `Title`, which stays free to read as the model *of* the concept.
- The Abstract already listed what this topic covers - "how a document's name encodes its category, concept, and facet" - so it needed no change, and none was made.

#### Considered and not done
- **A separate topic for it inside this document.** The topic that names a model after its concept is a naming rule, and this document's subject is naming; a second topic would have left the rule's owner and its reader in different places for no gain.
- **Extending the rule to every base document in the repository.** It is stated for a model's document. The two pairs of base documents that share a base name across folders are recorded as the reason a wrong subject path resolves to nothing there rather than renamed on the strength of a rule that does not reach them.
- **Fixing the counts into a permanent statement.** They are measurements of this repository now and were re-measured for this entry; a later document changes them, and the entry above records that re-measuring is owed whenever either number is cited.

#### Deliberation
- Owner: a documentation rule - such as what a name is - has nothing to do with `docs/modeling.md` and should really be settled in `docs/documentation.md`. The rule had been added to `Modeling` as a way of making it mandatory; mandatory and owned are separate questions, and the topic it was added to was the wrong owner for a rule about file names.

---

### An empty result changes nothing, and the check reports open work
- Time: 2026-10-04T05:35:11Z
- Type: Added
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](./comparisons/spec-kit.001.md) - **Reference**: the comparison whose adoption filter produced these changes. GitHub Spec Kit's `/converge` requires that a converged run leave `tasks.md` byte-for-byte unchanged with no empty Convergence header and report a fixed string; its `check_extension_version_bump.py` turns "please remember to bump" into a merge requirement, with the rationale recorded as a shipped bug class.
- Propagates to:
  - [.agents/scripts/memar-documentation.py](../.agents/scripts/memar-content.py): Done - the propagation report and the newline fix below. That file carries no changelog of its own.
  - [.agents/scripts/README.md](../.agents/scripts/README.md): Done - what `check` reports on a folder run, the one question it pointedly does not judge, and the `memar` launcher that reaches it by one word. That file carries no changelog of its own.
  - [.agents/scripts/tests/memar-documentation.py](../.agents/scripts/tests/memar-content.py): Done - five classes of tests for the report, plus five for the append convention. A Test belongs in the folder of the module that owns what it tests, per [Test Placement](../modules/process/test/rules/test-placement/test-placement.md).
  - [documentation.practice.md](./documentation.practice.md): None needed - [Trivial changes](./documentation-changelog.md#trivial-changes) already covers the changelog-entry case, and the new rule is the same economy stated at the level of the artifact rather than the entry; the practice's own step 4 already sends a session with no lasting design change to no entry at all.
  - [documentation-explanation.md](./documentation-explanation.md): None needed - the rule concerns what a check writes, not what a document is.
  - [cognition.changelog.md](./cognition.changelog.md): None needed - the norm change in that entry does not rest on this one.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - drafted, tested

#### What changed
- [Written surface](./documentation.md#written-surface) gains a rule: an empty result leaves the medium unchanged. A report, review, check, or convergence with nothing to report produces no artifact — no empty section, no placeholder heading, no empty changelog entry, no file created to hold a result that is not there. [Trivial changes](./documentation-changelog.md#trivial-changes) already says a session whose edits leave no lasting design change gets no entry; this carries the same economy up from the entry to every artifact a check might write, which is where it was missing. The rule is stated with a second reason as well as the tidiness one, because tidiness is not what makes it load-bearing: a loop whose success condition is "nothing was found" needs the nothing to be observable, or the party running it cannot distinguish a completed check from one that has not run and goes on producing work to fill the gap. The observable form of finding nothing is that the shared medium is exactly as it was.
- `memar-documentation.py check`, given a folder, prints the `Propagates to` entries left `Pending` across the document set in their own section, apart from the problems. The facet calls `Pending` a searchable state on purpose, and nothing could search it: `search` excludes changelog files because their content is history rather than current truth, which is the correct call for concept search and left the work-list with no surface at all. At the inspected tree the section reports 61 open propagations, which is the honest size of the queue the facet's design implies and which no surface had shown before.
- The state is read from the entry's own field rather than from the word's presence in a line, so a description mentioning `Pending` while reporting work already done is not read as an obligation, and the sources' `Pending deletion` and `Pending at absorb time` are both read as the open state they are. `Done` and `Rejected` are not reported: `Rejected` closes the search result permanently by the facet's own definition, and a section that kept raising decided matters would train a reader to skip it.
- A ledger is told from a specification by its stem ending in `.changelog`. `cognition.changelog.md` records entries in the field; `documentation-changelog.md` specifies the field and carries a heading, the field name, and a sample line in the field's own shape. Testing on the file-name suffix alone read the second as the first and reported the project's own rules as its outstanding work.
- `changelog_append` now writes the newline convention the file already holds rather than a fixed one, and normalizes a CRLF entry into an LF file. The append was found through the check this entry's first change strengthens: appending to this repository's own `cognition.changelog.md`, which holds CRLF, wrote an LF tail and made `check` report mixed line endings on the file — the tool the [practice](./documentation.practice.md) tells every contributor to append with, causing the defect it is the authority for detecting. The changelog was returned to its own convention, and five tests now hold the behavior from both sides.
- [.agents/scripts/README.md](../.agents/scripts/README.md) states what the folder run reports, why the section is printed apart from the problems, and how a ledger is told from a specification — that file being the folder's authority on its own interface. It also gains the `memar` launcher as the folder's fourth kind of file: a command that routes to this folder's tools and adds nothing, so a caller reaches Memar by one word without learning a path or a filename, and so the skill that names this folder can name a word instead of a location. Access multiplies; the implementation does not.

#### Considered and not done
- **Checking whether a body holds a rejected alternative belonging in a changelog entry (rejected, and kept as a negative result):** it is not decidable from the text. `documentation-changelog.md` is the document that specifies the field, so it carries a section by the field's own name in its own body, correctly placed; the specification of where records go and a record of one differ only in what the text is *for*. A threshold that separated them — heading depth, a bullet beside the heading, the file's name — either fires on this repository's own governing document or misses a record written the other way, and a check permanently red on a correct file is one a reader learns to skip. An implementation was written, run against the tree, caught by the check on the specification, and removed on that evidence rather than tuned. The hazard is real and named at [Relevance discipline](./documentation-explanation.md#relevance-discipline); the tests pin the two shapes a future attempt must not misjudge, so the question is not reopened blind.
- **Making an undischarged propagation decide `check`'s exit code (rejected):** every routine run would be red on work predating the run, and a gate that is always open is not a gate. The section prints on every folder run so it cannot be missed, and its count is in the summary line.
- **A flag that makes the section a gate for a caller that wants one (not taken):** a `Pending` entry is a fact about a queue, and which queue entries a given run should be blocked on is a project decision rather than a tool default. Leaving it as a report keeps the tool from holding an opinion the project has not stated.
- **Widening the report to every open obligation the script could find (rejected):** the remaining candidates are the same non-decidable class, and a check that reports guesses is worse than one that reports only what it can know.

---

### Add a source standing test to the citation rule
- Time: 2026-10-04T13:27:43Z
- Propagates to:
  - documentation-research.md: Done - `Methodology` now states that a question's origin is recorded without being cited, so the standing of an origin is never mistaken for the standing of a conclusion
  - rule.research.001.md: Done - its vocabulary sources no longer carry `Evidence` or a URL, and the specification it did not read is named as a limitation
  - documentation-handoff.research.001.md: Done - the vendor's account of its own product is `Reference`, and the finding states what it rests on instead
  - knowledge.changelog.md: Done - the relation of a tertiary compilation and a social-media post recorded earlier is restated there
  - content.changelog.md: Done - the same restatement for the post that entry cites
  - process.research.001.md: Reference - the session-identity half of that record became [Handoff Research 001](./documentation-handoff.research.001.md) before this rule was written
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed, argued

#### What changed
- `### Citations` gained a **Source standing** paragraph and a companion paragraph on recording an origin without citing it.
- Whether a source may be recorded at all is now settled before whether it is worth recording, as two independent tests: the terms of use or license must permit the use being made of the work, and the source must hold standing for the relation claimed of it.
- Where permission is unclear the citation is withheld and the record states that the material was observed without naming it. Naming a source can create an attribution obligation the project has not agreed to, which is a second and independent reason the default is not to record one.
- Sources of no standing are named as a class: a personal site, a blog, a social-media or network post, a chat channel, a conference-hallway or corridor remark, a vendor's marketing or "best practices" page, an AI-generated summary of any of these, and a tertiary compilation such as an encyclopedia article. None may be cited with `Evidence`, `Depends_on`, or `Extends`, and no proposition rests on one. A tertiary compilation is a pointer toward the primary sources behind it.
- The reasons are the two the owner gave: naming confers a standing the source has not earned whatever words are borrowed from it, and it tells the reader the proposition was reached by that source when the reasoning is Memar's own.
- Sources that pass both tests are named: standards bodies and formal specifications; peer-reviewed work; a published book of record; primary technical documentation of an artifact for claims about its observable behavior; and this project's own published record.
- A question may be raised by any source, including one of no standing, and that origin is recorded in the Research facet's Participants or in the paired handoff. What such an origin may never do is carry a conclusion: the recording document states the reasoning in its own words and either supports the conclusion from a source that passes both tests or marks the conclusion as its own.

#### Considered and not done
- A blanket prohibition on reading sources of no standing was rejected (Omid Hekayati — decided). The rule is about what a document records, not what may be read; the reading that prompted the rule is the reason it is needed.
- A rule against naming an informal source at all, including as `Reference`, was rejected as wider than the harm (Space Bunny Alpha — argued). Not naming is the default where permission is unclear, and a source of no standing may still be recorded for a reader who needs to know what was considered.
- Placing the rule beside the existing Content Rule on provenance was considered and not done (Space Bunny Alpha — argued): it governs citations rather than fabrication, and the cross-cutting band this document already carries is where citation practice lives.

#### Deliberation
The owner proposed the rule as a prohibition on citing informal sources (Omid Hekayati — claimed), and the first pass reproduced that shape as a standing test (Space Bunny Alpha — claimed). The owner then separated two concerns the first pass had merged: whether a source may be read, which is unrestricted, and whether naming one is safe, which is a question about rights and attribution as much as about credibility (Omid Hekayati — claimed). Wikipedia was put to the same test and found to fail on standing rather than on rights — its text is openly licensed and quotable with attribution, which is why the rule is written as two tests rather than one (Space Bunny Alpha — argued).

---

### The bound against redundant reading governs what the doer reads, not only what a document may list
- Time: 2026-10-04T00:00:00Z
- Cited:
  - [Content Rule: No Fabricated or Redundant Provenance](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) - Evidence: the bound this section already carried, extended from what a document may list to what a session reads
- Propagates to:
  - ../.agents/skills/memar/SKILL.md: Done - the three skill rules this section now states were removed from the skill, leaving the skill with the section as its authority
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- *No derivative inventories* now states three rules about what a session reads, beside the rule about what a document may list: do not enumerate a document set the task does not require, where a folder's README is its index rather than the folder's documents opened one by one; do not restart discovery once the knowledge the task needs is already in context; and do not read a task's documents merely because this practice is in force.
- The three corresponding rules were removed from the memar skill, which had been their only home.

#### Considered and not done
- The three rules were not given a section of their own (Space Bunny Alpha - argued). They are the same bound the section already carried, applied to the reader rather than to the writer, and a second section would restate one rule under two headings.
- The rules were not placed in [Cognition](./cognition.md) (Omid Hekayati - decided). Two of the three govern session economy rather than reasoning, and Cognition's own boundary paragraph states that norms specific to producing documentation are owned by the documentation system's specifications.
- The skill's session-economy rules were not moved at the same time (Space Bunny Alpha - argued). They are obligations and runtime facts mixed in one section, and [Documentation Changelog](./documentation-changelog.md) already settles the shape of that mixture - the obligation belongs beside the facet and only the runtime-dependent fact stays in the skill. Where the obligations go has no home yet, so the split is carried as an open question rather than performed.

---

### Three entries leave the documentation handoff, each answered by the meta-layer body
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation.handoff.md: Done - the mixed-facet, citation-relation-boundary, and further-reader-relationship entries were removed; the meta-layer body already answers each (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- *Mixed-facet documents* left `## Open Questions`: [Documentation -> Which facet does a document belong to?](./documentation.md#which-facet-does-a-document-belong-to) already decides the case - a document carrying both facets' content is settled by which purpose dominates.
- *Citations: Reference versus Depends_on boundary* left `## Open Questions`: [Documentation -> Citations -> Relation vocabulary](./documentation.md#citations) gives each relation its condition, and `Evidence` is stated as distinct from `Reference` (context only) and `Depends_on` (a structural dependency).
- *Further reader relationships* left `## Anticipated Work`: [Documentation -> Extensibility](./documentation.md#extensibility) already states that a document type fitting none of the five reader relationships would be met by adding a sixth facet following the same pattern, and how the Handoff and Research facets were each added this way is recorded in the surviving *Facet growth* item.

#### Considered and not done
- The `Reference` / `Depends_on` boundary was not sharpened in the body, and no implementability axis was added to the relation vocabulary (Space Bunny Alpha - argued). The vocabulary states each relation's condition, so the handoff entry was a request to restate what the section says; adding an axis would change a settled body rather than close an entry.
- No exception for genuinely mixed-content documents was added to the facet-selection guidance (Space Bunny Alpha - argued). The dominant-purpose test decides any real case, and a standing exception would invite exactly the ambiguity the test exists to remove.
- The *Facet registry* entry and the other remaining entries were left in the handoff (Space Bunny Alpha - argued): each asks something the meta-layer's body does not state.
---

### Rejected positions given a deletion procedure
- Time: 2026-09-27T09:38:12Z
- Type: Added
- Propagates to:
  - AGENTS.md: Done - the four rules that restated this document and the Changelog facet's governing specification were removed, leaving the pointer to this document and its facets.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided

#### What changed
- A `## Rejected positions` section was added to `documentation.practice.md`, giving the treatment of a rejected position three steps: the entry, section, or sentence whose claim is that position is deleted rather than annotated or kept as history; the alternative genuinely examined and not taken gets one `Considered and not done` line in the surviving entry; and the decision's positive statement stays in the document that holds the claim, with the changelog recording the outcome rather than the position it replaced.
- The restated copies those steps replace in `AGENTS.md` are gone: which fields a changelog entry carries and what it must not narrate is stated by [documentation-changelog.md → Structure](./documentation-changelog.md#structure) and [Trivial changes](./documentation-changelog.md#trivial-changes); where an examined alternative goes is [Considered and not done](./documentation-changelog.md#considered-and-not-done); what a body affirms and where a replaced formulation belongs is [documentation.md → Written surface](./documentation.md#written-surface); the folder README convention was already this document's own `## Folder READMEs` section.
- This entry was first written on the wrong file, `documentation-practice.changelog.md`, and was moved here by the changelog routing audit.

---

---

---

### Owed and planned capability marked in all three places
- Time: 2026-10-07T03:45:00Z
- Type: Changed
- Cited:
  - [Documentation — Comparison](./documentation-comparison.md) - Evidence: its Method requirements, added in the same session from the tensorus and hindsight comparisons.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) gains a fifth rule: owed or planned capability is marked in prose, by a quiescent default in code, and by a pointer at the entry point; a claim implied by one surface and absent from the others is a fabrication in the rule's first sense.

#### Considered and not done
- **A requirement that check enforces it** (deferred): content check could later verify that owed rows, disabled defaults, and entry-point notes co-occur; decided against adding enforcement now, so the norm stands on its reasoning first.

---

### A folder README carries no changelog and no handoff
- Time: 2026-10-07T15:14:08Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../CONTRIBUTORS.md#cursor) — drafted, applied

#### What changed
- [Folder READMEs](./documentation.practice.md#folder-readmes) gains a sixth step: a README has no `README.changelog.md` and no `README.handoff.md`. A decision about a folder is written into the README as the rule it now is; open work about a folder goes to the handoff of the module or document whose subject it is.
- Applied to the two READMEs that had companions. `docs/modules/README.md` took the one reason worth keeping into its body — why specification and realization are two trees — and that categories are not final. The open state of `modules/README.handoff.md` moved to the handoffs that own each subject: the category layout to [Modularity Handoff](./modularity.handoff.md#the-category-layout-of-this-repository), the archive findings to `modules/go-port/go-port.handoff.md`, `lib/`'s findings to `modules/lib/lib.handoff.md`, and the end-of-file convention to `modules/khayyam/rules/file-layout/file-layout.handoff.md`.

#### Considered and not done
- **Keeping a handoff beside a README that holds real open work** (rejected by the owner): the open work was always about some module's subject, and filed under the folder's index it had no owner to answer it.
- **Moving the count of broken links under `modules/`** (not done): `memar content check` reports it whenever it is run, so an entry restating the count would only go stale.
