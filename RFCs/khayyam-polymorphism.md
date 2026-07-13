---
Title: "Polymorphism in Khayyam"
Status: Proposed
Start Date: 2026-07-11
RFC Number: 495494
Applied to: ["Khayyam.md#Abstraction"]
Related RFCs:
    - Title: "Abstraction Design"
      URI: "./khayyam-abstraction.md"
      Reason: "Extends"
      Explanation: "This RFC builds directly on RFC 495493 (Abstraction Design). Where that RFC defines the abstraction type and its mechanics, this RFC classifies the polymorphism forms that Khayyam supports, which syntaxes it rejects, and why."
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Depends_on"
      Explanation: "Defines Protocol as a pure declarative specification. This RFC uses that definition to justify why abstractions carry no behavior, and why generic type parameters are unnecessary when abstraction conformance is the polymorphic mechanism."
    - Title: "Explicit Behavior Ownership"
      URI: "./explicit_behavior_ownership.md"
      Reason: "Depends_on"
      Explanation: "EBO provides the principled foundation (single visible owner) that this RFC applies at the language level. Generic type parameters introduce ownership ambiguity that violates EBO's visibility requirement."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Contribution: "Defined Khayyam's approach to polymorphism through abstraction conformance, authored the initial notes on abstraction extension and subtyping, established the domain-specific containers pattern as the alternative to generic collections, and articulated the anemic domain model argument against generic syntax."
    Tasks: []
  - Name: "Gemini"
    URI: "https://gemini.google.com/"
    Model: "3.1 pro"
    Effort: "Extended thinking enabled"
    Contribution: "Drafted initial text of RFC 00007 (Containers, Generics Elimination, and Rich Domain Models), argued for and against alternatives including the anemic domain model argument and the EBO-based rejection of generic syntax."
    Tasks: []
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Contribution: "Researched polymorphism theory (Strachey/Cardelli-Wegner classification), mapped Khayyam's mechanisms to formal polymorphism categories, drafted prior art comparisons and open questions, contributed the closed vs. open type parameters analysis."
    Tasks: []
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM"
    Effort: "Medium"
    Contribution: "Merged RFC 00007 content into this RFC, ensuring full preservation of all details including the closed vs. open type parameters analysis, the EBO rationale, and the domain-specific containers pattern."
    Tasks: []
---

# Polymorphism in Khayyam

## Summary
Khayyam achieves [polymorphism](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)) exclusively through its abstraction (`ab`) mechanism — without generic syntax, without function overloading, and without inheritance-based behavior transfer. This RFC classifies the polymorphism forms that Khayyam supports, the syntax it explicitly rejects, and the rationale for each decision. In Strachey's classic taxonomy, Khayyam provides **inclusion (subtype) polymorphism** (which also serves as Khayyam's mechanism for achieving **parametric polymorphism** — see "Relationship to Parametric Polymorphism" below) and **ad-hoc polymorphism via constrained interfaces**, while rejecting **generic type-parameter syntax** (`<T>`), **function overloading**, and **coercion polymorphism**. The compiler's Smart Compilation strategy (monomorphization vs. dynamic dispatch, documented in "The Compiler's Role: Dispatch Strategy" below) is the mechanism by which polymorphic code is resolved, entirely transparently to the developer.

Rather than generic type parameters (`List<T>`), Khayyam achieves type-safe, polymorphic containers and algorithms through domain-specific intermediate capsules (e.g. `ConnectionList` instead of `List<Connection>`), whose public methods strictly accept and return only the relevant capsule type and whose internal validation rules live directly inside their own methods — exactly where that logic belongs. This approach eliminates the "Anemic Domain Model" anti-pattern that generic collections tend to produce.

## Motivation

### The Problem This RFC Solves
Polymorphism is one of the most overloaded and confusing terms in programming language discourse. To many developers, "polymorphism" is synonymous with inheritance. Others equate it with generics. Still others think of it as function overloading. This confusion has real consequences: language designers add features they don't need (or omit features they do need) because they haven't clearly classified which form of polymorphism they're targeting.

Khayyam needs an explicit, documented classification of its polymorphism model for several reasons:

