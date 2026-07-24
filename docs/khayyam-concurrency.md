---
RFC Number: 000011
Title: "Concurrency: Syntax-Free and Definition-Driven"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001", "000003"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam embeds no concurrency model into its syntax — no `go` keyword, no `async`/`await`. Whether a method blocks or runs asynchronously is an intrinsic property of the method's own definition (tagged via an abstraction, e.g. `tp Async ab`), not a choice made by the caller, and execution is scheduled in user-space by framework-level schedulers, aligned with Unikernel/Exokernel architecture.

## Motivation
Embedding a concurrency model directly into language syntax (Go's `go`, Rust's `async`/`await`) couples the language permanently to one specific concurrency philosophy and is the classic source of the "function coloring" problem, where async and sync functions become incompatible without explicit, often painful conversion machinery.

## Guide-level explanation
A method's creator, not its caller, decides whether that method is asynchronous, by tagging it with an abstraction at definition time. Callers do not choose sync-vs-async behavior at the call site; they simply call the method, and its nature is already fixed by its own definition. Underlying execution runs on user-space (green) threads managed by library-level schedulers (e.g. the Memar framework's scheduler) — the language syntax itself remains entirely unaware of OS kernel threads.

## Reference-level explanation
- **Definition-Site over Call-Site:** concurrency behavior is intrinsic to the method, expressed via an abstraction tag, not a caller-side keyword.
- **User-Space Scheduling (Unikernel Synergy):** the default architectural stance favors green threads managed by library-level schedulers, for zero-overhead context switching.
- **Avoiding Function Coloring:** because asynchronous behavior is a Linter-verified abstraction (`ab`) rather than a compiler keyword, the function-coloring problem that plagues `async`/`await` languages does not arise, keeping the core AST clean and orthogonal.

## Drawbacks
Without a privileged compiler-level concurrency keyword, all of the static guarantees that languages like Rust derive from `async`/`await` being baked into the type system (e.g. compile-time prevention of blocking calls inside async contexts) must instead be reconstructed entirely by Linter rules — placing the same opt-in/swappable trade-off discussed in RFC 0008 and RFC 0009 onto concurrency safety as well.

## Rationale and alternatives
Built-in `async`/`await` syntax (Rust, JS, Python, C#) was rejected specifically because of the function-coloring problem it introduces; Go's `go` keyword was rejected as a syntax-level concurrency primitive that, per RFC 0001's framework-first philosophy, should not be hardcoded into the language at all.

## Prior art
Erlang/BEAM's process model and user-space green-thread scheduling are the closest prior art for definition-driven, syntax-light concurrency at scale. Go's goroutines popularized lightweight user-space threads but still couple their creation to a dedicated keyword (`go`), which Khayyam avoids.

## Unresolved questions
The precise mechanism by which the scheduler interacts with a `PANIC()` call (an abrupt halt implemented as an ordinary library method per RFC 0009) — specifically, how static analysis identifies "diverging" methods that never return normally, for the purposes of exhaustive `Deinit()`-path coverage discussed in RFC 0008 — is not yet resolved and is earmarked for a dedicated runtime/linter-focused RFC.

## Future possibilities
A dedicated `Khayyam-runtime`/`Khayyam-compiler` RFC set covering scheduler design, the PANIC/runtime interaction above, and how Unikernel thinking shows up concretely in the execution model is the recommended next step for this area.
