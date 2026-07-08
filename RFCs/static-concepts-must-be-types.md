---
RFC Number: 495421
Title: "Static Concepts Must Be Types"
Status: Proposed
Start Date: 2026-07-08
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000000", "000001", "495369"]
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Original design decision, years of production validation in memar-go, core principle formulation, Go philosophy analysis, Classification Problem identification, Immutable Infrastructure alignment insight"
    task: []
  - name: "Super Z"
    uri: ""
    model: "GLM"
    effort: ""
    contribution: "Drafted RFC through four revisions, documented trade-offs, integrated community research, wrote final comprehensive version"
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: "Internet research on Go community critiques; compiled citations from Rob Pike, Dave Cheney, Go 1.13 design docs, DoltHub, Matt Proud, golangci-lint, CedarDB, yegor256"
    task: []
---

## Summary

Identity belongs to the type system. In the Memar framework, the answer to "which concept is this?" MUST be determinable from the type alone, at compile time, without inspecting any runtime data. A static capsule — one with no per-instance dynamic data — MUST therefore be its own distinct type. A capsule whose instances share the same schema and differ only in values may use a shared type. A capsule whose instances have different data schemas SHOULD use distinct types. The Error capsule family is the primary motivating example, but the principle applies to any capsule in the framework.

This principle is not universally accepted. The Go ecosystem — in which memar-go is currently implemented — deliberately chose a value-oriented error model where identity is carried by runtime data (sentinel variables, wrapped errors inspected via `errors.Is`). That choice optimizes for flexibility and ergonomics. Memar's choice optimizes for type-level contract identity and compile-time verifiability. These are different design targets, both valid for their respective frameworks. This RFC documents Memar's position, responds to the known critiques from the Go community, and explains why the two frameworks' differing optimization targets lead to genuinely different conclusions.

The inability to create concepts at runtime — which a Go-native reading might list as a drawback — is in fact aligned with Memar's Immutable Infrastructure principle (RFC 495369): no capability may be added to a running Memar application without recompilation. This is not a limitation imposed by the type system; it is a deliberate governance choice that the type-system constraint naturally reinforces.

## Motivation

### The Core Question

Consider two approaches to representing a distinct concept such as "transaction unavailable":

1. **The concept is the type.** `ErrTransactionUnavailable` is its own type. The type *is* the concept. No data is needed to distinguish it from `ErrInsufficientFunds` — the type system does that.

2. **The concept is data.** A single `GenericError` type holds a `name` field set to `"ErrTransactionUnavailable"`. The concept "transaction unavailable" is represented by a string stored in memory at runtime, not by the type itself.

Both approaches produce a working program. The difference is not in correctness but in **what role the type system plays**. The first approach assigns the type system its strongest possible responsibility: answering "what is this?" The second approach reduces the type system to a container and delegates identity to data — the same kind of data that holds quantities, timestamps, and configuration values.

This RFC establishes that the first approach is not merely preferred but mandatory for static capsules, because in the Memar framework's architectural model, identity is the type system's job, and data is for variation between instances of the same concept — not for distinguishing one concept from another.

### Why This Is Not Obvious

Most programming languages and frameworks do not make this distinction explicitly. Go uses `errors.New("not found")` — a string value inside a shared interface type. Python uses exception classes, which are closer to the principle, but the culture mixes class-based and string-based patterns freely. JavaScript uses string codes or custom error subclasses — again, mixed. The industry has no consensus on whether identity belongs to the type system or to data, and the absence of a deliberate decision is what produces the inconsistency this RFC resolves.

RFC 000001 establishes that the framework is the architectural authority over the language. This means the framework gets to decide what the type system is responsible for — and this RFC decides that identity is one of those responsibilities.

### The Go Ecosystem's Implicit Question

The Go community's response to its own value-oriented error model is itself instructive. Over more than a decade, the Go ecosystem has progressively built type-level identity mechanisms around errors — without explicitly acknowledging that this is what it is doing:

- **`errors.New`** (Go 1.0): pure string-based identity. The type system provides no information about which error is represented.
- **Custom error types** (community practice from early Go): developers who needed structured, identifiable errors began defining their own types — `type NotFoundError struct{}` — because sentinel strings were insufficient for their needs. This is the community implicitly rediscovering the principle this RFC makes explicit.
- **`errors.Is` / `errors.As`** (Go 1.13): introduced to solve the problem that wrapped errors could no longer be compared by pointer equality. These functions restore the ability to determine "which error is this" — but they do so through runtime chain-walking, not through the type system. The type system still only knows `error`.
- **`golangci-lint` `errname` rule**: enforces that sentinel errors use the `Err` prefix (e.g., `ErrNotFound`) and error types use the `Error` suffix (e.g., `NotFoundError`). This lint rule encodes a naming convention that distinguishes identity-as-data (`ErrNotFound`, a variable) from identity-as-type (`NotFoundError`, a type definition) — a distinction the language itself does not enforce but the community has found necessary enough to automate.
- **Interface-based predicates** (custom `Is(target error) bool` methods): allow error types to define their own matching logic, effectively implementing type-level identity checking through a runtime method dispatch. This is the most sophisticated form of identity simulation that Go's value-oriented model permits — and it is still a simulation, because the method dispatch happens at runtime, not at compile time.

