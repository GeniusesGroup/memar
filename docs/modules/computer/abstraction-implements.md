---
Title: "abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration"
Status: Draft
Start Date: 2026-07-08
ID: 495413
---

# abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration

## Abstract
`abstraction_p.Implements` is a minimal, generic implementation-intent declaration that any abstraction MAY optionally compose into its own definition. Its sole purpose is to give codegen tools, linters, and compilers a uniform, structural, discoverable signal that a capsule intends to implement that specific abstraction, even before the capsule's implementation is complete. This is strictly a tooling-facing convenience, not a runtime type-safety or anti-misuse mechanism. Structural satisfaction remains a realization property (the Khayyam example below uses its implicit structural satisfaction); this document does not change that property, and adoption is entirely opt-in per abstraction.

## Introduction

### Motivation
Some abstractions — `Error` being the concrete motivating case — require a large number of methods once fully expanded (in Error's case, roughly 15-20 once `DataType`, `Field_MediaType`, and `ADT` are expanded through their own compositions). Manually writing this boilerplate for every concrete capsule is a real, recurring developer cost, and a natural candidate for code generation.

A code generator that wants to scaffold this boilerplate automatically needs *some* reliable signal of intent *before* the capsule is complete. A plain type-assertion against the target abstraction does not work for this: an incomplete capsule, by definition, does not yet satisfy the abstraction, so there is nothing for the tool to structurally detect. `abstraction_p.Implements` exists to provide exactly this signal, uniformly, across any abstraction that opts in.

`abstraction_p.Implements` gives code generators a reliable, uniform signal for scaffolding incomplete capsules. Its contract is with tooling: the declaration makes implementation intent discoverable before the target abstraction's method set is complete, while the realization's structural-satisfaction rules remain unchanged.

## Explanation

### Declaring and discovering intent
An abstraction author who judges an abstraction complex enough to benefit from codegen scaffolding composes `Implements` alongside its other embedded abstractions:

```khayyam
tp Error ab {
    DataType
    Field_MediaType
    ADT
    Implements
}
```

A developer starting a new concrete Error capsule declares this intent immediately, before writing any of
the abstraction's actual methods:

```khayyam
tp ErrServiceNotFound cp {
    Implements
}
```

A codegen tool scanning the codebase can now discover `ErrServiceNotFound` and know, unambiguously, that stub implementations for every method `Error` requires should be generated — without needing `ErrServiceNotFound` to already satisfy `Error` structurally, which it does not yet.

### Semantics and constraints
- **Strictly opt-in, per abstraction.** Not every abstraction needs this — only ones where an abstraction author judges the method count and boilerplate cost high enough that automated scaffolding provides real value. Applying it reflexively to every abstraction would be pure ceremony, in tension with a realization's minimalism.
- **A build/dev-time tooling signal.** An organization can use its Linter to flag runtime use of `Implements()` when that use would drive business-logic branching; the declaration's contract is with tooling, not with application code.
- **A specific abstraction MAY realize this pattern under its own, domain-specific name instead of literally composing `abstraction_p.Implements` itself.** `Error`'s `ImplementsError`/`ImplError()` (see `error_p`) is the first example: a distinctly-named analog rather than a literal embedding of the generic `Implements()`. The reason is disambiguation, not any difference in guarantee — a generic `Implements()` method cannot indicate *which* abstraction is being claimed once a capsule opts into declaring intent for more than one abstraction at a time, since they'd all collapse onto the same single method. A domain-specific name resolves this ambiguity. This applies equally across realizations; it is not a backend-specific concern.
- **Incomplete-implementation state is otherwise ordinary.** A capsule that declares `Implements` intent but has not yet written every required method simply does not yet satisfy the target abstraction — this is business as usual for a structural realization and needs no special-casing beyond what codegen already needs to detect "which methods are still missing" (an ordinary diff against the abstraction's method set).
