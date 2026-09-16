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
- Drafted from two public discussions on concurrency and distributed transactions (Saga patterns, distributed locking).
- Established the document's central claim — that a mechanism (transaction, lock, retry, Saga, event) is not itself the process, and that the process should be understood before a mechanism is selected — and worked it out across failure, retry, cancellation, concurrency, ordering, coordination, events, and asynchrony.
- The initial draft was produced through an extended dialectical session (ChatGPT).
- The core separations the document is built on were established: failure from rollback, retry from automatic server-side behavior, concurrency from locking, events from commands to known consumers, asynchrony from `async/await`, observation from the definition of the process (ChatGPT).

#### Deliberation
- The two public discussions (Saga/rollback, distributed locking) that seeded this document were brought, and the process-before-mechanism question that motivates it was framed (Omid Hekayati).
- Extracting Process out of `system.md` into a standalone document was proposed (ChatGPT).

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
- The document was reorganized into the current Explanation-facet template (`Abstract → Introduction → Explanation → Results → Discussion`) (Claude).
- Per-topic rationale and unresolved questions were migrated to sit under their own topics rather than in one flat list.
- The standalone-document question was resolved by updating `system.md` in the same pass rather than leaving the two documents inconsistent, making the System↔Process dependency asymmetric rather than symmetric (Claude).
- An overreaching claim that a process could exist "independently of any particular system boundary" was softened; as originally worded it conflicted with `system.md`'s own claim that a process without a system has no scope, boundary, or purpose (Claude).
- A Prior Art section was added (absent from the initial draft) (Claude).
- The Process ↔ Khayyam Method Type relationship was flagged as an open question rather than left unaddressed (Claude).

#### Deliberation
- Extracting Process into a standalone document was identified as reversing a decision `system.md` had already made and recorded ("Define Process as a standalone RFC (rejected)... would create the same circular dependency problem this RFC exists to prevent") without engaging with it; the resolution chosen was to make the System↔Process dependency asymmetric rather than symmetric, and to update `system.md` to match rather than leave the reversal undocumented (Claude).
- The document was confirmed to exist as a standalone document given how far the scope had grown beyond what `system.md`'s inline section could hold, and the corresponding update to `system.md` was approved (Omid Hekayati).

#### Considered and not done
- Leaving `system.md`'s original rejection of a standalone Process RFC in place and merging this content back into `system.md` instead (rejected): rejected once Omid confirmed the scope had genuinely outgrown what an inline subsection could hold without either truncating the analysis or making `system.md` disproportionately large relative to its other topics.

---

### Deep critique round — instance/definition split, intent/purpose, concurrency, events, composition, workflow
- Time: 2026-08-15T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, approved
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued, reviewed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- A three-way review round was applied to the document.
- The nine changes ChatGPT's critique converged on were applied; most were applied correctly, but three of the nine that ChatGPT's own summary claimed were done were not actually present in the file — the retry-occurrence/upstream-awareness nuance in the Continuation and Retry section, the Process Composition boundary criterion, and the Observation section's connection to Process Instance with the observer-relativity clarification — and this pass corrected that gap rather than trusting the summary, adding all three properly, in this document's own established prose style rather than as verbatim translations of the chat draft (Claude).
- A genuine structural leftover was cleaned up: "Relationship to Other Concepts"'s own Unresolved Questions list, a near-duplicate of items already listed under Definition, State and Transition, and Observation's own Discussion blocks — a leftover from an earlier consolidation pass — was pruned to the four items genuinely specific to that topic (Claude).
- One substantive cross-document critique that remains genuinely open was recorded rather than silently dropped: an explicit Unresolved Questions entry was added under Process and System recording the residual tension ChatGPT raised (item 9 of its critique), flagged rather than silently resolved, since fixing it would require editing `system.md`, which was out of scope for this pass (Claude).

