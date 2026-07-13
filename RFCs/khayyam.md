---
Title: "Khayyam"
Status: Draft
Start Date: 2026-07-13
RFC Number: 495539
Applied to: []
Related RFCs:
    - Title: "Khayyam - Programming Language"
      URI: "../Khayyam.md"
      Reason: "Reference"
      Explanation: "This assessment analyzes the design philosophy documented in the canonical Khayyam language specification."
    - Title: "Modeling"
      URI: "./modeling.md"
      Reason: "Depends_on"
      Explanation: ""
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Depends_on"
      Explanation: "Defines Protocol as a pure declarative specification"
    - Title: "Terminology"
      URI: "./terminology.md"
      Reason: "Foundation Alignment"
      Explanation: "Terminology governs how concepts are understood across modeling"
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Original idea and reflections", "Design leadership and coordination"]
        URI: ""
        Explanation: "Original author of all reflections and design assessments; identified the core principles, strengths, risks, and open design questions that form the substance of this RFC."
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: "Medium"
    Tasks:
      - Titles: ["Drafted initial text"]
        URI: ""
        Explanation: ""
    task: []
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Titles: ["Restructuring into RFC template"]
        URI: ""
        Explanation: "Restructured unstructured reflections into the canonical RFC template format; preserved original arguments and voice while mapping content to Reference-level topic subsections."
---

# Khayyam

## Summary
This RFC presents a comprehensive assessment of the Khayyam programming language's design philosophy, identifying its core architectural principles, observed strengths, recognized risks, and open design questions. The assessment concludes that Khayyam's defining characteristic is not its syntax but its deliberate derivation of language constructs from long-term system-modeling principles. Several topics identified here carry explicit seeds for future, more narrowly scoped RFCs — including Inclusion-Based Polymorphism, Self-Documenting Code Enforcement, Library-First Compilation Pipeline, Syntactic Atomicity, Target Platform Implications, Abstraction Boundary Guidelines, Error Propagation Model, Abstraction Stability and Versioning, and Primitive Capsule Specification.

## Motivation
As Khayyam evolves beyond its initial syntax specification, a structured assessment of its design philosophy is needed for two reasons. First, multiple design discussions have converged on a small set of recurring principles — behavior over type identity, domain modeling as a first-class concern, and the separation of syntax from governance — but these principles have never been formally documented in one place. Second, several open design questions (error propagation, abstraction granularity, evolution without breaking) have been identified informally and deserve a structured record with clear unresolved questions and future possibilities, so that future contributors can build on them rather than rediscovering the same issues.

## Guide-level explanation
Khayyam is evolving away from being a traditional programming language and toward becoming a system-modeling language. Most language designs begin by collecting useful features — OOP, generics, pattern matching, functional constructs, traits, reflection, meta-programming — and combining them into a coherent syntax. Khayyam follows a fundamentally different path: instead of asking "What features should a language provide?", it asks "What architectural principles should a long-lived system follow?" and then derives language constructs from those principles.

This RFC captures the current state of that derivation. It is organized into topics, each of which examines one facet of Khayyam's design. Some topics document observed strengths that emerge naturally from the language's constraints. Others document open questions — areas where the architectural direction is clear but the specific mechanism has not yet been finalized. A few topics carry explicit seeds for future RFCs, meaning they contain enough substance to warrant their own dedicated specification once the design matures.

The reader does not need to have read the canonical [Khayyam language specification](../Khayyam.md) to follow this assessment, though familiarity with Khayyam's core concepts — capsules, abstractions, methods, and Smart Compilation — will provide useful context.

## Reference-level explanation

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

### Behavior Over Type Identity
This may be the most important principle discovered during the polymorphism discussions. Traditional generic systems frequently focus on type identity — `T`, `K`, `V` — as the central mechanism for abstraction. Khayyam instead emphasizes required behavior. The essential question becomes "What capabilities are required?" rather than "What concrete type is this?".

This perspective influenced discussions around generics, parametric polymorphism, containers, algorithms, and infrastructure components, and repeatedly emerged as a unifying principle. A possible formulation: algorithms should declare the behaviors they require, not the concrete type identities they happen to operate on. This idea may deserve recognition as a foundational design principle rather than merely a polymorphism guideline.

