# Knowledge Changelog

## Changelog

### Initial draft (software-focused)
- Time: 2026-07-21T09:39:49Z
- Type: Added
- Cited:
  - [Reevaluating the Filesystem as a Fundamental Modeling Primitive](./protocols/filesystem.md) — Depends_on: this specification builds upon the filesystem critique to establish positive principles for knowledge modeling.
  - [The Knowledge-Creating Company](https://hbr.org/1991/07/the-knowledge-creating-company) — Reference: Nonaka & Takeuchi's foundational work on organizational knowledge creation (SECI), the process view of knowledge this framework adopts.
  - [Semantic File Systems](https://dl.acm.org/doi/10.1145/121132.121138) — Reference: Gifford et al.'s demonstration that attribute-based access outperforms hierarchical access for information-rich content.
  - [Unikernels: Library Operating Systems for the Cloud](https://anil.recoil.org/papers/2013-asplos-mirage.pdf) — Reference: evidence that general-purpose filesystems are not universal requirements, supporting filesystem-as-optional-capability.
  - [Usage and usefulness of technical software documentation](https://www.sciencedirect.com/science/article/abs/pii/S095058491400192X) — Reference: documentation value depends on discoverability, relevance, and accessibility — all knowledge-management concerns.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: initiated the architectural critique of File/Directory and Git's Snapshot/Commit model; directed the research toward separating storage engines from content models; advocated treating Repository as emergent projection rather than fundamental concept; emphasized that GUI must not determine the domain model; identified that organizations produce data but fail to produce retrievable knowledge; directed the insight that Comment = Content + Relation, not an independent entity.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — argued, analyzed: analyzed Git as a repair mechanism over filesystem flaws; developed the Task-centric knowledge evolution model; proposed Decision as outcome of Task, not root concept; identified Commit Message as compensation for the missing Task entity.
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, argued: reviewed chat history against resulting documents; softened the Path-Based Discovery claim to acknowledge path as a valid projection; added nuance to the Directory-to-Branch causal claim; introduced the Knowledge vs Document/Representation distinction; analyzed GUI Projection vs Domain Model separation.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — rewrote, researched: restructured the architectural critiques into principle-based format; developed the Content Addressability and Explicit Relations principles; synthesized multi-chat insights into the unified framework.

#### Summary
First draft of the specification, synthesized from extensive multi-party architectural discussions spanning the filesystem critique, Git analysis, content-modeling explorations, and knowledge-management theory in the software-development context. Intentionally principle-focused rather than implementation-focused, establishing the philosophical foundations for Geniuses Group's approach to knowledge in software development.

---

### Generalized to a cross-domain framework
- Time: 2026-07-21T12:43:59Z
- Type: Changed
- Cited:
  - [Key success factors of knowledge management systems for optimizing organizational performance](https://www.sciencedirect.com/science/article/pii/S2405844025024983) — Reference: critical success factors for KMS adoption and effectiveness.
  - [Organizational Knowledge and Knowledge Management - A New Framework](https://www.researchgate.net/publication/384774643_Organizational_Knowledge_and_Knowledge_Management_-_A_New_Framework) — Reference: knowledge-flow framework relevant to knowledge evolution and traceability.
  - [Managing Knowledge in Organizations: A Nonaka's SECI Model Operationalization](https://pmc.ncbi.nlm.nih.gov/articles/PMC6914727) — Reference: measurable dimensions for KM assessment.
  - [Knowledge Management in Health Organizations: A Systematic Literature Review](https://link.springer.com/article/10.1007/s13132-025-02760-3) — Reference: cross-domain applicability of KM principles in healthcare.
  - [Knowledge management and higher education institute: Review](https://www.sciencedirect.com/science/article/pii/S2199853124001434) — Reference: individual, national, and team factors in knowledge-sharing practices.
  - [14 Steps Toward Lean Knowledge Management](https://www.researchgate.net/publication/357482969_14_Steps_Toward_Lean_Knowledge_Management) — Reference: lean learning principles for efficient knowledge management.
  - [Knowledge Management in Small and Medium Enterprises: A Systematic Literature Review](https://www.emerald.com/jkm/article/28/2/590/1238330/Knowledge-management-in-small-and-medium) — Reference: scale-dependent KM barriers in SMEs.
  - [The Implementation of Knowledge Management in Health and Social Care Organisations](https://pmc.ncbi.nlm.nih.gov/articles/PMC12460784) — Reference: practical KM implementation assessment.
  - [Tacit Knowledge Sharing in Educational Organizations](https://toknowpress.net/ISBN/978-961-6914-28-4/4.pdf) — Reference: tacit knowledge assessment and transfer challenges.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, decided: requested generalization of the KM principles beyond the software-development domain.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote: conducted deep research into SECI, semantic filesystems, and KMS success factors; extended the framework to cross-domain applicability with healthcare, education, manufacturing, legal, and SME evidence.

#### Summary
Expanded from a software-focused specification to a cross-domain framework, on the recognition that the underlying principles are domain-independent and on the owner's request to generalize beyond software. Added cross-domain application patterns, multi-domain examples for each principle, and domain-specific research citations; preserved the software-specific content in a dedicated section. The claim that "knowledge management failure is the root cause of most organizational dysfunction" was adopted as the framing for this revision.

---

### Renamed to Knowledge, re-scoped to the concept, migrated to the Explanation-facet structure
- Time: 2026-09-05T11:30:00Z
- Type: Changed
- Cited:
  - [System](./system.md) — Depends_for: the foundational one-line definition of Knowledge lives there; this document is now the detailed treatment it defers to, following the precedent of Protocol.
  - [Thinking](./thinking.md) — Reference: thinking is the activity whose material knowledge is; the 4E section of that document already depends on this one.
  - [Agency](./agency.md) — Reference: agency acts on models built from knowledge; its Knowledge Management topics now link here.
  - [Framework](./framework.md) — Reference: the knowledge→thinking→intelligence→agency→goals chain this document's Concept Web topic links to is owned by Framework's Purpose Space topic.
  - [Content](./content.md) — Reference: the Content/Relation domain model that the knowledge-side integration must be worked out against.
- Propagates to:
  - `docs/system.md`: Done — Knowledge and Science now defers the detailed treatment to this document.
  - `docs/thinking.md`: Done — the 4E link retargeted to `./knowledge.md`.
  - `docs/agency.md`: Done — Knowledge Management mentions hyperlinked to this document; the glossary's Knowledge entry defers to it.
  - `docs/protocols/filesystem.md`: Done — stale citation title and URI fixed (the URI had broken in the protocols/ relocation); the "Principle 5" reference made name-based so renumbering cannot break it; and the document itself migrated to the Explanation-facet structure with a paired changelog in the same pass.
  - `docs/framework.md`: Done — new *Memar's Purpose Space: From Knowledge to Agency* topic states the chain and Memar's goal definition.
  - `README.md`: Done — Goals section now states the purpose chain and links to Framework.
  - Organization project (`GeniusesGroup/organization`): Done — seed document `docs/knowledge-management.md` created carrying the extracted KM-discipline content, with session context transferred to its `____Chats/`. Pending — the dedicated design session there that turns the seed into a real document.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: directed the rename (a document cannot manage knowledge without first defining it, and the KM discipline belongs to the Organization project); directed linking knowledge to thinking and agency so the concepts do not stand apart; stated the purpose chain (knowledge and thinking serve intelligence; intelligence serves agency toward goals such as quality of life) and adopted the goal definition of Memar; ruled that Memar may be stated as "a system that…" because every framework is also observable through the system lens; decided the extraction boundary (short cross-domain illustrations stay, the KM discipline moves); ruled that no standalone intelligence document is needed since intelligence is an output relation of the other concepts; directed merging the reserved practice placeholders into one companion.
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote: performed the rename (as a dedicated git commit to preserve history), the re-scope, the format migration, and the cross-document propagation.

#### Summary
Renamed `knowledge-management.md` to `knowledge.md` (pure `git mv` commit `2dc8576`, history preserved) and re-scoped the document from the KM discipline to the concept: the Abstract's central claim was re-grounded from an unfalsifiable organizational claim ("KM failure is the root cause of most organizational dysfunction") to a modeling claim (systems that conflate knowledge with its representations lose knowledge while keeping its artifacts). The sector-by-sector application guides, SECI operationalization, KMS success factors, and SME adoption guidance were extracted to the Organization project; compact cross-domain illustrations remain as evidence for the domain-independence claim. Structure migrated to the current Explanation facet: front matter reduced to Title/Status/Start Date/ID (the dead `Applied to` field removed); the 15 `Citations` and 4 `Contributors` entries absorbed into the two entries above; the top-level `## Future Possibilities` and `## Change Rationale` sections eliminated (nested under Discussion / moved here); the H1's "A Cross-Domain Framework" wording dropped, since *Framework* is a defined Memar concept and the old usage conflicted with it. New *Definition* and *Knowledge in Memar's Concept Web* topics establish this document as the detailed home of the concept (deferring to System's foundational definition) and state the knowledge→thinking→intelligence→agency→goals chain with its scope boundary. The duplicated Git content-addressability and commit-message passages (previously stated in both the principles and the software section) were consolidated, and the software-specific section was folded into a compact *Knowledge and Code* topic.

#### Rationale and alternatives
- **Keep the name Knowledge Management (rejected)**: it names an organizational discipline, not a concept — management rules cannot be stated before knowledge itself is defined, and most of the discipline belongs to the Organization project. The rename follows the precedent of [Agency](./agency.md), which was named after the property rather than the position/artifact once the property was recognized as more fundamental. The old H1's "A Cross-Domain Framework" additionally misused *Framework*, which Memar defines precisely ([Framework](./framework.md)).
- **Create a new document with a new ID (rejected)**: the title change alters the concept, which normally means a new document — but this document never left Draft, nothing depends on its identity, and re-scoping a Draft in place with the rename recorded here preserves the chain of reasoning without orphaning a never-settled number.
- **Delete all cross-domain content with the rename (rejected)**: the principles' domain-independence claim needs at least compact evidence; only the application discipline moved, not every non-software example.
- **Create `intelligence.md` as the home of the purpose chain (rejected)**: intelligence is an output relation of knowledge, thinking, and agency — a dedicated document could only restate its constituents. It is defined inline where the chain is stated ([Framework → Memar's Purpose Space](./framework.md#memars-purpose-space-from-knowledge-to-agency)), following the precedent of *Science* in [System](./system.md#knowledge-and-science), which is defined inline without its own document.
