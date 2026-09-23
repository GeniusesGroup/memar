---
Title: "Method in Khayyam"
Status: Draft
Start Date: "2026-07-28"
ID: "495900"
---

# Method in Khayyam

## Abstract
This document specifies how a Khayyam developer writes and composes callable behavior. It covers the mechanical grammar of the method signature itself (`tp {name} mt (self {owner}) (influencing variables...) (influenced variables...) { }`, pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods for FFI/contracts) — including why Khayyam rejects the traditional "arguments"/"return values" (input/output) framing in favor of naming what a variable actually does in a given call: an **owner**, an **influencing variable** (what influences the call), or an **influenced variable** (what the call influences). It then covers two design decisions built on top of that grammar: no dedicated `fn`/`func` keyword — a "function" is structurally just a method (`mt`), typically owned by a small capsule but not restricted to one; and no expression chaining — every intermediate result requires an explicitly declared, named variable, treated as a decomposition signal rather than a cost to eliminate. Both are expressions of the same underlying commitment: nothing about how behavior is declared, dispatched, or sequenced should be implicit or syntactically shortcut-able.

This document's examples frequently use a capsule as the method's owner, since capsule mechanics (field privacy, Sovereign Encapsulation) are the richest to illustrate — not because capsules are expected to be the most common owner in idiomatic Khayyam. A method owned by another method, or by an abstraction, is expected to be at least as common — abstraction composition in particular is central to Memar-style design, so methods attached to abstractions should be plentiful. Where the owner specifically is a capsule, this document depends on the capsule model specified in [Encapsulation in Khayyam](./encapsulation.md), which references this document back for the signature mechanics it no longer restates. (See [Method Structure](#method-structure) for the full range of types a method can be attached to.)

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

The distinction between static behavior and instance behavior is governed by the presence of the `self` reference in the method signature, enforced by the compiler:

- **Type-Level (Static) Invocation**: Methods defined without a `self` reference belong to the type's blueprint. They must be invoked directly through the type identifier (e.g., `tp.Create()`). Invoking a type-level method on a variable instance (`vr.Create()`) is a compile-time error.
- **Instance-Level Invocation**: Methods defined with a `self` reference require an active memory instance of the owner type. They must be invoked through a variable instance (e.g., `vr.Mutate()`). Invoking an instance-level method directly on the type identifier (`tp.Mutate()`) is a compile-time error.

This dispatch model ensures that the boundary between type-level and instance-level behavior is always visible in the method signature, not hidden behind a `static` keyword or a naming convention.

#### Type-level arguments for `sc` and `mt`
An argument position may be satisfied by a `vr` of the declared type or, for the subtypes `sc` and `mt`, by the type itself passed as a type-level argument. The compiler resolves which reading applies from the callee's signature; there is no ambiguity at the AST. Passing a bare type where a capsule or abstraction *value* is expected is meaningful only for `sc`/`mt`; elsewhere it is a governance smell the [Linter](../protocols/linter.md) may flag, not a syntax error. Passing an `mt` value in closure style — capturing state as an implicit capsule — is discouraged; see [Closures as Implicit Capsule Syntax](./encapsulation.md#closures-as-implicit-capsule-syntax).

#### Body-less Methods (FFI and Contracts)
A method can be defined without a body (`{}`). This is legally used in two scenarios:

1. **Contract Definition**: Defining the required signature for an abstraction (`ab`). The method body is provided by each capsule that implements the abstraction.
2. **Foreign Function Interface (FFI)**: When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file).

### Influencing and Influenced Variables, Not Inputs and Outputs
"Input" and "output" is a borrowed framing, and it is a poor fit for a language where a type carries its own methods with it and every variable is passed by reference. In a value-oriented language, an "input" really can be treated as read-only by the callee, because the callee has no mechanism to reach back and change it. That guarantee does not hold here, and it does not hold in any language where a real capsule/struct is passed by reference and carries its own mutating methods. Consider C: a function receiving a pointer to a struct is nominally receiving an "argument," but nothing stops that function from calling the struct's own mutating operations on it — developers routinely do exactly this, because the struct's mutating functions are conventionally recognizable and are, in practice, called from inside other functions that also treat the same struct as an "input." The struct was never purely an input to begin with; it was already something else the label just didn't have a name for.

Khayyam does not repeat this: instead of naming a method's variables by which end of the call they sit on (in vs. out), it names them by the *role they play in that specific call*:

- **Owner** (`self`) — the type instance the method is attached to and executes on behalf of. Most often a capsule, but not necessarily — see [Method Structure](#method-structure) for the full range of types a method can be attached to.
- **Influencing variable** — a variable that influences what the method does. This is what other languages call an "argument" or "input," but named for its actual role (it has *influence* — it affects the outcome) rather than for its position in a call.
- **Influenced variable** — a variable that is changed by the method as a side effect of the call. This is what other languages call a "return value" or "output," but named for its actual role — it is *impressionable* by this call — rather than for its position in the call.

These are relational categories, not fixed properties of a variable. The same `vr` can be an influencing variable in one method call and an influenced variable in another; the grammar's two parenthesized groups (`(influencing variables...)`, `(influenced variables...)`) simply declare, per call, which role each variable is playing this time.

#### The Open Question: A Variable That Is Both
A genuine unresolved case is a variable that plays both roles in the very same call. Consider `sk Socket` in a method that reads configuration values off `sk` (making it an influencing variable for that part of the method) and also calls `sk.Close()` before returning (making it an influenced variable, since the socket's own internal closed-state has now changed as a side effect of this call). There is currently no settled notation for declaring this dual role explicitly — a variable can only be written into one of the two parenthesized groups today, whichever the author judges primary.

The owner position, not yet a notation rule: a variable needing both roles in the same call is a *signal* that something is crooked somewhere — a prompt to find and fix the underlying modeling problem, the way other languages do not emphasize this and Khayyam deliberately does, because the fix is what makes the code readable. In the same spirit as [Composition Depth as a Decomposition Signal](#composition-depth-as-a-decomposition-signal-no-expression-chaining): if `sk`'s configuration is read in one place and its lifecycle is closed in another, the method doing both may be doing two jobs (reading state, and terminating a resource) that would be clearer as two methods with a traceable order between them, rather than one method where a single variable's effect on, and by, the call are tangled together. Atomic read-modify-write is not a counter-example: that case gets a *dedicated method* that owns the atomic operation as its own clear abstraction — the call site never needs dual-role notation for it. No strong concrete example has yet been found where dual role survives as correct modeling rather than as the signal; see the paired handoff's [Open Questions](./method.handoff.md#a-variable-that-is-both-influencing-and-influenced-in-the-same-call).

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

### Composition Depth as a Decomposition Signal (No Expression Chaining)
Khayyam method calls are statements, not chainable expressions (`a.Foo().Bar()` is not legal syntax). Every intermediate result requires an explicitly declared, named variable. A method or widget body that accumulates many such named steps is treated as a deliberate design signal calling for further decomposition, not a cost to optimize away with chaining syntax.

When a developer notices a method or widget accumulating multiple unrelated named steps — for example, a "register comment" widget that both resolves "who is the active user" *and* validates/saves the comment — this is the language pushing back against an under-decomposed model, not a syntax limitation to work around. The correct response is always further decomposition: split out a separate widget/capsule with its own narrow responsibility and its own error boundary (e.g. a dedicated widget that returns only an `ActiveUserID`), never a request for implicit chaining syntax. This is a language-level, syntactic enforcement of the same test stated conceptually in [System → When Is a Responsibility Coherent?](../system.md#when-is-a-responsibility-coherent) and applied architecturally in [Modularity → Module Identity and Responsibility](../modularity.md#module-identity-and-responsibility): whether a step's presence in this particular body is required by a shared concern, or is only there because it was convenient to write inline.

This applies uniformly, including to things that *feel* like a single operation — for example a `parse → validate → transform → aggregate` data pipeline. Each stage is a distinct concern with its own failure mode and reuse potential, and Khayyam intentionally provides no syntactic shortcut letting these stages collapse into one undifferentiated block.

Because every method's influenced variables are written by reference into pre-declared variables (never returned as an expression value — see [Method Structure](#method-structure)), there is no syntactic slot in the grammar for one call's result to be fed directly as another call's input. The verbosity of named intermediate steps is the price paid for forcing this discipline to be visible directly in the source, rather than living only in a developer's head or a comment.
