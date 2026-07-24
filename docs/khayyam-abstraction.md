---
Title: "Abstraction in Khayyam"
Status: Proposed
Start Date: 2026-07-11
RFC Number: 495493
Applied to: ["Khayyam.md#Abstraction"]
Related RFCs:
    - Title: "Library-Driven Control Flow"
      URI: "./khayyam-library_driven_control_flow.md"
      Reason: "Depends_on"
      Explanation: "This RFC builds on the precedent set by RFC of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Contribution: "Defined the core abstraction model and authored the pure-contract philosophy."
    Tasks: []
    URI: "https://gemini.google.com/"
    Model: "3.1 pro"
    Effort: "Extended thinking enabled"
    Contribution: "Drafted initial some text in this RFC"
    Tasks: []
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Contribution: "Identified the structural-vs-nominal tension, drafted the intentional-satisfaction problem statement, argued for and against alternatives, consolidated multiple RFCs into this unified document."
    Tasks: []
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM"
    Effort: "Medium"
    Contribution: "Merged RFC content into this RFC"
    Tasks: []
---

# Abstraction in Khayyam
Abstractions in Khayyam occupy a conceptual space closely related to [IDL (Interface Description Language)](https://en.wikipedia.org/wiki/Interface_description_language) as used in protocol packages: both describe behavioral contracts that specify *what* is required without prescribing implementation details. Just as an IDL defines the data and operations exchanged between parties in a protocol, a Khayyam abstraction defines the method signatures a capsule must expose — serving as the language-level counterpart to a protocol specification.

This RFC consolidates all design decisions, resolved policies, and open questions related to the `ab` (abstraction) type in Khayyam into a single authoritative document. It supersedes two prior drafts — RFC 495390 ("Intentional Abstraction Satisfaction") and RFC 000017 ("Rejection of Default Implementations") — and merges them with the existing DX Scaffolding content into one cohesive specification.

## Summary
Khayyam's abstraction (`ab`) is a **pure contract mechanism** with three resolved design properties and one open question:

1. **No executable logic.** An abstraction contains no method bodies — it describes *what* is required, never supplies *how*. Default implementations (as in Rust traits or Java `default` interface methods) are explicitly rejected.
2. **No generic syntax.** Abstractions carry no type parameters. Polymorphism classification and the rejection of generic syntax are documented in RFC 495494 (Polymorphism).
3. **Implicit structural satisfaction.** A capsule satisfies an abstraction if it implements all required methods with matching signatures. No explicit `impl` or `implements` keyword exists.
4. **Open question — intentional satisfaction.** Whether purely structural satisfaction carries an accidental-satisfaction risk (as it does in Go), and if so, whether a mitigation mechanism is needed without compromising Khayyam's minimalism.

## Motivation

### The Problem This RFC Solves
Abstractions are the primary mechanism for polymorphism and decoupled architecture in most modern systems languages. However, every major language makes different — and often conflicting — tradeoffs in how abstractions are defined, satisfied, and compiled. These tradeoffs have real, measurable consequences for developer experience, compilation strategy, and long-term code maintainability.

Khayyam needs a single, coherent abstraction model that is consistent with its core philosophy of *Grammar Atomicity*, *Zero-Magic Core*, and *Strict Separation of Concerns*. Specifically, the abstraction system must:

- **Preserve syntactic minimalism.** Introducing generic syntax, explicit implementation keywords, or inheritance-like mechanisms adds grammar surface area that conflicts with the language's design goals.
- **Enable zero-cost abstraction where possible.** When the compiler knows the concrete type behind an abstraction, it should be able to inline the call — eliminating VTable overhead entirely — without the developer writing different code.
- **Maintain the pure-contract invariant.** An abstraction must never silently provide behavior, as this reintroduces the implicit routing and inheritance problems that Khayyam was designed to avoid.
- **Support organizational scalability.** In large codebases, developers need tooling assistance (scaffolding, validation, proactive warnings) to work with abstractions without the language itself growing heavier.

### Concrete Pain Points Addressed
- **Go's accidental satisfaction problem.** In Go's structural typing system, any type with matching method signatures accidentally satisfies an interface. For marker-like abstractions (e.g., a small `Error` interface), an unrelated capsule can qualify without its author ever intending this. This RFC records this risk as an open question specific to Khayyam.
- **Rust's `impl` ceremony.** Rust requires explicit `impl Trait for Type` declarations at every implementation site. While this eliminates accidental satisfaction, it adds boilerplate that scales linearly with the number of abstraction-capsule pairs — in tension with Khayyam's minimalism goals for the common case.
- **Java/C# generic syntax complexity.** Explicit type parameters (`<T>`) force developers to expose implementation details that violate the principle of information hiding. Khayyam avoids this by carrying no type parameters on abstractions — see RFC 495494 for the full polymorphism classification and rationale.
- **Default method inheritance confusion.** Rust's default trait methods and Java's `default` interface methods silently provide behavior from an abstraction, blurring the line between contract and implementation and making the execution path harder to reason about at compile time.

## Guide-level explanation

### What Is an Abstraction in Khayyam?
Think of an abstraction as a **behavioral specification** — a promise that a capsule will respond to certain method calls. The abstraction itself is inert: it has no state, no logic, and no runtime presence. It exists purely as a compile-time contract.

When you write `tp Reader ab`, you are telling the compiler: "There exists a concept called `Reader`. I will define the methods it requires separately. Any capsule that provides those methods can be used wherever a `Reader` is expected."

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
r = myFileReader  // validated at compile time
```

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
tp CheckPresence mt (self PresenceHelper) (result Bool) (err Error) { /* ... */ }

// Each implementer explicitly delegates
tp Cache mt (self RedisStore) (result Bool) (err Error) {
    // explicit one-line delegation — no implicit inheritance
    result, err = self.helper.CheckPresence()
}
```

This is deliberate, visible boilerplate. It keeps the execution path 100% explicit and linear, free of compiler magic or implicit routing.

## Reference-level explanation

### Dispatch Strategy

The compiler's mechanism for resolving polymorphic calls (monomorphization vs. dynamic dispatch) is documented in RFC 495494 (Polymorphism).

### Abstraction Realization (Implicit Satisfaction)

Khayyam does not introduce any explicit syntax or keyword (such as `impl` or `implements`) to bind a capsule to an abstraction (`ab`). Abstraction realization is strictly implicit and structural at the compiler level.

- **Rule**: A capsule satisfies an `ab` if and only if it implements all methods declared by that abstraction with identical signatures (receiver type, parameter types, and return types all match).
- **Validation point**: The compiler validates abstraction satisfaction during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods will result in a strict compile-time error.

This design mirrors Go's interface satisfaction model at the language level. It eliminates the boilerplate of explicit implementation declarations (Rust's `impl Trait for Type`) and keeps the language grammar minimal. However, it also inherits Go's known risk of **accidental satisfaction** — see Unresolved Questions.

