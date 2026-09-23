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

Where a construct's design draws on a deliberate comparison against other languages' choices — grounded, where possible, in the wider computer-science literature rather than informal preference — that comparison lives in the relevant companion document's own paired changelog (see, for example, [Abstraction in Khayyam](./abstraction.changelog.md)'s comparison against Go, Rust, Java, TypeScript, Zig, and Haskell, recorded under Related work), not repeated here.

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

In this manner devs are forced to write very short codes in each file to respect single responsible codes. A file is meant to be read contracts-first: inclusion and type declarations before method bodies. Companion tooling may fold those declaration blocks and bodies so that order is the default view; that assist is [Linter → Tooling may present structure first](../protocols/linter.md#tooling-may-present-structure-first), not grammar.

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
Khayyam allows developers to indicate first-level [encapsulation-pattern](./encapsulation.md) by using `cp`.
- `tp {name} cp { ___ }`
- Capsule structure CAN include some other data types inside itself.
- Each field in a capsule is written as `fieldName fieldType` on each line. A one-token line in the same block is a bare abstraction name: the capsule composes that abstraction, the same shape an `ab` block uses for composition. What the named abstraction then requires is that abstraction's own specification ([Encapsulation → Capsule Structure and Privacy](./encapsulation.md#capsule-structure-and-privacy)).
- Khayyam only allows access to inner data types via methods (functions). There are no data fields to expose.

#### Method
[Method in Khayyam](./method.md) is itself a type. In Khayyam, functions and methods are not separate concepts. By using the `mt` subtype, developers define an executable behavior and attach it to a type. The owner type is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`).

- `tp {name} mt (self {owner}) (influencing variables...) (influenced variables...) { }`
- **Pass-by-Reference & State Protection:** All arguments passed into a method and all values returned from a method are passed strictly by reference. Explicit copy is a capsule method, not an assignment operator — see [Variable in Khayyam](./variable.md). The protocol-level copy and teardown rules this grammar realizes are in [Memory](../protocols/memory.md).
- **Inherent Encapsulation:** Even though capsules are passed by reference, their internal state remains strictly protected. Because Khayyam enforces that all data fields are entirely hidden, a receiving method cannot directly mutate the passed capsule's fields. State mutation can ONLY occur if the passed capsule explicitly exposes a behavior (method) that allows it, rendering keywords like `const` or `mut` architecturally obsolete.
- Devs MUST separate the owner, the influencing variables, and the influenced variables by using `()` to indicate all of them even when empty. Consider that all of them are the same in underlying layers, and this rule is just to improve code readability. The groups are the ones in the signature pattern above, defined in [Method in Khayyam → Influencing and Influenced Variables](./method.md#influencing-and-influenced-variables-not-inputs-and-outputs).
- The owner group names the parent type. `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`.
- Dev can use any naming for type owner naming, BUT suggest using `self` as the base point to other members in the type.
  - `tp Set mt (self Key) (key String) (err Error) {}`
- **Body-less Methods (FFI & Contracts):** A method can be defined without a body (`{}`). This is legitimately used in two scenarios:
  - Contract Definition: Defining the required signature for an abstraction (`ab`).
  - Foreign Function Interface (FFI): When the receiver is a concrete capsule (`cp`), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly `.s` or C `.o` file). See [Compiler](../protocols/compiler.md).

##### Method Invocation Rules
- **Uniform Invocation Syntax:** Khayyam strictly uses a single dot (`.`) operator for all method calls. The language intentionally rejects secondary tokens (such as `::`) to maintain syntax minimalism.
- **Context-Driven Semantics:** The owner group names the parent type. Both call groups are written.
  - **Call on the parent type:** `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)` is called `W32.Sum(a, b)(total, err)`. The body does not invoke `self`.
  - **Call on a variable of the parent type:** `tp Set mt (self Key) (value String) (err Error)` is called `k.Set(value)(err)`. When the parent type is a method, the receiver is that method ([Method → A method implements an abstraction by methods of its own](./method.md#a-method-implements-an-abstraction-by-methods-of-its-own)).


#### Abstraction
[Abstractions in Khayyam](./abstraction.md) are pure behavioral specifications. They do not contain logic, state, or even predefined method bodies. The methods that fulfill this specification are defined entirely outside the abstraction. To mirror the robust composition patterns found in systems engineering, Khayyam supports **Abstraction Composition** via a dedicated scope block `{}` at the type definition site.

- `tp {name} ab { {Composition of Abstractions} }`
- Abstractions MUST use other abstractions as arguments or returns, not other `capsule`s.
- **No Generic Syntax:** We do not introduce syntax complexity for [Polymorphism or Generics](./polymorphism.md) (like `<T>` in C# or `[T]` in Go). Khayyam inherently supports **Covariant Return Types**. If an abstraction dictates a method must return Abstraction `A`, a capsule can implement this method by returning Capsule `B` (as long as `B` implements `A`).
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
// An abstraction can embed other abstractions within its block to declare a sub-typing/behavioral dependency:
tp Error ab {
    DataType
    Field_MediaType
    ADT
}
```