- **Compiler implementation clarity.** The compiler team needs to know exactly what polymorphic behaviors the type system must support. Ambiguity here leads to either over-engineering (implementing unnecessary dispatch mechanisms) or under-engineering (failing to support valid use cases).
- **Cross-language compilation.** When translating Khayyam code to target languages (Go, Rust, C), the compiler needs to know which polymorphic mechanism to emit for each usage site. Without a clear classification, the translation is ambiguous.
- **Developer education.** Developers coming from Java, Rust, Go, or C++ will have different assumptions about what "polymorphism" means. An explicit classification prevents misunderstandings and sets correct expectations.
- **Consistency with RFC 495493.** The Abstraction Design RFC defines the `ab` mechanism in detail but does not explicitly classify which polymorphism forms it provides. This RFC closes that gap.

### The Anemic Domain Model Problem with Generic Collections

Generic collections create an illusion of correctness: domain logic that must live inside the container (e.g. "no duplicate Service IDs in this list") gets pushed outside the encapsulated type into disconnected layers (controllers, random services) because the generic abstraction has no room for it — directly breaking encapsulation and producing "Anemic Domain Models." Generic syntax (`<T>`) also introduces parsing/readability overhead that conflicts with Khayyam's minimal-syntax philosophy.

The problem is structural, not incidental. A `List<Connection>` cannot carry any domain-specific behavior — it is, by design, a type-agnostic container. But real domain logic needs type-specific containers: a `ConnectionList` that prevents duplicate connections, enforces connection lifecycle rules, and provides domain-meaningful query methods. By forcing all containers through the generic straitjacket, languages incentivize developers to push validation and business rules into external services rather than encapsulating them within the type itself.

### Concrete Pain Points Addressed

- **Java/C# developers** expect generics (`<T>`) for writing reusable algorithms. They need to understand that Khayyam's abstractions achieve the same code-reuse goal without the syntax, and when they might feel the absence.
- **Rust developers** expect trait bounds and explicit `impl` blocks for polymorphism. They need to understand how Khayyam's implicit structural satisfaction replaces that ceremony, and what the tradeoffs are.
- **Go developers** expect interface-based polymorphism plus (since Go 1.18) limited generics. They need to understand why Khayyam chose not to follow Go's path of adding generics on top of interfaces.
- **C++ developers** expect both templates (compile-time polymorphism) and virtual functions (runtime polymorphism). They need to understand how Khayyam's Smart Compilation unifies these into a single mechanism that the compiler manages automatically.

## Guide-level explanation

### What Is Polymorphism?
Polymorphism, at its core, means "one operation, many types" — the ability for a single piece of code to work with values of different types. The key insight, often missed, is that this is not a single mechanism. There are several fundamentally different ways to achieve it, each with distinct tradeoffs. Khayyam supports the key polymorphic forms — parametric, inclusion/subtype, and ad-hoc — but achieves them through its own unified mechanism (abstraction conformance) rather than through the separate syntaxes that mainstream languages use for each form. What Khayyam rejects is not the polymorphic *capability*, but specific *syntaxes* that conflict with its design principles.

### The Two Polymorphism Mechanisms You Will Use in Khayyam

1. **Writing code that accepts any abstraction-conforming capsule (Inclusion/Subtype Polymorphism)**
This is the primary form of polymorphism in Khayyam. You write a method that accepts an abstraction type as its parameter. Any capsule that satisfies that abstraction can be passed in:
```khayyam
// A method that works with ANY hasher — this is polymorphism
tp Process mt (self Service) (h Hasher, data Bytes) (err Error) {
    h.hash(data)(err)
}
```
Whether `Process` receives a `Sha256Hasher`, a `Md5Hasher`, or a `SaltyHasher` (which extends `Hasher`), the code works. The compiler decides, at each call site, whether to inline the specific hash implementation (monomorphization) or use a VTable (dynamic dispatch). You don't write different code for each case.

2. **Composing abstractions to create richer contracts (Abstraction Extension)**
You can build more specific abstractions by including other abstractions. This creates a subtyping relationship where a capsule conforming to the more specific abstraction is automatically usable wherever the more general one is expected:
```khayyam
tp Hasher ab {}

tp hash mt (self Hasher) (data Bytes) (h UInt64)

tp SaltyHasher ab {
    Hasher
}

tp salt mt (self SaltyHasher) () (h Bytes)
```
A `SaltyHasher` can be passed to any function expecting a `Hasher`, because it includes `Hasher`'s requirements. This is inheritance in its correct sense: requirements flow, behavior does not. The implementing capsule owns every method it defines.

