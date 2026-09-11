---
Title: "Inheritance in Khayyam"
Status: Proposed
Start Date: "2026-07-10"
ID: 495467
---

# Inheritance in Khayyam
This document specifies how Khayyam models inheritance at the language level: where the relationship legitimately exists, what replaces the mechanisms other languages label "inheritance," and how the compiler and linter enforce the separation.

## Abstract
In Khayyam, inheritance is a relationship between abstractions, not between capsules. When an abstraction includes another abstraction, it extends the set of requirements that conforming capsules must satisfy — but no behavior is transferred. Capsules never acquire behavior from other capsules through "inheritance," method promotion, or any implicit mechanism. The only sanctioned mechanism for behavior sharing is **explicit delegation**: the developer writes a method on the host capsule that visibly forwards the call to an embedded instance. This document specifies the language-level consequences of that separation and how the compiler and linter enforce it. The principled foundation — including the conceptual challenge to "inheritance" as a model for behavioral transfer — is established in the [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) document.

## Introduction

### Motivation
Languages commonly label several distinct mechanisms "inheritance": class inheritance, trait default implementations, interface extension, struct embedding with method promotion. Khayyam needs a single authoritative statement of which of these relationships it supports, where each belongs, and what replaces those it rejects — otherwise every design discussion relitigates the vocabulary instead of the decision.

#### The Design Goal: Minimal Independent Concepts, Not Base Classes
Khayyam's type model is not designed to help developers find *base classes*. It is designed around a different search: identifying the minimal set of independent concepts a system needs, from which every other concept is derived by composition. Where an object-oriented design reaches for a base class to share structure or behavior down a hierarchy, a Khayyam design asks which independent concepts are actually present and composes them explicitly: requirements compose through abstraction inclusion, behavior composes through capsule composition with explicit delegation. Every rule in this document is a consequence of that goal — a base-class mechanism has no work to do in a model that derives complexity through composition.

Beyond terminology, allowing behavior to appear in a capsule without being defined there introduces concrete problems in Khayyam's context of high-performance libraries, compiler-level escape analysis, and behavioral predictability:

- **Hidden Behavior Paths:** Behavior transfer creates methods in a capsule that are not defined in that capsule's source code. The compiler must traverse external sources to determine the full method set, complicating escape analysis and other static analyses.
- **Linear Escape Analysis:** Khayyam's compiler relies on perfectly linear escape analysis for memory optimization. Methods acquired from external sources that access parent state create non-local references that break this linearity.
- **Abstraction Purity:** Khayyam's abstractions are pure contracts — no logic, no state, no predefined method bodies. Allowing behavior to be transferred from abstractions (via default implementations) would collapse this purity.

## Explanation

### Abstraction Extension: Inheritance Between Abstractions
Inheritance, understood as the transfer of requirements from one abstraction to another, is a legitimate and useful relationship. In Khayyam, abstractions can include other abstractions. When an abstraction includes another, it extends the set of requirements that conforming capsules must satisfy:

```khayyam
tp DataType ab {}

tp Error ab {
    DataType
}
```

`Error` includes `DataType`, meaning any capsule that conforms to `Error` must define DataType too. No behavior is transferred — the inclusion is purely declarative. The capsule that implements `Error` owns every method it defines.

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

Khayyam explicitly rejects this pattern. The compiler treats any attempt to call an embedded capsule's method directly on the host as an "Undefined Method" error. The linter detects when a developer appears to be attempting to use method promotion and suggests the exact explicit delegation needed.

#### Not All Embedding Is the Same
An important clarification: not all embedding serves the same purpose. In Go, embedding has two distinct effects:
1. **Protocol composition:** An embedded interface's method set is included in the outer interface's requirements. This is a *declarative* relationship — no behavior is transferred.
2. **Behavior acquisition:** An embedded struct's methods become available on the outer struct. This is a *behavioral* relationship — methods are implicitly promoted.

Khayyam distinguishes these cases clearly:
- **Abstraction inclusion** (combining abstraction requirements) is allowed. When one abstraction includes another, the requirements are extended — this is inheritance between abstractions.
- **Capsule embedding with method promotion** is rejected. A capsule's internal fields are private; their methods are not exposed.

