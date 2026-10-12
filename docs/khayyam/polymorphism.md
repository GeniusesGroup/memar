---
Title: "Polymorphism in Khayyam"
Status: Proposed
Start Date: 2026-07-11
ID: 495494
---

# Polymorphism in Khayyam

## Abstract
Khayyam achieves [polymorphism](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)) exclusively through its abstraction (`ab`) mechanism — without generic syntax, without function overloading, and without inheritance-based behavior transfer. This document classifies the polymorphism forms that Khayyam supports, the syntax it explicitly rejects, and the rationale for each decision. In Strachey's classic taxonomy, Khayyam provides **inclusion (subtype) polymorphism** (which also serves as Khayyam's mechanism for achieving **parametric polymorphism** — see "Relationship to Parametric Polymorphism" below) and **ad-hoc polymorphism via constrained interfaces**, while rejecting **generic type-parameter syntax** (`<T>`), **function overloading**, and **coercion polymorphism**. How a call through an abstraction is performed is stated by the compiler that consumes the grammar, not here; the grammar offers no syntax to choose a strategy.

Rather than generic type parameters (`List<T>`), Khayyam achieves type-safe, polymorphic containers and algorithms through domain-specific intermediate capsules (e.g. `ConnectionList` instead of `List<Connection>`), whose public methods strictly accept and return only the relevant capsule type and whose internal validation rules live directly inside their own methods — exactly where that logic belongs. This approach eliminates the "Anemic Domain Model" anti-pattern that generic collections tend to produce.

## Introduction

### Assumptions and constraints
This document assumes familiarity with [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership). The rejection of generic syntax follows from EBO's ownership model; it is not an independent preference about syntax aesthetics. Without that model, the arguments below can be mistaken for a stylistic rejection rather than a consequence of the rule that every behavior has one visible owner.

### Motivation

### The Problem This document Solves
Polymorphism is one of the most overloaded and confusing terms in programming language discourse. To many developers, "polymorphism" is synonymous with inheritance. Others equate it with generics. Still others think of it as function overloading. This confusion has real consequences: language designers add features they don't need (or omit features they do need) because they haven't clearly classified which form of polymorphism they're targeting.

Khayyam needs an explicit, documented classification of its polymorphism model for several reasons:

- **Unambiguous scope.** Without a classification, "polymorphism" in a Khayyam discussion can mean inclusion, parameters, or overloading at different times, and two correct-looking proposals can be argued against each other.
- **Developer education.** Developers coming from Java, Rust, Go, or C++ will have different assumptions about what "polymorphism" means. An explicit classification prevents misunderstandings and sets correct expectations.
- **Consistency with document 495493.** The Abstraction Design document defines the `ab` mechanism in detail but does not explicitly classify which polymorphism forms it provides. This document closes that gap. The dependency runs one way: Polymorphism *uses* Abstraction — an abstraction can exist with no polymorphic use whatsoever — and this document completes or specializes nothing about it.

### The Anemic Domain Model Problem with Generic Collections
Generic collections create an illusion of correctness: domain logic that must live inside the container (e.g. "no duplicate Service IDs in this list") gets pushed outside the encapsulated type into disconnected layers (controllers, random services) because the generic abstraction has no room for it — directly breaking encapsulation and producing "Anemic Domain Models." Generic syntax (`<T>`) also introduces parsing/readability overhead that conflicts with Khayyam's minimal-syntax philosophy.

The problem is structural, not incidental. A `List<Connection>` cannot carry any domain-specific behavior — it is, by design, a type-agnostic container. But real domain logic needs type-specific containers: a `ConnectionList` that prevents duplicate connections, enforces connection lifecycle rules, and provides domain-meaningful query methods. By forcing all containers through the generic straitjacket, languages incentivize developers to push validation and business rules into external services rather than encapsulating them within the type itself.