### Polymorphism Without Generics: Domain-Specific Containers

Instead of a generic `List<Connection>`, a developer (or a code generator/AI assistant) defines an intermediate domain-specific capsule, `ConnectionList`, whose public methods strictly accept and return only `Connection` capsules, and whose internal validation rules (e.g. duplicate prevention) live directly inside its own methods (`ConnectionList.Add()`), exactly where that logic belongs. Where a method needs to accept any implementer of a shared behavior, it refers to the abstraction directly (e.g. `Index(el Element)` rather than `Index[T](el T)`).

This is not a workaround for the absence of generics — it is the principled approach. The domain-specific capsule does more than a generic container ever could: it enforces domain invariants, provides domain-meaningful method names, and keeps all logic related to a collection of connections inside the type that represents that concept.

### What You Will Not Do in Khayyam

- You will **not** write `fn process<T: Hasher>(h: T)` — there is no generic syntax. You write `fn process(h: Hasher)` and the compiler handles the rest.
- You will **not** overload a method name with different parameter types — there is no ad-hoc overloading. Each method has exactly one signature.
- You will **not** rely on implicit type coercion (e.g., an `Int32` silently becoming an `Int64`). The language does not perform implicit type conversions.
- You will **not** use generic collections like `List<T>`, `Map<K, V>`, or `Set<T>`. Instead, you will define (or scaffold) domain-specific capsule types that wrap the underlying ADTs and carry the domain logic that belongs to them.

### A Note on Ad-Hoc Behavior via Compile-Time Conditionals

A rare but valid form of ad-hoc polymorphism is the need to execute completely different logic based on the concrete type behind an abstraction — not just dispatching to the type's own implementation, but branching the caller's control flow. In Khayyam, this can be achieved through compile-time conditional checks (type inspection) within a single method, rather than through function overloading with different parameter types.

However, this need is rare in practice and arises primarily in the context of ADTs, where the abstraction principle itself is intentionally suspended (ADTs exist precisely to enable type-based branching). In all other contexts, if different behavior is needed for different types, the correct mechanism is abstraction conformance — where each capsule provides its own implementation of the shared abstraction's methods.

## Reference-level explanation

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
| **Parametric polymorphism** | Achieved via inclusion polymorphism + Smart Compilation | Khayyam does not have explicit type-parameter syntax (`<T>`), but the expressiveness of parametric polymorphism is fully available: a method accepting an abstraction type is, in effect, a universally quantified function ("for all types satisfying this abstraction"). The compiler monomorphizes or dispatches dynamically as appropriate. See "Relationship to Parametric Polymorphism" below for the theoretical justification. |
| **Ad-hoc polymorphism via constrained interfaces** | Abstraction types as method parameters | When a method accepts an abstraction type, it behaves differently for each concrete capsule that satisfies the abstraction. Each capsule provides its own implementation. This is a form of ad-hoc polymorphism — the same operation (`h.hash(data)`) dispatches to different code depending on the concrete type. |

**Syntax explicitly rejected:**

| Rejected Syntax | Why rejected |
|----------------|-------------|
| **Generic type-parameter syntax** (`<T>`, `[T]`) | See Rationale section below. Briefly: explicit type-parameter syntax forces developers to expose implementation details, adds grammar complexity, is redundant when the compiler achieves the same parametric polymorphism through abstraction conformance and Smart Compilation, and structurally encourages the Anemic Domain Model anti-pattern by providing type-agnostic containers that have no room for domain-specific behavior. |
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
tp Version mt (self VersionedSerializer) () (v UInt32)
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

#### The Compiler's Role: Dispatch Strategy

The specific machine-code mechanism used for each polymorphic call site is determined by the compiler's Smart Compilation strategy. The compiler analyzes the **reachability graph** of each abstraction usage site to determine the implementation strategy:

- **Monomorphization (compile-time):** If the compiler can trace every possible concrete capsule that could satisfy the abstraction at a given usage site (a **closed set**), it inlines the specific method. Zero runtime cost. The polymorphism exists only at the type-checking level; at the machine-code level, the call is a direct jump to the concrete method.
- **Dynamic dispatch (runtime):** If at least one possible capsule is unresolved at compile time (an **open set** — e.g., loaded from a plugin, determined by configuration, or passed across a module boundary where the full set is not visible), the compiler generates a VTable. One indirection per call. This is the standard cost of runtime polymorphism.

