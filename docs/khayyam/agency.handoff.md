# Agency in Khayyam Handoff

Open work for `agency.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Scheduler interaction with `PANIC()` and diverging-method analysis
The precise mechanism by which the scheduler interacts with a `PANIC()` call (an abrupt halt implemented as an ordinary library method per [Control Flow in Khayyam](./control_flow.md#error-propagation)) — specifically, how static analysis identifies "diverging" methods that never return normally, for the purposes of exhaustive `Deinit()`-path coverage discussed in [Memory Model](./memory_model.md) — is not yet resolved. Next: a dedicated runtime/linter-focused document.

### Standard-library representation of an execution Agent
Khayyam does not yet have a standard-library representation for an execution Agent. [Process → Concurrency](../process.md#concurrency) and [Agency → Execution Agent](../agency.md) establish what such a representation would need to satisfy conceptually; deciding its concrete shape — what it is called, its API, how it is registered and identified, how responsibility for a partition is assigned and reassigned — is deliberately left open. Naming a specific mechanism now, even as a mere proposal — including "Worker" or "Actor" — risks the same error `agency.md` argues against: a specific execution-Agent representation quietly becoming the assumed answer before the actual requirements (scheduling model, runtime constraints, linter governance) that a library-level decision should be made from have been worked out. That decision belongs to a runtime/compiler-focused document. See [Anticipated Work](#anticipated-work).

### Whether further Agency instances belong in the document
`agency.md`'s scope is no longer concurrency-only: [Agency Beyond Concurrency](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-contract-satisfaction) adds a second instance (abstraction satisfaction). One earlier candidate for a third instance was checked and closed: a method being "owned by" another method or abstraction, per [Method in Khayyam → Method Structure](./method.md#method-structure), is a type-system attachment point (which type a callable behavior is structurally attached to), not a party responsible for or delegating an action — it shares a word with Agency's "owner" vocabulary but not the underlying concept, and does not belong there. Whether other Khayyam design decisions besides these two connect to Agency remains open; the document adds an instance only when a real, checked connection is found, not speculatively.

### Whether an intentional-satisfaction mechanism should be adopted
Whether Khayyam should adopt an intentional-satisfaction mechanism at all — and if so, which of [Abstraction in Khayyam](./abstraction.md)'s three candidate options — is that document's own open question, not `agency.md`'s; [Agency Beyond Concurrency](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-contract-satisfaction) states what Agency's vocabulary adds to it without resolving it.

## Anticipated Work

- A standard-library representation of an execution Agent is the most direct next step `agency.md` points toward, but its name, API, and design are deliberately not proposed there — doing so would prescribe a mechanism the same way a `go` keyword or an `async`/`await` pair does, only in prose instead of grammar. That design work belongs to Khayyam's own compiler/runtime documentation, informed by [Agency → Execution Agent](../agency.md) and [Process → Concurrency](../process.md#concurrency) rather than by `agency.md` naming a shape in advance. (Migrated from the retired *Future possibilities*.)
