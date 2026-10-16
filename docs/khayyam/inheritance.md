---
Title: "Inheritance in Khayyam"
Status: Proposed
Start Date: "2026-07-10"
ID: 495467
---

# Inheritance in Khayyam
This document specifies how Khayyam models inheritance at the language level: where the relationship legitimately exists, and what replaces the mechanisms other languages label "inheritance."

## Abstract
In Khayyam, inheritance is a relationship between abstractions, not between capsules. When an abstraction includes another abstraction, it extends the set of requirements that conforming capsules must satisfy — but no behavior is transferred. Capsules never acquire behavior from other capsules through "inheritance," method promotion, or any implicit mechanism. The only sanctioned mechanism for behavior sharing is **explicit delegation**: a method on the host capsule that visibly forwards the call to an embedded instance. This document specifies the language-level consequences of that separation. The principled foundation — including the conceptual challenge to "inheritance" as a model for behavioral transfer — is established in the [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) document.

## Introduction

### Motivation
Languages commonly label several distinct mechanisms "inheritance": class inheritance, trait default implementations, interface extension, struct embedding with method promotion. Khayyam needs a single authoritative statement of which of these relationships it supports, where each belongs, and what replaces those it rejects — otherwise every design discussion relitigates the vocabulary instead of the decision.

#### The Design Goal: Minimal Independent Concepts, Not Base Classes
Khayyam's type model is not designed to help developers find *base classes*. It is designed around a different search: identifying the minimal set of independent concepts a system needs, from which every other concept is derived by composition. Where an object-oriented design reaches for a base class to share structure or behavior down a hierarchy, a Khayyam design asks which independent concepts are actually present and composes them explicitly: requirements compose through abstraction inclusion, behavior composes through capsule composition with explicit delegation. Every rule in this document is a consequence of that goal — a base-class mechanism has no work to do in a model that derives complexity through composition.

Beyond terminology, allowing behavior to appear in a capsule without being defined there conflicts with this model's stated commitments:

- **Abstraction Purity:** Khayyam's abstractions are pure behavioral specifications — no logic, no state, no predefined method bodies. Allowing behavior to be transferred from abstractions (via default implementations) would collapse this purity.
- **Own Definitions Only:** a method a capsule has but did not define is a method a reader of that capsule's source cannot account for. Requiring every method a capsule answers to be defined in that capsule is the same requirement Sovereign Encapsulation places on state.

## Explanation

### Abstraction Extension: Inheritance Between Abstractions
Inheritance, understood as the transfer of requirements from one abstraction to another, is a legitimate and useful relationship. In Khayyam, abstractions can include other abstractions. When an abstraction includes another, it extends the set of requirements that conforming capsules must satisfy. The Error module's `Error` is the case: its block, declared once in [`error.kh`](../../modules/process/error/protocol/error.kh), lists `Type` among the abstractions it includes, and `Type` is itself an abstraction ([`type.kh`](../../modules/computer/type/protocol/type.kh)).

`Error` includes `Type`, meaning any capsule that conforms to `Error` must define `Type` too. No behavior is transferred — the inclusion is purely declarative. The capsule that implements `Error` owns every method it defines.

This is inheritance in its correct sense: requirements flow from one abstraction to another, and the implementing capsule explicitly satisfies all of them.

### Capsule Composition Without Method Promotion
A capsule can contain other capsules as internal fields. However, **embedding a capsule does not automatically expose the inner capsule's methods to the outer capsule.** If a host capsule needs to expose a behavior of an embedded capsule, the developer must explicitly define a method on the host capsule and delegate the call.

Consider a practical scenario. A `TcpServer` capsule might internally use a `Logger` capsule for logging:

```khayyam
tp Logger cp {
    // Logger's internal state (hidden)
}

tp Log mt (self Logger) (msg String) (err Error) {
    // Logger's log implementation
}

tp TcpServer cp {
    // TcpServer's internal state (hidden)
    // Logger is an internal field — its methods are NOT available on TcpServer
}
```

If `TcpServer` needs to log, it must explicitly expose that capability:

```khayyam
tp Log mt (self TcpServer) (msg String) (err Error) {
    // Explicit delegation: TcpServer.Log delegates to its internal logger
    // The delegation is visible — readers can see what happens
}
```

The call chain is fully visible in the source code. No method "appears" on `TcpServer` without being defined there.

#### No Method Promotion
Method promotion is the mechanism by which a language automatically makes an embedded type's methods available on the containing type. Go's struct embedding is the most well-known example:

```go
// Go: method promotion
type Reader interface { Read() }
type File struct{}
func (f File) Read() { /* ... */ }
type MyCapsule struct { File }  // MyCapsule now has Read() implicitly
```

In this Go example, `MyCapsule` acquires `Read()` without defining it. The method is *promoted* from `File` to `MyCapsule` automatically. A developer reading `MyCapsule`'s source code would not see `Read()` defined there, yet it is available.

Khayyam explicitly rejects this pattern. Calling an embedded capsule's method directly on the host names a method the host does not define, and no declaration provides it.

#### Not All Embedding Is the Same
An important clarification: not all embedding serves the same purpose. In Go, embedding has two distinct effects:
1. **Protocol composition:** An embedded interface's method set is included in the outer interface's requirements. This is a *declarative* relationship — no behavior is transferred.
2. **Behavior acquisition:** An embedded struct's methods become available on the outer struct. This is a *behavioral* relationship — methods are implicitly promoted.

Khayyam distinguishes these cases clearly:
- **Abstraction inclusion** (combining abstraction requirements) is allowed. When one abstraction includes another, the requirements are extended — this is inheritance between abstractions.
- **Capsule embedding with method promotion** is rejected. A capsule's internal fields are private; their methods are not exposed.

### Template Method and Other OO Patterns
Traditional object-oriented design patterns that rely on behavior transfer — most notably Template Method, where a base class defines the skeleton of an algorithm and subclasses override specific steps — have no counterpart in Khayyam's model: there is no construct that places behavior in a type other than the one that defines it.

The model's substitute for that pattern is capsule composition: a capsule declares the abstractions its steps satisfy as fields, and its own methods call those steps. Every method involved is defined in the capsule whose source contains it. The alternative is more verbose than the pattern it replaces, and developers must learn it.

### Rules
**Rule: No Implicit Behavior Acquisition.**
Embedding a capsule inside another capsule does not expose the inner capsule's methods to the outer scope automatically. The inner capsule's methods belong to that capsule, including when reached from the containing capsule's methods.

**Rule: Explicit Delegation Required.**
If a host capsule offers a behavior of an embedded capsule, a method on the host capsule declares it and forwards the call to the embedded instance.

**Rule: Abstraction Conformance Is Structural.**
A capsule satisfies an abstraction if it implements every method declared by that abstraction. For each such method, the influencing-variable types must match exactly, the influenced-variable types must match exactly or by covariant return as specified in [Polymorphism → Covariant Return Types](./polymorphism.md#covariant-return-types), and the implementing method's receiver is the capsule, not the abstraction. The same rule is stated from the satisfaction side in [Abstraction Realization (Implicit Satisfaction)](./abstraction.md#abstraction-realization-implicit-satisfaction).

**Rule: Abstractions Have No Behavior.**
An abstraction (`ab`) cannot contain method bodies, state, or default implementations. Methods declared by an abstraction are signatures only.

Since there is no behavior transfer between capsules, a method a capsule answers to is either defined in it or reached through a method it declares itself. How each of those calls is carried out is a compiler's business ([Compiler](../../modules/computer/compiler/compiler.md)).

