---
RFC Number: 000015
Title: "Function as Capsule (No fn/func Keyword)"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001", "000002"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam does not provide a dedicated `fn`/`func` keyword or top-level access modifiers (`private`, `public`) for functions. A function is modeled as a capsule with methods describing its own behavior; the recommended convention for a simple, function-like call is a `Do` method on a small capsule.

## Motivation
Many languages need extra top-level keywords (`private`, `public`, etc.) to express access/authorization requirements for standalone functions. Khayyam believes such requirements can and do change over time, and that this is easily expressed through ordinary capsule methods rather than dedicated keywords — avoiding yet another category of special-cased, fixed syntax.

## Guide-level explanation
Instead of declaring a standalone function, a developer defines a capsule whose purpose is to perform the desired logic, and gives it a `Do` method:

```khayyam
// when is a helper function for setting the 'when' field of a Timer.
// It returns what the time will be, in nanoseconds, Duration d in the future.
tp Do mt (wh WhenHelper) (d duration.NanoSecond) (t monotonic.Time) {}

// use in this manner:
vr t1 monotonic.Time
WhenHelper.Do (d) (t1)
```

This is not a rejection of pure, standalone-function-style logic — it is fully supported — it is simply always expressed as a method on some capsule rather than as an unattached top-level declaration.

## Reference-level explanation
There is no `fn`/`func` keyword in the grammar. A "function" is, structurally, just a capsule (`tp {name}`) with one or more methods (`mt`), most commonly a single `Do` method when the intent is a simple, function-like call.

## Drawbacks
Even the simplest, most stateless utility function requires defining a capsule and a method rather than a single top-level function declaration, which is measurably more ceremony than virtually every other language for this common case.

## Rationale and alternatives
A dedicated `fn`/`func` keyword plus access-modifier keywords (the conventional approach) was rejected as an unnecessary second category of declaration syntax, when the same need is already fully expressible through the existing capsule/method model — consistent with Khayyam's broader "everything is a type" unification principle.

## Prior art
Most languages (C, Go, Java, Rust, Python) provide a dedicated function-declaration keyword distinct from their type/class declaration syntax. Smalltalk and other strictly message-passing-oriented languages, where even "free functions" are ultimately methods on some object, are closer in spirit to Khayyam's approach here.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
