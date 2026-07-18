---
Title: "Khayyam Design Philosophy"
Status: Draft
Start Date: 2026-07-13
RFC Number: 495539
Applied to: []
Related RFCs:
    - Title: "Khayyam - Programming Language"
      URI: "../Khayyam.md"
      Kind: Extends
      Explanation: "This document records the design philosophy and recurring architectural principles behind the canonical Khayyam language specification. It does not modify, restate, or supersede the specification itself."
    - Title: "Terminology"
      URI: "./terminology.md"
      Kind: Depends_on
      Explanation: "Terminology governs how concepts referenced throughout this document (capsule, abstraction, behavior) are defined across Memar."
    - Title: "Protocol"
      URI: "./protocol.md"
      Kind: Depends_on
      Explanation: "Per Protocol's definition ('a named set of declarative rules that governs processes within a system'), Khayyam's method/abstraction model is itself an instance of a protocol. This document's philosophy inherits that framing even though 'Protocol' is not named verbatim in the body text."
    - Title: "Framework"
      URI: "./framework.md"
      Reason: "Depends_on"
      Explanation: "The separation of encapsulation syntax from governance enforcement follows the framework/language/OS separation defined in that document."
    - Title: "Modeling"
      URI: "./modeling.md"
      Kind: Depends_on
      Explanation: "Modeling is the central recurring concept throughout this document — system-modeling language, domain modeling, architectural modeling. This document's philosophy is a direct application of Modeling's definitions to language design, even where the word itself isn't repeated in every section."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Original idea and reflections", "Design leadership and coordination"]
        URI: ""
        Explanation: "Original author of all reflections and design assessments; identified the core principles that form the substance of this RFC."
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Titles: ["Drafted initial text"]
        URI: ""
        Explanation: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Titles: ["Restructuring into RFC template"]
        URI: ""
        Explanation: "Restructured unstructured reflections into the canonical RFC template format; preserved original arguments and voice while mapping content to Reference-level topic subsections."
  - Name: "Claude"
    URI: "https://anthropic.com"
    Model: "Claude Sonnet 5"
    Effort: "High - thinking"
    Tasks:
      - Titles: ["Narrative/technical separation", "Governance and attribution review"]
        URI: ""
        Explanation: "Front-matter governance. Separated the document into a narrative/philosophy layer (retained here) and a technical/decision layer (extracted to a staging file for placement into dedicated future RFCs)."
---

# Khayyam Design Philosophy

## Summary
This RFC documents the design philosophy underlying the Khayyam programming language: the architectural principles, motivations, and observed strengths that emerge from Khayyam's approach of deriving language constructs from long-term system-modeling requirements, rather than assembling a feature set.

This RFC intentionally does not contain topic-specific technical decisions — error propagation mechanics, primitive capsule contracts, abstraction versioning rules, polymorphism compilation strategy, and similar concerns are addressed in their own dedicated RFCs as they are written. A reader who does not find a specific mechanism documented here should not assume it is unresolved; see the project's general documentation-navigation guidance for how to search across Memar's RFCs by topic rather than by filename.

## Motivation
Multiple design discussions across Khayyam's evolution have converged on a small set of recurring principles — behavior over type identity, domain modeling as a first-class concern, and the separation of syntax from governance — but these principles had never been documented together in one place. This RFC exists to record that shared philosophical foundation, so that future contributors have a stable reference point rather than rediscovering the same reasoning independently.

This RFC deliberately does not attempt to resolve open technical questions that have a distinct, separate mechanism to decide (how errors propagate, what primitive capsules guarantee, how abstractions version, and so on). Keeping those out of this document means this document's content will not go stale as implementation decisions are made elsewhere — a risk that materialized concretely during this RFC's own drafting, when an earlier version restated an error-handling question that had already been substantially addressed elsewhere.

Ongoing design tensions that apply continuously to syntax and grammar decisions — rather than being resolved once, elsewhere — remain part of this document, since there is no separate place where they would be decided independently of this philosophy.

## Guide-level explanation
Khayyam is evolving away from being a traditional programming language and toward becoming a system-modeling language. Most language designs begin by collecting useful features — OOP, generics, pattern matching, functional constructs, traits, reflection, meta-programming — and combining them into a coherent syntax. Khayyam follows a fundamentally different path: instead of asking "What features should a language provide?", it asks "What architectural principles should a long-lived system follow?" and then derives language constructs from those principles.

This RFC captures the philosophical layer of that derivation — the recurring principles observed across many separate design discussions. It intentionally stays at the level of *why* rather than *how*, wherever a distinct *how* has (or will have) a dedicated home elsewhere. The specific mechanisms (how errors propagate, how primitive types are specified, how abstractions version, how polymorphism compiles) are the concern of separate, focused RFCs, written once each design matures enough to be specified concretely.

The reader does not need to have read the canonical [Khayyam language specification](../Khayyam.md) to follow this document, though familiarity with Khayyam's core concepts — capsules, abstractions, methods, and Smart Compilation — will provide useful context.

## Reference-level explanation

