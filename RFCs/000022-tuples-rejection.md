---
RFC Number: 000022
Title: "Tuples Rejection"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002", "000007"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam has no tuple type or tuple literal syntax (`(a, b, c)` as an anonymous, positional, multi-value type). Any time a developer needs to group multiple values together, that grouping must be a named capsule with named fields, exactly like any other domain type.

## Motivation
Tuples are anonymous and positional — their meaning depends entirely on the order of their elements, which a reader cannot recover without already knowing how the tuple was constructed. This is in direct tension with Khayyam's explicitness principle: every grouping of related data is a domain concept that deserves a name, not an anonymous positional bundle.

## Guide-level explanation
Where another language might return `(string, int, error)` from a function, a Khayyam developer instead defines or reuses a named capsule with named fields appropriate to the domain (e.g. a `ParseResult` capsule with named `Value`, `Length`, and `Err` fields/methods), exactly as they would for any other piece of domain data.

## Reference-level explanation
There is no tuple literal or tuple type syntax in the grammar. Multiple related values are always grouped via an explicitly named capsule.

## Drawbacks
Even a trivial, throwaway pairing of two values (e.g. swapping two variables, or returning a quick coordinate pair) requires naming and defining a capsule, rather than using an anonymous, lightweight tuple literal — measurably more ceremony than virtually every modern language provides for this common case.

## Rationale and alternatives
Tuple types (the conventional approach in Go, Rust, Python, and many other languages) were rejected because their positional, anonymous nature conflicts with Khayyam's principle that every meaningful grouping of data should be a named, self-describing domain concept (RFC 0002, RFC 0007).

## Prior art
Go's multiple return values, Rust's and Python's tuple types, and TypeScript's tuple types are all common prior art for this feature; Khayyam's rejection here is closer in spirit to strongly nominal-typing-oriented languages and to general DDD advice discouraging "primitive obsession" and anonymous data bags.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
