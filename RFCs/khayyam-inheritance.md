---
Title: "Inheritance in Khayyam"
Status: Proposed
Start Date: 2026-07-10
RFC Number: 495467
Applied to: ["Khayyam.md"]
Related RFCs:
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Depends_on"
      Explanation: "Defines Protocol as a pure declarative specification. This RFC builds on that definition to explain how abstraction inclusion creates inheritance relationships between abstractions."
    - Title: "Explicit Behavior Ownership"
      URI: "./explicit_behavior_ownership.md"
      Reason: "Depends_on"
      Explanation: "EBO provides the principled foundation that behavior transfer between capsules is rejected. This RFC specifies the language-level enforcement of that principle."
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Core language design decisions, placement of inheritance in the abstraction layer, rejection of behavior transfer between capsules"
    task: []
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: ""
    contribution: "Drafted initial text for the original monolithic Protocol RFC; portions of the behavior transfer and method promotion analysis were incorporated from that draft"
    task: []
  - name: "Super Z"
    uri: "https://z.ai"
    model: "GLM"
    effort: "Medium"
    contribution: "Restructured this RFC from 'Rejection of Inheritance' to 'Inheritance in Khayyam,' reframing the topic as placement (inheritance belongs to abstractions, not capsules) rather than rejection. Added subtyping section with correct Khayyam syntax. Unified terminology with EBO RFC."
    task: ["reframe", "terminology-unification", "subtyping-section", "content-reorganization"]
---

# Inheritance in Khayyam

## Summary
In Khayyam, inheritance is a relationship between abstractions, not between capsules. When an abstraction includes another abstraction, it extends the set of requirements that conforming capsules must satisfy — but no behavior is transferred. Capsules never acquire behavior from other capsules through "inheritance," method promotion, or any implicit mechanism. The only sanctioned mechanism for behavior sharing is **explicit delegation**: the developer writes a method on the host capsule that visibly forwards the call to an embedded instance. This RFC specifies how Khayyam models inheritance at the language level and how the compiler and linter enforce the separation between abstraction extension (allowed) and behavior transfer between capsules (rejected). The principled foundation for this separation — including the conceptual challenge to "inheritance" as a model for behavioral transfer — is established in the [Explicit Behavior Ownership](./explicit_behavior_ownership.md) RFC.

## Motivation

### Where Inheritance Belongs
Inheritance, understood as the transfer of requirements from one abstraction to another, is a legitimate and useful relationship. In Khayyam, this relationship exists between abstractions: when abstraction A includes abstraction B, any capsule conforming to A must also satisfy B's requirements. The requirements are extended; no behavior is transferred.

What Khayyam rejects is the transfer of **behavior** (method implementations) between capsules. The mechanisms that other languages label "inheritance" — class inheritance, trait default implementations, method promotion through embedding — all share one property: a method appears in a capsule without that capsule's source code defining it. The principled case for why this is problematic is made in the [Explicit Behavior Ownership](./explicit_behavior_ownership.md) RFC. This RFC addresses the language-level consequences: how the compiler enforces the rule, what alternatives developers use, and what practical effects this has on compilation, analysis, and design patterns.

### Practical Problems with Behavior Transfer in Khayyam's Context
Khayyam is designed for building high-performance libraries and applications where compiler-level escape analysis, memory safety, and behavioral predictability are paramount. Allowing behavior to appear in a capsule without being defined there introduces several practical problems:

- **Hidden Behavior Paths:** Behavior transfer creates methods in a capsule that are not defined in that capsule's source code. The compiler must traverse external sources to determine the full method set, complicating escape analysis and other static analyses.
- **Linear Escape Analysis:** Khayyam's compiler relies on perfectly linear escape analysis for memory optimization. Methods acquired from external sources that access parent state create non-local references that break this linearity.
- **Abstraction Purity:** Khayyam's abstractions are designed as pure contracts — no logic, no state, no predefined method bodies. Allowing behavior to be transferred from abstractions (via default implementations) would collapse this purity.

