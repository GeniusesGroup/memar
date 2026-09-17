# Polymorphism in Khayyam Changelog

## Changelog

### Initial creation and container-content consolidation
- Time: 2026-07-11T00:00:00Z
- Type: Added
- Cited:
  - [Abstraction in Khayyam](./abstraction.md) — Extends: supplies the abstraction type and its mechanics; this document classifies the polymorphism it enables and the syntaxes Khayyam rejects.
  - [Protocol](../protocol.md) — Depends_on: defines Protocol as a pure declarative specification used to explain why abstractions carry no behavior.
  - [Type](../type.md) — Depends_on: the type model defines the concepts and categories on which polymorphism operates.
  - [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) — Depends_on: its requirement for a single visible behavior owner grounds the rejection of generic type-parameter syntax.
- Propagates to:
  - [Khayyam — Programming Language](./khayyam.md#abstraction): Done — the canonical Abstraction section reflects the abstraction mechanism on which this document builds.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Gemini](../../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — critically reviewed
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — researched and rewrote
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM, medium effort) — merged

#### What changed
- The polymorphism document was created, consolidating the former container/generics-elimination material (Gemini — drafted the original containers/generics-elimination material and its alternatives; Super Z — merged, preserving the former containers-without-generics document's detail in this document).
- The resulting specification defines abstraction conformance and extension, Smart Compilation dispatch, domain-specific containers, the rejection of generic syntax, overloading, and coercion, together with their rationale, prior art, and open questions.
- Abstraction-conformance polymorphism, and abstraction extension and subtyping, were defined (Omid Hekayati).
- The Strachey/Cardelli–Wegner taxonomy was researched, Khayyam mechanisms were mapped to it, and prior-art comparisons and open questions were developed (Claude).

#### Deliberation
- The domain-specific-container alternative was defined (Omid Hekayati).
- The anemic-domain-model argument against generic syntax was claimed (Omid Hekayati).
- The closed-versus-open type-parameter analysis was contributed (Claude).

---

### Migration to the current Explanation-facet structure
- Time: 2026-08-19T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: defines the current front matter, top-level body sections, and topic-first organization.
  - [Documentation — Changelog](../documentation-changelog.md) — Depends_on: defines this companion file as the home for migrated provenance and change history.
  - [How to make a new explanation document](../documentation-explanation.practice.md) — Reference: supplies the revision procedure applied in this migration.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- The base document was migrated from the retired `Summary` / `Guide-level explanation` / `Reference-level explanation` structure to `Abstract`, `Introduction`, `Explanation`, `Results`, and `Discussion`.
- Provenance moved out of front matter: historical citations, contributor information, and propagation tracking are preserved here instead; this companion changelog was created.
- The EBO prerequisite moved into Introduction as an explicit constraint.
- Global discussion categories nested under one `Discussion` section.
- The stale Variable-document anchor for explicit typing repaired.
- The detailed explanatory, analytical, prior-art, and open-question content remains intact.

#### Deliberation
- The same up-to-date documentation migration applied to the Variable document was requested (Omid Hekayati).

---

### Fix example naming and annotate dual-role call
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
Corrects `tp hash`/`tp salt` to `tp Hash`/`tp Salt` per the PascalCase convention and `UInt64`/`UInt32` to `W64`/`W32` per the `W`/`R` capsule naming in sibling documents (also `h.hash` → `h.Hash`). Annotates the `ConnectionList` example's `self.container.Add(conID, con) (con, err)` call where `con` occupies both roles — influencing in `(conID, con)` and influenced in `(con, err)` — as an exhibit of the open dual-role question in `khayyam-method.md`; no settled notation exists yet.

---

### Dispatch-reducibility dispute resolved from Structure Is Fixed by Definition
- Time: 2026-09-09T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — argued, rewrote

#### What changed
- The "Dynamic Dispatch Reducibility" topic is resolved in the affirmative for Memar from the base layer's own principle — Structure Is Fixed by Definition (type.md): dispatch may defer selection to runtime, but the candidate set and every candidate's implementation must already be spelled out in source (Explicit Behavior Ownership), and a genuinely runtime-only type selection — target set or implementation arriving while the system runs — would mint structure in execution, which the principle excludes outright.
- The topic title drops the "Under Immutable Infrastructure" suffix; the pending-finalization caveat is gone because the derivation no longer depends on the Draft protocol document. The runtime-logic-entry question is named without citation as a separate, convergent concern owned by the framework's protocol documents.
- The change is strictly a strengthening of grounding: the dispute had been held open pending the protocol document's dedicated session; it is now closed on grounds already adopted at the base layer.

---

### Second migration wave: Discussion retired; routed to changelog and handoff
- Time: 2026-09-11T08:29:10Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: the three-section skeleton and the Relevance-discipline routing this migration applies are defined by the Explanation facet's governing specification.
  - [Documentation — Handoff](../documentation-handoff.md) — Depends_on: any open work created by this migration follows the Handoff facet's specification.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.3) - applied

#### What changed
- The document-level `## Discussion` section was retired per the finalized method; no top-level Discussion remains in the body. Content was routed, never deleted.
- The four Unresolved questions and the three Future possibilities moved to the newly created paired [polymorphism.handoff.md](./polymorphism.handoff.md) as its Open Questions and Anticipated Work, respectively.
- The six Rationale and alternatives entries are preserved in this entry below under Considered and not done: five record the reasoning behind design decisions the body states as current design (parametric polymorphism through inclusion rather than type-parameter syntax; the rejection of function overloading and coercion; generics as a symptom of the behavior-ownership problem; the encapsulation/EBO argument against generic syntax), and one ("Alternative Considered: Zig-Style Comptime Duck Typing") is an explicitly considered-and-rejected alternative.
- The Prior art surveys are preserved in this entry below under Related work — except "Academic — Structural Subtyping as Parametric Polymorphism (Ghiotto et al., 2023)", which was dropped rather than copied: it is already graduated into the body's Relationship to Parametric Polymorphism, which names the paper and its result inline at the claim it supports.
- The five Drawbacks are preserved in this entry below under Drawbacks.
- Premise evidence stayed in the body, cited inline at the claims it supports: the rejection table's brief rationale summaries and the Ghiotto et al. citation were already inline and were left untouched. Two plain-text pointers to the retired section — "See Rationale section below" (rejection table) and "see Prior Art" (Relationship to Parametric Polymorphism) — were dropped in this same pass: the table cell's "Briefly:" summary and the inline Ghiotto et al. citation carry the substance, and the full records live in this entry.
- Links inside the migrated content were retargeted to resolve from this changelog's directory: the rationale's pointer to The Compiler's Role: Dispatch Strategy now links into [polymorphism.md](./polymorphism.md); the Explicit Behavior Ownership citation ([Type — Explicit Behavior Ownership](../type.md#explicit-behavior-ownership)) already resolved correctly from here and was kept unchanged. In the handoff, the Future-possibilities reference to "Unresolved Question 4" now links to the corresponding Open Question above it, and "documented in this document" now links to [polymorphism.md](./polymorphism.md).

#### Considered and not done (migrated from the retired document-level Rationale and alternatives)

##### Why Khayyam Achieves Parametric Polymorphism Through Inclusion Rather Than Type-Parameter Syntax
**The core argument:** Khayyam does not lack parametric polymorphism — it achieves the same universally-quantified code reuse through a different mechanism. When a method accepts an abstraction type, it is, in effect, parametric over all types satisfying that abstraction. The compiler's Smart Compilation strategy (see [The Compiler's Role: Dispatch Strategy](./polymorphism.md#the-compilers-role-dispatch-strategy)) determines the optimal dispatch mechanism (monomorphization or dynamic dispatch) from the dependency graph, without the developer needing to annotate type parameters, specify constraints, or manage variance.

Explicit type-parameter syntax (`<T>`) makes the developer explicitly manage these concerns. This is valuable when the type system is the primary mechanism for achieving polymorphism. But when a language already has a robust abstraction mechanism that the compiler can analyze for dispatch optimization, explicit type parameters become redundant syntax — they expose implementation details that the compiler can determine on its own, and they add grammar complexity for no gain in expressive power.

Khayyam's design philosophy is that the compiler should be intelligent enough to determine the optimal dispatch strategy from the dependency graph, without the developer having to annotate it. The abstraction type in the method signature is sufficient information for both type checking and optimization.

**What this costs:** The developer loses the ability to express type-level constraints that go beyond what an abstraction can specify (e.g., "this type must have a compile-time-known size" or "this type must be `Copy`-able"). If such constraints become necessary in specific domains, they would need to be expressed through additional abstractions (e.g., `tp StaticSized ab` with a method that returns the size at compile time), which is more verbose but consistent with the language's philosophy.

**Why explicit type carriers are often redundant**. Consider a BTree algorithm that needs to compare keys. What the algorithm actually requires is a behavioral contract — "I can compare keys" — not the identity of the key type itself.

In languages with generic syntax, this is commonly expressed as `BTree<K, V> where K: Ord`. However, the algorithm never uses the identity of `K`; it uses only the behavior guaranteed by `Ord`. The type parameter serves primarily as a carrier that associates the behavioral contract with a concrete type — a layer of indirection that adds syntactic overhead without contributing to the algorithm's logic.

Khayyam eliminates that carrier. The algorithm accepts an abstraction that defines comparison behavior, and any conforming capsule can participate. From the algorithm's perspective, the required information is fully expressed by the abstraction itself — no type parameter, no constraint clause, no variance annotation.

The compiler's Smart Compilation strategy can then apply equivalent optimization opportunities (for example, monomorphization when the reachable set of conforming capsules is closed, or dispatch strategies appropriate to open abstraction sets) without requiring explicit type-parameter syntax in the source code.

This distinction is central to Khayyam's design philosophy: algorithms should declare the behaviors they require, not the concrete type identities they happen to operate on. Generic syntax is one historical solution for expressing parametric reuse, but it conflates two different concerns: type generalization and behavior ownership. Khayyam keeps the first capability through abstraction conformance while rejecting the second consequence of generic syntax: moving ownership of domain behavior away from domain concepts.

##### Why No Function Overloading
Overloading creates a naming collision that must be resolved at every call site by the compiler. This resolution depends on the argument types, which means the same function name can refer to completely different code depending on context. This is the opposite of the explicit, linear execution model Khayyam strives for: the reader should be able to trace the code path without having to mentally resolve type-based dispatch for function names.

Abstraction conformance provides the same ergonomic benefit (one method name that works with multiple types) without the ambiguity: the method is defined once on the abstraction, and each conforming capsule provides its implementation. The dispatch is through the abstraction, not through name resolution.

##### Why No Coercion
Implicit type conversions are a form of hidden behavior. When an `Int32` is silently converted to an `Int64`, the developer may not be aware that a widening conversion occurred, which can mask bugs in numerical algorithms. In safety-critical and performance-critical code (Khayyam's target domain), this hidden behavior is unacceptable.

##### Generics as a Symptom, Not a Cause
Many arguments for and against generics treat generics themselves as the subject of debate. From Khayyam's perspective, generics are more accurately understood as a **symptom** of a deeper modeling problem: behavior ownership has already been separated from domain concepts before the question of generic syntax even arises.

Consider the typical path that leads to generic containers in a codebase:

1. A domain concept (e.g., "a collection of connections") is not modeled as its own first-class concept with its own identity, behavior, and invariants.
2. Instead, it is represented as a generic `List<Connection>` — a type-agnostic storage structure that happens to hold Connection values.
3. Domain logic (duplicate prevention, lifecycle rules, query methods) then has nowhere to live inside the type, so it migrates to external services, controllers, or utility functions.
4. The generic container is now entrenched, and the domain model is anemic.

In this sequence, the generic container is not the root cause — it is the mechanism by which an earlier modeling failure (failing to give "collection of connections" its own identity) becomes entrenched in code. The generic syntax made this path easy; but the decision to not model the concept as a first-class type preceded the syntax choice.

Generic syntax is one historical solution for expressing parametric reuse, but it conflates two different concerns: **type generalization** (a legitimate polymorphic capability) and **behavior ownership** (a modeling decision). Khayyam keeps the first capability through abstraction conformance while rejecting the second consequence of generic syntax: moving ownership of domain behavior away from domain concepts.

This reframing is important because it explains why adding generic syntax to Khayyam would be regressive even if the syntax itself were minimal and clean: the problem is not the angle brackets, it is the behavior-ownership structure that generic syntax imposes on every container, algorithm, and data structure that uses it.

##### Why Generic Syntax Breaks Encapsulation: The Anemic Domain Model and EBO Perspectives

Adding generic syntax (the mainstream default) was rejected because it structurally permits domain logic to live outside the type it concerns, which conflicts with Khayyam's encapsulation principle more directly than almost any other common language feature.

An additional principled foundation comes from the Explicit Behavior Ownership principle ([Type — Explicit Behavior Ownership](../type.md#explicit-behavior-ownership)). Generic type parameters introduce ownership ambiguity: a method such as `List<T>.Add(T item)` is defined in the generic template but appears on every parameterized instantiation (`List<Connection>`, `List<Service>`, etc.). The implementation is not visible at the point of use — it lives in the template, not in the concrete type's source. This violates EBO's visibility requirement: answering "where was this behavior defined?" when looking at `List<Connection>` requires navigating to a separate generic template and understanding parameter substitution. The domain-specific capsule approach (e.g., `ConnectionList` with its own explicitly defined methods) satisfies both encapsulation and EBO simultaneously.

##### Alternative Considered: Zig-Style Comptime Duck Typing

Zig's approach to polymorphism is radically minimalist: there is no abstraction or interface mechanism. Instead, functions take types as compile-time parameters, and the compiler checks at each instantiation whether the type supports the required operations. This is essentially C++-style template duck typing without the syntax.

While philosophically aligned with Khayyam's minimalism, this approach was rejected because:
1. It shifts the entire burden of polymorphism to the developer, who must write comptime logic for what should be a simple "accept any hasher" pattern.
2. Error messages for type mismatches occur at the instantiation site (inside the function body) rather than at the call site (where the wrong type is passed), making them harder to understand.
3. It provides no first-class abstraction type that can be used as a parameter type in method signatures — there is no way to express "this function accepts anything that behaves like a Reader" without making the entire function comptime-generic.

Khayyam's abstraction type provides a cleaner, more readable mechanism for the common case, while the compiler's Smart Compilation achieves the same zero-cost outcomes as Zig's comptime instantiation for cases where the concrete type is known.

#### Related work (from the retired Prior art)

##### Go — Interfaces (Inclusion) + Go 1.18 Generics (Limited Parametric)
Go is the closest analog to Khayyam's polymorphism model. Before Go 1.18, Go had only interface-based inclusion polymorphism — exactly what Khayyam provides. The Go team deliberately deferred generics for over a decade, arguing that interfaces were sufficient for most polymorphism needs.

In 2022, Go 1.18 introduced type parameters with interface constraints. The Go generics design document explicitly states: "Polymorphism in Go must fit smoothly into the surrounding language, without awkward special cases and without exposing implementation details." However, Go's generics have notable limitations: no generic methods on interfaces (only on concrete types), no specialization, and constraints must be expressed as interface types.

Khayyam's position is that Go 1.18 generics were added to solve a real problem (writing type-safe containers and algorithms) but introduced significant complexity for marginal benefit. The same code-reuse goals can be achieved through abstraction conformance + Smart Compilation, without the type-parameter syntax.

From the containers perspective, Khayyam's approach is closer in spirit to a strict "wrapper type per use case" discipline sometimes manually adopted in DDD-heavy codebases as a best practice, here made the only available path.

Go's experience also illustrates a broader pattern: when a language's base types and abstractions are introduced without sufficient behavioral contracts (e.g., `map` and `slice` in Go having no abstraction layer and no way to add domain-specific methods to them), developers eventually demand generic syntax as a workaround — not because they need parametric polymorphism per se, but because the existing types lack the abstraction surface needed for domain modeling. The pressure for generics in Go was, in part, a consequence of this initial abstraction gap. Generic syntax thus becomes a general-purpose communication channel between the developer and the compiler: when the language provides no other way to convey compile-time facts (constraints, optimization hints, element identity), type parameters become the default channel. Khayyam avoids this by ensuring that its base abstractions and capsule types carry their own behavioral contracts from the start.

##### Rust — Traits (Nominal Ad-hoc) + Generics (Parametric) + impl Blocks
Rust combines three polymorphism mechanisms: traits (ad-hoc, nominal), generics (parametric, with trait bounds), and `dyn Trait` objects (runtime subtype polymorphism). This is the most expressive polymorphism system in mainstream systems programming, but it comes at the cost of significant conceptual and syntactic complexity.

Khayyam deliberately avoids this combinatorial explosion. A single mechanism (abstraction conformance) with compiler-managed dispatch covers the same use cases, with less syntax surface area and fewer concepts for the developer to learn.

##### Haskell — Type Classes (Ad-hoc) + Parametric Polymorphism
Haskell's type system is parametric by default: every function is implicitly polymorphic unless constrained. Type classes provide ad-hoc polymorphism by defining behavior sets that types can instantiate. This is elegant and powerful but requires a sophisticated type system that is difficult to implement in a systems language targeting C-level performance.

Khayyam's approach is closer to Go's pragmatic simplicity than Haskell's theoretical elegance. The abstraction mechanism provides the same "define behavior, let types conform" pattern as type classes, but without the higher-kinded types, type inference engine, and associated complexity.

##### C++ — Templates (Unconstrained Parametric) + Virtual Functions (Subtype)
C++ provides two completely independent polymorphism mechanisms: templates (compile-time, unconstrained, duck-typed) and virtual functions (runtime, class-hierarchy-based). The C++ approach is the most flexible but also the most error-prone: template errors are notoriously hard to read, and the interaction between templates and virtual functions creates complex edge cases.

Khayyam's Smart Compilation can be seen as a unification of these two mechanisms: the compiler chooses between compile-time inlining (like template instantiation) and runtime dispatch (like virtual functions) based on what it can prove, without the developer managing two separate systems.

##### Mainstream Languages — Generics as the Default
Statically typed mainstream languages (Java, C#, Rust, Go since 1.18) all provide generics as a core mechanism for type-safe containers. Khayyam's approach is the deliberate exception, grounded in the argument that generic containers structurally encourage the Anemic Domain Model by providing type-agnostic containers that have no room for domain-specific behavior. The domain-specific capsule pattern is not a limitation of Khayyam's type system — it is an expression of Khayyam's encapsulation philosophy applied to collections.

#### Drawbacks (from the retired body Discussion)

##### 1. No Way to Constrain by Data Shape
In languages with explicit type-parameter syntax, a generic function can constrain its type parameter by both behavior (trait bounds) and data shape (e.g., "must have a `length` field"). In Khayyam, abstractions only constrain behavior (method signatures), not data layout. If a function needs to work with any type that has a specific internal structure, there is no way to express this constraint without defining an abstraction with a method that exposes that structure. This is not a limitation of Khayyam's parametric polymorphism per se — it is a property of behavior-based abstraction that holds regardless of whether the parametric polymorphism is expressed via `<T>` syntax or via abstraction conformance.

This is generally considered acceptable in systems programming — behavior-based constraints are more robust than structure-based ones because they decouple the consumer from the producer's internal representation. However, it can feel limiting in scenarios where data-shape polymorphism is the natural fit (e.g., generic serialization that needs to inspect field names).

##### 2. No Function Overloading for Ergonomic APIs
Languages like C++, Java, and Rust (via trait implementations) allow the same function name to be used with different parameter types. In Khayyam, each method has exactly one signature. This means developers must use distinct names for conceptually similar operations on different types (e.g., `AddInt`, `AddFloat` instead of a single overloaded `Add`).

In practice, this is mitigated by Khayyam's abstraction mechanism: if the operation is truly polymorphic, it should be expressed through an abstraction (e.g., `tp Adder ab` with `tp Add mt (self Adder) (other Adder) (result Adder)`). The need for overloading typically arises in contexts where the types share no common abstraction — which is often a sign that the overloading is being used as a convenience shortcut rather than a principled abstraction.

##### 3. Discoverability of Polymorphic Behavior
Without generic syntax, discovering that a method is polymorphic (i.e., that it accepts an abstraction type and can work with multiple concrete types) requires reading the method's parameter types. There is no syntactic marker like `<T>` that immediately signals "this is a generic function." This is a minor ergonomic cost, partially addressed by IDE tooling and documentation conventions.

##### 4. Potential for Ambiguity in Complex Dispatch Scenarios
In rare cases involving multiple levels of abstraction extension (e.g., `A` includes `B` includes `C`, and a capsule satisfies `A`), the compiler's dispatch logic must correctly resolve which method implementation to use, especially when method names collide across the abstraction hierarchy. This is a well-studied problem in type theory (diamond inheritance, linearization) and is not unique to Khayyam, but it needs explicit compiler behavior documentation.

##### 5. Engineering Cost of Domain-Specific Containers
The cost of writing an intermediate domain-specific capsule for every container usage is real, ongoing engineering effort, even for cases that would otherwise be a single line of generic syntax (`List<Connection> connections;`) in another language. This is reframed in this document as "a fundamental investment in Clean Architecture," but it is still a genuine, non-trivial cost paid on every container use, not just complex ones.

This cost is partially mitigated by two factors. First, Khayyam's ecosystem includes scaffolding tooling (the Memar framework) that can generate domain-specific container capsules from a declaration, reducing the manual effort to specifying the domain's validation rules and query methods rather than boilerplate container logic. Second, the domain-specific capsule does more than a generic container — it carries domain invariants and provides domain-meaningful APIs — so the investment yields returns in code quality that generic containers cannot provide.

---

### Abstraction-relation direction recorded from the vr-ab review session
- Time: 2026-09-16T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — ruled

#### What changed
- The Motivation's consistency bullet now states the ruling on the dependency's direction: Polymorphism *uses* Abstraction — an abstraction can exist with no polymorphic use — and this document neither completes nor specializes Abstraction.
- The initial-draft entry's `Extends` Cited label is left untouched as the historical record of that document's pre-ruling front matter; the relation was reframed to references/uses by ruling, not retroactively rewritten.

#### Deliberation
- The ruling — Polymorphism is not a subset or perfection of Abstraction, and the citation must read "references/uses" — was given in the vr-ab review session but never reached this document; recorded here when the session's chat file was pruned from `chats-context/` (Omid Hekayati — ruled).
