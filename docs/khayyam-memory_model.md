---
ID: 000008
Title: "Memory Model"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Citations:
  Depends_on: ["Framework", "khayyam-encapsulation"]
  Extends: []
  Conflicts with: []
Author(s): []
---

### 1. Memory Optimization & Compilation Strategy
Khayyam decouples memory safety and allocation performance through a clear multi-tiered compilation pipeline, completely separating deterministic compiler guarantees from advanced runtime orchestration libraries.

* **Fast/Static Compilation Mode (Development & Verification):** The core compiler utilizes a strictly linear, static **Escape Analysis** ruleset. Since the linter and language grammar forbid arbitrary pointers and implicit mutations, the compiler evaluates heap-to-stack promotions instantly during daily development cycles without performance regressions or compilation delays.
* **Adaptive Optimization Layer (Production & Unikernels):** **PGO (Profile-Guided Optimization)** in Khayyam is not a hardcoded compiler feature, but a **high-level orchestration library**. Developers explicitly introduce this library into their production pipeline. It hooks into high-level system abstractions—leveraging the deterministic, single-process nature of Unikernel deployments—to collect runtime execution traces. This data is then used to dynamically remap short-lived capsule memory footprints directly onto the entry stacks of user-space workers/goroutines, achieving near-zero allocation overhead.

---

## Memory Safety Guardian
Khayyam does not use a built-in heavy Garbage Collector or complex Borrow Checking syntax.
- **Execution Path Analysis:** If a capsule acquires memory via an allocator or requires explicit teardown, the Linter MUST perform static analysis to ensure that the `Deinit()` or `Free()` method is called in all possible execution exit paths before the capsule logically dies.
- **Zero Syntax Cost:** This guarantees memory safety at development time without polluting the language syntax with lifetime annotations.

---

# Memory Model: Sovereignty, No Pointers/Null, No Lifetime Annotations, PGO

