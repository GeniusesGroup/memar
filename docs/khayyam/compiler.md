---
Title: "Khayyam Compiler Directives"
Status: Proposed
Start Date: 2026-06-22
ID: 495024
---

# Khayyam Compiler Directives
This document is addressed to the developers of a Khayyam compiler — not to the Khayyam language. Nothing here adds to, restricts, or amends Khayyam's syntax or semantics; every directive below is a recommendation to a compiler implementation team about how Khayyam's own thinking (Zero-Magic Core, Separation of Syntax and Governance, no privileged types) should find concrete manifestation in the tool they build. The directives are currently enforced only by review against this document — there is no conformance suite yet, so implementation drift is caught by people, not tooling.

## Abstract
A Khayyam compiler is a separate system that consumes the Khayyam specification — not part of what Khayyam *is* (see [Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime)). This document states the directives its implementers work under: recognize only `sc` (code scope) and a small set of low-level jump intrinsics as control-flow primitives, and expose compiler-internal events to analysis tools rather than recognizing any library's constructs by name; keep entry-point and lifecycle conventions out of the language and in compiler configuration plus runtime libraries; evaluate explicitly-designated pure methods at compile time without privileging any type; and treat runtime code mutation as an `unsafe`, opt-in escape hatch under [Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition). Each directive constrains an *implementation*, never the language: disabling or weakening one changes how well a compiler serves Khayyam's philosophy, not what Khayyam programs may express.

## Introduction

### Motivation
Khayyam's core philosophy is a handoff: syntax strictly defines how code is structured, while behavior under the hood — memory management, execution policy, architectural constraint — is delegated to compilers, linters, and organizational frameworks. A handoff only works if the receiving side knows what it received. [Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime) documents the failure mode that motivates keeping the compiler a separate system: once a project owns its compiler, every convenience request becomes pressure to add syntax, special cases, or built-in magic, eroding the "no hidden control flow, no implicit behavior" principle Khayyam exists to protect. Separation of teams is the structural safeguard; but separation alone does not tell the compiler team what the safeguard requires of them day to day.

This document is that statement. It records, for the compiler's own developers, the specific shortcuts that would quietly reintroduce the magic Khayyam removed — special-casing a framework's `IF` by name, hardcoding a `main` lifecycle into the toolchain, privileging numeric types as builtins, normalizing runtime code mutation — and the affirmative behavior each replaced shortcut should be replaced by. A compiler implementer who has read this document should never have to re-derive, from the language specification alone, which side of Khayyam's syntax/governance line a given implementation decision falls on.

## Explanation

### Control Flow via `sc` and Jump Primitives
Khayyam's AST natively recognizes only two control-flow primitives: the `sc` (code scope) grouping and a small set of low-level jump/branch intrinsics (lowered to `goto` at the IR level). It does not natively recognize high-level `if`/`else`/`for`. For a compiler implementer this is not a limitation to work around but the direct expression of Khayyam's refusal to privilege any control-flow paradigm in the toolchain (see [The Grammar Refuses Protocol Semantics](./khayyam.md#the-grammar-refuses-protocol-semantics) for the language-side reasoning).

- **No privileged `goto` keyword at language level.** An early draft treated `goto` as the only native branching keyword; that thinking is retired (the reasoning is recorded in [the Control Flow protocol document's changelog](../protocols/control-flow.changelog.md)). The language exposes `sc`; the compiler lowers `sc`-driven branches to jumps internally, without a `goto` keyword in source.
- **No special-casing of framework `IF`.** The compiler does not treat `IF`/`ELSE` imported from the framework as intrinsics. Framework CF methods are ordinary library code built from `sc` + jumps.
- **Event abstraction.** The compiler, as an independent application, emits control-flow events (entering/leaving an `sc`, taking/skipping a branch) to which analysis libraries (DAA, linter) subscribe. DAA therefore learns branch exclusivity from `sc` events, not from recognizing `IF` by name. The full versioned contract is anticipated work — see the paired handoff.
- **Commands break with a new line.** Each command must end with a new line — the general rule the `return` marker rule below specializes.

Recognizing only `sc` + jumps means the compiler cannot hand-tune a lowering for any specific control-flow library — everything is lowered through the same generic primitives, and a naive lowering of library-driven branching can cost performance relative to a keyword-recognizing compiler's bespoke paths. The event-emission contract is also a real surface the compiler must keep stable: once analysis tools depend on it, changing event shape or ordering becomes a breaking change for consumers the compiler does not control.

#### GOTO (lowering detail)
- `goto(LocationLabel)` is a compiler-internal IR method (not a source keyword).
- Labels are resolved from `sc` boundaries:
  - `loop` / `end` / `next` correspond to `sc` entry/exit points.
  - `return` indicates return from a method body. It does not need to be written at the end of a method; it is a pure IR marker and must end with a line break so it cannot be used as `return 0`.

### Environment-Agnostic Entry Points
Khayyam does not enforce any syntax-level entry point or lifecycle functions such as `main`, `init`, or `deinit`.

Hardcoding an execution model into the language syntax restricts its adaptability for different environments (e.g., event-driven architectures, serverless, or WASM) and forces future breaking changes if the execution paradigm evolves. Instead, defining how a program boots or tears down is the strict responsibility of the `compiler` and `runtime` libraries. These libraries can introduce their own conventions, ensuring the core Khayyam language remains completely environment-agnostic and future-proof.

- **Delegation:** The compiler and the selected runtime framework are entirely responsible for defining how a program boots.
- **Adaptability:** This allows the compiler to easily target different environments (e.g., WASM, Serverless, embedded systems) by simply changing the compiler configuration, without breaking language compatibility.

With no syntax-level entry point, a newcomer cannot discover "where does this program start" from the language alone — the answer lives in the compiler configuration and the selected runtime's documentation. Misconfiguration is also quieter: a program with no boot convention wired in fails at a later, less obvious point than a missing `main` would.

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

Compile-time evaluation is effectively a second interpreter the implementation must build and keep semantically identical to runtime evaluation — divergence between the compile-time and runtime result of the same designated method is a real and subtle bug class. Explicit designation also adds an authoring obligation (marking purity) that languages with implicit const-evaluation do not have.

### Change Logic in Runtime (Unsafe)
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)

> **Relation to Structure Is Fixed by Definition (same as in runtime.md):** Default = the base principle's definition-time rule; this `unsafe` patching is an opt-in escape hatch, not the normal path. The two documents share the same resolution and do not contradict.
