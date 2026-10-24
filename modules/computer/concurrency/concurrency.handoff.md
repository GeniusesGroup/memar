# Concurrency Realization Handoff
Open work for `modules/computer/concurrency.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### The signaling primitive's contract
- State: delivery guarantees, multiple receivers, and priority are unspecified; the contract must be settled together with the Event concept in [process.md](../../process/process.md#events).
- Next: joint session with the Process document's Event topic.

### Substrate configuration exposure
- State: whether stack-size and suspension controls are exposed to application configuration or kept internal is undecided.
- Next: decide against the first realization.

### Foreign blocking code
- State: narrowed 2026-10-05. What the document settles: the mitigation and the documentation expectation, because the rule is already a two-branch obligation — an operation that would block a kernel thread (a socket read, a file operation, a lock wait) is either realized through the substrate's suspension mechanism or explicitly documented as substrate-hostile, and a library that silently blocks its carrier thread degrades the whole system while appearing locally correct ([The substrate: user-space threads](./concurrency.md#the-substrate-user-space-threads)). A call into a foreign library takes one of the same two branches; what is unstated is whether the obligation reaches code Memar does not own, whose documentation Memar cannot write.
- What remains: detection — how the substrate learns that a foreign call has blocked a kernel thread, whether by the library's own report or by the substrate measuring the carrier — and whether a detected block is reacted to or only surfaced. Nothing in concurrency.md names a detection mechanism.
- Next: write the detection half into [The substrate: user-space threads](./concurrency.md#the-substrate-user-space-threads); specify with the first realization; the networking libraries are the expected first encounter.

## Anticipated Work
- The signaling primitive's contract specification (delivery guarantees, multiple receivers, priority).
- Substrate observability (Worker states, queue depths, pool saturation) as a framework capability.
- Alignment checks with [Runtime](../runtime/runtime.md) once that protocol and a Khayyam-consuming realization of it mature.
