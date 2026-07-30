---
Title: "MetaProgramming in Khayyam"
Status: Draft
Start Date: "2026-07-30"
ID: "495955"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification's Abstraction section (Contract-First Approach, structural satisfaction) is what makes the opt-in abstraction pattern used throughout this document — most directly in Reflective Programming — possible."
    - Title: "Method in Khayyam"
      URI: "./khayyam-method.md"
      Relation: "Depends_on"
      Reason: "Decorators, macros, and reflection all ultimately act on or through ordinary methods, so this document depends on the owner/influencing/influenced method model specified there — a concern about the transparency of the language surface generally, distinct from method declaration itself."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: "Reference"
      Reason: "Sovereign Encapsulation and Closures as Implicit Capsule Syntax are the same 'nothing hidden, everything named' commitment this document applies to decorators, macros, and reflection."
    - Title: "Logic in Khayyam"
      URI: "./khayyam-logic.md"
      Relation: "Reference"
      Reason: "The zero-hidden-magic principle behind Library-Driven Control Flow's rejection of compiler-special-cased keywords is the same principle applied here to decorators and macros."
    - Title: "Variable in Khayyam"
      URI: "./khayyam-variable.md"
      Relation: "Reference"
      Reason: "The rejection of decorators and macros rests on the same explicitness commitment documented there under Explicit Types: convenience that hides a mechanism from the reader is a bad trade, whether the hidden mechanism is a type or a behavior transformation."
    - Title: "Polymorphism in Khayyam"
      URI: "./khayyam-polymorphism.md"
      Relation: "Reference"
      Reason: "The container-scaffolding example behind this document's Rejection of Syntactic Macros topic is consolidated into Polymorphism in Khayyam."
    - Title: "abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration"
      URI: "./abstraction-implements.md"
      Relation: "Reference"
      Reason: "A concrete, working example of this document's central pattern: a tooling-facing or introspection-facing need met entirely with an ordinary composed method and opt-in abstraction composition, with no new syntax required. Reflective Programming below follows the same pattern."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions for rejecting decorators and syntactic macros in the canonical Khayyam specification", "Identified the conceptual link between decorators/macros and reflective programming as related metaprogramming strategies, and proposed splitting them into a dedicated document"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "High"
    Tasks:
      - Works: ["Specified the Decorators Rejection and Rejection of Syntactic Macros and Meta-Programming topics", "Drafted the new Reflective Programming topic, applying the abstraction_p.Implements opt-in-abstraction pattern to reflection"]
        URI: ""
---

# MetaProgramming in Khayyam