## Guide-level Explanation

### Abstraction Extension: Inheritance Between Abstractions
In Khayyam, abstractions can include other abstractions. When an abstraction includes another, it extends the set of requirements that conforming capsules must satisfy:

```khayyam
tp Hasher ab {}

tp hash mt (self Hasher) (data Bytes) (h UInt64)

tp SaltyHasher ab {
    Hasher
}

tp salt mt (self SaltyHasher) () (h Bytes)
```

`SaltyHasher` includes `Hasher`, meaning any capsule that conforms to `SaltyHasher` must define both `hash()` and `salt()`. No behavior is transferred — the inclusion is purely declarative. The capsule that implements `SaltyHasher` owns every method it defines.

This is inheritance in its correct sense: requirements flow from one abstraction to another, and the implementing capsule explicitly satisfies all of them.

### Subtyping Through Abstraction Conformance
Abstraction inclusion creates a subtyping relationship. A capsule that conforms to `SaltyHasher` can be used wherever `Hasher` is expected, because `SaltyHasher` includes `Hasher`'s requirements. This is a structural subtyping relationship based on abstraction extension, not on behavior transfer.

For example, a function that accepts any `Hasher`:

```khayyam
tp Process mt (self Service) (h Hasher) (data Bytes) -> UInt64 {
    return h.hash(data)
}
```

A capsule that conforms to `SaltyHasher` (and therefore also to `Hasher`) can be passed to this function. The subtyping is established at the abstraction level; the behavior is owned by the conforming capsule.

This is one of the forms that polymorphism takes in Khayyam. A deeper treatment of polymorphism is left to a dedicated RFC.

### Capsule Composition: No Method Promotion
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

### No Method Promotion
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

### Not All Embedding Is the Same
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

This is functionally equivalent to Template Method but preserves explicit ownership: every method is defined in the capsule whose source code contains it.

## Reference-level Explanation

### Compiler Rules

**Rule: No Implicit Behavior Acquisition.**
Embedding a capsule inside another capsule does not expose the inner capsule's methods to the outer scope automatically. The compiler must treat the inner capsule's methods as private to that capsule, even when accessed from the containing capsule's methods.

**Rule: Explicit Delegation Required.**
If a host capsule needs to expose a behavior of an embedded capsule, the developer must explicitly define a method on the host capsule and transparently delegate the call to the embedded instance. The compiler must verify that the delegation call exists in the host capsule's source code.

**Rule: Abstraction Conformance is Structural.**
A capsule satisfies an abstraction if it implements all methods declared by that abstraction with identical signatures. The compiler validates this during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods result in a strict compile-time error.

**Rule: Abstractions Have No Behavior.**
An abstraction (`ab`) cannot contain method bodies, state, or default implementations. Methods declared by an abstraction are signatures only. This is enforced at the parser level.

### Linter Rules

**Anti-Lazy Inheritance Check:**
The linter blocks any patterns or workarounds that attempt to create implicit method promotion hooks. If a developer writes code that appears to be attempting to use behavior transfer (e.g., embedding a capsule and then calling its methods as if they were native), the linter flags this.

**Smart Remediation:**
When a compilation error occurs due to a missing method that actually exists within an embedded capsule, the linter must detect this structural configuration and suggest the exact explicit delegation method to the developer. For example, if `TcpServer` tries to call `.Log()` but only its internal `Logger` has `Log`, the linter suggests:
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
Khayyam's compiler intelligently decides whether to handle abstractions at compile-time (monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (dynamic dispatch when underlying capsules are hidden). This decision is based on the dependency graph, not on any behavior transfer mechanism.

Since there is no behavior transfer between capsules, the compiler never needs to resolve virtual dispatch tables through chains. The method resolution is always direct: either the method is defined in the capsule, or the capsule explicitly delegates to another capsule. This simplification enables more aggressive compiler optimizations, including:
- **Perfectly linear escape analysis:** No externally-acquired methods create non-local references.
- **Devirtualization:** Without behavior-transfer-based polymorphism, more calls can be resolved statically.
- **Inlining:** Explicit delegation calls are straightforward candidates for inlining.

