---
Title: "Method in Khayyam"
Status: Draft
Start Date: "2026-07-28"
ID: "495900"
---

# Method in Khayyam

## Abstract
This document specifies Khayyam's callable behavior and how it composes. It covers the mechanical grammar of the method signature itself (`tp {name} mt (self {owner}) (influencing variables...) (influenced variables...) { ___ }`, pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods for FFI/contracts) — including why Khayyam rejects the traditional "arguments"/"return values" (input/output) framing in favor of naming what a variable actually does in a given call: an **owner**, an **influencing variable** (what influences the call), or an **influenced variable** (what the call influences). It then covers two design decisions built on top of that grammar: no dedicated `fn`/`func` keyword — a "function" is structurally just a method (`mt`), which any type may own; and no expression chaining — every intermediate result requires an explicitly declared, named variable. Both are expressions of the same underlying commitment: nothing about how behavior is declared, dispatched, or sequenced should be implicit or syntactically shortcut-able.

This document's examples frequently use a capsule as the method's owner, since capsule mechanics (field privacy, Sovereign Encapsulation) are the richest to illustrate. Where the owner specifically is a capsule, this document depends on the capsule model specified in [Encapsulation in Khayyam](./encapsulation.md), which references this document back for the signature mechanics it no longer restates. (See [Method Structure](#method-structure) for the full range of types a method can be attached to.)

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
- The owner group names the method's parent type. `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`.
- **Pass-by-Reference and State Protection**: Every variable passed to a method — the owner, each influencing variable, and each influenced variable alike — is passed strictly by reference. When the owner or a variable is a capsule, even though it is passed by reference, its internal state remains strictly protected because all data fields are entirely hidden: a receiving method cannot directly mutate a passed capsule's fields, and state mutation can only occur if the passed capsule explicitly exposes a behavior (method) that allows it. (See [Influencing and Influenced Variables](#influencing-and-influenced-variables-not-inputs-and-outputs) for why "arguments" and "return values" are not the right names for these two groups.)
- **Parenthesized Separation**: Developers must separate the owner, influencing variables, and influenced variables by using `()` to indicate all three groups, even if empty. All three are the same at the underlying layers — each is just a variable reference; this rule exists to improve code readability.
- **Call on the parent type**: `W32.Sum(a, b)(total, err)`. The name before the dot is the parent type in `self`. Inside the body, `self` is not invoked.
- **Owner parameter naming**: any name is grammar-valid; this repository suggests `self` ([receiver parameter naming](../../bundles/khayyam/rules/receiver-parameter-naming/receiver-parameter-naming.md)).

Example:
```khayyam
tp Set mt (self Key) (key String) (err Error)
```

#### Method Invocation Rules
Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.

Every method names its parent type in the owner group. The call writes both groups. Two shapes:

```khayyam
tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)
W32.Sum(a, b)(total, err)
```

`W32` before the dot is the parent type named by `self`. `(a, b)` influences. `(total, err)` is influenced. The body of `Sum` does not invoke `self`.

```khayyam
tp Set mt (self Key) (value String) (err Error)
k.Set(value)(err)
```

`k` is a variable of the parent type. The body of `Set` works on that instance.

When the parent type is itself a method, the receiver is that method, and the call still writes both groups.

#### Type-level arguments for `sc` and `mt`
A method's influencing group may receive a `vr`, an `sc`, or an `mt`, and what that position then holds is what the called method's behavior is. A `vr` is an instance of a capsule or an abstraction. An `sc` is a code scope: a library method that drives a scope receives that scope here ([Khayyam → Scope](./khayyam.md#scope)). An `mt` is a method. Bare-type and closure-style `mt` passes this repository discourages are stated in [type as argument](../../bundles/khayyam/rules/type-as-argument/type-as-argument.md).

#### A method implements an abstraction by methods of its own
A method can implement an abstraction. It does so by defining methods whose owner is that method. Those methods are the method's own behavior: they state what it does internally. The method can present that implementation to tooling by composing an intent abstraction, as a capsule does with [`abstraction_p.Implements`](../modules/computer/abstraction-implements.md). Asynchrony is one such abstraction, decided at the method's definition; see [Agency → Definition-Site Over Call-Site](./agency.md#definition-site-over-call-site).

#### Body-less Methods (FFI and Contracts)
A method is body-less when nothing follows its third group, so its line ends at the closing parenthesis of the influenced group. A line ending with `{}` instead carries a body, and an empty body is a body holding no command; the two are different declarations. This is legally used in two scenarios:

1. **Contract Definition**: Defining the required signature for an abstraction (`ab`). The implementation is provided by each capsule that implements the abstraction.
2. **Foreign Function Interface (FFI)**: When the receiver is a concrete capsule (`cp`), a body-less method states that the implementation comes from outside the language — a library, or a foreign object linked into the program.

### Influencing and Influenced Variables, Not Inputs and Outputs
"Input" and "output" is a borrowed framing, and it is a poor fit for a language where a type carries its own methods with it and every variable is passed by reference. In a value-oriented language, an "input" really can be treated as read-only by the callee, because the callee has no mechanism to reach back and change it. That guarantee does not hold here, and it does not hold in any language where a real capsule/struct is passed by reference and carries its own mutating methods. Consider C: a function receiving a pointer to a struct is nominally receiving an "argument," but nothing stops that function from calling the struct's own mutating operations on it — developers routinely do exactly this, because the struct's mutating functions are conventionally recognizable and are, in practice, called from inside other functions that also treat the same struct as an "input." The struct was never purely an input to begin with; it was already something else the label just didn't have a name for.

Khayyam does not repeat this: instead of naming a method's variables by which end of the call they sit on (in vs. out), it names them by the *role they play in that specific call*:

- **Owner** (`self`) — the type instance the method is attached to and executes on behalf of. Most often a capsule, but not necessarily — see [Method Structure](#method-structure) for the full range of types a method can be attached to.
- **Influencing variable** — a variable that influences what the method does. This is what other languages call an "argument" or "input," but named for its actual role (it has *influence* — it affects the outcome) rather than for its position in a call.
- **Influenced variable** — a variable that is changed by the method as a side effect of the call. This is what other languages call a "return value" or "output," but named for its actual role — it is *impressionable* by this call — rather than for its position in the call.

These are relational categories, not fixed properties of a variable. The same `vr` can be an influencing variable in one method call and an influenced variable in another; the grammar's two parenthesized groups (`(influencing variables...)`, `(influenced variables...)`) declare, per call, which role each variable is playing this time.

#### The Open Question: A Variable That Is Both
A genuine unresolved case is a variable that plays both roles in the very same call. Consider `sk Socket` in a method that reads configuration values off `sk` (making it an influencing variable for that part of the method) and also calls `sk.Close()` before returning (making it an influenced variable, since the socket's own internal closed-state has now changed as a side effect of this call). There is currently no settled notation for declaring this dual role explicitly — a variable can only be written into one of the two parenthesized groups today, whichever the author judges primary. Atomic read-modify-write is not a counter-example: that case gets a dedicated method that owns the atomic operation as its own clear abstraction, so the call site never needs dual-role notation for it. No strong concrete example has yet been found where dual role survives as correct modeling; see the paired handoff's [Open Questions](./method.handoff.md#a-variable-that-is-both-influencing-and-influenced-in-the-same-call).

### No Dedicated fn/func Keyword
In Khayyam, functions and methods are not separate concepts. There is no `fn`/`func` keyword in the grammar — but more importantly than the missing keyword itself, Khayyam treats the instinct to reach for a genuinely standalone, type-independent function as usually a sign of unfinished thinking about the behavior, not a real requirement of the behavior itself.

Consider `Sum(a, b)`, which looks like the cleanest possible example of a function needing no type identity at all. In practice it rarely stays that simple: what happens on overflow — does it saturate, wrap, or return an error? What if `a` and `b` are different numeric types — coerce, or reject? These aren't hypothetical edge cases; they are the actual behavioral questions an addition operation has, and they don't have one universal answer — they have an answer *per numeric type*. Once that's visible, `Sum`'s real identity stops being a mystery: it was never identity-less, it belongs to whichever type's arithmetic it is — `W32.Sum`, `I64.Sum`, `Decimal_64_64.Sum` — each with its own overflow policy and its own combination rules. The apparent standalone function was quietly borrowing behavior a type already owned; it just hadn't been asked to admit it yet.

This is the actual case for having no `fn`/`func` keyword: not "a capsule is the only allowed shape," but "a behavior that seems to need no owner almost always turns out to need one, once you look closely enough — usually the type of one of its own influencing or influenced variables." A "function" is, structurally, just a method (`mt`) attached to whichever type actually owns the behavior: `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`, called as `W32.Sum(a, b)(total, err)`. A dedicated `fn`/`func` keyword plus access-modifier keywords was rejected as an unnecessary second category of declaration syntax on top of a model that already covers this case.

#### Example
Once in a while, a behavior really doesn't belong to any existing type — a one-off helper with no natural home. That is the case a small, purpose-built capsule with a `Do`-style method exists for:

```khayyam
// TimeHelper.When computes what a monotonic time will be, in nanoseconds, Duration d in the future.
tp When mt (self TimeHelper) (d NanoSecondDuration) (t MonotonicTime)

// use in this manner:
vr helper TimeHelper
vr t1 monotonic.Time
helper.When(d)(t1)
```

`When` names its parent type: `(self TimeHelper)`. The call is `helper.When(d)(t1)`.

A behavior is always expressed as a method, attached to whichever type owns it — `Sum` belongs to `W32`, so it is `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`, called as `W32.Sum(a, b)(total, err)`. The wrapper-capsule-plus-`Do` form above is what is left when no existing type owns the behavior.

### Composition Depth as a Decomposition Signal (No Expression Chaining)
Khayyam method calls are statements, not chainable expressions (`a.Foo().Bar()` is not legal syntax). Every intermediate result requires an explicitly declared, named variable.

Because every method's influenced variables are written by reference into pre-declared variables (never returned as an expression value — see [Method Structure](#method-structure)), there is no syntactic slot in the grammar for one call's result to be fed directly as another call's input. A body that needs several steps therefore writes several declarations, each visible in the source where it happens. This applies uniformly, including to steps that feel like a single operation — a `parse → validate → transform → aggregate` pipeline has no syntactic shortcut that collapses its stages into one undifferentiated block. The verbosity of named intermediate steps is the price of that visibility, rather than a step count living only in a reader's head or a comment.
