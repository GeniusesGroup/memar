---
Title: "Control Flow in Khayyam"
Status: Draft
Start Date: "2026-07-29"
ID: "495920"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification defines the `sc` subtype and the `in` import mechanism that library-provided control-flow methods are built on."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: "Depends_on"
      Reason: "Library-Defined Control Flow's ELSE-must-reference-its-condition rule is a direct application of that document's Closures as Implicit Capsule Syntax topic (no implicit binding to 'whatever came before')."
    - Title: "Method in Khayyam"
      URI: "./khayyam-method.md"
      Relation: "Depends_on"
      Reason: "Control flow (IF/ELSE, OnPresent/OnAbsent) is built entirely from ordinary method calls, and inherits that document's pass-by-reference, explicit-output-variable, no-chaining model rather than introducing any dedicated call syntax of its own."
    - Title: "The Error"
      URI: "./error.md"
      Relation: "Depends_on"
      Reason: "Error Propagation treats `Error` (and its concrete subtypes) as the value being propagated; what the abstraction itself is, and what contract it must satisfy, is defined there, not here."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions for library-driven control flow, elimination of logical/arithmetic operators, and the code scope (`sc`) mechanism in the canonical Khayyam specification"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://chatgpt.com/"
    Model: "Unspecified (custom GPT; exact underlying model not recorded — fill in if known)"
    Effort: "High"
    Tasks:
      - Works: ["Proposed extracting Domain-Driven Arithmetic out of this document, reframing Error Handling as Error Propagation (a form of control flow rather than an unrelated concern), separating what the compiler provides (execution primitives) from what libraries build on top of it, and reframing Structured Programming historically rather than as an unquestioned default"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "High"
    Tasks:
      - Works: ["Created this document by merging the standalone Library-Driven Control Flow and Domain-Driven Arithmetic documents, together with the Code Scope topic relocated from khayyam-encapsulation.md, into the current Explanation-facet specification", "Applied the architectural review agreed between the author and ChatGPT: promoted the compiler-exposes-primitives-only conclusion into the Abstract as a stated outcome, split a new Execution Primitives topic out of Library-Driven Control Flow (renamed Library-Defined Control Flow), expanded Structured Programming into a full Structured vs Unstructured Programming topic with its own Discussion bundle, renamed and reframed Error Handling as Error Propagation, and removed residual Domain-Driven Arithmetic content (comparison-operator examples aside) following its extraction to khayyam-variable.md"]
        URI: ""
---

# Control Flow in Khayyam

## Abstract
In software, [control flow](https://en.wikipedia.org/wiki/Control_flow) (or flow of control) describes how execution progresses from one command to the next. In many contexts, such as machine code and an imperative programming language, control progresses sequentially (to the command located immediately after the currently executing command) except when a command transfers control to another point – in which case the command is classified as a control flow command. Depending on context, other terms are used instead of command. For example, in machine code, the typical term is instruction and in an imperative language, the typical term is statement.

This document specifies how Khayyam expresses branching, looping, and failure propagation without any dedicated control-flow keyword or logical operator in the language grammar. It covers two related pieces: first, the `sc` (code scope) mechanism — the sole syntactic primitive that groups a body of statements to serve as a branch or loop target, itself inert until a library-provided control-flow method (`IF`, `LOOP`, and so on) drives it; second, Library-Defined Control Flow — Khayyam has no `if`/`else`/`for`/`while`/`goto` keywords and no logical operators (`&`, `|`, `!`); every branch, every loop, and every error-propagation path is an ordinary, named, library-provided method call (`IF`/`ELSE`, domain-specific `OnPresent`/`OnAbsent`, loop constructs driven through the Container ADT), imported explicitly and never auto-imported.

Working through both pieces in detail leads to a single architectural conclusion, rather than starting from one: Khayyam's compiler does not choose or privilege any control-flow model. It exposes only the minimal execution primitives — code scopes and a small set of compiler-intrinsic jump instructions — required to construct one. Every named control-flow abstraction built on those primitives, whatever paradigm it belongs to (structured branching and iteration, unrestricted jumps, retry loops, or a domain-specific presence/absence check — the paradigms known today, on today's conventional hardware; the list is not closed), is a library or framework decision, never a language one — and, critically, none of them is a fallback confined to cases where the "real" options don't fit: a domain-named method like `OnAbsent`/`OnPresent` is frequently the better choice, not a stylistic variant of `IF`/`ELSE`. Khayyam does not reject any control-flow paradigm; it only refuses to encode one of them permanently into its own syntax.

One thing this document does not cover, by deliberate scope decision rather than oversight: a method call is itself, structurally, a control-flow event — execution transfers to another location and, in Khayyam's pass-by-reference model, returns. Khayyam treats Method as a more foundational Type in its own right (see [Method in Khayyam](./khayyam-method.md)) rather than as one more topic in this document, because a capsule's ability to be called at all precedes any question of which control-flow paradigm calls it. This document is not hiding that relationship; it is simply drawn one layer above it.

For a walk-through of the core idea before the detailed rules, see the [Guide](#no-control-flow-keywords-no-logical-operators-at-a-glance) below.

## Introduction

### Motivation
Traditional languages hardcode control flow into the compiler as sacred, unchangeable keywords, forcing one specific paradigm onto every developer and conflicting with specialized architectural constraints in large organizations. There is also a structural reason: Khayyam methods return values through explicit output variables on separate lines (see [Method as Callable Capsule](./khayyam-method.md#method-as-callable-capsule)), so embedding a method call directly inside a traditional `if (method())`-style conditional creates significant parsing ambiguity.

The historical debate over which control-flow constructs a language *should* privilege — structured programming's `if`/`while`/`for` against the older, hardware-native `goto` — has largely been settled in mainstream language design, in favor of structured constructs (see [Structured vs Unstructured Programming](#structured-vs-unstructured-programming) below). Khayyam treats that outcome as informative rather than binding: it confirms that most code reads and maintains better as structured constructs, not that a compiler must forbid the alternative, or make either one a privileged part of its own grammar, forever.

Both observations point to the same fix: replace compiler-special-cased syntax (control-flow keywords, logical operators) with ordinary, named, library-provided methods that can carry an explicit failure path and can be swapped, extended, or governed by an organization's own linter policy without forking the language.

### Methodology
This document's terminology and structure were refined through explicit dialectical review across multiple AI systems (ChatGPT and Claude), rather than settled in a single pass — consistent with this project's general practice of treating cross-model critique as part of the design process itself, not just its write-up. Disagreements surfaced during that review (for example, whether "Library-Driven" or a broader "primitives vs. abstractions" framing better describes the underlying architectural commitment) are recorded in this document's Discussion sections rather than silently resolved.

## Explanation

### No Control-Flow Keywords, No Logical Operators At a Glance
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

Nothing here is compiler magic: `Add` and `IsGreaterThan` are ordinary capsule methods that can fail explicitly — how arithmetic and comparison are modeled is the subject of [Variable in Khayyam](./khayyam-variable.md), not this document — `IF`/`ELSE` are ordinary imported methods, and `Process`/`Skip` are ordinary code scopes (`sc`), ordinary enough that an organization could replace any of them with its own preferred library without touching the language.

### Structured vs Unstructured Programming
[Structured programming](https://en.wikipedia.org/wiki/Structured_programming) emerged as a reaction to unrestricted [`goto`](https://en.wikipedia.org/wiki/Goto)-based control flow. Dijkstra's influential critique argued that arbitrary jumps make a subroutine's execution path impossible to reason about locally, and proposed replacing them with three composable constructs — sequence, selection (`if`/`else`), and iteration (`for`/`while`) — that keep control flow representable as nested, well-scoped blocks. [Unstructured programming](https://en.wikipedia.org/wiki/Unstructured_programming), built on unrestricted jumps, is closer to the underlying hardware execution model and predates it; it is still how most compiled code looks once structured constructs are lowered to machine instructions.

Most languages designed since resolved this debate once, permanently, in the compiler: structured constructs became reserved keywords, and `goto` was either removed entirely or kept as a discouraged, restricted escape hatch. Khayyam treats this as the wrong place to resolve it. The argument for preferring structured constructs in most application code is not in dispute here — it is an argument about what most programs should look like, not about what a compiler is capable of expressing. Baking that preference into the grammar as privileged keywords does not make unstructured control flow disappear from the domains that genuinely rely on it — state machines, coroutine schedulers, generated code, interpreter dispatch loops — it just forces those domains to route around the language, or wrap `goto` in a permanent warning label, forever.

Khayyam supports both models as ordinary library constructs built on the same underlying primitives (see [Code Scope](#code-scope) and [Execution Primitives: The Compiler's Role](#execution-primitives-the-compilers-role) below): a `GOTO`-style jump method is exactly as valid, and exactly as unprivileged, as an `IF`/`ELSE` pair. Neither is a keyword; neither is forbidden by the language. An organization that wants to forbid raw jump methods in its own codebase, or mandate structured constructs exclusively, can do so with its Linter — without asking the language to make that choice, once, for every Khayyam program that will ever be written.

Structured, unstructured, and domain-named conditionals are simply the paradigms known today, on today's conventional, classical-hardware execution model — this document does not claim that list is closed. Nothing in Khayyam couples a control-flow model to a particular computation substrate: if a fundamentally different paradigm arrives — quantum computing's superposition-based branching, for instance — it does not need to be hacked into the language or wait for a compiler update; it is built as another library on the same `sc`/jump-intrinsic primitives already described here, exactly like `IF`/`ELSE` or `GOTO` are today.

#### Discussion

##### Drawbacks
This is a narrower drawback than it first looks, but not a fake one. It is not that Khayyam creates more room for developers to diverge in style than a language with a built-in `if` does — every language has exactly as much room for that (guard clauses vs. nested `if`, early return vs. exception-driven flow, and so on); it is just invisible at the call site, because the keyword itself never changes no matter how differently it is used. What Khayyam's model changes is *where* that divergence becomes visible: a newcomer has to identify which control-flow library a file is importing before they can read it fluently, rather than recognizing `if` on sight regardless of house style. That is real onboarding friction, and it is exactly why an organization is expected to standardize on one control-flow library per project via its Linter — the same way it already standardizes on one logging library or one HTTP client, rather than leaving that choice to sit in the language.

##### Rationale and alternatives
- **Structured-only (the mainstream default; rejected as a language-level mandate)**: removing `goto`-equivalents from the grammar entirely, as most modern languages do, was rejected because it permanently forecloses the domains that legitimately need unrestricted jumps, forcing them to simulate `goto` with labeled loops, exception-based jumps, or other awkward workarounds.
- **Unstructured-only / goto-first (rejected)**: no serious contemporary language proposes this, and Khayyam does not either; it is listed only to make clear that Khayyam is not reviving unstructured programming as a preferred style, merely refusing to forbid it at the language level.
- **Structured by convention, not by keyword (chosen)**: neither model is privileged in the grammar; an organization's Linter is expected to enforce whichever convention that organization prefers, exactly as it would enforce any other house style.
- **Domain-named conditional methods as the actual default reach, not a stylistic footnote (chosen alongside `IF`/`ELSE`)**: see [Domain-Specific Conditional Methods](#the-preferred-form-domain-specific-conditional-methods) below. This is not a third position in the structured-vs-unstructured debate so much as a demonstration that the debate's own vocabulary (`if`, `goto`) is too narrow to describe the best available option once a domain is stable enough to name its own conditions — a check like `saveErr.OnAbsent(...)` is neither a generic `if` nor a `goto`, and reads better than either.

##### Prior art
Dijkstra's "Go To Statement Considered Harmful" is the canonical argument for structured programming; Knuth's "Structured Programming with go to Statements" is the canonical rebuttal, arguing that disciplined, restricted use of `goto` is sometimes clearer than the structured alternative. Most mainstream languages since have sided fully with the structured camp at the grammar level; Khayyam's position is closer to Knuth's — that the discipline matters more than the mechanism — but pushes it further by refusing to encode either side into the compiler. Built-in syntax is not immune to instability either: Go's `for`-loop variable-capture semantics changed in Go 1.22, silently altering the behavior of existing code that relied on the previous per-loop (rather than per-iteration) scoping — a reminder that a compiler-owned keyword can still change meaning out from under a codebase whenever its authors decide to revisit it. A library-owned control-flow method's behavior, by contrast, only changes when the codebase's own dependency version does, under that codebase's own control.

##### Unresolved questions
None at this time.

##### Future possibilities
A standard-library `GOTO`/jump-based control-flow package, alongside the structured `IF`/`LOOP` family, is expected to exist so the unstructured path is not merely theoretical.

### Code Scope
Any control-flow abstraction needs some representation of "the code to run if this branch is taken" before it can do anything else — a value that is not data, but a deferred body of statements. Khayyam provides exactly one primitive for this: the code scope.

A code scope is defined with the `sc` subtype:

```khayyam
tp {name} sc { ___ }
```

Code scopes are used in logic methods such as `IF`, `LOOP`, `GOTO`, and other control-flow constructs that will be developed in libraries. A code scope must be used only inside a method body — it cannot appear at the file level or inside a capsule definition outside of a method.

This design ensures that control-flow constructs are not built into the language syntax but are instead provided as library-level abstractions, consistent with Khayyam's philosophy of separating syntax from governance. The language provides the `sc` mechanism; libraries and frameworks provide the specific control-flow implementations.

#### Discussion

##### Drawbacks
Even a basic construct like `if` or `for` requires an explicit import rather than a keyword the compiler already knows — a real, honest one-time cost per file (the `in` statement), and unfamiliar at first for developers used to keyword syntax. What this should not be read to imply is that keyword-based languages avoid an equivalent cost: they pay it once, permanently, inside the compiler's own source, where it cannot be inspected, customized, or upgraded without forking the language itself. Khayyam's version of that same design cost is visible in application code and, once paid by a library author, becomes a stable, shared reference every caller in the codebase imports rather than reinvents.

##### Rationale and alternatives
- **Built-in control-flow keywords (the conventional approach; rejected)**: would embed specific control-flow semantics into the language, preventing frameworks and organizations from defining their own control-flow policies (e.g., mandatory error checking on each iteration, or logging on each branch).
- **Code scope as a library-only feature without language support (considered, not chosen)**: without the `sc` type, libraries would need to use capsules for control flow, losing the semantic distinction between "a data capsule" and "a control-flow scope."

##### Prior art
Lisp's macro-based control flow and Forth's immediate words are distant precedents for library-defined control flow. No mainstream language provides `sc`-style scope abstractions as a first-class type.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Execution Primitives: The Compiler's Role
Beyond the `sc` subtype itself, the compiler exposes a small, fixed set of low-level, compiler-intrinsic jump and branch instructions — the same category of instruction a `goto`, an `if`, and a `while` all eventually lower to in any language's compiled output, regardless of which keyword the source code used to express them. These intrinsics are themselves scoped to today's conventional, classical-hardware execution model; nothing about that scoping is assumed to be permanent (see [Structured vs Unstructured Programming](#structured-vs-unstructured-programming) above). They carry no naming, error-handling, or usage convention of their own, and are not meant to be called directly by ordinary application code; they are the raw material a library uses to build a named, well-behaved control-flow method.

This is the entirety of the compiler's involvement in control flow: a way to group statements (`sc`) and a way to jump between them (compiler intrinsics). Everything else — what a jump is named, when it fires, what data it carries, whether it is packaged as `IF`, `GOTO`, `retry`, or a domain-specific presence check, and which paradigm it belongs to — is a library decision, not a compiler one.

#### Discussion

##### Drawbacks
This is not a cost unique to Khayyam so much as a cost every language pays, made visible here instead of hidden. Some author, somewhere, has to decide what a condition-evaluation shape looks like, how it surfaces errors, and what a Linter-friendly form of it is. In a language with a built-in `if`/`while`, that design work happened once, inside the compiler's own source, by the language's original authors — invisible to every developer who uses it, and effectively frozen for as long as the language exists (see the Go loop-variable example under [Structured vs Unstructured Programming](#structured-vs-unstructured-programming) for what happens when a language's own authors decide to revisit it anyway). In Khayyam, the same design work happens once, by a library author, in ordinary application-visible code — inspectable, forkable, and versioned like any other dependency, rather than a permanent, unexaminable property of the language. The genuine residual drawback is narrower than "extra ceremony": before an established control-flow package exists in a given codebase, whoever writes the first one has to make these decisions themselves rather than inherit a compiler default. This is a real but shallow, one-time setup cost, not an ongoing structural one — it does not meaningfully slow a team's path to high productivity once that first reference implementation exists.

##### Rationale and alternatives
- **A larger compiler-provided intrinsic set, closer to a mini standard library (considered, not chosen)**: would shrink the bootstrapping gap for common cases, but reintroduces the core problem this document exists to avoid — the compiler quietly acquiring opinions about which control-flow shapes are "common" or "standard," permanently, for every program that will ever run on it.
- **No intrinsics at all, everything reconstructed from raw hardware jumps by each library (rejected)**: would make every control-flow library reimplement the same low-level, error-prone plumbing, with no consistency guarantee across libraries.

##### Prior art
This mirrors how most compiled languages already treat their own backends: `if`/`while`/`for` all lower to the same small set of conditional-jump instructions at the machine-code level. Khayyam is unusual only in exposing that lowering boundary to library authors directly, rather than hiding it entirely behind compiler-owned keywords.

##### Unresolved questions
The precise, stable set of compiler-intrinsic jump instructions has not been enumerated in a public specification yet.

##### Future possibilities
A formal, versioned specification of the intrinsic instruction set, so third-party control-flow libraries can target it without depending on compiler internals.

### Library-Defined Control Flow
Khayyam strips all traditional control-flow keywords (`if`, `else`, `for`, `while`, `continue`, `retry`, `goto`) and all logical operators (`&`, `|`, `!`) from the language grammar. Every control-flow abstraction built on the primitives above — however it is named, and regardless of which paradigm it belongs to — is implemented entirely as a library-level method call (e.g. `tp IF in "memar/process/control-flow/if.kh"`), brought into scope explicitly via `in`, never via implicit/magical auto-import. "Library-defined" describes how these abstractions are packaged today, not a constraint the language itself imposes: nothing prevents a future code generator, compiler-intrinsics-aware framework, or an organization's own toolchain from producing the same abstractions through a different mechanism, as long as they are still built from the primitives above rather than added to the grammar.

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
      // log it with context, return a layer-appropriate error (naming and layering of this error path is an open question — see Unresolved questions)
      vr logEntry StorageFailureLog
      logEntry.From(saveErr)(logEntry)
      logEntry.AttachContext(self.InstanceID, req.TransactionID)(logEntry)
      Logger.DispatchEvent(logEntry)()
      err = ErrPaymentTemporarilyUnavailable
  }
}
```

The name `OnAbsent` / `OnPresent` directly expresses the semantics of the check (is an error *present* or *absent*?), which is both self-documenting and visually distinct — the two branch names cannot be confused for each other by a reader skimming a diff, unlike a pair built by negation prefix (the naming convention for such presence/absence or success/failure branch pairs is still an open question — see Unresolved questions).

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
Every conditional, even a trivial one, needs an explicit import and a named scope rather than a single keyword and a brace block — more characters at the call site than a keyword-based language, and that much is a plain, honest fact. What it is not is a hidden cost other languages avoid: a built-in `if` looks free at the call site precisely because its design cost was paid once, permanently, inside the compiler, while the convention around it — how it interacts with error handling, whether a check reads as a naked boolean or a named domain condition — is left to diverge silently, unpaid for, between call sites and teams. In Khayyam, once `IF`/`ELSE` or a domain-named pair like `OnPresent`/`OnAbsent` exists in a codebase, every subsequent call site imports that same reference implementation rather than re-deciding the same shape; the up-front verbosity buys one inspectable, swappable answer to "how do we branch here," instead of a keyword whose actual behavior around errors, logging, or domain meaning still gets reinvented ad hoc at every call site anyway.

##### Rationale and alternatives
Keeping `if`/`else`/`for` as compiler keywords (the universal default in other languages) was rejected — not because it is free, it is not, the same design decisions still have to be made, just once, by the language's original authors, and then frozen for every program that will ever run on it — but because it permanently couples one specific control-flow paradigm to the compiler, leaving no path for an organization to enforce a different one, or to reach for something more expressive like a domain-named conditional method (see [Domain-Specific Conditional Methods](#the-preferred-form-domain-specific-conditional-methods) above), without forking the language.

##### Prior art
No mainstream general-purpose language fully removes conditional/loop keywords from its grammar; Forth-family languages and some Lisp dialects come closest by treating control flow as ordinary words/forms rather than special syntax.

##### Unresolved questions
The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open.

##### Future possibilities
A richer standard library of named, domain-flavored conditional methods is expected to grow over time.

### Error Propagation
Error propagation is a form of control flow: whenever execution leaves its normal path because a fallible operation failed, control flow changes just as surely as it does inside an `IF`/`ELSE` branch — the only question is which method carries the change. What an error *is*, and what contract it must satisfy to count as one, is defined once, independent of any language, in [The Error](./error.md); this document is concerned only with how execution continues once one has occurred, inside Khayyam specifically.

Other languages answer that same question — how does execution continue after failure? — with different mechanisms, each a different point in the same trade-off space between visibility, verbosity, and compiler involvement: exceptions unwind the call stack via `throw`/`catch` (Java, Python, JS); Rust's `Result<T, E>` makes failure an ordinary return value inspected via pattern matching, with `?` as sugar for propagating it upward; Go returns an explicit `(value, error)` pair checked with `if err != nil`; and a panic/recover pair combines an abrupt halt with an opt-in unwinding mechanism (Go, and Khayyam's own `PANIC()`). Khayyam has no `try-catch`, `panic`/`recover`, or `?`-operator syntax of its own. Errors are always ordinary, explicit output values (capsules implementing the `Error` abstraction), and abrupt halts are an ordinary standard-library method call (e.g. `PANIC()`), not a compiler directive — closest in spirit to Go's explicit returns, but with the "did you check it" discipline shifted from mandatory boilerplate to the Linter.

A method that can fail declares an explicit `Error`-typed (or, where appropriate, a specific error-capsule-typed) output, exactly like any other output variable. The developer is not required to write any special syntax to "catch" it, but the Linter is relied upon to ensure every returned error is actually inspected/routed rather than silently discarded, instead of the compiler enforcing this via dedicated syntax.

- **No Hidden Control Flow:** no operator may mask an early return; every fallible operation's error path is a normal, visible output variable.
- **No Core-Level Panics:** abrupt execution halts are implemented as standard library methods (e.g. `PANIC()` in the Memar framework), not compiler directives or special syntax.
- **Linter Over Syntax:** instead of Go-style mandatory boilerplate, the compiler/linter ensures developers explicitly handle or route returned error capsules.
- **Covariant Error Returns:** a method may declare its error output as the generic `Error` abstraction, or as a specific concrete error capsule type directly (e.g. `(err ErrServiceNotFound)` instead of `(err Error)`), as long as that concrete type itself implements the `Error` abstraction. This is not considered a violation of the abstraction's contract, and gives callers static, compile-time knowledge of exactly which error type to expect without any runtime type-narrowing/reflection mechanism being required in the language. (The contract this covariance must satisfy is defined by the `Error` abstraction itself, in [The Error](./error.md) — this bullet only concerns the propagation channel's typing, not the abstraction's contract.)

#### Discussion

##### Drawbacks
Without compiler-enforced syntax (like Rust's `?` or Go's required `if err != nil` pattern that at least makes ignoring an error visually obvious), the actual discipline of "every error gets handled" depends entirely on Linter configuration and developer diligence — see [Memory Model](./khayyam-memory_model.md) for the equivalent trade-off in memory safety. A team running a weak or disabled Linter could silently drop errors with no language-level safety net at all.

##### Rationale and alternatives
A `try-catch`/exception model was rejected for hiding control flow in implicit stack unwinding. Rust's `?` operator was rejected for binding the compiler to one specific result type and for hiding an early return behind an operator. Go's mandatory verbose boilerplate was rejected as unnecessary ceremony once a strict Linter can enforce the same discipline without forcing every call site to spell it out manually.

##### Prior art
Rust's `Result`/`?`, Go's explicit `(value, error)` returns with manual checks, and exception-based models (Java, Python, JS) were all considered as the dominant prior art in this space; Khayyam's approach is closest in spirit to Go's explicit returns, but moves the "did you check it" enforcement from required syntax to tooling.

##### Unresolved questions
None at this time for the core propagation mechanism. See [The Error](./error.md) for the separate, framework-level question of when a low-level error should be translated/logged rather than propagated verbatim, and the "Conditional Method Naming Convention (Presence/Absence Pattern)" discussion (not yet a separate document) for the open question of standard conditional-method naming for branching on error/success.

##### Future possibilities
None recorded yet.

## Results

## Discussion

### Drawbacks
Together, these rules mean that every branch, every loop, every jump, and every error-propagation path in Khayyam is an explicit, named, importable method call rather than built-in syntax — more characters to type than virtually any mainstream language for the simplest possible program logic, and that much is a plain fact rather than a trade-off in disguise. What should not be read into it is that the equivalent design cost doesn't exist in languages with built-in keywords: it does, it is simply paid once by the language's own authors, hidden inside the compiler, and frozen for the language's entire lifetime rather than owned by the codebase using it. Khayyam's version of the cost is paid once too — by whoever writes the `IF`/`ELSE` or domain-named library a project settles on — and after that, every call site imports the same answer rather than re-deciding it. This is accepted as the price of keeping that design cost visible, inspectable, and owned by the codebase, rather than owned once, invisibly, and permanently, by the compiler.

### Rationale and alternatives
Every mechanism in this document traces to the same rejected alternative: built-in, compiler-special-cased control-flow syntax (keywords for branching/looping/jumping, an exception or `?`-operator mechanism for error propagation). All were rejected for the same structural reason: such syntax permanently couples one paradigm to the compiler, leaving no way for an organization to govern, extend, or replace it without forking the language. That coupling is not merely theoretical — built-in syntax can still change meaning out from under a codebase whenever a language's own authors revisit it (see the Go `for`-loop variable-capture change under [Structured vs Unstructured Programming](#structured-vs-unstructured-programming)); the difference is that such a change sits entirely outside the codebase's control, whereas a library's behavior only changes when the codebase's own dependency version does. Library-provided methods, by contrast, can be swapped, extended, linted, or restricted entirely at the organizational level — including by choosing to reintroduce something that looks and behaves like a keyword-based `if`, if that is what a team prefers, as long as it is still built from `sc` and the compiler's execution primitives rather than added to the grammar.

### Prior art
No mainstream general-purpose language fully removes both control-flow keywords and an exception/result-based error mechanism from its grammar. Forth-family languages and some Lisp dialects come closest for control flow itself, treating conditionals and loops as ordinary words/forms rather than special syntax; Go's explicit `(value, error)` returns are the closest mainstream precedent for treating error propagation as an ordinary value rather than a dedicated keyword or operator. Khayyam is unusual in making library-defined abstractions the *only* available path for both, rather than a convention layered on top of keywords and operators that still exist underneath.

### Unresolved questions
1. The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open.

### Future possibilities
- A richer standard library of named, domain-flavored conditional and error-propagation methods is expected to grow over time.

## Change Rationale
- **Initial creation.** Created by merging the standalone "Library-Driven Control Flow" and "Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation" documents into the current Explanation-facet specification, together with the "Code Scope" topic relocated from `khayyam-encapsulation.md` (code scopes are the primitive `IF`/`ELSE`/`LOOP` are built on, not a capsule-level concern). Both standalone document files, and the Code Scope section in `khayyam-encapsulation.md`, have been retired/removed accordingly.
- **Architectural rescoping (2026-07-31).** Following dialectical review with ChatGPT and Claude: `Domain-Driven Arithmetic` was extracted out of this document entirely by the author, to be treated separately in `khayyam-variable.md`; the residual comparison/arithmetic-operator references, the `MathEval` compile-time-type-checking Unresolved question, and the corresponding Future-possibilities item were removed here accordingly (see the companion note handed off alongside this revision for what to check against the target document). The document's core conclusion — that the compiler exposes only execution primitives and privileges no control-flow model — was promoted into the Abstract as a stated outcome rather than left implicit or treated as the document's starting motivation. The former `Structured programming` stub was expanded into a full `Structured vs Unstructured Programming` topic with its own Discussion bundle, reframing the historical goto-versus-structured debate as a question of what a compiler should privilege, not what a compiler should permit. A new `Execution Primitives: The Compiler's Role` topic was split out of the former `Library-Driven Control Flow` topic (itself renamed `Library-Defined Control Flow`) to keep "what the compiler provides" separate from "what libraries build on top of it." `Error Handling: Library-Driven and Syntax-Free` was renamed `Error Propagation` and reframed as one instance of control flow rather than an unrelated concern, with a short comparison of propagation strategies used by other languages (exceptions, `Result` types, Go-style returns, panic/recover) added to its opening.
- **Drawback-framing correction (2026-07-31).** The author flagged that several Drawbacks/Rationale passages implicitly compared Khayyam's *visible* design costs (imports, ceremony, more characters at a call site) against other languages' costs as if the latter were zero, when in fact those languages pay an equivalent design cost once, invisibly, inside the compiler — frozen for the language's lifetime rather than owned and adjustable by the codebase using it. The author also noted that `Structured vs Unstructured Programming` implied only two paradigms (structured, unstructured) existed, when `Domain-Specific Conditional Methods` demonstrates a third — one that is frequently the *better* option, not a stylistic fallback. Every Drawbacks/Rationale passage touching this comparison (`Structured vs Unstructured Programming`, `Code Scope`, `Execution Primitives`, `Library-Defined Control Flow`, and the document-wide Discussion) was rewritten to state the honest, narrower residual cost (onboarding-recognition friction, ecosystem-bootstrapping maturity, or plain call-site character count) instead of an implied "other languages don't pay this" framing, and to credit domain-named conditionals as a genuine third option rather than a footnote to `IF`/`ELSE`.
- **Openness and scope clarifications (2026-07-31).** Per further author feedback: the "structured / unstructured / domain-named" paradigm list was made explicitly non-exhaustive and scoped to today's conventional, classical-hardware execution model — nothing in Khayyam couples a control-flow model to a particular computation substrate, so a fundamentally different future paradigm (e.g. quantum computing's superposition-based branching) can be added as another library without touching the language, and this is now stated directly in both the Abstract and `Structured vs Unstructured Programming`. A proposed Drawback about divergent `IF` libraries across projects was not added, per the author's judgment that this is not a realistic failure mode. The residual bootstrapping-cost Drawback under `Execution Primitives`, and two "open cross-document question" phrasings that implicitly demanded an unwritten companion document, were softened to avoid creating any obligation toward other documents or overstating the difficulty of reaching high productivity. The Abstract now also explicitly acknowledges that method invocation is itself a control-flow event, and states — rather than leaves implicit — that Khayyam deliberately treats Method as a more foundational Type covered elsewhere, not as an oversight in this document's scope.