Each of these innovations addresses a real pain point caused by the absence of type-level identity for errors. Each is, in its own way, an attempt to rebuild some of the guarantees that type-level identity would have provided natively. The Memar framework's position is that these guarantees should be provided by the type system directly, not approximated through runtime mechanisms layered on top of a value-based model.

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

```
// MUST: Each static concept is its own type
tp ErrTransactionUnavailable sc {
    Name()       → "ErrTransactionUnavailable"
    Domain()     → "memar/finance"
    Summary()    → "The transaction could not be completed due to a temporary service issue."
    // ... all methods return compile-time constants
}
```

This is a MUST because it follows directly from the principle that identity belongs to the type system. A static concept has no data, so there is nothing to put in a shared container. The only remaining mechanism for identity is the type itself.

**Rule 2 — Dynamic Variation → Data**

If instances of a concept vary in their values (but share the same schema), that variation belongs in data — in fields on a single type that all instances share.

```
// A data carrier: instances differ in values but share the same schema
tp TransactionRecord sc {
    ID          string
    Amount      decimal
    Timestamp   string
    // ... schema is the same for all instances, values differ
}
```

This is the normal, expected use of data. Nothing unusual here.

**Rule 3 — Different Schema → Distinct Type (SHOULD)**

*Derived from maintainability, readability, and structural clarity — not from the identity principle.*

If two concepts require different data schemas (different fields, different method signatures, different structural shape), they SHOULD be distinct types even if they share some common behavior.

This is a SHOULD, not a MUST, because the reasoning here is different from Rule 1. Rule 1 is mandatory because identity is a hard architectural constraint: if identity belongs to the type system, then a static concept that is not a distinct type has no identity mechanism left. Rule 3 is a recommendation because it derives from practical engineering concerns — keeping the codebase navigable, making the type system's structure mirror the domain's structure, and preventing a single type from accumulating optional fields that are only meaningful for some of its instances. These are strong reasons, but they are not architectural constraints in the same sense as identity. A pragmatic exception (e.g., an externally-defined specification with an open-ended set of schemas) may justify a shared type with variant fields. The framework recommends distinct types as the default but does not mandate them in every case.

### The Error Capsule as Primary Example

Error capsules are the most prominent family of static capsules in the framework. An `Error` capsule (RFC 000000) carries no per-instance dynamic data: its `Name()`, `Domain()`, `Summary()`, and all other methods return values determined at type-definition time. Therefore, by Rule 1, each Error concept MUST be its own type.

```
// Each error is a distinct static concept → distinct type
tp ErrTransactionUnavailable sc { ... }
tp ErrInsufficientFunds      sc { ... }
tp ErrPermissionDenied       sc { ... }
```

The alternative — a single `GenericError` type with an `Init` method — would mean "transaction unavailable" is represented by a string stored at runtime inside a generic container. This demotes identity from compile-time type knowledge to runtime data comparison, which is exactly what this RFC prohibits for static capsules.

In the current Go implementation (`error.go`), the `Error` interface embeds `datatype_p.DataType`, `mediatype_p.Field_MediaType`, and `adt_p.ADT`, plus the `ImplementsError` marker and `Field_Error` accessor. Each concrete error capsule type implements the full method set:

```go
func (datatype_p.Quiddity) Abbreviation() string
func (datatype_p.Quiddity) Aliases() []string
func (datatype_p.Field_ID) DataTypeID() datatype_p.ID
func (datatype_p.Field_ID_Base64) DataTypeID_Base64() string
func (datatype_p.Detail) DevActionNote() string
func (datatype_p.Detail) Domain() string
func (datatype_p.Details) ExpireInFavorOf() datatype_p.DataType
func (datatype_p.Details) ExpiryDate() string
func (adt_p.Nil) IsNil() bool
func (datatype_p.Details) IssueDate() string
func (datatype_p.Field_LifeCycle) LifeCycle() datatype_p.LifeCycle
func (mediatype_p.Field_MediaType) MediaType() mediatype_p.MediaType
func (datatype_p.Quiddity) Name() string
func (datatype_p.Detail) Overview() string
func (datatype_p.Details) ReferenceURI() string
func (datatype_p.Detail) Summary() string
func (datatype_p.Detail) TAGS() []string
func (datatype_p.Detail) UserActionNote() string
```

For a static Error capsule, every one of these methods returns a compile-time constant. Two variables of the same error type are always indistinguishable — there is no per-instance state to compare. This is the definition of a static concept, and it is why Rule 1 applies with full force: the type is the only identity mechanism, and it is sufficient.