#### Deliberation
- A second, deeper critique pass was run against the structural-review version, raising sixteen points across two rounds (ChatGPT).
- Treating Intent and Purpose as sharply separate concepts was pushed back on, preferring them described as closely related with a difference of expression (implicit vs. articulated) rather than as two competing definitions (Omid Hekayati).
- It was confirmed that a retry request carries the same intent as the original but is not the same request occurrence, and that the upstream process can remain fully aware of retry counts per sub-part (Omid Hekayati).
- Replacing the existing Process↔System paragraph on scope/boundary/purpose was declined, preferring to add ChatGPT's alternative framing as a supplementary paragraph rather than a replacement, since a process still has no meaning entirely apart from at least one system (Omid Hekayati).
- Every other change was approved as proposed (Omid Hekayati).
- After Omid's responses, ChatGPT's critique converged, across two exchanges with Omid, on nine changes it judged necessary — separating Process Definition from Process Instance, refining Intent vs. Purpose, strengthening Concurrency (concurrency ≠ shared state, structural alternatives to locking), strengthening Events (emission ≠ continuation, consumer ≠ sub-process, handler behavior as a property of dispatch rules rather than of Event itself), adding Feedback and Process, adding Process and Workflow, removing the Method (Khayyam) entry from Relationship to Other Concepts as an unnecessary Khayyam-specific dependency, and pruning Unresolved Questions of items already settled by the above — and raised, but did not treat as required, two optional ones: a Process Composition boundary criterion (what makes something a separate sub-process rather than a step of one process) and an explicit Observation↔Instance link (ChatGPT).
- A residual, unresolved tension was raised (item 9 of the critique) that neither this round nor the prior structural review addressed: `system.md` still derives System's own existence from Process ("a system without processes is not a system... the interactions — which are processes — are what make the collection a system"), an asymmetry this document does not have in the other direction since it no longer derives Process's meaning from a fixed System boundary (ChatGPT).
- ChatGPT's own change-summary was verified against the file it actually produced, and three discrepancies were found — the Continuation and Retry section did not contain the retry-occurrence/upstream-awareness nuance Omid had asked for despite the summary claiming it was added; the Process Composition boundary criterion ChatGPT itself flagged as important was never written in; and the Observation section was never connected to Process Instance or given the observer-relativity clarification, despite the summary claiming both (Claude).

#### Considered and not done
- Fixing the `system.md` "heap" framing tension in the same pass, to fully close ChatGPT's item 9 (deferred): Omid's instruction for this round was scoped to `process.md`; recorded as an open question here so it is not lost, rather than assuming it can wait indefinitely without a record.

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
- Observation was reworked to state, rather than only imply, that modeling and observation form a repeating cycle rather than a one-time handoff, and to state the specific, corrected version of the development-time/observation-time distinction Omid actually argued in the source discussion, replacing an earlier internal draft that had it backwards (Claude).
- "Modeling and Observation Form a Cycle, Not Two Separated Phases" was added under Observation, incorporating the corrected framing and the falsifiable/unfalsifiable distinction between a boundary justified against a stated concern and one merely asserted to be cohesive (Claude).
- `system.md`'s new Responsibility section and `modeling.md`'s Domain Decomposition topic were cross-referenced (Claude).
- "capabilities and limitations" was aligned to "capabilities and constraints" in Process and Structure, to match the term `system.md`'s own Structure section uses throughout after its opening sentence (Claude).
- The two forward-reference placeholders (Module, Responsibility) were resolved now that `modularity.md` and `system.md`'s Responsibility section both exist: Relationship to Other Concepts points the Module bullet at `modularity.md`, resolving the placeholder that section had been carrying, and a System bullet reference to the new Responsibility section was added (Claude).

#### Deliberation
- A misattribution was corrected: the "this module has high cohesion" quote discussed in review is from a LinkedIn post by another author that Omid commented on, not from Omid's own writing (Omid Hekayati).
- Omid's own position, contrary to what was initially assumed, is that development-time and observation-time ask different questions rather than the same relativized one — development-time asks how to structure something for minimum coupling of any kind, observation-time asks for whom and against which concern an existing boundary holds up (Omid Hekayati).
- It was clarified that modeling and observation are not two strictly separated phases but a cycle, illustrated by `username` first being modeled as a plain field inside `User` and only later, on observation, found to warrant its own Module (Omid Hekayati).

