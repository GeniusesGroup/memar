---
Title: "Method in Khayyam"
Status: Draft
Start Date: "2026-07-28"
ID: "495900"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification defines the `mt` subtype and the method signature grammar this document elaborates and motivates."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: "Depends_on"
      Reason: "Method as Callable Capsule (now specified in this document) assumes the capsule model — Capsule Structure and Privacy, Sovereign Encapsulation — defined there. That document, in turn, now references this one for the method-signature mechanics it no longer restates."
    - Title: "Logic in Khayyam"
      URI: "./khayyam-logic.md"
      Relation: "Reference"
      Reason: "The source document for Composition Depth cited 'Library-Driven Control Flow' as a dependency. That document is now merged into Logic in Khayyam, whose IF/ELSE model relies on the same pass-by-reference, explicit-output-variable mechanic specified here under Method as Callable Capsule — no chaining, in either document, is a consequence of that mechanic."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions for the absence of a fn/func keyword, for rejecting expression chaining, and for the method signature grammar in the canonical Khayyam specification"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Works: ["Reference-level elaboration of method dispatch (static-vs-instance invocation, body-less methods for FFI/contracts), originally written as part of khayyam-encapsulation.md and relocated here unchanged"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "High"
    Tasks:
      - Works: ["Created this document by merging the standalone Function as Capsule and Composition Depth documents into the current Explanation-facet specification"]
        URI: ""
      - Works: ["Relocated Method as Callable Capsule (with its Method Invocation Rules and Body-less Methods subsections) here from khayyam-encapsulation.md, resolving the previously open question about where the mechanical method-signature spec belongs"]
        URI: ""
---

# Method in Khayyam

## Abstract
This document specifies how a Khayyam developer writes and composes callable behavior. It covers the mechanical grammar of the method signature itself (`tp {name} mt (self {owner}) (args) (returns) { }`, pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods for FFI/contracts), and two design decisions built on top of that grammar: first, that there is no dedicated `fn`/`func` keyword or top-level access-modifier syntax — a "function" is structurally just a capsule (`tp {name}`) with a method (`mt`), most commonly a single `Do` method for a simple, function-like call; second, that method calls are statements, not chainable expressions — every intermediate result requires an explicitly declared, named variable, and a method or widget body that accumulates many such named steps is treated as a deliberate signal calling for further decomposition, not a cost to eliminate with chaining syntax. All three are expressions of the same underlying commitment: nothing about how behavior is declared, dispatched, or sequenced should be implicit or syntactically shortcut-able.

A method's receiver is a capsule, so this document assumes and depends on the capsule model — field privacy, Sovereign Encapsulation — specified in [Encapsulation in Khayyam](./khayyam-encapsulation.md), which references this document back for the signature mechanics it no longer restates.