Two methods inherited from `DataType` deserve explicit discussion in the Error context:

- **`IsEmpty`**: Inherited from `adt_p.Empty`. For a static Error capsule with no per-instance data, the concept of "empty" is arguably meaningless — there is no container to be empty or full. Whether `IsEmpty()` should return `true` (no data to be empty of), `false` (the concept itself is fully present), or be excluded from the Error interface entirely, is a question for the ADT capsule family's own RFC, not this one. This RFC notes the tension but does not resolve it.

### Beyond Errors: Other Static Capsule Families

The same reasoning applies to any capsule family whose members are static concepts — where identity is the point, not data. Examples include:

- **Capability identifiers**: `CapabilityRead`, `CapabilityWrite`, `CapabilityAdmin` — each is a distinct permission concept, not a data container.
- **Status codes**: `StatusActive`, `StatusSuspended`, `StatusArchived` — each represents a distinct lifecycle state.
- **Permission descriptors**: `PermissionViewProfile`, `PermissionEditProfile`, `PermissionDeleteAccount` — each is a distinct authorization concept.

In each case, the capsule has no per-instance variation. By Rule 1, each MUST be its own type. If any of these families later acquire per-instance data (e.g., a permission with a scope parameter), that specific capsule graduates from a static concept to a data carrier, and Rule 2 applies instead — but the static members of the family remain distinct types.

### Why This Matters: What You Lose Without It

Consider a system that uses a single `GenericError` type with an `Init` method. A developer writes:

```go
func (s Service) Find(id ID) (Result, error) {
    // ...
    return Result{}, GenericError{}.Init("ErrNotFound", "memar/storage", "...")
}
```

The caller receives an `error` interface. To determine which error occurred, it must:
1. Type-assert to `GenericError` (or use `errors.As`).
2. Inspect the `Name()` field's return value.
3. Compare that string to the expected value.

This is a three-step runtime process to answer a question that the type system could have answered in one step: "is this a `ErrNotFound`?" Furthermore, the string comparison is fragile — a typo in either the producer or the consumer silently breaks the check. The compiler cannot help because it does not know that `"ErrNotFound"` is a concept identity — it sees a string like any other.

Now consider the same system under this RFC's principle:

```go
func (s Service) Find(id ID) (Result, ErrNotFound) {
    // ...
    return Result{}, ErrNotFound{}
}
```

The caller receives a value whose type *is* the concept. No string comparison, no type assertion chain, no runtime inspection. The type system carries the full identity. The compiler verifies that the caller handles the specific error type declared in the signature. A typo in the error type name is a compile-time error, not a silent runtime mismatch.

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

**Covariant Error Returns (RFC 000000).** RFC 000000 permits a method to declare its error output as a specific concrete type:

```
func (s Service) Find(id ID) (result Result, err ErrNotFound)
```

Because `ErrNotFound` is its own type (required by this RFC), the type system can express "this method returns exactly this error" as a compile-time contract. If errors were generic-initialized values, this contract would be impossible to express — the return type would always be the same generic type regardless of which error concept the method produces. Covariant returns are a benefit that falls out of correct identity modeling, not an argument for it.

**Boundary Translation (RFC 000010).** RFC 000010 requires that errors crossing layer boundaries be translated into new, layer-appropriate errors. Each translated error is itself a distinct concept, so by this RFC, it must be its own type. The type system thus maintains compile-time knowledge of error contracts at every layer boundary — not just at the point of origin.

**Code Generation.** A code generator producing capsule definitions MUST emit one type per static capsule concept. The generator's input (e.g., a YAML definition of each error's metadata) maps 1:1 to one output type definition per entry. This is a mechanical consequence: if each concept is a type, the generator must produce one type per concept.

**Cross-Language Compilation.** When a Go capsule type is compiled to JavaScript, each Go type maps to one JavaScript class. Because identity is in the type (not in data), the JavaScript class carries the full identity of the original concept. A caller in the target language uses native type checking (`instanceof`) to determine the specific concept, without string comparison or tag dispatch. This 1:1 type mapping is only possible because identity was never stored as data in the first place.

### Alignment with Immutable Infrastructure (RFC 495369)

A reading of this RFC's constraints from outside the Memar framework might identify "no runtime concept creation" as a limitation: static concepts cannot be created dynamically from configuration files, plugin descriptors, or database records; every concept must exist as a type at compile time.

Within the Memar framework, this is not a limitation but a reinforcement of a deliberate foundational principle. RFC 495369 (Immutable Infrastructure) establishes that Memar treats deployed infrastructure as immutable: any change to configuration is a change to the artifact itself, requiring a rebuild/recompile, rather than a runtime-interpreted change to an already-running instance. RFC 495369 further establishes a closely related governance principle: no logic or code may be added to a running Memar application at runtime — every capability increase must go through recompilation. This is treated as the same governance concern as "what code can be added to a repository," addressed once (through source review) rather than duplicated across two separate control points (source review and a runtime-loading mechanism).

