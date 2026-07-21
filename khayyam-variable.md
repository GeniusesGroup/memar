---
Title: "Variable in Khayyam"
Status: Draft
Start Date: 2026-07-15
RFC Number: 495591
Applied to: []
Related RFCs:
    - Title: "Khayyam - Programming Language"
      URI: "../Khayyam.md"
      Reason: "Reference"
      Explanation: "The canonical specification defines the core variable syntax (vr), import mechanism, and logical-reference semantics that this RFC elaborates and motivates."
    - Title: "Khayyam Design Philosophy"
      URI: "./khayyam.md"
      Reason: "Reference"
      Explanation: "The philosophy RFC documents the recurring principles (self-documenting code, syntactic atomicity, domain modeling) that underpin the variable design decisions recorded here."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions", "Defined the core variable semantics, no-assignment-operator rule, and de-primitive-ing philosophy in the canonical Khayyam specification."]
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
      - Works: ["Restructuring into RFC template", "Content consolidation and enrichment", "Restructured scattered variable-related content into the canonical RFC template; consolidated content from multiple source files; added reference-level elaborations on scope, initialization, and import mechanics."]
        URI: ""
---

# Variable Semantics and Declaration in Khayyam

## Summary
This RFC specifies the semantics, declaration rules, and design rationale for variables in Khayyam. A variable in Khayyam is a named reference to an instance of a type — never a raw data block and never decorated with consumer-side mutability keywords. Variables are declared with explicit types and initialized exclusively through capsule methods (no assignment operators). The language forbids multi-variable declarations, type inference, and magic numbers, ensuring that every variable declaration carries domain meaning and that the codebase remains self-documenting by construction.

## Motivation
In most mainstream languages, variable declarations are a locus of hidden complexity: type inference hides the actual type from readers, assignment operators enable implicit copies and aliasing bugs, multi-variable declarations compress distinct pieces of information into a single line, and consumer-side modifiers (`mut`, `const`, `readonly`) shift mutability decisions to every call site rather than anchoring them in the type's own definition. These conveniences optimize for writing speed at the expense of reading clarity, long-term maintainability, and domain integrity.

Khayyam's variable model was designed to eliminate each of these sources of opacity. By requiring explicit types, forbidding assignment operators, rejecting multi-declaration syntax, and separating variable identity from type behavior, the language ensures that every variable declaration communicates its domain purpose, its type, and its behavioral contract without ambiguity. This RFC documents those rules, explains their motivation, and records the alternatives that were considered and rejected.

## Guide-level explanation
A Khayyam variable is declared with the `vr` keyword, an explicit name, and an explicit type. There is no type inference, no assignment operator, and no multi-variable declaration syntax. Initialization happens through capsule methods, not through direct assignment. A variable creates a named reference to an instance of a type; the variable itself has no behavioral semantics — the behavior of the referenced instance is defined by its type.

```khayyam
// Declaration
vr x W8
// Initialization via capsule method
x.FromString("41")

vr y R32
y.FromString("3.14")
```

Variables can be declared at two scopes: file-level (module-level constants and singletons) and method-body level (local references). File-level variables can also be imported from other files using the `in` keyword:

```khayyam
vr MaxTimeout in "net/config"
```

Declaring a variable establishes a name and type relationship. It does not define how the underlying capsule is created or initialized — creation and initialization remain responsibilities of capsule behavior. This separation ensures that the variable syntax (`vr`) handles identity and reference, while the capsule definition handles behavior.

This design means that reading Khayyam code never requires mental type-inference reconstruction, never hides aliasing behind an `=` sign, and never surprises a reader with an unexpected mutation — the capsule's public interface is the complete and only contract.

## Reference-level explanation

### Variable Declaration Syntax
The `vr` keyword is the sole mechanism for declaring a variable. The grammar permits exactly one variable name and one type per declaration statement; there is no comma-separated multi-declaration form. The syntax is:

```khayyam
vr {name} {type}
```

The name must be a valid identifier. The type must be a previously defined or imported type (capsule, abstraction, method, or scope). A variable declaration is a distinct, separate statement — it cannot be combined with any other declaration on the same line, and it cannot carry an initializer inline. This ensures that every variable has its own visible scope in the source and that a reader can never skim past a declaration because it was compressed alongside others.

The explicit separation of declaration from initialization is deliberate. A variable's name and type are communicated in one step; its initial state is communicated in a separate, equally visible step. This two-step pattern reinforces the principle that the *what* (identity and type) and the *how* (initial state) are distinct pieces of information, each deserving its own moment of reader attention.

