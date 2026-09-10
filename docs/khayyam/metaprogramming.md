---
Title: "Metaprogramming in Khayyam"
Status: Draft
Start Date: 2026-07-30
ID: 495955
---

# Metaprogramming in Khayyam

## Abstract
[MetaProgramming](https://en.wikipedia.org/wiki/Metaprogramming) — a program manipulating, generating, or inspecting its own structure or behavior, rather than just executing it — is not built into Khayyam's grammar as dedicated syntax. This document covers the three metaprogramming strategies most relevant to Khayyam's design and the position it takes on each: **decorators** (Python's `@decorator`, Java/C#-style annotations that wrap or modify a method's behavior) have no dedicated syntax at all — cross-cutting behavior must be explicit, visible composition; **syntactic macros** (Rust's `macro_rules!`/procedural macros, the C preprocessor) have no dedicated syntax either — code generation is handled entirely by external tooling operating on ordinary, explicit source files; **reflection** (a program inspecting its own structure at compile time or runtime) *is* supported, but not as an intrinsic, universally-available capability — a type opts in explicitly by composing a reflection-facing abstraction, and the compiler or runtime provides the implementation only for what that abstraction exposes, never more.

All three positions trace to the same commitment documented throughout this project: nothing about a program's structure or behavior should be reachable, alterable, or inspectable through a path that isn't visible in ordinary, explicit source — a composed abstraction, a named method call — even when a hidden path would be more convenient to write.

For the core distinction between the three (why two are rejected outright and one is supported but bounded), see [Three Strategies, One Boundary](#three-strategies-one-boundary).

## Introduction

### Motivation
Decorators silently alter what a method actually does at the call site without that alteration being visible in the call itself — a function annotated `@retry` or `@cached` behaves completely differently from its plain signature, and a reader must separately know to look for and understand the decorator's implementation. Macro systems let code generate or rewrite other code at compile time through a separate, often opaque expansion phase — source code should mean exactly what it says, with no hidden expansion step a reader must mentally simulate to understand what will actually execute. Both conflict directly with Khayyam's foundational explicitness principle.

Reflection is a different kind of case. Unlike decorators and macros, which *alter* behavior invisibly, reflection typically only *inspects* structure — and Khayyam has a real, recurring need for exactly that: tooling (codegen, linters, serializers) legitimately needs to ask a type what it looks like. The question this document answers for reflection isn't "should this exist at all" but "should it be a universal, always-on capability of every type (as in Java, where every `Object` carries reflective capability by default), or an opt-in one, declared the same explicit way any other capability is declared." Khayyam takes the latter position, for the same reason it takes the position it does on decorators and macros: a capability that exists for every type whether or not that type's author asked for it is a hidden path into that type's structure, and hidden paths are what this document's other two rejections are about in the first place.

A further, more general question underlies all three positions: when a method or abstraction's design is fully legible to a human reader, why should the language itself need to get involved to help a specific tool — a codegen generator, an IDE, a linter, a serializer — do its job? [`abstraction_p.Implements`](./protocols/abstraction-implements.md) is a concrete, working answer to this question for one such need (signaling implementation intent before a capsule is structurally complete): it was met entirely with an ordinary composed method, no new syntax required, precisely because the tooling need was already reachable through the existing capsule/method vocabulary. Reflective Programming, below, follows exactly the same pattern for a different need (exposing structure to a tool at runtime or compile time). The same explicitness commitment that led Khayyam to reject implicit type inference in favor of always-explicit types (see [Explicit Types](./khayyam-variable.md#explicit-types)) applies throughout: convenience that saves the author some typing or wiring at declaration time, at the cost of a reader (or a type's own author) having to separately know about and mentally simulate a hidden mechanism, is a bad trade in a language whose central commitment is explicitness.

### Methodology
This document evaluates each metaprogramming strategy by separating the capability a tool needs from the mechanism commonly used to obtain it. It asks, in order: whether the capability changes behavior, generates source, or inspects declared structure; whether the affected type or call site can explicitly grant that capability; and whether the existing Type, Abstraction, Capsule, and Method vocabulary can express the grant without a new grammar feature.

This method produces different conclusions for the three strategies. Decorators and syntactic macros depend on a transformation that a reader cannot see in the ordinary call or source surface, so they are rejected. Structural inspection can be made visible as a capability a type explicitly composes, so opt-in reflection is retained as a direction. The implementation mechanism for that capability remains an open design question; the methodology settles the authorization boundary before selecting a compiler, runtime, or tooling realization.

## Explanation

### Three Strategies, One Boundary
Wikipedia's article on reflective programming names reflection as one of the standard strategies for metaprogramming, alongside code generation and macro systems — the three are commonly grouped together because all of them involve a program treating its own code or structure as data, rather than only executing it directly. Khayyam's position on each is shaped by the same question: does this strategy require the language to expose a hidden, always-available path into a type's structure or behavior, or can the same need be met through a capability the type's own author explicitly opts into?

- **Decorators** wrap a method's *behavior* invisibly. No opt-in is possible even in principle — the whole point of a decorator is that the call site doesn't have to know about it. Rejected outright; see [Decorators Rejection](#decorators-rejection).
- **Macros** generate or rewrite *code* invisibly, at compile time. Same problem, at the level of source text rather than a single call. Rejected outright; see [Rejection of Syntactic Macros and Meta-Programming](#rejection-of-syntactic-macros-and-meta-programming).
- **Reflection** inspects (and, in some languages, modifies) a type's own *structure*. Unlike the other two, this can be made opt-in without losing its value: a type that wants to be inspectable composes an abstraction that says so, and only what that abstraction exposes becomes visible to reflective tooling — nothing about types that didn't opt in. Supported, but bounded this way; see [Reflective Programming](#reflective-programming).

### Decorators Rejection
Khayyam has no decorator syntax (Python's `@decorator`, TypeScript/Java-style annotations that wrap or modify a method's behavior). Any cross-cutting behavior a decorator would normally provide (logging, caching, retry logic) must be expressed as explicit, visible composition — typically by the caller explicitly invoking the cross-cutting behavior itself — rather than an attribute silently wrapping the original method.

Decorators silently alter what a method actually does at the call site without that alteration being visible in the call itself — a function annotated `@retry` or `@cached` behaves completely differently from its plain signature, and a reader must separately know to look for and understand the decorator's implementation. This is in direct tension with Khayyam's broader principle that nothing about a method's runtime behavior should be hidden from its declaration and call sites — the same commitment as Sovereign Encapsulation and Closures as Implicit Capsule Syntax in [Encapsulation in Khayyam](./khayyam-encapsulation.md#sovereign-encapsulation), the zero-hidden-magic principle in [Control Flow in Khayyam](./khayyam-control_flow.md), and [Method in Khayyam](./khayyam-method.md)'s own no-chaining and no-fn-keyword decisions.

Where another language would write `@retry(times=3) func fetchData()`, a Khayyam developer instead explicitly composes the retry behavior at the call site or within an explicitly named wrapping capsule, so that the retry logic is visibly present in the source rather than silently injected by an annotation. There is no decorator/annotation syntax in the grammar capable of wrapping or altering a method's behavior; any equivalent functionality must be built from ordinary capsules and explicit method calls.

### Rejection of Syntactic Macros and Language-Level Metaprogramming
Khayyam provides no syntactic macro system (Rust-style `macro_rules!`/procedural macros, C preprocessor macros) and no compile-time meta-programming/code-generation facility baked into the language itself. Any code generation a project needs is handled by external tooling operating on the explicit source, not by language-level macro expansion.

Macro systems let code generate or rewrite other code at compile time through a separate, often opaque expansion phase, which conflicts directly with Khayyam's foundational explicitness principle: source code should mean exactly what it says, with no hidden expansion step a reader must mentally simulate to understand what will actually execute.

Where another language might reach for a macro to eliminate boilerplate (e.g. generating repetitive trait implementations), Khayyam developers rely on external scaffolding/code-generation tools that produce ordinary, explicit `.kh` source files ahead of time — files that are then read, reviewed, and version-controlled exactly like hand-written code, with no invisible expansion happening at compile time. There is no macro-definition or macro-invocation syntax in the grammar. Code generation, where needed, is explicitly a pre-compile, tooling-level step that emits ordinary source files, not a compiler-level expansion mechanism — [`abstraction_p.Implements`](./protocols/abstraction-implements.md) is a working example of exactly this pattern: it gives a codegen tool a discoverable signal to scaffold an incomplete capsule's boilerplate, entirely through an ordinary composed method rather than through any macro or annotation. The original source document's own container-scaffolding example pointed to what is now [Polymorphism in Khayyam](./khayyam-polymorphism.md) as the concrete case.

### Reflective Programming
Reflection — a program inspecting, and in some languages modifying, its own structure at compile time or runtime — is supported in Khayyam, but it is not an intrinsic capability every type carries by default. Khayyam's version has more in common with `abstraction_p.Implements` than with Java's `getClass()` or Go's `reflect` package: a type becomes reflectable by explicitly composing a reflection-facing abstraction, and only what that abstraction's methods expose becomes visible to reflective tooling. There is no universal backdoor into every type's fields and methods; there is an ordinary, opt-in capability, declared the same way any other capability is declared.

Concretely, a type that wants to expose its shape to tooling — a serializer needing field names and types, an ORM needing to enumerate methods, a debugger inspecting live state — composes an abstraction for that purpose (illustratively, `reflect_p.Structural` or a domain-specific analog, following the same naming pattern `abstraction_p.Implements` established: a generic name for the common case, with room for a domain-specific realization where disambiguation matters):

```khayyam
tp UserRecord cp {
    Structural
}
```

The compiler or runtime then provides the concrete implementation for whatever that abstraction's contract requires (e.g. a method enumerating `UserRecord`'s fields by name and type) — the same "compiler/runtime provides the implementation, the type only declares intent" division of labor `abstraction_p.Implements` already established for codegen scaffolding, applied here to introspection instead. A type that does not compose the abstraction is not reflectable at all — not partially, not through some fallback path — because there is nothing in its declaration granting that access.

This preserves Sovereign Encapsulation rather than working around it: reflection doesn't bypass "all fields are private, all interaction is through methods" — an opted-in type is still only exposing structural facts through ordinary methods the abstraction defines, exactly like any other capability a capsule chooses to offer.

## Results
Insufficient time has passed since this document's positions were adopted to report real, observed outcomes from their use. This section will be filled in once there is such experience to draw on.

