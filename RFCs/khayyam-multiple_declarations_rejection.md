---
RFC Number: 000023
Title: "Multiple Declarations Rejection"
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
Khayyam does not allow declaring multiple variables in a single statement (e.g. `vr a, b, c Type` or `var a, b = 1, 2`). Every variable declaration is its own explicit, separate statement.

## Motivation
Multi-variable declaration syntax saves a small amount of typing but compresses several distinct pieces of information (each variable's own name, type, and initial state) into a single line, making it easy to skim past one of several declared variables, especially when their types or initial values differ.

## Guide-level explanation
Where another language might write `var x, y int = 1, 2`, a Khayyam developer writes two separate, equally visible declarations:

```khayyam
vr x int
x.FromString("1")(x)
vr y int
y.FromString("2")(y)
```

Each declaration is its own line, with its own clear scope in the source, consistent with the broader principle (RFC 0004) that explicitness in the number of visible steps is preferred over compressed, multi-purpose syntax.

## Reference-level explanation
The grammar for `vr` permits exactly one variable name and one type per declaration statement; there is no comma-separated multi-declaration form.

## Drawbacks
Declaring several related variables together (e.g. the x/y components of a coordinate) requires multiple separate lines rather than one compact line, which is more verbose for this common case than most other languages.

## Rationale and alternatives
Multi-variable declaration syntax (the conventional approach in Go, C, and many other languages) was rejected for the same readability reasoning behind RFC 0004 and RFC 0002: compressing multiple distinct pieces of information into a single line works against the language's broader preference for one explicit, visible step per statement.

## Prior art
Go, C, and JavaScript all support multi-variable declaration syntax as a convenience. Languages with a stricter "one binding per statement" discipline (e.g. idiomatic, non-compressed style in many functional languages) are closer in spirit to Khayyam's choice here.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
