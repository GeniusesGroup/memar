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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — argued, analyzed
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — rewrote, researched

#### What changed
- First draft of the specification, synthesized from extensive multi-party architectural discussions spanning the filesystem critique, Git analysis, content-modeling explorations, and knowledge-management theory in the software-development context. Intentionally principle-focused rather than implementation-focused, establishing the philosophical foundations for Geniuses Group's approach to knowledge in software development.
- The Task-centric knowledge evolution model was developed (ChatGPT).
- The Knowledge vs Document/Representation distinction was introduced (Claude).
- The architectural critiques were restructured into principle-based format; the Content Addressability and Explicit Relations principles were developed; the multi-chat insights were synthesized into the unified framework (Super Z).

#### Deliberation
- The architectural critique of File/Directory and Git's Snapshot/Commit model was initiated; the research was directed toward separating storage engines from content models; treating Repository as emergent projection rather than fundamental concept was advocated; that GUI must not determine the domain model was emphasized; that organizations produce data but fail to produce retrievable knowledge was identified; the insight that Comment = Content + Relation, not an independent entity was directed (Omid Hekayati).
- Git was analyzed as a repair mechanism over filesystem flaws; Decision was proposed as outcome of Task, not root concept; Commit Message was identified as compensation for the missing Task entity (ChatGPT).
- The chat history was reviewed against the resulting documents; the Path-Based Discovery claim was softened to acknowledge path as a valid projection; nuance was added to the Directory-to-Branch causal claim; the GUI Projection vs Domain Model separation was analyzed (Claude).

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote

#### What changed
- Expanded from a software-focused specification to a cross-domain framework, on the recognition that the underlying principles are domain-independent.
- Cross-domain application patterns, multi-domain examples for each principle, and domain-specific research citations were added; the software-specific content was preserved in a dedicated section.
- Deep research into SECI, semantic filesystems, and KMS success factors was conducted (Super Z).
- The framework was extended to cross-domain applicability with healthcare, education, manufacturing, legal, and SME evidence (Super Z).
- The claim that "knowledge management failure is the root cause of most organizational dysfunction" was adopted as the framing for this revision.

#### Deliberation
- Generalization of the KM principles beyond the software-development domain was requested (Omid Hekayati).

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- `knowledge-management.md` was renamed to `knowledge.md` (pure `git mv` commit `2dc8576`, history preserved) and the document was re-scoped from the KM discipline to the concept: the Abstract's central claim was re-grounded from an unfalsifiable organizational claim ("KM failure is the root cause of most organizational dysfunction") to a modeling claim (systems that conflate knowledge with its representations lose knowledge while keeping its artifacts) (Qwen — performed).
- The sector-by-sector application guides, SECI operationalization, KMS success factors, and SME adoption guidance were extracted to the Organization project; compact cross-domain illustrations remain as evidence for the domain-independence claim.
- Structure migrated to the current Explanation facet: front matter reduced to Title/Status/Start Date/ID (the dead `Applied to` field removed); the 15 `Citations` and 4 `Contributors` entries absorbed into the two entries above; the top-level `## Future Possibilities` and `## Change Rationale` sections eliminated (nested under Discussion / moved here); the H1's "A Cross-Domain Framework" wording dropped, since *Framework* is a defined Memar concept and the old usage conflicted with it (Qwen — performed).
- The cross-document propagation was performed (Qwen).
- New *Definition* and *Knowledge in Memar's Concept Web* topics establish this document as the detailed home of the concept (deferring to System's foundational definition) and state the knowledge→thinking→intelligence→agency→goals chain with its scope boundary.
- The duplicated Git content-addressability and commit-message passages (previously stated in both the principles and the software section) were consolidated, and the software-specific section was folded into a compact *Knowledge and Code* topic.

