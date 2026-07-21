---
RFC Number: 0000
Title: "Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam provides no mathematical or logical operators (`+`, `-`, `==`, `*`). All operations are explicit methods on a capsule (e.g. `a.Add(b)(c, err)`), so the possibility of failure (overflow, division by zero) is always visible in the method's signature rather than hidden behind syntactic sugar.

## Motivation
Operations like addition or division are physical, hardware-bound processes that can fail; they are not infallible mathematical abstractions. Traditional syntax (`c = a + b`) leaves no room to return an error, forcing languages to invent dangerous workarounds: hidden panics, exceptions, or silent overflow.

## Guide-level explanation
Where another language would write `c = a + b`, Khayyam code calls a method directly on the domain capsule: `a.Add(b)(c, err)`. For simple operations, this method lives directly on the relevant domain capsule (e.g. a `Money` capsule exposing its own `Add`/`Sum` method, which can also enforce domain rules like currency matching while it's at it). For complex formulas where writing nested method calls would be unwieldy, developers may instead pass the formula as a string to a specialized evaluator capsule (e.g. `MathEval.FromString("x = (-b + sqrt(b^2 - 4ac)) / 2a")`). When the parameters to such a formula are compile-time constants, the compiler evaluates the deterministic, pure logic at compile time automatically — the same way a regex engine pre-compiles its automaton from a literal pattern — so this is not a runtime-only escape hatch; it carries the same compile-time guarantees as the direct method-call form whenever its inputs are known statically.

## Reference-level explanation
- No `+`, `-`, `*`, `==`, or similar tokens exist in the grammar.
- Arithmetic and comparison are always explicit capsule methods with explicit error outputs.
- `MathEval.FromString()` (or equivalent) handles complex formulas via string input, with compile-time evaluation when inputs are invariant.

## Drawbacks
Even trivial arithmetic requires a method call rather than an infix operator, which is significantly more verbose than virtually every other language in existence. For formulas passed as strings, type-checking of the formula's inner operands (e.g. preventing `Money + Duration`) depends on the specific evaluator capsule's implementation rather than being a language-level guarantee — this is currently an open design question for the standard `MathEval` implementation specifically (see Unresolved questions).

## Rationale and alternatives
Built-in infix operators (the universal default) were rejected because they structurally cannot express a failure path, which conflicts with Khayyam's broader principle (RFC 0009) that no control flow, including failure handling, should ever be hidden behind syntax.

## Prior art
Domain-modeling-heavy codebases in many languages already wrap arithmetic in named methods for business types (e.g. `Money.add()` in DDD-style Java/C# code) as a best practice; Khayyam makes this the *only* available path rather than an optional convention.

## Unresolved questions
Whether the standard `MathEval.FromString()`-style evaluator performs full compile-time type-checking of formula operands (preventing nonsensical cross-type operations like adding incompatible domain quantities), or only validates syntax while deferring type errors to runtime, is not yet settled for the recommended framework implementation.

## Future possibilities
None recorded yet.
