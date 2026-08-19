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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: framed the original problem, drove the discussion through many rounds, supplied the constitutional-law and Invoice/Product/Pricing examples, and rejected several proposed classifications as premature taxonomy.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — drafted: proposed the initial structural questions, drafted the document body and this changelog in an earlier, non-conformant format.

#### Summary
Created the first dedicated Explanation-facet document for Modularity, as Draft. It defines Module as a System considered under a modular boundary, independent of files, directories, packages, repositories, processes, services, containers, or deployment units; grounds Module identity in coherent responsibility and explicit relationships; distinguishes Module from Type, Process, and Protocol; treats Optional Module as a purpose-relative (not intrinsic) distinction; leaves the term Rule intentionally provisional; and treats EventTarget as a capability of an existing Type or Module rather than a separate event data model. It also reframes the Monolith-vs-Microservices comparison as a category error (an observer-boundary effect, not a modularity measure) and treats Big Ball of Mud as architectural degradation rather than a synonym for monolithic deployment.

#### Rationale and alternatives
The document consolidates and generalizes material previously expressed across `modeling.md`, `khayyam-modularity.md`, `process.md`, `protocol.md`, and the project's broader terminology and systems reasoning, rather than leaving Module implicitly defined by its scattered usages.

Several alternatives raised during drafting were deliberately not adopted: a closed taxonomy of Module kinds (Core/Extension/Optional/Infrastructure/Policy Module) was proposed and then withdrawn as premature classification without a settled definition; an Active/Passive Module distinction was proposed and withdrawn once no genuinely passive Module could be identified; and treating Rule as a Module's fixed attribute, versus treating it as a relationship between Modules, was left open rather than forced to a conclusion.

The document is intentionally Draft because terminology around Rule, Optional Module, EventTarget, and the precise formal relationships among Module, System, Structure, Framework, Protocol, Process, and Type remain open.

### Review pass: resolved structural duplication, added a comparison table and prior-art gap
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - modularity.md: Done — this entry documents the change made directly to the paired document in this same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a completeness check against the source discussion and for the changelog to be brought into the project's documentation-changelog format.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: found and merged a duplicated `### Discussion` subsection that had been generated both inside Explanation and again at the document's own top-level `## Discussion`; added a "Module Among Related Concepts" comparison table; added Domain-Driven Design's Core Domain as prior art; added an unresolved question about Module's positioning relative to Framework and Structure.

#### Summary
The earlier ChatGPT-generated draft had produced two separate `## Discussion`-style sections — one nested inside `## Explanation` and one at the document's own end — with overlapping subsection names (`Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities`) but different content in each. These were merged into a single top-level `## Discussion`, with no content dropped. A "Module Among Related Concepts" table was added after the Module/Process/Protocol section to make the boundary between Module, Type, Protocol, Process, Rule, Abstraction, and Encapsulation scannable at a glance, since sharpening exactly this kind of boundary is the document's stated purpose. Domain-Driven Design's Core Domain was added to Prior art, since it is a well-known prior attempt at the same core-vs-satellite distinction and, per the discussion, suffers from treating criticality as intrinsic rather than purpose-relative — the same confusion this document argues against. Finally, an unresolved question was added noting that Module's peer-level relationship to Framework and Structure — raised early in the source discussion but never written into the document itself — is left open rather than asserted.

#### Rationale and alternatives
Writing new content asserting Module's formal relationship to Framework and Structure was considered and rejected for this pass: the project's own convention is to defer structural claims until the underlying design question is settled elsewhere, and Framework's relationship to Module was never resolved in the source discussion. Logging it as an explicit unresolved question was chosen instead, so the gap is visible without prematurely committing the document to an unreviewed position.

---

### Coordination pass with system.md, process.md, and modeling.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Propagates to:
  - system.md: Done — this document now cites the new Responsibility section instead of using "responsibility" informally.
  - process.md: Done — Module, Process, and Protocol shortened to point at process.md's own fuller treatment instead of restating it.
  - modeling.md: Done — added as a cross-reference for the `username`/`User` example illustrating the modeling/observation cycle.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a coordinated pass across `system.md`, `process.md`, `modularity.md`, and `modeling.md` together, so shared concepts have one authoritative home each and every other document references it, rather than each document defining its own version and drifting apart over time.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: replaced "capabilities and limitations" with "capabilities and constraints" throughout (Abstract, Module Identity and Responsibility) to match the term `system.md`'s own Structure section uses; rewrote Module Identity and Responsibility to define a Module's identity via `system.md`'s new Responsibility section rather than an undefined "responsibility"; shortened Module, Process, and Protocol to state only the Module-specific consequence and point at `process.md`'s own, more detailed Process and Boundary and Process Composition topics rather than restating their reasoning independently; added Responsibility and Structure rows to the Module Among Related Concepts table and narrowed the closing note's list of unaddressed peer-level concepts to Framework, now that Structure is addressed; narrowed Unresolved question 10 correspondingly.

#### Summary
This document previously asserted "coherent responsibility" as if self-evident and duplicated `process.md`'s Module/Process boundary reasoning independently. Both are now resolved by citing a single authoritative source instead: Responsibility and its coherence test now live in `system.md`, and the Module/Process boundary argument now lives in `process.md`, with this document keeping only what is specific to Module's own side of each relationship.

---

### Fixed Protocol description to match protocol.md's actual ontology
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - protocol.md: Reference — this fix was found during a conceptual review of protocol.md against this and the other revised documents; see protocol.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a conceptual review of protocol.md against the rest of the now-revised document set.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: corrected "Module, Process, and Protocol" and the "Module Among Related Concepts" table, both of which described Protocol as governing "interactions within or between Systems" — this document's own paraphrase, not protocol.md's actual definition, which routes Protocol through Process (System contains Processes, governed by Protocols) rather than having Protocol govern System-to-System interaction directly. Added a link to protocol.md's "What is a Protocol?" topic.

#### Summary
This document's characterization of Protocol did not match protocol.md's own ontology. Corrected both occurrences (the Module/Process/Protocol topic and the comparison table) to say Protocol governs Processes within a System, rather than System-to-System interaction directly, and linked to protocol.md instead of restating its definition from memory.

---

### Completed Khayyam-specific modularity propagation
- Time: 2026-08-19T00:00:00Z
- Type: Changed
- Propagates to:
  - khayyam-modularity.md: Done — reduced the Khayyam document to language and ecosystem consequences, with this document as the conceptual authority.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: requested the Khayyam modularity document be reconciled with this general document.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote: verified that the general document already contains the authoritative Module definition and that the remaining Khayyam material is language/ecosystem-specific; added the reciprocal link and closed the pending propagation item.

#### Summary
The pending propagation to `khayyam-modularity.md` is complete. The Khayyam document no longer repeats the conceptual definition of Module or Modularity; it links here and retains only its treatment of `in`, explicit naming without package context, and framework-level manifest and dependency resolution.