This RFC's requirement that static concepts be types is naturally aligned with this governance model. If every concept that exists in the system's identity model must be a type, then new concepts require recompilation — exactly as RFC 495369 requires for any capability change. The type system and the immutable infrastructure principle reinforce each other: the type system provides the mechanism (concepts are types, types require compilation), and the immutable infrastructure principle provides the governance rationale (all capability changes go through the same build-review-deploy pipeline).

This alignment is not accidental. Both RFCs trace back to the same architectural conviction: the set of concepts a system recognizes should be known, reviewed, and fixed at build time — not emergent from runtime state. This RFC addresses the type-system expression of that conviction; RFC 495369 addresses the deployment and governance expression. Together, they ensure that a Memar system's conceptual vocabulary is as immutable as its infrastructure.

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

1. **Type proliferation.** A system with many static concepts will contain many distinct type definitions. This is the intended and correct consequence of giving each concept its own identity. The cost is borne by the code generator (which produces types mechanically), not by developers manually authoring them. In the rare case where a developer must define a static capsule by hand, the boilerplate is substantial (~20 method implementations for an Error capsule). This verbosity is accepted as a deliberate signal: the framework expects static capsules to be generated, and the manual path's weight reinforces that expectation.

2. **Not idiomatic Go.** This RFC's principle is not how the Go community writes error-handling code. Go's established idiom uses sentinel error variables (`var ErrNotFound = errors.New("not found")`), wrapped errors inspected via `errors.Is`, and occasional custom types when structured data is needed. Requiring a distinct type for every static concept — including concepts that would be sentinel variables in idiomatic Go — is a deliberate departure from community norms. Developers working in memar-go must understand that they are writing Memar-framework code that happens to be compiled by the Go compiler, not idiomatic Go code. The framework's architectural authority (RFC 000001) gives it the right to make this choice, but the friction is real and acknowledged.

3. **Conceptual shift for developers.** Developers accustomed to thinking of errors (or status codes, or identifiers) as values — strings, constants, or tagged union variants — must adjust to thinking of them as types. This is not merely a syntactic change but a shift in what the type system is expected to do. The framework's philosophy (RFC 000001) provides the foundation for this shift, but adoption friction is real and acknowledged.

4. **Increased API surface per concept.** Dave Cheney's caution applies: *"Public error types increase surface area, new implementations must only return types specified… error type cannot be changed or deprecated without breaking compatibility."* Each distinct type that appears in a public method signature becomes part of the API contract. Changing or removing that type is a breaking change. This is a genuine cost, and it is the strongest single argument against this RFC's principle from within the Go community. The framework accepts this cost because the benefit — type-level identity verified at compile time — is judged to outweigh it for the kind of systems Memar targets. But this is a trade-off, not a free win, and projects with different priorities (rapid iteration, unstable APIs, or a need to minimize public type counts) may reasonably reach a different conclusion.

## Rationale and alternatives

### The Single Argument

If one argument must be chosen among all those presented, it is this:

> A single generic type with `Init` demotes identity from the type system to runtime data. In the Memar framework's model, identity MUST be part of the type system — it MUST be knowable at compile time, verifiable by the compiler, and expressible in method signatures. Representing identity as data (a string in a field, a tag in an enum, a constant to compare) moves this knowledge from compile time to runtime, from the type checker to the test suite. This demotion is the fundamental violation.

Everything else — covariant returns, code generation simplicity, cross-language mapping, exhaustiveness checking — is a consequence of getting this one thing right. They are benefits, not reasons. The reason is the principle itself: identity belongs to the type system.

### Rejected: Single Generic Type with Init Method

A single `GenericError` type holding all metadata as instance fields, populated through an `Init` method or factory function.

**Rejected because:** it demotes identity to data. The "which error occurred" question — a question about concept identity — is answered by comparing a string stored in a field at runtime, instead of by the type system at compile time. This violates the core principle. The `Init` method accepts compile-time constants (name, domain, summary) and stores them as runtime state, using a data-container abstraction to simulate what the type system provides natively.

### Rejected: Enum-Tagged Single Type

A single type with an enum-like tag field distinguishing concepts.

**Rejected because:** functionally equivalent to the generic Init approach with respect to identity. The "which concept" question is answered by a runtime tag value, not by the type. The tag is typed (an enum) rather than untyped (a string), which provides marginal safety, but does not address the fundamental issue: identity has been moved from the type system to a runtime value.

### Rejected: String-Based Error Codes

Defining concepts as string constants.

**Rejected because:** the most extreme form of identity demotion. The type system provides no information about which concept is represented. All distinction is deferred to string comparison at runtime, with no compile-time safety, no structural metadata, and no mechanism for tooling (code generator, cross-language compiler, linter) to consume.