### Template Method and Other OO Patterns
Traditional object-oriented design patterns that rely on behavior transfer — most notably Template Method, where a base class defines the skeleton of an algorithm and subclasses override specific steps — do not have a direct equivalent in Khayyam's model.

The alternative is to use **abstractions** and **explicit delegation**. Instead of a base class with a template method:
1. Define an abstraction that declares the customizable steps.
2. Have the "template" capsule accept implementations of those steps via its fields.
3. The "template" capsule explicitly calls the provided implementations.

This is functionally equivalent to Template Method but preserves explicit ownership: every method is defined in the capsule whose source code contains it. The alternative is more verbose than the pattern it replaces, and developers must learn it.

### Compiler Rules

**Rule: No Implicit Behavior Acquisition.**
Embedding a capsule inside another capsule does not expose the inner capsule's methods to the outer scope automatically. The compiler treats the inner capsule's methods as private to that capsule, even when accessed from the containing capsule's methods.

**Rule: Explicit Delegation Required.**
If a host capsule needs to expose a behavior of an embedded capsule, the developer must explicitly define a method on the host capsule and transparently delegate the call to the embedded instance. The compiler verifies that the delegation call exists in the host capsule's source code.

**Rule: Abstraction Conformance Is Structural.**
A capsule satisfies an abstraction if it implements all methods declared by that abstraction with identical signatures. The compiler validates this during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods result in a strict compile-time error.

**Rule: Abstractions Have No Behavior.**
An abstraction (`ab`) cannot contain method bodies, state, or default implementations. Methods declared by an abstraction are signatures only. This is enforced at the parser level.

### Linter Rules

**Anti-Lazy Inheritance Check:**
The linter blocks any patterns or workarounds that attempt to create implicit method promotion hooks. If a developer writes code that appears to be attempting to use behavior transfer (e.g. embedding a capsule and then calling its methods as if they were native), the linter flags this.

**Smart Remediation:**
When a compilation error occurs due to a missing method that actually exists within an embedded capsule, the linter detects this structural configuration and suggests the exact explicit delegation method to the developer. For example, if `TcpServer` tries to call `.Log()` but only its internal `Logger` has `Log`, the linter suggests:

```
Method 'Log' is not defined on TcpServer.
The embedded Logger has this method. Add explicit delegation:
  tp Log mt (self TcpServer) (msg String) (err Error) { ... }
```

**Abstraction Validation and DX Scaffolding:**
Since Khayyam avoids explicit implementation keywords (no `impl` or `implements`), the linter assists developers in satisfying abstractions:
- **Scaffolding:** When a developer intends to implement an abstraction (detected via context or explicit linter hints), the linter provides automated code generation to scaffold all missing method signatures with empty bodies. This reduces the boilerplate of explicit implementation without introducing hidden behavior.
- **Proactive Warnings:** The linter analyzes the codebase and issues warnings if a capsule partially implements an abstraction's method set in a context where it is clearly expected to satisfy that abstraction, preventing unexpected compilation failures.

**Orphan Rule (Monkey Patching Prevention):**
Khayyam relies on the file system for modularity (no `package` keyword). Syntactically, it is possible to import a type and attach new methods to it in another file. The linter differentiates between extending a *local directory type* (permitted for file-splitting) and mutating a *distant/external library type* (which triggers a strict warning or error). This prevents unpredictable monkey patching — a form of hidden behavior acquisition where methods appear on a type without being defined in its original source. If external extension is needed, the developer must use composition (wrapping the external capsule in a local one).

### Interaction with Smart Compilation
Khayyam's compiler decides whether to handle abstractions at compile time (monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (dynamic dispatch when underlying capsules are hidden). This decision is based on the dependency graph, not on any behavior transfer mechanism.

Since there is no behavior transfer between capsules, the compiler never needs to resolve virtual dispatch tables through chains. The method resolution is always direct: either the method is defined in the capsule, or the capsule explicitly delegates to another capsule. This simplification enables more aggressive compiler optimizations, including:
- **Perfectly linear escape analysis:** No externally-acquired methods create non-local references.
- **Devirtualization:** Without behavior-transfer-based polymorphism, more calls can be resolved statically.
- **Inlining:** Explicit delegation calls are straightforward candidates for inlining.
