# Time Handoff

Open work for `protocols/time.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The Instant representation
- State: width, range, precision, and whether a monotonic source is part of the contract — blocked on the definitional question below and on the runtime substrate questions of [Concurrency Realization](./concurrency.handoff.md).
- Next: settle after the substrate and definitional items move.

### Is civil conversion a framework-level concern at all?
- State: the political-churn argument (zone rules change by legislation) suggests it belongs to application-layer libraries, but GUI and scheduling components push back.
- Next: decide against the GUI and scheduling components' actual needs.

### Distributed ordering versus the Instant contract
- State: how causality and ordering guarantees across components relate to the Instant contract belongs with [GP](./giti.md) and [sRPC](./sRPC.md); not settled here.
- Next: joint session with the networking protocols.

### Does Time warrant a fuller concept document?
- State: currently the separation rule is the permanent home; whether a dedicated concept document earns its place is undecided.
- Next: revisit when the representation design starts.

## Anticipated Work

- The Instant representation design.
- The distributed-ordering treatment alongside the networking protocols.
- The definitional discussion's own record, if the project chooses to publish it.