#### Deliberation
- The rename was directed: a document cannot manage knowledge without first defining it, and the KM discipline belongs to the Organization project (Omid Hekayati).
- Linking knowledge to thinking and agency was directed, so the concepts do not stand apart (Omid Hekayati).
- The purpose chain was stated — knowledge and thinking serve intelligence; intelligence serves agency toward goals such as quality of life — and the goal definition of Memar was adopted (Omid Hekayati).
- It was ruled that Memar may be stated as "a system that…" because every framework is also observable through the system lens (Omid Hekayati).
- The extraction boundary was decided: short cross-domain illustrations stay, the KM discipline moves (Omid Hekayati).
- It was ruled that no standalone intelligence document is needed, since intelligence is an output relation of the other concepts (Omid Hekayati).
- Merging the reserved practice placeholders into one companion was directed (Omid Hekayati).

#### Considered and not done
- **Keep the name Knowledge Management (rejected)**: it names an organizational discipline, not a concept — management rules cannot be stated before knowledge itself is defined, and most of the discipline belongs to the Organization project. The rename follows the precedent of [Agency](./agency.md), which was named after the property rather than the position/artifact once the property was recognized as more fundamental. The old H1's "A Cross-Domain Framework" additionally misused *Framework*, which Memar defines precisely ([Framework](./framework.md)).
- **Create a new document with a new ID (rejected)**: the title change alters the concept, which normally means a new document — but this document never left Draft, nothing depends on its identity, and re-scoping a Draft in place with the rename recorded here preserves the chain of reasoning without orphaning a never-settled number.
- **Delete all cross-domain content with the rename (rejected)**: the principles' domain-independence claim needs at least compact evidence; only the application discipline moved, not every non-software example.
- **Create `intelligence.md` as the home of the purpose chain (rejected)**: intelligence is an output relation of knowledge, thinking, and agency — a dedicated document could only restate its constituents. It is defined inline where the chain is stated ([Framework → Memar's Purpose Space](./framework.md#memars-purpose-space-from-knowledge-to-agency)), following the precedent of *Science* in [System](./system.md#knowledge-and-science), which is defined inline without its own document.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - knowledge.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body now carries only the fixed top-level sections Abstract, Introduction, Explanation, Results; the document-level `## Discussion` section and its five subsections (`Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities`) are retired from it.
- The `#### Discussion` wrapper nested under `Definition` (a `Rationale and alternatives` block) was dissolved too, per the first wave's every-wrapper precedent; its two rejected alternatives are preserved below as considered-and-not-done records.
- The six unresolved questions and the six anticipated-work items moved to the newly created `knowledge.handoff.md` as `Open Questions` and `Anticipated Work`.
- The four rejected-alternative positions and the document-level drawbacks — infrastructure investment, behavioral change, tooling gap, over-engineering risk, and the analysis-paralysis counterweight — are preserved below as considered-and-not-done records.
- The eight-work comparative prior-art survey is preserved below as related work, with its principle-pointing links retargeted to the base document.
- No premise evidence required folding into the body: each principle stands on its own argument, and the literature position the classification discussion depends on — Gifford et al.'s attribute-based retrieval — is already cited inline at the Classification principle; the survey works already carry `Cited` provenance in this file's two drafting entries.
- Final audit pass: the Methodology line now records that open questions stay genuinely open in the paired handoff, and `knowledge.practice.md`'s record-questions instruction was retargeted from the retired `Unresolved questions` section to a document's paired handoff.

#### Considered and not done
- **"Just use Confluence/Notion/Wiki" (rejected; migrated from the retired document-level Rationale and alternatives)**: these tools improve over raw files but still inherit the document-as-knowledge fallacy; they add layers (search, linking, collaboration) on top of fundamentally document-centric storage — useful, but not addressing the root issue.
- **"Just use a Knowledge Graph database" (rejected as complete solution; migrated from the same)**: a graph database provides storage mechanics, not a knowledge model; without principled design of what the nodes and edges MEAN, a knowledge graph becomes another data swamp — this time with cycles.
- **"Keep current tools but be more disciplined" (partial acceptance; migrated from the same)**: commit-message conventions, structured clinical notes, and standardized syllabi mitigate symptoms but do not cure the disease; for organizations already invested in existing tooling, this is a reasonable transitional strategy while building toward principle-aligned systems.
- **"These principles only apply to large organizations" (rejected; migrated from the same)**: small teams suffer knowledge loss more acutely, because they lack institutional memory and redundant personnel; the principles scale down — a solo practitioner benefits from task-centric history and explicit relationships.
- **Define knowledge as a static asset (rejected; migrated from the `Rationale and alternatives` nested under `Definition`)**: the research literature on organizational knowledge creation (Nonaka & Takeuchi's SECI model) established knowledge as a dynamic, social process rather than a stock of artifacts. The modeling principles below follow that reading — knowledge exists in the living relationships between assertions, evidence, tasks, and participants, not in the files that freeze them. The organizational application of that process view is developed in the Organization project.
- **Leave "knowledge" undefined and regulate only storage behavior (rejected; migrated from the same nested block)**: management rules stated over an undefined central term import the reader's colloquial sense. Memar's terminology governance ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, here, and letting other documents reference that definition.

#### Considered and not done (from the removed document-level Drawbacks section)
- **The principles are demanding — infrastructure investment**: graph-based storage, content-addressable identifiers, and rich relationship modeling do not come free with traditional stacks. The investment does scale, however: small teams can start with stable identifiers and structured decision logging alone. (Migrated from the retired document-level Drawbacks)
- **Behavioral change**: professionals are deeply habituated to existing mental models ("where is the file?", "which folder does this go in?"); migration requires unlearning regardless of domain. (Migrated from the same)
- **Tooling gap**: most organizations lack principle-aligned knowledge systems; custom or niche tooling is often required. (Migrated from the same)
- **Risk of over-engineering**: it is possible to build an elaborate knowledge graph nobody uses because it is too complex for everyday tasks; the principles should be applied incrementally, not all-at-once. (Migrated from the same)
- **Analysis paralysis is the most dangerous adoption failure mode** — endless modeling without shipping. The counterweight principle adopted against it: **imperfect knowledge management now beats perfect knowledge management never**. (Migrated from the same)

#### Related work
- **Gifford et al., Semantic File Systems (1991)**: demonstrated that attribute-based (semantic) access outperforms hierarchical (directory-tree) access for information-rich content. Directly supports [Storage Model ≠ Content Model](./knowledge.md#storage-model--content-model), [Relationships Are First-Class Citizens](./knowledge.md#relationships-are-first-class-citizens), and [Classification Should Not Be Confined to a Single Hierarchy](./knowledge.md#classification-should-not-be-confined-to-a-single-hierarchy). (Migrated from the retired document-level Prior art)
- **Madhavapeddy et al., Unikernels (2013)**: showed that general-purpose filesystems are not universal requirements, supporting the argument that filesystem is an optional capability, not a knowledge primitive. (Migrated from the same)
- **Nonaka & Takeuchi, The Knowledge-Creating Company (1991)**: the SECI model established knowledge as a dynamic, social process rather than a static asset. The base document adopts the process view; the organizational machinery (socialization, externalization, combination, internalization) is developed in the Organization project. (Migrated from the same)
- **Nygard, Architecture Decision Records**: a pattern for capturing decisions with context — the software instantiation of [Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) and [Knowledge Requires Explicit Context Recovery](./knowledge.md#knowledge-requires-explicit-context-recovery). (Migrated from the same)
- **Diátaxis Framework (Rock)**: documentation structured by audience need (tutorials, how-to, reference, explanation). Complements the base document's framework by addressing document PURPOSE. (Migrated from the same)
- **Zettelkasten Method (Luhmann)**: personal knowledge management based on atomic notes, links, and emergent structure. Influences [The Smallest Knowledge Unit Is Smaller Than You Think](./knowledge.md#the-smallest-knowledge-unit-is-smaller-than-you-think) and [Relationships Are First-Class Citizens](./knowledge.md#relationships-are-first-class-citizens). (Migrated from the same)
- **Solid (Berners-Lee)**: web decentralization emphasizing personal data pods, content addressability, and granular permissions — a technical implementation of several of the base document's principles. (Migrated from the same)
- **Communities of Practice (Wenger-Trayner)**: how groups learn together through shared practice — evidence for the process view of knowledge and for [Communication Channels Produce Knowledge but Are Not Knowledge Repositories](./knowledge.md#communication-channels-produce-knowledge-but-are-not-knowledge-repositories). (Migrated from the same)
