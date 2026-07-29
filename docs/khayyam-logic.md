---
Title: "Logic in Khayyam"
Status: Draft
Start Date: "2026-07-29"
ID: "495920"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification defines the `sc` subtype and the `in` import mechanism that library-provided control-flow and arithmetic methods are built on."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: "Depends_on"
      Reason: "The source RFC for Domain-Driven Arithmetic cited Encapsulation as a dependency: arithmetic is expressed as ordinary capsule methods (`a.Add(b)(c, err)`), so it depends on the capsule/method-privacy model defined there. Library-Driven Control Flow's ELSE-must-reference-its-condition rule is also a direct application of that document's Closures as Implicit Capsule Syntax topic (no implicit binding to 'whatever came before')."
    - Title: "Method in Khayyam"
      URI: "./khayyam-method.md"
      Relation: "Depends_on"
      Reason: "Both control flow (IF/ELSE, OnPresent/OnAbsent) and arithmetic (a.Add(b)(c, err)) are ordinary method calls, and inherit that document's pass-by-reference, explicit-output-variable, no-chaining model rather than introducing any dedicated call syntax of their own."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions for library-driven control flow, elimination of logical/arithmetic operators, and the code scope (`sc`) mechanism in the canonical Khayyam specification"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "High"
    Tasks:
      - Works: ["Created this document by merging the standalone Library-Driven Control Flow and Domain-Driven Arithmetic RFCs, together with the Code Scope topic relocated from khayyam-encapsulation.md, into the current Explanation-facet specification"]
        URI: ""
---

# Logic in Khayyam

## Abstract
This document specifies how Khayyam expresses computation and branching without dedicated operator or control-flow syntax. It covers three related pieces: first, the `sc` (code scope) mechanism — the sole syntactic primitive that groups a body of statements to serve as a branch or loop target, itself inert until a library-provided control-flow method (`IF`, `LOOP`, and so on) drives it; second, Library-Driven Control Flow — Khayyam has no `if`/`else`/`for`/`while`/`goto` keywords and no logical operators (`&`, `|`, `!`); all of it is ordinary library-level method calls (`IF`/`ELSE`, domain-specific `OnPresent`/`OnAbsent`, loop constructs driven through the Container ADT), imported explicitly and never auto-imported; third, Domain-Driven Arithmetic — Khayyam has no mathematical or comparison operators (`+`, `-`, `==`, `*`); all arithmetic and comparison are explicit capsule methods with explicit error outputs, with compile-time evaluation available whenever the inputs are statically known.

All three trace to the same underlying commitment: nothing about how a value is computed, compared, or branched on should be hidden behind syntax the compiler treats specially. Every one of these operations remains an ordinary, named, interceptable method call — subject to the same pass-by-reference and no-chaining rules as any other method (see [Method in Khayyam](./khayyam-method.md)).