#### Scope
- `tp {name} sc { ___ }`
- Scope is an area in which something acts or operates or has power or control.
- A code scope is inert until a library-provided method drives it: the grammar ships no control-flow keywords or logical operators of its own. See [Control Flow](../protocols/control-flow.md) for how flow constructs are built as libraries within this mechanism.
- Code scope MUST be used only inside a method body.
- Each command ends with a new line. There is no `goto` keyword: a compiler of this language lowers `sc`-driven branches to internal jumps, and `return` is an IR marker that must itself end with a line break so it cannot be written as `return 0`. That lowering is a realization of [Compiler → The compiler recognizes language primitives, not library names](../protocols/compiler.md#the-compiler-recognizes-language-primitives-not-library-names), not a grammar keyword.
- An argument position may be satisfied by a `vr` of the declared type or, for `sc` and `mt`, by the type itself passed as a type-level argument. See [Method → Type-level arguments for `sc` and `mt`](./method.md#type-level-arguments-for-sc-and-mt).

### Variable
See [Variable in Khayyam](./variable.md) for the full rationale behind these constraints.
- `vr {name} {type}`
- Like other programming languages, the `vr` keyword is used to declare a variable. However, **Variables in Khayyam are strictly Logical References** to a type's instance, never the raw data block itself, and never a raw machine pointer.
- **No `nil` / `null` keyword:** the grammar has no universal nullability token. Absence, when a type can represent it, is a method on that type's contract — conventionally `IsNull()` — realizing [Memory → Absence is a type's contract](../protocols/memory.md#absence-is-a-types-contract-not-a-universal-machine-condition).
- **No Implicit Copying & No Assignment Operators:** Khayyam completely eliminates assignment operators (like `=`). Passing a variable to a method ALWAYS passes the reference. The language natively prevents any implicit deep or shallow copying, ensuring zero hidden memory allocation overhead.
- If a deep copy or state duplication is logically required, it MUST be done explicitly via the capsule's behavior. The developer must declare a new variable and invoke a method (e.g., `vr newVar Type`, followed by `newVar.CopyFrom(oldVar)`).
- Variables CAN be declared in files and method bodies.

### How Khayyam realizes Memory
[Memory](../protocols/memory.md) owns the language-independent requirements. This language meets them without growing memory-management syntax:

- **No lifetime annotations.** The grammar has none. Correctness of lifetimes is obtained from sovereign encapsulation (no leaking raw internal references), deterministic `sc` boundaries, the absence of syntax-level pointers, definite-assignment analysis (an uninitialized `vr` is refused), and linter path coverage for release — not from author-written lifetime parameters.
- **Teardown surfaces.** When a capsule acquires memory that needs an explicit release, the conventional methods are `Deinit()` or `Free()`. Path-complete invocation of those methods is governance checked by the [Linter](../protocols/linter.md), under [Memory → Safety enforcement is governance](../protocols/memory.md#safety-enforcement-is-governance) and [Memory → Teardown is explicit, and automation writes source](../protocols/memory.md#teardown-is-explicit-and-automation-writes-source). The method names are library convention, not keywords.
- **Layout analysis.** A Khayyam-consuming compiler may run a linear static escape analysis for everyday builds, because the grammar forbids arbitrary pointers and implicit mutation. Profile-guided layout migration (heap↔stack, pre-sizing from traces) is a separable orchestration library — particularly motivated in predictable single-process environments such as unikernels remapping short-lived footprints onto worker entry stacks — and remains a long-term goal per [Memory → Layout optimization is not a language feature](../protocols/memory.md#layout-optimization-is-not-a-language-feature), not a solved claim of this grammar.
- **Generated companions.** When tooling automates path-complete release, it emits explicit source the program includes. The historical draft name `file_name.generated_by_gc1.kh` is a candidate only; the convention is open in [Memory's handoff](../protocols/memory.handoff.md#what-convention-names-and-places-generated-teardown-source).

### Khayyam Is Not Its Own Compiler or Runtime
Khayyam, as a sub-framework, defines a design space for expressing Memar's constraints in source form — explicit state, explicit error paths, no hidden control flow. It does not follow from this that Khayyam must also provide its own compiler or runtime as part of what Khayyam *is*.

Building a compiler or runtime is a separate concern with its own design space, its own trade-offs, and its own failure modes. Folding it into Khayyam's own scope creates a well-documented failure pattern seen across many language projects: once a language project owns compiler and runtime implementation, every new developer-convenience request becomes pressure to add syntax, special cases, or built-in magic to make that convenience possible — because the team that controls the language spec is the same team that feels the pain of not having the convenience. Over time this erodes the "no hidden control flow, no implicit behavior" principle that Khayyam exists to protect — protection that has to come from the inside, from the people most invested in protecting it.

Keeping compiler and runtime implementation outside Khayyam's own scope as separate systems that consume Khayyam's specification, built by teams whose incentives are implementation correctness and performance rather than syntax convenience — is therefore not an incidental scoping choice. It is a structural safeguard against the specific failure mode described above.

This has a direct consequence for how Khayyam's own documents should be scoped: a proposal to add syntax "to make the compiler's job easier" or "because other languages do it this way" is, by this principle, a signal to examine the proposal skeptically rather than a reason to adopt it. The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" still needs worked examples before this can be considered settled — see the paired handoff's [Open Questions](./khayyam.handoff.md#open-questions).

### Separation of Syntax and Governance: A Principle

**Principle:** *Syntax defines what exists* (ontology: which types, values, and relationships a program may mention). *Governance defines how instances flow* (policies about lifecycle, error routing, and architectural constraints on those instances). The compiler enforces the first; the linter/framework enforces the second. This line is not “syntax is small vs. linter is big” — it is *what* vs. *how*.

- **Syntax (compiler-enforced):** Whether a type, value, or relationship may appear at all. Examples: “a bare numeric literal `41` may not appear as a value without a named capsule” (claiming existence of an unmodeled value), “a static method must be called on the type, an instance method on a variable” (which entity a name resolves to), “all fields are private, access only via methods.”
- **Governance (linter/framework-enforced):** Policies about how already-well-typed instances move through the program. Examples: memory-safety teardown-path coverage, error-inspection discipline, code-scope naming conventions, orphan-rule for cross-file extension, architectural constraints like “no `Utils` capsules.”

A decision that *creates* or *denies* existence belongs in syntax precisely because a linter rule can be disabled — disabling a syntax rule changes what programs exist; disabling a governance rule changes how well they are kept. This is why `variable.md` rejects moving the magic-number ban to the linter (“lint rules can be disabled, weakening the safeguard”) while [Memory](../protocols/memory.md) accepts linter-enforcement for memory safety — the former denies existence of unmodeled values, the latter polices flow of already-typed instances. The split itself is the [Linter](../protocols/linter.md) protocol's compiler-versus-linter line, realized here as grammar versus governance.

### The Grammar Refuses Protocol Semantics
**Principle:** *A construct enters the grammar only when its semantics can be stated without adopting any protocol's definitions.* Where what a construct means would require the definitions a protocol owns — what an error is, what a memory guarantee is, what a concurrency primitive may assume — the grammar refuses the construct, and the need is met through the language's generic mechanisms instead: ordinary values and explicit outputs, explicit imports, library-provided methods, and the `ab` construct for authoring specifications.

What the grammar provides instead is the generic substrate: ordinary values and explicit outputs, explicit imports, library-provided methods, and the `ab` construct for authoring specifications — a protocol's definitions enter a Khayyam program through these, never as syntax. The design of library-defined control flow — the generic conditionals, the domain-named branch pairs, and the error-propagation model built on this substrate — is owned by the [Control Flow protocol](../protocols/control-flow.md); the reasons individual flow constructs were not added to the grammar are recorded in [that document's changelog](../protocols/control-flow.changelog.md).

The boundary is protocol-level, not concept-level. The grammar does express the modeling concepts defined at the base layer — `tp` for Type, `sc` for Scope — because those definitions are general and language-independent, and the grammar supplies only the declaration mechanism, not a specific contract. What the grammar may never do is adopt one specific contract's semantics as its own: protocols are owned by the governance framework above the language (Memar today, another framework tomorrow), and baking one in would reduce the language to that framework's syntax extension. This principle is the negative image of the Separation of Syntax and Governance above: that principle divides what the language already owns between compiler and linter; this one decides what never enters the language's scope at all.

### Execution Semantics Philosophy

Khayyam is designed around the principle that execution behavior should remain explicit, predictable, and architecturally visible. The primary objective is to minimize hidden runtime assumptions and maximize the visibility of computational behavior within the model itself.

As a result, Khayyam favors:

- Explicit execution behavior over implicit concurrency models
- Explicit resource management over hidden runtime mechanisms
- Direct computational semantics over operating-system-dependent abstractions

These preferences influence language design decisions such as execution models, memory abstractions, and runtime responsibilities. The goal is not to require a specific deployment environment. Rather, the goal is to ensure that architectural decisions remain visible, modelable, and predictable regardless of the underlying execution platform.

Many of these principles align naturally with unikernel-style computing, where applications operate with minimal hidden runtime layers and explicit control over execution behavior. However, Khayyam adopts these ideas as architectural principles rather than deployment requirements; the execution-side contract is [Runtime](../protocols/runtime.md) — one environment among OS, unikernel, WASM host, and language library, not a Khayyam-owned VM. The unikernel-aligned assumption may limit early adoption in organizations that do not yet use unikernels in production.

Every language feature should have explicit execution semantics. Architectural behavior should emerge from visible models and protocols rather than from implicit runtime facilities or operating-system abstractions. This approach seeks to reduce the gap between architectural intent, implementation behavior, and runtime execution, allowing systems to remain understandable and evolvable over long periods of time.

Like the Separation of Syntax and Governance, this is not a topic with a single decision to be made once and filed elsewhere — it is the principle applied every time a construct's interaction with execution (memory, concurrency, boot, teardown) is designed. It stays here for the same reason.

### Behavior Over Type Identity
Traditional generic systems frequently focus on type identity — `T`, `K`, `V` — as the central mechanism for abstraction. Khayyam instead emphasizes required behavior: the essential question is "what capabilities are required?" rather than "what concrete type is this?" This recurred across discussions of generics, parametric polymorphism, containers, algorithms, and infrastructure components alike, and is one of the reasons behind the No Generic Syntax rule under Abstraction, above. See [Abstraction in Khayyam → Behavior Over Type Identity](./abstraction.md#behavior-over-type-identity) for the full treatment, including why several canonical parametric-polymorphism patterns (`identity<T>()`, `Option<T>`, `Result<T,E>`) are tied to constraints other languages have that Khayyam does not.

### Type Principles Realized
The principles stated in [Type](../type.md) — Type as semantic entity, nominal identity, four categories of Type, owned rules — are realized in this language's constructs. Each bullet below names that realization and points at the companion document or base section that carries the full reasoning. The itemized account moved here from Type's former Manifestation in Khayyam section so that citations to it run downward (recorded in the paired changelog).

- **No primitive types**: Khayyam does not have primitive types. Even values that other languages represent as `int`, `bool`, or `string` are wrapped in named capsules (`W32`, `Bool`, `String`). This is a direct consequence of the "Type as semantic entity" principle: if `Age` and `Height` are different Types, their representation must also be different Types, not shared primitives. This eliminates the ascent problem described in [Type vs Implementation Type](../type.md#type-vs-implementation-type) at the language level.
- **Sovereign Encapsulation**: all of a Capsule's internal fields are strictly private, and all interaction occurs through method invocation — the owned-rules principle enforced at the language level (see [Encapsulation](./encapsulation.md)). Mutability is an intrinsic property of the Capsule's own definition, never a consumer-side keyword: identity and contract are declared at the definition site and cannot be bypassed at the call site.
- **The `tp` keyword**: In Khayyam, every type is declared with `tp`. The keyword is category-agnostic — `tp` declares a Type, and the subtype keyword (`cp`, `mt`, `ab`, `sc`) specifies its category. This reflects the foundational principle that Capsule, Method, Abstraction, and Scope are different realizations of the same concept: Type.
- **Method as Type**: Khayyam's `mt` subtype makes methods first-class Types (see [Method](./method.md)). A method can be imported, attached to any receiver type, and composed through the same mechanisms as Capsules and Abstractions. This is the "Method as callable Type" principle made concrete, and it has no direct precedent in mainstream languages — most treat functions as separate from the type system.
- **Abstraction as pure specification**: Khayyam's `ab` subtype defines Abstractions without method bodies (see [Abstraction](./abstraction.md)). Methods that fulfill an Abstraction's specification are defined independently as separate Types. Satisfaction is implicit and structural — no `impl` keyword. Default implementations are rejected. This maintains the clean separation: Abstractions define *what*, Capsules define *how*, Methods are currently the primary mechanism connecting them.
- **Inheritance is between Abstractions**: When an Abstraction includes another Abstraction, requirements are extended — no behavior is transferred (see [Inheritance](./inheritance.md)). Behavior transfer between Capsules is rejected; explicit delegation is the alternative. This placement of inheritance is a direct consequence of the Type category model: inheritance belongs to the specification layer — requirement extension between Abstractions — not the state layer of Capsules.
- **Behavior over type identity**: Polymorphism in Khayyam operates through abstraction conformance, not through generic type parameters (see [Polymorphism](./polymorphism.md)). The question is "what capabilities are required?" not "what concrete type is this?" A method accepting an Abstraction type is, in effect, a universally quantified function over all Types satisfying that Abstraction. Smart Compilation handles the dispatch strategy transparently.

### System-Modeling Language Philosophy
The more Khayyam evolves, the less it appears to be a traditional programming language and the more it resembles a system-modeling language. This distinction may ultimately become one of Khayyam's defining characteristics.

Many language designs begin by collecting useful features and combining them into a coherent syntax: OOP, Generics, Pattern Matching, Functional Constructs, Traits / Interfaces, Reflection, and Meta-programming. Khayyam appears to follow a different path. Instead of asking "What features should a language provide?", it asks "What architectural principles should a long-lived system follow?" and then derives language constructs from those principles.

This distinction is not merely philosophical. It has concrete implications for every design decision in the language, from how polymorphism works to how compilation is structured. A traditional language optimizes for feature completeness; Khayyam is designed to optimize for architectural integrity over time.

#### Long-Term Architectural Potential
One of the strongest aspects of Khayyam is its apparent focus on preventing architectural decay. Many language features optimize for short-term convenience. Khayyam often appears willing to accept additional modeling effort if it improves system clarity, domain integrity, architectural longevity, and maintainability over decades. This is unusual among modern languages and represents a deliberate trade-off that prioritizes the sustainability of large-scale systems over the speed of small-scale prototyping. The cost of that trade is concrete: a system-modeling approach inherently demands more upfront design investment, and developers accustomed to rapid prototyping in dynamically typed or feature-rich languages may find the initial modeling overhead excessive, particularly for small projects or proof-of-concept work where long-term architectural integrity is irrelevant.

### Self-Documenting Code and Naming
In most languages, naming is a style preference. In Khayyam, it is enforced by the language itself: magic numbers are forbidden, primitives must be wrapped in named capsules (`W32`, not `int`), and generic containers are replaced by domain-specific names (`UserRegistry`, not `Map<ID, User>`).

This means that in a Khayyam codebase, it is structurally impossible to write opaque code even if a developer tries. The grammar is designed to make the architect's intent visible at every call site.

Human-facing text — a description, a name a person reads — is a value a method writes into an influenced variable. The type that owns the behavior owns that text, so another language is another method on that type, not a prose line above the declaration. Localized names and descriptions are the same family [Type → Human-facing identity](../type.md#human-facing-identity) already places on the Type. The method that returns the text, and the owner it is attached to, are not yet a worked signature; see the paired handoff.

This is not a one-time mechanism to be decided and then documented elsewhere — it is an ongoing tension that recurs every time a new naming rule, keyword, or grammar constraint is considered. Because of that, it stays part of this document, the same document every new construct is considered against, rather than being extracted into a separate style-guide document that would only drift from whatever this document actually specifies.

### Syntactic Atomicity and Semantic Clarity
Khayyam is designed around the principle that language constructs should communicate intent as explicitly and unambiguously as possible. This idea is explored through **syntactic atomicity**: each syntactic construct should correspond to a single semantic intent, and each semantic intent should preferably be represented by a single syntactic construct.

The primary goal is semantic clarity rather than AI assistance. By reducing ambiguity, implicit conventions, overloaded meanings, and context-dependent interpretation, Khayyam seeks to make architectural intent easier to understand, reason about, validate, transform, and maintain. These benefits are expected to apply broadly to humans, compilers, analysis tools, verification systems, and machine-assisted reasoning systems alike. This remains a design hypothesis requiring empirical validation.

Like naming, this is not a topic with a single decision to be made once and filed elsewhere — it is the principle applied every time a new keyword, syntactic form, or grammar rule is proposed for Khayyam. It stays here for the same reason.

### Domain Modeling Principles
Khayyam pushes development in the opposite direction of most modern languages when it comes to domain modeling. Where other languages claim to support Domain-Driven Design but whose abstractions frequently collapse into generic containers and primitive types — `List<User>`, `Map<String, Object>`, `Dictionary<string, any>` — Khayyam encourages domain-specific concepts: `UserRegistry`, `ConnectionIndex`, `ServiceCatalog`, `PermissionStore`.

Questions of modeling methodology — how concepts are discovered, when a concept deserves an independent abstraction versus remaining a derived or contextual one, and what the limits of modeling actually are — are intentionally not answered here. They are domain-independent and are addressed in [Modeling](../modeling.md), in particular *Concept Existence vs. Model Existence*; this document stays on the language side of that boundary. The domain modeling approach demands that developers invest time in naming and structuring types before writing behavior. For developers accustomed to starting with functions and extracting types later, this represents a workflow inversion that may slow initial development velocity.

#### Resistance to Primitive Obsession
Large systems often accumulate thousands of values represented as `string`, `int`, and `bool`, while each instance carries completely different business meaning. Khayyam's emphasis on capsules and explicit modeling naturally pushes developers away from this pattern. This is not merely a typing preference; it is an architectural safeguard. By requiring all values to be wrapped in named capsules, the language is designed to keep business meaning from being lost to primitive types.

#### Resistance to Utility-Oriented Architecture
Many mature codebases eventually develop structures such as `Helpers`, `Utils`, `Common`, `Shared`, and `Base`, which become architectural dumping grounds. Khayyam's modeling style appears to discourage this evolution. Responsibilities are expected to live within meaningful capsules rather than generic utility containers. The language's import mechanism and single-responsibility file conventions reinforce this by making it natural to organize behavior around domain concepts rather than around utility categories.

### Naming
Khayyam takes its name from [Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) (1048–1131), a Persian polymath: mathematician, astronomer, philosopher, and poet.

The connection is not simply that a Persian project chose a well-known Persian name. Three parts of Omar Khayyam's actual work echo choices this language makes:

- **Solving from first principles, not from precedent.** Omar Khayyam's treatment of cubic equations found general geometric solutions rather than accumulating special-case tricks for each equation shape — the same posture behind this language's *Grammar Atomicity* and *Zero-Magic Core*: deriving a small set of constructs from architectural principles, rather than assembling a feature collection because other languages have those features.
- **Precision that outlasts its own era.** Omar Khayyam's reform of the Persian calendar (the basis of the modern Jalali calendar) was, by some measures, more accurate than the Gregorian calendar introduced nearly five centuries later — achieved through careful observation, not additional complexity. This language's willingness to accept more upfront modeling effort in exchange for architectural integrity over decades follows the same trade: precision paid for once, holding up over a long horizon.
- **Skepticism of received answers.** Omar Khayyam's poetry is remembered, in part, for a willingness to question inherited certainty rather than repeat it. This language's own recurring design instinct — that a proposal to add something merely because other languages do it that way is a signal to examine the proposal more skeptically, not a reason to adopt it — is the same posture applied to language design.

None of this is a claim that the language was engineered to match the man point for point. It is closer to the reverse: the name was available, it fit, and looking closely at why it fits is worth doing once, here, rather than leaving it as a passing choice of etymology.
