---
RFC Number: 495421
Title: "Static Concepts Must Be Types"
Status: Proposed
Start Date: 2026-07-08
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001", "495369"]
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Original design decision, years of production validation in memar-go, core principle formulation, Classification Problem identification, Immutable Infrastructure compatibility insight"
    task: []
  - name: "Super Z"
    uri: ""
    model: "GLM"
    effort: ""
    contribution: "Drafted RFC through six revisions, documented trade-offs"
    task: []
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: "RFC review and architectural refinement"
    contribution: "Web research, reframed rationale around Concept vs Data, generalized rule beyond Error capsules, clarified MUST/SHOULD criteria"
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: ""
    task: []
---

## Summary

Identity belongs to the type system. In the Memar framework, the answer to "which concept is this?" MUST be determinable from the type alone, at compile time, without inspecting any runtime data. A static capsule — one with no per-instance dynamic data — MUST therefore be its own distinct type. A capsule whose instances share the same schema and differ only in values may use a shared type. A capsule whose instances have different data schemas SHOULD use distinct types.

The inability to create concepts at runtime — which might be listed as a drawback from outside the framework — is in fact compatible with Memar's Immutable Infrastructure principle (RFC 495369): no capability may be added to a running Memar application without recompilation. This is not a limitation imposed by the type system; it is a deliberate governance choice that the type-system constraint is compatible with.

This RFC establishes the universal principle. A companion document, `Static_Concepts_Must_Be_Types-vs-go_philosophy.md` in the memar-go repository, documents how this principle interacts with Go's value-oriented error model — the specific challenges, trade-offs, and community critiques that arise when implementing this principle in Go.

## Motivation

### The Core Question

Consider two approaches to representing a distinct concept such as "transaction unavailable":

1. **The concept is the type.** `ErrTransactionUnavailable` is its own type. The type *is* the concept. No data is needed to distinguish it from `ErrInsufficientFunds` — the type system does that.

2. **The concept is data.** A single `GenericError` type holds a `name` field set to `"ErrTransactionUnavailable"`. The concept "transaction unavailable" is represented by a string stored in memory at runtime, not by the type itself.

Both approaches produce a working program. The difference is not in correctness but in **what role the type system plays**. The first approach assigns the type system its strongest possible responsibility: answering "what is this?" The second approach reduces the type system to a container and delegates identity to data — the same kind of data that holds quantities, timestamps, and configuration values.

This RFC establishes that the first approach is not merely preferred but mandatory for static capsules, because in the Memar framework's architectural model, identity is the type system's job, and data is for variation between instances of the same concept — not for distinguishing one concept from another.

### Why This Is Not Obvious

Most programming languages and frameworks do not make this distinction explicitly. Some use string values inside shared types, some use exception classes (closer to the principle but mixed with string-based patterns), some use enum variants within a shared type (identity as a runtime tag, not as the type itself). The industry has no consensus on whether identity belongs to the type system or to data, and the absence of a deliberate decision is what produces the inconsistency this RFC resolves.

RFC 000001 establishes that the framework is the architectural authority over the language. This means the framework gets to decide what the type system is responsible for — and this RFC decides that identity is one of those responsibilities.

## Guide-level explanation

### Identity, Data, and Behavior Are Separate Responsibilities

Every value in a Memar system serves one of three roles:

- **Identity**: answering "which concept is this?" — `ErrTransactionUnavailable`, `CapabilityRead`, `StatusActive`.
- **Behavior**: answering "what can this do?" — methods like `Save()`, `Validate()`, `Format()`.
- **Data**: answering "what values does this instance carry?" — fields like `amount`, `timestamp`, `name`.

These three responsibilities have distinct, non-overlapping homes in the architecture:

| Responsibility | Home | Verifiable at |
|---------------|------|--------------|
| Identity | The type system (the type itself) | Compile time |
| Behavior | Methods on the type | Compile time (signature), runtime (execution) |
| Data | Instance state (fields) | Runtime |

Identity is neither behavior nor data. Behavior belongs to methods. Data belongs to instance state. Identity belongs to the type system. Confusing these three responsibilities forces one mechanism to simulate another and weakens architectural clarity: data-simulated identity cannot be checked at compile time, type-simulated data cannot vary between instances, and behavior-simulated identity cannot be expressed in method signatures.