#### Reassessment of Parametric Polymorphism
Many canonical examples of parametric polymorphism are historically tied to limitations of existing languages rather than fundamental architectural requirements. Examples include `identity<T>()`, `swap<T>()`, `Option<T>`, and `Result<T,E>`. In several cases, these abstractions exist primarily because of constraints such as single-return-value functions, nullability problems, exception models, and weak domain modeling. When those constraints disappear in Khayyam, some of these patterns become significantly less important.

This suggests that discussions about generics should not begin with "How do we support generic syntax?" but rather "Why does this requirement exist in the first place?".

#### Inclusion-Based Polymorphism
Consider a BTree algorithm that needs to compare keys. What the algorithm actually requires is a behavioral contract — "I can compare keys" — not the identity of the key type itself. In languages with generic syntax, this is commonly expressed as `BTree<K, V> where K: Ord`. However, the algorithm never uses the identity of `K`; it uses only the behavior guaranteed by `Ord`. The type parameter serves primarily as a carrier that associates the behavioral contract with a concrete type — a layer of indirection that adds syntactic overhead without contributing to the algorithm's logic.

Khayyam eliminates that carrier. The algorithm accepts an abstraction that defines comparison behavior, and any conforming capsule can participate. From the algorithm's perspective, the required information is fully expressed by the abstraction itself — no type parameter, no constraint clause, no variance annotation.

The compiler's Smart Compilation strategy can then apply the same optimizations (such as monomorphization when the reachable set of conforming capsules is closed, or dynamic dispatch when it is open) without requiring explicit type-parameter syntax in the source code.

#### Discussion

##### Rationale and alternatives
- **Adopt traditional generic syntax with constraint clauses (rejected)**: this would reintroduce the type-carrier indirection that Khayyam's design philosophy explicitly removes.
- **Use structural typing as in Go (considered, not chosen)**: Go's structural typing achieves similar expressiveness but without the Smart Compilation optimization path that Khayyam's abstraction model enables.
- **Use full dependent types (rejected)**: excessive complexity for the problem being solved; Khayyam aims for minimalism, not expressive maximality.

##### Unresolved questions
1. Are there realistic algorithms that genuinely require type identity rather than behavioral contracts, and if so, how should Khayyam handle them?
2. How does the absence of explicit type parameters affect tooling — IDE auto-completion, documentation generation, and static analysis?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Inclusion-Based Polymorphism**. A future RFC should formalize the compilation strategy, define the rules for Smart Compilation's monomorphization-vs-dispatch decision, and provide concrete benchmark data comparing Khayyam's approach to traditional generic syntax in real-world scenarios.

### Self-Documenting Code and Naming
In most languages, naming is a style preference. In Khayyam, it is enforced by the language itself: magic numbers are forbidden, primitives must be wrapped in named capsules (`W32`, not `int`), and generic containers are replaced by domain-specific names (`UserRegistry`, not `Map<ID, User>`).

This means that in a Khayyam codebase, it is structurally impossible to write opaque code even if a developer tries. The language grammar makes the architect's intent visible at every call site.

#### Discussion

##### Unresolved questions
1. Where is the boundary between "enforced clarity" and "forced verbosity"? When does a domain-specific capsule name become unnecessary indirection? A capsule called `RetryCounter` adds clarity; a capsule called `LoopIndex` may not.
2. Should Khayyam provide a linter rule or a compiler directive that allows teams to define their own boundaries for this trade-off?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Self-Documenting Code Enforcement**. A future RFC should define a formal heuristic for distinguishing clarity-enhancing names from verbosity-inducing ones, and specify whether enforcement is a compiler-level or linter-level concern.

### Library-First Compilation Pipeline
PGO in Khayyam is not a compiler flag — it is a library that developers explicitly include in their production pipeline. This is a genuinely unusual design decision with deep implications. If PGO can be a library, what else in the compilation pipeline could be? Escape analysis, inlining heuristics, dead code elimination? The principle seems to be: if an optimization strategy depends on runtime context, it belongs in a library, not in the compiler.

This creates a separation between **deterministic guarantees** (the compiler) and **contextual optimizations** (libraries). The compiler must always produce correct code without any library. Libraries then improve performance when the developer chooses to include them.

