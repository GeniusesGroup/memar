# Modularity Changelog

## Changelog

### Initial draft consolidating Module and Modularity
- Time: 2026-08-15T18:40:39Z (approximate — taken from the source chat log; adjust if this was not UTC)
- Type: Added
- Cited:
  - [Big Ball of Mud](https://www.laputan.org/mud/) — Evidence: used as prior art to argue that architectural degradation is a loss of coherent structure and controlled relationships, not a property of monolithic deployment specifically.
- Propagates to:
  - modeling.md: Pending — should eventually reduce its local Module-related reasoning (e.g. "Extensible Behavior Belongs to Pluggable Modules") and reference this document instead.
  - khayyam-modularity.md: Done — reduced to language/ecosystem consequences with this document as conceptual authority (recorded below, "Completed Khayyam-specific modularity propagation"); the file has since moved to docs/khayyam/modularity.md, which cites this document as authoritative.
  - process.md: Done — should reference this document for the Module/Process boundary distinction instead of restating it locally. [see process.md:349]
  - protocol.md: Pending — should reference this document for the Module/Protocol boundary distinction instead of restating it locally.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [ChatGPT](../../../CONTRIBUTORS.md#chatgpt) — drafted

#### What changed
- Created the first dedicated Explanation-facet document for Modularity, as Draft. It defines Module as a System considered under a modular boundary, independent of files, directories, packages, repositories, processes, services, containers, or deployment units; grounds Module identity in coherent responsibility and explicit relationships; distinguishes Module from Type, Process, and Protocol; treats Optional Module as a purpose-relative (not intrinsic) distinction; leaves the term Rule intentionally provisional; and treats EventTarget as a capability of an existing Type or Module rather than a separate event data model. It also reframes the Monolith-vs-Microservices comparison as a category error (an observer-boundary effect, not a modularity measure) and treats Big Ball of Mud as architectural degradation rather than a synonym for monolithic deployment.
- The document consolidates and generalizes material previously expressed across `modeling.md`, `khayyam-modularity.md`, `process.md`, `protocol.md`, and the project's broader terminology and systems reasoning, rather than leaving Module implicitly defined by its scattered usages.
- The document body and this changelog were drafted in an earlier, non-conformant format (ChatGPT).
- The document is intentionally Draft because terminology around Rule, Optional Module, EventTarget, and the precise formal relationships among Module, System, Structure, Framework, Protocol, Process, and Type remain open.

#### Deliberation
- The original problem was framed (Omid Hekayati).
- The initial structural questions were proposed (ChatGPT).
- The discussion was driven through many rounds (Omid Hekayati).
- The constitutional-law and Invoice/Product/Pricing examples were supplied (Omid Hekayati).
- Several proposed classifications were rejected as premature taxonomy (Omid Hekayati).

#### Considered and not done
- **A closed taxonomy of Module kinds (Core/Extension/Optional/Infrastructure/Policy Module) (rejected)**: raised during drafting and withdrawn as premature classification without a settled definition.
- **An Active/Passive Module distinction (rejected)**: raised during drafting and withdrawn once no genuinely passive Module could be identified.
- **Treating Rule as a Module's fixed attribute, versus treating it as a relationship between Modules (left open)**: left open rather than forced to a conclusion.

### Review pass: resolved structural duplication, added a comparison table and prior-art gap
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - modularity.md: Done — this entry documents the change made directly to the paired document in this same pass.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- The earlier ChatGPT-generated draft had produced two separate `## Discussion`-style sections — one nested inside `## Explanation` and one at the document's own end — with overlapping subsection names (`Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities`) but different content in each. These were merged into a single top-level `## Discussion`, with no content dropped.
- A "Module Among Related Concepts" table was added after the Module/Process/Protocol section to make the boundary between Module, Type, Protocol, Process, Rule, Abstraction, and Encapsulation scannable at a glance, since sharpening exactly this kind of boundary is the document's stated purpose.
- Domain-Driven Design's Core Domain was added to Prior art, since it is a well-known prior attempt at the same core-vs-satellite distinction and, per the discussion, suffers from treating criticality as intrinsic rather than purpose-relative — the same confusion this document argues against.
- An unresolved question was added noting that Module's peer-level relationship to Framework and Structure — raised early in the source discussion but never written into the document itself — is left open rather than asserted.

#### Deliberation
- A completeness check against the source discussion, and bringing the changelog into the project's documentation-changelog format, were requested (Omid Hekayati).

#### Considered and not done
- **Writing new content asserting Module's formal relationship to Framework and Structure (rejected for this pass)**: the project's own convention is to defer structural claims until the underlying design question is settled elsewhere, and Framework's relationship to Module was never resolved in the source discussion. Logging it as an explicit unresolved question was chosen instead, so the gap is visible without prematurely committing the document to an unreviewed position.

---

### Coordination pass with system.md, process.md, and modeling.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Propagates to:
  - system.md: Done — this document now cites the new Responsibility section instead of using "responsibility" informally.
  - process.md: Done — Module, Process, and Protocol shortened to point at process.md's own fuller treatment instead of restating it.
  - modeling.md: Done — added as a cross-reference for the `username`/`User` example illustrating the modeling/observation cycle.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document previously asserted "coherent responsibility" as if self-evident and duplicated `process.md`'s Module/Process boundary reasoning independently. Both are now resolved by citing a single authoritative source instead: Responsibility and its coherence test now live in `system.md`, and the Module/Process boundary argument now lives in `process.md`, with this document keeping only what is specific to Module's own side of each relationship.
- "capabilities and limitations" replaced with "capabilities and constraints" throughout (Abstract, Module Identity and Responsibility), to match the term `system.md`'s own Structure section uses.
- Module Identity and Responsibility rewritten to define a Module's identity via `system.md`'s new Responsibility section rather than an undefined "responsibility".
- Module, Process, and Protocol shortened to state only the Module-specific consequence and point at `process.md`'s own, more detailed Process and Boundary and Process Composition topics rather than restating their reasoning independently.
- Responsibility and Structure rows added to the Module Among Related Concepts table; the closing note's list of unaddressed peer-level concepts narrowed to Framework, now that Structure is addressed; Unresolved question 10 narrowed correspondingly.

#### Deliberation
- A coordinated pass across `system.md`, `process.md`, `modularity.md`, and `modeling.md` together was requested, so shared concepts have one authoritative home each and every other document references it, rather than each document defining its own version and drifting apart over time (Omid Hekayati).

---

### Fixed Protocol description to match protocol.md's actual ontology
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - protocol.md: Reference — this fix was found during a conceptual review of protocol.md against this and the other revised documents; see protocol.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document's characterization of Protocol did not match protocol.md's own ontology. Corrected both occurrences (the Module/Process/Protocol topic and the comparison table) to say Protocol governs Processes within a System, rather than System-to-System interaction directly, and linked to protocol.md instead of restating its definition from memory.
- The corrected occurrences had described Protocol as governing "interactions within or between Systems" — this document's own paraphrase, not protocol.md's actual definition, which routes Protocol through Process (System contains Processes, governed by Protocols) rather than having Protocol govern System-to-System interaction directly.
- The link added points to protocol.md's "What is a Protocol?" topic.

#### Deliberation
- A conceptual review of protocol.md against the rest of the now-revised document set was requested (Omid Hekayati).

---

### Completed Khayyam-specific modularity propagation
- Time: 2026-08-19T00:00:00Z
- Type: Changed
- Propagates to:
  - khayyam-modularity.md: Done — reduced the Khayyam document to language and ecosystem consequences, with this document as the conceptual authority.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- The pending propagation to `khayyam-modularity.md` is complete. The Khayyam document no longer repeats the conceptual definition of Module or Modularity; it links here and retains only its treatment of `in`, explicit naming without package context, and framework-level manifest and dependency resolution.
- Verified that the general document already contains the authoritative Module definition and that the remaining Khayyam material is language/ecosystem-specific; the reciprocal link added and the pending propagation item closed.

#### Deliberation
- Reconciling the Khayyam modularity document with this general document was requested (Omid Hekayati).

---

### Capability completeness, foundation restraint, and decoupling conceptual from runtime dependency
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../../../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
- Propagates to:
  - modeling.md: Done in this same pass — Edge Types unresolved questions now include the bidirectional-relationship question referenced by Unresolved question 11.

#### What changed
- Added four things. "Capability Completeness": a Module introducing a meaningful domain relationship owns everything that makes it work — relationship, governing rules, and required processing — and a capability's parts must not scatter across its endpoints' Modules, with removal-cost stated as the negative test. "Foundational Concepts Should Remain Few": a mature System is expected to hold a small, stable set of foundational Concepts carrying many attached capabilities; an apparently new domain is first a hypothesis about a relationship, Rule, or Optional Module over existing Concepts, with industry domain names explicitly denied evidentiary status, and both failure directions (under-modeling, artificial decomposition) guarded. A sentence in Module Identity and Responsibility stating that a capability does not inherit identity from the concepts it operates on. "Conceptual Relationships Are Not Runtime Coupling": model-level mutual dependence may be realized asymmetrically in time and mechanism and is not inherently a defect; language-layer cycle rules constrain expression, not the domain. Extended document-level Unresolved Questions with the cross-Module hosting question.
- The findings were generalized to principle level without domain examples, and the placement deferral record below added.

#### Deliberation
- The discovery discussions these principles generalize from were driven — capabilities repeatedly misread as candidate new domains; one capability's parts nearly scattered across endpoint Modules; mutual conceptual dependency mistaken for a defect because of language-level cycle rules (Omid Hekayati).
- The positions were co-developed across parallel sessions, including the reversal that had initially separated a capability's processing from its relationship (ChatGPT).
- Scope and wording were approved (Omid Hekayati).

#### Considered and not done
- **Prescribing repository placement conventions for capabilities (rejected)**: where a Module is stored, and how repository trees express core-versus-plugable organization, are representation and tooling concerns deliberately kept outside this conceptual document. Current working position at the time of this change, recorded here so it is not re-derived later: repository placement and any entry-point/primary-domain taxonomy for optional capabilities remain open implementation-layer questions pending a dedicated layout/tooling document; nothing in this document should be read as settling them.

---

### Foundational-status test distilled from core-domain review
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../../../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
- Propagates to:
  - none — self-contained addition to this document.

#### What changed
- Added "What Earns Foundational Status", immediately following "Foundational Concepts Should Remain Few". The earlier topic sets the expectation and shifts the burden of proof; the new one supplies the decision procedure once the burden is met: attempt to express, through the remaining abstractions, the reality the candidate covers. Forced fabrication or distortion of another foundational abstraction earns foundational consideration; a gap fillable by an independently modeled capability places the candidate above the foundations regardless of how central it feels to any organization. Importance and usage frequency are recorded as non-evidence (consistent with the document's existing position on criticality-as-intrinsic readings of DDD's Core Domain), and two guards are stated explicitly: only fabrication landing inside the foundational set counts, and the test evaluates actual rather than anticipated requirements.
- The criterion was generalized into a topic without domain examples, and the two honesty guards added.

#### Deliberation
- The criterion was reached during a core-versus-plugable review of an economics domain tree — a foundational abstraction is one whose absence would force fabricating or altering another foundational concept to express the same reality (Omid Hekayati).
- The criterion and its application were co-developed across the same session (ChatGPT).
- Importance and usage frequency were confirmed to carry no evidentiary weight (Omid Hekayati).

#### Considered and not done
- **Folding the test into "Foundational Concepts Should Remain Few" as a paragraph (rejected)**: the two topics answer different questions — expectation and burden-shifting versus decision procedure — and keeping them separate lets each claim be cited independently when future classification debates reach for one and not the other.
- **Transferring the concrete domain placements that motivated the criterion (rejected)**: which specific domains in a given ecosystem's tree are foundational versus plugable is domain modeling work that belongs to that ecosystem's own documents; only the generalizable criterion enters this foundation document.

---

### Cross-reference to Code/Rule separation in modeling.md
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed.
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — applied.
- Propagates to:
  - none — companion edit to modeling.changelog.md (Code/Rule separation absorption).

#### What changed
Added a pointer from "Rules as a Provisional Term" to modeling.md's new "Separating Structure (Code) from Policy (Rule)" section, recording that a graph-node framing of Rule exists there and that its reconciliation with this document's module framing is an open question. No position change in this document.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - modularity.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, and Results only; the document-level `## Discussion` and the three topic-level `#### Discussion` wrappers (under Foundational Concepts Should Remain Few, What Earns Foundational Status, and Capability Completeness) are gone.
- Drawbacks were current-state claims about the design's cost, so they stayed inline at the claims they qualify: each topic's Drawbacks text now closes its own topic, and the document-level boundary-cost and two-failure-directions passages are folded into Module Identity and Responsibility at "Creating boundaries has a cost."
- Retired `Rationale and alternatives` content - the two topic-level subsections and the document-level section - is preserved below under Considered and not done; the document-level `Prior art` survey is preserved below under Related work.
- Unresolved questions (the document-level list plus the Capability Completeness question) and `Future possibilities` moved to the paired `modularity.handoff.md` as Open Questions and Anticipated Work.
- Passages already carried by the body were dropped rather than copied: the Rule-provisional restatement (Rules as a Provisional Term already states it), the implementation-mechanism deferral (Modularity and Implementation Representation plus this file's 2026-08-25 placement bullet already carry it), and the Big Ball of Mud prior-art paragraph (the body's Big Ball of Mud and Modularity section states it, and the initial-draft entry already cites Big Ball of Mud as evidence).
- Pointers into retired sections now link to their live homes: the Module Among Related Concepts note links to the handoff's Open Questions, and the Rules as a Provisional Term note links to Modeling's handoff where the Code/Rule reconciliation question now lives.

#### Considered and not done
- **Industry-domain-driven decomposition (rejected; migrated from the Foundational-Concepts-Should-Remain-Few topic's retired Rationale and alternatives)**: mirroring the ecosystem's recognized domains as foundational Concepts imports today's product boundaries as tomorrow's architectural boundaries.
- **Foundation-count as a target metric (rejected; migrated from the same topic's retired Rationale and alternatives)**: "few" describes the expected outcome of honest independence testing, not a quota; the number of foundations is an output of the model, never an input to it.
- **Importance or usage frequency as the foundational-status criterion (rejected; migrated from the What-Earns-Foundational-Status topic's retired Rationale and alternatives)**: criticality is relative to a particular System's purpose, and treating it as an intrinsic property of a Module reproduces exactly the confusion this document attributes to common readings of Domain-Driven Design's Core Domain (see this entry's Related work).
- **Universality across organizations as the foundational-status criterion (rejected; migrated from the same topic's retired Rationale and alternatives)**: a Concept every organization happens to want may still be composable from existing foundations; universality measures demand, not structural necessity.
- **Defining Module through packages, services, repositories, processes, containers, or plugins (rejected; migrated from the document-level retired Rationale and alternatives)**: each is too dependent on a particular representation or operational arrangement; defining modularity through the physical organization of software would make the architectural model unstable whenever languages, build systems, deployment platforms, or repository conventions changed. This was the central alternative rejected by the document.
- **Treating Microservices as the natural unit of modularity (rejected; migrated from the same section)**: deployment independence can be useful, but it is neither necessary nor sufficient for conceptual modularity.
- **Requiring a new domain data model for every extensible behavior (rejected; migrated from the same section)**: existing Concepts, service requests, responses, and capabilities should be reused when they already express the required information.
- **A closed taxonomy of Module kinds (rejected; migrated from the same section)**: terms such as *Core Module*, *Infrastructure Module*, and *Policy Module* may be useful in particular contexts, but they should not become part of the foundational definition unless the project discovers a real conceptual distinction that requires them. (The same rejection was first recorded in this file's initial-draft entry; this bullet preserves the retired section's own wording and scope note.)
- **Dropping the Optional Module term along with the taxonomy (not done; recorded decision; migrated from the same section)**: Optional Module is retained because it expresses a concrete distinction already required by the model - a Module can be structurally non-essential to a particular System while still providing valuable behavior.

#### Related work
- The discussion of modularity in software has appeared in object-oriented design, component systems, structured programming, package systems, service-oriented architecture, microservices, and Domain-Driven Design. These traditions provide useful mechanisms and observations but do not supply a single definition of Module that is independent of their implementation assumptions. Domain-Driven Design's Core Domain is a particularly relevant case: the term is commonly presented as if criticality were an intrinsic property of a domain, which invites the same confusion this document argues against - a Module's essential or optional status is relative to a particular System's purpose, not an inherent property of the Module itself. (Migrated from the document-level retired Prior art.)
- Memar treats prior architectural terminology as evidence and material for comparison rather than as authority over the definitions used by the project. (Migrated from the same section.)

---

### Khayyam upward links removed — citation direction enforced
- Time: 2026-09-23T07:07:01Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- "Conceptual Relationships Are Not Runtime Coupling" no longer hyperlinks Modularity in Khayyam: language-level cycle restrictions belong to the language layer, and each language's own modularity document records them — named in prose, not cited upward via hyperlink.
- The closing section's pointer to the Khayyam modularity treatment is now the plain phrase "the language's own modularity document"; the application that document records is still named, only not linked.

#### Deliberation
- Citation direction rule: a base document never links into `khayyam/` — not even as an instance pointer; plain-text naming only (Omid Hekayati — decided).

---

### Where the abstract data types belong is carried here
- Time: 2026-09-29T10:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided: code under `modules/` introduces itself, and a code folder carries only a README
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `modularity.handoff.md`: the ADT module-placement question moved to Abstract Data Types Handoff (`docs/modules/computer/adt.handoff.md#do-the-abstract-data-types-belong-under-computer-or-under-math`); its path now ends in a README for `modules/computer/adt/` or a widened criterion in Math → Realization membership (`docs/modules/math/math.md#realization-membership`).

---

### Fourteen `modules/` category-tree questions raised on the handoff
- Time: 2026-09-29T11:30:00Z
- Type: Added
- Propagates to:
  - docs/protocols/: Pending — folder categorization waits on owner answers to the fourteen `modules/` tree questions.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `modularity.handoff.md`: fourteen open questions from a critique of the `modules/` first-level category tree were raised here — storage/memory inversion, duplicate runtime homes, type categories under `computer/`, plural registry folders, `process/time` membership, duplicated identity types, split concurrency, foreign protocols outside `lib/`, `lib/` duplicates, mixed domain/implementation axes, `modules/modules` naming, `time/` axis mixing, minor naming inconsistencies, and `modules/README.md` drift. Each entry states evidence, a proposed change, and that it is not yet approved by the owner.

---

### Top-level `modules/storage/` renamed to `modules/memory/`
- Time: 2026-09-29T13:00:00Z
- Type: Changed
- Propagates to:
  - docs/protocols/: Pending — inner `storage/memory/` allocator placement still open in the handoff.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `modularity.handoff.md`: the top-level rename question is resolved — `modules/storage/` is now `modules/memory/`; former inner `storage/memory/` content is split into `reference/` and `address/` with `heap.kh` and `mem.kh` interim at module root pending owner choice of `allocator/` vs `heap/`.

---

### Repository layout questions raised on the Modularity handoff are out of scope for it
- Time: 2026-09-29T14:00:00Z
- Type: Changed
- Propagates to:
  - docs/protocols/README.handoff.md: Done — the provisional `docs/protocols/` category-folder note lives there.
  - docs/protocols/memory/memory.handoff.md: Done — `heap.kh` / `mem.kh` placement is a question about the memory module, so it lives with that module.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided: Modularity handoff carries Modularity-concept questions only
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) — applied

#### What changed
- `modularity.handoff.md`: the fourteen repository folder-layout questions were raised on this document in error — where a question about the `modules/` tree is answered is the owner's, and no document in this repository is the home for a cross-cutting layout question. Only the Modularity-concept questions and anticipated work remain here; the `heap.kh` / `mem.kh` question, which is about one module, went to that module's handoff, and the `docs/protocols/` category-folder note to that folder's own handoff.
- No handoff was created for `modules/README.md`. A layer that realizes specifications is not a base artifact that carries a Changelog or Handoff companion, so the questions stay unrecorded until the owner answers where they belong.

---

### The name-collision reasoning the language document carried
- Time: 2026-10-04T09:00:00Z
- Type: Added
- Cited:
  - Khayyam — Changelog (`docs/khayyam/khayyam.changelog.md`) — Evidence: `:630` records this document as the pending destination for the removed name-collision reasoning, and `:647` carries the three fragments the removal left behind.
  - Khayyam → Import Mechanism (`in`) (`docs/khayyam/khayyam.md#import-mechanism-in`) — Reference: `:62`, the sentence that sends a reader here for what a collision means and what a project does about one.
  - [Type → Type Identity](../../../docs/type.md#type-identity) — Premise: the base-layer statement that within one bounded context the name uniquely identifies the concept, and that two different structures under one name are a modeling conflict rather than two valid Types.
  - Khayyam Rule — Qualified Names (`bundles/khayyam/rules/qualified-names/qualified-names.md`) — Reference: the governance half — how a declaration carries the identity of the part that owns it, and what a tool reports when it meets a collision.
  - Khayyam Rule — Scope Visibility (`bundles/khayyam/rules/scope-visibility/scope-visibility.md`) — Reference: the owner's general rule that two identical names mean the development is faulty.
- Propagates to:
  - Khayyam → Import Mechanism (`in`) (`docs/khayyam/khayyam.md#import-mechanism-in`): Reference — its `Modularity is the subject` sentence now resolves; nothing in that file needed changing.
  - [Type → Type Identity](../../../docs/type.md#type-identity): Rejected — it already states the general rule, in the terms a name-collision finding is a special case of; adding the modular consequence there would have put a claim about Module identity into a document about Type.
  - Khayyam Rule — Qualified Names (`bundles/khayyam/rules/qualified-names/qualified-names.md`): Pending — its opening paragraph, its third case, its *Why it exists*, and its third *does not claim* bullet all cite the language document as holding the claim that a collision is an architecture error whose remedy is a redesign. That sentence was removed on 2026-10-03 and the section now points here instead, so four of its sentences rest on a premise its citation no longer carries. Not this session's file to write.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, ruled
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied, placed

#### What changed
- A new topic, [One Term, One Identity](./modularity.md#one-term-one-identity), carries the reasoning the audit removed: a term that has to stand for two different things is not an ambiguity the model may carry but a record that two independently identified things were collapsed onto one identity, and the collapse happened where they were brought together rather than where either was identified. It rejects both remedies the vocabulary offers — a second name for one of the two, and letting one answer to the other's term throughout — and states what is owed instead: each identified by the Responsibility it actually carries, an explicit relationship between them, and composition where one is wanted only as a means of reaching the other.
- The Abstract states the same claim in two sentences, since a reader who gets the document's shape from the Abstract should not meet the collision claim for the first time at the topic.
- **The base-document test was applied to the wording, not only to the placement.** Nothing in the topic is specific to a programming language, and nothing is specific to software: it is stated as Responsibilities, identity, boundaries, and explicit relationships, which is what a person building a house or designing a gas heater is already reasoning with. The evidence is that each sentence survives translation unchanged — two trades of a building both answer to the word *plumber* is the same finding as two libraries both declaring `Connection`, and the repair is the same one. No vocabulary of any language appears in it, and no compiler is mentioned.
- **The claim was placed here rather than in the rule about duplicate names, or in both, and the reason is one home per claim.** The general rule — one name, one concept, and a collision being a fault in the development rather than a shadowing a language permits — is already stated twice, once at the base layer by [Type → Type Identity](../../../docs/type.md#type-identity) and once as this repository's own governance by Scope Visibility (`bundles/khayyam/rules/scope-visibility/scope-visibility.md`). What neither of those carries, and what was removed with no destination, is the modular consequence: what a collision is a finding *about*, and what the model owes in answer. That is this document's, and it is stated here alone; the rule keeps the instruction a developer follows, and this document keeps the reasoning the instruction serves.

#### Considered and not done
- **Restating the general rule here as a lead-in.** It would have made the topic self-contained and would have put one claim in three documents. Rejected: the topic states what is owed in answer to a collision found, and assumes the reader already holds that a collision is a fault — the same way [Capability Completeness](./modularity.md#capability-completeness) assumes a boundary exists rather than arguing that one should.
- **Naming the language's import operator or the kind of thing it brings in.** The removed passages spoke of two abstractions claiming one concept and of wrapping a dependency in a local capsule. Naming either would have made the topic a Khayyam document parked in a base one, which is the caution the owner placed on adding a topic here at all.
- **Writing the topic as a procedure for resolving a collision.** "Report it, rename it, re-check it" is followable work and belongs to a Practice companion or to a project's governance rules, not to this document, whose subject is what the collision is.
- **Restoring the removed blockquote to the language document.** Rejected: the owner's ruling is that a language document states what a construct is, and what a collision means for the concepts involved is not a fact about the construct. The language document's remaining sentence says exactly that and points here.

#### Decision
- The collision reasoning belongs to Modularity, and the base document carries it in terms that hold for any kind of development (Omid Hekayati — decided). The general rule stays where it is already stated twice, and the mechanical half stays with the naming rules; this document holds the consequence and no vocabulary of any language.

---

### Six handoff questions closed by answers the record already carries
- Time: 2026-10-04T18:21:13Z
- Type: Fixed
- Propagates to:
  - modularity.handoff.md: Done — six open-question entries were deleted, each already answered in the document set (handoff: no entry of its own).
  - modeling.md: Done — Action: None — *Extensible Behavior Belongs to Pluggable Modules* already states the attachment relationship.
  - protocols/process/event.md: Done — Action: None — *The EventTarget capability* and *Relationship to other concepts* already carry the reusable contract and the Type/Protocol/Process split.
  - khayyam/modularity.md: Done — Action: None — *Manifest as the Module Contract* already separates Module identity from repository and filesystem conventions.
  - system.md: Done — Action: None — *When Is a Responsibility Coherent?* already states what a checkable boundary claim is.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `modularity.handoff.md` no longer carries the question "Can Capability Completeness be checked other than by hypothetical removal?". [Modularity → Capability Completeness](./modularity.md#capability-completeness) already answers it: removal is the negative test the completeness rule travels with, and the operative test is whether "the added material varies for reasons tied to this capability's own Responsibility, not whether it could physically be placed here" — a check made on the material itself rather than on a hypothetical deletion.
- The question "What exact relationship should a Module expose when it permits optional behavior to attach without changing its own model?" left the handoff. [Modeling → Extensible Behavior Belongs to Pluggable Modules](../../../docs/modeling.md#extensible-behavior-belongs-to-pluggable-modules) already answers it: `Invoice` "connects to any number of independently modeled, pluggable Modules through an ordinary reference edge", exposing the attachment point without changing its own shape.
- The question "What properties of an EventTarget are fundamental enough to define once and reuse across Types and Modules?" left the handoff. Event → The EventTarget capability (`docs/modules/process/event.md#the-eventtarget-capability`) already answers it: "the contract is three methods" — `DispatchEvent`, `AddEventListener`, `RemoveEventListener` — composed once by whatever Type or Module exposes the capability.
- The question "When an EventTarget exposes a request or response to interested participants, which parts belong to the Type, the Protocol, and the Process?" left the handoff. Event → The EventTarget capability (`docs/modules/process/event.md#the-eventtarget-capability`) assigns the Type and Module their half — a system whose "service request and response models already carry the relevant data does not acquire a parallel structure to notify anyone" — and Event → Relationship to other concepts (`docs/modules/process/event.md#relationship-to-other-concepts`) routes the rest: Process owns what an event is at the concept layer, Modularity "places the capability on the Type or Module that exposes it", and this protocol is "that capability's shape".
- The question "How should Module identity and dependency resolution be represented independently of repository and filesystem conventions?" left the handoff. Khayyam Modularity → Manifest as the Module Contract (`docs/khayyam/modularity.md#manifest-as-the-module-contract`) already answers it: the manifest is "the formal external contract through which a Module can be identified, referenced, validated, and consumed without inspecting its internal directory layout", and dependency resolution is one responsibility derived from that contract rather than the whole of it.
- The question "What evidence distinguishes a necessary Module boundary from fragmentation introduced only by implementation convenience?" left the handoff. [System → When Is a Responsibility Coherent?](../../../docs/system.md#when-is-a-responsibility-coherent) already answers it: what can be checked is "whether the part has an independent behavioral boundary and lifecycle", observed by asking whether validation, versioning, or meaning changes for reasons unconnected to the concept currently holding it.
- No base document was edited. All six answers were already in place; the graduation is the handoff ceasing to list questions the record has answered.

#### Considered and not done
- Marking the six entries Answered rather than deleting them — not taken. A handoff records where a discussion stands, and a resolved question is state the base documents now carry; leaving it here duplicates the answer and guarantees drift.
- Adding a short index of the six answers, or a pointer from the handoff to the sections holding them — not taken. The handoff's remaining entries are open questions, and an index of settled answers is the changelog's and the base documents' work, not the handoff's.
- Deleting the Anticipated Work line about a future document defining how modular boundaries can be reviewed independently of implementation structure — not taken. That line anticipates a review method with four named checks, of which the boundary-coherence question was one; the others remain anticipated work nobody has committed to, and the line was never scheduling that one question.
- Restating the co-variation test, the ordinary reference edge, the three-method contract, the manifest contract, or the boundary test inside `modularity.md` — not taken. Each already has one home, and a second copy in Modularity would put a claim about Modeling, the Event protocol, Khayyam, or System into a document whose subject is Module.

---

### Optionality and relationship ownership located by Responsibility
- Time: 2026-10-04T20:15:58Z
- Type: Added
- Propagates to:
  - modularity.handoff.md: Done — three open-question entries removed; the sections named below are their homes.
  - system.changelog.md: Done — the answer to the question about domain-coupled Responsibilities recorded in this document's handoff is recorded there.
  - modeling.handoff.md: Rejected — not edited here; the counterpart entry under Modeling's edge-types material is closed by that document's own changelog.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Modularity → Core Structure and Optional Modules](./modularity.md#core-structure-and-optional-modules) now states where the distinction between an optional extension and an ordinary independently related Module lies: with the containing System, not with either Module or with the explicitness of the relationship between them.
- [Modularity → Capability Completeness](./modularity.md#capability-completeness) now states where the Module owning a cross-boundary relationship lives: with whichever endpoint's Responsibility the relationship serves, and with neither endpoint when no endpoint's boundary spans every case it covers — the test [Modeling → A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once) states for domains.
- `modularity.handoff.md` no longer carries "Which properties distinguish an optional extension from an ordinary independently related Module?" or "Where should the Module that owns a cross-boundary relationship live when its endpoints belong to different Modules?"; its State about hosting chosen for repository convenience is now answered by the ownership rule rather than standing as a warning.
- `modularity.handoff.md` also no longer carries "How should modularity be evaluated when a single Module intentionally contains multiple lower-level responsibilities that are tightly coupled by the domain?"; that question is a question about Responsibility coherence and is answered in [System → When Is a Responsibility Coherent?](../../../docs/system.md#when-is-a-responsibility-coherent), recorded in [system.changelog.md](../../../docs/system.changelog.md).

#### Considered and not done
- **Closing the optionality question as already carried by the record, with no edit (rejected)**: the paragraph stated the removal test but never said the property is relative to the containing System, and that relativity is what keeps "optional" from being read as an attribute of a Module.
- **Adding the ownership rule to *Pluggable Does Not Mean Plugin* instead (rejected)**: that section separates a conceptual relationship from a loading mechanism; optionality and ownership are different distinctions, and merging them would make pluggability read as the test for either.
- **Naming an independent third home by default (rejected)**: an independent third Module is what the answer gives when no endpoint spans the cases the relationship covers, not a default that repository layout can invoke.
- **Closing the counterpart entry in `modeling.handoff.md` from here (rejected)**: that entry is Modeling's own open question about its edge types, and its closure belongs in that document's changelog rather than in this one.

---

### The Rule section states its modular consequence and links the settled concept
- Time: 2026-10-05T08:59:05Z
- Propagates to:
  - modularity.handoff.md: Done - the question of the final terminology for the kind of Optional Module discussed provisionally as a Rule removed; the Module/Framework question and the anticipated work left open
  - rule.md: Done - the settled two-lens statement lives there, and this section carries only the modular consequence of it
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `### Rules as a Provisional Term` now states what holds on the modular side: a Rule is a Module developed on its own, related to another Module, and its behavior can be attached to an existing Module without becoming part of that Module's essential identity.
- The paragraph that left the module and graph-node framings unreconciled, and this document's refusal to take a position on them, is replaced by a link to [Rule → One Concept, Two Lenses](./rule.md#one-concept-two-lenses), which states that the two are one concept, that neither lens is primary, and what each lens owes.
- `modularity.handoff.md` no longer carries the final-terminology question, and its first anticipated-work bullet names Rule rather than a provisional Rule concept.

#### Considered and not done
- **Retiring the section's title, "Rules as a Provisional Term"**: not done (Space Bunny Alpha — argued). protocols/ddd.md (`docs/modules/lib/process/ddd.md`) links this anchor from its comparison table, that document is outside this change's reach, and an anchor with no matching heading is a broken link. A title that no longer matches the settled position is the cheaper defect.
- **Restating the two-lens position in this document**: rejected. The concept is defined once in `rule.md`; a second and third copy in the two subject documents is how the copies begin to diverge, which is the failure [Modularity → One Term, One Identity](./modularity.md#one-term-one-identity) names.
- **Renaming what a Rule attaches to, or adding an attachment-point mechanism here**: not done. What an attaching Rule must provide is this document's own question, already carried by [Capability Completeness](./modularity.md#capability-completeness) and the handoff's anticipated work.

#### Deliberation
The section had been hedged in two directions at once — a Rule that *may* be a Module, and a second framing this document declined to reconcile — because the term's standing was open on the owner's side. The ruling closes the standing, so the hedge is removed rather than softened (Omid Hekayati — decided): what is left in this section is the modular consequence, and the two-lens statement is referenced where it is defined so that this document need not repeat it (Space Bunny Alpha — argued).

---

### Which modularity properties modeling alone can establish
- Time: 2026-10-05T09:53:19Z
- Type: Added
- Propagates to:
  - modularity.handoff.md: Done — the question was deleted; the answer is the paragraph added to *Module Identity and Responsibility*
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `### Module Identity and Responsibility` now states that no modularity property is established by modeling alone: what can be checked is whether a part has an independent behavioral boundary and lifecycle, checked by proposing the boundary and observing whether it holds, while coherence, coupling, and whether a boundary was needed at all are judgments stated against a concern, and a tool that measures one of them supplies evidence for that judgment rather than a verdict.
- `modularity.handoff.md` no longer carries "Which modularity properties can be established by modeling alone, and which require implementation or tooling support?" The split the question assumed is not where the line falls: the two paragraphs already cited by that section had decided it, and the section now says so where a reader of it arrives.

#### Considered and not done
- **Answering with a list of which properties fall in each half**: not done, and it is what the question asked for. No passage enumerates the properties and their establishment modes, and the two the record does discuss — independent boundary and lifecycle on one side, coherence and coupling on the other — are already stated as a checkable claim and a stated-concern judgment respectively, so the partition would have been an inventory added to the document rather than a consequence drawn from it.
- **Naming tooling as the deciding instrument for the measurable half**: rejected. The section's own cycle paragraph says the check is made by observing whether the boundary holds, and *When Is a Responsibility Coherent?* says a claim stated against a concern is one evidence can support or contradict; a measurement is evidence for that judgment and not the judgment itself.
- **Closing the handoff's second question, the Module/Framework relationship, with the same section**: not taken. Nothing in System's or Framework's treatment of Framework settles it, and its omission here is deliberate rather than an oversight, as that section states.

---

### The toolchain and the Memar server leave `modules/` for `bundles/`
- Time: 2026-10-07T15:46:42Z
- Type: Changed
- Cited:
  - Bundles (`bundles/README.md`) — `Depends_on`: what a bundle is, the two-question membership test, and what does not belong there
- Propagates to:
  - [modularity.handoff.md](./modularity.handoff.md#the-category-layout-of-this-repository): Done — the top-level-folders item now holds only `modules/go-port/`, and says the question no longer stands for the other two
  - `docs/modules/README.md#one-layout-for-both-trees`: Done — the layout names `bundles/` as outside it, with no counterpart in either tree
  - `modules/README.md#the-kinds-of-folder-here`: Done — the "by language" kind is gone, `memar/` left the "not yet in a category" kind, and what runs or aggregates modules is listed as not belonging
  - `bundles/memar/memar.handoff.md`: Done — its question about its place in the layout is answered under Direction and removed from the open questions
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../../CONTRIBUTORS.md#cursor) — applied

#### What changed
- Owner decision (2026-10-07): a new top-level `bundles/` holds what runs or aggregates modules — servers, executables, toolchains — so that `modules/` holds only reusable modules. `modules/khayyam/` moved to `bundles/khayyam/` and `modules/memar/` to `bundles/memar/`, through git, with untracked contents and every folder moving with them.
- Every reference across the repository was re-pointed: relative links re-derived from each file's old location, repo-rooted mentions in live files, the one `.kh` inclusion address that named `modules/memar/`, and the code and configuration paths (the extension's scripts and manifest, the toolchain's tests and default excludes, `.gitignore`, and the `memar content` corpus, which now includes `bundles/`). In changelogs and research records only links were changed; their prose keeps the paths it recorded.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:12Z
- Type: Changed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the working tree against HEAD for `modularity.md`, `modularity.handoff.md` and this changelog. Every settled question is recorded here and each answer is placed in the document that owns it: eleven handoff questions were removed, and each is covered by the 2026-10-04 and 2026-10-05 entries. The `modularity.md` additions (the Abstract's collision claim, *One Term, One Identity*, the optionality sentence, the cross-boundary ownership sentence, the modeling-alone paragraph, the Rule wording) match their entries. The anchors and quotes they cite were checked, and `memar content check` reports no problem.
- Restored two entries removed from this changelog without a record: the 2026-09-29T13:00:00Z entry on the `modules/storage/` to `modules/memory/` rename, and the 2026-09-29T11:30:00Z entry on the fourteen category-tree questions. A changelog is history, and the 2026-09-29T14:00:00Z entry that follows speaks of "the fourteen" questions with nothing before it to say what they were. Both are verbatim from HEAD, put in time order. The second had lost its heading in HEAD, so the heading `Fourteen `modules/` category-tree questions raised on the handoff` was supplied.
- Restored the handoff question "Can Capability Completeness be checked other than by hypothetical removal?". The 2026-10-04T18:21:13Z entry closed it by pointing at the co-variation test in *Capability Completeness*, which is a judgment made on the material and does not say whether completeness can be checked statically from declared dependencies, which is what the question asked. It stays open until an answer to that is placed.
- `modularity.handoff.md`, first item under *The category layout of this repository*: the sentence said `modules/README.md` and `modules/lib/lib.md` both place the runtime under `computer/runtime/`. Only `lib.md` does; `modules/README.md` lists `runtime/` as a category of its own. Corrected to say so, since that disagreement is part of the question.

#### Considered and not done
- **Editing the 2026-09-29T14:00:00Z entry**, which says the handoff carries concept questions only, now that the handoff holds a layout section. Not done: the section arrived by the owner's ruling recorded in [A folder README carries no changelog and no handoff](../modules/content/documentation/documentation.changelog.md#a-folder-readme-carries-no-changelog-and-no-handoff), history is not rewritten, and the 2026-10-07 entry already links the section. No entry in this changelog records the section's arrival, which is left to the owner.

---

### The `modules/go-port/` question no longer stands, and the handoff's links run down only
- Time: 2026-10-12T11:30:00Z
- Type: Changed
- Cited:
  - [Documentation → Citation Direction](../modules/content/documentation/documentation.md#citation-direction) — `Depends_on`: a base document links to its own layer or a lower one, and names a higher place in plain text
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- Removed from *The category layout of this repository* the entry **The top-level folder that is not a category**. It asked where `modules/go-port/`, the Go port's residue, should sit, since it stood beside the categories with no counterpart under `docs/modules/`. The folder no longer exists: its material became the Go target's research record, `bundles/khayyam/targets/go/target.research.001.md`, whose closing note says the owner ruled the temporary module must never enter version control and that the record retires it; its rule catalog sits at `bundles/khayyam/targets/go/rules/`. With no folder left at the top of `modules/` that is not a category, the question has no subject. The entry's second half — that the same question no longer stood for the language toolchain or the Memar server once the owner's decision of 2026-10-07 moved both to `bundles/` — is recorded by the 2026-10-07T15:46:42Z entry above.
- The handoff's links to `modules/`, `bundles/`, and `docs/modules/` pointed up the layers of the written content; each is now plain text naming the same place, per the rule cited above. Nothing else in the section changed.
- Occasion: the owner noticed that this base document's handoff named `modules/go-port/` — a folder in the code tree that had already moved to an implementation's record — and that a base document was linking above its layer at all.

---

### The one-layout-for-both-trees argument is dropped with the specification folder
- Time: 2026-10-16T00:45:00Z
- Type: Changed
- Cited:
  - Documentation → Citation Direction — `Depends_on`: the layers named there no longer include a specification folder beside the modules
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- `docs/modules/README.md` is merged into `modules/README.md` and `docs/modules/lib/README.md` into `modules/lib/lib.md`; the specification folder `docs/modules/` is gone, because every module's documents now sit beside the module's code. The membership criterion and the account of where implementations live moved into `modules/README.md`.
- The section **One layout for both trees** of the former `docs/modules/README.md` is not carried over. Its argument was that a module specified at `docs/modules/<category>/<name>.md` is realized at `modules/<category>/<name>/`, so that a category was created, renamed, merged or retired in the specification tree first and then in the code tree, and a responsibility had one address in both trees. With the documents beside their modules there is one tree, one address and nothing to reconcile, so the argument has no subject; a category is created, renamed, merged or retired in `modules/` alone.
- Links that named the section (`README.md#one-layout-for-both-trees`) now point at this entry.

#### Considered and not done
- **Keeping the section as a record of the old layout.** Not done: a README states the rule as it now is and keeps no history, and this entry is where the history of the decision lives.

---

### The classification module is dissolved into Modularity and Label; the Modularity document joins its module
- Time: 2026-10-23T12:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- This document and its changelog and handoff moved from `docs/` to `modules/knowledge/modularity/`, the module that now owns the placements. [Placements](./placements.md) and its handoff are the former Classification document and handoff.
- The labels `kernel`, `pluggable`, `bundle` and `guest` stand in `labels/`, and the rules `placement` and `kernel-neutrality` in `rules/`. The category label and the rule for the levels of a category, a category being a label, moved to Label, which also holds the rule that a folder is a label.
- Every link and path naming a moved place was rewritten in one pass.

#### Considered and not done
- **Moving the open questions of the old handoff to the modules they concern.** Not done: they stay in the placements handoff until each is ruled on, and each moves with its ruling.
