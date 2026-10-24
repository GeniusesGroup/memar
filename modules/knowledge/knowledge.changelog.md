# Knowledge Changelog

## Changelog

### Initial draft (software-focused)
- Time: 2026-07-21T09:39:49Z
- Type: Added
- Cited:
  - Reevaluating the Filesystem as a Fundamental Modeling Primitive (`docs/modules/lib/memory/filesystem.md`) — Depends_on: this specification builds upon the filesystem critique to establish positive principles for knowledge modeling.
  - [The Knowledge-Creating Company](https://hbr.org/1991/07/the-knowledge-creating-company) — Reference: Nonaka & Takeuchi's foundational work on organizational knowledge creation (SECI), the process view of knowledge this framework adopts.
  - [Semantic File Systems](https://dl.acm.org/doi/10.1145/121132.121138) — Reference: Gifford et al.'s demonstration that attribute-based access outperforms hierarchical access for information-rich content.
  - [Unikernels: Library Operating Systems for the Cloud](https://anil.recoil.org/papers/2013-asplos-mirage.pdf) — Reference: evidence that general-purpose filesystems are not universal requirements, supporting filesystem-as-optional-capability.
  - [Usage and usefulness of technical software documentation](https://www.sciencedirect.com/science/article/abs/pii/S095058491400192X) — Reference: documentation value depends on discoverability, relevance, and accessibility — all knowledge-management concerns.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — argued, analyzed
  - [Claude](../../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — rewrote, researched

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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, deep think max) — researched, rewrote

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
  - [System](../../docs/system.md) — Depends_for: the foundational one-line definition of Knowledge lives there; this document is now the detailed treatment it defers to, following the precedent of Protocol.
  - [Thinking](../../docs/cognition.md) — Reference: thinking is the activity whose material knowledge is; the 4E section of that document already depends on this one.
  - [Agency](../../docs/agency.md) — Reference: agency acts on models built from knowledge; its Knowledge Management topics now link here.
  - [Framework](../../docs/framework.md) — Reference: the knowledge→thinking→intelligence→agency→goals chain this document's Concept Web topic links to is owned by Framework's Purpose Space topic.
  - [Content](content/content.md) — Reference: the Content/Relation domain model that the knowledge-side integration must be worked out against.
- Propagates to:
  - `docs/system.md`: Done — Knowledge and Science now defers the detailed treatment to this document.
  - `docs/thinking.md`: Done — the 4E link retargeted to `./knowledge.md`.
  - `docs/agency.md`: Done — Knowledge Management mentions hyperlinked to this document; the glossary's Knowledge entry defers to it.
  - `docs/protocols/memory/filesystem.md`: Done — stale citation title and URI fixed (the URI had broken in the protocols/ relocation); the "Principle 5" reference made name-based so renumbering cannot break it; and the document itself migrated to the Explanation-facet structure with a paired changelog in the same pass.
  - `docs/framework.md`: Done — new *Memar's Purpose Space: From Knowledge to Agency* topic states the chain and Memar's goal definition.
  - `README.md`: Done — Goals section now states the purpose chain and links to Framework.
  - Organization project (`GeniusesGroup/organization`): Done — seed document `docs/knowledge-management.md` created carrying the extracted KM-discipline content, with session context transferred to its `____Chats/`. Pending — the dedicated design chat there that turns the seed into a real document.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Qwen](../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

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
- **Keep the name Knowledge Management (rejected)**: it names an organizational discipline, not a concept — management rules cannot be stated before knowledge itself is defined, and most of the discipline belongs to the Organization project. The rename follows the precedent of [Agency](../../docs/agency.md), which was named after the property rather than the position/artifact once the property was recognized as more fundamental. The old H1's "A Cross-Domain Framework" additionally misused *Framework*, which Memar defines precisely ([Framework](../../docs/framework.md)).
- **Create a new document with a new ID (rejected)**: the title change alters the concept, which normally means a new document — but this document never left Draft, nothing depends on its identity, and re-scoping a Draft in place with the rename recorded here preserves the chain of reasoning without orphaning a never-settled number.
- **Delete all cross-domain content with the rename (rejected)**: the principles' domain-independence claim needs at least compact evidence; only the application discipline moved, not every non-software example.
- **Create `intelligence.md` as the home of the purpose chain (rejected)**: intelligence is an output relation of knowledge, thinking, and agency — a dedicated document could only restate its constituents. It is defined inline where the chain is stated ([Framework → Memar's Purpose Space](../../docs/framework.md#memars-purpose-space-from-knowledge-to-agency)), following the precedent of *Science* in [System](../../docs/system.md#knowledge-and-science), which is defined inline without its own document.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - knowledge.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) - moved

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
- **Leave "knowledge" undefined and regulate only storage behavior (rejected; migrated from the same nested block)**: management rules stated over an undefined central term import the reader's colloquial sense. Memar's terminology governance ([Terminology → Terminology Authority and Governance](../../docs/terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, here, and letting other documents reference that definition.

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

---

### Continuous model, executable projections, durable writing
- Time: 2026-09-18T12:20:00Z
- Type: Changed
- Cited:
  - [comparisons/superpowers.001.md](../../docs/comparisons/superpowers.001.md) — Evidence: owner critique of treating marketplace/plugin skill packs, prose recipes for generative work, and reader-workaround documentation as substitutes for a continuous knowledge model.
  - [Agency → Prompt Engineering and Harness Engineering](../../docs/agency.md#prompt-engineering-and-harness-engineering) — Depends_on: distribution and harness technique remain under Communication, not the knowledge model.
- Propagates to:
  - [.agents/scripts/README.md](../../.agents/scripts/README.md) — Clarified: marketplace/plugin are delivery tax, not the mental model.
  - [.agents/skills/README.md](../../.agents/skills/README.md) — Recorded: failed split of Khayyam/Cognition into peer skills.
  - [comparisons/README.md](../../docs/comparisons/README.md) — Points at these principles as standing assumptions for public comparisons.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../../CONTRIBUTORS.md#composer) (Composer via [Cursor](../../CONTRIBUTORS.md#cursor)) — drafted

#### What changed
- Expanded [Knowledge and Code](./knowledge.md#knowledge-and-code) to separate prose contracts from executable generative services (language-server / tool-call style), using Error-module generation as the illustrative pattern rather than a Practice that narrates each concrete artifact.
- Added [A Project Carries One Continuous Mental Model](./knowledge.md#a-project-carries-one-continuous-mental-model): distribution adapters may multiply; the internal model must not be partitioned into per-harness skill packs. Records Memar's failed experiments with a separate Khayyam skill and Cognition as a peer skill.
- Added [Write for the Structure of the Subject, Not for Today's Reader Limits](./knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits): governing text must remain true as readers (including models) change capability; load-bearing logic must not live in decorative tables or digraphs that models misparse.

#### Deliberation
- Marketplace/plugin as the project's self-introduction, multi-skill fragmentation, prose-only generative recipes, and documentation aimed at temporary agent weaknesses were rejected as knowledge-model shapes (Omid Hekayati). The comparison with Superpowers was the occasion; the principles are stated domain-generally where they apply, and software-specifically under Knowledge and Code where generation is the issue.

---

### Install as a project pointer; drop host-tool plugin packaging
- Time: 2026-09-19T09:57:00Z
- Type: Changed
- Cited:
  - [schema.org](https://schema.org/) — Depends_on: identity vocabulary for `manifest.yaml` (SoftwareApplication, SoftwareSourceCode, and shared CreativeWork properties). CodeMeta was considered as a middle vocabulary and rejected: it is a citation crosswalk that restricts and extends schema.org for scientific software, which this file is not.
- Propagates to:
  - [AGENTS.md](../../AGENTS.md): Done — session entry is now `.agents/memar/README.md`; `.agents/README.md` is a directory index, not loaded every session.
  - [README.md](../../README.md): Done — two install scripts (project via AGENTS.md, agent apps) plus a weaker chatbot path.
  - [.agents/skills/README.md](../../.agents/skills/README.md): Done — plugin/marketplace pointer removed.
  - [comparisons/README.md](../../docs/comparisons/README.md): Done — standing principle retargeted off `installing.md`.
  - `.agents/installing.md` and host-tool plugin/marketplace manifests: Done — removed.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../CONTRIBUTORS.md#cursor)) — drafted

#### What changed
- [A Project Carries One Continuous Mental Model](./knowledge.md#a-project-carries-one-continuous-mental-model) no longer treats marketplace/plugin packaging as a tax Memar still pays. Access is a pointer installed into a consuming project's instruction files, plus an optional user-level skill copy; the skill remains a routing practice into the live `docs/` tree.

#### Considered and not done
- **CodeMeta 3.1 as the manifest vocabulary**: it would have limited property choice, but it is an intermediary over schema.org aimed at scientific-software citation, with extra terms this project does not need (`readme`, `developmentStatus`, `issueTracker`) and a conventional filename (`codemeta.json`) this repository is not adopting.
- **Keeping host-tool plugin manifests at the repository root**: they do not make Memar discoverable by name in official marketplaces; the user still has to add the GitHub repository by hand. They cluttered the root without changing how sessions load the practice.

---

### Scale what the record owes a reader by what misreading it costs
- Time: 2026-10-03T14:13:29Z
- Type: Changed
- Cited:
  - [Knowledge Research 001](./knowledge.research.001.md) — **Evidence**: the inquiry that produced the weighting and the paragraph below, and the record of the claim that was withdrawn from it and the paragraph rewritten. `Complete`.
  - [ASD-STE100 FAQ](https://www.asd-ste100.org/faq.html) — **Evidence**: the maintainers' own answers on what a checker can and cannot do for STE, on whether writing in it correctly saves the writer effort, on whether its dictionary is closed, and on the line its authors draw between the language and its principles. Written by the Simplified Technical English Maintenance Group; read at one remove from the specification's own text.
  - [ASD-STE100](https://www.asd-ste100.org/) — **Evidence**: the controlled language itself, its stated purpose, its scale (fifty-three writing rules, a dictionary of about nine hundred approved words), and its current issue. Read from the maintainers' own site.
  - [Simplified Technical English](https://en.wikipedia.org/wiki/Simplified_Technical_English) — **Evidence**: the standard's history, and the failure recorded against its use outside the industries that wrote it. Tertiary sourcing, used for the record of third-party failure only; no claim in this document rests on it alone.
  - [Karpathy on consuming model output](https://x.com/karpathy/status/2105819303471976479) — **Evidence**: the occasion. The post's own claim is that his authors get more readable output when asked for STE, which is a self-assessment of practice; it is admitted as the claim being weighed, not as support for what this document now states.
- Propagates to:
  - [knowledge.research.001.md](./knowledge.research.001.md): Complete — the inquiry this entry answers; its [Findings](./knowledge.research.001.md#findings) hold the reasoning and its [Conclusion](./knowledge.research.001.md#conclusion) holds the negative result.
  - [content.md](content/content.md): Done — the same occasion adds the inspectability consequence to [Concrete Evidence: Tree/Graph Notation in This Very Document](content/content.md#concrete-evidence-treegraph-notation-in-this-very-document).
  - [terminology.md](../../docs/terminology.md): None needed — [Terminology → Terminology Authority and Governance](../../docs/terminology.md#terminology-authority-and-governance) already confines Memar's governance to the terms it has defined and disclaims the language generally, which is what makes the diagnosis portable here without the instrument.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — drafted

#### What changed
- [Write for the Structure of the Subject, Not for Today's Reader Limits](./knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits) now states that what a document owes its reader is weighted by what that reader's misreading costs. Where the subject cannot absorb an error, what is owed is not legibility but performability: every step executable as written, with no step left to interpretation.
- The case that prompted it is named and bounded. ASD-STE100 answers this obligation with fifty-three writing rules and about nine hundred approved words; what Memar takes from it is the diagnosis rather than the instrument — a reader who misresolves a word is a defect with an owner, answered by defining the term and stating where the definition diverges from ordinary usage, not by narrowing the vocabulary a reader may use. The reason the instrument does not travel is stated from the standard's own maintainers rather than from a secondary account: a checking product cannot replace the specification, no such product is certified as compliant with it, writing in it correctly demands professional judgment rather than saving it, and its dictionary is not closed — the domain's own technical names are the exemption the maintainers themselves carve out. A checker standing in for an understanding is the substitution Test → What a Passing Suite Establishes (`docs/modules/process/test.md#what-a-passing-suite-establishes`) already rules out.
- The Principle statement gains its third sentence, so the section's summary states the whole of what the section now holds.
- The paragraph was written once and then rewritten within the same day. Its first version rested on a claim sourced to a tertiary article, and on a premise about the standard's intended reader that the maintainers deny; the claim was replaced with statements read from the maintainers and the narrow premise was withdrawn. [Knowledge Research 001 → A correction this research's own first pass required](./knowledge.research.001.md#a-correction-this-researchs-own-first-pass-required) records the correction rather than only its repair.

#### Considered and not done
- **Adopting a controlled vocabulary for Memar's written record**: rejected. [Terminology → Terminology Authority and Governance](../../docs/terminology.md#terminology-authority-and-governance) governs the terms Memar has defined and disclaims ordinary language, and [cognition.practice.md](../../docs/cognition.practice.md) lists terminology policing — objecting to word choice while agreeing on meaning — among the critiques that are not critique. A dictionary-bound register would also freeze the questions this project keeps open, several of which are open precisely because no name has been settled yet.
- **A separate principle section for the cost weighting, with its own Principle statement**: not taken. The weighting qualifies the section it was found through rather than standing beside it, and a second section would have split one principle into two summaries of each other.
- **An interactive HTML or generated-video rendering of Memar documents**: not taken, and not recorded here. The rendering side of that question belongs to [Content → Authoring Syntax vs. Semantic Graph](content/content.md#authoring-syntax-vs-semantic-graph), which already states that the Graph is reached by many independent Renderers; whether this project wants such renderers is an open question, and the occasion does not settle it.

---

### The Task is named as deliberately undefined where it carries weight
- Time: 2026-10-04T00:00:00Z
- Type: Changed
- Cited:
  - [Terminology → A Term Deliberately Left Open](../../docs/terminology.md#a-term-deliberately-left-open) - **Reference**: the class and its single member, decided in the session that recorded them.
- Propagates to:
  - [terminology.md](../../docs/terminology.md): Done - the class this site points at.
  - [documentation-changelog.md](../../modules-plugable/knowledge/documentation/changelog/changelog.md): Done - the `Tasks` field marks its own use the same way.
  - [documentation.practice.md](../../modules-plugable/knowledge/documentation/documentation.practice.md): None needed - the practice's Research procedure sends an inquiry's outcome to its base changelog, which is where this entry is.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided the position this site records
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) - drafted

#### What changed
- [Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) states, at the principle statement that makes the Task the primary unit of knowledge evolution, that the word carries its ordinary sense and is deliberately not defined by Memar, with a link to [A Term Deliberately Left Open](../../docs/terminology.md#a-term-deliberately-left-open). The passage is one of the two places where the word does real work in Memar, and it is read far more often than the facet that now governs the term; a reader arriving here first met the principle without the qualification, and a reader who took the ordinary sense as Memar's had adopted a definition Memar never made.

#### Considered and not done
- **A footnote rather than a sentence in the principle statement (rejected):** the qualification is not incidental to the claim. The claim's force depends on the Task being a unit rather than an event, and a reader who reads *Task* as Memar's undefined-but-defaulted word is reading a different claim.
- **Restating the class's reasoning here (rejected):** the Content Rule's prohibition on redundant restatement, and the reasoning belongs with the class rather than beside each of its two members.

---

### Restate the relation of two sources recorded before the standing rule
- Time: 2026-10-04T13:27:43Z
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) - claimed, argued, applied

#### What changed
No entry above is edited. This entry states the relation two of them recorded, under [Documentation → Citations → Source standing](../../modules-plugable/knowledge/documentation/documentation.md#citations) as that rule now reads.
- The tertiary compilation cited in *Scale what the record owes a reader by what misreading it costs* is recorded with the `Reference` relation, not `Evidence`. A tertiary compilation is a pointer toward primary sources, and the entry's own text already said that no claim in the document rests on it alone; the body text it supported does not carry the claim it was cited for.
- The social-media post cited in that entry and in *A rendering is checked by eye, and names the reader it is for* is recorded with the `Reference` relation, not `Evidence`. A post of that kind is admitted as the claim being weighed and as the occasion for the question, which is what both entries already said in their own words; the conclusions rest on the notation examined in the documents themselves.

#### Considered and not done
- Relabelling the two entries in place was rejected (Space Bunny Alpha — argued). A changelog is append-only, and an entry rewritten after the fact cannot be distinguished from one that was written that way; restating the relation here keeps the earlier text intact and the correction visible.
- Withdrawing the social-media post from the record entirely was rejected (Space Bunny Alpha — argued). Recording where a question came from is legitimate and both entries record it honestly; what was wrong was the relation, not the record.

#### Deliberation
The rule added in [Documentation → Citations](../../modules-plugable/knowledge/documentation/documentation.md#citations) was applied against the whole doc set rather than only against the session that wrote it, and four citations across four records were found that the rule does not accept (Space Bunny Alpha — argued). Two were in records this chat owns and were corrected there: `rule.research.001.md`, whose vocabulary sources support nothing and whose specification was never read, and `documentation-handoff.research.001.md`, whose vendor article is a vendor's account of its own product. The other two sit in changelogs written by earlier chats and are corrected by this entry instead (Omid Hekayati — decided).

---

### Knowledge handoff: granularity and snapshot-hybrid questions removed

- Time: 2026-10-04T18:17:13Z
- Type: Fixed
- Propagates to:
  - knowledge.handoff.md: Done — the "What IS the minimum viable knowledge unit?" and "Can snapshot-style state ever be completely eliminated?" open questions were deleted; `knowledge.md` already answers both (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `docs/knowledge.handoff.md` no longer carries the open question on the minimum viable knowledge unit. Its answer is in [Knowledge → The Smallest Knowledge Unit Is Smaller Than You Think](./knowledge.md#the-smallest-knowledge-unit-is-smaller-than-you-think): units are representable "at the granularity of individual concepts, assertions, and distinctions", the list extends from Concept and Assertion to Distinction, Pattern, Rule, and Question, and the principle statement closes the domain-dependence half of the question with "The choice of granularity should be driven by the use case, not by storage convenience."
- The same handoff no longer carries the open question on whether snapshot-style state can ever be eliminated, nor its hybrid-model follow-up. [Knowledge → Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) already holds both positions at once: knowledge history is organized around the Task rather than the snapshot, and snapshots "remain valuable for reproducible builds, deployment state, forensics, regulatory audits, and legal holds" — precisely the legal-hold, audit, and clinical cases the question named, so the coexistence the question asked for is stated, not merely permitted.
- No other open question in that handoff was touched.

#### Considered and not done
- Rewriting the entries as resolved entries, or marking them "Answered": a handoff holds current state, and a rule already recorded in its governing document must not be restated there — the duplicate is what drifts. Both questions leave without a marker, per [Documentation Handoff → Optional Sections](../../modules-plugable/knowledge/documentation/handoff/handoff.md#optional-sections).
- Deleting the `## Anticipated Work` line on **Versioning Strategy**: it asks how versioning works in a non-file-centric system — content versions, snapshot versions, logical timestamps — which is broader than the coexistence of snapshot state with task-centric evolution, so it stays as work still owed.
- Narrowing the **Versioning Strategy** line to exclude the snapshot half, since that half is now settled: the line's own question — how versioning works where there are no files — is not what the deleted question asked, and rewording it would be an edit the closed question does not justify.

---

### Hierarchy is a projection, not the crossover's location
- Time: 2026-10-04T20:14:25Z
- Type: Changed
- Propagates to:
  - knowledge.handoff.md: Done — the open question on where hierarchical classification is actually optimal was deleted; the answer is in the governing document.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Classification Should Not Be Confined to a Single Hierarchy](./knowledge.md#classification-should-not-be-confined-to-a-single-hierarchy) gains a paragraph stating that a tree remains a legitimate projection where membership is genuinely single-parent — configuration baselines, taxonomic ranks, library classification — but that it is a projection and not the knowledge model: identity stays independent of position there as elsewhere, and a second taxonomy is added beside the tree rather than replacing it. The paragraph locates the crossover in the first question whose answer requires crossing facets rather than in a class of domains, and qualifies the section's Principle statement instead of excepting itself from it.
- `knowledge.handoff.md` no longer carries the entry "Are there domains where hierarchical classification IS actually optimal?". Its other four entries — concurrent knowledge modification, Task decomposition, cultural factors, and the concept-hub entry point — are untouched.

#### Considered and not done
- **Naming configuration management, biological taxonomy, and library classification as domains where hierarchy is optimal (rejected):** the record cannot establish that membership in those domains is in fact single-parent. An assertion about them would be domain knowledge the principle does not rest on, and it would place the crossover in exactly the class of domains the paragraph's own sentence denies.
- **Rewriting the deleted entry as a settled entry (rejected):** a handoff holds current state, and a rule recorded in the governing document must not be restated there — the duplicate is what drifts.

---

### Concurrent modification, the entry point, and Task decomposition resolved from what the principles already hold
- Time: 2026-10-05T11:40:00Z
- Type: Changed
- Cited:
  - [Terminology](../../docs/terminology.md) - Consumed definitions: Terminology Authority and Governance (one authoritative home per Definition, and the governing document where two disagree) and A Term Deliberately Left Open (Task as a term used but never defined in Memar).
  - [Changelog](../../modules-plugable/knowledge/documentation/changelog/changelog.md) - Consumed structure: Considered and not done, the home for reasoning examined and not applied.
- Propagates to:
  - knowledge.handoff.md: Done - three open questions removed: concurrent knowledge modification without locking semantics, whether the Task concept decomposes further, and the entry point into a knowledge system.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) gains a paragraph stating that concurrent modification is reconciled as what it is: two changes to one definition arriving at once are two decisions about the same invariant rather than two writes to one text, the invariant has one authoritative home, and what is reconciled is the claim and not the file — the revision that holds stands in the governing document, and the reasoning of the one that does not stays readable as Considered and not done.
- [The Smallest Knowledge Unit Is Smaller Than You Think](./knowledge.md#the-smallest-knowledge-unit-is-smaller-than-you-think) gains a paragraph stating that an entry into a knowledge system is one of its units surfaced rather than a page — a concept carrying its definition together with the context that unit holds — and that a listing, a wiki page, or a search result remains a valid projection of that entry.
- `knowledge.handoff.md` no longer carries three entries. "How do we handle concurrent knowledge modification without locking semantics?" and "What is the entry point into a knowledge system, and what does a concept hub carry?" are answered by the two paragraphs above. "Does the Task concept itself decompose further?" is answered by [Terminology → A Term Deliberately Left Open](../../docs/terminology.md#a-term-deliberately-left-open): Task is a term used but never defined in Memar, and what a Task is structurally, what states it has, and how one is identified belong to the project developing it. Its remaining entry, on cultural factors in principle adoption, is untouched.
- The removed entry-point entry's registered candidate source, a wiki system named Genera, stays unregistered. No primary source for it has been read, so under [Documentation → Citations](../../modules-plugable/knowledge/documentation/documentation.md#citations) it may prompt a question but may never carry a conclusion; the one thing it was registered to settle — whether that system's entry is a page or a unit surfaced — is settled here without it.

#### Considered and not done
- **Answering the entry-point question from a named external system (rejected)**: the handoff recorded the candidate and withheld its link until a primary source is read. A conclusion resting on an unread source is a claim the record cannot defend, and the conclusion the entry was reaching for follows from two principles this document already states.
- **Naming a concept-hub type, or an entry-point pattern beside it (rejected)**: a Type carries the four elements [Terminology Authority and Governance](../../docs/terminology.md#terminology-authority-and-governance) requires before a term has authority, and the paragraph states what the entry carries without adding a word the framework would then have to govern.
- **Defining Task here as Memar's own primitive, so the decomposition question could close in this document (rejected)**: [A Term Deliberately Left Open](../../docs/terminology.md#a-term-deliberately-left-open) states the price of taking the word — the concept cannot grow past the shape the framework's convenience gave it — and names the project where Task's structure is being worked out.
- **Adding a locking or merge-semantics section beside the new paragraph (rejected)**: such a section would state a mechanism over the artifact rather than over the unit of evolution, which is the thing the paragraph identifies as what gets reconciled.
- **Restating the entry-point conclusion in `knowledge.handoff.md` as a settled entry (rejected)**: a handoff holds current state, and a rule the governing document now carries must not be duplicated there.

---

### The domain-independence evidence named as one observer's route, and organizational knowledge management released from one project
- Time: 2026-10-05T12:20:00Z
- Type: Changed
- Cited:
  - [Protocol](../../docs/protocol.md) - Consumed definitions: Who Defines a Protocol (each definer's account is decidable at the level of the organization that offers it; plurality of definers is what makes convergence objective rather than hypothetical).
  - [Terminology](../../docs/terminology.md) - Consumed definitions: A Term Deliberately Left Open (what a Task is structurally belongs to the project developing it, not to the framework) and Terminology Authority and Governance.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Methodology](./knowledge.md#methodology) now names its warrant for domain-independence as one observer's, and records the stronger route beside it: "That is one observer's route to that conclusion, and the record should name it as such rather than let it read as the only available one. The stronger route is that separate organizations have arrived at these failures and the principles addressing them independently; each states its account at the level of the organization that developed it ([Protocol → Who Defines a Protocol](../../docs/protocol.md#who-defines-a-protocol)), and their agreement where they overlap is what identifies the concept they are each modelling rather than leaving it assumed."
- The scope boundary under [Knowledge in Memar's Concept Web](./knowledge.md#knowledge-in-memars-concept-web) now reads that knowledge management as an organizational discipline "belongs to whichever project is developing it; the Organization project is where that development is happening, not where the concept is owned."

#### Deliberation
- Both passages were identified in an earlier read-only pass of this chat by the same participant now applying them, which surveyed `docs/` for passages in tension with the organizational-plurality ruling; that ruling was made elsewhere in this chat and applied to the Protocol document earlier in the wave.
- The Methodology sentence was left standing and named rather than replaced. The cross-domain observation is real evidence and this document performed it; dropping it in favour of independent arrivals would replace a warrant the record holds with one it does not yet hold, since no second organization's independently arrived-at account of these principles has been read.
- The scope-boundary sentence was read as naming where the work happens rather than where the concept lives, because that is what the surrounding clause does elsewhere: it routes creation workflows, tacit-to-explicit conversion practice, sector adoption patterns, and change management out of this document. Ownership language would have said the concept has one home, which is the claim the change removes.
- The open question "How do cultural factors affect principle adoption?" stays. It asks whether the principles need cultural localization, and what this entry records is which warrant supports their universality — a different question, and one the entry's own wording keeps open by stating the independent-arrival route as stronger without asserting that it has been satisfied.
- The Anticipated Work entries on migration and the Task domain model are untouched; both still name the Organization project as where that work is done, which this change now reads the same way.

---

### Material with no producing decision: a placement survey, and what Knowledge already holds
- Time: 2026-10-07T06:25:00Z
- Type: Added
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](../../docs/comparisons/spec-kit.001.md) - Evidence: the comparison whose separate-research items raised the question, and whose account of the categories this survey inherited rather than re-read.
- Propagates to:
  - knowledge.handoff.md: Done - the survey's five open questions now live there.
  - documentation.md: Reference - the Content Rule was the first candidate home and was set aside on its own scope statement; nothing changed there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - questioner, goal-setter
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) - researcher

#### What changed
- No document changed. What this entry records is a survey and its negative result: whether Memar needs a named category for material that exists in the shared medium without any decision having produced it, and if so what kind of thing that category would be.

#### Surveyed
- **Placement.** Knowledge is the base artifact, because the question's subject is the provenance of material in the medium, which is that document's declared subject. Process disqualifies itself in its own Abstract - it is concerned with behavior and progression, "not with the static existence of things" - and a category for material that exists is a category of static existence. The Content Rule cannot host it without changing its stated scope, since the medium holds modules, code, and generated artifacts as well as documents; that assumption was the survey's first and did not survive the rule's own scope statement. `docs/protocols/` is not the home per its own membership criterion.
- **What Knowledge already holds, which is most of the answer.** The Decision is already the primary unit of knowledge evolution; the knowledge unit is already defined as more than the artifact, so material with no producing decision is describable in that vocabulary today as a unit that is only its artifact; Attribution is already a first-class relation type; and a Rule is already required to be authored, for one class of artifact.
- **The nearest named condition is adjacent, not covering.** Context decay is about context lost, not context never held - the artifact had a decision whose rationale has since decayed, where material with no producing decision never had one to lose.
- **Two adjacent rules that do not reach the case.** The empty-result rule governs what a check adds, not what it finds; and a change judged too small to audit receives no entry, which is a different situation from material that is not a change at all.

#### Considered and not done
- **Proposing the category** (not taken): the survey establishes where such a category would have to live and what it would collide with, and the question of whether Memar needs one at all is unasked by any document consulted. That is a decision for the owner, and it is now a question in [Knowledge Handoff](./knowledge.handoff.md) rather than a claim in a record.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:29Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the working tree against HEAD for `knowledge.md`, `knowledge.handoff.md`, `knowledge.changelog.md` and `knowledge.research.001.md`. The link changes from `protocols/` to `modules/` resolve (`memar content check`). The five body additions (Methodology's one-observer sentence, the scope boundary, the concurrent-modification paragraph, the single-parent tree paragraph, the entry-point paragraph) are each carried by the 2026-10-04 and 2026-10-05 entries above, and the handoff removals they record are the only removals; no changelog entry was removed.
- [Methodology](./knowledge.md#methodology) is corrected where it stated more than the record holds. It said separate organizations "have arrived at" these failures independently, while the 2026-10-05T12:20:00Z entry's Deliberation says no second organization's independent account has been read and that the route is stated "without asserting that it has been satisfied". The sentence now states the stronger route in the conditional and says the record has not followed it.
- [Classification Should Not Be Confined to a Single Hierarchy](./knowledge.md#classification-should-not-be-confined-to-a-single-hierarchy) no longer names configuration baselines, taxonomic ranks and library classification as single-parent. The 2026-10-04T20:14:25Z entry's *Considered and not done* rejects naming them because the record cannot establish that membership in those domains is single-parent; the paragraph did the thing the entry rejected. The paragraph now says a tree remains legitimate "where membership is genuinely single-parent" and names no domain. That entry's *What changed* still lists the three domains; it records what was applied then and is not rewritten.
- `knowledge.research.001.md` differs from HEAD only in link paths and in its working-copy line endings; no finding changed.

#### Considered and not done
- Removing the "Task Domain Model" item from `knowledge.handoff.md` Anticipated Work because Terminology leaves Task undefined: not done, since the item asks for a model the Organization project is developing, which that term entry does not contradict.

---

### An agent's route to a third-party library's shape is a question, not a rule
- Time: 2026-10-12T10:08:42Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided
  - Auto (model not recorded) via [OpenCode](../../CONTRIBUTORS.md#opencode) - applied

#### What changed
- [Knowledge Handoff → What an agent is to do when it lacks a third-party library's shape](./knowledge.handoff.md#what-an-agent-is-to-do-when-it-lacks-a-third-party-librarys-shape) records the question: no Memar document states the route an agent takes when it needs the current interface of a library the project depends on and cannot reach it from the project's own sources.
- The entry names the four norms the surrounding documents already hold for that case - source is context and never a substitute for inspectable support, a stale shared artifact is reported rather than propagated, an answer the lookup does not hold is reported rather than supplied, and the performed service over a live corpus is delivered outside this repository - so that the next chat does not re-derive them.
- Two questions are left to the owner: which route is sanctioned, and whether such material grounds an agent's reasoning or is evidence to be checked.

#### Considered and not done
- Writing the rule in `knowledge.md` or `agency.md`: not done. A source's standing is already held as a discourse norm ([Cognition → Evaluate claims on their merits](../../docs/cognition.md#evaluate-claims-on-their-merits-treat-source-as-neither-authority-nor-disqualifier)), so a second statement would restate it, and the act the question turns on - a text an agent reads as material rather than a claim offered in an exchange - is not the act that norm governs. The gap is the question, not the norm.
- Naming the neighbouring project this question came from: not done, by the owner's ruling. The examination is a document in `docs/comparisons/` and is found by listing that folder.

---

### Review of the Context7 placements of 2026-10-12
- Time: 2026-10-12T11:01:35Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — revised

#### What changed
- The earlier entry "An agent's route to a third-party library's shape is a question, not a rule" carried a Time of 2026-10-12T11:20:00Z, which was invented and later than the write; it now carries the file's write time, 2026-10-12T10:08:42Z.
- [Knowledge Handoff → What an agent is to do when it lacks a third-party library's shape](./knowledge.handoff.md#what-an-agent-is-to-do-when-it-lacks-a-third-party-librarys-shape): the absence claim is scoped to the search made, and the entry now cites Module dependency (`docs/modules/computer/module-dependency.md`), whose pinned repository reference already answers which revision a project builds against, and says what stays open. The earlier entry's "four norms" was wrong: three are norms and the README sentence is a scoping statement; the handoff now says so.

#### Why
- An independent evaluation (task 20261012-T105448Z-25360) found the invented time, an unscoped absence claim, and a missing citation of the document that already answers part of the question.

#### Considered and not done
- Moving the question out of Knowledge: not done. Knowledge is a weak home, but no better owner was found, and the owner has not ruled.

---

### Practice description states when and what not
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- `knowledge.practice.md`'s `description` now states when each of its three procedures is used and what it is not — the critique procedure, and the concept and its principles, which Documentation — Practice → Description quality criteria requires.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.

---

### The document moves to `modules/knowledge/`
- Time: 2026-10-17T12:30:00Z
- Type: Changed
- Cited:
  - [Modules → What does not belong here](../README.md#what-does-not-belong-here) — `Depends_on`: a concept document stands beside the module or category of its subject
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- `docs/knowledge.md` and its companions (changelog, handoff, practice and research) moved to `modules/knowledge/`, so the concept stands in the category it belongs to and the category's `README.md` is a link to it. Links to the documents were rewritten and nothing else in them changed; a closing section naming the category's modules was added to the document.
- Occasion: the owner's ruling of 2026-10-17 that a category without its concept document invites a misreading of the concept.

---

### Organization's knowledge text carried into this document
- Time: 2026-10-19T11:00:00Z
- Type: Changed
- Cited:
  - Organization's `modules/knowledge/knowledge.md` at commit 19834121 — `Depends_on`: the text the merge of 2026-10-19 left only in history, carried here by hand
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- Added to [The Modules of This Category](./knowledge.md#the-modules-of-this-category) the placement of organizational knowledge management: a composition bundle, not a module, with its bundle, handoff and channel-comms links.
- Occasion: the merge of organization into memar kept this file and left organization's version in history.

#### Considered and not done
- **The Wikipedia definition of knowledge and of knowledge management (dropped)**: the [Definition](./knowledge.md#definition) section and the opening paragraph already define both for Memar's purpose, and a second definition beside them would be two models.
- **The "Idea backlog" on health-directive labels "Life support" and "Donate" (kept here, not ratified)**: bare labels with no semantics in a protocol package. Review questions it carried: which capability owns an advance health directive, a signed-instrument concern of [Contract](../rights/contract/contract.md), a person-record label set, or something else; until who may set it and what it triggers is written the labels fail the no-bare-edges test and stay backlog; and why the category root carried them at all, possibly a misplaced protocol. `modules/knowledge/protocol` does not exist in memar, so no labels were carried.

---

### Where documentation, search and Markdown stand
- Time: 2026-10-24T09:00:00Z
- Type: Changed
- Cited:
  - [Pluggable](modularity/labels/pluggable.md) - Reference: a pluggable folder named by its kernel module holds that module's optional parts
  - [Guest](modularity/labels/guest.md) - Reference: the label of a module whose subject is an outside surface
- Tasks:
  - main:.agents/tasks/20261018-T133018Z-26648/: Partial - the split of the content module's services; the owner agreed the placements in the chat
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — ruled the placements (2026-10-24)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — proposed, moved and recorded

#### What changed
- The section The Modules of This Category no longer says Documentation stands directly under the category. Documentation is a structure laid over content and text, so it is optional for them and is the pluggable `modules-plugable/knowledge/documentation/`; the way a document is written in Markdown is not its identity, and Markdown is the guest module `modules-plugable/computer/codec/markdown/`. A search over text is not a domain: its services are in the Text module.

#### Considered and not done
- A search module of its own (proposed first, refused by the owner: there is no search domain, only services that cover a search requirement).
- Documentation under the kernel category, as it stood: the plan and report records, which the task module needs, left it for the task module, which removed the kernel's dependence on it.
