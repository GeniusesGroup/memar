# Khayyam Runtime Specification (Reference Architecture) Handoff

Open work for `runtime.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### How do pinned user-space tasks block on kernel boundaries without stalling their core's run queue?
The interaction model between user-space scheduling and unavoidable kernel boundaries — how a pinned task blocks on file I/O without stalling its core's run queue — is not yet specified, and is the most likely place this model leaks complexity to application developers. (From the Concurrency and Execution Model topic's retired Unresolved questions.)

### What does the `unsafe` tag gate at the runtime layer, and how is a module replacement audited?
What the `unsafe` tag concretely gates at the runtime layer — an API surface requiring explicit enablement, a linter/compiler cooperation, or both — and how a module replacement is audited, are not yet specified. (From the Change Logic in Runtime (Unsafe) topic's retired Unresolved questions.)

### Which parts of this reference architecture, if any, become a conformance floor for any Khayyam runtime?
The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" — shared with [Khayyam's own unresolved questions](./khayyam.handoff.md#open-questions) — applies here with special force: which parts of this reference architecture, if any, should eventually be promoted into requirements any Khayyam runtime must meet (a conformance floor), versus remaining Memar-Framework-specific choices. (From the retired document-level Unresolved questions.)

## Anticipated Work

- A minimal conformance floor for any Khayyam runtime (what the language actually assumes from below, if anything), separating portable guarantees from Memar-Framework specifics. (From the retired document-level Future possibilities.)
- The scheduler/synchronization capsule contracts, specifying what a swappable primitive must satisfy to interoperate with the framework's scheduling — resolving the syscall-boundary question under [Concurrency and Execution Model](./runtime.md#concurrency-and-execution-model). (From the retired document-level Future possibilities.)