#### Considered and not done
- Leaving the corrected development-time/observation-time distinction as a passing remark rather than its own labeled subsection (rejected): the distinction had already been gotten wrong once during review, in text headed toward these documents; giving it a named subsection with a citation to the source definitions makes the corrected version the one a future reader actually finds.

---

### Concurrency: added the escalating decision chain the source discussion had agreed on but never actually written in
- Time: 2026-08-16T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The Concurrency topic already contained the core conclusion (concurrency does not imply shared state; a process can sometimes be redesigned by partitioning ownership or responsibility instead of adding a lock); the explicit step-by-step chain that motivated it was added as a code block immediately following the existing prose — shared state → shared mutable state → shared invariant → common ownership → partitionable responsibility → scheduling → synchronization → locking, each step skipped if an earlier one already resolves the concern — changing nothing about the existing conclusions (Claude).
- An unresolved question requesting the source material for the concurrency-vs-parallelism disambiguation was logged; that disambiguation is not yet added (Claude).

#### Deliberation
- On rereading, the Concurrency topic was found too thin relative to how much ground the source discussion had actually covered, and the concurrency-vs-parallelism disambiguation from a separate LinkedIn disagreement was specifically asked for (Omid Hekayati).
- A check of the topic against the full source transcript found the escalating question chain had been explicitly proposed and agreed on in the source discussion but was never actually written into the document — only the prose conclusion (the account/ownership/scheduling paragraph) had made it in, not the chain itself (Claude).
- A Concurrency-vs-Parallelism comparison was not added, since it does not appear anywhere in the transcript provided for this document and inventing the distinction risked repeating an earlier misattribution error in this same review (Claude).

#### Considered and not done
- Writing a Concurrency-vs-Parallelism comparison from general knowledge of the two terms, since the request specifically named it (rejected): this document's own standard is to ground claims in the actual source discussion rather than plausible-sounding first-principles reasoning, and a previous entry in this changelog already recorded one instance of getting Omid's actual position backwards by guessing instead of checking the source text. Requesting the source material is slower but avoids repeating that mistake on a topic connected to a real disagreement with a third party.

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
- Concurrency and Parallelism are not treated as two concepts in this document. The class of hazard usually attributed only to multi-core execution — two activities corrupting shared state because each assumes it is the only one acting on it — occurs identically on a single core whenever activities can interleave, so splitting the two terms hides rather than clarifies the hazard. What does vary is how many Workers a process's activities are distributed across and how those Workers relate to physical cores; that relationship, including deliberately pinning work to a fixed Worker, is a modeling decision available regardless of core count. Go's scheduler is used as a concrete illustration of a mechanism that is pleasant to use without thereby proving the underlying concurrency has been modeled.
- "This Document Treats Concurrency as One Concept, Not Two" was added under Concurrency, incorporating the goroutine example, the Worker/CPU-core distinction, and the Go scheduler illustration (Claude).
- The Common Modeling Errors bullet was corrected and the corresponding Unresolved question resolved, folding the remaining open piece (a formal Worker/core identity model) into the existing scheduling question (Claude).

#### Deliberation
- Not using "Parallelism" as a separate concept at all was proposed, treating it as the same kind of unsuccessful ecosystem coinage as the object-oriented sense of *inheritance* (Omid Hekayati).
- The goroutine example was supplied — two goroutines sharing a variable, one yielding mid-operation to the other, corrupting shared state without ever needing a second CPU core — as evidence that the hazard usually filed under "Parallelism" is really just Concurrency, present on a single core (Omid Hekayati).
- Worker (a logical execution unit the model can register and identify) was distinguished from CPU core (a physical resource assigned by the OS or runtime), and worker-pinning was named as a modeling-time decision that can resolve a concurrency hazard without a lock (Omid Hekayati).
- Go's goroutine scheduler was characterized as imposing needless queuing and locking cost without an abstraction layer to hide it, while acknowledging its popularity and ease of use (Omid Hekayati).