### Rejected: Go-Style Sentinel Errors with `errors.Is`

Using `errors.New("not found")` (or `var ErrNotFound = errors.New(...)`) as sentinel values, distinguished at runtime via `errors.Is(err, ErrNotFound)`.

**Rejected because:** identity is carried by a variable's value (a pointer to an internal struct containing a string), not by the type system. The type of both `ErrNotFound` and `ErrPermissionDenied` is the same: `*errors.errorString` (or whatever internal type `errors.New` returns). The type system cannot distinguish them. `errors.Is` provides structured comparison, but it is runtime chain-walking, not compile-time type checking. As DoltHub's benchmark analysis demonstrated, this chain-walking carries a performance cost: `errors.Is` is approximately 5.5x slower than a boolean return when the value is not found, and 6x slower when it is found. This performance cost is a secondary concern — the primary rejection reason remains the identity demotion.

This rejection is specific to Memar's architectural goals. Within the Go ecosystem, sentinel errors with `errors.Is` are a well-designed solution for Go's optimization targets. The Go 1.13 design doc (Newton et al.) explicitly lists sentinel variables as one of the accepted patterns for identifiable errors, alongside custom types and predicate functions. The Go team's position is that flexibility in error representation is more valuable than type-level identity. Memar's position is the reverse. These are different optimization targets, both valid for their respective frameworks.

### Rejected: Interface-Based Predicates

Defining custom `Is(target error) bool` methods on error types, allowing each error to define its own matching logic.

**Rejected because:** while more sophisticated than sentinel comparison, this is still runtime behavior. The method dispatch happens at runtime; the type system does not know which `Is` method will match until the code executes. This approach can express rich identity logic (e.g., "this error matches if it carries a specific code *and* a specific domain"), but it cannot express identity at compile time. For static capsules — where identity is the entire point and there is no instance data to factor into the comparison — the added runtime complexity is unnecessary overhead for a weaker guarantee than the type system provides natively.

### The Memar–Go Design Target Comparison

The Go community's critiques of distinct error types are not wrong — they are correctly analyzing the trade-off from within Go's design frame. The disagreement is about the design frame itself, not about the analysis within it.

**What Go optimizes for:**

- **Flexibility**: a function can return any error without committing to a specific type in its signature. This makes API evolution easier: adding a new error case does not require changing the return type.
- **Simplicity of the error model**: `error` is a single interface. There is no error type hierarchy to learn, no inheritance chain to navigate.
- **Ergonomics for common cases**: `errors.New("not found")` is three words. Defining a custom type requires a struct definition, an `Error() string` method, and usually a constructor.
- **Composability**: `fmt.Errorf("context: %w", err)` wraps any error without needing to know its type. Wrapping chains are transparent to `errors.Is` and `errors.As`.

These are genuine strengths, and they explain why the Go community has not converged on "one type per error concept" as an idiom despite more than a decade of discussion.

**What Memar optimizes for:**

- **Type-level contract identity**: the answer to "which concept is this?" is known at compile time, verified by the type checker, and expressible in method signatures.
- **Architectural clarity**: identity, behavior, and data have distinct, non-overlapping homes. No mechanism simulates another's job.
- **Framework-as-authority**: the framework (RFC 000001) decides what the type system is responsible for, and this RFC decides that identity is one of those responsibilities. The framework's goals take precedence over language-community conventions.
- **Cross-language fidelity**: when capsule types are compiled to other languages, identity maps 1:1 through the type system. No string-based dispatch, no runtime chain-walking.

These are different optimization targets. Neither is objectively "correct" in isolation — each is correct for its framework's goals. Go's value-oriented error model serves Go's goals well. Memar's type-oriented model serves Memar's goals well. The disagreement is architectural, not technical: it is about what the type system should be responsible for, and that question has no universal answer.

The Go ecosystem's own evolution, however, is instructive. The progressive introduction of custom error types, `errors.Is/As`, the `errname` lint rule, and interface-based predicates reveals a pattern: the Go community keeps building type-level identity mechanisms around errors without explicitly acknowledging that this is what it is doing. Each innovation addresses a real pain point caused by the absence of type-level identity. Each is, in its own way, an attempt to approximate the guarantees that type-level identity would have provided natively. Memar's position is that these guarantees should be provided by the type system directly, not approximated through runtime mechanisms.

### Impact of Not Doing This

Without a deliberate, documented decision, the question of "distinct type or generic?" will be answered inconsistently across the codebase and across language bindings. Some concepts will be types, others will be data, and the resulting inconsistency will propagate into every tool that consumes capsule definitions. The type system's role in the framework will be unclear — sometimes it carries identity, sometimes it doesn't — and developers will make the choice based on convenience rather than principle. This RFC settles the question by stating the principle that resolves it: identity is the type system's responsibility.

## Prior art

### Java Exception Classes

