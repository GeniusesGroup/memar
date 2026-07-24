---
Title: "Encapsulation in Khayyam"
Status: Draft
Start Date: 2026-07-15
RFC Number: 495592
Applied to: []
Related RFCs:
    - Title: "Khayyam - Programming Language"
      URI: "../Khayyam.md"
      Reason: "Reference"
      Explanation: "The canonical specification defines capsule, method, and abstraction syntax that this RFC elaborates and motivates."
    - Title: "Khayyam Design Philosophy"
      URI: "./khayyam.md"
      Reason: "Reference"
      Explanation: "The philosophy RFC documents the recurring principles (behavior over type identity, domain modeling, syntactic atomicity) that underpin the encapsulation design decisions recorded here."
    - Title: "Abstraction in Khayyam"
      URI: "./khayyam-abstraction.md"
      Reason: "Reference"
      Explanation: "The abstraction mechanism is specified separately. This RFC documents the encapsulation guarantees (capsules hide all internal state, all interaction occurs through methods) that make the abstraction model possible."
    - Title: "Polymorphism in Khayyam"
      URI: "./khayyam-polymorphism.md"
      Reason: "Reference"
      Explanation: "Polymorphism classification and dispatch strategy are specified separately. This RFC defines the capsule-level boundaries that constrain polymorphic behavior."
Contributor(s):
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
    Effort: "High"
    Tasks:
      - Works: ["Restructuring into RFC template", "Content consolidation and enrichment", "Restructured scattered encapsulation-related content into the canonical RFC template; consolidated content from staging and specification files; added reference-level elaborations on capsule structure, method dispatch, abstraction design, and primitive capsule specification."]
        URI: ""
---

# Encapsulation in Khayyam

## Summary
This RFC specifies Khayyam's encapsulation model: the architectural rules governing how capsules own their state and behavior, how interaction occurs exclusively through methods, and how mutability is an intrinsic property of the capsule's own definition rather than a consumer-side keyword. The central principle is Sovereign Encapsulation — all internal fields of a capsule are strictly private, all interaction occurs via method invocation (message passing). The RFC also covers the rejection of tuples, the method invocation model (uniform dot syntax with self-based dispatch), primitive capsule behavioral guarantees, and the capsule-level constant model.

## Motivation
Languages like Rust, C++, and TypeScript split the burden of managing mutability and lifecycle safety between the definition site and the consumer site, via keywords such as `mut`/`const`. This forces the consumer to explicitly dictate how they intend to treat an instance, and lets a caller override boundaries that should fundamentally belong to the domain model — a form of syntactic band-aid for weak encapsulation, and a source of constant call-site cognitive load. Meanwhile, tuple types and generic containers allow anonymous, positional data groupings that obscure domain meaning, and public field access breaks encapsulation at the structural level.

Khayyam's encapsulation model was designed to address all of these issues simultaneously. By making all fields private, all interaction method-based, all mutability intrinsic to the capsule, and all multi-value groupings named capsules, the language ensures that domain boundaries are expressed at the definition site and cannot be bypassed at the call site. This RFC documents those rules, explains their motivation, and records the alternatives that were considered and rejected.

## Guide-level explanation
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

A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the Abstraction RFC (RFC 495493). The polymorphic dispatch strategy is defined separately in the Polymorphism RFC (RFC 495494).

There are no tuple types — any multi-value grouping must be a named capsule with named fields. There are no consumer-side mutability keywords (`mut`, `const`, `readonly`). All arguments to methods are passed by reference, but the capsule's internal state remains protected because all fields are hidden and mutation can only occur through explicitly exposed methods.

## Reference-level explanation

### Sovereign Encapsulation
A capsule is the unit that owns its state and behavior. All internal fields of a capsule are strictly private; there is no public-field syntax; interaction only occurs via method invocation (message passing). Mutability and lifecycle behavior are intrinsic properties of the capsule's own definition, never something a caller can grant or deny at the call site.

A capsule's public methods are its entire contract. If a capsule exposes no mutating methods, it is inherently immutable — the consumer needs no keyword to promise not to mutate it, because there is no mechanical way to do so. If a consumer needs a differently-behaving variant of a data structure (e.g. a mutable wrapper around an otherwise immutable value), that is treated as a new business domain requirement: a new capsule with a distinct identity (e.g. `TransactionAmount` wrapping a fixed `Decimal_64_64`), not a local syntax trick like declaring `const`.