#### Discussion

##### Drawbacks
Declaring several related variables together — for example, the x and y components of a coordinate — requires multiple separate lines rather than one compact line. This is measurably more verbose than most other languages for this common case. However, the verbosity is intentional: each variable is equally visible, and a reader cannot accidentally overlook one of several declarations that were compressed into a single statement.

##### Rationale and alternatives
- **Multi-variable declaration syntax (the conventional approach in Go, C, and JavaScript; rejected)**: compressing multiple distinct pieces of information (each variable's own name, type, and initial state) into a single line works against the language's broader preference for one explicit, visible step per statement. A reader can easily skim past one of several declared variables, especially when their types or initial values differ.
- **Inline initialization (e.g., `vr x W8 = 41`; rejected)**: would reintroduce an assignment operator in a different form, conflicting with the language's decision to eliminate `=` entirely and to make all state changes explicit through capsule methods.

##### Prior art
Go, C, and JavaScript all support multi-variable declaration syntax as a convenience. Languages with a stricter "one binding per statement" discipline — idiomatic, non-compressed style in many functional languages — are closer in spirit to Khayyam's choice here.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### No Type Inference
Khayyam explicitly does not support automatic type inference at the compiler level. Every variable declaration must include an explicit type. While implementing type inference is technically trivial, it introduces "magic" into the codebase: it slightly speeds up the writing process for the author but significantly increases the cognitive load for the reader, who must mentally reconstruct the inferred type from context.

In Khayyam, code readability is paramount. Developers must declare explicit types. Linters will heavily assist developers during the writing phase, suggesting the correct types based on the assigned capsules, ensuring the final code is crystal clear, explicitly typed, and requires minimal mental processing for future maintainers.

This rule also reinforces the "de-Primitive-ing" principle: because every variable must carry an explicit type, and because primitives are replaced by named capsules (e.g., `W32` instead of `int`), the type declaration itself communicates domain meaning rather than just machine representation.

#### Discussion

##### Drawbacks
Explicit type declarations require more keystrokes per variable than inferred types. For developers accustomed to Rust's `let x = 42` or Go's `:=` short declaration, the additional explicitness may feel like unnecessary ceremony, especially for obvious cases where the type is self-evident from the right-hand side.

##### Rationale and alternatives
- **Full type inference (as in Haskell, Rust with `let`, Kotlin with `val`; rejected)**: optimizes for the writer at the expense of every future reader, and undermines the self-documenting code principle that every variable's domain meaning should be visible at the declaration site.
- **Partial inference (infer only when "obvious"; considered, not chosen)**: the boundary of "obvious" is subjective and creates inconsistency across a codebase — some variables will have explicit types and others won't, with no principled rule for which is which.
- **Linter-suggested, compiler-enforced (Khayyam's chosen approach)**: the compiler requires explicit types; the linter assists by suggesting the correct type during development. This gives the writer tooling support while preserving the reader's ability to see every type without inference.

##### Prior art
Go requires explicit types in `var` declarations but allows `:=` short declarations with inference. Rust allows `let` with optional type annotations. Haskell uses full Hindley-Milner inference. Khayyam's approach is closest to a strict explicit-typing discipline with linter assistance, similar to some enterprise Java style guides that mandate explicit generic type parameters even when they could be inferred.

##### Unresolved questions
None at this time.

##### Future possibilities
A linter auto-completion mode that proposes the full type annotation as the developer types, reducing the mechanical cost of explicit typing without compromising readability.

### Mutability Is a Type Concern, Not a Variable Concern
A variable in Khayyam creates a named reference to an instance of a type. The variable itself has no behavioral semantics — whether the referenced instance can or cannot mutate is determined entirely by the type's own definition (specifically, whether the capsule exposes any mutating methods), not by any modifier on the variable declaration.

This means the question "is this variable immutable?" is ill-posed in Khayyam. The correct question is "does this type expose mutating behavior?" — and that question is answered by inspecting the type's method contract, not the variable's declaration syntax.

This is not a consumer-side keyword constraint (there is no `const` or `let`) — it is a direct consequence of the separation between variable identity and type behavior. A variable is a name and a type relationship; the type owns the behavior.

#### Discussion

##### Drawbacks
Every behavioral variant of a value (e.g., a frequently-needed mutable view of an otherwise-immutable type) requires defining and naming a new capsule, rather than a one-character keyword at the call site. This is intentional friction, but it does mean more named types exist in a codebase than in languages with consumer-side modifiers.

##### Rationale and alternatives
- **Consumer-side `mut`/`const` (as in Rust, C++, TypeScript; rejected)**: allows behavior overrides at the call site that bypass the domain model's own invariants, and adds a constant low-grade decision burden to every variable declaration. It also conflates two distinct concerns: the identity of a reference (variable) and the behavioral contract of the referenced instance (type).
- **Reassignable-by-default with `const` opt-out (as in JavaScript `let`/`const`; rejected)**: makes mutation the path of least resistance, encouraging developers to default to mutable variables and add `const` only when they remember — the opposite of Khayyam's intent.

##### Prior art
Rust's `let` (immutable by default) with `mut` opt-in is the closest mainstream prior art at the syntax level, though Rust conflates binding, object, ownership, and mutation into a single declaration modifier. Khayyam separates these concerns: the variable is the reference, the type owns the behavior.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### No Assignment Operators
Khayyam completely eliminates assignment operators (like `=`). Variables represent logical references to type instances; passing a variable to a method provides access to the same instance. The language structurally prevents any implicit deep or shallow copying through its syntax — the storage and copying model is an implementation concern addressed by future RFCs on resource management.

This rule has far-reaching implications: it means that state changes are always mediated by capsule methods, never by direct assignment. A variable's reference never silently changes to point to a different capsule instance — any such change requires an explicit method call that makes the operation visible in the source code.

If a deep copy or state duplication is logically required, it must be done explicitly via the capsule's behavior:

```khayyam
vr newVar Type
newVar.CopyFrom(oldVar)
```

The removal of `=` also eliminates an entire class of bugs related to unintended aliasing (where two variables unexpectedly reference the same mutable data), because the language makes it structurally impossible to create such aliases through assignment. Any aliasing that does occur is always explicit and intentional, created through method parameters that reference the same instance.

#### Discussion

##### Drawbacks
The absence of assignment operators means that even trivial state updates — setting a flag, incrementing a counter — must go through a method call. This adds syntactic overhead for operations that would be a single character (`=`) in other languages. However, this overhead ensures that every state change is traceable, auditable, and mediated by the capsule's own behavioral contract.

##### Rationale and alternatives
- **Allow `=` for simple reassignment (rejected)**: would create a two-tier system where some state changes use `=` and others use methods, with no principled rule for which is which. It would also reintroduce the aliasing bugs that the elimination of `=` prevents.
- **Allow `=` but only for value types (considered, not chosen)**: Khayyam has no value-type/reference-type distinction at the variable level — all variables are logical references — so this distinction cannot be cleanly drawn.

##### Prior art
Most languages use `=` for assignment. Languages that restrict or eliminate assignment — such as pure functional languages (Haskell, Erlang) where all variables are single-assignment — are closer in spirit, though Khayyam's approach is less restrictive (mutation is possible through capsule methods) while still preventing implicit aliasing.

##### Unresolved questions
None at this time.

##### Future possibilities
None recorded yet.

### Variable as Logical Reference
A variable in Khayyam does not represent a storage location or a raw memory region. It represents a logical reference to a type instance. The storage model is an implementation concern; the language model concerns identity and access.

This means:
- **A variable's type determines its behavioral contract.** Since the type is always a named type, the variable's capabilities are fully discoverable from that type's public interface — no reflection, no runtime type queries, no `instanceof` needed.

This design is a direct consequence of the "Separation of Syntax and Governance" philosophy: the variable syntax (`vr`) handles identity and reference, while the type definition handles behavior. The storage and lifecycle model is a separate concern addressed by future RFCs on resource management.

#### Discussion

##### Drawbacks
Developers coming from value-semantic languages (C, C++, Go) may initially expect that assigning one variable to another creates an independent copy. In Khayyam, both variables reference the same instance. This requires a mental model shift from "variables as containers" to "variables as references," which may cause confusion during the initial learning period.

##### Rationale and alternatives
- **Value semantics by default (as in C, Go; rejected)**: would require implicit copies on every assignment or pass, introducing hidden memory allocation overhead and creating a performance model that depends on the compiler's copy-elision decisions.
- **Hybrid value/reference semantics (as in C++ with move semantics; rejected)**: introduces a complex taxonomy (lvalue, rvalue, xvalue, prvalue, glvalue) that adds far more cognitive load than Khayyam's simple reference model.

##### Prior art
Java's reference semantics for objects are superficially similar, but Java still uses assignment (`=`) and has a separate primitive type system that uses value semantics. Khayyam's model is more uniform: everything is a reference, and there are no primitives at the language level.

##### Unresolved questions
- How the reference model interacts with the resource management layer for lifecycle enforcement is a separate concern addressed by future RFCs.

##### Future possibilities
None recorded yet.

### Variable Scope and Visibility
Variables in Khayyam can be declared at two distinct scopes:

1. **File-level variables**: declared at the top level of a `.kh` file. These serve as module-level constants, singletons, or shared configuration values. A file-level variable is accessible within its own file and can be imported by other files via the `in` keyword.

2. **Method-body variables**: declared inside a method's body. These are local references that exist for the duration of the method's execution. They are not accessible outside the method and cannot be imported by other files.

The `in` keyword serves as the import mechanism for file-level variables from other files:

```khayyam
vr MaxTimeout in "net/config"
```

Since Khayyam treats the file system as the ultimate source of truth (avoiding abstract concepts like namespaces or packages), the import path is a literal file path. The imported variable name is the same as the name declared in the source file, maintaining referential transparency.

This scoping model reinforces the language's single-responsibility principle at the file level: because files are the unit of import, and because each import targets a specific named variable, developers are naturally encouraged to keep files small and focused, with each file exporting only the variables that belong to its domain.

#### Discussion

##### Drawbacks
The file-as-module model means that a file with many exported variables can become a large import surface, and there is no mechanism to import "all variables from a file" — each variable must be imported individually. This is intentional (it makes dependencies explicit) but may feel verbose for files that export many related constants.

##### Rationale and alternatives
- **Namespace-based imports (as in Python `from X import *`; rejected)**: hides which specific variables are used and creates namespace pollution, contradicting the explicitness principle.
- **Package-level imports (as in Java/C#; rejected)**: introduces an abstract naming layer (package names) that is separate from the file system, creating a mapping problem between the import name and the physical file location.

##### Prior art
Go's import model is the closest mainstream prior art, importing at the package level but requiring explicit use of the package name to access exported identifiers. Khayyam's model is more granular: each import targets a specific named variable from a specific file.

##### Unresolved questions
- Whether a file can export a variable under a different name than its declaration name (aliasing) is not currently addressed.

##### Future possibilities
None recorded yet.

### Self-Documenting Code and No Magic Numbers
In traditional languages, developers often write raw formulas like `if a == b + 1` and rely on comments to explain what `1` means. Khayyam forces developers to eliminate magic numbers by requiring that every value be wrapped in a named capsule with a descriptive name. By declaring an explicit variable for `1` with a descriptive name before using it in a method call, the code becomes inherently self-documenting at the declaration site, eliminating the need for redundant comments.

Because variables require explicit types, the source code preserves the concepts introduced during modeling. A variable declaration should reveal a domain concept, not merely a machine representation. This is the variable-level manifestation of Khayyam's broader self-documenting architecture principle (documented in the Design Philosophy RFC).

#### Discussion

##### Drawbacks
The boundary between "enforced clarity" and "forced verbosity" is not always clear. A capsule called `RetryCounter` adds clarity; a capsule called `LoopIndex` may not. The language does not currently provide a mechanism for teams to adjust this boundary — it is enforced uniformly by the grammar.

##### Rationale and alternatives
- **Allow magic numbers with mandatory comments (rejected)**: comments can drift out of sync with the code, and a comment does not provide the compiler or linter with a name to enforce consistency across uses.
- **Linter rule rather than language-level constraint (considered, not chosen)**: lint rules can be disabled or ignored at the organizational level, weakening the architectural safeguard.

##### Prior art
Domain-Driven Design as formulated by Eric Evans advocates for rich domain models and the elimination of "primitive obsession," but leaves enforcement to developer discipline. Khayyam encodes this discipline into the language grammar itself, making it structurally difficult to violate.

##### Unresolved questions
1. Where is the boundary between "enforced clarity" and "forced verbosity"? When does a domain-specific capsule name become unnecessary indirection?
2. Should Khayyam provide a linter rule or a compiler directive that allows teams to define their own boundaries for this trade-off?

##### Future possibilities
A linter rule that detects capsule names that are unlikely to carry domain meaning (e.g., names that are synonyms for primitive operations like `Counter`, `Index`, `Flag`) and suggests merging them into their parent capsule's domain.

### Constants as Capsule-Returned Values
The constant model in Khayyam is fully specified in RFC 495592 ([Encapsulation in Khayyam](./khayyam-encapsulation.md), section "Constants as Capsule-Returned Values"). In summary: a constant is a variable returned by a capsule method that cannot change after first initialization — an organizational and architectural rule enforced by the capsule's own design (not exposing a mutating method), not by a dedicated compiler keyword. From the variable's perspective, a constant is declared and initialized like any other variable; the immutability guarantee is inherited from the capsule's behavioral contract.

### Resource Lifecycle (Deferred)
The storage model and resource lifecycle for variable-backed instances are implementation concerns, not variable-syntax concerns. A variable does not need to know whether its instance lives in an Arena, a Pool, or on the stack — that is a governance decision, not a syntax concern.

This topic — including memory allocation, deallocation, garbage collection alternatives, and resource management ADTs — is deferred to a future RFC on resource management.

#### Discussion

##### Drawbacks
Developers accustomed to garbage-collected languages (Go, Java, C#) will eventually need to engage with explicit resource management. The specifics of that engagement are not a variable-level concern.

##### Rationale and alternatives
- **Garbage collection (as in Go, Java; rejected)**: introduces unpredictable pause times and hidden runtime overhead, contradicting Khayyam's principle of making all behavior explicit and predictable.
- **Explicit resource management (Khayyam's intended approach)**: makes resource lifecycle a visible, predictable, and auditable part of the program's architecture. The precise mechanism is deferred to a future RFC.

##### Prior art
Rust's ownership model is the closest mainstream prior art in terms of explicit resource management. The specific approach Khayyam will take is not yet specified.

##### Unresolved questions
- The precise resource management model, API surface, and interaction with variable declarations is deferred to a future RFC.

##### Future possibilities
None recorded yet.

## Discussion

### Naming Conventions
Variable names in Khayyam should reflect their domain purpose, not their type or implementation detail. Because every variable already carries an explicit type annotation, the name is free to focus on the *why* rather than the *what*. Suggested conventions (non-binding, enforceable via linter configuration):

- **Domain-meaningful names**: `vr MaxRetries W8` is preferred over `vr Count W8` or `vr N W8`.
- **No type-redundant prefixes**: since the type is always explicit, Hungarian-notation-style prefixes (`vr intCount W8`) are unnecessary and discouraged.
- **Constant-like variables**: file-level variables that serve as module constants should use PascalCase (e.g., `vr MaxTimeout Duration`), matching the capsule naming convention.

### Drawbacks
The variable model's insistence on explicit types, no assignment operators, and no multi-declaration syntax creates a measurably more verbose declaration experience than virtually every modern language. For every variable, the developer must write a separate declaration line with an explicit type, and then a separate initialization line via a method call. This verbosity is the price of guaranteed readability and domain integrity — but it is a real price, and it is felt most acutely during rapid prototyping or when writing boilerplate-heavy code.

### Rationale and alternatives
- **Combine declaration and initialization (rejected)**: would require an assignment operator, conflicting with the no-assignment rule and its aliasing-prevention benefits.
- **Allow type inference for "obvious" cases (rejected)**: the boundary of "obvious" is subjective and creates inconsistency; see [No Type Inference](#no-type-inference).
- **Allow multi-declaration for same-type variables (rejected)**: would compress distinct variables into a single line, violating the one-visible-step-per-statement principle; see [Variable Declaration Syntax](#variable-declaration-syntax).

### Prior art
Rust's `let` with optional `mut` is the closest mainstream variable model, though it allows type inference and uses `=` for assignment. Go's `var` declaration with explicit type is syntactically similar to Khayyam's `vr`, but Go allows `:=` short declarations and assignment operators.

### Unresolved questions
1. Should the linter provide an auto-fix mode that converts multi-declaration syntax (if encountered in migrated code) into separate `vr` declarations?
2. How does the variable model interact with the Memar framework's governance layer — are there framework-specific rules for variable naming, scoping, or lifecycle that extend beyond the language-level rules documented here?

### Future possibilities
- A migration tool that automatically converts variable declarations from other languages into Khayyam's `vr` syntax, handling the separation of declaration and initialization.
- A linter rule set for variable naming conventions, configurable per organization, that enforces the domain-meaningful naming principle at the project level.

## Change Rationale
