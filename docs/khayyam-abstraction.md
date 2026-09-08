---
Title: "Abstraction in Khayyam"
Status: Proposed
Start Date: "2026-07-11"
ID: "495493"
---

# Abstraction in Khayyam
Abstractions in Khayyam occupy a conceptual space closely related to [IDL (Interface Description Language)](https://en.wikipedia.org/wiki/Interface_description_language) as used in protocol packages: both describe behavioral contracts that specify *what* is required without prescribing implementation details. Just as an IDL defines the data and operations exchanged between parties in a protocol, a Khayyam abstraction defines the method signatures a capsule must expose — serving as the language-level counterpart to a protocol specification.

This document consolidates all design decisions, resolved policies, and open questions related to the `ab` (abstraction) type in Khayyam into a single authoritative document. It supersedes two prior, now-absorbed drafts — one on intentional abstraction satisfaction, one on the rejection of default implementations — and merges them with the existing DX Scaffolding content into one cohesive specification.

## Abstract
Khayyam's abstraction (`ab`) is a **pure contract mechanism** with three resolved design properties and one open question:

1. **No executable logic.** An abstraction contains no method bodies — it describes *what* is required, never supplies *how*. Default implementations (as in Rust traits or Java `default` interface methods) are explicitly rejected.
2. **No generic syntax.** Abstractions carry no type parameters. Polymorphism classification and the rejection of generic syntax are documented in [Polymorphism in Khayyam](./khayyam-polymorphism.md).
3. **Implicit structural satisfaction.** A capsule satisfies an abstraction if it implements all required methods with matching signatures. No explicit `impl` or `implements` keyword exists.
4. **Open question — intentional satisfaction.** Whether purely structural satisfaction carries an accidental-satisfaction risk (as it does in Go), and if so, whether a mitigation mechanism is needed without compromising Khayyam's minimalism.

This document also states, as of this revision, a broader framing behind these choices than existed when they were first made: Khayyam asks what behavior a piece of code requires, not what concrete type identity it operates on — see *Behavior Over Type Identity*, below.

## Introduction

### Motivation

#### The Problem This Document Solves
Abstractions are the primary mechanism for polymorphism and decoupled architecture in most modern systems languages. However, every major language makes different — and often conflicting — tradeoffs in how abstractions are defined, satisfied, and compiled. These tradeoffs have real, measurable consequences for developer experience, compilation strategy, and long-term code maintainability.

Khayyam needs a single, coherent abstraction model that is consistent with its core philosophy of *Grammar Atomicity*, *Zero-Magic Core*, and *Strict Separation of Concerns*. Specifically, the abstraction system must:

- **Preserve syntactic minimalism.** Introducing generic syntax, explicit implementation keywords, or inheritance-like mechanisms adds grammar surface area that conflicts with the language's design goals.
- **Enable zero-cost abstraction where possible.** When the compiler knows the concrete type behind an abstraction, it should be able to inline the call — eliminating VTable overhead entirely — without the developer writing different code.
- **Maintain the pure-contract invariant.** An abstraction must never silently provide behavior, as this reintroduces the implicit routing and inheritance problems that Khayyam was designed to avoid.
- **Support organizational scalability.** In large codebases, developers need tooling assistance (scaffolding, validation, proactive warnings) to work with abstractions without the language itself growing heavier.

#### Concrete Pain Points Addressed
- **Go's accidental satisfaction problem.** In Go's structural typing system, any type with matching method signatures accidentally satisfies an interface. For marker-like abstractions (e.g., a small `Error` interface), an unrelated capsule can qualify without its author ever intending this. This document records this risk as an open question specific to Khayyam.
- **Rust's `impl` ceremony.** Rust requires explicit `impl Trait for Type` declarations at every implementation site. While this eliminates accidental satisfaction, it adds boilerplate that scales linearly with the number of abstraction-capsule pairs — in tension with Khayyam's minimalism goals for the common case.
- **Java/C# generic syntax complexity.** Explicit type parameters (`<T>`) force developers to expose implementation details that violate the principle of information hiding. Khayyam avoids this by carrying no type parameters on abstractions — see [Polymorphism in Khayyam](./khayyam-polymorphism.md) for the full polymorphism classification and rationale.
- **Default method inheritance confusion.** Rust's default trait methods and Java's `default` interface methods silently provide behavior from an abstraction, blurring the line between contract and implementation and making the execution path harder to reason about at compile time.

## Explanation

### What Is an Abstraction in Khayyam?
Think of an abstraction as a **behavioral specification** — a promise that a capsule will respond to certain method calls. The abstraction itself is inert: it has no state, no logic, and no runtime presence. It exists purely as a compile-time contract.

When you write `tp Reader ab`, you are telling the compiler: "There exists a concept called `Reader`. I will define the methods it requires separately. Any capsule that provides those methods can be used wherever a `Reader` is expected."

Khayyam treats abstraction as a pure contractual agreement. An abstraction represents behavior: if it requires an `Element`, it simply accepts `Element`. Any capsule that satisfies this interface is valid. The abstraction does not care about the concrete capsule's internal structure — it only cares about the behavioral contract. This "Contract-First Approach" means abstractions are implementation-agnostic by construction.

### Defining an Abstraction
An abstraction is defined with the `ab` subtype keyword. The required methods are defined independently, attached to the abstraction type as their receiver:

```khayyam
// Define the abstraction
tp Reader ab

// Define the methods it requires (body-less signatures)
tp Read mt (self Reader) (data Element) (err Error)
tp Close mt (self Reader) () (err Error)
```

An abstraction can also **compose other abstractions** by listing them inside its block. This is Khayyam's equivalent of interface inheritance — but purely contractual, with no behavior inherited:

```khayyam
tp Error ab {
    DataType
    Field_MediaType
    ADT
}
```

### Satisfying an Abstraction
A capsule satisfies an abstraction simply by implementing all of its required methods with matching signatures. No `implements` keyword is needed. The compiler verifies satisfaction at the point where the abstraction type is expected (assignment, parameter passing, etc.):

```khayyam
// A capsule that happens to satisfy Reader
tp FileReader cp {
    handle FileHandle
}

tp Read mt (self FileReader) (data Element) (err Error) { /* ... */ }
tp Close mt (self FileReader) () (err Error) { /* ... */ }

// The compiler accepts this because FileReader satisfies Reader
vr r Reader
r.CopyFrom(myFileReader)()  // validated at compile time — `r = myFileReader` is not Khayyam syntax.
```

See *Agency Beyond Concurrency* in [Agency in Khayyam](./khayyam-agency.md#agency-beyond-concurrency-intentional-vs-accidental-contract-satisfaction) for what this design choice means read through Agency's vocabulary.

### What You Cannot Do
- You **cannot** put a method body inside an abstraction definition. Abstractions are pure contracts.
- You **cannot** use a capsule type as an argument or return type in an abstraction's method signature — only other abstractions are allowed, ensuring the contract remains implementation-agnostic.
- You **cannot** explicitly declare "I implement this abstraction" using any keyword. Satisfaction is structural.
- You **cannot** define default implementations in an abstraction. Shared behavior must use explicit delegation to an ordinary capsule.

### Sharing Behavior Across Implementations
If multiple capsules need to share common behavior (e.g., a default "presence check" implementation reused by multiple types implementing the same abstraction), Khayyam requires **explicit delegation** rather than default implementations. You define the shared behavior in an ordinary capsule, and each implementing capsule explicitly delegates to it:

```khayyam
// Shared behavior lives in an ordinary capsule
tp PresenceHelper cp { /* ... */ }
tp CheckPresence mt (self PresenceHelper) () (result Bool, err Error) { /* ... */ }

// Each implementer explicitly delegates
tp Cache mt (self RedisStore) (result Bool) (err Error) {
   // explicit one-line delegation — no implicit inheritance
   self.helper.CheckPresence()(result, err)
}
```

This is deliberate, visible boilerplate. It keeps the execution path 100% explicit and linear, free of compiler magic or implicit routing.

### Dispatch Strategy
The compiler's mechanism for resolving polymorphic calls (monomorphization vs. dynamic dispatch) is documented in [Polymorphism in Khayyam](./khayyam-polymorphism.md).

### Abstraction Realization (Implicit Satisfaction)
Khayyam does not introduce any explicit syntax or keyword (such as `impl` or `implements`) to bind a capsule to an abstraction (`ab`). Abstraction realization is strictly implicit and structural at the compiler level.

- **Rule**: A capsule satisfies an `ab` if and only if it implements every method declared by that abstraction. For each such method, the influencing-variable types must match exactly, the influenced-variable types must match exactly or via covariant return (see [Covariant Return Types in Polymorphism](./khayyam-polymorphism.md#covariant-return-types)), and the receiver is the implementing capsule itself (not the abstraction). The example `tp Read mt (self FileReader) (data Element) (err Error)` therefore satisfies `tp Read mt (self Reader) (data Element) (err Error)` — the receiver differs by design.
- **Validation point**: The compiler validates abstraction satisfaction during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods will result in a strict compile-time error.

This design mirrors Go's interface satisfaction model at the language level. It eliminates the boilerplate of explicit implementation declarations (Rust's `impl Trait for Type`) and keeps the language grammar minimal. However, it also inherits Go's known risk of **accidental satisfaction**: an unrelated capsule can accidentally satisfy a small, marker-like abstraction if its method signatures happen to match — see [Abstraction in Khayyam Handoff](./khayyam-abstraction.handoff.md) for the status of this risk. For example, if a `FileLogger` capsule happens to define a `String()` method with the correct signature, it could accidentally qualify as a `Stringer` abstraction without its author ever intending this relationship. The risk is most acute for small abstractions with one or two methods, where signature collision is statistically more likely; for large abstractions with many methods, accidental satisfaction is practically impossible.

### Rejection of Default Implementations
Khayyam explicitly **rejects** default method implementations (also known as "default trait methods" in Rust or "default interface methods" in Java 8+). An abstraction (`ab`) is a pure contract with no executable logic of its own.

**Rationale:** Allowing executable logic inside an abstraction violates its contractual purity in two ways:

1. **It breaks the "what, not how" invariant.** An abstraction should describe *what* behavior is required, never silently supply *how* that behavior is implemented. When an abstraction contains a method body, it becomes a partial implementation — a hybrid that is neither a clean contract nor a clean type, making the execution path harder to reason about.
2. **It introduces implicit, dynamic routing behavior.** Default methods create a form of implicit inheritance: the method body lives in the abstraction, but executes in the context of the concrete capsule. This reintroduces the same class-hierarchy confusion that composition-over-inheritance patterns were designed to avoid, and it clouds compile-time optimization because the compiler can no longer assume the call target is a simple VTable entry or a monomorphized concrete method.

**The alternative — explicit delegation:** Shared behavior across multiple capsules lives in an ordinary capsule, and each implementer explicitly delegates to it. This is one line of boilerplate per implementation site, but it keeps the execution model completely transparent:

```khayyam
// Shared behavior capsule
tp DefaultValidator cp { /* ... */ }
tp Validate mt (self DefaultValidator) () (result Bool, err Error) { /* ... */ }

// Each implementer writes an explicit delegation line
tp Validate mt (self UserRecord) (result Bool) (err Error) {
   self.validator.Validate()(result, err)
}
```

**Tooling support for boilerplate reduction:** The elimination of repetitive delegation boilerplate is offloaded to organizational Linter and Scaffolding tooling. A Linter rule can:
- Detect when a capsule partially implements an abstraction's method set
- Auto-generate the missing delegation lines (scaffolding)
- Verify that the delegation call targets the correct shared capsule
- Warn if a developer appears to be hand-duplicating shared logic instead of delegating

This ensures the final source code remains 100% explicit, linear, and free of compiler magic, while the development workflow remains ergonomic.

### Abstraction Validation and DX Scaffolding
Because the language syntax avoids explicit implementation keywords, the burden of developer assistance shifts entirely to the Linter and associated tooling. This is consistent with Khayyam's philosophy of keeping the language grammar minimal and delegating governance to organizational tooling (the Memar framework). One concrete cost follows from this shift: without explicit `impl` declarations, discovering which capsules satisfy a given abstraction requires a tool-assisted graph traversal rather than a simple text search for `impl AbstractionName`, and the Linter and IDE tooling must provide this capability. This is a tooling burden, not a language burden, but it is a real cost in ecosystem maturity — a new Khayyam project will have less mature tooling than a new Rust project where `impl` blocks are trivially searchable.

- **Scaffolding**: When a developer intends to implement an abstraction (detected via context or explicit linter hints), the Linter provides automated code generation to scaffold all missing method signatures with empty bodies.
- **Proactive Warnings**: The Linter analyzes the codebase and issues warnings if a capsule partially implements an abstraction's method set in a context where it is clearly expected to satisfy that abstraction, preventing unexpected compilation failures.

### Behavior Over Type Identity
This may be the most important principle to have emerged from Khayyam's polymorphism discussions generally, not only from this document's own scope. Traditional generic systems frequently focus on type identity — `T`, `K`, `V` — as the central mechanism for abstraction. Khayyam instead emphasizes required behavior: the essential question is "what capabilities are required?" rather than "what concrete type is this?" This is the same question [*What Is an Abstraction in Khayyam?*](#what-is-an-abstraction-in-khayyam), above, already answers for abstraction satisfaction specifically; stated here as the more general principle behind it, since it recurred across discussions of generics, parametric polymorphism, containers, algorithms, and infrastructure components alike, not only abstraction satisfaction. A possible formulation: algorithms should declare the behaviors they require, not the concrete type identities they happen to operate on.

#### A Note on Parametric Polymorphism
Many canonical examples of parametric polymorphism are historically tied to limitations of other languages rather than to fundamental architectural requirements. `identity<T>()`, `swap<T>()`, `Option<T>`, and `Result<T,E>` exist, in several cases, primarily because of constraints such as single-return-value functions, nullability problems, exception models, and weak domain modeling. Where Khayyam removes those constraints — multiple influenced variables per method, no null/exception model of the kind that motivates `Option`/`Result` — some of these patterns become significantly less necessary in the first place, not merely re-solvable with different syntax.

This suggests generics discussions in Khayyam should not open with "how do we support generic syntax?" but with "why does this requirement exist in the first place, and does it still exist once Khayyam's own constraints are accounted for?" The specific compilation mechanism that follows once a real requirement is identified — how Khayyam's inclusion-based approach actually works and compiles — remains [Polymorphism in Khayyam](./khayyam-polymorphism.md)'s own subject, not this document's.

## Results
