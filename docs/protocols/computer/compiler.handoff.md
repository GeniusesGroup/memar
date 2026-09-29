# Compiler Handoff

Open work for `compiler.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The analysis-event schema
The event schema — event names, payloads, ordering guarantees, and the subscription API that definite-assignment analysis, linters, and IDEs consume — is not yet specified anywhere. It needs its own specification before the first analysis tool depends on it.

### How a single binary links multiple runtimes
How a single binary links multiple runtime libraries, each with its own boot convention, is not yet worked out — it is the concrete case where "boot is a configuration choice" most needs a specified resolution order.

### Compile-time designation
The designation mechanism itself — a naming convention, an `ab` contract, or a compiler directive — is not yet specified, nor is how a compile-time evaluation failure (a designated operation that turns out to touch runtime state) is reported.

### What the `unsafe` tag gates
What the `unsafe` tag concretely gates — a compiler refusal unless explicitly enabled, a linter rule, or both — and how a patching operation is audited, are not yet specified. Shared with [Runtime](./runtime.handoff.md).

### Language-versus-implementation boundary, with worked examples
The precise boundary between "what a language specifies" and "what a compiler of that language provides" still needs worked examples before it can be considered settled — shared with [Khayyam's open question on the same boundary](../khayyam/khayyam.handoff.md#the-precise-boundary-between-what-khayyam-specifies-and-what-a-khayyam-toolchain-or-module-provides-still-needs-worked-examples-before-it-can-be-considered-settled).

## Anticipated Work

- A conformance test suite a compiler realization can run against, turning each requirement from review-time guidance into a checkable contract.
- A dedicated specification for the compiler's emitted analysis events, before the first analysis tool depends on the contract.
- The Lexer protocol is already split out: [lexer.md](./lexer.md). Remaining frontend questions (input, output, responsibility boundary, contract with a given backend) stay here until a dedicated frontend protocol is justified.
- An **Implementation Readiness Review** before any compiler code is written: for each remaining open item, settle whether the concept is defined, its boundary is clear, its semantic rule is explicit, it belongs to the language or to a compiler, it is foundational law or pluggable policy, multiple realizations can satisfy it, and what must remain invariant across realizations.
- A **first implementation prototype targeting JavaScript**: a language frontend → a semantic representation → the local Khayyam toolchain under [`modules/khayyam/`](../../modules/khayyam/) → V8, with WebAssembly as the intended second target. The prototype exists to reach running feedback quickly. Two disciplines bind it: the JS backend must never become the hidden specification of the language's semantics; standing up two backends behind one semantic representation is the earliest test that those semantics are implementation-independent. The name `Parser` is not assumed for the frontend.
