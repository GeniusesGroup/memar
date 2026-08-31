---
Title: "Khayyam Compiler Directives"
Status: Proposed
Start Date: 2026-06-22
ID: 495024
---

# Khayyam Compiler Directives
This document is addressed to the developers of a Khayyam compiler — not to the Khayyam language. Nothing here adds to, restricts, or amends Khayyam's syntax or semantics; every directive below is a recommendation to a compiler implementation team about how Khayyam's own thinking (Zero-Magic Core, Separation of Syntax and Governance, no privileged types) should find concrete manifestation in the tool they build.

## Abstract
A Khayyam compiler is a separate system that consumes the Khayyam specification — not part of what Khayyam *is* (see [Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime)). This document states the directives its implementers work under: recognize only `sc` (code scope) and a small set of low-level jump intrinsics as control-flow primitives, and expose compiler-internal events to analysis tools rather than recognizing any library's constructs by name; keep entry-point and lifecycle conventions out of the language and in compiler configuration plus runtime libraries; evaluate explicitly-designated pure methods at compile time without privileging any type; and treat runtime code mutation as an `unsafe`, opt-in escape hatch under the default of Immutable Infrastructure. Each directive constrains an *implementation*, never the language: disabling or weakening one changes how well a compiler serves Khayyam's philosophy, not what Khayyam programs may express.

## Introduction

### Motivation
Khayyam's core philosophy is a handoff: syntax strictly defines how code is structured, while behavior under the hood — memory management, execution policy, architectural constraint — is delegated to compilers, linters, and organizational frameworks. A handoff only works if the receiving side knows what it received. [Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime) documents the failure mode that motivates keeping the compiler a separate system: once a project owns its compiler, every convenience request becomes pressure to add syntax, special cases, or built-in magic, eroding the "no hidden control flow, no implicit behavior" principle Khayyam exists to protect. Separation of teams is the structural safeguard; but separation alone does not tell the compiler team what the safeguard requires of them day to day.

This document is that statement. It records, for the compiler's own developers, the specific shortcuts that would quietly reintroduce the magic Khayyam removed — special-casing a framework's `IF` by name, hardcoding a `main` lifecycle into the toolchain, privileging numeric types as builtins, normalizing runtime code mutation — and the affirmative behavior each replaced shortcut should be replaced by. A compiler implementer who has read this document should never have to re-derive, from the language specification alone, which side of Khayyam's syntax/governance line a given implementation decision falls on.

## Explanation

### Control Flow via `sc` and Jump Primitives
Khayyam's AST natively recognizes only two control-flow primitives: the `sc` (code scope) grouping and a small set of low-level jump/branch intrinsics (lowered to `goto` at the IR level). It does not natively recognize high-level `if`/`else`/`for`. For a compiler implementer this is not a limitation to work around but the direct expression of Khayyam's refusal to privilege any control-flow paradigm in the toolchain (see [Control Flow in Khayyam](./khayyam-control_flow.md) for the language-side reasoning).