## Summary
Khayyam rejects implicit runtime memory magic (garbage-collector heuristics like Go's Escape Analysis), raw machine pointers, the `nil`/`null` concept, and Rust-style lifetime annotations, while still achieving deterministic memory safety. Safety is guaranteed statically by the compiler/linter ecosystem; optimization of memory layout is delegated separately to Profile-Guided Optimization (PGO) tooling. Memory allocation itself is treated as a pluggable library concern, not a language-mandated runtime.

## Motivation
In garbage-collected languages, implicit heuristics strip the systems architect of deterministic control — e.g. forcing critical buffers onto the heap despite explicit local-scope intent, inducing unpredictable GC pauses in high-throughput code. Meanwhile, exposing raw pointers (as in C/C++) conflates machine addresses with high-level references and forces the introduction of `nil`/`null`, leading to Null Pointer Exceptions. Rust's lifetime annotations solve memory safety mathematically but at a steep syntactic and cognitive cost, needed specifically because Rust's syntax allows arbitrary references to local stack variables to cross synchronous/asynchronous boundaries.

## Guide-level explanation
A Khayyam developer interacts only with controlled references to capsules — never raw pointers, never a `nil` keyword. If a capsule can represent "no value" (acting as a container or optional wrapper), it must explicitly implement an `IsNull()` method; emptiness is a semantic behavior of that capsule, not a hardware state the language understands natively. Memory safety (no use-after-free, no data races) is enforced by the compiler/linter via Definite Assignment Analysis and `Deinit()`-path coverage, not by the developer writing lifetime annotations. Memory *optimization* (e.g. moving an allocation from heap to a local scope) is a separate concern handled automatically by the compiler analyzing real runtime execution profiles (PGO) — particularly effective in predictable environments like Unikernels — rather than by developer-supplied syntax hints.

## Reference-level explanation
- **Memory Sovereignty:** architects retain explicit layout control via the compiler/linter ecosystem; no generic execution engine silently overrides this.
- **No `nil` Keyword:** no dedicated nullability keyword exists in the grammar.
- **Definite Assignment Analysis:** no variable (`vr`) may be read, evaluated, or passed unless it has been explicitly, definitively initialized; an unwritten reference is a compile-time failure.
- **Behavioral Nullability (`IsNull()`):** nullability is a capsule-level semantic behavior, not a hardware state.
- **No Lifetime Annotations:** achieved via strict capsule encapsulation (no leaking raw internal references), deterministic scope boundaries (`sc`) bound to linter-enforced `Deinit()` patterns, and the absence of syntax-level pointers (so the compiler can statically prove variable validity via Definite Assignment Analysis alone).
- **Pluggable Allocators:** memory allocation is an independent library concern (Arena, Object Pools, etc.), chosen per application profile, not a forced monolithic runtime.
- **Linters as the Guardian (true home of borrow-checking):** memory safety, data-race prevention, and use-after-free analysis are static-analysis concerns implemented in the Linter, not syntax (e.g. lifetime annotations). **This guarantee is, by default, a recommended policy enforced by the standard Linter tooling — it is not an inherent, unbypassable property of the language itself the way Rust's borrow checker is unbypassable for producing a binary. An organization may relax or replace this tool**, trading the default safety guarantee for flexibility; this should not be read as a language-level guarantee equivalent to Rust's.
- **Explicit over Magic:** specialized memory-tracking needs (e.g. reference counting) are handled via explicit, generated code (`file_name.generated_by_gc1.kh`) rather than hidden compiler/borrow-checker magic.
- **PGO:** the compiler analyzes runtime execution profiles to optimize memory layouts, pre-allocate deterministic buffer sizes, and perform dynamic escape analysis — moving heap allocations to local scopes automatically, based on metrics rather than syntax.


### Explicit Memory Sovereignty for Variables
Khayyam removes hidden Garbage Collection overhead from the variable model. Because variables are logical references to capsule instances, the lifecycle of the underlying memory is governed by explicit Memory ADTs (e.g., Arenas, Pools) rather than by an implicit garbage collector. Migrated libraries must assign lifecycles explicitly, making resource utilization one hundred percent predictable.

This means that when a variable is declared, the memory for its capsule instance is allocated through a memory service that the developer controls. When the variable goes out of scope or is no longer needed, the memory is deallocated through the same service — not through a GC pause that the developer cannot predict or control.

The separation of variable syntax (reference identity) from memory management (lifecycle governance) is a direct application of Khayyam's core philosophy: the language defines *how* code is structured, and the framework defines *how* memory behaves. A variable does not need to know whether its capsule instance lives in an Arena, a Pool, or on the stack — that is a governance decision, not a syntax concern.

## Drawbacks
Relying on the Linter (rather than the compiler itself) as the actual enforcement point for memory safety means the safety guarantee is only as strong as whichever Linter configuration a given build pipeline actually runs — unlike Rust, where an unsafe binary simply cannot be produced by the standard toolchain. The PGO-driven approach to memory layout optimization is, at the time of writing, an ambitious target without a known production-grade precedent operating at the scope described here (automatic, profile-driven heap↔stack migration as a general mechanism); this should currently be read as a long-term architectural goal rather than an already-solved engineering problem.

## Rationale and alternatives
A Rust-style compiler-enforced borrow checker (mandatory, unbypassable) was considered and rejected as the *default* mechanism in favor of a Linter-based, swappable one, consistent with [framework-over-language philosophy](./framework.md) — but this means the strength of the safety guarantee is now a toolchain-configuration decision, not a language guarantee, and this trade-off should be stated explicitly wherever this guarantee is discussed.

## Prior art
Go's Escape Analysis is cited directly as the motivating counter-example of implicit, non-overridable runtime memory magic. Rust's borrow checker and lifetime annotations are cited as the motivating counter-example of syntactic cost for safety. PGO as a discipline is well established (e.g. in LLVM/GCC toolchains) for performance optimization, though not typically for the scope of automatic heap/stack allocation-site migration described here.

## Unresolved questions
Whether the constant/inline-compile-time-binary-mutation idea mentioned for "dynamically-valued constants" (changing binary code directly to avoid a memory call, with the same memory size) will actually be provided is explicitly marked as undecided in the source material itself.

## Future possibilities
A published compatibility contract specifying exactly which static analyses the default Linter performs (and which are organization-overridable) would make the safety/flexibility trade-off in this document much easier to reason about for newcomers.
