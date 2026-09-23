---
Title: "Control Flow"
Status: Draft
Start Date: 2026-06-30
ID: 495215
---

# Control Flow

## Abstract
This document is the framework-level home for Memar's control-flow protocol: the rules governing how execution changes course in systems built with Memar, independent of any language. It holds the design of library-defined control flow — the generic `IF`/`ELSE` form, the preferred domain-specific conditional methods, the mechanism summary, structured and unstructured flow as equal library constructs, and the error-propagation model — the naming convention for domain-specific conditional method pairs (two etymologically distinct roots rather than base-plus-negation); its open questions and anticipated work are tracked in the paired [handoff](./control-flow.handoff.md). Grammar-level facts belong to each language's own documents (that Khayyam's grammar ships no branching, looping, or exception syntax, grouping branch bodies with a single inert `sc` primitive, is stated in [Khayyam](../khayyam/khayyam.md)); the reasons individual constructs were not added to a grammar are recorded in this document's [changelog](./control-flow.changelog.md), not in any body. Topics still to be developed here: the conditional-pair protocol as an abstraction contract, loop- and iteration-shaped control flow, and halting semantics.

## Introduction

### Motivation
`IF`/`ELSE` are only a generic default: developers should prefer domain-specific conditional methods whose name expresses the actual condition (e.g. for branching on an `Error` value, instead of `IF(err.IsNull(), ...)`). Why the Khayyam grammar contains none of these mechanisms is a language-layer fact stated in [Khayyam](../khayyam/khayyam.md); the reasons individual constructs were refused by the grammar are recorded in [this document's changelog](./control-flow.changelog.md). A framework-level protocol layer remains above the grammar facts: what rules a conditional pair must satisfy to be a well-formed protocol participant, what the standard library's success/failure branching pair should be named and where it should live, and how control flow behaves across boundary crossings where no language mechanism exists. Naming such pairs carelessly carries real readability risk: an antonym pair built by negation-prefix, such as `IfErrorOccurred`/`IfErrorNotOccurred`, is dangerously easy to misread, since the `Not`/no-`Not` difference is visually subtle both for a human skimming a diff and for an AI assistant reading code quickly.

## Explanation

### Two etymologically distinct roots, not base-plus-negation
For conditional pairs in general, prefer two etymologically distinct roots over a base term plus its negation — e.g. `Failed`/`Succeeded`-style pairs rather than `X`/`NotX`-style pairs. This makes each branch immediately, visually distinguishable rather than requiring the reader to notice a single added/missing word.

### Candidates for the success/failure branching pair
For the specific, very common case of branching on an `Error` value's success or failure, several naming and placement directions were explored during design discussion but none has been finalized. Not yet finalized — pending resolution of the [Unresolved questions](./control-flow.handoff.md#open-questions) below.

- `IfErrorOccurred`/`IfErrorNotOccurred` — rejected for the negation-prefix readability risk above.
- `IfFailed`/`IfSucceeded` as global, package-less functions — rejected for a language-neutral reason: a global function name carries no inherent domain context; without an explicit receiver, the name alone does not say what is being checked for failure or success. Package or namespace qualification is how other languages supply that missing context to a global name; a language with no package/namespace concept has nothing to qualify it with, and the bare global form is refused outright rather than rescued by convention (Khayyam's lack of a package/namespace concept is that instance — [Khayyam](../khayyam/khayyam.md)). The replacement direction is type-level (static) invocation: a method defined without `self`, invoked on the type identifier rather than on an instance — the type identifier supplies the anchor the global name lacked (Khayyam's `tp.Create()` form, stated in the same document). Naming the pair itself remains open (Unresolved questions).
- `storageErr.OnFailure(...)` / `storageErr.OnSuccess(...)` as instance methods on the `Error` value itself — closer to Khayyam's Uniform Invocation Syntax (the receiver supplies the missing domain context that a global function lacks), but raises a deeper, still-unresolved semantic question (see [Unresolved questions](./control-flow.handoff.md#open-questions) below): is it correct for an `Error` — whose identity already represents failure — to also expose an "on success" branch, or does this actually belong on a more general, shared abstraction instead?
- `storageErr.OnPresent(...)` / `storageErr.OnAbsent(...)` — a candidate built around the *existing* presence/absence behavior a type may expose as a contract term ([Memory → Absence is a type's contract](./memory.md#absence-is-a-types-contract-not-a-universal-machine-condition)), framed neutrally around "does a value exist" rather than "did the business operation succeed." This was proposed as a way to let the same method pair work naturally both for `Error` (`OnAbsent` = "no error occurred") and for any other presence/absence-style capsule (e.g. an optional search result), but it has not been confirmed as final.

### Library-Defined Control Flow
In this protocol's model, flow constructs — conditionals, loops, jumps, and domain-specific branch methods — are library-level method calls over the primitive that groups a branch body, never grammar keywords. In Khayyam's realization this is directly visible: the grammar ships no control-flow keywords (`if`, `else`, `for`, `while`, `continue`, `retry`, `goto`) and no logical operators (`&`, `|`, `!`); every control-flow abstraction is implemented entirely as a library-level method call (e.g. `tp IF in "memar/process/control-flow/if.kh"`), brought into scope explicitly via `in`, never via implicit auto-import. "Library-defined" describes how these abstractions are packaged today, not a constraint the model itself imposes: nothing prevents a future code generator, compiler-intrinsics-aware framework, or an organization's own toolchain from producing the same abstractions through a different mechanism, as long as they are still built from the primitives rather than added to a grammar. Across all such libraries the common denominator is the branch-grouping primitive, not how any particular library drives it — an analysis tool that listens to scope-entry/exit and branch events understands every library's flow, not just one library's `IF`.

A code scope names *what* would run; the library method decides *when*. A mid-scope `CF.Return()` — like `return` in other languages — is therefore ordinary control flow, not automatically a smell; similarly `CF.Break()` is not automatically a smell. What matters is not mixing the two concepts.

#### The Generic Form: IF/ELSE
A developer never reaches for a built-in `if`; they explicitly import a conditional abstraction such as `IF`/`ELSE` from the framework and call it like any other method, passing the branch as a named scope (`sc`) rather than an anonymous block:

```khayyam
tp IF in "memar/process/control-flow/if.kh"
tp ELSE in "memar/process/control-flow/else.kh"
tp Error in "memar/process/error/error.kh"

tp CheckSomeThing mt () (data Data) (err Error) {
  vr isValid Status
  validator.Check(data)(isValid)

  IF(isValid, ValidData)
  tp ValidData sc {
      // Code scope to execute if valid
  }
  ELSE(isValid, InvalidData)
  tp InvalidData sc {
      // Code scope to execute if invalid
  }
}
```

`ELSE` always takes an explicit reference back to the same condition value it pairs with; it never relies on implicit lexical adjacency to "whatever conditional came before it" — that would reintroduce hidden state binding: a construct must carry its dependencies in its own arguments rather than reach for state implied by position or surrounding text. Khayyam's encapsulation design rejects closures on this same ground ([Closures as Implicit Capsule Syntax](../khayyam/encapsulation.md#closures-as-implicit-capsule-syntax)) — an instance of this rule, not its authority.

#### The Preferred Form: Domain-Specific Conditional Methods
`IF`/`ELSE` are a generic default only — a last resort when no more specific name exists. In real domain code, the condition being tested almost always has a name that is far more expressive than a generic boolean check. When that name exists, use it.

Consider a payment processing method that saves a transaction to a storage service. Instead of:

```khayyam
tp IF in "memar/process/control-flow/if.kh"
tp ELSE in "memar/process/control-flow/else.kh"

tp ProcessPayment mt (self PaymentService) (req PaymentRequest) (err Error) {
  vr saveErr StorageError
  storage.Save(req.Transaction)(saveErr)

  vr saveErrIsNull Bool
  saveErr.IsNull()(saveErrIsNull)

  IF(saveErrIsNull, PaymentSaved)
  tp PaymentSaved sc {
      // ...
  }
  ELSE(saveErrIsNull, PaymentFailed)
  tp PaymentFailed sc {
      // ...
  }
}
```

The storage result capsule itself exposes domain-named conditional methods, so the calling code reads as a sequence of named intentions rather than a generic boolean check:

```khayyam
tp Error in "memar/process/error/error.kh"
tp Logger in "memar/process/log/logger.kh"

tp ProcessPayment mt (self PaymentService) (req PaymentRequest) (err Error) {
    vr saveErr StorageError
    storage.Save(req.Transaction)(saveErr)

    saveErr.OnAbsent(PaymentRecorded)
    tp PaymentRecorded sc {
        // storage succeeded — no error was present
        // continue processing
    }

    saveErr.OnPresent(PaymentStorageFailed)
    tp PaymentStorageFailed sc {
        // storage failed — a real error is present
        // log it with context, return a layer-appropriate error (naming and layering of this error path is an open question owned by [The Error](./error.md))
        vr logEntry StorageFailureLog
        logEntry.From(saveErr)(logEntry)
        logEntry.AttachContext(self.InstanceID, req.TransactionID)(logEntry)
        Logger.DispatchEvent(logEntry)()

        err.CloneFrom(ErrPaymentTemporarilyUnavailable)()
    }
}
```

The name `OnAbsent` / `OnPresent` directly expresses the semantics of the check (is an error *present* or *absent*?), which is both self-documenting and visually distinct — the two branch names cannot be confused for each other by a reader skimming a diff, unlike a pair built by negation prefix (the naming convention for such presence/absence or success/failure branch pairs is still an open question — see [Unresolved questions](./control-flow.handoff.md#open-questions)).

This pattern generalizes: whenever a capsule result has a natural binary or multi-way interpretation meaningful to its domain (valid/invalid, found/not-found, granted/denied), the capsule itself should expose conditional methods by those names, so the calling code never reduces a rich domain event to a naked boolean check.

Looping is built the same way: low-level compiler-intrinsic jump methods replace `while`/`for`/`do-while`, but collection iteration MUST be driven through the Container ADT, never manual pointer/index manipulation.

#### Mechanism Summary
- **Syntax Minimalism:** foundational execution jumps and condition evaluations are standard method calls (Compiler Intrinsics) tied to specific execution contexts, not reserved words.
- **Library-Level Abstraction:** advanced control flow (Ruby-style `retry`, `continue`) is implemented purely as libraries/modular packages.
- **Explicit Scope & Tooling Assistance:** the compiler never performs implicit auto-imports of control-flow libraries; everything is explicit via `in`. An LSP/Developer Assistant is relied on to reduce the resulting friction without introducing compiler magic.
- **Linter Governance over Compiler Dictatorship:** organizations can configure their Linter to block raw intrinsic jump methods and mandate their own approved control-flow libraries, without touching the language core.
- **Elimination of Logical Operators:** `&`, `|`, `!` do not exist in the grammar; boolean/conditional logic is expressed via explicit capsule methods. The compiler guarantees these explicit method chains are optimized directly into atomic hardware bitwise instructions (`AND`/`OR`), so syntactic purity does not cost hardware efficiency.


### Structured and Unstructured Flow as Libraries

The model supports both structured and unstructured flow as ordinary library constructs built on the same underlying primitives (in Khayyam's realization, the `sc` subtype and the compiler's jump/branch intrinsics): a `GOTO`-style jump method is exactly as valid, and exactly as unprivileged, as an `IF`/`ELSE` pair. Neither is a keyword; neither is forbidden by the language. An organization that wants to forbid raw jump methods in its own codebase, or mandate structured constructs exclusively, can do so with its Linter — without asking the language to make that choice, once, for every Khayyam program that will ever be written.

Structured, unstructured, and domain-named conditionals are simply the paradigms known today, on today's conventional, classical-hardware execution model — this document does not claim that list is closed. Nothing in the model couples a control-flow model to a particular computation substrate: if a fundamentally different paradigm arrives — quantum computing's superposition-based branching, for instance — it does not need to be hacked into the language or wait for a compiler update; it is built as another library on the same `sc`/jump-intrinsic primitives already described here, exactly like `IF`/`ELSE` or `GOTO` are today.

### Error Propagation
Error propagation is a form of control flow: whenever execution leaves its normal path because a fallible operation failed, control flow changes just as surely as it does inside an `IF`/`ELSE` branch — the only question is which method carries the change. What an error *is*, and what contract it must satisfy to count as one, is defined once, independent of any language, in [The Error](./error.md); this document is concerned only with how execution continues once one has occurred, inside Khayyam specifically. That the Khayyam grammar offers no dedicated error syntax is itself a rule, not an omission — see [The Grammar Refuses Protocol Semantics](../khayyam/khayyam.md#the-grammar-refuses-protocol-semantics).

A method that can fail declares an explicit `Error`-typed (or, where appropriate, a specific error-capsule-typed) output, exactly like any other output variable. The developer is not required to write any special syntax to "catch" it, but the Linter is relied upon to ensure every returned error is actually inspected/routed rather than silently discarded, instead of the compiler enforcing this via dedicated syntax.

- **No Hidden Control Flow:** no operator may mask an early return; every fallible operation's error path is a normal, visible output variable.
- **No Core-Level Panics:** abrupt execution halts are implemented as standard library methods (e.g. `PANIC()` in the Memar framework), not compiler directives or special syntax.
- **Linter Over Syntax:** instead of Go-style mandatory boilerplate, the compiler/linter ensures developers explicitly handle or route returned error capsules.

### Topics to be developed here
This document holds the protocol's design directly. Planned topics, each to be added as it is actually designed rather than pre-registered in detail:

- **The conditional-pair protocol** — the contract a well-formed conditional method pair must satisfy: how the condition is evaluated, whether the two branches are symmetric, how the receiver's state is read, and how the pair relates to the presence/absence abstraction family.
- **Iteration and loop-shaped control flow** — the same library-driven treatment applied to repetition, where the condition lives.
- **Halting semantics** — abrupt control transfer (`PANIC()`-family behavior) as an ordinary method call, its contract, and its relationship to error propagation ([The Error](./error.md)).
