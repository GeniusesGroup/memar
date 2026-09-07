# Memory Handoff

Open work for `protocols/memory.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The contract-term notation
- State: the requirement is stated (copy/ownership semantics are contract members) but the notation is undecided — a capability interface, a naming convention, or a `Syllab`-level annotation.
- Next: design the notation after the abstraction syntax stabilizes.

### Copy semantics at process/network boundaries versus in-process call boundaries
- State: the [Error protocol](./error.md)'s boundary rules suggest the default may differ across a network boundary; the interaction is not worked out.
- Next: work out jointly with the error protocol's next revision.

### The copy convention's interaction with pooling
- State: a pooled buffer is shared across requests by definition; which of a pooled library's outputs are copies and which are views needs a worked-out taxonomy, not just the rule.
- Next: build the taxonomy against a concrete pooled implementation (the networking realization is the first candidate).

### Volatility vocabulary in the OS contract's storage topic
- State: the block grant in [OS → Storage](./os.md#storage-block-abstractions-not-filesystems) is non-volatile memory under this document's definition; whether the OS document should adopt the volatility vocabulary formally, or keep its current block-grant framing with a cross-link, is not decided.
- Next: settle during the next OS document revision.

### Are `Prior art`-style comparative surveys needed for the reclamation taxonomy?
- State: the taxonomy's comparative survey (how each ecosystem positions its mechanism, and the marketing claims attached) was moved to this document's changelog under the documentation method's Discussion-pattern revision. If the survey proves needed in the body for a reader to evaluate the position, that is evidence the criterion needs a refinement; if not, it stays historical.
- Next: revisit after the first implementation evidence lands.

## Anticipated Work

- The contract-term notation design (capability interface, naming convention, or Syllab-level annotation).
- A taxonomy of buffer ownership classes for pooled implementations.
- Once Khayyam's memory model stabilizes, a check that the contract terms and the reclamation taxonomy here can be realized in it without per-language divergence.
- Alignment of the OS storage topic's vocabulary with the definition here.