### Rejection of Default Implementations

Khayyam explicitly **rejects** default method implementations (also known as "default trait methods" in Rust or "default interface methods" in Java 8+). An abstraction (`ab`) is a pure contract with no executable logic of its own.

**Rationale:** Allowing executable logic inside an abstraction violates its contractual purity in two ways:

1. **It breaks the "what, not how" invariant.** An abstraction should describe *what* behavior is required, never silently supply *how* that behavior is implemented. When an abstraction contains a method body, it becomes a partial implementation — a hybrid that is neither a clean contract nor a clean type, making the execution path harder to reason about.

2. **It introduces implicit, dynamic routing behavior.** Default methods create a form of implicit inheritance: the method body lives in the abstraction, but executes in the context of the concrete capsule. This reintroduces the same class-hierarchy confusion that composition-over-inheritance patterns were designed to avoid, and it clouds compile-time optimization because the compiler can no longer assume the call target is a simple VTable entry or a monomorphized concrete method.

**The alternative — explicit delegation:** Shared behavior across multiple capsules lives in an ordinary capsule, and each implementer explicitly delegates to it. This is one line of boilerplate per implementation site, but it keeps the execution model completely transparent:

```khayyam
// Shared behavior capsule
tp DefaultValidator cp { /* ... */ }
tp Validate mt (self DefaultValidator) (result Bool) (err Error) { /* ... */ }

// Each implementer writes an explicit delegation line
tp Validate mt (self UserRecord) (result Bool) (err Error) {
    result, err = self.validator.Validate()
}
```

**Tooling support for boilerplate reduction:** The elimination of repetitive delegation boilerplate is offloaded to organizational Linter and Scaffolding tooling. A Linter rule can:
- Detect when a capsule partially implements an abstraction's method set
- Auto-generate the missing delegation lines (scaffolding)
- Verify that the delegation call targets the correct shared capsule
- Warn if a developer appears to be hand-duplicating shared logic instead of delegating

