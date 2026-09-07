# Process Changelog

## Changelog

### Initial draft from Saga and locking discussions
- Time: 2026-08-14T00:00:00Z
- Type: Added
- Cited:
  - [Designing Distributed Systems (Brendan Burns)](https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/) — Reference: distinguishing a lock as a permanent grant from a lease that must be renewed and can silently expire, used to support the concurrency/locking separation.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — claimed, argued

#### What changed
Drafted from two public discussions on concurrency and distributed transactions (Saga patterns, distributed locking). Established the document's central claim — that a mechanism (transaction, lock, retry, Saga, event) is not itself the process, and that the process should be understood before a mechanism is selected — and worked it out across failure, retry, cancellation, concurrency, ordering, coordination, events, and asynchrony.

Brought the two public discussions (Saga/rollback, distributed locking) that seeded this document and framed the process-before-mechanism question that motivates it. (Omid Hekayati)

Produced the initial draft through an extended dialectical session; established the core separations the document is built on (failure from rollback, retry from automatic server-side behavior, concurrency from locking, events from commands to known consumers, asynchrony from `async/await`, observation from the definition of the process); proposed extracting Process out of `system.md` into a standalone document. (ChatGPT)

---

### Structural and cross-document review
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - system.md: Done — `### Process` section shortened to a pointer to this document; its Rationale and Alternatives entry updated to record the reversal explicitly instead of silently.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, approved
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
Reorganized the document into the current Explanation-facet template (`Abstract → Introduction → Explanation → Results → Discussion`), migrated per-topic rationale and unresolved questions to sit under their own topics rather than in one flat list, and resolved the standalone-document question by updating `system.md` in the same pass rather than leaving the two documents inconsistent.

Confirmed the document should exist as a standalone document given how far the scope had grown beyond what `system.md`'s inline section could hold; approved the corresponding update to `system.md`. (Omid Hekayati)

Restructured the initial draft into the project's Explanation-facet template; identified that extracting Process into a standalone document reversed a decision `system.md` had already made and recorded ("Define Process as a standalone RFC (rejected)... would create the same circular dependency problem this RFC exists to prevent") without engaging with it; resolved this by making the System↔Process dependency asymmetric rather than symmetric, and by updating `system.md` to match rather than leaving the reversal undocumented; softened an overreaching claim that a process could exist "independently of any particular system boundary," which as originally worded conflicted with `system.md`'s own claim that a process without a system has no scope, boundary, or purpose; added a Prior Art section (absent from the initial draft); flagged the Process ↔ Khayyam Method Type relationship as an open question rather than leaving it unaddressed. (Claude)

#### Considered and not done
Considered leaving `system.md`'s original rejection of a standalone Process RFC in place and merging this content back into `system.md` instead. Rejected once Omid confirmed the scope had genuinely outgrown what an inline subsection could hold without either truncating the analysis or making `system.md` disproportionately large relative to its other topics.

---

### Deep critique round — instance/definition split, intent/purpose, concurrency, events, composition, workflow
- Time: 2026-08-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, approved
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued, reviewed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
A three-way review round. ChatGPT's critique converged, across two exchanges with Omid, on nine necessary changes and two optional ones; most were applied correctly, but three of the nine that ChatGPT's own summary claimed were done were not actually present in the file, and this pass corrected that gap rather than trusting the summary. Also cleaned up a genuine structural leftover (duplicated Unresolved Questions) and recorded, rather than silently dropped, one substantive cross-document critique that remains genuinely open.

Pushed back on treating Intent and Purpose as sharply separate concepts, preferring them described as closely related with a difference of expression (implicit vs. articulated) rather than as two competing definitions; confirmed a retry request carries the same intent as the original but is not the same request occurrence, and that the upstream process can remain fully aware of retry counts per sub-part; declined to replace the existing Process↔System paragraph on scope/boundary/purpose, preferring to add ChatGPT's alternative framing as a supplementary paragraph rather than a replacement, since a process still has no meaning entirely apart from at least one system; approved every other change as proposed. (Omid Hekayati)