This RFC addresses the most consequential form of this conflation: **using data to simulate identity**. Specifically, it prohibits representing a static concept — a concept with no per-instance data — as a value inside a generic type, because that would mean identity, which belongs to the type system, is stored as runtime data instead.

### The Principle in Plain Terms

When a capsule is a **static concept** — meaning it has no per-instance data, all its method return values are determined at type-definition time, and two variables of the same type are always indistinguishable — then the concept IS the type. There is nothing to put in a field, nothing to pass to `Init`, and nothing to compare at runtime. The type itself carries the entire identity.

Representing a static concept as data inside a generic type means the type system is no longer answering "what is this?" — a string comparison at runtime is. This is a demotion: identity, which the type system can verify at compile time, has been moved to data, which can only be checked at runtime.

### The Three Rules

**Rule 1 — Static Concept → Distinct Type (MUST)**

*Derived from the identity principle.*

If a capsule has no per-instance dynamic data, it MUST be its own dedicated type. No generic type with `Init`, no tag field, no string comparison. The type is the concept.

```khayyam
// MUST: Each static concept is its own type
tp ErrTransactionUnavailable sc {
    // ... all methods return compile-time constants
}
```

This is a MUST because it follows directly from the principle that identity belongs to the type system. A static concept has no data, so there is nothing to put in a shared container. The only remaining mechanism for identity is the type itself.

**Rule 2 — Dynamic Variation → Data**

If instances of a concept vary in their values (but share the same schema), that variation belongs in data — in fields on a single type that all instances share.

```khayyam
// A data carrier: instances differ in values but share the same schema
tp TransactionRecord cp {
    ID          String
    Amount      Decimal
    Timestamp   String
    // ... schema is the same for all instances, values differ
}
```

This is the normal, expected use of data. Nothing unusual here.

**Rule 3 — Different Schema → Distinct Type (SHOULD)**

*Derived from maintainability, readability, and structural clarity — not from the identity principle.*

If two concepts require different data schemas (different fields, different method signatures, different structural shape), they SHOULD be distinct types even if they share some common behavior.

This is a SHOULD, not a MUST, because the reasoning here is different from Rule 1. Rule 1 is mandatory because identity is a hard architectural constraint: if identity belongs to the type system, then a static concept that is not a distinct type has no identity mechanism left. Rule 3 is a recommendation because it derives from practical engineering concerns — keeping the codebase navigable, making the type system's structure mirror the domain's structure, and preventing a single type from accumulating optional fields that are only meaningful for some of its instances. These are strong reasons, but they are not architectural constraints in the same sense as identity. A pragmatic exception (e.g., an externally-defined specification with an open-ended set of schemas) may justify a shared type with variant fields. The framework recommends distinct types as the default but does not mandate them in every case.

### Static Capsule Families

The principle applies to any capsule family whose members are static concepts — where identity is the point, not data. Examples include:

- **Error identifiers**: `ErrTransactionUnavailable`, `ErrInsufficientFunds`, `ErrPermissionDenied` — each is a distinct failure concept. (The Error capsule family has its own dedicated RFC for in-depth design decisions; this RFC establishes only the structural principle that each Error concept must be a distinct type.)

- **Capability identifiers**: `CapabilityRead`, `CapabilityWrite`, `CapabilityAdmin` — each is a distinct permission concept, not a data container.

- **Status codes**: `StatusActive`, `StatusSuspended`, `StatusArchived` — each represents a distinct lifecycle state.

- **Permission descriptors**: `PermissionViewProfile`, `PermissionEditProfile`, `PermissionDeleteAccount` — each is a distinct authorization concept.

In each case, the capsule has no per-instance variation. By Rule 1, each MUST be its own type. If any of these families later acquire per-instance data (e.g., a permission with a scope parameter), that specific capsule graduates from a static concept to a data carrier, and Rule 2 applies instead — but the static members of the family remain distinct types.

### Multi-Concept Returns via Abstraction

A method that can fail in multiple ways returns the parent abstraction, not a specific concept type:

```khayyam
// Single-cause: the method can only return this specific error
tp Authorize mt (self Service) (token Token) (result AuthResult) (err ErrPermissionDenied)

// Multi-cause: the method may return any Error
tp Find mt (self Service) (id ID) (result Result) (err Error)
```