This ensures the final source code remains 100% explicit, linear, and free of compiler magic, while the development workflow remains ergonomic.

### Abstraction Validation and DX Scaffolding

Because the language syntax avoids explicit implementation keywords, the burden of developer assistance shifts entirely to the Linter and associated tooling. This is consistent with Khayyam's philosophy of keeping the language grammar minimal and delegating governance to organizational tooling (the Memar framework).

- **Scaffolding**: When a developer intends to implement an abstraction (detected via context or explicit linter hints), the Linter provides automated code generation to scaffold all missing method signatures with empty bodies.
- **Proactive Warnings**: The Linter analyzes the codebase and issues warnings if a capsule partially implements an abstraction's method set in a context where it is clearly expected to satisfy that abstraction, preventing unexpected compilation failures.

## Drawbacks

Every design decision carries a cost. The following are the known drawbacks of Khayyam's abstraction model:

### 1. Accidental Satisfaction Risk (Structural Typing)

By adopting implicit structural satisfaction, Khayyam inherits Go's known weakness: an unrelated capsule can accidentally satisfy a small, marker-like abstraction if its method signatures happen to match. For example, if a `FileLogger` capsule happens to define a `String()` method with the correct signature, it could accidentally qualify as a `Stringer` abstraction without its author ever intending this relationship.

This risk is most acute for small abstractions with one or two methods, where signature collision is statistically more likely. For large abstractions with many methods, accidental satisfaction is practically impossible. See Unresolved Questions for the status of this risk.

### 2. Explicit Delegation Boilerplate

The rejection of default implementations means that every capsule sharing common behavior must carry its own explicit delegation line. This is deliberate, visible boilerplate repeated across every implementer. While Linter tooling can auto-generate these lines, the resulting source code is still longer than it would be with default methods.

The counter-argument is that this boilerplate is *honest* — it makes the execution path visible and auditable in a way that default methods do not.

### 3. Discoverability of "What Implements This Abstraction"

Without explicit `impl` declarations, discovering which capsules satisfy a given abstraction requires a tool-assisted graph traversal rather than a simple text search for `impl AbstractionName`. The Linter and IDE tooling must provide this capability. This is a tooling burden, not a language burden, but it is a real cost in ecosystem maturity — a new Khayyam project will have less mature tooling than a new Rust project where `impl` blocks are trivially searchable.

### 4. No Backward-Compatible Path to Explicit Satisfaction

If the open question on intentional satisfaction is later resolved in favor of requiring some form of explicit declaration (option (b) or (c) in Unresolved Questions), this would be a backward-incompatible change to the current model. Every existing capsule-abstraction relationship would need to be audited and potentially annotated. The earlier this question is resolved, the lower the migration cost.

## Rationale and alternatives

### Why This Design Over Alternatives

**Against explicit generic syntax (`<T>`, `[T]`):** Abstractions carry no type parameters. The full classification of Khayyam's polymorphism model and the rationale for rejecting generic syntax are documented in RFC 495494.

**Against Rust's `impl` ceremony:** While Rust's explicit `impl Trait for Type` eliminates accidental satisfaction, it adds boilerplate at every implementation site. In a large codebase with many abstraction-capsule pairs, this scales poorly and is in tension with Khayyam's minimalism goals for the common case. The current structural model is simpler and more ergonomic; the accidental-satisfaction risk is recorded as an open question for targeted mitigation, not as a reason to adopt full nominal typing.

**Against default implementations (Rust traits, Java interfaces):** Default method bodies in abstractions violate the "abstraction as pure contract" principle. They create implicit inheritance-like behavior that conflicts with Khayyam's explicitness goals. The alternative — explicit delegation to shared capsules — is more verbose but completely transparent: the execution path is always visible, and the compiler's optimization decisions are never obscured by hidden routing logic.

**Against doing nothing (no abstraction mechanism):** Without abstractions, polymorphism would require either raw function pointers (erasing type safety) or code duplication. Neither is acceptable for a language that aims to support high-performance library development.

### The Pure Contract Philosophy

Khayyam treats abstraction as a pure contractual agreement. An abstraction represents behavior: if it requires an `Element`, it simply accepts `Element`. Any capsule that satisfies this interface is valid. The abstraction does not care about the concrete capsule's internal structure — it only cares about the behavioral contract. This "Contract-First Approach" means abstractions are implementation-agnostic by construction.

