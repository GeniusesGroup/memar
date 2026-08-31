---
Title: "Khayyam - Programming Language"
Status: Proposed
Start Date: "2020-02-02"
ID: "484848"
---

# Khayyam - Programming Language
This language is ideal for developers who want clean, spoken code capable of writing high-performance libraries and applications without fighting the compiler.

## Abstract
**Core Philosophy: Separation of Syntax and Governance.** Khayyam is built on radical approaches (*Grammar Atomicity*, *Zero-Magic Core*, *Strict Separation of Concerns*, ...) to minimalism. It strictly defines *how* code is structured (the syntax) but intentionally delegates *how* code behaves under the hood (such as memory management, strict architectural constraints, execution policies, ...) to Compilers, Linters, and Organizational Frameworks (like the Memar framework).

This philosophy ensures the language core remains pure, un-opinionated, and future-proof. Khayyam provides the foundational building blocks, empowering organizations to enforce their own best practices through custom linter rules rather than syntactic dictatorships.

## Introduction

### Motivation
A language that bakes architectural opinions into its grammar forces every project using it to inherit those opinions, whether or not they fit. Khayyam's motivation is to give developers clean, spoken code and high-performance libraries and applications without fighting the compiler — while keeping the language itself small enough that it never becomes the thing a project has to work around. What the language strictly owns (syntax) and what it deliberately hands off (behavior, governance, architectural constraint) is the central design question every section below answers for one specific construct.

Multiple design discussions across Khayyam's evolution converged independently on the same small set of recurring principles — behavior over type identity, domain modeling as a first-class concern, and the separation of syntax from governance — well before they were ever written down together in one place. The sections below are that convergence, made explicit: a single reference point for principles that had previously only existed as separately-rediscovered reasoning across many separate conversations.

### Methodology
This document gives a general, syntax-level overview of Khayyam — enough to read and write valid code. It is deliberately not exhaustive: the reasoning behind each construct, the alternatives considered, and currently open questions live in companion documents, linked inline wherever a construct has one of its own. The approach has been to keep this specification itself short and link outward, rather than grow one very long document that tries to hold both the syntax and its full justification.

Where a construct's design draws on a deliberate comparison against other languages' choices — grounded, where possible, in the wider computer-science literature rather than informal preference — that comparison lives in the relevant companion document's own Prior art section (see, for example, [Abstraction in Khayyam](./khayyam-abstraction.md)'s comparison against Go, Rust, Java, TypeScript, Zig, and Haskell), not repeated here.

## Explanation

### File Extension
We choose `.kh` for files that have Khayyam language code.

### Keywords
Khayyam fundamentally relies on only two primary top-level concepts for declaration and importing: Types (`tp`), Variables (`vr`).

#### Language Keyword in a Glance
|    Top level    |       types        |
| :-------------: | :----------------: |
|   `tp` (type)   |   `in` (include)   |
| `vr` (variable) |   `cp` (capsule)   |
|                 |   `mt` (method)    |
|                 | `ab` (abstraction) |
|                 |    `sc` (scope)    |

