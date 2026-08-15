# Process Changelog

## Changelog

### Initial draft from Saga and locking discussions
- Time: 2026-08-14T00:00:00Z
- Type: Added
- Cited:
  - [Designing Distributed Systems (Brendan Burns)](https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/) — Reference: distinguishing a lock as a permanent grant from a lease that must be renewed and can silently expire, used to support the concurrency/locking separation.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - 
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