### The Three Directions on Intentional Satisfaction

Three potential resolutions exist for the open question of intentional vs. accidental satisfaction. None is chosen yet:

**(a) Keep the current structural model as documented.** Simplest, matches `Khayyam.md` as written today, but leaves the accidental-satisfaction risk open at the language level for any marker-like abstraction — not just Error, but any small abstraction the standard library or an organization defines going forward.

**(b) Require explicit, nominal declaration for every abstraction implementation.** Along the lines of Rust's `impl Trait for Type`. Eliminates the risk entirely, but adds ceremony to every implementation site and is a significant, backward-incompatible change to a philosophy Khayyam currently states as a feature ("Contract-First Approach").

**(c) A hybrid model.** Structural satisfaction remains the default, but specific abstractions — those identified as small, marker-like, or identity-bearing — can opt into requiring an explicit declaration. This would need a formal criterion for which abstractions qualify, and a library-driven (not new-keyword) mechanism for declaring it, consistent with "Library-Driven Control Flow" RFC's precedent of keeping such behaviors as ordinary method calls rather than new syntax.

## Prior art

### Go — Interfaces (Structural Typing, No Defaults)

Go's interfaces are the closest existing model to Khayyam's abstraction design. Go uses fully structural typing: a type satisfies an interface if it has all the required methods, with no `implements` declaration. Go interfaces carry no default implementations. This simplicity is widely praised, but it comes with the accidental-satisfaction problem documented extensively in the Go community. The Go community's pragmatic response has been to accept this risk for large interfaces (where it is negligible) and use unexported marker methods for small, identity-carrying interfaces — a workaround at the library level, not a language-level solution.

### Rust — Traits (Nominal Typing, Default Methods)

Rust's traits use fully nominal typing with explicit `impl Trait for Type` declarations. This eliminates accidental satisfaction entirely. Rust also supports default method bodies in traits, which provide shared behavior without requiring implementers to write delegation code. The cost is mandatory ceremony at every implementation site and the implicit routing behavior of default methods (a trait's default method body executes in the context of the concrete type, creating a form of multiple dispatch that can be surprising). Khayyam explicitly rejects default method bodies.

### Java — Interfaces (Nominal Typing, Default Methods, Generics)

Java's interfaces use nominal typing with `implements` declarations. Since Java 8, interfaces support `default` methods with executable bodies. Java also has full generic syntax (`<T>`), whose rejection is documented in RFC 495494 (Polymorphism). This combination provides maximum flexibility but at the cost of significant syntax complexity and the same implicit routing concerns as Rust's default methods. Khayyam explicitly rejects the default method mechanism.

### TypeScript — Structural Typing (Compile-Time Only)

TypeScript's type system uses structural typing for interface satisfaction, closely mirroring Go's model. TypeScript interfaces can describe object shapes, and any object with matching properties satisfies the interface. TypeScript has no default method implementations (its interfaces are purely type-level, erased at runtime). The accidental-satisfaction risk exists but is less practically concerning because TypeScript interfaces are not used as runtime dispatch mechanisms. Khayyam's abstractions, by contrast, have runtime implications (VTable generation), making accidental satisfaction a potentially more serious issue.

### Zig — No Built-in Interfaces (Comptime-Based Alternatives)
Zig takes the most radical minimalist approach: it has no interface or trait mechanism at all. Generic behavior is achieved through `comptime` (compile-time code execution) and duck typing at the generic function level. This provides maximum simplicity but shifts the entire burden of polymorphism to the developer. Khayyam's design occupies a middle ground: it provides a first-class abstraction type for cleaner API contracts while keeping the language grammar minimal.

### Haskell — Typeclasses (Nominal, No Defaults in the Language Core)

Haskell's typeclasses use nominal typing with explicit `instance` declarations. Typeclasses in their pure form carry no default implementations (though GHC extensions add them). Haskell's approach is closest to a "pure contract" model, and it demonstrates that nominal typing and zero-cost abstraction can coexist. However, Haskell's typeclass resolution happens at compile time through a separate mechanism (instance resolution), which is a form of implicit behavior that Khayyam's explicit delegation model avoids.

## Unresolved questions

This RFC consolidates the open questions from both superseded RFCs. The central unresolved issue is:

### 1. Is Khayyam's Structural Satisfaction Model Sufficient, or Does It Need an Intentional-Satisfaction Mechanism?

This is the primary open question, carried forward from RFC 495390. It has several sub-questions:

**(a) Current model assessment.** Is the "Contract-First Approach" wording in `Khayyam.md` — "Any capsule that satisfies this interface is valid" — an accurate, complete, and intended description of Khayyam's abstraction model? If so, Khayyam is structurally typed at the language level with the same accidental-satisfaction risk as Go. If not, what additional mechanism exists that is not yet reflected in the documentation?

**(b) If structural typing is confirmed, should Khayyam move toward option (b) or (c)?** Does doing so conflict with or require revisiting the "Smart Compilation" (monomorphization vs. dynamic dispatch) strategy, which currently assumes purely structural matching to drive the compiler's dispatch decisions? An explicit declaration might give the compiler additional, useful information for that choice — or it might be entirely orthogonal.

**(c) If a hybrid model (c) is chosen, what is the formal criterion?** "Marker-like" is a working intuition, not a formal definition. A criterion might be based on: method count (abstractions with N or fewer methods), the presence of a "marker method" (a method with no parameters and a unit return, whose only purpose is identity), or a library-level annotation. Each has tradeoffs.

**(d) If any explicit declaration mechanism is introduced, what does it look like syntactically?** Can it be expressed as an ordinary library-driven method call (per the precedent of avoiding new keywords), or does it require an actual grammar change?

**(e) Does any answer here affect the "Smart Compilation" decision between monomorphization and dynamic dispatch?** I.e. does an explicit declaration give the compiler additional, useful information for that choice, or is it orthogonal?

This RFC should not advance past Draft status for the intentional-satisfaction question until question (a) is resolved.

### 2. Linter Delegation Verification — Exact Mechanism Unspecified

The exact mechanism by which a Linter recognizes a valid delegation call versus a hand-written duplicate implementation is not yet specified. The Linter needs to determine:
- Whether a capsule's method body is a pure delegation to a shared helper (acceptable) vs. a re-implementation of the shared logic (a code-duplication warning).
- Whether the shared helper capsule itself is the canonical source for that behavior (as defined by organizational convention or a configuration file).

This is a tooling-level specification, not a language-level one, but it affects the practical viability of the explicit-delegation model.

### 3. Cross-Language Compiler Implications

When a Khayyam compiler translates an abstraction to a target language (e.g., Go, Rust, C), the structural-satisfaction model must be correctly mapped to the target's type system. In Go's case, this is natural (Go is also structural). In Rust's case, the compiler must generate `impl` blocks for every capsule-abstraction pair it discovers through graph analysis. If an intentional-satisfaction mechanism is later introduced, it would directly simplify this cross-language translation by providing unambiguous, queryable metadata about which abstractions each capsule is intended to implement.

### 4. Abstraction Design and Over-Abstraction Risk
Khayyam's abstractions are intended as "architectural contracts that express meaningful behavioral boundaries." But the language currently provides no formal guideline for where one abstraction should end and another should begin. Should a `Sortable` abstraction also imply `Equatable`? Should a `Serializable` abstraction imply `Cloneable`? In Khayyam, where inclusion is the mechanism, the question becomes: what is the minimum coherent behavioral boundary?

This is not just a style question. It affects API surface area, compilation strategy (more conforming capsules means less monomorphization), and onboarding friction.

A possible heuristic: an abstraction should represent a **domain concept**, not a **technical capability**. `UserRepository` is a valid abstraction. `Filterable` is probably not.

The largest non-technical risk may be abstraction inflation. If developers misunderstand the role of abstractions, they may begin creating `Readable`, `Writable`, `Searchable`, `Filterable`, `Sortable`, `Composable`, and so on, as generic reuse mechanisms. This recreates the same problems seen in interface-heavy ecosystems. The intended role of abstractions is: architectural contracts that express meaningful behavioral boundaries — not general-purpose code reuse tools. The success of Khayyam may depend heavily on preserving this distinction.

##### Drawbacks
Without formal guidelines, different teams (or different developers within the same team) will make inconsistent abstraction-granularity decisions. Over time, this inconsistency can erode the API coherence that the abstraction model is designed to provide.

##### Rationale and alternatives
- **Define a maximum set of methods per abstraction (rejected)**: arbitrary numeric limits do not capture the semantic coherence that matters.
- **Require a domain-concept naming heuristic as a compiler rule (considered, not chosen)**: too subjective for mechanical enforcement; better suited as a linter guideline.
- **Adopt traditional generic syntax with constraint clauses (rejected)**: would reintroduce the type-carrier indirection that Khayyam's design philosophy explicitly removes.
- **Use structural typing as in Go (considered, not chosen)**: Go's structural typing achieves similar expressiveness but without the Smart Compilation optimization path that Khayyam's abstraction model enables.

