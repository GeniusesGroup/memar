---
RFC Number: 495467
Title: "Khayyam Rejection of Inheritance"
Status: Proposed
Start Date: 2026-07-10
Applied to: ["Khayyam.md"]
Supersedes: ""
Superseded by: ""
Related:
  Depends_on: ["protocol.md", "explicit_behavior_ownership.md"]
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Core language design decisions, Composition over Inheritance rule, social inheritance analogy, rejection reasoning"
    task: []
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: ""
    contribution: "Drafted initial text for the original monolithic Protocol RFC; portions of the inheritance and method promotion analysis were incorporated from that draft"
    task: []
  - name: "Super Z"
    uri: "https://z.ai"
    model: "GLM"
    effort: "Medium"
    contribution: "Created this RFC as a focused, language-level document extracted from the original monolithic Protocol RFC. Incorporated meta-observation about inheritance disagreements, and content from Khayyam-compiler.md (Composition over Inheritance, No Method Promotion) and Khayyam-linter.md (Explicit Delegation Verification, Anti-Lazy Inheritance Check). Structured per RFC template with Drawbacks, Rationale, and Prior Art sections."
    task: ["content-split", "restructuring", "enrichment", "integration"]
---

# Khayyam Rejection of Inheritance

## Summary
Khayyam does not provide a classical inheritance mechanism. Capsules cannot acquire behavior from other capsules through inheritance, subtyping, or method promotion. Embedding a capsule inside another capsule does not expose the inner capsule's methods to the outer scope. The only sanctioned mechanism for behavior sharing is **explicit delegation**: the developer writes a method on the host capsule that visibly forwards the call to the embedded instance. This RFC formalizes this rejection at the language level and specifies how the compiler and linter enforce the rule. The principled foundation for this rejection — including the conceptual challenge to the inheritance model itself — is established in the [Explicit Behavior Ownership](./explicit_behavior_ownership.md) RFC.

## Motivation

### The Inheritance Trap
The current direction of Khayyam is not "some inheritance is good" and "some inheritance is bad." Instead, the language should **avoid importing traditional inheritance assumptions without justification**. This is a stronger position than the common "prefer composition over inheritance" advice found in textbooks, because it questions the conceptual model itself rather than merely recommending one technique over another.

Many software discussions start from the assumption that inheritance exists and then attempt to categorize it: "good inheritance" vs. "bad inheritance," "type inheritance" vs. "implementation inheritance," "interface inheritance" vs. "behavioral inheritance." This framing already assumes that inheritance is the correct conceptual model for the relationships being discussed. Khayyam should not inherit assumptions from existing language ecosystems. The model should be built from first principles.

### Practical Problems with Inheritance in Khayyam's Context
Khayyam is designed for building high-performance libraries and applications where compiler-level escape analysis, memory safety, and behavioral predictability are paramount. Inheritance introduces several practical problems in this context:

- **Hidden Behavior Paths:** Inheritance creates methods in a capsule that are not defined in that capsule's source code. The compiler must traverse the inheritance chain to determine the full method set, complicating escape analysis and other static analyses.
- **Linear Escape Analysis:** Khayyam's compiler relies on perfectly linear escape analysis for memory optimization. Inherited methods that access parent state create non-local references that break this linearity.
- **Abstraction Purity:** Khayyam's abstractions (`ab`) are designed as pure contracts — no logic, no state, no predefined method bodies. Allowing inheritance of behavior from abstractions (via default implementations) would collapse this purity.

### Meta-Observation: What Inheritance Debates Are Really About
A recurring lesson from discussions about inheritance is that many apparent disagreements about inheritance are actually disagreements about:
- **Ownership:** Who is responsible for this behavior?
- **Visibility:** Where does this behavior come from?
- **Discoverability:** How do I find the implementation?
- **Protocol relationships:** What is the actual structural relationship between these components?

rather than about inheritance itself. By addressing ownership, visibility, and discoverability directly (via the Explicit Behavior Ownership principle), many of the problems that inheritance claims to solve are resolved without importing inheritance's conceptual baggage. This RFC operates in conjunction with the EBO RFC: EBO provides the principled foundation, and this RFC provides the language-level specification.

## Guide-level Explanation

### Composition over Inheritance: The Khayyam Rule
In Khayyam, a capsule can contain other capsules as internal fields. However, **embedding a capsule does not automatically expose the inner capsule's methods to the outer capsule.** If a host capsule needs to expose a behavior of an embedded capsule, the developer must explicitly define a method on the host capsule and delegate the call.

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

Khayyam explicitly rejects this pattern. The compiler treats any attempt to call an embedded capsule's method directly on the host as an "Undefined Method" error. The linter detects when a developer appears to be attempting lazy inheritance and suggests the exact explicit delegation needed.

### Go Embedding: Not All Embedding Is the Same
An important clarification from the working notes: not all embedding serves the same purpose. In Go, embedding has two distinct effects:
1. **Protocol composition:** An embedded interface's method set is included in the outer interface's requirements. This is a *declarative* relationship — no behavior is transferred.
2. **Behavior acquisition:** An embedded struct's methods become available on the outer struct. This is a *behavioral* relationship — methods are implicitly promoted.