This is not an all-or-nothing decision. The same polymorphic code may be compiled differently at different call sites, depending on what the compiler can prove at each specific location. The developer never specifies which strategy to use.

### Relationship to Parametric Polymorphism

An important theoretical observation, supported by recent research (see Prior Art), is that **inclusion polymorphism and parametric polymorphism have significant overlap in expressive power**. The paper "Structural Subtyping as Parametric Polymorphism" (Ghiotto et al., 2023, POPL) demonstrates that structural subtyping can encode parametric polymorphism, and vice versa, in certain type systems.

This is relevant to Khayyam because it means that the absence of explicit generic syntax does not necessarily mean a loss of expressive power. When a developer writes:

```khayyam
tp Process mt (self Service) (h Hasher, data Bytes) (err Error) { /* ... */ }
```

This is, in effect, a universally quantified function: "for all types `H` that satisfy `Hasher`, this method works." The compiler can monomorphize this for each known `H` — achieving the same result as if the developer had written `Process<H: Hasher>(h: H)` — without the type-parameter syntax.

The difference is not in expressive power, but in **where the quantification is visible**: in parametric polymorphism, the type parameter is explicit in the syntax; in Khayyam's inclusion polymorphism, the quantification is implicit in the abstraction type and resolved by the compiler.

### Generic Syntax Elimination: Domain-Specific Containers and the Anemic Domain Model

This section details how Khayyam replaces generic type parameters with domain-specific intermediate capsules, and why this is not a limitation but a deliberate design choice that strengthens encapsulation.

#### Domain-Specific Containers

Raw ADTs are not exposed directly to application logic; intermediate domain capsules (`ConnectionList`, `ServiceRegistry`) wrap them. These domain-specific containers have public methods that strictly accept and return only the relevant capsule type, and their internal validation rules live directly inside their own methods — exactly where that logic belongs. Where a method needs to accept any implementer of a shared behavior, it refers to the abstraction directly (e.g. `Index(el Element)` rather than `Index[T](el T)`).

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
    self.container.Add(conID, con) (con, err)
}

