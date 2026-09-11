# Documentation — Explanation Changelog
This document records why and how `documentation-explanation.md` changed over time. See [Documentation — Changelog](./documentation-changelog.md) for what this file's structure means.

## Changelog

### Historical entries (pre-Changelog-facet)
- Time: unknown (historical import — only relative order is known; see [Documentation — Changelog → Unresolved questions](./documentation-changelog.md#unresolved-questions) for why no timestamp was invented)
- Cited:
  - [Diátaxis](https://diataxis.fr/) — Reference: cited historically (entry 13) as prior art for separating procedural content from reference/explanation content. This citation is preserved here as historical record; it is not repeated in the base document's own text going forward, per the current rule that argumentative citations live only in the changelog.
  - [Architecture Decisions: Demystifying Architecture](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-jeff-tyree-and-art-akerman/index.md) — Reference: cited historically (entry 12) as independent evidence that separately-designed, single-purpose templates converge on the same underlying concerns under different names. A widely-cited independent architecture-decision-record template, examined as evidence that independently-designed templates for a single document purpose (here, ADR) still converge on the same handful of underlying concerns (claim, rationale, alternatives, consequences, related decisions) as this specification's own Optional Sections catalog, just under different names.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati)
  - [Claude](../CONTRIBUTORS.md#claude) - claude-sonnet-5
  - [Super Z](../CONTRIBUTORS.md#super-z) - GLM 5.2
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) - GPT 5.5

#### What changed
The thirteen entries below are migrated as-is from `documentation-explanation.md`'s former `## Change Rationale` section (itself a rename of an even earlier `rfc-template.md`'s Change Rationale, going back to before the Explanation/Practice/Changelog facet split existed). Individual contributor roles per historical entry were not tracked at the time and are not reconstructed retroactively — only the registry is known reliably. Going forward, new entries use the full structure defined in `documentation-changelog.md`.

1. **Initial consolidation.** Consolidated the RFC template and its field specifications into a single specification, motivated by the loading cost of feeding multiple files into every chat session and the drift risk between the template and its specs. A pre-Final merging rule allows related Draft/Proposed RFCs to be consolidated without generating a new RFC number. A contributor preservation rule requires every contributor to add their own entry and forbids modifying others'.
2. **Second revision.** Fixed front-matter self-inconsistencies: `Applied to` contained `["*"]` while `Status` was `Proposed`, contradicting the Status table (emptied, with a clarifying rule); `Start Date` had drifted from the date implied by `RFC Number` (corrected). Clarified the Contributor preservation rule governs every RFC, not only this document. Corrected an inaccurate claim in the `Related RFCs` `URI` field description. Replaced vague merge-numbering guidance with an explicit tie-break rule. Generalized collision-resolution guidance away from a specific PR-based mechanism.
3. **Third revision.** Replaced the flat content-type-first organization of Reference-level explanation with a topic-first structure after confirming, against a real RFC (`protocol.md`), that content was genuinely scattered across up to six top-level sections. Introduced the RFC-wide `Discussion` section, kept separate from `Change Rationale`. Moved `The Template` into Guide-level explanation. Removed `Contribution` in favor of Task-based tracking, requiring at least one `Tasks` entry per contributor. Shortened and refocused Motivation on a shared structure across Geniuses Group's projects rather than a Memar-specific concern.
4. **Fourth revision.** Fixed a malformed internal reference and added an explicit rule that all internal section references must be real hyperlinks. Removed `Common concepts`, promoting `URI` to its own Reference-level topic. Relocated `Field Naming Convention` from `Discussion` to `Reference-level explanation`. Documented the recursive sub-section/Discussion nesting pattern. Rewrote Guide-level explanation to be self-contained for the ordinary case. Added an explicit rule that `Tasks` entries should be short and headline-style. Refined the Contributors preservation rule to allow pruning stale claims.
5. **Fifth revision.** Merged `Tasks`' `Titles` and `Explanation` fields into a single `Works` field after this document's own Contributors list showed the predicted failure mode in practice. Logged an Unresolved question under `Related RFCs` about the `Depends_on`/`Reference` boundary, deferred to a dedicated future session.
6. **Sixth revision.** Renamed `Summary` to `Abstract` and rewrote its content to state this document's actual claim rather than give navigational instructions. Introduced `Introduction` (`Motivation`, `Methodology`) and `Explanation` (`Guide-level explanation`, `Reference-level explanation`) as wrapper sections. Added `Results`, defined as strictly retrospective. Renamed `Related RFCs` to `Citations`, broadening its scope to non-RFC sources, and corrected an inverted field pairing (`Relation` now holds the relationship category, `Reason` the free-text justification). Added source-credibility criteria for external citations. Considered and rejected relocating `Prior art` to an early, standalone section. Added a progressive migration rule. Generalized the "custom subsection with a stated reason" allowance to `Introduction` and `Explanation`'s own subsections. Noted, as a newly surfaced constraint, that the deepest defined nesting level reached the maximum heading depth Markdown/HTML supports.
7. **Seventh revision.** Removed the fixed `Guide-level explanation` / `Reference-level explanation` heading pair, recognizing that forcing every RFC's practical walkthrough under a literal "explanation"-suffixed name was itself inconsistent with the observation that such content, in this document's own case, does not explain anything — it documents usage. Topics moved directly under `Explanation` in author-chosen order and names. An RFC could optionally designate one topic as an illustrative walkthrough, linked from the Abstract labeled "Guide."
8. **Eighth revision.** Fixed inconsistencies found by comparing against the file actually supplied: unified the Discussion pattern so every topic wraps rationale-type content consistently. `Suggested Naming Conventions` made a consistent sibling of `Discussion`. Moved `File` to be the first real topic. Removed duplicate sentences.
9. **Ninth revision.** Worked from the file actually supplied, incorporating its own restructuring (grouping conventions, pulling the Discussion pattern out of Body sections) while fixing execution issues.
10. **Tenth revision.** Fixed a heading-level mismatch between prose and example. Corrected a misunderstanding of a `Conventions` heading appearing twice with two distinct, both-valid meanings. Removed a `Motivation and Methodology` topic that had bundled two unrelated concepts. Broadened a naming-only convention item into a general `Conventions` item.
11. **Eleventh revision.** Renamed this specification from `rfc-template.md` (`RFC Template Specification`) to `documentation.md` (`Documentation Framework Specification`), following an extended discussion on knowledge management concluding that `RFC`, `PRD`, `ADR`, and similar labels are better treated as profiles applied to one shared documentation structure than as independent document types requiring separate templates. `RFC Number` was renamed to `ID` throughout.
12. **Twelfth revision.** Shortened `Title` to match the actual filename. Removed a `Document Profiles` topic in favor of a single shared structure plus a growing `Optional Sections` catalog. Expanded `Optional Sections` with `Definition`, `Assumptions and Constraints`, `Implications`, and `Examples` after screening a larger candidate list. Added the Tyree-Akerman architecture-decision-record template as Prior art. Added a `Contributors` entry for ChatGPT.
13. **Thirteenth revision.** Moved the procedural "how to make a new document" walkthrough out of this specification entirely, into a companion Skill file, on the principle that a document following this specification describes structure, not step-by-step procedure — the distinction the Diátaxis documentation framework draws between reference/explanation and tutorials/how-to guides, cited here as Prior art at the time. The `Guide` convention was widened to allow linking to an external Skill file.

### Split into Explanation, Practice, and Changelog facets
- Time: unknown (historical import — occurred after the thirteen entries above, before this file's creation)
- Cited:
  - [Documentation](./documentation.md) — Depends_for: this document is the Explanation facet `documentation.md` defines the concept of.
  - [Modeling](./modeling.md) — Depends_on: documentation is treated as the result of correct modeling; the concept of documentation cannot be understood or defined independently from the modeling process.
- Contributors:
  - See the project-wide [CONTRIBUTORS.md](../CONTRIBUTORS.md) registry.

#### What changed
`documentation.md` was split into three files: this document's base (`documentation-explanation.md`, keeping the original `ID`, as substantive successor), a new lightweight meta-specification (`documentation.md`) defining the Facet concept, and `documentation-practice.md` governing the Practice facet, adopting the schema independently converged on by Anthropic, OpenAI, and Microsoft's own skill-creator files rather than inventing a new one.

### Created the paired practice file
- Time: 2026-07-25T00:00:00Z
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: this practice file is the procedure for producing an Explanation-facet document; the structure it produces is defined by that specification, not repeated here.
  - [Documentation](./documentation.md) — Reference: the meta-layer that defines what a Facet is and why Practice-facet files exist alongside Explanation-facet specifications.
- Contributors:
  - See the project-wide [CONTRIBUTORS.md](../CONTRIBUTORS.md) registry.

#### What changed
Created as the Practice-facet companion to `documentation-explanation.md`, following the Practice facet's schema (name/description-only front matter, imperative body, under ~500 lines). Walks a contributor through producing a new Explanation-facet document: copying the template, generating the `ID`, filling in front matter, writing the body, and progressive migration of older documents.

### Migrated Citations, Contributors, and Applied to into this changelog file
- Time: 2026-08-05T08:51:08Z
- Type: Changed
- Cited:
  - [Documentation](./documentation.md) — Depends_on: this document specifies the Explanation facet defined by documentation.md; the Facet concept itself, and why Explanation is governed separately from Practice, is defined there, not repeated here.
  - [Modeling](./modeling.md) — Depends_on: Documentation is the result of correct modeling. The concept of Documentation cannot be understood or defined independently from the modeling process.
  - [Architecture Decisions: Demystifying Architecture](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-jeff-tyree-and-art-akerman/index.md) — Reference: a widely-cited independent architecture-decision-record template, examined as evidence that independently-designed templates for a single document purpose (here, ADR) still converge on the same handful of underlying concerns (claim, rationale, alternatives, consequences, related decisions) as this specification's own Optional Sections catalog, just under different names.
  - [Diátaxis](https://diataxis.fr/) — Reference: supports treating procedural how-to content as categorically distinct from the reference/explanation content this specification governs, motivating the separation of Skill files from documents following this specification.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued

#### What changed
Per the decision to move all provenance (citations, contributor attribution, cross-document propagation tracking) out of Explanation-facet base documents and into their paired Changelog-facet file, this document was created. `documentation-explanation.md`'s own front-matter `Citations` and `Contributors` fields, and its `## Change Rationale` section, are superseded by this file and should be removed from the base document (tracked separately — see Propagates to).

- This changelog file was extracted from `documentation-explanation.md`'s front-matter `Citations`/`Contributors` and body `## Change Rationale` (Claude).

Claims migrated from the pre-finalization Contributors roster, concerning the historical revisions recorded in the "Historical entries (pre-Changelog-facet)" entry above:

- The specification was drafted and revised across multiple rounds; regressions and naming collisions in the supplied file's own restructuring were fixed; and the specification was renamed and generalized to document-generic wording (Claude).
- Contributors were migrated to Task-based tracking; the Abstract/Introduction/Explanation restructuring and the author-named Guide-topic convention were implemented; Optional Sections were expanded with Definition/Assumptions and Constraints/Implications/Examples, screened against duplicate-concept overlap; and procedural how-to content was moved into a companion Skill file, citing Diátaxis as prior art for the separation (Claude).
- An earlier revision's section layout was restructured, and the pre-Final merging and contributor-preservation rules were applied (Super Z).
- Multiple front-matter inconsistencies were caught (Omid Hekayati).

#### Deliberation
- Every revision was directed (Omid Hekayati).
- The merge-numbering and collision-resolution rules were resolved (Omid Hekayati).
- The topic-first Reference-level structure and the Discussion section were proposed (Claude).
- The Contribution-to-Task decision was resolved (Omid Hekayati).
- The Abstract/Introduction/Explanation restructuring was directed (Omid Hekayati).
- Removing the fixed Guide-level/Reference-level headings in favor of an author-named, Abstract-linked Guide topic was proposed (Omid Hekayati).
- One shared documentation structure with RFC/PRD/ADR as profiles, not independent templates, was argued for (ChatGPT).
- The generalization from RFC-specific to document-generic scope was directed (Omid Hekayati).
- The Optional Sections catalog was proposed as the mechanism for that generalization, over a formal Profile abstraction (Omid Hekayati).
- Model/Risks/Problem were suggested as candidate catalog items (ChatGPT).
- The cross-discipline scientific-paper analogy and the token-equality argument used in this specification's own Optional Sections framing were drawn (ChatGPT).

#### Propagates to
- `documentation-explanation.md`: Done — removed front-matter `Citations`, `Contributors`, `Applied to`; removed `## Change Rationale` section; removed the now-redundant `### Citations`, `### Contributors`, `### Applied to` topic definitions from its body (these concepts are now defined here and in `documentation-changelog.md` instead); removed the obsolete `Guide`/optional-topic mechanism now that Practice-facet files handle procedural content generally.
- `documentation.md`: Done — same front-matter cleanup; added an explicit rule that procedural content belongs in a companion `<base>.practice.md` file rather than an internal Guide topic.

### Moved URI definition to the meta-layer as a cross-cutting concern
- Time: 2026-08-11T00:00:00Z
- Type: Changed
- Cited:
  - [Documentation](./documentation.md) — Depends_for: the URI format (absolute vs. relative reference, the `file:` scheme prohibition) is now defined there as a cross-cutting convention, applying wherever a URI appears in any document of any facet.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- The `#### URI` subsection under `### Conventions` was the canonical definition of URI format (absolute vs. relative reference) and the `file:` scheme prohibition. That rule applies wherever a URI appears — internal hyperlinks, citation entries, contributor identity, examples — in any document of any facet, not only in Explanation-facet documents.
- The definition was moved to `documentation.md → URI` as a cross-cutting convention, and this specification's `#### URI` subsection — a full subsection carrying the RFC 3986 definition, the two forms, the `file:` prohibition, and the note about provenance fields having moved to the Changelog — was trimmed to a one-line reference pointing there.
- The Internal Cross-References example was updated from `[URI](#uri)` — which would have become a broken anchor once the `#### URI` subsection was removed — to `[Conventions](#conventions)`, an example that remains valid.

#### Deliberation
- The `#### URI` subsection under `### Conventions` was defining a rule (the `file:` scheme prohibition) that applies to any document of any facet, not only Explanation-facet documents (Omid Hekayati — argued).
- Keeping it here made this specification the de facto canonical home for a cross-cutting concern, which is the wrong place (Omid Hekayati — argued).

#### Considered and not done
- **Keep the URI definition here, since this specification is where it has always lived (rejected)**: would have left a cross-cutting concern canonically defined in a facet-specific specification. The Changelog spec would either have had to redefine the same rule (drift risk) or reference this specification's URI subsection (making the Explanation spec an implicit meta-layer for the Changelog spec, which inverts the intended hierarchy).
- **Remove the `#### URI` subsection entirely, with no replacement reference (considered, not chosen)**: would have left a reader of this specification's `### Conventions` section with no signal that URI format is governed by a project-wide rule. A one-line reference costs almost nothing and saves the reader from accidentally defining a non-portable URI scheme inline.

### Aligned the practice file with the post-Changelog-facet specification
- Time: 2026-08-11T00:00:00Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: the base specification's body skeleton dropped `Change Rationale` and the `Applied to`/`Citations`/`Contributors` front-matter fields as part of the Changelog-facet migration; the practice file was updated to match.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: step 6 of the practice's procedure creates a paired Changelog-facet file, whose structure is defined by that specification.
  - [Documentation](./documentation.md) — Reference: added to the practice's Reference files list because the cross-cutting Citations and URI conventions now live there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
The practice file had been missed when the Changelog-facet migration was applied to the rest of the documentation set: its procedure was still instructing a contributor to fill in `Applied to`, `Citations`, and `Contributors` in the base document's front matter and to keep a `## Change Rationale` body section, all of which the base specification no longer permits. Brought in line: front-matter instructions cover only `Title`, `Status`, `Start Date`, `ID`; the Template drops the migrated fields and section; the obsolete "Guide" topic convention is removed; step 6 now creates the paired `<base>.changelog.md` file and migrates older documents' former provenance fields into Changelog entries; and the `documentation-changelog.md` reference was added.

#### Deliberation
- The practice file had been missed during the earlier round of changes that moved provenance out of Explanation-facet base documents into the Changelog facet (Omid Hekayati — pointed out).

#### Considered and not done
- **Keep the "Guide" topic convention in the practice's step 4 (rejected)**: the Guide/optional-topic mechanism was removed in favor of the Practice facet's companion-file convention — instructing the contributor to also create an internal "Guide" topic would re-introduce the obsolete convention the practice file itself replaces.

---

### Method finalized; body restructured; discussion content relocated per the finalized method
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Propagates to:
  - documentation-explanation.handoff.md: Created - this specification's open questions and anticipated work moved there.
  - documentation-changelog.md: Done - entry structure restructured (What changed / Considered and not done / Related work / Decision; Contributors presence-only) in the same pass.
  - documentation-handoff.md: Done - Open Questions / Anticipated Work structure added; open-question residence rule stated in the same pass.
  - documentation-handoff.practice.md: Done - no changes needed (verified clean).
  - documentation-explanation.practice.md: Done - template and steps rewritten to follow the finalized body structure.
  - All documents reformed under the new pattern: process.md, error.md, memory.md, concurrency.md, dependency-management.md, time.md, networking.md, networking-connection.md, sRPC.md, modeling.md, type.md (in this session's scope; others migrate progressively).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - reviewed, argued, rewrote, moved

#### What changed
- The `Discussion` wrapper is dissolved entirely, and `Drawbacks` with it (Omid Hekayati - the wrapper's content, on inspection, was questions in declarative clothing and evaluations the current-state reader does not need; an explanatory document is not a place for doubt, and an AI-assisted reader cannot reliably separate a negated position from an affirmed one when loading a body into context).
- The body's fixed top-level sections are reduced to `Abstract`, `Introduction`, `Explanation`, `Results` (Omid Hekayati - the four-section skeleton with an open catalog is clearer than a five-section skeleton carrying a doubt-shaped wrapper; Super Z - applied).
- `Rationale and alternatives` leaves the body: rejected-alternative reasoning is decision-shaping context and lives in the changelog entry's `Considered and not done` section (Omid Hekayati - directed; Super Z - named the section).
- `Future possibilities` leaves the body for the handoff's `Anticipated Work` section (Omid Hekayati - decided; Super Z - had flagged it as an open question in the same session and recorded it rather than deciding).
- `Prior art` is retired as a title and its two functions split (Omid Hekayati - identified the title as wrong from the start, citing the patent-law sense of the term; Super Z - proposed the split): premise evidence stays inline at the claim it supports; comparative surveys become the changelog entry's `Related work` section.
- `Unresolved questions` are retired as a title; open questions live in the handoff as `Open Questions`, distinct in name from anything in a base document (Omid Hekayati - no two documentation types should carry identical titles; Super Z - applied).
- Changelog entries restructured: `Summary` becomes `What changed`; `Considered and not done`, `Related work`, and `Decision` added as optional entry sections (Omid Hekayati - demanded structured sections instead of prose Summary after seeing migrated content flattened into narrative; Super Z - written).
- The Contributors bullet shrinks to presence plus role tags; every substantive claim in an entry carries its attribution inline in parentheses, so statements and their authors never separate (Omid Hekayati - the role prose had grown and scattered attribution; Super Z - wrote the rule).
- The Relevance discipline convention added: a body statement earns its place by serving the current-state reader; decision-shaping context is changelog content regardless of which body section it would sit in (Omid Hekayati - the criterion's two-reader framing approved; Super Z - written).
- This specification's own body was reformed under the pattern it prescribes: the Status field's, ID field's, and Progressive migration topic's rationale-and-alternatives and question content, the document-level Rationale and Future sections, and the ecosystem-survey narratives (Rust RFC template organization, Rust/IETF numbering schemes, the Tyree-and-Akerman ADR template survey) moved to this changelog and the paired handoff (Super Z).
- A final audit found several `Rationale and alternatives`, `Prior art`, and `Unresolved questions` blocks that the earlier passes missed; all are recorded below and in the paired handoff (Super Z - audit and migration).
- The practice companion (`documentation-explanation.practice.md`) reformed: template shows the four fixed sections only with `{Sub section}` placeholders marked as Optional Sections candidates; steps rewritten to route rejected alternatives, open questions, and anticipated work to the changelog entry and handoff respectively (Omid Hekayati - supplied the corrected template shape; Super Z - applied).

#### Considered and not done
- Renaming the body's evidence practice with a new titled wrapper (`Evidence`) (Super Z - proposed, then withdrawn): evidence is cited inline at claims, so no wrapper title is needed; the changelog `Cited` field's existing `Evidence` relation already carries the word.
- Keeping `Future possibilities` in the body pending separate review (Super Z - flagged the question) (Omid Hekayati - decided immediately against: same criterion as the other removals).
- Keeping a `Discussion` wrapper that holds only `Drawbacks` (rejected): a wrapper for a single optional section is structural weight with no routing content left inside; the section enters the catalog directly. (Omid Hekayati)
- Keeping `Rationale and alternatives` as a body wrapper so the design's rejected alternatives stay near their decision (rejected): the AI-loading hazard outweighs locality; the changelog's `Considered and not done` carries them. (Omid Hekayati)
- A lint-style check for provenance in bodies (Super Z - proposed): premature without tooling; the convention plus review is the current enforcement.
- A dedicated one-time migration pass across all existing documents (rejected): the progressive-migration rule applies; each file migrates at its next natural edit. (Super Z)
- Maintaining this detailed Status semantics alongside the compact table in `README.md` means the two must stay consistent as either evolves; the specification also elaborates obligations without precisely defining what counts as a correction small enough to apply in place versus a change substantial enough to require a superseding document. (Super Z - migrated from Status field)
- The ID number is no longer purely arbitrary - it encodes creation order, a deliberate exception justified because creation time is immutable. Collisions at hour granularity must currently be resolved manually - a stopgap, since no tooling exists. Retroactive backfilling for documents sharing a `Start Date` has no principled ordering signal. (Super Z - migrated from ID field)
- Consolidating the specification and its field specifications into one document means they can no longer be loaded independently; the document is longer than any of its predecessors, and there is no way to load only part of it into context. The mitigating factor - the Abstract being self-contained for the ordinary case - was already stated in the body's usage guidance and stays there. (Super Z - migrated from document level)

#### Related work
- The Rust RFC process maintains a single `0000-template.md` plus a separate process README rather than consolidating template and per-field specifications; this project consolidated because its AI-assisted document-writing sessions make multi-file loading costs salient. (Super Z - migrated)
- Rust's RFC numbering assigns no number at drafting (a `0000-` placeholder until a PR exists, then the PR's number), with an internal preference for small continuous-feeling numbers; IETF RFCs are strictly sequential and centrally assigned. (Super Z - migrated)
- The Jeff Tyree and Art Akerman architecture-decision-record template maps closely onto this specification's concerns, with `Implications` its one genuinely distinct contribution, adopted into Optional Sections. (Super Z - migrated)

#### Decision
All retired wrapper titles are removed from the pattern; documents written under the old pattern migrate progressively on their next natural edit. Open questions (Optional Sections catalog extensions, Future-possibilities disposition, spec-split threshold, ID collision tooling) and anticipated work live in the paired handoff. (Omid Hekayati - approved)

### Removed the specification's own stale references to the retired Discussion section
- Time: 2026-09-08T08:23:05Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) - wrote

#### What changed
- The finalization had left the specification contradicting itself: the Abstract still listed `Discussion` as a fifth body section, and the Optional Sections intro still said "the fixed five" and named `Discussion` as a nesting host - both corrected to the four fixed sections the `Body sections` rule states.
- The `Conventions` catalog entry pointed at "that topic's `Discussion`" as its sibling anchor; reworded to "that topic's other subsections", since topic-level Discussion wrappers retire together with the document-level one.
- The scientific-paper analogy's use of "Discussion" describes external paper conventions, not this specification's skeleton, and was kept.
- Surfaced during the 2026-09-07 commit-readiness review of the second migration wave; the owner directed closing it before that wave is briefed, and the wave itself is now tracked in the paired handoff.

### Results section removed; skeleton reduced to three fixed sections; results routing established
- Time: 2026-09-10T16:57:44Z
- Type: Changed
- Cited:
  - [ICMJE Recommendations](https://www.icmje.org/recommendations/) — Evidence: the manuscript-preparation standard requires findings presented in logical sequence with the main findings first, and places interpretation, context against the totality of evidence, and conclusions beyond the data in Discussion, not Results.
  - [Bavdekar SB, Chandak S. Results: Unraveling the Findings. J Assoc Physicians India. 2015;63(9):44-6](https://pubmed.ncbi.nlm.nih.gov/27608866/) — Evidence: "Results section is used to inform readers about the actual observations made in the research study."
  - [Snyder N, Foltz C, Lendner M, Vaccaro AR. How to Write an Effective Results Section. Clin Spine Surg. 2019;32(7):295-6](https://pubmed.ncbi.nlm.nih.gov/31145152/) — Evidence: findings are reported objectively, "even without interpreting the data."
  - [Hess DR. How to write an effective discussion. Respir Care. 2004;49(10):1238-41](https://pubmed.ncbi.nlm.nih.gov/15447810/) — Evidence: "Explaining the meaning of the results to the reader is the purpose of the discussion section of a research paper."
  - [Schulz KF, Altman DG, Moher D. CONSORT 2010 Statement. BMJ. 2010;340:c332](https://doi.org/10.1136/bmj.c332) — Evidence: every Results-domain checklist item is this-trial data (participant flow, recruitment, outcomes and estimation, harms), while Generalisability (item 21) and Interpretation (item 22) sit under Discussion — even generalization across contexts is not a Results content.
  - [Appelbaum M, Cooper H, Kline RB, Mayo-Wilson E, Nezu AM, Rao SM. Journal article reporting standards for quantitative research (JARS-Quant). Am Psychol. 2018;73(1):3-25](https://pubmed.ncbi.nlm.nih.gov/29345484/) — Evidence: hypotheses (anticipated results) and analyses (observed results) are separate reporting groupings (primary, secondary, exploratory).
- Propagates to:
  - documentation.md: Done - own Results section removed; `Results routing` added as a cross-cutting convention, following the URI precedent for concerns that span facets.
  - documentation-explanation.practice.md: Done - template and step 4 updated.
  - README.md, .agents/skills/memar/SKILL.md: Done - stale structure lines corrected (trivial; no paired changelogs).
  - 45 base documents, Results section removed same-session under the owner's directive, applied through sub-agents; per the owner's ruling a removal this mechanical carries no per-document changelog entry - this consolidated list is the record. Top-level (17): documentation-handoff.md, documentation-changelog.md, documentation-research.md, documentation-practice.md, framework.md, knowledge.md, process.md, protocol.md, software.md, system.md, thinking.md, terminology.md, modularity.md, modeling.md, type.md, content.md, agency.md. Protocols (15): lexer.md, giti.md, chapar.md, sdk.md, concurrency.md, dependency-management.md, networking.md, networking-connection.md, os.md, time.md, abstraction-implements.md, error.md, memory.md, filesystem.md, immutable_infrastructure.md. Khayyam (13, under docs/khayyam/): abstraction.md, agency.md, compiler.md, encapsulation.md, inheritance.md, khayyam.md, linter.md, metaprogramming.md, method.md, modularity.md, polymorphism.md, runtime.md, variable.md.
  - Four carried non-placeholder content and were routed, not deleted: agency.md (watch-items to the handoff's Open Questions), filesystem.md (external literature evidence inline at the claims it supports), immutable_infrastructure.md (deferral note to the handoff's Anticipated Work), error.md (validation note inline at the Boundary translation claim). The paired handoffs and filesystem.md's inline evidence carry their own provenance lines; the 26 per-document changelog entries first appended for this pass were removed on the same ruling.
  - protocols/control-flow.md: Done through the concurrent session's own commit (be9c260), which dropped its Results placeholder under this decision; docs/khayyam/control_flow.md was retired and deleted outright with that session, needing no migration. content.md's earlier blocker (its changelog being off-limits) dissolved with the no-entry ruling.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - argued, directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.3) - researched, argued, wrote

#### What changed
- The fixed body skeleton is reduced to `Abstract`, `Introduction`, `Explanation` (Omid Hekayati - directed removal after the results-notion round; Super Z - applied).
- Relevance discipline gains an `Observed results` bullet pointing to the cross-cutting routing map (Super Z - written; Omid Hekayati - placement decided: the map lives in documentation.md, not here, because its homes span four facets).
- documentation.md gains `Results routing`: an agent holding a result looks up its home at the meta layer by type - anticipated to the Abstract claim, derived to `Implications`, observed to the changelog entry, inline Evidence, a Research record, or handoff working state - without needing to know which facet's structure applies first (Omid Hekayati - argued the placement and the lookup path; Super Z - written).
- The empirical record of this specification's own Results rule was audited before removal: all ~50 `## Results` sections in the repository were unpopulated placeholders in three drifted boilerplate variants, several files carried the heading with nothing under it, and the section had repeatedly attracted misrouted content - external literature evidence (filesystem.md), a deferred-analysis list (immutable_infrastructure.md, since repaired), watch-items belonging to the handoff (agency.md), and a claim-validation note belonging inline (error.md) (Super Z - survey).
- The same-session migration was directed by the owner, superseding the 2026-09-06 rejection of a dedicated migration pass; applied through sub-agents with per-document changelog entries, excluding documents under concurrent edit (Omid Hekayati - directed).

#### Deliberation
- The same round's three-notion decomposition (anticipated / derived / observed) showed each notion already has a named home, making the fixed section redundant rather than load-bearing (Super Z - analysis; Omid Hekayati - drew the removal conclusion from it).
- Keeping the section was defended and failed on three tests: Relevance discipline already excludes observations from the body (they change confidence in claims, not the claims, definitions, arguments, or open questions themselves); no document ever populated it while it attracted misrouted content; and the scientific-skeleton analogy was misapplied - a paper reports a completed study, so its Results always exist, while a living specification's use is concurrent and unbounded, so its Results could only ever be meta-commentary about the document itself, whose readers (audit, inquiry) already have facets (Super Z - critique pass; Omid Hekayati - accepted).
- The sufficiency of the resulting three-section skeleton is recorded as an open question in the paired handoff rather than claimed settled (Omid Hekayati - raised; Super Z - recorded).

#### Considered and not done
- **Keep the section with a disambiguating definition naming the three notions (rejected)**: the correct analysis applied to the wrong remedy - it preserved a section the discipline already excludes and practice never used.
- **Demote Results to an Optional Sections entry, present only when populated (rejected)**: the content type remains excluded by Relevance discipline; claim-supporting observations already route inline as Evidence; and presence-as-maturity-signal would track use-maturity, which the Status rules deliberately refuse to do.
- **Rename the section to Observed results (rejected)**: the same content under a truer name fixes neither the hollowness nor the misrouting.
- **A separate Research-facet record for the literature evidence (rejected for now)**: this entry carries the full quote set at equal durability; a record can be promoted later if re-examination demand appears.
- **Progressive-only migration (superseded)**: the owner directed same-session migration of all documents in this session.

#### Related work
- ICMJE: "Present your results in logical sequence in the text, tables, and figures, giving the main or most important findings first"; Discussion is where findings are put "in the context of the totality of the relevant evidence", and conclusions must not go beyond what the data support.
- Bavdekar & Chandak 2015: the Results section informs readers of "the actual observations made in the research study", objective and complete.
- Snyder et al. 2019: a case is built "even without interpreting the data" - reporting and interpreting are separable acts.
- Hess 2004: meaning-explanation of results is the Discussion's purpose, by definition.
- CONSORT 2010: Results items are exclusively this-trial data; generalizability and interpretation are Discussion items - the scope-attribution boundary this routing adopts (a document reports what its own project's use produced; cross-system effect claims are inquiry material).
- Appelbaum et al. 2018 (JARS-Quant): anticipated results (hypotheses) and observed results (analyses) are distinct reporting groupings.
- Genre correction underlying the removal: a paper's Results reports the study's subject matter; a specification's "Results" would report the specification's own fortunes - meta-evidence, whose homes are the audit and inquiry facets, not the body.
- Kotz & Cals 2013 (J Clin Epidemiol. 66(9):945) and Foote 2009 (Chest. 135(3):866-8) were retrieved but yielded no verifiable quotable text (no accessible abstract or full text); they are excluded rather than paraphrased from memory.

#### Decision
The skeleton is three fixed sections; an Explanation-facet document carries no `Results` section; a result's home is determined by its type per documentation.md → Results routing; existing Results sections migrated same-session where their files were not under concurrent edit - routed, not deleted, wherever they carried content; the excluded documents (content.md, the docs/khayyam/ subtree, modeling, type, abstraction-implements, control-flow, error, memory) migrate progressively. (Omid Hekayati - approved)