For a walk-through of the core idea before the detailed rules, see the [Guide](#no-operators-no-control-flow-keywords-at-a-glance) below.

## Introduction

### Motivation
Traditional languages hardcode control flow into the compiler as sacred, unchangeable keywords, forcing one specific paradigm onto every developer and conflicting with specialized architectural constraints in large organizations. There is also a structural reason: Khayyam methods return values through explicit output variables on separate lines (see [Method as Callable Capsule](./khayyam-method.md#method-as-callable-capsule)), so embedding a method call directly inside a traditional `if (method())`-style conditional creates significant parsing ambiguity.

Separately, operations like addition or division are physical, hardware-bound processes that can fail; they are not infallible mathematical abstractions. Traditional syntax (`c = a + b`) leaves no room to return an error, forcing languages to invent dangerous workarounds: hidden panics, exceptions, or silent overflow.

Both problems point to the same fix: replace compiler-special-cased syntax (control-flow keywords, arithmetic/logical operators) with ordinary, named, library-provided methods that can carry an explicit failure path and can be swapped, extended, or governed by an organization's own linter policy without forking the language.

### Methodology

## Explanation

### No Operators, No Control-Flow Keywords At a Glance
Where another language would write:

```
if a + b > threshold {
    process()
} else {
    skip()
}
```

Khayyam code imports the specific behaviors it needs and calls them like any other method:

```khayyam
tp IF in "memar/process/control-flow/if.kh"
tp ELSE in "memar/process/control-flow/else.kh"

vr sum W32
a.Add(b)(sum, addErr)

vr isOverThreshold Bool
sum.IsGreaterThan(threshold)(isOverThreshold)

IF(isOverThreshold, Process)
tp Process sc {
    process.Run()(processErr)
}
ELSE(isOverThreshold, Skip)
tp Skip sc {
    skip.Run()(skipErr)
}
```

Nothing here is compiler magic: `Add` and `IsGreaterThan` are ordinary capsule methods that can fail explicitly, `IF`/`ELSE` are ordinary imported methods, and `Process`/`Skip` are ordinary code scopes (`sc`) — ordinary enough that an organization could replace any of them with its own preferred library without touching the language.

### Code Scope
A code scope is defined with the `sc` subtype:

```khayyam
tp {name} sc { ___ }
```

Code scopes are used in logic methods such as `IF`, `LOOP`, `GOTO`, and other control-flow constructs that will be developed in libraries. A code scope must be used only inside a method body — it cannot appear at the file level or inside a capsule definition outside of a method.

This design ensures that control-flow constructs are not built into the language syntax but are instead provided as library-level abstractions, consistent with Khayyam's philosophy of separating syntax from governance. The language provides the `sc` mechanism; libraries and frameworks provide the specific control-flow implementations.

#### Discussion

##### Drawbacks
Without built-in control-flow syntax, even basic constructs like `if` and `for` require importing a library. This may feel unfamiliar to developers coming from languages where these constructs are keywords, and it adds an import dependency that does not exist in other languages.

##### Rationale and alternatives
- **Built-in control-flow keywords (the conventional approach; rejected)**: would embed specific control-flow semantics into the language, preventing frameworks and organizations from defining their own control-flow policies (e.g., mandatory error checking on each iteration, or logging on each branch).
- **Code scope as a library-only feature without language support (considered, not chosen)**: without the `sc` type, libraries would need to use capsules for control flow, losing the semantic distinction between "a data capsule" and "a control-flow scope."

##### Prior art
Lisp's macro-based control flow and Forth's immediate words are distant precedents for library-defined control flow. No mainstream language provides `sc`-style scope abstractions as a first-class type.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Library-Driven Control Flow
Khayyam strips all traditional control-flow keywords (`if`, `else`, `for`, `while`, `continue`, `retry`, `goto`) and all logical operators (`&`, `|`, `!`) from the language grammar. These behaviors are implemented entirely as library-level method calls (e.g. `tp IF in "memar/process/control-flow/if.kh"`), brought into scope explicitly via `in`, never via implicit/magical auto-import.

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

`ELSE` always takes an explicit reference back to the same condition value it pairs with; it never relies on implicit lexical adjacency to "whatever conditional came before it" — that would reintroduce hidden state binding, which conflicts with the same principle used to reject closures (see [Closures as Implicit Capsule Syntax](./khayyam-encapsulation.md#closures-as-implicit-capsule-syntax)).

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
      // log it with context, return a layer-appropriate error (naming and layering of this error path is an open cross-document question — see Unresolved questions)
      vr logEntry StorageFailureLog
      logEntry.From(saveErr)(logEntry)
      logEntry.AttachContext(self.InstanceID, req.TransactionID)(logEntry)
      self.LogSink.Record(logEntry)()
      err = ErrPaymentTemporarilyUnavailable
  }
}
```

The name `OnAbsent` / `OnPresent` directly expresses the semantics of the check (is an error *present* or *absent*?), which is both self-documenting and visually distinct — the two branch names cannot be confused for each other by a reader skimming a diff, unlike a pair built by negation prefix (the naming convention for such presence/absence or success/failure branch pairs is an open cross-document discussion — see Unresolved questions).

This pattern generalizes: whenever a capsule result has a natural binary or multi-way interpretation meaningful to its domain (valid/invalid, found/not-found, granted/denied), the capsule itself should expose conditional methods by those names, so the calling code never reduces a rich domain event to a naked boolean check.

Looping is built the same way: low-level compiler-intrinsic jump methods replace `while`/`for`/`do-while`, but collection iteration MUST be driven through the Container ADT, never manual pointer/index manipulation.

#### Mechanism Summary
- **Syntax Minimalism:** foundational execution jumps and condition evaluations are standard method calls (Compiler Intrinsics) tied to specific execution contexts, not reserved words.
- **Library-Level Abstraction:** advanced control flow (Ruby-style `retry`, `continue`) is implemented purely as libraries/modular packages.
- **Explicit Scope & Tooling Assistance:** the compiler never performs implicit auto-imports of control-flow libraries; everything is explicit via `in`. An LSP/Developer Assistant is relied on to reduce the resulting friction without introducing compiler magic.
- **Linter Governance over Compiler Dictatorship:** organizations can configure their Linter to block raw intrinsic jump methods and mandate their own approved control-flow libraries, without touching the language core.
- **Elimination of Logical Operators:** `&`, `|`, `!` do not exist in the grammar; boolean/conditional logic is expressed via explicit capsule methods. The compiler guarantees these explicit method chains are optimized directly into atomic hardware bitwise instructions (`AND`/`OR`), so syntactic purity does not cost hardware efficiency.

#### Discussion

##### Drawbacks
Every conditional, even a trivial one, requires an explicit import and a named scope rather than a single keyword and a brace block — substantially more ceremony for the simplest possible program logic. This is accepted as the price of removing all compiler-level special-casing of control flow.

##### Rationale and alternatives
Keeping `if`/`else`/`for` as compiler keywords (the universal default in other languages) was rejected because it permanently couples one specific control-flow paradigm to the compiler, leaving no path for an organization to enforce a different one without forking the language.

##### Prior art
No mainstream general-purpose language fully removes conditional/loop keywords from its grammar; Forth-family languages and some Lisp dialects come closest by treating control flow as ordinary words/forms rather than special syntax.

##### Unresolved questions
The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open — the original RFC pointed to a dedicated naming-discussion RFC that has not yet been supplied to this document set; see this document's own Unresolved questions.

##### Future possibilities
A richer standard library of named, domain-flavored conditional methods is expected to grow over time.

### Domain-Driven Arithmetic
Khayyam provides no mathematical or logical operators (`+`, `-`, `==`, `*`). All operations are explicit methods on a capsule (e.g. `a.Add(b)(c, err)`), so the possibility of failure (overflow, division by zero) is always visible in the method's signature rather than hidden behind syntactic sugar.

Where another language would write `c = a + b`, Khayyam code calls a method directly on the domain capsule: `a.Add(b)(c, err)`. For simple operations, this method lives directly on the relevant domain capsule (e.g. a `Money` capsule exposing its own `Add`/`Sum` method, which can also enforce domain rules like currency matching while it's at it). For complex formulas where writing nested method calls would be unwieldy, developers may instead pass the formula as a string to a specialized evaluator capsule (e.g. `MathEval.FromString("x = (-b + sqrt(b^2 - 4ac)) / 2a")`). When the parameters to such a formula are compile-time constants, the compiler evaluates the deterministic, pure logic at compile time automatically — the same way a regex engine pre-compiles its automaton from a literal pattern — so this is not a runtime-only escape hatch; it carries the same compile-time guarantees as the direct method-call form whenever its inputs are known statically.

#### Mechanism Summary
- No `+`, `-`, `*`, `==`, or similar tokens exist in the grammar.
- Arithmetic and comparison are always explicit capsule methods with explicit error outputs.
- `MathEval.FromString()` (or equivalent) handles complex formulas via string input, with compile-time evaluation when inputs are invariant.

Like every other method call in Khayyam, `a.Add(b)(c, err)` is a statement, not a chainable expression — writing `a.Add(b).Multiply(c)` is not legal syntax any more than it would be for a non-arithmetic method. A formula deep enough to need several such calls is, by the same reasoning documented for methods generally, a signal to reach for `MathEval` rather than a reason to want expression chaining (see [Composition Depth as a Decomposition Signal](./khayyam-method.md#composition-depth-as-a-decomposition-signal-no-expression-chaining)).

#### Discussion

##### Drawbacks
Even trivial arithmetic requires a method call rather than an infix operator, which is significantly more verbose than virtually every other language in existence. For formulas passed as strings, type-checking of the formula's inner operands (e.g. preventing `Money + Duration`) depends on the specific evaluator capsule's implementation rather than being a language-level guarantee — this is currently an open design question for the standard `MathEval` implementation specifically (see Unresolved questions).

##### Rationale and alternatives
Built-in infix operators (the universal default) were rejected because they structurally cannot express a failure path, which conflicts with Khayyam's broader principle that no control flow, including failure handling, should ever be hidden behind syntax (the same principle Library-Driven Control Flow applies to branching).

##### Prior art
Domain-modeling-heavy codebases in many languages already wrap arithmetic in named methods for business types (e.g. `Money.add()` in DDD-style Java/C# code) as a best practice; Khayyam makes this the *only* available path rather than an optional convention.

##### Unresolved questions
Whether the standard `MathEval.FromString()`-style evaluator performs full compile-time type-checking of formula operands (preventing nonsensical cross-type operations like adding incompatible domain quantities), or only validates syntax while deferring type errors to runtime, is not yet settled for the recommended framework implementation.

##### Future possibilities
None recorded yet.

## Results

## Discussion

### Drawbacks
Together, these rules mean that every branch, every loop, and every arithmetic or comparison operation in Khayyam is an explicit, named, importable method call rather than built-in syntax. This is substantially more verbose than virtually any mainstream language for the simplest possible program logic — a single comparison and branch that would be one line elsewhere becomes an import, a method call, two named code scopes, and (if a domain-specific name doesn't already exist) a call to a generic `IF`/`ELSE` pair. This is accepted uniformly across both control flow and arithmetic as the price of never hiding a failure path or a branching decision behind syntax the compiler treats specially.

### Rationale and alternatives
Both control flow and arithmetic trace to the same rejected alternative: built-in, compiler-special-cased syntax (keywords for branching/looping, infix operators for computation). Both were rejected for the same structural reason — such syntax cannot carry an explicit failure path and permanently couples one paradigm to the compiler, leaving no way for an organization to govern or replace it without forking the language. Library-provided methods, by contrast, can be swapped, extended, linted, or restricted entirely at the organizational level.

### Prior art
No mainstream general-purpose language fully removes both operators and control-flow keywords from its grammar. Forth-family languages and some Lisp dialects come closest for control flow; DDD-style wrapping of arithmetic in named methods (e.g. `Money.add()`) is common practice, but optional, in mainstream object-oriented languages. Khayyam is unusual in making both of these the *only* available path rather than a convention layered on top of operators/keywords that still exist underneath.

### Unresolved questions
1. The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open.
2. Whether the standard `MathEval.FromString()`-style evaluator performs full compile-time type-checking of formula operands is not yet settled.
3. The source RFCs for this document referenced several other RFCs by number (000009, 000010, 000020) for foundational type-system rules, method-output mechanics, layer-appropriate error handling, and branch-naming conventions. Some of these have since been identified and merged elsewhere in this document set (e.g. the method-output mechanic is now [Method as Callable Capsule](./khayyam-method.md#method-as-callable-capsule)); others have not yet been supplied and their content is unverified from this document's perspective.

### Future possibilities
- A richer standard library of named, domain-flavored conditional methods is expected to grow over time.
- A formal specification for compile-time type-checking of `MathEval`-style formula operands.

## Change Rationale
- **Initial creation.** Created by merging the standalone "Library-Driven Control Flow" and "Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation" RFCs into the current Explanation-facet specification, together with the "Code Scope" topic relocated from `khayyam-encapsulation.md` (code scopes are the primitive `IF`/`ELSE`/`LOOP` are built on, not a capsule-level concern). Both standalone RFC files, and the Code Scope section in `khayyam-encapsulation.md`, have been retired/removed accordingly. Numbered RFC cross-references in the original source text (RFC 000009, 000010, 000020) were preserved in substance but could not all be resolved to real documents in this document set; resolved ones were re-linked, unresolved ones are logged under Unresolved questions rather than guessed at.