Ran a second, deeper critique pass against the structural-review version above, raising sixteen points across two rounds; after Omid's responses, converged on nine changes it judged necessary: separating Process Definition from Process Instance, refining Intent vs. Purpose, strengthening Concurrency (concurrency ≠ shared state, structural alternatives to locking), strengthening Events (emission ≠ continuation, consumer ≠ sub-process, handler behavior as a property of dispatch rules rather than of Event itself), adding Feedback and Process, adding Process and Workflow, removing the Method (Khayyam) entry from Relationship to Other Concepts as an unnecessary Khayyam-specific dependency, and pruning Unresolved Questions of items already settled by the above; also raised, but did not treat as required, a Process Composition boundary criterion (what makes something a separate sub-process rather than a step of one process) and an explicit Observation↔Instance link. (ChatGPT)

Verified ChatGPT's own change-summary against the file it actually produced and found three discrepancies — the Continuation and Retry section did not contain the retry-occurrence/upstream-awareness nuance Omid had asked for despite the summary claiming it was added; the Process Composition boundary criterion ChatGPT itself flagged as important was never written in; and the Observation section was never connected to Process Instance or given the observer-relativity clarification, despite the summary claiming both. Added all three properly, in this document's own established prose style rather than as verbatim translations of the chat draft. Separately found that "Relationship to Other Concepts"'s own Unresolved Questions list had become a near-duplicate of items already listed under Definition, State and Transition, and Observation's own Discussion blocks — a leftover from an earlier consolidation pass — and pruned it to the four items genuinely specific to that topic. Added an explicit Unresolved Questions entry under Process and System recording a residual, unresolved tension ChatGPT raised (item 9 of its critique) that neither this round nor the prior structural review addressed: `system.md` still derives System's own existence from Process ("a system without processes is not a system... the interactions — which are processes — are what make the collection a system"), an asymmetry this document does not have in the other direction since it no longer derives Process's meaning from a fixed System boundary; flagged rather than silently resolved, since fixing it would require editing `system.md`, which was out of scope for this pass. (Claude)

#### Considered and not done
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — corrected, argued
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
Reworked Observation to state, rather than only imply, that modeling and observation form a repeating cycle rather than a one-time handoff, and to state the specific, corrected version of the development-time/observation-time distinction Omid actually argued in the source discussion, replacing an earlier internal draft that had it backwards. Aligned "capabilities and limitations" to "capabilities and constraints" to match `system.md`. Resolved two forward-reference placeholders (Module, Responsibility) now that `modularity.md` and `system.md`'s Responsibility section both exist.

Corrected a misattribution — the "this module has high cohesion" quote discussed in review is from a LinkedIn post by another author that Omid commented on, not from Omid's own writing; Omid's own position, contrary to what was initially assumed, is that development-time and observation-time ask different questions rather than the same relativized one — development-time asks how to structure something for minimum coupling of any kind, observation-time asks for whom and against which concern an existing boundary holds up; also clarified that modeling and observation are not two strictly separated phases but a cycle, illustrated by `username` first being modeled as a plain field inside `User` and only later, on observation, found to warrant its own Module. (Omid Hekayati)

Added "Modeling and Observation Form a Cycle, Not Two Separated Phases" under Observation, incorporating the corrected framing above and the falsifiable/unfalsifiable distinction between a boundary justified against a stated concern and one merely asserted to be cohesive; cross-referenced `system.md`'s new Responsibility section and `modeling.md`'s Domain Decomposition topic; changed "capabilities and limitations" to "capabilities and constraints" in Process and Structure to match the term `system.md`'s own Structure section uses throughout after its opening sentence; updated Relationship to Other Concepts to point the Module bullet at `modularity.md` now that it exists, resolving the placeholder that section had been carrying, and added a System bullet reference to the new Responsibility section. (Claude)

