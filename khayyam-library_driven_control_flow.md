---
RFC Number: 000003
Title: "Library-Driven Control Flow"
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
Khayyam strips all traditional control-flow keywords (`if`, `else`, `for`, `while`, `continue`, `retry`, `goto`) and all logical operators (`&`, `|`, `!`) from the language grammar. These behaviors are implemented entirely as library-level method calls (e.g. `tp IF in "memar/process/control-flow/if.kh"`), brought into scope explicitly via `in`, never via implicit/magical auto-import.

## Motivation
Traditional languages hardcode control flow into the compiler as sacred, unchangeable keywords, forcing one specific paradigm onto every developer and conflicting with specialized architectural constraints in large organizations. There is also a structural reason: Khayyam methods return values through explicit output variables on separate lines (RFC 000004), so embedding a method call directly inside a traditional `if (method())`-style conditional creates significant parsing ambiguity.

## Guide-level explanation

### The generic form: IF/ELSE

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

`ELSE` always takes an explicit reference back to the same condition value it pairs with; it never relies on implicit lexical adjacency to "whatever conditional came before it" — that would reintroduce hidden state binding, which conflicts with the same principle used to reject closures (RFC 000005).

### The preferred form: domain-specific conditional methods

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
      // log it with context, return a layer-appropriate error (see RFC 000010)
      vr logEntry StorageFailureLog
      logEntry.From(saveErr)(logEntry)
      logEntry.AttachContext(self.InstanceID, req.TransactionID)(logEntry)
      self.LogSink.Record(logEntry)()
      err = ErrPaymentTemporarilyUnavailable
  }
}
```

The name `OnAbsent` / `OnPresent` directly expresses the semantics of the check (is an error *present* or *absent*?), which is both self-documenting and visually distinct — the two branch names cannot be confused for each other by a reader skimming a diff, unlike a pair built by negation prefix (see RFC 000020 for the open naming discussion).

This pattern generalizes: whenever a capsule result has a natural binary or multi-way interpretation meaningful to its domain (valid/invalid, found/not-found, granted/denied), the capsule itself should expose conditional methods by those names, so the calling code never reduces a rich domain event to a naked boolean check.

Looping is built the same way: low-level compiler-intrinsic jump methods replace `while`/`for`/`do-while`, but collection iteration MUST be driven through the Container ADT, never manual pointer/index manipulation.

## Reference-level explanation
- **Syntax Minimalism:** foundational execution jumps and condition evaluations are standard method calls (Compiler Intrinsics) tied to specific execution contexts, not reserved words.
- **Library-Level Abstraction:** advanced control flow (Ruby-style `retry`, `continue`) is implemented purely as libraries/modular packages.
- **Explicit Scope & Tooling Assistance:** the compiler never performs implicit auto-imports of control-flow libraries; everything is explicit via `in`. An LSP/Developer Assistant is relied on to reduce the resulting friction without introducing compiler magic.
- **Linter Governance over Compiler Dictatorship:** organizations can configure their Linter to block raw intrinsic jump methods and mandate their own approved control-flow libraries, without touching the language core.
- **Elimination of Logical Operators:** `&`, `|`, `!` do not exist in the grammar; boolean/conditional logic is expressed via explicit capsule methods. The compiler guarantees these explicit method chains are optimized directly into atomic hardware bitwise instructions (`AND`/`OR`), so syntactic purity does not cost hardware efficiency.

## Drawbacks
Every conditional, even a trivial one, requires an explicit import and a named scope rather than a single keyword and a brace block — substantially more ceremony for the simplest possible program logic. This is accepted as the price of removing all compiler-level special-casing of control flow.

## Rationale and alternatives
Keeping `if`/`else`/`for` as compiler keywords (the universal default in other languages) was rejected because it permanently couples one specific control-flow paradigm to the compiler, leaving no path for an organization to enforce a different one without forking the language.

## Prior art
No mainstream general-purpose language fully removes conditional/loop keywords from its grammar; Forth-family languages and some Lisp dialects come closest by treating control flow as ordinary words/forms rather than special syntax.

## Unresolved questions
The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open — see RFC 000020.

## Future possibilities
A richer standard library of named, domain-flavored conditional methods is expected to grow over time; see RFC 000020.