tp GetConnection mt (self ConnectionList) (id ConnectionID) (con Connection, err Error) {
    self.container.Get(id) (con, err)
}
```

The type safety that `<T>` provides in other languages is achieved here through the method signatures themselves: `AddConnection` accepts only `Connection` capsules, and `GetConnection` returns only `Connection` capsules. Both `AddConnection` and `GetConnection` agree on `ConnectionID` as the key and `Connection` as the value — there is no scenario where these two methods could specify different types for the same container. The linter|compiler enforces this at the call site: passing a `Service` capsule to `AddConnection` triggers an immediate error because the parameter type is `Connection`, not because of a generic type-parameter constraint.

#### Linter-Enforced Type Safety in Container Contexts

Because Khayyam has no type inference (variables must be explicitly typed) and relies on strict linters, passing an incorrect capsule type to a container method's `Add()` triggers an immediate linting error. This provides the same type-safety guarantee that generic type parameters provide in other languages, but through a different enforcement mechanism: rather than the compiler rejecting `list<Int>.add("string")` via type-parameter constraints, the Khayyam linter rejects `connectionList.Add(service)` because the method signature of `ConnectionList.Add()` explicitly accepts only `Connection` capsules.

#### Closed vs. Open Type Parameters — Why "How Many Layers" Is the Wrong Test

When evaluating whether a generic-like parameter is safe to keep in a host language lacking Khayyam's contract model, the relevant question is not how many call layers separate the definition from its use, but whether the parameter is **closed** or **open** at its point of definition. A closed parameter is one the defining package itself binds to a fixed, framework-owned type (e.g. a container operation defined in terms of `Element`, where `Element` is always resolved by the framework, never chosen anew by each caller) — this carries no propagation cost, regardless of how many layers exist below or above it. An open parameter is one whose concrete binding is deferred to the caller (e.g. `Encoder[BUF any]`, where `BUF` must be supplied by whoever constructs an `Encoder`) — this is virulent by construction: every intermediate layer between the parameter's origin and its final concrete binding must either propagate the same open parameter or collapse it early via type erasure. Whether that path happens to be one layer or five is incidental; what matters is whether the parameter ever reaches call sites (e.g. business-logic service implementations) that must remain readable and free of type-system bookkeeping. See [memar-go generics elimination RFC] for an empirical account of this failure mode observed across three call layers (buffer → encoder/string → socket → business handler) in a host language lacking contract-based abstraction.

#### Dynamic Dispatch Reducibility Under Immutable Infrastructure

Whether dynamic dispatch is *always* reducible to a compile-time-resolved form was initially raised as an open dispute. Given Memar's Immutable Infrastructure principle (no runtime addition of logic; every capability increase requires recompilation — see [immutable-infrastructure.md], still Draft), this dispute is expected to resolve in the affirmative for Memar specifically, since no genuinely runtime-only type selection should exist under that principle. This is noted as expected-resolved-pending-that-RFC's-finalization, not yet settled, since the Immutable Infrastructure RFC itself remains a placeholder pending dedicated discussion.

#### No Method Overloading

A method name must represent one clear, unambiguous intent. This is not merely a syntactic restriction — it is a consequence of Khayyam's polymorphism model. With inclusion polymorphism, if different behavior is needed for different types, the correct mechanism is abstraction conformance: define an abstraction that captures the shared behavior, and let each capsule provide its own implementation. Overloading would provide a second, conflicting path to the same goal, creating ambiguity about which mechanism to use in any given situation.

## Drawbacks

### 1. No Way to Constrain by Data Shape

In languages with explicit type-parameter syntax, a generic function can constrain its type parameter by both behavior (trait bounds) and data shape (e.g., "must have a `length` field"). In Khayyam, abstractions only constrain behavior (method signatures), not data layout. If a function needs to work with any type that has a specific internal structure, there is no way to express this constraint without defining an abstraction with a method that exposes that structure. This is not a limitation of Khayyam's parametric polymorphism per se — it is a property of behavior-based abstraction that holds regardless of whether the parametric polymorphism is expressed via `<T>` syntax or via abstraction conformance.

This is generally considered acceptable in systems programming — behavior-based constraints are more robust than structure-based ones because they decouple the consumer from the producer's internal representation. However, it can feel limiting in scenarios where data-shape polymorphism is the natural fit (e.g., generic serialization that needs to inspect field names).

### 2. No Function Overloading for Ergonomic APIs

Languages like C++, Java, and Rust (via trait implementations) allow the same function name to be used with different parameter types. In Khayyam, each method has exactly one signature. This means developers must use distinct names for conceptually similar operations on different types (e.g., `AddInt`, `AddFloat` instead of a single overloaded `Add`).

In practice, this is mitigated by Khayyam's abstraction mechanism: if the operation is truly polymorphic, it should be expressed through an abstraction (e.g., `tp Adder ab` with `tp Add mt (self Adder) (other Adder) (result Adder)`). The need for overloading typically arises in contexts where the types share no common abstraction — which is often a sign that the overloading is being used as a convenience shortcut rather than a principled abstraction.

### 3. Discoverability of Polymorphic Behavior

Without generic syntax, discovering that a method is polymorphic (i.e., that it accepts an abstraction type and can work with multiple concrete types) requires reading the method's parameter types. There is no syntactic marker like `<T>` that immediately signals "this is a generic function." This is a minor ergonomic cost, partially addressed by IDE tooling and documentation conventions.

### 4. Potential for Ambiguity in Complex Dispatch Scenarios

In rare cases involving multiple levels of abstraction extension (e.g., `A` includes `B` includes `C`, and a capsule satisfies `A`), the compiler's dispatch logic must correctly resolve which method implementation to use, especially when method names collide across the abstraction hierarchy. This is a well-studied problem in type theory (diamond inheritance, linearization) and is not unique to Khayyam, but it needs explicit compiler behavior documentation.

### 5. Engineering Cost of Domain-Specific Containers

The cost of writing an intermediate domain-specific capsule for every container usage is real, ongoing engineering effort, even for cases that would otherwise be a single line of generic syntax (`List<Connection> connections;`) in another language. This is reframed in this RFC as "a fundamental investment in Clean Architecture," but it is still a genuine, non-trivial cost paid on every container use, not just complex ones.

This cost is partially mitigated by two factors. First, Khayyam's ecosystem includes scaffolding tooling (the Memar framework) that can generate domain-specific container capsules from a declaration, reducing the manual effort to specifying the domain's validation rules and query methods rather than boilerplate container logic. Second, the domain-specific capsule does more than a generic container — it carries domain invariants and provides domain-meaningful APIs — so the investment yields returns in code quality that generic containers cannot provide.

## Rationale and Alternatives

### Why Khayyam Achieves Parametric Polymorphism Through Inclusion Rather Than Type-Parameter Syntax

**The core argument:** Khayyam does not lack parametric polymorphism — it achieves the same universally-quantified code reuse through a different mechanism. When a method accepts an abstraction type, it is, in effect, parametric over all types satisfying that abstraction. The compiler's Smart Compilation strategy (see "The Compiler's Role: Dispatch Strategy") determines the optimal dispatch mechanism (monomorphization or dynamic dispatch) from the dependency graph, without the developer needing to annotate type parameters, specify constraints, or manage variance.

Explicit type-parameter syntax (`<T>`) makes the developer explicitly manage these concerns. This is valuable when the type system is the primary mechanism for achieving polymorphism. But when a language already has a robust abstraction mechanism that the compiler can analyze for dispatch optimization, explicit type parameters become redundant syntax — they expose implementation details that the compiler can determine on its own, and they add grammar complexity for no gain in expressive power.

Khayyam's design philosophy is that the compiler should be intelligent enough to determine the optimal dispatch strategy from the dependency graph, without the developer having to annotate it. The abstraction type in the method signature is sufficient information for both type checking and optimization.

**What this costs:** The developer loses the ability to express type-level constraints that go beyond what an abstraction can specify (e.g., "this type must have a compile-time-known size" or "this type must be `Copy`-able"). If such constraints become necessary in specific domains, they would need to be expressed through additional abstractions (e.g., `tp StaticSized ab` with a method that returns the size at compile time), which is more verbose but consistent with the language's philosophy.

### Why No Function Overloading

Overloading creates a naming collision that must be resolved at every call site by the compiler. This resolution depends on the argument types, which means the same function name can refer to completely different code depending on context. This is the opposite of the explicit, linear execution model Khayyam strives for: the reader should be able to trace the code path without having to mentally resolve type-based dispatch for function names.

Abstraction conformance provides the same ergonomic benefit (one method name that works with multiple types) without the ambiguity: the method is defined once on the abstraction, and each conforming capsule provides its implementation. The dispatch is through the abstraction, not through name resolution.

### Why No Coercion

Implicit type conversions are a form of hidden behavior. When an `Int32` is silently converted to an `Int64`, the developer may not be aware that a widening conversion occurred, which can mask bugs in numerical algorithms. In safety-critical and performance-critical code (Khayyam's target domain), this hidden behavior is unacceptable.

### Why Generic Syntax Breaks Encapsulation: The Anemic Domain Model and EBO Perspectives

Adding generic syntax (the mainstream default) was rejected because it structurally permits domain logic to live outside the type it concerns, which conflicts with Khayyam's encapsulation principle more directly than almost any other common language feature.

An additional principled foundation comes from the Explicit Behavior Ownership principle (RFC 495466). Generic type parameters introduce ownership ambiguity: a method such as `List<T>.Add(T item)` is defined in the generic template but appears on every parameterized instantiation (`List<Connection>`, `List<Service>`, etc.). The implementation is not visible at the point of use — it lives in the template, not in the concrete type's source. This violates EBO's visibility requirement: answering "where was this behavior defined?" when looking at `List<Connection>` requires navigating to a separate generic template and understanding parameter substitution. The domain-specific capsule approach (e.g., `ConnectionList` with its own explicitly defined methods) satisfies both encapsulation and EBO simultaneously.

### Alternative Considered: Zig-Style Comptime Duck Typing

Zig's approach to polymorphism is radically minimalist: there is no abstraction or interface mechanism. Instead, functions take types as compile-time parameters, and the compiler checks at each instantiation whether the type supports the required operations. This is essentially C++-style template duck typing without the syntax.

While philosophically aligned with Khayyam's minimalism, this approach was rejected because:
1. It shifts the entire burden of polymorphism to the developer, who must write comptime logic for what should be a simple "accept any hasher" pattern.
2. Error messages for type mismatches occur at the instantiation site (inside the function body) rather than at the call site (where the wrong type is passed), making them harder to understand.
3. It provides no first-class abstraction type that can be used as a parameter type in method signatures — there is no way to express "this function accepts anything that behaves like a Reader" without making the entire function comptime-generic.

Khayyam's abstraction type provides a cleaner, more readable mechanism for the common case, while the compiler's Smart Compilation achieves the same zero-cost outcomes as Zig's comptime instantiation for cases where the concrete type is known.

## Prior Art

### Go — Interfaces (Inclusion) + Go 1.18 Generics (Limited Parametric)

Go is the closest analog to Khayyam's polymorphism model. Before Go 1.18, Go had only interface-based inclusion polymorphism — exactly what Khayyam provides. The Go team deliberately deferred generics for over a decade, arguing that interfaces were sufficient for most polymorphism needs.

In 2022, Go 1.18 introduced type parameters with interface constraints. The Go generics design document explicitly states: "Polymorphism in Go must fit smoothly into the surrounding language, without awkward special cases and without exposing implementation details." However, Go's generics have notable limitations: no generic methods on interfaces (only on concrete types), no specialization, and constraints must be expressed as interface types.

Khayyam's position is that Go 1.18 generics were added to solve a real problem (writing type-safe containers and algorithms) but introduced significant complexity for marginal benefit. The same code-reuse goals can be achieved through abstraction conformance + Smart Compilation, without the type-parameter syntax.

From the containers perspective, Khayyam's approach is closer in spirit to a strict "wrapper type per use case" discipline sometimes manually adopted in DDD-heavy codebases as a best practice, here made the only available path.

### Rust — Traits (Nominal Ad-hoc) + Generics (Parametric) + impl Blocks

Rust combines three polymorphism mechanisms: traits (ad-hoc, nominal), generics (parametric, with trait bounds), and `dyn Trait` objects (runtime subtype polymorphism). This is the most expressive polymorphism system in mainstream systems programming, but it comes at the cost of significant conceptual and syntactic complexity.

Khayyam deliberately avoids this combinatorial explosion. A single mechanism (abstraction conformance) with compiler-managed dispatch covers the same use cases, with less syntax surface area and fewer concepts for the developer to learn.

### Haskell — Type Classes (Ad-hoc) + Parametric Polymorphism

Haskell's type system is parametric by default: every function is implicitly polymorphic unless constrained. Type classes provide ad-hoc polymorphism by defining behavior sets that types can instantiate. This is elegant and powerful but requires a sophisticated type system that is difficult to implement in a systems language targeting C-level performance.

Khayyam's approach is closer to Go's pragmatic simplicity than Haskell's theoretical elegance. The abstraction mechanism provides the same "define behavior, let types conform" pattern as type classes, but without the higher-kinded types, type inference engine, and associated complexity.

### C++ — Templates (Unconstrained Parametric) + Virtual Functions (Subtype)

C++ provides two completely independent polymorphism mechanisms: templates (compile-time, unconstrained, duck-typed) and virtual functions (runtime, class-hierarchy-based). The C++ approach is the most flexible but also the most error-prone: template errors are notoriously hard to read, and the interaction between templates and virtual functions creates complex edge cases.

Khayyam's Smart Compilation can be seen as a unification of these two mechanisms: the compiler chooses between compile-time inlining (like template instantiation) and runtime dispatch (like virtual functions) based on what it can prove, without the developer managing two separate systems.

### Academic — Structural Subtyping as Parametric Polymorphism (Ghiotto et al., 2023)

The paper "Structural Subtyping as Parametric Polymorphism" (POPL 2023) formally demonstrates that structural subtyping and parametric polymorphism are encodable in each other within a suitably expressive type system. This provides theoretical backing for Khayyam's design: achieving parametric polymorphism through inclusion polymorphism (structural subtyping via abstraction conformance) does not sacrifice expressive power — it merely shifts where the type abstraction is expressed (in the abstraction definition vs. in the type parameter).

### Mainstream Languages — Generics as the Default

Statically typed mainstream languages (Java, C#, Rust, Go since 1.18) all provide generics as a core mechanism for type-safe containers. Khayyam's approach is the deliberate exception, grounded in the argument that generic containers structurally encourage the Anemic Domain Model by providing type-agnostic containers that have no room for domain-specific behavior. The domain-specific capsule pattern is not a limitation of Khayyam's type system — it is an expression of Khayyam's encapsulation philosophy applied to collections.

## Unresolved questions

### 1. Are There Concrete Use Cases Where Inclusion-Based Parametric Polymorphism Falls Short?

Khayyam achieves parametric polymorphism through inclusion polymorphism + Smart Compilation, and the theoretical argument (Ghiotto et al., 2023) supports their equivalence in expressive power. However, there may be practical edge cases where the abstraction-conformance mechanism cannot replicate what explicit type-parameter syntax provides. Specific scenarios to investigate:

- **Type-safe container abstractions:** Can `tp List ab { Count mt (self List) () (n Int) }` replace `List<T>` for all practical container use cases, or are there scenarios where the container's element type must be known at compile time for memory layout optimization in a way that abstraction conformance cannot express?
- **Compile-time computation on types:** Are there scenarios where a function needs to perform type-level computation (e.g., computing a buffer size based on a type's properties) that cannot be expressed through method calls on an abstraction?
- **Data-shape constraints:** Are there practical scenarios where constraining by data layout (not just behavior) is necessary, and cannot be worked around by exposing the layout through an abstraction method?

This question should be answered by attempting to implement a representative set of generic algorithms (sort, map, filter, reduce, binary search) using only abstraction conformance, and documenting any cases where the approach breaks down.

### 2. Should Abstraction Extension Support Multiple Inclusion Without Conflict Resolution?

When an abstraction `C` includes both `A` and `B`, and `A` and `B` both define a method with the same name and compatible signatures, what happens? Options include:

- **(a)** The method is required once (signature unification).
- **(b)** The capsule must implement the method separately for each abstraction's "view."
- **(c)** This is a compile-time error, and the developer must restructure the abstraction hierarchy.

This is the classic diamond problem from multiple inheritance. Khayyam avoids the worst case (behavior transfer), but the name collision issue remains. The answer affects how abstraction extension can be used in practice.

### 3. Can the Smart Compilation Strategy Be Extended to Devirtualization?

Devirtualization is an optimization where a runtime dispatch call is converted to a direct call when the compiler can prove the concrete type at a specific call site, even if the function was originally compiled for dynamic dispatch. This is common in JVM and .NET runtimes.

If Khayyam's compiler supports devirtualization (converting a VTable call to a direct call after initial dynamic compilation), it would mean that the monomorphization/dynamic-dispatch decision doesn't need to be made at compile time — it can be deferred and optimized incrementally. This would increase the optimization potential for plugin architectures and dynamically loaded code.

### 4. Should There Be a Mechanism for "Sealed" Abstractions?

A sealed abstraction is one that can only be satisfied by capsules defined within the same module or package. This is useful for modeling closed type hierarchies (e.g., `Result` with exactly two variants: `Ok` and `Err`). Without sealing, any external capsule could satisfy the abstraction, which may be undesirable for abstractions that represent a closed set of behaviors.

This could be expressed as a Linter rule (enforcing that only certain files can contain capsules satisfying a specific abstraction) rather than a language feature, consistent with Khayyam's governance philosophy.

### 5. Scaffolded Container Capsules: Version Control or Build-Time Generation?

Whether scaffolded concrete container capsules (e.g. a generated `connection_list.kh`) are intended to be committed to version control or generated fresh on every build is not yet settled; this affects IDE/autocomplete behavior before a build has run. This is a tooling-level question, not a language-design question, but it directly impacts the developer experience of working with domain-specific containers — the primary mechanism through which Khayyam achieves polymorphic container behavior without generic syntax.

## Future possibilities

### Polymorphic Data Structures Without Generics

If the open question about type-safe containers (Unresolved Question 1) is resolved favorably, Khayyam could support a standard library of polymorphic data structures (List, Map, Set, Queue) implemented purely through abstraction conformance. This would demonstrate that the "no generics" design is viable for practical, production-quality code.

### Cross-Language Polymorphism Mapping

A future RFC or engineering note could document the exact mapping from Khayyam's polymorphism to each target language:
- **Go target:** Khayyam abstraction → Go interface. Smart Compilation monomorphization → Go generic function instantiation.
- **Rust target:** Khayyam abstraction → Rust trait. Implicit satisfaction → generated `impl` blocks.
- **C target:** Khayyam abstraction → C header with function pointers (VTable struct). Monomorphization → static inline functions.

### Compile-Time Polymorphism Assertions

A future extension could allow developers to write compile-time assertions about polymorphic behavior, expressed as Linter rules rather than language syntax. For example: "All capsules satisfying `Serializer` must also satisfy `Clone`." This would be enforced at the organizational level, not at the language level.