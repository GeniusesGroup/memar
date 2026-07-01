---
RFC Number: 0000
Title: "Absence of Closures and Anonymous Functions"
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
Khayyam intentionally omits support for closures and anonymous functions. If a behavior requires captured state, that state must surface as a named, explicit Capsule (`cp`) with its own Method (`mt`), not be hidden inside an unnamed function.

## Motivation
Closures are heavily used in other languages for callbacks and inline dynamic logic (e.g. capturing variables for sorting or filtering). While syntactically convenient, this introduces architectural problems: hidden state capturing creates invisible dependencies and breaks explicit state management, and the ease of writing inline functions encourages developers to mash multiple distinct behaviors into a single method body under the false promise of "refactoring later."

## Guide-level explanation
If a behavior needs state (like a captured variable), that is by definition a new domain entity. Developers must define a specific capsule for it, explicitly pass the required state in, and implement the necessary method. This keeps all state dependencies explicit, testable, strictly encapsulated, and analyzable by the compiler.

## Reference-level explanation
There is no closure or lambda syntax in the grammar. Any callback-shaped requirement is expressed as a named capsule implementing the relevant abstraction (e.g. a comparator capsule implementing a `Compare` method), referenced by name like any other type.

## Drawbacks
The discomfort and verbosity of having to name a capsule for even small, single-use behaviors (e.g. a one-off sort comparator) is a real and acknowledged cost. There is a recognized risk that a developer could recreate the same laziness this rule is meant to prevent by writing a throwaway, badly-named, single-use capsule instead of a proper closure — this is treated as a naming-convention/linter concern (see future linter RFCs), not a reason to reconsider this decision.

## Rationale and alternatives
**Reduced Optimization Surface:** capsule-centric code, where state is always a named, explicit type, is significantly easier for the compiler to analyze and optimize than ad-hoc captured scopes. Both models are theoretically equivalent in the worst case, but capsule-based state is far more consistently optimizable in practice, because the compiler always has a concrete, named type to reason about rather than an implicit closure environment whose shape varies by call site. (An earlier, now-corrected version of this rationale argued closures cause additional heap allocation/escape compared to capsules — this is not accurate: a named capsule holding the same captured references has the same memory-lifetime profile as a closure would. The real justification is architectural explicitness and analyzability, not raw performance.)

## Prior art
Java's pre-Java-8 model (no lambdas, only anonymous inner classes) followed the same philosophy Khayyam follows here, and it is informative evidence about the real-world cost of this constraint: the resulting boilerplate for simple, single-use callbacks (event listeners, one-off comparators) was significant enough that Java eventually added lambda expressions in Java 8 under sustained developer pressure.

A second, more direct data point comes from Go's standard `net/http` package, which offers two parallel ways to register a request handler for the same need: a closure-based form, `func HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request))`, and a capsule/struct-based form, `func Handle(pattern string, handler Handler)`. In practice, when both paths exist side by side, developers consistently default to the closure-based path, and encapsulation suffers in both forms regardless: `pattern` ends up living outside the handler type rather than being owned by it. This is read as evidence that offering closures alongside a capsule-based alternative does not lead to better modeling — it leads to the closure path being taken by default, with the encapsulation discipline silently degraded. Removing the closure path entirely is treated as a deliberate forcing function rather than an oversight, precisely because this dual-path failure mode is observed in real, widely-used code rather than hypothesized.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