- **No privileged `goto` keyword at language level.** An early draft treated `goto` as the only native branching keyword; that thinking is retired (see [Control Flow in Khayyam](./khayyam-control_flow.md#execution-primitives-the-compilers-role)). The language exposes `sc`; the compiler lowers `sc`-driven branches to jumps internally, without a `goto` keyword in source.
- **No special-casing of framework `IF`.** The compiler does not treat `IF`/`ELSE` imported from the framework as intrinsics. Framework CF methods are ordinary library code built from `sc` + jumps.
- **Event abstraction.** The compiler, as an independent application, emits control-flow events (entering/leaving an `sc`, taking/skipping a branch) to which analysis libraries (DAA, linter) subscribe. DAA therefore learns branch exclusivity from `sc` events, not from recognizing `IF` by name. See [Execution Primitives: The Compiler's Role](./khayyam-control_flow.md#execution-primitives-the-compilers-role) for the full contract.
- **Commands break with a new line.** Each command must end with a new line — the general rule the `return` marker rule below specializes.

#### GOTO (lowering detail)
- `goto(LocationLabel)` is a compiler-internal IR method (not a source keyword).
- Labels are resolved from `sc` boundaries:
  - `loop` / `end` / `next` correspond to `sc` entry/exit points.
  - `return` indicates return from a method body. It does not need to be written at the end of a method; it is a pure IR marker and must end with a line break so it cannot be used as `return 0`.

#### Discussion

##### Drawbacks
Recognizing only `sc` + jumps means the compiler cannot hand-tune a lowering for any specific control-flow library — everything is lowered through the same generic primitives, and a naive lowering of library-driven branching can cost performance relative to a keyword-recognizing compiler's bespoke paths. The event-emission contract is also a real surface the compiler must keep stable: once analysis tools depend on it, changing event shape or ordering becomes a breaking change for consumers the compiler does not control.

##### Rationale and alternatives
- **Treat the framework's `IF`/`ELSE` as compiler intrinsics (rejected)**: promotes one library's names to privileged status inside the toolchain — exactly the coupling Khayyam's control-flow model exists to avoid. Every other control-flow library would remain second-class, and an organization swapping the framework's library for its own would silently lose whatever optimization the special case provided.
- **Keep `goto` as a source-level keyword (rejected; retired thinking)**: see the retired-draft note above; it made the unstructured paradigm privileged rather than one library-built option among many.
- **Silence instead of events (rejected)**: without emitted control-flow events, each analysis tool would have to re-derive branch structure by re-recognizing library names in the AST — reimplementing, per tool, the coupling the event design avoids.

##### Prior art
Mainstream compilers do special-case well-known library symbols for optimization — C compilers' builtin recognition of `memcpy`/`strlen`, Go's compiler magic for `map`, `chan`, and `append`. Khayyam's directive is the deliberate inverse: lower everything through the same primitives and expose events, so no library gains toolchain privilege by being first or bundled. LLVM's design — analyses consuming a lowered IR rather than source-level library names — is the closest structural precedent for the event abstraction.

##### Unresolved questions
The event schema — event names, payloads, ordering guarantees, and the subscription API that DAA, linters, and IDEs consume — is not yet specified anywhere. It needs its own specification before the first analysis tool depends on it (see [Future possibilities](#future-possibilities)).

### Environment-Agnostic Entry Points
Khayyam does not enforce any syntax-level entry point or lifecycle functions such as `main`, `init`, or `deinit`.

Hardcoding an execution model into the language syntax restricts its adaptability for different environments (e.g., event-driven architectures, serverless, or WASM) and forces future breaking changes if the execution paradigm evolves. Instead, defining how a program boots or tears down is the strict responsibility of the `compiler` and `runtime` libraries. These libraries can introduce their own conventions, ensuring the core Khayyam language remains completely environment-agnostic and future-proof.

- **Delegation:** The compiler and the selected runtime framework are entirely responsible for defining how a program boots.
- **Adaptability:** This allows the compiler to easily target different environments (e.g., WASM, Serverless, embedded systems) by simply changing the compiler configuration, without breaking language compatibility.

#### Discussion

##### Drawbacks
With no syntax-level entry point, a newcomer cannot discover "where does this program start" from the language alone — the answer lives in the compiler configuration and the selected runtime's documentation. Misconfiguration is also quieter: a program with no boot convention wired in fails at a later, less obvious point than a missing `main` would.

##### Rationale and alternatives
- **Hardcode `main`/`init`/`deinit` into the language (rejected)**: permanently couples one execution model to the grammar, forcing a breaking language change whenever the execution paradigm evolves, and making the language wrong-by-default for environments (event-driven, serverless, WASM, embedded) whose boot model differs.
- **Let the compiler pick one canonical boot convention (rejected)**: moves the coupling from the grammar to the only implementation most users will ever touch — nearly the same coupling with a thinner layer of deniability; boot remains a *configuration* choice, resolved per target.

##### Prior art
C distinguishes hosted and freestanding environments: the standard requires a `main` function only for hosted implementations, freestanding (embedded) C has no required entry point, and startup code (crt0) is supplied by the environment's toolchain — long-standing evidence that entry-point conventions can live outside a language's grammar. Go, by contrast, requires a `main` package as a language-level rule — the coupling Khayyam's directive avoids.

##### Unresolved questions
How a single binary links multiple runtime libraries, each with its own boot convention, is not yet worked out — it is the concrete case where "boot is a configuration choice" most needs a specified resolution order.

### Compile-Time Functions
- Methods that calculate configurations, constants, or pure logic that do not depend on runtime state MUST be evaluated by the compiler during the compilation phase. The compiler replaces these method calls with constant capsules in the final binary.
- Whether a method qualifies is not because the compiler magically knows `FromASCII`/`Multiplication` — there are no privileged types. `W32`/`NanoSecond` are ordinary capsules. A method qualifies only if it is explicitly designated as pure/const (e.g., it touches no `vr` outside its own scope and its inputs are compile-time constants). The string `"7200"` in the example is human-readable text supplied to a typed variable's method — the variable's type (`NanoSecond`) gives the value its identity, so it is not a magic number; the operation happens at compile time, not runtime.
- Below function MUST compute in compile time not runtime. Any use of `CNF_KeepAlive_Idle` return variable is just a simple constant capsule.

```Khayyam
tp CNF_KeepAlive_Idle mt (self TCPConfig) () (dur duration.NanoSecond) {
    dur.FromASCII("7200")
    dur.Multiplication(duration.NanoSecondInSecond)
}

tp closeIdleSocket mt (tcpSock TCPSock) (st NetSocket) (err Error) {
    // some logic ...
    vr idleDur duration.NanoSecond
    Config.CNF_KeepAlive_Idle()(idleDur)
    vr passIdle Bool
    tcpSock.checkIdlePass(idleDur)(passIdle)
    // some logic ...
}
```

#### Discussion

##### Drawbacks
Compile-time evaluation is effectively a second interpreter the implementation must build and keep semantically identical to runtime evaluation — divergence between the compile-time and runtime result of the same designated method is a real and subtle bug class. Explicit designation also adds an authoring obligation (marking purity) that languages with implicit const-evaluation do not have.

##### Rationale and alternatives
- **Privilege specific types or methods as compiler builtins (rejected)**: violates Zero-Magic Core; there are no privileged types (see [No Privileged Types](./khayyam-variable.md#no-privileged-types)) — `W32` and `NanoSecond` are ordinary capsules, and the compiler knowing `FromASCII` "by name" would be exactly the magic this directive exists to prevent.
- **Let the compiler decide purity automatically by analysis (considered, not chosen)**: silently deciding on the author's behalf conflicts with the principle that design decisions belong to the author and remain visible in source. Automatic analysis may be layered on top of explicit designation as a convenience or diagnostic, but designation stays the source of truth.
- **Evaluate nothing at compile time (rejected)**: loses the pre-compilation guarantee and pushes genuinely static configuration cost into every runtime startup.

##### Prior art
Zig's `comptime`, C++ `constexpr`, and D's CTFE all evaluate pure code at compile time over ordinary language constructs rather than a separate macro language. Zig's approach is closest in spirit; Khayyam differs in tying eligibility to explicit designation of the method (author-owned, visible in source) rather than to a language-level `const` typing discipline.

##### Unresolved questions
The designation mechanism itself — a naming convention, an `ab` contract, or a compiler directive — is not yet specified, nor is how a compile-time evaluation failure (e.g., a designated method that turns out to touch runtime state) is reported to the developer.

### Change Logic in Runtime (Unsafe)
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)

> **Relation to Immutable Infrastructure (same as in khayyam-runtime.md):** Default = immutable/rebuild; this `unsafe` patching is an opt-in escape hatch, not the normal path. The two documents share the same resolution and do not contradict.

#### Discussion

##### Rationale and alternatives
- **Make runtime module replacement a first-class, always-available capability (rejected)**: contradicts Immutable Infrastructure as the default deployment model — no runtime addition of capability without recompilation — and would normalize the uncontrolled capability evolution that principle exists to prevent.
- **Omit the capability entirely (rejected)**: microservice-style module turnover has genuine uses; removing it entirely would push adopters toward out-of-band binary manipulation with no audit story at all.
- **Keep it opt-in and tagged `unsafe` (chosen)**: the capability exists, is visibly dangerous at the call site, and sits outside the normal path — the same shape as the [runtime-side resolution](./khayyam-runtime.md#change-logic-in-runtime-unsafe) of this topic.

##### Prior art
WebAssembly's module add/remove at runtime is the design Khayyam's own text names. Erlang/OTP's hot code loading shows runtime replacement can be industrialized — but only behind significant surrounding machinery (supervision trees, versioned state-transition code), evidence that the feature is legitimate yet never free; the machinery is the runtime's concern, not the language's.

##### Unresolved questions
What the `unsafe` tag concretely gates — a compiler refusal unless explicitly enabled, a linter rule, or both — and how a patching operation is audited, are not yet specified.

## Results
No observed results are recorded yet. This section will be updated when implementing against these directives yields evidence that can be distinguished from their intended rationale.

## Discussion

### Drawbacks
These directives constrain implementers without (yet) a conformance suite — each one is currently enforced only by review against this document, so drift is caught by people, not tooling. The document also speaks for implementations while [Khayyam](./khayyam.md) speaks for the language: a reader looking for "what Khayyam is" must not take directives here as syntax or semantics, and that boundary is itself still being worked out (see Unresolved questions).

### Rationale and alternatives
- **Fold compiler decisions into [Khayyam](./khayyam.md) (rejected)**: Khayyam's own Methodology keeps that document a short overview that links outward; implementation directives there would couple language evolution to implementation detail and grow exactly the document the language spec deliberately keeps small.
- **Leave compiler behavior unspecified (rejected)**: the handoff from language to implementation is Khayyam's central architectural move; leaving the receiving side undocumented means each compiler team re-derives — or silently ignores — the philosophy the handoff exists to preserve, reproducing the convenience-pressure failure mode the separation was designed to prevent.

### Prior art
Go's language specification is deliberately implementation-neutral, with gc, gollvm, and gccgo as independent consumers of it, and compiler-specific behavior documented separately from the spec. Khayyam's split follows the same shape at smaller scale — directives rather than conformance chapters — for the same reason: the language's stability should not depend on any one implementation's details.

### Unresolved questions
1. The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" — shared with [Khayyam's own Unresolved questions](./khayyam.md#discussion); the directives here must be revised once that boundary is settled with worked examples.

### Future possibilities
- A conformance test suite a compiler implementation can run against, turning each directive from review-time guidance into a checkable contract.
- A dedicated specification for the compiler's emitted control-flow events, resolving the open question under [Control Flow via `sc` and Jump Primitives](#control-flow-via-sc-and-jump-primitives) before the first analysis tool depends on the contract.
