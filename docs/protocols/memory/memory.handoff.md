# Memory Handoff
Open work for `protocols/memory/memory.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### The contract-term notation
- State: the requirement is stated (copy/ownership semantics are contract members) but the notation is undecided — a capability interface, a naming convention, or a `Syllab`-level annotation.
- Next: design the notation after the abstraction syntax stabilizes.

### Copy semantics at process/network boundaries versus in-process call boundaries
- State: the [Error protocol](../process/error.md)'s boundary rules suggest the default may differ across a network boundary; the interaction is not worked out. Next in that direction: work it out jointly with the error protocol's next revision.
- State: the adjacent, narrower question — whether an ordinary in-process argument or return value that stays inside one ownership domain is required to be passed by reference rather than copied — is also open. This document currently requires only that the copy/share choice be *stated* as a contract term, and states its default for values that *cross* ownership domains. Whether to also fix a protocol-level default for plain call-boundary passing was raised while dissolving a draft coding-style rule that asserted such a default as a MUST; it is deliberately not adopted here, since the neutrality above is this document's own position and a protocol-level MUST would have to be argued against it rather than past it. Where the claim is settled today it is settled at the realization layer: Khayyam's grammar passes arguments and returns strictly by reference and forbids implicit copying ([Khayyam](../../khayyam/khayyam.md)) — an instance of this protocol, not its authority.
- Next: decide in a dedicated session, together with the tier the chosen position carries (protocol default, library contract term, or tooling-suggested).

### The copy convention's interaction with pooling
- State: a pooled buffer is shared across requests by definition; which of a pooled library's outputs are copies and which are views needs a worked-out taxonomy, not just the rule.
- Next: build the taxonomy against a concrete pooled implementation (the networking realization is the first candidate).

### Volatility vocabulary in the OS contract's storage topic
- State: the block grant in [OS → Storage](../computer/os.md#storage-block-abstractions-not-filesystems) is non-volatile memory under this document's definition; whether the OS document should adopt the volatility vocabulary formally, or keep its current block-grant framing with a cross-link, is not decided.
- Next: settle during the next OS document revision.

### Are `Prior art`-style comparative surveys needed for the reclamation taxonomy?
- State: the taxonomy's comparative survey (how each ecosystem positions its mechanism, and the marketing claims attached) was moved to this document's changelog under the documentation method's Discussion-pattern revision. If the survey proves needed in the body for a reader to evaluate the position, that is evidence the criterion needs a refinement; if not, it stays historical.
- Next: revisit after the first implementation evidence lands.

### What convention names and places generated teardown source?
- State: automation of path-complete release is required to emit explicit source, but the filename, inclusion rule, and whether the artifact is temporary or checked-in are not specified. A historical Khayyam-shelf draft used `file_name.generated_by_gc1.kh` as an example name only.
- Next: settle with the [Linter](../computer/linter.md) and [Compiler](../computer/compiler.md) protocols, as a convention those documents' rule-authorship work can consume.

### Must every `Service` carry `Deinit`?
- State: raised 2026-09-28 by the lifecycle/process/storage pass of the memar-go port. [Teardown is explicit, and automation writes source](../memory/memory.md#teardown-is-explicit-and-automation-writes-source) and [Khayyam → How Khayyam realizes Memory](../../khayyam/khayyam.md#how-khayyam-realizes-memory) give `Deinit` to a capsule whose acquisition requires a release, and the lifecycle protocol `modules/computer/capsule/protocol/life_cycle_contract.kh` carries that teardown surface only. `modules/process/service/protocol/service.kh` composes `Capsule_LifeCycle` into `Service` unconditionally, so every service must declare `Deinit` even when it acquired nothing to release. No lifecycle or service document exists, so the mismatch is carried here, beside the teardown rule. Not edited.
- Question for the owner: does every service acquire something whose release is required, so the unconditional composition stands, or does `Service` drop `Capsule_LifeCycle` and leave `Deinit` to the services that need it?
- Next: owner ruling; then `service.kh` is edited or the reason is stated where the service contract is documented.

### Where do `heap.kh` and `mem.kh` belong?
- State: after the top-level rename `modules/storage/` → `modules/memory/` and the split of former inner `storage/memory/` content into `reference/` and `address/`, `heap.kh` and `mem.kh` remain interim at module root pending owner choice. [Memory → Allocators are libraries](./memory.md#allocators-are-libraries).
- Proposed mapping: `heap.kh` and `mem.kh` → `modules/memory/allocator/` (or `heap/` if the name is kept).
- Status: Not yet approved by the owner. The top-level rename `modules/storage/` → `modules/memory/` and the inner split are settled and recorded in this document's State line above.
- Next: owner ruling on `allocator/` versus `heap/`; then move the files or state the reason where the memory module README documents membership.

### Where does an address-sized integer (`uintptr`) go?
- State: ruled 2026-09-28 by the owner, from [Math Handoff → Does the tower hold widths the reference does not declare?](../math/math.handoff.md#does-the-tower-hold-widths-the-reference-does-not-declare) item (d): an address-sized integer belongs to the memory domain, not to the numeric tower, and the math module declares no capsule for it. The reference uses Go `uintptr` in `memar-go/storage/memory/pointer.go` (`type PTR uintptr`) and in a race context in `memar-go/computer/runtime/scheduler/thread.go`. The memory module already declares `MemoryAddress` and `Memory_Pointer` in `modules/memory/address/protocol/address.kh`; neither is tied to `uintptr` by any document or translation rule. Recorded, not built.
- Open: whether `uintptr` is `MemoryAddress`, `Memory_Pointer`, or a concept of its own in this module, and whether an address-sized value is a capsule here beside those abstractions.
- Next: owner ruling on which declaration receives `uintptr`; until then a translation reports each `uintptr` rather than choosing one.

### Compile-time binary mutation of dynamically-valued constants
- State: an idea recorded in the retired Khayyam-shelf memory-model draft — mutating the binary in place so a "dynamically-valued constant" avoids a memory call, at the same size — was explicitly undecided in that draft's source material. It is not adopted here.
- Next: reopen only with a dedicated argument; otherwise leave dropped.

### Published compatibility contract for default memory-safety analyses
- State: a future possibility carried from the retired Khayyam-shelf draft — publish exactly which static analyses a reference linter configuration performs for memory safety (and which are organization-overridable) so the safety/flexibility trade-off is legible to newcomers without reading the full rule set.
- Next: draft alongside the [Linter](../computer/linter.md) authorship/notation work; not required for the protocol positions above to stand.

### Should storage capabilities be named as independent capabilities, against this document's rejection of named kinds?
- State: recovered 2026-09-30 from an audit of Omid Hekayati's Go-community Telegram-group messages. The owner's position is that a storage concern's needs are independent axes rather than one bundled kind — durable key/value retention, time-series retention, full-text search, vector search, transactions, and a faster derived tier are separately adoptable, and a framework that requires a system to carry a local store, a cache, and a distributed store together has turned one requirement into a package. The tension is with this document's own position, which is not a gap but a designed refusal: [Volatility: the real classifier](./memory.md#volatility-the-real-classifier) keeps retention as a *property* precisely so the field is not split into named kinds, and [The memory/storage dichotomy rejected](./memory.md#the-memorystorage-dichotomy-rejected) records that reifying a tier is what produces the shadow-tier pathology.
- Question for the owner: are these capabilities to be stated as properties a contract may require (in the spirit of [Copy and ownership semantics are contract members](./memory.md#copy-and-ownership-semantics-are-contract-members)), which preserves the refusal, or as a named capability vocabulary, which reifies the field a second time? No document enumerates them today; the closest existing statement is [OS](../computer/os.md), where whether blocks become records, tables, logs, journals, or object stores is explicitly left as meaning owned by the system above the boundary.
- Next: answer this before any storage design session opens, because a profile list adopted by default would be exactly the reification the two sections above reject, and the [Filesystem](../memory/filesystem.md) protocol's "a high-level library whose inclusion is a decision" stance is the precedent for the property-shaped answer.

### What is the retention and erasure rule for preserved history, and where do a record's versions live?
- State: the Modeling document fixes the modeling half — a concern's actual history of state changes is reality, a fix or reversal is a new fact referencing what it corrects, and no storage engine is prescribed ([Modeling → Modeling State Change as Events, Not Destructive Updates](../../modeling.md#modeling-state-change-as-events-not-destructive-updates)) — and the owner has stated the same position directly and repeatedly in the Go-group discussions recovered 2026-09-30: there is no logical reason to update or delete data, and a decision recorded at one time must not be erased by a later decision to change it. The same discussions carry the qualifications that keep this from being an absolute rule, and those qualifications are stated nowhere in `docs/`: secret erasure, legal purge, and bounded retention are not the same act as a state change, and "never delete" makes all three impossible.
- Question for the owner: what is the erasure rule that sits beside history preservation — is a removed value a tombstone that records the removal as a fact, a gap in the history, or an exception to the whole rule — and who states it, this protocol or the Modeling document? Related and equally unstated: whether the versions of one record must be co-located. The source argues both ways inside a single message — that the storage layer should not be made to understand the nature of the data, and that in a distributed store the temporal versions of a record must be kept on one node rather than spread across nodes.
- Next: owner ruling on the erasure rule first; the placement question then belongs to whichever storage design consumes the capability question above, and to [Time Handoff → Distributed ordering versus the Instant contract](../time/time.handoff.md#distributed-ordering-versus-the-instant-contract) for what "co-located" would cost.

### Must teardown be idempotent, and which lifecycle names belong to which resource family?
- State: recovered 2026-09-30 from an audit of Omid Hekayati's Go-community Telegram-group messages, where the owner's stated house practice was three lifecycle members for most structures — initialize, re-initialize, de-initialize — with two disciplines attached: re-initialization is worth its cost only after being measured against release, and must not let information from the previous cycle leak into the new one; and initialization performed inside an external factory function was rejected outright, because it moves the capsule's own behavior outside its encapsulation. What survives of that practice in this repository is narrower than the source: `modules/computer/capsule/protocol/life_cycle.kh` states that `Init` and `Reinit` are not members of the protocol, and this document gives `Deinit` only to a capsule whose acquisition requires a release ([Teardown is explicit, and automation writes source](./memory.md#teardown-is-explicit-and-automation-writes-source)). No document states whether releasing twice is defined, permitted, or an error — a rule the question immediately above this one needs before the composition in `service.kh` can be ruled on either way.
- Question for the owner: is idempotence a protocol requirement for teardown, and does the state sequence differ by resource family — a value with construction and validation, a resource with an open/running/closing/closed progression, a pooled object with reset and a separate lifecycle — or does one sequence serve every resource with the differences left to each protocol that owns one?
- Next: settle alongside [Must every `Service` carry `Deinit`?](#must-every-service-carry-deinit), which asks the same underlying question from the composition side; a ruling on idempotence alone does not answer it, and a ruling there alone leaves this one open. Initialization staying inside the capsule is already settled by [Khayyam → Sovereign Encapsulation](../../khayyam/encapsulation.md) and is recorded here only so the rejected factory alternative is not re-proposed.

## Anticipated Work
- The contract-term notation design (capability interface, naming convention, or Syllab-level annotation).
- A taxonomy of buffer ownership classes for pooled implementations.
- A check that the contract terms, the reclamation taxonomy, and the emitted-source automation path can be realized by more than one language's toolchain without per-language divergence of the *requirements*.
- Alignment of the OS storage topic's vocabulary with the definition here.
- The generated-source convention for teardown automation.
- The published compatibility contract for default memory-safety analyses.
