# Process Changelog

## Changelog

### Initial draft from Saga and locking discussions
- Time: 2026-08-14T00:00:00Z
- Type: Added
- Cited:
  - [Designing Distributed Systems (Brendan Burns)](https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/) — Reference: distinguishing a lock as a permanent grant from a lease that must be renewed and can silently expire, used to support the concurrency/locking separation.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: brought the two public discussions (Saga/rollback, distributed locking) that seeded this document and framed the process-before-mechanism question that motivates it.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — claimed, argued: produced the initial draft through an extended dialectical session; established the core separations the document is built on (failure from rollback, retry from automatic server-side behavior, concurrency from locking, events from commands to known consumers, asynchrony from `async/await`, observation from the definition of the process); proposed extracting Process out of `system.md` into a standalone document.

#### Summary
Drafted from two public discussions on concurrency and distributed transactions (Saga patterns, distributed locking). Established the document's central claim — that a mechanism (transaction, lock, retry, Saga, event) is not itself the process, and that the process should be understood before a mechanism is selected — and worked it out across failure, retry, cancellation, concurrency, ordering, coordination, events, and asynchrony.

---

### Structural and cross-document review
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - system.md: Done — `### Process` section shortened to a pointer to this document; its Rationale and Alternatives entry updated to record the reversal explicitly instead of silently.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, approved: confirmed the document should exist as a standalone document given how far the scope had grown beyond what `system.md`'s inline section could hold; approved the corresponding update to `system.md`.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: restructured the initial draft into the project's Explanation-facet template; identified that extracting Process into a standalone document reversed a decision `system.md` had already made and recorded ("Define Process as a standalone RFC (rejected)... would create the same circular dependency problem this RFC exists to prevent") without engaging with it; resolved this by making the System↔Process dependency asymmetric rather than symmetric, and by updating `system.md` to match rather than leaving the reversal undocumented; softened an overreaching claim that a process could exist "independently of any particular system boundary," which as originally worded conflicted with `system.md`'s own claim that a process without a system has no scope, boundary, or purpose; added a Prior Art section (absent from the initial draft); flagged the Process ↔ Khayyam Method Type relationship as an open question rather than leaving it unaddressed.

#### Summary
Reorganized the document into the current Explanation-facet template (`Abstract → Introduction → Explanation → Results → Discussion`), migrated per-topic rationale and unresolved questions to sit under their own topics rather than in one flat list, and resolved the standalone-document question by updating `system.md` in the same pass rather than leaving the two documents inconsistent.

#### Rationale and alternatives
Considered leaving `system.md`'s original rejection of a standalone Process RFC in place and merging this content back into `system.md` instead. Rejected once Omid confirmed the scope had genuinely outgrown what an inline subsection could hold without either truncating the analysis or making `system.md` disproportionately large relative to its other topics.

---

### Deep critique round — instance/definition split, intent/purpose, concurrency, events, composition, workflow
- Time: 2026-08-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, approved: pushed back on treating Intent and Purpose as sharply separate concepts, preferring them described as closely related with a difference of expression (implicit vs. articulated) rather than as two competing definitions; confirmed a retry request carries the same intent as the original but is not the same request occurrence, and that the upstream process can remain fully aware of retry counts per sub-part; declined to replace the existing Process↔System paragraph on scope/boundary/purpose, preferring to add ChatGPT's alternative framing as a supplementary paragraph rather than a replacement, since a process still has no meaning entirely apart from at least one system; approved every other change as proposed.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued, reviewed: ran a second, deeper critique pass against the structural-review version above, raising sixteen points across two rounds; after Omid's responses, converged on nine changes it judged necessary: separating Process Definition from Process Instance, refining Intent vs. Purpose, strengthening Concurrency (concurrency ≠ shared state, structural alternatives to locking), strengthening Events (emission ≠ continuation, consumer ≠ sub-process, handler behavior as a property of dispatch rules rather than of Event itself), adding Feedback and Process, adding Process and Workflow, removing the Method (Khayyam) entry from Relationship to Other Concepts as an unnecessary Khayyam-specific dependency, and pruning Unresolved Questions of items already settled by the above; also raised, but did not treat as required, a Process Composition boundary criterion (what makes something a separate sub-process rather than a step of one process) and an explicit Observation↔Instance link.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: verified ChatGPT's own change-summary against the file it actually produced and found three discrepancies — the Continuation and Retry section did not contain the retry-occurrence/upstream-awareness nuance Omid had asked for despite the summary claiming it was added; the Process Composition boundary criterion ChatGPT itself flagged as important was never written in; and the Observation section was never connected to Process Instance or given the observer-relativity clarification, despite the summary claiming both. Added all three properly, in this document's own established prose style rather than as verbatim translations of the chat draft. Separately found that "Relationship to Other Concepts"'s own Unresolved Questions list had become a near-duplicate of items already listed under Definition, State and Transition, and Observation's own Discussion blocks — a leftover from an earlier consolidation pass — and pruned it to the four items genuinely specific to that topic. Added an explicit Unresolved Questions entry under Process and System recording a residual, unresolved tension ChatGPT raised (item 9 of its critique) that neither this round nor the prior structural review addressed: `system.md` still derives System's own existence from Process ("a system without processes is not a system... the interactions — which are processes — are what make the collection a system"), an asymmetry this document does not have in the other direction since it no longer derives Process's meaning from a fixed System boundary; flagged rather than silently resolved, since fixing it would require editing `system.md`, which was out of scope for this pass.

