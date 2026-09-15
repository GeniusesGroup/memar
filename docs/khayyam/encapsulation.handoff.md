# Encapsulation in Khayyam Handoff

Open work for `encapsulation.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Memory aliasing through borrowed, externally-mutable buffers
- State: carried from the Sovereign-Encapsulation topic's retired Unresolved questions list; the deferral itself is stated in the body at [Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation). Whether a capsule backed by a borrowed, externally-mutable buffer can be mutated through a channel other than its own method contract (raw memory aliasing at or below the buffer level) is deferred to future documents on memory management and buffer ownership; this is a case where an ownership/borrow-tracking policy in the compiler or linter layer could plausibly close the gap.

### What behavioral guarantees do primitive capsules provide?
- State: carried from the Primitive-Capsule-Specification topic's retired Unresolved questions list.
1. What behavioral guarantees does each primitive capsule provide? Is there a formal specification for `W32`, `W64`, `R32`, `R64`, and other primitive capsules?
2. Should primitive capsules be defined by the language itself, by the standard library, or by the Memar framework? Each choice has different implications for portability and governance.
3. How do primitive capsule guarantees interact with the compiler's optimization strategy — can a `W32` with wrapping semantics be optimized differently from a `W32` with saturating semantics?

### How are constant methods specified and used?
- State: carried from the Constants-as-Capsule-Returned-Values topic's retired Unresolved questions list.
1. Whether developers should be able to change a "dynamically-valued constant" at runtime by having the compiler force the runtime to rewrite binary code directly (avoiding a memory-service call, with the same memory size) is explicitly marked as undecided and remains unresolved.
2. How to pass a return value from a constant method to other methods — the interaction between constant methods and the broader method-call chain needs further specification.

### Document-level
- State: carried from the document-level retired Unresolved questions list.
1. Should the language or the Memar framework provide a set of "standard" capsules for common patterns (e.g., `Pair`, `Result`, `Option`) to reduce the ceremony of defining named capsules for simple cases?
2. How does the encapsulation model interact with serialization and deserialization — can a capsule's internal state be serialized without going through its public methods?

### Does the `get`/`set` generation MAY belong here?
The 2026-09-15 pass landed "a linter MAY write accessors on request" in [Capsule Structure and Privacy](./encapsulation.md). That sentence is a suggested tooling rule, not a fact of encapsulation. Whether it stays, or moves to a protocol-layer suggested-rules catalog, is owned by [Linter Handoff → Do suggested rules get a catalog document](../protocols/linter.handoff.md#do-suggested-rules-get-a-catalog-document-stay-in-subject-documents-or-split-by-kind). Do not add more maybe-rules here until that is decided.

## Anticipated Work

- A linter mode that detects capsules with "trivial getter" methods (methods that simply return a field value without transformation) and suggests whether they indicate a missing domain abstraction or are genuinely appropriate. (From the Capsule-Structure-and-Privacy topic.)
- A formal specification document for each primitive capsule, defining its behavioral guarantees, overflow semantics, serialization contract, and range semantics, serving as the reference for both compiler implementation and migration guidance. (From the Primitive-Capsule-Specification topic.)
- A standard library of commonly-needed capsules (e.g., `Pair`, `Result`, `Option`, `Range`) that provide named, domain-specific alternatives to tuples and generic containers, following the naming and design conventions documented in the base document. (Document-level.)
