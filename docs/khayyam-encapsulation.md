---
Title: "Encapsulation in Khayyam"
Status: Draft
Start Date: "2026-07-15"
ID: "495592"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification defines capsule, method, and abstraction syntax that this document elaborates and motivates."
    - Title: "Khayyam Design Philosophy"
      URI: "./khayyam-design_philosophy.md"
      Relation: "Reference"
      Reason: "The philosophy document records the recurring principles (behavior over type identity, domain modeling, syntactic atomicity) that underpin the encapsulation design decisions recorded here."
    - Title: "Abstraction in Khayyam"
      URI: "./khayyam-abstraction.md"
      Relation: "Reference"
      Reason: "The abstraction mechanism is specified separately. This document records the encapsulation guarantees (capsules hide all internal state, all interaction occurs through methods) that make the abstraction model possible."
    - Title: "Polymorphism in Khayyam"
      URI: "./khayyam-polymorphism.md"
      Relation: "Reference"
      Reason: "Polymorphism classification and dispatch strategy are specified separately. This document defines the capsule-level boundaries that constrain polymorphic behavior."
    - Title: "Method in Khayyam"
      URI: "./khayyam-method.md"
      Relation: "Reference"
      Reason: "Method as Callable Capsule — the mechanical spec of the method signature itself (pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods) — previously lived in this document's Explanation section and has moved there, since a capsule is an abstraction over `vr`/`mt`, not the other way around. This document now depends on that spec rather than restating it."
    - Title: "Logic in Khayyam"
      URI: "./khayyam-logic.md"
      Relation: "Reference"
      Reason: "The Code Scope (`sc`) topic previously lived in this document's Explanation section and has moved there, since code scopes are structurally the mechanism control-flow libraries (IF/ELSE/LOOP) are built on, not a capsule-level concern."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions", "Sovereign Encapsulation concept", "Defined the capsule structure, method model, and the elimination of consumer-side mutability keywords in the canonical Khayyam specification."]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Works: ["Critical review"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Works: ["Restructuring into document template", "Content consolidation and enrichment", "Restructured scattered encapsulation-related content into the canonical document template; consolidated content from staging and specification files; added reference-level elaborations on capsule structure, method dispatch, abstraction design, and primitive capsule specification."]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium"
    Tasks:
      - Works: ["Migrated document structure to the current Explanation-facet specification (Abstract / Introduction / Explanation / Results / Discussion / Change Rationale)", "Merged the standalone Absence of Closures and Anonymous Functions document into the Explanation section as a topic following Method as Callable Capsule, preserving all original content", "Extracted Method as Callable Capsule to khayyam-method.md and Code Scope to khayyam-logic.md, since capsule is an abstraction over vr/mt rather than the reverse", "Reframed Absence of Closures and Anonymous Functions from a negative (\"we don't support X\") framing to a positive one (closures as an implicit-capsule syntax we chose not to admit, and why)"]
        URI: ""
---

# Encapsulation in Khayyam

## Abstract
This document specifies Khayyam's encapsulation model: the architectural rules governing how capsules own their state and behavior, how interaction occurs exclusively through methods, and how mutability is an intrinsic property of the capsule's own definition rather than a consumer-side keyword. The central principle is Sovereign Encapsulation — all internal fields of a capsule are strictly private, all interaction occurs via method invocation (message passing). The document also covers the rejection of tuples, closures as an inadmissible implicit-capsule syntax, primitive capsule behavioral guarantees, and the capsule-level constant model.