---

### Agency-driven execution responsibility and concurrency
- Time: 2026-08-17
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — integrated

#### What changed
- `Agency and Execution Responsibility` was added to make explicit that Process may involve many execution Agents whose set can change without changing the conceptual Process (Omid Hekayati — clarified that Process execution may be distributed among many Agents independently of domain-entity boundaries; ChatGPT — integrated the resulting model into `process.md`).
- The topic added dynamic responsibility assignment, partitioning, rebalancing, Consistent Hashing as an example mechanism, responsibility-before-synchronization reasoning, domain-state versus execution-ownership distinction, and Worker/Actor as implementation representations (Omid Hekayati — emphasized dynamic responsibility assignment and the distinction between execution ownership and domain ownership; ChatGPT — integrated).
- Existing Concurrency guidance was strengthened to state explicitly that assigning an Execution Agent to an account or partition does not make that Agent the permanent domain owner and does not require an Account Service to own all progression.

#### Considered and not done
- The new treatment deliberately starts from Process, state, invariants, responsibility, and partitioning before synchronization. Worker, Actor, Lock, Queue, Scheduler, and Consistent Hashing remain implementation mechanisms rather than definitions of Process or Concurrency.

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
- The previous entry's "Agency and Execution Responsibility" topic, agency.md's own "Agency in Process Execution" topic, and Concurrency's own prose were independently saying the same thing three times within two documents; the content was reduced to one authoritative copy in agency.md, with this document keeping only short pointers and the residue specific to Process. No conceptual content was changed — only where each piece of it lives.
- "Agency and Execution Responsibility" was shrunk to a pointer at agency.md plus only the Process-specific residue; Concurrency's redundant paragraph was trimmed to a one-line pointer at the (now-shrunk) topic above; the three Agency-related Common Modeling Errors bullets were trimmed to shorter versions pointing at Agency's own fuller catalog (Claude).
- The oddly-named "#### Others" heading under Concurrency was renamed to "Go's Scheduler as an Illustration" (Claude).
- The link from Concurrency's Worker/CPU-core paragraph to [Agency → Execution Agent](./agency.md#execution-agent), lost when the prior pass was accidentally based on a stale file, was re-added (Claude).
- The existing Agency bullet under Relationship to Other Concepts and the existing scheduling Unresolved question were left as ChatGPT had written them, since both were already accurate and did not need correction (Claude).

#### Deliberation
- An earlier pass was pointed out to have mistakenly applied edits to a stale copy of this document, discarding the "Agency and Execution Responsibility" topic ChatGPT had just added; the edits were asked to be redone against the actual latest version instead (Omid Hekayati).
- The pass was re-based on the actual latest process.md and process.changelog.md rather than a stale local copy (Claude).
- It was found that "Agency and Execution Responsibility" (added by the prior entry) substantially duplicated agency.md's own "Agency in Process Execution" topic — same Account/Agent example, same Consistent Hashing diagram, same responsibility-before-synchronization chain, same Worker/Actor-as-representation argument — and that Concurrency's own paragraph re-walked through the same Account/Agent example a third time (Claude).

