---
RFC Number: 0000
Title: "Error Handling: Library-Driven and Syntax-Free"
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
Khayyam has no `try-catch`, `panic`/`recover`, or `?`-operator syntax. Errors are always ordinary, explicit output values (capsules implementing the `Error` abstraction), and abrupt halts are an ordinary standard-library method call (e.g. `PANIC()`), not a compiler directive.

## Motivation
Syntactic sugar like Rust's `?` operator masks early returns and binds the compiler to a specific standard-library type (`Result`); Khayyam believes control flow should never be hidden behind an operator. Go's alternative — explicit but extremely verbose `if err != nil` boilerplate at every call site — is also avoided, not by hiding the check, but by shifting enforcement from syntax to the Linter.

## Guide-level explanation
A method that can fail declares an explicit `Error`-typed (or, where appropriate, a specific error-capsule-typed — see Reference-level explanation) output, exactly like any other output variable. The developer is not required to write any special syntax to "catch" it, but the Linter is relied upon to ensure every returned error is actually inspected/routed rather than silently discarded, instead of the compiler enforcing this via dedicated syntax.

## Reference-level explanation
- **No Hidden Control Flow:** no operator may mask an early return; every fallible operation's error path is a normal, visible output variable.
- **No Core-Level Panics:** abrupt execution halts are implemented as standard library methods (e.g. `PANIC()` in the Memar framework), not compiler directives or special syntax.
- **Linter Over Syntax:** instead of Go-style mandatory boilerplate, the compiler/linter ensures developers explicitly handle or route returned error capsules.
- **Covariant Error Returns:** a method may declare its error output as the generic `Error` abstraction, or as a specific concrete error capsule type directly (e.g. `(err ErrServiceNotFound)` instead of `(err Error)`), as long as that concrete type itself implements the `Error` abstraction. This is not considered a violation of the abstraction's contract, and gives callers static, compile-time knowledge of exactly which error type to expect without any runtime type-narrowing/reflection mechanism being required in the language.

## Drawbacks
Without compiler-enforced syntax (like Rust's `?` or Go's required `if err != nil` pattern that at least makes ignoring an error visually obvious), the actual discipline of "every error gets handled" depends entirely on Linter configuration and developer diligence — see RFC 0008's equivalent trade-off for memory safety. A team running a weak or disabled Linter could silently drop errors with no language-level safety net at all.

## Rationale and alternatives
A `try-catch`/exception model was rejected for hiding control flow in implicit stack unwinding. Rust's `?` operator was rejected for binding the compiler to one specific result type and for hiding an early return behind an operator. Go's mandatory verbose boilerplate was rejected as unnecessary ceremony once a strict Linter can enforce the same discipline without forcing every call site to spell it out manually.

## Prior art
Rust's `Result`/`?`, Go's explicit `(value, error)` returns with manual checks, and exception-based models (Java, Python, JS) were all considered as the dominant prior art in this space; Khayyam's approach is closest in spirit to Go's explicit returns, but moves the "did you check it" enforcement from required syntax to tooling.

## Unresolved questions
None at this time for the core mechanism. See RFC 0010 for the separate, framework-level question of when a low-level error should be translated/logged rather than propagated verbatim, and RFC 0020 for the open question of standard conditional-method naming for branching on error/success.

## Future possibilities
None recorded yet.