A capsule is an abstraction layered over `vr` (variable) and `mt` (method), not an independent primitive. Accordingly, the mechanical grammar of the method signature itself is specified in [Method in Khayyam](./khayyam-method.md#method-as-callable-capsule), and the `sc` (code scope) mechanism underlying control-flow libraries is specified in [Logic in Khayyam](./khayyam-logic.md#code-scope) — this document references both rather than restating them.

For a walk-through of the core mechanics before the detailed rules, see the [Guide](#capsules-and-methods-at-a-glance) below.

## Introduction

### Motivation
Languages like Rust, C++, and TypeScript split the burden of managing mutability and lifecycle safety between the definition site and the consumer site, via keywords such as `mut`/`const`. This forces the consumer to explicitly dictate how they intend to treat an instance, and lets a caller override boundaries that should fundamentally belong to the domain model — a form of syntactic band-aid for weak encapsulation, and a source of constant call-site cognitive load. Meanwhile, tuple types and generic containers allow anonymous, positional data groupings that obscure domain meaning, and public field access breaks encapsulation at the structural level.

Khayyam's encapsulation model was designed to address all of these issues simultaneously. By making all fields private, all interaction method-based, all mutability intrinsic to the capsule, and all multi-value groupings named capsules, the language ensures that domain boundaries are expressed at the definition site and cannot be bypassed at the call site. This document records those rules, explains their motivation, and records the alternatives that were considered and rejected.

### Methodology

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

A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the [Abstraction document](./khayyam-abstraction.md). The polymorphic dispatch strategy is defined separately in the [Polymorphism document](./khayyam-polymorphism.md).

There are no tuple types — any multi-value grouping must be a named capsule with named fields. There are no consumer-side mutability keywords (`mut`, `const`, `readonly`). All arguments to methods are passed by reference, but the capsule's internal state remains protected because all fields are hidden and mutation can only occur through explicitly exposed methods.

### Sovereign Encapsulation
A capsule is the unit that owns its state and behavior. All internal fields of a capsule are strictly private; there is no public-field syntax; interaction only occurs via method invocation (message passing). Mutability and lifecycle behavior are intrinsic properties of the capsule's own definition, never something a caller can grant or deny at the call site.

A capsule's public methods are its entire contract. If a capsule exposes no mutating methods, it is inherently immutable — the consumer needs no keyword to promise not to mutate it, because there is no mechanical way to do so. If a consumer needs a differently-behaving variant of a data structure (e.g. a mutable wrapper around an otherwise immutable value), that is treated as a new business domain requirement: a new capsule with a distinct identity (e.g. `TransactionAmount` wrapping a fixed `Decimal_64_64`), not a local syntax trick like declaring `const`.

The immutability guarantee described here is a *method-contract* guarantee: a capsule exposing no mutating method cannot be mutated *through its own public interface*. It does not, by itself, resolve whether the memory a capsule's fields reference can also be mutated by some other owner of that same memory (e.g. a capsule holding a view into a buffer that a separate owner is permitted to overwrite elsewhere) — that is a distinct, lower-level memory-management concern, not addressed by this document. Whether, and how, this distinction is checked or enforced is left entirely to the compiler and/or linter layer, which may adopt a strict, Rust-`mut`-like enforcement policy; a more permissive policy that stays silent whenever an aliasing pattern is provably safe; or any other policy of its own design. This document does not mandate a specific enforcement policy — only that no *consumer-side keyword* can override a capsule's own declared behavior. The interaction between this guarantee and the underlying memory-management model is substantial and is deliberately deferred to future documents on memory management and buffer/storage ownership.

#### Discussion

##### Drawbacks
Every behavioral variant of a value (e.g. a frequently-needed mutable view of an otherwise-immutable type) requires defining and naming a new capsule, rather than a one-character keyword at the call site. This is intentional friction (consistent with the broader design philosophy that prefers explicit domain modeling over syntactic shortcuts), but it does mean more named types exist in a codebase than in languages with consumer-side modifiers.

##### Rationale and alternatives
The alternative (consumer-side `mut`/`const`) was rejected because it allows behavior overrides at the call site that bypass the domain model's own invariants, and because it adds a constant low-grade decision burden to every variable declaration.

##### Prior art
Rust's `mut`, C++'s `const`, TypeScript's `readonly` all place mutability responsibility at the consumer site. Smalltalk-style strict message-passing encapsulation (no public fields at all) is closer to Khayyam's model.

##### Unresolved questions
- The relationship between this document's method-contract immutability guarantee and lower-level storage-aliasing concerns (a capsule backed by a borrowed, externally-mutable buffer) is deferred to future documents on memory management and buffer ownership.

##### Future possibilities
None recorded yet.

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

#### Discussion

##### Drawbacks
Even trivial read access to a field (e.g., getting a configuration value) requires a method definition. For capsules with many fields, this can result in a large number of getter-style methods. However, these methods serve a critical purpose: they define the capsule's behavioral contract, and they can be evolved independently of the internal representation without breaking consumers.

##### Rationale and alternatives
- **Allow selective field exposure (as in C# properties, Rust `pub` fields; rejected)**: creates a two-tier system where some fields are public and others are private, with no principled rule for which should be which. It also breaks the guarantee that a capsule's entire contract is discoverable through its method interface.
- **Allow friend/internal visibility (as in C++, Java package-private; rejected)**: introduces scope-based exceptions that weaken the encapsulation guarantee and create implicit coupling between files or modules.

##### Prior art
Smalltalk's object model (all instance variables are private, all interaction is through messages) is the closest prior art. Go's struct model with uppercase/lowercase visibility is a weaker form that still allows direct field access for exported fields.

##### Unresolved questions
None at this time.

##### Future possibilities
A linter mode that detects capsules with "trivial getter" methods (methods that simply return a field value without transformation) and suggests whether they indicate a missing domain abstraction or are genuinely appropriate.

### Closures as Implicit Capsule Syntax
A closure, looked at structurally rather than syntactically, is not really a separate language feature — it is an implicit capsule. Whatever a closure captures is, in effect, a set of unnamed fields; whatever a closure runs when called is, in effect, an unnamed method attached to those fields. Every closure written in another language is already doing what a Khayyam capsule does — holding state and offering behavior over it — the only difference is that it does so anonymously, without a declared type, and without going through Sovereign Encapsulation's requirement that a capsule's state be named and explicit.

Seen this way, Khayyam does not need a standalone rule that singles out and forbids closures. It only needs to decline adding syntax for a capsule that is allowed to skip naming its own fields. If a behavior needs state (the kind of thing a closure would capture), that state is, by definition, a new domain entity with a name — so a developer defines a specific capsule for it, explicitly passes the required state in, and implements the necessary method, exactly as for any other capsule. There is no closure or lambda syntax in the grammar; any callback-shaped requirement is expressed as a named capsule implementing the relevant abstraction (e.g. a comparator capsule implementing a `Compare` method), referenced by name like any other type.

This framing also clarifies why this topic belongs inside the encapsulation document rather than standing alone: it is not an independent restriction sitting beside Sovereign Encapsulation — it *is* Sovereign Encapsulation, applied to the one syntactic form (an inline, capturing function) that would otherwise let a capsule's state stay implicit and unnamed.

Declining to admit this implicit-capsule syntax into the grammar has real consequences worth naming plainly. Closures are heavily used in other languages for callbacks and inline dynamic logic (e.g. capturing variables for sorting or filtering), and their convenience carries real architectural costs: hidden state capturing creates invisible dependencies and breaks explicit state management, and the ease of writing inline functions encourages developers to mash multiple distinct behaviors into a single method body under the false promise of "refactoring later." Requiring every captured state to surface as a named capsule keeps all state dependencies explicit, testable, strictly encapsulated, and analyzable by the compiler.

#### Discussion

##### Drawbacks
The discomfort and verbosity of having to name a capsule for even small, single-use behaviors (e.g. a one-off sort comparator) is a real and acknowledged cost. There is a recognized risk that a developer could recreate the same laziness this rule is meant to prevent by writing a throwaway, badly-named, single-use capsule instead of a proper closure — this is treated as a naming-convention/linter concern (see future linter documents), not a reason to reconsider this decision.

##### Rationale and alternatives
**Reduced Optimization Surface:** capsule-centric code, where state is always a named, explicit type, is significantly easier for the compiler to analyze and optimize than ad-hoc captured scopes. Both models are theoretically equivalent in the worst case, but capsule-based state is far more consistently optimizable in practice, because the compiler always has a concrete, named type to reason about rather than an implicit closure environment whose shape varies by call site. (An earlier, now-corrected version of this rationale argued closures cause additional heap allocation/escape compared to capsules — this is not accurate: a named capsule holding the same captured references has the same memory-lifetime profile as a closure would. The real justification is architectural explicitness and analyzability, not raw performance.)

##### Prior art
Java's pre-Java-8 model (no lambdas, only anonymous inner classes) followed the same philosophy Khayyam follows here, and it is informative evidence about the real-world cost of this constraint: the resulting boilerplate for simple, single-use callbacks (event listeners, one-off comparators) was significant enough that Java eventually added lambda expressions in Java 8 under sustained developer pressure.

A second, more direct data point comes from Go's standard `net/http` package, which offers two parallel ways to register a request handler for the same need: a closure-based form, `func HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request))`, and a capsule/struct-based form, `func Handle(pattern string, handler Handler)`. In practice, when both paths exist side by side, developers consistently default to the closure-based path, and encapsulation suffers in both forms regardless: `pattern` ends up living outside the handler type rather than being owned by it. This is read as evidence that offering closures alongside a capsule-based alternative does not lead to better modeling — it leads to the closure path being taken by default, with the encapsulation discipline silently degraded. Removing the closure path entirely is treated as a deliberate forcing function rather than an oversight, precisely because this dual-path failure mode is observed in real, widely-used code rather than hypothesized.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Relationship with Abstractions
A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the [Abstraction document](./khayyam-abstraction.md). This document concerns itself only with the encapsulation guarantees that make the abstraction model possible: capsules hide all internal state, and all interaction occurs through methods whose signatures the abstraction defines.

### Tuples Rejection
Khayyam has no tuple type or tuple literal syntax (`(a, b, c)` as an anonymous, positional, multi-value type). Any time a developer needs to group multiple values together, that grouping must be a named capsule with named fields, exactly like any other domain type.

Where another language might return `(string, int, error)` from a function, a Khayyam developer instead defines or reuses a named capsule with named fields appropriate to the domain (e.g. a `ParseResult` capsule with named `Value`, `Length`, and `Err` fields/methods), exactly as they would for any other piece of domain data.

There is no tuple literal or tuple type syntax in the grammar. Multiple related values are always grouped via an explicitly named capsule.

Tuples are rejected not because they lack behavior at the point of definition — a `(String, Int)` pair may appear harmless in isolation — but because they facilitate a wrong architectural evolution path. Over time, what begins as an anonymous positional grouping inevitably accumulates associated behavior (validation, formatting, conversion) that becomes scattered across the codebase rather than co-located with the data it concerns. This is the same trajectory that leads from anonymous data bags to anemic domain models. By requiring multi-value concepts to be represented as named types when they have semantic meaning, Khayyam ensures that domain identity is established from the outset and that behavior has a natural home.

#### Discussion

##### Drawbacks
Even a trivial, throwaway pairing of two values (e.g. swapping two variables, or returning a quick coordinate pair) requires naming and defining a capsule, rather than using an anonymous, lightweight tuple literal — measurably more ceremony than virtually every modern language provides for this common case.

##### Rationale and alternatives
- **Tuple types (the conventional approach in Go, Rust, Python, and many other languages; rejected)**: their positional, anonymous nature allows unnamed structural grouping of values without introducing a domain identity. While tuple types are a valid construct in formal type theory, in architectural modeling they serve as a primitive form of encapsulation — one that provides state grouping without ownership, without behavior, and without identity. This combination facilitates the gradual emergence of anemic domain models, where data and behavior become separated across the codebase.

##### Prior art
Go's multiple return values, Rust's and Python's tuple types, and TypeScript's tuple types are all common prior art for this feature; Khayyam's rejection here is closer in spirit to strongly nominal-typing-oriented languages and to general DDD advice discouraging "primitive obsession" and anonymous data bags.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Primitive Capsule Specification
The canonical Khayyam specification claims that replacing `int32` with `W32` is "zero-cost." But `W32` is not just a renamed integer — it is a capsule that provides behavioral guarantees beyond what `int32` offers. The migration contract depends on what exactly `W32` guarantees.

Possible behavioral guarantees for primitive capsules include:
- **Overflow behavior**: wrapping vs. panic vs. saturating. A `W32` (whole 32-bit) capsule likely wraps on overflow, while a different capsule might panic or saturate. The distinction is domain-meaningful, not just a compiler flag.
- **Bit-width enforcement**: no implicit widening or narrowing. A `W32` stays a `W32`; the developer must explicitly convert to a different width through a capsule method.
- **Serialization contract**: predictable binary layout. A `W32` guarantees a specific byte order and alignment, making it safe for network transmission and file storage without additional serialization logic.
- **Range semantics**: if used as an index, bounds checking may be enforced by the capsule's methods rather than by the language runtime.

The answer matters because it defines the migration contract. If `W32` only provides renaming, the "zero-cost" claim is trivial. If it provides behavioral guarantees, the migration is more complex but the value is real — the capsule enforces invariants that a raw `int32` cannot.

This topic is also relevant to whether primitive capsules should be defined by the language itself, by the standard library, or by the Memar framework. Each choice has different implications for portability (can a `W32` be used without the Memar framework?), governance (who decides what behavioral guarantees a primitive capsule provides?), and consistency (do all primitive capsules follow the same specification pattern?).

#### Discussion

##### Drawbacks
Defining behavioral guarantees for primitive capsules adds complexity to the "de-Primitive-ing" migration story. A developer replacing `int32` with `W32` must now understand that `W32` is not a drop-in replacement but a capsule with specific behavioral contracts that may differ from the raw integer semantics they expect.

##### Rationale and alternatives
- **Primitive capsules as pure renames with no behavioral guarantees (rejected)**: would make the "de-Primitive-ing" migration trivially zero-cost but would also make it meaningless — a rename without behavioral difference adds no value.
- **Primitive capsules with full behavioral specifications (Khayyam's apparent intent)**: makes the migration more valuable but requires explicit specification of each primitive capsule's behavioral guarantees.

##### Prior art
Zig's integer types include comptime range checks and overflow semantics. Rust's integer types distinguish between wrapping (`wrapping_add`), checked (`checked_add`), and saturating (`saturating_add`) operations through methods, not through separate types. Ada's range types are closer to Khayyam's model of encoding range semantics in the type itself.

##### Unresolved questions
1. What behavioral guarantees does each primitive capsule provide? Is there a formal specification for `W32`, `W64`, `R32`, `R64`, and other primitive capsules?
2. Should primitive capsules be defined by the language itself, by the standard library, or by the Memar framework? Each choice has different implications for portability and governance.
3. How do primitive capsule guarantees interact with the compiler's optimization strategy — can a `W32` with wrapping semantics be optimized differently from a `W32` with saturating semantics?

##### Future possibilities
A formal specification document for each primitive capsule, defining its behavioral guarantees, overflow semantics, serialization contract, and range semantics, serving as the reference for both compiler implementation and migration guidance.

### Constants as Capsule-Returned Values
A constant in Khayyam is simply a variable returned by a capsule method that cannot change after first initialization — an organizational and architectural rule, not a dedicated compiler keyword. Two flavors are distinguished:

- **Static constants**: compile-time declared and initialized, usually inlined directly at compile time. Conceptually equivalent to "a function that runs entirely at compile time and returns the value living in that function's body."
- **Dynamically-valued constants**: compile-time declared, but runtime-initialized. These require a runtime memory-service call to obtain their value since they cannot be inlined.

A "config" capsule for a module, for example, exposes module-level values through methods. Some of those methods may allow controlled, intentional changes to specific values; others guarantee a value never changes once initialized. Both cases are ordinary capsule methods — there is no separate `const`-flavored declaration syntax.

This approach is consistent with Sovereign Encapsulation: the "this value never changes" guarantee depends on the capsule author's discipline (not exposing a mutating method) rather than being enforced by a keyword, and the consumer discovers the guarantee through the capsule's public interface, not through a modifier on the variable declaration.

#### Discussion

##### Drawbacks
Without a dedicated keyword, the "this value never changes" guarantee for a constant depends entirely on the capsule author's discipline (not exposing a mutating method) rather than being enforced by a single, unmistakable declaration keyword a reader can immediately recognize.

##### Rationale and alternatives
- **Dedicated `const` keyword (the conventional approach in most languages; rejected)**: would reintroduce a consumer/producer-side modifier that Khayyam otherwise eliminates entirely in favor of behavior being intrinsic to the capsule. A dedicated `const` keyword was already rejected at the consumer side; this section addresses the producer side — how a value that should never change after initialization is expressed without introducing a separate keyword category.
- **`constexpr`/`comptime` keyword (as in C++, Zig; rejected)**: while closer in spirit to Khayyam's "constant as a compile-time function" framing, these still introduce a separate keyword category rather than making the behavior intrinsic to the capsule's method design.

##### Prior art
Most languages provide an explicit `const`/`final`/`let` keyword. Khayyam's "constant as a compile-time function" framing is conceptually close to `constexpr` functions in C++ or `comptime` values in Zig, though without a dedicated keyword marking them as such.

##### Unresolved questions
- Whether developers should be able to change a "dynamically-valued constant" at runtime by having the compiler force the runtime to rewrite binary code directly (avoiding a memory-service call, with the same memory size) is explicitly marked as undecided and remains unresolved.
- How to pass a return value from a constant method to other methods — the interaction between constant methods and the broader method-call chain needs further specification.

##### Future possibilities
None recorded yet.

## Results

## Discussion

### Naming Conventions
Suggested conventions for capsule and abstraction names (non-binding, enforceable via linter configuration):

- **Capsule names**: PascalCase, domain-meaningful (e.g., `AppConfig`, `UserRegistry`, `ConnectionIndex`). Avoid generic names like `Manager`, `Handler`, `Helper` — these indicate missing domain specificity.
- **Abstraction names**: PascalCase, domain-concept framing (e.g., `Reader`, `Writer`, `Repository`). Avoid technical-capability framing (e.g., `Readable`, `Writable`, `Filterable`) — these indicate over-abstraction risk.
- **Method names**: PascalCase for public methods, matching the capsule's domain language. Avoid getter/setter prefixes (`Get...`, `Set...`) when the method name can express the domain action more directly (e.g., `ApplyTimeout` instead of `SetTimeout`).
- **Field names**: PascalCase inside capsules, consistent with the type naming convention. Since fields are always private, their names are an internal design decision of the capsule author.

### Drawbacks
The encapsulation model's insistence on method-only interaction, no tuples, no closures, and no consumer-side mutability keywords creates a codebase with more named types and more method definitions than virtually any mainstream language. For simple data structures (a 2D coordinate, a key-value pair, a result type) or simple one-off behaviors (a sort comparator, a callback), the developer must define a named capsule with named fields and explicit methods, rather than using a tuple, a struct with public fields, or a closure. This is the price of guaranteed domain integrity and encapsulation — but it is a real price, and it is felt most acutely during rapid prototyping or when writing glue code between systems.

### Rationale and alternatives
- **Allow public fields for simple data carriers (rejected)**: would create a two-tier system where some capsules have public fields and others don't, with no principled rule for which should be which. It would also break the guarantee that a capsule's entire contract is its method interface.
- **Allow tuples for "simple" multi-value returns (rejected)**: the boundary between "simple" and "complex" is subjective; once tuples are allowed for simple cases, they tend to proliferate to complex cases where they obscure domain meaning.
- **Allow consumer-side `const` for read-only references (rejected)**: see [Sovereign Encapsulation](#sovereign-encapsulation) for the full rationale.
- **Allow closures for simple, single-use callbacks (rejected)**: see [Closures as Implicit Capsule Syntax](#closures-as-implicit-capsule-syntax) for the full rationale.

### Prior art
Smalltalk's strict message-passing encapsulation (no public fields, all interaction through messages) is the closest mainstream prior art for the capsule model. Prior art for abstractions and polymorphism is documented in their documents respectively.

### Unresolved questions
1. Should the language or the Memar framework provide a set of "standard" capsules for common patterns (e.g., `Pair`, `Result`, `Option`) to reduce the ceremony of defining named capsules for simple cases?
2. How does the encapsulation model interact with serialization and deserialization — can a capsule's internal state be serialized without going through its public methods?

### Future possibilities
- A standard library of commonly-needed capsules (e.g., `Pair`, `Result`, `Option`, `Range`) that provide named, domain-specific alternatives to tuples and generic containers, following the naming and design conventions documented in this document.

## Change Rationale
- **Structural migration.** Brought the document in line with the current Explanation-facet specification (`documentation-explanation.md`): `Summary` renamed to `Abstract`; `Motivation` moved under a new `Introduction` wrapper alongside an (empty) `Methodology`; the former `Guide-level explanation` promoted to a named, first-listed `Explanation` topic ("Capsules and Methods at a Glance") and linked from the Abstract as "Guide"; the `Reference-level explanation` heading removed, its topics now sitting directly under `Explanation`; added an empty `Results` section per the fixed body-section order.
- **Closures merge.** Merged the standalone "Absence of Closures and Anonymous Functions" document into `Explanation` as a new topic, placed immediately after "Method as Callable Capsule," on the grounds that it is a direct corollary of Sovereign Encapsulation rather than an independent rule. All original content (summary, motivation, guide- and reference-level explanation, and the full Discussion bundle) was preserved; only the internal headings were removed as part of folding it into the topic-plus-Discussion shape. The document-wide `Discussion > Drawbacks` and `Rationale and alternatives` were extended with one clause each to reflect the newly merged topic. The standalone file has been retired.
- **Extraction of non-capsule content.** A capsule is an abstraction layered over `vr` and `mt`, not an independent primitive — so content specific to those underlying concepts should be defined in their own documents and only referenced here. Accordingly: "Method as Callable Capsule" (including its Method Invocation Rules and Body-less Methods subsections) moved to [Method in Khayyam](./khayyam-method.md); "Code Scope" moved to [Logic in Khayyam](./khayyam-logic.md), since `sc` is structurally the mechanism control-flow libraries are built on rather than a capsule-level concern. The Abstract and front-matter Citations were updated to reference both documents instead of restating their content.
- **Positive reframing of closures.** "Absence of Closures and Anonymous Functions" renamed to "Closures as Implicit Capsule Syntax" and its opening reframed: rather than starting from "Khayyam does not support closures," it now starts from the structural observation that a closure already *is* an implicit, unnamed capsule, and that Sovereign Encapsulation's existing requirement (state must be named and explicit) is sufficient on its own to explain why this syntax was not admitted — no separate prohibitive rule is needed. The Discussion subsections (Drawbacks, Rationale and alternatives, Prior art) were left unchanged, since the case they make does not depend on which framing introduces the topic. Cross-reference links elsewhere in this document were updated to the new heading.