For a walk-through of the core idea before the detailed rules, see the [Guide](#a-function-is-a-capsule) below.

## Introduction

### Motivation
Many languages need extra top-level keywords (`private`, `public`, etc.) to express access/authorization requirements for standalone functions. Khayyam believes such requirements can and do change over time, and that this is easily expressed through ordinary capsule methods rather than dedicated keywords — avoiding yet another category of special-cased, fixed syntax.

Separately, in nearly every mainstream language, the ability to chain method calls or pass one call's result directly into another is taken for granted. But this convenience also lets multiple distinct responsibilities silently accumulate inside a single function body or expression without any forcing function to notice. Khayyam treats the resulting verbosity as intentional: a method or widget that needs many named intermediate steps to do its job is very likely doing more than one job.

### Methodology

## Explanation

### A Function Is a Capsule
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

### Method as Callable Capsule
In Khayyam, functions and methods are not separate concepts; a method is fundamentally a callable capsule. By using the `mt` subtype, developers define an executable behavior and attach it to a receiver. The receiver is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`).

The method signature follows this pattern:

```khayyam
tp {name} mt (self {capsule_owner}) ({efficacy variables}...) ({impressible(affective) variables}...) { ___ }
```

Key rules:
- **Pass-by-Reference and State Protection**: All arguments passed into a method and all values returned from a method are passed strictly by reference. Even though capsules are passed by reference, their internal state remains strictly protected because all data fields are entirely hidden. A receiving method cannot directly mutate the passed capsule's fields. State mutation can only occur if the passed capsule explicitly exposes a behavior (method) that allows it.
- **Parenthesized Separation**: Developers must separate `capsule`, `args`, and `returns` by using `()` to indicate all of them, even if empty. All three are the same at the underlying layers; this rule exists to improve code readability.
- **Standalone Functions**: Developers can write pure standalone functions by omitting the `self` parameter — there is no limitation requiring a receiver.
- **Recommended Naming**: Developers can use any naming for the capsule owner parameter, but `self` is suggested as the base point to reference other members in the capsule.

Example:
```khayyam
tp Set mt (self Key) (key String) (err Error) {}
```

#### Method Invocation Rules
Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.

The distinction between static behavior and instance behavior is governed by the presence of the `self` reference in the method signature, enforced strictly at the tooling/linter layer:

- **Type-Level (Static) Invocation**: Methods defined without a `self` reference belong to the type's blueprint. They must be invoked directly through the type identifier (e.g., `tp.Create()`). Invoking a type-level method on a variable instance (`vr.Create()`) is flagged as an error.
- **Instance-Level Invocation**: Methods defined with a `self` reference require an active memory capsule. They must be invoked through a variable instance (e.g., `vr.Mutate()`). Invoking an instance-level method directly on the type identifier (`tp.Mutate()`) is rejected.

This dispatch model ensures that the boundary between type-level and instance-level behavior is always visible in the method signature, not hidden behind a `static` keyword or a naming convention.

#### Body-less Methods (FFI and Contracts)
A method can be defined without a body (`{}`). This is legally used in two scenarios:

1. **Contract Definition**: Defining the required signature for an abstraction (`ab`). The method body is provided by each capsule that implements the abstraction.
2. **Foreign Function Interface (FFI)**: When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file).

#### Discussion

##### Drawbacks
The strict separation of capsule, args, and returns with `()` adds syntactic ceremony for methods that take no arguments or return no values. A method like `tp Close mt (self Reader) () () {}` has two empty parenthetical groups that carry no information — they exist purely for consistency and readability conventions.

##### Rationale and alternatives
- **Unified parameter list without parenthetical separation (rejected)**: would make it harder to distinguish at a glance which parameters are inputs and which are outputs, especially for methods with many parameters.
- **Separate keyword for functions vs. methods (rejected)**: a method is fundamentally a callable capsule; introducing a separate keyword would create an artificial distinction where none exists at the semantic level.

##### Prior art
Go's method syntax with an explicit receiver is syntactically similar. Rust's `fn` with `&self`/`&mut self` is semantically similar but introduces reference annotations that Khayyam eliminates. Smalltalk's message-passing model is the closest conceptual match.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### No Dedicated fn/func Keyword
There is no `fn`/`func` keyword in the grammar. A "function" is, structurally, just a capsule (`tp {name}`) with one or more methods (`mt`), most commonly a single `Do` method when the intent is a simple, function-like call.

A dedicated `fn`/`func` keyword plus access-modifier keywords (the conventional approach) was rejected as an unnecessary second category of declaration syntax, when the same need is already fully expressible through the existing capsule/method model — consistent with Khayyam's broader "everything is a type" unification principle.

#### Discussion

##### Drawbacks
Even the simplest, most stateless utility function requires defining a capsule and a method rather than a single top-level function declaration, which is measurably more ceremony than virtually every other language for this common case.

##### Prior art
Most languages (C, Go, Java, Rust, Python) provide a dedicated function-declaration keyword distinct from their type/class declaration syntax. Smalltalk and other strictly message-passing-oriented languages, where even "free functions" are ultimately methods on some object, are closer in spirit to Khayyam's approach here.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Composition Depth as a Decomposition Signal (No Expression Chaining)
Khayyam method calls are statements, not chainable expressions (`a.Foo().Bar()` is not legal syntax). Every intermediate result requires an explicitly declared, named variable. A method or widget body that accumulates many such named steps is treated as a deliberate design signal calling for further decomposition, not a cost to optimize away with chaining syntax.

When a developer notices a method or widget accumulating multiple unrelated named steps — for example, a "register comment" widget that both resolves "who is the active user" *and* validates/saves the comment — this is the language pushing back against an under-decomposed model, not a syntax limitation to work around. The correct response is always further decomposition: split out a separate widget/capsule with its own narrow responsibility and its own error boundary (e.g. a dedicated widget that returns only an `ActiveUserID`), never a request for implicit chaining syntax.

This applies uniformly, including to things that *feel* like a single operation — for example a `parse → validate → transform → aggregate` data pipeline. Each stage is a distinct concern with its own failure mode and reuse potential, and Khayyam intentionally provides no syntactic shortcut letting these stages collapse into one undifferentiated block.

Because every method's outputs are written into pre-declared variables passed by reference (not returned as an expression value — see [Method as Callable Capsule](#method-as-callable-capsule)), there is no syntactic slot in the grammar for one call's result to be fed directly as another call's input. The verbosity of named intermediate steps is the price paid for forcing this discipline to be visible directly in the source, rather than living only in a developer's head or a comment.

#### Discussion

##### Drawbacks
Even a simple, genuinely single-purpose sequence (e.g. a three-step pure math calculation) requires multiple named temporary variables, which can read as noisier than an equivalent one-line chained expression in other languages, especially for short-lived, never-reused intermediate values.

##### Rationale and alternatives
Allowing expression-level chaining (as virtually all modern languages do) was rejected because it removes the friction that currently makes over-large method/widget bodies visible and uncomfortable — without that friction, the language would have no organic pressure toward decomposition, relying entirely on developer discipline or external linting to catch the same problem after the fact.

##### Prior art
Go and Rust both support method chaining freely; this is treated as the default in modern language design, which makes Khayyam's rejection here a deliberate, atypical choice rather than an oversight.

##### Unresolved questions
None at this time. (An earlier concern — whether this rule could be misapplied to single-responsibility pipelines that only *look* like several operations — was resolved: it applies uniformly, since each pipeline stage genuinely is a distinct concern with its own failure mode.)

##### Future possibilities
None recorded yet.

## Results

## Discussion

### Drawbacks
Together, these two rules mean Khayyam code contains more named capsules and more named intermediate variables than equivalent code in most mainstream languages: every simple, stateless utility becomes a capsule-plus-method pair, and every multi-step computation becomes a sequence of named variables rather than a chained expression. Both costs are treated as deliberate, load-bearing friction rather than incidental ceremony to be minimized.

### Rationale and alternatives
Both rules trace back to the same underlying choice: Khayyam consistently declines to add a second, shortcut syntax alongside an already-sufficient general mechanism (the capsule/method model for callables; named, pre-declared variables for method outputs), even where the shortcut is common practice elsewhere and would reduce ceremony in the common case.

### Unresolved questions
1. Whether Decorators Rejection and Rejection of Macros belong in this document — under discussion; not yet merged pending that decision.

### Future possibilities
None recorded yet.

## Change Rationale
- **Initial creation.** Created by merging the standalone "Function as Capsule (No fn/func Keyword)" and "Composition Depth as a Decomposition Signal (No Expression Chaining)" documents into the current Explanation-facet specification. Both standalone files have been retired. Deliberately excluded, pending a separate decision: Decorators Rejection and Rejection of Macros (their fit as "method" content is disputed) and the mechanical method-signature spec already present in `khayyam-encapsulation.md` (left in place rather than duplicated, with a cross-reference and an open question about relocating it).
- **Relocation of Method as Callable Capsule.** Resolved the previously open question: since a capsule is an abstraction over `vr`/`mt` rather than the reverse, the mechanical method-signature spec (Method as Callable Capsule, with its Method Invocation Rules and Body-less Methods subsections) belongs in this document, not in `khayyam-encapsulation.md`. Relocated here verbatim, placed as the first detailed topic after the Guide. `khayyam-encapsulation.md` now references this document instead of containing the spec. Also resolved: `library_driven_control_flow.md` has now been reviewed (merged into `khayyam-logic.md`); the Citations entry was updated accordingly and the corresponding Unresolved question removed.
