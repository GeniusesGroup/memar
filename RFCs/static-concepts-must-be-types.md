---
RFC Number: 495421
Title: "Static Concepts Must Be Types"
Status: Proposed
Start Date: 2026-07-08
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000000", "000001"]
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Original design decision, years of production validation in memar-go, core principle formulation, Go philosophy analysis, classification problem identification"
    task: []
  - name: "Super Z"
    uri: "https://chat.z.ai/"
    model: "GLM"
    effort: ""
    contribution: "Drafted RFC, web research, documented trade-offs, incorporated community objections"
    task: []
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: "RFC review and architectural refinement"
    contribution: "Web research, reframed rationale around Concept vs Data, generalized rule beyond Error capsules, clarified MUST/SHOULD criteria"
    task: []
---

## Summary
Identity belongs to the type system. In the Memar framework, the answer to "which concept is this?" MUST be determinable from the type alone, at compile time, without inspecting any runtime data. A static capsule — one with no per-instance dynamic data — MUST therefore be its own distinct type. A capsule whose instances share the same schema and differ only in values may use a shared type. A capsule whose instances have different data schemas SHOULD use distinct types. The Error capsule family is the primary motivating example, but the principle applies to any capsule in the framework.

This RFC was developed through extensive discussion, web research, and critical review of alternative approaches — particularly Go's "errors are values" philosophy, which represents the most prominent counter-position in the industry. The principle itself withstood critical scrutiny; the primary open challenge is not the principle but its classification boundary: determining what qualifies as a "static concept" in practice. A companion RFC addressing that classification question is anticipated as the natural next step.

## Motivation

### The Core Question
Consider two approaches to representing a distinct concept such as "transaction unavailable":

1. **The concept is the type.** `ErrTransactionUnavailable` is its own type. The type *is* the concept. No data is needed to distinguish it from `ErrInsufficientFunds` — the type system does that.

2. **The concept is data.** A single `GenericError` type holds a `name` field set to `"ErrTransactionUnavailable"`. The concept "transaction unavailable" is represented by a string stored in memory at runtime, not by the type itself.

Both approaches produce a working program. The difference is not in correctness but in **what role the type system plays**. The first approach assigns the type system its strongest possible responsibility: answering "what is this?" The second approach reduces the type system to a container and delegates identity to data — the same kind of data that holds quantities, timestamps, and configuration values.

This RFC establishes that the first approach is not merely preferred but mandatory for static capsules, because in the Memar framework's architectural model, identity is the type system's job, and data is for variation between instances of the same concept — not for distinguishing one concept from another.

### Why This Is Not Obvious
Most programming languages and frameworks do not make this distinction explicitly. Go uses `errors.New("not found")` — a string value inside a shared interface type. Python uses exception classes, which are closer to the principle, but the culture mixes class-based and string-based patterns freely. JavaScript uses string codes or custom error subclasses — again, mixed. The industry has no consensus on whether identity belongs to the type system or to data, and the absence of a deliberate decision is what produces the inconsistency this RFC resolves.

This absence of consensus is not because the question has been analyzed and settled. It is because most languages and frameworks have never explicitly asked it. Go, for example, made a deliberate trade-off favoring flexibility over type-level identity — but did not frame it as a decision about identity at all. The question "should identity live in the type system?" is architectural, and it requires an architectural authority to pose it. RFC 000001 establishes that the framework is that authority for Memar. This RFC exercises that authority to answer the question.

### Why This Matters Now
The code generator and cross-language compiler planned for the Memar SDK must emit capsule definitions into multiple target languages (Go, JavaScript, and potentially others). The chosen representation determines the generator's output structure, the compiler's type-mapping strategy, and the ergonomics of the generated code for SDK consumers. This decision must be settled before either tool is built, because the generator's output format and the compiler's type-mapping logic both depend on whether each concept is a distinct type or a value inside a shared container.

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

### Beyond Errors: Other Static Capsule Families

The same reasoning applies to any capsule family whose members are static concepts — where identity is the point, not data. Examples include:

- **Capability identifiers**: `CapabilityRead`, `CapabilityWrite`, `CapabilityAdmin` — each is a distinct permission concept, not a data container.
- **Status codes**: `StatusActive`, `StatusSuspended`, `StatusArchived` — each represents a distinct lifecycle state.
- **Permission descriptors**: `PermissionViewProfile`, `PermissionEditProfile`, `PermissionDeleteAccount` — each is a distinct authorization concept.

In each case, the capsule has no per-instance variation. By Rule 1, each MUST be its own type. If any of these families later acquire per-instance data (e.g., a permission with a scope parameter), that specific capsule graduates from a static concept to a data carrier, and Rule 2 applies instead — but the static members of the family remain distinct types.

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

### Suggested Naming Conventions

For error capsules, the convention `Err` + `PascalCase description` is already in use (e.g. `ErrTransactionUnavailable`, `ErrInsufficientFunds`). This RFC records it as a suggested default for that capsule family.

This is a non-binding convention: enforcement, if any, is a per-organization Linter configuration choice, not a language-level requirement. Other static capsule families may follow their own domain-appropriate naming conventions.

## Drawbacks

1. **Type proliferation and API surface.** A system with many static concepts will contain many distinct type definitions. This increases the API surface area of each package — a concern that Dave Cheney has articulated in the context of Go: *"Public error types increase surface area... new implementations must only return types specified... error type cannot be changed or deprecated..."* (Cheney, "Error handling in Upspin"). Each new static concept adds a type that becomes part of the package's public contract, and evolving or removing that contract has downstream consequences. This cost is real and acknowledged. In Memar, it is mitigated by two factors: (a) the code generator bears the mechanical cost of producing types, not developers; (b) the framework's error model (RFC 000010) explicitly separates internal diagnostic detail from external contracts, so the public API surface of error types carries only what the caller needs — layer-appropriate, minimal, and stable by design.

2. **No runtime concept creation.** Static concepts cannot be created dynamically from configuration files, plugin descriptors, or database records. Every concept must be defined at compile time. This is a deliberate consequence: if identity belongs to the type system, then concepts that do not exist as types do not exist in the system's identity model. Systems requiring runtime-defined concepts (e.g., plugin architectures with third-party failure modes not known to the core system at compile time) need a separate mechanism outside this RFC's scope.

3. **Conceptual shift for developers.** Developers accustomed to thinking of errors (or status codes, or identifiers) as values — strings, constants, or tagged union variants — must adjust to thinking of them as types. This is not merely a syntactic change but a shift in what the type system is expected to do. The framework's philosophy (RFC 000001) provides the foundation for this shift, but adoption friction is real and acknowledged. The manual path for defining static capsules involves substantial boilerplate (~20 method implementations for an Error capsule), which reinforces the expectation that the code generator should be used.

4. **Navigation and discovery.** A large system with hundreds of static concept types may challenge codebase navigation. Developers searching for "what errors can this method return?" must consult the method signature (which, thanks to covariant returns, tells them exactly) rather than scanning for sentinel variable declarations. IDE support and generated documentation mitigate this, but it remains a practical concern for codebase exploration.

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

### Addressed Objections from Industry Review

The following objections were identified through web research and community discussion. Each is addressed here to document why it does not overturn the RFC's principle.

**"Error types bloat APIs and increase coupling."**

Dave Cheney warns: *"Public error types increase surface area... error type cannot be changed or deprecated without breaking compatibility."* This is a valid concern about API evolution, and it is acknowledged in Drawback #1. However, the concern assumes that exposing concrete error types as part of a public API is inherently risky. In Memar, this risk is architecturally bounded: errors are contracts to the immediate caller (RFC 000010), and the boundary translation discipline ensures that internal implementation details never leak into external error types. The coupling that Cheney warns about — callers depending on internal implementation details exposed through error types — is precisely what the separation of Error from Log (RFC 000010) prevents. Additionally, the code generator produces error types from a declarative specification, making versioning and deprecation a specification-level concern rather than a code-level one.

**"Go chose value-based errors deliberately — isn't that evidence against this approach?"**

Go's "errors are values" philosophy (Pike, 2015) is a conscious trade-off favoring flexibility and simplicity over type-level identity. This RFC does not claim that Go's designers were ignorant of the trade-off. They were not. The disagreement is about the **optimization target**:

| Memar | Go |
|-------|-----|
| Architectural identity | Simplicity |
| Strong contracts | Low cognitive load |
| Domain modeling | Practical programming |
| Type-level meaning | Value-level meaning |

Go's ecosystem largely serves networked services where errors are serialized to JSON or HTTP status codes and sent across process boundaries. In that context, type-level identity is lost during serialization regardless of how the error is represented internally — so investing in type-level identity provides diminishing returns. Memar's SDK use case is different: errors must retain their identity across language boundaries through type-preserving compilation (Go → JavaScript), not through serialization. The two frameworks optimize for different contexts, and both trade-offs are rational within their respective contexts.

That said, the evolutionary trajectory of Go's own error handling is instructive. Go started with direct comparison (`if err == ErrNotFound`), then added `errors.Is()` for wrapped errors, then `errors.As()` for type-based inspection, then `errors.Join()` for combining multiple errors. Each addition provides a mechanism that type-level identity would have provided natively. As one critic observed: *"The ecosystem keeps rebuilding a type system around errors without admitting it."* This is an overstatement — Go's tools are value-based, not type-based — but the direction of travel (more structured, more inspectable, more identity-preserving) suggests that the absence of type-level identity creates pressure that the ecosystem then expends effort to compensate for.

**"Performance: sentinel checks are faster than type checks or errors.Is()."**

Benchmarks from DoltHub (Musgrave, 2024) show that `errors.Is()` can be 5.5–6× slower than a simple boolean check when an error is not found. This is a real performance cost — but it is a cost of Go's specific value-based comparison mechanism (recursive tree walking through wrapped error chains), not a cost of type-based identity itself. A type assertion (`err.(*MyErrorType)`) in Go is a direct, fast operation — it does not walk chains or compare strings. In Memar, where identity is in the type, the equivalent check is a native type check (compile-time in signatures, `instanceof` in JavaScript, type assertion in Go), which carries no such overhead. The performance argument against value-based identity actually *supports* type-based identity.

**"No one stops you from defining error types today — why make it mandatory?"**

The Go 1.13 design document (Newton et al.) explicitly lists multiple acceptable patterns for signaling identifiable errors: sentinel variables, custom types, or predicate functions. This permissive approach is appropriate for Go, which targets a broad community with diverse needs. Memar targets a specific architectural vision with specific tooling (code generator, cross-language compiler, linter). In that context, allowing a mix of representations creates inconsistency that propagates into every tool. The mandatory rule exists because the tools need a reliable invariant to build on — not because individual developers are incapable of making the right choice on a case-by-case basis.

**"Exceptions (CedarDB argument) are better than error values for system-level errors."**

CedarDB's Philipp Fent (2024) argues that exceptions provide better error handling for server-side systems: less boilerplate (CockroachDB has ~24,570 `if err != nil` patterns vs. CedarDB's ~140 catch blocks), automatic resource cleanup through stack unwinding, and better handling of system-level failures (OOM, integer overflow, stack overflow). This is a legitimate argument for *exceptions as a control flow mechanism* — a separate question from the one this RFC addresses. Memar already rejects exceptions (RFC 000000) for the same reason Rust does: implicit control flow. The CedarDB argument does not address whether identity should be in the type system or in data; it addresses whether error propagation should be explicit (return values) or implicit (exceptions). These are independent design axes.

### Impact of Not Doing This

Without a deliberate, documented decision, the question of "distinct type or generic?" will be answered inconsistently across the codebase and across language bindings. Some concepts will be types, others will be data, and the resulting inconsistency will propagate into every tool that consumes capsule definitions. The type system's role in the framework will be unclear — sometimes it carries identity, sometimes it doesn't — and developers will make the choice based on convenience rather than principle. This RFC settles the question by stating the principle that resolves it: identity is the type system's responsibility.

## Prior art

### Java Exception Classes

Java assigns each error concept its own class extending `Exception` or `RuntimeException`. This is the closest mainstream prior art to this RFC's principle: identity is carried by the type, and callers use type-based dispatch (`catch (SpecificException e)`) to react to specific error concepts. Java's weakness is not the type-per-concept model — which is sound and validated by decades of use — but the exception mechanism (implicit stack unwinding, catch blocks at arbitrary distances from the throw site) that Memar rejects per RFC 000000. Yegor Bugayenko (2015) argues that Java's checked exceptions were the correct idea and that unchecked exceptions were the mistake — a position that aligns with this RFC's stance that the compiler should enforce error handling, though Memar achieves this through linter enforcement rather than language-level syntax.