In the multi-cause case, the return type is the `Error` abstraction. The caller receives a value whose concrete type is one of the specific error concepts (`ErrNotFound`, `ErrPermissionDenied`, etc.). Determining which specific error occurred requires a runtime type check — a single type assertion against the concrete type. This is the standard pattern in any language with abstraction types: the abstraction in the return type declares the method's capability to fail, and the concrete type of the returned value carries the specific identity.

The identity guarantee is preserved at the individual concept level: each error is still its own type, and checking "is this an `ErrNotFound`?" is a direct type assertion — not a string comparison, not a field inspection, not a chain-walk through wrapper layers. What is deferred to runtime is the *dispatch* among possible errors, not the *identification* of any individual error.

This pattern is not unique to errors. Any static capsule family whose methods may return one of several concepts uses the same approach: the abstraction as the return type, the concrete type as the identity mechanism.

### Why This Matters: What You Lose Without It

Consider a system that uses a single `GenericError` type with an `Init` method. A developer writes:

```khayyam
tp Find mt (self Service) (id ID) (result Result) (err GenericError) {
    // ...
    err = GenericError{}
    err.Init("ErrNotFound", "memar/storage", "...")
}
```

The caller receives a `GenericError`. To determine which error occurred, it must:
1. Access the `Name()` method's return value.
2. Compare that string to the expected value.

This is a runtime process to answer a question that the type system could have answered in one step: "is this a `ErrNotFound`?" Furthermore, the string comparison is fragile — a typo in either the producer or the consumer silently breaks the check. The compiler cannot help because it does not know that `"ErrNotFound"` is a concept identity — it sees a string like any other.

Now consider the same system under this RFC's principle:

```khayyam
tp Find mt (self Service) (id ID) (result Result) (err ErrNotFound) {
    // ...
    err = ErrNotFound{}
}
```

The caller receives a value whose type *is* the concept. No string comparison, no runtime inspection. The type system carries the full identity. The compiler verifies that the caller handles the specific error type declared in the signature. A typo in the error type name is a compile-time error, not a silent runtime mismatch.

This is not a marginal ergonomics improvement. It is a qualitative difference in what the type system guarantees and what the developer can rely on without testing.

## Reference-level explanation

### The Formal Principle

> **Identity belongs to the type system.** The answer to "which concept is this?" MUST be determinable from the type alone, at compile time, without inspecting any runtime data. When a capsule's entire purpose is to represent a distinct concept and it carries no per-instance dynamic data, the capsule MUST be a distinct type. No generic-initialized type, no tag field, no string comparison may substitute for type-level identity.

### Formal Rules

| Rule | Condition | Requirement | Origin |
|------|-----------|-------------|--------|
| 1 | Capsule has no per-instance dynamic data | MUST be a distinct type | The identity principle: if there is no data, the type is the only identity mechanism |
| 2 | Instances differ only in values, same schema | Data fields on a shared type | The natural role of data: variation between instances |
| 3 | Concepts have different data schemas | SHOULD be distinct types | Maintainability, readability, and structural clarity |

### Enforcement

Current tooling may not fully enforce the distinction between static concepts and data carriers. A structural linter can heuristically detect the absence of fields and `Init` methods, but the final determination may require understanding the capsule's design intent. Future tooling — particularly domain-aware linters operating on the code generator's input definitions (e.g., YAML/DSL specifications) — may provide stronger enforcement, since the generator's input format makes the static/dynamic distinction explicit by construction. Whether and how to integrate such enforcement into the framework's toolchain is a question for a future RFC focused on the code generator's workflow.

### Implications for Existing Framework Mechanisms

The following are **consequences** of this RFC's principle, not reasons for it. They are listed here to document the impact on existing framework mechanisms.

**Covariant Returns.** The framework permits a method to declare its error output as a specific concrete type:

```khayyam
tp Find mt (self Service) (id ID) (result Result) (err ErrNotFound)
```

Because `ErrNotFound` is its own type (required by this RFC), the type system can express "this method returns exactly this error" as a compile-time contract. If errors were generic-initialized values, this contract would be impossible to express — the return type would always be the same generic type regardless of which error concept the method produces. Covariant returns are a benefit that falls out of correct identity modeling, not an argument for it. Khayyam inherently supports covariant return types as part of its abstraction system: if an abstraction dictates a method must return abstraction `A`, a capsule can return capsule `B` (as long as `B` implements `A`).

