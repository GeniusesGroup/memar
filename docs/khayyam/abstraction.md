---
Title: "Abstraction in Khayyam"
Status: Proposed
Start Date: "2026-07-11"
ID: "495493"
---

# Abstraction in Khayyam
Abstractions in Khayyam occupy a conceptual space closely related to [IDL (Interface Description Language)](https://en.wikipedia.org/wiki/Interface_description_language) as used in protocol packages: both describe behavioral requirements that specify *what* is required without prescribing implementation details. Just as an IDL defines the data and operations of a protocol's exchanges, a Khayyam abstraction defines the method signatures a capsule must expose — the language-level counterpart of a protocol's declared requirements. (The abstraction itself is not a contract: it names required behavior, not parties, obligations, or commitments — see [Protocol vs Contract](../protocol.md#protocol-vs-contract).)

This document consolidates all design decisions and resolved policies related to the `ab` (abstraction) type in Khayyam into a single authoritative document.

## Abstract
Khayyam's abstraction (`ab`) is a **pure behavioral specification** with four resolved design properties:

1. **No executable logic.** An abstraction contains no method bodies — it describes *what* is required, never supplies *how*. Default implementations (as in Rust traits or Java `default` interface methods) are explicitly rejected.
2. **No generic syntax.** Abstractions carry no type parameters. Polymorphism classification and the rejection of generic syntax are documented in [Polymorphism in Khayyam](./polymorphism.md).
3. **Implicit structural satisfaction.** A capsule satisfies an abstraction if it implements all required methods with matching signatures. No explicit `impl` or `implements` keyword exists.
4. **No language-level intent marker.** Satisfaction stays structural. A capsule that wants its satisfaction of an abstraction to read as deliberate composes an intent abstraction into its own definition and explicitly delegates the methods the abstraction it declares requires; the check applied to it is the ordinary structural one (see *Deliberate Satisfaction Is Composed, Not Declared*).

This document also states, as of this revision, a broader framing behind these choices than existed when they were first made: Khayyam asks what behavior a piece of code requires, not what concrete type identity it operates on — see *Behavior Over Type Identity*, below.

## Introduction

### Motivation

#### The Problem This Document Solves
Abstractions are the primary mechanism for polymorphism and decoupled architecture in most modern systems languages. However, every major language makes different — and often conflicting — tradeoffs in how abstractions are defined, satisfied, and compiled. These tradeoffs have real, measurable consequences for developer experience, compilation strategy, and long-term code maintainability.

Khayyam needs a single, coherent abstraction model that is consistent with its core philosophy of *Grammar Atomicity*, *Zero-Magic Core*, and *Strict Separation of Concerns*. Specifically, the abstraction system must:

- **Preserve syntactic minimalism.** Introducing generic syntax, explicit implementation keywords, or inheritance-like mechanisms adds grammar surface area that conflicts with the language's design goals.
- **Maintain the pure-specification invariant.** An abstraction must never silently provide behavior, as this reintroduces the implicit routing and inheritance problems that Khayyam was designed to avoid.
- **Support organizational scalability.** In large codebases, developers need tooling assistance (scaffolding, validation, proactive warnings) to work with abstractions without the language itself growing heavier.

#### Concrete Pain Points Addressed
- **Go's accidental satisfaction problem.** In Go's structural typing system, any type with matching method signatures accidentally satisfies an interface. For marker-like abstractions (e.g., a small `Error` interface), an unrelated capsule can qualify without its author ever intending this. Khayyam keeps structural satisfaction and answers this risk by composition and explicit delegation rather than by grammar — see *Deliberate Satisfaction Is Composed, Not Declared*, below.
- **Rust's `impl` ceremony.** Rust requires explicit `impl Trait for Type` declarations at every implementation site. While this eliminates accidental satisfaction, it adds boilerplate that scales linearly with the number of abstraction-capsule pairs — in tension with Khayyam's minimalism goals for the common case.
- **Java/C# generic syntax complexity.** Explicit type parameters (`<T>`) force developers to expose implementation details that violate the principle of information hiding. Khayyam avoids this by carrying no type parameters on abstractions — see [Polymorphism in Khayyam](./polymorphism.md) for the full polymorphism classification and rationale.
- **Default method inheritance confusion.** Rust's default trait methods and Java's `default` interface methods silently provide behavior from an abstraction, blurring the line between specification and implementation and making the execution path harder to reason about at compile time.

## Explanation

### What Is an Abstraction in Khayyam?
Think of an abstraction as a **behavioral specification** — a declaration that a capsule will respond to certain method calls. The abstraction itself is inert: it has no state, no logic, and no runtime presence. It exists purely as a compile-time declaration of required behavior — not a contract: it creates no parties, no reciprocal obligations, and no commitments (see [Protocol vs Contract](../protocol.md#protocol-vs-contract)).

When you write `tp Reader ab`, you are declaring: "There exists a concept called `Reader`. The methods it requires are defined separately. Any capsule that provides those methods can be used wherever a `Reader` is expected."

Khayyam treats abstraction as a one-sided declaration of required behavior. An abstraction represents behavior: if it requires an `Element`, it simply accepts `Element`. Any capsule that provides those methods is valid. The abstraction does not care about the concrete capsule's internal structure — it only cares about the declared behavioral surface. This means abstractions are implementation-agnostic by construction.

### Defining an Abstraction
An abstraction is defined with the `ab` subtype keyword. The required methods are defined independently, attached to the abstraction type as their receiver:

```khayyam
// Define the abstraction
tp Reader ab

// Define the methods it requires (body-less signatures)
tp Read mt (self Reader) (data Element) (err Error)
tp Close mt (self Reader) () (err Error)

// Abstractions referenced by those signatures
tp Element ab
tp Error ab
```

In these examples `Element` and `Error` are abstractions — declared behavior, not capsule types. Per *What You Cannot Do*, only abstractions may appear in an abstraction-owned method signature; a primitive capsule (`W32`, `W64`, …) or a concrete capsule there is invalid.

An abstraction can also **compose other abstractions** by listing them inside its block. This is Khayyam's equivalent of interface inheritance — declared requirements compose, with no behavior inherited:

```khayyam
tp Error ab {
    Type
    Field_MediaType
    ADT
}
```

### Satisfying an Abstraction
A capsule satisfies an abstraction simply by implementing all of its required methods with matching signatures. No `implements` keyword is needed. Satisfaction is judged wherever an abstraction type is required — where a value is declared as one, or where it is passed to a position declared with one.

```khayyam
// A capsule that happens to satisfy Reader
tp FileReader cp {
    handle FileHandle
}

tp Read mt (self FileReader) (data Element) (err Error) { /* ... */ }
tp Close mt (self FileReader) () (err Error) { /* ... */ }

// `r` may name a `FileReader` here: `FileReader` satisfies `Reader`
vr r Reader
r.CopyFrom(myFileReader)()  // validated at compile time — `r = myFileReader` is not Khayyam syntax.
```

See *Agency Beyond Concurrency* in [Agency in Khayyam](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-abstraction-satisfaction) for what this design choice means read through Agency's vocabulary.

### What You Cannot Do
- You **cannot** put a method body inside an abstraction definition. Abstractions declare required behavior only.
- You **cannot** use a capsule type as an argument or return type in an abstraction's method signature — only other abstractions are allowed, ensuring the specification remains implementation-agnostic.
- You **cannot** explicitly declare "I implement this abstraction" using any keyword. Satisfaction is structural; deliberate satisfaction is expressed by composition and delegation, never by grammar (*Deliberate Satisfaction Is Composed, Not Declared*).
- You **cannot** define default implementations in an abstraction. Shared behavior must use explicit delegation to an ordinary capsule.

### A Concept Is an Abstraction; a Concrete Instance Is a Capsule
A name that carries a concept is declared as an abstraction, and a concrete instance of that concept — a width, a unit, one representation of a value — is declared as a capsule. `Error`, `Duration`, `Signed`, and `Boolean` name concepts and are abstractions; `I32`, `Second`, and `Bool` are concrete and are capsules, each an instance of its concept by satisfying it ([Abstraction Realization](#abstraction-realization-implicit-satisfaction)). Neither is declared as the other.

Which of the two a signature names follows from who owns the signature:
1. A signature owned by an abstraction names the concept — `Signed` for a signed integer of any width, `Duration` for a span in any unit, `Boolean` for a truth value — because it may name abstractions only ([What You Cannot Do](#what-you-cannot-do)).
2. A signature owned by a capsule may name a capsule, including the capsule itself.

What a contract names is the concept; the unit or width it is measured in is the implementation's to choose, finer-grained, and never a floor the contract must meet. An implementation is free to be more precise than what it is asked for, and asking for less is what keeps it so: a contract that fixed a unit or a width would make every implementation of it exactly that resolution, for no gain in meaning. What the contract keeps is the magnitude asked for — the span, the count — and it loses only the measure that magnitude is expressed in.

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

This is deliberate, visible boilerplate. It keeps the execution path explicit and linear, with no implicit routing.

### Dispatch Strategy
The grammar states no strategy for resolving a call through an abstraction and offers no syntax to choose one; what a Khayyam compiler does at a given call site is [Compiler](../modules/computer/compiler.md)'s business.

### Abstraction Realization (Implicit Satisfaction)
Khayyam does not introduce any explicit syntax or keyword (such as `impl` or `implements`) to bind a capsule to an abstraction (`ab`). Abstraction realization is strictly implicit and structural.

- **Rule**: A capsule satisfies an `ab` if and only if it implements every method declared by that abstraction. For each such method, the influencing-variable types must match exactly, the influenced-variable types must match exactly or via covariant return (see [Covariant Return Types in Polymorphism](./polymorphism.md#covariant-return-types)), and the receiver is the implementing capsule itself (not the abstraction). The example `tp Read mt (self FileReader) (data Element) (err Error)` therefore satisfies `tp Read mt (self Reader) (data Element) (err Error)` — the receiver differs by design.
- **Where it is judged**: wherever an abstraction type is required — a `vr` declared as one, or a value passed to a position declared with one. A capsule missing a required method, or declaring one with a signature that does not match, does not satisfy the abstraction.

This design mirrors Go's interface satisfaction model at the language level. It eliminates the boilerplate of explicit implementation declarations (Rust's `impl Trait for Type`) and keeps the language grammar minimal. However, it also inherits Go's known risk of **accidental satisfaction**: an unrelated capsule can accidentally satisfy a small, marker-like abstraction if its method signatures happen to match. For example, if a `FileLogger` capsule happens to define a `String()` method with the correct signature, it could accidentally qualify as a `Stringer` abstraction without its author ever intending this relationship. The risk is most acute for small abstractions with one or two methods, where signature collision is statistically more likely; for large abstractions with many methods, accidental satisfaction is practically impossible. Khayyam answers this risk with composition and delegation rather than with a nominal declaration: see *Deliberate Satisfaction Is Composed, Not Declared*, below.

### Deliberate Satisfaction Is Composed, Not Declared
The language does not intervene in satisfaction. A capsule cannot name the abstraction it satisfies, cannot seal a declaration that only a matching implementation could enter, and the grammar carries no intent marker of any kind. This is the position [abstraction_p.Implements](../modules/computer/abstraction-implements.md) already takes at the protocol level, where an intent to implement an abstraction is itself an abstraction a capsule may compose into its own definition — see its [*Declaring and discovering intent*](../modules/computer/abstraction-implements.md#declaring-and-discovering-intent).

A capsule that wants its satisfaction of an abstraction to read as deliberate composes an intent abstraction and explicitly delegates the methods the abstraction it declares requires, naming a capsule that owns the behavior. [*Rejection of Default Implementations*](#rejection-of-default-implementations) already requires each of those methods to be written in the implementing capsule, and [Type → Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) requires every method of a component to be defined in its own source or explicitly delegated by it:

```khayyam
// The intent is an ordinary abstraction, named for the abstraction it declares
tp ImplementsError ab

// A capsule that deliberately satisfies Error composes the intent and
// explicitly delegates each required method to a helper that owns the behavior
tp ErrServiceNotFound cp {
    ImplementsError
    helper ErrNotFoundImpl
}

tp IsRetryable mt (self ErrServiceNotFound) (result Bool) (err Error) {
   self.helper.IsRetryable()(result, err)
}
```

The intent abstraction is then satisfied by the ordinary structural check — wherever an abstraction type is required, the same signature comparison decides, and a missing or unmatched method is the same failure it is for any other abstraction. Declaring the intent grants no exemption from satisfaction and no guarantee beyond it; what it adds is the undertaking itself, written in the capsule's own source beside the delegations that discharge it, where tooling and readers find it.

For the same reason no verification mechanism of its own is called for. The delegations are ordinary source and the intent abstraction is judged by the ordinary rule, so a deliberate declaration is judged the way any other satisfier is.

### Rejection of Default Implementations
Khayyam explicitly **rejects** default method implementations (also known as "default trait methods" in Rust or "default interface methods" in Java 8+). An abstraction (`ab`) is a pure behavioral declaration with no executable logic of its own.

**Rationale:** Allowing executable logic inside an abstraction violates its purity as a declaration of required behavior in two ways:

1. **It breaks the "what, not how" invariant.** An abstraction should describe *what* behavior is required, never silently supply *how* that behavior is implemented. When an abstraction contains a method body, it becomes a partial implementation — a hybrid that is neither a clean specification nor a clean type, making the execution path harder to reason about.
2. **It introduces implicit, dynamic routing behavior.** Default methods create a form of implicit inheritance: the method body lives in the abstraction, but executes in the context of the concrete capsule. This reintroduces the same class-hierarchy confusion that composition-over-inheritance patterns were designed to avoid.

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

### Abstraction Validation and DX Scaffolding
The grammar has no implementation keyword, so which capsules satisfy a given abstraction is not written at any one place in source; finding them, and generating or verifying delegation, is tooling's work, not the language's.

### Behavior Over Type Identity
This may be the most important principle to have emerged from Khayyam's polymorphism discussions generally, not only from this document's own scope. Traditional generic systems frequently focus on type identity — `T`, `K`, `V` — as the central mechanism for abstraction. Khayyam instead emphasizes required behavior: the essential question is "what capabilities are required?" rather than "what concrete type is this?" This is the same question [*What Is an Abstraction in Khayyam?*](#what-is-an-abstraction-in-khayyam), above, already answers for abstraction satisfaction specifically; stated here as the more general principle behind it, since it recurred across discussions of generics, parametric polymorphism, containers, algorithms, and infrastructure components alike, not only abstraction satisfaction. A possible formulation: algorithms should declare the behaviors they require, not the concrete type identities they happen to operate on.

#### A Note on Parametric Polymorphism
Many canonical examples of parametric polymorphism are historically tied to limitations of other languages rather than to fundamental architectural requirements. `identity<T>()`, `swap<T>()`, `Option<T>`, and `Result<T,E>` exist, in several cases, primarily because of constraints such as single-return-value functions, nullability problems, exception models, and weak domain modeling. Where Khayyam removes those constraints — multiple influenced variables per method, no null/exception model of the kind that motivates `Option`/`Result` — some of these patterns become significantly less necessary in the first place, not merely re-solvable with different syntax.

This suggests generics discussions in Khayyam should not open with "how do we support generic syntax?" but with "why does this requirement exist in the first place, and does it still exist once Khayyam's own constraints are accounted for?" The specific compilation mechanism that follows once a real requirement is identified — how Khayyam's inclusion-based approach actually works and compiles — remains [Polymorphism in Khayyam](./polymorphism.md)'s own subject, not this document's.
