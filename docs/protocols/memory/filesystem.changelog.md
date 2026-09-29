# Reevaluating the Filesystem as a Fundamental Modeling Primitive Changelog

## Changelog

### Initial draft
- Time: 2026-07-19T20:26:35Z
- Type: Added
- Cited:
  - [Documentation](../documentation.md) — Reference: this specification is informed by the Documentation framework's analysis of document types as profiles rather than independent structures.
  - [Knowledge](../knowledge.md) — Depends_on: this critique and that specification are companion documents with opposite polarity (critique vs. principles); the positive knowledge-modeling principles this critique enables are stated there.
  - [Semantic File Systems](https://dl.acm.org/doi/10.1145/121132.121138) — Reference: Gifford et al.'s demonstration that attribute-based (semantic) access outperforms hierarchical (directory-tree) access for information-rich content; primary academic support for the classification critique.
  - [Unikernels: Library Operating Systems for the Cloud](https://anil.recoil.org/papers/2013-asplos-mirage.pdf) — Reference: Madhavapeddy et al.'s evidence that general-purpose filesystems are not universal requirements, supporting the filesystem-is-optional argument.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — reviewed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote

#### What changed
- The first draft established the core critique that the filesystem is a storage model improperly used as a knowledge model (Omid Hekayati — the critique).
- The draft was synthesized from architectural review chat logs and deep academic research: deep research into graph theory and OS architecture was conducted, and the academic and architectural critiques were synthesized into the document format (Super Z).

#### Deliberation
- The architectural critique of File/Directory and Git's Snapshot/Commit model was initiated (Omid Hekayati).
- The research was directed to separate storage engines from content models (Omid Hekayati).
- Including the Unikernel arguments against mandatory filesystem layers was proposed (Omid Hekayati).
- A critical review was provided, analyzing Git as a patch layer over filesystem flaws (ChatGPT).

---

### Git reframed as repair mechanism; critique extended to File
- Time: 2026-07-20T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — argued, rewrote

#### What changed
- Addressed architectural critiques by reframing Git as a "repair mechanism" over filesystem flaws rather than an independent tool.
- Introduced the "Storage Leakage" and "Historical Accident" concepts.
- Expanded the critique to equally target the "File" abstraction as an artificial knowledge boundary.
- Toned down Unikernel claims to avoid overstating.
- Reopened Unresolved Questions to genuinely reflect the Draft status of this exploration, restructuring them to remain genuinely open (Super Z).
- The architectural critiques were synthesized into the revised document (Super Z).

#### Deliberation
- The "Git as Repair Mechanism" and "Historical Accident" frameworks were proposed (Omid Hekayati).
- The "Git as a Patch Layer" analysis was developed (Super Z).
- The critique was directed to equally target the File abstraction, not just Directory (Omid Hekayati).
- Reopening unresolved questions was advocated (Omid Hekayati).

---

### Reviewer critiques reconciled into the text
- Time: 2026-07-21T00:00:00Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, argued
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided

#### What changed
- The document text was reconciled against reviewer critiques that had been raised in discussion but not yet applied; the unincorporated critiques were identified by reviewing the full chat history against the resulting document (Claude).
- The Path-Based Discovery claim was softened to acknowledge path as one valid projection among many rather than a universally invalid model (Claude).
- Nuance was added to the Directory-to-Branch causal claim regarding concurrent development: it no longer overstates Branch's origin as solely a directory-escape mechanism (Claude).
- The File section now carries an explicit Knowledge vs. Document/Representation distinction (Claude).
- An Unresolved Question was added on whether Repository is itself a fundamental domain concept or an emergent, filesystem-era projection (Claude).
- A title/abstract contradiction was identified (Omid Hekayati).

---

### Citations deepened; external evidence added; UI-projection refinement
- Time: 2026-07-21T07:55:29Z
- Type: Changed
- Cited:
  - [Crash Consistency: Rethinking the Fundamental Abstractions of File Systems](https://spawn-queue.acm.org/doi/10.1145/2800695.2801719) — Reference: abstract persistence models for filesystem crash behavior, demonstrating ongoing academic re-examination of filesystem fundamentals.
  - [The operating system: should there be one?](https://www.humprog.org/~stephen/research/papers/kell13operating.pdf) — Reference: how the "file" abstraction evolved through Unix and Plan 9, supporting the historical-accident analysis.
  - POSIX Abstractions in Modern Operating Systems (Yang et al., 2016) — Reference: many modern applications use POSIX in compatibility layers rather than natively, suggesting filesystem APIs persist by convention rather than necessity. (Named in the document's Prior art without a URI; none is recorded here rather than guessed.)
  - A Tale of Two Abstractions: The Case for Object Storage (Bittman et al., HotStorage '19) — Reference: file and object abstractions coexist because they optimize for different use cases — filesystem is one valid projection among many. (Named in the document's Prior art without a URI; none is recorded here rather than guessed.)
  - [The Knowledge-Creating Company](https://hbr.org/1991/07/the-knowledge-creating-company) — Reference: the SECI model's tacit/explicit distinction informs the Knowledge vs. Document position.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed

#### What changed
- Fourth revision round: citations deepened with corrected URIs and additional new academic sources.
- Drawbacks made specific about cognitive transition costs and the critique's scope (knowledge systems, not all systems), adding cognitive-transition specificity and domain-appropriate applicability.
- Prior art given explicit per-source lineage to specific sections.
- Results populated with external validation evidence (semantic-filesystem performance studies, unikernel production adoption, knowledge-graph scale).
- The cognitive-transition Unresolved question added.
- The "File/Directory as UI Projection, Not Domain Model" topic added.
- Attribution note: the Change Rationale this entry was migrated from names the POSIX, Object Storage, Zettelkasten, and SECI sources as this round's additions; the Crash Consistency and Kell citations were also present in the old front matter but their round is not recorded — they are placed here (the citation-expansion round) as the best inference, not as verified fact.

#### Deliberation
- That File/Directory have always been primarily UI/projection, not domain model, was emphasized (Omid Hekayati).

---

### Migrated to the Explanation-facet structure; stale links fixed
- Time: 2026-09-05T12:30:00Z
- Type: Changed
- Propagates to:
  - knowledge.md: Done — the `Pending` propagation recorded in knowledge.changelog.md (this document's own format migration) is closed by this entry.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- Front matter reduced to Title/Status/Start Date/ID: the six `Citations`, the four-entry `Contributors` roster, and the dead `Applied to` field were absorbed into the entries above, and the top-level `## Change Rationale` section moved here as its four entries (its four numbered rounds became the four entries above, dated approximately by inferred round and commit history — the open question `documentation-changelog.md` names for migrated historical entries; the initial draft's time is the real commit time).
- A one-line summary was added under the H1.
- Two plain-text internal section references in Prior art became hyperlinks.
- The front-matter citation of the knowledge document was corrected to `../knowledge.md` (its URI had broken in the protocols/ relocation and still named the pre-rename title), and the body's "Principle 5" reference was made name-based ("the UI Projection ≠ Domain Model principle") so principle renumbering in the knowledge document cannot break it.
- No argument content changed.

#### Deliberation
- That every old-style document touched going forward be migrated to the current structure, with a paired changelog file, one document at a time, was requested — a standing request, first recorded in system.changelog.md (Omid Hekayati).

---

### Stance topic added recording why this document lives in protocols/; companion practice created
- Time: 2026-09-05T13:40:00Z
- Type: Added
- Cited:
  - [Framework](../framework.md) — Reference: the explicit-decision-over-defaults standard the practice's Recording section applies.
- Propagates to:
  - `protocols/README.md`: Done — the membership criterion now names the second kind of document this one is (Memar's position on an external protocol surface), so the placement question does not recur at the folder level either.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Qwen](../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — drafted, rewrote

#### What changed
- Added the first Explanation topic, "Memar's Stance on the Filesystem Protocol Surface": the document's protocols/ membership (a position on an external protocol surface, not a general concept) and its practical function — the filesystem as a high-level library whose inclusion is a per-concern decision, with the critique topics as the evidence for the check.
- The Abstract gained one sentence pointing at that check.
- Created `filesystem.practice.md` as the companion need-check: six criteria, each linked to the critique topic that argues it, plus when-to-run triggers, a recorded-decision requirement, and anti-patterns.
- Per the changelog scope rule, the practice companion shares this ledger and receives no changelog of its own.

#### Deliberation
- The rationale for this document's placement in `protocols/` was supplied: the filesystem is a protocol surface owned outside Memar that Memar's stack will likely implement itself (e.g. in memar-khayyam), so the document states why Memar does not adopt the prevailing OS view and treats the filesystem as a high-level library chosen by decision; its function is a warning to the builder to set aside the old default and actually check the need (Omid Hekayati).
- Writing that rationale into the document itself, so the placement question does not recur, was directed (Omid Hekayati).
- Creating a companion practice replacing the strong default with explicit criteria drawn from the arguments already in the text was directed (Omid Hekayati).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - filesystem.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only: the document-level `## Discussion` — with its `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Possible questions`, `Unresolved questions`, and `Future possibilities` subsections — is retired; no `Discussion`, `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, or `Future possibilities` heading survives in the body. This document carried no topic-level Discussion wrappers, so none needed dissolving.
- One premise fold: the retired `Possible questions` answer on what becomes harder and easier if the filesystem is removed entirely (CLI navigation and legacy tool integration harder; multiple classification, semantic querying, decision traceability, and a single source of truth easier) is now carried inline in the "Memar's Stance on the Filesystem Protocol Surface" topic, at the check-the-need claim it supports; the section's other answered questions needed no fold (verified graduated below).
- The five `Unresolved questions` plus the Repository question carried in `Possible questions` — the one item there never marked addressed — moved to the paired handoff's Open Questions; the `Future possibilities` program (alternative primitives for Content and Task modeling, the versioning-redefinition document, and the four named topics) moved there as Anticipated Work.
- The retired section's rejected alternatives and weighed drawbacks — the three claims of `Rationale and alternatives`, the resolved `Possible questions` record rejecting graph-based emulation of filesystem concepts in favor of clean redesign, and the four `Drawbacks` items — are preserved below under Considered and not done.
- The six-source `Prior art` survey is preserved below under Related work, its two links into the base document repointed to file-relative form.
- Verified graduated, not copied: the `Drawbacks` closing scope paragraph (the critique applies most strongly to knowledge systems, targets leakage not legitimate use, naming compilation, artifact caching, configuration delivery, and log storage) is already carried by the Stance topic's "for compilation, artifact caching, configuration delivery, and log storage, a filesystem may well be the right answer... What is not acceptable is choosing it by default, without the check" and the Abstract's knowledge-systems scoping; `Possible questions` items 1–3 (file as projection, model around relationships, repository state as artifact) are already carried by the "File: An Artificial Knowledge Boundary", "Storage Leakage", "Git as a Filesystem Repair Mechanism", and "The Repository State (Snapshot) Fallacy" topics — item 3's forward half (task-tied logical snapshots replacing physical ones) is preserved in the handoff's Task-Centric Versioning item; and `Rationale and alternatives` item 2's refined position (Git as a repair layer, not an independent innovation) is already carried by the Git topic and the Methodology — dropping these from the body loses nothing.
- No hyperlink in the body pointed at a retired section's anchor, so no link repointing was needed inside the document; the Introduction's Methodology note that unresolved questions are kept genuinely open still holds, with the questions now living in the paired handoff. The companion practice file's two links into the retired `#drawbacks` and `#future-possibilities` anchors were not edited here (Practice companions are outside a base-document migration's reach) and are reported for its own follow-up.
- Final audit pass: the Methodology note now says the unresolved questions stay open in the paired handoff; `filesystem.practice.md`'s two links into retired body anchors (Drawbacks, Future possibilities - Projection Layer Architecture) were retargeted to this changelog and the handoff's Anticipated Work.

#### Considered and not done
- **"Filesystem is bad, we must replace it" (rejected; migrated from the removed document-level `Rationale and alternatives`)**: the document does not argue the filesystem was a mistake — it was highly effective for storage-oriented systems; the claim is narrowly scoped: the filesystem is an inherited assumption for *knowledge systems*, not a fundamental requirement.
- **"Git is an independent knowledge tool" (refined; migrated from the removed document-level `Rationale and alternatives`)**: Git is a filesystem repair mechanism; its flaws in knowledge management are inherited directly from the file/directory paradigm.
- **"We should build a Graph Database" (rejected as direct implication; migrated from the removed document-level `Rationale and alternatives`)**: a graph database provides storage mechanics, not a knowledge model; without principled design of what nodes and edges MEAN, a graph database becomes another data swamp — this time with cycles. The principles in the document describe conceptual structure; implementation technology choice is separate.
- **Filesystem emulation over a graph (rejected; migrated from the removed `Possible questions`)**: every filesystem concept can be represented as graph structures mathematically (e.g., a directory = edge with `contains` label), but merely emulating filesystem concepts in a graph carries over historical baggage — a clean architectural redesign is preferred over emulation.

#### Considered and not done (from the removed document-level Drawbacks section)
- The filesystem is one of the most successful and deeply entrenched abstractions in computer science history; deviating from it requires rethinking developer tooling, deployment pipelines, and human interaction paradigms that have been optimized over five decades.
- **Interoperability friction**: most third-party tools expect POSIX-compliant, file-based I/O — build systems, linters, deployment tools, and IDEs all assume files exist at paths.
- **Cognitive transition cost**: developers have internalized file-centric mental models ("open file," "save file," "move file"); migration requires unlearning as much as learning.
- **Risk of replacement failure**: if the replacement system has gaps (and any system will), the migration may leave the organization worse than before — with broken tooling and incomplete knowledge management.
- **Performance maturity**: filesystems are heavily optimized after decades of engineering effort; new abstractions rarely match this level of performance out of the gate.

#### Related work
- **Semantic File Systems (Gifford, Jouvelot, Sheldon, & O'Toole, 1991)**: landmark ACM research introducing attribute-based file access. Demonstrated that automatic extraction and indexing of file properties enables queries impossible with hierarchical directories. Directly inspired the [Directory as Tree: A Flawed Classification Model](./filesystem.md#directory-as-tree-a-flawed-classification-model) topic of the base document. (Migrated from the removed document-level `Prior art`.)
- **Unikernels (Madhavapeddy, Williams, & Spork, 2013)**: ASPLOS paper presenting MirageOS and the library OS approach. Showed that compiling applications into specialized OS images eliminates the need for general-purpose filesystems. Validated by subsequent production deployments in cloud environments. (Migrated from the removed document-level `Prior art`.)
- **POSIX Abstractions in Modern Operating Systems (Yang et al., 2016)**: ACM study examining POSIX usage patterns in Android, OS X, and Ubuntu. Found that many modern applications use POSIX in compatibility layers rather than natively, suggesting filesystem APIs persist by convention rather than necessity. (Migrated from the removed document-level `Prior art`.)
- **A Tale of Two Abstractions: The Case for Object Storage (Bittman et al., HotStorage '19)**: USENIX research comparing file and object abstractions for persistent data. Found that both abstractions coexist because they optimize for different use cases — supporting the base document's position that filesystem is one valid projection among many. (Migrated from the removed document-level `Prior art`.)
- **Zettelkasten Method (Luhmann, sommergessen)**: personal knowledge management system using atomic notes with emergent structure through linking. Influences the [File: An Artificial Knowledge Boundary](./filesystem.md#file-an-artificial-knowledge-boundary) critique by demonstrating practical knowledge systems that don't use files or folders as primary organization. (Migrated from the removed document-level `Prior art`.)
- **Nonaka SECI Model (Nonaka & Takeuchi, 1995)**: while focused on organizational learning, the SECI model's distinction between tacit and explicit knowledge informs the base document's Knowledge vs. Document distinction. Explicit knowledge artifacts (documents) are always incomplete projections of the richer tacit knowledge context. (Migrated from the removed document-level `Prior art`.)