**Boundary Translation (RFC 000010).** RFC 000010 requires that errors crossing layer boundaries be translated into new, layer-appropriate errors. Each translated error is itself a distinct concept, so by this RFC, it must be its own type. The type system thus maintains compile-time knowledge of error contracts at every layer boundary — not just at the point of origin.

**Code Generation.** A code generator producing capsule definitions MUST emit one type per static capsule concept. The generator's input (e.g., a YAML definition of each error's metadata) maps 1:1 to one output type definition per entry. This is a mechanical consequence: if each concept is a type, the generator must produce one type per concept.

**Cross-Language Compilation.** When a capsule type is compiled from one target language to another, each source-language type maps to one target-language type. Because identity is in the type (not in data), the target-language type carries the full identity of the original concept. A caller in the target language uses native type checking to determine the specific concept, without string comparison or tag dispatch. This 1:1 type mapping is only possible because identity was never stored as data in the first place.

### Compatibility with Immutable Infrastructure (RFC 495369)

A reading of this RFC's constraints from outside the Memar framework might identify "no runtime concept creation" as a limitation: static concepts cannot be created dynamically from configuration files, plugin descriptors, or database records; every concept must exist as a type at compile time.

Within the Memar framework, this is compatible with — and served by the same architectural reasoning as — RFC 495369 (Immutable Infrastructure). That RFC establishes that Memar treats deployed infrastructure as immutable: any change to configuration is a change to the artifact itself, requiring a rebuild/recompile, rather than a runtime-interpreted change to an already-running instance. RFC 495369 further establishes a closely related governance principle: no logic or code may be added to a running Memar application at runtime — every capability increase must go through recompilation. This is treated as the same governance concern as "what code can be added to a repository," addressed once (through source review) rather than duplicated across two separate control points (source review and a runtime-loading mechanism).

This RFC's requirement that static concepts be types is compatible with this governance model: if every concept must be a type, new concepts require recompilation, which is consistent with RFC 495369's requirement that capability changes go through the build pipeline.

It is important to be precise about the relationship between the two RFCs. They are **compatible** and share a common architectural inclination, but they are **logically independent**:

- This RFC's principle: identity must be in the type system, not in data.
- RFC 495369's principle: all capability changes require recompilation.

A system could, in principle, satisfy RFC 495369 with a purely data-based identity model — for example, a closed, compile-time-fixed set of immutable sentinel values with numeric IDs, where no new concept can be added at runtime but identity is still carried by data rather than by the type. Such a system would be fully compatible with immutable infrastructure without adopting this RFC's principle. The two principles are *convergent* (both push toward compile-time fixedness) but not *interdependent* (neither logically requires the other).

What this RFC adds, beyond what RFC 495369 alone provides, is the *type-system mechanism* for identity: not only are concepts fixed at compile time, but the type system itself carries and verifies their identity. This is a stronger guarantee than compile-time-fixed data — it is compile-time-*typed* identity.

A potential future mechanism — a runtime type registry that could register new concept types without full recompilation — could theoretically be compatible with this RFC's identity principle (identity is in the type, even if the type is registered at runtime) while conflicting with RFC 495369's governance principle (a new capability was added without recompilation). Whether such a mechanism is desirable, architecturally sound, or within the scope of either RFC is an open question. The current position is that it should not be assumed or built into the framework's default behavior; like configuration-driven behavior in RFC 495369, it is an optional feature whose presence must be deliberately designed and justified, not an implicit backdoor around the default governance model.

### The Classification Problem

The most important unresolved challenge this RFC leaves for future work is the **Classification Problem**: how does a developer (or a tool) determine whether a given capsule is a "static concept" or a "data carrier"?

The principle is clear in its extremes. `ErrTransactionUnavailable` — a capsule with no fields, no `Init` method, and all methods returning compile-time constants — is unambiguously a static concept. `TransactionRecord` — a capsule with `ID`, `Amount`, and `Timestamp` fields — is unambiguously a data carrier. The difficulty lies in the gray zone between these extremes:

- A status capsule that carries only a `timestamp` field indicating when the status was set — is it a static concept with incidental metadata, or a data carrier with one field?
- A permission capsule that has a `scope` parameter in some deployments but not others — is it static or dynamic, and does the answer change per-deployment?
- A concept that is static today but may acquire instance data in a future version — at what point does it "graduate" from Rule 1 to Rule 2?

This RFC deliberately does not attempt to define a formal classification procedure. The principle ("if it has no per-instance data, it is static") is itself well-defined; the challenge is determining, for a given capsule design, whether it *has* per-instance data in the architectural sense. This determination depends on the capsule's design intent, which is not always self-evident from the code alone.

The Classification Problem is the single most important topic for a follow-up RFC. Until such an RFC exists, the framework relies on the developer's judgment, guided by the principle stated here and by the examples in this document. Future tooling (particularly the code generator, whose input format makes the static/dynamic distinction explicit) will reduce but not eliminate the need for human judgment in ambiguous cases.

### Suggested Naming Conventions

For error capsules, the convention `Err` + `PascalCase description` is already in use (e.g. `ErrTransactionUnavailable`, `ErrInsufficientFunds`). This RFC records it as a suggested default for that capsule family.

This is a non-binding convention: enforcement, if any, is a per-organization Linter configuration choice, not a language-level requirement. Other static capsule families may follow their own domain-appropriate naming conventions.

## Drawbacks

1. **Type proliferation.** A system with many static concepts will contain many distinct type definitions. This is the intended and correct consequence of giving each concept its own identity. The cost is borne by the code generator (which produces types mechanically), not by developers manually authoring them. In the rare case where a developer must define a static capsule by hand, the boilerplate is substantial. This verbosity is accepted as a deliberate signal: the framework expects static capsules to be generated, and the manual path's weight reinforces that expectation.

2. **Conceptual shift for developers.** Developers accustomed to thinking of errors (or status codes, or identifiers) as values — strings, constants, or tagged union variants — must adjust to thinking of them as types. This is not merely a syntactic change but a shift in what the type system is expected to do. The framework's philosophy (RFC 000001) provides the foundation for this shift, but adoption friction is real and acknowledged.

3. **Increased API surface per concept.** Each distinct type that appears in a public method signature becomes part of the API contract. Changing or removing that type is a breaking change. This is a genuine cost. The framework accepts this cost because the benefit — type-level identity verified at compile time — is judged to outweigh it for the kind of systems Memar targets. But this is a trade-off, not a free win, and projects with different priorities (rapid iteration, unstable APIs, or a need to minimize public type counts) may reasonably reach a different conclusion.

## Rationale and alternatives

### The Single Argument

If one argument must be chosen among all those presented, it is this:

> A single generic type with `Init` demotes identity from the type system to runtime data. In the Memar framework's model, identity MUST be part of the type system — it MUST be knowable at compile time, verifiable by the compiler, and expressible in method signatures. Representing identity as data (a string in a field, a tag in an enum, a constant to compare) moves this knowledge from compile time to runtime, from the type checker to the test suite. This demotion is the fundamental violation.

Everything else — covariant returns, code generation simplicity, cross-language mapping — is a consequence of getting this one thing right. They are benefits, not reasons. The reason is the principle itself: identity belongs to the type system.

### Rejected: Single Generic Type with Init Method

A single `GenericError` type holding all metadata as instance fields, populated through an `Init` method or factory function.

**Rejected because:** it demotes identity to data. The "which error occurred" question — a question about concept identity — is answered by comparing a string stored in a field at runtime, instead of by the type system at compile time. This violates the core principle. The `Init` method accepts compile-time constants (name, domain, summary) and stores them as runtime state, using a data-container abstraction to simulate what the type system provides natively.

### Rejected: Enum-Tagged Single Type

A single type with an enum-like tag field distinguishing concepts.

**Rejected because:** functionally equivalent to the generic Init approach with respect to identity. The "which concept" question is answered by a runtime tag value, not by the type. The tag is typed (an enum) rather than untyped (a string), which provides marginal safety, but does not address the fundamental issue: identity has been moved from the type system to a runtime value. This is the approach taken by Rust's error enums — Rust accepts this trade-off because it values exhaustiveness checking within a grouped failure family. Memar values type-level identity in individual method signatures more than grouped exhaustiveness. These are different design goals, both valid.