## Abstract
[MetaProgramming](https://en.wikipedia.org/wiki/Metaprogramming) — a program manipulating, generating, or inspecting its own structure or behavior, rather than just executing it — is not built into Khayyam's grammar as dedicated syntax. This document covers the three metaprogramming strategies most relevant to Khayyam's design and the position it takes on each: **decorators** (Python's `@decorator`, Java/C#-style annotations that wrap or modify a method's behavior) have no dedicated syntax at all — cross-cutting behavior must be explicit, visible composition; **syntactic macros** (Rust's `macro_rules!`/procedural macros, the C preprocessor) have no dedicated syntax either — code generation is handled entirely by external tooling operating on ordinary, explicit source files; **reflection** (a program inspecting its own structure at compile time or runtime) *is* supported, but not as an intrinsic, universally-available capability — a type opts in explicitly by composing a reflection-facing abstraction, and the compiler or runtime provides the implementation only for what that abstraction exposes, never more.

All three positions trace to the same commitment documented throughout this project: nothing about a program's structure or behavior should be reachable, alterable, or inspectable through a path that isn't visible in ordinary, explicit source — a composed abstraction, a named method call — even when a hidden path would be more convenient to write.

For the core distinction between the three (why two are rejected outright and one is supported but bounded), see the [Guide](#three-strategies-one-boundary) below.

## Introduction

### Motivation
Decorators silently alter what a method actually does at the call site without that alteration being visible in the call itself — a function annotated `@retry` or `@cached` behaves completely differently from its plain signature, and a reader must separately know to look for and understand the decorator's implementation. Macro systems let code generate or rewrite other code at compile time through a separate, often opaque expansion phase — source code should mean exactly what it says, with no hidden expansion step a reader must mentally simulate to understand what will actually execute. Both conflict directly with Khayyam's foundational explicitness principle.

Reflection is a different kind of case. Unlike decorators and macros, which *alter* behavior invisibly, reflection typically only *inspects* structure — and Khayyam has a real, recurring need for exactly that: tooling (codegen, linters, serializers) legitimately needs to ask a type what it looks like. The question this document answers for reflection isn't "should this exist at all" but "should it be a universal, always-on capability of every type (as in Java, where every `Object` carries reflective capability by default), or an opt-in one, declared the same explicit way any other capability is declared." Khayyam takes the latter position, for the same reason it takes the position it does on decorators and macros: a capability that exists for every type whether or not that type's author asked for it is a hidden path into that type's structure, and hidden paths are what this document's other two rejections are about in the first place.

A further, more general question underlies all three positions: when a method or abstraction's design is fully legible to a human reader, why should the language itself need to get involved to help a specific tool — a codegen generator, an IDE, a linter, a serializer — do its job? [`abstraction_p.Implements`](./abstraction-implements.md) is a concrete, working answer to this question for one such need (signaling implementation intent before a capsule is structurally complete): it was met entirely with an ordinary composed method, no new syntax required, precisely because the tooling need was already reachable through the existing capsule/method vocabulary. Reflective Programming, below, follows exactly the same pattern for a different need (exposing structure to a tool at runtime or compile time). The same explicitness commitment that led Khayyam to reject implicit type inference in favor of always-explicit types (see [Explicit Types](./khayyam-variable.md#explicit-types)) applies throughout: convenience that saves the author some typing or wiring at declaration time, at the cost of a reader (or a type's own author) having to separately know about and mentally simulate a hidden mechanism, is a bad trade in a language whose central commitment is explicitness.

### Methodology

## Explanation

### Three Strategies, One Boundary
Wikipedia's article on reflective programming names reflection as one of the standard strategies for metaprogramming, alongside code generation and macro systems — the three are commonly grouped together because all of them involve a program treating its own code or structure as data, rather than only executing it directly. Khayyam's position on each is shaped by the same question: does this strategy require the language to expose a hidden, always-available path into a type's structure or behavior, or can the same need be met through a capability the type's own author explicitly opts into?

- **Decorators** wrap a method's *behavior* invisibly. No opt-in is possible even in principle — the whole point of a decorator is that the call site doesn't have to know about it. Rejected outright; see [Decorators Rejection](#decorators-rejection).
- **Macros** generate or rewrite *code* invisibly, at compile time. Same problem, at the level of source text rather than a single call. Rejected outright; see [Rejection of Syntactic Macros and Meta-Programming](#rejection-of-syntactic-macros-and-meta-programming).
- **Reflection** inspects (and, in some languages, modifies) a type's own *structure*. Unlike the other two, this can be made opt-in without losing its value: a type that wants to be inspectable composes an abstraction that says so, and only what that abstraction exposes becomes visible to reflective tooling — nothing about types that didn't opt in. Supported, but bounded this way; see [Reflective Programming](#reflective-programming).

### Decorators Rejection
Khayyam has no decorator syntax (Python's `@decorator`, TypeScript/Java-style annotations that wrap or modify a method's behavior). Any cross-cutting behavior a decorator would normally provide (logging, caching, retry logic) must be expressed as explicit, visible composition — typically by the caller explicitly invoking the cross-cutting behavior itself — rather than an attribute silently wrapping the original method.

Decorators silently alter what a method actually does at the call site without that alteration being visible in the call itself — a function annotated `@retry` or `@cached` behaves completely differently from its plain signature, and a reader must separately know to look for and understand the decorator's implementation. This is in direct tension with Khayyam's broader principle that nothing about a method's runtime behavior should be hidden from its declaration and call sites — the same commitment as Sovereign Encapsulation and Closures as Implicit Capsule Syntax in [Encapsulation in Khayyam](./khayyam-encapsulation.md#sovereign-encapsulation), the zero-hidden-magic principle in [Logic in Khayyam](./khayyam-logic.md), and [Method in Khayyam](./khayyam-method.md)'s own no-chaining and no-fn-keyword decisions.

Where another language would write `@retry(times=3) func fetchData()`, a Khayyam developer instead explicitly composes the retry behavior at the call site or within an explicitly named wrapping capsule, so that the retry logic is visibly present in the source rather than silently injected by an annotation. There is no decorator/annotation syntax in the grammar capable of wrapping or altering a method's behavior; any equivalent functionality must be built from ordinary capsules and explicit method calls.

#### Discussion

##### Drawbacks
Common cross-cutting concerns (retry, caching, timing/logging wrappers) that a decorator would express in a single line require explicit, repeated composition at every relevant call site or an explicitly named wrapping capsule, which is more verbose than the decorator-based equivalent in other languages.

##### Rationale and alternatives
Decorator/annotation syntax (Python, TypeScript, Java, C#) was rejected because it lets a method's effective runtime behavior diverge silently from what its declaration shows — directly conflicting with Khayyam's explicitness principle.

##### Prior art
Python decorators and Java/C# annotations are the primary prior art being rejected here. Languages without a decorator mechanism (C, Go) instead rely on explicit wrapper functions/structs for the same cross-cutting needs, which is closer to Khayyam's chosen approach.

##### Unresolved questions
The original source document cited "Error Handling: Library-Driven and Syntax-Free" as a foundational dependency for the "nothing should be hidden" principle. That document's identity is known (see Citations) but its content has not yet been supplied to this document set, so the specific claim it's meant to support here is unverified.

##### Future possibilities
None recorded yet.

### Rejection of Syntactic Macros and Meta-Programming
Khayyam provides no syntactic macro system (Rust-style `macro_rules!`/procedural macros, C preprocessor macros) and no compile-time meta-programming/code-generation facility baked into the language itself. Any code generation a project needs is handled by external tooling operating on the explicit source, not by language-level macro expansion.

Macro systems let code generate or rewrite other code at compile time through a separate, often opaque expansion phase, which conflicts directly with Khayyam's foundational explicitness principle: source code should mean exactly what it says, with no hidden expansion step a reader must mentally simulate to understand what will actually execute.

Where another language might reach for a macro to eliminate boilerplate (e.g. generating repetitive trait implementations), Khayyam developers rely on external scaffolding/code-generation tools that produce ordinary, explicit `.kh` source files ahead of time — files that are then read, reviewed, and version-controlled exactly like hand-written code, with no invisible expansion happening at compile time. There is no macro-definition or macro-invocation syntax in the grammar. Code generation, where needed, is explicitly a pre-compile, tooling-level step that emits ordinary source files, not a compiler-level expansion mechanism — [`abstraction_p.Implements`](./abstraction-implements.md) is a working example of exactly this pattern: it gives a codegen tool a discoverable signal to scaffold an incomplete capsule's boilerplate, entirely through an ordinary composed method rather than through any macro or annotation. The original source document's own container-scaffolding example pointed to what is now [Polymorphism in Khayyam](./khayyam-polymorphism.md) as the concrete case.

#### Discussion

##### Drawbacks
Without a macro system, some categories of legitimate boilerplate reduction (e.g. deriving a family of trait implementations automatically at compile time) require external tooling to be run as a separate build step, rather than being handled inline by the compiler itself — adding a tooling dependency for cases a macro system would otherwise absorb into the language.

##### Rationale and alternatives
Macro systems (Rust's `macro_rules!`/proc-macros, C's preprocessor) were rejected because they introduce a compile-time code-rewriting phase that is, by design, somewhat opaque to a reader inspecting only the source — directly in tension with the zero-hidden-magic principle running through this document, [Sovereign Encapsulation](./khayyam-encapsulation.md#sovereign-encapsulation), and [Library-Driven Control Flow](./khayyam-logic.md#library-driven-control-flow) (rejecting macros for the same reason those documents reject implicit mutability keywords and compiler-special-cased control flow, respectively).

##### Prior art
Rust's macro system and the C preprocessor are the primary prior art being rejected here. Languages and ecosystems that instead rely on external code generators emitting plain source (e.g. Go's `go generate` convention, or Protocol Buffers' code generation step) are closer in spirit to Khayyam's chosen approach. Notably, Rust — which also has no built-in reflection — leans on its macro system (e.g. `serde`'s derive macros) to cover needs Khayyam covers instead through opt-in reflection (see [Reflective Programming](#reflective-programming)); rejecting macros without offering some other release valve for that category of need would leave a real gap.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

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

#### Discussion

##### Drawbacks
Compared to universal, always-on reflection (Java, Go, C#), Khayyam's opt-in model means a tool that wants to inspect an arbitrary, unknown type simply cannot, unless that type's author already anticipated the need and composed the relevant abstraction. This is a real limitation for exploratory tooling (a generic debugger or REPL that wants to inspect "whatever value is here") that universal reflection handles for free.

##### Rationale and alternatives
- **Universal, always-on reflection (the conventional approach in Java, Go, C#; rejected)**: gives every type an always-available introspection surface whether or not its author intended one, which is exactly the kind of hidden, unauthorized-by-declaration path this document's decorator and macro rejections also reject — the fact that reflection only *reads* rather than *rewrites* does not change that the path itself is not visible in the type's own declaration.
- **No reflection at all, rely entirely on macros for structure-dependent codegen (Rust's approach; considered, not chosen)**: works, but only by keeping the macro system Khayyam has already rejected for unrelated, stronger reasons (see [Rejection of Syntactic Macros and Meta-Programming](#rejection-of-syntactic-macros-and-meta-programming)). Opt-in reflection covers much of the same need (a tool asking a type what it looks like) without requiring a compile-time code-rewriting phase at all.

##### Prior art
Java's `Class`/`getClass()` and Go's `reflect` package are the primary prior art for universal, always-on reflection, rejected here in favor of an opt-in model. Rust deliberately has no reflection and relies on derive macros (`serde`, `Debug`) for the same category of need — a useful contrast, since Khayyam rejects Rust's macro-based solution too but, unlike Rust, retains a non-macro path to the same underlying need. C#'s attribute-plus-reflection combination is closer to a hidden-by-default, opt-out model (nearly everything is reflectable unless deliberately hidden) — the inverse of Khayyam's opt-in-by-default stance.

##### Unresolved questions
- The exact shape of the reflection-facing abstraction (or family of abstractions, if field-level, method-level, and full-structural reflection warrant separate contracts) has not been designed. `reflect_p.Structural` above is illustrative naming only, not a settled proposal.
- Whether the compiler provides the implementation automatically once a type composes the abstraction (similar to a derive), or whether the type's author must still write it by hand with compiler-provided helpers, is undecided.
- Whether reflective access, once granted via the abstraction, can be further scoped (e.g. field names only, no values; read-only, no modification) or is all-or-nothing per composed abstraction.
- Whether runtime-modifying reflection (not just inspection) is in scope for Khayyam at all, or whether this document's position should be inspection-only by design — the drafting here leaned on inspection-oriented examples throughout and has not tested the modification case.

##### Future possibilities
A standard `reflect_p` package defining the canonical reflection-facing abstraction(s), analogous to `abstraction_p.Implements`, once real tooling needs (serialization, ORMs, debuggers) clarify what shape it should take.

## Results

## Discussion

### Drawbacks
Together, these three positions mean that in Khayyam, any tool wanting to alter a method's behavior invisibly, generate code invisibly, or inspect a type's structure without that type's author having opted in, simply cannot — it must instead work through visible composition, external tooling, or an explicitly composed abstraction. This is a real capability gap relative to languages that offer at least one of these unconditionally, and it means some legitimate tooling categories (universal serializers, generic debuggers, ORMs that work on arbitrary unannotated types) require more upfront cooperation from a type's author in Khayyam than they would elsewhere.

### Rationale and alternatives
All three positions trace to the same underlying test: does this capability require a hidden path into a type's behavior or structure that the type's own declaration doesn't show? Decorators and macros fail this test unconditionally and are rejected outright. Reflection can pass it, but only if implemented as an opt-in capability rather than a universal one — so that's the position Khayyam takes, rather than either rejecting reflection entirely (which would leave a real gap decorators/macros can't fill either, given they're also rejected) or adopting it universally (which would reopen the hidden-path problem from the other direction).

### Prior art
Prior art for each individual position is documented under its own topic above. Taken as a whole, this document's stance — support the underlying need (introspection) while rejecting the specific mechanisms (decorators, macros, universal reflection) that would make it invisible or unconditional — mirrors the pattern already established by `abstraction_p.Implements`: solve the tooling problem with an ordinary, opt-in, composed method, not a language feature.

### Unresolved questions
1. The reflection-facing abstraction's exact shape is undesigned — see Reflective Programming's own Unresolved questions for the specific open sub-questions.
2. "Error Handling: Library-Driven and Syntax-Free," cited by the source Decorators Rejection document, has not yet been supplied to this document set for review.

### Future possibilities
A standard `reflect_p` package (see Reflective Programming's Future possibilities).

## Change Rationale
- Synthesizes the standalone "Decorators Rejection" and "Rejection of Syntactic Macros and Meta-Programming" documents.
- Reflective Programming is newly drafted rather than migrated from an existing document; treat it as more provisional than the rest of this document — several open questions are logged under its own Discussion, and the illustrative `reflect_p.Structural` naming is not a settled proposal.