##### Prior art
Rust's trait system is the closest mainstream prior art for behavioral contracts, but Rust uses `impl Trait for Type` syntax and allows generic bounds. Go's structural interfaces are simpler but lack monomorphization optimization. Haskell's type classes are more powerful but introduce a level of abstraction complexity that Khayyam deliberately avoids.

##### Unresolved questions
1. Is the domain-concept vs. technical-capability heuristic sufficient, or does it need to be supplemented with more specific criteria?
2. Should the Memar framework define a curated set of canonical abstractions that serve as reference examples for appropriate granularity?
3. Are there realistic algorithms that genuinely require type identity rather than behavioral contracts, and if so, how should Khayyam handle them?

### 5. Abstraction Stability and Versioning

When an abstraction's behavioral contract changes — a new method is added, a return type changes, a precondition is tightened — what happens to every capsule that conforms to it?

In Rust, adding a method to a trait is a breaking change. In Go, adding a method to an interface is not (structural typing). In Java, default methods were introduced specifically to solve this problem. Khayyam's inclusion-based model needs its own answer. Since Smart Compilation may monomorphize based on the current set of conforming capsules, an abstraction change could trigger recompilation across the entire dependency graph.

This is not just a compiler problem. It is an ecosystem governance problem. If core abstractions in the Memar framework evolve frequently, the cost of upgrading becomes a function of the abstraction stability model, not the code change itself.

##### Drawbacks
There are no direct drawbacks to documenting this question now. The cost of not documenting it is that an abstraction evolution decision made ad hoc later could create ecosystem-wide breakage with no prior analysis.

##### Rationale and alternatives
- **Adopt Rust's trait-evolution rules (rejected)**: Rust's nominal typing makes adding a method a breaking change, which is overly conservative for Khayyam's inclusion-based model.
- **Adopt Go's structural typing approach (considered, not chosen)**: Go's approach is too permissive for Khayyam's goal of explicit behavioral contracts, since any capsule that happens to have the right methods would accidentally conform.

##### Prior art
Rust's trait-evolution rules, Go's interface-addition semantics, and Java's default methods are the primary prior art. Semantic versioning (SemVer) provides a general versioning framework, but does not address the specific challenge of versioning *behavioral contracts* where satisfaction is structural rather than declared.

##### Unresolved questions
1. What is the minimal safe evolution operation on an abstraction? Can a new method be added non-breakingly if it has a default implementation expressed as a standalone method?
2. Should Khayyam define a formal versioning scheme for abstractions, similar to semantic versioning but adapted for behavioral contracts?

## Future possibilities

### Compiler-Generated Dispatch Metadata

Once the intentional-satisfaction question is resolved (in any direction), the compiler could emit metadata files (e.g., a JSON manifest) listing every capsule and the abstractions it satisfies. This would be valuable for:
- IDE tooling (jump-to-implementation, find-all-satisfiers)
- Cross-language compiler backends (generating `impl` blocks for Rust, `implements` for Java)
- Documentation generation (automated "implemented by" pages for each abstraction)

### Abstraction-Level Documentation Annotations

A future RFC could define a convention (not a language feature) for attaching documentation, examples, or invariants to an abstraction — similar to Rust's doc comments on traits or Go's interface documentation conventions. This would be an organizational tooling concern, not a grammar change.

### Composable Abstraction Constraints

A future extension could allow organizations to define "abstraction constraints" — predicates that an abstraction's satisfiers must meet (e.g., "any capsule satisfying `Serializable` must also satisfy `Clone`"). This would be enforced at the Linter level and expressed as configuration, not as language syntax.

### Curated Canonical Abstractions

A curated reference set of canonical abstractions in the Memar framework, serving as examples of appropriate granularity and domain-concept framing. This would provide new developers with concrete templates for what a well-designed abstraction looks like, reducing the risk of over-abstraction.

### Abstraction-Granularity Linter Rules

A linter rule that detects abstraction names that are likely technical capabilities rather than domain concepts (e.g., names ending in `-able`, `-ible`) and suggests reconsideration. A complementary rule could detect under-abstraction (abstractions with too many methods that should be split into smaller, more focused behavioral boundaries).