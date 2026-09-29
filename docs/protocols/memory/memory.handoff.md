# Memory Handoff

Open work for `protocols/memory/memory.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The contract-term notation
- State: the requirement is stated (copy/ownership semantics are contract members) but the notation is undecided — a capability interface, a naming convention, or a `Syllab`-level annotation.
- Next: design the notation after the abstraction syntax stabilizes.

### Copy semantics at process/network boundaries versus in-process call boundaries
- State: the [Error protocol](../process/error.md)'s boundary rules suggest the default may differ across a network boundary; the interaction is not worked out. Next in that direction: work it out jointly with the error protocol's next revision.
- State: the adjacent, narrower question — whether an ordinary in-process argument or return value that stays inside one ownership domain is required to be passed by reference rather than copied — is also open. This document currently requires only that the copy/share choice be *stated* as a contract term, and states its default for values that *cross* ownership domains. Whether to also fix a protocol-level default for plain call-boundary passing was raised while dissolving a draft coding-style rule that asserted such a default as a MUST; it is deliberately not adopted here, since the neutrality above is this document's own position and a protocol-level MUST would have to be argued against it rather than past it. Where the claim is settled today it is settled at the realization layer: Khayyam's grammar passes arguments and returns strictly by reference and forbids implicit copying ([Khayyam](../khayyam/khayyam.md)) — an instance of this protocol, not its authority.
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
- State: raised 2026-09-28 by the lifecycle/process/storage pass of the memar-go port. [Teardown is explicit, and automation writes source](../memory/memory.md#teardown-is-explicit-and-automation-writes-source) and [Khayyam → How Khayyam realizes Memory](../khayyam/khayyam.md#how-khayyam-realizes-memory) give `Deinit` to a capsule whose acquisition requires a release, and the lifecycle protocol `modules/computer/capsule/protocol/life_cycle_contract.kh` carries that teardown surface only. `modules/process/service/protocol/service.kh` composes `Capsule_LifeCycle` into `Service` unconditionally, so every service must declare `Deinit` even when it acquired nothing to release. No lifecycle or service document exists, so the mismatch is carried here, beside the teardown rule. Not edited.
- Question for the owner: does every service acquire something whose release is required, so the unconditional composition stands, or does `Service` drop `Capsule_LifeCycle` and leave `Deinit` to the services that need it?
- Next: owner ruling; then `service.kh` is edited or the reason is stated where the service contract is documented.

### Where do `heap.kh` and `mem.kh` belong?
- State: after the top-level rename `modules/storage/` → `modules/memory/` and the split of former inner `storage/memory/` content into `reference/` and `address/`, `heap.kh` and `mem.kh` remain interim at module root pending owner choice. [Memory → Allocators are libraries](../memory.md#allocators-are-libraries).
- Proposed mapping: `heap.kh` and `mem.kh` → `modules/memory/allocator/` (or `heap/` if the name is kept).
- Status: Not yet approved by the owner. The top-level rename and inner split are recorded in [Modules Handoff → Should `memory/` be top-level instead of nested under `storage/`?](../../../modules/README.handoff.md#should-memory-be-top-level-instead-of-nested-under-storage).
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

## Anticipated Work

- The contract-term notation design (capability interface, naming convention, or Syllab-level annotation).
- A taxonomy of buffer ownership classes for pooled implementations.
- A check that the contract terms, the reclamation taxonomy, and the emitted-source automation path can be realized by more than one language's toolchain without per-language divergence of the *requirements*.
- Alignment of the OS storage topic's vocabulary with the definition here.
- The generated-source convention for teardown automation.
- The published compatibility contract for default memory-safety analyses.