### Rejected: String-Based Codes

Defining concepts as string constants.

**Rejected because:** the most extreme form of identity demotion. The type system provides no information about which concept is represented. All distinction is deferred to string comparison at runtime, with no compile-time safety, no structural metadata, and no mechanism for tooling (code generator, cross-language compiler, linter) to consume.

### Impact of Not Doing This

Without a deliberate, documented decision, the question of "distinct type or generic?" will be answered inconsistently across the codebase and across language bindings. Some concepts will be types, others will be data, and the resulting inconsistency will propagate into every tool that consumes capsule definitions. The type system's role in the framework will be unclear — sometimes it carries identity, sometimes it doesn't — and developers will make the choice based on convenience rather than principle. This RFC settles the question by stating the principle that resolves it: identity is the type system's responsibility.

## Prior art

### Java Exception Classes

Java assigns each error concept its own class extending `Exception` or `RuntimeException`. This is the closest mainstream prior art to this RFC's principle. Java's weakness is not the type-per-concept model — which is sound and validated by decades of use — but the exception mechanism (implicit stack unwinding, catch blocks at arbitrary distances from the throw site) that Memar rejects. Java's checked exception mechanism also demonstrates the API-surface risk: each exception type in a `throws` clause becomes part of the method's contract, making API evolution harder. Memar does not use checked exceptions, so this specific risk is less severe.

### Rust and Swift Error Enums

Rust and Swift use enum variants within error types, where each variant is a distinct concept. Rust optimizes for grouped failure families — the ability to say "this method can fail in one of these related ways" and handle them exhaustively in a single `match`. Memar optimizes for type-level contract identity — the ability to say "this method returns exactly this concept" in the type signature. These are different design goals, both valid for their respective frameworks. Rust's approach provides exhaustiveness checking (the compiler verifies that all variants are handled) but identity is in a runtime tag, not in the type itself. Memar's approach provides type-level identity per concept but does not provide per-signature exhaustiveness — a trade-off the framework accepts because identity is judged to be the higher-priority guarantee.

### The Industry's Implicit Drift Toward Type Identity

Across multiple language communities, there is an observable drift toward type-level identity for error-like concepts — even in ecosystems that officially reject it. Developers who need structured, identifiable errors begin defining custom types because sentinel strings are insufficient. Lint rules emerge to distinguish identity-as-data from identity-as-type. Richer comparison mechanisms are built to approximate what the type system would have provided natively. This drift suggests that the need for type-level identity is real and widespread, even when a language's official philosophy does not prioritize it. Memar's position is that this need should be met by the type system directly, not approximated through layered runtime mechanisms. The companion document `Static_Concepts_Must_Be_Types-vs-go_philosophy.md` documents this drift in detail within the Go ecosystem.

## Unresolved questions

- **Dynamic capsule schema boundary.** Rule 3 states that different schemas SHOULD produce distinct types, but the boundary between "different schema" and "same schema with optional fields" is not always clear. A `TransactionRecord` with 12 fields and a `TransactionRecord` with 13 fields (one added in a later version) — are these the same schema or different? This judgment is left to the developer and, ultimately, to the framework's versioning RFCs when they exist. This RFC does not attempt to define a formal schema-equivalence relation.

- **Tooling enforcement strategy.** Whether and how linters, the code generator, or future domain-aware tooling should enforce Rule 1 is a tooling question deferred to a future RFC. The current assessment is that enforcement is most naturally achieved at the code generator's input layer, where the static/dynamic distinction is explicit by construction, rather than at the output source-code layer where it must be inferred heuristically.

- **The Classification Problem — formalization.** This RFC identifies the Classification Problem (determining whether a capsule is a static concept or a data carrier) as the most important open question, but does not provide a formal classification procedure. A dedicated RFC — potentially titled "How To Distinguish Concepts From Data" — is needed to define criteria, heuristics, and, where possible, mechanical checks for this determination. Until such an RFC exists, the framework relies on the developer's judgment.