### Rust and Swift Error Enums

Rust and Swift use enum variants within error types, where each variant is a distinct concept. Rust optimizes for grouped failure families — the ability to say "this method can fail in one of these related ways" and handle them exhaustively in a single `match`. Memar optimizes for type-level contract identity — the ability to say "this method returns exactly this concept" in the type signature. These are different design goals, both valid for their respective frameworks. Rust's approach provides namespace grouping (all transaction errors under `TransactionError::`) at the cost of preventing a method from expressing "I return exactly this one error" in its signature. Memar's approach provides that precision at the cost of losing the grouping — a trade-off that is acceptable because Memar's domain-based naming conventions (e.g., all errors in `memar/finance/errors/`) provide the grouping through file organization rather than through the type system.

### Go: "Errors Are Values"

Go's error handling is the most important counter-example to examine, because it represents the strongest and most deliberate alternative to type-based identity.

**The philosophy.** Rob Pike (2015) established the foundational principle: *"Errors are values... values can be programmed. Since errors are values, errors can be programmed."* This philosophy treats errors as ordinary data — storable, wrappable, inspectable, and serializable. The Go standard library and the broader ecosystem have built extensive tooling around this principle: `errors.New()`, `fmt.Errorf("...: %w", err)` for wrapping, `errors.Is()` and `errors.As()` for inspection, and `errors.Join()` for combining multiple errors.

**The evolution.** Go's error handling has evolved significantly, and the direction of evolution is revealing:

1. **Go 1.0 (2012):** Direct comparison — `if err == ErrNotFound`. Sentinel errors are package-level variables of type `*errors.errorString`. Identity is a pointer comparison, but only works for unwrapped errors.

2. **Go 1.13 (2019):** Error wrapping — `fmt.Errorf("...: %w", err)` creates a wrapped error chain. `errors.Is()` and `errors.As()` walk the chain to find matches. The Go 1.13 design document (Newton et al.) explicitly acknowledges multiple valid patterns: sentinel variables, custom types, and predicate functions. The design notes: *"Whether you wrap or not... wrapping an error makes that error part of your API. If you don't want to commit to supporting that error... you shouldn't wrap the error."*

3. **Go 1.20 (2023):** Multi-error support — `errors.Join()` combines multiple errors into one. `errors.Is()` and `errors.As()` automatically unwrap joined errors.

4. **Community tooling:** `golangci-lint` enforces naming conventions — sentinel errors must be prefixed with `Err` (e.g., `ErrNotFound`), struct-based error types must be suffixed with `Error` (e.g., `PathError`). The `errorlint` rule flags code that interacts poorly with the wrapping scheme. These conventions exist to compensate for the absence of type-level identity: without distinct types, naming conventions become the primary mechanism for communicating "this is a distinct error concept."

**The performance cost.** DoltHub (Musgrave, 2024) benchmarked Go error comparison approaches and found that `errors.Is()` is 5.5–6× slower than a boolean return when an error is not found, because it must walk the wrapped error chain recursively. Direct pointer comparison on unwrapped sentinels is fast, but wrapping — which is the recommended practice for adding context — introduces the overhead. This is a direct consequence of identity being stored as data (strings, wrapped chains) rather than as type: the system must inspect data at runtime to answer a question that the type system could have answered for free at compile time.

**What Go got right.** Go's error handling provides genuine flexibility that a rigid type system can inhibit. Errors can be enriched with context as they propagate: a low-level `os.PathError` can be wrapped with "failed to load config" and then wrapped again with "failed to initialize service," creating a rich diagnostic chain. A static type with no per-instance data cannot do this — but Memar addresses this through the Log system (RFC 000010), not through the Error capsule. The diagnostic chain is a log event, not an error contract. Go conflates the two; Memar separates them.

