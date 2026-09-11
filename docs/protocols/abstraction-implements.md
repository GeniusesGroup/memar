---
Title: "abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration"
Status: Draft
Start Date: 2026-07-08
ID: 495413
---

# abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration

## Abstract
`abstraction_p.Implements` is a minimal, generic, exported abstraction — a single body-less method, `Implements()` — that any Khayyam abstraction MAY optionally compose into its own definition. Its sole purpose is to give codegen tools, linters, and compilers a uniform, structural, discoverable signal that a capsule intends to implement that specific abstraction, even before the capsule's implementation is complete. This is strictly a tooling-facing convenience, not a runtime type-safety or anti-misuse mechanism. Khayyam's abstraction satisfaction remains, and is intended to remain, purely structural (per [khayyam.md](../khayyam/khayyam.md)'s "Contract-First Approach"); this document does not change that, and adoption is entirely opt-in per abstraction.

## Introduction

### Motivation
Some Khayyam abstractions — `Error` being the concrete motivating case — require a large number of methods once fully expanded (in Error's case, roughly 15-20 once `DataType`, `Field_MediaType`, and `ADT` are expanded through their own compositions). Manually writing this boilerplate for every concrete capsule is a real, recurring developer cost, and a natural candidate for code generation.

A code generator that wants to scaffold this boilerplate automatically needs *some* reliable signal of intent *before* the capsule is complete. A plain type-assertion against the target abstraction does not work for this: an incomplete capsule, by definition, does not yet satisfy the abstraction, so there is nothing for the tool to structurally detect. `abstraction_p.Implements` exists to provide exactly this signal, uniformly, across any abstraction that opts in.

An earlier, related proposal — now rejected — explored a marker-method pattern meant to guard against *accidental* structural satisfaction of an abstraction. That approach was rejected for two independent reasons, discovered during review: (1) `Error`'s actual, fully-expanded method set is large enough that accidental collision is already implausible without any special guard; (2) no such mechanism protects against *deliberate* misuse in Khayyam, Go, or Rust — a developer who wants to misrepresent a type can always choose to do so regardless of the type system. `abstraction_p.Implements` solves a genuinely different problem (tooling convenience for incomplete capsules) and should not be read as a revival of that rejected design under a new name.

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
- **Strictly opt-in, per abstraction.** Not every abstraction needs this — only ones where an abstraction author judges the method count and boilerplate cost high enough that automated scaffolding provides real value. Applying it reflexively to every abstraction would be pure ceremony, in tension with Khayyam's minimalism.
- **Purely a build/dev-time tooling signal, not a runtime safety mechanism.** Nothing in the language prevents `Implements()` from being called at runtime, but doing so to drive business-logic branching reintroduces exactly the kind of runtime type-narrowing [The Error](./error.md#multi-cause-returns) explicitly rejects for its covariant-return design, and should be flagged by an organization's Linter if it occurs. This document's contract is with tooling, not with application code.
- **A specific abstraction MAY realize this pattern under its own, domain-specific name instead of literally composing `abstraction_p.Implements` itself.** `Error`'s `ImplementsError`/`ImplError()` (see `error_p`) is the first example: a distinctly-named analog rather than a literal embedding of the generic `Implements()`. The reason is disambiguation, not any difference in guarantee — a generic `Implements()` method cannot indicate *which* abstraction is being claimed once a capsule opts into declaring intent for more than one abstraction at a time, since they'd all collapse onto the same single method. A domain-specific name resolves this ambiguity. This applies equally in Khayyam and in any backend; it is not a backend-specific concern. (An earlier draft of this reasoning additionally claimed Go's version could be hardened into a compiler-enforced "sealed interface" using package-private visibility. That claim was examined and rejected: deliberately embedding a shared marker struct and deliberately writing the same empty method independently are equally trivial to do, so neither realization actually provides a stronger guarantee against intentional misuse than the other; only the naming-disambiguation reasoning survives, folded in here.)
- **Incomplete-implementation state is otherwise ordinary.** A capsule that declares `Implements` intent but has not yet written every required method simply does not yet satisfy the target abstraction — this is business as usual for Khayyam's structural typing and needs no special-casing beyond what codegen already needs to detect "which methods are still missing" (an ordinary diff against the abstraction's method set).
