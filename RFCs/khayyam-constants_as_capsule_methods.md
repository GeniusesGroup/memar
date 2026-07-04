---
RFC Number: 000016
Title: "Constants as Capsule-Returned Values"
Status: Draft
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002", "000015"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
A constant in Khayyam is simply a variable returned by a capsule method that cannot change after first initialization — an organizational/architectural rule, not a dedicated compiler keyword. Two flavors are distinguished: static constants (inlined at compile time) and dynamically-valued constants (declared at compile time but initialized at runtime).

## Motivation
A dedicated `const` keyword was already rejected at the consumer side (RFC 0002); this RFC addresses the producer side specifically — how a value that should never change after initialization is expressed without introducing a separate keyword category.

## Guide-level explanation
A "config" capsule for a module, for example, exposes module-level values through methods. Some of those methods may allow controlled, intentional changes to specific values; others guarantee a value never changes once initialized. Both cases are ordinary capsule methods — there is no separate `const`-flavored declaration syntax.

## Reference-level explanation
- **Static constants:** compile-time declared and initialized, usually inlined directly at compile time, conceptually equivalent to "a function that runs entirely at compile time and returns the value living in that function's body."
- **Dynamically-valued constants:** compile-time declared, but runtime-initialized, requiring a runtime memory-service call to obtain their value since they cannot be inlined.

## Drawbacks
Without a dedicated keyword, the "this value never changes" guarantee for a constant depends entirely on the capsule author's discipline (not exposing a mutating method) rather than being enforced by a single, unmistakable declaration keyword a reader can immediately recognize.

## Rationale and alternatives
A dedicated `const` keyword (the conventional approach in most languages) was rejected for the same reasons given in RFC 0002 — it would reintroduce a consumer/producer-side modifier that Khayyam otherwise eliminates entirely in favor of behavior being intrinsic to the capsule.

## Prior art
Most languages provide an explicit `const`/`final`/`let` keyword. Khayyam's "constant as a compile-time function" framing is conceptually close to `constexpr` functions in C++ or `comptime` values in Zig, though without a dedicated keyword marking them as such.

## Unresolved questions
Whether developers should be able to change a "dynamically-valued constant" at runtime by having the compiler force the runtime to rewrite binary code directly (avoiding a memory-service call, with the same memory size) is explicitly marked as undecided in the source material ("Really decide to provide this??") and remains unresolved.

## Future possibilities
None recorded yet.