The immutability guarantee described here is a *method-contract* guarantee: a capsule exposing no mutating method cannot be mutated *through its own public interface*. It does not, by itself, resolve whether the memory a capsule's fields reference can also be mutated by some other owner of that same memory (e.g. a capsule holding a view into a buffer that a separate owner is permitted to overwrite elsewhere) — that is a distinct, lower-level memory-management concern, not addressed by this RFC. Whether, and how, this distinction is checked or enforced is left entirely to the compiler and/or linter layer, which may adopt a strict, Rust-`mut`-like enforcement policy; a more permissive policy that stays silent whenever an aliasing pattern is provably safe; or any other policy of its own design. This RFC does not mandate a specific enforcement policy — only that no *consumer-side keyword* can override a capsule's own declared behavior. The interaction between this guarantee and the underlying memory-management model is substantial and is deliberately deferred to future RFCs on memory management and buffer/storage ownership.

#### Discussion

##### Drawbacks
Every behavioral variant of a value (e.g. a frequently-needed mutable view of an otherwise-immutable type) requires defining and naming a new capsule, rather than a one-character keyword at the call site. This is intentional friction (consistent with the broader design philosophy that prefers explicit domain modeling over syntactic shortcuts), but it does mean more named types exist in a codebase than in languages with consumer-side modifiers.

##### Rationale and alternatives
The alternative (consumer-side `mut`/`const`) was rejected because it allows behavior overrides at the call site that bypass the domain model's own invariants, and because it adds a constant low-grade decision burden to every variable declaration.

##### Prior art
Rust's `mut`, C++'s `const`, TypeScript's `readonly` all place mutability responsibility at the consumer site. Smalltalk-style strict message-passing encapsulation (no public fields at all) is closer to Khayyam's model.

##### Unresolved questions
- The relationship between this RFC's method-contract immutability guarantee and lower-level storage-aliasing concerns (a capsule backed by a borrowed, externally-mutable buffer) is deferred to future RFCs on memory management and buffer ownership.

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

