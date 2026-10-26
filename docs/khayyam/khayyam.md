---
Title: "Khayyam - Programming Language"
Status: Proposed
Start Date: 2025-04-24
ID: 484848
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

**Declaration separator.** Each declaration — `tp`, `vr`, and their subtype and `in` forms — occupies one line, and the line's break terminates it. Every declaration form in this document set is written that way, and a statement inside a method body is terminated the same way (see *Scope*).

**Identifiers.** An identifier begins with a letter or `_` and continues with letters, digits, or `_`; a letter is a letter in whichever script writes it, so a name in Persian, Chinese, Latin, or any other script has the same shape as any other name. Identifiers are case-sensitive. The seven keywords above name the declaration forms rather than names, so an identifier spells something else.

### Import Mechanism (`in`)
Khayyam treats the URI that names a source as the ultimate source of truth (a file URI, a UUID, or another URI form; not a dependency on any particular filesystem's broader feature set — no directory permissions, watches, or other OS-level filesystem semantics are implied), avoiding abstract concepts like `namespace` or `package`. The `in` keyword is used as a routing operator to include entities from other files. Since capsules (`cp`), abstractions (`ab`), and methods (`mt`) are all fundamentally types, the import syntax remains strictly orthogonal:

- **Type Inclusion:** `tp {name} in "{path}"`
  - *Example:* `tp TcpConn in "net/tcp.kh"` (Imports a capsule, abstraction, or method type)
  - *Example:* `tp ErrServiceNotFound in "modules/process/services/errors/service-not-found.kh"` without need to indicate a name to call them, e.g. `err.CopyFrom(ErrServiceNotFound)(err)` (statement form; `=` does not exist in Khayyam)
- **Variable Inclusion:** `vr {name} in "{path}"`
  - *Example:* `vr MaxTimeout in "net/config.kh"` (Imports a specific variable, constant, or singleton)

**The path is a URI**, and the language states no scheme for it: what it is written as and how it resolves are [Modularity in Khayyam → Dependency Resolution and Companion Manifest](./modularity.md#dependency-resolution-and-companion-manifest)'s subject.

> **A name an `in` declaration includes is the name it declares.** The grammar offers no `as` form, so an included entity keeps its own name, and a file that needs two entities sharing a name has no way to bring both under distinct names. What such a collision means, and what a project does about one, is [Modularity in Khayyam → When Two Included Names Collide](./modularity.md#when-two-included-names-collide).

### Type
What a type is, is [Type](../type.md#definition-of-type)'s subject. In Khayyam every type is declared in the shape below.
```khayyam
tp {name} {subtype} {subtype defined value}
```

The `{subtype}` slot is one of the five subtypes — `in`, `cp`, `mt`, `ab`, `sc` — and it supplies the declaration's category (see *Type Principles Realized*). The value slot holds what defines that subtype: a path for `in`, a block for `cp` and `sc`, a signature plus optional body for `mt`, and an optional composition block for `ab`.

#### Capsule
`cp` declares a capsule, the language's [encapsulation](./encapsulation.md) construct. Its form, its fields and the abstractions it composes, and the privacy of its state are defined in [Encapsulation in Khayyam → Capsule Structure and Privacy](./encapsulation.md#capsule-structure-and-privacy).

#### Method
`mt` declares a method, which is itself a type and may be attached to any type. Its signature — the owner, influencing, and influenced groups — pass-by-reference and state protection, and body-less methods for contracts and foreign implementations are defined in [Method in Khayyam → Method Structure](./method.md#method-structure). Because a receiving method can change a capsule's state only through a method that capsule exposes, the language has no work for a `const` or `mut` keyword.

##### Method Invocation Rules
Every call is written with the single dot and both call groups, on the parent type or on a variable of it, as [Method in Khayyam → Method Invocation Rules](./method.md#method-invocation-rules) defines.

#### Abstraction
`ab` declares an abstraction, a pure behavioral specification with no logic, state, or method bodies, optionally composing other abstractions in its block. Its form, its composition, and what its signatures may name are defined in [Abstraction in Khayyam → Defining an Abstraction](./abstraction.md#defining-an-abstraction) and [What You Cannot Do](./abstraction.md#what-you-cannot-do). The grammar has no generic syntax and no dispatch syntax: the first, and covariant return types in its place, are [Polymorphism in Khayyam → What the Grammar Does Not Admit](./polymorphism.md#what-the-grammar-does-not-admit) and [Covariant Return Types](./polymorphism.md#covariant-return-types); the second is [Abstraction in Khayyam → Dispatch Strategy](./abstraction.md#dispatch-strategy).

#### Scope
- `tp {name} sc { ___ }`
- Scope is an area in which something acts or operates or has power or control.
- A code scope is inert until a library-provided method drives it: the grammar ships no control-flow keywords or logical operators of its own. See [Control Flow](../../modules/process/control-flow/control-flow.md) for how flow constructs are built as libraries within this mechanism.
- Each command ends with a new line; what performs a scope's commands is the driving method's business — see [Control Flow](../../modules/process/control-flow/control-flow.md).
- **No keyword for leaving a method early.** What ends an execution before the last command of a method's body is a flow-management operation, and [Control Flow → Structured and Unstructured Flow as Libraries](../../modules/process/control-flow/control-flow.md#structured-and-unstructured-flow-as-libraries) requires of such a construct only that it be an ordinary method on some type. Until a library declares one, a program written in this language has no way to leave a method early, which is a statement of what the language has rather than a shortfall in it: a method call already carries everything the operation needs, and [Minimal Legislation: A Principle](#minimal-legislation-a-principle) holds that the grammar states only what a program's meaning requires.
- What may fill an argument position, a type passed as an argument included, is [Method in Khayyam → Type-level arguments for `sc` and `mt`](./method.md#type-level-arguments-for-sc-and-mt).

### Variable
`vr` declares a variable. Its form, where it may be declared, the absence of assignment operators and implicit copies, and its standing as a logical reference to a type's instance are defined in [Variable in Khayyam](./variable.md) — [Variable Declaration Syntax](./variable.md#variable-declaration-syntax), [No Assignment Operators](./variable.md#no-assignment-operators), [Variable as Logical Reference](./variable.md#variable-as-logical-reference). A variable is never the raw data block and never a raw machine pointer.
- **No `nil` / `null` keyword:** the grammar has no universal nullability token. Absence, when a type can represent it, is [Memory → Absence is a type's contract](../../modules/computer/memory/memory.md#absence-is-a-types-contract-not-a-universal-machine-condition).

### How Khayyam realizes Memory
[Memory](../../modules/computer/memory/memory.md) owns the language-independent requirements. This language meets them without growing memory-management syntax:

- **No lifetime annotations.** The grammar has none. Correctness of lifetimes is obtained from sovereign encapsulation (no leaking raw internal references), deterministic `sc` boundaries, the absence of syntax-level pointers, the refusal of uninitialized reads ([Memory → Uninitialized reads are refused](../../modules/computer/memory/memory.md#uninitialized-reads-are-refused)), and governance over release ([Memory → Safety enforcement is governance](../../modules/computer/memory/memory.md#safety-enforcement-is-governance)) — not from author-written lifetime parameters.
- **Teardown surfaces.** Teardown is a method on the type's contract, as [Memory → Teardown is explicit, and automation writes source](../../modules/computer/memory/memory.md#teardown-is-explicit-and-automation-writes-source) requires; the grammar adds no destructor syntax.
- **Layout analysis.** Whether an analysis is run at all, and which one, is a compiler's choice — [Memory → Layout optimization is not a language feature](../../modules/computer/memory/memory.md#layout-optimization-is-not-a-language-feature) states why the grammar settles the matter it needs (no arbitrary pointers, no implicit mutation) and leaves the rest to the tool. What the grammar forbids is the pointer syntax that such an analysis would be about.
### Khayyam Is Not Its Own Compiler or Runtime
Khayyam, as a sub-framework, defines a design space for expressing Memar's constraints in source form — explicit state, explicit error paths, no hidden control flow. It does not follow from this that Khayyam must also provide its own compiler or runtime as part of what Khayyam *is*.

Building a compiler or runtime is a separate concern with its own design space, its own trade-offs, and its own failure modes. Folding it into Khayyam's own scope creates a well-documented failure pattern seen across many language projects: once a language project owns compiler and runtime implementation, every new developer-convenience request becomes pressure to add syntax, special cases, or built-in magic to make that convenience possible — because the team that controls the language spec is the same team that feels the pain of not having the convenience. Over time this erodes the "no hidden control flow, no implicit behavior" principle that Khayyam exists to protect — protection that has to come from the inside, from the people most invested in protecting it.

Keeping compiler and runtime implementation outside Khayyam's own scope as separate systems that consume Khayyam's specification, built by teams whose incentives are implementation correctness and performance rather than syntax convenience — is therefore not an incidental scoping choice. It is a structural safeguard against the specific failure mode described above.

This has a direct consequence for how Khayyam's own documents should be scoped: a proposal to add syntax "to make the compiler's job easier" or "because other languages do it this way" is, by this principle, a signal to examine the proposal skeptically rather than a reason to adopt it. The precise boundary between "what Khayyam specifies" and "what a Khayyam toolchain or module provides" still needs worked examples before this can be considered settled — see the paired handoff's [Open Questions](./khayyam.handoff.md#open-questions).

### Separation of Syntax and Governance: A Principle
**Principle:** *Syntax defines what exists* (ontology: which types, values, and relationships a program may mention). *Governance defines how instances flow* (policies about lifecycle, error routing, and architectural constraints on those instances). The compiler enforces the first; the linter/framework enforces the second. This line is not “syntax is small vs. linter is big” — it is *what* vs. *how*.

- **Syntax (compiler-enforced):** Whether a type, value, or relationship may appear at all. Examples: “a bare numeric literal `41` may not appear as a value without a named capsule” (claiming existence of an unmodeled value), “a static method must be called on the type, an instance method on a variable” (which entity a name resolves to), “all fields are private, access only via methods.”
- **Governance (linter/framework-enforced):** Policies about how already-well-typed instances move through the program. Examples at the protocol level include memory-safety teardown-path coverage and error-inspection discipline.

A decision that *creates* or *denies* existence belongs in syntax precisely because a linter rule can be disabled — disabling a syntax rule changes what programs exist; disabling a governance rule changes how well they are kept. This is why [Variable in Khayyam's changelog](./variable.changelog.md) records rejecting moving the magic-number ban to the linter (“lint rules can be disabled or ignored at the organizational level, weakening the architectural safeguard”) while [Memory](../../modules/computer/memory/memory.md) accepts linter-enforcement for memory safety — the former denies existence of unmodeled values, the latter polices flow of already-typed instances. The split itself is the [Linter](../../modules/computer/linter/linter.md) protocol's compiler-versus-linter line, realized here as grammar versus governance.

A rule that settles what this document leaves open is a toolchain's or an organization's, not the language's: it is not the only possible rule, and anyone may define and use their own.

### The Grammar Refuses Protocol Semantics
**Principle:** *A construct enters the grammar only when its semantics can be stated without adopting any protocol's definitions.* Where what a construct means would require the definitions a protocol owns — what an error is, what a memory guarantee is, what a concurrency primitive may assume — the grammar refuses the construct, and the need is met through the language's generic mechanisms instead: ordinary values and explicit outputs, explicit imports, library-provided methods, and the `ab` construct for authoring specifications.

The design of library-defined control flow — the generic conditionals, the domain-named branch pairs, and the error-propagation model built on this substrate — is owned by the [Control Flow protocol](../../modules/process/control-flow/control-flow.md); the reasons individual flow constructs were not added to the grammar are recorded in [that document's changelog](../../modules/process/control-flow/control-flow.changelog.md).

The boundary is protocol-level, not concept-level. The grammar does express the modeling concepts defined at the base layer — `tp` for Type, `sc` for Scope — because those definitions are general and language-independent, and the grammar supplies only the declaration mechanism, not a specific contract. What the grammar may never do is adopt one specific contract's semantics as its own: protocols are owned by the governance framework above the language (Memar today, another framework tomorrow), and baking one in would reduce the language to that framework's syntax extension. This principle is the negative image of the Separation of Syntax and Governance above: that principle divides what the language already owns between compiler and linter; this one decides what never enters the language's scope at all.

### Minimal Legislation: A Principle
**Principle:** *The grammar states what a program's meaning requires, and a condition a tool or an organization needs belongs to that tool's rules.* A construct earns a place here when a program is well-formed or ill-formed according to it — when its existence, its resolution, or its observable behavior turns on it. A condition whose handling may differ between one realization and the next — how a name is spelled, which prose a file carries, how firmly a tool insists on a given form, where a declaration may be written — is stated by the tool that applies it, in that tool's own rules, where an organization states it, keeps it, or drops it and the language stays the same either way.

This is the question every proposed construct answers, and the question every construct already here answered once. [Separation of Syntax and Governance](#separation-of-syntax-and-governance-a-principle) divides what the language owns between the compiler and governance; [The Grammar Refuses Protocol Semantics](#the-grammar-refuses-protocol-semantics) settles what never enters the language's scope at all; this principle says how much enters it, and it is what decides the remainder. Where a rule that passes this test is then written is [Linter → A rule's home is its subject's document](../../modules/computer/linter/linter.md#a-rules-home-is-its-subjects-document)'s subject.

A rule that is a tool's is not thereby a small one. An organization may forbid outright what the grammar leaves free, and a second organization may write the same language and never meet the rule at all — that is what makes it a rule, and it is why the question worth asking of any proposed condition is whether turning it off would change what a program means. What every organization gets from the grammar is the same: the declarations a program may contain, the meanings those declarations have, and nothing a tool could have said on its own.

### Execution Semantics Philosophy
Khayyam is designed around the principle that execution behavior should remain explicit, predictable, and architecturally visible. The primary objective is to minimize hidden runtime assumptions and maximize the visibility of computational behavior within the model itself.

As a result, Khayyam favors:

- Explicit execution behavior over implicit concurrency models
- Explicit resource management over hidden runtime mechanisms
- Direct computational semantics over operating-system-dependent abstractions

These preferences influence language design decisions such as execution models, memory abstractions, and runtime responsibilities. The goal is not to require a specific deployment environment. Rather, the goal is to ensure that architectural decisions remain visible, modelable, and predictable regardless of the underlying execution platform.

Many of these principles align naturally with unikernel-style computing, where applications operate with minimal hidden runtime layers and explicit control over execution behavior. However, Khayyam adopts these ideas as architectural principles rather than deployment requirements; the execution-side contract is [Runtime](../../modules/computer/runtime/runtime.md) — one environment among OS, unikernel, WASM host, and language library, not a Khayyam-owned VM. The unikernel-aligned assumption may limit early adoption in organizations that do not yet use unikernels in production.

Every language feature should have explicit execution semantics. Architectural behavior should emerge from visible models and protocols rather than from implicit runtime facilities or operating-system abstractions. This approach seeks to reduce the gap between architectural intent, implementation behavior, and runtime execution, allowing systems to remain understandable and evolvable over long periods of time.

Like the Separation of Syntax and Governance, this is not a topic with a single decision to be made once and filed elsewhere — it is the principle applied every time a construct's interaction with execution (memory, concurrency, boot, teardown) is designed. It stays here for the same reason.

### Behavior Over Type Identity
Khayyam asks what capabilities are required rather than what concrete type a value is, and that is one reason the grammar has no generic syntax. [Abstraction in Khayyam → Behavior Over Type Identity](./abstraction.md#behavior-over-type-identity) states the principle and its reasons.

### Type Principles Realized
The principles stated in [Type](../type.md) — Type as semantic entity, nominal identity, four categories of Type, owned rules — are realized in this language's constructs. Khayyam is currently the first and most concrete realization of these principles, so most readers meet Type through this language's syntax before they meet it as a modeling concept; that is a fact about where the principles were first put into practice, not about where Type originates. Each principle's realization is stated by the document that owns it:

- **No primitive types**, every value wrapped in a named capsule: [Type → Type vs Implementation Type](../type.md#type-vs-implementation-type), [Variable in Khayyam → No Privileged Types](./variable.md#no-privileged-types).
- **Sovereign encapsulation**: [Encapsulation in Khayyam → Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation).
- **One category-agnostic `tp` keyword, and fewer top-level constructs**: [Type → Categories of Type](../type.md#categories-of-type), [Type → Type Categories vs Language Keywords](../type.md#type-categories-vs-language-keywords).
- **No keywords for Type metadata**: [Type → Type Metadata](../type.md#type-metadata).
- **Method as Type**: [Type → Method — Type as Callable Behavior](../type.md#method--type-as-callable-behavior), [Method in Khayyam](./method.md).
- **Abstraction as pure specification**, satisfied structurally, with no default implementations: [Abstraction in Khayyam](./abstraction.md).
- **Inheritance is between Abstractions**: [Inheritance in Khayyam](./inheritance.md).
- **Behavior over type identity**: [Polymorphism in Khayyam](./polymorphism.md).

### System-Modeling Language Philosophy
The more Khayyam evolves, the less it appears to be a traditional programming language and the more it resembles a system-modeling language. This distinction may ultimately become one of Khayyam's defining characteristics.

Many language designs begin by collecting useful features and combining them into a coherent syntax: OOP, Generics, Pattern Matching, Functional Constructs, Traits / Interfaces, Reflection, and Meta-programming. Khayyam appears to follow a different path. Instead of asking "What features should a language provide?", it asks "What architectural principles should a long-lived system follow?" and then derives language constructs from those principles.

This distinction is not merely philosophical. It has concrete implications for every design decision in the language, from how polymorphism works to how compilation is structured. A traditional language optimizes for feature completeness; Khayyam is designed to optimize for architectural integrity over time.

#### Long-Term Architectural Potential
One of the strongest aspects of Khayyam is its apparent focus on preventing architectural decay. Many language features optimize for short-term convenience. Khayyam often appears willing to accept additional modeling effort if it improves system clarity, domain integrity, architectural longevity, and maintainability over decades. This is unusual among modern languages and represents a deliberate trade-off that prioritizes the sustainability of large-scale systems over the speed of small-scale prototyping. The cost of that trade is concrete: a system-modeling approach inherently demands more upfront design investment, and developers accustomed to rapid prototyping in dynamically typed or feature-rich languages may find the initial modeling overhead excessive, particularly for small projects or proof-of-concept work where long-term architectural integrity is irrelevant.

### Self-Documenting Code and Naming
In most languages, naming is a style preference. In Khayyam, the parts of it the grammar can settle are settled: a bare literal carries no meaning of its own, primitives must be wrapped in named capsules (`W32`, not `int`), and there is no generic container syntax to name (`UserRegistry`, not `Map<ID, User>`). Which names a program uses is that program's own rule, not the language's.

The grammar is designed to make the architect's intent visible at every call site.

Human-facing text — a description, a name a person reads — is a value a method writes into an influenced variable. The type that owns the behavior owns that text, so another language is another method on that type, not a prose line above the declaration. Localized names and descriptions are the same family [Type → Human-facing identity](../type.md#human-facing-identity) already places on the Type. The method that returns the text, and the owner it is attached to, are not yet a worked signature; see the paired handoff.

This is not a one-time mechanism to be decided and then documented elsewhere — it is an ongoing tension that recurs every time a new naming rule, keyword, or grammar constraint is considered. Because of that, it stays part of this document, the same document every new construct is considered against, rather than being extracted into a separate style-guide document that would only drift from whatever this document actually specifies.

### Syntactic Atomicity and Semantic Clarity
Khayyam is designed around the principle that language constructs should communicate intent as explicitly and unambiguously as possible. This idea is explored through **syntactic atomicity**: each syntactic construct should correspond to a single semantic intent, and each semantic intent should preferably be represented by a single syntactic construct.

The primary goal is semantic clarity rather than AI assistance. By reducing ambiguity, implicit conventions, overloaded meanings, and context-dependent interpretation, Khayyam seeks to make architectural intent easier to understand, reason about, validate, transform, and maintain. These benefits are expected to apply broadly to humans, compilers, analysis tools, verification systems, and machine-assisted reasoning systems alike. This remains a design hypothesis requiring empirical validation.

Like naming, this is not a topic with a single decision to be made once and filed elsewhere — it is the principle applied every time a new keyword, syntactic form, or grammar rule is proposed for Khayyam. It stays here for the same reason.

### Domain Modeling Principles
Khayyam pushes development in the opposite direction of most modern languages when it comes to domain modeling. Where other languages claim to support Domain-Driven Design but whose abstractions frequently collapse into generic containers and primitive types — `List<User>`, `Map<String, Object>`, `Dictionary<string, any>` — Khayyam encourages domain-specific concepts: `UserRegistry`, `ConnectionIndex`, `ServiceCatalog`, `PermissionStore`.

How concepts are discovered, and when one deserves an independent abstraction, is [Modeling → Concept Existence vs. Model Existence](../modeling.md#concept-existence-vs-model-existence)'s subject. The domain modeling approach demands that developers invest time in naming and structuring types before writing behavior. For developers accustomed to starting with functions and extracting types later, this represents a workflow inversion that may slow initial development velocity.

#### Resistance to Primitive Obsession
Large systems often accumulate thousands of values represented as `string`, `int`, and `bool`, while each instance carries completely different business meaning. Khayyam's emphasis on capsules and explicit modeling naturally pushes developers away from this pattern. This is not merely a typing preference; it is an architectural safeguard. By requiring all values to be wrapped in named capsules, the language is designed to keep business meaning from being lost to primitive types.

#### Resistance to Utility-Oriented Architecture
Khayyam's modeling style organizes behavior around domain capsules rather than utility categories; how a project names them is that project's own rule.

### Naming
Khayyam takes its name from [Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) (1048–1131), a Persian polymath: mathematician, astronomer, philosopher, and poet.

The connection is not simply that a Persian project chose a well-known Persian name. Three parts of Omar Khayyam's actual work echo choices this language makes:

- **Solving from first principles, not from precedent.** Omar Khayyam's treatment of cubic equations found general geometric solutions rather than accumulating special-case tricks for each equation shape — the same posture behind this language's *Grammar Atomicity* and *Zero-Magic Core*: deriving a small set of constructs from architectural principles, rather than assembling a feature collection because other languages have those features.
- **Precision that outlasts its own era.** Omar Khayyam's reform of the Persian calendar (the basis of the modern Jalali calendar) was, by some measures, more accurate than the Gregorian calendar introduced nearly five centuries later — achieved through careful observation, not additional complexity. This language's willingness to accept more upfront modeling effort in exchange for architectural integrity over decades follows the same trade: precision paid for once, holding up over a long horizon.
- **Skepticism of received answers.** Omar Khayyam's poetry is remembered, in part, for a willingness to question inherited certainty rather than repeat it. This language's own recurring design instinct — that a proposal to add something merely because other languages do it that way is a signal to examine the proposal more skeptically, not a reason to adopt it — is the same posture applied to language design.

None of this is a claim that the language was engineered to match the man point for point. It is closer to the reverse: the name was available, it fit, and looking closely at why it fits is worth doing once, here, rather than leaving it as a passing choice of etymology.