## Drawbacks
- **No Direct Template Method Pattern:** The traditional Template Method pattern relies on behavior transfer and does not have a direct syntactic equivalent. The alternative (abstraction + explicit delegation) is more verbose but functionally equivalent. Developers must learn the alternative pattern.
- **More Explicit Code:** Every behavior must be written explicitly. For large component structures where many components share similar behavior, this results in more source code. In the AI era, this is less a cost and more a structural advantage: AI-generated delegation code is cheap to produce, and the resulting explicit structure makes the codebase more legible to both human and AI participants. The source code is undeniably longer, but length is not the relevant metric — legibility is.
- **Design Pattern Migration:** Teams migrating from OO languages (Java, C#, C++) must reformulate behavior-transfer-based designs. This is not just a syntax change — it requires rethinking the architectural relationships between components.
- **No "Base Class" Convenience:** Common patterns like a `BaseService` class that provides shared infrastructure (logging, configuration, error handling) to all service subclasses do not translate directly. Each service must explicitly compose its infrastructure.

## Rationale and Alternatives

### Why Not Allow "Safe" Behavior Transfer?
An alternative is to allow restricted behavior transfer — for example, "single inheritance is allowed but only from abstract base classes" or "inheritance is allowed but the base class cannot have concrete methods." This was rejected. The principled argument is in the EBO RFC (see "Why Not Accept 'Controlled' Hidden Behavior?"). At the language level, the additional concern is that even restricted behavior transfer creates conceptual dependency on the transfer model that influences how developers think about component relationships, and the "safe" boundaries are subjective and tend to erode over time as exceptions are added.

### Why Not Use Go-Style Embedding?
Go's embedding is often cited as a "middle ground" between behavior transfer and composition. It provides method promotion without the full complexity of class-based behavior transfer. This was rejected because method promotion is still implicit behavior acquisition — the embedding component's source code does not show the promoted methods. The visibility problem remains, just in a milder form.

### Why Not Use Rust-Style Traits with Defaults?
Rust traits allow default method implementations, which provide behavior sharing without traditional class-based behavior transfer. This was rejected because default implementations introduce the same ownership ambiguity that EBO prohibits: a method exists in a type but the type's source code does not define it. The default method's implementation lives in the trait, creating dual ownership.

### Impact of Not Doing This
If Khayyam allowed behavior transfer between capsules, every subsequent design decision would need to account for chains, method resolution order, and hidden behavior paths. The compiler would need to support virtual dispatch tables, the linter would need to trace hierarchies, and developers would need to mentally simulate chains to understand a capsule's full behavior. By establishing at the foundation that behavior transfer between capsules does not exist, all of this complexity is eliminated.

## Prior Art

- **Go Struct Embedding:** Go allows embedding structs and interfaces within other structs. Embedded struct methods are promoted to the outer struct. This is the most well-known "composition with promotion" mechanism. Khayyam rejects the promotion aspect while keeping the composition aspect (capsules can contain other capsules as fields). Go's interface-level embedding (interface inclusion) aligns with Khayyam's abstraction extension.
- **Rust Traits:** Rust traits can have default method implementations and blanket implementations. Both introduce behavior without the implementing type's source code defining it. Khayyam rejects both, keeping traits (abstractions) as pure declarations.
- **Java Class Inheritance:** Java supports single class inheritance with concrete method bodies and multi-interface implementation. Java 8+ added default interface methods. Khayyam rejects all forms of behavior transfer and default methods. Java's interface extension (without defaults) aligns with Khayyam's abstraction extension.
- **C++ Multiple Inheritance:** C++ allows multiple inheritance with concrete method bodies, including the diamond problem. Khayyam's rejection of behavior transfer between capsules eliminates this class of problems entirely.
- **Swift Protocols with Extensions:** Swift protocols can be extended with default implementations via protocol extensions. This allows behavior injection that is invisible at the conforming type's definition site. Khayyam rejects this pattern.
- **Kotlin Open Classes:** Kotlin marks classes as `open` to allow inheritance, with `final` as the default. This is a more conservative approach than Java's, but still allows behavior transfer when opted in. Khayyam does not provide behavior transfer between capsules at all.
- **Zig Comptime and Delegation:** Zig has no inheritance and relies on explicit composition and compile-time code generation. This aligns closely with Khayyam's approach and validates the feasibility of a behavior-transfer-free design in a systems programming language.

## Unresolved Questions
- **Design Pattern Catalog:** What is the complete catalog of OO design patterns that rely on behavior transfer, and what are the Khayyam equivalents for each? A dedicated document or RFC may be needed to guide developers migrating from OO languages.
- **Performance Benchmarking:** What is the actual runtime performance impact of explicit delegation compared to behavior-transfer-based dispatch? Early evidence from Zig and similar systems suggests the overhead is negligible, but formal benchmarking is needed.
- **Code Generation Standards:** What are the standards for AI or tooling-generated delegation code? Should generated code be marked with specific annotations? Should there be a standard directory or naming convention for generated files?
- **Abstraction Inclusion Depth:** How deep can abstraction inclusion chains go (abstraction A includes B includes C)? Is there a practical limit, and does it introduce any of the visibility problems that behavior transfer creates? The current position is that inclusion depth is not inherently problematic because no behavior is transferred.
- **Polymorphism in Khayyam:** Subtyping through abstraction conformance is one form of polymorphism. What other forms does Khayyam support, and how do they interact with EBO? A dedicated RFC is needed.

## Future Possibilities
- **AI-Assisted Delegation Scaffolding:** The linter and IDE tooling could automatically generate explicit delegation methods when a developer composes capsules, reducing the boilerplate of explicit delegation while preserving source-level visibility.
- **Delegation Pattern Library:** A standard library of common delegation patterns (forwarding, adapting, decorating, intercepting) that developers can use as templates for explicit delegation.
- **Ownership Visualization:** IDE tooling that visualizes the explicit delegation graph for a capsule, showing which methods are native and which delegate to embedded capsules. This would provide the "overview" benefit of hierarchies without the hidden behavior.
- **Formal Proof of Completeness:** A formal argument that explicit delegation can express every relationship that behavior transfer can express, with examples demonstrating the translation. This would address the concern that some patterns are "impossible" without behavior transfer.

## Change Rationale
This RFC was created by splitting the original monolithic "Protocol" document into three focused RFCs. The inheritance-related content was distributed between the Explicit Behavior Ownership RFC (which addresses the principled foundation) and this RFC (which addresses the language-level specification for Khayyam).

This RFC was originally titled "Rejection of Inheritance" and framed Khayyam's position as a rejection. During review, it became clear that this framing was misleading: Khayyam does not reject inheritance — it places it where it belongs. Inheritance (the extension of requirements) is supported between abstractions. What is rejected is the transfer of behavior between capsules, which is not inheritance in any meaningful sense. The RFC was retitled and restructured to reflect this positioning.

Content was incorporated from multiple sources beyond the original monolithic document:
- **Working notes:** The Go embedding clarification was extracted from the working notes and integrated as a core argument. The meta-observation about what "inheritance" debates are really about was initially integrated here but subsequently moved to the Explicit Behavior Ownership RFC during terminology and content review — it is a general conceptual argument, not a language-specific design decision.
- **Khayyam-compiler.md:** The "Composition over Inheritance (No Method Promotion)" section provided the formal compiler rules.
- **Khayyam-linter.md:** The "Explicit Delegation Verification" and "Anti-Lazy Inheritance Check" sections provided the linter enforcement rules.
- **Khayyam.md:** The abstraction definition and conformance model provided the context for how Khayyam handles the relationship between capsules and abstractions without behavior transfer.