Khayyam distinguishes these cases clearly:
- **Abstraction composition** (combining protocol requirements) is allowed via the `{}` composition block in `ab` definitions.
- **Capsule embedding with method promotion** is rejected. A capsule's internal fields are private; their methods are not exposed.

### Interaction with Abstractions
Khayyam's abstractions (`ab`) are pure contracts. They define method signatures that implementing capsules must provide, but they contain no logic, no state, and no default implementations. This purity is maintained precisely because inheritance of behavior from abstractions is rejected.

When a capsule implements an abstraction, it does so by defining all required methods explicitly. The compiler validates structural conformance: if a capsule defines methods matching all signatures declared by an abstraction, it satisfies that abstraction. No explicit `implements` keyword is needed — conformance is implicit and structural at the compiler level.

This design means that the relationship between a capsule and an abstraction is a *conformance* relationship, not an *inheritance* relationship. The capsule does not "inherit" from the abstraction; it satisfies the abstraction's requirements through explicit implementation.

### Template Method and Other OO Patterns
Classical object-oriented design patterns that rely on inheritance — most notably Template Method, where a base class defines the skeleton of an algorithm and subclasses override specific steps — do not have a direct equivalent in Khayyam's inheritance-free model.

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
The linter blocks any patterns or workarounds that attempt to create implicit or magical method promotion hooks. If a developer writes code that appears to be attempting inheritance (e.g., embedding a capsule and then calling its methods as if they were native), the linter flags this.

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
Khayyam's compiler intelligently decides whether to handle abstractions at compile-time (monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (dynamic dispatch when underlying capsules are hidden). This decision is based on the dependency graph, not on inheritance.

Since there is no inheritance, the compiler never needs to resolve virtual dispatch tables through inheritance chains. The method resolution is always direct: either the method is defined in the capsule, or the capsule explicitly delegates to another capsule. This simplification enables more aggressive compiler optimizations, including:
- **Perfectly linear escape analysis:** No inherited methods create non-local references.
- **Devirtualization:** Without inheritance-based polymorphism, more calls can be resolved statically.
- **Inlining:** Explicit delegation calls are straightforward candidates for inlining.