### Concrete Pain Points Addressed
- **Java/C# developers** expect generics (`<T>`) for writing reusable algorithms. They need to understand that Khayyam's abstractions achieve the same code-reuse goal without the syntax, and when they might feel the absence.
- **Rust developers** expect trait bounds and explicit `impl` blocks for polymorphism. They need to understand how Khayyam's implicit structural satisfaction replaces that ceremony, and what the tradeoffs are.
- **Go developers** expect interface-based polymorphism plus (since Go 1.18) limited generics. They need to understand why Khayyam chose not to follow Go's path of adding generics on top of interfaces.
- **C++ developers** expect both templates (compile-time polymorphism) and virtual functions (runtime polymorphism). They need to understand that Khayyam reaches polymorphism one way — through abstractions — and does not distinguish the two.

## Explanation

### What Is Polymorphism?
Polymorphism, at its core, means "one operation, many types" — the ability for a single piece of code to work with values of different types. The key insight, often missed, is that this is not a single mechanism. There are several fundamentally different ways to achieve it, each with distinct tradeoffs. Khayyam supports the key polymorphic forms — parametric, inclusion/subtype, and ad-hoc — but achieves them through its own unified mechanism (abstraction conformance) rather than through the separate syntaxes that mainstream languages use for each form. What Khayyam rejects is not the polymorphic *capability*, but specific *syntaxes* that conflict with its design principles.

### The Two Polymorphism Mechanisms
1. **Writing code that accepts any abstraction-conforming capsule (Inclusion/Subtype Polymorphism)**
This is the primary form of polymorphism in Khayyam. You write a method that accepts an abstraction type as its parameter. Any capsule that satisfies that abstraction can be passed in:
```khayyam
tp Hasher ab
tp Bytes ab
tp Digest ab
tp Error ab

// A method that works with ANY hasher — this is polymorphism
tp Process mt (self Service) (h Hasher, data Bytes) (d Digest, err Error) {
    h.Hash(data)(d, err)
}
```
Whether `Process` receives a `Sha256Hasher`, a `Md5Hasher`, or a `SaltyHasher` (which extends `Hasher`), the code works. One declaration of `Hash` covers every capsule that satisfies `Hasher`.

2. **Composing abstractions to create richer abstractions (Abstraction Extension)**
You can build more specific abstractions by including other abstractions. This creates a subtyping relationship where a capsule conforming to the more specific abstraction is automatically usable wherever the more general one is expected:
```khayyam
tp Hasher ab
tp Bytes ab
tp Digest ab
tp Error ab

tp Hash mt (self Hasher) (data Bytes) (d Digest, err Error)

tp SaltyHasher ab {
    Hasher
}

tp Salt mt (self SaltyHasher) () (s Bytes)
```
A `SaltyHasher` can be passed to any function expecting a `Hasher`, because it includes `Hasher`'s requirements. This is inheritance in its correct sense: requirements flow, behavior does not. The implementing capsule owns every method it defines.

### Polymorphism Without Generics: Domain-Specific Containers
The question "what replaces `List<T>`?" reveals a modeling assumption that deserves examination. `List<T>` presents itself as a container — a storage structure parameterized by element type. But from the domain's perspective, what actually exists is not "a list of connections" but a **concept** — "the set of connections managed by this service" — that happens to use a list as its internal storage mechanism. The concept has its own identity, its own invariants (no duplicate connections, lifecycle rules), and its own behavior (query methods, bulk operations). None of these belong to a generic list; they belong to the concept itself.

A developer (or a code generator/AI assistant) therefore defines a domain-specific capsule, `ConnectionList`, whose public methods strictly accept and return only `Connection` capsules, and whose internal validation rules live directly inside its own methods — exactly where that logic belongs. Where a method needs to accept any implementer of a shared behavior, it refers to the abstraction directly (e.g. `Index(el Element)` rather than `Index[T](el T)`).

This is not a workaround for the absence of generics — it is the principled approach. The domain-specific capsule does more than a generic container ever could: it enforces domain invariants, provides domain-meaningful method names, and keeps all logic related to a collection of connections inside the type that represents that concept. The raw list or map is an implementation detail inside the capsule, not the public abstraction that application code interacts with.