- **Interaction with plugin and extension systems.** Systems requiring runtime-defined concepts (e.g., plugin architectures with third-party failure modes, or extensible permission models where new permissions are defined by plugins) need a mechanism outside this RFC's scope. Whether such systems are compatible with Memar's immutable infrastructure principle (RFC 495369) at all, or whether they require a separate concept-registry mechanism with its own RFC, is an open architectural question. The current position is that any mechanism for runtime concept registration would need to provide the same identity guarantees that the type system provides for compile-time concepts — a challenging requirement that may constrain the design space significantly.

- **`IsEmpty` / `IsNil` / `IsNull` semantics for static capsules.** These methods are inherited from `ADT` and may not be meaningful for static capsules that carry no per-instance data. Whether they should return fixed values, be excluded from static capsule interfaces, or carry family-specific semantics, is a question for the ADT capsule family's own RFC.

## Future possibilities

- **Code generator RFC.** A dedicated RFC specifying the code generator's input format, output structure, and target-language emission strategy. That RFC will build on this RFC's principle as a foundational constraint: the generator must emit one type per static concept.

- **Cross-language compiler RFC.** A RFC specifying how capsule types are mapped between languages, relying on this RFC's guarantee that identity is type-level, enabling 1:1 type mapping.

- **"How To Distinguish Concepts From Data" RFC.** A dedicated RFC addressing the Classification Problem: formal criteria for determining whether a capsule is a static concept or a data carrier. This is the single most important follow-up to this RFC, because the Classification Problem is the primary source of ambiguity in applying the principle.

- **Extension to dynamic capsules with schema variation.** If the framework later needs a formal rule for when dynamic capsules with different schemas must be separate types (currently a SHOULD in Rule 3), a follow-up RFC could define a schema-equivalence relation and upgrade Rule 3 to a MUST where the relation is well-defined.

- **Immutable Infrastructure deep-dive (RFC 495369 expansion).** RFC 495369 is currently a placeholder recording the immutable infrastructure principle. A dedicated session is planned to define its full scope, including its relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning.

---

## Change Rationale

| Revision | Section | Change | Reason |
|----------|---------|--------|--------|
| 6 (this) | Entire document | Split into two files: this principle RFC (memar) and a Go philosophy companion (memar-go). Removed all Go-specific analysis, community critiques, and language comparisons from this file. Converted examples to Khayyam syntax. Simplified multi-cause returns to standard abstraction pattern. | User direction: RFC should be Khayyam/Memar-centered, not Go-centered; Error has its own RFC; Go comparison belongs in memar-go |
| 6 | Guide → "Static Capsule Families" | Replaced separate "Error Capsule as Primary Example" and "Beyond Errors" sections with unified section; Error is one family among many | User: "too much focus on Error in this file; Error will have its own RFC" |
| 6 | Guide → "Multi-Concept Returns via Abstraction" | New section replacing "Multi-Cause Error Returns"; presents Error abstraction as the standard, well-understood pattern, not an open problem | User: "the answer is defining a variable with the abstraction type" |
| 6 | Drawbacks | Removed "Not idiomatic Go" and "No exhaustiveness checking" — these are implementation-specific, not principle-level | Move to memar-go companion |
| 6 | Rationale | Removed "Go-Style Sentinel Errors", "Interface-Based Predicates", "Memar–Go Design Target Comparison" | Move to memar-go companion |
| 6 | Prior art | Shortened significantly; moved detailed Go analysis to companion; added "Industry's Implicit Drift" high-level observation | User: "text is too built on other languages" |
| 6 | Unresolved questions | Removed "Multi-cause error return signatures" — no longer an open question | User: abstraction type is the standard answer |
| 6 | Related → Depends_on | Removed 000000 (incorrect reference); kept 000001 and 495369 | User: "incorrectly attributed to 000000" |
| 5 | Reference → Immutable Infrastructure | Renamed from "Alignment with" to "Compatibility with"; added logical independence analysis | Claude's critique: over-claim of reinforcement |
| 5 | Reference → The Classification Problem | Elevated from brief mention to full subsection | User identified as most important future challenge |
| 4 | Summary | Added immutable infrastructure compatibility | RFC 495369 alignment |
| 4 | Guide → Identity/Data/Behavior | Added three-column table and key paragraph | Core architectural insight |
| 4 | Reference → Compatibility with Immutable Infrastructure | New subsection | User: "No runtime concept creation" is not a drawback |
| 4 | Drawbacks | Removed "No runtime concept creation" | Reframed as compatible with RFC 495369 |