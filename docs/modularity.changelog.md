# Modularity Changelog

## Changelog

### Initial draft consolidating Module and Modularity
- Time: 2026-08-15T18:40:39Z (approximate — taken from the source chat log; adjust if this was not UTC)
- Type: Added
- Cited:
  - [Big Ball of Mud](https://www.laputan.org/mud/) — Evidence: used as prior art to argue that architectural degradation is a loss of coherent structure and controlled relationships, not a property of monolithic deployment specifically.
- Propagates to:
  - modeling.md: Pending — should eventually reduce its local Module-related reasoning (e.g. "Extensible Behavior Belongs to Pluggable Modules") and reference this document instead.
  - khayyam-modularity.md: Pending — should retain only the language/ecosystem-layer consequences of modularity and reference this document for the conceptual definition.
  - process.md: Pending — should reference this document for the Module/Process boundary distinction instead of restating it locally.
  - protocol.md: Pending — should reference this document for the Module/Protocol boundary distinction instead of restating it locally.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — drafted

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed.
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — applied.
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- "Conceptual Relationships Are Not Runtime Coupling" no longer hyperlinks Modularity in Khayyam: language-level cycle restrictions belong to the language layer, and each language's own modularity document records them — named in prose, not cited upward via hyperlink.
- The closing section's pointer to the Khayyam modularity treatment is now the plain phrase "the language's own modularity document"; the application that document records is still named, only not linked.

#### Deliberation
- Citation direction rule: a base document never links into `khayyam/` — not even as an instance pointer; plain-text naming only (Omid Hekayati — decided).
