---
Title: "Method in Khayyam"
Status: Draft
Start Date: "2026-07-28"
ID: "495900"
---

# Method in Khayyam

## Abstract
This document specifies how a Khayyam developer writes and composes callable behavior. It covers the mechanical grammar of the method signature itself (`tp {name} mt (self {owner}) (influencing variables...) (influenced variables...) { }`, pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods for FFI/contracts) — including why Khayyam rejects the traditional "arguments"/"return values" (input/output) framing in favor of naming what a variable actually does in a given call: an **owner**, an **influencing variable** (what influences the call), or an **influenced variable** (what the call influences). It then covers two design decisions built on top of that grammar: no dedicated `fn`/`func` keyword — a "function" is structurally just a method (`mt`), typically owned by a small capsule but not restricted to one; and no expression chaining — every intermediate result requires an explicitly declared, named variable, treated as a decomposition signal rather than a cost to eliminate. Both are expressions of the same underlying commitment: nothing about how behavior is declared, dispatched, or sequenced should be implicit or syntactically shortcut-able.

This document's examples frequently use a capsule as the method's owner, since capsule mechanics (field privacy, Sovereign Encapsulation) are the richest to illustrate — not because capsules are expected to be the most common owner in idiomatic Khayyam. A method owned by another method, or by an abstraction, is expected to be at least as common — abstraction composition in particular is central to Memar-style design, so methods attached to abstractions should be plentiful. Where the owner specifically is a capsule, this document depends on the capsule model specified in [Encapsulation in Khayyam](./khayyam-encapsulation.md), which references this document back for the signature mechanics it no longer restates. (See [Method Structure](#method-structure) for the full range of types a method can be attached to.)

For the mechanical spec, start with [Method Structure](#method-structure) below; for why a seemingly free-standing function still needs an owner, see the worked example under [No Dedicated fn/func Keyword](#no-dedicated-fnfunc-keyword).

## Introduction

### Motivation
Many languages need extra top-level keywords (`private`, `public`, etc.) to express access/authorization requirements for standalone functions. Khayyam believes such requirements can and do change over time, and that this is easily expressed through ordinary capsule methods rather than dedicated keywords — avoiding yet another category of special-cased, fixed syntax.

Separately, in nearly every mainstream language, the ability to chain method calls or pass one call's result directly into another is taken for granted. But this convenience also lets multiple distinct responsibilities silently accumulate inside a single function body or expression without any forcing function to notice. Khayyam treats the resulting verbosity as intentional: a method or widget that needs many named intermediate steps to do its job is very likely doing more than one job.

### Methodology

## Explanation

### Method Structure
A method (`mt`) is itself a type, structurally analogous to a capsule (`cp`) in that it is declared with `tp` and can be composed and referenced like any other type — but where a capsule is a unit that *holds* data, a method is a unit that *is* callable. By using the `mt` subtype, developers define an executable behavior and attach it to an owner. That owner is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`) — wherever a receiver is genuinely warranted. 

The method signature follows this pattern:

```khayyam
tp {name} mt (self {owner_type}) ({influencing variables}...) ({influenced variables}...) { ___ }
```

#### Key Rules
- A method declared without an owner at all (no `self`) is a plain, receiver-less standalone function.
- **Pass-by-Reference and State Protection**: Every variable passed to a method — the owner, each influencing variable, and each influenced variable alike — is passed strictly by reference. When the owner or a variable is a capsule, even though it is passed by reference, its internal state remains strictly protected because all data fields are entirely hidden: a receiving method cannot directly mutate a passed capsule's fields, and state mutation can only occur if the passed capsule explicitly exposes a behavior (method) that allows it. (See [Influencing and Influenced Variables](#influencing-and-influenced-variables-not-inputs-and-outputs) for why "arguments" and "return values" are not the right names for these two groups.)
- **Parenthesized Separation**: Developers must separate the owner, influencing variables, and influenced variables by using `()` to indicate all three groups, even if empty. All three are the same at the underlying layers — each is just a variable reference; this rule exists to improve code readability.
- **Standalone Functions**: Developers can write pure standalone functions by omitting the `self` parameter — there is no limitation requiring a receiver.
- **Recommended Naming**: Developers can use any naming for the owner parameter, but `self` is suggested as the base point to reference other members of whatever type owns the method.

Example:
```khayyam
tp Set mt (self Key) (key String) (err Error) {}
```

#### Method Invocation Rules
Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.

The distinction between static behavior and instance behavior is governed by the presence of the `self` reference in the method signature, enforced strictly at the tooling/linter layer:

- **Type-Level (Static) Invocation**: Methods defined without a `self` reference belong to the type's blueprint. They must be invoked directly through the type identifier (e.g., `tp.Create()`). Invoking a type-level method on a variable instance (`vr.Create()`) is flagged as an error.
- **Instance-Level Invocation**: Methods defined with a `self` reference require an active memory instance of the owner type. They must be invoked through a variable instance (e.g., `vr.Mutate()`). Invoking an instance-level method directly on the type identifier (`tp.Mutate()`) is rejected.

This dispatch model ensures that the boundary between type-level and instance-level behavior is always visible in the method signature, not hidden behind a `static` keyword or a naming convention.

#### Body-less Methods (FFI and Contracts)
A method can be defined without a body (`{}`). This is legally used in two scenarios:

1. **Contract Definition**: Defining the required signature for an abstraction (`ab`). The method body is provided by each capsule that implements the abstraction.
2. **Foreign Function Interface (FFI)**: When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file).

#### Discussion

##### Drawbacks
The strict separation of owner, influencing variables, and influenced variables with `()` adds syntactic ceremony for methods that need neither. In practice this case is rarer than it first appears — most methods that look parameter-less still have at least one influenced variable, typically an `Error` (e.g. `tp Close mt (self Reader) () (err Error) {}`, not `() ()`, since closing a reader can fail). But a method that genuinely has nothing to declare on either side — e.g. a `tp Reset mt (self Counter) () () {}` that is defined to always succeed — still carries two empty parenthetical groups that convey no information, purely for the sake of consistency with every other method's shape.

##### Rationale and alternatives
- **Unified parameter list without parenthetical separation (rejected)**: would make it harder to distinguish at a glance which variables are influencing variables and which are influenced variables, especially for methods with many parameters.
- **Separate keyword for functions vs. methods (rejected)**: a method is fundamentally its own type category, attachable to any owner type; introducing a separate keyword for the receiver-less case would create an artificial distinction where none exists at the semantic level.

##### Prior art
Go's method syntax with an explicit receiver is syntactically similar. Rust's `fn` with `&self`/`&mut self` is semantically similar but introduces reference annotations that Khayyam eliminates. Smalltalk's message-passing model is the closest conceptual match.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Influencing and Influenced Variables, Not Inputs and Outputs
"Input" and "output" is a borrowed framing, and it is a poor fit for a language where a type carries its own methods with it and every variable is passed by reference. In a value-oriented language, an "input" really can be treated as read-only by the callee, because the callee has no mechanism to reach back and change it. That guarantee does not hold here, and it does not hold in any language where a real capsule/struct is passed by reference and carries its own mutating methods. Consider C: a function receiving a pointer to a struct is nominally receiving an "argument," but nothing stops that function from calling the struct's own mutating operations on it — developers routinely do exactly this, because the struct's mutating functions are conventionally recognizable and are, in practice, called from inside other functions that also treat the same struct as an "input." The struct was never purely an input to begin with; it was already something else the label just didn't have a name for.

Khayyam does not repeat this: instead of naming a method's variables by which end of the call they sit on (in vs. out), it names them by the *role they play in that specific call*:

- **Owner** (`self`) — the type instance the method is attached to and executes on behalf of. Most often a capsule, but not necessarily — see [Method Structure](#method-structure) for the full range of types a method can be attached to.
- **Influencing variable** — a variable that influences what the method does. This is what other languages call an "argument" or "input," but named for its actual role (it has *influence* — it affects the outcome) rather than for its position in a call.
- **Influenced variable** — a variable that is changed by the method as a side effect of the call. This is what other languages call a "return value" or "output," but named for its actual role — it is *impressionable* by this call — rather than for its position in the call.

These are relational categories, not fixed properties of a variable. The same `vr` can be an influencing variable in one method call and an influenced variable in another; the grammar's two parenthesized groups (`(influencing variables...)`, `(influenced variables...)`) simply declare, per call, which role each variable is playing this time.

#### The Open Question: A Variable That Is Both
A genuine unresolved case is a variable that plays both roles in the very same call. Consider `sk Socket` in a method that reads configuration values off `sk` (making it an influencing variable for that part of the method) and also calls `sk.Close()` before returning (making it an influenced variable, since the socket's own internal closed-state has now changed as a side effect of this call). There is currently no settled notation for declaring this dual role explicitly — a variable can only be written into one of the two parenthesized groups today, whichever the author judges primary.

One working hypothesis, not yet a rule: a variable needing both roles in the same call may itself be a decomposition signal, in the same spirit as [Composition Depth as a Decomposition Signal](#composition-depth-as-a-decomposition-signal-no-expression-chaining) — if `sk`'s configuration is read in one place and its lifecycle is closed in another, the method doing both may be doing two jobs (reading state, and terminating a resource) that would be clearer as two methods with a traceable order between them, rather than one method where a single variable's effect on, and by, the call are tangled together. This is offered as a hypothesis to test against real code, not a settled rule — see Unresolved questions.

#### Discussion

##### Drawbacks
Owner/influencing/influenced is one more piece of vocabulary a newcomer has to learn instead of reaching for the already-familiar "input"/"output" mental model every other language uses. And the dual-role case above shows the three-way split is not yet a complete model — a real, common pattern (a resource handle that is read from and then closed in the same call) does not fit cleanly into exactly one of the two non-owner groups.

##### Rationale and alternatives
- **Keep "arguments" and "return values" (the conventional framing; rejected)**: accurately describes languages where the callee cannot reach back into the caller's variables, but is actively misleading in Khayyam, where every non-owner variable is passed by reference and can, in principle, be mutated through its own exposed methods regardless of which parenthesized group it sits in. Keeping the conventional names would quietly promise a read/write guarantee the language does not make.
- **"Input"/"output" (a common relabeling; rejected for the same reason)**: still a positional framing (which side of the call is it "on"), not a role framing (what does it actually do in this call); it inherits the same misleading guarantee as "arguments"/"return values."

##### Prior art
C's pass-by-pointer struct parameters are the direct prior art for the problem being solved here — the same "argument that is also mutated internally" pattern this section describes. Go and Rust's pointer/reference parameters share the same structural ambiguity; Rust's borrow checker is the closest prior art for actually *enforcing* a distinction between read-only and mutable access at the language level (via `&` vs `&mut`), which Khayyam's current model does not attempt — the influencing/influenced split here is a naming and modeling clarification, not an enforcement mechanism.

##### Unresolved questions
- Whether a variable playing both the influencing and influenced role in the same call should get explicit notation (a third grouping, a marker, or something else), or whether it should remain disallowed/discouraged in favor of splitting the method, is not yet decided.
- Whether the compiler or linter should (or even can, without deeper static analysis) detect when a variable declared in the influencing group is, in fact, being mutated inside the method body via one of its own exposed methods — surfacing exactly the case this section describes as a warning.

##### Future possibilities
A linter rule that flags an influencing variable receiving a call to one of its own known-mutating methods, prompting the author to either move it to the influenced group or consider splitting the method, once the dual-role question above is resolved.

### No Dedicated fn/func Keyword
In Khayyam, functions and methods are not separate concepts. There is no `fn`/`func` keyword in the grammar — but more importantly than the missing keyword itself, Khayyam treats the instinct to reach for a genuinely standalone, type-independent function as usually a sign of unfinished thinking about the behavior, not a real requirement of the behavior itself.

Consider `Sum(a, b)`, which looks like the cleanest possible example of a function needing no type identity at all. In practice it rarely stays that simple: what happens on overflow — does it saturate, wrap, or return an error? What if `a` and `b` are different numeric types — coerce, or reject? These aren't hypothetical edge cases; they are the actual behavioral questions an addition operation has, and they don't have one universal answer — they have an answer *per numeric type*. Once that's visible, `Sum`'s real identity stops being a mystery: it was never identity-less, it belongs to whichever type's arithmetic it is — `W32.Sum`, `I64.Sum`, `Decimal_64_64.Sum` — each with its own overflow policy and its own combination rules. The apparent standalone function was quietly borrowing behavior a type already owned; it just hadn't been asked to admit it yet.

This is the actual case for having no `fn`/`func` keyword: not "a capsule is the only allowed shape," but "a behavior that seems to need no owner almost always turns out to need one, once you look closely enough — usually the type of one of its own influencing or influenced variables." A "function" is, structurally, just a method (`mt`) attached to whichever type actually owns the behavior; a receiver-less method (no `self`) remains available for the genuinely rare case where no owner applies at all — and a dedicated `fn`/`func` keyword plus access-modifier keywords (the conventional approach) was rejected as an unnecessary second category of declaration syntax on top of a model that already covers this case.

#### Example
Once in a while, a behavior really doesn't belong to any existing type — a one-off helper with no natural home. This is the case a small, purpose-built capsule with a `Do`-style method exists for — a fallback for the genuinely ownerless case, not the default first move:

```khayyam
// TimeHelper.When computes what a monotonic time will be, in nanoseconds, Duration d in the future.
tp When mt (self TimeHelper) (d NanoSecondDuration) (t MonotonicTime) {}

// use in this manner:
vr t1 monotonic.Time
TimeHelper.When(d)(t1)
```

This is not a rejection of pure, standalone-function-style logic — it is fully supported — it is simply always expressed as a method, and, wherever possible, attached to the type the behavior actually belongs to (as `Sum` belongs to `W32`) rather than to a fresh wrapper capsule invented for the occasion. The wrapper-capsule-plus-`Do` pattern above is what's left over once that search comes up genuinely empty.

#### Discussion

##### Drawbacks
This reframing adds a real thinking cost before writing anything: instead of just typing a free function, a developer has to first ask which type the behavior actually belongs to — for `Sum`, that means noticing the overflow/coercion questions and picking a numeric type before writing a line of logic. And for the genuinely rare case where no existing type fits, expressing the behavior still requires a named method (typically wrapped in a small capsule to give it a name and a home) rather than a single top-level function declaration, which remains more ceremony than virtually every other language needs for this case.

##### Rationale and alternatives
- **Dedicated `fn`/`func` keyword plus access-modifier keywords (the conventional approach; rejected)**: an unnecessary second category of declaration syntax layered on top of a model — attach a method to whichever type owns the behavior — that already covers the case, once that type is correctly identified.
- **Free functions with no owner as the default (rejected)**: makes it too easy to stop at the first "this doesn't need a type" impression, which the `Sum` example shows is usually wrong on inspection; defaulting to a method on an owning type forces that inspection to happen at declaration time rather than being skipped.

##### Prior art
Most languages (C, Go, Java, Rust, Python) provide a dedicated function-declaration keyword distinct from their type/class declaration syntax, and treat `Sum(a, b)`-style free functions as entirely ordinary. Smalltalk and other strictly message-passing-oriented languages, where even "free functions" are ultimately methods on some object, are closer in spirit to Khayyam's approach here. Domain-modeling-heavy codebases in many languages (e.g. `Money.add()` over a free `add(a, b)`) already arrive at the same "behavior belongs to a type" conclusion as a best practice, without the language forcing it.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Composition Depth as a Decomposition Signal (No Expression Chaining)
Khayyam method calls are statements, not chainable expressions (`a.Foo().Bar()` is not legal syntax). Every intermediate result requires an explicitly declared, named variable. A method or widget body that accumulates many such named steps is treated as a deliberate design signal calling for further decomposition, not a cost to optimize away with chaining syntax.

When a developer notices a method or widget accumulating multiple unrelated named steps — for example, a "register comment" widget that both resolves "who is the active user" *and* validates/saves the comment — this is the language pushing back against an under-decomposed model, not a syntax limitation to work around. The correct response is always further decomposition: split out a separate widget/capsule with its own narrow responsibility and its own error boundary (e.g. a dedicated widget that returns only an `ActiveUserID`), never a request for implicit chaining syntax. This is a language-level, syntactic enforcement of the same test stated conceptually in [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) and applied architecturally in [Modularity → Module Identity and Responsibility](./modularity.md#module-identity-and-responsibility): whether a step's presence in this particular body is required by a shared concern, or is only there because it was convenient to write inline.

This applies uniformly, including to things that *feel* like a single operation — for example a `parse → validate → transform → aggregate` data pipeline. Each stage is a distinct concern with its own failure mode and reuse potential, and Khayyam intentionally provides no syntactic shortcut letting these stages collapse into one undifferentiated block.

Because every method's influenced variables are written by reference into pre-declared variables (never returned as an expression value — see [Method Structure](#method-structure)), there is no syntactic slot in the grammar for one call's result to be fed directly as another call's input. The verbosity of named intermediate steps is the price paid for forcing this discipline to be visible directly in the source, rather than living only in a developer's head or a comment.

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
Together, these decisions mean Khayyam code contains more named methods and more named intermediate variables than equivalent code in most mainstream languages: every seemingly type-independent utility requires first identifying which type actually owns the behavior (or, failing that, a purpose-built capsule-plus-method pair); every multi-step computation becomes a sequence of named variables rather than a chained expression. Both costs are treated as deliberate, load-bearing friction rather than incidental ceremony to be minimized. Separately, the owner/influencing/influenced reframing of method parameters trades a familiar (if inaccurate) input/output mental model for a more accurate but less familiar one, and does not yet have a settled answer for variables that play both roles in the same call.

### Rationale and alternatives
Both `fn`/`func`-keyword and expression-chaining rejections trace back to the same underlying choice: Khayyam consistently declines to add a second, shortcut syntax alongside an already-sufficient general mechanism (the method model, attached to whichever type actually owns the behavior; named, pre-declared variables for a method's influenced variables), even where the shortcut is common practice elsewhere and would reduce ceremony in the common case. The influencing/influenced reframing follows a related but distinct logic: not "add no new mechanism" but "name the existing mechanism by what it does, not by an inherited framing (input/output) that doesn't hold once methods are pass-by-reference and types carry their own mutating behavior."

### Prior art
Prior art for each individual decision is documented under its own topic above. Taken together, Smalltalk's message-passing model (no free functions, no operator overloading magic) is the closest overall precedent for this document's general stance: prefer an already-general mechanism, explicitly used, over a second, more convenient but less legible one.

### Unresolved questions
1. Whether a variable playing both the influencing and influenced role in the same call needs its own notation, or should be treated as a signal to split the method — see [Influencing and Influenced Variables](#influencing-and-influenced-variables-not-inputs-and-outputs).

### Future possibilities
A linter rule flagging influencing variables that receive calls to their own known-mutating methods (see [Influencing and Influenced Variables](#influencing-and-influenced-variables-not-inputs-and-outputs)).
