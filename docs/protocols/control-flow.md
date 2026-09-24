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

- `IfErrorOccurred`/`IfErrorNotOccurred` — a negation-prefix pair whose visual similarity can make the branches easy to misread.
- `IfFailed`/`IfSucceeded` as methods on the parent type — the receiver supplies the domain context that a global name lacks; the naming pair itself remains open (see the [Unresolved questions](./control-flow.handoff.md#open-questions)).
- `storageErr.OnFailure(...)` / `storageErr.OnSuccess(...)` as instance methods on the `Error` value itself — the receiver supplies domain context, while the semantic question remains open: whether success belongs on `Error` or on a more general shared abstraction.
- `storageErr.OnPresent(...)` / `storageErr.OnAbsent(...)` — a candidate built around the presence/absence behavior a type may expose as a contract term ([Memory → Absence is a type's contract](./memory.md#absence-is-a-types-contract-not-a-universal-machine-condition)), framed around whether a value exists rather than whether a business operation succeeded.

### Library-Defined Control Flow
In this protocol's model, flow constructs — conditionals, loops, jumps, and domain-specific branch methods — are explicit operations over the primitive that groups a branch body. A realization may package these operations as library methods, compiler intrinsics, or another explicit mechanism. Khayyam is one realization example: its grammar ships no control-flow keywords or logical operators, and its control-flow abstractions are library-level method calls brought into scope explicitly via `in`. Across realizations, the common denominator is the branch-grouping primitive, not how a particular library or compiler drives it — an analysis tool that listens to scope-entry/exit and branch events understands every realization's flow.

A code scope names *what* would run; an explicit control-flow operation decides *when*. A mid-scope return operation is therefore ordinary control flow, and a break operation is likewise an explicit branch decision. The model keeps the scope and the transition as distinct concerns.

#### The Generic Form: IF/ELSE
A realization may expose a generic conditional abstraction that receives an explicit branch scope. The following Khayyam source is one realization of that generic form:

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

`ELSE` always takes an explicit reference back to the same condition value it pairs with; the construct carries its dependencies in its own arguments rather than relying on position or surrounding text. A realization may express that rule through named scopes, explicit closures, or another mechanism with the same observable dependency boundary.

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

Looping is built the same way: a realization can provide low-level compiler-intrinsic jump methods for repetition and use its collection-iteration contract, keeping the control-flow policy in named methods rather than raw pointer/index manipulation.

#### Mechanism Summary
- **Syntax Minimalism:** foundational execution jumps and condition evaluations are standard method calls tied to specific execution contexts, leaving the choice of syntax to each realization.
- **Library-Level Abstraction:** advanced control flow is implemented through named library methods and modules.
- **Explicit Scope & Tooling Assistance:** each realization makes the visibility and import rules explicit, while an LSP or developer assistant can reduce the resulting friction without introducing compiler magic.
- **Linter Governance over Compiler Dictatorship:** organizations can configure their Linter to block raw intrinsic jump methods and mandate their own approved control-flow libraries, without changing the protocol.
- **Explicit Logical Operations:** a realization may express boolean and conditional logic through named capsule methods; its compiler may optimize those method chains into hardware instructions while preserving the protocol's semantics.


### Structured and Unstructured Flow as Libraries

The model supports both structured and unstructured flow as ordinary library constructs built on the same underlying primitives (in a realization such as Khayyam, the `sc` subtype and the compiler's jump/branch intrinsics): a `GOTO`-style jump method is exactly as valid, and exactly as unprivileged, as an `IF`/`ELSE` pair. Both are ordinary library constructs, and a realization's Linter supplies any project-specific governance over their use. An organization that wants to forbid raw jump methods in its own codebase, or mandate structured constructs exclusively, can do so with its Linter — without asking a language to make that choice, once, for every program realized in it.

Structured, unstructured, and domain-named conditionals are paradigms known today on conventional execution models — this document does not claim that list is closed. Nothing in the model couples a control-flow model to a particular computation substrate: a different paradigm can be added as another library over the realization's underlying control-flow primitives, exactly as `IF`/`ELSE` or `GOTO` are added in a realization today.

### Error Propagation
Error propagation is a form of control flow: whenever execution leaves its normal path because a fallible operation failed, control flow changes just as surely as it does inside an `IF`/`ELSE` branch — the only question is which method carries the change. What an error *is*, and what contract it must satisfy to count as one, is defined once, independent of any language, in [The Error](./error.md); this document is concerned only with how execution continues once one has occurred. The Khayyam grammar is one realization-specific illustration: it offers no dedicated error syntax, a choice that belongs to that language's layer — see [The Grammar Refuses Protocol Semantics](../khayyam/khayyam.md#the-grammar-refuses-protocol-semantics).

A method that can fail exposes an explicit error path in the realization's call contract. The protocol requires that path to remain visible and governable; the realization may express it as an output value, a result type, or another explicit mechanism, and its tooling checks that the path is handled or routed.

- **Visible Error Paths:** every fallible operation exposes its error path as an ordinary, named part of the call contract.
- **Explicit Halt Operations:** abrupt execution halts are explicit operations in the realization's library or contract layer, with governance supplied by the appropriate tooling.
- **Tooling-Assisted Routing:** the realization's compiler or Linter helps developers handle and route returned error capsules without making a particular syntax mandatory.

### Topics to be developed here
This document holds the protocol's design directly. Planned topics, each to be added as it is actually designed rather than pre-registered in detail:

- **The conditional-pair protocol** — the contract a well-formed conditional method pair must satisfy: how the condition is evaluated, whether the two branches are symmetric, how the receiver's state is read, and how the pair relates to the presence/absence abstraction family.
- **Iteration and loop-shaped control flow** — the same library-driven treatment applied to repetition, where the condition lives.
- **Halting semantics** — abrupt control transfer (`PANIC()`-family behavior) as an ordinary method call, its contract, and its relationship to error propagation ([The Error](./error.md)).
