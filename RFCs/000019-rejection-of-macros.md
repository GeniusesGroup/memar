---
RFC Number: 000019
Title: "Rejection of Syntactic Macros and Meta-Programming"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam provides no syntactic macro system (Rust-style `macro_rules!`/procedural macros, C preprocessor macros) and no compile-time meta-programming/code-generation facility baked into the language itself. Any code generation a project needs is handled by external tooling operating on the explicit source, not by language-level macro expansion.

## Motivation
Macro systems let code generate or rewrite other code at compile time through a separate, often opaque expansion phase, which conflicts directly with Khayyam's foundational explicitness principle: source code should mean exactly what it says, with no hidden expansion step a reader must mentally simulate to understand what will actually execute.

## Guide-level explanation
Where another language might reach for a macro to eliminate boilerplate (e.g. generating repetitive trait implementations), Khayyam developers rely on external scaffolding/code-generation tools that produce ordinary, explicit `.kh` source files ahead of time — files that are then read, reviewed, and version-controlled exactly like hand-written code, with no invisible expansion happening at compile time.

## Reference-level explanation
There is no macro-definition or macro-invocation syntax in the grammar. Code generation, where needed (e.g. the container scaffolding discussed in RFC 0007), is explicitly a pre-compile, tooling-level step that emits ordinary source files, not a compiler-level expansion mechanism.

## Drawbacks
Without a macro system, some categories of legitimate boilerplate reduction (e.g. deriving a family of trait implementations automatically at compile time) require external tooling to be run as a separate build step, rather than being handled inline by the compiler itself — adding a tooling dependency for cases a macro system would otherwise absorb into the language.

## Rationale and alternatives
Macro systems (Rust's `macro_rules!`/proc-macros, C's preprocessor) were rejected because they introduce a compile-time code-rewriting phase that is, by design, somewhat opaque to a reader inspecting only the source — directly in tension with the zero-hidden-magic principle running through RFC 0002, RFC 0003, and RFC 0005.

## Prior art
Rust's macro system and the C preprocessor are the primary prior art being rejected here. Languages and ecosystems that instead rely on external code generators emitting plain source (e.g. Go's `go generate` convention, or Protocol Buffers' code generation step) are closer in spirit to Khayyam's chosen approach.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