### Method as Callable Capsule
In Khayyam, functions and methods are not separate concepts; a method is fundamentally a callable capsule. By using the `mt` subtype, developers define an executable behavior and attach it to a receiver. The receiver is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`).

The method signature follows this pattern:

```khayyam
tp {name} mt (self {capsule_owner}) ({efficacy variables}...) ({impressible(affective) variables}...) { ___ }
```

Key rules:
- **Pass-by-Reference and State Protection**: All arguments passed into a method and all values returned from a method are passed strictly by reference. Even though capsules are passed by reference, their internal state remains strictly protected because all data fields are entirely hidden. A receiving method cannot directly mutate the passed capsule's fields. State mutation can only occur if the passed capsule explicitly exposes a behavior (method) that allows it.
- **Parenthesized Separation**: Developers must separate `capsule`, `args`, and `returns` by using `()` to indicate all of them, even if empty. All three are the same at the underlying layers; this rule exists to improve code readability.
- **Standalone Functions**: Developers can write pure standalone functions by omitting the `self` parameter — there is no limitation requiring a receiver.
- **Recommended Naming**: Developers can use any naming for the capsule owner parameter, but `self` is suggested as the base point to reference other members in the capsule.

Example:
```khayyam
tp Set mt (self Key) (key String) (err Error) {}
```

#### Method Invocation Rules

Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.

The distinction between static behavior and instance behavior is governed by the presence of the `self` reference in the method signature, enforced strictly at the tooling/linter layer:

- **Type-Level (Static) Invocation**: Methods defined without a `self` reference belong to the type's blueprint. They must be invoked directly through the type identifier (e.g., `tp.Create()`). Invoking a type-level method on a variable instance (`vr.Create()`) is flagged as an error.
- **Instance-Level Invocation**: Methods defined with a `self` reference require an active memory capsule. They must be invoked through a variable instance (e.g., `vr.Mutate()`). Invoking an instance-level method directly on the type identifier (`tp.Mutate()`) is rejected.

This dispatch model ensures that the boundary between type-level and instance-level behavior is always visible in the method signature, not hidden behind a `static` keyword or a naming convention.

#### Body-less Methods (FFI and Contracts)

A method can be defined without a body (`{}`). This is legally used in two scenarios:

1. **Contract Definition**: Defining the required signature for an abstraction (`ab`). The method body is provided by each capsule that implements the abstraction.
2. **Foreign Function Interface (FFI)**: When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file).

#### Discussion

##### Drawbacks
The strict separation of capsule, args, and returns with `()` adds syntactic ceremony for methods that take no arguments or return no values. A method like `tp Close mt (self Reader) () () {}` has two empty parenthetical groups that carry no information — they exist purely for consistency and readability conventions.

##### Rationale and alternatives
- **Unified parameter list without parenthetical separation (rejected)**: would make it harder to distinguish at a glance which parameters are inputs and which are outputs, especially for methods with many parameters.
- **Separate keyword for functions vs. methods (rejected)**: a method is fundamentally a callable capsule; introducing a separate keyword would create an artificial distinction where none exists at the semantic level.

##### Prior art
Go's method syntax with an explicit receiver is syntactically similar. Rust's `fn` with `&self`/`&mut self` is semantically similar but introduces reference annotations that Khayyam eliminates. Smalltalk's message-passing model is the closest conceptual match.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Relationship with Abstractions
A capsule exposes behavior through methods. The relationship between capsules and abstractions is defined separately in the Abstraction RFC (RFC 495493). This RFC concerns itself only with the encapsulation guarantees that make the abstraction model possible: capsules hide all internal state, and all interaction occurs through methods whose signatures the abstraction defines.

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

### Code Scope
A code scope is defined with the `sc` subtype:

```khayyam
tp {name} sc { ___ }
```

Code scopes are used in logic methods such as `IF`, `LOOP`, `GOTO`, and other control-flow constructs that will be developed in libraries. A code scope must be used only inside a method body — it cannot appear at the file level or inside a capsule definition outside of a method.

This design ensures that control-flow constructs are not built into the language syntax but are instead provided as library-level abstractions, consistent with Khayyam's philosophy of separating syntax from governance. The language provides the `sc` mechanism; libraries and frameworks provide the specific control-flow implementations.

#### Discussion

##### Drawbacks
Without built-in control-flow syntax, even basic constructs like `if` and `for` require importing a library. This may feel unfamiliar to developers coming from languages where these constructs are keywords, and it adds an import dependency that does not exist in other languages.

##### Rationale and alternatives
- **Built-in control-flow keywords (the conventional approach; rejected)**: would embed specific control-flow semantics into the language, preventing frameworks and organizations from defining their own control-flow policies (e.g., mandatory error checking on each iteration, or logging on each branch).
- **Code scope as a library-only feature without language support (considered, not chosen)**: without the `sc` type, libraries would need to use capsules for control flow, losing the semantic distinction between "a data capsule" and "a control-flow scope."

##### Prior art
Lisp's macro-based control flow and Forth's immediate words are distant precedents for library-defined control flow. No mainstream language provides `sc`-style scope abstractions as a first-class type.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

## Discussion

### Naming Conventions
Suggested conventions for capsule and abstraction names (non-binding, enforceable via linter configuration):

- **Capsule names**: PascalCase, domain-meaningful (e.g., `AppConfig`, `UserRegistry`, `ConnectionIndex`). Avoid generic names like `Manager`, `Handler`, `Helper` — these indicate missing domain specificity.
- **Abstraction names**: PascalCase, domain-concept framing (e.g., `Reader`, `Writer`, `Repository`). Avoid technical-capability framing (e.g., `Readable`, `Writable`, `Filterable`) — these indicate over-abstraction risk.
- **Method names**: PascalCase for public methods, matching the capsule's domain language. Avoid getter/setter prefixes (`Get...`, `Set...`) when the method name can express the domain action more directly (e.g., `ApplyTimeout` instead of `SetTimeout`).
- **Field names**: PascalCase inside capsules, consistent with the type naming convention. Since fields are always private, their names are an internal design decision of the capsule author.

### Drawbacks
The encapsulation model's insistence on method-only interaction, no tuples, and no consumer-side mutability keywords creates a codebase with more named types and more method definitions than virtually any mainstream language. For simple data structures (a 2D coordinate, a key-value pair, a result type), the developer must define a named capsule with named fields and explicit methods, rather than using a tuple or a struct with public fields. This is the price of guaranteed domain integrity and encapsulation — but it is a real price, and it is felt most acutely during rapid prototyping or when writing glue code between systems.

### Rationale and alternatives
- **Allow public fields for simple data carriers (rejected)**: would create a two-tier system where some capsules have public fields and others don't, with no principled rule for which should be which. It would also break the guarantee that a capsule's entire contract is its method interface.
- **Allow tuples for "simple" multi-value returns (rejected)**: the boundary between "simple" and "complex" is subjective; once tuples are allowed for simple cases, they tend to proliferate to complex cases where they obscure domain meaning.
- **Allow consumer-side `const` for read-only references (rejected)**: see [Sovereign Encapsulation](#sovereign-encapsulation) for the full rationale.

### Prior art
Smalltalk's strict message-passing encapsulation (no public fields, all interaction through messages) is the closest mainstream prior art for the capsule model. Prior art for abstractions and polymorphism is documented in RFC 495493 (Abstraction) and RFC 495494 (Polymorphism) respectively.

### Unresolved questions
1. Should the language or the Memar framework provide a set of "standard" capsules for common patterns (e.g., `Pair`, `Result`, `Option`) to reduce the ceremony of defining named capsules for simple cases?
2. How does the encapsulation model interact with serialization and deserialization — can a capsule's internal state be serialized without going through its public methods?

### Future possibilities
- A standard library of commonly-needed capsules (e.g., `Pair`, `Result`, `Option`, `Range`) that provide named, domain-specific alternatives to tuples and generic containers, following the naming and design conventions documented in this RFC.

## Change Rationale
