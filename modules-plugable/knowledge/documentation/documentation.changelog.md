# Documentation Changelog
This document records why and how `documentation.md` changed over time. See [Documentation — Changelog](./changelog/changelog.md) for what this file's structure means.

## Changelog

### Initial split into three facets
- Time: unknown (historical import — this document's own creation, before this changelog existed)
- Cited:
  - [Diátaxis](https://diataxis.fr/) — Extends: the Facet concept borrows Diátaxis's core insight — that documentation content is categorically different depending on whether the reader is meant to study it or to follow it — and adapts it to this project's own scope and naming. Diátaxis itself identifies four forms (Tutorials, How-to guides, Reference, Explanation); this project initially distinguished two facets (Practice, Explanation), then added Changelog as a third, with the same underlying two-axis principle.
  - [Modeling](../../../docs/modeling.md) — Depends_on: Documentation is the result of correct modeling. The concept of Documentation cannot be understood or defined independently from the modeling process.
  - [Anthropic Claude skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — Reference: one of three independently-designed real Skill-file conventions examined as evidence for the Practice facet's governing schema.
  - [OpenAI Codex skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) — Reference: second independently-converged real Skill-file convention, explicitly listing inclusion of auxiliary documentation inside a skill as an anti-pattern.
  - [Microsoft skill-creator](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) — Reference: third independently-converged real Skill-file convention, sharing the same core schema despite layering additional SDK-specific structure on top.
  - Dependency Resolution via File URI and Companion Manifest (`docs/khayyam/modularity.md`) — Reference: the Explanation facet's use of URI for contributor identity and citations follows the same File URI approach already established for dependency resolution, in the document that absorbed that one.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — argued, directed, proposed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) — rewrote
  - [Claude](../../../CONTRIBUTORS.md#claude) — argued, proposed

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
  - [Claude](../../../CONTRIBUTORS.md#claude) — rewrote, flagged

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Documentation — Handoff](./handoff/handoff.md) — Depends_on: the newly registered facet's governing specification; the meta-layer's entry is a pointer to it, not a restatement of it.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided, directed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- Registered the Handoff facet in the meta-layer as the fourth facet: the Abstract now names four facets (adding "read to resume a paused discussion"), the core observation paragraph's three-reader enumeration became four readers, the Facets list gained a Handoff entry (definition plus pointer to [documentation-handoff.md](./handoff/handoff.md), following the lean definition-plus-pointer pattern established for the other facets), the facet-selection guidance, Extensibility, hierarchy table (now five files), Drawbacks, and Future possibilities were updated to the four-facet model, and the Methodology records that the Handoff pattern repeated informally across working chats before being named — the same adoption path as the Changelog facet.
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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) - rewrote, moved

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
  - [Documentation — Research](./research/research.md) — Depends_on: the newly registered facet's governing specification; the meta-layer's entry is a pointer to it, not a restatement of it.
- Propagates to:
  - documentation.handoff.md: Done - the Facet growth anticipated-work entry updated from the fifth-facet case to the sixth-facet case, now that the fifth facet exists.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Registered the Research facet in the meta-layer as the fifth facet: the Abstract now names five facets (adding "examined to evaluate a deliberate inquiry"), the core observation paragraph's reader enumeration became five readers, the Facets list gained a Research entry (definition plus pointer to [documentation-research.md](./research/research.md), following the lean definition-plus-pointer pattern established for the other facets), the facet-selection guidance gained the research branch, Extensibility was updated to the five-facet model, and the hierarchy table grew to six files (Omid Hekayati — confirmed the registration and the draft; Super Z — applied).
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
  - [Documentation — Explanation](./explanation/explanation.md) — Depends_on: the three-section skeleton this change self-applies, and the Results-routing exclusion it implements, are defined by the Explanation facet's governing specification; the removal decision and its evidence base are recorded in that document's paired changelog (2026-09-10T16:57:44Z entry).
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - argued, directed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM 5.3) - researched, wrote

#### What changed
- `Results routing` was added as a cross-cutting convention, after `URI` and on the same precedent: a concern whose homes span several facets is defined at the meta layer, at pointer level, with each home's structure left to that facet's own specification. The routing keys on the type of the result — anticipated (the document's Abstract claim), derived (the `Implications` catalog entry), observed (the changelog entry that made the change, inline Evidence at a claim, a Research record, or handoff working state) — so an agent holding a result looks up its home by type without needing to know which facet's structure applies first (Omid Hekayati - argued the placement and the lookup path; Super Z - written).
- The document's own `## Results` section - an unpopulated placeholder - was removed under the three-section skeleton (`Abstract`, `Introduction`, `Explanation`); an Explanation-facet document carries no Results section.

---

### File Naming and Documentation Language registered as cross-cutting conventions
- Time: 2026-09-14T17:47:53Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./explanation/explanation.md) - Reference: the two rules specific to that specification's front matter (the slug derives from `Title`; the name is stable once `Final`) stay stated there, while the separator structure moved here.
  - Filesystem (`docs/modules/lib/memory/filesystem.md`) - Reference: the rejected alternative home, cited because its own thesis is the reason for the rejection.
- Propagates to:
  - documentation-explanation.md: Done - its `File` topic's superseded filename wording ("hyphenated, no number, no domain prefix") replaced by a pointer to [File Naming](./documentation.md#file-naming); that wording contradicted the practice the convention now describes, since directories carry the category and digits appear inside conceptual terms (`osi_1`) and in Research ordinals by design.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - argued, directed
  - [ZCode](../../../CONTRIBUTORS.md#zcode) - researched, wrote

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../../../CONTRIBUTORS.md#composer) (Composer via [Cursor](../../../CONTRIBUTORS.md#cursor)) — drafted

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — required the reading rule
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — wrote

#### What changed
- [documentation.practice.md](./documentation.practice.md) states that work a practice already covers is done by reading that practice. The paired explanation is opened when a step names a section to check, or when the task is to change the explanation.
- The changelog step states session consolidation: one session produces one entry on a base artifact. A later edit in that chat extends the entry.

#### Deliberation
Owner: an executing agent does not need to read the explanatory document to carry out a rule that the practice can state. The practice files already existed for that split, and they did not say so as a reading rule. The modeling chat wrote a relation rule into the explanation and did not add the steps to the practice.

---

### The body affirms what holds; removed formulations stay in the changelog
- Time: 2026-09-23T09:05:00Z
- Type: Fixed
- Cited:
  - [Documentation — Explanation](./explanation/explanation.md) — Depends_on: Relevance discipline already sends a negated alternative to the changelog because a reader loading the body treats a negation as a live claim.
- Propagates to:
  - documentation.practice.md: Done — the written-surface step states the same rule, including when a prior snapshot exists.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — applied

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
  - [Modeling → Expected Output of a Modeling Chat](../../../docs/modeling.md#expected-output-of-a-modeling-session) - Depends_on: the document that now carries the reduced claim and points here for the rule
  - Khayyam Rules Catalog (`bundles/khayyam/rules/README.md`) - Evidence: "Each rule has its own folder, holding a main document named after the rule" - the one kind of artifact in this repository that already kept the rule, and the precedent it is drawn from
  - [Documentation Practice → Folder READMEs](./documentation.practice.md#folder-readmes) - Depends_on: the folder-README rule that makes a folder's main document addressable by a path a reader types
- Propagates to:
  - docs/modeling.md: Done - the rule it stated is now a pointer here, and its Abstract and *Expected Output of a Modeling Chat* carry the reduced claim.
  - docs/modeling.practice.md: Done - its closing pointer goes here.
  - docs/modeling.changelog.md: Done - the entry recording the rename now cites the rule's home.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - required
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - drafted, applied

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
  - [Comparison: Memar and GitHub Spec Kit](../../../docs/comparisons/spec-kit.001.md) - **Reference**: the comparison whose adoption filter produced these changes. GitHub Spec Kit's `/converge` requires that a converged run leave `tasks.md` byte-for-byte unchanged with no empty Convergence header and report a fixed string; its `check_extension_version_bump.py` turns "please remember to bump" into a merge requirement, with the rationale recorded as a shipped bug class.
- Propagates to:
  - [.agents/scripts/memar-documentation.py](../../../modules/knowledge/content/content.py): Done - the propagation report and the newline fix below. That file carries no changelog of its own.
  - [.agents/scripts/README.md](../../../.agents/scripts/README.md): Done - what `check` reports on a folder run, the one question it pointedly does not judge, and the `memar` launcher that reaches it by one word. That file carries no changelog of its own.
  - [.agents/scripts/tests/memar-documentation.py](../../../modules/knowledge/content/tests/content.py): Done - five classes of tests for the report, plus five for the append convention. A Test belongs in the folder of the module that owns what it tests, per Test Placement (`modules/process/test/rules/test-placement/test-placement.md`).
  - [documentation.practice.md](./documentation.practice.md): None needed - [Trivial changes](./changelog/changelog.md#trivial-changes) already covers the changelog-entry case, and the new rule is the same economy stated at the level of the artifact rather than the entry; the practice's own step 4 already sends a session with no lasting design change to no entry at all.
  - [documentation-explanation.md](./explanation/explanation.md): None needed - the rule concerns what a check writes, not what a document is.
  - [cognition.changelog.md](../../../docs/cognition.changelog.md): None needed - the norm change in that entry does not rest on this one.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - drafted, tested

#### What changed
- [Written surface](./documentation.md#written-surface) gains a rule: an empty result leaves the medium unchanged. A report, review, check, or convergence with nothing to report produces no artifact — no empty section, no placeholder heading, no empty changelog entry, no file created to hold a result that is not there. [Trivial changes](./changelog/changelog.md#trivial-changes) already says a session whose edits leave no lasting design change gets no entry; this carries the same economy up from the entry to every artifact a check might write, which is where it was missing. The rule is stated with a second reason as well as the tidiness one, because tidiness is not what makes it load-bearing: a loop whose success condition is "nothing was found" needs the nothing to be observable, or the party running it cannot distinguish a completed check from one that has not run and goes on producing work to fill the gap. The observable form of finding nothing is that the shared medium is exactly as it was.
- `memar-documentation.py check`, given a folder, prints the `Propagates to` entries left `Pending` across the document set in their own section, apart from the problems. The facet calls `Pending` a searchable state on purpose, and nothing could search it: `search` excludes changelog files because their content is history rather than current truth, which is the correct call for concept search and left the work-list with no surface at all. At the inspected tree the section reports 61 open propagations, which is the honest size of the queue the facet's design implies and which no surface had shown before.
- The state is read from the entry's own field rather than from the word's presence in a line, so a description mentioning `Pending` while reporting work already done is not read as an obligation, and the sources' `Pending deletion` and `Pending at absorb time` are both read as the open state they are. `Done` and `Rejected` are not reported: `Rejected` closes the search result permanently by the facet's own definition, and a section that kept raising decided matters would train a reader to skip it.
- A ledger is told from a specification by its stem ending in `.changelog`. `cognition.changelog.md` records entries in the field; `documentation-changelog.md` specifies the field and carries a heading, the field name, and a sample line in the field's own shape. Testing on the file-name suffix alone read the second as the first and reported the project's own rules as its outstanding work.
- `changelog_append` now writes the newline convention the file already holds rather than a fixed one, and normalizes a CRLF entry into an LF file. The append was found through the check this entry's first change strengthens: appending to this repository's own `cognition.changelog.md`, which holds CRLF, wrote an LF tail and made `check` report mixed line endings on the file — the tool the [practice](./documentation.practice.md) tells every contributor to append with, causing the defect it is the authority for detecting. The changelog was returned to its own convention, and five tests now hold the behavior from both sides.
- [.agents/scripts/README.md](../../../.agents/scripts/README.md) states what the folder run reports, why the section is printed apart from the problems, and how a ledger is told from a specification — that file being the folder's authority on its own interface. It also gains the `memar` launcher as the folder's fourth kind of file: a command that routes to this folder's tools and adds nothing, so a caller reaches Memar by one word without learning a path or a filename, and so the skill that names this folder can name a word instead of a location. Access multiplies; the implementation does not.

#### Considered and not done
- **Checking whether a body holds a rejected alternative belonging in a changelog entry (rejected, and kept as a negative result):** it is not decidable from the text. `documentation-changelog.md` is the document that specifies the field, so it carries a section by the field's own name in its own body, correctly placed; the specification of where records go and a record of one differ only in what the text is *for*. A threshold that separated them — heading depth, a bullet beside the heading, the file's name — either fires on this repository's own governing document or misses a record written the other way, and a check permanently red on a correct file is one a reader learns to skip. An implementation was written, run against the tree, caught by the check on the specification, and removed on that evidence rather than tuned. The hazard is real and named at [Relevance discipline](./explanation/explanation.md#relevance-discipline); the tests pin the two shapes a future attempt must not misjudge, so the question is not reopened blind.
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
  - process.research.001.md: Reference - the session-identity half of that record became [Handoff Research 001](./handoff/handoff.research.001.md) before this rule was written
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - claimed, argued

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- *No derivative inventories* now states three rules about what a session reads, beside the rule about what a document may list: do not enumerate a document set the task does not require, where a folder's README is its index rather than the folder's documents opened one by one; do not restart discovery once the knowledge the task needs is already in context; and do not read a task's documents merely because this practice is in force.
- The three corresponding rules were removed from the memar skill, which had been their only home.

#### Considered and not done
- The three rules were not given a section of their own (Space Bunny Alpha - argued). They are the same bound the section already carried, applied to the reader rather than to the writer, and a second section would restate one rule under two headings.
- The rules were not placed in [Cognition](../../../docs/cognition.md) (Omid Hekayati - decided). Two of the three govern session economy rather than reasoning, and Cognition's own boundary paragraph states that norms specific to producing documentation are owned by the documentation system's specifications.
- The skill's session-economy rules were not moved at the same time (Space Bunny Alpha - argued). They are obligations and runtime facts mixed in one section, and [Documentation Changelog](./changelog/changelog.md) already settles the shape of that mixture - the obligation belongs beside the facet and only the runtime-dependent fact stays in the skill. Where the obligations go has no home yet, so the split is carried as an open question rather than performed.

---

### Three entries leave the documentation handoff, each answered by the meta-layer body
- Time: 2026-10-04T18:19:38Z
- Type: Fixed
- Propagates to:
  - documentation.handoff.md: Done - the mixed-facet, citation-relation-boundary, and further-reader-relationship entries were removed; the meta-layer body already answers each (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - argued, applied

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided

#### What changed
- A `## Rejected positions` section was added to `documentation.practice.md`, giving the treatment of a rejected position three steps: the entry, section, or sentence whose claim is that position is deleted rather than annotated or kept as history; the alternative genuinely examined and not taken gets one `Considered and not done` line in the surviving entry; and the decision's positive statement stays in the document that holds the claim, with the changelog recording the outcome rather than the position it replaced.
- The restated copies those steps replace in `AGENTS.md` are gone: which fields a changelog entry carries and what it must not narrate is stated by [documentation-changelog.md → Structure](./changelog/changelog.md#structure) and [Trivial changes](./changelog/changelog.md#trivial-changes); where an examined alternative goes is [Considered and not done](./changelog/changelog.md#considered-and-not-done); what a body affirms and where a replaced formulation belongs is [documentation.md → Written surface](./documentation.md#written-surface); the folder README convention was already this document's own `## Folder READMEs` section.
- This entry was first written on the wrong file, `documentation-practice.changelog.md`, and was moved here by the changelog routing audit.

---

---

---

### Owed and planned capability marked in all three places
- Time: 2026-10-07T03:45:00Z
- Type: Changed
- Cited:
  - [Documentation — Comparison](./comparison/comparison.md) - Evidence: its Method requirements, added in the same chat from the tensorus and hindsight comparisons.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) gains a fifth rule: owed or planned capability is marked in prose, by a quiescent default in code, and by a pointer at the entry point; a claim implied by one surface and absent from the others is a fabrication in the rule's first sense.

#### Considered and not done
- **A requirement that check enforces it** (deferred): content check could later verify that owed rows, disabled defaults, and entry-point notes co-occur; decided against adding enforcement now, so the norm stands on its reasoning first.

---

### A folder README carries no changelog and no handoff
- Time: 2026-10-07T15:14:08Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) — drafted, applied

#### What changed
- [Folder READMEs](./documentation.practice.md#folder-readmes) gains a sixth step: a README has no `README.changelog.md` and no `README.handoff.md`. A decision about a folder is written into the README as the rule it now is; open work about a folder goes to the handoff of the module or document whose subject it is.
- Applied to the two READMEs that had companions. `docs/modules/README.md` took the one reason worth keeping into its body — why specification and realization are two trees — and that categories are not final. The open state of `modules/README.handoff.md` moved to the handoffs that own each subject: the category layout to [Modularity Handoff](../../../modules/knowledge/modularity/modularity.handoff.md#the-category-layout-of-this-repository), the archive findings to `modules/go-port/go-port.handoff.md`, `lib/`'s findings to `modules/lib/lib.handoff.md`, and the end-of-file convention to `modules/khayyam/rules/file-layout/file-layout.handoff.md`.

#### Considered and not done
- **Keeping a handoff beside a README that holds real open work** (rejected by the owner): the open work was always about some module's subject, and filed under the folder's index it had no owner to answer it.
- **Moving the count of broken links under `modules/`** (not done): `memar content check` reports it whenever it is run, so an entry restating the count would only go stale.

---

### Source standing admits a vendor's report of its own shipped product; every citation keeps Memar's reasoning its own
- Time: 2026-10-10T09:01:01Z
- Type: Changed
- Cited:
  - [Comparison: Memar and the Model Context Protocol](../../../docs/comparisons/mcp.001.md) - Reference: the essay whose two vendor posts, Anthropic's and Cloudflare's reports of their own shipped products, occasioned the change.
- Propagates to:
  - docs/comparisons/mcp.001.md: Done - its Method clause on the two vendor posts points to Source standing as the rule that admits them.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) — drafted, applied

#### What changed
- [Citations → Source standing](./documentation.md#citations): the list of sources without standing names a personal site or blog; a vendor's own technical documentation or engineering report of a product it ships is primary documentation of that product, supporting claims about what the product does, what it ships, and what the vendor reports measuring, each measurement stated as the vendor's report and never as a general result. The license test is unchanged: a work whose terms do not permit the use is not cited.
- The same paragraph states provenance for every citation, whatever its standing: a citation supports a claim about what its source itself shows or did and never presents Memar's reasoning as reached by that source; Memar's positions are stated as Memar's, and an outside source that agrees with one is never framed as its origin.

#### Decision
- The owner (Omid Hekayati, 2026-10-10) softened the rule so it does not read as a ban on citing a vendor's own report of its own product, keeping both his standing concerns explicit: a source whose terms do not permit the use is not cited, and no citation may let anyone later claim that Memar took its ideas from that source.

---

### Recording is not gated; removal is
- Time: 2026-10-10T14:30:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - An AI agent (via [Cursor](../../../CONTRIBUTORS.md#cursor)) — drafted, applied

#### What changed
- New section [Recording Is Not Gated; Removal Is](./documentation.md#recording-is-not-gated-removal-is): nothing the work learns goes unrecorded; a rule, an open question, a finding, or a note is written into the document that owns its subject when the work reaches it, without waiting for anyone's permission; open questions are recorded along the path of reasoning as they arise; removal is the act that loses information and the one that takes care — what removed text said is moved, kept, or stated in the changelog entry that removed it.
- The Abstract's list of cross-cutting conventions names it.
- Occasion: in a pricing session in the `organization` project, a sub-agent declined to add rules to two bare edges because "filling it would invent content the owner hasn't given", and the session moved a changelog entry rather than leaving it; the owner stated that documenting a lesson has always needed no one's permission and that only deleting text deserves sensitivity.

#### Considered and not done
- **Placing the rule only in Cognition's *Confirm before large-scope changes*** (rejected): the rule governs what every document receives and loses, which is documentation's subject; Cognition carries the boundary sentence that keeps its norm from gating additions, and links here.
- **Requiring additions to be proposed when they span several documents** (rejected): an addition loses nothing, and holding it for approval is the loss the rule prevents; the owning document's rules still judge its placement and content.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:50:00Z
- Type: Changed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to documentation.md, its handoff and this changelog against HEAD.
- The new section [Recording Is Not Gated; Removal Is](./documentation.md#recording-is-not-gated-removal-is) said open questions are recorded in "the owning document's open questions"; open questions live in the handoff, not the document, so it now says "the open questions of the owning document's handoff".
- The handoff's removals (*Mixed-facet documents*, *Further reader relationships*) are recorded by the 2026-10-04T18:19:38Z entry above, with the body sections that answer them.
- The path fixes in File Naming (`modules/identifier/media-type.md`, `bundles/khayyam/rules/`) point at existing paths. The counts in that paragraph (41 of 115, 26 folders) were not recounted; the hunk changed only a path.
- `memar content check` reports two broken links in this changelog (lines 296, 298: `memar-content.py` paths under `.agents/scripts/`); they are in committed text, not in this change, and were left.

---

### A README points; content that matters gets a document
- Time: 2026-10-12T10:57:14Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- New section [A README Points; Content Gets a Document](./documentation.md#a-readme-points-content-gets-a-document): content whose changes matter does not live in a folder README; finding it there is the signal to make it a document. Any agent may create a missing changelog for a document it changes.
- The citation-direction rule, today kept in docs/khayyam/README.md and docs/modules/README.md and not followed, is the standing instance; task 20261012-T105449Z-28376 gives it a document of its own.

---

### Citation direction gets a home here, and `memar content check` enforces it
- Time: 2026-10-12T11:40:00Z
- Type: Changed
- Propagates to:
  - `docs/modules/README.md`: Done — its **Citation direction** paragraph is one sentence pointing here
  - `docs/khayyam/README.md#citation-direction`: Done — its section is one sentence pointing here
  - [docs/README.md](../../../docs/README.md): Done — the `khayyam/` paragraph points here instead of restating the rule
  - `.agents/scripts/services/content_check.py`: Done — an upward relative link is reported as a problem, with its tests in `.agents/scripts/services/tests/content_check.py` (class `CitationDirection`)
  - Every document in `docs/` outside `docs/khayyam/`: Done — 658 upward links in 88 files turned into plain text
  - Every document in `docs/khayyam/`: Pending — 119 upward links, left to task 20261012-T105448Z-14472, which owns that folder
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- New section [Citation Direction](./documentation.md#citation-direction), stated once for the four layers of the written content, lowest first: base documents (`docs/` and its companions, `docs/comparisons/` among them), module documents (`docs/modules/`), the language (`docs/khayyam/`), and implementations and their documents (`bundles/` and the code tree `modules/`). A document links to its own layer or a lower one, never a higher one; a higher place is named in plain text and nothing is derived from it. The rule holds for every relative link — prose, `Propagates to` lines, changelog history — and for every relation, the inverse ones included. The Abstract's list of cross-cutting conventions names it.
- Until now the rule lived only in the READMEs of `docs/khayyam/` and `docs/modules/`, named only those two folders, and no tool tested it. The owner found it broken in `modularity.handoff.md`, which named `modules/go-port/` — a folder in the code tree that had already become an implementation's record — and linked above its layer. Measured when the check was first run: 777 upward links across `docs/`, 658 of them outside `docs/khayyam/`.
- `docs/modules/README.md` allowed a base document to reference a module document as a **consumed contract**. That nuance survives only in the downward direction: a higher layer applying a lower one's definitions is citing down; a base document consumes no module's contract, and names one in plain text where it must.
- The sweep: each upward link `[label](../../../docs/path#anchor)` became ``label (`path#anchor`)``, the path rooted at the repository, or the rooted code span alone where the label only repeated the path — the plain-text form [Links in recorded entries](./changelog/changelog.md#links-in-recorded-entries) already gives a link that no longer claims an address. Nothing was removed. The repair is trivial in [Trivial changes](./changelog/changelog.md#trivial-changes)'s sense for each document it touched, so this entry records it once rather than an entry per document; the one document whose content changed beyond its links, `modularity.handoff.md`, has its own entry in `modularity.changelog.md`.

#### Considered and not done
- **Keeping the rule in `docs/documentation.md`'s *Citations* section itself** (not done): that section defines the structured `Cited` field, while the direction rule governs every relative link, so it is a sibling section beside it.
- **Exempting changelog history** (not done): an entry's links are addresses into the current tree, not history, so they follow the rule like any other link.
- **Exempting every README** (not done): a README may link anywhere inside its own folder, which is what pointing is; a link out of its folder follows the rule.

---

### Owed capability is declared as `Owed: <id>`
- Time: 2026-10-13T10:45:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — drafted, applied

#### What changed
- The Content Rule's *Owed or planned capability* clause now names the declaration: a line `Owed: <id>`, the id a lowercase dotted slug and never a path, carried also by the title of a pending Test (`docs/modules/process/test.practice.md#the-cycle`). An id found on one side only is an inconsistency; a pending Test that passes while the mark remains is a hint, not an error; owed capability no Test can execute is marked the same way and judged by a reader.

#### Considered and not done
- **A path or version-pinned reference** (not done): it goes stale exactly when the document it points into changes.
- **Making "owed but satisfied" an error** (not done): the owner ruled it a hint, since the test passing cannot say which side is wrong.

---

### One Status vocabulary, defined once
- Time: 2026-10-13T10:40:00Z
- Type: Changed
- Propagates to:
  - `.agents/scripts/services/session_plan.py`, `session_report.py`, the other session readers, and `memar task --help`: Done (tasks `20261013-T103111Z-27036` and the sessions of topic `memar-projects`) - the plan's `open` and `done` become `Active` and `Complete`, the report's `Stop` line is read as a Status, and plan.md and report.md carry PascalCase front matter; readers first, writers a release later, as the proposal of task `20261013-T085819Z-2244` orders. The report carries a Status only (task `20261013-T142914Z-28176`): `session_report.py` reads the old `Outcome` and `Stop` words as the Status they leave, the report skeleton, the help, and the digest speak Status alone, and the old words are one table in the script, easy to change.
  - `.agents/skills/memar/SKILL.md` and [documentation-handoff.practice.md](./handoff/handoff.practice.md): Done (task `20261013-T111639Z-22724`) - wording that says a plan's Status is `open`, or names a "Stop line", changes with the writers.
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- New section [Status](./documentation.md#status) holds the one table of Status values, each with its meaning, the kinds that may use it, and whether it is safe to depend on: `Draft`, `Proposed`, `Final`, `Superseded`, `Rejected` for Explanation-facet documents; `Queued`, `Active`, `Blocked`, `Complete` for a task's plan; `Active`, `Paused`, `Blocked`, `Complete` for a handoff; `Active`, `Paused`, `Complete`, `Withdrawn` for a research. The one table serves a task's plan and its report: a value says which kinds may use it, so a value for the report alone would be a row whose only kind is the task report, and none is needed now. The section says how a run that ended unmet reads (budget ended or no progress: `Active`; stopped at an act needing approval: `Blocked`; the report's Result part says which), and when a plan and its report agree (equal Statuses). The Abstract names it among the cross-cutting conventions.
- The Explanation, Handoff and Research Status passages now link to it and keep only what is specific to the kind; the values themselves are stated nowhere else.
- Why: the values were defined in four places (the Explanation table, the Handoff line, the Research line, and the task plan's help text), the six endings had no document home, and the plan's `open` and `done` were the only words in the set that no document defined.
- Rests on recommended answers the owner has not yet given, from the proposal in task `20261013-T085819Z-2244`: (1) the plan's `open` and `done` unify with Handoff and Research as `Active` and `Complete`; (5) the home is this document, with the Handoff and Research placements unchanged; (6) no `Withdrawn` for a plan; the owner ruled (2026-10-13, task `20261013-T103111Z-30088`) that Status and the report's Outcome are one concept in one table, which replaced the proposal's decisions (2) and (3), a separate `Outcome` field with its own six words. The words `Active`/`Complete` for `open`/`done`, the PascalCase keys, and the lazy migration are accepted provisionally, so the script keeps them in tables that are one place to change. Decision 4 (PascalCase keys in plan.md and report.md, lazy migration) is not written in the document: the field-naming rule already covers it and the migration is script work.

#### Considered and not done
- **A new document for Status** (not done, proposed answer to decision 5): the section is cross-cutting like Results routing and File Naming, which already live here.
- **`Withdrawn` for a plan** (not done, proposed answer to decision 6): no plan has needed it, and the owner ruled that deleting a plan is meaningless; a table row is added with the kind when one does.
- **A second table, `Outcome`, for how a session's run ended** (not done, owner's ruling): `success` and `Complete` are the same thing, and two sections for one concept split it; the table's `Kinds that may use it` column carries the difference between a plan and a report.
- **Report-only Status values for `clean no-op`, `exhausted`, `no progress`, `approval-required`** (not done): each reads as `Complete`, `Active`, `Active`, `Blocked`, and the report's Result part says which, so none adds information a Status cannot carry; the owner accepts report-only values in the table, and the entry *Merged Status vocabulary: report-only values* in [documentation.handoff.md](./documentation.handoff.md) asks whether `clean no-op` should be one.

---

### A fact in code is written once
- Time: 2026-10-13T16:30:00Z
- Type: Added
- Cited:
  - [Modeling](../../../docs/modeling.md#one-authoritative-location-per-concerns-data) - Reference: a text copy of a fact in code is the derived copy with no re-derivation path that this section names.
- Propagates to:
  - `memar task --help`, `.agents/scripts/services/session_plan.py`, `session_report.py`: Pending - the Status values and the record fields are stated again in the help and in the scripts; the sessions of topic `memar-khayyam-types` make them one definition that the help calls.
  - The organization's rule of one file per human language: Pending - the third list item of the new section defers to it; a session of the topic writes it in the other repository.
  - [documentation.md](./documentation.md#status): Done (task `20261013-T190846Z-16860`) - the table is gone and the section names the type; see the entry *The Status table leaves documentation.md*.
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- New section [A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once). Where a fact is written in code, no place keeps a copy: a document names the type, a help text calls its methods.
- Five questions in order: 0 the presumption that everything is code unless shown otherwise, then 1 a program reads or branches on it, 2 a closed set or fixed shape, 3 stated in two places, 4 a reader must be persuaded, which alone shows otherwise. A statement holding a fact and its reason is split.
- The citation-direction case is settled: a base document does not embed a declaration and names the type by a code span path; a module document does the same; a document of the language or of an implementation may show a fragment as an example of syntax, which is text and defines no type's fact.
- Examples: Status, the task plan and report as records without a separate Outcome, and a service's inputs and outputs as types.
- The Content Rule's *No redundant restatement* bullet and the Abstract point to it.
- Rests on the owner's rulings of 2026-10-13 (task `20261013-T142915Z-8820`): the presumption, no copy of a code fact, concepts shown in code and documents referring to it, human-language descriptions in a file per language. Not yet reviewed by a session that did not write it.

#### Considered and not done
- **Letting a base document embed a short declaration** (not done): it is a copy no compiler checks, and it carries one language's syntax into the base layer.
- **Putting the rule in `modeling.md` beside Separating Structure (Code) from Policy (Rule)** (not done): there Code means the structural layer of a graph model, not a machine-read definition, and the two uses of the word would be read as one. The rule applies the existing modeling rule of one authoritative location and cites it.
- **Moving the base layer's concepts into code** (not done): a concept defined independent of every language, such as an error, stays prose; the open question *Does the presumption reach a concept defined at the base layer* in [documentation.handoff.md](./documentation.handoff.md) holds it for the owner.
- **Naming the per-language files and the `dt-` prefix in this section** (not done): they belong to the organizational rule and to the naming of basic types, each in a session of its own.

---

### The Status table is checked against the code that holds the vocabulary
- Time: 2026-10-13T16:16:00Z
- Type: Changed
- Propagates to:
  - `.agents/scripts/services/status.py`, `session_record.py`, `session_plan.py`, `session_report.py`, `session.py` and the other session readers: Done (task `20261013-T160505Z-29212`) - the Status values and the plan and report records are declared once and obtained from the types; no script spells a Status word.
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- A bullet in [Status](./documentation.md#status) names the code that holds the closed set (`status.py`, `session_record.py`) and says the table below is checked against it by `.agents/scripts/services/tests/status.py`, which renders the table from the type and fails on any difference.
- No value, meaning, kind or safety in the table changed: the code now holds all eleven values with the same text, so the gap between the table (eleven) and the scripts (four) is closed in the code's favour as the source, without losing a value.
- Rests on the owner's ruling of 2026-10-13 that the code is the source and the documents refer to it, and on [A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once). Not yet reviewed by a session that did not write it.

#### Considered and not done
- **Removing the table and naming the type only** (not done): the rule says a document lists no value of a code type, but the owner asked that the table be checked against the code, and the table is what a reader of the rule sees without opening code. The check keeps the two equal; whether the table should go is the open question *Status table or type: which is the source* in [documentation.handoff.md](./documentation.handoff.md).
- **Editing the prose bullet that says which ending leaves a report `Active`, `Blocked` or `Complete`** (not done): the mapping is now also in the type (`Status.report_ending`); the bullet keeps its reason and is left for the session that places the rest of the rule.

---

### The task records' shape is printed by `memar task ensure --help`
- Time: 2026-10-14T18:20:00Z
- Type: Changed
- Propagates to:
  - `.agents/scripts/services/session_new.py`: Done (task `20261014-T175052Z-9344`) - its help prints the plan's outline and the report's skeleton by calling the record types.
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus 5.5) - drafted, applied

#### What changed
- Two places, the *Task records* bullet under [A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once) and the bullet under [Status](./documentation.md#status) that names where the shape of plan.md and report.md is stated, now name `memar task ensure --help` in place of `memar task --help`.
- Why: by the owner's ruling of 2026-10-14 each command's help states only its own work; `new` is the verb that writes the two files, so their shape moved into its help, and `memar task --help` keeps the Status words and how a session ends.

---

### Practice description states a boundary
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- `documentation.practice.md`'s `description` now states what it is not: one facet's own procedure, which it routes to, and the schemas, naming, and language rules, which [Documentation — Practice → Description quality criteria](./practice/practice.md#description-quality-criteria) requires.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.

---

### Real code in its own file, examples in documents; the base refers to modules as concepts, and no link is removed to comply
- Time: 2026-10-16T00:07:29Z
- Type: Changed
- Propagates to:
  - `.agents/scripts/services/content_links.py` and its test `.agents/scripts/services/tests/content_check.py`: Done (tasks `20261015-T122252Z-5984` and `20261016-T075834Z-5360`) - the layer map has the two layers, and an upward link is printed as a warning, a debt, not counted as a problem.
  - `docs/khayyam/` documents, changelogs, handoffs and research, and the base documents that linked into the Documentation module: Pending (task `20261016-T075836Z-9780`) - the links that tasks `20261015-T122252Z-5984` and P6b turned into plain words are restored, pointing at the new paths.
  - Fences in documents that restate a real definition: Pending (task `20261015-T122303Z-23544`) - each is replaced by a pointer to the definition; an illustrative example stays.
  - `docs/khayyam/README.md`, `docs/README.md`, `docs/modules/README.md`, `modules/README.md`: Done (tasks `20261015-T122252Z-5984` and `20261016-T075834Z-5360`).
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled, approved the first wording, corrected its course on 2026-10-16
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus 5.5) — proposed, revised, applied, amended

#### What changed
- [A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once): code is any text a machine reads, and in Memar it is Khayyam, the official language; question 0 names Khayyam. Real code — a definition a machine reads, the one source of a fact — is written in its module's file, and a document of any layer refers to it and says why. An example is banned from no text: an illustrative example, written for a reader and taken by no program as a source, stays in its document in any language; a real example, one a tool or a test reads, is code and lives in a folder of examples (for Khayyam, one such as `bundles/khayyam/examples/`), which a document may refer to. An illustrative example that restates a real definition is replaced by a pointer to it. The paragraph that banned an embedded declaration in a base document alone, on the ground that the base is bound to no language, is removed.
- [Citation Direction](./documentation.md#citation-direction): two layers instead of four. The language documents are base documents, since the modules are written in the language and its grammar adopts no module's semantics; a module's documents and code are one layer, so a module's document links to its code. That a base document refers to a module only as a concept is the direction the base travels in, not a reason to delete a link: a link is never removed to comply, an existing upward link is a debt repaid when its text is upgraded conceptually, and a new one may be written where the text needs it. A base document's changelog and handoff, and a comparison essay, may name a file's path in a code span. The example of a base concept is Type, since no base document defines Error.
- `memar content check` maps the two layers and prints an upward link among its warnings, apart from its problems.
- `docs/khayyam/README.md`, `docs/README.md`, `docs/modules/README.md` and `modules/README.md` say the same.
- What happened between: the first application (task `20261015-T122252Z-5984`) stated that no document holds code, with a comparison essay excepted, and made an upward link a problem; to clear it, that chat turned 140 links from `docs/khayyam/` into plain words (88 labelled records in changelogs and handoffs, 52 concept names), and session P6b turned 187 links from base documents into the Documentation module into words and removed 19 parenthetical path code spans. The owner's answers of 2026-10-16 replaced the ban by the distinction above and ruled that a needed link is never deleted, whatever the reason: where only the link went and the text stayed, an implicit reference remains. Those conversions are to be undone (Propagates to, above); the comparison exception to the ban, which the ban alone made necessary, is removed.
- Why: the owner's rulings of 2026-10-14 (Khayyam official and allowed in all documents; no pseudocode), of 2026-10-15 (the base refers to modules as concepts; Khayyam's documents are base documents; documents beside their modules; code-span paths in base changelogs and handoffs, and in `docs/comparisons/`, stay allowed) and of 2026-10-16 (example code is not banned, only real code has its own file; a link is never removed to comply; the referencing principle belongs in the definition of concepts), split into sessions by task 20261014T113228Z-12672-0.
- The six open questions of 2026-10-14 in the [handoff](./documentation.handoff.md) are closed by these rulings: the Tentative statements of the section are rewritten; what "official" binds is answered by [Framework → Khayyam and Other Languages](../../../docs/framework.md#khayyam-and-other-languages); citation direction protects that a base claim holds without reading any module; where documentation lives is the open entry *The place of Documentation under Content is not final*; the code a document refers to lives in the module whose subject it is. The entry *Does the presumption reach a concept defined at the base layer* is restated as *Where does a base concept's Khayyam declaration live*. The entry *Does the principle of referencing belong in the definition of concepts* is opened (the owner leans to Terminology; not settled).
- Made in task 20261015-T122252Z-5984; amended in task 20261016-T075834Z-5360, before any commit, to the owner's answers of 2026-10-16.

#### Considered and not done
- **Keeping four layers and changing only their justification** (the handoff's earlier recommendation): it kept the language above the modules, which contradicts the grammar's refusal of protocol semantics and the owner's ruling that the language documents are base documents.
- **A Khayyam block in a document as a marked quotation compared to its source by a test**: it keeps a copy of real code on purpose; an illustrative example needs no such test, and a real definition is referred to, not quoted.
- **No document holds code** (the first application's rule): it removed illustrative examples a reader needs and called for exceptions it could not justify; the owner ruled on 2026-10-16 that only real code has its own file.
- **An upward link as a problem the check fails on** (the first application's rule): clearing it led sessions to delete links while the text still leaned on the module, which hides the reference rather than removing it; the owner ruled on 2026-10-16 that a link is never removed to comply.

---

### A facet is registered by its specification alone
- Time: 2026-10-16T15:10:00Z
- Type: Changed
- Propagates to:
  - documentation.handoff.md: Pending - its *Facet growth* item states that the `Facets currently defined` section "grows by one entry per facet", and its registry question reasons from "the current scale of five facets"; neither is true after this entry, and both need the state it leaves.
  - modules/content/documentation/plan/plan.md and modules/content/documentation/report/report.md: Done (task `20261016-T141543Z-22844`) - the two specifications this entry's first facet addition applies to; their own changelog entries record their creation.
  - modules/content/documentation/comparison/comparison.md: Done - its [Methodology](./comparison/comparison.md#methodology) says an essay's reader relationship "is none the five facets define"; the claim holds, the number is gone, and the file's own method is not this document's subject.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
The facet count and the facet enumeration this document held are gone, so that placing a specification in a subfolder named for its facet is the whole of registering one. Nine sentences changed, by line:

- `:9`, the opening: it "names the five facets currently in use" → it "says where the facets in use are specified and how one is added".
- `:12`, the Abstract: the five facets and their one-line definitions are replaced by the discovery rule — the facets in use are the specifications in this folder's subfolders, each subfolder named for its facet, and listing that folder finds them; the trailing "none of the five facets" → "none of the facets".
- `:35`, [Facet](./documentation.md#facet): "The facet itself is the meta-layer: it names the category, states what makes it distinct, and points to its specification" → a facet's name and what makes it distinct are stated in its own governing specification, so a facet added later needs nothing written here.
- `:37`: "doing five categorically different things" → "doing categorically different things"; "Forcing all five into one shared schema" → "Forcing every kind of content into one shared schema".
- `:40`, `Facets currently defined`: "Five facets are defined as of this document's current revision" → the placement rule, the statement that no count is held here, and the statement that a relationship none of the recognised ones answers enters the system by its specification alone.
- `:78`, [Which facet does a document belong to?](./documentation.md#which-facet-does-a-document-belong-to): one sentence added, saying which relationships a document is compared against and that one answering to none of them is Extensibility's case rather than a document outside the facets. The enumeration of the recognised relationships is kept here, and it is the only place one remains.
- `:81`, [Extensibility](./documentation.md#extensibility): rewritten. "Registering it here" and "a sixth facet could be added" are replaced by: a facet is added by writing its specification into a subfolder named for it and by nothing else; what the specification must state; and what a facet that needs a relationship none of those recognised answers changes.
- `:84`-`:88`, [Relationship between this document and its facet specifications](./documentation.md#relationship-between-this-document-and-its-facet-specifications): "The six files form a hierarchy" and the six-row table beneath it are removed, and the sentence "All six are Explanation-facet documents … are Research-facet documents" is restated without the count and without naming each facet. A new paragraph states the placement and discovery rule, and that each specification's own opening lines say what subject it governs.
- `:91`, [Comparison](./documentation.md#comparison-a-document-kind-outside-the-facets): "like the six above" → "like the facet specifications beside it".

**Why none of this is the derivative inventory the Content Rule forbids.** The removed table was one: a list of this folder's files with their roles, mirroring a live collection. Every replacement points at the authoritative location instead — this folder's subfolders — which is what [Content Rule → No derivative inventories](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) asks a document to do ("Point the reader at the authoritative location (list the directory …) instead"). What remains per facet is not a membership entry but content: what a reader of that kind of document is expected to do, and what that relationship costs to confuse with the others — judgment the folder does not contain and cannot be derived from it. Two of the changed sentences (`:40` and `:81`) say outright that this document holds no count and registers nothing, so a reader is not sent here to enumerate.

**What this leaves open, by choice.** `### Facets currently defined` still describes the reader relationships already recognised, one `####` heading each, and a facet whose relationship is a new one does not get an entry there: it enters by its specification. The trade is stated rather than hidden — the relationships already recognised stay comparable to each other at the point a document is placed, and a relationship outside them is given a facet whose own specification states it. Removing those `####` sections altogether would mean moving each facet's definition and the judgment around it into that facet's specification, which is five more documents than this change touched.

#### Considered and not done
- **Rewriting the enumerations as a list of seven facets** (the first draft's route): it is the inventory the Content Rule forbids, and it keeps the count as a fact this document holds, which is what the owner ruled against.
- **Printing the shape of the records in `memar task ensure --help` by calling the record type**, which `session_record.py`'s own docstring claims it does: out of scope here, and `tests/session.py` pins that help's wording; the claim in that docstring is left standing and recorded below.
- **Moving the `####` facet definitions into the five existing facet specifications**: the remedy for the residue named above, deferred because it reaches five specifications this change did not touch.

---

### The facet definitions leave documentation.md for each facet's own specification
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - explanation, practice, changelog, handoff and research specifications under modules/content/documentation/: Done (task `20261016-T150928Z-4276`) - each holds its own `Reader relationship` section, recorded in its changelog.
  - plan and report specifications under modules/content/documentation/: Done (task `20261016-T150928Z-4276`) - the two facets `documentation.md` never defined; they still read whole.
  - documentation.handoff.md: Done - its *Facet growth* item already states that a new facet edits nothing here.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The section `Facets currently defined` and its five `####` definitions are gone from [documentation.md](./documentation.md). Each definition moved to the facet's own `Reader relationship` section: Explanation, Practice, Changelog, Handoff and Research each received what was said of them here, merged with what their specification already stated; Comparison is not a facet and is untouched; Plan and Report never had a definition here.
- The Introduction's account of how each facet arose (the third need, the three ecosystems, the Changelog and Handoff precedents) is no longer here; [Motivation](./documentation.md#motivation) and [Methodology](./documentation.md#methodology) say each facet's specification states it, and the content is in those specifications' Motivation, Methodology and Abstract.
- [Which facet does a document belong to?](./documentation.md#which-facet-does-a-document-belong-to) no longer lists the five purposes: it tells the author to compare against the relationship each specification states, found by listing this folder.
- [Extensibility](./documentation.md#extensibility) and [Relationship between this document and its facet specifications](./documentation.md#relationship-between-this-document-and-its-facet-specifications) name no facet and no count.
- The earlier entry *A facet is registered by its specification alone* said the enumeration at `:78` was kept and the `####` sections remained; this entry removes both, which is the remedy that entry named. Its two links to the removed section were taken out of link form into code spans, as [Links in recorded entries](./changelog/changelog.md#links-in-recorded-entries) says.
- Made in task 20261016-T150928Z-4276.

**Why none of this is the derivative inventory the Content Rule forbids.** What replaces the definitions is a pointer to the folder and the rule that each specification states its own relationship; no list of facets, no count and no table is kept here, so the next facet edits only its own module. `memar content backlinks` found no document linking into the removed section.

#### Considered and not done
- **A shorter list of the facets, each with a link**: it is the inventory the Content Rule forbids, and the next facet would edit this document again.
- **Keeping the `Facets currently defined` heading with a pointer under it**: the heading would name a set this document does not hold.

---

### The Status table leaves documentation.md
- Time: 2026-10-16T19:23:38Z
- Type: Removed
- Propagates to:
  - [explanation.md](./explanation/explanation.md#status), [handoff.md](./handoff/handoff.md#status), [research.md](./research/research.md#status-mandatory): Done (task `20261016-T194830Z-21416`) - each listed the Status values its kind may take, a copy of what `Status.for_kind` gives under the same ruling; removing them is a removal in three facet specifications, left to the owner.
  - [documentation.handoff.md](./documentation.handoff.md): Done - the entry *Status table or type: which is the source* is answered by the ruling and removed.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus 5.5) — applied

#### What changed
- The table of eleven Status values (value, meaning, kinds, safe to depend on) is gone from [Status](./documentation.md#status). The section keeps its rules and reasons and names `.agents/scripts/services/status.py` as the one declaration of the values; a value is read, added or changed in the type alone. It says the type is a Python class now and a Khayyam capsule later, and that its place under `.agents/scripts` is not settled.
- The test that rendered the table from the type and compared it with this document (`TableEqualsCode` in `.agents/scripts/services/tests/status.py`) and the method it called (`Status.table_lines`) are removed: with no copy there is nothing to keep equal.
- The owner's ruling of 2026-10-16 decides it: every field documentation declares is a type, and once typed the prose restating it leaves the document, keeping only reason and explanation.
- Made in task 20261013-T190846Z-16860.

#### Considered and not done
- **Keeping the table as a checked copy**: the earlier recommendation, until the table could be generated. The ruling removes restating prose whether or not it is checked, and the owner named the check an extra cost.
- **A `memar content` verb that prints the table from the type**: no reader needs it now; it is left as a question in task 20261013-T190846Z-16860's report.

---

### The declarations this specification names moved out of services/
- Time: 2026-10-17T09:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Status](./documentation.md#status): the closed set of values is declared in `modules/content/documentation/primitive/status.py` and the shape of a task's plan and report in `modules/content/documentation/record.py`, not in the scripts' `services/`. No value or rule changed.
- Why: the owner's rulings of 2026-10-17 place a module's primitive types in the module's own `primitive/` and the shapes built from them in its root; the Status type and the task record's shape were the first moved out of the scripts' `services/`.
- Made in task 20261017-T082614Z-25876.

---

### Bulk edits skip symbolic-link READMEs
- Time: 2026-10-19T00:00:00Z
- Type: Added
- Ruling: owner, 2026-10-18/19 (in the organization repository); carried here when organization merged into memar (task 20261018-T133019Z-4704)
- Contributors:
  - Claude Opus 5.5 - applied

#### What changed
- [Folder READMEs](./documentation.practice.md#folder-readmes), step 4, gains one sentence: on a host without symbolic links a README link is a text file with no final newline, and a bulk pass skips every mode-`120000` path. A "final newline" pass in organization changed 89 such links and the owner called the result sloppy; the lesson was kept only in an agent's private memory and is recorded here so that it binds every session.

---

### Documentation is a pluggable module
- Time: 2026-10-24T09:20:00Z
- Type: Changed
- Cited:
  - [Pluggable](../../../modules/knowledge/modularity/labels/pluggable.md) - Reference: the test of a pluggable module
- Tasks:
  - main:.agents/tasks/20261018-T133018Z-26648/: Partial - the placement; the owner ruled it (2026-10-24)
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled that documentation was always a structure laid over content and text
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — moved it and repaired the references

#### What changed
- The module moved from `modules/knowledge/documentation/` to `modules-plugable/knowledge/documentation/`, with every link, import and path that named it. Before the move the facets the task module reads left it: the Plan and Report records went to the task module, the Status type to the Status module, the Label types to the Label module, and the closed-vocabulary bases (`Word`, `Section`, `RecordKey`) to the content module's `primitive/`; nothing in `modules/` imports it now.
- It received the services of the documentation discipline that were in the content module (`services/`): the changelog record and append, the questions, the propagations, the owed marks, the normative-references lists and their check, the document ID, and `memar content check` as the composer of the domains' checks.
- Marks of the lists of normative references whose section only changed in its links were re-marked (11 entries, each shown to differ only in references).

#### Considered and not done
- Keeping the kernel facets that the task module reads: a kernel module may not import a pluggable one, and an allowance was not needed once they moved.