Java assigns each error concept its own class extending `Exception` or `RuntimeException`. This is the closest mainstream prior art to this RFC's principle. Java's weakness is not the type-per-concept model — which is sound and validated by decades of use — but the exception mechanism (implicit stack unwinding, catch blocks at arbitrary distances from the throw site) that Memar rejects per RFC 000000.

Java's experience also demonstrates Dave Cheney's concern about API surface: Java APIs with many distinct exception types do become harder to evolve, as each exception type in a `throws` clause becomes part of the method's contract. However, Java's checked exception mechanism amplifies this problem by forcing callers to handle (or declare) every exception type explicitly. Memar does not use checked exceptions — its error handling is explicit-return-based (RFC 000000) — so the API-surface concern, while real, is less severe than in Java.

### Rust and Swift Error Enums

Rust and Swift use enum variants within error types, where each variant is a distinct concept. Rust optimizes for grouped failure families — the ability to say "this method can fail in one of these related ways" and handle them exhaustively in a single `match`. Memar optimizes for type-level contract identity — the ability to say "this method returns exactly this concept" in the type signature. These are different design goals, both valid for their respective frameworks.

Rust's approach deserves special attention because it is the most rigorous alternative to type-per-concept in a statically-typed language. A Rust `enum Error { NotFound, PermissionDenied, }` provides exhaustiveness checking (the compiler verifies that all variants are handled) and pattern matching (dispatching on the variant is native syntax). What it does not provide is type-level identity in method signatures: the return type is always `Result<T, Error>`, and the specific variant is a runtime value. This is analogous to Memar's rejected "enum-tagged single type" alternative — identity is in a runtime tag, not in the type itself. Rust accepts this trade-off because it values exhaustiveness checking within a grouped failure family more than it values type-level identity in individual method signatures. Memar makes the opposite choice.

### Go Sentinel Errors and `errors.Is` / `errors.As`

Go uses `errors.New("not found")` — string-based values inside a shared `error` interface. This is the pattern this RFC explicitly rejects for static capsules: identity as data, not as type.

The Go 1.13 design document (Newton et al.) explicitly lists multiple acceptable patterns for signaling identifiable errors:

> "There are other existing patterns… such as directly returning a sentinel, a specific type, or a value… with a predicate."

The document further clarifies the relationship between the two mechanisms:

> "`errors.Is` behaves like comparison to a sentinel error, and `errors.As` behaves like a type assertion."

This is a fair description of the status quo: Go provides *both* value-based and type-based identity mechanisms, treats them as equally valid, and lets the developer choose. Memar's RFC removes that choice for static capsules: the type-based mechanism is mandatory. This is a constraint, not a freedom — but it is a constraint that the framework is entitled to impose (RFC 000001) and that serves its architectural goals.

**Rob Pike's framing** of the Go position is the clearest statement of the underlying philosophy:

> "Errors are values… values can be programmed. Since errors are values, errors can be programmed."

This is a statement about *what errors are* in Go: they are values, and values are programmable. The flexibility this provides is real and deliberate. Memar's position is that for *static concepts* — concepts with no per-instance variation — this flexibility is unnecessary and the cost (loss of compile-time identity) is unacceptable.

**Russ Cox's 2024 assessment** of Go's error handling trajectory acknowledges the verbosity but defends the choice:

> "If Go had introduced specific syntactic sugar for error handling early on, few would argue… we are 15 years down the road… Go has a perfectly fine way to handle errors, even if it may seem verbose."

This is a pragmatic defense of Go's value-oriented model: it works, it is stable, and the cost of changing it now outweighs the benefit. Memar, as a new framework designing from first principles rather than evolving an existing ecosystem, does not face this constraint.

### Go Naming Conventions and Tooling

The `golangci-lint` `errname` rule enforces a naming convention that implicitly distinguishes identity-as-data from identity-as-type:

- Sentinel errors (identity-as-data): prefixed with `Err` — `ErrNotFound`, `ErrPermissionDenied`.
- Error types (identity-as-type): suffixed with `Error` — `NotFoundError`, `PermissionDeniedError`.

The `errorlint` rule flags code that can cause problems with Go 1.13's error wrapping scheme. Together, these lint rules encode community knowledge that identity-as-data and identity-as-type are *different things that require different treatment* — a distinction that the language itself does not enforce but the community has found necessary enough to automate.

Memar's position is that this distinction should be enforced by the type system, not by a lint rule that can be disabled. If identity belongs to the type system, then identity-as-data for static concepts is not a style violation to be caught by a linter — it is an architectural violation that should be structurally impossible.

### Dave Cheney on Public Error Types

Dave Cheney, one of the most respected voices on Go error handling, has cautioned against exposing concrete error types in public APIs:

> "Public error types increase surface area, new implementations must only return types specified… error type cannot be changed or deprecated without breaking compatibility."