#### Discussion

##### Drawbacks
The risk is fragmentation: different projects may use different optimization libraries, making performance harder to reason about across the ecosystem. This needs a clear governance model.

##### Rationale and alternatives
- **Keep all optimizations in the compiler (rejected)**: this would prevent developers from choosing optimization strategies appropriate to their specific runtime context and deployment target.
- **Use a plugin system (considered, not chosen)**: a plugin system introduces its own complexity and stability guarantees that the simpler library-based approach avoids.

##### Unresolved questions
1. What governance model should the ecosystem adopt to prevent optimization-library fragmentation?
2. Is there a minimum set of optimizations that must always be compiler-provided for correctness, regardless of library availability?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Library-First Compilation Pipeline**. A future RFC should enumerate which compilation phases are candidates for library extraction, define the interface between the compiler and optimization libraries, and establish the governance model for ecosystem-wide optimization consistency.

### Syntactic Atomicity and Semantic Clarity
Khayyam is designed around the principle that language constructs should communicate intent as explicitly and unambiguously as possible. This idea is explored through **syntactic atomicity**: each syntactic construct should correspond to a single semantic intent, and each semantic intent should preferably be represented by a single syntactic construct.

The primary goal is semantic clarity rather than AI assistance. By reducing ambiguity, implicit conventions, overloaded meanings, and context-dependent interpretation, Khayyam seeks to make architectural intent easier to understand, reason about, validate, transform, and maintain. These benefits are expected to apply broadly to humans, compilers, analysis tools, verification systems, and machine-assisted reasoning systems alike. This remains a design hypothesis requiring empirical validation.

#### Discussion

##### Unresolved Questions
1. What level of syntactic atomicity provides meaningful benefits without introducing excessive verbosity? Highly regular, atomic syntax can feel verbose to experienced developers who rely on implicit conventions — where is the boundary between clarity and unnecessary ceremony?
2. How can syntactic atomicity be measured objectively?
3. Which forms of ambiguity are most harmful to long-term system maintainability?

##### Future Possibilities
This topic carries an explicit seed for a dedicated RFC: **Syntactic Atomicity**.

A future RFC should define syntactic atomicity formally, establish measurable criteria, and evaluate its impact on readability, maintainability, tooling, automated reasoning, and long-term architectural clarity.

### Execution Semantics Philosophy
Khayyam is designed around the principle that execution behavior should remain explicit, predictable, and architecturally visible. The primary objective is to minimize hidden runtime assumptions and maximize the visibility of computational behavior within the model itself.

As a result, Khayyam favors:
* Explicit execution behavior over implicit concurrency models
* Explicit resource management over hidden runtime mechanisms
* Direct computational semantics over operating-system-dependent abstractions

These preferences influence language design decisions such as execution models, memory abstractions, and runtime responsibilities. The goal is not to require a specific deployment environment. Rather, the goal is to ensure that architectural decisions remain visible, modelable, and predictable regardless of the underlying execution platform.

Many of these principles align naturally with unikernel-style computing, where applications operate with minimal hidden runtime layers and explicit control over execution behavior. However, Khayyam adopts these ideas as architectural principles rather than deployment requirements.

Every language feature should have explicit execution semantics. Architectural behavior should emerge from visible models and protocols rather than from implicit runtime facilities or operating-system abstractions.

This approach seeks to reduce the gap between architectural intent, implementation behavior, and runtime execution, allowing systems to remain understandable and evolvable over long periods of time.

#### Discussion

##### Drawbacks
If a team needs to deploy Khayyam code on a standard Linux server, how much of the language's value proposition is lost? The unikernel-first assumption may limit early adoption in organizations that do not yet use unikernels in production.

##### Unresolved questions
1. Should Khayyam define a **hosted mode** for development and testing that simulates unikernel constraints on a standard OS, similar to how Rust's `#[no_std]` is opt-in rather than the default?
2. What is the minimum set of OS abstractions Khayyam must provide for hosted-mode development to be productive?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Target Platform Implications**. A future RFC should define the hosted-mode specification, enumerate the OS abstractions required for productive development outside a unikernel, and specify the boundary between unikernel-native and hosted-mode behavior.