#### Considered and not done
Considered leaving the corrected development-time/observation-time distinction as a passing remark rather than its own labeled subsection. Rejected because the distinction had already been gotten wrong once during review, in text headed toward these documents; giving it a named subsection with a citation to the source definitions makes the corrected version the one a future reader actually finds.

---

### Concurrency: added the escalating decision chain the source discussion had agreed on but never actually written in
- Time: 2026-08-16T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
The Concurrency topic already contained the core conclusion (concurrency does not imply shared state; a process can sometimes be redesigned by partitioning ownership or responsibility instead of adding a lock) but not the explicit step-by-step chain that motivated it, which had been proposed and agreed in the source discussion. Added the chain as a code block immediately following the existing prose, changing nothing about the existing conclusions.

On rereading, found the Concurrency topic too thin relative to how much ground the source discussion had actually covered, and specifically asked for the concurrency-vs-parallelism disambiguation from a separate LinkedIn disagreement he had — that disambiguation is not yet added; see Unresolved questions. (Omid Hekayati)

Checked the topic against the full source transcript and found the escalating question chain (shared state → shared mutable state → shared invariant → common ownership → partitionable responsibility → scheduling → synchronization → locking, each step skipped if an earlier one already resolves the concern) had been explicitly proposed and agreed on in the source discussion but was never actually written into the document — only the prose conclusion (the account/ownership/scheduling paragraph) had made it in, not the chain itself. Added it as an explicit block. Did not add a Concurrency-vs-Parallelism comparison, since it does not appear anywhere in the transcript provided for this document and inventing the distinction risked repeating an earlier misattribution error in this same review; logged as an unresolved question requesting the source material instead. (Claude)

#### Considered and not done
Considered writing a Concurrency-vs-Parallelism comparison from general knowledge of the two terms, since the request specifically named it. Rejected: this document's own standard is to ground claims in the actual source discussion rather than plausible-sounding first-principles reasoning, and a previous entry in this changelog already recorded one instance of getting Omid's actual position backwards by guessing instead of checking the source text. Requesting the source material is slower but avoids repeating that mistake on a topic connected to a real disagreement with a third party.

---