This is a valid concern and is acknowledged in the Drawbacks section of this RFC. Cheney's advice — that clients should depend on behavior (interfaces, `Is`, `As`) rather than concrete types — is sound *within Go's value-oriented error model*, where the type system does not carry identity. In Memar's model, where the type system *does* carry identity, depending on the concrete type is not coupling to an implementation detail — it is depending on the concept itself. The type *is* the concept. Cheney's concern about "error type cannot be changed or deprecated" applies with full force: removing a static concept type is a breaking change because it removes a concept from the system's identity model. This is accepted as a deliberate consequence of the principle.

Cheney has also critiqued sentinel errors:

> "[Sentinel error] should be immutable… sentinel error values in Go… are not constants."

This observation — that Go's sentinel errors are variables, not constants, and can therefore be reassigned — is another example of the identity-as-data model's weakness. When identity is a variable, it can be accidentally or maliciously changed. When identity is a type, it cannot.

### Matt Proud on Structured vs. Opaque Errors

Matt Proud (2024) provided a clear analysis of the trade-off between structured error types and opaque errors:

**In favor of types:**

> "Structured error values… communicate a specific condition **and granular state**… in a manner that can be programmatically inspected (e.g., field access or a method) on the error type."

**Against opaque errors:**

> "Opaque errors… have no public identifier… no way to discriminate one from another — save from examining their string values, which is unsafe."

Proud's analysis aligns with this RFC's position: when identity matters (when the caller needs to discriminate between concepts), opaque errors are unsafe and structured types are necessary. This RFC extends Proud's observation from "when discrimination is needed" to "always, for static concepts," on the grounds that if a concept has no per-instance data, there is no reason *not* to make it a type.

### DoltHub Performance Analysis

DoltHub (Musgrave, 2024) published benchmark results showing the performance cost of Go's runtime error-inspection mechanisms:

> "[`errors.Is`] strategy has bad performance, at 5.5x slower than the `Bool` strategy when the value is not found, and 6x slower when it is."

These numbers demonstrate that the identity-as-data model carries a measurable runtime cost. In most I/O-bound contexts, this cost is negligible — but in tight inner loops or performance-critical paths, it is real. Type-level identity (a single type assertion) is faster because it does not require chain-walking. This performance difference is a secondary benefit of type-level identity, not a primary argument for it — but it is worth documenting as a concrete consequence.

### CedarDB Boilerplate Critique