## Drawbacks
- **No Template Method Pattern:** The classical Template Method pattern relies on inheritance and does not have a direct syntactic equivalent. The alternative (abstraction + explicit delegation) is more verbose but functionally equivalent. Developers must learn the alternative pattern.
- **More Explicit Code:** Every behavior must be written explicitly. For large component hierarchies where many components share similar behavior, this results in more source code. AI-assisted code generation and linter-based scaffolding mitigate this, but the source code is undeniably longer.
- **Design Pattern Migration:** Teams migrating from OO languages (Java, C#, C++) must reformulate inheritance-based designs. This is not just a syntax change — it requires rethinking the architectural relationships between components.
- **No "Base Class" Convenience:** Common patterns like a `BaseService` class that provides shared infrastructure (logging, configuration, error handling) to all service subclasses do not translate directly. Each service must explicitly compose its infrastructure.

## Rationale and Alternatives

### Why Not Allow "Safe" Inheritance?
An alternative is to allow single inheritance with restrictions — for example, "single inheritance is allowed but only from abstract base classes" or "inheritance is allowed but the base class cannot have concrete methods." This was rejected because:
1. It still introduces hidden behavior paths (the developer must check the parent class to know the full method set).
2. It creates a conceptual dependency on the inheritance model that influences how developers think about component relationships.
3. The "safe" boundaries are subjective and tend to erode over time as exceptions are added.

### Why Not Use Go-Style Embedding?
Go's embedding is often cited as a "middle ground" between inheritance and composition. It provides method promotion without the full complexity of class inheritance. This was rejected because method promotion is still implicit behavior acquisition — the embedding component's source code does not show the promoted methods. The visibility problem remains, just in a milder form.

### Why Not Use Rust-Style Traits with Defaults?
Rust traits allow default method implementations, which provide behavior sharing without traditional inheritance. This was rejected because default implementations introduce the same ownership ambiguity that EBO prohibits: a method exists in a type but the type's source code does not define it. The default method's implementation lives in the trait, creating dual ownership.

### Impact of Not Doing This
If Khayyam allowed inheritance, every subsequent design decision would need to account for inheritance chains, method resolution order, and hidden behavior paths. The compiler would need to support virtual dispatch tables, the linter would need to trace inheritance hierarchies, and developers would need to mentally simulate inheritance to understand a capsule's full behavior. By rejecting inheritance at the foundation, all of this complexity is eliminated.

## Prior Art

- **Go Struct Embedding:** Go allows embedding structs and interfaces within other structs. Embedded struct methods are promoted to the outer struct. This is the most well-known "composition with promotion" mechanism. Khayyam rejects the promotion aspect while keeping the composition aspect (capsules can contain other capsules as fields).
- **Rust Traits:** Rust traits can have default method implementations and blanket implementations. Both introduce behavior without the implementing type's source code defining it. Khayyam rejects both, keeping traits (abstractions) as pure declarations.
- **Java Class Inheritance:** Java supports single class inheritance with concrete method bodies and multi-interface implementation. Java 8+ added default interface methods. Khayyam rejects all forms of inheritance and default methods.
- **C++ Multiple Inheritance:** C++ allows multiple inheritance with concrete method bodies, including the diamond problem. Khayyam's rejection of all inheritance eliminates this class of problems entirely.
- **Swift Protocols with Extensions:** Swift protocols can be extended with default implementations via protocol extensions. This allows behavior injection that is invisible at the conforming type's definition site. Khayyam rejects this pattern.
- **Kotlin Open Classes:** Kotlin marks classes as `open` to allow inheritance, with `final` as the default. This is a more conservative approach than Java's, but still allows inheritance when opted in. Khayyam takes the stronger position of not providing inheritance at all.
- **Zig Comptime and Delegation:** Zig has no inheritance and relies on explicit composition and compile-time code generation. This aligns closely with Khayyam's approach and validates the feasibility of an inheritance-free design in a systems programming language.

## Unresolved Questions
- **Design Pattern Catalog:** What is the complete catalog of OO design patterns that rely on inheritance, and what are the Khayyam equivalents for each? A dedicated document or RFC may be needed to guide developers migrating from OO languages.
- **Performance Benchmarking:** What is the actual runtime performance impact of explicit delegation compared to inheritance-based dispatch? Early evidence from Zig and similar systems suggests the overhead is negligible, but formal benchmarking is needed.
- **Code Generation Standards:** What are the standards for AI or tooling-generated delegation code? Should generated code be marked with specific annotations? Should there be a standard directory or naming convention for generated files?
- **Abstraction Composition Depth:** How deep can abstraction composition chains go (abstraction A includes B includes C)? Is there a practical limit, and does it introduce any of the visibility problems that inheritance creates? The current position is that composition depth is not inherently problematic because no behavior is transferred.

## Future Possibilities
- **AI-Assisted Delegation Scaffolding:** The linter and IDE tooling could automatically generate explicit delegation methods when a developer composes capsules, reducing the boilerplate of explicit delegation while preserving source-level visibility.
- **Delegation Pattern Library:** A standard library of common delegation patterns (forwarding, adapting, decorating, intercepting) that developers can use as templates for explicit delegation.
- **Ownership Visualization:** IDE tooling that visualizes the explicit delegation graph for a capsule, showing which methods are native and which delegate to embedded capsules. This would provide the "overview" benefit of inheritance hierarchies without the hidden behavior.
- **Formal Proof of Completeness:** A formal argument that explicit delegation can express every relationship that inheritance can express, with examples demonstrating the translation. This would address the concern that some patterns are "impossible" without inheritance.

## Change Rationale
This RFC was created by splitting the original monolithic "Protocol" document into three focused RFCs. The inheritance-related content was distributed between the Explicit Behavior Ownership RFC (which addresses the principled foundation) and this RFC (which addresses the language-level specification for Khayyam).

Content was incorporated from multiple sources beyond the original monolithic document:
- **Working notes:** The meta-observation about what inheritance debates are really about, and the Go embedding clarification were extracted from the working notes and integrated as core arguments. The Social Inheritance Analogy was initially integrated here but subsequently moved to the Explicit Behavior Ownership RFC during boundary review — it is a general conceptual argument, not a language-specific design decision.
- **Khayyam-compiler.md:** The "Composition over Inheritance (No Method Promotion)" section provided the formal compiler rules.
- **Khayyam-linter.md:** The "Explicit Delegation Verification" and "Anti-Lazy Inheritance Check" sections provided the linter enforcement rules.
- **Khayyam.md:** The abstraction definition and conformance model provided the context for how Khayyam handles the relationship between capsules and abstractions without inheritance.

## Related RFCs

| **RFC** | **Relationship** |
|---------|-----------------|
| protocol.md | **Depends on.** Defines Protocol as a pure declarative specification. This RFC uses that definition to justify why abstractions carry no behavior. |
| explicit_behavior_ownership.md | **Depends on.** Provides the principled foundation (single visible owner) that this RFC applies at the language level. |
| khayyam-rejection_of_default_implementations.md | **Superseded by** explicit_behavior_ownership.md and this RFC. Default implementations are a form of implicit behavior inheritance. |
| khayyam-rejection_of_macros.md | **Superseded by** explicit_behavior_ownership.md. Macros that hide behavior are a separate concern from inheritance. |
| khayyam-rejection_of_method_promotion.md | **Superseded by** this RFC. Method promotion is a specific mechanism of implicit behavior inheritance, and its rejection is a consequence of the broader inheritance rejection. |
| khayyam-error_abstraction.md | **References.** Error handling in Khayyam uses abstractions and explicit ownership, consistent with this RFC's rules. |