#### Considered and not done
- Keeping the full walkthrough in this document as well, on the grounds that a reader of process.md's Concurrency topic shouldn't have to leave the document to see a concrete example (rejected): the example is identical to agency.md's, and keeping two full copies is exactly the drift risk this project's review has been working against — a future edit to one copy (e.g. renaming Consistent Hashing's role, or changing the Account/Agent example) would silently leave the other stale. A pointer costs the reader one click; a second full copy costs the project a second maintenance burden.

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
- The *Requests, Cancellation, and Timeout* topic was added: the request-scoped context mechanism (Go `context` and its C#/JS/Python equivalents) examined in the three roles it is commonly cast in — process identity, cancellation/deadline carrier, cross-layer data channel — and each rejected on process-model grounds: cancellation validity and timeout budgets are properties of the executing module, data carriage past intermediate layers is a layering violation that hides missing access.
- Two Common Modeling Errors bullets were added covering the same ground as modeling-time warnings.
- The topic was kept in this document rather than a new protocol document, with the path to a future protocol treatment recorded under the topic's Rationale.
- The critique was reworked into process.md's established structure (Common Modeling Errors bullets, topic with Rationale/Unresolved questions) in the document's own prose style, and the topic was verified against the source discussion excerpts before writing (Super Z).

#### Deliberation
- The `context` critique was brought from years of public developer-community discussions (Go Engineers, gopherconf.ir, Gommunity): a request cannot be expected to cancel cleanly from outside the body executing it; per-request deadlines presume a global property no single layer owns; and threading data between layers through the context conceals missing legitimate access (e.g. to a network socket) instead of exposing a broken API (Omid Hekayati).
- The position was stated: timeout is an internal budget of the executing mechanism — like a cache TTL — configurable once from outside, not re-declared per request; cancellation validity belongs to the executing module's state machine, the external party only requests it (Omid Hekayati).
- The topic was proposed as a standalone protocol document first (Super Z).
- The counter-position was advanced that cancellation is genuinely achievable at cooperative boundaries (checkpoints), so the objection is to unaccounted-for guarantees rather than to cancellation itself (Super Z).
- What tipped the balance: the counter-position's force was recorded while accepting Omid's direction that the guarantee must be purchased by the module's own design, not declared by a context value (Super Z — recorded; Omid Hekayati — the direction).
- The separate document was rejected and the document's home chosen: folding the topic into process.md rather than a new request-lifecycle protocol document, with the treatment to stay language-general and Go as one illustration among several (Omid Hekayati).

#### Considered and not done
- A standalone `request-lifecycle.md` under docs/protocols (rejected): the protocols directory's membership criterion requires a document to specify a protocol, and the critique — however sharp — does not yet specify one; forcing it there would have produced a position paper wearing a protocol document's clothes. Recorded instead with the explicit conditions under which the topic graduates into a protocol document (a request-scope contract, a wire-level cancellation shape for sRPC).

---

### Provenance stripped; Prior art / Unresolved questions relocated per the documentation-method revision
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - process.handoff.md: Created — all seven topic-level unresolved-question lists and the document-level pointer moved there, organized by topic.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

#### What changed
- The document-level Prior art's premise evidence (Whitehead's process philosophy and CSP/π-calculus as the lineage of process-distinct-from-sequence; Burns's lock-versus-lease distinction as the direct basis of the distributed-systems argument) was folded into the Definition topic's Rationale entry it supports.
- Its comparative residue lives in this entry's Related work section.
- The document-level Unresolved-questions pointer section was removed; its role is superseded by the handoff.
- The body was reduced to wrapping only Drawbacks, Rationale and alternatives, and Future possibilities at every level; open questions live in the paired handoff; premise evidence stays with the claims it supports.

#### Related work
- BPM/workflow literature positioning.
- The note that the lock/lease discussion referenced a public exchange.

---

### Documentation-method migration completed: Discussion wrappers, Drawbacks, and Future possibilities dissolved
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - process.handoff.md: Done - the anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Omid Hekayati - decided; Super Z - applied).
- The finalized documentation method was applied to this document (Omid Hekayati).
- The remaining `#### Discussion` wrappers dissolved: the Definition topic's rejected-alternative entry moved to this entry's `Considered and not done` (its process-philosophy/CSP lineage sentence stays inline as premise evidence at the no-sequence definition claim); the Process and System topic's rejected-alternative entries moved to this entry's `Considered and not done`; the empty wrappers under Process Composition and Relationship to Other Concepts removed (Super Z).
- The two rejected-alternative entries (strict-sequence rejection; the system.md inline-definition supersession and the Protocol sub-concept rejection) were folded into their topics' bodies as stated rejections with their reasoning, per the finalized method's rule that premise evidence and stated rejections stay inline (Super Z).
- The document-level `## Discussion` dissolved: `Drawbacks` content to this entry's `Considered and not done`; the pointer-style `Rationale and alternatives` retired (its targets are recorded in the entries below); `Future possibilities` to the paired handoff's `Anticipated Work`; the document-level Drawbacks and Future possibilities content moved below, without loss (Super Z).

#### Considered and not done
- **Requiring Process to be a strict sequence (rejected; migrated from the Definition topic's retired `Rationale and alternatives`)**: `system.md`'s prior definition called Process "an organized sequence of activities or interactions." This document deliberately drops "sequence," because sequence is one possible shape a process can take, not a defining property — treating it as defining would make concurrent, event-driven, and independently-progressing processes look like deviations from the "real" definition rather than the ordinary cases they are. (Omid Hekayati)
- **Keep Process defined inline in `system.md` (formerly the settled position; now superseded; migrated from the Process and System topic's retired `Rationale and alternatives`)**: `system.md` previously rejected a standalone Process document with a specific argument: "Process cannot be defined without reference to System. A standalone Process document would either duplicate System's definition or silently depend on it, creating the same circular dependency problem this document exists to prevent." That argument is correct about *symmetric* duplication, but this document resolves it by making the dependency asymmetric and one-directional instead: `system.md` defines System and keeps only the System-specific half of the Process↔System relationship; this document defines Process in full, including the Process-specific half of that same relationship. Neither document re-derives the other's core definition. As of that revision, `system.md` has been updated accordingly — its own `### Process` section is now a short pointer here, and its Rationale and Alternatives entry now records this reversal explicitly rather than silently.
- **Define Process as a sub-concept under Protocol (rejected, inherited from `system.md`; migrated from the Process and System topic's retired `Rationale and alternatives`)**: Protocol governs processes, but Process is not a sub-concept of Protocol — processes exist whether or not they are governed by protocols, and Process is a foundational concept that Protocol depends on, not the reverse. `protocol.md`'s own chain — "System → contains → Processes → governed by → Protocols" — is consistent with this document as long as "contains" is read as "provides context for" rather than "cannot exist independent of any system," which is the reading this document adopts above.
- **Grounding the Requests/Cancellation examples in Go only (rejected; migrated from the topic's inline considered-and-rejected paragraph)**: the examined mechanism family is not Go-specific — C#, JavaScript, and Python have adopted equivalents with the same three roles and the same costs, so the analysis is recorded generally with the languages as illustrations, consistent with how Go's Scheduler as an Illustration is used under Concurrency.

#### Considered and not done (from the removed document-level Drawbacks section)
- **This document is large, covering a number of adjacent concepts (Concurrency, Coordination, Events, Asynchrony) that could each eventually justify their own document** — a known and accepted risk from the outset. (Omid Hekayati)
- **Extracting Process into its own document reintroduces the drift risk `system.md`'s original Rationale and Alternatives warned about: two documents now each describe the Process↔System relationship from their own side, and each future change to either concept needs a corresponding check against the other** — accepted, and tracked as the Process-and-System open question in the paired handoff. (Omid Hekayati)

---

### Motivation restored to a motivation; Development topic annotated as an umbrella adoption
- Time: 2026-09-16T00:00:00Z
- Type: Changed
- Propagates to:
  - process.handoff.md: Done — Development's graduation criterion rewritten around the umbrella rule.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed, argued, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- The Motivation section had grown into a revision history rather than a statement of why the document exists: the paragraph announcing the later addition of the `context` discussion, and the paragraph reporting the later addition of the *Expectations and Checks* and *Development as a Process* topics, were removed. Both are already recorded in this changelog's own entries below, so nothing was lost; Motivation now states only the document's origin and purpose — the recurring mechanism-first pattern across the source discussions, and the discipline of separating process from mechanism. The Failure paragraph's self-referential framing ("this document also absorbs…") was rewritten as a timeless statement of the document's scope boundary with the future Error documentation (Super Z — applied; Omid Hekayati — the review).
- The *Development as a Process* topic gained a paragraph recording Omid's position, adopted in this pass: Development is carried as an **umbrella term** — a word naming no content of its own, serving only to gather concepts that already exist, like *object-oriented* over encapsulation, inheritance, and polymorphism, or *leader* over the distinct concepts management science separates. Its content in this document is therefore exactly the Process topics applied to the entity being advanced. The competing scholarly definitions of development (one tradition defines it as the growth of a system's problem-solving power) are candidate characterizations of the target stage and the measure of progress toward it — decisions a particular development's model makes, not adjudications this topic performs (Omid Hekayati — argued; Super Z — drafted).

#### Considered and not done
- **Moving the removed Motivation paragraphs into the changelog as new content (rejected as unnecessary)**: before deleting, the coverage was checked — the `context` discussion's addition and the two-topics addition are already recorded by their own entries in this changelog ("Requests, Cancellation, and Timeout"; "Two topics added"), so the paragraphs carried no information this file lacked, and copying them would only create a second copy to keep in sync.
- **Adopting one of the scholarly definitions (e.g. growth of problem-solving power) as the topic's definition (rejected)**: they are rival characterizations of what a development aims at, and the umbrella stance exists precisely so the topic does not adjudicate them; each becomes relevant only when a concrete development's model must fix its target stage and progress measure.

#### Deliberation
- Omid's review of the day's edits raised three points; the first and third are recorded in this entry — the second, the scope of the TDD protocol document, was accepted in the same pass and is recorded in [tdd.changelog.md](./protocols/tdd.changelog.md)'s corresponding entry (Omid Hekayati).
- On the first point, Omid objected that Motivation had come to read like a changelog entry rather than a motivation; the objection was accepted without reservation and the trim was made (Omid Hekayati).
- On the third point, Omid argued the word Development itself warrants no root-document concept under the project's standard against umbrella concepts at the root: it introduces nothing of its own and merely connects principles that already exist, the way OOP is an umbrella over encapsulation and the like, and that thinkers attach rival definitions to the word anyway (e.g. "increase of the system's problem-solving power") (Omid Hekayati).
- The resolution adopted keeps the topic (it was already written as an adoption of the word's established general meaning, adding no structure) but states the umbrella character explicitly, so future edits test additions against the umbrella rule instead of letting content accrete (Super Z — proposed; Omid Hekayati — accepted).

---

### Two topics added: Expectations and Checks; Development as a Process
- Time: 2026-09-16T00:00:00Z
- Type: Added
- Propagates to:
  - protocols/tdd.md: Done — its concept-level core relocated here; the protocol document rewritten to consume the new topic.
  - protocols/tdd.changelog.md: Done — relocation entry recorded there.
  - process.handoff.md: Done — open questions and the Development graduation criterion recorded there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, approved
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- **Expectations and Checks** (placed after Outcomes): the process-level concept beneath every domain's testing practices. A process model states its expected input and output before enactment; expectations held tacitly in temporary memory are invisible to other participants and exempt from checking, so the discipline is writing them first; a check is the comparison of a process instance against the model's stated expectations; software's *test* is named as one domain's word for check; the realization of a check is a mechanism under *Process Before Mechanism*; boundary cases (inquiry processes, post-hoc verification) are delimited. The concept's dependence on Process is now stated in Process's own document — without the process model, testing has no subject (Omid Hekayati).
- **Development as a Process** (placed after Process and Workflow): Development defined per its established general meaning — a process in which an entity passes by degrees toward a different stage — adopted as an instance of Process with no new structure of its own; domain-independence kept by grounding the word in Process rather than in software; Memar's own concern (the development of systems, carried out by a network of agents) named; governance of development processes assigned to the protocol layer, named here without citation per that layer's citation rule (Omid Hekayati).
- One Abstract sentence added so the Abstract covers the new topics.

#### Considered and not done
- **Giving Development its own document at docs/ root (rejected for now)**: the concept's warranted content — definition, per-topic inheritance from Process, pointer to Agency's Development section, governance note — fits a topic without residue; a standalone document would currently be a canopy over concepts that all already have homes. The graduation criterion is recorded in the paired handoff's Anticipated Work; the same path brought Process itself out of `system.md` when its topic outgrew the parent. (Omid Hekayati)
- **Placing a Development document under protocols/ (rejected)**: the protocols directory's membership criterion is a contract, rule set, or encoding format; Development is the *process under governance*, not a rule set — TDD is the rule set. A protocol-layer document would also have had to define the Development concept itself, a concept-document job the folder's README excludes. (Omid Hekayati)
- **Leaving the expectations/check concept in the TDD protocol document (rejected)**: the concept is domain-independent and definitional — a check presupposes a process model whose expectations precede its instances — so its home is the base layer. Keeping it in the protocol document would force base documents to cite a protocol layer for a general meaning, which the layering's citation rule forbids. (Omid Hekayati)

---

### Defect Resolution as an Inquiry topic added
- Time: 2026-09-16T00:00:00Z
- Type: Added
- Propagates to:
  - protocols/tdd.practice.md: Done — the Boundary section names the reported defect as the inquiry case's recurring instance and links this topic.
  - protocols/tdd.changelog.md: Done — the retarget recorded in its session entry.
  - process.handoff.md: Done — the topic's open questions and its protocol-layer graduation criterion recorded there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [Buffy](../CONTRIBUTORS.md#buffy)) — drafted

#### What changed
- A new topic, **Defect Resolution as an Inquiry** (placed after *Failure*, before *Continuation and Retry*): a defect is defined as a failure observed against an expectation, so the concept presupposes the expectation and unrecorded expectations are stated first; resolving a defect of unknown cause is classified as an **inquiry** process whose expectations are stated for the inquiry itself (evidence, decision, record) per *Expectations and Checks*'s already-stated boundary; the ecosystem's single word *debugging* is named as hiding the seam between the inquiry and the correction that follows it; the inquiry runs on Cognition's operations and awareness disciplines — the characteristic failure being confirmation — and is recorded per the Research facet where it deserves to survive; and the concluding correction is an ordinary development step under *Expectations and Checks*, with the model-caused case routed to Modeling's discipline.
- The topic adds no rules of its own: its content is three already-owned rules (Expectations and Checks' inquiry boundary, Cognition's discourse norms and operations, the Research facet's record) linked to the defect-resolution situation — reasons and links, no examples or procedures.

#### Considered and not done
- **A standalone document for the subject at docs/ root (rejected for now)**: the warranted content fits a topic without residue — every rule it needs is already owned by Process, Cognition, Modeling, and the Documentation system, and no question about defects exists that those documents cannot already answer. The graduation criterion is recorded in the paired handoff's Anticipated Work. (Omid Hekayati)
- **A protocol document under protocols/ (rejected)**: the protocols folder's membership criterion is a contract, rule set, or encoding format; the topic states no Memar-specific rules — an agent holding the base documents derives the resolution procedure from them. A protocol layer would also have had to define the Defect concept itself, a concept-document job the folder's README excludes. (Omid Hekayati)
- **Placing the topic in cognition.md (rejected)**: the inquiry's conduct borrows Cognition's operations, but the subject — a defect and its resolution — is a process situation and its home is the process document; Cognition is cited, not extended. (Super Z — proposed; Omid Hekayati — accepted)
- **A paired debugging practice document (rejected for now)**: an agent holding cognition.practice.md's operation-level and named-error checks derives the investigation procedure; a practice file would restate what the practice layer already carries. (Super Z)

#### Deliberation
- The owner's position, carried into the topic's design: what an executing agent needs is the link between an owned rule and the situation, not exemplars — the same position that excluded worked examples from the TDD protocol document; a hundred examples teach imitation of case surfaces, while one well-placed rule generates the correct procedure for every next case (Omid Hekayati).
- The owner objected to the initial framing that treated the subject as a missing protocol; the correction accepted: the discipline already exists, distributed across the documents that own its pieces — what was missing was only the pointer from the defect situation to those owners (Omid Hekayati — objected; Super Z — corrected).

---
