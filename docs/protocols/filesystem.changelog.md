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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: initiated the architectural critique of File/Directory and Git's Snapshot/Commit model; directed the research to separate storage engines from content models; proposed including the Unikernel arguments against mandatory filesystem layers.
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — reviewed, argued: critical review; analyzed Git as a patch layer over filesystem flaws.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote: conducted deep research into graph theory and OS architecture; synthesized the academic and architectural critiques into the document format.

#### Summary
First draft, synthesized from architectural review chat logs and deep academic research. Established the core critique that the filesystem is a storage model improperly used as a knowledge model.

---

### Git reframed as repair mechanism; critique extended to File
- Time: 2026-07-20T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: proposed the "Git as Repair Mechanism" and "Historical Accident" frameworks; directed the critique to equally target the File abstraction, not just Directory; advocated reopening unresolved questions.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — argued, rewrote: developed the "Git as a Patch Layer" analysis; synthesized the architectural critiques into the revised document; restructured the Unresolved Questions to remain genuinely open.

#### Summary
Addressed architectural critiques by reframing Git as a "repair mechanism" over filesystem flaws rather than an independent tool. Introduced the "Storage Leakage" and "Historical Accident" concepts. Expanded the critique to equally target the "File" abstraction as an artificial knowledge boundary. Toned down Unikernel claims to avoid overstating. Reopened Unresolved Questions to genuinely reflect the Draft status of this exploration.

---

### Reviewer critiques reconciled into the text
- Time: 2026-07-21T00:00:00Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, argued: reviewed the full chat history against the resulting document to identify reviewer critiques raised but not yet incorporated; softened the Path-Based Discovery claim to acknowledge path as one valid projection rather than a universally invalid model; added nuance to the Directory-to-Branch causal claim regarding concurrent development; introduced the Knowledge vs. Document/Representation distinction into the File section; added an Unresolved Question on whether Repository is itself a fundamental domain concept.
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided: identified the title/abstract contradiction.

#### Summary
Reconciled the document text against reviewer critiques that had been raised in discussion but not yet applied: Path-Based Discovery now treats paths as one valid projection among many rather than a universally invalid model; the Directory-to-Branch causal claim no longer overstates Branch's origin as solely a directory-escape mechanism; the File section carries an explicit Knowledge vs. Document/Representation distinction; and the question of whether Repository is fundamental or an emergent, filesystem-era projection was added to the open questions.

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
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote: enhanced citations with corrected URIs and additional academic sources; expanded Drawbacks with cognitive-transition specificity and domain-appropriate applicability; enriched Prior art with per-source lineage to specific sections; added the Results section's external validation evidence; added the cognitive-transition Unresolved question.
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed: emphasized that File/Directory have always been primarily UI/projection, not domain model.

#### Summary
Fourth revision round: citations deepened with new academic sources, Drawbacks made specific about cognitive transition costs and the critique's scope (knowledge systems, not all systems), Prior art given explicit lineage, Results populated with external evidence (semantic-filesystem performance studies, unikernel production adoption, knowledge-graph scale), and the "File/Directory as UI Projection, Not Domain Model" topic added. Attribution note: the Change Rationale this entry was migrated from names the POSIX, Object Storage, Zettelkasten, and SECI sources as this round's additions; the Crash Consistency and Kell citations were also present in the old front matter but their round is not recorded — they are placed here (the citation-expansion round) as the best inference, not as verified fact.

---

### Migrated to the Explanation-facet structure; stale links fixed
- Time: 2026-09-05T12:30:00Z
- Type: Changed
- Propagates to:
  - knowledge.md: Done — the `Pending` propagation recorded in knowledge.changelog.md (this document's own format migration) is closed by this entry.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: asked that every old-style document touched going forward be migrated to the current structure, with a paired changelog file, one document at a time (standing request, first recorded in system.changelog.md).
  - [Qwen](../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote.

#### Summary
Front matter reduced to Title/Status/Start Date/ID: the six `Citations`, the four-entry `Contributors` roster, and the dead `Applied to` field were absorbed into the entries above, and the top-level `## Change Rationale` section moved here as its four entries (its four numbered rounds became the four entries above, dated approximately by inferred round and commit history — the open question `documentation-changelog.md` names for migrated historical entries; the initial draft's time is the real commit time). A one-line summary was added under the H1. Two plain-text internal section references in Prior art became hyperlinks. The front-matter citation of the knowledge document was corrected to `../knowledge.md` (its URI had broken in the protocols/ relocation and still named the pre-rename title), and the body's "Principle 5" reference was made name-based ("the UI Projection ≠ Domain Model principle") so principle renumbering in the knowledge document cannot break it. No argument content changed.

---

### Stance topic added recording why this document lives in protocols/; companion practice created
- Time: 2026-09-05T13:40:00Z
- Type: Added
- Cited:
  - [Framework](../framework.md) — Reference: the explicit-decision-over-defaults standard the practice's Recording section applies.
- Propagates to:
  - `protocols/README.md`: Done — the membership criterion now names the second kind of document this one is (Memar's position on an external protocol surface), so the placement question does not recur at the folder level either.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: supplied the rationale for this document's placement in `protocols/` — the filesystem is a protocol surface owned outside Memar that Memar's stack will likely implement itself (e.g. in memar-khayyam), so the document states why Memar does not adopt the prevailing OS view and treats the filesystem as a high-level library chosen by decision; its function is a warning to the builder to set aside the old default and actually check the need; directed that the rationale be written into the document itself so the question does not recur; directed creating a companion practice replacing the strong default with explicit criteria drawn from the arguments already in the text.
  - [Qwen](../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — drafted, rewrote.

#### Summary
Added the first Explanation topic, "Memar's Stance on the Filesystem Protocol Surface": the document's protocols/ membership (a position on an external protocol surface, not a general concept) and its practical function — the filesystem as a high-level library whose inclusion is a per-concern decision, with the critique topics as the evidence for the check. The Abstract gained one sentence pointing at that check. Created `filesystem.practice.md` as the companion need-check: six criteria, each linked to the critique topic that argues it, plus when-to-run triggers, a recorded-decision requirement, and anti-patterns. Per the changelog scope rule, the practice companion shares this ledger and receives no changelog of its own.