### Abstraction Design
Khayyam's abstractions are intended as "architectural contracts that express meaningful behavioral boundaries." But the language currently provides no formal guideline for where one abstraction should end and another should begin.

Consider: should a `Sortable` abstraction also imply `Equatable`? Should a `Serializable` abstraction imply `Cloneable`? In trait-heavy languages, these questions lead to trait hierarchies. In Khayyam, where inclusion is the mechanism, the question becomes: what is the minimum coherent behavioral boundary?

This is not just a style question. It affects API surface area, compilation strategy (more conforming capsules means less monomorphization), and onboarding friction.

A possible heuristic: an abstraction should represent a **domain concept**, not a **technical capability**. `UserRepository` is a valid abstraction. `Filterable` is probably not.

#### Over-Abstraction Risk
The largest non-technical risk may be abstraction inflation. If developers misunderstand the role of abstractions, they may begin creating `Readable`, `Writable`, `Searchable`, `Filterable`, `Sortable`, `Composable`, and so on, as generic reuse mechanisms. This recreates the same problems seen in interface-heavy ecosystems.

The intended role of abstractions appears to be: architectural contracts that express meaningful behavioral boundaries — not general-purpose code reuse tools. The success of Khayyam may depend heavily on preserving this distinction.

#### Discussion

##### Drawbacks
Without formal guidelines, different teams (or different developers within the same team) will make inconsistent abstraction-granularity decisions. Over time, this inconsistency can erode the API coherence that the abstraction model is designed to provide.

##### Rationale and alternatives
- **Define a maximum set of methods per abstraction (rejected)**: arbitrary numeric limits do not capture the semantic coherence that matters.
- **Require a domain-concept naming heuristic as a compiler rule (considered, not chosen)**: too subjective for mechanical enforcement; better suited as a linter guideline.

##### Unresolved questions
1. Is the domain-concept vs. technical-capability heuristic sufficient, or does it need to be supplemented with more specific criteria?
2. Should the Memar framework define a curated set of canonical abstractions that serve as reference examples for appropriate granularity?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Abstraction Boundary Guidelines**. A future RFC should formalize the granularity heuristic, provide positive and negative examples, and specify whether enforcement belongs at the compiler, linter, or organizational-governance level.

### Error Propagation Model
The canonical Khayyam specification notes that `Result<T, E>` exists in other languages primarily because of nullability problems and single-return-value functions — constraints that Khayyam does not share. But errors still occur in any system: network connections fail, files don't exist, and parsers encounter invalid input. If Khayyam does not use `Result<T, E>`, the error propagation mechanism remains an open design question that deserves its own RFC.