CedarDB, a database system written in Rust, has publicly critiqued the boilerplate cost of defining many error types. Their argument is that for systems with large numbers of error conditions (hundreds in a database's case), the mechanical overhead of defining a distinct type for each — even with Rust's relatively concise enum syntax — becomes a real maintenance burden.

This critique is acknowledged. In Memar, the cost is mitigated by the code generator: error capsule types are produced mechanically from a YAML/DSL definition, and the developer authoring a new error concept writes a declarative entry, not a full type definition. The boilerplate exists in the generated output, not in the developer's input. This does not eliminate the output verbosity, but it eliminates the human effort of producing it.

For the rare case where a developer must define a static capsule by hand (e.g., before the code generator exists for a given target language), the verbosity is substantial (~20 method implementations for an Error capsule). This is accepted as a deliberate signal: the framework expects static capsules to be generated, and the manual path's weight reinforces that expectation. CedarDB's critique applies to manually-authored types in a system without code generation; it does not apply — or applies with greatly reduced force — to a system where the generator absorbs the mechanical work.

### yegor256 and Checked Exceptions Advocacy

yegor256 (Yegor Bugayenko), a prominent critic of Go's error handling, has advocated for checked exceptions as a mechanism for enforcing error contracts at the call site. While Memar does not use checked exceptions (it uses explicit error returns per RFC 000000), yegor256's underlying argument — that the compiler should enforce error handling contracts — is aligned with this RFC's position. The disagreement is about the mechanism (checked exceptions vs. explicit return types) rather than the principle (the compiler should know about error contracts).

yegor256's advocacy is relevant here because it represents a strand of opinion within the broader programming community that agrees with Memar's premise: that error handling benefits from compiler-enforced contracts, and that the Go ecosystem's value-oriented model leaves too much to runtime convention. This RFC does not adopt yegor256's specific mechanism (checked exceptions), but it shares the conviction that the type system should carry error identity.

## Unresolved questions

- **Dynamic capsule schema boundary.** Rule 3 states that different schemas SHOULD produce distinct types, but the boundary between "different schema" and "same schema with optional fields" is not always clear. A `TransactionRecord` with 12 fields and a `TransactionRecord` with 13 fields (one added in a later version) — are these the same schema or different? This judgment is left to the developer and, ultimately, to the framework's versioning RFCs when they exist. This RFC does not attempt to define a formal schema-equivalence relation.

- **Tooling enforcement strategy.** Whether and how linters, the code generator, or future domain-aware tooling should enforce Rule 1 is a tooling question deferred to a future RFC. The current assessment is that enforcement is most naturally achieved at the code generator's input layer, where the static/dynamic distinction is explicit by construction, rather than at the output source-code layer where it must be inferred heuristically.

- **The Classification Problem — formalization.** This RFC identifies the Classification Problem (determining whether a capsule is a static concept or a data carrier) as the most important open question, but does not provide a formal classification procedure. A dedicated RFC — potentially titled "How To Distinguish Concepts From Data" — is needed to define criteria, heuristics, and, where possible, mechanical checks for this determination. Until such an RFC exists, the framework relies on the developer's judgment.

- **Interaction with plugin and extension systems.** Systems requiring runtime-defined concepts (e.g., plugin architectures with third-party failure modes, or extensible permission models where new permissions are defined by plugins) need a mechanism outside this RFC's scope. Whether such systems are compatible with Memar's immutable infrastructure principle (RFC 495369) at all, or whether they require a separate concept-registry mechanism with its own RFC, is an open architectural question. The current position is that any mechanism for runtime concept registration would need to provide the same identity guarantees that the type system provides for compile-time concepts — a challenging requirement that may constrain the design space significantly.

- **`IsEmpty` / `IsNil` / `IsNull` semantics for Error capsules.** These methods are inherited from `adt_p.ADT` and may not be meaningful for static Error capsules. Whether they should return fixed values, be excluded from the Error interface, or carry Error-specific semantics, is a question for the ADT capsule family's own RFC.

## Future possibilities

- **Code generator RFC.** A dedicated RFC specifying the code generator's input format, output structure, and target-language emission strategy. That RFC will build on this RFC's principle as a foundational constraint: the generator must emit one type per static concept.

- **Cross-language compiler RFC.** A RFC specifying how capsule types are mapped between languages, relying on this RFC's guarantee that identity is type-level, enabling 1:1 type mapping.

- **"How To Distinguish Concepts From Data" RFC.** A dedicated RFC addressing the Classification Problem: formal criteria for determining whether a capsule is a static concept or a data carrier. This is the single most important follow-up to this RFC, because the Classification Problem is the primary source of ambiguity in applying the principle.

- **Extension to dynamic capsules with schema variation.** If the framework later needs a formal rule for when dynamic capsules with different schemas must be separate types (currently a SHOULD in Rule 3), a follow-up RFC could define a schema-equivalence relation and upgrade Rule 3 to a MUST where the relation is well-defined.

- **Immutable Infrastructure deep-dive (RFC 495369 expansion).** RFC 495369 is currently a placeholder recording the immutable infrastructure principle. A dedicated session is planned to define its full scope, including its relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning. The alignment between this RFC's type-system constraints and 495369's governance constraints should be explored in that session — particularly whether the two RFCs should be formally cross-referenced as mutually reinforcing or merged into a single foundational RFC.

---

## Change Rationale

| Revision | Section | Change | Reason |
|----------|---------|--------|--------|
| 4 (this) | Summary | Added Go comparison, immutable infrastructure alignment, framing as different optimization targets | User's Go philosophy analysis and RFC 495369 |
| 4 | Motivation → "The Go Ecosystem's Implicit Question" | New subsection | User insight: "Go ecosystem keeps rebuilding a type system around errors without admitting it" |
| 4 | Guide → Error Capsule | Added `Equivalence` and `IsEmpty` discussion for Error context | Open questions identified in error.go |
| 4 | Guide → "Why This Matters" | New subsection | Concrete before/after comparison showing what is lost without the principle |
| 4 | Reference → "Alignment with Immutable Infrastructure" | New subsection | User feedback: "No runtime concept creation" is not a drawback — it is aligned with RFC 495369 |
| 4 | Reference → "The Classification Problem" | New subsection | User identified this as the most important future challenge; elevated from brief mention |
| 4 | Drawbacks | Removed "No runtime concept creation" as drawback #2 | Reframed as alignment with RFC 495369, not a cost |
| 4 | Drawbacks | Added "Not idiomatic Go" and "Increased API surface" | Honest accounting informed by community research |
| 4 | Rationale → "Rejected: Go-Style Sentinel Errors" | New alternative | Explicitly addressed Go's primary pattern |
| 4 | Rationale → "Rejected: Interface-Based Predicates" | New alternative | Addressed custom `Is()` method pattern |
| 4 | Rationale → "The Memar–Go Design Target Comparison" | New subsection | User's core insight: different optimization targets, both valid |
| 4 | Prior art | Major expansion: Go naming conventions, Dave Cheney quotes, Matt Proud, DoltHub, CedarDB, yegor256, Go 1.13 design doc, Rob Pike, Russ Cox | Internet research findings |
| 4 | Unresolved questions | Added Classification Problem, plugin/extension interaction, ADT method semantics | Issues identified during research and user analysis |
| 4 | Future possibilities | Added "How To Distinguish Concepts From Data" RFC, Immutable Infrastructure deep-dive | User-identified future work |