### What the Grammar Does Not Admit
- No generic syntax: there is no `fn` keyword ([Method → No Dedicated fn/func Keyword](./method.md#no-dedicated-fnfunc-keyword)) and no type parameter to write, so a reusable behavior is written as an ordinary method taking the abstraction it requires — `tp Process mt (self Service) (h Hasher, data Bytes) (d Digest, err Error)`.
- No method overloading: each method name has exactly one signature.
- No implicit type coercion: an `Int32` does not silently become an `Int64`, or any other type. A change of type is an explicit method call.
- No generic collection types: there is no `List<T>`, `Map<K, V>`, or `Set<T>` to name. [Domain-Specific Containers](#domain-specific-containers) below states what a collection of domain values is instead.

### Generic Syntax vs Generic Capability
Khayyam rejects generic **syntax**, not generic **capability**.

A generic capability means that one implementation can operate over multiple concrete types according to a declared behavioral contract. This is a valuable and widely-needed capability: sorting algorithms, hashers, serializers, and container operations all require it. Khayyam fully provides this capability through abstraction conformance — a method accepting an abstraction type is, in effect, a universally quantified function over all types satisfying that abstraction.

Generic **syntax** (`<T>`, `[T]`, `where T: Trait`) is only one historically-dominant way to express that capability. It works by introducing explicit type parameters that the developer must annotate, constrain, and propagate through call chains. This syntax conflates two fundamentally different concerns:

1. **Type generalization** — the ability for one piece of code to work with multiple types. This is the legitimate capability that polymorphism should provide.
2. **Behavior ownership placement** — the question of *where* the behavior's definition lives and *who* owns it. Generic syntax structurally places behavior definitions in templates rather than in the concrete types that represent domain concepts, which is a behavior-ownership decision, not a polymorphism decision.

Khayyam keeps the first capability — through abstraction conformance — while rejecting the second consequence of generic syntax: moving behavior ownership away from domain concepts and into type-parameterized templates. The distinction matters because it is the ownership consequence, not the polymorphism capability, that produces the Anemic Domain Model anti-pattern discussed throughout this document.

This is why the question "how do you achieve generics without generic syntax?" is, from Khayyam's perspective, a category error. The correct question is: "how do you achieve polymorphic capability while preserving behavior ownership?" — and abstraction conformance is the answer.

### A Note on Ad-Hoc Behavior via Type Inspection
A rare but real need is to execute completely different logic based on the concrete type behind an abstraction — not merely to reach that type's own implementation, but to branch on which type it is. The grammar admits no construct that does this: no statement tests what a value's concrete type is, and an abstraction-typed position names the abstraction. Where behavior differs per concrete capsule, each capsule provides its own implementation of the abstraction's methods, and the call reaches the one belonging to the capsule it was made on.

This need arises primarily in the context of ADTs, where the abstraction principle itself is intentionally suspended (ADTs exist precisely to enable type-based branching).

### Polymorphism Classification in Khayyam
The foundational classification of polymorphism types in programming language theory comes from Christopher Strachey's 1967 lecture, later refined by Luca Cardelli and Peter Wegner (1985). They identify two major categories:

| Category | Strachey's term | Description |
|----------|----------------|-------------|
| **Ad-hoc** | Ad-hoc polymorphism | The same operation behaves differently for different types. Each type may have a completely different implementation. |
| **Universal** | Parametric polymorphism | A single implementation works uniformly across all types. The code is written once and instantiated for each concrete type. |
| **Universal** | Inclusion (subtype) polymorphism | A subtype can be used wherever its supertype is expected, based on a subtyping relationship. |

Cardelli and Wegner further divide ad-hoc polymorphism into **overloading** (same name, different implementations based on argument types) and **coercion** (implicit type conversion). This gives us the full taxonomy:

```
Polymorphism
├── Ad-hoc
│   ├── Overloading (e.g., C++ function overloading)
│   └── Coercion (e.g., implicit int → float)
└── Universal
    ├── Parametric (e.g., Java generics, Rust generics, Haskell type variables)
    └── Inclusion / Subtype (e.g., Java interfaces, Go interfaces, Rust trait objects)
```

Additionally, the academic literature recognizes **row polymorphism** (structural polymorphism on records/structs, found in ML-like languages) as a distinct form that enables extensible record types.

### Khayyam's Position in This Taxonomy
**Supported:**

| Form | Mechanism in Khayyam | Notes |
|------|---------------------|-------|
| **Inclusion (subtype) polymorphism** | Abstraction conformance (`ab`) | A capsule satisfying an abstraction is a subtype of that abstraction. This is Khayyam's primary polymorphism mechanism. |
| **Parametric polymorphism** | Achieved via inclusion polymorphism | Khayyam does not have explicit type-parameter syntax (`<T>`), but the expressiveness of parametric polymorphism is fully available: a method accepting an abstraction type is, in effect, a universally quantified function ("for all types satisfying this abstraction"). See "Relationship to Parametric Polymorphism" below for the theoretical justification. |
| **Ad-hoc polymorphism via constrained interfaces** | Abstraction types as method parameters | When a method accepts an abstraction type, it behaves differently for each concrete capsule that satisfies the abstraction. Each capsule provides its own implementation. This is a form of ad-hoc polymorphism — the same operation (`h.Hash(data)`) dispatches to different code depending on the concrete type. |

**Syntax explicitly rejected:**

| Rejected Syntax | Why rejected |
|----------------|-------------|
| **Generic type-parameter syntax** (`<T>`, `[T]`) | Briefly: explicit type-parameter syntax forces developers to expose implementation details, adds grammar complexity, is redundant when abstraction conformance already yields the same parametric polymorphism, and structurally encourages the Anemic Domain Model anti-pattern by providing type-agnostic containers that have no room for domain-specific behavior. |
| **Function/method overloading** | Overloading introduces ambiguity: the same name maps to multiple implementations based on argument types. This conflicts with Khayyam's goal of explicit, unambiguous code. Each method has exactly one signature. If different behavior is needed for different types, abstraction conformance provides it cleanly. |
| **Implicit type coercion** | Implicit type conversions create hidden behavior that is difficult to reason about and can introduce subtle bugs. Khayyam's philosophy of total explicitness rejects all implicit conversions. If a type change is needed, it must be done explicitly via a method call. |
| **Row polymorphism** | While theoretically interesting, row polymorphism is primarily useful for extensible record types. Khayyam's capsules are strictly encapsulated (internal fields are never exposed), so the structural extensibility that row polymorphism provides is not applicable. |

### How Inclusion Polymorphism Works in Detail

#### Basic Subtyping Through Conformance
When a capsule satisfies an abstraction, it becomes a subtype of that abstraction in the type system. This is the Liskov Substitution Principle in action: any code written to work with the abstraction must also work correctly with any conforming capsule.

```khayyam
// Any capsule that defines Read and Close satisfies Reader
tp FileReader cp { handle FileHandle }
tp Read mt (self FileReader) (data Element) (err Error) { /* ... */ }
tp Close mt (self FileReader) () (err Error) { /* ... */ }

tp NetworkReader cp { conn TcpConn }
tp Read mt (self NetworkReader) (data Element) (err Error) { /* ... */ }
tp Close mt (self NetworkReader) () (err Error) { /* ... */ }

// This function is polymorphic: it accepts ANY Reader subtype
tp CopyAll mt (self Service) (src Reader, dst Writer) (err Error) {
    // ...
}
```

#### Subtyping Through Abstraction Extension
When abstraction `B` includes abstraction `A`, `B` is a subtype of `A`. Any capsule conforming to `B` is automatically a subtype of `A` as well:

```khayyam
tp Serializer ab {}
tp Serialize mt (self Serializer) (data Bytes) (out Bytes) (err Error)

tp VersionedSerializer ab {
    Serializer
}
tp VersionInfo ab

tp Version mt (self VersionedSerializer) () (v VersionInfo)
```

A capsule conforming to `VersionedSerializer` can be passed to any function expecting a `Serializer`. The subtyping relationship is established at the abstraction level through declarative inclusion — no behavior is transferred, only requirements.

#### Covariant Return Types
If an abstraction method returns abstraction `A`, a conforming capsule may return capsule `B` (as long as `B` satisfies `A`). This is a natural consequence of the structural satisfaction model:

```khayyam
tp Factory ab {}
tp Create mt (self Factory) () (product Product)

tp CarFactory cp { /* ... */ }
tp Create mt (self CarFactory) () (product Car) { /* Car satisfies Product */ }
```

#### What the Grammar Says About Dispatch
The grammar states nothing about how a call through an abstraction is performed, and offers no syntax to choose: the same polymorphic code may be performed differently at different call sites depending on what is knowable where, and no declaration expresses a preference. That decision, and what it costs at each call site, belongs to the compiler that consumes this grammar — see [Compiler](../modules/computer/compiler.md).

### Relationship to Parametric Polymorphism
An important theoretical observation, supported by recent research, is that **inclusion polymorphism and parametric polymorphism have significant overlap in expressive power**. The paper "Structural Subtyping as Parametric Polymorphism" (Ghiotto et al., 2023, POPL) demonstrates that structural subtyping can encode parametric polymorphism, and vice versa, in certain type systems.

This is relevant to Khayyam because it means that the absence of explicit generic syntax does not necessarily mean a loss of expressive power. When a developer writes:

```khayyam
tp Process mt (self Service) (h Hasher, data Bytes) (d Digest, err Error) { /* ... */ }
```

This is, in effect, a universally quantified function: "for all types `H` that satisfy `Hasher`, this method works." That covers every `H` the abstraction admits, with no type-parameter syntax written anywhere.

The difference is not in expressive power, but in **where the quantification is visible**: in parametric polymorphism, the type parameter is explicit in the syntax; in Khayyam's inclusion polymorphism, the quantification is carried by the abstraction type the signature names.

### Generic Syntax Elimination: Domain-Specific Containers and the Anemic Domain Model
This section details how Khayyam replaces generic type parameters with domain-specific capsules, and why this is not a limitation but a deliberate design choice that strengthens encapsulation.

#### Domain-Specific Containers
The framing "domain-specific containers replace generic containers" is misleading if it implies that a `ConnectionList` is a wrapper around `List<T>`. The correct framing is: **a domain concept that happens to use collection-like storage is modeled as its own first-class type**, not as a parameterized storage structure.

The concept "the set of connections managed by this service" is not a `List` variant — it is an independently-modeled concept with its own identity, behavior, and invariants. The fact that it uses a map or list internally is an implementation detail, not its public identity. Application code interacts with the concept's methods (`AddConnection`, `GetConnection`, `RemoveDisconnected`); it never interacts with the underlying storage abstraction.

Raw ADTs are not exposed directly to application logic; domain capsules (`ConnectionList`, `ServiceRegistry`) wrap them. These capsules have public methods that strictly accept and return only the relevant capsule type, and their internal validation rules live directly inside their own methods — exactly where that logic belongs. Where a method needs to accept any implementer of a shared behavior, it refers to the abstraction directly (e.g. `Index(el Element)` rather than `Index[T](el T)`).

The base ADTs (e.g. a raw hash map) act as plain "hosts" — they do not need generic syntax to know their "guest" element's identity; the guest capsule manages its own identity/memory rules.

A concrete example illustrates why no type-parameter syntax is needed. A `ConnectionList` capsule wraps a raw map and exposes domain-specific methods whose signatures already carry the full type information:

```khayyam
tp ConnectionList cp { container Map }

// The method signature specifies the exact types: ConnectionID as key, Connection as value.
// No generic syntax is needed — the types are explicit in the method contract itself.
tp AddConnection mt (self ConnectionList) (con Connection) (err Error) {
    // TODO::: Add any logic like validation here

    vr conID ConnectionID
    con.ConnectionID(conID) (err)
    // NOTE: `con` here occupies both roles — influencing in `(conID, con)` and influenced in `(con, err)`. This exhibits the open dual-role question of method.md#the-open-question-a-variable-that-is-both; no settled notation exists yet. A future notation may require explicit marking or splitting.
    self.container.Add(conID, con) (con, err)
}

tp GetConnection mt (self ConnectionList) (id ConnectionID) (con Connection, err Error) {
    self.container.Get(id) (con, err)
}
```

The type safety that `<T>` provides in other languages is achieved here through the method signatures themselves: `AddConnection` accepts only `Connection` capsules, and `GetConnection` returns only `Connection` capsules. Both `AddConnection` and `GetConnection` agree on `ConnectionID` as the key and `Connection` as the value — there is no scenario where these two methods could specify different types for the same container. The constraint is the signature itself: a call passing a `Service` capsule names a position declared for `Connection`, and no declaration provides it.

#### Closed vs. Open Type Parameters — Why "How Many Layers" Is the Wrong Test
When evaluating whether a generic-like parameter is safe to keep in a host language lacking Khayyam's abstraction model, the relevant question is not how many call layers separate the definition from its use, but whether the parameter is **closed** or **open** at its point of definition. A closed parameter is one the defining package itself binds to a fixed, framework-owned type (e.g. a container operation defined in terms of `Element`, where `Element` is always resolved by the framework, never chosen anew by each caller) — this carries no propagation cost, regardless of how many layers exist below or above it. An open parameter is one whose concrete binding is deferred to the caller (e.g. `Encoder[BUF any]`, where `BUF` must be supplied by whoever constructs an `Encoder`) — this is virulent by construction: every intermediate layer between the parameter's origin and its final concrete binding must either propagate the same open parameter or collapse it early via type erasure. Whether that path happens to be one layer or five is incidental; what matters is whether the parameter ever reaches call sites (e.g. business-logic service implementations) that must remain readable and free of type-system bookkeeping. A closed parameter keeps its binding at the definition, while an open parameter requires every intermediate layer to preserve or close that binding; this rule remains observable when a host language realizes the abstraction.

#### Dynamic Dispatch Reducibility
Whether dynamic dispatch is *always* reducible to a compile-time-resolved form was initially raised as an open dispute. For Memar it resolves in the affirmative from the base layer's own principles: dispatch among candidates may defer to runtime, but the candidate set and every candidate's implementation must already be spelled out in source — [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) permits no behavior the source does not define — and a genuinely runtime-only type selection, whose target set or implementation arrives while the system runs, would mint structure in execution, which [Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition) excludes outright. Selection within the established closure is execution (the base principle's first boundary clause), not structural change.

#### No Method Overloading
A method name has exactly one signature. With inclusion polymorphism, behavior that differs per concrete capsule is expressed by each capsule implementing the abstraction's methods, so a second path to the same need would leave two mechanisms competing for the same declaration name.

#### Why the Matrix Question Does Not Challenge This document
The question most often raised against Khayyam's design takes a form like "what about `Matrix<T, const N: usize>`?" — but this question conflates two fundamentally different concerns. The `T` parameter is a polymorphism question (fully covered by abstraction conformance). The `const N` parameter is a **type-level computation** question: it encodes a compile-time fact (the matrix dimension) into the type identity, which is then a fact about the type rather than a requirement the type states.

In current mainstream languages, type parameters have become a general-purpose communication channel between the developer and whatever consumes the type. When a language lacks other mechanisms for conveying compile-time facts (dimension constraints, memory layout hints, optimization metadata), the only available channel is the type system — so developers encode everything into type parameters. This is not a strength of generic syntax; it is a consequence of lacking alternatives.

**Khayyam's design position:** a compile-time fact is not identity information, and the grammar does not let a type carry it as one. Whether a fact beyond the four Type categories a signature may name belongs in the language at all, and if so through what construct, is an open question for the language — one this document does not settle.

This separates three concerns that generic syntax conflates:

- **Polymorphic reuse** — fully provided through abstraction conformance. This is settled.
- **Compile-time facts** (dimensions, layout constraints, optimization hints) — not identity. Whether they are stated through an abstraction a type composes, or left to a tool's rules, is unsettled; either way they are not written into type identity.
- **Rule verification** (dimension and unit compatibility, state machine transitions, protocol constraints) — a rule about an operation, not an identity property of a type. A matrix multiplication requiring compatible dimensions says nothing about what a `Matrix` is.

The remaining work is what the language states about compile-time facts, if anything; that belongs to whichever document owns the question rather than to this polymorphism-focused document.
