# Runtime Handoff

Open work for `runtime.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### How do pinned user-space tasks block on kernel boundaries without stalling their core's run queue?
The interaction model between user-space scheduling and unavoidable kernel boundaries — how a pinned task blocks on file I/O without stalling its core's run queue — is not yet specified. Core-pinning itself is not a Runtime protocol requirement; if it is a MUST, it belongs in a [Concurrency](../computer/concurrency.md) extension. The leak, when pinning is chosen, still appears at the runtime-host boundary.

### What does the `unsafe` tag gate at the runtime layer, and how is a module replacement audited?
What the `unsafe` tag concretely gates — an API surface requiring explicit enablement, a linter/compiler cooperation, or both — and how a module replacement is audited, are not yet specified. Shared with [Compiler](../computer/compiler.handoff.md).

### Which host kinds are in the first conformance floor?
The protocol names OS, unikernel, WASM host, language library, and JavaScript engine as equally legitimate runtimes. Which of those, if any, a first conformance suite must include — versus remaining examples — is not decided.

## Anticipated Work

- **Two runtime signatures still name the capsule `Bool`.** `IsAsync` in [`modules/computer/runtime/protocol/concurrency.kh`](../../modules/computer/runtime/protocol/concurrency.kh) and `IsBlocking` in [`modules/computer/runtime/protocol/blocking.kh`](../../modules/computer/runtime/protocol/blocking.kh) are owned by abstractions and name `Bool`, included from the folder URI `modules/math/boolean`; under [Abstraction in Khayyam → A Concept Is an Abstraction; a Concrete Instance Is a Capsule](../khayyam/abstraction.md#a-concept-is-an-abstraction-a-concrete-instance-is-a-capsule) they name `Boolean`, included from `modules/math/boolean/protocol/boolean.kh`. Not edited. (From the memar-go port's truth-value pass, 2026-09-28.)
- A minimal conformance floor for any Memar runtime (what an artifact may assume from the environment), separating portable guarantees from host-specific choices.
- The scheduler/synchronization capsule contracts remain [Concurrency](../computer/concurrency.md)'s work; this document only hosts them. Resolve the syscall-boundary question jointly.
- Whether core-pinning is a concurrency-realization MUST, rather than a Memar-framework reference choice, is for a dedicated concurrency session.
