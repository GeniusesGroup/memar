---
Title: "Encapsulation in Khayyam"
Status: Draft
Start Date: "2026-07-15"
ID: "495592"
---

# Encapsulation in Khayyam

## Abstract
This document specifies Khayyam's encapsulation model: the architectural rules governing how capsules own their state and behavior, how interaction occurs exclusively through methods, and how mutability is an intrinsic property of the capsule's own definition rather than a consumer-side keyword. The central principle is Sovereign Encapsulation — all internal fields of a capsule are strictly private, all interaction occurs via method invocation (message passing). The document also covers the rejection of tuples, closures as an inadmissible implicit-capsule syntax, primitive capsule behavioral guarantees, and the capsule-level constant model.

A capsule is an abstraction layered over `vr` (variable) and `mt` (method), not an independent primitive. Accordingly, the mechanical grammar of the method signature itself is specified in [Method in Khayyam](./method.md#method-as-callable-capsule), and the `sc` (code scope) mechanism underlying control-flow libraries is specified in [Khayyam](./khayyam.md#scope) — this document references both rather than restating them.

For a walk-through of the core mechanics before the detailed rules, see the [Guide](#capsules-and-methods-at-a-glance) below.

## Introduction

### Motivation
Languages like Rust, C++, and TypeScript split the burden of managing mutability and lifecycle safety between the definition site and the consumer site, via keywords such as `mut`/`const`. This forces the consumer to explicitly dictate how they intend to treat an instance, and lets a caller override boundaries that should fundamentally belong to the domain model — a form of syntactic band-aid for weak encapsulation, and a source of constant call-site cognitive load. Meanwhile, tuple types and generic containers allow anonymous, positional data groupings that obscure domain meaning, and public field access breaks encapsulation at the structural level.

Khayyam's encapsulation model was designed to address all of these issues simultaneously. By making all fields private, all interaction method-based, all mutability intrinsic to the capsule, and all multi-value groupings named capsules, the language ensures that domain boundaries are expressed at the definition site and cannot be bypassed at the call site. This document records those rules and explains their motivation; the alternatives that were considered and rejected are recorded in the paired changelog.

## Explanation

### Capsules and Methods at a Glance
In Khayyam, a capsule is the fundamental unit of encapsulation. It is defined with the `cp` subtype:

```khayyam
tp AppConfig cp {
    Timeout Duration
    MaxRetries W8
}
```

All fields inside a capsule are strictly private — there is no public-field syntax. Interaction with a capsule occurs exclusively through its methods, defined with the `mt` subtype:

```khayyam
tp GetTimeout mt (self AppConfig) () (timeout Duration)
tp SetTimeout mt (self AppConfig) (timeout Duration) (err Error)
```

If a capsule exposes no mutating methods, it is inherently immutable — the consumer needs no keyword to promise not to mutate it, because there is no mechanical way to do so. If a consumer needs a differently-behaving variant, that is a new capsule with a distinct identity (e.g. `MutableAppConfig` wrapping `AppConfig`), not a modifier.

A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the [Abstraction document](./abstraction.md). The polymorphic dispatch strategy is defined separately in the [Polymorphism document](./polymorphism.md).

There are no tuple types — any multi-value grouping must be a named capsule with named fields. There are no consumer-side mutability keywords (`mut`, `const`, `readonly`). All arguments to methods are passed by reference, but the capsule's internal state remains protected because all fields are hidden and mutation can only occur through explicitly exposed methods.

### Sovereign Encapsulation
A capsule is the unit that owns its state and behavior. All internal fields of a capsule are strictly private; there is no public-field syntax; interaction only occurs via method invocation (message passing). Mutability and lifecycle behavior are intrinsic properties of the capsule's own definition, never something a caller can grant or deny at the call site.

This rule is not scoped to capsules as a whole — it governs every reference to an instance, whether that reference is a local variable or a capsule's own field. A field, like a variable, is simply a name bound to an instance of a type; neither the field declaration nor the variable declaration carries behavioral semantics of its own. Asking "is this field immutable?" or "is this variable immutable?" is therefore an ill-posed question in Khayyam — the well-posed question is "does this type expose mutating methods?", answered by inspecting the referenced type's method contract, not the declaration site of the reference that points to it. This is what makes Sovereign Encapsulation a single rule rather than two: the same mechanism that keeps a capsule's fields private also determines whether an instance held by a field, or by a variable, can be mutated. There is no separate field-level or variable-level mutability system that needs to be kept consistent with the capsule-level one — they are the same system, viewed from different call sites.

A capsule's public methods are its entire contract. If a capsule exposes no mutating methods, it is inherently immutable — the consumer needs no keyword to promise not to mutate it, because there is no mechanical way to do so. If a consumer needs a differently-behaving variant of a data structure (e.g. a mutable wrapper around an otherwise immutable value), that is treated as a new business domain requirement: a new capsule with a distinct identity (e.g. `TransactionAmount` wrapping a fixed `Decimal_64_64`), not a local syntax trick like declaring `const`.

The immutability guarantee described here is a *method-contract* guarantee: a capsule exposing no mutating method cannot be mutated *through its own public interface*. It does not, by itself, resolve whether the memory a capsule's fields reference can also be mutated by some other owner of that same memory (e.g. a capsule holding a view into a buffer that a separate owner is permitted to overwrite elsewhere) — that is a distinct, lower-level memory-management concern, not addressed by this document. Whether, and how, this distinction is checked or enforced is left entirely to the compiler and/or linter layer, which may adopt a strict, Rust-`mut`-like enforcement policy; a more permissive policy that stays silent whenever an aliasing pattern is provably safe; or any other policy of its own design. This document does not mandate a specific enforcement policy — only that no *consumer-side keyword* can override a capsule's own declared behavior. The interaction between this guarantee and the underlying memory-management model is substantial and is deliberately deferred to future documents on memory management and buffer/storage ownership.

Every behavioral variant of a value (e.g. a frequently-needed mutable view of an otherwise-immutable type) requires defining and naming a new capsule, rather than a one-character keyword at the call site. This is intentional friction (consistent with the broader design philosophy that prefers explicit domain modeling over syntactic shortcuts), but it does mean more named types exist in a codebase than in languages with consumer-side modifiers.

**Representation exposure is not resolvable by any enforcement policy, and this document does not claim otherwise.** If a capsule's own method surface returns a reference to a sub-capsule that itself exposes mutating methods (e.g. a `Tcp` capsule offering `ReceiveBuffer() Buffer`, where `Buffer` has its own `Overwrite` method), any caller holding that returned `Buffer` can mutate it through `Buffer`'s own, entirely legitimate contract — outside `Tcp`'s knowledge or control. Nothing here is hidden or type-unsound: `Buffer`'s mutating methods are declared honestly, and `Tcp` chose to return a `Buffer` rather than a narrower, read-only abstraction over it. This is the same failure mode long documented in object-oriented languages as "representation exposure" (returning a mutable reference to internal state defeats encapsulation regardless of how strict the language's field-privacy rules are) — see e.g. the "defensive copying" guidance in *Effective Java*. No amount of compiler or linter policy can distinguish this from a legitimate, intended API, because it is one: whether to return a narrower abstraction (e.g. a read-only `Buffer` view exposing no mutating method) instead of the full `Buffer` capsule is entirely the capsule author's own design discipline, not something Sovereign Encapsulation can enforce from outside. The same applies, more sharply, if a capsule's own field type happens to expose an `unsafe`-style direct-memory-access method: any consumer holding an instance of that field type can mutate the backing memory without the owning capsule ever being called. Sovereign Encapsulation guarantees that *no consumer-side keyword* can force mutation against a type's contract; it does not and cannot guarantee that every capsule author has designed a narrow-enough contract to prevent transitive exposure through capsules they chose to return or expose.

Reference-rebinding — reassigning a variable or field's name to point at a different instance, as distinct from mutating the instance it already points to — is not a gap in this document, at either level. Khayyam has no primitive types; every variable's or field's declared type is itself a capsule or an abstraction. Obtaining a *new* instance to rebind to (whether for a local variable or a field) still requires going through that type's own constructor or an explicit copy/clone abstraction it chooses to implement (see `variable.md`'s Domain-Driven Arithmetic) — there is no ambient, type-independent way to conjure a value. And for a local variable specifically, rebinding touches no capsule's private state at all (it is not privately-owned state of anything), so no Sovereign Encapsulation invariant is even at stake; for a field, rebinding *is* mutation, gated by the same privacy rule already described above. Nothing is left open here.

### Capsule Structure and Privacy
A capsule is declared with the `cp` subtype under the `tp` keyword:

```khayyam
tp {name} cp { ___ }
```

Each field in a capsule is written as `fieldName fieldType` on its own line. Fields are always private — there is no visibility modifier, no `public`/`private` keyword, and no way to expose a field directly. The only way to read or modify a capsule's internal state is through methods attached to that capsule.

This absolute privacy rule is not a default that can be overridden; it is a structural guarantee of the language. A capsule author cannot accidentally expose a field, and a consumer cannot access a field even if the author intended to expose it through some other mechanism. All access must go through methods, making the capsule's public interface its complete and only contract.

A capsule structure can include other data types inside itself, allowing composition:

```khayyam
tp ServerConfig cp {
    Host String
    Port W16
    Timeout Duration
    TLSConfig TLSConfig
}
```

The `TLSConfig` field is itself a capsule, composed within `ServerConfig`. Access to `TLSConfig`'s internal data must go through `TLSConfig`'s own methods — `ServerConfig` does not gain special access to `TLSConfig`'s fields by virtue of containing it.

Even trivial read access to a field (e.g., getting a configuration value) requires a method definition. For capsules with many fields, this can result in a large number of getter-style methods. However, these methods serve a critical purpose: they define the capsule's behavioral contract, and they can be evolved independently of the internal representation without breaking consumers.

### Closures as Implicit Capsule Syntax
A closure, looked at structurally rather than syntactically, is not really a separate language feature — it is an implicit capsule. Whatever a closure captures is, in effect, a set of unnamed fields; whatever a closure runs when called is, in effect, an unnamed method attached to those fields. Every closure written in another language is already doing what a Khayyam capsule does — holding state and offering behavior over it — the only difference is that it does so anonymously, without a declared type, and without going through Sovereign Encapsulation's requirement that a capsule's state be named and explicit.

Seen this way, Khayyam does not need a standalone rule that singles out and forbids closures. It only needs to decline adding syntax for a capsule that is allowed to skip naming its own fields. If a behavior needs state (the kind of thing a closure would capture), that state is, by definition, a new domain entity with a name — so a developer defines a specific capsule for it, explicitly passes the required state in, and implements the necessary method, exactly as for any other capsule. There is no closure or lambda syntax in the grammar; any callback-shaped requirement is expressed as a named capsule implementing the relevant abstraction (e.g. a comparator capsule implementing a `Compare` method), referenced by name like any other type.

This framing also clarifies why this topic belongs inside the encapsulation document rather than standing alone: it is not an independent restriction sitting beside Sovereign Encapsulation — it *is* Sovereign Encapsulation, applied to the one syntactic form (an inline, capturing function) that would otherwise let a capsule's state stay implicit and unnamed.

Declining to admit this implicit-capsule syntax into the grammar has real consequences worth naming plainly. Closures are heavily used in other languages for callbacks and inline dynamic logic (e.g. capturing variables for sorting or filtering), and their convenience carries real architectural costs: hidden state capturing creates invisible dependencies and breaks explicit state management, and the ease of writing inline functions encourages developers to mash multiple distinct behaviors into a single method body under the false promise of "refactoring later." Requiring every captured state to surface as a named capsule keeps all state dependencies explicit, testable, strictly encapsulated, and analyzable by the compiler.

**Reduced Optimization Surface:** capsule-centric code, where state is always a named, explicit type, is significantly easier for the compiler to analyze and optimize than ad-hoc captured scopes. Both models are theoretically equivalent in the worst case, but capsule-based state is far more consistently optimizable in practice, because the compiler always has a concrete, named type to reason about rather than an implicit closure environment whose shape varies by call site. (An earlier, now-corrected version of this rationale argued closures cause additional heap allocation/escape compared to capsules — this is not accurate: a named capsule holding the same captured references has the same memory-lifetime profile as a closure would. The real justification is architectural explicitness and analyzability, not raw performance.)

The discomfort and verbosity of having to name a capsule for even small, single-use behaviors (e.g. a one-off sort comparator) is a real and acknowledged cost. There is a recognized risk that a developer could recreate the same laziness this rule is meant to prevent by writing a throwaway, badly-named, single-use capsule instead of a proper closure — this is treated as a naming-convention/linter concern (see future linter documents), not a reason to reconsider this decision.

### Relationship with Abstractions
A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the [Abstraction document](./abstraction.md). This document concerns itself only with the encapsulation guarantees that make the abstraction model possible: capsules hide all internal state, and all interaction occurs through methods whose signatures the abstraction defines.

### Tuples Rejection
Khayyam has no tuple type or tuple literal syntax (`(a, b, c)` as an anonymous, positional, multi-value type). Any time a developer needs to group multiple values together, that grouping must be a named capsule with named fields, exactly like any other domain type.

Where another language might return `(string, int, error)` from a function, a Khayyam developer instead defines or reuses a named capsule with named fields appropriate to the domain (e.g. a `ParseResult` capsule with named `Value`, `Length`, and `Err` fields/methods), exactly as they would for any other piece of domain data.

There is no tuple literal or tuple type syntax in the grammar. Multiple related values are always grouped via an explicitly named capsule.

Tuples are rejected not because they lack behavior at the point of definition — a `(String, Int)` pair may appear harmless in isolation — but because they facilitate a wrong architectural evolution path. Over time, what begins as an anonymous positional grouping inevitably accumulates associated behavior (validation, formatting, conversion) that becomes scattered across the codebase rather than co-located with the data it concerns. This is the same trajectory that leads from anonymous data bags to anemic domain models. By requiring multi-value concepts to be represented as named types when they have semantic meaning, Khayyam ensures that domain identity is established from the outset and that behavior has a natural home.

Even a trivial, throwaway pairing of two values (e.g. swapping two variables, or returning a quick coordinate pair) requires naming and defining a capsule, rather than using an anonymous, lightweight tuple literal — measurably more ceremony than virtually every modern language provides for this common case.

### Primitive Capsule Specification
The canonical Khayyam specification claims that replacing `int32` with `W32` is "zero-cost." But `W32` is not just a renamed integer — it is a capsule that provides behavioral guarantees beyond what `int32` offers. The migration contract depends on what exactly `W32` guarantees.

Possible behavioral guarantees for primitive capsules include:
- **Overflow behavior**: wrapping vs. panic vs. saturating. A `W32` (whole 32-bit) capsule likely wraps on overflow, while a different capsule might panic or saturate. The distinction is domain-meaningful, not just a compiler flag.
- **Bit-width enforcement**: no implicit widening or narrowing. A `W32` stays a `W32`; the developer must explicitly convert to a different width through a capsule method.
- **Serialization contract**: predictable binary layout. A `W32` guarantees a specific byte order and alignment, making it safe for network transmission and file storage without additional serialization logic.
- **Range semantics**: if used as an index, bounds checking may be enforced by the capsule's methods rather than by the language runtime.

The answer matters because it defines the migration contract. If `W32` only provides renaming, the "zero-cost" claim is trivial. If it provides behavioral guarantees, the migration is more complex but the value is real — the capsule enforces invariants that a raw `int32` cannot.

This topic is also relevant to whether primitive capsules should be defined by the language itself, by the standard library, or by the Memar framework. Each choice has different implications for portability (can a `W32` be used without the Memar framework?), governance (who decides what behavioral guarantees a primitive capsule provides?), and consistency (do all primitive capsules follow the same specification pattern?).

None of the possible behavioral guarantees listed above create an exception to Sovereign Encapsulation's "all interaction occurs through methods" rule, and none are guaranteed by this document — they are illustrative ("possible"), not mandatory. Whether a given primitive capsule's methods happen to be trivial enough for the compiler to inline is a backend optimization decision, orthogonal to the interaction model: the operation still goes through a method either way. A capsule author is free to design a `W32`-like capsule whose methods are cheap and unchecked (accepting the same risk profile as a raw primitive type in another language) or one whose methods are heavier and safer (e.g. checked arithmetic); the tradeoff, and the cost it implies, is local to that capsule's own design, not a language-level default. This is also why "zero-cost" cannot be asserted for `W32` as a category — it depends entirely on which behavioral guarantees the specific `W32` a project uses chooses to implement.

Defining behavioral guarantees for primitive capsules adds complexity to the "de-Primitive-ing" migration story. A developer replacing `int32` with `W32` must now understand that `W32` is not a drop-in replacement but a capsule with specific behavioral contracts that may differ from the raw integer semantics they expect.

### Constants as Capsule-Returned Values
A constant in Khayyam is simply a variable returned by a capsule method that cannot change after first initialization — an organizational and architectural rule, not a dedicated compiler keyword. Two flavors are distinguished:

- **Static constants**: compile-time declared and initialized, usually inlined directly at compile time. Conceptually equivalent to "a function that runs entirely at compile time and returns the value living in that function's body."
- **Dynamically-valued constants**: compile-time declared, but runtime-initialized. These require a runtime memory-service call to obtain their value since they cannot be inlined.

A "config" capsule for a module, for example, exposes module-level values through methods. Some of those methods may allow controlled, intentional changes to specific values; others guarantee a value never changes once initialized. Both cases are ordinary capsule methods — there is no separate `const`-flavored declaration syntax.

This approach is consistent with Sovereign Encapsulation: the "this value never changes" guarantee depends on the capsule author's discipline (not exposing a mutating method) rather than being enforced by a keyword, and the consumer discovers the guarantee through the capsule's public interface, not through a modifier on the variable declaration.

Without a dedicated keyword, the "this value never changes" guarantee for a constant depends entirely on the capsule author's discipline (not exposing a mutating method) rather than being enforced by a single, unmistakable declaration keyword a reader can immediately recognize.

### Naming Conventions
Suggested conventions for capsule and abstraction names (non-binding, enforceable via linter configuration):

- **Capsule names**: PascalCase, domain-meaningful (e.g., `AppConfig`, `UserRegistry`, `ConnectionIndex`). Avoid generic names like `Manager`, `Handler`, `Helper` — these indicate missing domain specificity.
- **Abstraction names**: PascalCase, domain-concept framing (e.g., `Reader`, `Writer`, `Repository`). Avoid technical-capability framing (e.g., `Readable`, `Writable`, `Filterable`) — these indicate over-abstraction risk.
- **Method names**: PascalCase for public methods, matching the capsule's domain language. Avoid getter/setter prefixes (`Get...`, `Set...`) when the method name can express the domain action more directly (e.g., `ApplyTimeout` instead of `SetTimeout`).
- **Field names**: PascalCase inside capsules, consistent with the type naming convention. Since fields are always private, their names are an internal design decision of the capsule author.
