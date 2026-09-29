# Concurrency Realization Handoff

Open work for `protocols/concurrency.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The signaling primitive's contract
- State: delivery guarantees, multiple receivers, and priority are unspecified; the contract must be settled together with the Event concept in [process.md](../../process.md#events).
- Next: joint session with the Process document's Event topic.

### Substrate configuration exposure
- State: whether stack-size and suspension controls are exposed to application configuration or kept internal is undecided.
- Next: decide against the first realization.

### Foreign blocking code
- State: how the substrate interacts with calls into libraries that block kernel threads — detection, mitigation, documentation expectations — is unspecified.
- Next: specify with the first realization; the networking libraries are the expected first encounter.

## Anticipated Work

- The signaling primitive's contract specification (delivery guarantees, multiple receivers, priority).
- Substrate observability (Worker states, queue depths, pool saturation) as a framework capability.
- Alignment checks with [Runtime](./runtime.md) once that protocol and a Khayyam-consuming realization of it mature.