Possibilities worth exploring include capsule-level error state (similar to Go's error return, but encapsulated), abstraction-level error contracts (a `Failable` abstraction that defines error semantics), and memory ADT-based error propagation (leveraging the same explicit lifecycle model used for memory).

The choice here will significantly impact every capsule and abstraction in the ecosystem.

#### Discussion

##### Rationale and alternatives
- **Adopt `Result<T, E>` directly (rejected)**: this would reintroduce the type-carrier pattern that Khayyam's inclusion-based polymorphism philosophy explicitly removes.
- **Use exception-like mechanisms (rejected)**: exceptions introduce hidden control flow, contradicting Khayyam's principle of making all behavior explicit and visible at the call site.

##### Unresolved questions
1. Which of the three proposed mechanisms — capsule-level error state, abstraction-level error contracts, or memory ADT-based propagation — best aligns with Khayyam's existing design principles?
2. How does the error propagation model interact with Smart Compilation's optimization strategy? Can error paths be optimized as aggressively as success paths?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Error Propagation Model**. A future RFC should evaluate each proposed mechanism against Khayyam's design principles, provide concrete syntax proposals, and analyze the performance implications of each approach.

### Abstraction Stability and Versioning
When an abstraction's behavioral contract changes — a new method is added, a return type changes, a precondition is tightened — what happens to every capsule that conforms to it?

In Rust, adding a method to a trait is a breaking change. In Go, adding a method to an interface is not (structural typing). In Java, default methods were introduced specifically to solve this problem. Khayyam's inclusion-based model needs its own answer. Since Smart Compilation may monomorphize based on the current set of conforming capsules, an abstraction change could trigger recompilation across the entire dependency graph.

This is not just a compiler problem. It is an ecosystem governance problem. If core abstractions in the Memar framework evolve frequently, the cost of upgrading becomes a function of the abstraction stability model, not the code change itself.

#### Discussion

##### Rationale and alternatives
- **Adopt Rust's trait-evolution rules (rejected)**: Rust's nominal typing makes adding a method a breaking change, which is overly conservative for Khayyam's inclusion-based model.
- **Adopt Go's structural typing approach (considered, not chosen)**: Go's approach is too permissive for Khayyam's goal of explicit behavioral contracts, since any capsule that happens to have the right methods would accidentally conform.

##### Unresolved questions
1. What is the minimal safe evolution operation on an abstraction? Can a new method be added non-breakingly if it has a default implementation expressed as a standalone method?
2. Should Khayyam define a formal versioning scheme for abstractions, similar to semantic versioning but adapted for behavioral contracts?

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Abstraction Stability and Versioning**. A future RFC should define the versioning model for abstractions, specify the safe-evolution rules, and describe the recompilation strategy when an abstraction in a dependency changes.

### Primitive Capsule Specification
The canonical Khayyam specification claims that replacing `int32` with `W32` is "zero-cost" via Smart Compilation. But `W32` is not just a renamed integer — it is a capsule that presumably provides behavioral guarantees beyond what `int32` offers. What exactly does `W32` guarantee? Some possibilities include overflow behavior (wrapping vs. panic vs. saturating), bit-width enforcement (no implicit widening), serialization contract (predictable binary layout), and range semantics (if used as an index, bounds checking).

The answer matters because it defines the migration contract. If `W32` only provides renaming, the "zero-cost" claim is trivial. If it provides behavioral guarantees, the migration is more complex but the value is real.

#### Discussion

##### Unresolved questions
1. What behavioral guarantees does each primitive capsule provide? Is there a formal specification for `W32`, `W64`, `F32`, `F64`, and other primitive capsules?
2. Should primitive capsules be defined by the language itself, by the standard library, or by the Memar framework? Each choice has different implications for portability and governance.

##### Future possibilities
This topic carries an explicit seed for a dedicated RFC: **Primitive Capsule Specification**. A future RFC should enumerate every primitive capsule, define its behavioral contract precisely, and specify the migration path from raw primitive types.

## Discussion

### Naming Conventions
Not applicable at the RFC-wide level. Each topic section above that introduces naming implications includes its own Suggested Naming Conventions or Naming Discussion where relevant.

### Drawbacks
The primary risk of this assessment is that it documents aspirations and principles without yet having implementation evidence for several of them. Smart Compilation, infrastructure-level data structures, ADT integration, runtime optimization strategies, and memory model implications are all theoretically sound and do not currently appear contradictory. However, they remain hypotheses that must eventually be validated through real implementations. Premature commitment to architectural principles that prove impractical in implementation could lead to costly rework.

### Rationale and alternatives
- **Publish separate RFCs for each topic rather than one assessment (rejected)**: the topics are interconnected — behavior over type identity informs both the polymorphism model and the naming philosophy — and splitting them would obscure these connections.
- **Wait until implementation evidence exists before documenting (rejected)**: documenting the principles now creates a shared reference point that prevents parallel discussions from diverging, even if some conclusions may later be revised.

### Prior art
Rust's design philosophy documents and Go's "Go Proverbs" serve a similar purpose of capturing design intent alongside technical specification. This RFC differs by integrating the assessment directly into the RFC structure rather than maintaining it as a separate, informal document.

### Unresolved questions
1. Should this assessment be split into multiple RFCs once the individual topic-seed RFCs are written, or should it persist as a single overview document?
2. How frequently should this assessment be revisited as the implementation matures?

### Future possibilities
Each topic section above that carries an explicit seed for a future RFC represents a concrete next step. In priority order, the error propagation model and the abstraction stability model have the most direct impact on the ecosystem and should likely be addressed first, followed by the primitive capsule specification and the abstraction boundary guidelines.

## Change Rationale