### Import Mechanism (`in`)
Khayyam treats the file URI system as the ultimate source of truth (a URI addressing scheme for locating source, not a dependency on any particular filesystem's broader feature set — no directory permissions, watches, or other OS-level filesystem semantics are implied), avoiding abstract concepts like `namespace` or `package`. The `in` keyword is used as a routing operator to include entities from other files. Since capsules (`cp`), abstractions (`ab`), and methods (`mt`) are all fundamentally types, the import syntax remains strictly orthogonal:

In this manner devs are forced to write very short codes in each file to respect single responsible codes.

- **Type Inclusion:** `tp {name} in "{path}"`
  - *Example:* `tp TcpConn in "net/tcp"` (Imports a capsule, abstraction, or method type)
  - *Example:* `tp ErrServiceNotFound in "memar/process/services/errors/service-not-found.kh"` without need to indicate a name to call them, e.g. `err.CopyFrom(ErrServiceNotFound)(err)` (statement form; `=` does not exist in Khayyam)
- **Variable Inclusion:** `vr {name} in "{path}"`
  - *Example:* `vr MaxTimeout in "net/config"` (Imports a specific variable, constant, or singleton)

> **Name collision is an architecture error, not a language disambiguation problem.** If two external dependencies export the same name (e.g., both export `Error`) and a single file needs both, Khayyam provides no `as` alias syntax. That silence is deliberate. A collision signals that two abstractions claim to own one concept — the correct fix is not a wrapper or adaptor at the import site but a root-cause redesign so that one abstraction is the single owner of that concept. Where a temporary workaround is unavoidable, wrap one dependency in a local capsule (composition) rather than aliasing it; aliasing preserves the duplicated abstraction and, as the author noted, “becomes the dirty mental model of the developer who keeps reaching for unsustainable solutions.” Tooling/versioning (which file URI resolves to which version) is a build/tooling-layer concern, not a syntax concern, and therefore does not appear here.

### Type
Type or data type is a subdivision of a particular kind of things. All things MUST be defined in the shape below to be understood by the Khayyam compiler.
```khayyam
tp {name} [Type] [subtype defined value]
```

#### Capsule
Khayyam allows developers to indicate first-level [encapsulation-pattern](./khayyam-encapsulation.md) by using `cp`.
- `tp {name} cp { ___ }`
- Capsule structure CAN include some other data types inside itself.
- Each field in a capsule is written as `fieldName fieldType` on each line.
- Khayyam only allows access to inner data types via methods (functions). There are no data fields to expose.

#### Method
[Method in Khayyam](./khayyam-method.md) is itself a type. In Khayyam, functions and methods are not separate concepts. By using the `mt` subtype, developers define an executable behavior and attach it to a type. The owner type is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`).

- `tp {name} mt (self {owner}) (influencing variables...) (influenced variables...) { }`
- **Pass-by-Reference & State Protection:** All arguments passed into a method and all values returned from a method are passed strictly by reference. See [Memory Model in Khayyam](./khayyam-memory_model.md) for the full rationale.
- **Inherent Encapsulation:** Even though capsules are passed by reference, their internal state remains strictly protected. Because Khayyam enforces that all data fields are entirely hidden, a receiving method cannot directly mutate the passed capsule's fields. State mutation can ONLY occur if the passed capsule explicitly exposes a behavior (method) that allows it, rendering keywords like `const` or `mut` architecturally obsolete.
- Devs MUST separate `type_owner`, `efficacy (args)`, and `impressible (returns)` by using `()` to indicate all of them even when empty. Consider that all of them are the same in underlying layers, and this rule is just to improve code readability.
- Devs CAN write pure standalone functions in this way; there is no limitation.
- Dev can use any naming for type owner naming, BUT suggest using `self` as the base point to other members in the type.
  - `tp Set mt (self Key) (key String) (err Error) {}`
- **Body-less Methods (FFI & Contracts):** A method can be defined without a body (`{}`). This is legitimately used in two scenarios:
  - Contract Definition: Defining the required signature for an abstraction (`ab`).
  - Foreign Function Interface (FFI): When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file). See [Khayyam Compiler Directives](./Khayyam-compiler.md) for the compiler-side handling.

##### Method Invocation Rules
- **Uniform Invocation Syntax:** Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.
- **Context-Driven Semantics:** The distinction between static behavior and instance behavior is governed by the presence of the `self` reference in the method signature, enforced by the compiler (not the linter):
  - **Type-Level (Static) Invocation:** Methods defined without a `self` reference belong to the type's blueprint. They MUST be invoked directly through the type identifier (e.g., `tp.Create()`). Invoking a type-level method on a variable instance (`vr.Create()`) is a compile-time error.
  - **Instance-Level Invocation:** Methods defined with a `self` reference require an active memory capsule. They MUST be invoked through a variable instance (e.g., `vr.Mutate()`). Invoking an instance-level method directly on the type identifier (`tp.Mutate()`) is a compile-time error.


#### Abstraction
[Abstractions in Khayyam](./khayyam-abstraction.md) are pure contracts. They do not contain logic, state, or even predefined method bodies. The methods that fulfill this contract are defined entirely outside the abstraction. To mirror the robust composition patterns found in systems engineering, Khayyam supports **Abstraction Composition** via a dedicated scope block `{}` at the type definition site.

- `tp {name} ab { {Composition of Abstractions} }`
- Abstractions MUST use other abstractions as arguments or returns, not other `capsule`s.
- **No Generic Syntax:** We do not introduce syntax complexity for [Polymorphism or Generics](./khayyam-polymorphism.md) (like `<T>` in C# or `[T]` in Go). Khayyam inherently supports **Covariant Return Types**. If an abstraction dictates a method must return Abstraction `A`, a capsule can implement this method by returning Capsule `B` (as long as `B` implements `A`).
- **Smart Compilation:** The compiler decides smartly whether to handle these abstractions at compile-time (Monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (via dynamic dispatch/interfaces when underlying capsules are hidden), entirely freeing the developer from generic syntax management.

Examples:
```khayyam
// Defining a pure abstraction
tp Reader ab

// The methods belonging to this abstraction are defined independently
tp Read mt (self Reader) (data Element) (err Error)
tp Close mt (self Reader) () (err Error)
```

```khayyam
// An abstraction can embed other abstractions within its block to declare a sub-typing/contractual dependency:
tp Error ab {
    DataType
    Field_MediaType
    ADT
}
```

#### Scope
- `tp {name} sc { ___ }`
- Scope is an area in which something acts or operates or has power or control.
- Code scope is used in many logic methods like `IF`, `LOOP`, `GOTO`, ... See [Control Flow in Khayyam](./khayyam-control_flow.md) for how these are built as libraries within this mechanism, not language keywords.
- Code scope MUST be used only inside a method body.

### Variable
See [Variable in Khayyam](./khayyam-variable.md) for the full rationale behind these constraints.
- `vr {name} {type}`
- Like other programming languages, the `vr` keyword is used to declare a variable. However, **Variables in Khayyam are strictly Logical References** to a type's instance, never the raw data block itself.
- **No Implicit Copying & No Assignment Operators:** Khayyam completely eliminates assignment operators (like `=`). Passing a variable to a method ALWAYS passes the reference. The language natively prevents any implicit deep or shallow copying, ensuring zero hidden memory allocation overhead.
- If a deep copy or state duplication is logically required, it MUST be done explicitly via the capsule's behavior. The developer must declare a new variable and invoke a method (e.g., `vr newVar Type`, followed by `newVar.CopyFrom(oldVar)`).
- Variables CAN be declared in files and method bodies.

### Khayyam Is Not Its Own Compiler or Runtime
Khayyam, as a sub-framework, defines a design space for expressing Memar's constraints in source form — explicit state, explicit error paths, no hidden control flow. It does not follow from this that Khayyam must also provide its own compiler or runtime as part of what Khayyam *is*.

Building a compiler or runtime is a separate concern with its own design space, its own trade-offs, and its own failure modes. Folding it into Khayyam's own scope creates a well-documented failure pattern seen across many language projects: once a language project owns compiler and runtime implementation, every new developer-convenience request becomes pressure to add syntax, special cases, or built-in magic to make that convenience possible — because the team that controls the language spec is the same team that feels the pain of not having the convenience. Over time this erodes the "no hidden control flow, no implicit behavior" principle that Khayyam exists to protect — protection that has to come from the inside, from the people most invested in protecting it.

Keeping compiler and runtime implementation outside Khayyam's own scope as separate systems that consume Khayyam's specification, built by teams whose incentives are implementation correctness and performance rather than syntax convenience — is therefore not an incidental scoping choice. It is a structural safeguard against the specific failure mode described above.

This has a direct consequence for how Khayyam's own documents should be scoped: a proposal to add syntax "to make the compiler's job easier" or "because other languages do it this way" is, by this principle, a signal to examine the proposal skeptically rather than a reason to adopt it. The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" still needs worked examples before this can be considered settled — see Unresolved questions.

### Separation of Syntax and Governance: A Principle

**Principle:** *Syntax defines what exists* (ontology: which types, values, and relationships a program may mention). *Governance defines how instances flow* (policies about lifecycle, error routing, and architectural constraints on those instances). The compiler enforces the first; the linter/framework enforces the second. This line is not “syntax is small vs. linter is big” — it is *what* vs. *how*.

- **Syntax (compiler-enforced):** Whether a type, value, or relationship may appear at all. Examples: “a bare numeric literal `41` may not appear as a value without a named capsule” (claiming existence of an unmodeled value), “a static method must be called on the type, an instance method on a variable” (which entity a name resolves to), “all fields are private, access only via methods.”
- **Governance (linter/framework-enforced):** Policies about how already-well-typed instances move through the program. Examples: memory safety / `Deinit()`-path coverage, error-inspection discipline, code-scope naming conventions, orphan-rule for cross-file extension, architectural constraints like “no `Utils` capsules.”

A decision that *creates* or *denies* existence belongs in syntax precisely because a linter rule can be disabled — disabling a syntax rule changes what programs exist; disabling a governance rule changes how well they are kept. This is why `khayyam-variable.md` rejects moving the magic-number ban to the linter (“lint rules can be disabled, weakening the safeguard”) while `khayyam-memory_model.md` accepts linter-enforcement for memory safety — the former denies existence of unmodeled values, the latter polices flow of already-typed instances.

### Behavior Over Type Identity
Traditional generic systems frequently focus on type identity — `T`, `K`, `V` — as the central mechanism for abstraction. Khayyam instead emphasizes required behavior: the essential question is "what capabilities are required?" rather than "what concrete type is this?" This recurred across discussions of generics, parametric polymorphism, containers, algorithms, and infrastructure components alike, and is one of the reasons behind the No Generic Syntax rule under Abstraction, above. See [Abstraction in Khayyam → Behavior Over Type Identity](./khayyam-abstraction.md#behavior-over-type-identity) for the full treatment, including why several canonical parametric-polymorphism patterns (`identity<T>()`, `Option<T>`, `Result<T,E>`) are tied to constraints other languages have that Khayyam does not.

### System-Modeling Language Philosophy
The more Khayyam evolves, the less it appears to be a traditional programming language and the more it resembles a system-modeling language. This distinction may ultimately become one of Khayyam's defining characteristics.

Many language designs begin by collecting useful features and combining them into a coherent syntax: OOP, Generics, Pattern Matching, Functional Constructs, Traits / Interfaces, Reflection, and Meta-programming. Khayyam appears to follow a different path. Instead of asking "What features should a language provide?", it asks "What architectural principles should a long-lived system follow?" and then derives language constructs from those principles.

This distinction is not merely philosophical. It has concrete implications for every design decision in the language, from how polymorphism works to how compilation is structured. A traditional language optimizes for feature completeness; Khayyam optimizes for architectural integrity over time.

#### Long-Term Architectural Potential
One of the strongest aspects of Khayyam is its apparent focus on preventing architectural decay. Many language features optimize for short-term convenience. Khayyam often appears willing to accept additional modeling effort if it improves system clarity, domain integrity, architectural longevity, and maintainability over decades. This is unusual among modern languages and represents a deliberate trade-off that prioritizes the sustainability of large-scale systems over the speed of small-scale prototyping.

#### Discussion

##### Drawbacks
A system-modeling approach inherently demands more upfront design investment. Developers accustomed to rapid prototyping in dynamically typed or feature-rich languages may find the initial modeling overhead excessive, particularly for small projects or proof-of-concept work where long-term architectural integrity is irrelevant.

##### Prior art
The idea of a language derived from architectural principles rather than feature collections has precedents in restricted domains — for example, Erlang's design from telecommunications reliability requirements, or Verilog's design from hardware modeling needs. Khayyam's ambition is to apply this principle more broadly to general-purpose system software.

##### Unresolved questions
1. Is the system-modeling language framing the right way to position Khayyam externally, or does it create confusion with actual modeling languages (UML, Alloy) that serve a different purpose?
2. At what project size does the architectural integrity trade-off begin to pay for itself?

### Self-Documenting Code and Naming
In most languages, naming is a style preference. In Khayyam, it is enforced by the language itself: magic numbers are forbidden, primitives must be wrapped in named capsules (`W32`, not `int`), and generic containers are replaced by domain-specific names (`UserRegistry`, not `Map<ID, User>`).

This means that in a Khayyam codebase, it is structurally impossible to write opaque code even if a developer tries. The language grammar makes the architect's intent visible at every call site.

This is not a one-time mechanism to be decided and then documented elsewhere — it is an ongoing tension that recurs every time a new naming rule, keyword, or grammar constraint is considered. Because of that, it stays part of this document, the same document every new construct is considered against, rather than being extracted into a separate style-guide document that would only drift from whatever this document actually specifies.

#### Discussion

##### Unresolved questions
1. Where is the boundary between "enforced clarity" and "forced verbosity"? When does a domain-specific capsule name become unnecessary indirection? A capsule called `RetryCounter` adds clarity; a capsule called `LoopIndex` may not.
2. Should Khayyam provide a linter rule or a compiler directive that allows teams to define their own boundaries for this trade-off?

### Syntactic Atomicity and Semantic Clarity
Khayyam is designed around the principle that language constructs should communicate intent as explicitly and unambiguously as possible. This idea is explored through **syntactic atomicity**: each syntactic construct should correspond to a single semantic intent, and each semantic intent should preferably be represented by a single syntactic construct.

The primary goal is semantic clarity rather than AI assistance. By reducing ambiguity, implicit conventions, overloaded meanings, and context-dependent interpretation, Khayyam seeks to make architectural intent easier to understand, reason about, validate, transform, and maintain. These benefits are expected to apply broadly to humans, compilers, analysis tools, verification systems, and machine-assisted reasoning systems alike. This remains a design hypothesis requiring empirical validation.

Like naming, this is not a topic with a single decision to be made once and filed elsewhere — it is the principle applied every time a new keyword, syntactic form, or grammar rule is proposed for Khayyam. It stays here for the same reason.

#### Discussion

##### Unresolved questions
1. What level of syntactic atomicity provides meaningful benefits without introducing excessive verbosity? Highly regular, atomic syntax can feel verbose to experienced developers who rely on implicit conventions — where is the boundary between clarity and unnecessary ceremony?
2. How can syntactic atomicity be measured objectively?
3. Which forms of ambiguity are most harmful to long-term system maintainability?

### Domain Modeling Principles
Khayyam pushes development in the opposite direction of most modern languages when it comes to domain modeling. Where other languages claim to support Domain-Driven Design but whose abstractions frequently collapse into generic containers and primitive types — `List<User>`, `Map<String, Object>`, `Dictionary<string, any>` — Khayyam encourages domain-specific concepts: `UserRegistry`, `ConnectionIndex`, `ServiceCatalog`, `PermissionStore`.

#### Resistance to Primitive Obsession
Large systems often accumulate thousands of values represented as `string`, `int`, and `bool`, while each instance carries completely different business meaning. Khayyam's emphasis on capsules and explicit modeling naturally pushes developers away from this pattern. This is not merely a typing preference; it is an architectural safeguard. By requiring all values to be wrapped in named capsules, the language ensures that business meaning is never lost to primitive types.

#### Resistance to Utility-Oriented Architecture
Many mature codebases eventually develop structures such as `Helpers`, `Utils`, `Common`, `Shared`, and `Base`, which become architectural dumping grounds. Khayyam's modeling style appears to discourage this evolution. Responsibilities are expected to live within meaningful capsules rather than generic utility containers. The language's import mechanism and single-responsibility file conventions reinforce this by making it natural to organize behavior around domain concepts rather than around utility categories.

#### Discussion

##### Drawbacks
The domain modeling approach demands that developers invest time in naming and structuring types before writing behavior. For developers accustomed to starting with functions and extracting types later, this represents a workflow inversion that may slow initial development velocity.

##### Rationale and alternatives
- **Allow generic containers alongside domain-specific capsules (rejected)**: this would immediately re-open the door to the primitive-obsession and utility-dumping patterns that Khayyam's design explicitly aims to prevent.
- **Provide a lint rule rather than a language-level constraint (considered, not chosen)**: lint rules can be disabled or ignored at the organizational level, weakening the architectural safeguard.

##### Prior art
Domain-Driven Design as formulated by Eric Evans advocates for rich domain models, but leaves enforcement to developer discipline. Khayyam encodes this discipline into the language grammar itself, making it structurally difficult to violate.

### Naming
Khayyam takes its name from [Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) (1048–1131), a Persian polymath: mathematician, astronomer, philosopher, and poet.

The connection is not simply that a Persian project chose a well-known Persian name. Three parts of Omar Khayyam's actual work echo choices this language makes:

- **Solving from first principles, not from precedent.** Omar Khayyam's treatment of cubic equations found general geometric solutions rather than accumulating special-case tricks for each equation shape — the same posture behind this language's *Grammar Atomicity* and *Zero-Magic Core*: deriving a small set of constructs from architectural principles, rather than assembling a feature collection because other languages have those features.
- **Precision that outlasts its own era.** Omar Khayyam's reform of the Persian calendar (the basis of the modern Jalali calendar) was, by some measures, more accurate than the Gregorian calendar introduced nearly five centuries later — achieved through careful observation, not additional complexity. This language's willingness to accept more upfront modeling effort in exchange for architectural integrity over decades follows the same trade: precision paid for once, holding up over a long horizon.
- **Skepticism of received answers.** Omar Khayyam's poetry is remembered, in part, for a willingness to question inherited certainty rather than repeat it. This language's own recurring design instinct — that a proposal to add something merely because other languages do it that way is a signal to examine the proposal more skeptically, not a reason to adopt it — is the same posture applied to language design.

None of this is a claim that the language was engineered to match the man point for point. It is closer to the reverse: the name was available, it fit, and looking closely at why it fits is worth doing once, here, rather than leaving it as a passing choice of etymology.

## Results

## Discussion

### Drawbacks
This document now combines finalized syntax and semantics with the philosophical and architectural reasoning behind them, after absorbing what previously lived in a separate design-philosophy document. Combining both in one place risks the same duplication problem that separation was originally meant to prevent: a construct's rationale, once stated here, must not also be restated — and risk drifting out of sync — in that construct's own dedicated document (e.g. [Abstraction in Khayyam](./khayyam-abstraction.md), [Method in Khayyam](./khayyam-method.md)). This document manages that risk the same way those documents manage their own overlaps with each other: state a topic once, in the place closest to where a reader would look for it, and link to it from everywhere else rather than restating it.

### Rationale and alternatives
- **Keep a separate philosophy document (original approach, reversed)**: Khayyam previously split the canonical specification from a separate document holding the recurring architectural principles and design tensions behind it. In practice this created the same duplication risk splitting was meant to avoid — technical claims in the philosophy document could drift out of sync with the dedicated documents where those mechanisms were actually decided, which happened concretely once, when an earlier draft of that document restated an error-propagation question already substantially addressed elsewhere. The document was retired and its content merged back here and into each construct's own dedicated document, rather than trying to patch the split further. See this document's own changelog for the full provenance of what moved where.
- **Keep philosophy and syntax reference as two documents indefinitely, accepting the drift risk (rejected)**: rejected once a second, independent failure of the same kind (this document's own now-superseded "Behavior Over Type Identity"/"Reassessment of Parametric Polymorphism" sections had drifted out of sync with the more developed version already migrated to `khayyam-abstraction.md`) confirmed the risk was recurring, not a one-time accident.

### Prior art
Rust's design philosophy documents and Go's "Go Proverbs" serve a similar purpose of capturing design intent alongside technical specification, generally as separate documents from the language reference itself. Khayyam's own experience with that split — the drift described above — is a data point specific to this project, not a general argument against the pattern; other projects may find the split works well for them.

### Unresolved questions
1. The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" (see *Khayyam Is Not Its Own Compiler or Runtime*, above) still needs worked examples before it can be considered settled.
2. Now that philosophy and syntax reference live in one document, is there a size or complexity threshold at which splitting a specific topic back out into its own dedicated document becomes worthwhile, the way *Behavior Over Type Identity* already points to [Abstraction in Khayyam](./khayyam-abstraction.md) rather than restating it here?

### Future possibilities
None recorded at this time.