**What Go's evolution reveals.** Each iteration of Go's error handling adds more structure, more inspectability, and more identity-preserving mechanisms. The ecosystem has built, through library code and tooling, much of what a type system would have provided natively. This does not mean Go's approach is wrong — it means that the absence of type-level identity creates pressure that the community expends effort to compensate for. In a framework that controls its own language, tooling, and code generator, that compensation effort can be invested in the type system itself.

### CedarDB: Exceptions for System Reliability

CedarDB (Fent, 2024) advocates for C++ exceptions over error return values in database systems, arguing: (a) 100× less error-handling code than Go's approach (140 catch blocks vs. CockroachDB's ~24,570 `if err != nil` patterns); (b) automatic resource cleanup through stack unwinding with RAII; (c) better handling of system-level failures (OOM, SIGFPE) that Go's error values cannot represent. The performance argument is notable: CedarDB's benchmark shows C++ exceptions are ~4× faster than Rust's `Result` type for their workload.

CedarDB's argument is about **control flow mechanism** (exceptions vs. return values), not about **identity representation** (types vs. data). Memar already rejects exceptions (RFC 000000) for the same reason Rust does. However, CedarDB raises a valid point that is relevant here: system-level failures (OOM, integer overflow, stack overflow) are errors that carry **runtime context** — they are not static concepts. In Memar's model, these are Log events (RFC 000010), not Error capsules. The framework's separation of Error from Log means that system-level failures are handled by the observability system, not by the error contract system — a cleaner separation than either Go's (which has no mechanism for these at all) or CedarDB's (which uses exceptions for everything).

## Unresolved questions

- **The Classification Problem: what qualifies as a "static concept"?.** This is the most significant open question identified during the review of this RFC. The principle itself — "identity belongs to the type system" — withstood critical scrutiny. No argument was found that fundamentally undermines it. However, applying the principle requires determining whether a given capsule is a "static concept" (and therefore subject to Rule 1) or a "data carrier" (subject to Rule 2). Some cases are clear: `ErrPermissionDenied` is universally recognizable as a static concept. Other cases are domain-dependent: `CustomerTypeGold` might be a static concept in one domain (a fixed enumeration of customer tiers) and a data carrier in another (a user-configurable label with associated metadata). A companion RFC — potentially titled "How To Distinguish Concepts From Data" — is anticipated as the natural next step. That RFC would need to provide classification heuristics, decision criteria, and examples that help developers make this determination consistently. The stability of this RFC's principle depends more on the clarity of that classification than on the principle itself.

- **Dynamic capsule schema boundary.** Rule 3 states that different schemas SHOULD produce distinct types, but the boundary between "different schema" and "same schema with optional fields" is not always clear. A `TransactionRecord` with 12 fields and a `TransactionRecord` with 13 fields (one added in a later version) — are these the same schema or different? This judgment is left to the developer and, ultimately, to the framework's versioning RFCs when they exist. This RFC does not attempt to define a formal schema-equivalence relation.

- **Tooling enforcement strategy.** Whether and how linters, the code generator, or future domain-aware tooling should enforce Rule 1 is a tooling question deferred to a future RFC. The current assessment is that enforcement is most naturally achieved at the code generator's input layer, where the static/dynamic distinction is explicit by construction, rather than at the output source-code layer where it must be inferred heuristically.

## Future possibilities

- **"How To Distinguish Concepts From Data" RFC.** A companion RFC providing classification heuristics, decision criteria, and worked examples for determining whether a given capsule is a static concept or a data carrier. This is the most impactful follow-up, as the Classification Problem (see Unresolved questions) is the primary practical risk to consistent application of this RFC's principle.

- **Code generator RFC.** A dedicated RFC specifying the code generator's input format, output structure, and target-language emission strategy. That RFC will build on this RFC's principle as a foundational constraint: the generator must emit one type per static concept.

- **Cross-language compiler RFC.** A RFC specifying how capsule types are mapped between languages, relying on this RFC's guarantee that identity is type-level, enabling 1:1 type mapping.

- **Extension to dynamic capsules with schema variation.** If the framework later needs a formal rule for when dynamic capsules with different schemas must be separate types (currently a SHOULD in Rule 3), a follow-up RFC could define a schema-equivalence relation and upgrade Rule 3 to a MUST where the relation is well-defined.