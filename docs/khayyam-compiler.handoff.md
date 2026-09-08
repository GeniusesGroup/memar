# Khayyam Compiler Directives Handoff

Open work for `khayyam-compiler.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Control Flow via `sc` and Jump Primitives
The event schema — event names, payloads, ordering guarantees, and the subscription API that DAA, linters, and IDEs consume — is not yet specified anywhere. It needs its own specification before the first analysis tool depends on it (see [Anticipated Work](#anticipated-work)).

### Environment-Agnostic Entry Points
How a single binary links multiple runtime libraries, each with its own boot convention, is not yet worked out — it is the concrete case where "boot is a configuration choice" most needs a specified resolution order.

### Compile-Time Functions
The designation mechanism itself — a naming convention, an `ab` contract, or a compiler directive — is not yet specified, nor is how a compile-time evaluation failure (e.g., a designated method that turns out to touch runtime state) is reported to the developer.

### Change Logic in Runtime (Unsafe)
What the `unsafe` tag concretely gates — a compiler refusal unless explicitly enabled, a linter rule, or both — and how a patching operation is audited, are not yet specified.

### Language-vs-implementation boundary
The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" is still being worked out — shared with [Khayyam's open question on the same boundary](./khayyam.handoff.md#the-precise-boundary-between-what-khayyam-specifies-and-what-a-khayyam-implementation-provides-still-needs-worked-examples-before-it-can-be-considered-settled); the directives in `khayyam-compiler.md` must be revised once that boundary is settled with worked examples.

## Anticipated Work

- A conformance test suite a compiler implementation can run against, turning each directive from review-time guidance into a checkable contract.
- A dedicated specification for the compiler's emitted control-flow events, resolving the open question under [Control Flow via `sc` and Jump Primitives](./khayyam-compiler.md#control-flow-via-sc-and-jump-primitives) before the first analysis tool depends on the contract.
- A dedicated **Tokenizer/lexer abstraction**, specified as an independent protocol before any compiler consumes it (split out of the Task Management/Organization chat, 2026-08-12); the protocol now has its own document: [protocols/lexer.md](./protocols/lexer.md).
- An **Implementation Readiness Review** before any compiler code is written: for each remaining open item, settle whether the concept is defined, its boundary is clear, its semantic rule is explicit, it belongs to Khayyam or to an implementation, it is foundational law or pluggable policy, multiple implementations can realize it, and what must remain invariant across implementations. This review is the [protocol-before-implementation](./protocol.md) discipline applied to the compiler effort itself.
- A **first implementation prototype targeting JavaScript**: Khayyam source → language frontend → a semantic representation → [memar-js](https://github.com/GeniusesGroup/memar-js/) → V8, with WebAssembly as the intended second target. The prototype exists to reach real, running feedback quickly — backend and frontend code executing against the same semantics — not to be a production compiler. Two disciplines bind it: the JS backend must never become the hidden specification of Khayyam's semantics (the semantic representation is the source of truth both targets realize); and standing up two backends behind one semantic representation doubles as the earliest test that the language's semantics are implementation-independent. Before any code, the frontend abstraction itself must be specified through the usual protocol process, answering at minimum: its input; its output; its responsibility boundary (syntax only, or semantic validity too); what is dropped at this stage; what is deliberately not resolved here; its contract with `memar-js`; and what must remain shared so a later Go backend need not re-derive the language's semantics. The name `Parser` is deliberately not assumed for this component — the name encodes an architecture, and the abstraction is decided before the vocabulary is.
- A **repository question** for the language itself: Khayyam does not provide a compiler ([Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime)), so a dedicated `khayyam` repository is not created for now — language work starts inside [memar-khayyam](https://github.com/GeniusesGroup/memar-khayyam/), and a separate repository becomes justified only when the language can be understood and specified independently of Memar; even then it would hold the language as an artifact (specification, semantics, examples), never an implementation.