### Khayyam Is Not Its Own Compiler or Runtime
Khayyam, as a sub-framework, defines a design space for expressing Memar's constraints in source form — explicit state, explicit error paths, no hidden control flow. It does not follow from this that Khayyam must also provide its own compiler or runtime as part of what Khayyam *is*.

Building a compiler or runtime is a separate concern with its own design space, its own trade-offs, and its own failure modes. Folding it into Khayyam's own scope creates a well-documented failure pattern seen across many language projects: once a language project owns compiler and runtime implementation, every new developer-convenience request becomes pressure to add syntax, special cases, or built-in magic to make that convenience possible — because the team that controls the language spec is the same team that feels the pain of not having the convenience. Over time this erodes the "no hidden control flow, no implicit behavior" principle
Khayyam exists to protect, from the inside, by the people most invested in protecting it.

Keeping compiler and runtime implementation outside Khayyam's own scope as separate systems that consume Khayyam's specification, built by teams whose incentives are implementation correctness and performance rather than syntax convenience — is therefore not an incidental scoping choice. It is a structural safeguard against the specific failure mode described above.

This has a direct consequence for how Khayyam's own RFCs should be scoped: a proposal to add syntax "to make the compiler's job easier" or "because other languages do it this way" is, by this principle, a signal to examine the proposal skeptically rather than a reason to adopt it.

(This is a draft note for further discussion — the precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" still needs worked examples before this can be a settled RFC section.)

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

This suggests that discussions about generics should not begin with "How do we support generic syntax?" but rather "Why does this requirement exist in the first place?". The specific compilation mechanism that follows from this reasoning — how Khayyam's inclusion-based approach actually works and compiles — is the subject of its own dedicated RFC, not this document.

### Self-Documenting Code and Naming
In most languages, naming is a style preference. In Khayyam, it is enforced by the language itself: magic numbers are forbidden, primitives must be wrapped in named capsules (`W32`, not `int`), and generic containers are replaced by domain-specific names (`UserRegistry`, not `Map<ID, User>`).

This means that in a Khayyam codebase, it is structurally impossible to write opaque code even if a developer tries. The language grammar makes the architect's intent visible at every call site.

This is not a one-time mechanism to be decided and then documented elsewhere — it is an ongoing tension that recurs every time a new naming rule, keyword, or grammar constraint is considered. Because of that, it stays part of this document rather than being extracted into a dedicated topic RFC.

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

## Discussion

### Naming Conventions
Not applicable at the RFC-wide level. Each topic section above that introduces naming implications includes its own Suggested Naming Conventions or Naming Discussion where relevant.

### Drawbacks
The principles documented here are, by nature, interpretive rather than settled fact — they describe a consistent direction observed across many design discussions, not a technical conclusion that can be independently verified. A reader could mistake this philosophical framing for a finalized technical decision on any given topic; it is not. Conversely, the absence of a topic from this document does not imply it is unresolved elsewhere — it may simply belong in a different, more focused RFC. Both risks are mitigated by the project's general documentation-navigation guidance rather than by anything specific to this document.

### Rationale and alternatives
- **Keep philosophy and technical decisions combined in a single document (original approach, revised)**: earlier drafts of this RFC combined both layers, reasoning that the topics are interconnected. In practice, this created a duplication risk: technical claims restated here could drift out of sync with the dedicated RFCs where those same mechanisms are actually decided. This risk materialized concretely — an earlier draft's discussion of error propagation restated a question already substantially addressed by the existing error-abstraction RFC and by the canonical specification's own method-return pattern. The current approach keeps here only what is either (a) pure philosophy with no separate technical mechanism, or (b) an ongoing design tension with no single external decision point (naming, syntactic atomicity). Topics with a distinct, separable mechanism move to their own RFCs as they are written, and are not individually cross-referenced from this document — readers are directed to the project's general documentation-navigation guidance instead.
- **Wait until implementation evidence exists before documenting (rejected)**: documenting the philosophical principles now still creates a shared reference point, even if specific technical mechanisms are decided later — and because this document no longer makes technical claims about those separable mechanisms, this reasoning holds more cleanly than it did in the original, mixed-scope version.

### Prior art
Rust's design philosophy documents and Go's "Go Proverbs" serve a similar purpose of capturing design intent alongside technical specification. This RFC differs by keeping the philosophical/ongoing-tension layer separate from decidable technical specification entirely, rather than combining both.

### Unresolved questions
1. As the technical topics implied by this philosophy (error propagation, primitive capsule contracts, abstraction versioning, inclusion-based polymorphism, and others) get their own dedicated RFCs, does this document need to change at all, or does it remain stable as a pure philosophy reference?
2. How frequently should this document be revisited to confirm the principles it describes still hold as more of Khayyam is implemented?

### Future possibilities
As Khayyam's technical RFCs are written for the topics this philosophy implies, this document is expected to remain largely unchanged — its scope is philosophy and ongoing design tensions, not one-time mechanism decisions, so it does not need to track the completion status of those RFCs individually. This RFC can move toward Final once its own scope is judged complete, independent of how many companion technical RFCs still remain to be written.

## Change Rationale