#### Summary
A three-way review round. ChatGPT's critique converged, across two exchanges with Omid, on nine necessary changes and two optional ones; most were applied correctly, but three of the nine that ChatGPT's own summary claimed were done were not actually present in the file, and this pass corrected that gap rather than trusting the summary. Also cleaned up a genuine structural leftover (duplicated Unresolved Questions) and recorded, rather than silently dropped, one substantive cross-document critique that remains genuinely open.

#### Rationale and alternatives
Considered fixing the `system.md` "heap" framing tension in the same pass, to fully close ChatGPT's item 9. Deferred instead, since Omid's instruction for this round was scoped to `process.md`; recorded as an open question here so it is not lost, rather than assuming it can wait indefinitely without a record.

---

### Observation topic rewritten around the modeling/observation cycle; capability/constraint wording aligned with system.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Cited:
  - Merriam-Webster — Reference: definitions of *cohesion*, *cohering*, and *coherence* Omid supplied from his own reference-checking during the LinkedIn discussion that motivated this document's Observation topic, used to ground the terminology precisely rather than relying on the informal sense of "cohesion" already in circulation.
- Propagates to:
  - system.md: Done — new Responsibility section added there and cross-referenced from here in the same pass.
  - modularity.md: Done — Module Identity and Responsibility section now cites this topic instead of asserting "coherent responsibility" independently.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — corrected, argued: corrected a misattribution — the "this module has high cohesion" quote discussed in review is from a LinkedIn post by another author that Omid commented on, not from Omid's own writing; Omid's own position, contrary to what was initially assumed, is that development-time and observation-time ask different questions rather than the same relativized one — development-time asks how to structure something for minimum coupling of any kind, observation-time asks for whom and against which concern an existing boundary holds up; also clarified that modeling and observation are not two strictly separated phases but a cycle, illustrated by `username` first being modeled as a plain field inside `User` and only later, on observation, found to warrant its own Module.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: added "Modeling and Observation Form a Cycle, Not Two Separated Phases" under Observation, incorporating the corrected framing above and the falsifiable/unfalsifiable distinction between a boundary justified against a stated concern and one merely asserted to be cohesive; cross-referenced `system.md`'s new Responsibility section and `modeling.md`'s Domain Decomposition topic; changed "capabilities and limitations" to "capabilities and constraints" in Process and Structure to match the term `system.md`'s own Structure section uses throughout after its opening sentence; updated Relationship to Other Concepts to point the Module bullet at `modularity.md` now that it exists, resolving the placeholder that section had been carrying, and added a System bullet reference to the new Responsibility section.

#### Summary
Reworked Observation to state, rather than only imply, that modeling and observation form a repeating cycle rather than a one-time handoff, and to state the specific, corrected version of the development-time/observation-time distinction Omid actually argued in the source discussion, replacing an earlier internal draft that had it backwards. Aligned "capabilities and limitations" to "capabilities and constraints" to match `system.md`. Resolved two forward-reference placeholders (Module, Responsibility) now that `modularity.md` and `system.md`'s Responsibility section both exist.

#### Rationale and alternatives
Considered leaving the corrected development-time/observation-time distinction as a passing remark rather than its own labeled subsection. Rejected because the distinction had already been gotten wrong once during review, in text headed toward these documents; giving it a named subsection with a citation to the source definitions makes the corrected version the one a future reader actually finds.