### Concurrency treated as a single concept, without a separate Parallelism term
- Time: 2026-08-16T00:00:00Z
- Type: Added
- Cited:
  - [Omid's LinkedIn comment](https://www.linkedin.com/feed/update/urn:li:activity:7493294839263051777/?dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287493323440364531712%2Curn%3Ali%3Aactivity%3A7493294839263051777%29) — Reference: the source disagreement this addition is grounded in; requires LinkedIn authentication and could not be fetched directly, so this document relies on Omid's own paraphrase of it rather than the primary text.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, claimed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
Concurrency and Parallelism are not treated as two concepts in this document. The class of hazard usually attributed only to multi-core execution — two activities corrupting shared state because each assumes it is the only one acting on it — occurs identically on a single core whenever activities can interleave, so splitting the two terms hides rather than clarifies the hazard. What does vary is how many Workers a process's activities are distributed across and how those Workers relate to physical cores; that relationship, including deliberately pinning work to a fixed Worker, is a modeling decision available regardless of core count. Go's scheduler is used as a concrete illustration of a mechanism that is pleasant to use without thereby proving the underlying concurrency has been modeled.

Proposed not using "Parallelism" as a separate concept at all, treating it as the same kind of unsuccessful ecosystem coinage as the object-oriented sense of *inheritance*; supplied the goroutine example — two goroutines sharing a variable, one yielding mid-operation to the other, corrupting shared state without ever needing a second CPU core — as evidence that the hazard usually filed under "Parallelism" is really just Concurrency, present on a single core; distinguished Worker (a logical execution unit the model can register and identify) from CPU core (a physical resource assigned by the OS or runtime), and named worker-pinning as a modeling-time decision that can resolve a concurrency hazard without a lock; characterized Go's goroutine scheduler as imposing needless queuing and locking cost without an abstraction layer to hide it, while acknowledging its popularity and ease of use. (Omid Hekayati)

Added "This Document Treats Concurrency as One Concept, Not Two" under Concurrency, incorporating the goroutine example, the Worker/CPU-core distinction, and the Go scheduler illustration; corrected the Common Modeling Errors bullet and resolved the corresponding Unresolved question, folding the remaining open piece (a formal Worker/core identity model) into the existing scheduling question. (Claude)

---

### Agency-driven execution responsibility and concurrency
- Time: 2026-08-17
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — integrated

#### What changed
Added `Agency and Execution Responsibility` to make explicit that Process may involve many execution Agents whose set can change without changing the conceptual Process. Added dynamic responsibility assignment, partitioning, rebalancing, Consistent Hashing as an example mechanism, responsibility-before-synchronization reasoning, domain-state versus execution-ownership distinction, and Worker/Actor as implementation representations. Existing Concurrency guidance was strengthened to state explicitly that assigning an Execution Agent to an account or partition does not make that Agent the permanent domain owner and does not require an Account Service to own all progression.

Clarified that Process execution may be distributed among many Agents independently of domain-entity boundaries; emphasized dynamic responsibility assignment and the distinction between execution ownership and domain ownership. (Omid Hekayati)

Integrated the resulting model into `process.md`. (ChatGPT)

#### Considered and not done
The new treatment deliberately starts from Process, state, invariants, responsibility, and partitioning before synchronization. Worker, Actor, Lock, Queue, Scheduler, and Consistent Hashing remain implementation mechanisms rather than definitions of Process or Concurrency.

---

### Trimmed Agency and Execution Responsibility, closing the duplication with agency.md
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Propagates to:
  - agency.md: Done — reciprocal links and a Process entry in its "Relation to Memar" diagram were added there in the same pass; see agency.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote, corrected

#### What changed
The previous entry's "Agency and Execution Responsibility" topic, agency.md's own "Agency in Process Execution" topic, and Concurrency's own prose were independently saying the same thing three times within two documents. Reduced to one authoritative copy in agency.md, with this document keeping only short pointers and the residue specific to Process. No conceptual content was changed — only where each piece of it lives.

Pointed out that an earlier pass had mistakenly applied edits to a stale copy of this document, discarding the "Agency and Execution Responsibility" topic ChatGPT had just added; asked for the edits to be redone against the actual latest version instead. (Omid Hekayati)

Re-based this pass on the actual latest process.md and process.changelog.md rather than a stale local copy. Found that "Agency and Execution Responsibility" (added by the prior entry) substantially duplicated agency.md's own "Agency in Process Execution" topic — same Account/Agent example, same Consistent Hashing diagram, same responsibility-before-synchronization chain, same Worker/Actor-as-representation argument — and that Concurrency's own paragraph re-walked through the same Account/Agent example a third time. Shrank "Agency and Execution Responsibility" to a pointer at agency.md plus only the Process-specific residue; trimmed Concurrency's redundant paragraph to a one-line pointer at the (now-shrunk) topic above; trimmed the three Agency-related Common Modeling Errors bullets to shorter versions pointing at Agency's own fuller catalog; renamed the oddly-named "#### Others" heading under Concurrency to "Go's Scheduler as an Illustration"; re-added the link from Concurrency's Worker/CPU-core paragraph to [Agency → Execution Agent](./agency.md#execution-agent) that had been lost when the prior pass was accidentally based on a stale file. Left the existing Agency bullet under Relationship to Other Concepts and the existing scheduling Unresolved question as ChatGPT had written them, since both were already accurate and did not need correction. (Claude)

#### Considered and not done
Considered keeping the full walkthrough in this document as well, on the grounds that a reader of process.md's Concurrency topic shouldn't have to leave the document to see a concrete example. Rejected: the example is identical to agency.md's, and keeping two full copies is exactly the drift risk this project's review has been working against — a future edit to one copy (e.g. renaming Consistent Hashing's role, or changing the Account/Agent example) would silently leave the other stale. A pointer costs the reader one click; a second full copy costs the project a second maintenance burden.

---

### Requests, Cancellation, and Timeout — the context critique folded into Process
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Propagates to:
  - protocols/sRPC.md: Done — Open Questions section added there in the same pass, asking for the wire-level cancellation contract and pointing back here.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) — reviewed, argued, rewrote

#### What changed
Added the *Requests, Cancellation, and Timeout* topic: the request-scoped context mechanism (Go `context` and its C#/JS/Python equivalents) examined in the three roles it is commonly cast in — process identity, cancellation/deadline carrier, cross-layer data channel — and each rejected on process-model grounds: cancellation validity and timeout budgets are properties of the executing module, data carriage past intermediate layers is a layering violation that hides missing access. Added two Common Modeling Errors bullets covering the same ground as modeling-time warnings. Kept in this document rather than a new protocol document, with the path to a future protocol treatment recorded under the topic's Rationale.

The `context` critique was brought from years of public developer-community discussions (Go Engineers, gopherconf.ir, Gommunity): a request cannot be expected to cancel cleanly from outside the body executing it; per-request deadlines presume a global property no single layer owns; and threading data between layers through the context conceals missing legitimate access (e.g. to a network socket) instead of exposing a broken API. Position stated: timeout is an internal budget of the executing mechanism — like a cache TTL — configurable once from outside, not re-declared per request; cancellation validity belongs to the executing module's state machine, the external party only requests it. Also chose the document's home: folding the topic into process.md rather than a new request-lifecycle protocol document, and asked that the treatment stay language-general with Go as one illustration among several (Omid Hekayati).

The topic was proposed as a standalone protocol document first, and the counter-position advanced that cancellation is genuinely achievable at cooperative boundaries (checkpoints), so the objection is to unaccounted-for guarantees rather than to cancellation itself; the counter-position's force was recorded while accepting Omid's direction that the guarantee must be purchased by the module's own design, not declared by a context value. After Omid's rejection of the separate document, the critique was reworked into process.md's established structure (Common Modeling Errors bullets, topic with Rationale/Unresolved questions) in the document's own prose style; the topic was verified against the source discussion excerpts before writing (Super Z).

#### Considered and not done
Considered a standalone `request-lifecycle.md` under docs/protocols. Rejected: the protocols directory's membership criterion requires a document to specify a protocol, and the critique — however sharp — does not yet specify one; forcing it there would have produced a position paper wearing a protocol document's clothes. Recorded instead with the explicit conditions under which the topic graduates into a protocol document (a request-scope contract, a wire-level cancellation shape for sRPC). (Super Z - proposed; Omid Hekayati - rejected)

---

### Provenance stripped; Prior art / Unresolved questions relocated per the documentation-method revision
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - process.handoff.md: Created — all seven topic-level unresolved-question lists and the document-level pointer moved there, organized by topic.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

#### What changed
The document-level Prior art's premise evidence (Whitehead's process philosophy and CSP/π-calculus as the lineage of process-distinct-from-sequence; Burns's lock-versus-lease distinction as the direct basis of the distributed-systems argument) was folded into the Definition topic's Rationale entry it supports; its comparative residue (BPM/workflow literature positioning, the note that the lock/lease discussion referenced a public exchange) lives in this entry. The document-level Unresolved-questions pointer section was removed; its role is superseded by the handoff.

The body was reduced to wrapping only Drawbacks, Rationale and alternatives, and Future possibilities at every level; open questions live in the paired handoff; premise evidence stays with the claims it supports.

---

### Documentation-method migration completed: Discussion wrappers, Drawbacks, and Future possibilities dissolved
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - process.handoff.md: Done - the anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Omid Hekayati - decided; Super Z - applied).
- The remaining `#### Discussion` wrappers dissolved: the Definition topic's rejected-alternative entry moved to this entry's `Considered and not done` (its process-philosophy/CSP lineage sentence stays inline as premise evidence at the no-sequence definition claim); the Process and System topic's rejected-alternative entries moved to this entry's `Considered and not done`; the empty wrappers under Process Composition and Relationship to Other Concepts removed (Super Z).
- The document-level `## Discussion` dissolved: `Drawbacks` content to this entry's `Considered and not done`; the pointer-style `Rationale and alternatives` retired (its targets are recorded in the entries below); `Future possibilities` to the paired handoff's `Anticipated Work` (Super Z).

Applied the finalized documentation method to this document. (Omid Hekayati)

Dissolved the remaining `#### Discussion` wrappers (Definition, Process and System, Process Composition, Relationship to Other Concepts) and the document-level `## Discussion`; folded the two rejected-alternative entries (strict-sequence rejection; the system.md inline-definition supersession and the Protocol sub-concept rejection) into their topics' bodies as stated rejections with their reasoning, per the finalized method's rule that premise evidence and stated rejections stay inline; moved the document-level Drawbacks and Future possibilities content below, without loss. (Super Z)

#### Considered and not done
- **Requiring Process to be a strict sequence (rejected; migrated from the Definition topic's retired `Rationale and alternatives`)**: `system.md`'s prior definition called Process "an organized sequence of activities or interactions." This document deliberately drops "sequence," because sequence is one possible shape a process can take, not a defining property — treating it as defining would make concurrent, event-driven, and independently-progressing processes look like deviations from the "real" definition rather than the ordinary cases they are. (Omid Hekayati)
- **Keep Process defined inline in `system.md` (formerly the settled position; now superseded; migrated from the Process and System topic's retired `Rationale and alternatives`)**: `system.md` previously rejected a standalone Process document with a specific argument: "Process cannot be defined without reference to System. A standalone Process document would either duplicate System's definition or silently depend on it, creating the same circular dependency problem this document exists to prevent." That argument is correct about *symmetric* duplication, but this document resolves it by making the dependency asymmetric and one-directional instead: `system.md` defines System and keeps only the System-specific half of the Process↔System relationship; this document defines Process in full, including the Process-specific half of that same relationship. Neither document re-derives the other's core definition. As of that revision, `system.md` has been updated accordingly — its own `### Process` section is now a short pointer here, and its Rationale and Alternatives entry now records this reversal explicitly rather than silently.
- **Define Process as a sub-concept under Protocol (rejected, inherited from `system.md`; migrated from the Process and System topic's retired `Rationale and alternatives`)**: Protocol governs processes, but Process is not a sub-concept of Protocol — processes exist whether or not they are governed by protocols, and Process is a foundational concept that Protocol depends on, not the reverse. `protocol.md`'s own chain — "System → contains → Processes → governed by → Protocols" — is consistent with this document as long as "contains" is read as "provides context for" rather than "cannot exist independent of any system," which is the reading this document adopts above.
- **Grounding the Requests/Cancellation examples in Go only (rejected; migrated from the topic's inline considered-and-rejected paragraph)**: the examined mechanism family is not Go-specific — C#, JavaScript, and Python have adopted equivalents with the same three roles and the same costs, so the analysis is recorded generally with the languages as illustrations, consistent with how Go's Scheduler as an Illustration is used under Concurrency.

#### Considered and not done (from the removed document-level Drawbacks section)
- **This document is large, covering a number of adjacent concepts (Concurrency, Coordination, Events, Asynchrony) that could each eventually justify their own document** — a known and accepted risk from the outset. (Omid Hekayati)
- **Extracting Process into its own document reintroduces the drift risk `system.md`'s original Rationale and Alternatives warned about: two documents now each describe the Process↔System relationship from their own side, and each future change to either concept needs a corresponding check against the other** — accepted, and tracked as the Process-and-System open question in the paired handoff. (Omid Hekayati)
