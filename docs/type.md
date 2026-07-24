---
Title: "Type"
Status: Draft
Start Date: 2026-07-19
RFC Number: 495685
Applied to: []
Citations:
    - Title: "Modeling"
      URI: "./modeling.md"
      Relation: Depends_on
      Reason: "Type is the result of correct modeling. The concept of Type cannot be understood or defined independently from the modeling process that identifies what should exist as a Type. Modeling establishes that abstractions are justified by independent responsibilities, not by data — and Type is the construct that carries that justification into the language."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: Reference
      Reason: "Specifies how Capsule and Method manifest in Khayyam — Sovereign Encapsulation, method invocation rules, and the rejection of tuples and consumer-side mutability keywords."
    - Title: "Abstraction in Khayyam"
      URI: "./khayyam-abstraction.md"
      Relation: Reference
      Reason: "Specifies how Abstraction manifests in Khayyam — pure contracts, implicit structural satisfaction, rejection of default implementations, and abstraction composition."
    - Title: "Inheritance in Khayyam"
      URI: "./khayyam-inheritance.md"
      Relation: Reference
      Reason: "Specifies that inheritance in Khayyam is a relationship between abstractions, not between capsules — behavior transfer is rejected, abstraction extension is supported."
    - Title: "Polymorphism in Khayyam"
      URI: "./khayyam-polymorphism.md"
      Relation: Reference
      Reason: "Classifies the polymorphism forms Khayyam supports through abstraction conformance — inclusion, parametric, and ad-hoc — and the rejection of generic syntax."
    - Title: "Khayyam Design Philosophy"
      URI: "./khayyam.md"
      Relation: Reference
      Reason: "Documents the recurring principles (Behavior Over Type Identity, Domain Modeling, Syntactic Atomicity) that the Type concept in Khayyam is an instance of."
    - Title: "Khayyam - Programming Language"
      URI: "../Khayyam.md"
      Relation: Reference
      Reason: "The canonical specification of Khayyam's type subtypes and their syntax."
    - Title: "RFC Template Specification"
      URI: "./rfc-template.md"
      Relation: Reference
      Reason: "This document follows the canonical RFC structure."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Authored initial reflections on Type as Semantic Entity and its relationship with Capsule and Abstraction", "Directed the philosophical framing: Type as an independent concept before its manifestation in Khayyam", "Identified Method as a type category and the absence of primitive types in Khayyam", "Corrected assumptions about primitive types and emphasized the independent-concept-first structure", "Critical review: identified Method-as-Type argument weakness, Scope justification gap, Type definition exclusivity concern, and DDD reference overhead"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Titles: ["Critical review"]
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "High"
    Tasks:
      - Works: ["Conducted cross-language and type-theoretic research", "Authored critical analysis and comparative sections", "Restructured the document to follow the RFC template", "Revised across multiple iterations: removed Primitive Types, added Method and Scope as type categories, separated independent Type concept from Khayyam manifestation, incorporated findings from companion RFCs"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Critical review of 4th revision: identified Method-as-Type argument weakness, Scope-as-Type justification gap, Type definition exclusivity risk, DDD reference overhead, premature bridging claim, and Type hierarchy resolution"]
        URI: ""
---

# Type

## Abstract
This RFC defines **Type** as a foundational modeling concept: a first-class semantic entity with an explicit identity and a defined contract. The definition is given independently of any specific language — it describes what Type *means* as a modeling decision, not what a compiler requires. A Type represents a named concept in the domain model; its identity is nominal and its purpose is semantic, not structural. This understanding of Type has found concrete expression in the Khayyam programming language, where every type — whether it owns state (Capsule), defines callable behavior (Method), specifies a contract (Abstraction), or delimits a semantic boundary (Scope) — participates in a unified type model derived from these principles. See [Guide](#how-to-identify-a-type-in-the-domain) for a practical decision framework.

## Introduction

### Motivation
In most programming languages, the word "type" serves the compiler's need to classify data: how many bytes, what layout, which operations are valid. This instrumental view is necessary for machine execution but insufficient for system modeling. When type is reduced to an implementation artifact, the result is what Evans calls the "Anemic Domain Model" — data structures stripped of behavioral meaning, with logic scattered across service layers that the type system cannot verify or enforce.

The concept of Type, before it becomes a language construct, is a modeling concept. It answers the question: "What things in this domain have independent identity and meaning?" This question exists regardless of whether a compiler is present. A domain modeler deciding that "Contract" is a distinct concept from "Document" is making a Type decision — the compiler merely records it.

This document defines Type at that modeling level first, then shows how Khayyam's type system is a concrete realization of these principles. The separation is deliberate: the definition should remain valid even if Khayyam's syntax changes, because it describes a concept, not a syntax.

### Type Beyond Programming Languages
Type, as defined in this RFC, is not introduced by programming languages. A language is one mechanism for expressing Types, not the reason Types exist. A Type exists wherever a system distinguishes one meaningful category of entity from another — a domain model, a business process, a protocol, or an organizational structure can contain Types even where no source code exists to represent them. Khayyam does not create the existence of Types; it provides a language for expressing a distinction that already holds at the modeling level.

In practice, the correlation between Type and Khayyam is strong, because Khayyam is currently the first and most concrete realization of these principles — most readers will encounter Type through Khayyam's syntax before encountering it as an abstract modeling concept. That correlation is a fact about where this RFC's principles are first put into practice; it is not a claim about where Type originates. The [Definition of Type](#definition-of-type) below is written to hold independently of Khayyam, and [Manifestation in Khayyam](#manifestation-in-khayyam) exists as a separate section specifically to keep that boundary visible: principles first, language second.

### Methodology
This document was developed through analysis of existing RFCs in the Memar project — particularly Modeling, Encapsulation, Abstraction, Inheritance, and Polymorphism — to extract the common concept that underlies them all. The analysis attempted to avoid presuppositions about what Type should be, instead deriving its properties from the principles and decisions already established across these companion documents. Where a claim about Type depends on a specific decision already recorded elsewhere, that dependency is made explicit through Citations rather than restated. Where the evidence from companion documents was insufficient to justify a definitive claim, the question is recorded as unresolved rather than assumed.

## Explanation

### How to identify a Type in the domain
Not every concept in a domain should become a Type. The following framework provides practical guidance for the modeling decision.

**Should be a Type** when the concept:
- Has independent identity in the domain — domain experts name and reason about it separately.
- Has its own lifecycle — it can be defined, composed, specialized, and evolved independently.
- Has rules or invariants that belong to it specifically.
- Participates in relationships where it is an endpoint with its own identity.

**Should NOT be a Type** when the concept fails these criteria — see [What Is Not a Type](#what-is-not-a-type) for the detailed catalog of exclusions and examples.

**The gray zone**: Some concepts fall where reasonable modelers disagree. The modeling RFC addresses this directly: an abstraction is justified by an autonomous responsibility and lifecycle, not by the existence of data. A concept may justify an independent Type only when it represents an autonomous concern with its own rules, behavior, lifecycle, validation requirements, or architectural responsibilities. The mere ability to assign a name to something does not automatically justify introducing a separate Type. This criterion — derived from modeling.md's "Concept Existence vs. Model Existence" principle — provides the boundary: the gray zone is resolved by asking not "can we name this?" but "does this carry an independent responsibility?"

**A note on lifecycle**: The term "lifecycle" in this framework does not exclusively mean runtime creation and destruction (create, persist, destroy). For some Type categories — particularly Method — lifecycle encompasses the stages of definition, composition, specialization, and execution. A Method is defined with a signature, composed with other Methods or Types, specialized through receiver attachment, and executed when invoked. These stages constitute a lifecycle, even though a Method is not "created" or "destroyed" in the same way a Capsule instance is. The framework applies across categories when lifecycle is understood at this level of generality.

**A note on independent identity**: "Independent identity" is a claim about meaning, not about unconstrained existence, and the two are easily conflated. A concept has independent identity when it is named and reasoned about on its own terms — not when it can exist free of any containing context. A parameter has an identity distinct from the Method that declares it (a `Person` parameter is still recognized and reasoned about as `Person`), even though the parameter cannot exist outside that Method's signature. The same reasoning applies to any Type category whose current usage places it inside another construct: containment constrains where the concept may appear, not what the concept means. This distinction matters when applying the framework to categories such as Scope — see [Scope](#scope--type-as-semantic-boundary).

#### Discussion
##### Drawbacks
Any decision framework risks false precision. The responsibility-based criterion helps, but responsibility itself can be a matter of perspective — what looks like an independent responsibility to one modeler may look like a derived view to another. The lifecycle criterion also requires careful interpretation: if lifecycle is broadened to include definition and composition stages, the risk is that nearly every named artifact can be argued to have a "lifecycle," weakening the criterion's discriminating power.

##### Rationale and alternatives
- **No framework, rely on intuition (rejected)**: Without guidance, the tendency is to over-type or under-type without consistency.
- **A strict checklist with binary answers (rejected)**: Domain modeling is not binary. The responsibility criterion reduces the gray zone but does not eliminate it — that is a feature, not a flaw.

### Definition of Type
A **Type** is a first-class modeled entity with an explicit identity and a defined contract.

**First-class** means Types are named, referable, and composable — they participate in the model as entities that can be passed, referenced, and related, not merely as internal classifications.

**Modeled entity** means a Type exists because of a modeling decision, not because an implementation requires a data classification. The modeling decision identifies something in the domain that has independent identity and meaning. This does not mean every Type must correspond to a physical object — `Order` is a Type even though orders are administrative constructs — but it must correspond to a concept that domain participants recognize, name, and reason about.

**Explicit identity** means a Type has a name and a boundary that distinguish it from other Types, even those with similar structure. This is a nominal position: two Types with identical structure but different names represent different concepts. The implications of this choice are examined in [Type Identity](#type-identity).

**Defined contract** means a Type specifies what it guarantees — its operations, its rules, its valid states, and its relationships — without necessarily specifying how those guarantees are realized. The contract is the interface between the Type's semantic identity and its concrete manifestations.

A Type may contain:

- **Identity**: The name and boundary that distinguish this Type from others.
- **Behavior**: Operations the Type supports, defined by their semantics.
- **Rules**: Constraints, invariants, and behavioral guards. See [Type and Rules](#type-and-rules).
- **Relations**: Connections to other Types. Whether a given Relation itself warrants becoming a Type is a modeling-layer decision made using the same criteria as any other Type — see [Type and Relations](#type-and-relations).
- **Constraints**: Restrictions on valid values or relationships across instances.
- **Documentation**: Knowledge artifacts that support understanding.

#### What Is Not a Type
The definition above establishes the inclusive boundary of Type — what qualifies. An equally important function is the exclusive boundary: what does *not* qualify, even though it may be named, useful, or present in the domain model. This section is the detailed counterpart to the negative criteria introduced in [How to identify a Type](#how-to-identify-a-type-in-the-domain) — it is not a separate set of rules, but the same boundary worked out through concrete categories and examples.

The following are **not** Types:

- **Attributes and values**: A person's age, a product's price, an order's status — these are properties that belong to a Type, not Types in their own right. They derive their meaning from the Type they belong to, and they have no independent identity or contract. This holds unless the domain model explicitly elevates one of these to an independent concern — for example, `Money` may be a Type with its own rules (rounding, currency conversion) even though it functions as a value in many contexts.

- **Implementation mechanisms**: Garbage collection strategies, memory layouts, dispatch tables, serialization formats — these are how Types are realized, not Types themselves. They serve the implementation, not the domain model.

- **Runtime infrastructure**: Threads, sockets, file handles, message queues — these are platform artifacts that a Type may reference or wrap, but they are not Types unless the domain model gives them independent identity and contract. A `Connection` capsule that wraps a socket with domain-specific rules is a Type; the raw socket handle is not.

- **Organizational structures**: Modules, packages, namespaces, directories — these organize Types but are not themselves Types. They are grouping mechanisms that exist for navigation and access control, not for domain modeling.

- **Transient computational states**: Loop counters, intermediate calculation results, temporary buffers — these exist during computation but carry no domain meaning. They are artifacts of execution, not of modeling.

The exclusive boundary matters because Type is a foundational concept, but not every named artifact automatically becomes a Type. The expansion of the Type category should remain conservative: a concept should be admitted as a Type only when the modeling justification — independent identity, autonomous responsibility, defined contract — is clear. Admitting too many concepts as Types dilutes the category, making it progressively harder to distinguish what is architecturally significant from what is merely named. The history of Object-Oriented Programming provides a cautionary parallel: the concept of "Object" once had a clear meaning, but was gradually overloaded to encompass data, behavior, identity, namespace, module, service, and factory — until it became so broad that it lost discriminating power. The Type concept should not follow that trajectory.

#### Discussion
##### Drawbacks
Defining Type as "first-class modeled entity" sets an expectation that a type system can verify and enforce modeling-level properties. If "modeled entity" is merely a naming convention — if the type system treats semantically distinct Types as interchangeable because they share structure — then the claim is aspirational. Any language claiming semantic types must ensure the type system can observe and enforce the distinction.

##### Rationale and alternatives
- **Define Type structurally (rejected)**: A structural definition fails to capture the modeling-level distinction. Two concepts with the same structure are not necessarily the same concept.
- **Define Type as a formal type-theoretic construct (considered, deferred)**: Martin-Löf Type Theory defines types through introduction, elimination, and computation rules. This is rigorous but may be too formal for the current stage. A future revision could strengthen the definition toward this formalism.

##### Prior art
Martin-Löf's intuitionistic type theory treats types as meaningful propositions. OWL's named classes carry semantic identity beyond their property definitions. Neither of these fully aligns with the position taken here — MLTT is more formal but at a different abstraction level; OWL is declarative without behavioral semantics.

### Type Identity
A Type's identity is **nominal** — it derives from the Type's declared name within a bounded context, not from its structure.

Two Types with identical structure but different names are different Types because they represent different concepts. `Age` and `Height` may both be represented as integers, but they are different Types because they mean different things.

Conversely, two Types with different structures but the same name in the same bounded context represent a modeling conflict, not two valid Types. The name, within a context, uniquely identifies the concept.

**Contextual scoping**: The concept "Customer" in a billing context is not the same concept as "Customer" in a shipping context, even though they share a name. A type system must provide a mechanism — modules, namespaces, or explicit context declarations — to scope Type identity.

**The nominal enforcement requirement**: If `Age` and `Height` are nominally distinct Types, the type system must prevent their conflation — you cannot pass an `Age` where a `Height` is expected, even though both share the same representation. If the type system cannot observe this distinction, nominal identity is merely a naming convention, not a semantic property.

**Interaction with structural satisfaction**: In Khayyam, a Capsule satisfies an Abstraction through implicit structural satisfaction — if a Capsule implements all required methods with matching signatures, it conforms, without an explicit `impl` keyword. This introduces a tension with nominal identity at the Abstraction layer: a Capsule might accidentally satisfy an Abstraction it was never intended to implement (Go's well-known accidental satisfaction problem). Whether this risk warrants a mitigation mechanism is recorded as an open question in the Abstraction RFC. The Type Identity principle stated here — nominal identity within a context — applies at the declaration level; structural satisfaction operates at the conformance level. The two are not contradictory, but their interaction requires careful design.

#### Discussion
##### Drawbacks
Nominal typing creates composability barriers that structural typing avoids. If `Age` and `Height` are distinct, you cannot write a single `max(a, b)` for both without an explicit abstraction covering both. This is the cost of semantic precision — and its benefit: it prevents accidental conflation of distinct concepts.

##### Rationale and alternatives
- **Structural typing (rejected)**: Two Types with the same structure would be interchangeable, defeating semantic identity. TypeScript's structural typing demonstrates this: `interface Person { name: string }` and `interface Company { name: string }` are interchangeable, which is precisely the conflation this principle prevents.
- **Behavioral typing (considered, insufficient alone)**: Two Types are the same iff they support the same operations. But `Age` and `Height` both support arithmetic, yet should not be interchangeable. Behavioral typing alone is insufficient without nominal anchoring.

##### Unresolved questions
How does nominal identity interact with generic or parameterized types? If `Registry<T>` is a Type, is `Registry<Person>` the same concept as `Registry<Company>`? In nominal systems, each instantiation is a different type — this seems correct, but the implications for code reuse need exploration.

### Type vs Implementation Type
A programming language type is one possible representation of a modeling Type. They are not the same thing, and conflating them causes two distinct problems:

**The descent problem**: A single modeling Type may have multiple valid implementation representations. A `Person` Type might be stored as a row in a relational database, a document in a document store, or an object in memory. If the modeling Type is defined by its implementation, it cannot be represented differently in different contexts without losing its identity.

**The ascent problem**: A single implementation type may represent multiple modeling Types. An `int32` can represent an `Age`, a `Height`, a `Temperature`, or a `Quantity` — each of which is a different modeling Type. If the implementation type defines the modeling Type, these distinctions are lost.

The modeling Type is primary; the implementation type is secondary. The mapping from modeling Type to implementation type is a design decision, not an identity. However, this creates a gap that must be bridged: if the modeling Type exists at a different level, there must be a mechanism for mapping between them. This mechanism is not specified here — it is a concern of the language that realizes these principles.

### Categories of Type
The Type concept manifests through distinct categories that represent different semantic roles. These categories are not subtypes of each other — they are different ways a Type can fulfill its role in the domain model.

#### Type Categories Are Not a Hierarchy
The categories defined within the Type model should not be interpreted as an inheritance tree or taxonomic hierarchy.

A Capsule is not a specialization of an Abstraction. An Abstraction is not a specialization of a Method. A Method is not a specialization of a Scope. Each category exists because it fulfills a distinct semantic role within the language model.

Relationships between categories are expressed through participation, ownership, visibility, composition, satisfaction, or other semantic connections — not through parent-child classification.

This distinction is important because traditional programming languages often organize concepts into rigid hierarchies. The Type model instead treats categories as independent concepts connected through explicit semantic relationships.

Understanding a category should not require understanding its position in a hierarchy. Each category must remain meaningful and well-defined in isolation.

This principle — graph of semantic relationships, not inheritance hierarchy — extends beyond the Type model. It reflects a foundational modeling decision: concepts are connected through explicit semantic roles, not through taxonomic classification. This same principle is expected to apply across the broader Memar modeling framework and is likely to be reflected in companion documents such as `modeling.md` and `terminology.md`.

#### Capsule — Type with Owned State
A Capsule is a Type that owns state and the behavior that operates on it.

"Owned state" means the Capsule is responsible for the lifecycle and integrity of its data. It controls access to its state and ensures that all modifications preserve its rules. This is ownership in the semantic sense: the Capsule is the authoritative source of truth for the state it contains. In Khayyam, this is enforced through Sovereign Encapsulation — all internal fields are strictly private, and all interaction occurs via method invocation.

"Behavior" means the Capsule provides operations that reflect the Type's semantics. A `BankAccount` Capsule does not merely store a balance — it provides `deposit` and `withdraw` operations that enforce business rules. The behavior is part of the Type's contract, not an implementation detail.

#### Method — Type as Callable Behavior
A Method is a Type that represents executable behavior. It is not a separate concept from Type — it is a Type whose primary semantic role is to be callable.

This is a departure from most languages where functions are not types. In the Khayyam model, a method is a callable entity: it has an identity, a contract (its signature), and it participates in the type system like any other Type. A method can be attached to any Type — a Capsule, an Abstraction, or even another Method.

Methods are Types not because they contain executable code, but because they represent first-class semantic entities within the language model. Higher-level concepts such as rules, workflows, vouchers, policies, and campaigns are ultimately expressed through method structures and compositions. A `Voucher` rule that applies a discount to an invoice and adjusts a campaign balance is, at the level of the language, a Method (or composition of Methods) attached to the relevant Types. The Method category provides the fundamental semantic building block through which these higher-level domain concepts are realized.

This is what separates a Method from an ordinary expression or statement inside a method body: an expression has no existence outside the body that contains it, while a Method has its own signature, can be imported across files, attached to a receiver independently of where it was originally defined, and composed with other Methods as a named, referenceable unit. It is this independent, referenceable existence — not merely the presence of executable code — that qualifies Method as a Type category rather than an internal language mechanism.

The key implications:
- Methods can be imported, referenced, and composed like any other Type.
- A method's contract includes its receiver type, its efficacy (output) variables, and its impressible (input) variables.
- Methods without a `self` reference are type-level (static) behaviors; methods with `self` are instance-level behaviors. This distinction is governed by the presence of `self` in the signature, not by a separate keyword.
- Body-less methods serve two purposes: defining the required signature for an Abstraction (contract), or signaling FFI (the implementation will be provided externally during linking).
- A Method can carry other Methods — one method may compose or delegate to others, forming executable behavior trees.

**Method lifecycle**: A Method has a lifecycle that encompasses definition (signature declaration), composition (attachment to a receiver type and combination with other methods), specialization (override or extension in a satisfying capsule), and execution (invocation). This lifecycle is distinct from the instance lifecycle of a Capsule — a Method is not "created" or "destroyed" at runtime in the same sense — but it constitutes a genuine lifecycle nonetheless: the Method passes through identifiable stages that affect its identity and behavior within the type model.

The "Method as Type" position has consequences for the composition of categories: since methods are types, they are currently the primary mechanism through which capsules satisfy abstractions. An Abstraction specifies which methods must exist; a Capsule provides their implementations. The method itself, as a Type, is the unit of composition. Whether Methods are the *only* such mechanism, or whether other constructs (Relations, Protocols) may serve comparable bridging roles in the future, remains an open question. This is why the Inheritance RFC can state that "behavior transfer between capsules is rejected" while "abstraction extension (inheritance of requirements) is supported" — the method, as a Type, is the unit that connects the two categories as currently modeled.

#### Abstraction — Type as Contract
An Abstraction is a Type-level contract without owning state or behavior.

An Abstraction specifies what operations a Type must support, but not how those operations are implemented or what data they operate on. It defines pure intent. Methods that fulfill an Abstraction's contract are defined independently — they are separate Types, not embedded within the Abstraction.

An Abstraction can compose other Abstractions, building compound contracts from simpler ones. This is Khayyam's mechanism for inheritance between abstractions: when Abstraction B includes Abstraction A, B extends the set of requirements — no behavior is transferred, only requirements flow. This distinction between requirement extension and behavior transfer is fundamental.

Abstractions must use other Abstractions as their arguments and return types — not Capsules — preserving the contract-level abstraction boundary. This ensures that an Abstraction's contract is entirely implementation-agnostic.

Crucially, Abstractions do not contain predefined method bodies. They are pure contracts. Default implementations (as in Rust traits or Java `default` interface methods) are explicitly rejected — they blur the line between contract and implementation, and introduce implicit behavior routing that contradicts the principle of Explicit Behavior Ownership. This maintains a clean separation: Abstractions define *what*, Capsules define *how*, and Methods are currently the primary mechanism connecting them.

A Capsule satisfies an Abstraction through implicit structural satisfaction: if a Capsule implements all required methods with matching signatures, it conforms, without an explicit `impl` keyword. The compiler validates this at the point where the abstraction type is expected.

#### Scope — Type as Semantic Boundary
A Scope is a Type that delimits a semantic boundary within which names, relationships, ownership rules, and visibility constraints are established.

A Scope is not merely a syntactic block. It defines what is visible, what is accessible, what is owned, and what is isolated within its boundary — properties determined by the Scope's own naming rules, visibility rules, and entry/exit semantics, not by whatever construct currently contains it (see [A note on independent identity](#how-to-identify-a-type-in-the-domain)). Many higher-level constructs can be modeled as specialized forms of Scope rather than independent language primitives: a namespace, a module's visibility boundary, a package boundary, a transaction's isolation boundary, and a local algorithmic block (as used by `if`, `loop`, `goto`) are all instances of the same fundamental concept — a bounded region with its own naming, access, and composition rules.

Khayyam's current syntax places scopes inside method bodies to express algorithmic control flow, and its examples reflect that usage. This is a placement rule enforced at the language and tooling layer, not a defining property of Scope itself: nothing in the semantic-boundary definition above requires a Scope to be nested inside a Method, and namespace- or module-level boundaries are realizations of the same category that are not nested inside any Method. Where Khayyam's syntax permits or restricts Scope's placement is a language-design question for the Khayyam specification and its governing linters — see [Khayyam.md](../Khayyam.md) — not a claim this RFC makes about what a Scope is.

The decision to treat Scope as a Type category reflects the principle that language constructs which establish independent semantic boundaries deserve first-class treatment in the type model. If Scope were merely a compiler-level syntactic convenience with no semantic significance, it would not qualify as a Type. The fact that it governs visibility, ownership, composition, and isolation — all of which are semantic properties — justifies its inclusion.

#### The Relationships Between Categories
All four categories — Capsule, Method, Abstraction, Scope — are equally direct realizations of Type; none is nested inside another as a subtype. What connects them is a set of named, cross-cutting relations, not a shared ancestor:

| Relation | From → To | Nature |
|---|---|---|
| satisfies | Capsule → Abstraction | implicit structural conformance |
| attaches to | Method → Capsule / Abstraction / Method | receiver binding |
| extends | Abstraction → Abstraction | requirement inclusion, no behavior transfer |
| commonly used within | Scope → Method | current Khayyam usage pattern, not a containment requirement (see [Scope](#scope--type-as-semantic-boundary)) |

These categories share the foundational properties of Type — identity, contract, and composability — but differ in what they own and what role they play. The key relationships:

- **Method currently connects Capsule and Abstraction**: An Abstraction declares required methods; a Capsule provides their implementations. The method is the unit of composition — it is what Abstractions require and what Capsules provide. Whether this is the sole bridging mechanism, or whether other constructs may serve comparable roles in the future, remains open.
- **Capsule satisfies Abstraction**: Through implicit structural satisfaction — the Capsule implements all required methods with matching signatures.
- **Abstraction extends Abstraction**: Via inclusion, requirements flow without behavior transfer. This is inheritance in its correct sense.
- **Capsule never inherits from Capsule**: Behavior transfer between capsules is rejected. The alternative is explicit delegation — the developer writes a method on the host capsule that visibly forwards the call to an embedded instance.
- **Scope commonly appears within Method**: In current Khayyam usage, scopes structure execution and define semantic boundaries inside method bodies — a usage pattern, not a requirement of the Scope category itself.
- **Method can attach to any Type**: Not only Capsules — methods can be defined on Abstractions (defining the required signature) and on other Methods.

None of these categories is a subtype of another. They are different semantic roles fulfilled by the same foundational concept: Type.

#### Why Only Four Categories?
Not every concept that participates in the Type model earns its own category. A Type category is justified only when it represents a fundamental semantic role that cannot be expressed as a specialization, composition, or usage pattern of a category that already exists. Capsule (owns state), Method (callable behavior), Abstraction (pure contract), and Scope (semantic boundary) are currently considered to meet this bar — each governs a role none of the other three governs.

Concepts such as Rule, Relation, Protocol, Workflow, and Policy depend on Types, and some of them may themselves warrant becoming Types (see [How to identify a Type](#how-to-identify-a-type-in-the-domain)) — but they do not, at present, justify a distinct *category* within the Type model, because their behavior is currently expressible through composition of Capsule, Method, and Abstraction. The Rule/Voucher example in [Method as Type](#method--type-as-callable-behavior) illustrates this: a Voucher is not a fifth category, it is a composition of Methods attached to relevant Types.

This boundary is deliberately conservative, for the reason argued in [What Is Not a Type](#what-is-not-a-type): admitting a new category too readily risks the same dilution that made "Object" in OOP progressively meaningless. Should a future concept prove genuinely irreducible to the existing four roles, introducing a fifth category is not ruled out — but the burden of proof sits with demonstrating irreducibility, not with defending the current count.

#### Type Categories vs Language Keywords
Other languages introduce many more top-level constructs than Khayyam does — `struct`, `class`, `record`, `union`, `interface`, `trait`, `namespace`, `module`, `package`, `enum`, `concept`, among others. This is not evidence that Khayyam's model is incomplete; it reflects a different premise. The existence of a dedicated keyword in another language does not imply the existence of a distinct foundational concept. Several of the most common keywords above are, on inspection, specific realizations of a category this RFC already covers:

| Common keyword elsewhere | Typical role | Khayyam category |
|---|---|---|
| `struct`, `class`, `record`, `entity`, `value object` | owns state and behavior | Capsule |
| `interface`, `trait`, `contract`, `concept` | pure contract | Abstraction |
| `function`, `procedure`, `routine`, `handler` | callable behavior | Method |
| `namespace`, `module`, `package` | boundary of visibility, ownership, or isolation | Scope |

This mapping is not exhaustive and not a claim that every keyword in every language reduces cleanly to one of these four roles. A construct like `union`, for instance, is arguably closer to an implementation strategy for representing overlapping state than to a modeling role, and this RFC takes no position on it. The claim is narrower and specific to the rows above: where a construct's role is owning state, defining a pure contract, providing callable behavior, or establishing a visibility/ownership boundary, Khayyam expresses it through the corresponding Type category rather than through a dedicated keyword of its own.

#### Discussion
##### Drawbacks
Four categories increase the conceptual burden: developers must decide not only "should this be a Type?" but "what category?" The distinction is clear in principle but can be blurry in practice. Additionally, the "How to identify a Type" framework currently works well for Capsules and Abstractions — which clearly have independent identity and autonomous responsibility — but is less immediately intuitive for Method and Scope, whose inclusion as Type categories requires additional justification beyond the base criteria.

##### Rationale and alternatives
- **Unify Capsule and Abstraction (rejected)**: This loses the essential distinction between "owns state" and "defines contract." Scala's experience with stateful traits demonstrates the problems of unification.
- **Treat Method as a separate concept from Type (rejected)**: Methods *are* Types. Making them non-types would prevent them from being imported, composed, and referenced through the same mechanism — breaking the orthogonality of the type model. It would also remove the natural bridging unit between Abstractions and Capsules.
- **Treat Method as a kind of Capsule (considered, not chosen)**: A method is a "callable capsule" in spirit, but calling it a Capsule obscures the fundamental distinction: a Method's primary purpose is executability, not state ownership. The categories should reflect semantic role, not implementation similarity.
- **Treat Scope as a compiler construct, not a Type (considered, not chosen)**: If Scope were merely syntactic, it would not qualify. But Scope establishes semantic boundaries — visibility, ownership, composition, isolation — that are relevant to the type model. These properties justify its inclusion as a Type category.

##### Prior art
Rust's struct/trait distinction parallels Capsule/Abstraction, but Rust treats functions as separate from the type system. OCaml's structure/signature distinction is similar but also separates functions from types. Khayyam's "Method as Type" is a genuinely different position — closer to Smalltalk's "everything is an object" but with explicit type categories rather than a single uniform concept.

##### Unresolved questions
1. Does Method fundamentally represent a Type category, or is Method a behavior owned by another Type? The current model treats Method as a Type, and the "fundamental semantic building block" argument supports this position. However, alternative interpretations remain possible — for instance, a Method could be viewed as a behavioral facet of the Type it is attached to, rather than an independent entity. The question is recorded as unresolved because the current model's treatment of Method-as-Type, while well-motivated, has not yet been validated through implementation experience.
2. How does "Method as Type" affect compilation and dispatch? If a Method is a Type, does it have a runtime representation, or is it purely compile-time?

### Type and Modeling
Because Types represent semantic entities, defining a Type is a modeling decision rather than merely a programming decision.

A Type should correspond to a meaningful concept in the domain model, not simply to a convenient collection of data fields. Before defining Types, the modeler must identify the concepts, boundaries, identities, and relationships that exist in the modeled reality. A Type is the result of correct modeling, not a replacement for the modeling process. This document depends on the principles defined in `modeling.md`, especially the "Modeling Before Implementation" principle.

The modeling RFC establishes that the output of modeling is a set of abstractions, concerns, relationships, and supporting documents — not capsules. Capsules are implementation-level realizations. This means the modeling phase identifies Types at the Abstraction level first; the Capsule level comes later, during architecture and implementation. The Type concept spans both levels, but the modeling decision that justifies a Type's existence operates at the Abstraction level.

#### Discussion
##### Drawbacks
If every type definition requires a modeling decision, the cost of introducing types increases. For prototyping and exploration, this is a significant friction. A type system derived from modeling principles must provide mechanisms for gradual introduction — lightweight types that can be strengthened as the model matures — without requiring full modeling justification from the start.

### Type and Rules
A Type may own rules that define valid states and behaviors. However, the term "rules" covers several distinct concepts that should be separated:

**Type Invariants** are state properties that must hold for all valid instances of the Type. They can be checked by inspecting a single instance. Example: `balance >= 0`. These correspond to Eiffel's class invariants.

**Constraints** are relational properties that restrict valid values or relationships across multiple instances. They involve more than one instance. Example: "SSN is unique across all Persons." Constraints cannot be checked by inspecting a single instance — they require a broader context.

**Behavioral Rules** govern state transitions — what operations are valid given the current state. Example: "Cannot ship a cancelled Order." These are transition guards, not state properties. They correspond to Eiffel's preconditions and postconditions.

**Business Rules** are domain-specific policies that may vary across deployments, contexts, or time. Example: "Discount cannot exceed 50%." Business rules are often the most volatile category — they change when policies change.

Conflating these categories under a single "rules" concept creates ambiguity. Is "SSN is unique" a rule of the `Person` Type? It involves all Persons, not just one. Is "Discount cannot exceed 50%" a permanent part of the `Order` Type, or a configurable policy? Separating them makes the ownership, checking strategy, and volatility of each explicit.

What Eiffel's Design by Contract teaches: invariants are checked at class boundaries; runtime contract checking is the default because compile-time verification is undecidable in general; and the Liskov Substitution Principle creates a formal relationship between type hierarchies and rule hierarchies.

What dependent and refinement types teach: the strongest possible integration of rules and types dissolves the distinction entirely — a rule *is* a type. This is powerful but comes at high cognitive cost. Refinement types (LiquidHaskell) provide a practical middle ground limited to SMT-decidable predicates.

#### Discussion
##### Unresolved questions
1. Are rules checked at compile time or runtime? This is the most consequential implementation decision.
2. What happens when rules from different Types conflict?
3. Can business rules be configured without changing the Type's identity?
4. What is the relationship between rule hierarchies and type realization?

### Type and Relations
A Relation connects Types to one another, but it is not itself a fifth Type category alongside Capsule, Method, Abstraction, and Scope. A Relation presupposes the existence of the Types it connects — it cannot be defined without them — and so it operates one layer above the concern this document addresses: what qualifies as a Type, and what a Type is made of.

This matters because graph-based domain models — the tool Memar uses for domain discovery, where both Nodes and Edges may carry independent meaning — are *consumers* of Type at a higher modeling layer, not part of Type's own definition. An `Employment` relation between `Person` and `Company` may itself need to become a Type once it has properties like start/end dates or status, but that decision is made using the same criteria as any other Type (see [How to identify a Type](#how-to-identify-a-type-in-the-domain)); it does not require a separate "Relation" category to exist first.

#### Discussion
##### Future possibilities
Whether Relations warrant dedicated language-level treatment — endpoint ownership, first-class status conditions, directionality, arity — is deferred to a future companion RFC that can address it as a modeling-layer concern in its own right, informed by prior art such as Chen's Entity-Relationship model, RDF/OWL, property graph databases, and Alloy.

### Manifestation in Khayyam
The principles defined above — Type as semantic entity, nominal identity, four categories of Type, owned rules — have found concrete expression in the Khayyam programming language. This section documents that manifestation without repeating the companion RFCs; for details, see the Citations.

**No primitive types**: Khayyam does not have primitive types. Even values that other languages represent as `int`, `bool`, or `string` are wrapped in named capsules (`W32`, `Bool`, `String`). This is a direct consequence of the "Type as semantic entity" principle: if `Age` and `Height` are different Types, their representation must also be different Types, not shared primitives. This eliminates the ascent problem described in [Type vs Implementation Type](#type-vs-implementation-type) at the language level.

**The `tp` keyword**: In Khayyam, every type is declared with `tp`. The keyword is category-agnostic — `tp` declares a Type, and the subtype keyword (`cp`, `mt`, `ab`, `sc`) specifies its category. This reflects the foundational principle that Capsule, Method, Abstraction, and Scope are different realizations of the same concept: Type.

**Method as Type**: Khayyam's `mt` subtype makes methods first-class Types. A method can be imported, attached to any receiver type, and composed through the same mechanisms as Capsules and Abstractions. This is the "Method as callable Type" principle made concrete, and it has no direct precedent in mainstream languages — most treat functions as separate from the type system.

**Abstraction as pure contract**: Khayyam's `ab` subtype defines Abstractions without method bodies. Methods that fulfill an Abstraction's contract are defined independently as separate Types. Satisfaction is implicit and structural — no `impl` keyword. Default implementations are rejected. This maintains the clean separation: Abstractions define *what*, Capsules define *how*, Methods are currently the primary mechanism connecting them.

**Inheritance is between Abstractions**: When an Abstraction includes another Abstraction, requirements are extended — no behavior is transferred. Behavior transfer between Capsules is rejected; explicit delegation is the alternative. This placement of inheritance is a direct consequence of the Type category model: inheritance belongs to the contract layer, not the state layer.

**Behavior over type identity**: Polymorphism in Khayyam operates through abstraction conformance, not through generic type parameters. The question is "what capabilities are required?" not "what concrete type is this?" A method accepting an Abstraction type is, in effect, a universally quantified function over all Types satisfying that Abstraction. Smart Compilation handles the dispatch strategy transparently.

**Sovereign Encapsulation**: All internal fields of a Capsule are strictly private. All interaction occurs via method invocation. Mutability is an intrinsic property of the Capsule's own definition, never a consumer-side keyword. This is the Type principle that identity and contract are declared at the definition site and cannot be bypassed at the call site.

## Results
This document is still in Draft status. No real-world outcomes from applying this Type model have been observed yet. This section will be populated once the model has been implemented and used in at least one non-trivial project.

## Discussion

### Drawbacks
The most significant drawback is the gap between aspiration and specification. The claim that Types are "semantic entities" sets an expectation that the type system can verify semantic properties. Without a formal definition of "semantic identity" and without specifying the Capsule/Abstraction realization mechanism in full detail, the claim is philosophical rather than technical. This is acceptable for a Draft but must be addressed before Proposed status.

The second drawback is the absence of primitives. While eliminating primitives solves the ascent problem, it creates a bootstrapping challenge: what are the foundational Capsules that everything else builds on, and how are they defined without circularity? This is an implementation concern but it affects the Type model's coherence.

### Rationale and alternatives
- **Adopt a traditional type system and enforce modeling through conventions (rejected)**: This works when the team has strong discipline and fails when it does not. The goal is to make discipline enforceable.
- **Adopt a dependent type system (rejected for now)**: Too complex for the current stage. Refinement types may be added as a middle ground in future revisions.

### Prior art
- **Martin-Löf Type Theory**: Types as meaningful entities defined by formal rules. This document shares the aspiration but lacks MLTT's rigor.
- **Rust**: Struct/trait distinction parallels Capsule/Abstraction. Rust treats functions as separate from types; Khayyam does not.
- **Eiffel**: Design by Contract parallels rules owned by Types. Eiffel's runtime checking is the most mature implementation.
- **Alloy**: Relations as foundational entities. Alloy demonstrates that first-class relations are viable and powerful.
- **Smalltalk**: "Everything is an object" parallels "everything is a Type," but Smalltalk lacks explicit type categories.

Khayyam's contribution is not any single one of these ideas but their integration: a unified type model where Capsules, Methods, Abstractions, and Scopes are all Types; Methods are currently the primary mechanism connecting Capsules and Abstractions; inheritance is placed between Abstractions while behavior transfer between Capsules is rejected; and polymorphism operates through abstraction conformance rather than generic syntax — all derived from the principle that Type is a modeling decision, not a compiler convenience.

### Unresolved questions
1. **Formal semantics of "semantic identity"**: Proposed direction — nominal declaration + contract specification + contextual scoping. Needs rigorous definition.
2. **Multiple Abstraction satisfaction**: Can a Capsule satisfy multiple Abstractions? How are method name conflicts resolved?
3. **Rule checking**: Are rules checked at compile time or runtime? What are the decidability boundaries?
4. **Rule conflicts**: What happens when rules from different Types realized by the same Capsule conflict?
5. **Method as Type**: Does Method fundamentally represent a Type category, or is Method a behavior owned by another Type? The current model treats Method as a Type, supported by the "fundamental semantic building block" and "independent, referenceable existence" arguments — but alternative interpretations remain possible and the position has not yet been validated through implementation experience.
6. **Gradual typing**: How does a language enforcing "every type is a semantic entity" interoperate with systems that do not share this philosophy?
7. **Bootstrapping**: Without primitives, what are the foundational Capsules, and how are they defined without circularity?
8. **Method dispatch**: If a Method is a Type, does it have a runtime representation, or is it purely compile-time?
9. **Accidental satisfaction**: Implicit structural satisfaction (no `impl` keyword) risks accidental conformance. Whether this warrants a mitigation mechanism is recorded as an open question in the Abstraction RFC.

### Future possibilities
1. **Refinement types for invariants**: An SMT solver could check simple invariants at compile time.
2. **Formal specification of the satisfaction mechanism**: Once design decisions are made, the Capsule/Abstraction bridge could be specified formally.
3. **Gradual typing at boundaries**: A mechanism for converting between semantic Types and structural types at API boundaries.
4. **Rule analysis tooling**: Static analysis to verify invariants, detect rule conflicts, and identify over-constraining.
5. **A dedicated Relation RFC**: Addressing whether and how Relations gain independent status, endpoint ownership, directionality, and arity, as a modeling-layer concern built on top of — not inside — this Type definition.

## Change Rationale
- **Initial draft**: Established the foundational concepts of Type as Semantic Entity, Type and Modeling, Capsule and Abstraction as realizations of Type, Type and Rules, Type and Relations.
- **Second revision**: Restructured into the RFC template. Added Type Identity, Type vs Implementation Type, rule categories, Capsule/Abstraction bridge analysis, and unresolved questions based on cross-language research.
- **Third revision**: Corrected structural errors based on review feedback: removed Primitive Types (Khayyam has none), added Method as a Type category (mt), added Scope as a Type category (sc), repositioned the definition of Type as an independent concept before its manifestation in Khayyam, reduced overall length by consolidating repetitive comparative analysis, and aligned the category model with Khayyam's actual four-subtype structure (cp, mt, ab, sc).
- **Fourth revision**: Incorporated findings from the companion RFCs (Encapsulation, Abstraction, Inheritance, Polymorphism, Modeling). Added Citations to all companion RFCs. Resolved the Type Identity open question about structural satisfaction vs. nominal identity by referencing the Abstraction RFC's treatment of implicit structural satisfaction and accidental satisfaction risk. Added the relationship between inheritance and Type categories (inheritance between Abstractions, not Capsules). Added the modeling RFC's "Concept Existence vs. Model Existence" principle to the decision framework. Refined Methodology section to reflect the actual research approach.
- **Fifth revision**: Applied critical review from ChatGPT (GPT-5.5). Key changes: (1) Removed all references to DDD and Aggregate Root — these belong in companion RFCs, not in the Type definition. (2) Added "What Is Not a Type" section to establish the exclusive boundary of the Type definition, addressing the risk that an overly inclusive definition dilutes the concept. (3) Moved the Type hierarchy question from Unresolved to an official position: "Type Categories Are Not a Hierarchy" — categories are connected through semantic relationships, not taxonomic classification. (4) Strengthened the Scope category: Scope is a "semantic boundary" that defines visibility, ownership, composition, and isolation — not merely a syntactic block. (5) Improved the Method-as-Type argument: Methods are Types because they are fundamental semantic building blocks through which higher-level concepts (rules, vouchers, policies) are expressed, not merely because they have identity and contract. (6) Weakened the bridging claim: Methods are "currently the primary mechanism" connecting Capsules and Abstractions, not the definitive bridge. (7) Clarified Method lifecycle: it encompasses definition, composition, specialization, and execution — not runtime creation/destruction. (8) Added conservative expansion principle: the Type category should remain conservative, avoiding the OOP-style overloading that rendered "Object" meaningless. (9) Added Method-as-Type as an unresolved question to record that the position is well-motivated but not yet validated through implementation. (10) Removed the "Beyond DDD" subsection from Type and Modeling.
- **Sixth revision**: Applied critical review from Claude, cross-checked against `Khayyam.md`. Key changes: (1) Replaced the parent-child tree diagram under "The Relationships Between Categories" with a relation table, since the tree's visual shape contradicted the adjacent "Type Categories Are Not a Hierarchy" claim. (2) Resolved a direct contradiction in the Scope section: the claim that a Scope's "identity is derived from its containing Method" conflicted with the independent-identity criterion in "How to identify a Type." Scope's containment within a method body is now explicitly framed as a syntactic placement constraint, distinct from its independent semantic identity (naming, visibility, and control-flow boundary). (3) Reframed "Type and Relations": a Relation presupposes the Types it connects and therefore operates one layer above this document's concern (what qualifies as a Type). The section no longer argues for Relations as a candidate Type category at this level; it defers first-class-Relation questions (endpoint ownership, directionality, arity) to a future companion RFC, and the "Manifestation in Khayyam" section no longer lists first-class relations among the realized principles, since Khayyam does not currently manifest them. (4) Strengthened the Method-as-Type argument by adding the distinguishing property — independent, referenceable existence (signature, cross-file import, receiver-independent attachment, composition) — that separates a Method from an ordinary expression or statement, closing a circularity gap where the prior argument could equally apply to any executable construct. (5) Removed duplication between "How to identify a Type" and "What Is Not a Type": the former now points to the latter for the negative-criteria catalog instead of repeating it with different wording.
- **Seventh revision**: Applied a second round of critical review from ChatGPT (GPT-5.5), cross-examined and refined through discussion. Key changes: (1) Removed the placement-based justification for Scope entirely, rather than merely softening it: the claim that Scope "must" live inside a Method is now documented as Khayyam's current syntax/usage pattern (a language-layer concern, deferred to `Khayyam.md`), not a defining property argued in this RFC. (2) Added "A note on independent identity" to the identification framework, generalizing the fix beyond Scope: independent identity is a claim about meaning, not about existing free of any containing context — a parameter has identity distinct from its Method despite being confined to that Method's signature, and the same reasoning applies to any category whose current usage places it inside another construct. (3) Added "Why Only Four Categories?": a Type category is justified only when it represents a fundamental semantic role irreducible to a specialization, composition, or usage pattern of an existing category; Rule, Relation, Protocol, Workflow, and Policy depend on Types without currently justifying a distinct category. (4) Added "Type Categories vs Language Keywords": a mapping table showing that common keywords in other languages (`struct`/`class`/`record`, `interface`/`trait`, `function`/`procedure`, `namespace`/`module`/`package`) are typically realizations of Capsule, Abstraction, Method, or Scope respectively — the existence of a dedicated keyword elsewhere does not imply a distinct foundational concept. (5) Added "Type Beyond Programming Languages" to the Introduction: Type is not introduced by programming languages; a language is one mechanism for expressing Types, not their origin. The strong correlation between Type and Khayyam in this document reflects that Khayyam is currently the first concrete manifestation of these principles, not a claim that Type is a language feature.
